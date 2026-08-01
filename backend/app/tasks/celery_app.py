"""Celery configuration for background tasks."""

from celery import Celery
from celery.schedules import crontab

from app.core.config import settings

celery_app = Celery(
    "trading_academy",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=[
        "app.tasks.market_data",
        "app.tasks.analytics",
        "app.tasks.notifications",
    ],
)

# Celery configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,
    task_soft_time_limit=3000,
    worker_prefetch_multiplier=4,
    worker_max_tasks_per_child=1000,
    result_expires=86400,
    beat_schedule={
        # Update market data every 5 minutes
        "update-market-data": {
            "task": "app.tasks.market_data.update_all_symbols",
            "schedule": 300.0,
        },
        # Daily analytics computation
        "daily-analytics": {
            "task": "app.tasks.analytics.compute_daily_metrics",
            "schedule": crontab(hour=1, minute=0),
        },
        # Weekly portfolio rebalancing suggestions
        "weekly-rebalance": {
            "task": "app.tasks.analytics.generate_rebalance_suggestions",
            "schedule": crontab(hour=2, minute=0, day_of_week=1),
        },
        # Clean old market data cache
        "clean-cache": {
            "task": "app.tasks.market_data.clean_old_cache",
            "schedule": crontab(hour=3, minute=0),
        },
    },
)

# Auto-discover tasks
celery_app.autodiscover_tasks(["app.tasks"])


@celery_app.task(bind=True, ignore_result=True)
def debug_task(self):
    """Debug task."""
    print(f"Request: {self.request!r}")