# FastAPI Project - Claude Configuration

## Project Overview
This is a FastAPI-based REST API project designed for high-performance, async web services with automatic OpenAPI documentation. FastAPI provides modern Python features including async/await, type hints, and dependency injection for building robust APIs.

**Key Technologies:**
- **FastAPI**: Modern, fast web framework for building APIs
- **Uvicorn/Gunicorn**: ASGI server for production deployment
- **Pydantic**: Data validation using Python type annotations
- **SQLAlchemy**: Python SQL toolkit and ORM (if using database)
- **Alembic**: Database migration tool
- **Pytest**: Testing framework with async support

## Architecture & Patterns

### Directory Structure
```
project/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application factory
│   ├── config.py            # Configuration settings
│   ├── dependencies.py      # Dependency injection
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/             # API version 1
│   │   │   ├── __init__.py
│   │   │   ├── endpoints/  # API endpoints
│   │   │   └── deps.py     # API dependencies
│   ├── core/
│   │   ├── __init__.py
│   │   ├── security.py     # Authentication/authorization
│   │   ├── config.py       # Core configuration
│   │   └── exceptions.py   # Custom exceptions
│   ├── models/             # SQLAlchemy models
│   ├── schemas/            # Pydantic schemas
│   ├── crud/              # CRUD operations
│   └── db/                # Database configuration
├── tests/                 # Test files
├── alembic/              # Database migrations
├── requirements.txt      # Python dependencies
└── .env                 # Environment variables
```

### FastAPI Patterns
- **Router-based organization**: Use APIRouter for modular endpoints
- **Dependency injection**: Leverage FastAPI's DI system for databases, auth, etc.
- **Pydantic models**: Use for request/response validation and serialization
- **Async/await**: Prefer async functions for I/O operations
- **Background tasks**: Use for non-blocking operations
- **Exception handlers**: Custom error handling with proper HTTP status codes

## Development Workflow

### Common Commands
```bash
# Development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run with specific environment
uvicorn app.main:app --reload --env-file .env.local

# Production server
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker

# Database migrations
alembic revision --autogenerate -m "Description"
alembic upgrade head
alembic downgrade -1

# Testing
pytest
pytest -v                           # Verbose output
pytest --cov=app                   # With coverage
pytest -k "test_user"              # Run specific tests
pytest --cov=app --cov-report=html # HTML coverage report

# Code quality
black app/ tests/                  # Code formatting
isort app/ tests/                  # Import sorting
flake8 app/ tests/                 # Linting
mypy app/                          # Type checking

# API documentation
# Visit http://localhost:8000/docs (Swagger UI)
# Visit http://localhost:8000/redoc (ReDoc)
```

### Development Process
1. **Plan API endpoints** - Define routes, methods, and data models
2. **Create Pydantic schemas** - Define request/response models
3. **Implement CRUD operations** - Database interaction layer
4. **Build API endpoints** - FastAPI route handlers
5. **Add authentication** - JWT, OAuth2, or session-based
6. **Write tests** - Unit and integration tests
7. **Add documentation** - Docstrings and OpenAPI descriptions
8. **Performance optimization** - Database queries, caching, async

### Git Workflow
- **Feature branches**: `feature/user-authentication`
- **API versioning**: Use `/api/v1/` prefix for routes
- **Migration files**: Always review before committing
- **Environment files**: Never commit `.env` with secrets

## Code Quality & Standards

### Python Code Style
- **Follow PEP 8** with Black formatting
- **Type hints**: Use for all function parameters and returns
- **Docstrings**: Google style for functions and classes
- **Async/await**: Prefer over sync code for I/O operations
- **Error handling**: Use FastAPI's HTTPException for API errors

### API Design Standards
- **RESTful conventions**: GET, POST, PUT, DELETE with proper status codes
- **Consistent naming**: snake_case for JSON fields, PascalCase for models
- **Pagination**: Use limit/offset or cursor-based pagination
- **Filtering**: Query parameters for filtering and sorting
- **Error responses**: Consistent error format with detail messages
- **API versioning**: Use path-based versioning (/api/v1/)

### Database Standards
- **Migrations**: Use Alembic for all schema changes
- **Models**: SQLAlchemy ORM with proper relationships
- **Queries**: Use async sessions for database operations
- **Indexing**: Add indexes for frequently queried fields
- **Constraints**: Use database constraints for data integrity

## Testing Strategy

### Test Types
```python
# Unit tests - Test individual functions
def test_user_creation():
    user_data = {"email": "test@example.com", "password": "password123"}
    user = create_user(user_data)
    assert user.email == "test@example.com"

# API tests - Test endpoints
@pytest.mark.asyncio
async def test_get_users(client: AsyncClient):
    response = await client.get("/api/v1/users/")
    assert response.status_code == 200
    assert len(response.json()) > 0

# Integration tests - Test with database
@pytest.mark.asyncio
async def test_user_crud_operations(db_session):
    # Test create, read, update, delete operations
    pass
```

### Test Configuration
- **Test database**: Use separate database for testing
- **Fixtures**: Create reusable test data with pytest fixtures
- **Mock external services**: Use responses or httpx_mock
- **Async testing**: Use pytest-asyncio for async test functions
- **Coverage targets**: Aim for >80% code coverage

## Environment Variables

### Required Variables
```bash
# Application
SECRET_KEY=your-secret-key-here
DEBUG=False
ENVIRONMENT=development
API_V1_STR=/api/v1

# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost/dbname
TEST_DATABASE_URL=postgresql+asyncpg://user:password@localhost/test_dbname

# Authentication
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALGORITHM=HS256

# External Services
REDIS_URL=redis://localhost:6379
CELERY_BROKER_URL=redis://localhost:6379
SMTP_SERVER=localhost
SMTP_PORT=587
```

### Development vs Production
- **Development**: Use `.env.local` for local overrides
- **Testing**: Use `.env.test` for test environment
- **Production**: Use environment variables or secrets management
- **Never commit**: `.env` files with real secrets to version control

## API Documentation

### OpenAPI/Swagger
- **Automatic docs**: FastAPI generates OpenAPI spec automatically
- **Endpoint descriptions**: Add docstrings to route functions
- **Schema examples**: Use Pydantic Field examples
- **Tags**: Group related endpoints with tags
- **Response models**: Define response schemas for all endpoints

### Documentation Standards
```python
@router.post("/users/", response_model=UserResponse, tags=["users"])
async def create_user(
    *,
    db: AsyncSession = Depends(get_db),
    user_in: UserCreate,
) -> UserResponse:
    """
    Create a new user.
    
    - **email**: User email address (must be unique)
    - **password**: User password (min 8 characters)
    - **full_name**: User's full name (optional)
    
    Returns the created user without password.
    """
    # Implementation here
```

## Critical Rules

### Security Requirements
- ⚠️ **NEVER** store passwords in plain text - always hash with bcrypt
- ⚠️ **NEVER** commit secrets or API keys to version control
- ⚠️ **ALWAYS** validate input data with Pydantic models
- ⚠️ **ALWAYS** use parameterized queries to prevent SQL injection
- ⚠️ **ALWAYS** implement proper CORS configuration for production
- ⚠️ **ALWAYS** use HTTPS in production environments
- ⚠️ **NEVER** expose internal error details to API responses

### Performance Requirements
- ⚠️ **ALWAYS** use async/await for database operations
- ⚠️ **ALWAYS** implement proper database connection pooling
- ⚠️ **NEVER** perform blocking operations in async functions
- ⚠️ **ALWAYS** add database indexes for frequently queried fields
- ⚠️ **ALWAYS** implement response caching for expensive operations
- ⚠️ **NEVER** return all records without pagination

### Data Integrity
- ⚠️ **ALWAYS** use database transactions for multi-step operations
- ⚠️ **ALWAYS** validate foreign key relationships
- ⚠️ **NEVER** delete records without proper cascade handling
- ⚠️ **ALWAYS** backup database before running migrations in production
- ⚠️ **ALWAYS** use database constraints for data validation

## Common Commands Reference

### Daily Development
```bash
# Start development
uvicorn app.main:app --reload

# Run tests with coverage
pytest --cov=app --cov-report=term-missing

# Format and lint code
black app/ tests/ && isort app/ tests/ && flake8 app/ tests/

# Check types
mypy app/

# Create new migration
alembic revision --autogenerate -m "Add user table"

# Apply migrations
alembic upgrade head
```

### Database Operations
```bash
# Reset database
alembic downgrade base && alembic upgrade head

# Create test data
python -m app.scripts.create_test_data

# Backup database
pg_dump $DATABASE_URL > backup.sql

# Load backup
psql $DATABASE_URL < backup.sql
```

### Deployment
```bash
# Build for production
pip freeze > requirements.txt

# Run production server
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# Health check
curl http://localhost:8000/health

# Load test
ab -n 1000 -c 10 http://localhost:8000/api/v1/users/
```

## Claude-Specific Instructions

### Code Generation Preferences
- **Always** include type hints in generated Python code
- **Always** create Pydantic models for request/response schemas
- **Prefer** async functions for all I/O operations
- **Include** comprehensive error handling with proper HTTP status codes
- **Add** docstrings with parameter descriptions for all public functions
- **Use** dependency injection pattern for database sessions and services
- **Follow** FastAPI best practices for route organization and structure

### Response Format
- **Code blocks**: Use Python syntax highlighting
- **Explanations**: Include brief comments explaining FastAPI-specific patterns
- **Examples**: Provide working examples that can be copied and pasted
- **Testing**: Include corresponding test code when generating endpoints
- **Documentation**: Add OpenAPI documentation strings for generated routes

### Architecture Decisions
- **Prefer** SQLAlchemy async sessions over sync
- **Use** Pydantic v2 syntax and features
- **Implement** proper separation of concerns (models, schemas, CRUD, routes)
- **Include** proper exception handling with custom exceptions
- **Add** logging statements for debugging and monitoring
- **Consider** caching strategies for frequently accessed data

### Development Focus
- **API-first design**: Start with API specification before implementation
- **Test-driven development**: Write tests alongside implementation
- **Performance awareness**: Consider async patterns and database efficiency
- **Security mindset**: Always consider authentication and authorization
- **Documentation**: Maintain up-to-date API documentation
- **Monitoring**: Include health checks and metrics endpoints