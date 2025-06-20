# Create Documentation

Generate comprehensive documentation for features, APIs, or project components.

## Usage:
`/project:create-docs [component-name] [doc-type]`

## Process:
1. **Analyze Component**: Understand the component's purpose and functionality
2. **Identify Audience**: Determine who will read this documentation
3. **Choose Format**: Select appropriate documentation format and structure
4. **Extract Information**: Gather details from code, comments, and existing docs
5. **Generate Content**: Create clear, comprehensive documentation
6. **Add Examples**: Include practical examples and use cases
7. **Review & Polish**: Ensure clarity, accuracy, and completeness
8. **Update Index**: Add to project documentation index

## Documentation Types:
- **API**: Endpoint documentation with request/response examples
- **User Guide**: Step-by-step instructions for end users
- **Developer Guide**: Technical implementation details
- **Architecture**: System design and component relationships
- **Installation**: Setup and configuration instructions
- **Troubleshooting**: Common issues and solutions

## Framework-Specific Outputs:
- **FastAPI**: OpenAPI/Swagger documentation integration
- **Django**: Sphinx documentation with autodoc
- **Data Science**: Jupyter notebook documentation
- **CLI Tools**: Man pages and help text generation

## Documentation Structure:
```markdown
# [Component Name]

## Overview
Brief description and purpose

## Features
- Feature 1: Description
- Feature 2: Description

## Installation/Setup
Step-by-step setup instructions

## Usage
### Basic Usage
Simple examples to get started

### Advanced Usage
Complex scenarios and configurations

## API Reference (if applicable)
Detailed API documentation

## Examples
Practical examples and use cases

## Troubleshooting
Common issues and solutions

## Contributing
How to contribute to this component

## Changelog
Recent changes and updates
```

## Examples:
- `/project:create-docs authentication api`
- `/project:create-docs data-pipeline user-guide`
- `/project:create-docs payment-system architecture`

## Best Practices:
- Use clear, concise language
- Include code examples with explanations
- Add screenshots for UI components
- Maintain consistency with project style guide
- Test all code examples before publishing

## Notes:
- Documentation should be updated with every feature change
- Consider internationalization for user-facing documentation
- Use diagrams for complex system relationships
- Integrate with project's documentation build system
