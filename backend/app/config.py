"""
config.py — Single source of truth for all environment configuration.
Reads from .env file via Pydantic Settings.
"""

from pydantic_settings import BaseSettings
from pydantic import field_validator
from functools import lru_cache


class Settings(BaseSettings):
    """
    All configuration values come from the .env file.
    If a required value is missing, the app will fail to start — by design.
    """

    # ── Application ──────────────────────────────────────────────────────
    APP_NAME: str = "Nexus Vault API"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False

    # ── Database ──────────────────────────────────────────────────────────
    DATABASE_URL: str  # Required — must be in .env

    # ── CORS ──────────────────────────────────────────────────────────────
    # Comma-separated list of allowed origins (e.g. "http://localhost:3000")
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:3001"

    @field_validator("DATABASE_URL")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        if not v.startswith("postgresql"):
            raise ValueError("DATABASE_URL must be a PostgreSQL connection string")
        return v

    def get_allowed_origins(self) -> list[str]:
        """Parse ALLOWED_ORIGINS string into a list."""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """
    Cached settings instance — only reads .env once per process.
    Use this as a FastAPI dependency: Depends(get_settings)
    """
    return Settings()
