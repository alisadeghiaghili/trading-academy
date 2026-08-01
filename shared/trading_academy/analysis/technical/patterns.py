"""Chart pattern recognition."""

import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class PatternType(str, Enum):
    """Chart pattern types."""

    # Reversal patterns
    HEAD_AND_SHOULDERS = "head_and_shoulders"
    INVERSE_HEAD_AND_SHOULDERS = "inverse_head_and_shoulders"
    DOUBLE_TOP = "double_top"
    DOUBLE_BOTTOM = "double_bottom"
    TRIPLE_TOP = "triple_top"
    TRIPLE_BOTTOM = "triple_bottom"
    ROUNDING_TOP = "rounding_top"
    ROUNDING_BOTTOM = "rounding_bottom"

    # Continuation patterns
    ASCENDING_TRIANGLE = "ascending_triangle"
    DESCENDING_TRIANGLE = "descending_triangle"
    SYMMETRICAL_TRIANGLE = "symmetrical_triangle"
    BULLISH_FLAG = "bullish_flag"
    BEARISH_FLAG = "bearish_flag"
    BULLISH_PENNANT = "bullish_pennant"
    BEARISH_PENNANT = "bearish_pennant"
    RECTANGLE = "rectangle"
    CUP_AND_HANDLE = "cup_and_handle"

    # Candlestick patterns
    DOJI = "doji"
    HAMMER = "hammer"
    INVERTED_HAMMER = "inverted_hammer"
    SHOOTING_STAR = "shooting_star"
    HANGING_MAN = "hanging_man"
    BULLISH_ENGULFING = "bullish_engulfing"
    BEARISH_ENGULFING = "bearish_engulfing"
    MORNING_STAR = "morning_star"
    EVENING_STAR = "evening_star"
    THREE_WHITE_SOLDIERS = "three_white_soldiers"
    THREE_BLACK_CROWS = "three_black_crows"
    PIERCING_LINE = "piercing_line"
    DARK_CLOUD_COVER = "dark_cloud_cover"


class PatternDirection(str, Enum):
    """Pattern expected direction."""

    BULLISH = "bullish"
    BEARISH = "bearish"
    NEUTRAL = "neutral"


@dataclass
class PatternSignal:
    """Detected pattern signal."""

    pattern_type: PatternType
    direction: PatternDirection
    confidence: float  # 0-1
    start_idx: int
    end_idx: int
    key_levels: Dict[str, float]
    target_price: Optional[float] = None
    stop_loss: Optional[float] = None
    description: str = ""


def find_peaks(series: pd.Series, distance: int = 5) -> List[int]:
    """Find local peaks in series."""
    from scipy.signal import find_peaks as sp_find_peaks
    peaks, _ = sp_find_peaks(series.values, distance=distance)
    return peaks.tolist()


def find_troughs(series: pd.Series, distance: int = 5) -> List[int]:
    """Find local troughs in series."""
    from scipy.signal import find_peaks as sp_find_peaks
    troughs, _ = sp_find_peaks((-series).values, distance=distance)
    return troughs.tolist()


def detect_head_and_shoulders(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    distance: int = 5,
    tolerance: float = 0.03
) -> List[PatternSignal]:
    """Detect Head and Shoulders pattern."""
    signals = []
    peaks = find_peaks(high, distance)

    if len(peaks) < 3:
        return signals

    for i in range(len(peaks) - 2):
        left_shoulder = peaks[i]
        head = peaks[i + 1]
        right_shoulder = peaks[i + 2]

        # Check head is higher than shoulders
        head_high = high.iloc[head]
        ls_high = high.iloc[left_shoulder]
        rs_high = high.iloc[right_shoulder]

        if head_high <= ls_high or head_high <= rs_high:
            continue

        # Check shoulders roughly equal
        shoulder_diff = abs(ls_high - rs_high) / ls_high
        if shoulder_diff > tolerance:
            continue

        # Find neckline (support between shoulders)
        neckline_start = left_shoulder
        neckline_end = right_shoulder
        neckline_region = low.iloc[neckline_start:neckline_end]
        neckline = neckline_region.min()

        # Check break below neckline
        break_idx = None
        for j in range(right_shoulder + 1, min(right_shoulder + 20, len(close))):
            if close.iloc[j] < neckline:
                break_idx = j
                break

        if break_idx is not None:
            # Calculate target (head to neckline distance projected down)
            target = neckline - (head_high - neckline)
            stop = head_high

            signals.append(PatternSignal(
                pattern_type=PatternType.HEAD_AND_SHOULDERS,
                direction=PatternDirection.BEARISH,
                confidence=0.75,
                start_idx=left_shoulder,
                end_idx=break_idx,
                key_levels={
                    "left_shoulder": ls_high,
                    "head": head_high,
                    "right_shoulder": rs_high,
                    "neckline": neckline,
                },
                target_price=target,
                stop_loss=stop,
                description="Head and Shoulders reversal pattern detected",
            ))

    return signals


def detect_inverse_head_and_shoulders(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    distance: int = 5,
    tolerance: float = 0.03
) -> List[PatternSignal]:
    """Detect Inverse Head and Shoulders pattern."""
    signals = []
    troughs = find_troughs(low, distance)

    if len(troughs) < 3:
        return signals

    for i in range(len(troughs) - 2):
        left_shoulder = troughs[i]
        head = troughs[i + 1]
        right_shoulder = troughs[i + 2]

        # Check head is lower than shoulders
        head_low = low.iloc[head]
        ls_low = low.iloc[left_shoulder]
        rs_low = low.iloc[right_shoulder]

        if head_low >= ls_low or head_low >= rs_low:
            continue

        # Check shoulders roughly equal
        shoulder_diff = abs(ls_low - rs_low) / ls_low
        if shoulder_diff > tolerance:
            continue

        # Find neckline (resistance between shoulders)
        neckline_start = left_shoulder
        neckline_end = right_shoulder
        neckline_region = high.iloc[neckline_start:neckline_end]
        neckline = neckline_region.max()

        # Check break above neckline
        break_idx = None
        for j in range(right_shoulder + 1, min(right_shoulder + 20, len(close))):
            if close.iloc[j] > neckline:
                break_idx = j
                break

        if break_idx is not None:
            target = neckline + (neckline - head_low)
            stop = head_low

            signals.append(PatternSignal(
                pattern_type=PatternType.INVERSE_HEAD_AND_SHOULDERS,
                direction=PatternDirection.BULLISH,
                confidence=0.75,
                start_idx=left_shoulder,
                end_idx=break_idx,
                key_levels={
                    "left_shoulder": ls_low,
                    "head": head_low,
                    "right_shoulder": rs_low,
                    "neckline": neckline,
                },
                target_price=target,
                stop_loss=stop,
                description="Inverse Head and Shoulders reversal pattern detected",
            ))

    return signals


def detect_double_top(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    distance: int = 10,
    tolerance: float = 0.02
) -> List[PatternSignal]:
    """Detect Double Top pattern."""
    signals = []
    peaks = find_peaks(high, distance)

    if len(peaks) < 2:
        return signals

    for i in range(len(peaks) - 1):
        p1, p2 = peaks[i], peaks[i + 1]
        h1, h2 = high.iloc[p1], high.iloc[p2]

        # Check tops roughly equal
        if abs(h1 - h2) / h1 > tolerance:
            continue

        # Find valley between peaks
        valley_region = low.iloc[p1:p2]
        valley_idx = valley_region.idxmin()
        valley_low = valley_region.min()

        # Check break below valley
        break_idx = None
        for j in range(p2 + 1, min(p2 + 15, len(close))):
            if close.iloc[j] < valley_low:
                break_idx = j
                break

        if break_idx is not None:
            target = valley_low - (h1 - valley_low)
            stop = h1

            signals.append(PatternSignal(
                pattern_type=PatternType.DOUBLE_TOP,
                direction=PatternDirection.BEARISH,
                confidence=0.7,
                start_idx=p1,
                end_idx=break_idx,
                key_levels={"top1": h1, "top2": h2, "neckline": valley_low},
                target_price=target,
                stop_loss=stop,
                description="Double Top reversal pattern detected",
            ))

    return signals


def detect_double_bottom(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    distance: int = 10,
    tolerance: float = 0.02
) -> List[PatternSignal]:
    """Detect Double Bottom pattern."""
    signals = []
    troughs = find_troughs(low, distance)

    if len(troughs) < 2:
        return signals

    for i in range(len(troughs) - 1):
        t1, t2 = troughs[i], troughs[i + 1]
        l1, l2 = low.iloc[t1], low.iloc[t2]

        # Check bottoms roughly equal
        if abs(l1 - l2) / l1 > tolerance:
            continue

        # Find peak between troughs
        peak_region = high.iloc[t1:t2]
        peak_idx = peak_region.idxmax()
        peak_high = peak_region.max()

        # Check break above peak
        break_idx = None
        for j in range(t2 + 1, min(t2 + 15, len(close))):
            if close.iloc[j] > peak_high:
                break_idx = j
                break

        if break_idx is not None:
            target = peak_high + (peak_high - l1)
            stop = l1

            signals.append(PatternSignal(
                pattern_type=PatternType.DOUBLE_BOTTOM,
                direction=PatternDirection.BULLISH,
                confidence=0.7,
                start_idx=t1,
                end_idx=break_idx,
                key_levels={"bottom1": l1, "bottom2": l2, "neckline": peak_high},
                target_price=target,
                stop_loss=stop,
                description="Double Bottom reversal pattern detected",
            ))

    return signals


def detect_triangles(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    min_points: int = 4,
    max_slope_diff: float = 0.001
) -> List[PatternSignal]:
    """Detect Triangle patterns (ascending, descending, symmetrical)."""
    signals = []
    peaks = find_peaks(high, distance=5)
    troughs = find_troughs(low, distance=5)

    if len(peaks) < min_points or len(troughs) < min_points:
        return signals

    # Check recent points for triangle formation
    recent_peaks = peaks[-min_points:]
    recent_troughs = troughs[-min_points:]

    # Fit lines
    from scipy.stats import linregress

    peak_slope, peak_intercept, _, _, _ = linregress(
        np.arange(len(recent_peaks)), high.iloc[recent_peaks].values
    )
    trough_slope, trough_intercept, _, _, _ = linregress(
        np.arange(len(recent_troughs)), low.iloc[recent_troughs].values
    )

    # Classify triangle
    peak_flat = abs(peak_slope) < max_slope_diff
    trough_flat = abs(trough_slope) < max_slope_diff
    converging = peak_slope < 0 and trough_slope > 0

    if peak_flat and trough_slope > 0:
        pattern = PatternType.ASCENDING_TRIANGLE
        direction = PatternDirection.BULLISH
        desc = "Ascending Triangle continuation pattern"
    elif trough_flat and peak_slope < 0:
        pattern = PatternType.DESCENDING_TRIANGLE
        direction = PatternDirection.BEARISH
        desc = "Descending Triangle continuation pattern"
    elif converging:
        pattern = PatternType.SYMMETRICAL_TRIANGLE
        direction = PatternDirection.NEUTRAL
        desc = "Symmetrical Triangle continuation pattern"
    else:
        return signals

    # Calculate target (height of triangle at widest point)
    widest_high = high.iloc[recent_peaks].max()
    widest_low = low.iloc[recent_troughs].min()
    height = widest_high - widest_low
    apex_high = peak_intercept + peak_slope * (len(recent_peaks) - 1)
    apex_low = trough_intercept + trough_slope * (len(recent_troughs) - 1)

    if direction == PatternDirection.BULLISH:
        target = apex_high + height
        stop = apex_low
    elif direction == PatternDirection.BEARISH:
        target = apex_low - height
        stop = apex_high
    else:
        target = None
        stop = None

    signals.append(PatternSignal(
        pattern_type=pattern,
        direction=direction,
        confidence=0.65,
        start_idx=min(recent_peaks[0], recent_troughs[0]),
        end_idx=max(recent_peaks[-1], recent_troughs[-1]),
        key_levels={
            "resistance_slope": peak_slope,
            "support_slope": trough_slope,
            "apex_high": apex_high,
            "apex_low": apex_low,
        },
        target_price=target,
        stop_loss=stop,
        description=desc,
    ))

    return signals


def detect_flags_pennants(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    volume: pd.Series,
    trend_period: int = 20
) -> List[PatternSignal]:
    """Detect Flag and Pennant patterns."""
    signals = []

    # Detect strong trend first
    sma_trend = close.rolling(trend_period).mean()
    trend = np.where(close > sma_trend, 1, -1)

    # Look for consolidation after strong move
    # Simplified implementation - would need more sophisticated logic
    return signals


def detect_cup_and_handle(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    min_cup_depth: float = 0.15,
    max_handle_depth: float = 0.33
) -> List[PatternSignal]:
    """Detect Cup and Handle pattern."""
    signals = []

    # Find major low (cup bottom)
    troughs = find_troughs(low, distance=20)

    if len(troughs) < 3:
        return signals

    for i in range(len(troughs) - 2):
        left_rim = troughs[i]
        cup_bottom = troughs[i + 1]
        right_rim = troughs[i + 2]

        left_high = high.iloc[left_rim]
        bottom_low = low.iloc[cup_bottom]
        right_high = high.iloc[right_rim]

        # Check cup depth
        cup_depth = (left_high - bottom_low) / left_high
        if cup_depth < min_cup_depth:
            continue

        # Check rims roughly equal
        rim_diff = abs(left_high - right_high) / left_high
        if rim_diff > 0.05:
            continue

        # Look for handle (small pullback after right rim)
        handle_start = right_rim
        handle_region = close.iloc[handle_start:handle_start + 20]

        if len(handle_region) < 5:
            continue

        handle_low = handle_region.min()
        handle_depth = (right_high - handle_low) / right_high

        if handle_depth > max_handle_depth:
            continue

        # Breakout above right rim
        break_idx = None
        for j in range(handle_start + 5, min(handle_start + 30, len(close))):
            if close.iloc[j] > right_high:
                break_idx = j
                break

        if break_idx is not None:
            target = right_high + (right_high - bottom_low)
            stop = handle_low

            signals.append(PatternSignal(
                pattern_type=PatternType.CUP_AND_HANDLE,
                direction=PatternDirection.BULLISH,
                confidence=0.7,
                start_idx=left_rim,
                end_idx=break_idx,
                key_levels={
                    "left_rim": left_high,
                    "cup_bottom": bottom_low,
                    "right_rim": right_high,
                    "handle_low": handle_low,
                },
                target_price=target,
                stop_loss=stop,
                description="Cup and Handle continuation pattern detected",
            ))

    return signals


def detect_all_patterns(
    df: pd.DataFrame,
    include_candlestick: bool = True
) -> List[PatternSignal]:
    """Detect all chart patterns in DataFrame."""
    signals = []

    high = df["high"]
    low = df["low"]
    close = df["close"]

    # Chart patterns
    signals.extend(detect_head_and_shoulders(high, low, close))
    signals.extend(detect_inverse_head_and_shoulders(high, low, close))
    signals.extend(detect_double_top(high, low, close))
    signals.extend(detect_double_bottom(high, low, close))
    signals.extend(detect_triangles(high, low, close))
    signals.extend(detect_cup_and_handle(high, low, close))

    # Candlestick patterns (if OHLC available)
    if include_candlestick and "open" in df.columns:
        signals.extend(detect_candlestick_patterns(df))

    # Sort by confidence
    signals.sort(key=lambda s: s.confidence, reverse=True)

    return signals


def detect_candlestick_patterns(df: pd.DataFrame) -> List[PatternSignal]:
    """Detect candlestick patterns."""
    signals = []

    open_ = df["open"]
    high = df["high"]
    low = df["low"]
    close = df["close"]

    for i in range(2, len(df)):
        # Doji
        body = abs(close.iloc[i] - open_.iloc[i])
        range_ = high.iloc[i] - low.iloc[i]
        if range_ > 0 and body / range_ < 0.1:
            signals.append(PatternSignal(
                pattern_type=PatternType.DOJI,
                direction=PatternDirection.NEUTRAL,
                confidence=0.5,
                start_idx=i,
                end_idx=i,
                key_levels={"price": close.iloc[i]},
                description="Doji - indecision candle",
            ))

        # Hammer / Hanging Man
        lower_shadow = min(open_.iloc[i], close.iloc[i]) - low.iloc[i]
        upper_shadow = high.iloc[i] - max(open_.iloc[i], close.iloc[i])
        body_size = abs(close.iloc[i] - open_.iloc[i])

        if body_size > 0 and lower_shadow > 2 * body_size and upper_shadow < body_size:
            if close.iloc[i] > open_.iloc[i]:  # Green hammer
                direction = PatternDirection.BULLISH
                pattern = PatternType.HAMMER
            else:  # Red hanging man
                direction = PatternDirection.BEARISH
                pattern = PatternType.HANGING_MAN

            signals.append(PatternSignal(
                pattern_type=pattern,
                direction=direction,
                confidence=0.6,
                start_idx=i,
                end_idx=i,
                key_levels={"price": close.iloc[i]},
                description=f"{pattern.value.replace('_', ' ').title()} detected",
            ))

        # Shooting Star / Inverted Hammer
        if body_size > 0 and upper_shadow > 2 * body_size and lower_shadow < body_size:
            if close.iloc[i] < open_.iloc[i]:  # Red shooting star
                direction = PatternDirection.BEARISH
                pattern = PatternType.SHOOTING_STAR
            else:  # Green inverted hammer
                direction = PatternDirection.BULLISH
                pattern = PatternType.INVERTED_HAMMER

            signals.append(PatternSignal(
                pattern_type=pattern,
                direction=direction,
                confidence=0.6,
                start_idx=i,
                end_idx=i,
                key_levels={"price": close.iloc[i]},
                description=f"{pattern.value.replace('_', ' ').title()} detected",
            ))

        # Engulfing
        if i >= 1:
            prev_open = open_.iloc[i-1]
            prev_close = close.iloc[i-1]
            curr_open = open_.iloc[i]
            curr_close = close.iloc[i]

            bullish = (prev_close < prev_open) and (curr_close > curr_open) and \
                      (curr_close > prev_open) and (curr_open < prev_close)
            bearish = (prev_close > prev_open) and (curr_close < curr_open) and \
                      (curr_close < prev_open) and (curr_open > prev_close)

            if bullish:
                signals.append(PatternSignal(
                    pattern_type=PatternType.BULLISH_ENGULFING,
                    direction=PatternDirection.BULLISH,
                    confidence=0.7,
                    start_idx=i-1,
                    end_idx=i,
                    key_levels={"price": curr_close},
                    description="Bullish Engulfing pattern",
                ))
            elif bearish:
                signals.append(PatternSignal(
                    pattern_type=PatternType.BEARISH_ENGULFING,
                    direction=PatternDirection.BEARISH,
                    confidence=0.7,
                    start_idx=i-1,
                    end_idx=i,
                    key_levels={"price": curr_close},
                    description="Bearish Engulfing pattern",
                ))

    return signals