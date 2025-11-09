"""
Base classes and interfaces for news sources.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging
import time
from collections import deque
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from ..models.article import Article, ArticleSource

logger = logging.getLogger(__name__)


class NewsSourceException(Exception):
    """Base exception for news source errors."""
    pass


class RateLimitException(NewsSourceException):
    """Raised when rate limit is exceeded."""
    pass


class AuthenticationException(NewsSourceException):
    """Raised when authentication fails."""
    pass


class NewsSource(ABC):
    """Abstract base class for all news sources."""

    def __init__(
        self,
        source_id: ArticleSource,
        credentials: Optional[Dict[str, str]] = None,
        timeout: int = 30,
        max_retries: int = 3,
        rate_limit: Optional[int] = None
    ):
        """
        Initialize the news source.

        Args:
            source_id: The source identifier
            credentials: Optional credentials dictionary
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
            rate_limit: Maximum requests per minute (None for no limit)
        """
        self.source_id = source_id
        self.credentials = credentials or {}
        self.timeout = timeout
        self.max_retries = max_retries
        self.rate_limit = rate_limit

        # Rate limiting state
        self._request_times: deque = deque(maxlen=rate_limit if rate_limit else None)

        # Create session with retry logic
        self.session = self._create_session()

    def _create_session(self) -> requests.Session:
        """Create a requests session with retry logic."""
        session = requests.Session()

        # Configure retry strategy
        retry_strategy = Retry(
            total=self.max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        return session

    def _check_rate_limit(self):
        """Check and enforce rate limiting."""
        if not self.rate_limit:
            return

        now = time.time()

        # Remove requests older than 1 minute
        cutoff = now - 60
        while self._request_times and self._request_times[0] < cutoff:
            self._request_times.popleft()

        # Check if we've exceeded the rate limit
        if len(self._request_times) >= self.rate_limit:
            sleep_time = 60 - (now - self._request_times[0])
            if sleep_time > 0:
                logger.warning(
                    f"Rate limit reached for {self.source_id}. "
                    f"Sleeping for {sleep_time:.2f} seconds."
                )
                raise RateLimitException(
                    f"Rate limit exceeded. Please wait {sleep_time:.2f} seconds."
                )

        # Record this request
        self._request_times.append(now)

    def _make_request(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> requests.Response:
        """
        Make an HTTP request with rate limiting and error handling.

        Args:
            url: The URL to request
            params: Query parameters
            headers: HTTP headers

        Returns:
            Response object

        Raises:
            NewsSourceException: On request failure
        """
        self._check_rate_limit()

        try:
            response = self.session.get(
                url,
                params=params,
                headers=headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise AuthenticationException(
                    f"Authentication failed for {self.source_id}: {str(e)}"
                )
            elif e.response.status_code == 429:
                raise RateLimitException(
                    f"Rate limit exceeded for {self.source_id}: {str(e)}"
                )
            else:
                raise NewsSourceException(
                    f"HTTP error for {self.source_id}: {str(e)}"
                )

        except requests.exceptions.RequestException as e:
            raise NewsSourceException(
                f"Request failed for {self.source_id}: {str(e)}"
            )

    @abstractmethod
    def requires_credentials(self) -> bool:
        """
        Check if this source requires credentials.

        Returns:
            True if credentials are required
        """
        pass

    @abstractmethod
    def validate_credentials(self) -> bool:
        """
        Validate that provided credentials are correct.

        Returns:
            True if credentials are valid

        Raises:
            AuthenticationException: If credentials are invalid
        """
        pass

    @abstractmethod
    def fetch_articles(
        self,
        max_articles: int = 50,
        category: Optional[str] = None,
        query: Optional[str] = None,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None
    ) -> List[Article]:
        """
        Fetch articles from the news source.

        Args:
            max_articles: Maximum number of articles to fetch
            category: Optional category filter
            query: Optional search query
            from_date: Optional start date
            to_date: Optional end date

        Returns:
            List of Article objects

        Raises:
            NewsSourceException: On fetch failure
        """
        pass

    @abstractmethod
    def get_categories(self) -> List[str]:
        """
        Get available categories for this source.

        Returns:
            List of category names
        """
        pass

    def __str__(self) -> str:
        """String representation."""
        return f"{self.__class__.__name__}({self.source_id.value})"

    def __repr__(self) -> str:
        """Detailed representation."""
        return (
            f"{self.__class__.__name__}("
            f"source_id={self.source_id.value}, "
            f"has_credentials={bool(self.credentials)})"
        )
