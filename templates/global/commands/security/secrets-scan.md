# Secrets Scan

Detect and remediate exposed secrets, API keys, passwords, and sensitive data in codebase.

## Usage:
`/project:secrets-scan [--remediate] [--history]` or `/user:secrets-scan [--remediate]`

## Process:
1. **Pattern Detection**: Scan for common secret patterns (API keys, passwords, tokens)
2. **Git History Analysis**: Check commit history for accidentally committed secrets
3. **Configuration Files**: Review config files, environment files, and documentation
4. **Dependencies Scan**: Check third-party packages for exposed credentials
5. **False Positive Filtering**: Use entropy analysis and context to reduce noise
6. **Remediation Planning**: Generate steps to secure found secrets
7. **Prevention Setup**: Configure pre-commit hooks and secret scanning tools
8. **Monitoring Setup**: Establish ongoing secret detection monitoring

## Secret Types Detected:
- **API Keys**: AWS, Google Cloud, Azure, GitHub, Stripe, etc.
- **Database Credentials**: Connection strings, passwords
- **Encryption Keys**: Private keys, certificates, JWT secrets
- **Service Tokens**: OAuth tokens, webhook secrets
- **Cloud Credentials**: Service account keys, access tokens

## Framework-Specific Scanning:
- **FastAPI**: Environment variables, dependency configuration, JWT secrets
- **Django**: Settings files, database configuration, secret keys
- **Flask**: Config objects, session secrets, database URLs
- **Data Science**: Jupyter notebooks, data source credentials, model artifacts

## Arguments:
- `--remediate`: Automatically apply fixes where safe (environment variables, .gitignore)
- `--history`: Scan full Git history (can be time-consuming)
- `--exclude-patterns`: Custom patterns to exclude from scanning
- `--export-report`: Generate detailed report for security team

## Examples:
- `/project:secrets-scan` - Scan current codebase for secrets
- `/project:secrets-scan --history` - Include full Git history scan
- `/project:secrets-scan --remediate` - Auto-fix where possible
- `/user:secrets-scan --export-report` - Generate comprehensive security report

## Detection Tools:
- **Multi-language**: truffleHog, detect-secrets, GitLeaks
- **Git History**: git-secrets, repo-supervisor
- **Real-time**: pre-commit hooks, IDE plugins
- **Cloud Native**: AWS GuardDuty, Azure Security Center

## Remediation Actions:
1. **Immediate**: Remove secrets from code, rotate compromised credentials
2. **Configuration**: Move to environment variables or secrets management
3. **Git History**: Use git-filter-branch or BFG Repo-Cleaner for history cleanup
4. **Prevention**: Set up pre-commit hooks and CI/CD scanning
5. **Monitoring**: Configure alerting for future secret exposure

## Validation Checklist:
- [ ] No hardcoded secrets in source code
- [ ] All secrets moved to secure configuration management
- [ ] Git history cleaned of exposed credentials
- [ ] Pre-commit hooks configured to prevent future exposure
- [ ] Environment variable templates created (.env.example)
- [ ] Secrets rotation completed for any exposed credentials
- [ ] Team trained on secure secret management practices

## Output:
- List of detected secrets with severity and location
- Git commits containing exposed secrets
- Remediation instructions for each finding
- Pre-commit hook configuration
- Secrets management best practices guide

## Notes:
- **CRITICAL**: Rotate any exposed credentials immediately
- Never commit .env files with real secrets
- Use dedicated secrets management services (AWS Secrets Manager, HashiCorp Vault)
- Regular team training on secure development practices
- Consider using tools like GitHub secret scanning for continuous monitoring