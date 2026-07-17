# Decision Log

## Why SQLite?
- Lightweight, file-based database
- No server required
- Perfect for development and small-scale use
- Easy to set up and maintain
- Works seamlessly with SQLAlchemy

## Why SQLAlchemy?
- ORM for database interactions
- Abstracts away SQL dialect differences
- Provides query building and model relationships
- Well-suited for FastAPI applications
- Easy to migrate to other databases if needed

## Why FastAPI?
- High performance (based on Starlette and Pydantic)
- Automatic API documentation (Swagger UI/Redoc)
- Built-in request validation with Pydantic
- Asynchronous support
- Modern Python features (type hints, etc.)

## Why Content Hashing?
- Efficient change detection
- SHA-256 for reliability
- Normalizes whitespace for consistent hashing
- Enables staleness detection for generated artifacts
- Supports version comparison

## Why Version Pinning?
- Ensures selections are tied to specific versions
- Prevents unexpected changes to selections
- Enables accurate staleness checks
- Maintains reproducibility

## Why Modular Architecture?
- Separates concerns (API, services, models, LLM)
- Easier to test individual components
- Enables independent development of features
- Improves maintainability and scalability
- Follows clean architecture principles
