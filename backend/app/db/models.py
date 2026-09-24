"""Database models for the trading academy."""

import enum
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class UserRole(str, enum.Enum):
    """User role enumeration."""

    FREE = "free"
    PRO = "pro"
    INSTITUTIONAL = "institutional"
    ADMIN = "admin"


class LicenseStatus(str, enum.Enum):
    """License status enumeration."""

    ACTIVE = "active"
    EXPIRED = "expired"
    REVOKED = "revoked"
    PENDING = "pending"


class LessonType(str, enum.Enum):
    """Lesson type enumeration."""

    THEORY = "theory"
    PRACTICE = "practice"
    QUIZ = "quiz"
    SIMULATION = "simulation"


class TradeSide(str, enum.Enum):
    """Trade side enumeration."""

    BUY = "buy"
    SELL = "sell"


class OrderType(str, enum.Enum):
    """Order type enumeration."""

    MARKET = "market"
    LIMIT = "limit"
    STOP_LIMIT = "stop_limit"
    TRAILING_STOP = "trailing_stop"


class OrderStatus(str, enum.Enum):
    """Order status enumeration."""

    PENDING = "pending"
    FILLED = "filled"
    PARTIALLY_FILLED = "partially_filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"


class User(Base):
    """User model."""

    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, native_enum=False),
        default=UserRole.FREE,
        nullable=False,
    )
    locale: Mapped[str] = mapped_column(String(10), default="en", nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    last_login_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    licenses: Mapped[list["License"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    progress: Mapped[list["UserProgress"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    trades: Mapped[list["PaperTrade"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    quiz_attempts: Mapped[list["QuizAttempt"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_users_email_active", "email", "is_active"),
    )


class License(Base):
    """License key model for subscription management."""

    __tablename__ = "licenses"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    license_key: Mapped[str] = mapped_column(String(512), unique=True, index=True, nullable=False)
    tier: Mapped[UserRole] = mapped_column(Enum(UserRole, native_enum=False), nullable=False)
    status: Mapped[LicenseStatus] = mapped_column(
        Enum(LicenseStatus, native_enum=False),
        default=LicenseStatus.PENDING,
        nullable=False,
    )
    issued_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    revoked_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    extra: Mapped[dict] = mapped_column("metadata", JSONB, default=dict, nullable=False)

    # Relationships
    user: Mapped["User"] = relationship(back_populates="licenses")

    __table_args__ = (
        Index("ix_licenses_user_status", "user_id", "status"),
        Index("ix_licenses_expires", "expires_at"),
    )


class Module(Base):
    """Learning module model."""

    __tablename__ = "modules"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    order: Mapped[int] = mapped_column(Integer, nullable=False)
    required_tier: Mapped[UserRole] = mapped_column(
        Enum(UserRole, native_enum=False),
        default=UserRole.FREE,
        nullable=False,
    )
    is_published: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    lessons: Mapped[list["Lesson"]] = relationship(back_populates="module", cascade="all, delete-orphan", order_by="Lesson.order")

    __table_args__ = (
        Index("ix_modules_order_published", "order", "is_published"),
    )


class Lesson(Base):
    """Lesson model."""

    __tablename__ = "lessons"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    module_id: Mapped[UUID] = mapped_column(ForeignKey("modules.id", ondelete="CASCADE"), nullable=False, index=True)
    slug: Mapped[str] = mapped_column(String(100), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    lesson_type: Mapped[LessonType] = mapped_column(Enum(LessonType, native_enum=False), nullable=False)
    content: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)  # Notebook content, quiz questions, etc.
    order: Mapped[int] = mapped_column(Integer, nullable=False)
    estimated_minutes: Mapped[int] = mapped_column(Integer, default=30, nullable=False)
    required_tier: Mapped[UserRole] = mapped_column(
        Enum(UserRole, native_enum=False),
        default=UserRole.FREE,
        nullable=False,
    )
    is_published: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    module: Mapped["Module"] = relationship(back_populates="lessons")
    progress: Mapped[list["UserProgress"]] = relationship(back_populates="lesson", cascade="all, delete-orphan")
    quiz_questions: Mapped[list["QuizQuestion"]] = relationship(back_populates="lesson", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint("module_id", "slug", name="uq_lesson_module_slug"),
        Index("ix_lessons_module_order", "module_id", "order"),
    )


class UserProgress(Base):
    """User lesson progress model."""

    __tablename__ = "user_progress"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    lesson_id: Mapped[UUID] = mapped_column(ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), default="not_started", nullable=False)  # not_started, in_progress, completed
    score: Mapped[Optional[float]] = mapped_column(nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    time_spent_seconds: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    extra: Mapped[dict] = mapped_column("metadata", JSONB, default=dict, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="progress")
    lesson: Mapped["Lesson"] = relationship(back_populates="progress")

    __table_args__ = (
        UniqueConstraint("user_id", "lesson_id", name="uq_user_lesson_progress"),
        Index("ix_user_progress_user_status", "user_id", "status"),
    )


class QuizQuestion(Base):
    """Quiz question model."""

    __tablename__ = "quiz_questions"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    lesson_id: Mapped[UUID] = mapped_column(ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False, index=True)
    question_text: Mapped[dict] = mapped_column(JSONB, nullable=False)  # i18n: {en: "...", fa: "...", de: "..."}
    question_type: Mapped[str] = mapped_column(String(50), nullable=False)  # single_choice, multiple_choice, true_false, numeric
    options: Mapped[list[dict]] = mapped_column(JSONB, nullable=False)  # i18n options
    correct_answer: Mapped[dict] = mapped_column(JSONB, nullable=False)
    explanation: Mapped[dict] = mapped_column(JSONB, nullable=False)  # i18n explanation
    difficulty: Mapped[int] = mapped_column(Integer, default=1, nullable=False)  # 1-5
    order: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    lesson: Mapped["Lesson"] = relationship(back_populates="quiz_questions")
    attempts: Mapped[list["QuizAttempt"]] = relationship(back_populates="question", cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_quiz_questions_lesson_order", "lesson_id", "order"),
    )


class QuizAttempt(Base):
    """Quiz attempt model."""

    __tablename__ = "quiz_attempts"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    question_id: Mapped[UUID] = mapped_column(ForeignKey("quiz_questions.id", ondelete="CASCADE"), nullable=False, index=True)
    user_answer: Mapped[dict] = mapped_column(JSONB, nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)
    time_spent_seconds: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    attempted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    user: Mapped["User"] = relationship(back_populates="quiz_attempts")
    question: Mapped["QuizQuestion"] = relationship(back_populates="attempts")

    __table_args__ = (
        Index("ix_quiz_attempts_user_question", "user_id", "question_id"),
    )


class PaperTrade(Base):
    """Paper trade model for simulated trading."""

    __tablename__ = "paper_trades"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    symbol: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    side: Mapped[TradeSide] = mapped_column(Enum(TradeSide, native_enum=False), nullable=False)
    order_type: Mapped[OrderType] = mapped_column(Enum(OrderType, native_enum=False), nullable=False)
    quantity: Mapped[float] = mapped_column(nullable=False)
    price: Mapped[Optional[float]] = mapped_column(nullable=True)  # Limit/stop price
    stop_price: Mapped[Optional[float]] = mapped_column(nullable=True)
    trail_amount: Mapped[Optional[float]] = mapped_column(nullable=True)
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus, native_enum=False), default=OrderStatus.PENDING, nullable=False)
    filled_quantity: Mapped[float] = mapped_column(default=0.0, nullable=False)
    filled_price: Mapped[Optional[float]] = mapped_column(nullable=True)
    commission: Mapped[float] = mapped_column(default=0.0, nullable=False)
    pnl: Mapped[float] = mapped_column(default=0.0, nullable=False)
    strategy_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    tags: Mapped[list[str]] = mapped_column(JSONB, default=list, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    closed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    user: Mapped["User"] = relationship(back_populates="trades")

    __table_args__ = (
        Index("ix_paper_trades_user_symbol", "user_id", "symbol"),
        Index("ix_paper_trades_user_status", "user_id", "status"),
    )


class MarketData(Base):
    """Market data cache model."""

    __tablename__ = "market_data"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    symbol: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    timeframe: Mapped[str] = mapped_column(String(10), nullable=False, index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    open: Mapped[float] = mapped_column(nullable=False)
    high: Mapped[float] = mapped_column(nullable=False)
    low: Mapped[float] = mapped_column(nullable=False)
    close: Mapped[float] = mapped_column(nullable=False)
    volume: Mapped[float] = mapped_column(nullable=False)
    source: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        UniqueConstraint("symbol", "timeframe", "timestamp", "source", name="uq_market_data"),
        Index("ix_market_data_symbol_timeframe_timestamp", "symbol", "timeframe", "timestamp"),
    )