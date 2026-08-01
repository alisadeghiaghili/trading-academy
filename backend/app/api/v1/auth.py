"""Authentication endpoints."""

from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from app.core.config import settings
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.db.session import get_db
from app.db.models import User, UserRole
from app.schemas import (
    Token,
    TokenRefresh,
    LoginRequest,
    RegisterRequest,
    UserResponse,
    UserWithLicense,
)
from app.core.licensing import get_license_manager

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: RegisterRequest,
    db: AsyncSession = Depends(get_db),
) -> UserResponse:
    """Register a new user."""
    # Check if email exists
    result = await db.execute(select(User).where(User.email == user_data.email))
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Create user
    user = User(
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        full_name=user_data.full_name,
        locale=user_data.locale,
        role=UserRole.FREE,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    return UserResponse.model_validate(user)


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
) -> Token:
    """Login with email and password."""
    result = await db.execute(select(User).where(User.email == form_data.username))
    user = result.scalar_one_or_none()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is disabled",
        )

    # Get user's active license
    license_manager = get_license_manager()
    license_tier = None
    for license_obj in user.licenses:
        valid, _ = license_manager.validate_license(license_obj)
        if valid:
            license_tier = license_obj.tier.value
            break

    access_token = create_access_token(
        user_id=user.id,
        role=user.role.value,
        license_tier=license_tier,
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    refresh_token = create_refresh_token(user_id=user.id)

    # Update last login
    user.last_login_at = datetime.now(timezone.utc)
    await db.commit()

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


@router.post("/refresh", response_model=Token)
async def refresh_token(
    token_data: TokenRefresh,
    db: AsyncSession = Depends(get_db),
) -> Token:
    """Refresh access token."""
    try:
        payload = decode_token(token_data.refresh_token)
        if payload.type != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
            )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    user_id = UUID(payload.sub)
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )

    # Get user's active license
    license_manager = get_license_manager()
    license_tier = None
    for license_obj in user.licenses:
        valid, _ = license_manager.validate_license(license_obj)
        if valid:
            license_tier = license_obj.tier.value
            break

    access_token = create_access_token(
        user_id=user.id,
        role=user.role.value,
        license_tier=license_tier,
    )
    refresh_token = create_refresh_token(user_id=user.id)

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


@router.post("/logout")
async def logout() -> dict:
    """Logout (client should discard tokens)."""
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=UserWithLicense)
async def get_current_user(
    current_user: User = Depends(get_current_user_dependency),
) -> UserWithLicense:
    """Get current user profile with license info."""
    license_manager = get_license_manager()
    license_tier = None
    license_status = None
    license_expires_at = None
    features = []

    for license_obj in current_user.licenses:
        valid, _ = license_manager.validate_license(license_obj)
        if valid:
            license_tier = license_obj.tier.value
            license_status = license_obj.status.value
            license_expires_at = license_obj.expires_at
            features = license_obj.metadata.get("features", [])
            break

    return UserWithLicense(
        **UserResponse.model_validate(current_user).model_dump(),
        license_tier=license_tier,
        license_status=license_status,
        license_expires_at=license_expires_at,
        features=features,
    )


# Dependency for getting current user
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_PREFIX}/auth/login")


async def get_current_user_dependency(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    """Get current authenticated user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_token(token)
        if payload.type != "access":
            raise credentials_exception
        user_id = UUID(payload.sub)
    except (JWTError, ValueError):
        raise credentials_exception

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if user is None:
        raise credentials_exception

    return user