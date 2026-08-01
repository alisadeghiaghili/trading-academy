"""Lesson management endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from uuid import UUID
from typing import List, Optional

from app.db.session import get_db
from app.db.models import Lesson, Module, User, UserProgress, UserRole, LessonType
from app.schemas import (
    LessonCreate,
    LessonUpdate,
    LessonResponse,
    LessonWithProgress,
    PaginatedResponse,
    PageParams,
)
from app.api.v1.auth import get_current_user_dependency
from app.core.licensing import get_license_manager

router = APIRouter(prefix="/lessons", tags=["lessons"])


@router.get("/{lesson_id}", response_model=LessonWithProgress)
async def get_lesson(
    lesson_id: UUID,
    current_user: User = Depends(get_current_user_dependency),
    db: AsyncSession = Depends(get_db),
) -> LessonWithProgress:
    """Get lesson by ID with user progress."""
    result = await db.execute(
        select(Lesson)
        .options(selectinload(Lesson.module))
        .where(Lesson.id == lesson_id)
    )
    lesson = result.scalar_one_or_none()

    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found",
        )

    # Check access
    if not lesson.is_published and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found",
        )

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

    if lesson.required_tier not in accessible_tiers:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Lesson requires higher tier",
        )

    # Get user progress
    result = await db.execute(
        select(UserProgress).where(
            (UserProgress.user_id == current_user.id) &
            (UserProgress.lesson_id == lesson_id)
        )
    )
    progress = result.scalar_one_or_none()

    lesson_resp = LessonResponse.model_validate(lesson)
    progress_data = None
    if progress:
        progress_data = {
            "status": progress.status,
            "score": progress.score,
            "completed_at": progress.completed_at.isoformat() if progress.completed_at else None,
            "time_spent_seconds": progress.time_spent_seconds,
        }

    return LessonWithProgress(
        **lesson_resp.model_dump(),
        progress=progress_data,
    )


@router.get("/{lesson_id}/content", response_model=dict)
async def get_lesson_content(
    lesson_id: UUID,
    current_user: User = Depends(get_current_user_dependency),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Get lesson content (notebook, quiz questions, etc.)."""
    result = await db.execute(
        select(Lesson).where(Lesson.id == lesson_id)
    )
    lesson = result.scalar_one_or_none()

    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found",
        )

    if not lesson.is_published and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found",
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

    if lesson.required_tier not in accessible_tiers:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Lesson requires higher tier",
        )

    # Return lesson content based on type
    content = lesson.content or {}

    if lesson.lesson_type == LessonType.QUIZ:
        # Get quiz questions
        from app.db.models import QuizQuestion
        result = await db.execute(
            select(QuizQuestion)
            .where(QuizQuestion.lesson_id == lesson_id)
            .order_by(QuizQuestion.order)
        )
        questions = result.scalars().all()
        content["questions"] = [
            {
                "id": str(q.id),
                "question_text": q.question_text,
                "question_type": q.question_type,
                "options": q.options,
                "difficulty": q.difficulty,
                "order": q.order,
            }
            for q in questions
        ]

    return content


# Admin endpoints
@router.post("", response_model=LessonResponse, status_code=status.HTTP_201_CREATED)
async def create_lesson(
    lesson_data: LessonCreate,
    current_user: User = Depends(get_current_user_dependency),
    db: AsyncSession = Depends(get_db),
) -> LessonResponse:
    """Create a new lesson (admin only)."""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    # Verify module exists
    result = await db.execute(select(Module).where(Module.id == lesson_data.module_id))
    module = result.scalar_one_or_none()
    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Module not found",
        )

    # Check slug uniqueness within module
    result = await db.execute(
        select(Lesson).where(
            (Lesson.module_id == lesson_data.module_id) &
            (Lesson.slug == lesson_data.slug)
        )
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Lesson slug already exists in this module",
        )

    lesson = Lesson(**lesson_data.model_dump())
    db.add(lesson)
    await db.commit()
    await db.refresh(lesson)

    return LessonResponse.model_validate(lesson)


@router.patch("/{lesson_id}", response_model=LessonResponse)
async def update_lesson(
    lesson_id: UUID,
    lesson_update: LessonUpdate,
    current_user: User = Depends(get_current_user_dependency),
    db: AsyncSession = Depends(get_db),
) -> LessonResponse:
    """Update a lesson (admin only)."""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    result = await db.execute(select(Lesson).where(Lesson.id == lesson_id))
    lesson = result.scalar_one_or_none()

    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found",
        )

    update_data = lesson_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(lesson, field, value)

    await db.commit()
    await db.refresh(lesson)

    return LessonResponse.model_validate(lesson)


@router.delete("/{lesson_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_lesson(
    lesson_id: UUID,
    current_user: User = Depends(get_current_user_dependency),
    db: AsyncSession = Depends(get_db),
) -> None:
    """Delete a lesson (admin only)."""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    result = await db.execute(select(Lesson).where(Lesson.id == lesson_id))
    lesson = result.scalar_one_or_none()

    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found",
        )

    await db.delete(lesson)
    await db.commit()