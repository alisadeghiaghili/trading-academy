"""User progress endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from uuid import UUID
from datetime import datetime, timezone

from app.db.session import get_db
from app.db.models import UserProgress, Lesson, User
from app.schemas import ProgressUpdate, ProgressResponse, PaginatedResponse, PageParams
from app.api.v1.auth import get_current_user_dependency

router = APIRouter(prefix="/progress", tags=["progress"])


@router.get("", response_model=PaginatedResponse[ProgressResponse])
async def list_progress(
    params: PageParams = Depends(),
    status_filter: str | None = None,
    current_user: User = Depends(get_current_user_dependency),
    db: AsyncSession = Depends(get_db),
) -> PaginatedResponse[ProgressResponse]:
    """List current user's lesson progress."""
    query = select(UserProgress).where(UserProgress.user_id == current_user.id)

    if status_filter:
        query = query.where(UserProgress.status == status_filter)

    query = query.order_by(UserProgress.updated_at.desc())

    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    total = await db.scalar(count_query)

    # Paginate
    query = query.offset((params.page - 1) * params.page_size).limit(params.page_size)
    result = await db.execute(query)
    progress_list = result.scalars().all()

    return PaginatedResponse.create(
        items=[ProgressResponse.model_validate(p) for p in progress_list],
        total=total,
        params=params,
    )


@router.get("/lesson/{lesson_id}", response_model=ProgressResponse | None)
async def get_lesson_progress(
    lesson_id: UUID,
    current_user: User = Depends(get_current_user_dependency),
    db: AsyncSession = Depends(get_db),
) -> ProgressResponse | None:
    """Get progress for a specific lesson."""
    result = await db.execute(
        select(UserProgress).where(
            (UserProgress.user_id == current_user.id) &
            (UserProgress.lesson_id == lesson_id)
        )
    )
    progress = result.scalar_one_or_none()

    if not progress:
        return None

    return ProgressResponse.model_validate(progress)


@router.post("/lesson/{lesson_id}/start", response_model=ProgressResponse)
async def start_lesson(
    lesson_id: UUID,
    current_user: User = Depends(get_current_user_dependency),
    db: AsyncSession = Depends(get_db),
) -> ProgressResponse:
    """Start a lesson (mark as in_progress)."""
    # Verify lesson exists
    result = await db.execute(select(Lesson).where(Lesson.id == lesson_id))
    lesson = result.scalar_one_or_none()

    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found",
        )

    # Get or create progress
    result = await db.execute(
        select(UserProgress).where(
            (UserProgress.user_id == current_user.id) &
            (UserProgress.lesson_id == lesson_id)
        )
    )
    progress = result.scalar_one_or_none()

    if not progress:
        progress = UserProgress(
            user_id=current_user.id,
            lesson_id=lesson_id,
            status="in_progress",
        )
        db.add(progress)
    elif progress.status == "not_started":
        progress.status = "in_progress"

    progress.updated_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(progress)

    return ProgressResponse.model_validate(progress)


@router.patch("/lesson/{lesson_id}", response_model=ProgressResponse)
async def update_progress(
    lesson_id: UUID,
    progress_update: ProgressUpdate,
    current_user: User = Depends(get_current_user_dependency),
    db: AsyncSession = Depends(get_db),
) -> ProgressResponse:
    """Update lesson progress."""
    result = await db.execute(
        select(UserProgress).where(
            (UserProgress.user_id == current_user.id) &
            (UserProgress.lesson_id == lesson_id)
        )
    )
    progress = result.scalar_one_or_none()

    if not progress:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Progress not found. Start the lesson first.",
        )

    update_data = progress_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(progress, field, value)

    # Auto-complete if score >= 70% for quiz
    if progress_update.score is not None and progress_update.score >= 70:
        progress.status = "completed"
        progress.completed_at = datetime.now(timezone.utc)

    progress.updated_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(progress)

    return ProgressResponse.model_validate(progress)


@router.post("/lesson/{lesson_id}/complete", response_model=ProgressResponse)
async def complete_lesson(
    lesson_id: UUID,
    score: float | None = None,
    time_spent: int = 0,
    current_user: User = Depends(get_current_user_dependency),
    db: AsyncSession = Depends(get_db),
) -> ProgressResponse:
    """Mark lesson as completed."""
    result = await db.execute(
        select(UserProgress).where(
            (UserProgress.user_id == current_user.id) &
            (UserProgress.lesson_id == lesson_id)
        )
    )
    progress = result.scalar_one_or_none()

    if not progress:
        progress = UserProgress(
            user_id=current_user.id,
            lesson_id=lesson_id,
        )
        db.add(progress)

    progress.status = "completed"
    progress.completed_at = datetime.now(timezone.utc)
    if score is not None:
        progress.score = score
    progress.time_spent_seconds += time_spent
    progress.updated_at = datetime.now(timezone.utc)

    await db.commit()
    await db.refresh(progress)

    return ProgressResponse.model_validate(progress)


@router.get("/stats/summary")
async def get_progress_summary(
    current_user: User = Depends(get_current_user_dependency),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Get user's progress summary."""
    from app.db.models import Module

    # Total modules/lessons
    total_modules = await db.scalar(select(func.count(Module.id)).where(Module.is_published == True))
    total_lessons = await db.scalar(select(func.count(Lesson.id)).where(Lesson.is_published == True))

    # Completed lessons
    completed_lessons = await db.scalar(
        select(func.count(UserProgress.id)).where(
            (UserProgress.user_id == current_user.id) &
            (UserProgress.status == "completed")
        )
    )

    # In progress
    in_progress_lessons = await db.scalar(
        select(func.count(UserProgress.id)).where(
            (UserProgress.user_id == current_user.id) &
            (UserProgress.status == "in_progress")
        )
    )

    # Total time spent
    total_time = await db.scalar(
        select(func.sum(UserProgress.time_spent_seconds)).where(
            UserProgress.user_id == current_user.id
        )
    ) or 0

    # Average score
    avg_score = await db.scalar(
        select(func.avg(UserProgress.score)).where(
            (UserProgress.user_id == current_user.id) &
            (UserProgress.score.isnot(None))
        )
    )

    return {
        "total_modules": total_modules or 0,
        "total_lessons": total_lessons or 0,
        "completed_lessons": completed_lessons or 0,
        "in_progress_lessons": in_progress_lessons or 0,
        "completion_rate": (completed_lessons / total_lessons * 100) if total_lessons else 0,
        "total_time_hours": round(total_time / 3600, 2),
        "average_score": round(avg_score, 2) if avg_score else 0,
    }