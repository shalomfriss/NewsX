"""
Database-based article storage implementation.
"""

import logging
from typing import List, Optional
from datetime import datetime
from contextlib import contextmanager

from sqlalchemy import create_engine, Column, String, DateTime, Text, Integer, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool

from .base import ArticleRepository
from ..models.article import Article, ArticleSource

logger = logging.getLogger(__name__)

Base = declarative_base()


class ArticleModel(Base):
    """SQLAlchemy model for articles."""

    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    content = Column(Text, nullable=True)
    url = Column(String(2048), nullable=False, unique=True, index=True)
    source = Column(String(50), nullable=False, index=True)
    author = Column(String(200), nullable=True)
    published_at = Column(DateTime, nullable=False, index=True)
    fetched_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    image_url = Column(String(2048), nullable=True)
    categories = Column(Text, nullable=True)  # JSON string
    keywords = Column(Text, nullable=True)  # JSON string

    # Composite index for common queries
    __table_args__ = (
        Index('idx_source_published', 'source', 'published_at'),
    )


class DatabaseRepository(ArticleRepository):
    """Database-based article repository using SQLAlchemy."""

    def __init__(
        self,
        database_url: str,
        pool_size: int = 5,
        max_overflow: int = 10,
        echo: bool = False
    ):
        """
        Initialize database repository.

        Args:
            database_url: Database connection URL
            pool_size: Connection pool size
            max_overflow: Maximum overflow connections
            echo: Echo SQL statements (for debugging)
        """
        self.engine = create_engine(
            database_url,
            poolclass=QueuePool,
            pool_size=pool_size,
            max_overflow=max_overflow,
            echo=echo
        )

        # Create tables
        Base.metadata.create_all(self.engine)

        # Session factory
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )

        logger.info(f"Database repository initialized: {database_url}")

    @contextmanager
    def get_session(self) -> Session:
        """Get a database session with automatic cleanup."""
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def _article_to_model(self, article: Article) -> ArticleModel:
        """Convert Article to ArticleModel."""
        import json

        return ArticleModel(
            title=article.title,
            description=article.description,
            content=article.content,
            url=str(article.url),
            source=article.source.value,
            author=article.author,
            published_at=article.published_at,
            fetched_at=article.fetched_at,
            image_url=str(article.image_url) if article.image_url else None,
            categories=json.dumps(article.categories) if article.categories else None,
            keywords=json.dumps(article.keywords) if article.keywords else None
        )

    def _model_to_article(self, model: ArticleModel) -> Article:
        """Convert ArticleModel to Article."""
        import json

        return Article(
            title=model.title,
            description=model.description,
            content=model.content,
            url=model.url,
            source=ArticleSource(model.source),
            author=model.author,
            published_at=model.published_at,
            fetched_at=model.fetched_at,
            image_url=model.image_url,
            categories=json.loads(model.categories) if model.categories else [],
            keywords=json.loads(model.keywords) if model.keywords else []
        )

    def save_article(self, article: Article) -> bool:
        """Save a single article."""
        try:
            with self.get_session() as session:
                # Check if article exists
                existing = session.query(ArticleModel).filter_by(
                    url=str(article.url)
                ).first()

                if existing:
                    logger.info(f"Article already exists: {article.title}")
                    return False

                # Create and save new article
                article_model = self._article_to_model(article)
                session.add(article_model)

                logger.info(f"Saved article to database: {article.title}")
                return True

        except Exception as e:
            logger.error(f"Failed to save article {article.title}: {e}")
            return False

    def save_articles(self, articles: List[Article]) -> int:
        """Save multiple articles."""
        count = 0

        try:
            with self.get_session() as session:
                for article in articles:
                    try:
                        # Check if article exists
                        existing = session.query(ArticleModel).filter_by(
                            url=str(article.url)
                        ).first()

                        if existing:
                            logger.debug(f"Article already exists: {article.title}")
                            continue

                        # Create and save new article
                        article_model = self._article_to_model(article)
                        session.add(article_model)
                        count += 1

                    except Exception as e:
                        logger.warning(f"Failed to save article {article.title}: {e}")
                        continue

                logger.info(f"Saved {count} articles to database")

        except Exception as e:
            logger.error(f"Failed to save articles: {e}")

        return count

    def get_article(self, url: str) -> Optional[Article]:
        """Retrieve an article by URL."""
        try:
            with self.get_session() as session:
                model = session.query(ArticleModel).filter_by(url=url).first()
                if model:
                    return self._model_to_article(model)
                return None

        except Exception as e:
            logger.error(f"Failed to retrieve article: {e}")
            return None

    def get_articles_by_source(
        self,
        source: ArticleSource,
        limit: Optional[int] = None
    ) -> List[Article]:
        """Retrieve articles from a specific source."""
        try:
            with self.get_session() as session:
                query = session.query(ArticleModel).filter_by(
                    source=source.value
                ).order_by(ArticleModel.published_at.desc())

                if limit:
                    query = query.limit(limit)

                models = query.all()
                return [self._model_to_article(m) for m in models]

        except Exception as e:
            logger.error(f"Failed to retrieve articles by source: {e}")
            return []

    def get_articles_by_date_range(
        self,
        from_date: datetime,
        to_date: datetime,
        source: Optional[ArticleSource] = None
    ) -> List[Article]:
        """Retrieve articles within a date range."""
        try:
            with self.get_session() as session:
                query = session.query(ArticleModel).filter(
                    ArticleModel.published_at >= from_date,
                    ArticleModel.published_at <= to_date
                )

                if source:
                    query = query.filter_by(source=source.value)

                query = query.order_by(ArticleModel.published_at.desc())
                models = query.all()
                return [self._model_to_article(m) for m in models]

        except Exception as e:
            logger.error(f"Failed to retrieve articles by date range: {e}")
            return []

    def article_exists(self, url: str) -> bool:
        """Check if an article already exists."""
        try:
            with self.get_session() as session:
                return session.query(ArticleModel).filter_by(url=url).first() is not None

        except Exception as e:
            logger.error(f"Failed to check article existence: {e}")
            return False

    def count_articles(self, source: Optional[ArticleSource] = None) -> int:
        """Count total articles."""
        try:
            with self.get_session() as session:
                query = session.query(ArticleModel)

                if source:
                    query = query.filter_by(source=source.value)

                return query.count()

        except Exception as e:
            logger.error(f"Failed to count articles: {e}")
            return 0

    def delete_article(self, url: str) -> bool:
        """Delete an article."""
        try:
            with self.get_session() as session:
                article = session.query(ArticleModel).filter_by(url=url).first()

                if not article:
                    return False

                session.delete(article)
                logger.info(f"Deleted article: {article.title}")
                return True

        except Exception as e:
            logger.error(f"Failed to delete article: {e}")
            return False
