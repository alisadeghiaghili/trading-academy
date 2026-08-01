"""Security utilities: password hashing, JWT tokens, license validation."""

import time
from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID

from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import BaseModel

from app.core.config import settings


# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


# JWT Token models
class TokenPayload(BaseModel):
    """JWT token payload."""

    sub: str  # user_id
    exp: int  # expiration timestamp
    iat: int  # issued at timestamp
    type: str  # "access" or "refresh"
    role: str
    license_tier: Optional[str] = None


class LicensePayload(BaseModel):
    """License JWT payload."""

    license_key: str
    user_id: str
    tier: str
    features: list[str]
    exp: int
    iat: int
    iss: str = "trading-academy"


def create_access_token(
    user_id: UUID,
    role: str,
    license_tier: Optional[str] = None,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Create JWT access token.

    Args:
        user_id: User UUID.
        role: User role.
        license_tier: User's license tier.
        expires_delta: Optional custom expiration.

    Returns:
        Encoded JWT token.
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = TokenPayload(
        sub=str(user_id),
        exp=int(expire.timestamp()),
        iat=int(datetime.now(timezone.utc).timestamp()),
        type="access",
        role=role,
        license_tier=license_tier,
    )

    private_key = settings.license_private_key
    if not private_key:
        # Fallback to symmetric for development
        return jwt.encode(payload.model_dump(), settings.SECRET_KEY, algorithm="HS256")

    return jwt.encode(payload.model_dump(), private_key, algorithm="RS256")


def create_refresh_token(user_id: UUID, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT refresh token.

    Args:
        user_id: User UUID.
        expires_delta: Optional custom expiration.

    Returns:
        Encoded JWT token.
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    payload = TokenPayload(
        sub=str(user_id),
        exp=int(expire.timestamp()),
        iat=int(datetime.now(timezone.utc).timestamp()),
        type="refresh",
        role="",  # Not needed for refresh
    )

    private_key = settings.license_private_key
    if not private_key:
        return jwt.encode(payload.model_dump(), settings.SECRET_KEY, algorithm="HS256")

    return jwt.encode(payload.model_dump(), private_key, algorithm="RS256")


def decode_token(token: str) -> TokenPayload:
    """Decode and validate JWT token.

    Args:
        token: JWT token string.

    Returns:
        Decoded token payload.

    Raises:
        JWTError: If token is invalid or expired.
    """
    public_key = settings.license_public_key
    if not public_key:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    else:
        payload = jwt.decode(token, public_key, algorithms=["RS256"])

    return TokenPayload(**payload)


def create_license_token(
    license_key: str,
    user_id: UUID,
    tier: str,
    features: list[str],
    expires_at: datetime,
) -> str:
    """Create signed license token.

    Args:
        license_key: License key string.
        user_id: User UUID.
        tier: License tier.
        features: List of enabled features.
        expires_at: License expiration datetime.

    Returns:
        Signed JWT license token.
    """
    now = datetime.now(timezone.utc)
    payload = LicensePayload(
        license_key=license_key,
        user_id=str(user_id),
        tier=tier,
        features=features,
        exp=int(expires_at.timestamp()),
        iat=int(now.timestamp()),
    )

    private_key = settings.license_private_key
    if not private_key:
        return jwt.encode(payload.model_dump(), settings.SECRET_KEY, algorithm="HS256")

    return jwt.encode(payload.model_dump(), private_key, algorithm="RS256")


def verify_license_token(token: str) -> LicensePayload:
    """Verify and decode license token.

    Args:
        token: License JWT token.

    Returns:
        Decoded license payload.

    Raises:
        JWTError: If token is invalid, expired, or tampered.
    """
    public_key = settings.license_public_key
    if not public_key:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    else:
        payload = jwt.decode(token, public_key, algorithms=["RS256"])

    return LicensePayload(**payload)


def is_token_expired(exp_timestamp: int) -> bool:
    """Check if token is expired.

    Args:
        exp_timestamp: Expiration timestamp.

    Returns:
        True if expired.
    """
    return datetime.now(timezone.utc).timestamp() > exp_timestamp


# Feature flags per tier
TIER_FEATURES = {
    "free": [
        "basic_lessons",
        "basic_quizzes",
        "demo_paper_trading",
        "community_access",
    ],
    "pro": [
        "basic_lessons",
        "basic_quizzes",
        "demo_paper_trading",
        "community_access",
        "full_curriculum",
        "advanced_quizzes",
        "full_paper_trading",
        "backtesting",
        "strategy_builder",
        "risk_analytics",
        "portfolio_optimizer",
        "coaching_feedback",
        "priority_support",
    ],
    "institutional": [
        "basic_lessons",
        "basic_quizzes",
        "demo_paper_trading",
        "community_access",
        "full_curriculum",
        "advanced_quizzes",
        "full_paper_trading",
        "backtesting",
        "strategy_builder",
        "risk_analytics",
        "portfolio_optimizer",
        "coaching_feedback",
        "priority_support",
        "api_access",
        "white_label",
        "custom_branding",
        "sso",
        "audit_logs",
        "dedicated_support",
    ],
    "admin": [
        "all",
    ],
}


def get_features_for_tier(tier: str) -> list[str]:
    """Get feature list for a tier.

    Args:
        tier: Tier name.

    Returns:
        List of feature names.
    """
    return TIER_FEATURES.get(tier, TIER_FEATURES["free"])


def has_feature(tier: str, feature: str) -> bool:
    """Check if tier has a feature.

    Args:
        tier: Tier name.
        feature: Feature name.

    Returns:
        True if tier has feature.
    """
    features = get_features_for_tier(tier)
    return "all" in features or feature in features