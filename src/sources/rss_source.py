"""
RSS feed source implementation for news sources without APIs.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
import logging
import feedparser
from email.utils import parsedate_to_datetime

from .base import NewsSource, NewsSourceException
from ..models.article import Article, ArticleSource

logger = logging.getLogger(__name__)


class RSSSource(NewsSource):
    """Generic RSS feed source for news outlets without dedicated APIs."""

    # RSS feed URLs for various sources
    RSS_FEEDS = {
        ArticleSource.BBC: [
            "http://feeds.bbci.co.uk/news/politics/rss.xml",
            "http://feeds.bbci.co.uk/news/world/rss.xml",
            "http://feeds.bbci.co.uk/news/uk/rss.xml"
        ],
        ArticleSource.REUTERS: [
            "https://www.reutersagency.com/feed/?taxonomy=best-topics&post_type=best",
            "https://www.reuters.com/rssfeed/domesticNews",
            "https://www.reuters.com/rssfeed/politicsNews"
        ],
        ArticleSource.POLITICO: [
            "https://www.politico.com/rss/politics08.xml",
            "https://www.politico.com/rss/congress.xml",
            "https://www.politico.com/rss/whitehouse.xml"
        ],
        ArticleSource.THE_HILL: [
            "https://thehill.com/news/feed/",
            "https://thehill.com/homenews/administration/feed/",
            "https://thehill.com/homenews/senate/feed/"
        ],
        ArticleSource.NPR: [
            "https://feeds.npr.org/1001/rss.xml",  # News
            "https://feeds.npr.org/1014/rss.xml",  # Politics
            "https://feeds.npr.org/1003/rss.xml"   # U.S.
        ],
        ArticleSource.CNN: [
            "http://rss.cnn.com/rss/cnn_topstories.rss",
            "http://rss.cnn.com/rss/cnn_us.rss",
            "http://rss.cnn.com/rss/cnn_allpolitics.rss"
        ],
        ArticleSource.ABC: [
            "https://abcnews.go.com/abcnews/topstories",
            "https://abcnews.go.com/abcnews/politicsheadlines"
        ],
        ArticleSource.CBS: [
            "https://www.cbsnews.com/latest/rss/main",
            "https://www.cbsnews.com/latest/rss/politics"
        ],
        ArticleSource.NBC: [
            "https://feeds.nbcnews.com/nbcnews/public/news",
            "https://feeds.nbcnews.com/nbcnews/public/politics"
        ],
        ArticleSource.PBS: [
            "https://www.pbs.org/newshour/feeds/rss/headlines",
            "https://www.pbs.org/newshour/feeds/rss/politics"
        ],
        ArticleSource.WASHINGTON_POST: [
            "https://feeds.washingtonpost.com/rss/politics",
            "https://feeds.washingtonpost.com/rss/national"
        ],
        ArticleSource.THE_ATLANTIC: [
            "https://www.theatlantic.com/feed/all/",
            "https://www.theatlantic.com/feed/channel/politics/"
        ],
        ArticleSource.PROPUBLICA: [
            "https://www.propublica.org/feeds/propublica/main"
        ],
        ArticleSource.AL_JAZEERA: [
            "https://www.aljazeera.com/xml/rss/all.xml",
            "https://www.aljazeera.com/xml/rss/us-canada.xml",
            "https://www.aljazeera.com/xml/rss/americas.xml"
        ]
    }

    def __init__(self, source_id: ArticleSource, credentials: Optional[Dict[str, str]] = None, **kwargs):
        """Initialize RSS source."""
        super().__init__(
            source_id=source_id,
            credentials=credentials,
            rate_limit=30,  # Conservative rate limit for RSS
            **kwargs
        )

        self.feed_urls = self.RSS_FEEDS.get(source_id, [])
        if not self.feed_urls:
            raise NewsSourceException(f"No RSS feeds configured for {source_id}")

    def requires_credentials(self) -> bool:
        """RSS feeds don't require credentials."""
        return False

    def validate_credentials(self) -> bool:
        """No credentials to validate for RSS feeds."""
        return True

    def fetch_articles(
        self,
        max_articles: int = 50,
        category: Optional[str] = None,
        query: Optional[str] = None,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None
    ) -> List[Article]:
        """Fetch articles from RSS feeds."""
        articles = []
        articles_per_feed = max(1, max_articles // len(self.feed_urls))

        for feed_url in self.feed_urls:
            try:
                feed_articles = self._fetch_from_feed(
                    feed_url,
                    max_articles=articles_per_feed,
                    query=query,
                    from_date=from_date,
                    to_date=to_date
                )
                articles.extend(feed_articles)

                if len(articles) >= max_articles:
                    break

            except Exception as e:
                logger.warning(f"Failed to fetch from RSS feed {feed_url}: {e}")
                continue

        # Sort by published date (newest first)
        articles.sort(key=lambda x: x.published_at, reverse=True)

        # Trim to max_articles
        articles = articles[:max_articles]

        logger.info(f"Fetched {len(articles)} articles from {self.source_id.value} RSS feeds")
        return articles

    def _fetch_from_feed(
        self,
        feed_url: str,
        max_articles: int = 20,
        query: Optional[str] = None,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None
    ) -> List[Article]:
        """Fetch articles from a single RSS feed."""
        articles = []

        try:
            # Parse the RSS feed
            feed = feedparser.parse(feed_url)

            if feed.bozo:
                logger.warning(f"RSS feed parsing warning for {feed_url}: {feed.bozo_exception}")

            logger.debug(f"Feed {feed_url} has {len(feed.entries)} total entries")

            for entry in feed.entries[:max_articles]:
                try:
                    article = self._parse_entry(entry)

                    if not article:
                        logger.debug(f"Failed to parse entry from {feed_url}")
                        continue

                    # Apply filters
                    if from_date and article.published_at < from_date:
                        logger.debug(f"Article filtered by from_date: {article.title}")
                        continue

                    if to_date and article.published_at > to_date:
                        logger.debug(f"Article filtered by to_date: {article.title}")
                        continue

                    if query and query.strip():
                        # Support OR queries by splitting on " OR "
                        query_lower = query.lower()
                        title_lower = article.title.lower()
                        desc_lower = (article.description or '').lower()
                        content_lower = (article.content or '').lower()

                        # Check if query contains OR operator
                        if ' or ' in query_lower:
                            # Split by OR and check if any term matches
                            keywords = [k.strip() for k in query_lower.split(' or ') if k.strip()]
                            match_found = False
                            for keyword in keywords:
                                if keyword in title_lower or keyword in desc_lower or keyword in content_lower:
                                    match_found = True
                                    break

                            if not match_found:
                                logger.debug(f"Article filtered by query '{query}': {article.title}")
                                continue
                        else:
                            # Simple keyword matching
                            if query_lower not in title_lower and query_lower not in desc_lower and query_lower not in content_lower:
                                logger.debug(f"Article filtered by query '{query}': {article.title}")
                                continue

                    logger.debug(f"Article accepted: {article.title}")
                    articles.append(article)

                except Exception as e:
                    logger.warning(f"Failed to parse RSS entry: {e}")
                    continue

        except Exception as e:
            logger.error(f"Failed to fetch RSS feed {feed_url}: {e}")
            raise NewsSourceException(f"RSS feed fetch failed: {str(e)}")

        return articles

    def _parse_entry(self, entry) -> Optional[Article]:
        """Parse an RSS feed entry."""
        try:
            # Extract title
            title = entry.get('title', '')
            if not title:
                return None

            # Extract URL
            url = entry.get('link', '')
            if not url:
                return None

            # Extract description/summary
            description = entry.get('summary') or entry.get('description')

            # Extract content
            content = None
            if hasattr(entry, 'content'):
                content = entry.content[0].value
            elif description:
                content = description

            # Extract author
            author = entry.get('author') or entry.get('dc:creator')

            # Extract published date
            published_at = datetime.utcnow()
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                try:
                    published_at = datetime(*entry.published_parsed[:6])
                except Exception:
                    pass
            elif hasattr(entry, 'published'):
                try:
                    published_at = parsedate_to_datetime(entry.published)
                except Exception:
                    pass

            # Extract image
            image_url = None
            if hasattr(entry, 'media_content') and entry.media_content:
                image_url = entry.media_content[0].get('url')
            elif hasattr(entry, 'media_thumbnail') and entry.media_thumbnail:
                image_url = entry.media_thumbnail[0].get('url')

            # Extract tags/categories
            categories = []
            keywords = []
            if hasattr(entry, 'tags'):
                for tag in entry.tags:
                    tag_term = tag.get('term', '')
                    if tag_term:
                        keywords.append(tag_term)

            return Article(
                title=title,
                description=description,
                content=content,
                url=url,
                source=self.source_id,
                author=author,
                published_at=published_at,
                image_url=image_url,
                categories=categories,
                keywords=keywords
            )

        except Exception as e:
            logger.warning(f"Failed to parse RSS entry: {e}")
            return None

    def get_categories(self) -> List[str]:
        """RSS sources don't have predefined categories."""
        return []


# Factory function to create RSS sources
def create_rss_source(source_id: ArticleSource, **kwargs) -> RSSSource:
    """
    Create an RSS source for a given source ID.

    Args:
        source_id: The source identifier
        **kwargs: Additional arguments for the source

    Returns:
        RSSSource instance
    """
    return RSSSource(source_id=source_id, **kwargs)
