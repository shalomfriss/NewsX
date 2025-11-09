# News Aggregator

A comprehensive news aggregation system that fetches political news from multiple reputable sources and stores them as markdown files or in a database. Features a user-friendly GUI for managing API credentials.

## Features

- **Multi-Source Support**: Fetches news from 17+ reputable sources including:
  - API-based: NewsAPI, The Guardian, New York Times
  - RSS-based: BBC, Reuters, AP, Politico, The Hill, NPR, CNN, ABC, CBS, NBC, PBS, Washington Post, The Atlantic, ProPublica

- **Credential Management**:
  - User-friendly GUI popup for entering API credentials
  - Clickable links to API registration pages
  - Secure encrypted storage of credentials

- **Flexible Storage**:
  - File system storage (markdown files organized by source)
  - Database storage (PostgreSQL, MySQL, SQLite)
  - Easy switching between storage modes

- **Robust Architecture**:
  - Clean architecture with separation of concerns
  - Abstract base classes for easy extensibility
  - Comprehensive error handling
  - Rate limiting and retry logic
  - Parallel fetching for performance

- **Political News Focus**:
  - Automatically filters for political content
  - Customizable search queries
  - Date range filtering

## Architecture

```
backend/
├── src/
│   ├── config/          # Configuration and credential management
│   │   ├── settings.py
│   │   └── credentials.py
│   ├── models/          # Data models (Article, etc.)
│   │   └── article.py
│   ├── sources/         # News source implementations
│   │   ├── base.py
│   │   ├── newsapi_source.py
│   │   ├── guardian_source.py
│   │   ├── nyt_source.py
│   │   └── rss_source.py
│   ├── storage/         # Storage layer (file/database)
│   │   ├── base.py
│   │   ├── file_storage.py
│   │   └── database_storage.py
│   ├── services/        # Business logic
│   │   └── aggregator.py
│   ├── ui/              # GUI components
│   │   └── credential_manager.py
│   └── utils/           # Utilities
│       └── logging_config.py
├── news_md/             # Markdown file storage (auto-created)
├── main.py              # Application entry point
├── requirements.txt     # Python dependencies
├── .env.example         # Example configuration
└── README.md           # This file
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Optional: PostgreSQL or MySQL for database storage

### Setup Steps

1. **Clone or navigate to the backend directory**:
   ```bash
   cd /Users/206845153/Documents/repos/news/backend
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the application**:
   ```bash
   cp .env.example .env
   # Edit .env with your preferred settings
   ```

## Getting API Keys

**📖 For detailed credential setup instructions, see [CREDENTIALS_SETUP.md](Documentation/CREDENTIALS_SETUP.md)**

### Two Ways to Provide Credentials

#### Option 1: Environment Variables (Recommended)

Set credentials in your `.env` file:

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your API keys:
NEWSAPI_API_KEY=your_key_here
GUARDIAN_API_KEY=your_key_here
NYT_API_KEY=your_key_here
```

**Advantages:** Industry standard, works in production/Docker, no GUI required

#### Option 2: GUI Credential Manager

Run the credential setup wizard:

```bash
python main.py --setup-credentials
```

**Advantages:** User-friendly, clickable registration links, encrypted storage

### Required API Keys (for API-based sources)

1. **NewsAPI** (Free tier: 100 requests/day)
   - Register at: https://newsapi.org/register
   - Get your API key from the dashboard
   - Access to 80,000+ news sources worldwide

2. **The Guardian** (Free tier: 5,000 requests/day, 12 requests/second)
   - Register at: https://open-platform.theguardian.com/access
   - API key will be emailed to you
   - Access to Guardian content dating back to 1999

3. **New York Times** (Free tier: 500 requests/day)
   - Register at: https://developer.nytimes.com/get-started
   - Create an app and enable the APIs you want
   - Access to Article Search and Top Stories APIs

### No API Key Required (RSS-based sources)

The following 14 sources work without API keys:
- BBC News, Reuters, Associated Press
- Politico, The Hill, NPR
- CNN, ABC, CBS, NBC, PBS NewsHour
- Washington Post, The Atlantic, ProPublica

## Usage

### Basic Usage

**First-time setup** (will prompt for credentials):
```bash
python main.py
```

### Middle East Analysis Agent

The repository now ships with a specialized agent that inspects every markdown
article in `news_md/` and creates structured analysis reports in
`news_analysis_md/`.

1. **Set your OpenAI key** (required for LLM-backed analysis):
   ```bash
   export OPENAI_API_KEY="sk-your-key"
   ```
2. **Run the agent module**:
   ```bash
   python -m src.agents.middle_east_analysis_agent --log-level INFO
   ```
   Key flags:
   - `--limit 10` – analyze only the first 10 files (useful for testing)
   - `--dry-run` – generate placeholder files without calling the API
   - `--model gpt-4o-mini` – override the default model name

The agent always removes the existing `news_analysis_md/` contents before
writing fresh results and mirrors the directory structure from `news_md/`.

The application will:
1. Check for missing API credentials
2. Open an improved GUI popup if credentials are needed
3. Provide clickable links to API registration pages
4. Show/hide buttons to verify your API keys
5. Give real-time feedback during setup
6. Securely encrypt and save your credentials
7. Fetch and save news articles

**📖 New to the credential manager?** See the [Credential Manager Guide](Documentation/CREDENTIAL_MANAGER_GUIDE.md) for a visual walkthrough.

### Command-Line Options

**Fetch news from all available sources**:
```bash
python main.py
```

**Setup or update credentials**:
```bash
python main.py --setup-credentials
```

**Fetch from specific sources**:
```bash
python main.py --sources newsapi guardian nyt
```

**Fetch news from the last 7 days**:
```bash
python main.py --days 7
```

**Custom search query**:
```bash
python main.py --query "presidential election"
```

**Date range query**:
```bash
python main.py --from-date 2025-11-01 --to-date 2025-11-07
```

**View statistics**:
```bash
python main.py --stats
```

**Use database storage**:
```bash
python main.py --database postgresql://user:password@localhost/newsdb
```

**Specify output directory**:
```bash
python main.py --output-dir /path/to/articles
```

**Debug mode**:
```bash
python main.py --log-level DEBUG
```

### Full Command-Line Reference

```
usage: main.py [-h] [--setup-credentials] [--sources SOURCES [SOURCES ...]]
               [--max-articles MAX_ARTICLES] [--query QUERY] [--days DAYS]
               [--from-date FROM_DATE] [--to-date TO_DATE] [--stats]
               [--database DATABASE] [--output-dir OUTPUT_DIR]
               [--log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
               [--no-parallel]

Options:
  --setup-credentials   Setup or update API credentials using GUI
  --sources            Specific sources to fetch from
  --max-articles       Maximum articles per source
  --query              Search query for articles
  --days               Fetch articles from the last N days
  --from-date          Fetch articles from this date (YYYY-MM-DD)
  --to-date            Fetch articles until this date (YYYY-MM-DD)
  --stats              Show statistics and exit
  --database           Database URL
  --output-dir         Output directory for markdown files
  --log-level          Logging level
  --no-parallel        Disable parallel fetching
```

## Configuration

### Environment Variables (.env file)

```bash
# Storage type: 'file' or 'database'
STORAGE_TYPE=file

# File storage directory
NEWS_MD_DIR=news_md

# Database URL (if using database storage)
DATABASE_URL=postgresql://user:password@localhost:5432/newsdb

# Fetching settings
MAX_ARTICLES_PER_SOURCE=50
FETCH_POLITICAL_ONLY=True

# Enabled sources (comma-separated)
ENABLED_SOURCES=newsapi,guardian,nyt,bbc,reuters,politico,the_hill,npr

# Logging
LOG_LEVEL=INFO
DEBUG=False
```

### Credential Storage

Credentials are stored securely in `~/.news_aggregator/credentials.enc`:
- Encrypted using Fernet (symmetric encryption)
- Encryption key stored separately with restricted permissions
- Can be managed via GUI or programmatically

### Database Setup

**PostgreSQL**:
```bash
# Install PostgreSQL and create database
createdb newsdb

# Set in .env or command line
DATABASE_URL=postgresql://user:password@localhost:5432/newsdb
STORAGE_TYPE=database
```

**MySQL**:
```bash
# Set in .env
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/newsdb
STORAGE_TYPE=database
```

**SQLite** (for testing):
```bash
DATABASE_URL=sqlite:///news.db
STORAGE_TYPE=database
```

## Output Format

### Markdown Files

Articles are stored as markdown files organized by source:

```
news_md/
├── newsapi/
│   ├── 20251107_120000_newsapi_senate-votes-on-new-bill.md
│   └── 20251107_120500_newsapi_presidential-address.md
├── guardian/
│   ├── 20251107_113000_guardian_uk-politics-update.md
│   └── ...
├── bbc/
├── reuters/
└── ...
```

**Markdown Format**:
```markdown
# Article Title

**Source:** newsapi
**Published:** 2025-11-07 12:00:00 UTC
**URL:** https://example.com/article
**Author:** John Smith
**Categories:** politics, government
**Keywords:** senate, legislation, congress

![Article Image](https://example.com/image.jpg)

## Summary

Article description or summary...

## Content

Full article content...
```

### Database Schema

```sql
CREATE TABLE articles (
    id INTEGER PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    content TEXT,
    url VARCHAR(2048) NOT NULL UNIQUE,
    source VARCHAR(50) NOT NULL,
    author VARCHAR(200),
    published_at TIMESTAMP NOT NULL,
    fetched_at TIMESTAMP NOT NULL,
    image_url VARCHAR(2048),
    categories TEXT,  -- JSON
    keywords TEXT     -- JSON
);

CREATE INDEX idx_source ON articles(source);
CREATE INDEX idx_published_at ON articles(published_at);
CREATE INDEX idx_source_published ON articles(source, published_at);
```

## Extending the System

### Adding a New News Source

1. **For API-based sources**, create a new source class:

```python
# src/sources/example_source.py
from .base import NewsSource
from ..models.article import Article, ArticleSource

class ExampleSource(NewsSource):
    def __init__(self, credentials=None, **kwargs):
        super().__init__(
            source_id=ArticleSource.EXAMPLE,
            credentials=credentials,
            **kwargs
        )

    def requires_credentials(self) -> bool:
        return True

    def validate_credentials(self) -> bool:
        # Validate API key
        pass

    def fetch_articles(self, **kwargs) -> List[Article]:
        # Fetch and parse articles
        pass

    def get_categories(self) -> List[str]:
        return ['politics', 'world', 'business']
```

2. **Register the source** in `src/services/aggregator.py`:

```python
SOURCE_CLASSES = {
    # ... existing sources ...
    ArticleSource.EXAMPLE: ExampleSource,
}
```

3. **Add to credential manager** (if requires credentials) in `src/ui/credential_manager.py`:

```python
API_REGISTRATION_URLS = {
    # ... existing URLs ...
    "example": {
        "name": "Example News",
        "url": "https://example.com/api/register",
        "fields": ["api_key"],
        "description": "Example news source API"
    }
}
```

### For RSS-based sources:

Simply add the RSS feed URL to `RSS_FEEDS` in `src/sources/rss_source.py`:

```python
RSS_FEEDS = {
    # ... existing feeds ...
    ArticleSource.EXAMPLE: [
        "https://example.com/rss/politics.xml"
    ]
}
```

## Troubleshooting

### Common Issues

**Issue**: "No module named 'tkinter'"
- **Solution**: Install tkinter:
  - Ubuntu/Debian: `sudo apt-get install python3-tk`
  - macOS: Included with Python
  - Windows: Reinstall Python with tcl/tk option

**Issue**: "Failed to load encryption key"
- **Solution**: Delete `~/.news_aggregator/.key` and restart (will create new key)

**Issue**: "Rate limit exceeded"
- **Solution**: Wait or adjust rate limits in source implementations

**Issue**: "Database connection failed"
- **Solution**:
  - Check DATABASE_URL format
  - Ensure database server is running
  - Install appropriate database driver (psycopg2, PyMySQL)

**Issue**: "No articles fetched"
- **Solution**:
  - Check API credentials are valid
  - Verify internet connection
  - Check logs for specific errors
  - Try with `--log-level DEBUG`

### Logging

Logs are printed to console by default. For file logging:

```python
# Add to .env
LOG_FILE=news_aggregator.log
```

## Performance Considerations

- **Parallel Fetching**: Enabled by default, disable with `--no-parallel` if needed
- **Rate Limiting**: Automatically handles rate limits with exponential backoff
- **Connection Pooling**: Database connections are pooled for efficiency
- **Caching**: Articles are deduplicated by URL to prevent duplicates

## Security

- **Credential Encryption**: All API keys encrypted at rest using Fernet
- **File Permissions**: Credential files have restricted permissions (600)
- **No Plaintext Storage**: Credentials never stored in plaintext
- **Environment Variables**: Sensitive data can be loaded from .env (not committed)

## License

This project is provided as-is for educational and personal use.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review logs with `--log-level DEBUG`
3. Verify API credentials are valid
4. Check that news sources are accessible

## Acknowledgments

News sources:
- NewsAPI.org
- The Guardian Open Platform
- New York Times Developer Network
- BBC, Reuters, AP, and other RSS feed providers
