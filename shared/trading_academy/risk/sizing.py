"""Risk management and position sizing."""

import numpy as np
import pandas as pd
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class SizingMethod(str, Enum):
    """Position sizing methods."""

    FIXED_FRACTIONAL = "fixed_fractional"
    KELLY = "kelly"
    VOLATILITY_BASED = "volatility_based"
    FIXED_RISK = "fixed_risk"
    OPTIMAL_F = "optimal_f"
    CONSTANT_LEVERAGE = "constant_leverage"


@dataclass
class PositionSizeResult:
    """Position sizing calculation result."""

    size: float  # Position size in base currency
    size_pct: float  # As percentage of equity
    risk_amount: float  # Risk in base currency
    risk_pct: float  # Risk as percentage of equity
    shares: float  # Number of shares/contracts
    method: SizingMethod


def fixed_fractional_size(
    equity: float,
    risk_pct: float,
    entry_price: float,
    stop_price: float,
    contract_multiplier: float = 1.0,
) -> PositionSizeResult:
    """Fixed fractional position sizing.

    Args:
        equity: Total account equity.
        risk_pct: Risk per trade as percentage (e.g., 0.02 for 2%).
        entry_price: Entry price.
        stop_price: Stop loss price.
        contract_multiplier: Contract multiplier (for futures).

    Returns:
        PositionSizeResult with calculated size.
    """
    risk_per_share = abs(entry_price - stop_price)
    if risk_per_share == 0:
        return PositionSizeResult(0, 0, 0, 0, 0, SizingMethod.FIXED_FRACTIONAL)

    risk_amount = equity * risk_pct
    shares = risk_amount / risk_per_share
    size = shares * entry_price * contract_multiplier
    size_pct = size / equity

    return PositionSizeResult(
        size=size,
        size_pct=size_pct,
        risk_amount=risk_amount,
        risk_pct=risk_pct,
        shares=shares,
        method=SizingMethod.FIXED_FRACTIONAL,
    )


def kelly_size(
    equity: float,
    win_rate: float,
    avg_win: float,
    avg_loss: float,
    max_fraction: float = 0.25,
    entry_price: float = 1.0,
    stop_price: float = 0.98,
) -> PositionSizeResult:
    """Kelly Criterion position sizing.

    Args:
        equity: Total account equity.
        win_rate: Historical win rate (0-1).
        avg_win: Average winning trade return.
        avg_loss: Average losing trade return (positive).
        max_fraction: Maximum Kelly fraction (safety cap).
        entry_price: Entry price.
        stop_price: Stop loss price.

    Returns:
        PositionSizeResult with calculated size.
    """
    if avg_loss <= 0 or win_rate <= 0 or win_rate >= 1:
        return PositionSizeResult(0, 0, 0, 0, 0, SizingMethod.KELLY)

    # Kelly fraction: f* = (bp - q) / b
    # where b = avg_win/avg_loss, p = win_rate, q = 1 - win_rate
    b = avg_win / avg_loss
    p = win_rate
    q = 1 - win_rate

    kelly_fraction = (b * p - q) / b
    kelly_fraction = max(0, min(kelly_fraction, max_fraction))

    risk_amount = equity * kelly_fraction
    risk_per_share = abs(entry_price - stop_price)

    if risk_per_share == 0:
        return PositionSizeResult(0, 0, 0, 0, 0, SizingMethod.KELLY)

    shares = risk_amount / risk_per_share
    size = shares * entry_price
    size_pct = size / equity

    return PositionSizeResult(
        size=size,
        size_pct=size_pct,
        risk_amount=risk_amount,
        risk_pct=kelly_fraction,
        shares=shares,
        method=SizingMethod.KELLY,
    )


def volatility_based_size(
    equity: float,
    atr: float,
    entry_price: float,
    atr_multiplier: float = 2.0,
    risk_pct: float = 0.02,
    contract_multiplier: float = 1.0,
) -> PositionSizeResult:
    """Volatility-based (ATR) position sizing.

    Args:
        equity: Total account equity.
        atr: Average True Range.
        entry_price: Entry price.
        atr_multiplier: ATR multiplier for stop distance.
        risk_pct: Risk per trade as percentage.
        contract_multiplier: Contract multiplier.

    Returns:
        PositionSizeResult with calculated size.
    """
    stop_distance = atr * atr_multiplier
    stop_price = entry_price - stop_distance  # For long positions

    return fixed_fractional_size(
        equity=equity,
        risk_pct=risk_pct,
        entry_price=entry_price,
        stop_price=stop_price,
        contract_multiplier=contract_multiplier,
    )


def fixed_risk_size(
    equity: float,
    risk_amount: float,
    entry_price: float,
    stop_price: float,
    contract_multiplier: float = 1.0,
) -> PositionSizeResult:
    """Fixed risk amount position sizing.

    Args:
        equity: Total account equity.
        risk_amount: Fixed risk amount per trade.
        entry_price: Entry price.
        stop_price: Stop loss price.
        contract_multiplier: Contract multiplier.

    Returns:
        PositionSizeResult with calculated size.
    """
    risk_per_share = abs(entry_price - stop_price)
    if risk_per_share == 0:
        return PositionSizeResult(0, 0, 0, 0, 0, SizingMethod.FIXED_RISK)

    shares = risk_amount / risk_per_share
    size = shares * entry_price * contract_multiplier
    size_pct = size / equity
    risk_pct = risk_amount / equity

    return PositionSizeResult(
        size=size,
        size_pct=size_pct,
        risk_amount=risk_amount,
        risk_pct=risk_pct,
        shares=shares,
        method=SizingMethod.FIXED_RISK,
    )


def optimal_f_size(
    equity: float,
    trades: List[float],
    entry_price: float,
    stop_price: float,
    contract_multiplier: float = 1.0,
) -> PositionSizeResult:
    """Optimal f position sizing (Ralph Vince).

    Args:
        equity: Total account equity.
        trades: List of trade returns (as fractions, e.g., 0.05 for 5%).
        entry_price: Entry price.
        stop_price: Stop loss price.
        contract_multiplier: Contract multiplier.

    Returns:
        PositionSizeResult with calculated size.
    """
    if not trades:
        return PositionSizeResult(0, 0, 0, 0, 0, SizingMethod.OPTIMAL_F)

    trades_arr = np.array(trades)
    worst_loss = abs(min(trades_arr))  # Worst trade as fraction

    if worst_loss == 0:
        return PositionSizeResult(0, 0, 0, 0, 0, SizingMethod.OPTIMAL_F)

    # Find optimal f by maximizing geometric mean
    best_f = 0
    best_gmean = 1

    for f in np.linspace(0.01, 1.0, 100):
        hpr = 1 + f * (trades_arr / worst_loss)
        if np.any(hpr <= 0):
            continue
        gmean = np.prod(hpr) ** (1 / len(hpr))
        if gmean > best_gmean:
            best_gmean = gmean
            best_f = f

    risk_amount = equity * best_f
    return fixed_risk_size(
        equity=equity,
        risk_amount=risk_amount,
        entry_price=entry_price,
        stop_price=stop_price,
        contract_multiplier=contract_multiplier,
    )


@dataclass
class RiskMetrics:
    """Portfolio risk metrics."""

    var_95: float  # Value at Risk 95%
    var_99: float  # Value at Risk 99%
    expected_shortfall_95: float  # Conditional VaR
    max_drawdown: float
    max_drawdown_duration: int
    sharpe_ratio: float
    sortino_ratio: float
    calmar_ratio: float
    volatility: float
    downside_volatility: float
    skew: float
    kurtosis: float
    beta: float
    correlation_matrix: Optional[pd.DataFrame] = None


def calculate_risk_metrics(
    returns: pd.Series,
    benchmark_returns: Optional[pd.Series] = None,
    risk_free_rate: float = 0.02,
) -> RiskMetrics:
    """Calculate comprehensive risk metrics.

    Args:
        returns: Portfolio returns series.
        benchmark_returns: Benchmark returns for beta calculation.
        risk_free_rate: Annual risk-free rate.

    Returns:
        RiskMetrics object.
    """
    returns = returns.dropna()

    if len(returns) < 2:
        return RiskMetrics(
            var_95=0, var_99=0, expected_shortfall_95=0,
            max_drawdown=0, max_drawdown_duration=0,
            sharpe_ratio=0, sortino_ratio=0, calmar_ratio=0,
            volatility=0, downside_volatility=0,
            skew=0, kurtosis=0, beta=0,
        )

    # VaR
    var_95 = np.percentile(returns, 5)
    var_99 = np.percentile(returns, 1)

    # Expected Shortfall (CVaR)
    es_95 = returns[returns <= var_95].mean()

    # Drawdown
    cumulative = (1 + returns).cumprod()
    running_max = cumulative.expanding().max()
    drawdown = (cumulative - running_max) / running_max
    max_dd = drawdown.min()

    # Drawdown duration
    dd_duration = 0
    max_dd_duration = 0
    for dd in drawdown:
        if dd < 0:
            dd_duration += 1
            max_dd_duration = max(max_dd_duration, dd_duration)
        else:
            dd_duration = 0

    # Ratios
    excess_returns = returns - risk_free_rate / 252
    sharpe = excess_returns.mean() / returns.std() * np.sqrt(252) if returns.std() > 0 else 0

    downside_returns = returns[returns < 0]
    downside_vol = downside_returns.std() * np.sqrt(252) if len(downside_returns) > 0 else 0
    sortino = excess_returns.mean() / downside_vol * np.sqrt(252) if downside_vol > 0 else 0

    calmar = (returns.mean() * 252) / abs(max_dd) if max_dd != 0 else 0

    # Moments
    skew = returns.skew()
    kurt = returns.kurtosis()

    # Beta
    beta = 0
    if benchmark_returns is not None:
        aligned = pd.concat([returns, benchmark_returns], axis=1).dropna()
        if len(aligned) > 1:
            cov = aligned.iloc[:, 0].cov(aligned.iloc[:, 1])
            bench_var = aligned.iloc[:, 1].var()
            beta = cov / bench_var if bench_var > 0 else 0

    return RiskMetrics(
        var_95=var_95,
        var_99=var_99,
        expected_shortfall_95=es_95,
        max_drawdown=max_dd,
        max_drawdown_duration=max_dd_duration,
        sharpe_ratio=sharpe,
        sortino_ratio=sortino,
        calmar_ratio=calmar,
        volatility=returns.std() * np.sqrt(252),
        downside_volatility=downside_vol,
        skew=skew,
        kurtosis=kurt,
        beta=beta,
    )


def calculate_position_correlation(
    positions: Dict[str, pd.Series],
    method: str = "pearson"
) -> pd.DataFrame:
    """Calculate correlation matrix for positions.

    Args:
        positions: Dict of symbol -> returns series.
        method: Correlation method.

    Returns:
        Correlation matrix DataFrame.
    """
    df = pd.DataFrame(positions)
    return df.corr(method=method)


def portfolio_var(
    positions: Dict[str, float],
    returns: Dict[str, pd.Series],
    confidence: float = 0.95,
    method: str = "historical"
) -> float:
    """Calculate portfolio VaR.

    Args:
        positions: Dict of symbol -> position value.
        returns: Dict of symbol -> returns series.
        confidence: Confidence level.
        method: VaR method (historical, parametric, monte_carlo).

    Returns:
        Portfolio VaR.
    """
    if method == "historical":
        # Create portfolio returns
        total_value = sum(positions.values())
        weights = {k: v / total_value for k, v in positions.items()}

        portfolio_returns = pd.Series(0.0, index=next(iter(returns.values())).index)
        for symbol, weight in weights.items():
            if symbol in returns:
                portfolio_returns += returns[symbol] * weight

        return np.percentile(portfolio_returns.dropna(), (1 - confidence) * 100)

    return 0.0


def kelly_criterion(
    win_prob: float,
    win_loss_ratio: float,
    max_fraction: float = 1.0
) -> float:
    """Calculate Kelly Criterion fraction.

    Args:
        win_prob: Probability of winning (0-1).
        win_loss_ratio: Average win / average loss.
        max_fraction: Maximum fraction to return.

    Returns:
        Optimal fraction to bet.
    """
    if win_prob <= 0 or win_prob >= 1 or win_loss_ratio <= 0:
        return 0.0

    f = (win_prob * win_loss_ratio - (1 - win_prob)) / win_loss_ratio
    return max(0, min(f, max_fraction))


def risk_of_ruin(
    win_prob: float,
    payoff_ratio: float,
    risk_per_trade: float,
    target_ruin: float = 0.01
) -> float:
    """Calculate risk of ruin.

    Args:
        win_prob: Win probability.
        payoff_ratio: Average win / average loss.
        risk_per_trade: Fraction risked per trade.
        target_ruin: Target probability of ruin.

    Returns:
        Number of trades to reach target ruin probability.
    """
    if win_prob <= 0.5:
        return float('inf')

    p = win_prob
    q = 1 - win_prob
    b = payoff_ratio

    # Risk of ruin formula
    # R = ((1 - edge) / (1 + edge))^(capital / risk_per_trade)
    # where edge = p - q/b
    edge = p - q / b
    if edge <= 0:
        return float('inf')

    # Simplified approximation
    return np.log(target_ruin) / np.log((1 - edge) / (1 + edge))