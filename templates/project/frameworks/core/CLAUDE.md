# Core Python Project - Claude Configuration

## Project Overview
This is a general-purpose Python project designed for flexibility and following modern Python development best practices. This template provides a solid foundation for any Python project including libraries, utilities, scripts, research projects, or custom applications that don't fit into specific framework categories.

**Key Technologies:**
- **Python 3.8+**: Modern Python with type hints and latest features
- **pytest**: Comprehensive testing framework
- **Black + isort**: Code formatting and import sorting
- **mypy**: Static type checking
- **pre-commit**: Git hooks for code quality
- **setuptools/Poetry**: Package management and distribution
- **Virtual environments**: Isolation and dependency management

## Architecture & Patterns

### Directory Structure
```
project/
├── src/
│   └── package_name/           # Main package directory
│       ├── __init__.py
│       ├── main.py             # Main entry point
│       ├── core/               # Core functionality
│       │   ├── __init__.py
│       │   ├── config.py       # Configuration handling
│       │   ├── exceptions.py   # Custom exceptions
│       │   └── utils.py        # Utility functions
│       ├── modules/            # Feature modules
│       │   ├── __init__.py
│       │   └── feature.py      # Feature implementations
│       └── data/               # Data processing (if applicable)
│           ├── __init__.py
│           ├── models.py       # Data models
│           └── processors.py   # Data processing logic
├── tests/                      # Test files
│   ├── __init__.py
│   ├── conftest.py             # pytest configuration
│   ├── test_core/              # Core functionality tests
│   ├── test_modules/           # Module tests
│   └── fixtures/               # Test data and fixtures
├── docs/                       # Documentation
│   ├── index.md                # Main documentation
│   ├── api.md                  # API documentation
│   └── examples/               # Usage examples
├── scripts/                    # Utility scripts
│   ├── setup.py                # Setup utilities
│   └── deploy.py               # Deployment scripts
├── configs/                    # Configuration files
│   ├── settings.yaml           # Application settings
│   └── logging.yaml            # Logging configuration
├── requirements.txt            # Dependencies
├── requirements-dev.txt        # Development dependencies
├── pyproject.toml             # Modern Python configuration
├── setup.py                   # Package setup (if needed)
├── README.md                  # Project documentation
├── CHANGELOG.md               # Version history
├── LICENSE                    # License file
└── .env.example               # Environment variables template
```

### Python Development Patterns
- **Package structure**: Proper `src/` layout for distribution
- **Modular design**: Clear separation of concerns
- **Configuration management**: External config files and environment variables
- **Error handling**: Custom exceptions and comprehensive error handling
- **Logging**: Structured logging with configurable levels
- **Documentation**: Comprehensive docstrings and external documentation
- **Testing**: Unit tests, integration tests, and test fixtures

## Development Workflow

### Common Commands
```bash
# Virtual environment setup
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Alternative: Poetry
poetry install
poetry shell

# Alternative: Conda
conda create -n project-name python=3.9
conda activate project-name

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
poetry install --with dev

# Development installation
pip install -e .
poetry install

# Testing
pytest
pytest -v                          # Verbose output
pytest --cov=src tests/           # With coverage
pytest -k "test_specific"         # Run specific tests
pytest --cov-report=html          # HTML coverage report

# Code quality
black src/ tests/                 # Code formatting
isort src/ tests/                 # Import sorting
flake8 src/ tests/                # Linting
mypy src/                         # Type checking
bandit src/                       # Security scanning

# Pre-commit hooks
pre-commit install
pre-commit run --all-files

# Package building
python setup.py sdist bdist_wheel
poetry build
twine upload dist/*               # Upload to PyPI

# Documentation
mkdocs serve                      # Serve documentation locally
sphinx-build docs/ docs/_build/   # Build Sphinx docs
```

### Development Process
1. **Project initialization** - Set up virtual environment and dependencies
2. **Code structure** - Organize code into logical modules and packages
3. **Configuration setup** - Environment variables and config files
4. **Testing implementation** - Unit tests and integration tests
5. **Documentation** - Code documentation and usage examples
6. **Quality assurance** - Linting, type checking, and security scanning
7. **Version control** - Git workflow with meaningful commits
8. **CI/CD setup** - Automated testing and deployment
9. **Package distribution** - PyPI publishing (if applicable)

### Git Workflow
- **Feature branches**: `feature/add-new-module`
- **Conventional commits**: Clear, descriptive commit messages
- **Version tagging**: Semantic versioning (v1.2.3)
- **Documentation**: Keep README and CHANGELOG updated
- **Dependencies**: Regular dependency updates and security checks

## Code Quality & Standards

### Python Code Style
- **Follow PEP 8** with Black formatting (88 character line length)
- **Type hints**: Use for all function parameters and returns
- **Docstrings**: Google style for all public functions, classes, and modules
- **Import organization**: isort with standard library, third-party, local imports
- **Error handling**: Explicit exception handling with informative messages

### Code Organization Standards
- **Single responsibility**: Each module and function has a clear purpose
- **DRY principle**: Don't repeat yourself - extract common functionality
- **SOLID principles**: Object-oriented design best practices
- **Configuration externalization**: No hardcoded values in source code
- **Logging over print**: Use logging module for all output
- **Constants**: Define constants in a central location

### Documentation Standards
- **README.md**: Clear project description, installation, and usage
- **Docstrings**: All public APIs documented with examples
- **Type annotations**: Help with IDE support and documentation generation
- **CHANGELOG.md**: Document all notable changes
- **Examples**: Practical usage examples in docs/ or examples/
- **API documentation**: Auto-generated from docstrings

## Testing Strategy

### Test Types
```python
# Unit tests - Test individual functions and classes
def test_utility_function():
    result = utility_function(input_data)
    assert result == expected_output
    assert isinstance(result, ExpectedType)

# Integration tests - Test component interactions
def test_data_processing_pipeline():
    processor = DataProcessor(config)
    result = processor.process(sample_data)
    assert result.status == "success"
    assert len(result.data) > 0

# Property-based tests - Test with generated data
from hypothesis import given, strategies as st

@given(st.text())
def test_string_processing(input_string):
    result = process_string(input_string)
    assert isinstance(result, str)
    assert len(result) >= 0

# Fixture usage - Reusable test data
@pytest.fixture
def sample_config():
    return {
        "debug": True,
        "log_level": "INFO",
        "max_items": 100
    }

def test_with_config(sample_config):
    processor = Processor(sample_config)
    assert processor.debug is True
```

### Test Configuration
- **pytest.ini**: Configure pytest behavior and plugins
- **conftest.py**: Shared fixtures and test configuration
- **Test isolation**: Each test is independent and can run alone
- **Mock external dependencies**: Use unittest.mock for external services
- **Coverage targets**: Aim for >80% code coverage
- **Performance tests**: Test critical paths for performance regressions

## Environment Variables

### Configuration Variables
```bash
# Application settings
PROJECT_ENV=development
PROJECT_DEBUG=true
PROJECT_LOG_LEVEL=INFO
PROJECT_CONFIG_FILE=configs/settings.yaml

# Development settings
PYTHONPATH=./src
PYTHONDONTWRITEBYTECODE=1
PYTHONUNBUFFERED=1

# Testing
TEST_DATABASE_URL=sqlite:///:memory:
TEST_LOG_LEVEL=WARNING

# External services (if applicable)
API_URL=https://api.example.com
API_KEY=your-api-key
DATABASE_URL=sqlite:///data.db
CACHE_URL=redis://localhost:6379

# Build and deployment
BUILD_ENV=development
DEPLOYMENT_TARGET=local
VERSION=1.0.0
```

### Configuration Management
```python
# config.py example
import os
from pathlib import Path
from typing import Optional

class Config:
    """Application configuration."""
    
    # Base settings
    DEBUG: bool = os.getenv("PROJECT_DEBUG", "false").lower() == "true"
    LOG_LEVEL: str = os.getenv("PROJECT_LOG_LEVEL", "INFO")
    ENV: str = os.getenv("PROJECT_ENV", "development")
    
    # Paths
    PROJECT_ROOT: Path = Path(__file__).parent.parent
    CONFIG_DIR: Path = PROJECT_ROOT / "configs"
    DATA_DIR: Path = PROJECT_ROOT / "data"
    
    # External services
    API_URL: Optional[str] = os.getenv("API_URL")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///data.db")
    
    @classmethod
    def load_from_file(cls, config_path: str) -> "Config":
        """Load configuration from YAML file."""
        # Implementation for loading from file
        pass
```

## Package Development

### setuptools Configuration
```python
# setup.py
from setuptools import setup, find_packages

setup(
    name="your-package-name",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A short description of your package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/your-package",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.0",
        "pydantic>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "mypy>=1.0.0",
            "flake8>=5.0.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "your-tool=your_package.main:main",
        ],
    },
)
```

### Modern pyproject.toml
```toml
[build-system]
requires = ["setuptools>=45", "wheel", "setuptools_scm[toml]>=6.2"]
build-backend = "setuptools.build_meta"

[project]
name = "your-package-name"
authors = [{name = "Your Name", email = "your.email@example.com"}]
description = "A short description of your package"
readme = "README.md"
requires-python = ">=3.8"
license = {text = "MIT"}
classifiers = [
    "Development Status :: 3 - Alpha",
    "Programming Language :: Python :: 3",
]
dependencies = [
    "requests>=2.25.0",
    "pydantic>=2.0.0",
]
dynamic = ["version"]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "black>=23.0.0",
    "mypy>=1.0.0",
    "flake8>=5.0.0",
]

[tool.setuptools.packages.find]
where = ["src"]

[tool.black]
line-length = 88
target-version = ['py38']

[tool.isort]
profile = "black"

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```

## Critical Rules

### Code Quality Requirements
- ⚠️ **ALWAYS** use type hints for all function parameters and returns
- ⚠️ **ALWAYS** include comprehensive docstrings for public APIs
- ⚠️ **NEVER** commit code without running tests and linting
- ⚠️ **ALWAYS** handle exceptions gracefully with informative messages
- ⚠️ **ALWAYS** use logging instead of print statements
- ⚠️ **NEVER** hardcode configuration values in source code

### Testing Requirements
- ⚠️ **ALWAYS** write tests for new functionality
- ⚠️ **ALWAYS** maintain test coverage above 80%
- ⚠️ **NEVER** commit failing tests
- ⚠️ **ALWAYS** test edge cases and error conditions
- ⚠️ **ALWAYS** use fixtures for reusable test data
- ⚠️ **NEVER** test implementation details, test behavior

### Security Requirements
- ⚠️ **NEVER** commit secrets, API keys, or credentials to version control
- ⚠️ **ALWAYS** use environment variables for sensitive configuration
- ⚠️ **ALWAYS** validate and sanitize all user inputs
- ⚠️ **ALWAYS** use secure coding practices (avoid eval, exec, etc.)
- ⚠️ **ALWAYS** keep dependencies updated and scan for vulnerabilities
- ⚠️ **NEVER** ignore security warnings from tools like bandit

### Documentation Requirements
- ⚠️ **ALWAYS** maintain an up-to-date README.md
- ⚠️ **ALWAYS** document breaking changes in CHANGELOG.md
- ⚠️ **ALWAYS** include usage examples in documentation
- ⚠️ **NEVER** leave TODO comments in production code
- ⚠️ **ALWAYS** document configuration options and environment variables
- ⚠️ **ALWAYS** include installation and setup instructions

## Common Commands Reference

### Daily Development
```bash
# Activate environment and install dependencies
source venv/bin/activate
pip install -r requirements-dev.txt

# Run tests and quality checks
pytest --cov=src tests/
black src/ tests/ && isort src/ tests/ && flake8 src/ tests/
mypy src/

# Run the application
python -m src.package_name
python src/package_name/main.py
```

### Package Management
```bash
# Update dependencies
pip-compile requirements.in
pip-compile requirements-dev.in
pip-sync requirements.txt requirements-dev.txt

# Poetry alternatives
poetry update
poetry add new-package
poetry add --group dev new-dev-package
```

### CI/CD and Distribution
```bash
# Build package
python setup.py sdist bdist_wheel
poetry build

# Upload to PyPI
twine upload dist/*
poetry publish

# Create release
git tag v1.0.0
git push origin v1.0.0
```

## Claude-Specific Instructions

### Code Generation Preferences
- **Always** include comprehensive type hints and docstrings
- **Always** follow the project structure and organization patterns
- **Include** proper error handling and logging
- **Add** unit tests for all new functionality
- **Use** modern Python features and best practices
- **Include** configuration management for any settings
- **Add** appropriate imports and organize them properly

### Development Focus
- **Modular design**: Create reusable, well-structured modules
- **Testing mindset**: Write testable code with dependency injection
- **Documentation**: Include examples and clear explanations
- **Performance awareness**: Consider efficiency and resource usage
- **Security consciousness**: Validate inputs and handle sensitive data properly
- **Maintainability**: Write code that's easy to understand and modify

### Project Setup Assistance
- **Help with project structure**: Create appropriate directories and files
- **Dependency management**: Suggest appropriate packages and versions
- **Configuration setup**: Help configure development tools and CI/CD
- **Testing setup**: Create test structure and example tests
- **Documentation**: Generate README, docstrings, and usage examples
- **Best practices**: Apply Python and software development best practices