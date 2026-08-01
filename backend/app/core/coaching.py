"""Trading coaching and adaptive feedback engine."""

import asyncio
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any, Optional
from uuid import UUID
from dataclasses import dataclass
from enum import Enum

from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_context
from app.db.models import PaperTrade, User, UserProgress, Lesson, QuizAttempt
from app.core.licensing import get_license_manager, has_feature


class FeedbackType(str, Enum):
    """Type of coaching feedback."""

    RISK_MANAGEMENT = "risk_management"
    STRATEGY_ADHERENCE = "strategy_adherence"
    POSITION_SIZING = "position_sizing"
    ENTRY_TIMING = "entry_timing"
    EXIT_TIMING = "exit_timing"
    EMOTIONAL_CONTROL = "emotional_control"
    LEARNING_GAP = "learning_gap"
    POSITIVE_REINFORCEMENT = "positive_reinforcement"


class FeedbackSeverity(str, Enum):
    """Severity of feedback."""

    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


@dataclass
class CoachingFeedback:
    """Coaching feedback item."""

    type: FeedbackType
    severity: FeedbackSeverity
    title: str
    message: str
    trade_id: Optional[UUID] = None
    lesson_id: Optional[UUID] = None
    actionable_advice: Optional[str] = None
    related_concepts: List[str] = None

    def __post_init__(self):
        if self.related_concepts is None:
            self.related_concepts = []


class TradingCoach:
    """Adaptive trading coach that analyzes user behavior and provides feedback."""

    # Risk thresholds
    MAX_POSITION_SIZE_PCT = 0.10  # 10% of portfolio
    MAX_DAILY_LOSS_PCT = 0.05     # 5% daily loss limit
    MAX_DRAWDOWN_PCT = 0.20       # 20% max drawdown
    MIN_RISK_REWARD = 1.5         # Minimum risk:reward ratio

    def __init__(self):
        self.license_manager = get_license_manager()

    async def analyze_trade(self, trade_id: UUID) -> List[CoachingFeedback]:
        """Analyze a completed trade and generate feedback."""
        feedback = []

        async with get_db_context() as db:
            # Get trade with user
            result = await db.execute(
                select(PaperTrade, User)
                .join(User, User.id == PaperTrade.user_id)
                .where(PaperTrade.id == trade_id)
            )
            row = result.one_or_none()

            if not row:
                return feedback

            trade, user = row

            # Check if user has coaching feature
            if not self._has_coaching_access(user):
                return feedback

            # Position sizing check
            feedback.extend(await self._check_position_sizing(trade, user, db))

            # Risk:reward check
            feedback.extend(self._check_risk_reward(trade))

            # Strategy adherence
            feedback.extend(await self._check_strategy_adherence(trade, user, db))

            # Entry/exit timing
            feedback.extend(self._check_timing(trade, db))

            # Emotional patterns
            feedback.extend(await self._check_emotional_patterns(trade, user, db))

        return feedback

    def _has_coaching_access(self, user: User) -> bool:
        """Check if user has access to coaching features."""
        for license_obj in user.licenses:
            valid, _ = self.license_manager.validate_license(license_obj)
            if valid and has_feature(license_obj.tier.value, "coaching_feedback"):
                return True
        return False

    async def _check_position_sizing(
        self,
        trade: PaperTrade,
        user: User,
        db: AsyncSession
    ) -> List[CoachingFeedback]:
        """Check if position size is appropriate."""
        feedback = []

        # Get user's portfolio value (simplified - sum of closed trades PnL + starting capital)
        result = await db.execute(
            select(func.sum(PaperTrade.pnl)).where(
                (PaperTrade.user_id == user.id) &
                (PaperTrade.status == "filled")
            )
        )
        total_pnl = result.scalar() or 0
        starting_capital = 10000  # Default, should be configurable
        portfolio_value = starting_capital + total_pnl

        position_value = trade.filled_quantity * (trade.filled_price or trade.price or 0)
        position_pct = position_value / portfolio_value if portfolio_value > 0 else 0

        if position_pct > self.MAX_POSITION_SIZE_PCT:
            feedback.append(CoachingFeedback(
                type=FeedbackType.POSITION_SIZING,
                severity=FeedbackSeverity.WARNING,
                title="Position Size Exceeds Limit",
                message=(
                    f"This position represents {position_pct:.1%} of your portfolio, "
                    f"exceeding the recommended {self.MAX_POSITION_SIZE_PCT:.0%} maximum."
                ),
                trade_id=trade.id,
                actionable_advice=(
                    "Reduce position size to stay within risk limits. "
                    "Consider using fixed fractional sizing (1-2% per trade)."
                ),
                related_concepts=["position_sizing", "risk_management", "kelly_criterion"],
            ))

        return feedback

    def _check_risk_reward(self, trade: PaperTrade) -> List[CoachingFeedback]:
        """Check risk:reward ratio."""
        feedback = []

        if trade.order_type in ["limit", "stop_limit"] and trade.price and trade.stop_price:
            entry = trade.price
            stop = trade.stop_price

            if trade.side.value == "buy":
                risk = entry - stop
                # Assume target is 2x risk (simplified)
                reward = risk * 2
            else:
                risk = stop - entry
                reward = risk * 2

            if risk > 0:
                rr_ratio = reward / risk
                if rr_ratio < self.MIN_RISK_REWARD:
                    feedback.append(CoachingFeedback(
                        type=FeedbackType.RISK_MANAGEMENT,
                        severity=FeedbackSeverity.WARNING,
                        title="Unfavorable Risk:Reward Ratio",
                        message=(
                            f"Risk:reward ratio is {rr_ratio:.2f}:1, "
                            f"below the recommended {self.MIN_RISK_REWARD}:1 minimum."
                        ),
                        trade_id=trade.id,
                        actionable_advice=(
                            "Adjust stop loss or target to achieve better risk:reward. "
                            "Consider wider targets or tighter stops."
                        ),
                        related_concepts=["risk_reward", "trade_management", "expectancy"],
                    ))

        return feedback

    async def _check_strategy_adherence(
        self,
        trade: PaperTrade,
        user: User,
        db: AsyncSession
    ) -> List[CoachingFeedback]:
        """Check if trade follows stated strategy rules."""
        feedback = []

        if not trade.strategy_name:
            return feedback

        # Get recent trades with same strategy
        result = await db.execute(
            select(PaperTrade).where(
                (PaperTrade.user_id == user.id) &
                (PaperTrade.strategy_name == trade.strategy_name) &
                (PaperTrade.status == "filled") &
                (PaperTrade.id != trade.id)
            ).order_by(PaperTrade.created_at.desc()).limit(20)
        )
        recent_trades = result.scalars().all()

        if len(recent_trades) >= 5:
            # Check consistency (simplified - check if all same side)
            sides = [t.side.value for t in recent_trades]
            buy_ratio = sides.count("buy") / len(sides)

            # If strategy is trend-following but mixing directions
            if "trend" in trade.strategy_name.lower() and 0.3 < buy_ratio < 0.7:
                feedback.append(CoachingFeedback(
                    type=FeedbackType.STRATEGY_ADHERENCE,
                    severity=FeedbackSeverity.INFO,
                    title="Strategy Direction Inconsistency",
                    message=(
                        f"Your '{trade.strategy_name}' trades show mixed directions "
                        f"({buy_ratio:.0%} buys). Trend strategies typically favor one direction."
                    ),
                    trade_id=trade.id,
                    actionable_advice=(
                        "Review your strategy rules. Ensure you're following "
                        "the trend direction consistently."
                    ),
                    related_concepts=["trend_following", "strategy_discipline", "market_regime"],
                ))

        return feedback

    def _check_timing(self, trade: PaperTrade, db: AsyncSession) -> List[CoachingFeedback]:
        """Check entry/exit timing quality."""
        feedback = []

        # Check if chased price (market order far from recent price)
        if trade.order_type == "market" and trade.filled_price:
            # In production, compare to VWAP or recent candles
            pass

        # Check if held loser too long
        if trade.pnl < 0 and trade.closed_at and trade.created_at:
            hold_time = trade.closed_at - trade.created_at
            if hold_time > timedelta(days=7) and trade.pnl < -100:
                feedback.append(CoachingFeedback(
                    type=FeedbackType.EXIT_TIMING,
                    severity=FeedbackSeverity.WARNING,
                    title="Held Losing Position Too Long",
                    message=(
                        f"Held losing position for {hold_time.days} days "
                        f"with ${abs(trade.pnl):.2f} loss."
                    ),
                    trade_id=trade.id,
                    actionable_advice=(
                        "Set and honor stop losses. Define max hold time for losing trades "
                        "in your trading plan."
                    ),
                    related_concepts=["stop_loss", "loss_aversion", "disposition_effect"],
                ))

        return feedback

    async def _check_emotional_patterns(
        self,
        trade: PaperTrade,
        user: User,
        db: AsyncSession
    ) -> List[CoachingFeedback]:
        """Check for emotional trading patterns."""
        feedback = []

        # Check for revenge trading (quick re-entry after loss)
        result = await db.execute(
            select(PaperTrade).where(
                (PaperTrade.user_id == user.id) &
                (PaperTrade.status == "filled") &
                (PaperTrade.pnl < 0) &
                (PaperTrade.closed_at.isnot(None))
            ).order_by(PaperTrade.closed_at.desc()).limit(1)
        )
        last_loss = result.scalar_one_or_none()

        if last_loss and trade.created_at and last_loss.closed_at:
            time_since_loss = trade.created_at - last_loss.closed_at
            if time_since_loss < timedelta(minutes=30) and trade.side == last_loss.side:
                feedback.append(CoachingFeedback(
                    type=FeedbackType.EMOTIONAL_CONTROL,
                    severity=FeedbackSeverity.WARNING,
                    title="Possible Revenge Trading",
                    message=(
                        f"Opened new {trade.side.value} position "
                        f"{time_since_loss.seconds // 60} minutes after a loss "
                        f"in the same direction."
                    ),
                    trade_id=trade.id,
                    actionable_advice=(
                        "Take a break after losses. Review your trading plan "
                        "before entering new positions."
                    ),
                    related_concepts=["revenge_trading", "emotional_control", "trading_psychology"],
                ))

        # Check for overtrading (too many trades in short period)
        today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        result = await db.execute(
            select(func.count(PaperTrade.id)).where(
                (PaperTrade.user_id == user.id) &
                (PaperTrade.created_at >= today_start)
            )
        )
        trades_today = result.scalar() or 0

        if trades_today > 20:
            feedback.append(CoachingFeedback(
                type=FeedbackType.EMOTIONAL_CONTROL,
                severity=FeedbackSeverity.WARNING,
                title="High Trade Frequency",
                message=(
                    f"Executed {trades_today} trades today. "
                    f"High frequency may indicate overtrading."
                ),
                trade_id=trade.id,
                actionable_advice=(
                    "Set daily trade limits. Focus on quality over quantity. "
                    "Review if each trade meets your criteria."
                ),
                related_concepts=["overtrading", "trade_frequency", "discipline"],
            ))

        return feedback

    async def analyze_user_patterns(self, user_id: UUID) -> Dict[str, Any]:
        """Comprehensive user trading pattern analysis."""
        async with get_db_context() as db:
            # Get all filled trades
            result = await db.execute(
                select(PaperTrade).where(
                    (PaperTrade.user_id == user_id) &
                    (PaperTrade.status == "filled")
                ).order_by(PaperTrade.created_at)
            )
            trades = result.scalars().all()

            if not trades:
                return {"message": "No completed trades to analyze"}

            # Basic stats
            total_trades = len(trades)
            winning_trades = [t for t in trades if t.pnl > 0]
            losing_trades = [t for t in trades if t.pnl < 0]

            win_rate = len(winning_trades) / total_trades if total_trades > 0 else 0
            avg_win = sum(t.pnl for t in winning_trades) / len(winning_trades) if winning_trades else 0
            avg_loss = sum(t.pnl for t in losing_trades) / len(losing_trades) if losing_trades else 0
            profit_factor = abs(avg_win / avg_loss) if avg_loss != 0 else float('inf')
            expectancy = (win_rate * avg_win) + ((1 - win_rate) * avg_loss)

            # By symbol
            by_symbol = {}
            for trade in trades:
                if trade.symbol not in by_symbol:
                    by_symbol[trade.symbol] = {"trades": 0, "pnl": 0, "wins": 0}
                by_symbol[trade.symbol]["trades"] += 1
                by_symbol[trade.symbol]["pnl"] += trade.pnl
                if trade.pnl > 0:
                    by_symbol[trade.symbol]["wins"] += 1

            # By side
            buys = [t for t in trades if t.side.value == "buy"]
            sells = [t for t in trades if t.side.value == "sell"]

            # By time of day (hour)
            by_hour = {}
            for trade in trades:
                hour = trade.created_at.hour
                if hour not in by_hour:
                    by_hour[hour] = {"trades": 0, "pnl": 0}
                by_hour[hour]["trades"] += 1
                by_hour[hour]["pnl"] += trade.pnl

            # Streaks
            current_streak = 0
            max_win_streak = 0
            max_loss_streak = 0
            for trade in trades:
                if trade.pnl > 0:
                    current_streak = max(0, current_streak) + 1
                    max_win_streak = max(max_win_streak, current_streak)
                else:
                    current_streak = min(0, current_streak) - 1
                    max_loss_streak = max(max_loss_streak, abs(current_streak))

            return {
                "summary": {
                    "total_trades": total_trades,
                    "win_rate": round(win_rate * 100, 2),
                    "avg_win": round(avg_win, 2),
                    "avg_loss": round(avg_loss, 2),
                    "profit_factor": round(profit_factor, 2),
                    "expectancy": round(expectancy, 2),
                    "max_win_streak": max_win_streak,
                    "max_loss_streak": max_loss_streak,
                },
                "by_symbol": {
                    k: {**v, "win_rate": round(v["wins"] / v["trades"] * 100, 2)}
                    for k, v in by_symbol.items()
                },
                "by_side": {
                    "buy": {
                        "trades": len(buys),
                        "pnl": round(sum(t.pnl for t in buys), 2),
                        "win_rate": round(sum(1 for t in buys if t.pnl > 0) / len(buys) * 100, 2) if buys else 0,
                    },
                    "sell": {
                        "trades": len(sells),
                        "pnl": round(sum(t.pnl for t in sells), 2),
                        "win_rate": round(sum(1 for t in sells if t.pnl > 0) / len(sells) * 100, 2) if sells else 0,
                    },
                },
                "by_hour": by_hour,
                "recommendations": self._generate_recommendations(trades, win_rate, avg_win, avg_loss),
            }

    def _generate_recommendations(
        self,
        trades: List[PaperTrade],
        win_rate: float,
        avg_win: float,
        avg_loss: float
    ) -> List[str]:
        """Generate personalized recommendations."""
        recs = []

        if win_rate < 0.4:
            recs.append("Win rate below 40%. Focus on improving entry criteria and trade selection.")

        if avg_win < abs(avg_loss):
            recs.append("Average win smaller than average loss. Work on letting winners run and cutting losers faster.")

        if win_rate > 0.6 and avg_win > abs(avg_loss):
            recs.append("Strong performance! Consider increasing position size gradually within risk limits.")

        # Check for specific patterns
        symbols = set(t.symbol for t in trades)
        if len(symbols) == 1:
            recs.append("Trading only one symbol. Consider diversifying across uncorrelated assets.")

        return recs

    async def get_lesson_recommendations(self, user_id: UUID) -> List[Dict[str, Any]]:
        """Get lesson recommendations based on trading weaknesses."""
        patterns = await self.analyze_user_patterns(user_id)

        recommendations = []

        if isinstance(patterns, dict) and "summary" in patterns:
            summary = patterns["summary"]

            if summary["win_rate"] < 40:
                recommendations.append({
                    "lesson_topic": "Technical Analysis - Entry Signals",
                    "reason": "Low win rate suggests entry criteria need improvement",
                    "priority": "high",
                })

            if summary["avg_win"] < abs(summary["avg_loss"]):
                recommendations.append({
                    "lesson_topic": "Risk Management - Trade Management",
                    "reason": "Winners smaller than losers - need better exit strategy",
                    "priority": "high",
                })

            if summary["max_loss_streak"] > 3:
                recommendations.append({
                    "lesson_topic": "Trading Psychology - Emotional Control",
                    "reason": "Long losing streaks indicate emotional decision making",
                    "priority": "medium",
                })

            # Check symbol concentration
            by_symbol = patterns.get("by_symbol", {})
            if len(by_symbol) == 1:
                recommendations.append({
                    "lesson_topic": "Portfolio Management - Diversification",
                    "reason": "Concentrated in single symbol",
                    "priority": "medium",
                })

        return recommendations