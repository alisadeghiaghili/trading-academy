"""Gamification models for Trading Academy."""

from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional
from enum import Enum

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum as SAEnum,
    ForeignKey,
    Integer,
    String,
    Float,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class BadgeTier(str, Enum):
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"
    PLATINUM = "platinum"
    DIAMOND = "diamond"


class ChallengeType(str, Enum):
    DAILY_LESSON = "daily_lesson"
    DAILY_QUIZ = "daily_quiz"
    DAILY_TRADE = "daily_trade"
    DAILY_LOGIN = "daily_login"
    WEEKLY_CHALLENGE = "weekly_challenge"
    SPECIAL_EVENT = "special_event"
    PATTERN_SPOTTER = "pattern_spotter"
    RISK_MANAGER = "risk_manager"
    STRATEGY_MASTER = "strategy_master"
    NEWS_TRACKER = "news_tracker"


class AchievementCategory(str, Enum):
    LEARNING = "learning"
    TRADING = "trading"
    QUIZ = "quiz"
    STREAK = "streak"
    RISK = "risk"
    SOCIAL = "social"
    EXPLORATION = "exploration"
    MASTERY = "mastery"


class UserLevel(str, Enum):
    BEGINNER = "beginner"
    NOVICE = "novice"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"
    MASTER = "master"
    GRANDMASTER = "grandmaster"
    LEGEND = "legend"


class Badge(Base):
    """Achievement badges that users can earn."""

    __tablename__ = "badges"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    code: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    name: Mapped[dict] = mapped_column(JSONB, nullable=False)  # i18n: {en, fa, de}
    description: Mapped[dict] = mapped_column(JSONB, nullable=False)
    category: Mapped[AchievementCategory] = mapped_column(
        SAEnum(AchievementCategory, native_enum=False), nullable=False
    )
    tier: Mapped[BadgeTier] = mapped_column(
        SAEnum(BadgeTier, native_enum=False), default=BadgeTier.BRONZE, nullable=False
    )
    icon_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    icon_emoji: Mapped[str] = mapped_column(String(10), default="🏅", nullable=False)
    xp_reward: Mapped[int] = mapped_column(Integer, default=50, nullable=False)
    criteria: Mapped[dict] = mapped_column(JSONB, nullable=False)  # {type, target, field}
    is_secret: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class UserBadge(Base):
    """User's earned badges."""

    __tablename__ = "user_badges"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    badge_id: Mapped[UUID] = mapped_column(
        ForeignKey("badges.id", ondelete="CASCADE"), nullable=False, index=True
    )
    earned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    badge: Mapped[Badge] = relationship()


class UserXP(Base):
    """User experience points and level tracking."""

    __tablename__ = "user_xp"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True, index=True
    )
    total_xp: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    current_level: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    level_title: Mapped[UserLevel] = mapped_column(
        SAEnum(UserLevel, native_enum=False), default=UserLevel.BEGINNER, nullable=False
    )
    xp_to_next_level: Mapped[int] = mapped_column(Integer, default=100, nullable=False)
    lessons_completed: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    quizzes_passed: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    trades_completed: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    login_streak: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    longest_login_streak: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    learning_streak: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    longest_learning_streak: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    perfect_quizzes: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_study_time_minutes: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )


class XPTransaction(Base):
    """XP transaction log."""

    __tablename__ = "xp_transactions"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    source: Mapped[str] = mapped_column(String(50), nullable=False)  # lesson, quiz, trade, streak, badge, challenge
    source_id: Mapped[Optional[UUID]] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class DailyChallenge(Base):
    """Daily challenges for users."""

    __tablename__ = "daily_challenges"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    challenge_type: Mapped[ChallengeType] = mapped_column(
        SAEnum(ChallengeType, native_enum=False), nullable=False
    )
    title: Mapped[dict] = mapped_column(JSONB, nullable=False)
    description: Mapped[dict] = mapped_column(JSONB, nullable=False)
    target: Mapped[int] = mapped_column(Integer, default=1, nullable=False)  # e.g., complete 3 lessons
    xp_reward: Mapped[int] = mapped_column(Integer, default=100, nullable=False)
    coin_reward: Mapped[int] = mapped_column(Integer, default=10, nullable=False)
    bonus_xp: Mapped[int] = mapped_column(Integer, default=0, nullable=False)  # extra XP for streaks
    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class UserChallenge(Base):
    """User challenge progress."""

    __tablename__ = "user_challenges"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    challenge_id: Mapped[UUID] = mapped_column(
        ForeignKey("daily_challenges.id", ondelete="CASCADE"), nullable=False, index=True
    )
    progress: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    xp_earned: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    challenge: Mapped[DailyChallenge] = relationship()


class DailyReward(Base):
    """Daily login reward tracking."""

    __tablename__ = "daily_rewards"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    reward_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    streak_day: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    xp_earned: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    coin_earned: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    bonus_claimed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class LeaderboardEntry(Base):
    """Leaderboard entries."""

    __tablename__ = "leaderboard_entries"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    category: Mapped[str] = mapped_column(String(50), nullable=False)  # xp, trades, quiz, streak
    score: Mapped[float] = mapped_column(Float, default=0, nullable=False)
    rank: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    period: Mapped[str] = mapped_column(String(20), nullable=False)  # daily, weekly, monthly, all_time
    period_start: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    period_end: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )


class Tutorial(Base):
    """Interactive guided tutorials."""

    __tablename__ = "tutorials"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    title: Mapped[dict] = mapped_column(JSONB, nullable=False)
    description: Mapped[dict] = mapped_column(JSONB, nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, default=1, nullable=False)  # 1-5
    steps: Mapped[list] = mapped_column(JSONB, nullable=False)  # Tutorial steps
    estimated_minutes: Mapped[int] = mapped_column(Integer, default=10, nullable=False)
    xp_reward: Mapped[int] = mapped_column(Integer, default=50, nullable=False)
    required_tier: Mapped[str] = mapped_column(String(20), default="free", nullable=False)
    is_published: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class UserTutorial(Base):
    """User tutorial progress."""

    __tablename__ = "user_tutorials"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    tutorial_id: Mapped[UUID] = mapped_column(
        ForeignKey("tutorials.id", ondelete="CASCADE"), nullable=False, index=True
    )
    current_step: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    time_spent_seconds: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class PatternGame(Base):
    """Chart pattern recognition game/scenario."""

    __tablename__ = "pattern_games"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    title: Mapped[dict] = mapped_column(JSONB, nullable=False)
    description: Mapped[dict] = mapped_column(JSONB, nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, default=1, nullable=False)  # 1-5
    pattern_type: Mapped[str] = mapped_column(String(50), nullable=False)  # head_shoulders, double_top, etc.
    chart_data: Mapped[list] = mapped_column(JSONB, nullable=False)  # OHLCV data for the pattern
    correct_answer: Mapped[str] = mapped_column(String(50), nullable=False)
    options: Mapped[list] = mapped_column(JSONB, nullable=False)  # Multiple choice options
    explanation: Mapped[dict] = mapped_column(JSONB, nullable=False)
    xp_reward: Mapped[int] = mapped_column(Integer, default=30, nullable=False)
    is_published: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class PatternGameAttempt(Base):
    """User pattern game attempts."""

    __tablename__ = "pattern_game_attempts"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    game_id: Mapped[UUID] = mapped_column(
        ForeignKey("pattern_games.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user_answer: Mapped[str] = mapped_column(String(50), nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)
    time_taken_seconds: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    xp_earned: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    attempted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class EconomicEvent(Base):
    """Economic calendar events."""

    __tablename__ = "economic_events"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    title_fa: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    title_de: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    country: Mapped[str] = mapped_column(String(10), nullable=False)  # ISO country code
    impact: Mapped[str] = mapped_column(String(20), nullable=False)  # high, medium, low
    event_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    actual_value: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    forecast_value: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    previous_value: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    currency: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)  # affected currency
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_published: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class NewsItem(Base):
    """Trading news items."""

    __tablename__ = "news_items"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    title_fa: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    title_de: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    summary_fa: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    summary_de: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    content_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    source: Mapped[str] = mapped_column(String(100), nullable=False)
    source_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    image_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    category: Mapped[str] = mapped_column(String(50), nullable=False)  # crypto, stocks, forex, macro
    sentiment: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)  # bullish, bearish, neutral
    related_symbols: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    importance: Mapped[int] = mapped_column(Integer, default=1, nullable=False)  # 1-5
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    is_published: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
