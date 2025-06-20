# Setup Guide

Complete step-by-step guide to get started with awesome-claude-code templates and tools.

## 🚀 Quick Start (5 minutes)

### Option 1: One-Line Installation
```bash
curl -sSL https://raw.githubusercontent.com/username/awesome-claude-code/main/scripts/install.sh | bash
```

### Option 2: Manual Installation
```bash
# Clone the repository
git clone https://github.com/username/awesome-claude-code.git
cd awesome-claude-code

# Install Python dependencies
pip install -r tools/requirements.txt

# Run interactive setup
python tools/setup.py
```

## 📋 Prerequisites

### Required
- **Python 3.8+** - For the interactive setup tool
- **Git** - For version control and cloning repositories
- **Claude Code** - The AI coding assistant ([installation guide](https://docs.anthropic.com/claude/docs))

### Recommended
- **Virtual environment tool** (venv, conda, poetry, pipenv)
- **Modern terminal** with good Unicode support
- **IDE with Claude Code integration** (VS Code, Windsurf, PyCharm, etc.)

### Check Your Setup
```bash
# Verify Python version
python --version  # Should be 3.8 or higher

# Verify Git
git --version

# Verify Claude Code
claude --version

# Check if you have a package manager
pip --version     # pip
poetry --version  # poetry (optional)
conda --version   # conda (optional)
```

## 🛠️ Detailed Installation

### Step 1: Clone the Repository
```bash
# Choose a location for the templates
cd ~
git clone https://github.com/username/awesome-claude-code.git
cd awesome-claude-code
```

### Step 2: Install Python Dependencies
```bash
# Create virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r tools/requirements.txt
```

**Dependencies installed:**
- `click` - Command line interface
- `rich` - Beautiful terminal output
- `jsonschema` - JSON validation
- `pathlib` - Path handling (built-in for Python 3.4+)

### Step 3: Run the Interactive Setup Tool
```bash
python tools/setup.py
```

This will guide you through:
1. **Project Information** - Name, description, framework
2. **Technology Stack** - Database, Python version, package manager
3. **Development Environment** - IDE, OS, shell preferences
4. **Code Quality Tools** - Black, isort, flake8, mypy, pytest, etc.
5. **MCP Server Configuration** - External tool integrations
6. **Configuration Scope** - Global vs project-specific settings

## 🎯 Setup Options

### Interactive Mode (Recommended)
```bash
python tools/setup.py
```
- Full guided setup with prompts
- Smart defaults based on your environment
- Validates all inputs
- Creates all necessary files

### Non-Interactive Mode
```bash
python tools/setup.py --non-interactive
```
- Uses sensible defaults
- Creates basic configuration quickly
- Good for automated setup or testing

### Preset Mode
```bash
python tools/setup.py --preset backend-team
python tools/setup.py --preset data-science
python tools/setup.py --preset startup
```
- Uses pre-configured team settings
- Optimized for specific use cases
- Can be customized after generation

## 📁 What Gets Created

### Global Configuration (Optional)
```
~/.claude/
├── CLAUDE.md          # Global AI instructions
└── settings.json      # Global permissions and settings
```

### Project Configuration
```
your-project/
├── CLAUDE.md              # Project-specific AI instructions
├── .claude/
│   └── settings.json      # Project permissions
├── .mcp.json             # MCP server configuration (if enabled)
└── setup.sh              # Project initialization script
```

### Additional Files
- **requirements.txt** - Python dependencies (if using pip)
- **pyproject.toml** - Modern Python configuration (if using poetry)
- **.gitignore** - Appropriate ignores for your framework
- **README.md** - Project documentation template

## 🔧 Configuration Customization

### After Initial Setup
1. **Review CLAUDE.md** - Customize AI instructions for your project
2. **Check settings.json** - Adjust permissions as needed
3. **Configure MCP servers** - Add API keys and connection strings
4. **Run setup.sh** - Initialize your project structure

### Environment Variables
Create a `.env` file with your project-specific variables:
```bash
# Copy the example file
cp .env.example .env

# Edit with your values
DATABASE_URL=postgresql://localhost/myproject
SECRET_KEY=your-secret-key-here
API_KEY=your-api-key-here
```

## 🌐 Framework-Specific Setup

### FastAPI Projects
```bash
# Setup FastAPI with PostgreSQL
python tools/setup.py
# Choose: FastAPI, PostgreSQL, uvicorn, pytest

# Generated files include:
# - FastAPI-specific CLAUDE.md with API development patterns
# - settings.json with uvicorn and API testing permissions
# - .mcp.json with PostgreSQL and HTTP fetch servers
```

### Django Projects
```bash
# Setup Django with database management
python tools/setup.py
# Choose: Django, PostgreSQL, pytest, django-admin commands

# Generated files include:
# - Django-specific CLAUDE.md with management commands
# - settings.json with Django permissions
# - Database migration instructions
```

### Data Science Projects
```bash
# Setup data science environment
python tools/setup.py
# Choose: Data Science, Jupyter, pandas, scikit-learn

# Generated files include:
# - CLAUDE.md with notebook and data analysis patterns
# - settings.json with Jupyter and Python REPL permissions
# - MCP configuration for filesystem and Python execution
```

## 🎭 Team Presets

### Backend Development Team
```bash
python tools/setup.py --preset backend-team
```
**Includes:**
- API development focus (FastAPI/Django)
- Database tools (PostgreSQL MCP)
- Security scanning (bandit)
- Comprehensive testing (pytest, coverage)
- API documentation tools

### Data Science Team
```bash
python tools/setup.py --preset data-science
```
**Includes:**
- Jupyter notebook support
- Data processing libraries
- Python REPL MCP server
- Visualization tools
- Experiment tracking patterns

### Startup Team
```bash
python tools/setup.py --preset startup
```
**Includes:**
- Rapid development focus
- Minimal overhead
- Essential tools only
- Quick deployment patterns
- Flexibility for pivoting

### Enterprise Team
```bash
python tools/setup.py --preset enterprise
```
**Includes:**
- Security-first approach
- Compliance considerations
- Extensive testing requirements
- Documentation standards
- Audit trail patterns

## 🔍 Verification Steps

### Test Your Setup
```bash
# Navigate to a test project
mkdir test-claude-project
cd test-claude-project

# Initialize with Claude Code
claude

# Check that CLAUDE.md is loaded
# You should see project-specific context in Claude's responses

# Test common commands
/check              # Should run code quality checks
/commit             # Should generate commit messages
/context-prime      # Should analyze project structure
```

### Validate Configuration Files
```bash
# Run validation tool
python ~/.awesome-claude-code/tools/validate-config.py .

# Check JSON syntax
python -m json.tool .claude/settings.json
python -m json.tool .mcp.json  # if it exists
```

### Test MCP Servers (if configured)
```bash
# List configured MCP servers
claude mcp list

# Test a specific server (example: PostgreSQL)
claude mcp test postgres
```

## 🚨 Troubleshooting Common Issues

### Python Import Errors
```bash
# If you see "ModuleNotFoundError"
pip install -r tools/requirements.txt

# If using a virtual environment, make sure it's activated
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

### Permission Errors
```bash
# If Claude Code can't execute commands
# Check your settings.json permissions array
# Make sure bash commands are in the "allow" list
```

### Template Generation Fails
```bash
# Check Python version
python --version  # Must be 3.8+

# Try with verbose output
python tools/setup.py --verbose

# Check for file system permissions
ls -la ~/.claude/  # Should be writable
```

### Claude Code Not Finding Configuration
```bash
# Verify files are in the correct location
ls -la CLAUDE.md .claude/settings.json

# Check that you're in the project directory
pwd

# Try restarting Claude Code
claude --restart
```

## 🔄 Updating Your Setup

### Update Templates
```bash
# Pull latest changes
cd ~/.awesome-claude-code
git pull origin main

# Re-run setup to get new features
python tools/setup.py
```

### Migrate Configurations
```bash
# Use migration tool for version updates
python tools/migrate-config.py --from v1 --to v2
```

### Backup Your Configurations
```bash
# Backup before major changes
cp -r ~/.claude ~/.claude-backup
cp CLAUDE.md CLAUDE.md.backup
cp .claude/settings.json .claude/settings.json.backup
```

## 🎓 Learning Path

### Beginner (First Week)
1. **Complete basic setup** with interactive tool
2. **Customize CLAUDE.md** for your main project
3. **Learn essential commands**: `/check`, `/commit`, `/clean`
4. **Establish daily workflow** with Claude Code

### Intermediate (First Month)
1. **Explore advanced commands**: `/implement-task`, `/pr-review`
2. **Set up MCP servers** for database/API integration
3. **Create custom commands** for repeated tasks
4. **Optimize prompt patterns** for your domain

### Advanced (Ongoing)
1. **Multi-Claude workflows** for complex projects
2. **Team configuration standardization**
3. **Custom MCP server development**
4. **Contribute improvements** back to awesome-claude-code

## 💡 Tips for Success

### Start Small
- Begin with basic setup and gradually add complexity
- Focus on one framework/project type initially
- Add tools incrementally as you see value

### Document Your Journey
- Keep notes on what works for your workflow
- Share successful patterns with your team
- Contribute improvements back to the community

### Stay Updated
- Watch the awesome-claude-code repository for updates
- Follow Claude Code release notes for new features
- Participate in community discussions

### Measure Impact
- Track how Claude Code improves your productivity
- Note which configurations provide the most value
- Adjust settings based on actual usage patterns

## 🆘 Getting Help

### Documentation
- [Best Practices](best-practices.md) - Optimization tips
- [Customization Guide](customization.md) - Advanced configuration
- [Troubleshooting](troubleshooting.md) - Common issues and solutions

### Community Support
- **GitHub Issues**: [Report bugs or request features](https://github.com/username/awesome-claude-code/issues)
- **GitHub Discussions**: [Ask questions and share tips](https://github.com/username/awesome-claude-code/discussions)
- **Contributing**: [Help improve the project](../CONTRIBUTING.md)

### Professional Support
For enterprise teams needing additional support:
- Custom template development
- Team training and onboarding
- Configuration optimization consulting

---

**Next Steps:** Once you've completed the setup, check out the [Best Practices Guide](best-practices.md) to optimize your Claude Code workflow!