"""Application configuration using Pydantic Settings."""

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field, PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    APP_NAME: str = "Trading Academy"
    APP_VERSION: str = "0.1.0"
    ENVIRONMENT: Literal["development", "staging", "production"] = "development"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 1

    # Database
    DATABASE_URL: PostgresDsn = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/trading_academy",
        validation_alias="DATABASE_URL",
    )
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20
    DATABASE_ECHO: bool = False

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"

    # Security
    SECRET_KEY: str = Field(..., validation_alias="SECRET_KEY")
    ALGORITHM: str = "RS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    LICENSE_PUBLIC_KEY_PATH: str = "keys/license_public.pem"
    LICENSE_PRIVATE_KEY_PATH: str = "keys/license_private.pem"

    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:5173"]

    # Internationalization
    DEFAULT_LOCALE: str = "en"
    SUPPORTED_LOCALES: list[str] = ["en", "fa", "de"]
    LOCALE_DIR: str = "locale"

    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    # Rate limiting
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW_SECONDS: int = 60

    # External APIs
    BINANCE_API_KEY: str | None = None
    BINANCE_API_SECRET: str | None = None
    COINGECKO_API_KEY: str | None = None
    NEWSAPI_KEY: str | None = None

    # Monitoring
    ENABLE_METRICS: bool = True
    METRICS_PORT: int = 9090

    @computed_field
    @property
    def license_public_key(self) -> str:
        """Load license public key from file."""
        path = Path(self.LICENSE_PUBLIC_KEY_PATH)
        if path.exists():
            return path.read_text(encoding="utf-8")
        return ""

    @computed_field
    @property
    def license_private_key(self) -> str:
        """Load license private key from file."""
        path = Path(self.LICENSE_PRIVATE_KEY_PATH)
        if path.exists():
            return path.read_text(encoding="utf-8")
        return ""


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()