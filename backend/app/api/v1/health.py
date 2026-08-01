"""Health check endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from app.core.config import settings
from app.db.session import get_db
from app.schemas import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check(db: AsyncSession = Depends(get_db)) -> HealthResponse:
    """Health check endpoint."""
    # Check database
    db_status = "connected"
    try:
        await db.execute("SELECT 1")
    except Exception:
        db_status = "disconnected"

    # Check Redis
    redis_status = "connected"
    try:
        redis = Redis.from_url(settings.REDIS_URL)
        await redis.ping()
        await redis.close()
    except Exception:
        redis_status = "disconnected"

    return HealthResponse(
        status="healthy" if db_status == "connected" and redis_status == "connected" else "degraded",
        version=settings.APP_VERSION,
        environment=settings.ENVIRONMENT,
        database=db_status,
        redis=redis_status,
    )


@router.get("/health/ready")
async def readiness_check(db: AsyncSession = Depends(get_db)) -> dict:
    """Kubernetes readiness probe."""
    try:
        await db.execute("SELECT 1")
        return {"status": "ready"}
    except Exception:
        return {"status": "not ready"}


@router.get("/health/live")
async def liveness_check() -> dict:
    """Kubernetes liveness probe."""
    return {"status": "alive"}