"""
Secure credential storage and management.
"""

import json
import logging
from pathlib import Path
from typing import Dict, Optional
from cryptography.fernet import Fernet
import os
import base64
import hashlib

logger = logging.getLogger(__name__)


class CredentialStore:
    """Manages secure storage and retrieval of API credentials."""

    def __init__(self, storage_path: Optional[Path] = None, encryption_key: Optional[str] = None):
        """
        Initialize the credential store.

        Args:
            storage_path: Path to store encrypted credentials
            encryption_key: Optional custom encryption key (will be generated if not provided)
        """
        self.storage_path = storage_path or Path.home() / ".news_aggregator" / "credentials.enc"
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)

        # Generate or load encryption key
        self.key_path = self.storage_path.parent / ".key"
        self.encryption_key = self._get_or_create_key(encryption_key)
        self.cipher = Fernet(self.encryption_key)

    def _get_or_create_key(self, custom_key: Optional[str] = None) -> bytes:
        """Get or create an encryption key."""
        if custom_key:
            # Use custom key (hash it to ensure correct length)
            key_hash = hashlib.sha256(custom_key.encode()).digest()
            return base64.urlsafe_b64encode(key_hash)

        # Try to load existing key
        if self.key_path.exists():
            try:
                with open(self.key_path, 'rb') as f:
                    return f.read()
            except Exception as e:
                logger.warning(f"Failed to load encryption key: {e}")

        # Generate new key
        key = Fernet.generate_key()
        try:
            # Store key securely (600 permissions on Unix-like systems)
            with open(self.key_path, 'wb') as f:
                f.write(key)
            os.chmod(self.key_path, 0o600)
        except Exception as e:
            logger.warning(f"Failed to save encryption key: {e}")

        return key

    def save_credentials(self, credentials: Dict[str, Dict[str, str]]) -> bool:
        """
        Save credentials securely.

        Args:
            credentials: Dictionary of credentials keyed by source ID

        Returns:
            True if successful, False otherwise
        """
        try:
            # Merge with existing credentials
            existing = self.load_credentials()
            existing.update(credentials)

            # Convert to JSON
            json_data = json.dumps(existing, indent=2)

            # Encrypt
            encrypted_data = self.cipher.encrypt(json_data.encode())

            # Save to file
            with open(self.storage_path, 'wb') as f:
                f.write(encrypted_data)

            # Set file permissions (Unix-like systems)
            try:
                os.chmod(self.storage_path, 0o600)
            except Exception:
                pass  # Windows doesn't support chmod

            logger.info(f"Credentials saved successfully to {self.storage_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to save credentials: {e}")
            return False

    def load_credentials(self) -> Dict[str, Dict[str, str]]:
        """
        Load and decrypt credentials.

        Returns:
            Dictionary of credentials keyed by source ID
        """
        if not self.storage_path.exists():
            return {}

        try:
            # Read encrypted data
            with open(self.storage_path, 'rb') as f:
                encrypted_data = f.read()

            # Decrypt
            decrypted_data = self.cipher.decrypt(encrypted_data)

            # Parse JSON
            credentials = json.loads(decrypted_data.decode())

            return credentials

        except Exception as e:
            logger.error(f"Failed to load credentials: {e}")
            return {}

    def get_credential(self, source_id: str, field: str) -> Optional[str]:
        """
        Get a specific credential field for a source.

        First checks environment variables, then falls back to encrypted storage.
        Environment variable format: {SOURCE_ID}_{FIELD} (e.g., NEWSAPI_API_KEY)

        Args:
            source_id: The news source identifier
            field: The credential field name (e.g., 'api_key')

        Returns:
            The credential value or None if not found
        """
        # Check environment variables first
        env_var_name = f"{source_id.upper()}_{field.upper()}"
        env_value = os.getenv(env_var_name)
        if env_value:
            logger.debug(f"Using credential from environment variable: {env_var_name}")
            return env_value

        # Fall back to encrypted storage
        credentials = self.load_credentials()
        return credentials.get(source_id, {}).get(field)

    def has_credentials(self, source_id: str) -> bool:
        """
        Check if credentials exist for a source.

        Checks both environment variables and encrypted storage.

        Args:
            source_id: The news source identifier

        Returns:
            True if credentials exist, False otherwise
        """
        # Check common environment variable patterns
        env_var_patterns = [
            f"{source_id.upper()}_API_KEY",
            f"{source_id.upper()}_KEY",
        ]
        for env_var in env_var_patterns:
            if os.getenv(env_var):
                logger.debug(f"Found credential in environment: {env_var}")
                return True

        # Check encrypted storage
        credentials = self.load_credentials()
        return source_id in credentials and bool(credentials[source_id])

    def delete_credentials(self, source_id: Optional[str] = None) -> bool:
        """
        Delete credentials for a source or all credentials.

        Args:
            source_id: The news source identifier (None to delete all)

        Returns:
            True if successful, False otherwise
        """
        try:
            if source_id is None:
                # Delete all credentials
                if self.storage_path.exists():
                    self.storage_path.unlink()
                logger.info("All credentials deleted")
            else:
                # Delete specific source credentials
                credentials = self.load_credentials()
                if source_id in credentials:
                    del credentials[source_id]
                    return self.save_credentials(credentials)

            return True

        except Exception as e:
            logger.error(f"Failed to delete credentials: {e}")
            return False

    def list_configured_sources(self) -> list:
        """
        Get a list of sources with configured credentials.

        Returns:
            List of source IDs
        """
        credentials = self.load_credentials()
        return list(credentials.keys())
