"""
NewsAPI.org source implementation.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
import logging

from .base import NewsSource, NewsSourceException, AuthenticationException
from ..models.article import Article, ArticleSource

logger = logging.getLogger(__name__)


class NewsAPISource(NewsSource):
    """News source implementation for NewsAPI.org."""

    BASE_URL = "https://newsapi.org/v2"

    def __init__(self, credentials: Optional[Dict[str, str]] = None, **kwargs):
        """Initialize NewsAPI source."""
        super().__init__(
            source_id=ArticleSource.NEWSAPI,
            credentials=credentials,
            rate_limit=100,  # 100 requests per day for free tier
            **kwargs
        )

    def requires_credentials(self) -> bool:
        """NewsAPI requires an API key."""
        return True

    def validate_credentials(self) -> bool:
        """Validate NewsAPI credentials."""
        if not self.credentials.get('api_key'):
            raise AuthenticationException("NewsAPI requires an 'api_key' credential")

        try:
            # Test the API key with a simple request
            response = self._make_request(
                f"{self.BASE_URL}/top-headlines",
                params={
                    'apiKey': self.credentials['api_key'],
                    'country': 'us',
                    'pageSize': 1
                }
            )
            data = response.json()
            return data.get('status') == 'ok'

        except Exception as e:
            logger.error(f"NewsAPI credential validation failed: {e}")
            return False

    def fetch_articles(
        self,
        max_articles: int = 50,
        category: Optional[str] = None,
        query: Optional[str] = None,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None
    ) -> List[Article]:
        """Fetch articles from NewsAPI."""
        articles = []

        try:
            # Default to political news if no query provided
            if not query and not category:
                query = "politics OR election OR government OR congress OR senate OR biden OR trump"

            params: Dict[str, Any] = {
                'apiKey': self.credentials.get('api_key'),
                'language': 'en',
                'sortBy': 'publishedAt',
                'pageSize': min(max_articles, 100),
            }

            # Use appropriate endpoint
            if query or from_date or to_date:
                endpoint = f"{self.BASE_URL}/everything"
                params['q'] = query or 'politics'

                if from_date:
                    params['from'] = from_date.strftime('%Y-%m-%d')
                if to_date:
                    params['to'] = to_date.strftime('%Y-%m-%d')
            else:
                endpoint = f"{self.BASE_URL}/top-headlines"
                params['country'] = 'us'
                if category:
                    params['category'] = category

            response = self._make_request(endpoint, params=params)
            data = response.json()

            if data.get('status') != 'ok':
                raise NewsSourceException(f"NewsAPI error: {data.get('message', 'Unknown error')}")

            for item in data.get('articles', []):
                try:
                    article = self._parse_article(item)
                    if article:
                        articles.append(article)
                except Exception as e:
                    logger.warning(f"Failed to parse NewsAPI article: {e}")
                    continue

            logger.info(f"Fetched {len(articles)} articles from NewsAPI")

        except Exception as e:
            logger.error(f"Failed to fetch articles from NewsAPI: {e}")
            raise NewsSourceException(f"NewsAPI fetch failed: {str(e)}")

        return articles

    def _parse_article(self, item: Dict[str, Any]) -> Optional[Article]:
        """Parse a NewsAPI article response."""
        try:
            # Skip articles without titles or URLs
            if not item.get('title') or not item.get('url'):
                return None

            # Skip removed articles
            if '[Removed]' in str(item.get('title', '')):
                return None

            return Article(
                title=item['title'],
                description=item.get('description'),
                content=item.get('content'),
                url=item['url'],
                source=ArticleSource.NEWSAPI,
                author=item.get('author'),
                published_at=item.get('publishedAt', datetime.utcnow().isoformat()),
                image_url=item.get('urlToImage'),
                categories=[],
                keywords=[]
            )

        except Exception as e:
            logger.warning(f"Failed to parse article: {e}")
            return None

    def get_categories(self) -> List[str]:
        """Get available NewsAPI categories."""
        return [
            'business',
            'entertainment',
            'general',
            'health',
            'science',
            'sports',
            'technology'
        ]
