"""
The Guardian API source implementation.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
import logging

from .base import NewsSource, NewsSourceException, AuthenticationException
from ..models.article import Article, ArticleSource

logger = logging.getLogger(__name__)


class GuardianSource(NewsSource):
    """News source implementation for The Guardian API."""

    BASE_URL = "https://content.guardianapis.com"

    def __init__(self, credentials: Optional[Dict[str, str]] = None, **kwargs):
        """Initialize Guardian source."""
        super().__init__(
            source_id=ArticleSource.GUARDIAN,
            credentials=credentials,
            rate_limit=60,  # 60 requests per minute
            **kwargs
        )

    def requires_credentials(self) -> bool:
        """Guardian API requires an API key."""
        return True

    def validate_credentials(self) -> bool:
        """Validate Guardian API credentials."""
        if not self.credentials.get('api_key'):
            raise AuthenticationException("Guardian API requires an 'api_key' credential")

        try:
            response = self._make_request(
                f"{self.BASE_URL}/search",
                params={
                    'api-key': self.credentials['api_key'],
                    'page-size': 1
                }
            )
            data = response.json()
            return data.get('response', {}).get('status') == 'ok'

        except Exception as e:
            logger.error(f"Guardian API credential validation failed: {e}")
            return False

    def fetch_articles(
        self,
        max_articles: int = 50,
        category: Optional[str] = None,
        query: Optional[str] = None,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None
    ) -> List[Article]:
        """Fetch articles from The Guardian API."""
        articles = []

        try:
            # Default to political news
            search_query = query or "politics OR election OR government"

            params: Dict[str, Any] = {
                'api-key': self.credentials.get('api_key'),
                'q': search_query,
                'page-size': min(max_articles, 50),
                'show-fields': 'all',
                'show-tags': 'all',
                'order-by': 'newest'
            }

            if category:
                params['section'] = category

            if from_date:
                params['from-date'] = from_date.strftime('%Y-%m-%d')

            if to_date:
                params['to-date'] = to_date.strftime('%Y-%m-%d')

            response = self._make_request(f"{self.BASE_URL}/search", params=params)
            data = response.json()

            if data.get('response', {}).get('status') != 'ok':
                raise NewsSourceException("Guardian API returned error status")

            for item in data.get('response', {}).get('results', []):
                try:
                    article = self._parse_article(item)
                    if article:
                        articles.append(article)
                except Exception as e:
                    logger.warning(f"Failed to parse Guardian article: {e}")
                    continue

            logger.info(f"Fetched {len(articles)} articles from The Guardian")

        except Exception as e:
            logger.error(f"Failed to fetch articles from The Guardian: {e}")
            raise NewsSourceException(f"Guardian API fetch failed: {str(e)}")

        return articles

    def _parse_article(self, item: Dict[str, Any]) -> Optional[Article]:
        """Parse a Guardian API article response."""
        try:
            fields = item.get('fields', {})
            tags = item.get('tags', [])
            
            # Check content length - skip if insufficient
            content = fields.get('bodyText', '')
            
            # Require at least 200 characters of content
            if not content or len(content.strip()) < 200:
                logger.debug(f"Skipping Guardian article with insufficient content: {item.get('webTitle', '')[:50]}")
                return None

            # Extract keywords from tags
            keywords = [tag.get('webTitle', '') for tag in tags if tag.get('webTitle')]

            return Article(
                title=item.get('webTitle', ''),
                description=fields.get('trailText') or fields.get('standfirst'),
                content=content,
                url=item.get('webUrl', ''),
                source=ArticleSource.GUARDIAN,
                author=fields.get('byline'),
                published_at=item.get('webPublicationDate', datetime.utcnow().isoformat()),
                image_url=fields.get('thumbnail'),
                categories=[item.get('sectionName', '')] if item.get('sectionName') else [],
                keywords=keywords
            )

        except Exception as e:
            logger.warning(f"Failed to parse Guardian article: {e}")
            return None

    def get_categories(self) -> List[str]:
        """Get available Guardian categories (sections)."""
        return [
            'politics',
            'world',
            'us-news',
            'business',
            'opinion',
            'technology',
            'science',
            'environment',
            'education',
            'society'
        ]
