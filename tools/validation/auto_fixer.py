"""Auto-fix capabilities for common configuration issues."""

import re
import json
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass

from .base import ValidationResult, ValidationLevel


@dataclass
class AutoFixResult:
    """Result of an auto-fix operation."""
    success: bool
    description: str
    original_content: str
    fixed_content: str
    backup_created: bool = False
    backup_path: Optional[Path] = None


class AutoFixer:
    """Automatically fixes common configuration issues."""
    
    def __init__(self, config_path: Path, create_backups: bool = True):
        self.config_path = config_path
        self.create_backups = create_backups
        self.fix_results: List[AutoFixResult] = []
        
        # Define auto-fix rules
        self.fix_rules = {
            'claude_md': [
                self._fix_missing_headers,
                self._fix_malformed_includes,
                self._fix_long_lines,
                self._fix_trailing_whitespace,
                self._fix_missing_sections
            ],
            'mcp_json': [
                self._fix_mcp_json_syntax,
                self._fix_missing_mcp_fields,
                self._fix_invalid_server_paths
            ],
            'settings_json': [
                self._fix_json_syntax,
                self._fix_missing_required_settings,
                self._fix_deprecated_settings
            ]
        }
    
    def auto_fix_file(self, file_path: Path, validation_results: List[ValidationResult]) -> List[AutoFixResult]:
        """Auto-fix issues in a specific file.
        
        Args:
            file_path: Path to the file to fix
            validation_results: Validation results for the file
            
        Returns:
            List of auto-fix results
        """
        if not file_path.exists():
            return []
        
        results = []
        original_content = file_path.read_text(encoding='utf-8')
        current_content = original_content
        
        # Determine file type and applicable rules
        file_type = self._get_file_type(file_path)
        if file_type not in self.fix_rules:
            return []
        
        # Create backup if requested
        backup_path = None
        if self.create_backups:
            backup_path = self._create_backup(file_path, original_content)
        
        # Apply auto-fix rules
        for fix_rule in self.fix_rules[file_type]:
            try:
                fixed_content, fix_applied, fix_description = fix_rule(
                    current_content, file_path, validation_results
                )
                
                if fix_applied:
                    result = AutoFixResult(
                        success=True,
                        description=fix_description,
                        original_content=current_content,
                        fixed_content=fixed_content,
                        backup_created=backup_path is not None,
                        backup_path=backup_path
                    )
                    results.append(result)
                    current_content = fixed_content
                    
            except Exception as e:
                result = AutoFixResult(
                    success=False,
                    description=f"Failed to apply fix: {e}",
                    original_content=current_content,
                    fixed_content=current_content
                )
                results.append(result)
        
        # Write fixed content if changes were made
        if current_content != original_content:
            file_path.write_text(current_content, encoding='utf-8')
        
        self.fix_results.extend(results)
        return results
    
    def _get_file_type(self, file_path: Path) -> str:
        """Determine the file type for auto-fix rules."""
        if file_path.name == 'CLAUDE.md':
            return 'claude_md'
        elif file_path.name == '.mcp.json':
            return 'mcp_json'
        elif file_path.name.endswith('settings.json'):
            return 'settings_json'
        return 'unknown'
    
    def _create_backup(self, file_path: Path, content: str) -> Path:
        """Create a backup of the file before fixing."""
        backup_dir = self.config_path / '.claude' / 'autofix_backups'
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"{file_path.name}.{timestamp}.backup"
        backup_path = backup_dir / backup_name
        
        backup_path.write_text(content, encoding='utf-8')
        return backup_path
    
    # CLAUDE.md auto-fix rules
    
    def _fix_missing_headers(self, content: str, file_path: Path, 
                            validation_results: List[ValidationResult]) -> Tuple[str, bool, str]:
        """Fix missing required headers in CLAUDE.md."""
        required_headers = [
            '# CLAUDE.md',
            '## Core Configuration',
            '## Development Workflow'
        ]
        
        lines = content.split('\n')
        missing_headers = []
        
        for header in required_headers:
            if not any(line.strip().startswith(header) for line in lines):
                missing_headers.append(header)
        
        if not missing_headers:
            return content, False, ""
        
        # Add missing headers at appropriate positions
        new_lines = lines[:]
        
        if '# CLAUDE.md' in missing_headers:
            new_lines.insert(0, '# CLAUDE.md - Configuration\n')
        
        if '## Core Configuration' in missing_headers:
            # Add after main header
            insert_pos = 1 if new_lines[0].startswith('#') else 0
            new_lines.insert(insert_pos, '\n## Core Configuration\n')
        
        if '## Development Workflow' in missing_headers:
            new_lines.append('\n## Development Workflow\n')
        
        fixed_content = '\n'.join(new_lines)
        description = f"Added missing headers: {', '.join(missing_headers)}"
        
        return fixed_content, True, description
    
    def _fix_malformed_includes(self, content: str, file_path: Path,
                               validation_results: List[ValidationResult]) -> Tuple[str, bool, str]:
        """Fix malformed @include references."""
        include_pattern = r'@include\s+([^\s#]+)(?:#([^\s]+))?'
        fixes_made = []
        
        def fix_include(match):
            file_ref = match.group(1)
            section_ref = match.group(2) if match.group(2) else None
            
            # Fix common path issues
            if not file_ref.endswith('.yml') and not file_ref.endswith('.yaml'):
                if '/' in file_ref:
                    file_ref = file_ref + '.yml'
            
            # Fix malformed section references
            if section_ref:
                # Ensure section reference follows proper format
                section_ref = section_ref.replace(' ', '_')
                fixes_made.append(f"Fixed section reference: {section_ref}")
                return f"@include {file_ref}#{section_ref}"
            else:
                return f"@include {file_ref}"
        
        fixed_content = re.sub(include_pattern, fix_include, content)
        description = '; '.join(fixes_made) if fixes_made else ""
        
        return fixed_content, len(fixes_made) > 0, description
    
    def _fix_long_lines(self, content: str, file_path: Path,
                       validation_results: List[ValidationResult]) -> Tuple[str, bool, str]:
        """Fix lines that are too long."""
        max_length = 100
        lines = content.split('\n')
        fixed_lines = []
        fixes_made = 0
        
        for line in lines:
            if len(line) > max_length and not line.strip().startswith('#'):
                # Try to break long lines at sensible points
                if ' - ' in line:
                    # Break at list items
                    parts = line.split(' - ')
                    fixed_lines.append(parts[0])
                    for part in parts[1:]:
                        fixed_lines.append(f"  - {part}")
                    fixes_made += 1
                elif ',' in line and not line.strip().startswith('```'):
                    # Break at commas for non-code blocks
                    words = line.split(',')
                    current_line = words[0]
                    for word in words[1:]:
                        if len(current_line + ',' + word) > max_length:
                            fixed_lines.append(current_line + ',')
                            current_line = '  ' + word.strip()
                        else:
                            current_line += ',' + word
                    fixed_lines.append(current_line)
                    fixes_made += 1
                else:
                    fixed_lines.append(line)
            else:
                fixed_lines.append(line)
        
        fixed_content = '\n'.join(fixed_lines)
        description = f"Fixed {fixes_made} long lines" if fixes_made > 0 else ""
        
        return fixed_content, fixes_made > 0, description
    
    def _fix_trailing_whitespace(self, content: str, file_path: Path,
                                validation_results: List[ValidationResult]) -> Tuple[str, bool, str]:
        """Remove trailing whitespace from lines."""
        lines = content.split('\n')
        fixed_lines = [line.rstrip() for line in lines]
        
        changes_made = sum(1 for i, line in enumerate(lines) if line != fixed_lines[i])
        fixed_content = '\n'.join(fixed_lines)
        description = f"Removed trailing whitespace from {changes_made} lines" if changes_made > 0 else ""
        
        return fixed_content, changes_made > 0, description
    
    def _fix_missing_sections(self, content: str, file_path: Path,
                             validation_results: List[ValidationResult]) -> Tuple[str, bool, str]:
        """Add recommended sections that are missing."""
        recommended_sections = [
            '## Project Overview',
            '## Development Standards',
            '## Command Usage'
        ]
        
        missing_sections = []
        for section in recommended_sections:
            if section not in content:
                missing_sections.append(section)
        
        if not missing_sections:
            return content, False, ""
        
        # Add missing sections at the end
        additions = [f"\n{section}\n\nTODO: Add content for this section.\n" for section in missing_sections]
        fixed_content = content + '\n'.join(additions)
        description = f"Added recommended sections: {', '.join(missing_sections)}"
        
        return fixed_content, True, description
    
    # MCP JSON auto-fix rules
    
    def _fix_mcp_json_syntax(self, content: str, file_path: Path,
                            validation_results: List[ValidationResult]) -> Tuple[str, bool, str]:
        """Fix common JSON syntax issues in MCP configuration."""
        try:
            # Try to parse and reformat JSON
            data = json.loads(content)
            fixed_content = json.dumps(data, indent=2, ensure_ascii=False)
            return fixed_content, True, "Fixed JSON formatting"
        except json.JSONDecodeError as e:
            # Try to fix common JSON issues
            fixed_content = content
            fixes_made = []
            
            # Fix trailing commas
            fixed_content = re.sub(r',(\s*[}\]])', r'\1', fixed_content)
            if fixed_content != content:
                fixes_made.append("removed trailing commas")
            
            # Fix unquoted keys
            fixed_content = re.sub(r'(\w+):', r'"\1":', fixed_content)
            if len(fixes_made) == 0 and fixed_content != content:
                fixes_made.append("quoted unquoted keys")
            
            description = f"Fixed JSON syntax: {', '.join(fixes_made)}" if fixes_made else ""
            return fixed_content, len(fixes_made) > 0, description
    
    def _fix_missing_mcp_fields(self, content: str, file_path: Path,
                               validation_results: List[ValidationResult]) -> Tuple[str, bool, str]:
        """Add missing required fields to MCP configuration."""
        try:
            data = json.loads(content)
            fixes_made = []
            
            # Ensure mcpServers exists
            if 'mcpServers' not in data:
                data['mcpServers'] = {}
                fixes_made.append("added mcpServers section")
            
            # Check each server for required fields
            for server_name, server_config in data.get('mcpServers', {}).items():
                if 'command' not in server_config:
                    server_config['command'] = 'python'
                    fixes_made.append(f"added default command for {server_name}")
                
                if 'args' not in server_config:
                    server_config['args'] = []
                    fixes_made.append(f"added empty args for {server_name}")
            
            if fixes_made:
                fixed_content = json.dumps(data, indent=2, ensure_ascii=False)
                description = f"Fixed MCP fields: {', '.join(fixes_made)}"
                return fixed_content, True, description
            
        except json.JSONDecodeError:
            pass
        
        return content, False, ""
    
    def _fix_invalid_server_paths(self, content: str, file_path: Path,
                                 validation_results: List[ValidationResult]) -> Tuple[str, bool, str]:
        """Fix invalid server paths in MCP configuration."""
        try:
            data = json.loads(content)
            fixes_made = []
            
            for server_name, server_config in data.get('mcpServers', {}).items():
                args = server_config.get('args', [])
                for i, arg in enumerate(args):
                    if isinstance(arg, str) and arg.endswith('.py'):
                        # Check if the path exists
                        path = Path(arg)
                        if not path.is_absolute():
                            # Try to make it relative to config directory
                            potential_path = self.config_path / arg
                            if potential_path.exists():
                                args[i] = str(potential_path.resolve())
                                fixes_made.append(f"fixed path for {server_name}")
            
            if fixes_made:
                fixed_content = json.dumps(data, indent=2, ensure_ascii=False)
                description = f"Fixed server paths: {', '.join(fixes_made)}"
                return fixed_content, True, description
            
        except json.JSONDecodeError:
            pass
        
        return content, False, ""
    
    # Settings JSON auto-fix rules
    
    def _fix_json_syntax(self, content: str, file_path: Path,
                        validation_results: List[ValidationResult]) -> Tuple[str, bool, str]:
        """Fix JSON syntax issues in settings files."""
        return self._fix_mcp_json_syntax(content, file_path, validation_results)
    
    def _fix_missing_required_settings(self, content: str, file_path: Path,
                                      validation_results: List[ValidationResult]) -> Tuple[str, bool, str]:
        """Add missing required settings."""
        try:
            data = json.loads(content)
            fixes_made = []
            
            # Required settings for Claude Code
            required_settings = {
                'claude.model': 'claude-3-5-sonnet-20241022',
                'claude.temperature': 0.0,
                'claude.maxTokens': 4096
            }
            
            for setting, default_value in required_settings.items():
                if setting not in data:
                    data[setting] = default_value
                    fixes_made.append(f"added {setting}")
            
            if fixes_made:
                fixed_content = json.dumps(data, indent=2, ensure_ascii=False)
                description = f"Added required settings: {', '.join(fixes_made)}"
                return fixed_content, True, description
            
        except json.JSONDecodeError:
            pass
        
        return content, False, ""
    
    def _fix_deprecated_settings(self, content: str, file_path: Path,
                                validation_results: List[ValidationResult]) -> Tuple[str, bool, str]:
        """Remove or update deprecated settings."""
        try:
            data = json.loads(content)
            fixes_made = []
            
            # Deprecated settings to remove
            deprecated_settings = [
                'claude.legacy.mode',
                'claude.beta.features',
                'claude.experimental.ui'
            ]
            
            for setting in deprecated_settings:
                if setting in data:
                    del data[setting]
                    fixes_made.append(f"removed deprecated {setting}")
            
            if fixes_made:
                fixed_content = json.dumps(data, indent=2, ensure_ascii=False)
                description = f"Removed deprecated settings: {', '.join(fixes_made)}"
                return fixed_content, True, description
            
        except json.JSONDecodeError:
            pass
        
        return content, False, ""
    
    def get_fixable_issues(self, validation_results: List[ValidationResult]) -> List[ValidationResult]:
        """Get list of issues that can be automatically fixed.
        
        Args:
            validation_results: List of validation results
            
        Returns:
            List of fixable validation results
        """
        fixable_issues = []
        
        fixable_keywords = [
            'trailing whitespace',
            'long line',
            'missing header',
            'malformed include',
            'json syntax',
            'missing field',
            'invalid path',
            'deprecated setting'
        ]
        
        for result in validation_results:
            if result.level in [ValidationLevel.WARNING, ValidationLevel.ERROR]:
                message_lower = result.message.lower()
                if any(keyword in message_lower for keyword in fixable_keywords):
                    fixable_issues.append(result)
        
        return fixable_issues
    
    def get_fix_summary(self) -> Dict[str, Any]:
        """Get summary of all auto-fix operations performed.
        
        Returns:
            Dictionary with fix summary information
        """
        total_fixes = len(self.fix_results)
        successful_fixes = sum(1 for result in self.fix_results if result.success)
        failed_fixes = total_fixes - successful_fixes
        
        return {
            'total_fixes_attempted': total_fixes,
            'successful_fixes': successful_fixes,
            'failed_fixes': failed_fixes,
            'success_rate': (successful_fixes / total_fixes * 100) if total_fixes > 0 else 0,
            'fixes_by_type': self._group_fixes_by_type(),
            'backups_created': sum(1 for result in self.fix_results if result.backup_created)
        }
    
    def _group_fixes_by_type(self) -> Dict[str, int]:
        """Group fixes by type for summary."""
        fix_types = {}
        
        for result in self.fix_results:
            if result.success:
                # Extract fix type from description
                desc = result.description.lower()
                if 'header' in desc:
                    fix_types['headers'] = fix_types.get('headers', 0) + 1
                elif 'whitespace' in desc:
                    fix_types['whitespace'] = fix_types.get('whitespace', 0) + 1
                elif 'json' in desc:
                    fix_types['json_syntax'] = fix_types.get('json_syntax', 0) + 1
                elif 'include' in desc:
                    fix_types['includes'] = fix_types.get('includes', 0) + 1
                elif 'line' in desc:
                    fix_types['line_length'] = fix_types.get('line_length', 0) + 1
                else:
                    fix_types['other'] = fix_types.get('other', 0) + 1
        
        return fix_types