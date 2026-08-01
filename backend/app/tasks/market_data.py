"""Market data background tasks."""

import asyncio
from datetime import datetime, timedelta, timezone
from typing import List

from celery import shared_task
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.session import get_db_context
from app.db.models import MarketData, User
from shared.trading_academy.data_fetchers.binance import BinanceFetcher
from shared.trading_academy.data_fetchers.coingecko import CoinGeckoFetcher


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def update_symbol_data(self, symbol: str, timeframe: str = "1h", source: str = "binance") -> dict:
    """Update market data for a single symbol."""
    try:
        # Run async function in sync context
        return asyncio.run(_update_symbol_data_async(symbol, timeframe, source))
    except Exception as exc:
        raise self.retry(exc=exc)


async def _update_symbol_data_async(symbol: str, timeframe: str, source: str) -> dict:
    """Async implementation of symbol data update."""
    # Initialize fetcher
    if source == "binance":
        fetcher = BinanceFetcher(
            api_key=settings.BINANCE_API_KEY,
            api_secret=settings.BINANCE_API_SECRET,
        )
    elif source == "coingecko":
        fetcher = CoinGeckoFetcher(api_key=settings.COINGECKO_API_KEY)
    else:
        raise ValueError(f"Unknown source: {source}")

    async with fetcher:
        # Get latest timestamp in DB
        async with get_db_context() as db:
            result = await db.execute(
                select(func.max(MarketData.timestamp)).where(
                    (MarketData.symbol == symbol) &
                    (MarketData.timeframe == timeframe) &
                    (MarketData.source == source)
                )
            )
            latest_ts = result.scalar()

        # Determine start time
        if latest_ts:
            start = latest_ts + timedelta(minutes=1)
        else:
            # Default to last 30 days
            start = datetime.now(timezone.utc) - timedelta(days=30)

        # Fetch new data
        end = datetime.now(timezone.utc)
        df = await fetcher.fetch_ohlcv_async(symbol, timeframe, start, end)

        if df.empty:
            return {"symbol": symbol, "timeframe": timeframe, "source": source, "inserted": 0}

        # Insert into database
        async with get_db_context() as db:
            inserted = 0
            for _, row in df.iterrows():
                # Check for duplicates
                result = await db.execute(
                    select(MarketData).where(
                        (MarketData.symbol == symbol) &
                        (MarketData.timeframe == timeframe) &
                        (MarketData.timestamp == row["timestamp"]) &
                        (MarketData.source == source)
                    )
                )
                if not result.scalar_one_or_none():
                    market_data = MarketData(
                        symbol=symbol,
                        timeframe=timeframe,
                        timestamp=row["timestamp"],
                        open=row["open"],
                        high=row["high"],
                        low=row["low"],
                        close=row["close"],
                        volume=row["volume"],
                        source=source,
                    )
                    db.add(market_data)
                    inserted += 1

            await db.commit()

        return {
            "symbol": symbol,
            "timeframe": timeframe,
            "source": source,
            "inserted": inserted,
            "latest_timestamp": df["timestamp"].max().isoformat() if not df.empty else None,
        }


@shared_task
def update_all_symbols(timeframe: str = "1h", sources: List[str] = None) -> dict:
    """Update market data for all tracked symbols."""
    if sources is None:
        sources = ["binance", "coingecko"]

    # Major crypto symbols to track
    symbols = [
        "BTC/USDT", "ETH/USDT", "BNB/USDT", "SOL/USDT", "ADA/USDT",
        "XRP/USDT", "DOT/USDT", "DOGE/USDT", "AVAX/USDT", "MATIC/USDT",
        "LINK/USDT", "UNI/USDT", "LTC/USDT", "BCH/USDT", "ATOM/USDT",
    ]

    results = []
    for source in sources:
        for symbol in symbols:
            try:
                result = update_symbol_data.delay(symbol, timeframe, source)
                results.append({"symbol": symbol, "source": source, "task_id": result.id})
            except Exception as e:
                results.append({"symbol": symbol, "source": source, "error": str(e)})

    return {"scheduled": len(results), "details": results}


@shared_task
def clean_old_cache(days_to_keep: int = 90) -> dict:
    """Clean old market data cache."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=days_to_keep)

    async def _clean():
        async with get_db_context() as db:
            result = await db.execute(
                select(MarketData).where(MarketData.timestamp < cutoff)
            )
            old_data = result.scalars().all()
            count = len(old_data)
            for item in old_data:
                await db.delete(item)
            await db.commit()
            return count

    deleted = asyncio.run(_clean())
    return {"deleted_records": deleted, "cutoff_date": cutoff.isoformat()}


@shared_task
def backfill_historical_data(
    symbol: str,
    timeframe: str,
    start_date: str,
    end_date: str,
    source: str = "binance"
) -> dict:
    """Backfill historical data for a symbol."""
    start = datetime.fromisoformat(start_date.replace("Z", "+00:00"))
    end = datetime.fromisoformat(end_date.replace("Z", "+00:00"))

    return asyncio.run(_update_symbol_data_async(symbol, timeframe, source))