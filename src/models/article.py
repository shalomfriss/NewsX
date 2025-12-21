"""Article and related data models."""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, HttpUrl, Field, validator
from enum import Enum


class ArticleSource(str, Enum):
    """Enumeration of supported news sources."""
    NEWSAPI = "newsapi"
    GUARDIAN = "guardian"
    NYT = "nyt"
    BBC = "bbc"
    REUTERS = "reuters"
    AP = "ap"
    POLITICO = "politico"
    THE_HILL = "the_hill"
    BLOOMBERG = "bloomberg"
    WSJ = "wsj"
    NPR = "npr"
    CNN = "cnn"
    ABC = "abc"
    CBS = "cbs"
    NBC = "nbc"
    PBS = "pbs"
    WASHINGTON_POST = "washington_post"
    THE_ATLANTIC = "the_atlantic"
    PROPUBLICA = "propublica"
    AL_JAZEERA = "al_jazeera"


class Article(BaseModel):
    """Represents a news article."""

    title: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = Field(None, max_length=2000)
    content: Optional[str] = None
    url: HttpUrl
    source: ArticleSource
    author: Optional[str] = None
    published_at: datetime
    fetched_at: datetime = Field(default_factory=datetime.utcnow)
    image_url: Optional[HttpUrl] = None
    categories: List[str] = Field(default_factory=list)
    keywords: List[str] = Field(default_factory=list)

    @validator('published_at', pre=True)
    def parse_published_at(cls, v):
        """Parse various datetime formats."""
        if isinstance(v, datetime):
            return v
        if isinstance(v, str):
            # Try ISO 8601 format with timezone first (e.g., 2025-12-19T18:25:12-05:00)
            try:
                from dateutil import parser
                return parser.isoparse(v).replace(tzinfo=None)
            except:
                pass
            
            # Try multiple standard formats
            for fmt in [
                "%Y-%m-%dT%H:%M:%SZ",
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%dT%H:%M:%S.%fZ",
                "%Y-%m-%d"
            ]:
                try:
                    return datetime.strptime(v, fmt)
                except ValueError:
                    continue
        raise ValueError(f"Unable to parse datetime: {v}")

    def get_publication_name(self) -> str:
        """Get human-readable publication name from source."""
        source_names = {
            'newsapi': 'NewsAPI',
            'guardian': 'The Guardian',
            'nyt': 'The New York Times',
            'bbc': 'BBC News',
            'reuters': 'Reuters',
            'ap': 'Associated Press',
            'politico': 'Politico',
            'the_hill': 'The Hill',
            'bloomberg': 'Bloomberg',
            'wsj': 'The Wall Street Journal',
            'npr': 'NPR',
            'cnn': 'CNN',
            'abc': 'ABC News',
            'cbs': 'CBS News',
            'nbc': 'NBC News',
            'pbs': 'PBS NewsHour',
            'washington_post': 'The Washington Post',
            'the_atlantic': 'The Atlantic',
            'propublica': 'ProPublica',
            'al_jazeera': 'Al Jazeera'
        }
        source_value = self.source.value if hasattr(self.source, 'value') else str(self.source)
        return source_names.get(source_value, source_value.upper())

    def to_markdown(self) -> str:
        """Convert article to markdown format."""
        # Get source value (handle both string and enum)
        source_value = self.source.value if hasattr(self.source, 'value') else str(self.source)
        publication_name = self.get_publication_name()

        md_lines = [
            f"# {self.title}",
            "",
            f"**Publication:** {publication_name}",
            f"**Source:** {source_value}",
            f"**Published:** {self.published_at.strftime('%Y-%m-%d %H:%M:%S UTC')}",
            f"**URL:** {self.url}",
        ]

        if self.author:
            md_lines.append(f"**Author:** {self.author}")

        if self.categories:
            md_lines.append(f"**Categories:** {', '.join(self.categories)}")

        if self.keywords:
            md_lines.append(f"**Keywords:** {', '.join(self.keywords)}")

        md_lines.append("")

        if self.image_url:
            md_lines.append(f"![Article Thumbnail]({self.image_url})")
            md_lines.append("")

        if self.description:
            md_lines.append("## Summary")
            md_lines.append("")
            md_lines.append(self.description)
            md_lines.append("")

        if self.content:
            md_lines.append("## Content")
            md_lines.append("")
            md_lines.append(self.content)

        return "\n".join(md_lines)

    def get_filename(self) -> str:
        """Generate a safe filename for the article."""
        import re
        # Get source value (handle both string and enum)
        source_value = self.source.value if hasattr(self.source, 'value') else str(self.source)

        # Sanitize title for filename
        safe_title = re.sub(r'[^\w\s-]', '', self.title)
        safe_title = re.sub(r'[-\s]+', '-', safe_title)
        safe_title = safe_title[:100]  # Limit length

        timestamp = self.published_at.strftime('%Y%m%d_%H%M%S')
        return f"{timestamp}_{source_value}_{safe_title}.md"

    class Config:
        """Pydantic configuration."""
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }
