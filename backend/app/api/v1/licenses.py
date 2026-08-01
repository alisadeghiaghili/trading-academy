"""License management endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from app.db.session import get_db
from app.db.models import User, License, LicenseStatus, UserRole
from app.schemas import (
    LicenseCreate,
    LicenseResponse,
    LicenseValidationRequest,
    LicenseValidationResponse,
)
from app.api.v1.auth import get_current_user_dependency
from app.core.licensing import get_license_manager

router = APIRouter(prefix="/licenses", tags=["licenses"])


@router.post("/validate", response_model=LicenseValidationResponse)
async def validate_license(
    request: LicenseValidationRequest,
    db: AsyncSession = Depends(get_db),
) -> LicenseValidationResponse:
    """Validate a license key."""
    license_manager = get_license_manager()

    result = await db.execute(
        select(License).where(License.license_key == request.license_key)
    )
    license_obj = result.scalar_one_or_none()

    if not license_obj:
        return LicenseValidationResponse(
            valid=False,
            error="License key not found",
        )

    valid, reason = license_manager.validate_license(license_obj)

    if not valid:
        return LicenseValidationResponse(
            valid=False,
            error=reason,
        )

    return LicenseValidationResponse(
        valid=True,
        tier=license_obj.tier.value,
        features=license_obj.metadata.get("features", []),
        expires_at=license_obj.expires_at,
    )


@router.post("/activate", response_model=LicenseResponse)
async def activate_license(
    request: LicenseValidationRequest,
    current_user: User = Depends(get_current_user_dependency),
    db: AsyncSession = Depends(get_db),
) -> LicenseResponse:
    """Activate a license key for current user."""
    license_manager = get_license_manager()

    result = await db.execute(
        select(License).where(License.license_key == request.license_key)
    )
    license_obj = result.scalar_one_or_none()

    if not license_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="License key not found",
        )

    if license_obj.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="License key does not belong to this user",
        )

    valid, reason = license_manager.validate_license(license_obj)
    if not valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=reason,
        )

    license_obj.status = LicenseStatus.ACTIVE
    await db.commit()
    await db.refresh(license_obj)

    return LicenseResponse.model_validate(license_obj)


@router.get("", response_model=list[LicenseResponse])
async def list_my_licenses(
    current_user: User = Depends(get_current_user_dependency),
    db: AsyncSession = Depends(get_db),
) -> list[LicenseResponse]:
    """List current user's licenses."""
    result = await db.execute(
        select(License).where(License.user_id == current_user.id)
    )
    licenses = result.scalars().all()
    return [LicenseResponse.model_validate(l) for l in licenses]


@router.get("/current", response_model=LicenseResponse | None)
async def get_current_license(
    current_user: User = Depends(get_current_user_dependency),
    db: AsyncSession = Depends(get_db),
) -> LicenseResponse | None:
    """Get current user's active license."""
    license_manager = get_license_manager()

    for license_obj in current_user.licenses:
        valid, _ = license_manager.validate_license(license_obj)
        if valid:
            return LicenseResponse.model_validate(license_obj)

    return None


# Admin endpoints
@router.post("/generate", response_model=LicenseResponse, status_code=status.HTTP_201_CREATED)
async def generate_license(
    license_data: LicenseCreate,
    user_id: UUID,
    current_user: User = Depends(get_current_user_dependency),
    db: AsyncSession = Depends(get_db),
) -> LicenseResponse:
    """Generate a new license for a user (admin only)."""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    result = await db.execute(select(User).where(User.id == user_id))
    target_user = result.scalar_one_or_none()

    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    license_manager = get_license_manager()
    tier = UserRole(license_data.tier)

    license_obj = license_manager.create_license(
        user=target_user,
        tier=tier,
        expires_in_days=license_data.expires_in_days,
    )

    db.add(license_obj)
    await db.commit()
    await db.refresh(license_obj)

    return LicenseResponse.model_validate(license_obj)


@router.post("/{license_id}/revoke", response_model=LicenseResponse)
async def revoke_license(
    license_id: UUID,
    reason: str = "revoked",
    current_user: User = Depends(get_current_user_dependency),
    db: AsyncSession = Depends(get_db),
) -> LicenseResponse:
    """Revoke a license (admin only)."""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    result = await db.execute(select(License).where(License.id == license_id))
    license_obj = result.scalar_one_or_none()

    if not license_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="License not found",
        )

    license_manager = get_license_manager()
    license_manager.revoke_license(license_obj, reason)

    await db.commit()
    await db.refresh(license_obj)

    return LicenseResponse.model_validate(license_obj)


@router.post("/{license_id}/renew", response_model=LicenseResponse)
async def renew_license(
    license_id: UUID,
    additional_days: int,
    current_user: User = Depends(get_current_user_dependency),
    db: AsyncSession = Depends(get_db),
) -> LicenseResponse:
    """Renew a license (admin only)."""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    result = await db.execute(select(License).where(License.id == license_id))
    license_obj = result.scalar_one_or_none()

    if not license_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="License not found",
        )

    license_manager = get_license_manager()
    license_manager.renew_license(license_obj, additional_days)

    await db.commit()
    await db.refresh(license_obj)

    return LicenseResponse.model_validate(license_obj)