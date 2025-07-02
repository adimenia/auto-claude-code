# Security Audit

Perform comprehensive security vulnerability assessment and penetration testing analysis.

## Usage:
`/project:security-audit [--severity-level] [--scope]` or `/user:security-audit [--severity-level]`

## Process:
1. **Static Code Analysis**: Scan for common vulnerabilities (OWASP Top 10)
2. **Dependency Vulnerability Scan**: Check for known CVEs in dependencies
3. **Secrets Detection**: Find exposed API keys, passwords, and credentials
4. **Authentication Analysis**: Review auth mechanisms and session management
5. **Input Validation Check**: Analyze user input handling and sanitization
6. **Configuration Security**: Review security headers, HTTPS, and server config
7. **Database Security**: Check for SQL injection risks and data exposure
8. **Generate Security Report**: Create detailed findings with remediation steps

## Framework-Specific Checks:
- **FastAPI**: JWT security, dependency injection vulnerabilities, CORS configuration
- **Django**: CSRF protection, session security, admin interface security, SQL injection
- **Flask**: Session management, template injection, request validation
- **Data Science**: Data privacy, model security, notebook credential exposure

## Arguments:
- `--severity-level`: Filter by severity (critical, high, medium, low, info)
- `--scope`: Target scope (authentication, input-validation, dependencies, all)
- `--fix-mode`: Generate automated fix suggestions where possible
- `--compliance`: Check against specific standards (OWASP, SOC2, GDPR)

## Examples:
- `/project:security-audit` - Full security assessment
- `/project:security-audit --severity-level critical` - Critical vulnerabilities only
- `/project:security-audit --scope authentication` - Auth-focused scan
- `/user:security-audit --compliance OWASP` - OWASP Top 10 compliance check

## Security Tools Integration:
- **Python**: bandit, safety, semgrep, pip-audit
- **JavaScript**: npm audit, snyk, eslint-plugin-security
- **Secrets**: truffleHog, git-secrets, detect-secrets
- **Static Analysis**: CodeQL, SonarQube integration

## Validation Checklist:
- [ ] All critical and high severity issues identified
- [ ] No exposed secrets or credentials found
- [ ] Authentication mechanisms properly secured
- [ ] Input validation comprehensive and effective
- [ ] Security headers and HTTPS properly configured
- [ ] Dependencies free from known vulnerabilities
- [ ] Compliance requirements met
- [ ] Remediation steps provided for all findings

## Output:
- Executive summary with risk assessment
- Detailed vulnerability findings with CVSS scores
- Prioritized remediation roadmap
- Code snippets showing vulnerable patterns
- Automated fix suggestions where applicable

## Notes:
- Run before every major release
- Integrate with CI/CD pipeline as security gate
- Schedule regular automated scans
- Consider penetration testing for production systems
- Keep security tools and databases updated