"""Base classes for data fetchers."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional
import pandas as pd


@dataclass
class OHLCV:
    """Open, High, Low, Close, Volume data point."""

    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "timestamp": self.timestamp.isoformat(),
            "open": self.open,
            "high": self.high,
            "low": self.low,
            "close": self.close,
            "volume": self.volume,
        }


@dataclass
class TickerInfo:
    """Basic ticker information."""

    symbol: str
    name: str
    price: float
    change_24h: float
    change_24h_pct: float
    volume_24h: float
    market_cap: Optional[float] = None
    last_updated: Optional[datetime] = None


class BaseDataFetcher(ABC):
    """Abstract base class for all data fetchers."""

    def __init__(self, api_key: Optional[str] = None, api_secret: Optional[str] = None):
        """Initialize the data fetcher.

        Args:
            api_key: API key for authenticated endpoints.
            api_secret: API secret for authenticated endpoints.
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self._session = None

    @abstractmethod
    def fetch_ohlcv(
        self,
        symbol: str,
        timeframe: str = "1h",
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        limit: int = 1000,
    ) -> pd.DataFrame:
        """Fetch OHLCV data for a symbol.

        Args:
            symbol: Trading symbol (e.g., 'BTC/USDT').
            timeframe: Timeframe string (e.g., '1m', '5m', '1h', '1d').
            start: Start datetime (inclusive).
            end: End datetime (exclusive).
            limit: Maximum number of candles to fetch.

        Returns:
            DataFrame with columns: timestamp, open, high, low, close, volume.

        Raises:
            ValueError: If symbol or timeframe is invalid.
            ConnectionError: If API request fails.
        """
        pass

    @abstractmethod
    def fetch_ticker(self, symbol: str) -> TickerInfo:
        """Fetch current ticker information.

        Args:
            symbol: Trading symbol.

        Returns:
            TickerInfo with current market data.
        """
        pass

    @abstractmethod
    def fetch_symbols(self) -> list[str]:
        """Fetch list of available trading symbols.

        Returns:
            List of symbol strings.
        """
        pass

    def normalize_symbol(self, symbol: str) -> str:
        """Normalize symbol format for this exchange.

        Args:
            symbol: Raw symbol string.

        Returns:
            Normalized symbol.
        """
        return symbol.upper().replace("-", "/").replace("_", "/")

    def close(self) -> None:
        """Close any open connections."""
        if self._session:
            self._session.close()
            self._session = None

    def __enter__(self) -> "BaseDataFetcher":
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit."""
        self.close()


class CacheMixin:
    """Mixin for caching fetched data."""

    def __init__(self, *args, cache_dir: str = "data/cache", **kwargs):
        """Initialize cache mixin.

        Args:
            cache_dir: Directory for cache files.
            *args: Positional arguments for parent.
            **kwargs: Keyword arguments for parent.
        """
        super().__init__(*args, **kwargs)
        self.cache_dir = cache_dir

    def _get_cache_path(self, key: str) -> str:
        """Get cache file path for key.

        Args:
            key: Cache key.

        Returns:
            Full path to cache file.
        """
        import hashlib
        import os

        safe_key = hashlib.md5(key.encode()).hexdigest()
        return os.path.join(self.cache_dir, f"{safe_key}.parquet")

    def _load_from_cache(self, key: str, max_age_hours: int = 24) -> Optional[pd.DataFrame]:
        """Load DataFrame from cache if fresh enough.

        Args:
            key: Cache key.
            max_age_hours: Maximum age of cache in hours.

        Returns:
            Cached DataFrame or None if not found/expired.
        """
        import os
        from datetime import datetime, timedelta

        path = self._get_cache_path(key)
        if not os.path.exists(path):
            return None

        mtime = datetime.fromtimestamp(os.path.getmtime(path))
        if datetime.now() - mtime > timedelta(hours=max_age_hours):
            return None

        try:
            return pd.read_parquet(path)
        except Exception:
            return None

    def _save_to_cache(self, key: str, data: pd.DataFrame) -> None:
        """Save DataFrame to cache.

        Args:
            key: Cache key.
            data: DataFrame to cache.
        """
        import os

        os.makedirs(self.cache_dir, exist_ok=True)
        path = self._get_cache_path(key)
        data.to_parquet(path, index=False)