# Global Claude Configuration

## Development Environment
- **OS**: WSL2 (Ubuntu) on Windows / macOS / Linux
- **Primary IDE**: Windsurf (AI-powered VS Code fork) / VS Code / PyCharm
- **Python**: Python 3.11+ with pyenv for version management
- **Shell**: Bash/Zsh in WSL/Unix environments

## Python Development Standards
- **Code Style**: Black (88 char line length), isort, flake8, mypy
- **Documentation**: Google-style docstrings with type hints
- **Testing**: pytest with coverage reports (90%+ target)
- **Virtual Environments**: Always use venv, conda, or poetry
- **Package Management**: Pin versions in production, flexible in development

## Common Commands
```bash
# Python environment management
pyenv versions                    # List Python versions
python -m venv .venv             # Create virtual environment
source .venv/bin/activate        # Activate environment (Unix)
.venv\Scripts\activate           # Activate environment (Windows)
pip install -r requirements.txt  # Install dependencies
pip freeze > requirements.txt    # Save current dependencies

# Code quality and formatting
black .                          # Format code (88 char line length)
black --line-length 100 .       # Format with custom line length
isort .                          # Sort imports
flake8 .                         # Linting and style checks
mypy .                           # Type checking
bandit -r .                      # Security vulnerability scanning

# Testing and coverage
pytest                           # Run all tests
pytest -v                       # Verbose test output
pytest --cov=src                # Run with coverage report
pytest --cov=src --cov-report=html  # HTML coverage report
pytest -k "test_user"           # Run specific test patterns
pytest --markers                # List available test markers

# Git workflow
git status                       # Check repository status
git add -A                       # Stage all changes
git commit -m "feat: description"  # Conventional commit message
git push origin main             # Push to main branch
git pull --rebase origin main   # Pull with rebase to avoid merge commits
git log --oneline -10           # Show recent commit history

# Package management alternatives
pip install package_name         # Install with pip
pip install -e .                # Install current package in development mode
poetry install                  # Install with poetry
poetry add package_name         # Add dependency with poetry
conda install package_name      # Install with conda
conda env create -f environment.yml  # Create conda environment from file
```

## Development Preferences and Standards
- **Type Hints**: Always use type annotations for function parameters and return values
- **Error Handling**: Comprehensive try/catch blocks with proper logging for production code
- **Testing Philosophy**: Write tests alongside implementation, not as an afterthought
- **Documentation**: Update README.md and docstrings when adding features
- **Security**: Use environment variables for secrets, never commit API keys
- **Performance**: Profile before optimizing, prefer readability over premature optimization

## Critical Rules - NEVER VIOLATE
- **NEVER commit secrets, API keys, or passwords** to version control
- **NEVER skip type hints** in new Python code (use `# type: ignore` sparingly)
- **NEVER push to main branch** without running tests and quality checks
- **ALWAYS use virtual environments** for Python projects to avoid dependency conflicts
- **ALWAYS validate and sanitize user inputs** to prevent security vulnerabilities
- **ALWAYS include comprehensive error handling** in production code paths
- **ALWAYS update requirements.txt or pyproject.toml** when adding dependencies
- **NEVER use `sudo pip install`** - use virtual environments or user installs instead

## Prompt Engineering Patterns
Use these proven prompt patterns for better results:

### Planning and Architecture
- **"Think hard about architecture before coding"** - For complex features or system design
- **"Create a detailed implementation plan"** - Before starting large features
- **"Consider edge cases and error handling"** - For robust implementation

### Code Quality and Testing
- **"Include comprehensive error handling"** - For production-ready code
- **"Write unit tests alongside implementation"** - For test-driven development
- **"Follow Python best practices and PEP 8"** - For clean, maintainable code
- **"Add type hints and docstrings"** - For professional code documentation

### Debugging and Analysis
- **"Analyze this error systematically"** - For complex debugging scenarios
- **"Use the Five Whys technique"** - For root cause analysis
- **"Profile this code for performance"** - For optimization tasks

### Code Review and Improvement
- **"Review this code for security vulnerabilities"** - For security-focused review
- **"Suggest improvements for maintainability"** - For refactoring guidance
- **"Check for potential performance issues"** - For optimization opportunities

### Personas
- **/persona architect**: Analyze the code from an architectural perspective.
- **/persona developer**: Analyze the code from a developer's perspective.
- **/persona tester**: Analyze the code from a tester's perspective.

## File Organization Principles
```
project-root/
├── src/                 # Source code (importable package)
├── tests/              # Test files (mirror src structure)
├── docs/               # Documentation
├── scripts/            # Utility scripts and automation
├── data/               # Data files (not committed if large)
├── config/             # Configuration files
├── requirements.txt    # Production dependencies
├── requirements-dev.txt # Development dependencies
├── .env.example       # Environment variables template
├── .gitignore         # Git ignore patterns
├── README.md          # Project documentation
├── pyproject.toml     # Modern Python project configuration
└── Makefile or tasks.py # Task automation
```

## Environment Variables Best Practices
```bash
# Development environment template
DEBUG=True
LOG_LEVEL=INFO
DATABASE_URL=postgresql://localhost/myproject_dev
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=development-secret-key-change-in-production
API_KEY=your-development-api-key

# Security guidelines for environment variables
# 1. Never commit .env files to version control
# 2. Provide .env.example with dummy values
# 3. Use different keys for different environments
# 4. Rotate keys regularly in production
# 5. Use secrets management for production (AWS Secrets Manager, etc.)
```

## IDE and Tool Integration
- **VS Code/Windsurf Extensions**: Python, Pylance, GitLens, Thunder Client, Docker
- **PyCharm Configuration**: Enable type checking, configure code style to match Black
- **Git Hooks**: Use pre-commit hooks for automatic formatting and linting
- **Terminal Setup**: Configure shell aliases for common commands

## Performance and Optimization Guidelines
- **Profiling**: Use cProfile for performance analysis before optimizing
- **Database**: Use connection pooling and query optimization
- **Caching**: Implement caching for expensive operations (Redis, in-memory)
- **Async Programming**: Use async/await for I/O-bound operations
- **Memory Management**: Be aware of memory usage in long-running processes

## Security Checklist
- [ ] Input validation and sanitization implemented
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS prevention (proper output encoding)
- [ ] Authentication and authorization in place
- [ ] Secrets stored in environment variables or secrets manager
- [ ] HTTPS used for all external communications
- [ ] Dependencies regularly updated for security patches
- [ ] Error messages don't leak sensitive information

## Collaboration and Code Review Standards
- **Branch Naming**: `feature/TICKET-123-short-description`, `bugfix/fix-login-issue`
- **Commit Messages**: Use conventional commits (feat:, fix:, docs:, refactor:, test:)
- **Pull Requests**: Include description, testing notes, and breaking changes
- **Code Review**: Focus on logic, security, performance, and maintainability
- **Documentation**: Update relevant docs with any API or behavior changes

## Learning and Development
- **Stay Updated**: Follow Python community news, PEPs, and best practices
- **Continuous Learning**: Regularly read about new libraries and tools
- **Community Participation**: Contribute to open source projects when possible
- **Knowledge Sharing**: Document lessons learned and share with team

## Claude-Specific Instructions
- **Context Management**: Use `/context-prime` at start of new projects or major features
- **Quality Assurance**: Run `/check` before committing to catch issues early
- **Incremental Development**: Make small, focused changes rather than large refactors
- **Documentation**: Update this CLAUDE.md file when you discover new effective patterns
- **Testing**: Include test generation in all feature development requests
- **Error Recovery**: Use `/clear` if conversation goes off-track, `/compact` to summarize progress

## Effective Claude Code Usage Patterns
1. **Start with Context**: Always begin sessions with `/context-prime` for project awareness
2. **Incremental Development**: Build features step-by-step with testing at each stage
3. **Quality Gates**: Use `/clean` and `/check` frequently during development
4. **External Memory**: Use GitHub issues or markdown files for complex planning
5. **Review Process**: Use `/pr-review` for comprehensive code review feedback