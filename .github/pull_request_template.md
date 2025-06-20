## 📋 Description
Brief description of what this PR accomplishes.

Fixes #(issue_number)

## 🎯 Type of Change
- [ ] 🐛 Bug fix (non-breaking change which fixes an issue)
- [ ] ✨ New feature (non-breaking change which adds functionality)
- [ ] 💥 Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] 📚 Documentation update
- [ ] 🎨 Template improvement
- [ ] 🛠️ Tool enhancement
- [ ] 🧪 Test improvement
- [ ] 🔧 Configuration change

## 📝 Changes Made
### Templates
- [ ] Added new framework template: [Framework Name]
- [ ] Updated existing template: [Template Name]
- [ ] Fixed template issue: [Description]
- [ ] Added MCP server configuration
- [ ] Updated settings.json permissions

### Tools
- [ ] Enhanced setup tool functionality
- [ ] Added validation features
- [ ] Fixed tool bug
- [ ] Improved error handling
- [ ] Added new command line options

### Documentation
- [ ] Updated README.md
- [ ] Added/updated docs in docs/
- [ ] Improved setup instructions
- [ ] Added troubleshooting content
- [ ] Updated best practices

### Other
- [ ] Added tests
- [ ] Updated dependencies
- [ ] Fixed CI/CD pipeline
- [ ] Updated examples

## 🧪 Testing
### Manual Testing
- [ ] Tested the setup tool with new changes
- [ ] Validated template generation works correctly
- [ ] Tested on multiple operating systems: [Windows/macOS/Linux/WSL]
- [ ] Verified existing functionality still works

### Automated Testing
- [ ] All existing tests pass
- [ ] Added new tests for new functionality
- [ ] Templates pass validation
- [ ] JSON files are valid
- [ ] No security issues detected

### Test Commands Run
```bash
# List the commands you ran to test this change
python tools/setup.py --non-interactive
python tools/validate-config.py templates/
pytest tests/ -v
```

## 📋 Template Checklist (if applicable)
### For New Framework Templates
- [ ] CLAUDE.md includes all required sections:
  - [ ] Project Overview
  - [ ] Architecture
  - [ ] Development Workflow
  - [ ] Code Quality Standards
  - [ ] Critical Rules
  - [ ] Common Commands
  - [ ] Testing Strategy
  - [ ] Environment Variables
  - [ ] Claude-Specific Instructions
- [ ] settings.json includes appropriate permissions
- [ ] .mcp.json configured (if needed)
- [ ] Tested with real project
- [ ] Documentation updated

### For Template Updates
- [ ] Changes are backward compatible OR migration guide provided
- [ ] Updated relevant documentation
- [ ] Tested with existing projects using this template

## 📸 Screenshots (if applicable)
Add screenshots to help explain your changes, especially for:
- New UI elements in the setup tool
- New template outputs
- Documentation improvements

## 🔗 Related Issues
- Closes #[issue_number]
- Related to #[issue_number]
- Depends on #[issue_number]

## 📚 Documentation
- [ ] Code is self-documenting OR has appropriate comments
- [ ] README.md updated (if needed)
- [ ] docs/ updated (if needed)
- [ ] CHANGELOG.md updated (if significant change)

## ⚡ Performance Impact
- [ ] No performance impact
- [ ] Improves performance: [describe how]
- [ ] May impact performance: [describe impact and why it's acceptable]

## 🔒 Security Considerations
- [ ] No security impact
- [ ] Improves security: [describe how]
- [ ] Potential security considerations: [describe and mitigation]
- [ ] No hardcoded secrets or credentials
- [ ] Appropriate file permissions

## 🌍 Compatibility
### Python Versions
- [ ] Tested with Python 3.8+
- [ ] Uses only compatible dependencies

### Operating Systems
- [ ] Windows compatible
- [ ] macOS compatible  
- [ ] Linux compatible
- [ ] WSL compatible

### Claude Code Versions
- [ ] Compatible with current Claude Code version
- [ ] Backward compatible (or breaking changes documented)

## 📦 Dependencies
- [ ] No new dependencies added
- [ ] New dependencies added: [list and justify]
- [ ] Dependencies updated: [list and justify]
- [ ] All dependencies are secure and well-maintained

## 🚀 Deployment Notes
- [ ] No special deployment steps needed
- [ ] Special deployment steps: [describe]
- [ ] Database changes: [describe]
- [ ] Configuration changes needed: [describe]

## ✅ Final Checklist
- [ ] My code follows the project's style guidelines
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] Any dependent changes have been merged and published

## 🤝 Reviewer Notes
### For Reviewers
Please pay special attention to:
- [ ] Template structure and completeness
- [ ] Security implications
- [ ] Cross-platform compatibility
- [ ] Documentation accuracy
- [ ] Test coverage

### Questions for Reviewers
- Any specific areas you'd like reviewers to focus on?
- Any concerns or uncertainties about the approach?

## 📋 Post-Merge Tasks
- [ ] Update version numbers (if applicable)
- [ ] Create release notes (if applicable)
- [ ] Update examples (if applicable)
- [ ] Notify community (if significant feature)

---

**Additional Context:**
Add any other context about the pull request here.