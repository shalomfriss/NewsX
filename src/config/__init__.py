"""Configuration management for the news aggregation system."""

from .settings import Settings, get_settings
from .credentials import CredentialStore

__all__ = ["Settings", "get_settings", "CredentialStore"]
