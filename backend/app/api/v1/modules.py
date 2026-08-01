"""Module management endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from uuid import UUID
from typing import List

from app.db.session import get_db
from app.db.models import Module, Lesson, User, UserRole
from app.schemas import (
    ModuleCreate,
    ModuleUpdate,
    ModuleResponse,
    PaginatedResponse,
    PageParams,
)
from app.api.v1.auth import get_current_user_dependency
from app.core.licensing import get_license_manager, has_feature

router = APIRouter(prefix="/modules", tags=["modules"])


@router.get("", response_model=PaginatedResponse[ModuleResponse])
async def list_modules(
    params: PageParams = Depends(),
    published_only: bool = Query(True),
    current_user: User = Depends(get_current_user_dependency),
    db: AsyncSession = Depends(get_db),
) -> PaginatedResponse[ModuleResponse]:
    """List all modules."""
    query = select(Module)

    if published_only:
        query = query.where(Module.is_published == True)

        # Filter by user's license tier
        license_manager = get_license_manager()
        user_tier = UserRole.FREE
        for license_obj in current_user.licenses:
            valid, _ = license_manager.validate_license(license_obj)
            if valid:
                user_tier = license_obj.tier
                break

        # Only show modules user has access to
        accessible_tiers = [UserRole.FREE]
        if user_tier == UserRole.PRO:
            accessible_tiers.append(UserRole.PRO)
        elif user_tier == UserRole.INSTITUTIONAL:
            accessible_tiers.extend([UserRole.PRO, UserRole.INSTITUTIONAL])

        query = query.where(Module.required_tier.in_(accessible_tiers))

    query = query.order_by(Module.order)

    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    total = await db.scalar(count_query)

    # Paginate
    query = query.offset((params.page - 1) * params.page_size).limit(params.page_size)
    result = await db.execute(query)
    modules = result.scalars().all()

    # Add lessons count
    module_responses = []
    for module in modules:
        lessons_count = await db.scalar(
            select(func.count(Lesson.id)).where(Lesson.module_id == module.id)
        )
        resp = ModuleResponse.model_validate(module)
        resp.lessons_count = lessons_count or 0
        module_responses.append(resp)

    return PaginatedResponse.create(
        items=module_responses,
        total=total,
        params=params,
    )


@router.get("/{module_id}", response_model=ModuleResponse)
async def get_module(
    module_id: UUID,
    current_user: User = Depends(get_current_user_dependency),
    db: AsyncSession = Depends(get_db),
) -> ModuleResponse:
    """Get module by ID."""
    result = await db.execute(
        select(Module).where(Module.id == module_id)
    )
    module = result.scalar_one_or_none()

    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Module not found",
        )

    if not module.is_published and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Module not found",
        )

    lessons_count = await db.scalar(
        select(func.count(Lesson.id)).where(Lesson.module_id == module.id)
    )
    resp = ModuleResponse.model_validate(module)
    resp.lessons_count = lessons_count or 0
    return resp


@router.get("/{module_id}/lessons", response_model=List[dict])
async def get_module_lessons(
    module_id: UUID,
    current_user: User = Depends(get_current_user_dependency),
    db: AsyncSession = Depends(get_db),
) -> List[dict]:
    """Get all lessons in a module with user progress."""
    result = await db.execute(
        select(Module).where(Module.id == module_id)
    )
    module = result.scalar_one_or_none()

    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Module not found",
        )

    # Check access
    license_manager = get_license_manager()
    user_tier = UserRole.FREE
    for license_obj in current_user.licenses:
        valid, _ = license_manager.validate_license(license_obj)
        if valid:
            user_tier = license_obj.tier
            break

    accessible_tiers = [UserRole.FREE]
    if user_tier == UserRole.PRO:
        accessible_tiers.append(UserRole.PRO)
    elif user_tier == UserRole.INSTITUTIONAL:
        accessible_tiers.extend([UserRole.PRO, UserRole.INSTITUTIONAL])

    if module.required_tier not in accessible_tiers:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Module requires higher tier",
        )

    # Get lessons with progress
    from app.db.models import UserProgress
    result = await db.execute(
        select(Lesson, UserProgress)
        .outerjoin(
            UserProgress,
            (UserProgress.lesson_id == Lesson.id) & (UserProgress.user_id == current_user.id)
        )
        .where(Lesson.module_id == module_id)
        .order_by(Lesson.order)
    )
    lessons_with_progress = result.all()

    lessons_data = []
    for lesson, progress in lessons_with_progress:
        lesson_data = {
            "id": str(lesson.id),
            "slug": lesson.slug,
            "title": lesson.title,
            "description": lesson.description,
            "lesson_type": lesson.lesson_type,
            "order": lesson.order,
            "estimated_minutes": lesson.estimated_minutes,
            "is_published": lesson.is_published,
            "progress": {
                "status": progress.status if progress else "not_started",
                "score": progress.score if progress else None,
                "completed_at": progress.completed_at.isoformat() if progress and progress.completed_at else None,
            } if progress else {"status": "not_started"},
        }
        lessons_data.append(lesson_data)

    return lessons_data


# Admin endpoints
@router.post("", response_model=ModuleResponse, status_code=status.HTTP_201_CREATED)
async def create_module(
    module_data: ModuleCreate,
    current_user: User = Depends(get_current_user_dependency),
    db: AsyncSession = Depends(get_db),
) -> ModuleResponse:
    """Create a new module (admin only)."""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    # Check slug uniqueness
    result = await db.execute(select(Module).where(Module.slug == module_data.slug))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Module slug already exists",
        )

    module = Module(**module_data.model_dump())
    db.add(module)
    await db.commit()
    await db.refresh(module)

    resp = ModuleResponse.model_validate(module)
    resp.lessons_count = 0
    return resp


@router.patch("/{module_id}", response_model=ModuleResponse)
async def update_module(
    module_id: UUID,
    module_update: ModuleUpdate,
    current_user: User = Depends(get_current_user_dependency),
    db: AsyncSession = Depends(get_db),
) -> ModuleResponse:
    """Update a module (admin only)."""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    result = await db.execute(select(Module).where(Module.id == module_id))
    module = result.scalar_one_or_none()

    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Module not found",
        )

    update_data = module_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(module, field, value)

    await db.commit()
    await db.refresh(module)

    lessons_count = await db.scalar(
        select(func.count(Lesson.id)).where(Lesson.module_id == module.id)
    )
    resp = ModuleResponse.model_validate(module)
    resp.lessons_count = lessons_count or 0
    return resp


@router.delete("/{module_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_module(
    module_id: UUID,
    current_user: User = Depends(get_current_user_dependency),
    db: AsyncSession = Depends(get_db),
) -> None:
    """Delete a module (admin only)."""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    result = await db.execute(select(Module).where(Module.id == module_id))
    module = result.scalar_one_or_none()

    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Module not found",
        )

    await db.delete(module)
    await db.commit()