"""Core package initialization."""

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
from app.core.licensing import (
    LicenseManager,
    get_license_manager,
)
from app.core.coaching import (
    TradingCoach,
    CoachingFeedback,
    FeedbackType,
    FeedbackSeverity,
)
from app.core.websocket import (
    ConnectionManager,
    SubscriptionType,
    get_connection_manager,
    WSMessage,
    TickerMessage,
    OHLCVMessage,
    OrderBookMessage,
    TradeMessage,
    SubscriptionMessage,
    ErrorMessage,
    HeartbeatMessage,
)

__all__ = [
    # Config
    "settings",
    "get_settings",
    # I18n
    "I18nManager",
    "get_i18n_manager",
    "_",
    "ngettext",
    "detect_locale_from_header",
    "validate_locale",
    # Security
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
    # Licensing
    "LicenseManager",
    "get_license_manager",
    # Coaching
    "TradingCoach",
    "CoachingFeedback",
    "FeedbackType",
    "FeedbackSeverity",
    # WebSocket
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