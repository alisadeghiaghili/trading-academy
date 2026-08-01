"""API router initialization."""

from app.api.v1 import auth, users, licenses, modules, lessons, progress, quizzes, trades, market_data, health

__all__ = [
    "auth",
    "users",
    "licenses",
    "modules",
    "lessons",
    "progress",
    "quizzes",
    "trades",
    "market_data",
    "health",
]