# Contributing to Claude Code Configuration Templates

Thank you for your interest in contributing! This project aims to provide the best possible Claude Code workflow templates for the community.

## 🎯 Ways to Contribute

### 1. Template Improvements
- Enhance existing CLAUDE.md templates
- Add framework-specific optimizations
- Improve MCP server configurations
- Add new tool integrations

### 2. New Framework Support
- Create templates for new frameworks (Svelte, Next.js, etc.)
- Add database-specific configurations
- Support new development environments

### 3. Documentation
- Improve setup instructions
- Add use case examples
- Create troubleshooting guides
- Write best practice documentation

### 4. Tools and Scripts
- Enhance the Python setup tool
- Add new framework templates
- Improve command library
- Create additional utilities

## 📋 Contribution Process

### 1. Fork and Clone
```bash
git clone https://github.com/your-username/auto-claude-code.git
cd auto-claude-code
```

### 2. Create a Feature Branch
```bash
git checkout -b feature/add-svelte-template
```

### 3. Make Your Changes
- Follow the existing template structure
- Test your changes thoroughly
- Update documentation as needed

### 4. Test Your Changes
```bash
# Test the setup tool manually
python tools/setup.py --help

# Test template generation
mkdir test-project && cd test-project
python ../tools/setup.py
```

### 5. Submit a Pull Request
- Clear title and description
- Reference any related issues
- Include testing details

## 📏 Guidelines

### Template Standards
- Use consistent formatting and structure
- Include comprehensive comments
- Follow security best practices
- Test with real projects

### File Structure
All templates should follow this structure:
```
templates/project/frameworks/[framework-name]/
├── CLAUDE.md          # Framework-specific Claude instructions
├── settings.json      # Permissions and environment settings
├── .mcp.json         # MCP server configurations (if applicable)
└── README.md         # Framework-specific setup notes
```

### CLAUDE.md Template Requirements
- Project overview section
- Framework-specific architecture notes
- Development workflow commands
- Code quality standards
- Critical rules section
- Common commands reference
- Testing strategy
- Environment variables
- Claude-specific instructions

### Code Quality
- Python code should follow PEP 8
- Include type hints where applicable
- Add docstrings to functions
- Write tests for new functionality

### Documentation
- Use clear, concise language
- Include code examples
- Keep README.md updated
- Add inline comments for complex logic

## 🧪 Testing

### Template Testing
```bash
# Test setup tool with different frameworks
mkdir test-project && cd test-project
python ../tools/setup.py

# Test template generation
python ../tools/setup.py --help

# Verify generated files
ls -la  # Check for CLAUDE.md, settings.json, .mcp.json
```

### Python Tool Testing
```bash
# Test setup tool dependencies
cd tools && pip install -r requirements.txt

# Run setup tool with different options
python setup.py --help
python setup.py  # Interactive mode
```

## 🎯 Template Creation Guide

### Adding a New Framework

1. **Create directory structure**:
```bash
mkdir -p templates/project/frameworks/your-framework
```

2. **Create CLAUDE.md**:
- Copy from similar framework
- Customize for your framework's patterns
- Include framework-specific commands
- Add relevant dependencies

3. **Create settings.json**:
- Framework-specific bash permissions
- Relevant file edit permissions
- Environment variables

4. **Create .mcp.json** (if needed):
- Database servers for data-driven frameworks
- HTTP servers for API frameworks
- Custom servers for specialized needs

5. **Test thoroughly**:
- Create real project using template
- Verify all commands work
- Test Claude Code integration

### Example: Adding Svelte Template

```bash
# 1. Create structure
mkdir -p templates/project/frameworks/svelte

# 2. Create CLAUDE.md with Svelte-specific content
# Include: npm commands, dev server, build process, testing

# 3. Create settings.json with Node.js permissions
# Allow: npm install, npm run dev, npm run build, etc.

# 4. Test with real Svelte project
```

## 🚀 Release Process

1. Update version numbers in relevant files
2. Update CHANGELOG.md with new features
3. Test all templates and tools
4. Create GitHub release with proper tags
5. Update documentation

## 💡 Ideas for New Contributors

### Easy First Contributions
- Fix typos in documentation
- Add missing environment variables to templates
- Improve error messages in Python tools
- Add new team presets

### Medium Complexity
- Add new framework templates
- Enhance setup tool features
- Improve documentation
- Create example projects

### Advanced Contributions
- Build new MCP server integrations
- Create IDE plugins/extensions
- Add analytics and metrics
- Build web-based configuration tool

## 🆘 Getting Help

- **Issues**: Open a GitHub issue for bugs or questions
- **Discussions**: Use GitHub Discussions for feature ideas
- **Documentation**: Check the .github/docs/ folder for detailed guides
- **Examples**: Look at existing templates for patterns

## 📊 Code Style

### Python
```python
# Use type hints
def validate_template(template_path: Path) -> bool:
    """Validate a Claude template file."""
    pass

# Use descriptive variable names
framework_config = load_framework_config(framework_name)

# Include docstrings
class TemplateValidator:
    """Validates Claude Code configuration templates."""
    pass
```

### JSON
```json
{
  "permissions": {
    "allow": [
      "Bash(npm run*)",
      "Edit(src/**)"
    ]
  }
}
```

### Markdown
- Use consistent heading levels
- Include code blocks with proper syntax highlighting
- Use bullet points for lists
- Keep line length reasonable

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes for significant contributions
- Special recognition for major features

Thank you for helping make Claude Code workflows better for everyone! 🚀