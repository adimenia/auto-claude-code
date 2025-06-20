# Create Feature

Create a complete feature with tests, documentation, and proper integration.

## Usage:
`/project:create-feature [feature-name]`

## Process:
1. **Analyze Requirements**: Break down the feature requirements from $ARGUMENTS
2. **Plan Architecture**: Create component structure and data flow diagram
3. **Implement Core Logic**: Write the main feature implementation
4. **Add Error Handling**: Include comprehensive error handling and validation
5. **Write Tests**: Create unit tests, integration tests, and end-to-end tests
6. **Update Documentation**: Add feature documentation and update API docs
7. **Integration Check**: Ensure proper integration with existing codebase

## Framework-Specific Actions:
- **FastAPI**: Create routes, Pydantic models, OpenAPI docs, dependency injection
- **Django**: Create views, models, serializers, URL patterns, admin interface
- **Flask**: Create blueprints, forms, templates, add to app factory
- **Data Science**: Create analysis pipeline, data validation, model artifacts

## Examples:
- `/project:create-feature user-authentication`
- `/project:create-feature data-export-pipeline`
- `/project:create-feature real-time-notifications`

## Validation Checklist:
- [ ] Feature works as specified
- [ ] Tests pass with >80% coverage
- [ ] Documentation is updated
- [ ] No breaking changes to existing API
- [ ] Performance impact is acceptable
- [ ] Security considerations addressed

## Notes:
- Always run existing tests after implementation
- Follow project's coding standards from CLAUDE.md
- Consider backwards compatibility
- Add appropriate logging and monitoring