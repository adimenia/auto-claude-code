# Persona System Reference

> Expert personas for specialized code review and development guidance

## 🎭 Overview

The auto-claude-code template system includes **9 expert personas** that provide specialized perspectives on code quality, security, performance, and development practices. Each persona focuses on specific aspects of software development and provides targeted analysis and recommendations.

## 👥 Available Personas

### 🏗️ Architect
**Focus**: System design, scalability, and technical architecture

**Responsibilities**:
- **System Design**: Overall architecture patterns and design decisions
- **Scalability Planning**: Horizontal and vertical scaling strategies  
- **Technology Selection**: Framework and tool recommendations
- **Integration Patterns**: Service communication and data flow design
- **Performance Architecture**: System-level performance considerations
- **Future-Proofing**: Extensibility and maintainability planning

**When to Use**: Initial project setup, major refactoring, system redesign, technology migration

### 👨‍💻 Developer  
**Focus**: Code quality, patterns, and implementation best practices

**Responsibilities**:
- **Code Quality**: Clean code principles and maintainability
- **Design Patterns**: Appropriate pattern usage and implementation
- **Testing Strategy**: Unit testing, TDD, and test coverage
- **Documentation**: Code documentation and API design
- **Refactoring**: Code improvement and technical debt reduction
- **Standards Compliance**: Coding standards and style guidelines

**When to Use**: Code reviews, implementation guidance, refactoring decisions, testing strategy

### 🧪 Tester
**Focus**: Testing strategies, quality assurance, and validation

**Responsibilities**:
- **Test Coverage**: Comprehensive testing strategy and coverage analysis
- **Quality Assurance**: Bug prevention and quality gates
- **Test Automation**: Automated testing frameworks and CI integration
- **Edge Case Testing**: Boundary conditions and error scenarios
- **Performance Testing**: Load testing and performance validation
- **User Acceptance**: End-to-end testing and user journey validation

**When to Use**: Test planning, QA strategy, test automation setup, quality gates

### 🔒 Security Engineer
**Focus**: Vulnerability assessment, security auditing, and compliance

**Responsibilities**:
- **Vulnerability Assessment**: Security threat analysis and OWASP compliance
- **Authentication & Authorization**: Secure access control implementation
- **Data Protection**: Encryption, data privacy, and secure storage
- **Input Validation**: SQL injection, XSS, and input sanitization
- **Security Configuration**: Secure headers, HTTPS, and security policies
- **Dependency Security**: Third-party library vulnerability scanning
- **Secrets Management**: Secure credential and API key handling
- **Compliance**: GDPR, HIPAA, and regulatory requirement adherence

**When to Use**: Security audits, vulnerability assessment, compliance review, secure architecture

### 🚀 DevOps Engineer  
**Focus**: CI/CD, deployment, infrastructure, and monitoring

**Responsibilities**:
- **Deployment Strategy**: CI/CD pipeline design and automation
- **Infrastructure as Code**: Terraform, CloudFormation, and configuration management
- **Containerization**: Docker, Kubernetes, and orchestration
- **Monitoring & Logging**: Application monitoring, alerting, and observability
- **Scalability**: Auto-scaling, load balancing, and performance optimization
- **Container Readiness**: Containerization best practices and security
- **Environment Configuration**: Development, staging, and production environments
- **Backup & Recovery**: Disaster recovery and business continuity planning

**When to Use**: Deployment planning, infrastructure design, CI/CD setup, monitoring strategy

### ⚡ Performance Engineer
**Focus**: Optimization, load testing, and scalability

**Responsibilities**:
- **Performance Bottlenecks**: Identification and resolution of performance issues
- **Resource Utilization**: CPU, memory, and I/O optimization
- **Database Optimization**: Query performance and indexing strategies
- **Caching Strategy**: Application and database caching implementation
- **Asynchronous Processing**: Background jobs and async operation design
- **Load Testing Readiness**: Performance testing and capacity planning
- **Scalability Patterns**: Horizontal scaling and performance architecture
- **Profiling Integration**: Performance monitoring and profiling tools

**When to Use**: Performance optimization, load testing, scalability planning, bottleneck analysis

### 📊 Product Manager
**Focus**: UX, business logic, and feature completeness

**Responsibilities**:
- **User Experience**: User journey optimization and usability
- **Feature Completeness**: Business requirement validation and feature gaps
- **Business Logic**: Requirement translation and business rule implementation
- **Error Handling UX**: User-friendly error messages and recovery flows
- **Accessibility**: WCAG compliance and inclusive design
- **Performance Impact**: User-perceived performance and experience optimization
- **Data Analytics**: User behavior tracking and analytics implementation
- **Edge Cases**: User scenario validation and edge case handling

**When to Use**: Feature development, UX review, business logic validation, user experience optimization

### 🔗 Integration Specialist
**Focus**: API design, service integration, and data flow

**Responsibilities**:
- **API Design**: RESTful API design and GraphQL implementation
- **Data Flow**: Inter-service communication and data consistency
- **Error Propagation**: Distributed system error handling
- **Service Contracts**: API versioning and backward compatibility
- **Integration Testing**: Service integration and contract testing
- **Rate Limiting**: API throttling and usage control
- **Circuit Breakers**: Fault tolerance and resilience patterns
- **Message Formats**: Data serialization and protocol design

**When to Use**: API development, microservices architecture, system integration, data flow design

### 🧠 Data Scientist
**Focus**: ML models, data quality, and statistical rigor

**Responsibilities**:
- **Data Quality & Integrity**: Data validation, cleaning, and bias detection
- **Statistical Rigor**: Hypothesis testing, significance analysis, and methodology
- **Model Performance**: Model evaluation, validation, and performance metrics
- **Reproducibility**: Experiment tracking, version control, and documentation
- **Feature Engineering**: Feature selection, transformation, and domain knowledge
- **Ethical AI & Bias**: Fairness, bias detection, and responsible AI practices
- **Experiment Design**: A/B testing, statistical power, and experimental methodology
- **Model Interpretability**: Explainable AI and model transparency

**When to Use**: ML model development, data analysis, experiment design, model validation

## 🎯 Persona Activation

### Automatic Activation
Personas are automatically activated based on:
- **Command Context**: Specific commands trigger relevant personas
- **File Types**: Code analysis activates appropriate expertise
- **Project Context**: Framework and domain-specific activation

### Manual Activation
You can explicitly request persona perspectives:
```
# Security review with security engineer persona
Please review this authentication code from a security engineer perspective

# Performance analysis with performance engineer persona  
Analyze this database query performance as a performance engineer

# Architecture review with architect persona
Review this system design from an architect's perspective
```

### Multi-Persona Analysis
Request multiple perspectives for comprehensive analysis:
```
# Combined security and performance review
Please review this API endpoint from both security engineer and performance engineer perspectives

# Full team review
Analyze this feature implementation from architect, developer, tester, and product manager perspectives
```

## 🔄 Persona Collaboration Patterns

### Sequential Review
1. **Architect** → System design validation
2. **Developer** → Implementation review  
3. **Security Engineer** → Security assessment
4. **Tester** → Test strategy validation
5. **DevOps Engineer** → Deployment readiness

### Parallel Specialization
- **Security Engineer** + **DevOps Engineer** → Secure deployment pipeline
- **Performance Engineer** + **Data Scientist** → Scalable ML systems
- **Developer** + **Integration Specialist** → Robust API implementation

### Domain-Specific Teams
- **Web Development**: Architect + Developer + Security Engineer + DevOps Engineer
- **Data Science**: Data Scientist + Performance Engineer + Integration Specialist
- **Enterprise Systems**: Architect + Security Engineer + DevOps Engineer + Product Manager

## 🛠️ Command Specialization

### Security Commands
- **Primary**: Security Engineer
- **Secondary**: DevOps Engineer (for secure deployment)
- **Tertiary**: Architect (for security architecture)

### DevOps Commands  
- **Primary**: DevOps Engineer
- **Secondary**: Security Engineer (for secure infrastructure)
- **Tertiary**: Performance Engineer (for optimized deployment)

### Data Science Commands
- **Primary**: Data Scientist  
- **Secondary**: Performance Engineer (for scalable ML)
- **Tertiary**: Integration Specialist (for ML APIs)

### Performance Commands
- **Primary**: Performance Engineer
- **Secondary**: Architect (for scalable architecture)
- **Tertiary**: DevOps Engineer (for monitoring)

## 🎨 Customization

### Adding New Personas
1. Create new persona file in `templates/personas/`
2. Define focus areas and responsibilities
3. Add to command specialization mappings
4. Update documentation and examples

### Modifying Existing Personas  
1. Edit persona files in `templates/personas/`
2. Adjust focus areas and responsibilities
3. Update command integrations
4. Test with representative scenarios

### Creating Domain-Specific Variants
- **Industry-Specific**: Healthcare, finance, e-commerce personas
- **Technology-Specific**: Cloud-native, mobile, IoT personas  
- **Role-Specific**: Senior architect, junior developer, QA lead personas

## 📚 Best Practices

### Effective Persona Usage
1. **Match Expertise to Context**: Use appropriate personas for specific tasks
2. **Sequential Analysis**: Apply personas in logical order for comprehensive review
3. **Clear Communication**: Specify which persona perspective you're requesting
4. **Balanced Feedback**: Use multiple personas for well-rounded analysis

### Persona Integration with Commands
1. **Command-Driven Activation**: Let commands automatically activate relevant personas
2. **Explicit Requests**: Manually request specific persona perspectives when needed
3. **Multi-Persona Commands**: Use commands that benefit from multiple expert views
4. **Context Awareness**: Consider project context when selecting personas

### Quality Assurance
1. **Comprehensive Coverage**: Ensure all critical aspects are covered by appropriate personas
2. **Consistent Standards**: Maintain consistent quality standards across all personas
3. **Regular Updates**: Keep persona definitions current with industry best practices
4. **Validation**: Test persona effectiveness with real-world scenarios

---

*Each persona represents years of specialized expertise condensed into actionable guidance for your development workflow.*