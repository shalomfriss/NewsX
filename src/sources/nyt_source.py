"""
New York Times API source implementation.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
import logging

from .base import NewsSource, NewsSourceException, AuthenticationException
from ..models.article import Article, ArticleSource

logger = logging.getLogger(__name__)


class NYTSource(NewsSource):
    """News source implementation for New York Times API."""

    BASE_URL = "https://api.nytimes.com/svc"

    def __init__(self, credentials: Optional[Dict[str, str]] = None, **kwargs):
        """Initialize NYT source."""
        super().__init__(
            source_id=ArticleSource.NYT,
            credentials=credentials,
            rate_limit=60,  # Conservative rate limit
            **kwargs
        )

    def requires_credentials(self) -> bool:
        """NYT API requires an API key."""
        return True

    def validate_credentials(self) -> bool:
        """Validate NYT API credentials."""
        if not self.credentials.get('api_key'):
            raise AuthenticationException("NYT API requires an 'api_key' credential")

        try:
            response = self._make_request(
                f"{self.BASE_URL}/topstories/v2/home.json",
                params={'api-key': self.credentials['api_key']}
            )
            data = response.json()
            return data.get('status') == 'OK'

        except Exception as e:
            logger.error(f"NYT API credential validation failed: {e}")
            return False

    def fetch_articles(
        self,
        max_articles: int = 50,
        category: Optional[str] = None,
        query: Optional[str] = None,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None
    ) -> List[Article]:
        """Fetch articles from NYT API."""
        articles = []

        try:
            # Use Top Stories API or Article Search API
            if query or from_date or to_date:
                articles = self._fetch_from_search(
                    query=query or "politics",
                    max_articles=max_articles,
                    from_date=from_date,
                    to_date=to_date
                )
            else:
                # Use Top Stories API
                section = category or 'politics'
                articles = self._fetch_top_stories(section, max_articles)

            logger.info(f"Fetched {len(articles)} articles from NYT")

        except Exception as e:
            logger.error(f"Failed to fetch articles from NYT: {e}")
            raise NewsSourceException(f"NYT API fetch failed: {str(e)}")

        return articles

    def _fetch_top_stories(self, section: str, max_articles: int) -> List[Article]:
        """Fetch top stories from NYT."""
        articles = []

        response = self._make_request(
            f"{self.BASE_URL}/topstories/v2/{section}.json",
            params={'api-key': self.credentials.get('api_key')}
        )
        data = response.json()

        if data.get('status') != 'OK':
            raise NewsSourceException("NYT API returned error status")

        for item in data.get('results', [])[:max_articles]:
            try:
                article = self._parse_top_story(item)
                if article:
                    articles.append(article)
            except Exception as e:
                logger.warning(f"Failed to parse NYT article: {e}")
                continue

        return articles

    def _fetch_from_search(
        self,
        query: str,
        max_articles: int,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None
    ) -> List[Article]:
        """Fetch articles from NYT Article Search API."""
        articles = []

        params: Dict[str, Any] = {
            'api-key': self.credentials.get('api_key'),
            'q': query,
            'sort': 'newest',
            'fl': 'web_url,headline,abstract,lead_paragraph,source,pub_date,byline,multimedia,keywords'
        }

        if from_date:
            params['begin_date'] = from_date.strftime('%Y%m%d')

        if to_date:
            params['end_date'] = to_date.strftime('%Y%m%d')

        # Calculate pages needed
        page_size = 10
        total_pages = (max_articles + page_size - 1) // page_size

        for page in range(min(total_pages, 10)):  # Max 10 pages
            params['page'] = page

            response = self._make_request(
                f"{self.BASE_URL}/search/v2/articlesearch.json",
                params=params
            )
            data = response.json()

            if data.get('status') != 'OK':
                break

            for item in data.get('response', {}).get('docs', []):
                try:
                    article = self._parse_search_result(item)
                    if article:
                        articles.append(article)
                        if len(articles) >= max_articles:
                            return articles
                except Exception as e:
                    logger.warning(f"Failed to parse NYT search result: {e}")
                    continue

        return articles

    def _parse_top_story(self, item: Dict[str, Any]) -> Optional[Article]:
        """Parse a NYT Top Stories article."""
        try:
            # Check content length - NYT Top Stories only provide abstracts
            # Skip if abstract is too short
            abstract = item.get('abstract', '')
            if not abstract or len(abstract.strip()) < 100:
                logger.debug(f"Skipping NYT story with insufficient abstract: {item.get('title', '')[:50]}")
                return None
            
            # Get image URL
            image_url = None
            multimedia = item.get('multimedia', [])
            if multimedia:
                # Find largest image
                for media in multimedia:
                    if media.get('format') in ['superJumbo', 'Large Thumbnail']:
                        image_url = media.get('url')
                        break

            return Article(
                title=item.get('title', ''),
                description=abstract,
                content=abstract,  # NYT Top Stories don't provide full content via API
                url=item.get('url', ''),
                source=ArticleSource.NYT,
                author=item.get('byline'),
                published_at=item.get('published_date', datetime.utcnow().isoformat()),
                image_url=image_url,
                categories=[item.get('section', '')],
                keywords=item.get('des_facet', [])
            )

        except Exception as e:
            logger.warning(f"Failed to parse NYT top story: {e}")
            return None

    def _parse_search_result(self, item: Dict[str, Any]) -> Optional[Article]:
        """Parse a NYT Article Search result."""
        try:
            headline = item.get('headline', {})
            if not headline or not isinstance(headline, dict):
                logger.debug(f"NYT article missing headline: {item}")
                return None

            title = headline.get('main', '')
            if not title:
                logger.debug(f"NYT article has empty title")
                return None
            
            # Check content - NYT search provides lead_paragraph and abstract
            abstract = item.get('abstract', '')
            lead_paragraph = item.get('lead_paragraph', '')
            content = lead_paragraph or abstract
            
            # Require at least some substantive content
            if not content or len(content.strip()) < 100:
                logger.debug(f"Skipping NYT article with insufficient content: {title[:50]}")
                return None

            byline = item.get('byline', {})
            if not isinstance(byline, dict):
                byline = {}

            # Get image URL
            image_url = None
            multimedia = item.get('multimedia', [])
            if multimedia and isinstance(multimedia, list):
                image_url = f"https://www.nytimes.com/{multimedia[0].get('url', '')}"

            # Extract keywords
            keywords = []
            for keyword_obj in item.get('keywords', []):
                if isinstance(keyword_obj, dict) and keyword_obj.get('value'):
                    keywords.append(keyword_obj['value'])

            return Article(
                title=title,
                description=abstract,
                content=content,
                url=item.get('web_url', ''),
                source=ArticleSource.NYT,
                author=byline.get('original'),
                published_at=item.get('pub_date', datetime.utcnow().isoformat()),
                image_url=image_url,
                categories=[item.get('section_name', '')] if item.get('section_name') else [],
                keywords=keywords
            )

        except Exception as e:
            logger.warning(f"Failed to parse NYT search result: {e}", exc_info=True)
            return None

    def get_categories(self) -> List[str]:
        """Get available NYT categories."""
        return [
            'arts',
            'automobiles',
            'books',
            'business',
            'fashion',
            'food',
            'health',
            'home',
            'insider',
            'magazine',
            'movies',
            'nyregion',
            'obituaries',
            'opinion',
            'politics',
            'realestate',
            'science',
            'sports',
            'sundayreview',
            'technology',
            'theater',
            't-magazine',
            'travel',
            'upshot',
            'us',
            'world'
        ]
