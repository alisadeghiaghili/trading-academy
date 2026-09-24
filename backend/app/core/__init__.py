"""Core package initialization.

Heavy submodules (licensing, coaching, websocket) depend on the database layer
and are imported lazily to avoid circular imports with app.db.session.
"""

from typing import Any

from app.core.config import settings, get_settings
from app.core.i18n import (
    I18nManager,
    get_i18n_manager,
    _,
    ngettext,
    detect_locale_from_header,
    validate_locale,
)
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
    create_license_token,
    verify_license_token,
    get_features_for_tier,
    has_feature,
    TIER_FEATURES,
)

_LAZY_EXPORTS = {
    "LicenseManager": "app.core.licensing",
    "get_license_manager": "app.core.licensing",
    "TradingCoach": "app.core.coaching",
    "CoachingFeedback": "app.core.coaching",
    "FeedbackType": "app.core.coaching",
    "FeedbackSeverity": "app.core.coaching",
    "ConnectionManager": "app.core.websocket",
    "SubscriptionType": "app.core.websocket",
    "get_connection_manager": "app.core.websocket",
    "WSMessage": "app.core.websocket",
    "TickerMessage": "app.core.websocket",
    "OHLCVMessage": "app.core.websocket",
    "OrderBookMessage": "app.core.websocket",
    "TradeMessage": "app.core.websocket",
    "SubscriptionMessage": "app.core.websocket",
    "ErrorMessage": "app.core.websocket",
    "HeartbeatMessage": "app.core.websocket",
}


def __getattr__(name: str) -> Any:
    """Resolve lazy exports on first attribute access."""
    module_path = _LAZY_EXPORTS.get(name)
    if module_path is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    import importlib

    module = importlib.import_module(module_path)
    value = getattr(module, name)
    globals()[name] = value
    return value


def __dir__() -> list[str]:
    return sorted(list(globals().keys()) + list(_LAZY_EXPORTS.keys()))


__all__ = [
    "settings",
    "get_settings",
    "I18nManager",
    "get_i18n_manager",
    "_",
    "ngettext",
    "detect_locale_from_header",
    "validate_locale",
    "hash_password",
    "verify_password",
    "create_access_token",
    "create_refresh_token",
    "decode_token",
    "create_license_token",
    "verify_license_token",
    "get_features_for_tier",
    "has_feature",
    "TIER_FEATURES",
    "LicenseManager",
    "get_license_manager",
    "TradingCoach",
    "CoachingFeedback",
    "FeedbackType",
    "FeedbackSeverity",
    "ConnectionManager",
    "SubscriptionType",
    "get_connection_manager",
    "WSMessage",
    "TickerMessage",
    "OHLCVMessage",
    "OrderBookMessage",
    "TradeMessage",
    "SubscriptionMessage",
    "ErrorMessage",
    "HeartbeatMessage",
]
