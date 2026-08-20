"""
Central application configuration for Voryent AI Studio backend.

This module loads all environment-specific settings from environment
variables and the local `.env` file using Pydantic Settings.

Secrets are never hardcoded. They must be provided through the
environment or `.env`, and `.env` must never be committed to Git.
"""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings.

    Values are loaded from environment variables and `.env` automatically.
    """

    # ------------------------------------------------------------------
    # Application
    # ------------------------------------------------------------------
    APP_NAME: str = "Voryent AI Studio"
    ENVIRONMENT: str = "development"
    DEBUG: bool = False

    # ------------------------------------------------------------------
    # Database
    # ------------------------------------------------------------------
    DATABASE_URL: str

    # ------------------------------------------------------------------
    # Security / Authentication
    # ------------------------------------------------------------------
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours

    # ------------------------------------------------------------------
    # Redis / Queue
    # ------------------------------------------------------------------
    REDIS_URL: str = "redis://localhost:6379/0"

    # ------------------------------------------------------------------
    # CORS
    # ------------------------------------------------------------------
    CORS_ORIGINS: list[str] = Field(
        default_factory=lambda: [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ]
    )

    # ------------------------------------------------------------------
    # Pydantic Settings behaviour
    # ------------------------------------------------------------------
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    @property
    def is_development(self) -> bool:
        """Return True when running in a development environment."""
        return self.ENVIRONMENT.lower() == "development"

    @property
    def is_production(self) -> bool:
        """Return True when running in a production environment."""
        return self.ENVIRONMENT.lower() == "production"


# Global settings instance.
# Import this anywhere in the backend using:
#   from app.core.config import settings
settings = Settings()