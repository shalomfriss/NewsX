"""
News aggregation service that coordinates fetching from multiple sources.
"""

import logging
from typing import List, Dict, Optional, Type
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed

from ..models.article import Article, ArticleSource
from ..sources.base import NewsSource, NewsSourceException, AuthenticationException
from ..sources.newsapi_source import NewsAPISource
from ..sources.guardian_source import GuardianSource
from ..sources.nyt_source import NYTSource
from ..sources.rss_source import RSSSource
from ..storage.base import ArticleRepository
from ..config.credentials import CredentialStore
from ..config.settings import Settings

logger = logging.getLogger(__name__)


class NewsAggregator:
    """Coordinates news fetching from multiple sources."""

    # Map source IDs to their implementation classes
    SOURCE_CLASSES: Dict[ArticleSource, Type[NewsSource]] = {
        ArticleSource.NEWSAPI: NewsAPISource,
        ArticleSource.GUARDIAN: GuardianSource,
        ArticleSource.NYT: NYTSource,
        # RSS-based sources
        ArticleSource.BBC: RSSSource,
        ArticleSource.REUTERS: RSSSource,
        ArticleSource.POLITICO: RSSSource,
        ArticleSource.THE_HILL: RSSSource,
        ArticleSource.NPR: RSSSource,
        ArticleSource.CNN: RSSSource,
        ArticleSource.ABC: RSSSource,
        ArticleSource.CBS: RSSSource,
        ArticleSource.NBC: RSSSource,
        ArticleSource.PBS: RSSSource,
        ArticleSource.WASHINGTON_POST: RSSSource,
        ArticleSource.THE_ATLANTIC: RSSSource,
        ArticleSource.PROPUBLICA: RSSSource,
        ArticleSource.AL_JAZEERA: RSSSource,
    }

    def __init__(
        self,
        repository: ArticleRepository,
        credential_store: CredentialStore,
        settings: Settings
    ):
        """
        Initialize the news aggregator.

        Args:
            repository: Article storage repository
            credential_store: Credential storage
            settings: Application settings
        """
        self.repository = repository
        self.credential_store = credential_store
        self.settings = settings
        self.sources: Dict[ArticleSource, NewsSource] = {}

        # Initialize available sources
        self._initialize_sources()

    def _initialize_sources(self):
        """Initialize news sources based on available credentials."""
        for source_id_str in self.settings.enabled_sources:
            try:
                # Convert string to ArticleSource enum
                source_id = ArticleSource(source_id_str)

                if source_id not in self.SOURCE_CLASSES:
                    logger.warning(f"No implementation found for source: {source_id}")
                    continue

                source_class = self.SOURCE_CLASSES[source_id]

                # Get credentials for this source
                credentials = None
                if source_id in [ArticleSource.NEWSAPI, ArticleSource.GUARDIAN, ArticleSource.NYT]:
                    if self.credential_store.has_credentials(source_id.value):
                        credentials = {}
                        # First check environment variables, then encrypted storage
                        api_key = self.credential_store.get_credential(source_id.value, 'api_key')
                        if api_key:
                            credentials['api_key'] = api_key
                        else:
                            # Fallback to loading all credentials from encrypted storage
                            creds = self.credential_store.load_credentials().get(source_id.value, {})
                            credentials.update(creds)

                # Create source instance
                if source_class == RSSSource:
                    source = source_class(
                        source_id=source_id,
                        timeout=self.settings.request_timeout,
                        max_retries=self.settings.max_retries
                    )
                else:
                    source = source_class(
                        credentials=credentials,
                        timeout=self.settings.request_timeout,
                        max_retries=self.settings.max_retries
                    )

                # Validate credentials if required
                if source.requires_credentials():
                    if not credentials:
                        logger.warning(
                            f"Source {source_id.value} requires credentials but none provided. Skipping."
                        )
                        continue

                    if not source.validate_credentials():
                        logger.warning(
                            f"Invalid credentials for {source_id.value}. Skipping."
                        )
                        continue

                self.sources[source_id] = source
                logger.info(f"Initialized source: {source_id.value}")

            except Exception as e:
                logger.error(f"Failed to initialize source {source_id_str}: {e}")
                continue

        logger.info(f"Initialized {len(self.sources)} news sources")

    def get_missing_credentials(self) -> List[str]:
        """
        Get list of sources that require credentials but don't have them.

        Returns:
            List of source IDs that need credentials
        """
        missing = []

        for source_id_str in self.settings.enabled_sources:
            try:
                source_id = ArticleSource(source_id_str)

                # Skip sources that don't require credentials
                if source_id not in [ArticleSource.NEWSAPI, ArticleSource.GUARDIAN, ArticleSource.NYT]:
                    continue

                # Check if credentials are available
                if not self.credential_store.has_credentials(source_id.value):
                    missing.append(source_id.value)

            except Exception as e:
                logger.warning(f"Error checking credentials for {source_id_str}: {e}")
                continue

        return missing

    def fetch_from_source(
        self,
        source_id: ArticleSource,
        max_articles: Optional[int] = None,
        query: Optional[str] = None,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None
    ) -> List[Article]:
        """
        Fetch articles from a specific source.

        Args:
            source_id: The source to fetch from
            max_articles: Maximum number of articles to fetch
            query: Optional search query
            from_date: Optional start date
            to_date: Optional end date

        Returns:
            List of fetched articles
        """
        if source_id not in self.sources:
            logger.warning(f"Source not available: {source_id.value}")
            return []

        source = self.sources[source_id]
        max_articles = max_articles or self.settings.max_articles_per_source

        try:
            articles = source.fetch_articles(
                max_articles=max_articles,
                query=query,
                from_date=from_date,
                to_date=to_date
            )

            logger.info(f"Fetched {len(articles)} articles from {source_id.value}")
            return articles

        except NewsSourceException as e:
            logger.error(f"Failed to fetch from {source_id.value}: {e}")
            return []

    def fetch_from_all_sources(
        self,
        max_articles_per_source: Optional[int] = None,
        query: Optional[str] = None,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        parallel: bool = True
    ) -> Dict[ArticleSource, List[Article]]:
        """
        Fetch articles from all available sources.

        Args:
            max_articles_per_source: Maximum articles per source
            query: Optional search query
            from_date: Optional start date
            to_date: Optional end date
            parallel: Fetch in parallel (default True)

        Returns:
            Dictionary mapping sources to their articles
        """
        results: Dict[ArticleSource, List[Article]] = {}

        if not self.sources:
            logger.warning("No sources available for fetching")
            return results

        max_articles = max_articles_per_source or self.settings.max_articles_per_source

        if parallel:
            # Fetch in parallel using ThreadPoolExecutor
            with ThreadPoolExecutor(max_workers=len(self.sources)) as executor:
                future_to_source = {
                    executor.submit(
                        self.fetch_from_source,
                        source_id,
                        max_articles,
                        query,
                        from_date,
                        to_date
                    ): source_id
                    for source_id in self.sources
                }

                for future in as_completed(future_to_source):
                    source_id = future_to_source[future]
                    try:
                        articles = future.result()
                        results[source_id] = articles
                    except Exception as e:
                        logger.error(f"Error fetching from {source_id.value}: {e}")
                        results[source_id] = []
        else:
            # Fetch sequentially
            for source_id in self.sources:
                articles = self.fetch_from_source(
                    source_id,
                    max_articles,
                    query,
                    from_date,
                    to_date
                )
                results[source_id] = articles

        total_articles = sum(len(articles) for articles in results.values())
        logger.info(f"Fetched {total_articles} total articles from {len(results)} sources")

        return results

    def fetch_and_save(
        self,
        max_articles_per_source: Optional[int] = None,
        query: Optional[str] = None,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        parallel: bool = True
    ) -> Dict[str, int]:
        """
        Fetch articles from all sources and save them.

        Args:
            max_articles_per_source: Maximum articles per source
            query: Optional search query
            from_date: Optional start date
            to_date: Optional end date
            parallel: Fetch in parallel (default True)

        Returns:
            Dictionary with statistics (fetched, saved, duplicates)
        """
        # Set default query for political news if enabled
        if self.settings.fetch_political_only and not query:
            query = "politics OR election OR government OR congress OR senate"

        # Fetch articles
        results = self.fetch_from_all_sources(
            max_articles_per_source=max_articles_per_source,
            query=query,
            from_date=from_date,
            to_date=to_date,
            parallel=parallel
        )

        # Save articles
        total_fetched = 0
        total_saved = 0

        for source_id, articles in results.items():
            total_fetched += len(articles)
            saved_count = self.repository.save_articles(articles)
            total_saved += saved_count

            logger.info(
                f"{source_id.value}: Fetched {len(articles)}, Saved {saved_count}"
            )

        duplicates = total_fetched - total_saved

        stats = {
            'fetched': total_fetched,
            'saved': total_saved,
            'duplicates': duplicates,
            'sources': len(results)
        }

        logger.info(
            f"Summary - Fetched: {total_fetched}, Saved: {total_saved}, "
            f"Duplicates: {duplicates}, Sources: {len(results)}"
        )

        return stats

    def get_available_sources(self) -> List[str]:
        """Get list of available source IDs."""
        return [source_id.value for source_id in self.sources.keys()]

    def get_source_statistics(self) -> Dict[str, Dict[str, any]]:
        """
        Get statistics for each source.

        Returns:
            Dictionary of source statistics
        """
        stats = {}

        for source_id in self.sources:
            article_count = self.repository.count_articles(source_id)
            stats[source_id.value] = {
                'available': True,
                'article_count': article_count,
                'requires_credentials': self.sources[source_id].requires_credentials()
            }

        return stats
