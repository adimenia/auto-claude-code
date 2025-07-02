# Containerize

Create Docker containers and orchestration configurations for development and production deployment.

## Usage:
`/project:containerize [--orchestration] [--environment]` or `/user:containerize [--orchestration]`

## Process:
1. **Application Analysis**: Analyze application structure and dependencies
2. **Dockerfile Creation**: Generate optimized multi-stage Dockerfiles
3. **Docker Compose Setup**: Create development and testing environments
4. **Health Check Implementation**: Add container health monitoring
5. **Security Hardening**: Apply container security best practices
6. **Orchestration Config**: Generate Kubernetes/Docker Swarm configurations
7. **Volume Management**: Configure persistent storage and data volumes
8. **Testing & Validation**: Verify container functionality and performance

## Container Strategies:
- **Multi-stage Builds**: Separate build and runtime environments
- **Minimal Base Images**: Use Alpine or distroless images for security
- **Layer Optimization**: Minimize layers and image size
- **Security Scanning**: Integrate vulnerability scanning
- **Health Checks**: Implement proper health monitoring

## Framework-Specific Containers:
- **FastAPI**: Uvicorn server, async optimization, API health endpoints
- **Django**: WSGI/ASGI server, static files, database connections, migrations
- **Flask**: WSGI server, application factory, blueprint discovery
- **Data Science**: Jupyter notebooks, GPU support, data volume mounting
- **CLI Tools**: Entry point scripts, configuration mounting, cross-platform builds

## Arguments:
- `--orchestration`: Target orchestration (docker-compose, kubernetes, swarm)
- `--environment`: Environment type (development, staging, production)
- `--registry`: Container registry (dockerhub, gcr, ecr, acr)
- `--security`: Security features (non-root, secrets, scanning)

## Examples:
- `/project:containerize` - Basic Docker setup with compose
- `/project:containerize --orchestration kubernetes` - Full Kubernetes deployment
- `/project:containerize --environment production --security` - Production-ready secure container
- `/user:containerize --registry gcr` - Google Container Registry configuration

## Generated Configurations:

### Dockerfile (Multi-stage):
```dockerfile
# Build stage
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.11-slim
RUN adduser --disabled-password --gecos '' appuser
WORKDIR /app
COPY --from=builder /root/.local /home/appuser/.local
COPY . .
RUN chown -R appuser:appuser /app
USER appuser
ENV PATH=/home/appuser/.local/bin:$PATH
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1
CMD ["python", "-m", "app"]
```

### Docker Compose:
```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/dbname
    depends_on:
      db:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: dbname
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d dbname"]
      interval: 10s
      timeout: 5s
      retries: 5
volumes:
  postgres_data:
```

### Kubernetes Deployment:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: app
        image: myapp:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: database-url
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

## Security Best Practices:
- **Non-root user**: Run applications as non-privileged user
- **Minimal packages**: Only install necessary dependencies
- **Security scanning**: Regular vulnerability assessment
- **Secrets management**: Use orchestration secrets, not environment variables
- **Network policies**: Restrict container network access
- **Read-only filesystem**: Mount application as read-only where possible

## Validation Checklist:
- [ ] Container builds successfully without errors
- [ ] Application runs correctly in container environment
- [ ] Health checks function properly
- [ ] Container security scan passes
- [ ] Multi-environment setup (dev/staging/prod) working
- [ ] Persistent data volumes configured correctly
- [ ] Orchestration deployment successful
- [ ] Container logs accessible and meaningful

## Output:
- Optimized Dockerfile with multi-stage builds
- Docker Compose configuration for local development
- Kubernetes/orchestration deployment manifests
- Health check endpoints and monitoring configuration
- Container registry integration and CI/CD pipeline updates
- Security scanning setup and vulnerability reports
- Documentation for container operations and troubleshooting

## Notes:
- Always use specific image tags, avoid 'latest' in production
- Implement proper logging for container troubleshooting
- Consider init systems for multi-process containers
- Regular base image updates for security patches
- Monitor container resource usage and optimize accordingly
- Implement graceful shutdown handling for clean container stops