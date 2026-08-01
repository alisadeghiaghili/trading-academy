"""Backtesting engine."""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timezone


class OrderSide(str, Enum):
    BUY = "buy"
    SELL = "sell"


class OrderType(str, Enum):
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"
    STOP_LIMIT = "stop_limit"


@dataclass
class Order:
    """Order representation."""

    symbol: str
    side: OrderSide
    quantity: float
    order_type: OrderType = OrderType.MARKET
    price: Optional[float] = None
    stop_price: Optional[float] = None
    timestamp: Optional[datetime] = None
    tag: str = ""


@dataclass
class Position:
    """Position representation."""

    symbol: str
    quantity: float = 0.0
    entry_price: float = 0.0
    current_price: float = 0.0
    unrealized_pnl: float = 0.0
    realized_pnl: float = 0.0

    def update_price(self, price: float) -> None:
        """Update current price and unrealized PnL."""
        self.current_price = price
        self.unrealized_pnl = (price - self.entry_price) * self.quantity


@dataclass
class Trade:
    """Completed trade record."""

    symbol: str
    side: OrderSide
    entry_price: float
    exit_price: float
    quantity: float
    entry_time: datetime
    exit_time: datetime
    pnl: float
    pnl_pct: float
    commission: float
    tag: str = ""


@dataclass
class BacktestResult:
    """Backtest results."""

    initial_capital: float
    final_capital: float
    total_return: float
    total_return_pct: float
    trades: List[Trade] = field(default_factory=list)
    equity_curve: pd.Series = field(default_factory=pd.Series)
    drawdown_curve: pd.Series = field(default_factory=pd.Series)
    metrics: Dict[str, float] = field(default_factory=dict)

    def __post_init__(self):
        if isinstance(self.equity_curve, pd.Series) and len(self.equity_curve) > 0:
            self._calculate_metrics()

    def _calculate_metrics(self) -> None:
        """Calculate performance metrics."""
        returns = self.equity_curve.pct_change().dropna()

        if len(returns) == 0:
            return

        # Basic metrics
        self.metrics["total_trades"] = len(self.trades)
        self.metrics["winning_trades"] = len([t for t in self.trades if t.pnl > 0])
        self.metrics["losing_trades"] = len([t for t in self.trades if t.pnl < 0])
        self.metrics["win_rate"] = self.metrics["winning_trades"] / self.metrics["total_trades"] if self.metrics["total_trades"] > 0 else 0

        # PnL metrics
        wins = [t.pnl for t in self.trades if t.pnl > 0]
        losses = [t.pnl for t in self.trades if t.pnl < 0]
        self.metrics["avg_win"] = np.mean(wins) if wins else 0
        self.metrics["avg_loss"] = np.mean(losses) if losses else 0
        self.metrics["profit_factor"] = abs(np.sum(wins) / np.sum(losses)) if losses else float('inf')
        self.metrics["expectancy"] = (self.metrics["win_rate"] * self.metrics["avg_win"]) + ((1 - self.metrics["win_rate"]) * self.metrics["avg_loss"])

        # Return metrics
        self.metrics["total_return"] = self.total_return_pct
        self.metrics["annualized_return"] = (1 + self.total_return_pct) ** (252 / len(self.equity_curve)) - 1 if len(self.equity_curve) > 0 else 0

        # Risk metrics
        volatility = returns.std() * np.sqrt(252)
        downside_returns = returns[returns < 0]
        downside_vol = downside_returns.std() * np.sqrt(252) if len(downside_returns) > 0 else 0

        excess_returns = returns - 0.02 / 252
        self.metrics["sharpe_ratio"] = excess_returns.mean() / returns.std() * np.sqrt(252) if returns.std() > 0 else 0
        self.metrics["sortino_ratio"] = excess_returns.mean() / downside_vol * np.sqrt(252) if downside_vol > 0 else 0

        # Drawdown
        cumulative = (1 + returns).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        self.metrics["max_drawdown"] = drawdown.min()
        self.metrics["calmar_ratio"] = (self.metrics["annualized_return"] / abs(self.metrics["max_drawdown"])) if self.metrics["max_drawdown"] != 0 else 0

        # Streaks
        current_streak = 0
        max_win_streak = 0
        max_loss_streak = 0
        for t in self.trades:
            if t.pnl > 0:
                current_streak = max(0, current_streak) + 1
                max_win_streak = max(max_win_streak, current_streak)
            else:
                current_streak = min(0, current_streak) - 1
                max_loss_streak = max(max_loss_streak, abs(current_streak))

        self.metrics["max_win_streak"] = max_win_streak
        self.metrics["max_loss_streak"] = max_loss_streak

        # Trade duration
        if self.trades:
            durations = [(t.exit_time - t.entry_time).total_seconds() / 3600 for t in self.trades]
            self.metrics["avg_trade_duration_hours"] = np.mean(durations)


class BacktestEngine:
    """Vectorized backtesting engine."""

    def __init__(
        self,
        initial_capital: float = 100000,
        commission: float = 0.001,
        slippage: float = 0.0005,
        margin_requirement: float = 1.0,
    ):
        """Initialize backtest engine.

        Args:
            initial_capital: Starting capital.
            commission: Commission rate (e.g., 0.001 for 0.1%).
            slippage: Slippage rate.
            margin_requirement: Margin requirement (1.0 = no leverage).
        """
        self.initial_capital = initial_capital
        self.commission = commission
        self.slippage = slippage
        self.margin_requirement = margin_requirement

        # State
        self.capital = initial_capital
        self.positions: Dict[str, Position] = {}
        self.trades: List[Trade] = []
        self.equity_curve: List[float] = [initial_capital]
        self.timestamps: List[datetime] = []

    def run(
        self,
        data: Dict[str, pd.DataFrame],
        strategy: Callable[[Dict[str, pd.DataFrame], int, "BacktestEngine"], List[Order]],
        start_idx: int = 0,
        end_idx: Optional[int] = None,
    ) -> BacktestResult:
        """Run backtest.

        Args:
            data: Dict of symbol -> OHLCV DataFrame with DatetimeIndex.
            strategy: Function(data, current_idx, engine) -> List[Order].
            start_idx: Start index.
            end_idx: End index (None for all).

        Returns:
            BacktestResult.
        """
        # Align all data to common index
        common_index = None
        for df in data.values():
            if common_index is None:
                common_index = df.index
            else:
                common_index = common_index.intersection(df.index)

        if len(common_index) == 0:
            raise ValueError("No common timestamps in data")

        common_index = common_index[start_idx:end_idx]

        for i, timestamp in enumerate(common_index):
            current_idx = start_idx + i

            # Update position prices
            for symbol, position in self.positions.items():
                if symbol in data:
                    price = data[symbol].loc[timestamp, "close"]
                    position.update_price(price)

            # Calculate equity
            equity = self.capital + sum(p.unrealized_pnl for p in self.positions.values())
            self.equity_curve.append(equity)
            self.timestamps.append(timestamp)

            # Get current data slice for strategy
            current_data = {}
            for symbol, df in data.items():
                current_data[symbol] = df.loc[:timestamp]

            # Generate orders
            orders = strategy(current_data, current_idx, self)

            # Execute orders
            for order in orders:
                self._execute_order(order, timestamp, data)

        # Close all positions at end
        final_timestamp = common_index[-1]
        for symbol, position in list(self.positions.items()):
            if position.quantity != 0:
                price = data[symbol].loc[final_timestamp, "close"]
                self._close_position(symbol, price, final_timestamp)

        # Final equity
        final_equity = self.capital + sum(p.unrealized_pnl for p in self.positions.values())
        self.equity_curve[-1] = final_equity

        return self._create_result()

    def _execute_order(self, order: Order, timestamp: datetime, data: Dict[str, pd.DataFrame]) -> None:
        """Execute an order."""
        if order.symbol not in data:
            return

        current_bar = data[order.symbol].loc[timestamp]
        price = self._get_fill_price(order, current_bar)

        if price is None:
            return

        # Calculate cost
        cost = order.quantity * price * (1 + self.commission + self.slippage)

        if order.side == OrderSide.BUY:
            if cost > self.capital * self.margin_requirement:
                return  # Insufficient capital

            self.capital -= cost

            # Update or create position
            if order.symbol in self.positions:
                pos = self.positions[order.symbol]
                total_qty = pos.quantity + order.quantity
                pos.entry_price = (pos.entry_price * pos.quantity + price * order.quantity) / total_qty
                pos.quantity = total_qty
            else:
                self.positions[order.symbol] = Position(
                    symbol=order.symbol,
                    quantity=order.quantity,
                    entry_price=price,
                    current_price=price,
                )

        elif order.side == OrderSide.SELL:
            if order.symbol not in self.positions:
                return  # No position to sell

            pos = self.positions[order.symbol]
            sell_qty = min(order.quantity, pos.quantity)

            if sell_qty <= 0:
                return

            proceeds = sell_qty * price * (1 - self.commission - self.slippage)
            self.capital += proceeds

            # Realized PnL
            realized_pnl = (price - pos.entry_price) * sell_qty
            pos.realized_pnl += realized_pnl

            # Record trade
            self.trades.append(Trade(
                symbol=order.symbol,
                side=OrderSide.BUY,  # Original side
                entry_price=pos.entry_price,
                exit_price=price,
                quantity=sell_qty,
                entry_time=timestamp,  # Simplified
                exit_time=timestamp,
                pnl=realized_pnl - (sell_qty * price * (self.commission + self.slippage)),
                pnl_pct=(price - pos.entry_price) / pos.entry_price,
                commission=sell_qty * price * (self.commission + self.slippage),
                tag=order.tag,
            ))

            pos.quantity -= sell_qty
            if pos.quantity <= 0:
                del self.positions[order.symbol]

    def _get_fill_price(self, order: Order, bar: pd.Series) -> Optional[float]:
        """Get fill price based on order type."""
        if order.order_type == OrderType.MARKET:
            return bar["close"] * (1 + self.slippage if order.side == OrderSide.BUY else 1 - self.slippage)

        elif order.order_type == OrderType.LIMIT:
            if order.side == OrderSide.BUY and order.price <= bar["high"]:
                return min(order.price, bar["open"])
            elif order.side == OrderSide.SELL and order.price >= bar["low"]:
                return max(order.price, bar["open"])
            return None

        elif order.order_type == OrderType.STOP:
            if order.side == OrderSide.BUY and order.stop_price <= bar["high"]:
                return max(order.stop_price, bar["open"])
            elif order.side == OrderSide.SELL and order.stop_price >= bar["low"]:
                return min(order.stop_price, bar["open"])
            return None

        return None

    def _close_position(self, symbol: str, price: float, timestamp: datetime) -> None:
        """Close a position completely."""
        if symbol not in self.positions:
            return

        pos = self.positions[symbol]
        if pos.quantity == 0:
            return

        proceeds = pos.quantity * price * (1 - self.commission - self.slippage)
        self.capital += proceeds

        realized_pnl = (price - pos.entry_price) * pos.quantity
        pos.realized_pnl += realized_pnl

        self.trades.append(Trade(
            symbol=symbol,
            side=OrderSide.BUY,
            entry_price=pos.entry_price,
            exit_price=price,
            quantity=pos.quantity,
            entry_time=timestamp,
            exit_time=timestamp,
            pnl=realized_pnl - (pos.quantity * price * (self.commission + self.slippage)),
            pnl_pct=(price - pos.entry_price) / pos.entry_price,
            commission=pos.quantity * price * (self.commission + self.slippage),
            tag="forced_close",
        ))

        del self.positions[symbol]

    def _create_result(self) -> BacktestResult:
        """Create backtest result object."""
        equity_series = pd.Series(self.equity_curve, index=self.timestamps)

        return BacktestResult(
            initial_capital=self.initial_capital,
            final_capital=self.equity_curve[-1],
            total_return=self.equity_curve[-1] - self.initial_capital,
            total_return_pct=(self.equity_curve[-1] - self.initial_capital) / self.initial_capital,
            trades=self.trades,
            equity_curve=equity_series,
            drawdown_curve=self._calculate_drawdown(equity_series),
        )

    def _calculate_drawdown(self, equity: pd.Series) -> pd.Series:
        """Calculate drawdown series."""
        running_max = equity.expanding().max()
        return (equity - running_max) / running_max


def run_walk_forward(
    data: Dict[str, pd.DataFrame],
    strategy: Callable,
    train_window: int = 252,
    test_window: int = 63,
    step: int = 21,
    **engine_kwargs
) -> List[BacktestResult]:
    """Run walk-forward backtest.

    Args:
        data: Market data.
        strategy: Strategy function.
        train_window: Training window size.
        test_window: Test window size.
        step: Step size between windows.
        **engine_kwargs: Arguments for BacktestEngine.

    Returns:
        List of BacktestResult for each test window.
    """
    # Get common index length
    common_len = min(len(df) for df in data.values())

    results = []
    for start in range(0, common_len - train_window - test_window, step):
        train_end = start + train_window
        test_end = train_end + test_window

        if test_end > common_len:
            break

        engine = BacktestEngine(**engine_kwargs)
        result = engine.run(data, strategy, start_idx=train_end, end_idx=test_end)
        results.append(result)

    return results


def optimize_parameters(
    data: Dict[str, pd.DataFrame],
    strategy_factory: Callable[[Dict], Callable],
    param_grid: Dict[str, List],
    metric: str = "sharpe_ratio",
    **engine_kwargs
) -> Dict[str, Any]:
    """Optimize strategy parameters.

    Args:
        data: Market data.
        strategy_factory: Function that takes params dict and returns strategy function.
        param_grid: Dict of parameter name -> list of values.
        metric: Metric to optimize.
        **engine_kwargs: Arguments for BacktestEngine.

    Returns:
        Dict with best parameters and results.
    """
    from itertools import product

    param_names = list(param_grid.keys())
    param_values = list(param_grid.values())

    best_score = -np.inf
    best_params = None
    best_result = None
    all_results = []

    for combo in product(*param_values):
        params = dict(zip(param_names, combo))
        strategy = strategy_factory(params)

        engine = BacktestEngine(**engine_kwargs)
        result = engine.run(data, strategy)

        score = result.metrics.get(metric, -np.inf)

        all_results.append({
            "params": params,
            "score": score,
            "metrics": result.metrics,
        })

        if score > best_score:
            best_score = score
            best_params = params
            best_result = result

    return {
        "best_params": best_params,
        "best_score": best_score,
        "best_result": best_result,
        "all_results": all_results,
    }