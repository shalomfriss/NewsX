# AGENTS.md

## Build/Lint/Test Commands

- **Run the application**: `python main.py`
- **Run with specific sources**: `python main.py --sources newsapi --max-articles 1`
- **Setup credentials**: `python main.py --setup-credentials`
- **View stats**: `python main.py --stats`

No dedicated lint or test commands; testing is manual via running the app with different flags.

## Code Style Guidelines

- **Imports**: Use absolute imports from parent modules (e.g., `from ..models.article import Article`). Group standard library, third-party, then local imports.
- **Formatting**: Follow PEP 8. Use 4 spaces for indentation. Lines up to 88 characters.
- **Types**: Use type hints for all function parameters and return values. Use `Optional` for nullable types.
- **Naming**: Classes in CamelCase, functions/methods/variables in snake_case. Constants in UPPER_CASE.
- **Error Handling**: Use custom exceptions inheriting from base exceptions. Log errors with appropriate levels. Use try-except blocks around external calls.
- **Docstrings**: Use triple quotes for all classes and functions. Include Args, Returns, Raises sections where applicable.
- **Logging**: Use `logging.getLogger(__name__)` for module loggers. Log at appropriate levels (DEBUG, INFO, WARNING, ERROR).
- **Async/Await**: Not used; synchronous code only.
- **Security**: Never log sensitive data like API keys. Use encrypted storage for credentials.