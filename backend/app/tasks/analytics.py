"""Analytics background tasks."""

import asyncio
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any
from uuid import UUID

from celery import shared_task
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_context
from app.db.models import PaperTrade, User, UserProgress, Lesson, Module
from app.core.licensing import get_license_manager


@shared_task
def compute_daily_metrics() -> dict:
    """Compute daily platform metrics."""
    return asyncio.run(_compute_daily_metrics_async())


async def _compute_daily_metrics_async() -> dict:
    """Async implementation of daily metrics computation."""
    yesterday = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    day_before = yesterday - timedelta(days=1)

    async with get_db_context() as db:
        # New users
        new_users = await db.scalar(
            select(func.count(User.id)).where(
                and_(User.created_at >= day_before, User.created_at < yesterday)
            )
        ) or 0

        # Active users (made at least one trade or lesson progress)
        active_traders = await db.scalar(
            select(func.count(func.distinct(PaperTrade.user_id))).where(
                and_(PaperTrade.created_at >= day_before, PaperTrade.created_at < yesterday)
            )
        ) or 0

        active_learners = await db.scalar(
            select(func.count(func.distinct(UserProgress.user_id))).where(
                and_(UserProgress.updated_at >= day_before, UserProgress.updated_at < yesterday)
            )
        ) or 0

        # Total trades
        total_trades = await db.scalar(
            select(func.count(PaperTrade.id)).where(
                and_(PaperTrade.created_at >= day_before, PaperTrade.created_at < yesterday)
            )
        ) or 0

        # Completed lessons
        completed_lessons = await db.scalar(
            select(func.count(UserProgress.id)).where(
                and_(
                    UserProgress.status == "completed",
                    UserProgress.completed_at >= day_before,
                    UserProgress.completed_at < yesterday
                )
            )
        ) or 0

        # Revenue (new Pro/Institutional licenses)
        from app.db.models import License, LicenseStatus, UserRole
        new_paid_licenses = await db.scalar(
            select(func.count(License.id)).where(
                and_(
                    License.issued_at >= day_before,
                    License.issued_at < yesterday,
                    License.tier.in_([UserRole.PRO, UserRole.INSTITUTIONAL]),
                    License.status == LicenseStatus.ACTIVE
                )
            )
        ) or 0

    return {
        "date": day_before.date().isoformat(),
        "new_users": new_users,
        "active_traders": active_traders,
        "active_learners": active_learners,
        "total_active_users": max(active_traders, active_learners),
        "total_trades": total_trades,
        "completed_lessons": completed_lessons,
        "new_paid_licenses": new_paid_licenses,
    }


@shared_task
def generate_rebalance_suggestions() -> dict:
    """Generate portfolio rebalancing suggestions for Pro+ users."""
    return asyncio.run(_generate_rebalance_suggestions_async())


async def _generate_rebalance_suggestions_async() -> dict:
    """Async implementation of rebalance suggestions."""
    license_manager = get_license_manager()

    async with get_db_context() as db:
        # Get Pro and Institutional users with active licenses
        result = await db.execute(
            select(User)
            .join(License, License.user_id == User.id)
            .where(
                and_(
                    License.status == LicenseStatus.ACTIVE,
                    License.tier.in_([UserRole.PRO, UserRole.INSTITUTIONAL]),
                    User.is_active == True
                )
            )
            .distinct()
        )
        users = result.scalars().all()

        suggestions_count = 0
        for user in users:
            # Get user's open positions
            result = await db.execute(
                select(PaperTrade).where(
                    and_(
                        PaperTrade.user_id == user.id,
                        PaperTrade.status.in_(["filled", "partially_filled"])
                    )
                )
            )
            trades = result.scalars().all()

            if len(trades) >= 3:  # Only suggest for diversified portfolios
                suggestions_count += 1
                # In production, compute actual rebalancing suggestions here
                # using risk parity, correlation analysis, etc.

    return {
        "generated_for_users": suggestions_count,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@shared_task
def analyze_user_trading_patterns(user_id: str) -> dict:
    """Analyze a user's trading patterns for coaching."""
    return asyncio.run(_analyze_user_trading_patterns_async(UUID(user_id)))


async def _analyze_user_trading_patterns_async(user_id: UUID) -> dict:
    """Async implementation of trading pattern analysis."""
    from app.core.coaching import TradingCoach

    coach = TradingCoach()
    return await coach.analyze_user_patterns(user_id)


@shared_task
def compute_lesson_completion_rates() -> dict:
    """Compute lesson completion rates for curriculum optimization."""
    return asyncio.run(_compute_lesson_completion_rates_async())


async def _compute_lesson_completion_rates_async() -> dict:
    """Async implementation of completion rates."""
    async with get_db_context() as db:
        # Get all published lessons
        result = await db.execute(
            select(Lesson).where(Lesson.is_published == True)
        )
        lessons = result.scalars().all()

        rates = []
        for lesson in lessons:
            total = await db.scalar(
                select(func.count(UserProgress.id)).where(UserProgress.lesson_id == lesson.id)
            ) or 0

            completed = await db.scalar(
                select(func.count(UserProgress.id)).where(
                    and_(
                        UserProgress.lesson_id == lesson.id,
                        UserProgress.status == "completed"
                    )
                )
            ) or 0

            rates.append({
                "lesson_id": str(lesson.id),
                "lesson_title": lesson.title,
                "module_id": str(lesson.module_id),
                "total_students": total,
                "completed": completed,
                "completion_rate": round(completed / total * 100, 2) if total > 0 else 0,
            })

        # Sort by completion rate
        rates.sort(key=lambda x: x["completion_rate"])

    return {
        "computed_at": datetime.now(timezone.utc).isoformat(),
        "lessons_analyzed": len(rates),
        "lowest_completion": rates[:5] if rates else [],
        "highest_completion": rates[-5:] if rates else [],
    }