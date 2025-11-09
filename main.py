#!/usr/bin/env python3
"""
News Aggregator - Main Entry Point

A comprehensive news aggregation system that fetches political news from
multiple reputable sources and stores them in markdown files or a database.
"""

import sys
import argparse
import logging
from pathlib import Path
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.config.settings import get_settings
from src.config.credentials import CredentialStore
from src.storage.file_storage import FileSystemRepository
from src.storage.database_storage import DatabaseRepository
from src.services.aggregator import NewsAggregator
from src.utils.logging_config import setup_logging
from src.ui.credential_manager import show_credential_manager

logger = logging.getLogger(__name__)


def setup_credentials(credential_store: CredentialStore, force: bool = False) -> bool:
    """
    Setup credentials using GUI if needed.

    Args:
        credential_store: The credential store
        force: Force credential setup even if some exist

    Returns:
        True if setup successful, False otherwise
    """
    settings = get_settings()

    # Create aggregator to check which credentials are needed
    # Use temporary repository for initialization
    temp_repo = FileSystemRepository(settings.news_md_dir)
    aggregator = NewsAggregator(temp_repo, credential_store, settings)

    # Get list of sources that need credentials
    missing_sources = aggregator.get_missing_credentials()

    if not missing_sources and not force:
        logger.info("All required credentials are configured")
        return True

    if not missing_sources and force:
        # Show all sources that require credentials
        missing_sources = ['newsapi', 'guardian', 'nyt']

    logger.info(f"Credentials needed for: {', '.join(missing_sources)}")

    # Show credential manager GUI
    print("\nOpening credential manager...")
    print("Please enter your API credentials for the news sources.")
    print("Click the registration links to obtain API keys.\n")

    def save_callback(credentials):
        """Callback to save credentials."""
        credential_store.save_credentials(credentials)
        logger.info(f"Saved credentials for {len(credentials)} sources")

    collected_credentials = show_credential_manager(
        missing_sources,
        on_save=save_callback
    )

    if collected_credentials:
        logger.info(f"Successfully configured {len(collected_credentials)} sources")
        return True
    else:
        logger.warning("No credentials were configured")
        return False


def create_repository(settings):
    """Create the appropriate repository based on settings."""
    if settings.storage_type == 'database' and settings.database_url:
        logger.info(f"Using database storage: {settings.database_url}")
        return DatabaseRepository(
            database_url=settings.database_url,
            pool_size=settings.db_pool_size,
            max_overflow=settings.db_max_overflow
        )
    else:
        logger.info(f"Using file system storage: {settings.news_md_dir}")
        return FileSystemRepository(settings.news_md_dir)


def main():
    """Main application entry point."""
    parser = argparse.ArgumentParser(
        description="News Aggregator - Fetch political news from multiple sources",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Fetch news with credential setup
  python main.py

  # Fetch news from specific sources
  python main.py --sources newsapi guardian nyt

  # Fetch news from the last 7 days
  python main.py --days 7

  # Fetch news with custom query
  python main.py --query "presidential election"

  # Setup or update credentials
  python main.py --setup-credentials

  # Show statistics
  python main.py --stats

  # Use database storage
  python main.py --database postgresql://user:pass@localhost/newsdb
        """
    )

    parser.add_argument(
        '--setup-credentials',
        action='store_true',
        help='Setup or update API credentials using GUI'
    )

    parser.add_argument(
        '--sources',
        nargs='+',
        help='Specific sources to fetch from (e.g., newsapi guardian nyt)'
    )

    parser.add_argument(
        '--max-articles',
        type=int,
        help='Maximum articles per source (default from settings)'
    )

    parser.add_argument(
        '--query',
        type=str,
        help='Search query for articles'
    )

    parser.add_argument(
        '--days',
        type=int,
        help='Fetch articles from the last N days'
    )

    parser.add_argument(
        '--from-date',
        type=str,
        help='Fetch articles from this date (YYYY-MM-DD)'
    )

    parser.add_argument(
        '--to-date',
        type=str,
        help='Fetch articles until this date (YYYY-MM-DD)'
    )

    parser.add_argument(
        '--stats',
        action='store_true',
        help='Show statistics and exit'
    )

    parser.add_argument(
        '--database',
        type=str,
        help='Database URL (overrides settings)'
    )

    parser.add_argument(
        '--output-dir',
        type=str,
        help='Output directory for markdown files (overrides settings)'
    )

    parser.add_argument(
        '--log-level',
        type=str,
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='Logging level (default from settings)'
    )

    parser.add_argument(
        '--no-parallel',
        action='store_true',
        help='Disable parallel fetching'
    )

    args = parser.parse_args()

    # Load settings
    settings = get_settings()

    # Override settings with command-line arguments
    if args.database:
        settings.database_url = args.database
        settings.storage_type = 'database'

    if args.output_dir:
        settings.news_md_dir = Path(args.output_dir)

    if args.sources:
        settings.enabled_sources = args.sources

    log_level = args.log_level or settings.log_level

    # Setup logging
    setup_logging(log_level=log_level)

    logger.info("=" * 80)
    logger.info("NEWS AGGREGATOR STARTED")
    logger.info("=" * 80)

    # Initialize credential store
    credential_store = CredentialStore(
        storage_path=settings.credential_storage_path
    )

    # Setup credentials if requested
    if args.setup_credentials:
        setup_credentials(credential_store, force=True)
        return

    # Check for missing credentials and offer to set them up
    temp_repo = FileSystemRepository(settings.news_md_dir)
    temp_aggregator = NewsAggregator(temp_repo, credential_store, settings)
    missing = temp_aggregator.get_missing_credentials()

    if missing:
        logger.warning(f"Missing credentials for: {', '.join(missing)}")
        print(f"\nSome sources require API credentials: {', '.join(missing)}")
        response = input("Would you like to set them up now? (y/n): ").strip().lower()

        if response == 'y':
            if not setup_credentials(credential_store):
                logger.warning("Continuing without all credentials. Some sources will be unavailable.")
        else:
            logger.info("Continuing without all credentials. Some sources will be unavailable.")

    # Create repository
    repository = create_repository(settings)

    # Create aggregator
    aggregator = NewsAggregator(repository, credential_store, settings)

    # Show statistics if requested
    if args.stats:
        stats = aggregator.get_source_statistics()

        print("\n" + "=" * 80)
        print("NEWS AGGREGATOR STATISTICS")
        print("=" * 80)

        for source, info in stats.items():
            status = "Available" if info['available'] else "Unavailable"
            creds = "Required" if info['requires_credentials'] else "Not required"
            print(f"\n{source.upper()}")
            print(f"  Status: {status}")
            print(f"  Credentials: {creds}")
            print(f"  Articles stored: {info['article_count']}")

        total_articles = sum(info['article_count'] for info in stats.values())
        print(f"\nTotal articles: {total_articles}")
        print(f"Available sources: {len(stats)}")
        print("=" * 80)
        return

    # Parse dates
    from_date = None
    to_date = None

    if args.days:
        to_date = datetime.utcnow()
        from_date = to_date - timedelta(days=args.days)
        logger.info(f"Fetching articles from the last {args.days} days")

    if args.from_date:
        from_date = datetime.strptime(args.from_date, '%Y-%m-%d')

    if args.to_date:
        to_date = datetime.strptime(args.to_date, '%Y-%m-%d')

    # Fetch and save articles
    logger.info("Starting article fetch...")

    available_sources = aggregator.get_available_sources()
    logger.info(f"Available sources: {', '.join(available_sources)}")

    stats = aggregator.fetch_and_save(
        max_articles_per_source=args.max_articles,
        query=args.query,
        from_date=from_date,
        to_date=to_date,
        parallel=not args.no_parallel
    )

    # Print summary
    print("\n" + "=" * 80)
    print("FETCH SUMMARY")
    print("=" * 80)
    print(f"Articles fetched: {stats['fetched']}")
    print(f"Articles saved: {stats['saved']}")
    print(f"Duplicates skipped: {stats['duplicates']}")
    print(f"Sources queried: {stats['sources']}")
    print("=" * 80)

    if settings.storage_type == 'file':
        print(f"\nArticles saved to: {settings.news_md_dir.absolute()}")
    else:
        print(f"\nArticles saved to database: {settings.database_url}")

    logger.info("News aggregation completed successfully")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user")
        sys.exit(0)
    except Exception as e:
        logger.exception(f"Fatal error: {e}")
        sys.exit(1)
