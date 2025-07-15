# Personas List Command

## Command Overview
Display all available personas with their current status and capabilities.

## Usage
```
/personas:list
```

## Implementation

### Python Implementation
```python
from src.persona_system import persona_manager, command_handler

# Execute the personas list command
result = command_handler.handle_list_command()
print(result)
```

### Expected Output
```
Available Personas:

🟢 ACTIVE Data Scientist
   Type: data-scientist
   Description: ML models, data quality, and statistical rigor
   Specializations: data-exploration, model-development, experiment-tracking

⚪ Available Developer
   Type: developer
   Description: Code quality, patterns, and implementation best practices
   Specializations: create-feature, integration-test, check-all

⚪ Available Security Engineer
   Type: security-engineer
   Description: Vulnerability assessment, security auditing, and compliance
   Specializations: security-audit, secrets-scan, security-headers

⚪ Available DevOps Engineer
   Type: devops-engineer
   Description: CI/CD, deployment, infrastructure, and monitoring
   Specializations: setup-ci, containerize, deploy-config

⚪ Available Architect
   Type: architect
   Description: System design, scalability, and technical architecture
   Specializations: api-design, performance-audit, containerize

⚪ Available Performance Engineer
   Type: performance-engineer
   Description: Optimization, load testing, and scalability
   Specializations: performance-audit, load-test

⚪ Available Product Manager
   Type: product-manager
   Description: UX, business logic, and feature completeness
   Specializations: analyze-requirements, create-docs

⚪ Available Integration Specialist
   Type: integration-specialist
   Description: API design, service integration, and data flow
   Specializations: api-design, integration-test, data-migration

⚪ Available Tester
   Type: tester
   Description: Testing strategies, quality assurance, and validation
   Specializations: integration-test, load-test, check-all

Currently Active: Data Scientist
```

## Features
- **Status Indicators**: Shows active vs available personas
- **Type Information**: Displays persona type identifier
- **Quick Description**: Brief summary of persona focus
- **Specializations**: Key commands each persona specializes in
- **Active Status**: Shows which persona is currently active

## Integration Notes
- Integrates with existing persona management system
- No external dependencies required
- Command can be called at any time
- Provides foundation for other persona commands

## Related Commands
- `/personas:activate <persona>` - Activate a specific persona
- `/personas:deactivate` - Deactivate current persona
- `/personas:info <persona>` - Get detailed persona information
- `/personas:suggest <context>` - Get persona suggestions for context