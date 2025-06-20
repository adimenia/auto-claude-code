# Check All

Perform comprehensive code quality, security, and performance checks.

## Usage:
`/project:check-all [--fix]` or `/user:check-all [--fix]`

## Process:
1. **Code Formatting**: Check and optionally fix code formatting issues
2. **Linting**: Run linters (flake8, pylint, eslint) and report issues
3. **Type Checking**: Run mypy, TypeScript, or equivalent type checkers
4. **Security Scan**: Check for security vulnerabilities and secrets
5. **Dependency Audit**: Check for outdated or vulnerable dependencies
6. **Test Coverage**: Analyze test coverage and identify gaps
7. **Performance Check**: Basic performance regression detection
8. **Documentation Check**: Verify documentation is up to date

## Framework-Specific Checks:
- **Python**: black, isort, flake8, mypy, bandit, safety
- **JavaScript/TypeScript**: prettier, eslint, typescript, npm audit
- **FastAPI**: OpenAPI spec validation, endpoint testing
- **Django**: migration check, security settings review
- **Data Science**: data validation, model performance metrics

## Arguments:
- `--fix`: Automatically fix issues where possible
- `--strict`: Use strict checking mode with zero tolerance
- `--report`: Generate detailed report file

## Examples:
- `/project:check-all` - Run all checks and report issues
- `/project:check-all --fix` - Run checks and auto-fix what's possible
- `/user:check-all --strict` - Run with strict validation

## Output:
- Summary of all checks performed
- List of issues found with severity levels
- Recommendations for fixes
- Optional: Generated report file

## Notes:
- This command should be run before every commit
- Use in CI/CD pipeline for automated quality gates
- Configure in pre-commit hooks for automatic validation
