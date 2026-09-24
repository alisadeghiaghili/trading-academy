"""Main FastAPI application."""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from jose import JWTError

from app.core.config import settings
from app.core.i18n import get_i18n_manager, validate_locale
from app.db.session import init_db, close_db
from app.api.v1 import (
    auth,
    users,
    licenses,
    modules,
    lessons,
    progress,
    quizzes,
    trades,
    market_data,
    health,
    websocket,
    gamification,
)
from app.schemas import HealthResponse


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup
    logger.info("Starting Trading Academy Backend...")
    await init_db()
    logger.info("Database initialized")

    # Initialize i18n
    get_i18n_manager()
    logger.info("i18n initialized")

    yield

    # Shutdown
    logger.info("Shutting down...")
    await close_db()
    logger.info("Database connections closed")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Trading Academy API - Comprehensive trading education platform",
    docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT != "production" else None,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json" if settings.ENVIRONMENT != "production" else None,
    lifespan=lifespan,
)


# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Locale middleware
@app.middleware("http")
async def locale_middleware(request: Request, call_next):
    """Detect and set locale from header or query param."""
    # Check query param first
    locale = request.query_params.get("locale")

    # Then check Accept-Language header
    if not locale:
        accept_language = request.headers.get("Accept-Language", "")
        from app.core.i18n import detect_locale_from_header
        locale = detect_locale_from_header(accept_language)

    # Validate and set
    locale = validate_locale(locale)
    request.state.locale = locale

    response = await call_next(request)
    response.headers["Content-Language"] = locale
    return response


# Exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors."""
    locale = getattr(request.state, "locale", settings.DEFAULT_LOCALE)
    i18n = get_i18n_manager()

    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(x) for x in error["loc"]),
            "message": error["msg"],
            "type": error["type"],
        })

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation Error",
            "message": i18n.translate("validation_error", locale),
            "details": errors,
        },
    )


@app.exception_handler(SQLAlchemyError)
async def database_exception_handler(request: Request, exc: SQLAlchemyError):
    """Handle database errors."""
    logger.error(f"Database error: {exc}")
    locale = getattr(request.state, "locale", settings.DEFAULT_LOCALE)
    i18n = get_i18n_manager()

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Database Error",
            "message": i18n.translate("database_error", locale),
        },
    )


@app.exception_handler(JWTError)
async def jwt_exception_handler(request: Request, exc: JWTError):
    """Handle JWT errors."""
    locale = getattr(request.state, "locale", settings.DEFAULT_LOCALE)
    i18n = get_i18n_manager()

    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "error": "Authentication Error",
            "message": i18n.translate("invalid_token", locale),
        },
        headers={"WWW-Authenticate": "Bearer"},
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions with i18n."""
    locale = getattr(request.state, "locale", settings.DEFAULT_LOCALE)
    i18n = get_i18n_manager()

    # Try to translate detail if it's a known key
    detail = exc.detail
    if isinstance(detail, str) and not detail.startswith("{"):
        # Could translate here if detail matches translation keys
        pass

    return JSONResponse(
        status_code=exc.status_code,
        content={"error": detail},
        headers=exc.headers,
    )


# Include routers
app.include_router(health.router, prefix=settings.API_V1_PREFIX)
app.include_router(auth.router, prefix=settings.API_V1_PREFIX)
app.include_router(users.router, prefix=settings.API_V1_PREFIX)
app.include_router(licenses.router, prefix=settings.API_V1_PREFIX)
app.include_router(modules.router, prefix=settings.API_V1_PREFIX)
app.include_router(lessons.router, prefix=settings.API_V1_PREFIX)
app.include_router(progress.router, prefix=settings.API_V1_PREFIX)
app.include_router(quizzes.router, prefix=settings.API_V1_PREFIX)
app.include_router(trades.router, prefix=settings.API_V1_PREFIX)
app.include_router(market_data.router, prefix=settings.API_V1_PREFIX)
app.include_router(websocket.router, prefix=settings.API_V1_PREFIX)
app.include_router(gamification.router, prefix=settings.API_V1_PREFIX)


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": f"{settings.API_V1_PREFIX}/health",
    }


# Health check (also at root level for load balancers)
@app.get("/health", response_model=HealthResponse)
async def root_health():
    """Root health check."""
    return HealthResponse(
        status="healthy",
        version=settings.APP_VERSION,
        environment=settings.ENVIRONMENT,
        database="connected",
        redis="connected",
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        workers=settings.WORKERS if not settings.DEBUG else 1,
    )