# Personas Info Command

## Command Overview
Get detailed information about a specific persona, including focus areas, responsibilities, and specializations.

## Usage
```
/personas:info <persona_name>
```

## Parameters
- `<persona_name>`: Name or type of persona to get information about
  - Supported: `data-scientist`, `developer`, `security-engineer`, `devops-engineer`, `architect`, `performance-engineer`, `product-manager`, `integration-specialist`, `tester`
  - Can use full names: `Data Scientist`, `Security Engineer`, etc.

## Implementation

### Python Implementation
```python
from src.persona_system import persona_manager, command_handler

# Get detailed persona information
persona_name = "data-scientist"
result = command_handler.handle_info_command(persona_name)
print(result)
```

## Expected Output

### Data Scientist Persona Info
```
# Data Scientist Persona
**Description:** ML models, data quality, and statistical rigor

## Focus Areas:
• Data Quality & Integrity
• Statistical Rigor
• Model Performance
• Reproducibility
• Feature Engineering
• Ethical AI & Bias
• Experiment Design
• Model Interpretability

## Key Responsibilities:
• Data validation, cleaning, and bias detection
• Hypothesis testing, significance analysis, and methodology
• Model evaluation, validation, and performance metrics
• Experiment tracking, version control, and documentation
• Feature selection, transformation, and domain knowledge

## Command Specializations:
• data-exploration
• model-development
• experiment-tracking
• data-pipeline

## Activation Triggers:
• data
• ml
• model
• statistics
• experiment
```

### Security Engineer Persona Info
```
# Security Engineer Persona
**Description:** Vulnerability assessment, security auditing, and compliance

## Focus Areas:
• Vulnerability Assessment
• Authentication & Authorization
• Data Protection
• Input Validation
• Security Configuration
• Dependency Security
• Secrets Management
• Compliance

## Key Responsibilities:
• Security threat analysis and OWASP compliance
• Secure access control implementation
• Encryption, data privacy, and secure storage
• SQL injection, XSS, and input sanitization
• Secure headers, HTTPS, and security policies

## Command Specializations:
• security-audit
• secrets-scan
• security-headers

## Activation Triggers:
• security
• vulnerability
• auth
• compliance
```

### DevOps Engineer Persona Info
```
# DevOps Engineer Persona
**Description:** CI/CD, deployment, infrastructure, and monitoring

## Focus Areas:
• Deployment Strategy
• Infrastructure as Code
• Containerization
• Monitoring & Logging
• Scalability
• Environment Configuration
• Backup & Recovery

## Key Responsibilities:
• CI/CD pipeline design and automation
• Terraform, CloudFormation, and configuration management
• Docker, Kubernetes, and orchestration
• Application monitoring, alerting, and observability
• Auto-scaling, load balancing, and performance optimization

## Command Specializations:
• setup-ci
• containerize
• deploy-config

## Activation Triggers:
• deployment
• ci/cd
• docker
• kubernetes
• monitoring
```

### Invalid Persona
```
Persona 'invalid-persona' not found.
```

## Features
- **Comprehensive Information**: Complete persona profile
- **Focus Areas**: All areas of expertise
- **Detailed Responsibilities**: Key tasks and areas of focus
- **Command Specializations**: Commands this persona excels at
- **Activation Triggers**: Keywords that suggest this persona
- **Formatted Output**: Well-structured markdown format

## Use Cases

### Persona Selection
Use this command to:
- Understand what each persona specializes in
- Choose the right persona for your current task
- Learn about persona capabilities before activation
- Compare different personas for complex tasks

### Learning and Reference
- Study expertise areas of different personas
- Understand the scope of each specialization
- Reference command specializations
- Learn about activation triggers

## Integration with Other Commands

### Workflow Example
```bash
# Learn about data science persona
/personas:info data-scientist

# Activate it for ML work
/personas:activate data-scientist

# Check current status
/personas:list

# Get suggestions for different context
/personas:suggest "api development"

# Learn about suggested persona
/personas:info integration-specialist
```

## All Available Personas

### Technical Specialists
- **Data Scientist**: ML, statistics, data quality
- **Security Engineer**: Vulnerabilities, compliance, auditing
- **Performance Engineer**: Optimization, load testing, scalability
- **DevOps Engineer**: CI/CD, infrastructure, monitoring
- **Integration Specialist**: APIs, services, data flow

### Development Roles
- **Architect**: System design, scalability, architecture
- **Developer**: Code quality, patterns, best practices
- **Tester**: Testing strategies, QA, validation
- **Product Manager**: UX, business logic, requirements

## Related Commands
- `/personas:list` - See all available personas
- `/personas:activate <persona>` - Activate a specific persona
- `/personas:deactivate` - Deactivate current persona
- `/personas:suggest <context>` - Get persona suggestions for context

## Best Practices
1. **Research Before Activation**: Use info command to understand persona capabilities
2. **Compare Personas**: Check multiple personas for complex tasks
3. **Understand Specializations**: Review command specializations before choosing
4. **Learn Triggers**: Understand what contexts activate each persona
5. **Reference Guide**: Use as quick reference for persona capabilities