"""
Base repository interface for article storage.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime

from ..models.article import Article, ArticleSource


class ArticleRepository(ABC):
    """Abstract base class for article storage."""

    @abstractmethod
    def save_article(self, article: Article) -> bool:
        """
        Save a single article.

        Args:
            article: The article to save

        Returns:
            True if successful, False otherwise
        """
        pass

    @abstractmethod
    def save_articles(self, articles: List[Article]) -> int:
        """
        Save multiple articles.

        Args:
            articles: List of articles to save

        Returns:
            Number of articles successfully saved
        """
        pass

    @abstractmethod
    def get_article(self, url: str) -> Optional[Article]:
        """
        Retrieve an article by URL.

        Args:
            url: The article URL
w
        Returns:
            Article if found, None otherwise
        """
        pass

    @abstractmethod
    def get_articles_by_source(
        self,
        source: ArticleSource,
        limit: Optional[int] = None
    ) -> List[Article]:
        """
        Retrieve articles from a specific source.

        Args:
            source: The news source
            limit: Maximum number of articles to retrieve

        Returns:
            List of articles
        """
        pass

    @abstractmethod
    def get_articles_by_date_range(
        self,
        from_date: datetime,
        to_date: datetime,
        source: Optional[ArticleSource] = None
    ) -> List[Article]:
        """
        Retrieve articles within a date range.

        Args:
            from_date: Start date
            to_date: End date
            source: Optional source filter

        Returns:
            List of articles
        """
        pass

    @abstractmethod
    def article_exists(self, url: str) -> bool:
        """
        Check if an article already exists.

        Args:
            url: The article URL

        Returns:
            True if article exists, False otherwise
        """
        pass

    @abstractmethod
    def count_articles(self, source: Optional[ArticleSource] = None) -> int:
        """
        Count total articles.

        Args:
            source: Optional source filter

        Returns:
            Number of articles
        """
        pass

    @abstractmethod
    def delete_article(self, url: str) -> bool:
        """
        Delete an article.

        Args:
            url: The article URL

        Returns:
            True if successful, False otherwise
        """
        pass
