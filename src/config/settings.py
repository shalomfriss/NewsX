"""
Application settings and configuration.
"""

from pathlib import Path
from typing import Optional, List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables and .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow",
        env_parse_none_str="null"  # Prevent parsing issues with empty values
    )

    # Application settings
    app_name: str = "News Aggregator"
    debug: bool = Field(default=False, validation_alias="DEBUG")
    log_level: str = Field(default="INFO", validation_alias="LOG_LEVEL")

    # Storage settings
    storage_type: str = Field(default="file", validation_alias="STORAGE_TYPE")  # 'file' or 'database'
    news_md_dir: Path = Field(default=Path("news_md"), validation_alias="NEWS_MD_DIR")

    # Database settings (optional)
    database_url: Optional[str] = Field(default=None, validation_alias="DATABASE_URL")
    db_pool_size: int = Field(default=5, validation_alias="DB_POOL_SIZE")
    db_max_overflow: int = Field(default=10, validation_alias="DB_MAX_OVERFLOW")

    # API rate limiting
    rate_limit_calls: int = Field(default=100, validation_alias="RATE_LIMIT_CALLS")
    rate_limit_period: int = Field(default=3600, validation_alias="RATE_LIMIT_PERIOD")  # seconds

    # HTTP settings
    request_timeout: int = Field(default=30, validation_alias="REQUEST_TIMEOUT")
    max_retries: int = Field(default=3, validation_alias="MAX_RETRIES")
    retry_backoff_factor: float = Field(default=1.0, validation_alias="RETRY_BACKOFF_FACTOR")

    # News fetching settings
    max_articles_per_source: int = Field(default=50, validation_alias="MAX_ARTICLES_PER_SOURCE")
    fetch_political_only: bool = Field(default=True, validation_alias="FETCH_POLITICAL_ONLY")

    # Enabled sources
    # Using string type to avoid pydantic-settings JSON parsing
    # The validator will convert it to List[str]
    enabled_sources: List[str] = Field(
        default_factory=lambda: [
            "newsapi", "guardian", "nyt", "bbc", "reuters",
            "ap", "politico", "the_hill", "npr", "cnn",
            "abc", "cbs", "nbc", "pbs", "washington_post",
            "the_atlantic", "propublica", "al_jazeera"
        ]
    )

    # Credential storage
    credential_storage_path: Optional[Path] = Field(default=None, validation_alias="CREDENTIAL_STORAGE_PATH")

    @field_validator('news_md_dir', 'credential_storage_path', mode='before')
    @classmethod
    def convert_to_path(cls, v):
        """Convert string paths to Path objects."""
        if v is None:
            return v
        if isinstance(v, str):
            return Path(v)
        return v

    @field_validator('enabled_sources', mode='before')
    @classmethod
    def parse_enabled_sources(cls, v):
        """Parse comma-separated string or list."""
        if v is None or v == '':
            return []
        if isinstance(v, str):
            # Handle comma-separated values
            return [s.strip() for s in v.split(',') if s.strip()]
        if isinstance(v, list):
            return v
        return []

    def ensure_directories(self):
        """Create necessary directories if they don't exist."""
        if self.news_md_dir:
            self.news_md_dir.mkdir(parents=True, exist_ok=True)


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get the global settings instance."""
    global _settings
    if _settings is None:
        _settings = Settings()
        _settings.ensure_directories()
    return _settings


def reload_settings():
    """Reload settings from environment."""
    global _settings
    _settings = None
    return get_settings()
