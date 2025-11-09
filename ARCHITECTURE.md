# News Aggregator - Architecture Documentation

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Interface                          │
│  ┌──────────────────────┐      ┌──────────────────────────┐   │
│  │   CLI (main.py)      │      │  GUI (Credential Manager)│   │
│  │  - Arguments         │      │  - tkinter UI            │   │
│  │  - Statistics        │      │  - API key input         │   │
│  │  - Commands          │      │  - Registration links    │   │
│  └──────────────────────┘      └──────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Service Layer                              │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              NewsAggregator Service                       │  │
│  │  - Coordinate fetching from multiple sources              │  │
│  │  - Parallel execution (ThreadPoolExecutor)                │  │
│  │  - Statistics collection                                  │  │
│  │  - Credential validation                                  │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                ┌─────────────┴─────────────┐
                ▼                           ▼
┌───────────────────────────────┐  ┌───────────────────────────┐
│    Configuration Layer        │  │    Storage Layer          │
│  ┌─────────────────────────┐ │  │  ┌────────────────────┐  │
│  │  Settings (Pydantic)    │ │  │  │ ArticleRepository  │  │
│  │  - Environment vars     │ │  │  │   (Abstract)       │  │
│  │  - .env file            │ │  │  └────────────────────┘  │
│  │  - Validation           │ │  │           │               │
│  └─────────────────────────┘ │  │    ┌──────┴──────┐       │
│  ┌─────────────────────────┐ │  │    │             │       │
│  │  CredentialStore        │ │  │    ▼             ▼       │
│  │  - Fernet encryption    │ │  │  ┌────┐      ┌────────┐ │
│  │  - Secure storage       │ │  │  │File│      │Database│ │
│  │  - Load/Save            │ │  │  │ MD │      │SQLAlch.│ │
│  └─────────────────────────┘ │  │  └────┘      └────────┘ │
└───────────────────────────────┘  └───────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Source Layer                               │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              NewsSource (Abstract Base Class)             │  │
│  │  - Rate limiting                                          │  │
│  │  - Retry logic                                            │  │
│  │  - Session management                                     │  │
│  │  - Error handling                                         │  │
│  └──────────────────────────────────────────────────────────┘  │
│           │                       │                    │        │
│     ┌─────┴─────┐          ┌─────┴─────┐       ┌─────┴─────┐ │
│     ▼           ▼          ▼           ▼       ▼           ▼ │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────────┐ │
│  │NewsAPI │ │Guardian│ │  NYT   │ │  RSS   │ │   Future   │ │
│  │Source  │ │Source  │ │Source  │ │Source  │ │  Sources   │ │
│  └────────┘ └────────┘ └────────┘ └────────┘ └────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Model Layer                                │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Article (Pydantic Model)                     │  │
│  │  - Data validation                                        │  │
│  │  - Type checking                                          │  │
│  │  - Serialization                                          │  │
│  │  - Markdown export                                        │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Credential Setup Flow

```
User starts app
     │
     ▼
Check for credentials
     │
     ├─ All present ──────────────────┐
     │                                 │
     ├─ Missing ──────────────────────┤
     │                                 │
     ▼                                 ▼
Show credential GUI              Continue to fetching
     │
     ├─ User enters credentials
     │   │
     │   ▼
     │  Validate credentials
     │   │
     │   ├─ Valid ─────────────────┐
     │   │                          │
     │   ├─ Invalid ────> Retry     │
     │   │                          │
     │   ▼                          │
     │  Encrypt & Save              │
     │   │                          │
     └───┴──────────────────────────┘
         │
         ▼
    Continue to fetching
```

### 2. News Fetching Flow

```
Start fetching
     │
     ▼
Load configuration
     │
     ▼
Load credentials
     │
     ▼
Initialize sources
     │
     ├─── For each enabled source:
     │    │
     │    ├─ Validate credentials (if needed)
     │    │
     │    ├─ Create source instance
     │    │
     │    └─ Add to available sources
     │
     ▼
Fetch from all sources (parallel)
     │
     ├─── ThreadPoolExecutor:
     │    │
     │    ├─ Source 1 ──> fetch_articles() ──┐
     │    │                                    │
     │    ├─ Source 2 ──> fetch_articles() ──┤
     │    │                                    │
     │    ├─ Source 3 ──> fetch_articles() ──┤
     │    │                                    │
     │    └─ Source N ──> fetch_articles() ──┤
     │                                         │
     ├─────────────────────────────────────────┘
     │
     ▼
Collect all articles
     │
     ▼
Save to repository
     │
     ├─ Check for duplicates (URL hash)
     │
     ├─ Save new articles
     │
     └─ Update index/database
     │
     ▼
Return statistics
```

### 3. Article Fetching Flow (per source)

```
NewsSource.fetch_articles()
     │
     ▼
Check rate limit
     │
     ├─ Limit exceeded ──> Wait/Retry
     │
     ▼
Build API request
     │
     ▼
Make HTTP request
     │
     ├─ Network error ──> Retry with backoff
     │
     ├─ Auth error ────> Raise exception
     │
     ├─ Rate limit ────> Wait and retry
     │
     ▼
Parse response
     │
     ├─ For each article in response:
     │   │
     │   ├─ Extract fields
     │   │
     │   ├─ Validate data (Pydantic)
     │   │
     │   ├─ Create Article object
     │   │
     │   └─ Add to results
     │
     ▼
Return articles list
```

## Component Details

### 1. Configuration System

**Settings (Pydantic BaseSettings)**
- Environment variable loading
- .env file support
- Type validation
- Default values
- Conversion utilities

**CredentialStore**
- Fernet symmetric encryption
- Secure key management
- File permissions (600)
- JSON storage format
- CRUD operations

### 2. Source Layer

**Base Class (NewsSource)**
```python
Abstract Methods:
- requires_credentials() -> bool
- validate_credentials() -> bool
- fetch_articles(...) -> List[Article]
- get_categories() -> List[str]

Concrete Methods:
- _make_request(url, params) -> Response
- _check_rate_limit() -> None
```

**Implementations**
- NewsAPISource: REST API with JSON responses
- GuardianSource: REST API with pagination
- NYTSource: Multiple API endpoints
- RSSSource: Generic RSS/Atom feed parser

### 3. Storage Layer

**Repository Pattern**
```python
Interface:
- save_article(article) -> bool
- save_articles(articles) -> int
- get_article(url) -> Article
- get_articles_by_source(source) -> List[Article]
- get_articles_by_date_range(...) -> List[Article]
- article_exists(url) -> bool
- count_articles(source) -> int
- delete_article(url) -> bool
```

**File System Implementation**
- Markdown files organized by source
- JSON index for metadata
- URL hash for deduplication
- Atomic operations

**Database Implementation**
- SQLAlchemy ORM
- Connection pooling
- Transaction management
- Indexed queries
- Multi-database support

### 4. Service Layer

**NewsAggregator**
- Source initialization
- Credential management
- Parallel fetching
- Statistics collection
- Error aggregation

## Design Patterns

### 1. Repository Pattern
**Purpose:** Abstract storage details from business logic

```python
class ArticleRepository(ABC):
    # Abstract interface
    pass

class FileSystemRepository(ArticleRepository):
    # Concrete implementation for files
    pass

class DatabaseRepository(ArticleRepository):
    # Concrete implementation for database
    pass
```

**Benefits:**
- Easy to swap storage backends
- Testable (mock repository)
- Single responsibility

### 2. Factory Pattern
**Purpose:** Create source instances

```python
SOURCE_CLASSES = {
    ArticleSource.NEWSAPI: NewsAPISource,
    ArticleSource.GUARDIAN: GuardianSource,
    # ...
}

# Create source based on ID
source = SOURCE_CLASSES[source_id](credentials)
```

**Benefits:**
- Centralized source creation
- Easy to add new sources
- Type safety

### 3. Strategy Pattern
**Purpose:** Different storage strategies

```python
if settings.storage_type == 'database':
    repository = DatabaseRepository(settings.database_url)
else:
    repository = FileSystemRepository(settings.news_md_dir)
```

**Benefits:**
- Runtime strategy selection
- Configuration-driven
- Extensible

### 4. Template Method Pattern
**Purpose:** Common source behavior

```python
class NewsSource(ABC):
    def _make_request(self, url):
        # Common request logic
        self._check_rate_limit()
        # Retry logic
        # Error handling
        pass

    @abstractmethod
    def fetch_articles(self):
        # Subclass implements
        pass
```

**Benefits:**
- Code reuse
- Consistent behavior
- Customization points

## Architectural Principles

### 1. Separation of Concerns
- **Models:** Data structures only
- **Sources:** Data fetching only
- **Storage:** Persistence only
- **Services:** Business logic only
- **Config:** Configuration only
- **UI:** User interaction only

### 2. Dependency Injection
```python
class NewsAggregator:
    def __init__(self, repository, credential_store, settings):
        # Dependencies injected
        self.repository = repository
        self.credential_store = credential_store
        self.settings = settings
```

**Benefits:**
- Loose coupling
- Testability
- Flexibility

### 3. Interface Segregation
- Small, focused interfaces
- Sources implement only what they need
- Repository has clear contract

### 4. Single Responsibility
- Each class has one reason to change
- Clear responsibilities
- High cohesion

### 5. Open/Closed Principle
- Open for extension (new sources)
- Closed for modification (base classes)

## Error Handling Strategy

### Exception Hierarchy
```
NewsSourceException (base)
├── AuthenticationException
├── RateLimitException
└── [Future exceptions]
```

### Error Handling Levels

1. **Source Level**
   - Catch API errors
   - Retry on transient failures
   - Convert to NewsSourceException

2. **Service Level**
   - Catch source exceptions
   - Continue with other sources
   - Collect errors for reporting

3. **Application Level**
   - Display user-friendly messages
   - Log detailed errors
   - Provide recovery options

### Retry Strategy
```python
Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504]
)
```

## Security Architecture

### 1. Credential Security
```
User Input (API Key)
     │
     ▼
Fernet Encryption
     │
     ▼
Encrypted File (600 permissions)
     │
     ▼
~/.news_aggregator/credentials.enc
```

### 2. Validation
- Pydantic models validate all input
- URL validation prevents injection
- Safe filename generation
- Type checking throughout

### 3. Secure Defaults
- HTTPS URLs only
- Secure file permissions
- No logging of credentials
- Safe error messages

## Performance Optimizations

### 1. Parallel Fetching
```python
with ThreadPoolExecutor(max_workers=len(sources)) as executor:
    futures = [executor.submit(fetch, source) for source in sources]
    results = [future.result() for future in as_completed(futures)]
```

### 2. Connection Pooling
- HTTP session reuse
- Database connection pool
- Persistent connections

### 3. Efficient Deduplication
- MD5 hash of URLs
- O(1) lookup in index
- Minimal memory usage

### 4. Rate Limiting
- Per-source limits
- Sliding window
- Prevents API bans

## Scalability Considerations

### Horizontal Scaling
- Stateless design
- Shared database
- Distributed credentials

### Vertical Scaling
- Connection pooling
- Configurable workers
- Memory-efficient storage

### Data Volume
- Database indexing
- Pagination support
- Archival strategy

## Extension Points

### Adding Features
1. **New Source:** Inherit from NewsSource
2. **New Storage:** Implement ArticleRepository
3. **New UI:** Use NewsAggregator service
4. **New Format:** Add to Article.to_X() methods

### Customization
- Settings via environment
- Plugin architecture ready
- Clear interfaces
- Minimal coupling

## Conclusion

The architecture provides:
- **Maintainability:** Clear structure, documented
- **Extensibility:** Easy to add sources/features
- **Reliability:** Error handling, retries
- **Security:** Encrypted credentials, validation
- **Performance:** Parallel fetching, pooling
- **Testability:** Dependency injection, abstractions
- **Usability:** CLI, GUI, documentation
