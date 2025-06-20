# Customization Guide

Learn how to customize and extend awesome-claude-code templates for your specific needs, team preferences, and unique workflows.

## 🎯 Customization Philosophy

The templates in awesome-claude-code are designed to be:
- **Flexible** - Easy to modify for different use cases
- **Extensible** - Support for adding new tools and patterns
- **Maintainable** - Clear structure that survives updates
- **Team-Friendly** - Consistent across team members

## 📋 CLAUDE.md Customization

### Basic Structure
```markdown
# Project Name - Claude Configuration

## Project Overview
[Your project description and goals]

## Architecture  
[Your specific technology stack and design decisions]

## Development Workflow
[Your team's specific commands and processes]

## Code Quality Standards
[Your quality requirements and tools]

## Critical Rules - NEVER VIOLATE
[Your non-negotiable requirements]

## Common Commands
[Your frequently used commands]

## Testing Strategy
[Your testing approach and requirements]

## Environment Variables
[Your configuration requirements]

## Claude-Specific Instructions
[Your AI assistant guidelines]
```

### Advanced Customization Patterns

#### 1. Framework-Specific Instructions
```markdown
## FastAPI Specific Guidelines
- Always use async/await for database operations
- Implement proper dependency injection patterns
- Use Pydantic models for request/response validation
- Follow REST API conventions for endpoint design
- Include proper OpenAPI documentation

## Code Examples
When generating FastAPI code, follow these patterns:

```python
# Preferred async pattern
@app.get("/users/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    return await user_service.get_user(db, user_id)
```
```

#### 2. Domain-Specific Rules
```markdown
## Financial Services Compliance
- NEVER log sensitive financial data (SSN, account numbers, etc.)
- ALWAYS validate input data against business rules
- ALWAYS include audit trails for financial transactions
- ALWAYS use encrypted connections for database access
- FOLLOW PCI DSS guidelines for payment processing

## Healthcare Compliance (HIPAA)
- NEVER log patient identifiable information
- ALWAYS use encrypted storage for patient data
- ALWAYS implement proper access controls
- FOLLOW HIPAA guidelines for data handling
```

#### 3. Team-Specific Conventions
```markdown
## Team Conventions
- **Branch Naming**: feature/JIRA-123-short-description
- **Commit Messages**: Use conventional commits (feat:, fix:, docs:)
- **Code Review**: Minimum 2 reviewers for production code
- **Testing**: 90% code coverage requirement
- **Documentation**: Update README.md for any API changes

## Team Communication
- Use @channel in Slack for deployment notifications
- Link JIRA tickets in all PRs
- Update project status in weekly standups
- Document architectural decisions in ADR format
```

### Dynamic Content Based on Context
```markdown
## Context-Aware Instructions
When working in the `/api` directory:
- Focus on API design and documentation
- Ensure proper error handling and status codes
- Validate all input parameters
- Include rate limiting considerations

When working in the `/tests` directory:
- Write comprehensive test cases
- Include both positive and negative test scenarios
- Mock external dependencies appropriately
- Ensure tests are deterministic and fast

When working in the `/docs` directory:
- Update relevant documentation
- Ensure examples are current and working
- Include code samples where appropriate
- Maintain consistent formatting and style
```

## ⚙️ settings.json Customization

### Permission Customization
```json
{
  "permissions": {
    "allow": [
      // Basic Git operations
      "Bash(git status)",
      "Bash(git add*)",
      "Bash(git commit*)",
      
      // Framework-specific commands
      "Bash(npm run*)",           // Node.js projects
      "Bash(python manage.py*)",  // Django projects
      "Bash(uvicorn*)",           // FastAPI projects
      "Bash(pytest*)",            // Python testing
      
      // Database operations
      "Bash(psql*)",              // PostgreSQL
      "Bash(mysql*)",             // MySQL
      "Bash(redis-cli*)",         // Redis
      
      // Deployment commands
      "Bash(docker*)",            // Docker operations
      "Bash(kubectl*)",           // Kubernetes
      "Bash(terraform*)",         // Infrastructure
      
      // File operations
      "Edit(src/**)",             // Source code
      "Edit(tests/**)",           // Test files
      "Edit(docs/**)",            // Documentation
      "Read(*.md)",              // Markdown files
      "Read(*.json)",            // Configuration files
      
      // Custom scripts
      "Bash(scripts/*)"           // Custom project scripts
    ],
    "deny": [
      // Security restrictions
      "Bash(rm -rf*)",           // Prevent destructive operations
      "Bash(sudo*)",             // Prevent privilege escalation
      "Bash(curl*)",             // Prevent external downloads
      "Edit(.env)",              // Protect environment variables
      "Edit(secrets/**)",        // Protect secret files
      "Read(.env)",              // Prevent reading secrets
      
      // Production restrictions
      "Bash(*production*)",      // Prevent production commands
      "Bash(*prod*)",            // Prevent production shortcuts
      "Edit(*production*)"       // Prevent editing production files
    ]
  }
}
```

### Environment Variables
```json
{
  "env": {
    // Claude Code specific
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "CLAUDE_CODE_MAX_OUTPUT_TOKENS": "8000",
    
    // Project specific
    "PYTHONPATH": "./src",
    "PYTHON_VERSION": "3.11",
    "NODE_ENV": "development",
    
    // Development tools
    "PYTEST_CURRENT_TEST": "1",
    "COVERAGE_THRESHOLD": "90",
    
    // Framework specific
    "DJANGO_SETTINGS_MODULE": "config.settings.local",
    "FASTAPI_ENV": "development",
    
    // Custom variables
    "PROJECT_ROOT": ".",
    "LOG_LEVEL": "INFO",
    "DEBUG_MODE": "true"
  }
}
```

### Advanced Configuration Options
```json
{
  "permissions": {
    "allow": ["..."],
    "deny": ["..."]
  },
  "env": {"..."},
  
  // Cleanup settings
  "cleanupPeriodDays": 30,
  
  // Git integration
  "includeCoAuthoredBy": true,
  
  // Notification preferences
  "preferredNotifChannel": "desktop",
  
  // UI preferences
  "theme": "dark",
  
  // Performance settings
  "maxConcurrentOperations": 3,
  "timeoutSeconds": 30,
  
  // Logging
  "logLevel": "INFO",
  "logToFile": true
}
```

## 🌐 MCP Server Customization

### Database Servers
```json
{
  "mcpServers": {
    "postgres-dev": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "POSTGRES_CONNECTION_STRING": "postgresql://user:pass@localhost:5432/myproject_dev"
      }
    },
    "postgres-test": {
      "command": "npx", 
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "POSTGRES_CONNECTION_STRING": "postgresql://user:pass@localhost:5432/myproject_test"
      }
    }
  }
}
```

### Custom MCP Server
```json
{
  "mcpServers": {
    "custom-api": {
      "command": "python",
      "args": ["-m", "my_custom_mcp_server"],
      "env": {
        "API_BASE_URL": "https://api.mycompany.com",
        "API_KEY": "${API_KEY}",
        "TIMEOUT": "30"
      }
    }
  }
}
```

### Conditional MCP Servers
```json
{
  "mcpServers": {
    "development-only": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem"],
      "env": {
        "ALLOWED_DIRECTORIES": "/tmp,./sandbox",
        "ENVIRONMENT": "development"
      },
      "condition": {
        "env": {
          "NODE_ENV": "development"
        }
      }
    }
  }
}
```

## 🛠️ Custom Commands

### Creating Custom Slash Commands

#### 1. Project-Specific Commands
Create `.claude/commands/` directory and add custom commands:

**`.claude/commands/deploy-staging.md`**
```markdown
# Deploy to Staging

Deploy the current branch to staging environment with proper checks.

## Steps:
1. **Pre-deployment checks**:
   ```bash
   # Run tests
   pytest tests/ -v
   
   # Check code quality
   flake8 src/
   black --check src/
   
   # Security scan
   bandit -r src/
   ```

2. **Build and deploy**:
   ```bash
   # Build Docker image
   docker build -t myproject:staging .
   
   # Deploy to staging
   kubectl apply -f k8s/staging/
   
   # Update deployment
   kubectl set image deployment/myproject myproject=myproject:staging
   ```

3. **Post-deployment verification**:
   ```bash
   # Health check
   curl -f https://staging.myproject.com/health
   
   # Run smoke tests
   pytest tests/smoke/ --env=staging
   ```

Arguments: $ARGUMENTS (optional: specific service name)
```

**Usage:**
```bash
/project:deploy-staging
/project:deploy-staging api  # Deploy specific service
```

#### 2. Global Personal Commands
Create `~/.claude/commands/` for personal shortcuts:

**`~/.claude/commands/quick-review.md`**
```markdown
# Quick Code Review

Perform a quick code review focusing on common issues.

## Review Checklist:
1. **Security**: Check for hardcoded secrets, SQL injection, XSS
2. **Performance**: Look for N+1 queries, inefficient algorithms
3. **Maintainability**: Check code complexity, documentation
4. **Testing**: Verify test coverage, edge cases
5. **Standards**: Ensure coding standards compliance

## Commands to run:
```bash
# Security scan
bandit -r . -ll

# Performance profiling
python -m cProfile -s cumulative main.py

# Code complexity
radon cc . -a

# Test coverage
pytest --cov=. --cov-report=term-missing
```

Generate a summary report with findings and recommendations.

Arguments: $ARGUMENTS (optional: specific files or directories)
```

### Advanced Command Patterns

#### 1. Parameterized Commands
```markdown
# Create Feature Branch

Create a new feature branch with proper naming and setup.

## Process:
1. Ensure main branch is up to date
2. Create new branch: feature/JIRA-${TICKET}-${DESCRIPTION}
3. Set up branch-specific configuration
4. Create initial commit with branch setup

```bash
# Update main
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/JIRA-$1-$2

# Set up branch configuration
git config branch.feature/JIRA-$1-$2.remote origin
git config branch.feature/JIRA-$1-$2.merge refs/heads/feature/JIRA-$1-$2

# Initial commit
git commit --allow-empty -m "feat: initialize feature branch for JIRA-$1"
```

Arguments: 
- $1: JIRA ticket number (e.g., 123)
- $2: Brief description (e.g., user-authentication)
```

#### 2. Environment-Aware Commands
```markdown
# Database Migration

Run database migrations with environment-specific safety checks.

## Environment Detection:
- Production: Requires confirmation and backup
- Staging: Requires confirmation
- Development: Runs automatically

```bash
ENV=${NODE_ENV:-development}

case $ENV in
  production)
    echo "⚠️  Production migration detected!"
    echo "1. Creating backup..."
    pg_dump $DATABASE_URL > backup_$(date +%Y%m%d_%H%M%S).sql
    
    echo "2. Please confirm migration (yes/no):"
    read CONFIRM
    if [ "$CONFIRM" != "yes" ]; then
      echo "Migration cancelled"
      exit 1
    fi
    ;;
  staging)
    echo "🚧 Staging migration"
    echo "Confirm migration (yes/no):"
    read CONFIRM
    if [ "$CONFIRM" != "yes" ]; then
      echo "Migration cancelled"
      exit 1
    fi
    ;;
  *)
    echo "🔧 Development migration"
    ;;
esac

# Run migrations
python manage.py migrate
```

Arguments: $ARGUMENTS (optional: specific migration name)
```

## 🎭 Team Preset Customization

### Creating Custom Team Presets

#### 1. Backend API Team Preset
**`presets/backend-api-team.json`**
```json
{
  "name": "backend-api-team",
  "description": "Backend API development with microservices focus",
  "framework": "fastapi",
  "database": "postgresql",
  "python_version": "3.11",
  "package_manager": "poetry",
  "tools": {
    "black": true,
    "isort": true,
    "flake8": true,
    "mypy": true,
    "pytest": true,
    "bandit": true
  },
  "mcp_servers": {
    "postgres": true,
    "fetch": true,
    "github": true,
    "filesystem": false
  },
  "additional_tools": [
    "uvicorn",
    "sqlalchemy", 
    "alembic",
    "redis",
    "celery"
  ],
  "custom_rules": [
    "Always use async/await for database operations",
    "Implement proper API versioning",
    "Include comprehensive API documentation",
    "Use dependency injection for testability",
    "Implement proper error handling and logging"
  ]
}
```

#### 2. ML/Data Science Team Preset
**`presets/ml-team.json`**
```json
{
  "name": "ml-team",
  "description": "Machine learning and data science workflows",
  "framework": "data-science",
  "database": "none",
  "python_version": "3.11", 
  "package_manager": "conda",
  "tools": {
    "black": true,
    "isort": true,
    "flake8": false,
    "mypy": false,
    "pytest": true,
    "bandit": false
  },
  "mcp_servers": {
    "python": true,
    "filesystem": true,
    "fetch": true,
    "jupyter": true
  },
  "additional_tools": [
    "jupyter",
    "pandas",
    "numpy",
    "scikit-learn",
    "matplotlib",
    "seaborn",
    "mlflow",
    "dvc"
  ],
  "custom_rules": [
    "Use Jupyter notebooks for exploration, Python scripts for production",
    "Always version your datasets with DVC",
    "Document data preprocessing steps thoroughly",
    "Include model performance metrics in all experiments",
    "Use virtual environments for reproducible experiments"
  ]
}
```

### Using Custom Presets
```bash
# Use your custom preset
python tools/setup.py --preset backend-api-team

# Override specific settings
python tools/setup.py --preset ml-team --database postgresql
```

## 🔧 Advanced Customization Techniques

### 1. Conditional Configuration
Create configurations that adapt based on environment:

```markdown
## Environment-Specific Rules

{% if environment == "production" %}
## Production Rules
- NEVER allow direct database access
- ALWAYS require code review for deployments
- ALWAYS use encrypted connections
- NEVER log sensitive information
{% elif environment == "staging" %}
## Staging Rules  
- Allow limited database access for debugging
- Require approval for schema changes
- Use production-like data (anonymized)
{% else %}
## Development Rules
- Allow full database access
- Enable debug logging
- Use sample test data
{% endif %}
```

### 2. Template Inheritance
Create base templates that can be extended:

**`templates/base/CLAUDE.md`**
```markdown
# Base Claude Configuration

## Universal Rules
- NEVER commit secrets to version control
- ALWAYS use meaningful commit messages
- ALWAYS include tests for new features
- ALWAYS update documentation

## Code Quality
- Use consistent formatting
- Include type hints where applicable  
- Write self-documenting code
- Handle errors gracefully

## Security
- Validate all inputs
- Use parameterized queries
- Implement proper authentication
- Follow principle of least privilege
```

**`templates/project/frameworks/fastapi/CLAUDE.md`**
```markdown
{% extends "base/CLAUDE.md" %}

# FastAPI Project Configuration

{% block project_specific %}
## FastAPI Specific Rules
- Use async/await for all database operations
- Implement proper dependency injection
- Include comprehensive API documentation
- Use Pydantic models for validation
{% endblock %}

{% block commands %}
## FastAPI Commands
```bash
# Development server
uvicorn main:app --reload

# API documentation
open http://localhost:8000/docs

# Run tests
pytest tests/ -v
```
{% endblock %}
```

### 3. Dynamic Rule Generation
Create rules that adapt to the codebase:

```python
# In your setup tool customization
def generate_dynamic_rules(project_path):
    rules = []
    
    # Detect existing patterns
    if has_async_code(project_path):
        rules.append("Use async/await consistently throughout the codebase")
    
    if has_database_models(project_path):
        rules.append("Always create database migrations for model changes")
    
    if has_api_endpoints(project_path):
        rules.append("Include proper API documentation for all endpoints")
    
    return rules
```

## 📊 Validation and Testing

### Custom Validation Rules
Create your own validation logic:

**`tools/custom_validator.py`**
```python
import json
from pathlib import Path

def validate_custom_rules(claude_md_path: Path) -> List[str]:
    """Validate custom project rules."""
    errors = []
    content = claude_md_path.read_text()
    
    # Check for required sections
    required_sections = [
        "## Project Overview",
        "## Critical Rules",
        "## Team Conventions"
    ]
    
    for section in required_sections:
        if section not in content:
            errors.append(f"Missing required section: {section}")
    
    # Check for team-specific requirements
    if "JIRA-" not in content and "team" in content.lower():
        errors.append("Team projects should reference ticket system")
    
    return errors
```

### Testing Custom Configurations
```bash
# Test your custom setup
mkdir test-project
cd test-project
python ../awesome-claude-code/tools/setup.py --preset my-custom-preset

# Validate the results
python ../awesome-claude-code/tools/validate-config.py .

# Test with real Claude Code
claude
# Try some commands to ensure everything works
```

## 🚀 Deployment and Sharing

### Sharing Team Configurations
1. **Version Control**: Keep team configurations in your project repository
2. **Documentation**: Document any custom rules or patterns
3. **Onboarding**: Include setup instructions in your team's onboarding guide

### Contributing Back
If your customizations would benefit others:
1. **Create a template**: Generalize your specific customizations
2. **Write documentation**: Explain the use case and benefits
3. **Submit a PR**: Share with the awesome-claude-code community

### Maintaining Custom Configurations
```bash
# Create a backup before updates
cp -r .claude .claude-backup

# Update base templates
git pull origin main

# Re-apply your customizations
python tools/setup.py --preset your-team --merge-existing
```

## 🔍 Debugging Customizations

### Common Issues and Solutions

#### 1. Claude Code Not Loading Configuration
```bash
# Check file location
ls -la CLAUDE.md .claude/settings.json

# Verify JSON syntax
python -m json.tool .claude/settings.json

# Check permissions
chmod 644 CLAUDE.md .claude/settings.json
```

#### 2. Commands Not Working
```bash
# Check permissions in settings.json
grep -A 10 '"allow"' .claude/settings.json

# Test command manually
bash -c "your-command-here"
```

#### 3. MCP Servers Not Connecting
```bash
# Test MCP configuration
python -m json.tool .mcp.json

# Check server status
claude mcp list
claude mcp test server-name
```

Remember: Customization is an iterative process. Start with small changes, test thoroughly, and gradually build up your ideal configuration!