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
from ..utils.content_scraper import ContentScraper

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
            # Reuters RSS feeds are currently unavailable/blocked
            # Keeping empty to avoid errors
        ],
        ArticleSource.POLITICO: [
            "https://rss.politico.com/politics-news.xml",
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
            # CNN RSS feeds are currently unavailable/timing out
            # Disabled to prevent hanging
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

    def __init__(self, source_id: ArticleSource, credentials: Optional[Dict[str, str]] = None, 
                 fetch_full_content: bool = True, **kwargs):
        """
        Initialize RSS source.
        
        Args:
            source_id: The article source identifier
            credentials: Optional credentials (not used for RSS)
            fetch_full_content: Whether to scrape full article content from URLs
            **kwargs: Additional arguments
        """
        # Check if feeds are configured for this source
        self.feed_urls = self.RSS_FEEDS.get(source_id, [])
        if not self.feed_urls:
            logger.warning(f"No RSS feeds configured for {source_id.value}")
        
        super().__init__(
            source_id=source_id,
            credentials=credentials,
            rate_limit=30,  # Conservative rate limit for RSS
            **kwargs
        )
        
        self.fetch_full_content = fetch_full_content
        self.content_scraper = ContentScraper() if fetch_full_content else None

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
        if not self.feed_urls:
            logger.warning(f"✗ {self.source_id.value}: No RSS feeds available")
            return []
        
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
                logger.debug(f"Feed {feed_url[:50]} failed: {str(e)[:50]}")
                continue

        # Sort by published date (newest first)
        articles.sort(key=lambda x: x.published_at, reverse=True)

        # Trim to max_articles
        articles = articles[:max_articles]

        if articles:
            logger.info(f"✓ {self.source_id.value}: {len(articles)} articles")
        else:
            logger.warning(f"✗ {self.source_id.value}: No articles downloaded")
        
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
        
        # Extract category from feed URL
        feed_category = self._extract_category_from_url(feed_url)

        try:
            # Parse the RSS feed with timeout
            import socket
            original_timeout = socket.getdefaulttimeout()
            socket.setdefaulttimeout(self.timeout)
            
            try:
                feed = feedparser.parse(feed_url)
            finally:
                socket.setdefaulttimeout(original_timeout)

            if feed.bozo:
                logger.debug(f"RSS parse warning: {str(feed.bozo_exception)[:50]}")

            for entry in feed.entries[:max_articles]:
                try:
                    article = self._parse_entry(entry, feed_category)

                    if not article:
                        continue

                    # Apply filters
                    if from_date and article.published_at < from_date:
                        continue

                    if to_date and article.published_at > to_date:
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
                                continue
                        else:
                            # Simple keyword matching
                            if query_lower not in title_lower and query_lower not in desc_lower and query_lower not in content_lower:
                                continue

                    articles.append(article)

                except Exception as e:
                    logger.debug(f"Entry parse error: {str(e)[:40]}")
                    continue

        except Exception as e:
            logger.debug(f"Feed fetch failed: {str(e)[:50]}")
            return []

        return articles

    def _extract_category_from_url(self, url: str) -> Optional[str]:
        """Extract category/topic from feed URL."""
        # NPR feed IDs mapping
        npr_feeds = {
            '1001': 'News',
            '1014': 'Politics',
            '1003': 'US News',
        }
        
        # Check NPR feed IDs
        for feed_id, category in npr_feeds.items():
            if feed_id in url:
                return category
        
        # Common category patterns in RSS URLs
        categories = {
            'politics': 'Politics',
            'political': 'Politics',
            'congress': 'Congress',
            'whitehouse': 'White House',
            'world': 'World',
            'national': 'National',
            'us': 'US News',
            'domestic': 'Domestic',
            'administration': 'Administration',
            'senate': 'Senate',
            'defense': 'Defense',
            'policy': 'Policy',
            'topstories': 'Top Stories',
            'headlines': 'Headlines',
        }
        
        url_lower = url.lower()
        for key, category in categories.items():
            if key in url_lower:
                return category
        return None

    def _parse_entry(self, entry, feed_category: Optional[str] = None) -> Optional[Article]:
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
            
            # Fetch full content from article URL if enabled
            if self.fetch_full_content and url:
                try:
                    full_content = self.content_scraper.fetch_article_content(url)
                    if full_content and len(full_content) > len(content or ''):
                        content = full_content
                except Exception as e:
                    logger.debug(f"Scraping failed for {url[:50]}: {str(e)[:30]}")
                    pass
            
            # Skip articles without meaningful content
            if not content or len(content.strip()) < 100:
                logger.debug(f"Skipping article with insufficient content: {title[:50]}")
                return None

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
            
            # Add feed-level category first
            if feed_category and feed_category not in categories:
                categories.append(feed_category)
            
            if hasattr(entry, 'tags'):
                for tag in entry.tags:
                    tag_term = tag.get('term', '')
                    tag_scheme = tag.get('scheme', '') or ''
                    if tag_term:
                        # Skip numeric-only tags (likely feed IDs)
                        if tag_term.isdigit():
                            continue
                        
                        # If tag has a scheme/label indicating it's a category, use it as category
                        if tag.get('label') or 'category' in tag_scheme.lower():
                            if tag_term not in categories:
                                categories.append(tag_term)
                        else:
                            if tag_term not in keywords:
                                keywords.append(tag_term)
            
            # Also check for category field (skip if numeric)
            if hasattr(entry, 'category'):
                cat_val = entry.category if isinstance(entry.category, str) else str(entry.category)
                if cat_val and not cat_val.isdigit() and cat_val not in categories:
                    categories.append(cat_val)
            
            # Extract from feed categories
            if hasattr(entry, 'categories'):
                for cat in entry.categories:
                    if isinstance(cat, dict):
                        cat_term = cat.get('term', '')
                        if cat_term and cat_term not in categories and not cat_term.isdigit():
                            categories.append(cat_term)
                    elif isinstance(cat, (list, tuple)) and len(cat) > 0:
                        cat_val = cat[1] if len(cat) > 1 else cat[0]
                        if cat_val and cat_val not in categories and not str(cat_val).isdigit():
                            categories.append(cat_val)

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
