# Claude Code Configuration Templates & Tools

> Comprehensive templates and tools for setting up Claude Code workflows

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🚀 Quick Start

### Interactive Setup (Recommended)
```bash
# Clone the repository
git clone https://github.com/adimenia/auto-claude-code.git
cd auto-claude-code

# Run the interactive setup tool
python tools/setup.py
```


## 📚 What's Included

- **🤖 CLAUDE.md Templates**: Project and global configuration templates
- **⚙️ Settings Templates**: Comprehensive settings.json configurations  
- **🌐 MCP Configurations**: Pre-configured MCP server setups
- **🛠️ Interactive Setup Tool**: Python tool for guided configuration
- **📋 Development Modes**: Solo and team collaboration configurations
- **📖 Complete Methodology**: Step-by-step workflow documentation
- **🎯 Example Projects**: Real-world configuration examples
- **👥 Persona System**: Expert personas (architect, security, DevOps, data scientist, etc.)
- **⚡ Command Library**: 26+ specialized commands for development workflows
- **🔧 Professional Workflows**: Complete automation for security, CI/CD, data science

## 🎯 Features

- ✅ Cross-platform support (Windows, macOS, Linux, WSL)
- ✅ Framework-specific templates (FastAPI, Django, Flask, etc.)
- ✅ Interactive configuration generator
- ✅ Solo and team development modes
- ✅ Comprehensive documentation
- ✅ Interactive configuration generation
- ✅ Easy customization and extension
- 🆕 **Configuration validation & health checks**
- 🆕 **Smart migration & upgrade system**
- 🆕 **Automatic backup & restore capabilities**
- 🆕 **Expert persona system with 9 specialized roles**
- 🆕 **26+ professional-grade command templates**
- 🆕 **Complete security, DevOps, and data science workflows**
- 🆕 **MLflow, Airflow, and enterprise tool integrations**

## 📖 Documentation

### Core Documentation
- [Complete Methodology](.github/docs/methodology.md) - Comprehensive workflow guide
- [Setup Guide](.github/docs/setup_guide.md) - Step-by-step installation
- [Customization](.github/docs/customization.md) - How to modify templates
- [Best Practices](.github/docs/best_practices.md) - Claude Code optimization tips
- [Troubleshooting](.github/docs/troubleshooting.md) - Common issues and solutions

### 🆕 System References
- [**Command Library**](COMMANDS.md) - Complete reference for all 26+ available commands
- [**Persona System**](PERSONAS.md) - Expert personas and specialization guide
- [**Validation & Migration**](tools/VALIDATION_MIGRATION.md) - Configuration management tools

## 🛠️ Tools

### Interactive Setup Tool
```bash
python tools/setup.py                    # Interactive mode
python tools/setup.py --help             # View all options
```

### 🆕 Validation & Migration Tools
```bash
# Health check your configuration
python tools/setup.py --health-check

# Check for and apply upgrades
python tools/setup.py --upgrade

# Validate existing configuration
python tools/setup.py --validate
```

See [Validation & Migration Guide](tools/VALIDATION_MIGRATION.md) for detailed documentation.


## 🎭 Development Modes & Personas

The setup tool supports different development approaches with expert personas:

### Development Modes
- **Solo Development**: Individual developer workflow with personal productivity focus
- **Team Collaboration**: Team-oriented configuration with shared standards and practices
- **Framework-Specific**: Optimized configurations for FastAPI, Django, Flask, Data Science, CLI tools, and Web Scraping

### Expert Personas (9 Available)
- **🏗️ Architect**: System design, scalability, and technical architecture
- **👨‍💻 Developer**: Code quality, patterns, and implementation best practices
- **🧪 Tester**: Testing strategies, quality assurance, and validation
- **🔒 Security Engineer**: Vulnerability assessment, security auditing, and compliance
- **🚀 DevOps Engineer**: CI/CD, deployment, infrastructure, and monitoring
- **⚡ Performance Engineer**: Optimization, load testing, and scalability
- **📊 Product Manager**: UX, business logic, and feature completeness
- **🔗 Integration Specialist**: API design, service integration, and data flow
- **🧠 Data Scientist**: ML models, data quality, and statistical rigor

## 🏗️ Framework Support

| Framework | Status | Template | MCP Servers |
|-----------|--------|----------|-------------|
| FastAPI | ✅ Complete | ✅ | PostgreSQL, HTTP |
| Django | ✅ Complete | ✅ | PostgreSQL, HTTP |
| Flask | ✅ Complete | ✅ | SQLite, HTTP |
| Data Science | ✅ Complete | ✅ | Jupyter, Files |
| CLI Tools | ✅ Complete | ✅ | Files, HTTP |
| Web Scraping | 🚧 Beta | ✅ | HTTP, Browser |

## ⚡ Command Library (26+ Commands)

The template system includes a comprehensive command library organized by specialization:

### 🔒 Security Commands
- **security-audit**: OWASP Top 10 vulnerability assessment with automated scanning
- **secrets-scan**: Git history and codebase secrets detection with remediation
- **security-headers**: HTTP security headers configuration (CSP, HSTS, etc.)

### 🚀 DevOps Commands  
- **setup-ci**: Multi-platform CI/CD pipeline generation (GitHub Actions, GitLab, Azure)
- **containerize**: Docker containerization with security hardening and K8s manifests
- **deploy-config**: Cloud deployment configurations with blue-green strategies

### ⚡ Performance Commands
- **performance-audit**: Code profiling, database optimization, and bottleneck analysis
- **load-test**: Progressive load testing with Locust, k6, and performance monitoring

### 🔗 Data & API Commands
- **api-design**: RESTful API design with OpenAPI specs and authentication strategies
- **data-migration**: Database migration tools with cross-platform support
- **backup-strategy**: Disaster recovery with 3-2-1 backup rule implementation

### 🧪 Integration Commands
- **integration-test**: End-to-end testing with API testing and service mocking

### 🧠 Data Science Commands
- **data-exploration**: Automated EDA with pandas profiling and bias detection
- **model-development**: ML model training with hyperparameter tuning and MLflow
- **experiment-tracking**: MLflow, Weights & Biases integration with reproducibility
- **data-pipeline**: ETL/ELT pipelines with Apache Airflow and streaming capabilities

### 🚧 Coming Soon
- **model-deployment**: ML model serving and monitoring in production
- **model-monitoring**: Model drift detection and performance tracking
- **feature-engineering**: Automated feature selection and engineering pipelines
- **data-governance**: Data lineage, quality monitoring, and compliance frameworks

## 🚀 Quick Examples

### FastAPI Project Setup with Security
```bash
# Create new FastAPI project with optimized Claude config
python tools/setup.py
# Choose FastAPI framework in interactive setup
# Generated: CLAUDE.md with security-engineer persona, settings.json, .mcp.json

# Example commands available:
# /project:security-audit --framework fastapi
# /project:setup-ci --platform github-actions
# /project:containerize --multi-stage
```

### Data Science Project Setup  
```bash
# Create ML project with comprehensive data science tools
python tools/setup.py
# Choose Data Science framework in interactive setup
# Generated: Jupyter-optimized configs with data-scientist persona

# Example commands available:
# /project:data-exploration --dataset data/customers.csv --depth comprehensive
# /project:model-development --model-type classification --target churn
# /project:experiment-tracking --platform mlflow --auto-logging
# /project:data-pipeline --pipeline-type etl --orchestrator airflow
```

### Enterprise Security & DevOps
```bash
# Set up enterprise-grade security and deployment pipeline
# Available personas: security-engineer, devops-engineer, performance-engineer

# Security workflow:
# /project:security-audit --depth comprehensive
# /project:secrets-scan --remediate
# /project:security-headers --framework django

# DevOps workflow:  
# /project:setup-ci --platform azure-devops --stages security,test,deploy
# /project:containerize --security-hardened --kubernetes
# /project:deploy-config --cloud aws --strategy blue-green
```

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Contribution Ideas
- Add new framework templates
- Improve existing configurations
- Create team-specific presets
- Enhance documentation
- Report bugs and issues

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Acknowledgments

- Claude Code team for the amazing tool
- Community contributors and feedback
- All the developers sharing their workflow optimizations

## 🔗 Related Projects

- [Claude Code Official Docs](https://docs.anthropic.com/claude/docs)

---

⭐ If this project helps you, please give it a star on GitHub!