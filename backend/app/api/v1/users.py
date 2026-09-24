"""User management endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from uuid import UUID
from typing import List

from app.db.session import get_db
from app.db.models import User, UserRole
from app.schemas import UserResponse, UserUpdate, UserWithLicense, PaginatedResponse, PageParams
from app.api.v1.auth import get_current_user_dependency
from app.core.licensing import get_license_manager

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserWithLicense)
async def get_me(
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
            features = license_obj.extra.get("features", [])
            break

    return UserWithLicense(
        **UserResponse.model_validate(current_user).model_dump(),
        license_tier=license_tier,
        license_status=license_status,
        license_expires_at=license_expires_at,
        features=features,
    )


@router.patch("/me", response_model=UserResponse)
async def update_me(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user_dependency),
    db: AsyncSession = Depends(get_db),
) -> UserResponse:
    """Update current user profile."""
    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(current_user, field, value)

    await db.commit()
    await db.refresh(current_user)
    return UserResponse.model_validate(current_user)


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_me(
    current_user: User = Depends(get_current_user_dependency),
    db: AsyncSession = Depends(get_db),
) -> None:
    """Delete current user account."""
    current_user.is_active = False
    await db.commit()


# Admin endpoints
@router.get("", response_model=PaginatedResponse[UserResponse])
async def list_users(
    params: PageParams = Depends(),
    role: UserRole | None = Query(None),
    is_active: bool | None = Query(None),
    current_user: User = Depends(get_current_user_dependency),
    db: AsyncSession = Depends(get_db),
) -> PaginatedResponse[UserResponse]:
    """List users (admin only)."""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    query = select(User)
    if role:
        query = query.where(User.role == role)
    if is_active is not None:
        query = query.where(User.is_active == is_active)

    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    total = await db.scalar(count_query)

    # Paginate
    query = query.offset((params.page - 1) * params.page_size).limit(params.page_size)
    result = await db.execute(query)
    users = result.scalars().all()

    return PaginatedResponse.create(
        items=[UserResponse.model_validate(u) for u in users],
        total=total,
        params=params,
    )


@router.get("/{user_id}", response_model=UserWithLicense)
async def get_user(
    user_id: UUID,
    current_user: User = Depends(get_current_user_dependency),
    db: AsyncSession = Depends(get_db),
) -> UserWithLicense:
    """Get user by ID (admin or self)."""
    if current_user.role != UserRole.ADMIN and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    license_manager = get_license_manager()
    license_tier = None
    license_status = None
    license_expires_at = None
    features = []

    for license_obj in user.licenses:
        valid, _ = license_manager.validate_license(license_obj)
        if valid:
            license_tier = license_obj.tier.value
            license_status = license_obj.status.value
            license_expires_at = license_obj.expires_at
            features = license_obj.extra.get("features", [])
            break

    return UserWithLicense(
        **UserResponse.model_validate(user).model_dump(),
        license_tier=license_tier,
        license_status=license_status,
        license_expires_at=license_expires_at,
        features=features,
    )