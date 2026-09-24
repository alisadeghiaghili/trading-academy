"""License management core: generation, validation, enforcement."""

import hashlib
import hmac
import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID, uuid4

from app.core.config import settings
from app.core.security import (
    create_license_token,
    get_features_for_tier,
    has_feature,
    verify_license_token,
)
from app.db.models import License, LicenseStatus, User, UserRole


class LicenseManager:
    """Manages license keys and validation."""

    def __init__(self):
        self.issuer = "trading-academy"

    def generate_license_key(self, user_id: UUID, tier: UserRole) -> str:
        """Generate a new license key.

        Args:
            user_id: User UUID.
            tier: License tier.

        Returns:
            License key string.
        """
        # Format: TA-{tier}-{random}-{checksum}
        tier_prefix = tier.value.upper()[:3]
        random_part = secrets.token_urlsafe(16)
        raw = f"TA-{tier_prefix}-{random_part}"
        checksum = self._calculate_checksum(raw)
        return f"{raw}-{checksum}"

    def _calculate_checksum(self, data: str) -> str:
        """Calculate HMAC checksum for license key.

        Args:
            data: Data to checksum.

        Returns:
            Hex checksum (8 chars).
        """
        secret = settings.SECRET_KEY.encode()
        return hmac.new(secret, data.encode(), hashlib.sha256).hexdigest()[:8]

    def verify_license_key_format(self, license_key: str) -> bool:
        """Verify license key format and checksum.

        Args:
            license_key: License key to verify.

        Returns:
            True if valid format and checksum.
        """
        parts = license_key.split("-")
        if len(parts) != 4:
            return False
        if parts[0] != "TA":
            return False

        raw = "-".join(parts[:3])
        provided_checksum = parts[3]
        calculated_checksum = self._calculate_checksum(raw)

        return hmac.compare_digest(provided_checksum, calculated_checksum)

    def extract_tier_from_key(self, license_key: str) -> Optional[UserRole]:
        """Extract tier from license key.

        Args:
            license_key: License key string.

        Returns:
            UserRole or None if invalid.
        """
        parts = license_key.split("-")
        if len(parts) < 2:
            return None

        tier_prefix = parts[1].lower()
        tier_map = {
            "fre": UserRole.FREE,
            "pro": UserRole.PRO,
            "ins": UserRole.INSTITUTIONAL,
        }
        return tier_map.get(tier_prefix)

    def create_license(
        self,
        user: User,
        tier: UserRole,
        expires_in_days: Optional[int] = None,
    ) -> License:
        """Create a new license for user.

        Args:
            user: User model.
            tier: License tier.
            expires_in_days: Days until expiration (None for lifetime).

        Returns:
            Created License model.
        """
        license_key = self.generate_license_key(user.id, tier)

        expires_at = None
        if expires_in_days:
            expires_at = datetime.now(timezone.utc) + timedelta(days=expires_in_days)

        license_obj = License(
            user_id=user.id,
            license_key=license_key,
            tier=tier,
            status=LicenseStatus.ACTIVE,
            expires_at=expires_at,
            extra={
                "features": get_features_for_tier(tier.value),
                "issued_by": "system",
            },
        )

        return license_obj

    def validate_license(self, license_obj: License) -> tuple[bool, str]:
        """Validate a license object.

        Args:
            license_obj: License to validate.

        Returns:
            Tuple of (is_valid, reason).
        """
        # Check status
        if license_obj.status != LicenseStatus.ACTIVE:
            return False, f"License status: {license_obj.status.value}"

        # Check expiration
        if license_obj.expires_at and license_obj.expires_at < datetime.now(timezone.utc):
            return False, "License expired"

        # Verify key format
        if not self.verify_license_key_format(license_obj.license_key):
            return False, "Invalid license key format"

        # Verify tier matches key
        key_tier = self.extract_tier_from_key(license_obj.license_key)
        if key_tier and key_tier != license_obj.tier:
            return False, "License key tier mismatch"

        return True, "Valid"

    def create_license_jwt(self, license_obj: License) -> str:
        """Create JWT token for license.

        Args:
            license_obj: Validated license object.

        Returns:
            Signed JWT token.
        """
        expires_at = license_obj.expires_at or (datetime.now(timezone.utc) + timedelta(days=36500))
        return create_license_token(
            license_key=license_obj.license_key,
            user_id=license_obj.user_id,
            tier=license_obj.tier.value,
            features=get_features_for_tier(license_obj.tier.value),
            expires_at=expires_at,
        )

    def verify_license_jwt(self, token: str) -> tuple[bool, Optional[dict]]:
        """Verify license JWT token.

        Args:
            token: License JWT token.

        Returns:
            Tuple of (is_valid, payload_dict).
        """
        try:
            payload = verify_license_token(token)
            # Check expiration
            if datetime.now(timezone.utc).timestamp() > payload.exp:
                return False, {"error": "Token expired"}
            return True, payload.model_dump()
        except Exception as e:
            return False, {"error": str(e)}

    def check_feature_access(self, license_obj: License, feature: str) -> bool:
        """Check if license has access to a feature.

        Args:
            license_obj: License to check.
            feature: Feature name.

        Returns:
            True if feature is accessible.
        """
        valid, _ = self.validate_license(license_obj)
        if not valid:
            return False

        features = license_obj.extra.get("features", [])
        return "all" in features or feature in features

    def revoke_license(self, license_obj: License, reason: str = "revoked") -> License:
        """Revoke a license.

        Args:
            license_obj: License to revoke.
            reason: Revocation reason.

        Returns:
            Updated license object.
        """
        license_obj.status = LicenseStatus.REVOKED
        license_obj.revoked_at = datetime.now(timezone.utc)
        license_obj.extra["revocation_reason"] = reason
        return license_obj

    def renew_license(self, license_obj: License, additional_days: int) -> License:
        """Renew a license for additional days.

        Args:
            license_obj: License to renew.
            additional_days: Days to add.

        Returns:
            Updated license object.
        """
        if license_obj.expires_at and license_obj.expires_at > datetime.now(timezone.utc):
            license_obj.expires_at += timedelta(days=additional_days)
        else:
            license_obj.expires_at = datetime.now(timezone.utc) + timedelta(days=additional_days)

        license_obj.status = LicenseStatus.ACTIVE
        license_obj.extra["last_renewal"] = datetime.now(timezone.utc).isoformat()
        return license_obj


# Global instance
_license_manager: Optional[LicenseManager] = None


def get_license_manager() -> LicenseManager:
    """Get global license manager instance."""
    global _license_manager
    if _license_manager is None:
        _license_manager = LicenseManager()
    return _license_manager