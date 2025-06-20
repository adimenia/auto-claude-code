# Best Practices for Claude Code

Proven strategies and optimization techniques for maximizing productivity with Claude Code and awesome-claude-code templates.

## 🎯 Core Principles

### 1. Think First, Code Later
```
❌ "Write a user authentication system"
✅ "Think hard about user authentication architecture. Create a detailed plan covering:
   - Database schema design
   - Security considerations (password hashing, JWT tokens)
   - API endpoint structure
   - Error handling patterns
   - Testing strategy
   Only start coding after we've confirmed the plan."
```

### 2. Be Specific and Contextual
```
❌ "Fix this bug"
✅ "Fix the login bug where users see a blank screen after entering wrong credentials. 
   The issue appears to be in the authentication middleware around line 45 of auth.py. 
   The expected behavior is to show an error message and redirect to the login form."
```

### 3. Break Down Complex Tasks
```
❌ "Build a complete e-commerce platform"
✅ "Let's build the e-commerce platform incrementally:
   1. First, create the product catalog with basic CRUD operations
   2. Then, implement user authentication and profiles
   3. Next, add shopping cart functionality
   4. Finally, integrate payment processing
   Start with just the product model and API endpoints."
```

## 📋 CLAUDE.md Optimization

### Essential Sections
Every CLAUDE.md should include these critical sections:

#### 1. Project Context
```markdown
## Project Overview
This is a FastAPI-based microservice that handles user authentication and authorization 
for our e-commerce platform. It serves 10M+ requests/day and must maintain 99.9% uptime.

## Architecture
- **Framework**: FastAPI with async/await
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Cache**: Redis for session storage
- **Authentication**: JWT tokens with refresh mechanism
- **Deployment**: Docker containers on Kubernetes
```

#### 2. Critical Rules (Non-Negotiable)
```markdown
## Critical Rules - NEVER VIOLATE
- NEVER log user passwords or sensitive data
- NEVER commit API keys or secrets to version control
- NEVER skip database migrations in production deployments
- ALWAYS use parameterized queries to prevent SQL injection
- ALWAYS validate and sanitize user inputs
- ALWAYS include rate limiting for public APIs
- ALWAYS use HTTPS in production environments
```

#### 3. Development Patterns
```markdown
## Code Patterns
When creating new API endpoints:
```python
# ✅ Preferred pattern
@router.post("/users/", response_model=UserResponse)
async def create_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    try:
        result = await user_service.create_user(db, user)
        logger.info(f"User created: {result.id}")
        return result
    except UserExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
```
```

#### 4. Testing Requirements
```markdown
## Testing Standards
- **Unit Tests**: 90%+ code coverage required
- **Integration Tests**: All API endpoints must have tests
- **Mock External Services**: Use fixtures for database and API calls
- **Test Data**: Use factories, never hardcode test data
- **Performance Tests**: API endpoints must respond within 200ms

Example test structure:
```python
def test_create_user_success(test_db, user_factory):
    # Arrange
    user_data = user_factory.build()
    
    # Act
    response = client.post("/users/", json=user_data)
    
    # Assert
    assert response.status_code == 201
    assert response.json()["email"] == user_data["email"]
```
```

### Dynamic Context Loading
```markdown
## Context-Aware Instructions
When working in different directories:

### /src/models/
- Focus on database schema design
- Ensure proper relationships and indexes
- Include validation at the model level
- Add comprehensive docstrings

### /src/api/
- Implement proper error handling
- Include request/response validation
- Add rate limiting where appropriate
- Ensure consistent API patterns

### /tests/
- Write comprehensive test cases
- Use proper fixtures and factories
- Mock external dependencies
- Ensure tests are fast and deterministic
```

## ⚙️ Prompt Engineering Excellence

### 1. Context Stacking
Build context progressively:
```
Session Start:
"Analyze this FastAPI project structure and understand the authentication system."

After Context Established:
"Now let's add OAuth2 integration. Follow the existing patterns and security requirements."

During Implementation:
"Add comprehensive tests for the OAuth2 flow, including error cases and token refresh."
```

### 2. Thinking Modes for Complexity
Use escalating thinking prompts:
```
Simple Task: "Add a new API endpoint for user profiles"

Complex Task: "Think hard about implementing distributed caching across microservices"

Critical Decision: "Ultrathink about the database migration strategy for zero-downtime deployment"
```

### 3. Error-Driven Development
```
"Run the tests and analyze any failures. For each failing test:
1. Identify the root cause
2. Implement the minimal fix
3. Ensure the fix doesn't break other functionality
4. Add additional test cases if needed"
```

## 🔧 Settings.json Optimization

### Permission Strategy
Organize permissions by category:

```json
{
  "permissions": {
    "allow": [
      // Version Control (Essential)
      "Bash(git status)",
      "Bash(git add*)",
      "Bash(git commit*)",
      "Bash(git push*)",
      "Bash(git pull*)",
      
      // Development Tools (Framework Specific)
      "Bash(python -m pytest*)",
      "Bash(uvicorn*)",
      "Bash(black*)",
      "Bash(isort*)",
      "Bash(mypy*)",
      
      // Package Management (Controlled)
      "Bash(pip install*)",
      "Bash(poetry install)",
      "Bash(poetry add*)",
      
      // File Operations (Scoped)
      "Edit(src/**)",
      "Edit(tests/**)",
      "Edit(docs/**)",
      "Read(*.md)",
      "Read(*.json)",
      "Read(*.toml)",
      
      // Database (Development Only)
      "Bash(psql*)",
      "Bash(redis-cli*)",
      
      // Build and Deploy (Safe Commands)
      "Bash(docker build*)",
      "Bash(docker-compose up*)"
    ],
    "deny": [
      // Destructive Operations
      "Bash(rm -rf*)",
      "Bash(sudo*)",
      "Bash(*--force*)",
      
      // Security Sensitive
      "Edit(.env*)",
      "Edit(secrets/**)",
      "Read(.env*)",
      "Bash(curl*)",
      
      // Production Operations
      "Bash(*production*)",
      "Bash(*prod*)",
      "Bash(kubectl delete*)",
      
      // System Changes
      "Bash(pip uninstall*)",
      "Bash(npm uninstall*)"
    ]
  }
}
```

### Environment Variables Best Practices
```json
{
  "env": {
    // Claude Code Configuration
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "CLAUDE_CODE_MAX_OUTPUT_TOKENS": "8000",
    
    // Development Environment
    "PYTHONPATH": "./src",
    "PYTHON_VERSION": "3.11",
    "ENVIRONMENT": "development",
    
    // Tool Configuration
    "PYTEST_CURRENT_TEST": "1",
    "COVERAGE_THRESHOLD": "90",
    "BLACK_LINE_LENGTH": "88",
    
    // Framework Specific
    "FASTAPI_ENV": "development",
    "DATABASE_URL": "postgresql://localhost/myproject_dev",
    
    // Performance Tuning
    "ASYNC_WORKERS": "4",
    "MAX_CONNECTIONS": "100"
  }
}
```

## 🌐 MCP Server Best Practices

### 1. Database Server Configuration
```json
{
  "mcpServers": {
    "postgres-primary": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "POSTGRES_CONNECTION_STRING": "postgresql://user:pass@localhost:5432/myproject",
        "QUERY_TIMEOUT": "30000",
        "MAX_CONNECTIONS": "5"
      }
    },
    "postgres-readonly": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "POSTGRES_CONNECTION_STRING": "postgresql://readonly:pass@localhost:5432/myproject",
        "READ_ONLY": "true"
      }
    }
  }
}
```

### 2. Performance Optimization
```json
{
  "mcpServers": {
    "filesystem-optimized": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem"],
      "env": {
        "ALLOWED_DIRECTORIES": "./src,./tests,./docs",
        "MAX_FILE_SIZE": "1048576",
        "EXCLUDE_PATTERNS": "*.pyc,__pycache__,node_modules,.git"
      }
    }
  }
}
```

### 3. Security Configuration
```json
{
  "mcpServers": {
    "github-secure": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}",
        "ALLOWED_REPOS": "myorg/myproject,myorg/shared-libs",
        "READ_ONLY": "true"
      }
    }
  }
}
```

## 🚀 Workflow Optimization

### 1. Context Management
```bash
# Start each major task with context priming
/context-prime

# Use compact at natural breakpoints
/compact  # After completing a feature

# Clear context when switching contexts
/clear    # When moving to unrelated work
```

### 2. Development Rhythm
```
1. Morning Planning:
   - Review CLAUDE.md for project context
   - Use /context-prime to establish project understanding
   - Plan the day's work with /implement-task

2. Development Loop:
   - Write small, focused code changes
   - Use /check frequently for quality assurance
   - Commit often with /commit

3. Before Breaks:
   - Use /compact to summarize progress
   - Document any important decisions in external notes

4. End of Day:
   - Use /add-to-changelog for significant changes
   - Update project documentation
   - Prepare context for next session
```

### 3. Error Recovery Patterns
```
When Things Go Wrong:
1. Don't panic - use Ctrl+C to interrupt Claude
2. Use /clear to reset if conversation goes off-track
3. Provide specific error messages and context
4. Use "undo the last change" for quick reversions
5. Use Git for larger rollbacks: "git checkout HEAD~1 filename"
```

## 🧪 Testing Integration

### 1. Test-Driven Development with Claude
```
TDD Prompt Pattern:
"Let's implement user registration using TDD:
1. First, write a failing test for user registration validation
2. Implement the minimal code to make the test pass
3. Refactor while keeping tests green
4. Add edge case tests for invalid emails, duplicate users, etc."
```

### 2. Automated Quality Gates
```bash
# Pre-commit workflow
/check              # Run all quality checks
/clean              # Fix formatting issues
pytest --cov=80     # Ensure test coverage
/commit             # Create commit with checks passed
```

### 3. Test Organization
```python
# Preferred test structure
class TestUserRegistration:
    """Test user registration functionality."""
    
    def test_valid_registration_creates_user(self, db_session, user_factory):
        """Test that valid user data creates a new user."""
        # Arrange
        user_data = user_factory.build()
        
        # Act
        result = register_user(db_session, user_data)
        
        # Assert
        assert result.email == user_data.email
        assert result.id is not None
    
    def test_duplicate_email_raises_error(self, db_session, existing_user):
        """Test that registering with existing email raises error."""
        with pytest.raises(UserExistsError):
            register_user(db_session, {"email": existing_user.email})
```

## 📊 Performance Optimization

### 1. Claude Code Performance
```bash
# Monitor performance
claude stats

# Optimize token usage
claude config set max_output_tokens 4000  # Reduce if needed

# Use print mode for automation
claude -p "quick command"  # Faster for simple tasks
```

### 2. Configuration Performance
```json
{
  // Optimize for faster startup
  "cleanupPeriodDays": 7,        // Shorter cleanup period
  "maxConcurrentOperations": 2,  // Reduce if system is slow
  "timeoutSeconds": 15,          // Shorter timeout for faster feedback
  
  // Reduce telemetry in development
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "0"
  }
}
```

### 3. Smart Caching Strategies
```markdown
## Caching Instructions for Claude
- Cache database query results in Redis for 5 minutes
- Use HTTP ETags for API response caching
- Implement application-level caching for expensive computations
- Always include cache invalidation logic
- Monitor cache hit rates and adjust TTL accordingly
```

## 🤝 Team Collaboration

### 1. Shared Configuration Standards
```bash
# Team setup process
1. Clone project repository
2. Run: python ~/.awesome-claude-code/tools/setup.py --preset backend-team
3. Customize local settings only in .claude/settings.local.json
4. Never commit personal API keys or local paths
```

### 2. Code Review Integration
```
Code Review Prompt:
"Review this PR focusing on:
1. Security: Check for secrets, SQL injection, input validation
2. Performance: Look for N+1 queries, inefficient algorithms
3. Maintainability: Assess code complexity and documentation
4. Testing: Verify adequate test coverage and edge cases
5. Standards: Ensure adherence to team coding standards

Provide specific, actionable feedback with code examples."
```

### 3. Knowledge Sharing
```markdown
## Team Learning Pattern
Document successful prompts in team wiki:

### API Development
"Create a FastAPI endpoint for user management following our established patterns:
- Use dependency injection for database sessions
- Include proper error handling with custom exceptions
- Add comprehensive request/response validation
- Include rate limiting and authentication
- Write unit and integration tests"

### Bug Fixing
"Investigate and fix the authentication timeout issue:
1. Reproduce the problem with specific test cases
2. Analyze logs for error patterns
3. Identify root cause with systematic debugging
4. Implement fix with proper error handling
5. Add regression tests to prevent recurrence"
```

## 🔍 Debugging and Troubleshooting

### 1. Systematic Debugging
```
Debug Process:
1. "Reproduce the issue with a minimal test case"
2. "Add logging to trace the execution path"
3. "Use the debugger to inspect variable states"
4. "Identify the root cause systematically"
5. "Implement the fix with proper error handling"
6. "Add tests to prevent regression"
```

### 2. Log Analysis
```
Log Analysis Prompt:
"Analyze these error logs and identify patterns:
1. Group similar errors by type and frequency
2. Identify the most critical issues based on impact
3. Trace error origins through the call stack
4. Recommend immediate fixes and long-term improvements
5. Suggest monitoring improvements to catch issues earlier"
```

### 3. Performance Debugging
```
Performance Analysis:
"Profile this slow API endpoint:
1. Use cProfile to identify bottlenecks
2. Analyze database query performance with EXPLAIN
3. Check for N+1 query problems
4. Review memory usage patterns
5. Implement optimizations with benchmarks"
```

## 📈 Continuous Improvement

### 1. Metrics and Monitoring
Track these key metrics:
- **Development Velocity**: Story points completed per sprint
- **Code Quality**: Test coverage, static analysis scores
- **Bug Rate**: Bugs found in production vs. development
- **Review Efficiency**: Time from PR creation to merge
- **Claude Effectiveness**: Accepted suggestions vs. total suggestions

### 2. Regular Reviews
```
Weekly Review Questions:
1. Which Claude prompts were most effective this week?
2. What configuration changes improved productivity?
3. Which patterns should be added to CLAUDE.md?
4. What team standards need updating?
5. How can we better leverage Claude Code features?
```

### 3. Knowledge Evolution
```
Monthly Process:
1. Review and update CLAUDE.md files
2. Analyze successful prompt patterns
3. Update team presets based on learnings
4. Share improvements with the community
5. Plan experiments with new features
```

## 🎯 Success Patterns

### 1. High-Impact Workflows
These patterns consistently deliver value:
- **Context-First Development**: Always prime context before coding
- **Incremental Testing**: Write tests alongside implementation
- **Automated Quality**: Use /check and /clean religiously
- **Systematic Reviews**: Use /pr-review for comprehensive feedback
- **Documentation-Driven**: Update docs as you code

### 2. Team Adoption Strategy
```
Phase 1 (Week 1-2): Basic Setup
- Install awesome-claude-code templates
- Configure basic CLAUDE.md and settings
- Practice essential commands (/check, /commit, /clean)

Phase 2 (Week 3-4): Advanced Features
- Set up MCP servers for database access
- Create custom commands for common tasks
- Implement team-specific rules and patterns

Phase 3 (Month 2+): Optimization
- Fine-tune configurations based on usage
- Develop team-specific prompt libraries
- Contribute improvements back to community
```

### 3. Avoiding Common Pitfalls
```
❌ Don't:
- Start coding without establishing context
- Use vague prompts like "fix this"
- Ignore the /check command output
- Commit without running tests
- Skip updating documentation

✅ Do:
- Prime context at the start of each session
- Be specific about requirements and constraints
- Use quality checks before committing
- Write tests alongside implementation
- Keep CLAUDE.md updated with learnings
```

Remember: The best practices evolve with your team and projects. Start with these foundations and adapt based on what works for your specific context!