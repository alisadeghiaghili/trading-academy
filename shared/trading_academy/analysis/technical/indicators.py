"""Technical analysis indicators."""

import numpy as np
import pandas as pd
from typing import Optional, Tuple
import talib


def sma(series: pd.Series, period: int) -> pd.Series:
    """Simple Moving Average."""
    return series.rolling(window=period, min_periods=period).mean()


def ema(series: pd.Series, period: int) -> pd.Series:
    """Exponential Moving Average."""
    return series.ewm(span=period, adjust=False).mean()


def wma(series: pd.Series, period: int) -> pd.Series:
    """Weighted Moving Average."""
    weights = np.arange(1, period + 1)
    return series.rolling(window=period).apply(
        lambda x: np.dot(x, weights) / weights.sum(),
        raw=True
    )


def rsi(series: pd.Series, period: int = 14) -> pd.Series:
    """Relative Strength Index."""
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))


def macd(
    series: pd.Series,
    fast: int = 12,
    slow: int = 26,
    signal: int = 9
) -> Tuple[pd.Series, pd.Series, pd.Series]:
    """MACD - Moving Average Convergence Divergence."""
    ema_fast = ema(series, fast)
    ema_slow = ema(series, slow)
    macd_line = ema_fast - ema_slow
    signal_line = ema(macd_line, signal)
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram


def bollinger_bands(
    series: pd.Series,
    period: int = 20,
    std_dev: float = 2.0
) -> Tuple[pd.Series, pd.Series, pd.Series]:
    """Bollinger Bands."""
    middle = sma(series, period)
    std = series.rolling(window=period).std()
    upper = middle + (std * std_dev)
    lower = middle - (std * std_dev)
    return upper, middle, lower


def atr(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    period: int = 14
) -> pd.Series:
    """Average True Range."""
    tr1 = high - low
    tr2 = (high - close.shift()).abs()
    tr3 = (low - close.shift()).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    return tr.rolling(window=period).mean()


def stochastic(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    k_period: int = 14,
    d_period: int = 3
) -> Tuple[pd.Series, pd.Series]:
    """Stochastic Oscillator."""
    lowest_low = low.rolling(window=k_period).min()
    highest_high = high.rolling(window=k_period).max()
    k = 100 * ((close - lowest_low) / (highest_high - lowest_low))
    d = k.rolling(window=d_period).mean()
    return k, d


def adx(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    period: int = 14
) -> pd.Series:
    """Average Directional Index."""
    return pd.Series(talib.ADX(high.values, low.values, close.values, timeperiod=period), index=close.index)


def obv(close: pd.Series, volume: pd.Series) -> pd.Series:
    """On Balance Volume."""
    direction = np.where(close > close.shift(), 1, np.where(close < close.shift(), -1, 0))
    return (volume * direction).cumsum()


def vwap(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    volume: pd.Series
) -> pd.Series:
    """Volume Weighted Average Price."""
    typical_price = (high + low + close) / 3
    return (typical_price * volume).cumsum() / volume.cumsum()


def ichimoku(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    tenkan: int = 9,
    kijun: int = 26,
    senkou_b: int = 52,
    displacement: int = 26
) -> dict:
    """Ichimoku Cloud."""
    tenkan_sen = (high.rolling(tenkan).max() + low.rolling(tenkan).min()) / 2
    kijun_sen = (high.rolling(kijun).max() + low.rolling(kijun).min()) / 2
    senkou_a = ((tenkan_sen + kijun_sen) / 2).shift(displacement)
    senkou_b = ((high.rolling(senkou_b).max() + low.rolling(senkou_b).min()) / 2).shift(displacement)
    chikou = close.shift(-displacement)

    return {
        "tenkan_sen": tenkan_sen,
        "kijun_sen": kijun_sen,
        "senkou_span_a": senkou_a,
        "senkou_span_b": senkou_b,
        "chikou_span": chikou,
    }


def supertrend(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    period: int = 10,
    multiplier: float = 3.0
) -> Tuple[pd.Series, pd.Series]:
    """Supertrend Indicator."""
    atr_values = atr(high, low, close, period)
    hl2 = (high + low) / 2

    upper = hl2 + (multiplier * atr_values)
    lower = hl2 - (multiplier * atr_values)

    supertrend = pd.Series(index=close.index, dtype=float)
    direction = pd.Series(index=close.index, dtype=int)

    for i in range(len(close)):
        if i == 0:
            supertrend.iloc[i] = lower.iloc[i]
            direction.iloc[i] = 1
        else:
            if close.iloc[i] > supertrend.iloc[i-1]:
                supertrend.iloc[i] = max(lower.iloc[i], supertrend.iloc[i-1])
                direction.iloc[i] = 1
            else:
                supertrend.iloc[i] = min(upper.iloc[i], supertrend.iloc[i-1])
                direction.iloc[i] = -1

    return supertrend, direction


def donchian_channels(
    high: pd.Series,
    low: pd.Series,
    period: int = 20
) -> Tuple[pd.Series, pd.Series, pd.Series]:
    """Donchian Channels."""
    upper = high.rolling(window=period).max()
    lower = low.rolling(window=period).min()
    middle = (upper + lower) / 2
    return upper, middle, lower


def keltner_channels(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    period: int = 20,
    multiplier: float = 2.0
) -> Tuple[pd.Series, pd.Series, pd.Series]:
    """Keltner Channels."""
    ema_values = ema(close, period)
    atr_values = atr(high, low, close, period)

    upper = ema_values + (multiplier * atr_values)
    lower = ema_values - (multiplier * atr_values)
    middle = ema_values

    return upper, middle, lower


def pivot_points(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series
) -> dict:
    """Standard Pivot Points."""
    pp = (high + low + close) / 3
    r1 = 2 * pp - low
    s1 = 2 * pp - high
    r2 = pp + (high - low)
    s2 = pp - (high - low)
    r3 = high + 2 * (pp - low)
    s3 = low - 2 * (high - pp)

    return {
        "pivot": pp,
        "r1": r1, "r2": r2, "r3": r3,
        "s1": s1, "s2": s2, "s3": s3,
    }


def fibonacci_retracement(high: float, low: float) -> dict:
    """Fibonacci Retracement Levels."""
    diff = high - low
    return {
        "0.0": high,
        "0.236": high - 0.236 * diff,
        "0.382": high - 0.382 * diff,
        "0.5": high - 0.5 * diff,
        "0.618": high - 0.618 * diff,
        "0.786": high - 0.786 * diff,
        "1.0": low,
    }


def detect_trend(
    series: pd.Series,
    short_period: int = 20,
    long_period: int = 50
) -> pd.Series:
    """Detect trend direction (1=up, -1=down, 0=sideways)."""
    sma_short = sma(series, short_period)
    sma_long = sma(series, long_period)

    trend = pd.Series(0, index=series.index)
    trend[sma_short > sma_long] = 1
    trend[sma_short < sma_long] = -1
    return trend


def support_resistance(
    close: pd.Series,
    window: int = 20,
    min_touches: int = 2
) -> Tuple[list, list]:
    """Detect support and resistance levels."""
    # Simplified - find local highs/lows
    highs = close.rolling(window=window, center=True).max() == close
    lows = close.rolling(window=window, center=True).min() == close

    resistance_levels = close[highs].value_counts()
    support_levels = close[lows].value_counts()

    resistance = resistance_levels[resistance_levels >= min_touches].index.tolist()
    support = support_levels[support_levels >= min_touches].index.tolist()

    return sorted(resistance, reverse=True), sorted(support)


# Pattern Recognition
def detect_doji(open_: pd.Series, high: pd.Series, low: pd.Series, close: pd.Series) -> pd.Series:
    """Detect Doji candlestick pattern."""
    body = (close - open_).abs()
    range_ = high - low
    return (body / range_ < 0.1).astype(int)


def detect_hammer(open_: pd.Series, high: pd.Series, low: pd.Series, close: pd.Series) -> pd.Series:
    """Detect Hammer candlestick pattern."""
    body = (close - open_).abs()
    lower_shadow = np.where(close > open_, open_ - low, close - low)
    upper_shadow = np.where(close > open_, high - close, high - open_)
    return ((lower_shadow > 2 * body) & (upper_shadow < body)).astype(int)


def detect_engulfing(
    open_: pd.Series,
    close: pd.Series,
    prev_open: pd.Series,
    prev_close: pd.Series
) -> pd.Series:
    """Detect Bullish/Bearish Engulfing pattern."""
    bullish = (prev_close < prev_open) & (close > open_) & (close > prev_open) & (open_ < prev_close)
    bearish = (prev_close > prev_open) & (close < open_) & (close < prev_open) & (open_ > prev_close)
    return np.where(bullish, 1, np.where(bearish, -1, 0))


def add_all_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Add all common indicators to DataFrame."""
    df = df.copy()

    # Ensure required columns
    required = ["open", "high", "low", "close", "volume"]
    for col in required:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    # Trend
    df["sma_20"] = sma(df["close"], 20)
    df["sma_50"] = sma(df["close"], 50)
    df["sma_200"] = sma(df["close"], 200)
    df["ema_12"] = ema(df["close"], 12)
    df["ema_26"] = ema(df["close"], 26)
    df["ema_50"] = ema(df["close"], 50)

    # Momentum
    df["rsi_14"] = rsi(df["close"], 14)
    df["macd"], df["macd_signal"], df["macd_hist"] = macd(df["close"])

    # Volatility
    df["bb_upper"], df["bb_middle"], df["bb_lower"] = bollinger_bands(df["close"])
    df["atr_14"] = atr(df["high"], df["low"], df["close"])

    # Volume
    df["obv"] = obv(df["close"], df["volume"])
    df["vwap"] = vwap(df["high"], df["low"], df["close"], df["volume"])

    # Trend
    df["adx_14"] = adx(df["high"], df["low"], df["close"])
    df["supertrend"], df["supertrend_dir"] = supertrend(df["high"], df["low"], df["close"])

    # Channels
    df["dc_upper"], df["dc_middle"], df["dc_lower"] = donchian_channels(df["high"], df["low"])
    df["kc_upper"], df["kc_middle"], df["kc_lower"] = keltner_channels(df["high"], df["low"], df["close"])

    return df