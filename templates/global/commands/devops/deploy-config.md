# Deploy Config

Generate deployment configurations and infrastructure setup for various cloud platforms and environments.

## Usage:
`/project:deploy-config [--platform] [--environment] [--strategy]` or `/user:deploy-config [--platform]`

## Process:
1. **Platform Analysis**: Identify target deployment platform and requirements
2. **Infrastructure Design**: Create infrastructure as code configurations
3. **Environment Setup**: Configure development, staging, and production environments
4. **Deployment Strategy**: Implement blue-green, rolling, or canary deployments
5. **Load Balancing**: Configure traffic distribution and health checks
6. **Monitoring Setup**: Add application performance monitoring and alerting
7. **Backup & Recovery**: Implement data backup and disaster recovery procedures
8. **Security Configuration**: Apply security best practices and compliance

## Supported Platforms:
- **AWS**: EC2, ECS, Lambda, Elastic Beanstalk, CloudFormation
- **Google Cloud**: Compute Engine, Cloud Run, App Engine, Deployment Manager
- **Azure**: App Service, Container Instances, ARM templates
- **DigitalOcean**: Droplets, App Platform, Kubernetes
- **Heroku**: Buildpacks, add-ons, pipeline configuration
- **Vercel/Netlify**: Serverless functions, edge deployment

## Framework-Specific Deployments:
- **FastAPI**: ASGI server configuration, API gateway setup, auto-scaling
- **Django**: WSGI deployment, static files serving, database migrations
- **Flask**: WSGI configuration, reverse proxy setup, session management
- **Data Science**: Jupyter Hub deployment, GPU instances, model serving
- **CLI Tools**: Package distribution, cross-platform binaries, update mechanisms

## Arguments:
- `--platform`: Target platform (aws, gcp, azure, digitalocean, heroku, vercel)
- `--environment`: Environment type (dev, staging, production, multi-region)
- `--strategy`: Deployment strategy (blue-green, rolling, canary, recreate)
- `--scaling`: Auto-scaling configuration (horizontal, vertical, serverless)

## Examples:
- `/project:deploy-config` - Auto-detect and create basic deployment
- `/project:deploy-config --platform aws --strategy blue-green` - AWS with blue-green deployment
- `/project:deploy-config --environment multi-region --scaling horizontal` - Multi-region with auto-scaling
- `/user:deploy-config --platform heroku` - Simple Heroku deployment setup

## Deployment Strategies:

### Blue-Green Deployment:
- **Benefits**: Zero downtime, easy rollback, production testing
- **Requirements**: Load balancer, duplicate infrastructure
- **Use Cases**: Critical applications, database schema changes

### Rolling Deployment:
- **Benefits**: Resource efficient, gradual rollout
- **Requirements**: Health checks, graceful shutdown
- **Use Cases**: Stateless applications, gradual updates

### Canary Deployment:
- **Benefits**: Risk mitigation, A/B testing, performance validation
- **Requirements**: Traffic splitting, monitoring, rollback automation
- **Use Cases**: High-risk changes, performance-sensitive applications

## Configuration Examples:

### AWS CloudFormation (FastAPI):
```yaml
AWSTemplateFormatVersion: '2010-09-09'
Resources:
  ECSCluster:
    Type: AWS::ECS::Cluster
    Properties:
      ClusterName: fastapi-cluster
  
  TaskDefinition:
    Type: AWS::ECS::TaskDefinition
    Properties:
      Family: fastapi-app
      Cpu: 256
      Memory: 512
      NetworkMode: awsvpc
      RequiresCompatibilities:
        - FARGATE
      ContainerDefinitions:
        - Name: fastapi
          Image: !Sub ${AWS::AccountId}.dkr.ecr.${AWS::Region}.amazonaws.com/fastapi-app:latest
          PortMappings:
            - ContainerPort: 8000
          HealthCheck:
            Command:
              - CMD-SHELL
              - curl -f http://localhost:8000/health || exit 1
```

### Google Cloud Run:
```yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: fastapi-service
  annotations:
    run.googleapis.com/ingress: all
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/maxScale: "100"
        run.googleapis.com/cpu-throttling: "false"
    spec:
      containers:
      - image: gcr.io/PROJECT_ID/fastapi-app
        ports:
        - name: http1
          containerPort: 8000
        resources:
          limits:
            cpu: 1000m
            memory: 512Mi
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
```

### Docker Compose (Production):
```yaml
version: '3.8'
services:
  app:
    image: myapp:${APP_VERSION}
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
        order: start-first
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
    networks:
      - app-network
    environment:
      - DATABASE_URL_FILE=/run/secrets/db_url
    secrets:
      - db_url
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - app
    networks:
      - app-network

networks:
  app-network:
    driver: overlay

secrets:
  db_url:
    external: true
```

## Infrastructure Components:
- **Load Balancers**: Traffic distribution, SSL termination, health checks
- **Auto Scaling**: Horizontal pod/instance scaling based on metrics
- **Databases**: Managed database services, connection pooling, backups
- **Storage**: Object storage, persistent volumes, CDN integration
- **Monitoring**: APM, logging aggregation, alerting systems
- **Security**: WAF, VPC, security groups, secrets management

## Validation Checklist:
- [ ] Deployment scripts execute successfully
- [ ] Application accessible through load balancer
- [ ] Health checks functioning correctly
- [ ] Auto-scaling triggers working as expected
- [ ] Database connections and migrations successful
- [ ] SSL certificates installed and functional
- [ ] Monitoring and alerting operational
- [ ] Backup and recovery procedures tested
- [ ] Security configurations validated
- [ ] Performance benchmarks met

## Output:
- Infrastructure as Code templates (CloudFormation, Terraform, ARM)
- Deployment scripts and automation workflows
- Environment-specific configuration files
- Load balancer and reverse proxy configurations
- Monitoring and alerting setup instructions
- Security policy and compliance documentation
- Disaster recovery and backup procedures
- Cost optimization recommendations

## Notes:
- Always test deployments in staging environment first
- Implement proper rollback procedures for failed deployments
- Monitor resource usage and costs regularly
- Keep infrastructure configurations in version control
- Use managed services where possible to reduce operational overhead
- Implement proper secret management and rotation policies
- Regular security audits and compliance checks
- Document emergency procedures and contact information