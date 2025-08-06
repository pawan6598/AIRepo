"""Tests for configuration loading."""
from __future__ import annotations

from app.core.config import Settings


def test_settings_load() -> None:
    """Ensure settings can be instantiated."""
    settings = Settings(
        openai_api_key="test",
        database_url="sqlite:///:memory:",
        mongodb_uri="mongodb://localhost:27017",
        jwt_secret="secret",
    )
    assert settings.openai_api_key == "test"
