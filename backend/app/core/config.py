"""Application configuration module."""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Application settings loaded from environment and optional YAML config."""

    env_file: str | None = ".env"
    log_level: str = Field("INFO", env="LOG_LEVEL")
    openai_api_key: str = Field("changeme", env="OPENAI_API_KEY")
    database_url: str = Field("sqlite:///:memory:", env="DATABASE_URL")
    mongodb_uri: str = Field("mongodb://localhost:27017", env="MONGODB_URI")
    jwt_secret: str = Field("secret", env="JWT_SECRET")
    sentry_dsn: str | None = Field(None, env="SENTRY_DSN")

    class Config:
        env_file_encoding = "utf-8"


def load_yaml_config(path: str | Path) -> dict[str, Any]:
    """Load parameters from a YAML configuration file if PyYAML available."""
    try:
        import yaml  # type: ignore
    except Exception:
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


@lru_cache()
def get_settings() -> Settings:
    """Return cached settings instance."""
    return Settings()


settings = get_settings()
