# Personas Suggest Command

## Command Overview
Get persona suggestions based on context, keywords, or current work focus.

## Usage
```
/personas:suggest <context>
```

## Parameters
- `<context>`: Description of current work, keywords, or problem domain
  - Examples: "api development", "machine learning", "security review", "performance optimization"

## Implementation

### Python Implementation
```python
from src.persona_system import persona_manager, command_handler

# Get persona suggestions for context
context = "api development"
result = command_handler.handle_suggest_command(context)
print(result)
```

## Expected Output

### API Development Context
```
Suggested personas for 'api development':

• Integration Specialist - API design, service integration, and data flow
• Architect - System design, scalability, and technical architecture
• Security Engineer - Vulnerability assessment, security auditing, and compliance
```

### Machine Learning Context
```
Suggested personas for 'machine learning':

• Data Scientist - ML models, data quality, and statistical rigor
• Performance Engineer - Optimization, load testing, and scalability
```

### Security Review Context
```
Suggested personas for 'security review':

• Security Engineer - Vulnerability assessment, security auditing, and compliance
• DevOps Engineer - CI/CD, deployment, infrastructure, and monitoring
```

### Performance Optimization Context
```
Suggested personas for 'performance optimization':

• Performance Engineer - Optimization, load testing, and scalability
• Architect - System design, scalability, and technical architecture
```

### No Suggestions Found
```
No persona suggestions found for context: 'unusual-context'
```

## Context Keywords and Triggers

### Data Science Keywords
- `data`, `ml`, `machine learning`, `model`, `statistics`, `experiment`, `analytics`
- **Suggested Persona**: Data Scientist

### Security Keywords
- `security`, `vulnerability`, `auth`, `authentication`, `compliance`, `encryption`
- **Suggested Persona**: Security Engineer

### DevOps Keywords
- `deployment`, `ci/cd`, `docker`, `kubernetes`, `monitoring`, `infrastructure`
- **Suggested Persona**: DevOps Engineer

### Performance Keywords
- `performance`, `optimization`, `load`, `scaling`, `bottleneck`, `latency`
- **Suggested Persona**: Performance Engineer

### API/Integration Keywords
- `api`, `integration`, `services`, `microservices`, `endpoints`, `rest`
- **Suggested Persona**: Integration Specialist

### Architecture Keywords
- `architecture`, `design`, `scalability`, `system`, `patterns`
- **Suggested Persona**: Architect

### Development Keywords
- `code`, `development`, `testing`, `patterns`, `refactoring`
- **Suggested Persona**: Developer

### Testing Keywords
- `test`, `testing`, `quality`, `qa`, `validation`, `coverage`
- **Suggested Persona**: Tester

### Product Keywords
- `ux`, `business`, `user`, `requirements`, `features`
- **Suggested Persona**: Product Manager

## Use Cases

### Task Planning
```bash
# Starting new project
/personas:suggest "building a web application with user authentication"
# Result: Security Engineer, Integration Specialist, Developer

# Data analysis task
/personas:suggest "analyzing customer behavior data"
# Result: Data Scientist

# Performance issues
/personas:suggest "application is slow and needs optimization"
# Result: Performance Engineer, Architect
```

### Context Switching
```bash
# Currently working on ML models
/personas:suggest "deploying machine learning model to production"
# Result: DevOps Engineer, Data Scientist

# Moving from development to security
/personas:suggest "security audit and vulnerability assessment"
# Result: Security Engineer
```

### Multi-Persona Tasks
```bash
# Complex system design
/personas:suggest "designing scalable microservices architecture"
# Result: Architect, Integration Specialist, Performance Engineer

# Full application development
/personas:suggest "building secure e-commerce platform"
# Result: Security Engineer, Developer, Integration Specialist, Product Manager
```

## Advanced Usage

### Combining Suggestions with Info
```bash
# Get suggestions
/personas:suggest "api security"

# Learn about suggested personas
/personas:info security-engineer
/personas:info integration-specialist

# Activate the most appropriate one
/personas:activate security-engineer
```

### Sequential Persona Usage
```bash
# Planning phase
/personas:suggest "system architecture planning"
/personas:activate architect

# Development phase
/personas:suggest "implementing the system"
/personas:activate developer

# Security review phase
/personas:suggest "security review"
/personas:activate security-engineer
```

## Features
- **Context-Aware**: Analyzes keywords and context
- **Multiple Suggestions**: Can suggest multiple relevant personas
- **Ranked Results**: Most relevant personas listed first
- **Descriptive Output**: Shows persona description with suggestion
- **Flexible Input**: Works with various context formats

## Integration Notes
- Works with natural language descriptions
- Supports technical terms and keywords
- Case-insensitive matching
- No external dependencies
- Integrates with persona activation workflow

## Related Commands
- `/personas:list` - See all available personas
- `/personas:activate <persona>` - Activate a suggested persona
- `/personas:info <persona>` - Get detailed information about suggested persona
- `/personas:deactivate` - Deactivate current persona

## Best Practices
1. **Descriptive Context**: Use specific, descriptive context for better suggestions
2. **Multiple Keywords**: Include relevant keywords in your context
3. **Follow Up**: Use `/personas:info` to learn about suggested personas
4. **Context Evolution**: Use suggest command as your work context changes
5. **Validation**: Verify suggestions match your actual needs before activation