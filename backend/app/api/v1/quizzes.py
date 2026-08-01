"""Quiz endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from uuid import UUID
from typing import List

from app.db.session import get_db
from app.db.models import QuizQuestion, QuizAttempt, Lesson, User
from app.schemas import QuizAttemptCreate, QuizAttemptResponse
from app.api.v1.auth import get_current_user_dependency

router = APIRouter(prefix="/quizzes", tags=["quizzes"])


@router.post("/attempt", response_model=QuizAttemptResponse)
async def submit_quiz_attempt(
    attempt: QuizAttemptCreate,
    current_user: User = Depends(get_current_user_dependency),
    db: AsyncSession = Depends(get_db),
) -> QuizAttemptResponse:
    """Submit a quiz answer."""
    # Get question
    result = await db.execute(
        select(QuizQuestion).where(QuizQuestion.id == attempt.question_id)
    )
    question = result.scalar_one_or_none()

    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found",
        )

    # Check if lesson is accessible
    result = await db.execute(
        select(Lesson).where(Lesson.id == question.lesson_id)
    )
    lesson = result.scalar_one_or_none()

    if not lesson or not lesson.is_published:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Lesson not accessible",
        )

    # Check answer
    is_correct = False
    if question.question_type == "single_choice":
        correct = question.correct_answer.get("option_id")
        user_answer = attempt.user_answer.get("option_id")
        is_correct = correct == user_answer
    elif question.question_type == "multiple_choice":
        correct = set(question.correct_answer.get("option_ids", []))
        user_answer = set(attempt.user_answer.get("option_ids", []))
        is_correct = correct == user_answer
    elif question.question_type == "true_false":
        correct = question.correct_answer.get("value")
        user_answer = attempt.user_answer.get("value")
        is_correct = correct == user_answer
    elif question.question_type == "numeric":
        correct = question.correct_answer.get("value")
        user_answer = attempt.user_answer.get("value")
        tolerance = question.correct_answer.get("tolerance", 0.01)
        is_correct = abs(correct - user_answer) <= tolerance

    # Create attempt record
    quiz_attempt = QuizAttempt(
        user_id=current_user.id,
        question_id=question.id,
        user_answer=attempt.user_answer,
        is_correct=is_correct,
        time_spent_seconds=attempt.time_spent_seconds,
    )
    db.add(quiz_attempt)
    await db.commit()
    await db.refresh(quiz_attempt)

    return QuizAttemptResponse(
        id=quiz_attempt.id,
        user_id=quiz_attempt.user_id,
        question_id=quiz_attempt.question_id,
        user_answer=quiz_attempt.user_answer,
        is_correct=quiz_attempt.is_correct,
        time_spent_seconds=quiz_attempt.time_spent_seconds,
        attempted_at=quiz_attempt.attempted_at,
    )


@router.get("/lesson/{lesson_id}/questions", response_model=List[dict])
async def get_lesson_questions(
    lesson_id: UUID,
    current_user: User = Depends(get_current_user_dependency),
    db: AsyncSession = Depends(get_db),
) -> List[dict]:
    """Get all quiz questions for a lesson (without correct answers)."""
    result = await db.execute(
        select(Lesson).where(Lesson.id == lesson_id)
    )
    lesson = result.scalar_one_or_none()

    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found",
        )

    result = await db.execute(
        select(QuizQuestion)
        .where(QuizQuestion.lesson_id == lesson_id)
        .order_by(QuizQuestion.order)
    )
    questions = result.scalars().all()

    return [
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


@router.get("/lesson/{lesson_id}/results")
async def get_lesson_quiz_results(
    lesson_id: UUID,
    current_user: User = Depends(get_current_user_dependency),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Get quiz results for a lesson."""
    # Get all questions for lesson
    result = await db.execute(
        select(QuizQuestion).where(QuizQuestion.lesson_id == lesson_id)
    )
    questions = result.scalars().all()

    if not questions:
        return {"total": 0, "correct": 0, "score": 0, "attempts": []}

    # Get user attempts
    question_ids = [q.id for q in questions]
    result = await db.execute(
        select(QuizAttempt).where(
            (QuizAttempt.user_id == current_user.id) &
            (QuizAttempt.question_id.in_(question_ids))
        )
    )
    attempts = result.scalars().all()

    # Get latest attempt per question
    latest_attempts = {}
    for attempt in attempts:
        if attempt.question_id not in latest_attempts or \
           attempt.attempted_at > latest_attempts[attempt.question_id].attempted_at:
            latest_attempts[attempt.question_id] = attempt

    correct_count = sum(1 for a in latest_attempts.values() if a.is_correct)
    total = len(questions)

    return {
        "total": total,
        "correct": correct_count,
        "score": round(correct_count / total * 100, 2) if total > 0 else 0,
        "attempts": [
            {
                "question_id": str(q.id),
                "question_text": q.question_text,
                "user_answer": latest_attempts.get(q.id).user_answer if q.id in latest_attempts else None,
                "is_correct": latest_attempts.get(q.id).is_correct if q.id in latest_attempts else False,
                "explanation": q.explanation if q.id in latest_attempts and not latest_attempts[q.id].is_correct else None,
            }
            for q in questions
        ]
    }


@router.get("/stats/overall")
async def get_quiz_stats(
    current_user: User = Depends(get_current_user_dependency),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Get overall quiz statistics for user."""
    # Total attempts
    total_attempts = await db.scalar(
        select(func.count(QuizAttempt.id)).where(QuizAttempt.user_id == current_user.id)
    ) or 0

    # Correct attempts
    correct_attempts = await db.scalar(
        select(func.count(QuizAttempt.id)).where(
            (QuizAttempt.user_id == current_user.id) &
            (QuizAttempt.is_correct == True)
        )
    ) or 0

    # By difficulty
    from app.db.models import QuizQuestion
    result = await db.execute(
        select(QuizQuestion.difficulty, func.count(QuizAttempt.id), func.sum(QuizAttempt.is_correct.cast(int)))
        .join(QuizAttempt, QuizAttempt.question_id == QuizQuestion.id)
        .where(QuizAttempt.user_id == current_user.id)
        .group_by(QuizQuestion.difficulty)
    )
    by_difficulty = {}
    for difficulty, total, correct in result.all():
        by_difficulty[difficulty] = {
            "total": total,
            "correct": correct or 0,
            "accuracy": round((correct or 0) / total * 100, 2) if total > 0 else 0,
        }

    return {
        "total_attempts": total_attempts,
        "correct_attempts": correct_attempts,
        "overall_accuracy": round(correct_attempts / total_attempts * 100, 2) if total_attempts > 0 else 0,
        "by_difficulty": by_difficulty,
    }