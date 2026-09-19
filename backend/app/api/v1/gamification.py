"""Gamification API endpoints - XP, badges, challenges, leaderboard, tutorials."""

from datetime import datetime, timezone
from uuid import UUID
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.db.models import User
from app.db.gamification_models import (
    Badge,
    UserBadge,
    DailyChallenge,
    PatternGame,
    PatternGameAttempt,
    Tutorial,
    UserTutorial,
    ChallengeType,
)
from app.api.v1.auth import get_current_user_dependency
from app.core.gamification import get_gamification_service

router = APIRouter(prefix="/gamification", tags=["gamification"])


# ===== XP & Profile =====

@router.get("/profile")
async def get_gamification_profile(
    current_user: User = Depends(get_current_user_dependency),
) -> dict:
    """Get complete gamification profile for current user."""
    service = get_gamification_service()
    return await service.get_user_profile(current_user.id)


@router.post("/login/track")
async def track_daily_login(
    current_user: User = Depends(get_current_user_dependency),
) -> dict:
    """Track daily login and claim reward."""
    service = get_gamification_service()
    return await service.track_login(current_user.id)


@router.get("/xp/history")
async def get_xp_history(
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user_dependency),
    db: AsyncSession = Depends(get_db),
) -> list[dict]:
    """Get user's XP transaction history."""
    from app.db.gamification_models import XPTransaction

    result = await db.execute(
        select(XPTransaction)
        .where(XPTransaction.user_id == current_user.id)
        .order_by(XPTransaction.created_at.desc())
        .limit(limit)
    )
    transactions = result.scalars().all()

    return [
        {
            "id": str(t.id),
            "amount": t.amount,
            "source": t.source,
            "description": t.description,
            "created_at": t.created_at.isoformat(),
        }
        for t in transactions
    ]


# ===== Badges =====

@router.get("/badges")
async def list_all_badges(
    current_user: User = Depends(get_current_user_dependency),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """List all badges with earned status."""
    result = await db.execute(select(Badge))
    all_badges = result.scalars().all()

    result = await db.execute(
        select(UserBadge).where(UserBadge.user_id == current_user.id)
    )
    user_badges = {ub.badge_id: ub for ub in result.scalars().all()}

    badges = []
    for badge in all_badges:
        earned = badge.id in user_badges
        badges.append({
            "id": str(badge.id),
            "code": badge.code,
            "name": badge.name,
            "description": badge.description,
            "category": badge.category.value,
            "tier": badge.tier.value,
            "icon_emoji": badge.icon_emoji,
            "xp_reward": badge.xp_reward,
            "is_secret": badge.is_secret,
            "earned": earned,
            "earned_at": user_badges[badge.id].earned_at.isoformat() if earned else None,
        })

    earned_count = sum(1 for b in badges if b["earned"])
    return {
        "badges": badges,
        "total": len(badges),
        "earned": earned_count,
        "completion_pct": round(earned_count / len(badges) * 100, 1) if badges else 0,
    }


# ===== Challenges =====

@router.get("/challenges")
async def get_daily_challenges(
    current_user: User = Depends(get_current_user_dependency),
    db: AsyncSession = Depends(get_db),
) -> list[dict]:
    """Get today's active challenges with user progress."""
    service = get_gamification_service()
    profile = await service.get_user_profile(current_user.id)
    return profile.get("challenges", [])


@router.post("/challenges/{challenge_id}/progress")
async def update_challenge_progress(
    challenge_id: UUID,
    increment: int = Query(1, ge=1, le=10),
    current_user: User = Depends(get_current_user_dependency),
) -> dict:
    """Manually update challenge progress."""
    service = get_gamification_service()
    from app.db.gamification_models import ChallengeType

    # Find challenge
    async with get_db() as db:
        result = await db.execute(
            select(DailyChallenge).where(DailyChallenge.id == challenge_id)
        )
        challenge = result.scalar_one_or_none()
        if not challenge:
            raise HTTPException(status_code=404, detail="Challenge not found")

    return await service.update_challenge_progress(
        current_user.id, challenge.challenge_type, increment
    )


# ===== Leaderboard =====

@router.get("/leaderboard")
async def get_leaderboard(
    category: str = Query("xp", regex="^(xp|trades|quiz|streak)$"),
    period: str = Query("weekly", regex="^(daily|weekly|monthly|all_time)$"),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_user_dependency),
) -> dict:
    """Get leaderboard entries."""
    service = get_gamification_service()
    entries = await service.get_leaderboard(category, period, limit)

    # Find current user's rank
    my_rank = None
    my_entry = None
    for entry in entries:
        if entry["user_id"] == str(current_user.id):
            my_rank = entry["rank"]
            my_entry = entry
            break

    return {
        "category": category,
        "period": period,
        "entries": entries,
        "my_rank": my_rank,
        "my_entry": my_entry,
    }


# ===== Tutorials =====

@router.get("/tutorials")
async def list_tutorials(
    category: Optional[str] = None,
    current_user: User = Depends(get_current_user_dependency),
    db: AsyncSession = Depends(get_db),
) -> list[dict]:
    """List available tutorials with progress."""
    query = select(Tutorial).where(Tutorial.is_published == True).order_by(Tutorial.order)
    if category:
        query = query.where(Tutorial.category == category)

    result = await db.execute(query)
    tutorials = result.scalars().all()

    result = await db.execute(
        select(UserTutorial).where(UserTutorial.user_id == current_user.id)
    )
    user_tutorials = {ut.tutorial_id: ut for ut in result.scalars().all()}

    items = []
    for tutorial in tutorials:
        progress = user_tutorials.get(tutorial.id)
        items.append({
            "id": str(tutorial.id),
            "slug": tutorial.slug,
            "title": tutorial.title,
            "description": tutorial.description,
            "category": tutorial.category,
            "difficulty": tutorial.difficulty,
            "estimated_minutes": tutorial.estimated_minutes,
            "xp_reward": tutorial.xp_reward,
            "step_count": len(tutorial.steps),
            "current_step": progress.current_step if progress else 0,
            "is_completed": progress.is_completed if progress else False,
        })

    return items


@router.get("/tutorials/{tutorial_id}")
async def get_tutorial(
    tutorial_id: UUID,
    current_user: User = Depends(get_current_user_dependency),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Get tutorial content."""
    result = await db.execute(select(Tutorial).where(Tutorial.id == tutorial_id))
    tutorial = result.scalar_one_or_none()

    if not tutorial:
        raise HTTPException(status_code=404, detail="Tutorial not found")

    result = await db.execute(
        select(UserTutorial).where(
            (UserTutorial.user_id == current_user.id)
            & (UserTutorial.tutorial_id == tutorial_id)
        )
    )
    progress = result.scalar_one_or_none()

    return {
        "id": str(tutorial.id),
        "slug": tutorial.slug,
        "title": tutorial.title,
        "description": tutorial.description,
        "category": tutorial.category,
        "difficulty": tutorial.difficulty,
        "steps": tutorial.steps,
        "estimated_minutes": tutorial.estimated_minutes,
        "xp_reward": tutorial.xp_reward,
        "current_step": progress.current_step if progress else 0,
        "is_completed": progress.is_completed if progress else False,
    }


@router.post("/tutorials/{tutorial_id}/complete")
async def complete_tutorial(
    tutorial_id: UUID,
    current_user: User = Depends(get_current_user_dependency),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Mark tutorial as completed and award XP."""
    result = await db.execute(select(Tutorial).where(Tutorial.id == tutorial_id))
    tutorial = result.scalar_one_or_none()

    if not tutorial:
        raise HTTPException(status_code=404, detail="Tutorial not found")

    result = await db.execute(
        select(UserTutorial).where(
            (UserTutorial.user_id == current_user.id)
            & (UserTutorial.tutorial_id == tutorial_id)
        )
    )
    progress = result.scalar_one_or_none()

    if progress and progress.is_completed:
        raise HTTPException(status_code=400, detail="Tutorial already completed")

    if not progress:
        progress = UserTutorial(user_id=current_user.id, tutorial_id=tutorial_id)
        db.add(progress)

    progress.is_completed = True
    progress.completed_at = datetime.now(timezone.utc)
    progress.current_step = len(tutorial.steps)
    await db.commit()

    # Award XP
    service = get_gamification_service()
    xp_result = await service.award_xp(
        current_user.id,
        tutorial.xp_reward,
        "tutorial",
        f"Completed tutorial: {tutorial.slug}",
        tutorial_id,
    )

    return {"completed": True, "xp_result": xp_result}


# ===== Pattern Games =====

@router.get("/pattern-games")
async def list_pattern_games(
    difficulty: Optional[int] = None,
    current_user: User = Depends(get_current_user_dependency),
    db: AsyncSession = Depends(get_db),
) -> list[dict]:
    """List available pattern recognition games."""
    query = select(PatternGame).where(PatternGame.is_published == True)
    if difficulty:
        query = query.where(PatternGame.difficulty == difficulty)

    result = await db.execute(query)
    games = result.scalars().all()

    # Get user's attempt history
    result = await db.execute(
        select(PatternGameAttempt).where(PatternGameAttempt.user_id == current_user.id)
    )
    attempts = {}
    for att in result.scalars().all():
        if att.game_id not in attempts:
            attempts[att.game_id] = {"attempts": 0, "correct": 0}

    items = []
    for game in games:
        user_attempts = attempts.get(game.id, {"attempts": 0, "correct": 0})
        items.append({
            "id": str(game.id),
            "slug": game.slug,
            "title": game.title,
            "description": game.description,
            "difficulty": game.difficulty,
            "pattern_type": game.pattern_type,
            "xp_reward": game.xp_reward,
            "my_attempts": user_attempts["attempts"],
            "my_correct": user_attempts["correct"],
        })

    return items


@router.get("/pattern-games/{game_id}")
async def get_pattern_game(
    game_id: UUID,
    current_user: User = Depends(get_current_user_dependency),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Get pattern game with chart data (without revealing answer)."""
    result = await db.execute(select(PatternGame).where(PatternGame.id == game_id))
    game = result.scalar_one_or_none()

    if not game:
        raise HTTPException(status_code=404, detail="Pattern game not found")

    return {
        "id": str(game.id),
        "title": game.title,
        "description": game.description,
        "difficulty": game.difficulty,
        "chart_data": game.chart_data,
        "options": game.options,
        "xp_reward": game.xp_reward,
        # Note: correct_answer and explanation NOT included until after submission
    }


@router.post("/pattern-games/{game_id}/answer")
async def submit_pattern_answer(
    game_id: UUID,
    user_answer: str,
    time_taken_seconds: int = 0,
    current_user: User = Depends(get_current_user_dependency),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Submit pattern game answer."""
    result = await db.execute(select(PatternGame).where(PatternGame.id == game_id))
    game = result.scalar_one_or_none()

    if not game:
        raise HTTPException(status_code=404, detail="Pattern game not found")

    is_correct = user_answer == game.correct_answer
    xp_earned = game.xp_reward if is_correct else 0

    # Record attempt
    attempt = PatternGameAttempt(
        user_id=current_user.id,
        game_id=game_id,
        user_answer=user_answer,
        is_correct=is_correct,
        time_taken_seconds=time_taken_seconds,
        xp_earned=xp_earned,
    )
    db.add(attempt)
    await db.commit()

    # Award XP if correct
    if is_correct:
        service = get_gamification_service()
        await service.award_xp(
            current_user.id,
            xp_earned,
            "pattern_game",
            f"Correct pattern identification: {game.pattern_type}",
            game_id,
        )

    return {
        "is_correct": is_correct,
        "correct_answer": game.correct_answer,
        "explanation": game.explanation,
        "xp_earned": xp_earned,
    }


# ===== Economic Calendar =====

@router.get("/economic-calendar")
async def get_economic_calendar(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    impact: Optional[str] = None,
    limit: int = Query(50, ge=1, le=200),
    current_user: User = Depends(get_current_user_dependency),
    db: AsyncSession = Depends(get_db),
) -> list[dict]:
    """Get economic calendar events."""
    from app.db.gamification_models import EconomicEvent
    from datetime import datetime

    query = select(EconomicEvent).where(EconomicEvent.is_published == True)

    if start_date:
        start = datetime.fromisoformat(start_date.replace("Z", "+00:00"))
        query = query.where(EconomicEvent.event_date >= start)
    if end_date:
        end = datetime.fromisoformat(end_date.replace("Z", "+00:00"))
        query = query.where(EconomicEvent.event_date <= end)
    if impact:
        query = query.where(EconomicEvent.impact == impact)

    query = query.order_by(EconomicEvent.event_date).limit(limit)
    result = await db.execute(query)
    events = result.scalars().all()

    return [
        {
            "id": str(e.id),
            "title": e.title,
            "title_fa": e.title_fa,
            "title_de": e.title_de,
            "country": e.country,
            "impact": e.impact,
            "event_date": e.event_date.isoformat(),
            "actual": e.actual_value,
            "forecast": e.forecast_value,
            "previous": e.previous_value,
            "currency": e.currency,
        }
        for e in events
    ]


# ===== News Feed =====

@router.get("/news")
async def get_news_feed(
    category: Optional[str] = None,
    limit: int = Query(30, ge=1, le=100),
    current_user: User = Depends(get_current_user_dependency),
    db: AsyncSession = Depends(get_db),
) -> list[dict]:
    """Get trading news feed."""
    from app.db.gamification_models import NewsItem

    query = select(NewsItem).where(NewsItem.is_published == True)
    if category:
        query = query.where(NewsItem.category == category)

    query = query.order_by(NewsItem.published_at.desc()).limit(limit)
    result = await db.execute(query)
    items = result.scalars().all()

    return [
        {
            "id": str(n.id),
            "title": n.title,
            "title_fa": n.title_fa,
            "title_de": n.title_de,
            "summary": n.summary,
            "source": n.source,
            "source_url": n.source_url,
            "image_url": n.image_url,
            "category": n.category,
            "sentiment": n.sentiment,
            "related_symbols": n.related_symbols,
            "importance": n.importance,
            "published_at": n.published_at.isoformat(),
        }
        for n in items
    ]
