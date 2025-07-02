# Configuration Validation & Migration System

The auto-claude-code project now includes advanced validation and migration capabilities to ensure your Claude Code configurations remain healthy and up-to-date.

## Features Overview

### 🔍 Configuration Validation
- **CLAUDE.md Syntax Validator**: Validates markdown structure and YAML references
- **MCP Server Connectivity Tester**: Checks server availability and configuration
- **Template Compatibility Checker**: Ensures configuration matches template standards
- **Health Check Dashboard**: Rich console interface with detailed reports

### 🔄 Smart Migration System
- **Version Detection**: Automatic detection of configuration versions
- **Smart Diff Engine**: Intelligent comparison of configuration changes
- **Backup & Restore**: Automatic backups before migrations
- **Upgrade Assistant**: Guided upgrades with rollback capabilities

## Quick Start

### Health Check
Run a comprehensive health check on your current configuration:

```bash
python setup.py --health-check
```

### Upgrade Check
Check for available upgrades and apply them:

```bash
python setup.py --upgrade
```

### Validation Only
Run validation without upgrading:

```bash
python setup.py --validate
```

## Validation Features

### CLAUDE.md Validator
Checks for:
- Valid markdown structure
- Correct @include references
- Missing YAML files
- Malformed syntax
- Common configuration issues

### MCP Server Validator
Validates:
- Server configuration syntax
- Command availability
- Connection testing
- Dependency checks
- Security settings

### Template Validator
Ensures:
- Required files are present
- Directory structure is correct
- Framework-specific requirements
- Version compatibility
- Documentation completeness

## Migration Features

### Version Management
- Semantic versioning support
- Automatic version detection
- Configuration metadata tracking
- Checksum validation

### Smart Diffing
- Intelligent change detection
- Impact assessment
- Auto-merge capability for safe changes
- Conflict identification

### Backup System
- Automatic backups before changes
- Compressed backup storage
- Backup listing and management
- Import/export capabilities

## Usage Examples

### Programmatic Usage

```python
from validation import HealthChecker, ClaudeConfigValidator
from migration import VersionManager, UpgradeAssistant

# Run health check
config_path = Path("/path/to/config")
health_checker = HealthChecker(config_path)
results = health_checker.run_health_check()
health_checker.display_health_report()

# Check version and upgrade
version_manager = VersionManager(config_path)
current_version = version_manager.detect_current_version()

upgrade_assistant = UpgradeAssistant(config_path)
latest_version = upgrade_assistant.check_for_upgrades()
if latest_version:
    upgrade_assistant.perform_upgrade(latest_version)
```

### Command Line Usage

```bash
# Setup with validation enabled (default in interactive mode)
python setup.py

# Run health check only
python setup.py --health-check

# Check for upgrades
python setup.py --upgrade

# Validate existing configuration
python setup.py --validate

# Setup new project with framework
python setup.py --framework fastapi --validate
```

## Health Check Report

The health checker provides detailed reports including:

- **Overall Health Score**: 0-100% based on issues found
- **Error Count**: Critical issues that need immediate attention
- **Warning Count**: Issues that should be addressed
- **Recommendations**: Actionable suggestions for improvements
- **Auto-fixable Issues**: Problems that can be automatically resolved

### Sample Health Report

```
🔍 Configuration Health Check
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Status:     ✅ HEALTHY
Errors:     0
Warnings:   2
Info:       5
Checked:    2024-07-02 14:30:15

📋 ClaudeConfigValidator
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  Warnings:
  • Very long line (250 characters)
    💡 Consider breaking long lines for better readability
  • Recommended section 'Development' not found
    💡 Consider adding a 'Development' section for better organization

📋 MCPServerValidator  
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ℹ️  Information:
  • MCP server 'filesystem' started successfully
  • MCP server 'context7' started successfully
```

## Migration Workflow

### Automatic Upgrades
1. **Detection**: System detects outdated configuration
2. **Preview**: Shows what will change
3. **Backup**: Creates automatic backup
4. **Migration**: Applies changes safely
5. **Validation**: Verifies result health
6. **Rollback**: Available if issues occur

### Manual Migration
1. Check current version: `version_manager.detect_current_version()`
2. List available upgrades: `upgrade_assistant.check_for_upgrades()`
3. Preview changes: `upgrade_assistant.get_upgrade_preview(version)`
4. Perform upgrade: `upgrade_assistant.perform_upgrade(version)`
5. Verify result: `health_checker.run_health_check()`

## Configuration Files

The system creates several metadata files:

- `.version`: Current configuration version
- `.metadata.json`: Detailed configuration metadata
- `.claude/backups/`: Backup storage directory
- `.claude/.validation_cache`: Validation cache (optional)

## Error Handling

### Validation Errors
- **Critical**: Configuration cannot be used
- **Error**: Major issues that should be fixed
- **Warning**: Minor issues that can wait
- **Info**: Informational messages

### Migration Errors
- **Failed**: Migration could not complete
- **Rollback Required**: Changes need to be undone
- **Partial**: Some changes applied successfully
- **Success**: All changes applied correctly

## Best Practices

### For Validation
1. Run health checks regularly
2. Address errors before warnings
3. Keep configurations up to date
4. Use auto-fix for safe issues
5. Review recommendations regularly

### For Migration
1. Always backup before major changes
2. Test in development first
3. Read upgrade previews carefully
4. Have rollback plan ready
5. Validate after migration

## Troubleshooting

### Common Issues

**Health check fails to run**
- Check if validation modules are installed
- Verify Python path includes tools directory
- Install dependencies: `pip install -r requirements.txt`

**Migration fails**
- Check disk space for backups
- Verify write permissions
- Review error messages in output
- Use backup to restore if needed

**Validation false positives**
- Update validation rules if needed
- Report issues to project maintainers
- Use manual overrides cautiously

### Debug Mode
Enable verbose output for troubleshooting:

```bash
python setup.py --health-check --verbose
```

## Contributing

The validation and migration system is designed to be extensible:

- Add new validators by extending `BaseValidator`
- Create custom migration rules in `UpgradeAssistant`
- Improve health check reports in `HealthChecker`
- Add new diff algorithms to `SmartDiffEngine`

## API Reference

### Validation Classes
- `BaseValidator`: Base class for all validators
- `ClaudeConfigValidator`: CLAUDE.md file validator
- `MCPServerValidator`: MCP server configuration validator
- `TemplateValidator`: Template structure validator
- `HealthChecker`: Comprehensive health checking

### Migration Classes
- `BaseMigrator`: Base class for migration operations
- `VersionManager`: Version detection and management
- `SmartDiffEngine`: Configuration change analysis
- `BackupManager`: Backup and restore operations
- `UpgradeAssistant`: Guided upgrade functionality

### Result Classes
- `ValidationResult`: Individual validation result
- `MigrationResult`: Migration operation result
- `BackupInfo`: Backup file information
- `ConfigChange`: Configuration change details

This system ensures your Claude Code configurations remain healthy, secure, and up-to-date with minimal manual intervention.