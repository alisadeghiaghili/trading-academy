"""SQLAlchemy declarative base isolated to avoid circular imports."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all database models."""
