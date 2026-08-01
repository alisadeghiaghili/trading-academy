"""Notification background tasks."""

import asyncio
from datetime import datetime, timedelta, timezone
from typing import List
from uuid import UUID

from celery import shared_task
from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_context
from app.db.models import User, UserProgress, Lesson, PaperTrade, License, LicenseStatus
from app.core.config import settings


@shared_task
def send_daily_learning_reminders() -> dict:
    """Send daily learning reminders to inactive users."""
    return asyncio.run(_send_daily_learning_reminders_async())


async def _send_daily_learning_reminders_async() -> dict:
    """Async implementation of learning reminders."""
    # Users inactive for 3+ days
    cutoff = datetime.now(timezone.utc) - timedelta(days=3)

    async with get_db_context() as db:
        result = await db.execute(
            select(User).where(
                and_(
                    User.is_active == True,
                    User.last_login_at < cutoff,
                    User.role != "admin"
                )
            )
        )
        inactive_users = result.scalars().all()

        sent = 0
        for user in inactive_users:
            # In production, send email/push notification
            # await send_email(user.email, "Continue your trading journey!", ...)
            sent += 1

    return {
        "reminders_sent": sent,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@shared_task
def send_license_expiry_warnings() -> dict:
    """Send license expiry warnings."""
    return asyncio.run(_send_license_expiry_warnings_async())


async def _send_license_expiry_warnings_async() -> dict:
    """Async implementation of license expiry warnings."""
    # Licenses expiring in 7, 3, 1 days
    warning_days = [7, 3, 1]
    now = datetime.now(timezone.utc)

    async with get_db_context() as db:
        sent = 0
        for days in warning_days:
            target_date = now + timedelta(days=days)
            start = target_date.replace(hour=0, minute=0, second=0, microsecond=0)
            end = start + timedelta(days=1)

            result = await db.execute(
                select(License, User)
                .join(User, User.id == License.user_id)
                .where(
                    and_(
                        License.status == LicenseStatus.ACTIVE,
                        License.expires_at >= start,
                        License.expires_at < end,
                        User.is_active == True
                    )
                )
            )
            expiring = result.all()

            for license_obj, user in expiring:
                # In production, send notification
                # await send_email(user.email, f"Your license expires in {days} days", ...)
                sent += 1

    return {
        "warnings_sent": sent,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@shared_task
def send_trade_review_reminders() -> dict:
    """Send reminders to review completed trades."""
    return asyncio.run(_send_trade_review_reminders_async())


async def _send_trade_review_reminders_async() -> dict:
    """Async implementation of trade review reminders."""
    # Trades closed 1 day ago without review
    target_date = datetime.now(timezone.utc) - timedelta(days=1)
    start = target_date.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1)

    async with get_db_context() as db:
        result = await db.execute(
            select(PaperTrade, User)
            .join(User, User.id == PaperTrade.user_id)
            .where(
                and_(
                    PaperTrade.status == "filled",
                    PaperTrade.closed_at >= start,
                    PaperTrade.closed_at < end,
                    PaperTrade.tags.not_contains(["reviewed"]),
                    User.is_active == True
                )
            )
        )
        unreviewed = result.all()

        sent = 0
        for trade, user in unreviewed:
            # In production, send notification
            # await send_email(user.email, f"Review your {trade.symbol} trade", ...)
            sent += 1

    return {
        "review_reminders_sent": sent,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@shared_task
def send_weekly_progress_report() -> dict:
    """Send weekly progress reports to active learners."""
    return asyncio.run(_send_weekly_progress_report_async())


async def _send_weekly_progress_report_async() -> dict:
    """Async implementation of weekly progress reports."""
    week_ago = datetime.now(timezone.utc) - timedelta(weeks=1)

    async with get_db_context() as db:
        # Users with progress in last week
        result = await db.execute(
            select(User).where(
                and_(
                    User.is_active == True,
                    User.id.in_(
                        select(UserProgress.user_id).where(
                            UserProgress.updated_at >= week_ago
                        )
                    )
                )
            )
        )
        active_learners = result.scalars().all()

        sent = 0
        for user in active_learners:
            # Compute weekly stats
            progress_result = await db.execute(
                select(UserProgress).where(
                    and_(
                        UserProgress.user_id == user.id,
                        UserProgress.updated_at >= week_ago
                    )
                )
            )
            progress = progress_result.scalars().all()

            completed = sum(1 for p in progress if p.status == "completed")
            time_spent = sum(p.time_spent_seconds for p in progress)

            if completed > 0 or time_spent > 0:
                # In production, send formatted email
                # await send_email(user.email, "Your Weekly Trading Academy Progress", ...)
                sent += 1

    return {
        "reports_sent": sent,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }