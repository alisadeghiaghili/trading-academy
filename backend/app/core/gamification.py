"""Gamification service - XP, levels, badges, challenges, daily rewards."""

from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_context
from app.db.gamification_models import (
    Badge,
    UserBadge,
    UserXP,
    XPTransaction,
    DailyChallenge,
    UserChallenge,
    DailyReward,
    LeaderboardEntry,
    ChallengeType,
    AchievementCategory,
    BadgeTier,
    UserLevel,
)


# XP rewards for different activities
XP_REWARDS = {
    "lesson_started": 10,
    "lesson_completed": 50,
    "quiz_attempted": 5,
    "quiz_perfect": 100,
    "quiz_passed": 30,
    "trade_placed": 20,
    "trade_profitable": 40,
    "trade_reviewed": 15,
    "tutorial_completed": 50,
    "pattern_game_correct": 30,
    "daily_login": 20,
    "daily_challenge_complete": 100,
    "streak_bonus_day_3": 30,
    "streak_bonus_day_7": 100,
    "streak_bonus_day_30": 500,
    "module_completed": 200,
    "first_trade": 100,
    "coaching_review": 25,
}

# Level thresholds
LEVEL_THRESHOLDS = {
    1: {"xp": 0, "title": UserLevel.BEGINNER},
    2: {"xp": 100, "title": UserLevel.NOVICE},
    3: {"xp": 300, "title": UserLevel.NOVICE},
    4: {"xp": 600, "title": UserLevel.INTERMEDIATE},
    5: {"xp": 1000, "title": UserLevel.INTERMEDIATE},
    6: {"xp": 1500, "title": UserLevel.INTERMEDIATE},
    7: {"xp": 2200, "title": UserLevel.ADVANCED},
    8: {"xp": 3000, "title": UserLevel.ADVANCED},
    9: {"xp": 4000, "title": UserLevel.ADVANCED},
    10: {"xp": 5500, "title": UserLevel.EXPERT},
    11: {"xp": 7000, "title": UserLevel.EXPERT},
    12: {"xp": 9000, "title": UserLevel.EXPERT},
    13: {"xp": 12000, "title": UserLevel.MASTER},
    14: {"xp": 15000, "title": UserLevel.MASTER},
    15: {"xp": 20000, "title": UserLevel.MASTER},
    16: {"xp": 26000, "title": UserLevel.GRANDMASTER},
    17: {"xp": 33000, "title": UserLevel.GRANDMASTER},
    18: {"xp": 42000, "title": UserLevel.GRANDMASTER},
    19: {"xp": 52000, "title": UserLevel.LEGEND},
    20: {"xp": 65000, "title": UserLevel.LEGEND},
}

# Daily reward schedule (day -> xp)
DAILY_REWARDS = {
    1: {"xp": 20, "coins": 5},
    2: {"xp": 30, "coins": 8},
    3: {"xp": 40, "coins": 12, "bonus": True},
    4: {"xp": 50, "coins": 15},
    5: {"xp": 60, "coins": 20},
    6: {"xp": 80, "coins": 25},
    7: {"xp": 100, "coins": 50, "bonus": True},
}


def get_level_for_xp(total_xp: int) -> tuple[int, UserLevel, int]:
    """Calculate level, title, and XP to next level from total XP.

    Args:
        total_xp: Total accumulated XP.

    Returns:
        Tuple of (level, level_title, xp_to_next_level).
    """
    current_level = 1
    current_title = UserLevel.BEGINNER
    xp_to_next = 100

    for level, data in sorted(LEVEL_THRESHOLDS.items()):
        if total_xp >= data["xp"]:
            current_level = level
            current_title = data["title"]
        else:
            xp_to_next = data["xp"] - total_xp
            break

    return current_level, current_title, xp_to_next


class GamificationService:
    """Service for managing gamification features."""

    async def get_or_create_user_xp(self, user_id: UUID, db: AsyncSession) -> UserXP:
        """Get user XP record, creating if it doesn't exist."""
        result = await db.execute(select(UserXP).where(UserXP.user_id == user_id))
        user_xp = result.scalar_one_or_none()

        if not user_xp:
            user_xp = UserXP(user_id=user_id)
            db.add(user_xp)
            await db.commit()
            await db.refresh(user_xp)

        return user_xp

    async def award_xp(
        self,
        user_id: UUID,
        amount: int,
        source: str,
        description: str,
        source_id: Optional[UUID] = None,
    ) -> dict:
        """Award XP to user and handle level-up logic.

        Args:
            user_id: User UUID.
            amount: XP amount to award.
            source: Source of XP (lesson, quiz, trade, etc.).
            description: Description of the XP source.
            source_id: Optional ID of the source entity.

        Returns:
            Dict with new_total_xp, level, level_title, xp_to_next, leveled_up.
        """
        async with get_db_context() as db:
            user_xp = await self.get_or_create_user_xp(user_id, db)

            old_level = user_xp.current_level
            old_title = user_xp.level_title

            user_xp.total_xp += amount
            new_level, new_title, xp_to_next = get_level_for_xp(user_xp.total_xp)

            user_xp.current_level = new_level
            user_xp.level_title = new_title
            user_xp.xp_to_next_level = xp_to_next
            user_xp.updated_at = datetime.now(timezone.utc)

            # Log XP transaction
            transaction = XPTransaction(
                user_id=user_id,
                amount=amount,
                source=source,
                source_id=source_id,
                description=description,
            )
            db.add(transaction)
            await db.commit()

            leveled_up = new_level > old_level or new_title != old_title

            result = {
                "total_xp": user_xp.total_xp,
                "level": new_level,
                "level_title": new_title.value,
                "xp_to_next": xp_to_next,
                "leveled_up": leveled_up,
                "old_level": old_level,
                "old_title": old_title.value,
            }

            # Check for badges on level up
            if leveled_up:
                await self._check_level_badges(user_id, new_level, db)

            return result

    async def track_login(self, user_id: UUID) -> dict:
        """Track daily login and update streak.

        Returns:
            Dict with streak_day, xp_earned, coins_earned, is_new_login.
        """
        async with get_db_context() as db:
            user_xp = await self.get_or_create_user_xp(user_id, db)

            today = datetime.now(timezone.utc).date()

            # Check if already logged in today
            result = await db.execute(
                select(DailyReward)
                .where(
                    (DailyReward.user_id == user_id)
                    & (func.date(DailyReward.reward_date) == today)
                )
            )
            existing = result.scalar_one_or_none()

            if existing:
                return {
                    "streak_day": user_xp.login_streak,
                    "xp_earned": 0,
                    "coins_earned": 0,
                    "is_new_login": False,
                }

            # Check yesterday's login for streak
            yesterday = today - timedelta(days=1)
            result = await db.execute(
                select(DailyReward)
                .where(
                    (DailyReward.user_id == user_id)
                    & (func.date(DailyReward.reward_date) == yesterday)
                )
            )
            yesterday_reward = result.scalar_one_or_none()

            if yesterday_reward:
                user_xp.login_streak += 1
            else:
                user_xp.login_streak = 1

            # Update longest streak
            if user_xp.login_streak > user_xp.longest_login_streak:
                user_xp.longest_login_streak = user_xp.login_streak

            # Determine reward based on streak day
            streak_day = min(user_xp.login_streak, 7)
            reward = DAILY_REWARDS.get(streak_day, DAILY_REWARDS[7])

            # Create daily reward record
            daily_reward = DailyReward(
                user_id=user_id,
                reward_date=datetime.now(timezone.utc),
                streak_day=user_xp.login_streak,
                xp_earned=reward["xp"],
                coin_earned=reward["coins"],
            )
            db.add(daily_reward)

            # Award XP
            user_xp.total_xp += reward["xp"]
            new_level, new_title, xp_to_next = get_level_for_xp(user_xp.total_xp)
            user_xp.current_level = new_level
            user_xp.level_title = new_title
            user_xp.xp_to_next_level = xp_to_next
            user_xp.updated_at = datetime.now(timezone.utc)

            # Log transaction
            transaction = XPTransaction(
                user_id=user_id,
                amount=reward["xp"],
                source="daily_login",
                description=f"Daily login streak day {user_xp.login_streak}",
            )
            db.add(transaction)

            await db.commit()

            # Check streak badges
            await self._check_streak_badges(user_id, user_xp.login_streak, db)

            return {
                "streak_day": user_xp.login_streak,
                "xp_earned": reward["xp"],
                "coins_earned": reward["coins"],
                "is_new_login": True,
                "is_bonus_day": reward.get("bonus", False),
            }

    async def update_challenge_progress(
        self,
        user_id: UUID,
        challenge_type: ChallengeType,
        increment: int = 1,
    ) -> dict:
        """Update user's challenge progress.

        Args:
            user_id: User UUID.
            challenge_type: Type of challenge activity.
            increment: Amount to increment progress.

        Returns:
            Dict with challenge results.
        """
        async with get_db_context() as db:
            today = datetime.now(timezone.utc)
            today_start = today.replace(hour=0, minute=0, second=0, microsecond=0)
            today_end = today_start + timedelta(days=1)

            # Find active challenge of this type for today
            result = await db.execute(
                select(DailyChallenge).where(
                    (DailyChallenge.challenge_type == challenge_type)
                    & (DailyChallenge.is_active == True)
                    & (DailyChallenge.start_date <= today)
                    & (DailyChallenge.end_date >= today)
                )
            )
            challenge = result.scalar_one_or_none()

            if not challenge:
                return {"completed": False, "progress": 0}

            # Find or create user challenge progress
            result = await db.execute(
                select(UserChallenge).where(
                    (UserChallenge.user_id == user_id)
                    & (UserChallenge.challenge_id == challenge.id)
                )
            )
            user_challenge = result.scalar_one_or_none()

            if not user_challenge:
                user_challenge = UserChallenge(
                    user_id=user_id,
                    challenge_id=challenge.id,
                )
                db.add(user_challenge)

            user_challenge.progress += increment
            was_completed = user_challenge.is_completed
            now_completed = user_challenge.progress >= challenge.target

            if now_completed and not was_completed:
                user_challenge.is_completed = True
                user_challenge.completed_at = datetime.now(timezone.utc)
                user_challenge.xp_earned = challenge.xp_reward

                # Award XP
                user_xp = await self.get_or_create_user_xp(user_id, db)
                user_xp.total_xp += challenge.xp_reward
                new_level, new_title, xp_to_next = get_level_for_xp(user_xp.total_xp)
                user_xp.current_level = new_level
                user_xp.level_title = new_title
                user_xp.xp_to_next_level = xp_to_next
                user_xp.updated_at = datetime.now(timezone.utc)

                transaction = XPTransaction(
                    user_id=user_id,
                    amount=challenge.xp_reward,
                    source="challenge",
                    source_id=challenge.id,
                    description=f"Completed challenge: {challenge.challenge_type.value}",
                )
                db.add(transaction)

            await db.commit()

            return {
                "completed": now_completed,
                "newly_completed": now_completed and not was_completed,
                "progress": user_challenge.progress,
                "target": challenge.target,
                "xp_earned": user_challenge.xp_earned if now_completed else 0,
            }

    async def get_user_profile(self, user_id: UUID) -> dict:
        """Get complete gamification profile for user.

        Returns:
            Dict with XP, level, badges, streaks, challenges, leaderboard position.
        """
        async with get_db_context() as db:
            user_xp = await self.get_or_create_user_xp(user_id, db)

            # Get badges
            result = await db.execute(
                select(UserBadge, Badge)
                .join(Badge, Badge.id == UserBadge.badge_id)
                .where(UserBadge.user_id == user_id)
            )
            badges = [
                {
                    "id": str(badge.id),
                    "code": badge.code,
                    "name": badge.name,
                    "description": badge.description,
                    "category": badge.category.value,
                    "tier": badge.tier.value,
                    "icon_emoji": badge.icon_emoji,
                    "xp_reward": badge.xp_reward,
                    "earned_at": ub.earned_at.isoformat(),
                }
                for ub, badge in result.all()
            ]

            # Get active challenges
            today = datetime.now(timezone.utc)
            result = await db.execute(
                select(DailyChallenge, UserChallenge)
                .outerjoin(
                    UserChallenge,
                    (UserChallenge.challenge_id == DailyChallenge.id)
                    & (UserChallenge.user_id == user_id)
                )
                .where(
                    (DailyChallenge.is_active == True)
                    & (DailyChallenge.start_date <= today)
                    & (DailyChallenge.end_date >= today)
                )
            )
            challenges = []
            for challenge, user_ch in result.all():
                progress = user_ch.progress if user_ch else 0
                challenges.append({
                    "id": str(challenge.id),
                    "type": challenge.challenge_type.value,
                    "title": challenge.title,
                    "description": challenge.description,
                    "target": challenge.target,
                    "progress": progress,
                    "is_completed": user_ch.is_completed if user_ch else False,
                    "xp_reward": challenge.xp_reward,
                    "coin_reward": challenge.coin_reward,
                })

            # Get today's daily reward
            today_date = today.date()
            result = await db.execute(
                select(DailyReward)
                .where(
                    (DailyReward.user_id == user_id)
                    & (func.date(DailyReward.reward_date) == today_date)
                )
            )
            today_reward = result.scalar_one_or_none()

            return {
                "xp": {
                    "total_xp": user_xp.total_xp,
                    "current_level": user_xp.current_level,
                    "level_title": user_xp.level_title.value,
                    "xp_to_next_level": user_xp.xp_to_next_level,
                    "progress_pct": round(
                        (user_xp.total_xp / (user_xp.total_xp + user_xp.xp_to_next_level)) * 100, 1
                    ) if (user_xp.total_xp + user_xp.xp_to_next_level) > 0 else 0,
                },
                "stats": {
                    "lessons_completed": user_xp.lessons_completed,
                    "quizzes_passed": user_xp.quizzes_passed,
                    "trades_completed": user_xp.trades_completed,
                    "perfect_quizzes": user_xp.perfect_quizzes,
                    "total_study_time_minutes": user_xp.total_study_time_minutes,
                },
                "streaks": {
                    "login_streak": user_xp.login_streak,
                    "longest_login_streak": user_xp.longest_login_streak,
                    "learning_streak": user_xp.learning_streak,
                    "longest_learning_streak": user_xp.longest_learning_streak,
                },
                "badges": badges,
                "badge_count": len(badges),
                "challenges": challenges,
                "daily_reward_claimed": today_reward is not None,
            }

    async def get_leaderboard(
        self,
        category: str = "xp",
        period: str = "weekly",
        limit: int = 50,
    ) -> list[dict]:
        """Get leaderboard entries.

        Args:
            category: xp, trades, quiz, streak.
            period: daily, weekly, monthly, all_time.
            limit: Max entries to return.

        Returns:
            List of leaderboard entries.
        """
        async with get_db_context() as db:
            now = datetime.now(timezone.utc)

            if period == "daily":
                period_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
                period_end = period_start + timedelta(days=1)
            elif period == "weekly":
                days_since_monday = now.weekday()
                period_start = (now - timedelta(days=days_since_monday)).replace(
                    hour=0, minute=0, second=0, microsecond=0
                )
                period_end = period_start + timedelta(days=7)
            elif period == "monthly":
                period_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                if now.month == 12:
                    period_end = period_start.replace(year=now.year + 1, month=1)
                else:
                    period_end = period_start.replace(month=now.month + 1)
            else:
                period_start = datetime(2020, 1, 1, tzinfo=timezone.utc)
                period_end = datetime(2099, 12, 31, tzinfo=timezone.utc)

            # Get UserXP joined with User for names
            from app.db.models import User

            query = (
                select(UserXP, User)
                .join(User, User.id == UserXP.user_id)
                .where(User.is_active == True)
            )

            if category == "trades":
                query = query.order_by(UserXP.trades_completed.desc())
            elif category == "quiz":
                query = query.order_by(UserXP.quizzes_passed.desc())
            elif category == "streak":
                query = query.order_by(UserXP.login_streak.desc())
            else:
                query = query.order_by(UserXP.total_xp.desc())

            query = query.limit(limit)
            result = await db.execute(query)

            leaderboard = []
            for rank, (user_xp, user) in enumerate(result.all(), 1):
                score = {
                    "xp": user_xp.total_xp,
                    "trades": user_xp.trades_completed,
                    "quiz": user_xp.quizzes_passed,
                    "streak": user_xp.login_streak,
                }.get(category, user_xp.total_xp)

                leaderboard.append({
                    "rank": rank,
                    "user_id": str(user_xp.user_id),
                    "display_name": user.full_name or user.email.split("@")[0],
                    "level": user_xp.current_level,
                    "level_title": user_xp.level_title.value,
                    "score": score,
                    "badge_count": 0,
                })

            return leaderboard

    async def _check_level_badges(self, user_id: UUID, level: int, db: AsyncSession) -> None:
        """Check and award level-based badges."""
        level_badges = {
            5: "level_5_novice",
            10: "level_10_expert",
            15: "level_15_master",
            20: "level_20_legend",
        }

        for required_level, badge_code in level_badges.items():
            if level >= required_level:
                await self._award_badge(user_id, badge_code, db)

    async def _check_streak_badges(self, user_id: UUID, streak: int, db: AsyncSession) -> None:
        """Check and award streak-based badges."""
        streak_badges = {
            3: "streak_3_days",
            7: "streak_7_days",
            14: "streak_14_days",
            30: "streak_30_days",
            100: "streak_100_days",
        }

        for required_streak, badge_code in streak_badges.items():
            if streak >= required_streak:
                await self._award_badge(user_id, badge_code, db)

    async def _award_badge(self, user_id: UUID, badge_code: str, db: AsyncSession) -> bool:
        """Award a badge to user if they don't already have it.

        Returns:
            True if badge was newly awarded.
        """
        # Find badge
        result = await db.execute(select(Badge).where(Badge.code == badge_code))
        badge = result.scalar_one_or_none()

        if not badge:
            return False

        # Check if already earned
        result = await db.execute(
            select(UserBadge).where(
                (UserBadge.user_id == user_id) & (UserBadge.badge_id == badge.id)
            )
        )
        if result.scalar_one_or_none():
            return False

        # Award badge
        user_badge = UserBadge(user_id=user_id, badge_id=badge.id)
        db.add(user_badge)

        # Award badge XP
        if badge.xp_reward > 0:
            transaction = XPTransaction(
                user_id=user_id,
                amount=badge.xp_reward,
                source="badge",
                source_id=badge.id,
                description=f"Earned badge: {badge.code}",
            )
            db.add(transaction)

            # Update user XP
            user_xp = await self.get_or_create_user_xp(user_id, db)
            user_xp.total_xp += badge.xp_reward
            new_level, new_title, xp_to_next = get_level_for_xp(user_xp.total_xp)
            user_xp.current_level = new_level
            user_xp.level_title = new_title
            user_xp.xp_to_next_level = xp_to_next
            user_xp.updated_at = datetime.now(timezone.utc)

        await db.commit()
        return True


# Global instance
_gamification_service: Optional[GamificationService] = None


def get_gamification_service() -> GamificationService:
    """Get global gamification service instance."""
    global _gamification_service
    if _gamification_service is None:
        _gamification_service = GamificationService()
    return _gamification_service
