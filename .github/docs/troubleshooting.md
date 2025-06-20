# Troubleshooting Guide

Common issues and their solutions when using awesome-claude-code templates and tools.

## 🚨 Quick Diagnostics

Run these commands to quickly identify common issues:

```bash
# Check Python environment
python --version                    # Should be 3.8+
which python                       # Check Python location
pip list | grep -E "(click|rich)"  # Check dependencies

# Check Claude Code installation
claude --version                   # Verify Claude Code is installed
claude config list                # Show current configuration

# Check file permissions
ls -la CLAUDE.md .claude/          # Verify files exist and are readable
cat CLAUDE.md | head -5            # Test file content access

# Validate JSON configuration
python -m json.tool .claude/settings.json
python -m json.tool .mcp.json      # If MCP is configured
```

## 🛠️ Installation Issues

### Problem: Python Dependencies Failed to Install
```
Error: Failed building wheel for [package]
Error: Microsoft Visual C++ 14.0 is required
```

**Solutions:**
```bash
# Windows: Install Visual C++ Build Tools
# Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/

# macOS: Install Xcode Command Line Tools
xcode-select --install

# Linux: Install build essentials
sudo apt-get install build-essential python3-dev  # Ubuntu/Debian
sudo yum groupinstall "Development Tools"         # CentOS/RHEL

# Alternative: Use conda instead of pip
conda install click rich jsonschema
```

### Problem: Permission Denied During Installation
```
Error: [Errno 13] Permission denied: '/usr/local/lib/python3.x/site-packages/'
```

**Solutions:**
```bash
# Use virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
pip install -r tools/requirements.txt

# Or install for current user only
pip install --user -r tools/requirements.txt

# Fix permissions (if necessary)
sudo chown -R $USER ~/.local/lib/python*/site-packages
```

### Problem: Claude Code Not Found
```
Error: claude: command not found
```

**Solutions:**
```bash
# Check if Claude Code is installed
which claude

# Install Claude Code (example - check official docs for latest)
npm install -g @anthropic/claude-code

# Add to PATH (if installed but not in PATH)
echo 'export PATH="$PATH:/path/to/claude"' >> ~/.bashrc
source ~/.bashrc

# Verify installation
claude --version
```

## 📋 Configuration Issues

### Problem: CLAUDE.md Not Being Loaded
**Symptoms:** Claude doesn't seem to follow project-specific instructions

**Diagnostics:**
```bash
# Check file location and content
ls -la CLAUDE.md
head -10 CLAUDE.md

# Check if Claude detects the file
claude --show-context | grep CLAUDE.md

# Verify file encoding
file CLAUDE.md  # Should show UTF-8
```

**Solutions:**
```bash
# Ensure correct location
mv CLAUDE.md ./CLAUDE.md  # Must be in project root

# Fix file encoding if needed
iconv -f ISO-8859-1 -t UTF-8 CLAUDE.md > CLAUDE.md.utf8
mv CLAUDE.md.utf8 CLAUDE.md

# Restart Claude Code
claude --restart

# Test with explicit context loading
claude --context ./CLAUDE.md
```

### Problem: Settings.json Permission Errors
**Symptoms:** Claude Code can't execute allowed commands

**Diagnostics:**
```bash
# Validate JSON syntax
python -m json.tool .claude/settings.json

# Check specific permissions
jq '.permissions.allow' .claude/settings.json
jq '.permissions.deny' .claude/settings.json
```

**Solutions:**
```bash
# Fix JSON syntax errors
python tools/validate-config.py .claude/settings.json

# Common permission patterns
cat > .claude/settings.json << 'EOF'
{
  "permissions": {
    "allow": [
      "Bash(git*)",
      "Bash(python*)",
      "Bash(pytest*)",
      "Edit(src/**)",
      "Edit(tests/**)"
    ],
    "deny": [
      "Bash(rm -rf*)",
      "Edit(.env*)"
    ]
  }
}
EOF

# Restart Claude to reload permissions
claude --restart
```

### Problem: MCP Servers Not Connecting
**Symptoms:** Database or external tool queries fail

**Diagnostics:**
```bash
# Check MCP configuration
python -m json.tool .mcp.json

# Test MCP servers
claude mcp list
claude mcp test postgres  # Replace with your server name

# Check server logs
claude logs --mcp
```

**Solutions:**
```bash
# Fix common MCP configuration issues
cat > .mcp.json << 'EOF'
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "POSTGRES_CONNECTION_STRING": "postgresql://user:pass@localhost:5432/dbname"
      }
    }
  }
}
EOF

# Install MCP server if missing
npx @modelcontextprotocol/server-postgres

# Check environment variables
echo $POSTGRES_CONNECTION_STRING

# Test database connection manually
psql "postgresql://user:pass@localhost:5432/dbname" -c "\l"
```

## 🐍 Python Environment Issues

### Problem: Wrong Python Version
**Symptoms:** Setup tool fails with syntax errors

**Diagnostics:**
```bash
python --version           # Check current version
python3 --version          # Check Python 3 specifically
which python python3       # Check locations
```

**Solutions:**
```bash
# Use Python 3 explicitly
python3 tools/setup.py

# Set up Python version with pyenv
pyenv install 3.11.0
pyenv local 3.11.0

# Create virtual environment with specific version
python3.11 -m venv .venv
source .venv/bin/activate

# Update system Python (Ubuntu/Debian)
sudo apt update
sudo apt install python3.11
```

### Problem: Virtual Environment Issues
**Symptoms:** Packages not found, import errors

**Diagnostics:**
```bash
# Check if virtual environment is active
echo $VIRTUAL_ENV

# Check Python path
python -c "import sys; print(sys.executable)"

# List installed packages
pip list
```

**Solutions:**
```bash
# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Recreate virtual environment if corrupted
rm -rf .venv
python -m venv .venv
source .venv/bin/activate
pip install -r tools/requirements.txt

# Fix PATH issues
export PATH=".venv/bin:$PATH"
```

### Problem: Package Import Errors
```
ImportError: No module named 'click'
ModuleNotFoundError: No module named 'rich'
```

**Solutions:**
```bash
# Install missing dependencies
pip install click rich jsonschema

# Install from requirements file
pip install -r tools/requirements.txt

# Update pip if needed
python -m pip install --upgrade pip

# Clear pip cache if corrupted
pip cache purge
pip install --force-reinstall click rich
```

## 💻 Platform-Specific Issues

### Windows Issues

#### Problem: Path Separator Issues
**Symptoms:** File paths don't work correctly

**Solutions:**
```bash
# Use forward slashes in configuration
"Edit(src/**)"  # Works on Windows
"Edit(src\\**)" # Don't use backslashes

# Set proper Python path
python -c "import os; print(os.pathsep)"
```

#### Problem: PowerShell vs Command Prompt
**Symptoms:** Bash commands don't work

**Solutions:**
```bash
# Use Git Bash or WSL for bash commands
# Or configure for PowerShell in settings.json:
{
  "permissions": {
    "allow": [
      "PowerShell(git*)",
      "PowerShell(python*)"
    ]
  }
}
```

#### Problem: Long Path Names
**Symptoms:** File operations fail with path too long

**Solutions:**
```bash
# Enable long paths in Windows
# Run as Administrator:
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" `
-Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force

# Or use shorter project paths
cd C:\proj\
```

### macOS Issues

#### Problem: Xcode Command Line Tools Missing
**Symptoms:** Build failures during pip install

**Solutions:**
```bash
# Install Xcode Command Line Tools
xcode-select --install

# Verify installation
xcode-select -p
```

#### Problem: Python from Homebrew vs System
**Symptoms:** Version conflicts, permission issues

**Solutions:**
```bash
# Use Homebrew Python
brew install python@3.11
echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zshrc

# Or use pyenv for version management
brew install pyenv
pyenv install 3.11.0
pyenv global 3.11.0
```

### Linux Issues

#### Problem: Missing Development Headers
**Symptoms:** Compilation failures during pip install

**Solutions:**
```bash
# Ubuntu/Debian
sudo apt-get install python3-dev build-essential

# CentOS/RHEL/Fedora
sudo dnf groupinstall "Development Tools"
sudo dnf install python3-devel

# Alpine Linux
apk add python3-dev gcc musl-dev
```

#### Problem: Permission Issues with System Python
**Solutions:**
```bash
# Use virtual environment (recommended)
python3 -m venv ~/.venv/claude
source ~/.venv/claude/bin/activate

# Or use user installation
pip3 install --user -r tools/requirements.txt
```

### WSL Issues

#### Problem: Windows Path Integration
**Symptoms:** Can't access Windows files from WSL

**Solutions:**
```bash
# Access Windows files through /mnt/c/
cd /mnt/c/Users/YourName/Projects/

# Set Windows PATH in WSL
export PATH="$PATH:/mnt/c/Windows/System32"

# Configure git for Windows/WSL integration
git config --global core.autocrlf input
```

## 🔧 Tool-Specific Issues

### Problem: Setup Tool Hangs or Crashes
**Symptoms:** Interactive prompts don't respond

**Diagnostics:**
```bash
# Run with verbose output
python tools/setup.py --verbose

# Check for specific errors
python tools/setup.py 2>&1 | tee setup.log
```

**Solutions:**
```bash
# Use non-interactive mode
python tools/setup.py --non-interactive

# Check terminal compatibility
export TERM=xterm-256color

# Update rich library
pip install --upgrade rich

# Try basic Python REPL
python -c "from rich.console import Console; Console().print('Test')"
```

### Problem: Validation Tool Fails
**Symptoms:** validate-config.py reports errors incorrectly

**Solutions:**
```bash
# Check if files exist
ls -la templates/

# Run validation with debug output
python tools/validate-config.py --debug templates/

# Test JSON parsing manually
python -c "import json; print(json.load(open('.claude/settings.json')))"
```

### Problem: Generated Files Are Corrupted
**Symptoms:** CLAUDE.md or settings.json have syntax errors

**Solutions:**
```bash
# Regenerate with clean slate
rm CLAUDE.md .claude/settings.json .mcp.json
python tools/setup.py

# Check file encoding
file CLAUDE.md .claude/settings.json

# Validate generated JSON
python -m json.tool .claude/settings.json > /dev/null
```

## 🌐 Network and Connectivity Issues

### Problem: MCP Server Connection Timeouts
**Symptoms:** Database queries fail with timeout errors

**Diagnostics:**
```bash
# Test database connection directly
psql "postgresql://user:pass@localhost:5432/db" -c "SELECT 1;"

# Check network connectivity
ping localhost
telnet localhost 5432

# Check if database is running
sudo systemctl status postgresql  # Linux
brew services list | grep postgres  # macOS
```

**Solutions:**
```bash
# Start database service
sudo systemctl start postgresql  # Linux
brew services start postgresql   # macOS

# Check connection string format
export POSTGRES_CONNECTION_STRING="postgresql://user:pass@localhost:5432/dbname"

# Test with different timeout
{
  "mcpServers": {
    "postgres": {
      "env": {
        "POSTGRES_CONNECTION_STRING": "...",
        "CONNECT_TIMEOUT": "30",
        "QUERY_TIMEOUT": "60"
      }
    }
  }
}
```

### Problem: GitHub MCP Server Authentication
**Symptoms:** GitHub operations fail with 401/403 errors

**Solutions:**
```bash
# Check GitHub token
echo $GITHUB_PERSONAL_ACCESS_TOKEN

# Test token manually
curl -H "Authorization: token $GITHUB_PERSONAL_ACCESS_TOKEN" \
     https://api.github.com/user

# Generate new token at https://github.com/settings/tokens
# Required scopes: repo, read:user

# Update MCP configuration
{
  "mcpServers": {
    "github": {
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "your_new_token_here"
      }
    }
  }
}
```

## 🔍 Debugging Steps

### General Debugging Process
1. **Identify the Problem**
   ```bash
   # Get detailed error information
   python tools/setup.py --verbose 2>&1 | tee debug.log
   claude --debug
   ```

2. **Check Basic Requirements**
   ```bash
   # Verify Python version
   python --version
   
   # Check dependencies
   pip check
   
   # Verify Claude Code
   claude --version
   ```

3. **Isolate the Issue**
   ```bash
   # Test in clean environment
   mkdir test-debug
   cd test-debug
   python ../awesome-claude-code/tools/setup.py --non-interactive
   ```

4. **Collect Information**
   ```bash
   # System information
   uname -a
   python -c "import platform; print(platform.platform())"
   
   # Environment variables
   env | grep -E "(PYTHON|CLAUDE|PATH)"
   
   # File permissions
   ls -la CLAUDE.md .claude/
   ```

5. **Test Solutions**
   ```bash
   # Backup current configuration
   cp -r .claude .claude-backup
   
   # Try minimal configuration
   python tools/setup.py --preset minimal
   
   # Test individual components
   claude mcp test postgres
   ```

## 🆘 Getting Help

### Before Reporting Issues
1. **Search existing issues**: Check GitHub issues for similar problems
2. **Try the latest version**: Update awesome-claude-code templates
3. **Test with minimal config**: Use `--non-interactive` mode
4. **Collect debug information**: Include version info and error logs

### Information to Include in Bug Reports
```bash
# System information
echo "OS: $(uname -a)"
echo "Python: $(python --version)"
echo "Claude Code: $(claude --version)"

# Configuration files (remove sensitive data)
echo "=== CLAUDE.md ==="
head -20 CLAUDE.md

echo "=== settings.json ==="
cat .claude/settings.json

echo "=== Error log ==="
python tools/setup.py --verbose 2>&1 | tail -50
```

### Community Resources
- **GitHub Issues**: [Report bugs](https://github.com/username/awesome-claude-code/issues)
- **GitHub Discussions**: [Ask questions](https://github.com/username/awesome-claude-code/discussions)
- **Documentation**: [Check docs](../README.md)

### Self-Help Checklist
Before asking for help, try these steps:

- [ ] Read the error message completely
- [ ] Check the [Setup Guide](setup-guide.md)
- [ ] Verify your Python version (3.8+)
- [ ] Test with `--non-interactive` mode
- [ ] Check file permissions and paths
- [ ] Validate JSON configuration files
- [ ] Try in a clean virtual environment
- [ ] Search existing GitHub issues

Remember: Most issues are environment-related and can be resolved by following the installation steps carefully!