"""
Content scraper for fetching full article text from URLs.
"""

import logging
from typing import Optional
import requests
from newspaper import Article as NewspaperArticle
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class ContentScraper:
    """Scrapes full article content from URLs."""
    
    def __init__(self, timeout: int = 10):
        """
        Initialize content scraper.
        
        Args:
            timeout: Request timeout in seconds
        """
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
    
    def fetch_article_content(self, url: str) -> Optional[str]:
        """
        Fetch full article content from URL.
        
        Args:
            url: Article URL
            
        Returns:
            Article content or None if fetch fails
        """
        try:
            # Try newspaper3k first (best for news articles)
            article = NewspaperArticle(url)
            article.download()
            article.parse()
            
            if article.text and len(article.text.strip()) > 100:
                logger.debug(f"Successfully scraped content from {url} using newspaper3k")
                return article.text.strip()
            
            logger.debug(f"newspaper3k returned insufficient content, falling back to BeautifulSoup")
            
            # Fallback to BeautifulSoup
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
                element.decompose()
            
            # Try to find article content
            content_selectors = [
                'article',
                '[role="main"]',
                '.article-body',
                '.article-content',
                '.story-body',
                '.post-content',
                'main',
            ]
            
            for selector in content_selectors:
                content_elem = soup.select_one(selector)
                if content_elem:
                    text = content_elem.get_text(separator='\n', strip=True)
                    if len(text) > 100:
                        logger.debug(f"Successfully scraped content from {url} using BeautifulSoup")
                        return text
            
            # Last resort: get all paragraph text
            paragraphs = soup.find_all('p')
            if paragraphs:
                text = '\n\n'.join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
                if len(text) > 100:
                    logger.debug(f"Successfully scraped content from {url} using paragraph extraction")
                    return text
            
            logger.warning(f"Could not extract meaningful content from {url}")
            return None
            
        except Exception as e:
            logger.warning(f"Failed to scrape content from {url}: {e}")
            return None
    
    def close(self):
        """Close the session."""
        self.session.close()
