"""Pydantic schemas for API requests and responses."""

from datetime import datetime
from typing import Optional, List, Any, Generic, TypeVar
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, ConfigDict


# Base schemas
class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


# User schemas
class UserBase(BaseSchema):
    email: EmailStr
    full_name: Optional[str] = None
    locale: str = "en"


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=128)


class UserUpdate(BaseSchema):
    full_name: Optional[str] = None
    locale: Optional[str] = None
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    id: UUID
    role: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    last_login_at: Optional[datetime] = None


class UserWithLicense(UserResponse):
    license_tier: Optional[str] = None
    license_status: Optional[str] = None
    license_expires_at: Optional[datetime] = None
    features: List[str] = []


# Auth schemas
class Token(BaseSchema):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenRefresh(BaseSchema):
    refresh_token: str


class LoginRequest(BaseSchema):
    email: EmailStr
    password: str


class RegisterRequest(UserCreate):
    pass


# License schemas
class LicenseBase(BaseSchema):
    tier: str


class LicenseCreate(LicenseBase):
    expires_in_days: Optional[int] = None


class LicenseResponse(BaseSchema):
    id: UUID
    license_key: str
    tier: str
    status: str
    issued_at: datetime
    expires_at: Optional[datetime] = None
    features: List[str] = []


class LicenseValidationRequest(BaseSchema):
    license_key: str


class LicenseValidationResponse(BaseSchema):
    valid: bool
    tier: Optional[str] = None
    features: List[str] = []
    expires_at: Optional[datetime] = None
    error: Optional[str] = None


# Module schemas
class ModuleBase(BaseSchema):
    slug: str
    title: str
    description: str
    order: int
    required_tier: str = "free"


class ModuleCreate(ModuleBase):
    pass


class ModuleUpdate(BaseSchema):
    title: Optional[str] = None
    description: Optional[str] = None
    order: Optional[int] = None
    required_tier: Optional[str] = None
    is_published: Optional[bool] = None


class ModuleResponse(ModuleBase):
    id: UUID
    is_published: bool
    created_at: datetime
    updated_at: datetime
    lessons_count: int = 0


# Lesson schemas
class LessonBase(BaseSchema):
    slug: str
    title: str
    description: str
    lesson_type: str
    content: dict = {}
    order: int
    estimated_minutes: int = 30
    required_tier: str = "free"


class LessonCreate(LessonBase):
    module_id: UUID


class LessonUpdate(BaseSchema):
    title: Optional[str] = None
    description: Optional[str] = None
    lesson_type: Optional[str] = None
    content: Optional[dict] = None
    order: Optional[int] = None
    estimated_minutes: Optional[int] = None
    required_tier: Optional[str] = None
    is_published: Optional[bool] = None


class LessonResponse(LessonBase):
    id: UUID
    module_id: UUID
    is_published: bool
    created_at: datetime
    updated_at: datetime


class LessonWithProgress(LessonResponse):
    progress: Optional[dict] = None


# Progress schemas
class ProgressBase(BaseSchema):
    lesson_id: UUID
    status: str = "not_started"
    score: Optional[float] = None
    time_spent_seconds: int = 0


class ProgressUpdate(BaseSchema):
    status: Optional[str] = None
    score: Optional[float] = None
    time_spent_seconds: Optional[int] = None
    metadata: Optional[dict] = None


class ProgressResponse(ProgressBase):
    id: UUID
    user_id: UUID
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


# Quiz schemas
class QuizQuestionBase(BaseSchema):
    question_text: dict
    question_type: str
    options: List[dict]
    correct_answer: dict
    explanation: dict
    difficulty: int = 1
    order: int


class QuizQuestionCreate(QuizQuestionBase):
    lesson_id: UUID


class QuizQuestionResponse(QuizQuestionBase):
    id: UUID
    lesson_id: UUID
    created_at: datetime


class QuizAttemptCreate(BaseSchema):
    question_id: UUID
    user_answer: dict
    time_spent_seconds: int = 0


class QuizAttemptResponse(BaseSchema):
    id: UUID
    user_id: UUID
    question_id: UUID
    user_answer: dict
    is_correct: bool
    time_spent_seconds: int
    attempted_at: datetime


# Paper trade schemas
class PaperTradeBase(BaseSchema):
    symbol: str
    side: str
    order_type: str
    quantity: float = Field(..., gt=0)
    price: Optional[float] = None
    stop_price: Optional[float] = None
    trail_amount: Optional[float] = None
    strategy_name: Optional[str] = None
    notes: Optional[str] = None
    tags: List[str] = []


class PaperTradeCreate(PaperTradeBase):
    pass


class PaperTradeUpdate(BaseSchema):
    notes: Optional[str] = None
    tags: Optional[List[str]] = None


class PaperTradeResponse(PaperTradeBase):
    id: UUID
    user_id: UUID
    status: str
    filled_quantity: float
    filled_price: Optional[float] = None
    commission: float
    pnl: float
    created_at: datetime
    updated_at: datetime
    closed_at: Optional[datetime] = None


# Market data schemas
class OHLCVBase(BaseSchema):
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float


class OHLCVResponse(OHLCVBase):
    symbol: str
    timeframe: str
    source: str


class MarketDataQuery(BaseSchema):
    symbol: str
    timeframe: str = "1h"
    start: Optional[datetime] = None
    end: Optional[datetime] = None
    limit: int = 1000


# Health/Info schemas
class HealthResponse(BaseSchema):
    status: str
    version: str
    environment: str
    database: str
    redis: str


class LocaleInfo(BaseSchema):
    code: str
    name: str
    english_name: str
    native_name: str
    rtl: bool
    date_format: str
    datetime_format: str
    number_format: str
    currency_format: str


class FeatureFlagResponse(BaseSchema):
    tier: str
    features: List[str]


# Pagination
class PageParams(BaseSchema):
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)


T = TypeVar("T")


class PaginatedResponse(BaseSchema, Generic[T]):
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int

    @classmethod
    def create(cls, items: List[T], total: int, params: PageParams) -> "PaginatedResponse[T]":
        return cls(
            items=items,
            total=total,
            page=params.page,
            page_size=params.page_size,
            total_pages=(total + params.page_size - 1) // params.page_size,
        )