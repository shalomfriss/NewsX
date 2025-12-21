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
    
    def __init__(self, timeout: int = 5):
        """
        Initialize content scraper.
        
        Args:
            timeout: Request timeout in seconds (reduced to 5 for faster failure)
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
            # Skip if URL is None or empty
            if not url:
                return None
            
            # Try BeautifulSoup first (faster and more reliable than newspaper3k)
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
                    if len(text) > 200:
                        return text
            
            # Fallback: get all paragraph text
            paragraphs = soup.find_all('p')
            if paragraphs:
                text = '\n\n'.join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
                if len(text) > 200:
                    return text
            
            return None
            
        except requests.Timeout:
            logger.debug(f"Timeout scraping {url[:50]}")
            return None
        except requests.RequestException as e:
            logger.debug(f"Request error scraping {url[:50]}: {str(e)[:30]}")
            return None
        except Exception as e:
            logger.debug(f"Failed to scrape {url[:50]}: {str(e)[:50]}")
            return None
    
    def close(self):
        """Close the session."""
        self.session.close()
