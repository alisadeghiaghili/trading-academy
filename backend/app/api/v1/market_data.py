"""Market data endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from uuid import UUID
from datetime import datetime, timezone
from typing import List, Optional

from app.db.session import get_db
from app.db.models import MarketData, User
from app.schemas import OHLCVResponse, MarketDataQuery, PaginatedResponse, PageParams
from app.api.v1.auth import get_current_user_dependency

router = APIRouter(prefix="/market-data", tags=["market-data"])


@router.get("/ohlcv", response_model=PaginatedResponse[OHLCVResponse])
async def get_ohlcv(
    params: MarketDataQuery = Depends(),
    pagination: PageParams = Depends(),
    current_user: User = Depends(get_current_user_dependency),
    db: AsyncSession = Depends(get_db),
) -> PaginatedResponse[OHLCVResponse]:
    """Get OHLCV data for a symbol."""
    query = select(MarketData).where(MarketData.symbol == params.symbol.upper())

    if params.timeframe:
        query = query.where(MarketData.timeframe == params.timeframe)

    if params.start:
        query = query.where(MarketData.timestamp >= params.start)

    if params.end:
        query = query.where(MarketData.timestamp <= params.end)

    query = query.order_by(MarketData.timestamp.desc())

    # Apply limit from params or pagination
    limit = min(params.limit, pagination.page_size)
    query = query.limit(limit)

    result = await db.execute(query)
    data = result.scalars().all()

    # Reverse to chronological order
    data = list(reversed(data))

    total = len(data)  # For simplicity, using actual returned count

    return PaginatedResponse.create(
        items=[OHLCVResponse.model_validate(d) for d in data],
        total=total,
        params=pagination,
    )


@router.get("/symbols", response_model=List[str])
async def get_available_symbols(
    current_user: User = Depends(get_current_user_dependency),
    db: AsyncSession = Depends(get_db),
) -> List[str]:
    """Get list of available symbols."""
    result = await db.execute(
        select(MarketData.symbol).distinct()
    )
    symbols = result.scalars().all()
    return sorted(set(symbols))


@router.get("/timeframes", response_model=List[str])
async def get_available_timeframes(
    symbol: str = Query(...),
    current_user: User = Depends(get_current_user_dependency),
    db: AsyncSession = Depends(get_db),
) -> List[str]:
    """Get available timeframes for a symbol."""
    result = await db.execute(
        select(MarketData.timeframe)
        .where(MarketData.symbol == symbol.upper())
        .distinct()
    )
    timeframes = result.scalars().all()
    return sorted(set(timeframes))


@router.get("/latest/{symbol}")
async def get_latest_price(
    symbol: str,
    timeframe: str = "1h",
    current_user: User = Depends(get_current_user_dependency),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Get latest price for a symbol."""
    result = await db.execute(
        select(MarketData)
        .where(
            (MarketData.symbol == symbol.upper()) &
            (MarketData.timeframe == timeframe)
        )
        .order_by(MarketData.timestamp.desc())
        .limit(1)
    )
    data = result.scalar_one_or_none()

    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No data found for symbol",
        )

    return {
        "symbol": data.symbol,
        "timeframe": data.timeframe,
        "timestamp": data.timestamp.isoformat(),
        "open": data.open,
        "high": data.high,
        "low": data.low,
        "close": data.close,
        "volume": data.volume,
        "source": data.source,
    }