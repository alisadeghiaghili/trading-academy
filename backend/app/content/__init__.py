"""Curriculum content package.

Each module exports a dict matching the seed loader schema:
    {
        "slug": str,
        "title": str,
        "description": str,
        "order": int,
        "required_tier": str,
        "lessons": list[dict],
    }
"""

from app.content.crypto_basics import CRYPTO_BASICS
from app.content.technical_analysis import TECHNICAL_ANALYSIS
from app.content.risk_management import RISK_MANAGEMENT
from app.content.fundamental_analysis import FUNDAMENTAL_ANALYSIS
from app.content.portfolio_management import PORTFOLIO_MANAGEMENT

CURRICULUM = [
    CRYPTO_BASICS,
    TECHNICAL_ANALYSIS,
    RISK_MANAGEMENT,
    FUNDAMENTAL_ANALYSIS,
    PORTFOLIO_MANAGEMENT,
]

__all__ = ["CURRICULUM"]
