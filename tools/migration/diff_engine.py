"""Smart diff engine for configuration changes."""

import difflib
import json
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple, Union
from dataclasses import dataclass
from enum import Enum
import re


class ChangeType(Enum):
    """Types of configuration changes."""
    ADDED = "added"
    REMOVED = "removed"
    MODIFIED = "modified"
    MOVED = "moved"
    CONFLICT = "conflict"


@dataclass
class ConfigChange:
    """Represents a configuration change."""
    change_type: ChangeType
    file_path: Path
    old_content: Optional[str] = None
    new_content: Optional[str] = None
    line_number: Optional[int] = None
    section: Optional[str] = None
    description: str = ""
    impact_level: str = "medium"  # low, medium, high, critical
    auto_mergeable: bool = False
    
    def __post_init__(self):
        if not self.description:
            self.description = self._generate_description()
    
    def _generate_description(self) -> str:
        """Generate a description for the change."""
        if self.change_type == ChangeType.ADDED:
            return f"Added new content to {self.file_path.name}"
        elif self.change_type == ChangeType.REMOVED:
            return f"Removed content from {self.file_path.name}"
        elif self.change_type == ChangeType.MODIFIED:
            return f"Modified content in {self.file_path.name}"
        elif self.change_type == ChangeType.MOVED:
            return f"Moved content in {self.file_path.name}"
        elif self.change_type == ChangeType.CONFLICT:
            return f"Conflict detected in {self.file_path.name}"
        return "Unknown change"


class SmartDiffEngine:
    """Smart diff engine for configuration changes."""
    
    def __init__(self):
        """Initialize diff engine."""
        self.changes: List[ConfigChange] = []
        self.critical_sections = {
            "Core Configuration",
            "MCP Integration", 
            "Security Standards",
            "mcpServers"
        }
    
    def compare_configurations(self, old_path: Path, new_path: Path) -> List[ConfigChange]:
        """Compare two configuration directories.
        
        Args:
            old_path: Path to old configuration
            new_path: Path to new configuration
            
        Returns:
            List of detected changes
        """
        self.changes.clear()
        
        # Get all configuration files
        old_files = self._get_config_files(old_path)
        new_files = self._get_config_files(new_path)
        
        all_files = set(old_files.keys()) | set(new_files.keys())
        
        for file_name in all_files:
            old_file_path = old_files.get(file_name)
            new_file_path = new_files.get(file_name)
            
            if old_file_path and new_file_path:
                # File exists in both - compare content
                self._compare_file_content(old_file_path, new_file_path)
            elif old_file_path and not new_file_path:
                # File removed
                self._add_file_removed(old_file_path)
            elif new_file_path and not old_file_path:
                # File added
                self._add_file_added(new_file_path)
        
        return self.changes
    
    def _get_config_files(self, config_path: Path) -> Dict[str, Path]:
        """Get all configuration files in a directory.
        
        Args:
            config_path: Configuration directory path
            
        Returns:
            Dictionary mapping relative paths to absolute paths
        """
        files = {}
        
        if not config_path.exists():
            return files
        
        # Include main config files
        for pattern in ["CLAUDE.md", "settings.json", "*.yml", "*.yaml"]:
            for file_path in config_path.glob(pattern):
                if file_path.is_file():
                    rel_path = file_path.relative_to(config_path)
                    files[str(rel_path)] = file_path
        
        # Include command files
        commands_dir = config_path / "commands"
        if commands_dir.exists():
            for file_path in commands_dir.rglob("*.md"):
                rel_path = file_path.relative_to(config_path)
                files[str(rel_path)] = file_path
        
        return files
    
    def _compare_file_content(self, old_file: Path, new_file: Path) -> None:
        """Compare content of two files.
        
        Args:
            old_file: Old file path
            new_file: New file path
        """
        try:
            old_content = old_file.read_text(encoding='utf-8')
            new_content = new_file.read_text(encoding='utf-8')
        except IOError:
            return
        
        if old_content == new_content:
            return  # No changes
        
        # Determine file type and compare accordingly
        if old_file.suffix == '.json':
            self._compare_json_content(old_file, old_content, new_content)
        elif old_file.suffix in ['.md', '.yml', '.yaml']:
            self._compare_text_content(old_file, old_content, new_content)
    
    def _compare_json_content(self, file_path: Path, old_content: str, new_content: str) -> None:
        """Compare JSON configuration content.
        
        Args:
            file_path: File path
            old_content: Old JSON content
            new_content: New JSON content
        """
        try:
            old_data = json.loads(old_content)
            new_data = json.loads(new_content)
        except json.JSONDecodeError:
            # Fallback to text comparison
            self._compare_text_content(file_path, old_content, new_content)
            return
        
        self._compare_json_objects(file_path, old_data, new_data)
    
    def _compare_json_objects(self, file_path: Path, old_obj: Any, new_obj: Any, 
                             path: str = "") -> None:
        """Recursively compare JSON objects.
        
        Args:
            file_path: File path
            old_obj: Old JSON object
            new_obj: New JSON object
            path: Current path in JSON structure
        """
        if isinstance(old_obj, dict) and isinstance(new_obj, dict):
            # Compare dictionaries
            all_keys = set(old_obj.keys()) | set(new_obj.keys())
            
            for key in all_keys:
                current_path = f"{path}.{key}" if path else key
                
                if key in old_obj and key in new_obj:
                    if old_obj[key] != new_obj[key]:
                        self._compare_json_objects(file_path, old_obj[key], new_obj[key], current_path)
                elif key in old_obj:
                    # Key removed
                    self._add_json_change(file_path, ChangeType.REMOVED, current_path, old_obj[key], None)
                else:
                    # Key added
                    self._add_json_change(file_path, ChangeType.ADDED, current_path, None, new_obj[key])
        
        elif isinstance(old_obj, list) and isinstance(new_obj, list):
            # Compare lists
            if old_obj != new_obj:
                self._add_json_change(file_path, ChangeType.MODIFIED, path, old_obj, new_obj)
        
        else:
            # Compare primitives
            if old_obj != new_obj:
                self._add_json_change(file_path, ChangeType.MODIFIED, path, old_obj, new_obj)
    
    def _add_json_change(self, file_path: Path, change_type: ChangeType, 
                        json_path: str, old_value: Any, new_value: Any) -> None:
        """Add a JSON-specific change.
        
        Args:
            file_path: File path
            change_type: Type of change
            json_path: Path within JSON structure
            old_value: Old value
            new_value: New value
        """
        # Determine impact level
        impact_level = self._assess_json_impact(json_path, old_value, new_value)
        
        change = ConfigChange(
            change_type=change_type,
            file_path=file_path,
            old_content=json.dumps(old_value, indent=2) if old_value is not None else None,
            new_content=json.dumps(new_value, indent=2) if new_value is not None else None,
            section=json_path,
            impact_level=impact_level,
            auto_mergeable=self._is_json_auto_mergeable(json_path, change_type)
        )
        
        self.changes.append(change)
    
    def _assess_json_impact(self, json_path: str, old_value: Any, new_value: Any) -> str:
        """Assess impact level of JSON change.
        
        Args:
            json_path: Path in JSON structure
            old_value: Old value
            new_value: New value
            
        Returns:
            Impact level string
        """
        # Critical changes
        if "mcpServers" in json_path:
            return "critical"
        
        # High impact changes
        high_impact_paths = ["version", "environment", "security"]
        if any(path in json_path.lower() for path in high_impact_paths):
            return "high"
        
        # Medium impact changes
        medium_impact_paths = ["settings", "config", "options"]
        if any(path in json_path.lower() for path in medium_impact_paths):
            return "medium"
        
        return "low"
    
    def _is_json_auto_mergeable(self, json_path: str, change_type: ChangeType) -> bool:
        """Check if JSON change is auto-mergeable.
        
        Args:
            json_path: Path in JSON structure
            change_type: Type of change
            
        Returns:
            True if auto-mergeable
        """
        # Never auto-merge critical sections
        if "mcpServers" in json_path:
            return False
        
        # Only auto-merge additions of non-critical settings
        if change_type == ChangeType.ADDED:
            safe_additions = ["description", "author", "tags", "metadata"]
            return any(path in json_path.lower() for path in safe_additions)
        
        return False
    
    def _compare_text_content(self, file_path: Path, old_content: str, new_content: str) -> None:
        """Compare text-based configuration content.
        
        Args:
            file_path: File path
            old_content: Old content
            new_content: New content
        """
        old_lines = old_content.splitlines()
        new_lines = new_content.splitlines()
        
        # Use difflib to find differences
        differ = difflib.unified_diff(
            old_lines, new_lines,
            fromfile=f"old/{file_path.name}",
            tofile=f"new/{file_path.name}",
            lineterm="",
            n=3
        )
        
        diff_lines = list(differ)
        if not diff_lines:
            return
        
        # Parse diff output and create changes
        self._parse_unified_diff(file_path, diff_lines, old_content, new_content)
    
    def _parse_unified_diff(self, file_path: Path, diff_lines: List[str], 
                           old_content: str, new_content: str) -> None:
        """Parse unified diff output and create changes.
        
        Args:
            file_path: File path
            diff_lines: Unified diff lines
            old_content: Old file content
            new_content: New file content
        """
        current_section = None
        line_number = 0
        
        for line in diff_lines:
            if line.startswith('@@'):
                # Extract line number from hunk header
                match = re.search(r'\+(\d+)', line)
                if match:
                    line_number = int(match.group(1))
            
            elif line.startswith('-'):
                # Line removed
                content = line[1:]
                section = self._detect_section(content)
                impact = self._assess_text_impact(content, section)
                
                change = ConfigChange(
                    change_type=ChangeType.REMOVED,
                    file_path=file_path,
                    old_content=content,
                    line_number=line_number,
                    section=section,
                    impact_level=impact,
                    auto_mergeable=False
                )
                self.changes.append(change)
            
            elif line.startswith('+'):
                # Line added
                content = line[1:]
                section = self._detect_section(content)
                impact = self._assess_text_impact(content, section)
                
                change = ConfigChange(
                    change_type=ChangeType.ADDED,
                    file_path=file_path,
                    new_content=content,
                    line_number=line_number,
                    section=section,
                    impact_level=impact,
                    auto_mergeable=self._is_text_auto_mergeable(content, section)
                )
                self.changes.append(change)
                line_number += 1
            
            elif not line.startswith(' ') and not line.startswith('@@'):
                line_number += 1
    
    def _detect_section(self, content: str) -> Optional[str]:
        """Detect section from content line.
        
        Args:
            content: Content line
            
        Returns:
            Section name if detected
        """
        # Detect markdown headers
        if content.strip().startswith('#'):
            return content.strip().lstrip('#').strip()
        
        # Detect @include references
        if '@include' in content:
            match = re.search(r'@include\s+([^\s#]+)', content)
            if match:
                return f"Include: {match.group(1)}"
        
        # Detect YAML section markers
        if content.strip().endswith(':') and not content.strip().startswith(' '):
            return content.strip().rstrip(':')
        
        return None
    
    def _assess_text_impact(self, content: str, section: Optional[str]) -> str:
        """Assess impact level of text change.
        
        Args:
            content: Content line
            section: Section name
            
        Returns:
            Impact level string
        """
        # Critical sections
        if section and any(critical in section for critical in self.critical_sections):
            return "critical"
        
        # High impact indicators
        high_impact_keywords = ["security", "auth", "credentials", "secret", "key"]
        if any(keyword in content.lower() for keyword in high_impact_keywords):
            return "high"
        
        # Medium impact indicators
        medium_impact_keywords = ["config", "setting", "server", "database"]
        if any(keyword in content.lower() for keyword in medium_impact_keywords):
            return "medium"
        
        return "low"
    
    def _is_text_auto_mergeable(self, content: str, section: Optional[str]) -> bool:
        """Check if text change is auto-mergeable.
        
        Args:
            content: Content line
            section: Section name
            
        Returns:
            True if auto-mergeable
        """
        # Never auto-merge critical sections
        if section and any(critical in section for critical in self.critical_sections):
            return False
        
        # Safe to auto-merge comments and documentation
        safe_indicators = ["#", "//", "<!--", "description", "example", "note"]
        return any(indicator in content.lower() for indicator in safe_indicators)
    
    def _add_file_removed(self, file_path: Path) -> None:
        """Add file removal change.
        
        Args:
            file_path: Removed file path
        """
        change = ConfigChange(
            change_type=ChangeType.REMOVED,
            file_path=file_path,
            impact_level="high",
            auto_mergeable=False,
            description=f"File removed: {file_path.name}"
        )
        self.changes.append(change)
    
    def _add_file_added(self, file_path: Path) -> None:
        """Add file addition change.
        
        Args:
            file_path: Added file path
        """
        change = ConfigChange(
            change_type=ChangeType.ADDED,
            file_path=file_path,
            impact_level="medium",
            auto_mergeable=self._is_file_auto_mergeable(file_path),
            description=f"File added: {file_path.name}"
        )
        self.changes.append(change)
    
    def _is_file_auto_mergeable(self, file_path: Path) -> bool:
        """Check if new file is auto-mergeable.
        
        Args:
            file_path: File path
            
        Returns:
            True if auto-mergeable
        """
        # Safe to auto-merge documentation files
        safe_extensions = ['.md', '.txt', '.rst']
        if file_path.suffix.lower() in safe_extensions:
            # But not core configuration files
            if file_path.name.lower() in ['claude.md', 'readme.md']:
                return False
            return True
        
        return False
    
    def get_changes_by_impact(self, impact_level: str) -> List[ConfigChange]:
        """Get changes by impact level.
        
        Args:
            impact_level: Impact level to filter by
            
        Returns:
            List of changes with specified impact level
        """
        return [change for change in self.changes if change.impact_level == impact_level]
    
    def get_auto_mergeable_changes(self) -> List[ConfigChange]:
        """Get changes that can be auto-merged.
        
        Returns:
            List of auto-mergeable changes
        """
        return [change for change in self.changes if change.auto_mergeable]
    
    def get_conflict_changes(self) -> List[ConfigChange]:
        """Get changes that represent conflicts.
        
        Returns:
            List of conflict changes
        """
        return [change for change in self.changes if change.change_type == ChangeType.CONFLICT]
    
    def generate_summary(self) -> Dict[str, Any]:
        """Generate summary of changes.
        
        Returns:
            Summary dictionary
        """
        summary = {
            "total_changes": len(self.changes),
            "by_type": {
                "added": len([c for c in self.changes if c.change_type == ChangeType.ADDED]),
                "removed": len([c for c in self.changes if c.change_type == ChangeType.REMOVED]),
                "modified": len([c for c in self.changes if c.change_type == ChangeType.MODIFIED]),
                "moved": len([c for c in self.changes if c.change_type == ChangeType.MOVED]),
                "conflicts": len([c for c in self.changes if c.change_type == ChangeType.CONFLICT])
            },
            "by_impact": {
                "critical": len(self.get_changes_by_impact("critical")),
                "high": len(self.get_changes_by_impact("high")),
                "medium": len(self.get_changes_by_impact("medium")),
                "low": len(self.get_changes_by_impact("low"))
            },
            "auto_mergeable": len(self.get_auto_mergeable_changes()),
            "requires_review": len([c for c in self.changes if not c.auto_mergeable])
        }
        
        return summary