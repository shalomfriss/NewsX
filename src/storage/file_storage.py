"""
File system-based article storage implementation.
"""

import logging
from pathlib import Path
from typing import List, Optional
from datetime import datetime
import json
import hashlib

from .base import ArticleRepository
from ..models.article import Article, ArticleSource

logger = logging.getLogger(__name__)


class FileSystemRepository(ArticleRepository):
    """Stores articles as markdown files with JSON index."""

    def __init__(self, base_dir: Path):
        """
        Initialize file system repository.

        Args:
            base_dir: Base directory for storing articles
        """
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

        # Create source-specific subdirectories
        for source in ArticleSource:
            source_dir = self.base_dir / source.value
            source_dir.mkdir(parents=True, exist_ok=True)

        # Index file for quick lookups
        self.index_file = self.base_dir / "index.json"
        self.index = self._load_index()

    def _load_index(self) -> dict:
        """Load the article index."""
        if self.index_file.exists():
            try:
                with open(self.index_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load index: {e}")
                return {}
        return {}

    def _save_index(self):
        """Save the article index."""
        try:
            with open(self.index_file, 'w', encoding='utf-8') as f:
                json.dump(self.index, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Failed to save index: {e}")

    def _get_url_hash(self, url: str) -> str:
        """Generate a hash for a URL."""
        return hashlib.md5(url.encode()).hexdigest()

    def save_article(self, article: Article) -> bool:
        """Save a single article."""
        try:
            # Get source value (handle both string and enum)
            source_value = article.source.value if isinstance(article.source, ArticleSource) else str(article.source)

            # Generate filename
            source_dir = self.base_dir / source_value
            filename = article.get_filename()
            filepath = source_dir / filename

            # Check if article already exists
            url_hash = self._get_url_hash(str(article.url))
            if url_hash in self.index:
                logger.info(f"Article already exists: {article.title}")
                return False

            # Write markdown file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(article.to_markdown())

            # Update index
            self.index[url_hash] = {
                'url': str(article.url),
                'title': article.title,
                'source': source_value,
                'published_at': article.published_at.isoformat(),
                'fetched_at': article.fetched_at.isoformat(),
                'filepath': str(filepath.relative_to(self.base_dir))
            }
            self._save_index()

            logger.info(f"Saved article: {article.title}")
            return True

        except Exception as e:
            logger.error(f"Failed to save article {article.title}: {e}")
            return False

    def save_articles(self, articles: List[Article]) -> int:
        """Save multiple articles."""
        count = 0
        for article in articles:
            if self.save_article(article):
                count += 1
        return count

    def get_article(self, url: str) -> Optional[Article]:
        """Retrieve an article by URL."""
        url_hash = self._get_url_hash(url)
        if url_hash not in self.index:
            return None

        try:
            entry = self.index[url_hash]
            filepath = self.base_dir / entry['filepath']

            if not filepath.exists():
                logger.warning(f"Article file not found: {filepath}")
                return None

            # Note: This returns metadata only. Full markdown parsing would be needed
            # to reconstruct the complete Article object. For now, we return basic info.
            return Article(
                title=entry['title'],
                url=entry['url'],
                source=ArticleSource(entry['source']),
                published_at=datetime.fromisoformat(entry['published_at']),
                fetched_at=datetime.fromisoformat(entry['fetched_at'])
            )

        except Exception as e:
            logger.error(f"Failed to retrieve article: {e}")
            return None

    def get_articles_by_source(
        self,
        source: ArticleSource,
        limit: Optional[int] = None
    ) -> List[Article]:
        """Retrieve articles from a specific source."""
        articles = []
        source_value = source.value if isinstance(source, ArticleSource) else str(source)

        for url_hash, entry in self.index.items():
            if entry['source'] == source_value:
                try:
                    article = Article(
                        title=entry['title'],
                        url=entry['url'],
                        source=ArticleSource(entry['source']),
                        published_at=datetime.fromisoformat(entry['published_at']),
                        fetched_at=datetime.fromisoformat(entry['fetched_at'])
                    )
                    articles.append(article)

                    if limit and len(articles) >= limit:
                        break

                except Exception as e:
                    logger.warning(f"Failed to parse article entry: {e}")
                    continue

        return articles

    def get_articles_by_date_range(
        self,
        from_date: datetime,
        to_date: datetime,
        source: Optional[ArticleSource] = None
    ) -> List[Article]:
        """Retrieve articles within a date range."""
        articles = []

        for url_hash, entry in self.index.items():
            try:
                published_at = datetime.fromisoformat(entry['published_at'])

                if published_at < from_date or published_at > to_date:
                    continue

                if source and entry['source'] != source.value:
                    continue

                article = Article(
                    title=entry['title'],
                    url=entry['url'],
                    source=ArticleSource(entry['source']),
                    published_at=published_at,
                    fetched_at=datetime.fromisoformat(entry['fetched_at'])
                )
                articles.append(article)

            except Exception as e:
                logger.warning(f"Failed to parse article entry: {e}")
                continue

        return articles

    def article_exists(self, url: str) -> bool:
        """Check if an article already exists."""
        url_hash = self._get_url_hash(url)
        return url_hash in self.index

    def count_articles(self, source: Optional[ArticleSource] = None) -> int:
        """Count total articles."""
        if not source:
            return len(self.index)

        count = 0
        for entry in self.index.values():
            if entry['source'] == source.value:
                count += 1
        return count

    def delete_article(self, url: str) -> bool:
        """Delete an article."""
        url_hash = self._get_url_hash(url)
        if url_hash not in self.index:
            return False

        try:
            entry = self.index[url_hash]
            filepath = self.base_dir / entry['filepath']

            if filepath.exists():
                filepath.unlink()

            del self.index[url_hash]
            self._save_index()

            logger.info(f"Deleted article: {entry['title']}")
            return True

        except Exception as e:
            logger.error(f"Failed to delete article: {e}")
            return False
