# Setup CI

Generate comprehensive CI/CD pipeline configurations for automated testing, building, and deployment.

## Usage:
`/project:setup-ci [--platform] [--features]` or `/user:setup-ci [--platform]`

## Process:
1. **Platform Detection**: Identify target CI/CD platform and project structure
2. **Pipeline Design**: Create multi-stage pipeline (test, build, security, deploy)
3. **Environment Configuration**: Set up environment variables and secrets management
4. **Testing Strategy**: Configure unit tests, integration tests, and quality gates
5. **Security Integration**: Add security scanning and vulnerability checks
6. **Deployment Stages**: Configure staging and production deployment workflows
7. **Monitoring Setup**: Add pipeline monitoring and notification systems
8. **Documentation**: Generate pipeline documentation and troubleshooting guides

## Supported Platforms:
- **GitHub Actions**: Workflow files, marketplace actions, matrix builds
- **GitLab CI**: Pipeline configuration, runners, environments, pages
- **Azure DevOps**: Pipeline YAML, build agents, release pipelines
- **Jenkins**: Jenkinsfile, pipeline stages, plugins configuration
- **CircleCI**: Config YAML, orbs, workflows, contexts

## Framework-Specific Pipelines:
- **FastAPI**: API testing, OpenAPI validation, container builds, health checks
- **Django**: Database migrations, static files, multi-environment testing
- **Flask**: App factory testing, blueprint validation, WSGI deployment
- **Data Science**: Model validation, data pipeline testing, notebook execution
- **CLI Tools**: Cross-platform testing, binary building, package distribution

## Arguments:
- `--platform`: Target platform (github, gitlab, azure, jenkins, circleci)
- `--features`: Specific features (docker, kubernetes, security, monitoring)
- `--environments`: Target environments (staging, production, preview)
- `--matrix`: Enable matrix builds for multiple versions/platforms

## Examples:
- `/project:setup-ci` - Auto-detect and create basic CI pipeline
- `/project:setup-ci --platform github --features docker,security` - GitHub with Docker and security
- `/project:setup-ci --matrix python3.9,python3.10,python3.11` - Multi-version testing
- `/user:setup-ci --platform gitlab --environments staging,prod` - GitLab with multiple environments

## Pipeline Stages:

### Basic Pipeline:
1. **Checkout**: Code checkout and dependency caching
2. **Test**: Unit tests, integration tests, coverage reporting
3. **Quality**: Linting, type checking, security scanning
4. **Build**: Application building, asset compilation
5. **Deploy**: Staging deployment, production deployment

### Advanced Pipeline:
1. **Pre-flight**: Dependency vulnerability scan, license check
2. **Parallel Testing**: Multi-environment test matrix
3. **Security Gate**: SAST, DAST, container scanning
4. **Performance**: Load testing, performance regression
5. **Approval Gates**: Manual approvals for production
6. **Blue-Green Deploy**: Zero-downtime deployment strategy
7. **Post-deployment**: Health checks, rollback triggers

## Configuration Examples:

### GitHub Actions (FastAPI):
```yaml
name: FastAPI CI/CD
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.9, 3.10, 3.11]
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      - name: Run tests
        run: pytest --cov=app tests/
      - name: Security scan
        run: bandit -r app/
```

### GitLab CI (Django):
```yaml
stages:
  - test
  - security
  - build
  - deploy

test:
  stage: test
  script:
    - python manage.py test
    - coverage run --source='.' manage.py test
    - coverage report
  coverage: '/TOTAL.+ ([0-9]{1,3}%)/'
```

## Validation Checklist:
- [ ] Pipeline runs successfully on sample commits
- [ ] All test stages execute and pass
- [ ] Security scanning integrated and functional
- [ ] Environment variables and secrets properly configured
- [ ] Deployment stages tested in staging environment
- [ ] Rollback procedures defined and tested
- [ ] Monitoring and alerting configured
- [ ] Documentation complete and accessible

## Output:
- Platform-specific CI/CD configuration files
- Environment variable templates and documentation
- Deployment scripts and health check configurations
- Pipeline monitoring and alerting setup
- Troubleshooting guide and best practices documentation

## Notes:
- Test pipeline thoroughly in feature branches before main
- Use secrets management for sensitive configuration
- Implement proper caching to speed up builds
- Consider pipeline security and least-privilege access
- Regular maintenance and updates of CI/CD dependencies
- Monitor pipeline performance and optimize bottlenecks