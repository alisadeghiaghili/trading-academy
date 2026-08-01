"""Binance data fetcher implementation."""

import asyncio
from datetime import datetime, timezone
from typing import List, Optional
import httpx
import pandas as pd

from shared.trading_academy.data_fetchers.base import BaseDataFetcher, OHLCV, TickerInfo, CacheMixin


class BinanceFetcher(BaseDataFetcher, CacheMixin):
    """Binance API data fetcher."""

    BASE_URL = "https://api.binance.com"
    WS_BASE_URL = "wss://stream.binance.com:9443"

    def __init__(
        self,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        testnet: bool = False,
        cache_dir: str = "data/cache/binance",
    ):
        """Initialize Binance fetcher.

        Args:
            api_key: Binance API key.
            api_secret: Binance API secret.
            testnet: Use testnet.
            cache_dir: Cache directory.
        """
        BaseDataFetcher.__init__(self, api_key, api_secret)
        CacheMixin.__init__(self, cache_dir=cache_dir)

        self.testnet = testnet
        if testnet:
            self.BASE_URL = "https://testnet.binance.vision"
            self.WS_BASE_URL = "wss://testnet.binance.vision"

        self._client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client."""
        if self._client is None:
            self._client = httpx.AsyncClient(
                base_url=self.BASE_URL,
                timeout=30.0,
                headers={"X-MBX-APIKEY": self.api_key} if self.api_key else None,
            )
        return self._client

    async def close(self) -> None:
        """Close HTTP client."""
        if self._client:
            await self._client.aclose()
            self._client = None
        await super().close()

    def normalize_symbol(self, symbol: str) -> str:
        """Normalize symbol for Binance (BTCUSDT format)."""
        return symbol.upper().replace("/", "").replace("-", "").replace("_", "")

    def _denormalize_symbol(self, symbol: str) -> str:
        """Convert Binance symbol back to standard format."""
        # Simple heuristic - insert / before USDT, BTC, ETH, BNB, etc.
        quote_assets = ["USDT", "BTC", "ETH", "BNB", "BUSD", "USDC", "FDUSD"]
        for quote in quote_assets:
            if symbol.endswith(quote):
                base = symbol[:-len(quote)]
                return f"{base}/{quote}"
        return symbol

    async def fetch_ohlcv(
        self,
        symbol: str,
        timeframe: str = "1h",
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        limit: int = 1000,
    ) -> pd.DataFrame:
        """Fetch OHLCV data from Binance."""
        binance_symbol = self.normalize_symbol(symbol)
        interval = self._convert_timeframe(timeframe)

        # Check cache first
        cache_key = f"binance_{binance_symbol}_{interval}_{start}_{end}_{limit}"
        cached = self._load_from_cache(cache_key, max_age_hours=1)
        if cached is not None:
            return cached

        client = await self._get_client()

        params = {
            "symbol": binance_symbol,
            "interval": interval,
            "limit": min(limit, 1000),
        }

        if start:
            params["startTime"] = int(start.timestamp() * 1000)
        if end:
            params["endTime"] = int(end.timestamp() * 1000)

        try:
            response = await client.get("/api/v3/klines", params=params)
            response.raise_for_status()
            data = response.json()

            if not data:
                return pd.DataFrame()

            df = pd.DataFrame(data, columns=[
                "timestamp", "open", "high", "low", "close", "volume",
                "close_time", "quote_volume", "trades", "taker_buy_base",
                "taker_buy_quote", "ignore"
            ])

            # Convert to proper types
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
            for col in ["open", "high", "low", "close", "volume"]:
                df[col] = df[col].astype(float)

            # Select relevant columns
            df = df[["timestamp", "open", "high", "low", "close", "volume"]]

            # Cache result
            self._save_to_cache(cache_key, df)

            return df

        except httpx.HTTPError as e:
            raise ConnectionError(f"Binance API error: {e}")

    async def fetch_ohlcv_async(
        self,
        symbol: str,
        timeframe: str = "1h",
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        limit: int = 1000,
    ) -> pd.DataFrame:
        """Async alias for fetch_ohlcv."""
        return await self.fetch_ohlcv(symbol, timeframe, start, end, limit)

    def _convert_timeframe(self, timeframe: str) -> str:
        """Convert standard timeframe to Binance interval."""
        mapping = {
            "1m": "1m",
            "3m": "3m",
            "5m": "5m",
            "15m": "15m",
            "30m": "30m",
            "1h": "1h",
            "2h": "2h",
            "4h": "4h",
            "6h": "6h",
            "8h": "8h",
            "12h": "12h",
            "1d": "1d",
            "3d": "3d",
            "1w": "1w",
            "1M": "1M",
        }
        return mapping.get(timeframe, "1h")

    async def fetch_ticker(self, symbol: str) -> TickerInfo:
        """Fetch 24hr ticker from Binance."""
        binance_symbol = self.normalize_symbol(symbol)
        client = await self._get_client()

        try:
            response = await client.get("/api/v3/ticker/24hr", params={"symbol": binance_symbol})
            response.raise_for_status()
            data = response.json()

            return TickerInfo(
                symbol=symbol,
                name=self._denormalize_symbol(binance_symbol),
                price=float(data["lastPrice"]),
                change_24h=float(data["priceChange"]),
                change_24h_pct=float(data["priceChangePercent"]),
                volume_24h=float(data["volume"]),
                last_updated=datetime.now(timezone.utc),
            )
        except httpx.HTTPError as e:
            raise ConnectionError(f"Binance ticker error: {e}")

    async def fetch_symbols(self) -> List[str]:
        """Fetch all trading symbols from Binance."""
        client = await self._get_client()

        try:
            response = await client.get("/api/v3/exchangeInfo")
            response.raise_for_status()
            data = response.json()

            symbols = []
            for s in data["symbols"]:
                if s["status"] == "TRADING" and s["isSpotTradingAllowed"]:
                    symbols.append(self._denormalize_symbol(s["symbol"]))

            return symbols
        except httpx.HTTPError as e:
            raise ConnectionError(f"Binance symbols error: {e}")

    async def fetch_order_book(self, symbol: str, limit: int = 100) -> dict:
        """Fetch order book depth."""
        binance_symbol = self.normalize_symbol(symbol)
        client = await self._get_client()

        try:
            response = await client.get(
                "/api/v3/depth",
                params={"symbol": binance_symbol, "limit": limit}
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise ConnectionError(f"Binance order book error: {e}")

    async def fetch_recent_trades(self, symbol: str, limit: int = 100) -> List[dict]:
        """Fetch recent trades."""
        binance_symbol = self.normalize_symbol(symbol)
        client = await self._get_client()

        try:
            response = await client.get(
                "/api/v3/trades",
                params={"symbol": binance_symbol, "limit": limit}
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise ConnectionError(f"Binance trades error: {e}")


# Sync wrapper for compatibility
class BinanceFetcherSync:
    """Synchronous wrapper for BinanceFetcher."""

    def __init__(self, *args, **kwargs):
        self._fetcher = BinanceFetcher(*args, **kwargs)

    def fetch_ohlcv(self, *args, **kwargs) -> pd.DataFrame:
        return asyncio.run(self._fetcher.fetch_ohlcv(*args, **kwargs))

    def fetch_ticker(self, *args, **kwargs) -> TickerInfo:
        return asyncio.run(self._fetcher.fetch_ticker(*args, **kwargs))

    def fetch_symbols(self) -> List[str]:
        return asyncio.run(self._fetcher.fetch_symbols())

    def close(self):
        asyncio.run(self._fetcher.close())

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()