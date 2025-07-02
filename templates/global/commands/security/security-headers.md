# Security Headers

Configure and validate HTTP security headers and protective policies for web applications.

## Usage:
`/project:security-headers [--framework] [--level]` or `/user:security-headers [--validate-only]`

## Process:
1. **Current Headers Analysis**: Scan existing security header configuration
2. **Framework Detection**: Identify web framework and server setup
3. **Security Policy Design**: Define appropriate security policies for the application
4. **Header Configuration**: Generate framework-specific security header setup
5. **CSP Policy Creation**: Create Content Security Policy based on application needs
6. **HTTPS Configuration**: Ensure proper HTTPS and HSTS setup
7. **Validation Testing**: Test headers with security testing tools
8. **Monitoring Setup**: Configure ongoing header compliance monitoring

## Security Headers Configured:
- **Content-Security-Policy**: Prevent XSS and code injection attacks
- **Strict-Transport-Security**: Enforce HTTPS connections
- **X-Frame-Options**: Prevent clickjacking attacks
- **X-Content-Type-Options**: Prevent MIME-type confusion attacks
- **Referrer-Policy**: Control referrer information sharing
- **Permissions-Policy**: Control browser feature access
- **Cross-Origin-Embedder-Policy**: Enable cross-origin isolation
- **Cross-Origin-Opener-Policy**: Prevent cross-origin attacks

## Framework-Specific Implementation:
- **FastAPI**: Middleware configuration, security dependencies
- **Django**: Settings configuration, middleware setup, security middleware
- **Flask**: Extension setup (Flask-Talisman), application configuration
- **Static Sites**: Server configuration (Nginx, Apache), CDN settings

## Arguments:
- `--framework`: Specific framework (fastapi, django, flask, nginx, apache)
- `--level`: Security level (basic, standard, strict, paranoid)
- `--validate-only`: Only check existing headers without making changes
- `--csp-report`: Generate CSP report-only policy for testing

## Examples:
- `/project:security-headers` - Auto-detect and configure security headers
- `/project:security-headers --framework fastapi --level strict` - Strict FastAPI setup
- `/project:security-headers --validate-only` - Check current header configuration
- `/user:security-headers --csp-report` - Generate CSP testing policy

## Security Levels:
### Basic Level:
- HTTPS redirect, basic CSP, X-Frame-Options
- Suitable for simple applications with minimal third-party content

### Standard Level (Recommended):
- Comprehensive header set, moderate CSP, HSTS
- Balanced security for most web applications

### Strict Level:
- Restrictive CSP, strict referrer policy, advanced headers
- High-security applications, financial services

### Paranoid Level:
- Maximum security restrictions, minimal third-party content
- Government, healthcare, high-value target applications

## Configuration Examples:

### FastAPI:
```python
from fastapi.middleware.security import SecurityHeadersMiddleware

app.add_middleware(
    SecurityHeadersMiddleware,
    content_security_policy="default-src 'self'",
    strict_transport_security="max-age=31536000; includeSubDomains",
    x_frame_options="DENY"
)
```

### Django:
```python
# settings.py
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_HSTS_SECONDS = 31536000
CSP_DEFAULT_SRC = ("'self'",)
```

## Validation Checklist:
- [ ] All critical security headers implemented
- [ ] CSP policy tested and doesn't break functionality
- [ ] HTTPS properly configured with HSTS
- [ ] Headers validated with security testing tools
- [ ] Framework-specific best practices applied
- [ ] Monitoring configured for header compliance
- [ ] Documentation updated with security requirements

## Testing Tools:
- **Online Scanners**: Mozilla Observatory, Security Headers, SSL Labs
- **CLI Tools**: testssl.sh, nmap, curl header analysis
- **Browser Extensions**: Security header analyzers
- **Automated Testing**: Integration with CI/CD security testing

## Output:
- Current security header analysis report
- Framework-specific configuration code
- Security policy recommendations
- Implementation checklist
- Monitoring and compliance setup instructions

## Notes:
- Test CSP policies thoroughly before implementing in production
- Start with report-only mode for CSP to identify issues
- Regular review and updates as application evolves
- Consider using security header services for complex deployments
- Monitor for browser compatibility with new security features