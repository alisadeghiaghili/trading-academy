"""Internationalization (i18n) utilities using Babel and gettext."""

import gettext
import os
from functools import lru_cache
from pathlib import Path
from typing import Optional

from babel import Locale
from babel.support import Translations

from app.core.config import settings


class I18nManager:
    """Manages translations for supported locales."""

    def __init__(self, locale_dir: Optional[str] = None):
        """Initialize i18n manager.

        Args:
            locale_dir: Path to locale directory containing .mo files.
        """
        self.locale_dir = Path(locale_dir or settings.LOCALE_DIR)
        self.default_locale = settings.DEFAULT_LOCALE
        self.supported_locales = settings.SUPPORTED_LOCALES
        self._translations: dict[str, Translations] = {}
        self._load_translations()

    def _load_translations(self) -> None:
        """Load all translation catalogs."""
        for locale in self.supported_locales:
            try:
                trans = Translations.load(
                    str(self.locale_dir),
                    locales=[locale],
                    domain="messages",
                )
                self._translations[locale] = trans
            except (OSError, IOError):
                # Fallback to NullTranslations if catalog not found
                self._translations[locale] = gettext.NullTranslations()

    def get_translation(self, locale: str) -> Translations:
        """Get translation object for locale.

        Args:
            locale: Locale code (e.g., 'en', 'fa', 'de').

        Returns:
            Translations object for the locale.
        """
        if locale not in self._translations:
            locale = self.default_locale
        return self._translations.get(locale, self._translations[self.default_locale])

    def translate(self, message: str, locale: Optional[str] = None, **kwargs) -> str:
        """Translate a message.

        Args:
            message: Message ID to translate.
            locale: Target locale (defaults to default_locale).
            **kwargs: Format parameters for the translation.

        Returns:
            Translated and formatted message.
        """
        if locale is None:
            locale = self.default_locale
        trans = self.get_translation(locale)
        translated = trans.gettext(message)
        if kwargs:
            try:
                translated = translated.format(**kwargs)
            except (KeyError, ValueError):
                pass
        return translated

    def ntranslate(
        self,
        singular: str,
        plural: str,
        n: int,
        locale: Optional[str] = None,
        **kwargs,
    ) -> str:
        """Translate a pluralizable message.

        Args:
            singular: Singular form message ID.
            plural: Plural form message ID.
            n: Number to determine plural form.
            locale: Target locale.
            **kwargs: Format parameters.

        Returns:
            Translated message.
        """
        if locale is None:
            locale = self.default_locale
        trans = self.get_translation(locale)
        translated = trans.ngettext(singular, plural, n)
        if kwargs:
            try:
                translated = translated.format(**kwargs)
            except (KeyError, ValueError):
                pass
        return translated

    def get_locale_info(self, locale: str) -> dict:
        """Get locale metadata.

        Args:
            locale: Locale code.

        Returns:
            Dictionary with locale information.
        """
        try:
            babel_locale = Locale.parse(locale)
            return {
                "code": locale,
                "name": babel_locale.get_display_name(locale),
                "english_name": babel_locale.get_display_name("en"),
                "native_name": babel_locale.get_display_name(locale),
                "rtl": Locale.parse(locale).text_direction == "rtl",
                "date_format": babel_locale.date_formats["medium"],
                "datetime_format": babel_locale.datetime_formats["medium"],
                "number_format": babel_locale.number_formats["decimal"],
                "currency_format": babel_locale.currency_formats["standard"],
            }
        except Exception:
            return {
                "code": locale,
                "name": locale,
                "english_name": locale,
                "native_name": locale,
                "rtl": locale == "fa",
                "date_format": "MMM d, y",
                "datetime_format": "MMM d, y, h:mm a",
                "number_format": "#,##0.###",
                "currency_format": "¤#,##0.00",
            }

    def get_all_locales_info(self) -> list[dict]:
        """Get info for all supported locales."""
        return [self.get_locale_info(loc) for loc in self.supported_locales]


# Global instance
_i18n_manager: Optional[I18nManager] = None


def get_i18n_manager() -> I18nManager:
    """Get global i18n manager instance."""
    global _i18n_manager
    if _i18n_manager is None:
        _i18n_manager = I18nManager()
    return _i18n_manager


def _(message: str, locale: Optional[str] = None, **kwargs) -> str:
    """Convenience function for translation."""
    return get_i18n_manager().translate(message, locale, **kwargs)


def ngettext(
    singular: str,
    plural: str,
    n: int,
    locale: Optional[str] = None,
    **kwargs,
) -> str:
    """Convenience function for plural translation."""
    return get_i18n_manager().ntranslate(singular, plural, n, locale, **kwargs)


# Locale detection utilities
def detect_locale_from_header(accept_language: str) -> str:
    """Detect best matching locale from Accept-Language header.

    Args:
        accept_language: Value of Accept-Language header.

    Returns:
        Best matching supported locale.
    """
    # Simple parsing - in production use proper parsing
    languages = []
    for part in accept_language.split(","):
        lang_part = part.split(";")[0].strip().lower()
        if "-" in lang_part:
            base = lang_part.split("-")[0]
            languages.append(lang_part)
            languages.append(base)
        else:
            languages.append(lang_part)

    for lang in languages:
        if lang in settings.SUPPORTED_LOCALES:
            return lang
    return settings.DEFAULT_LOCALE


def validate_locale(locale: str) -> str:
    """Validate and normalize locale code.

    Args:
        locale: Locale code to validate.

    Returns:
        Validated locale code (falls back to default if invalid).
    """
    locale = locale.lower().strip()
    if locale in settings.SUPPORTED_LOCALES:
        return locale
    # Try base language
    base = locale.split("-")[0]
    if base in settings.SUPPORTED_LOCALES:
        return base
    return settings.DEFAULT_LOCALE