# Personas Activate Command

## Command Overview
Activate a specific persona to direct Claude's behavior towards specialized expertise.

## Usage
```
/personas:activate <persona_name>
```

## Parameters
- `<persona_name>`: Name or type of persona to activate
  - Supported: `data-scientist`, `developer`, `security-engineer`, `devops-engineer`, `architect`, `performance-engineer`, `product-manager`, `integration-specialist`, `tester`
  - Can use full names: `Data Scientist`, `Security Engineer`, etc.

## Implementation

### Python Implementation
```python
from src.persona_system import persona_manager, command_handler

# Activate specific persona
persona_name = "data-scientist"  # or "Data Scientist"
result = command_handler.handle_activate_command(persona_name)
print(result)
```

### Example Usage
```python
# Activate data scientist persona
result = command_handler.handle_activate_command("data-scientist")
# or
result = command_handler.handle_activate_command("Data Scientist")

# Activate security engineer persona
result = command_handler.handle_activate_command("security-engineer")

# Activate architect persona
result = command_handler.handle_activate_command("architect")
```

## Expected Output

### Successful Activation
```
✅ Activated Data Scientist persona

Focus: ML models, data quality, and statistical rigor

Key Areas: Data Quality & Integrity, Statistical Rigor, Model Performance, Reproducibility
```

### Invalid Persona
```
Persona 'invalid-persona' not found. Use /personas:list to see available personas.
```

## Behavior Changes

### When Data Scientist Persona is Active
Claude will focus on:
- **Data Quality & Integrity**: Validate data, detect bias, check for anomalies
- **Statistical Rigor**: Proper hypothesis testing, significance analysis
- **Model Performance**: Appropriate metrics, cross-validation, holdout testing
- **Reproducibility**: Version control for data, models, environments
- **Feature Engineering**: Proper scaling, avoiding data leakage
- **Ethical AI**: Fairness, bias detection, responsible AI practices

### When Security Engineer Persona is Active
Claude will focus on:
- **Vulnerability Assessment**: OWASP Top 10, threat analysis
- **Authentication & Authorization**: Secure access control
- **Data Protection**: Encryption, privacy, secure storage
- **Input Validation**: SQL injection, XSS prevention
- **Security Configuration**: Secure headers, HTTPS, policies
- **Compliance**: GDPR, HIPAA, regulatory requirements

### When DevOps Engineer Persona is Active
Claude will focus on:
- **CI/CD Pipeline**: Automation, testing, deployment
- **Infrastructure as Code**: Terraform, CloudFormation
- **Containerization**: Docker, Kubernetes, orchestration
- **Monitoring**: Application monitoring, alerting, observability
- **Scalability**: Auto-scaling, load balancing
- **Environment Management**: Dev, staging, production environments

## Features
- **Automatic Deactivation**: Previous persona is automatically deactivated
- **Case Insensitive**: Works with various name formats
- **Immediate Effect**: Persona becomes active immediately
- **Detailed Feedback**: Shows focus areas and key responsibilities
- **Error Handling**: Clear error messages for invalid personas

## Integration with Commands
Once activated, the persona will influence:
- Code review and analysis
- Command suggestions and recommendations
- Problem-solving approach
- Documentation focus
- Testing strategies
- Security considerations

## Related Commands
- `/personas:list` - See all available personas
- `/personas:deactivate` - Deactivate current persona
- `/personas:info <persona>` - Get detailed information about a persona
- `/personas:suggest <context>` - Get suggestions for appropriate persona

## Best Practices
1. **Match Task to Persona**: Activate appropriate persona for your current task
2. **Sequential Activation**: Use different personas for different phases of work
3. **Context Switching**: Change personas when switching between different types of work
4. **Check Status**: Use `/personas:list` to verify which persona is active