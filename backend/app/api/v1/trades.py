"""Paper trading endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from uuid import UUID
from datetime import datetime, timezone
from typing import List, Optional

from app.db.session import get_db
from app.db.models import PaperTrade, User, TradeSide, OrderType, OrderStatus
from app.schemas import PaperTradeCreate, PaperTradeUpdate, PaperTradeResponse, PaginatedResponse, PageParams
from app.api.v1.auth import get_current_user_dependency

router = APIRouter(prefix="/trades", tags=["paper-trading"])


@router.post("", response_model=PaperTradeResponse, status_code=status.HTTP_201_CREATED)
async def create_trade(
    trade_data: PaperTradeCreate,
    current_user: User = Depends(get_current_user_dependency),
    db: AsyncSession = Depends(get_db),
) -> PaperTradeResponse:
    """Create a new paper trade."""
    trade = PaperTrade(
        user_id=current_user.id,
        **trade_data.model_dump(),
    )
    db.add(trade)
    await db.commit()
    await db.refresh(trade)

    return PaperTradeResponse.model_validate(trade)


@router.get("", response_model=PaginatedResponse[PaperTradeResponse])
async def list_trades(
    params: PageParams = Depends(),
    symbol: Optional[str] = Query(None),
    status_filter: Optional[str] = Query(None),
    side: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user_dependency),
    db: AsyncSession = Depends(get_db),
) -> PaginatedResponse[PaperTradeResponse]:
    """List user's paper trades."""
    query = select(PaperTrade).where(PaperTrade.user_id == current_user.id)

    if symbol:
        query = query.where(PaperTrade.symbol.ilike(f"%{symbol}%"))
    if status_filter:
        query = query.where(PaperTrade.status == status_filter)
    if side:
        query = query.where(PaperTrade.side == side)

    query = query.order_by(PaperTrade.created_at.desc())

    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    total = await db.scalar(count_query)

    # Paginate
    query = query.offset((params.page - 1) * params.page_size).limit(params.page_size)
    result = await db.execute(query)
    trades = result.scalars().all()

    return PaginatedResponse.create(
        items=[PaperTradeResponse.model_validate(t) for t in trades],
        total=total,
        params=params,
    )


@router.get("/{trade_id}", response_model=PaperTradeResponse)
async def get_trade(
    trade_id: UUID,
    current_user: User = Depends(get_current_user_dependency),
    db: AsyncSession = Depends(get_db),
) -> PaperTradeResponse:
    """Get a specific trade."""
    result = await db.execute(
        select(PaperTrade).where(
            (PaperTrade.id == trade_id) &
            (PaperTrade.user_id == current_user.id)
        )
    )
    trade = result.scalar_one_or_none()

    if not trade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trade not found",
        )

    return PaperTradeResponse.model_validate(trade)


@router.patch("/{trade_id}", response_model=PaperTradeResponse)
async def update_trade(
    trade_id: UUID,
    trade_update: PaperTradeUpdate,
    current_user: User = Depends(get_current_user_dependency),
    db: AsyncSession = Depends(get_db),
) -> PaperTradeResponse:
    """Update trade notes/tags."""
    result = await db.execute(
        select(PaperTrade).where(
            (PaperTrade.id == trade_id) &
            (PaperTrade.user_id == current_user.id)
        )
    )
    trade = result.scalar_one_or_none()

    if not trade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trade not found",
        )

    update_data = trade_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(trade, field, value)

    trade.updated_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(trade)

    return PaperTradeResponse.model_validate(trade)


@router.post("/{trade_id}/cancel", response_model=PaperTradeResponse)
async def cancel_trade(
    trade_id: UUID,
    current_user: User = Depends(get_current_user_dependency),
    db: AsyncSession = Depends(get_db),
) -> PaperTradeResponse:
    """Cancel a pending trade."""
    result = await db.execute(
        select(PaperTrade).where(
            (PaperTrade.id == trade_id) &
            (PaperTrade.user_id == current_user.id)
        )
    )
    trade = result.scalar_one_or_none()

    if not trade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trade not found",
        )

    if trade.status not in [OrderStatus.PENDING, OrderStatus.PARTIALLY_FILLED]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only pending or partially filled trades can be cancelled",
        )

    trade.status = OrderStatus.CANCELLED
    trade.updated_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(trade)

    return PaperTradeResponse.model_validate(trade)


@router.get("/stats/summary")
async def get_trade_summary(
    current_user: User = Depends(get_current_user_dependency),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Get trading statistics."""
    # Total trades
    total_trades = await db.scalar(
        select(func.count(PaperTrade.id)).where(PaperTrade.user_id == current_user.id)
    ) or 0

    # Closed trades
    closed_trades = await db.scalar(
        select(func.count(PaperTrade.id)).where(
            (PaperTrade.user_id == current_user.id) &
            (PaperTrade.status == OrderStatus.FILLED)
        )
    ) or 0

    # Total P&L
    total_pnl = await db.scalar(
        select(func.sum(PaperTrade.pnl)).where(
            (PaperTrade.user_id == current_user.id) &
            (PaperTrade.status == OrderStatus.FILLED)
        )
    ) or 0

    # Win rate
    winning_trades = await db.scalar(
        select(func.count(PaperTrade.id)).where(
            (PaperTrade.user_id == current_user.id) &
            (PaperTrade.status == OrderStatus.FILLED) &
            (PaperTrade.pnl > 0)
        )
    ) or 0

    win_rate = (winning_trades / closed_trades * 100) if closed_trades > 0 else 0

    # Best/Worst trade
    best_trade = await db.scalar(
        select(func.max(PaperTrade.pnl)).where(
            (PaperTrade.user_id == current_user.id) &
            (PaperTrade.status == OrderStatus.FILLED)
        )
    ) or 0

    worst_trade = await db.scalar(
        select(func.min(PaperTrade.pnl)).where(
            (PaperTrade.user_id == current_user.id) &
            (PaperTrade.status == OrderStatus.FILLED)
        )
    ) or 0

    # By symbol
    result = await db.execute(
        select(PaperTrade.symbol, func.count(PaperTrade.id), func.sum(PaperTrade.pnl))
        .where(
            (PaperTrade.user_id == current_user.id) &
            (PaperTrade.status == OrderStatus.FILLED)
        )
        .group_by(PaperTrade.symbol)
    )
    by_symbol = {
        symbol: {"trades": count, "pnl": float(pnl or 0)}
        for symbol, count, pnl in result.all()
    }

    return {
        "total_trades": total_trades,
        "closed_trades": closed_trades,
        "open_trades": total_trades - closed_trades,
        "total_pnl": float(total_pnl),
        "win_rate": round(win_rate, 2),
        "winning_trades": winning_trades,
        "losing_trades": closed_trades - winning_trades,
        "best_trade": float(best_trade),
        "worst_trade": float(worst_trade),
        "by_symbol": by_symbol,
    }