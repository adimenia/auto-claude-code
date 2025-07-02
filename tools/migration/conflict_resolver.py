"""Conflict resolution algorithms for configuration merge conflicts."""

import re
import json
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple, Union
from dataclasses import dataclass
from enum import Enum

from .base import BaseMigrator, MigrationResult, MigrationStatus


class ConflictType(Enum):
    """Types of configuration conflicts."""
    CONTENT_CONFLICT = "content"
    SECTION_CONFLICT = "section"
    JSON_MERGE_CONFLICT = "json_merge"
    LINE_CONFLICT = "line"
    STRUCTURE_CONFLICT = "structure"


@dataclass
class ConflictInfo:
    """Information about a configuration conflict."""
    conflict_type: ConflictType
    file_path: Path
    line_number: Optional[int]
    local_content: str
    remote_content: str
    description: str
    auto_resolvable: bool = False
    suggested_resolution: Optional[str] = None


@dataclass
class ConflictResolution:
    """Result of conflict resolution."""
    conflict_info: ConflictInfo
    resolution_strategy: str
    resolved_content: str
    confidence: float  # 0.0 to 1.0
    manual_review_required: bool = False


class ConflictResolver(BaseMigrator):
    """Resolves merge conflicts in configuration files."""
    
    def __init__(self, config_path: Path, backup_enabled: bool = True):
        super().__init__(config_path, backup_enabled)
        
        # Resolution strategies by conflict type
        self.resolution_strategies = {
            ConflictType.CONTENT_CONFLICT: [
                self._resolve_content_conflict_merge,
                self._resolve_content_conflict_prefer_local,
                self._resolve_content_conflict_prefer_remote
            ],
            ConflictType.SECTION_CONFLICT: [
                self._resolve_section_conflict_merge,
                self._resolve_section_conflict_append
            ],
            ConflictType.JSON_MERGE_CONFLICT: [
                self._resolve_json_conflict_deep_merge,
                self._resolve_json_conflict_prefer_structure
            ],
            ConflictType.LINE_CONFLICT: [
                self._resolve_line_conflict_smart_merge,
                self._resolve_line_conflict_context_aware
            ],
            ConflictType.STRUCTURE_CONFLICT: [
                self._resolve_structure_conflict_preserve_both,
                self._resolve_structure_conflict_prioritize
            ]
        }
    
    def detect_conflicts(self, local_path: Path, remote_path: Path) -> List[ConflictInfo]:
        """Detect conflicts between local and remote configurations.
        
        Args:
            local_path: Path to local configuration
            remote_path: Path to remote configuration
            
        Returns:
            List of detected conflicts
        """
        conflicts = []
        
        if not local_path.exists() or not remote_path.exists():
            return conflicts
        
        local_content = local_path.read_text(encoding='utf-8')
        remote_content = remote_path.read_text(encoding='utf-8')
        
        # Different conflict detection based on file type
        if local_path.suffix == '.json':
            conflicts.extend(self._detect_json_conflicts(local_path, local_content, remote_content))
        elif local_path.suffix == '.md':
            conflicts.extend(self._detect_markdown_conflicts(local_path, local_content, remote_content))
        else:
            conflicts.extend(self._detect_text_conflicts(local_path, local_content, remote_content))
        
        return conflicts
    
    def resolve_conflict(self, conflict_info: ConflictInfo, 
                        strategy: Optional[str] = None) -> ConflictResolution:
        """Resolve a single conflict.
        
        Args:
            conflict_info: Information about the conflict
            strategy: Specific resolution strategy to use
            
        Returns:
            Conflict resolution result
        """
        strategies = self.resolution_strategies.get(conflict_info.conflict_type, [])
        
        if strategy:
            # Try to find the specified strategy
            for strategy_func in strategies:
                if strategy_func.__name__.endswith(strategy):
                    return strategy_func(conflict_info)
        
        # Try strategies in order of preference
        best_resolution = None
        highest_confidence = 0.0
        
        for strategy_func in strategies:
            try:
                resolution = strategy_func(conflict_info)
                if resolution.confidence > highest_confidence:
                    highest_confidence = resolution.confidence
                    best_resolution = resolution
            except Exception:
                continue
        
        if best_resolution:
            return best_resolution
        
        # Fallback to manual resolution
        return ConflictResolution(
            conflict_info=conflict_info,
            resolution_strategy="manual",
            resolved_content=conflict_info.local_content,
            confidence=0.0,
            manual_review_required=True
        )
    
    def resolve_all_conflicts(self, conflicts: List[ConflictInfo], 
                             auto_resolve: bool = True) -> Dict[str, Any]:
        """Resolve all conflicts in a file or directory.
        
        Args:
            conflicts: List of conflicts to resolve
            auto_resolve: Whether to automatically resolve high-confidence conflicts
            
        Returns:
            Dictionary with resolution results
        """
        results = {
            'total_conflicts': len(conflicts),
            'auto_resolved': 0,
            'manual_required': 0,
            'failed_resolutions': 0,
            'resolutions': [],
            'files_modified': set()
        }
        
        for conflict in conflicts:
            try:
                resolution = self.resolve_conflict(conflict)
                results['resolutions'].append(resolution)
                
                if resolution.manual_review_required:
                    results['manual_required'] += 1
                elif auto_resolve and resolution.confidence >= 0.8:
                    # Apply high-confidence resolutions automatically
                    self._apply_resolution(resolution)
                    results['auto_resolved'] += 1
                    results['files_modified'].add(conflict.file_path)
                else:
                    results['manual_required'] += 1
                    
            except Exception as e:
                results['failed_resolutions'] += 1
                # Log error for debugging
                self.add_result(MigrationResult(
                    status=MigrationStatus.FAILED,
                    message=f"Failed to resolve conflict: {e}",
                    errors=[str(e)]
                ))
        
        return results
    
    # Conflict detection methods
    
    def _detect_json_conflicts(self, file_path: Path, local_content: str, 
                              remote_content: str) -> List[ConflictInfo]:
        """Detect conflicts in JSON files."""
        conflicts = []
        
        try:
            local_data = json.loads(local_content)
            remote_data = json.loads(remote_content)
            
            # Deep comparison for JSON conflicts
            json_conflicts = self._compare_json_objects(local_data, remote_data, file_path)
            conflicts.extend(json_conflicts)
            
        except json.JSONDecodeError:
            # If JSON is invalid, treat as text conflict
            conflicts.extend(self._detect_text_conflicts(file_path, local_content, remote_content))
        
        return conflicts
    
    def _detect_markdown_conflicts(self, file_path: Path, local_content: str, 
                                  remote_content: str) -> List[ConflictInfo]:
        """Detect conflicts in Markdown files."""
        conflicts = []
        
        # Split into sections based on headers
        local_sections = self._parse_markdown_sections(local_content)
        remote_sections = self._parse_markdown_sections(remote_content)
        
        # Compare sections
        all_sections = set(local_sections.keys()) | set(remote_sections.keys())
        
        for section in all_sections:
            local_section = local_sections.get(section, "")
            remote_section = remote_sections.get(section, "")
            
            if local_section != remote_section:
                conflicts.append(ConflictInfo(
                    conflict_type=ConflictType.SECTION_CONFLICT,
                    file_path=file_path,
                    line_number=None,
                    local_content=local_section,
                    remote_content=remote_section,
                    description=f"Section '{section}' differs between versions",
                    auto_resolvable=self._is_section_auto_resolvable(local_section, remote_section)
                ))
        
        return conflicts
    
    def _detect_text_conflicts(self, file_path: Path, local_content: str, 
                              remote_content: str) -> List[ConflictInfo]:
        """Detect conflicts in text files."""
        conflicts = []
        
        if local_content == remote_content:
            return conflicts
        
        # Line-by-line comparison
        local_lines = local_content.splitlines()
        remote_lines = remote_content.splitlines()
        
        # Use unified diff to identify conflicting regions
        import difflib
        diff = list(difflib.unified_diff(local_lines, remote_lines, lineterm=''))
        
        if diff:
            conflicts.append(ConflictInfo(
                conflict_type=ConflictType.CONTENT_CONFLICT,
                file_path=file_path,
                line_number=None,
                local_content=local_content,
                remote_content=remote_content,
                description="File content differs between versions",
                auto_resolvable=self._is_content_auto_resolvable(local_content, remote_content)
            ))
        
        return conflicts
    
    def _compare_json_objects(self, local_obj: Any, remote_obj: Any, 
                             file_path: Path, path: str = "") -> List[ConflictInfo]:
        """Compare JSON objects recursively."""
        conflicts = []
        
        if type(local_obj) != type(remote_obj):
            conflicts.append(ConflictInfo(
                conflict_type=ConflictType.JSON_MERGE_CONFLICT,
                file_path=file_path,
                line_number=None,
                local_content=json.dumps(local_obj, indent=2),
                remote_content=json.dumps(remote_obj, indent=2),
                description=f"Type mismatch at path '{path}'",
                auto_resolvable=False
            ))
            return conflicts
        
        if isinstance(local_obj, dict) and isinstance(remote_obj, dict):
            all_keys = set(local_obj.keys()) | set(remote_obj.keys())
            
            for key in all_keys:
                key_path = f"{path}.{key}" if path else key
                
                if key in local_obj and key in remote_obj:
                    conflicts.extend(self._compare_json_objects(
                        local_obj[key], remote_obj[key], file_path, key_path
                    ))
                elif key in local_obj:
                    conflicts.append(ConflictInfo(
                        conflict_type=ConflictType.JSON_MERGE_CONFLICT,
                        file_path=file_path,
                        line_number=None,
                        local_content=json.dumps({key: local_obj[key]}, indent=2),
                        remote_content="",
                        description=f"Key '{key_path}' exists only in local version",
                        auto_resolvable=True,
                        suggested_resolution="keep_local"
                    ))
                else:
                    conflicts.append(ConflictInfo(
                        conflict_type=ConflictType.JSON_MERGE_CONFLICT,
                        file_path=file_path,
                        line_number=None,
                        local_content="",
                        remote_content=json.dumps({key: remote_obj[key]}, indent=2),
                        description=f"Key '{key_path}' exists only in remote version",
                        auto_resolvable=True,
                        suggested_resolution="keep_remote"
                    ))
        
        elif isinstance(local_obj, list) and isinstance(remote_obj, list):
            if local_obj != remote_obj:
                conflicts.append(ConflictInfo(
                    conflict_type=ConflictType.JSON_MERGE_CONFLICT,
                    file_path=file_path,
                    line_number=None,
                    local_content=json.dumps(local_obj, indent=2),
                    remote_content=json.dumps(remote_obj, indent=2),
                    description=f"Array differs at path '{path}'",
                    auto_resolvable=self._is_array_auto_resolvable(local_obj, remote_obj)
                ))
        
        elif local_obj != remote_obj:
            conflicts.append(ConflictInfo(
                conflict_type=ConflictType.JSON_MERGE_CONFLICT,
                file_path=file_path,
                line_number=None,
                local_content=str(local_obj),
                remote_content=str(remote_obj),
                description=f"Value differs at path '{path}'",
                auto_resolvable=False
            ))
        
        return conflicts
    
    # Resolution strategy methods
    
    def _resolve_content_conflict_merge(self, conflict: ConflictInfo) -> ConflictResolution:
        """Attempt to merge conflicting content intelligently."""
        local_lines = conflict.local_content.splitlines()
        remote_lines = conflict.remote_content.splitlines()
        
        # Simple 3-way merge simulation
        merged_lines = []
        i, j = 0, 0
        
        while i < len(local_lines) and j < len(remote_lines):
            if local_lines[i] == remote_lines[j]:
                merged_lines.append(local_lines[i])
                i += 1
                j += 1
            else:
                # Try to find common content
                local_ahead = self._find_matching_line(local_lines[i:], remote_lines[j])
                remote_ahead = self._find_matching_line(remote_lines[j:], local_lines[i])
                
                if local_ahead is not None and (remote_ahead is None or local_ahead <= remote_ahead):
                    # Add local unique content
                    merged_lines.extend(local_lines[i:i+local_ahead])
                    i += local_ahead
                elif remote_ahead is not None:
                    # Add remote unique content
                    merged_lines.extend(remote_lines[j:j+remote_ahead])
                    j += remote_ahead
                else:
                    # No common content found, add both
                    merged_lines.append(f"# LOCAL: {local_lines[i]}")
                    merged_lines.append(f"# REMOTE: {remote_lines[j]}")
                    i += 1
                    j += 1
        
        # Add remaining lines
        merged_lines.extend(local_lines[i:])
        merged_lines.extend(remote_lines[j:])
        
        merged_content = '\n'.join(merged_lines)
        confidence = 0.7 if "# LOCAL:" not in merged_content else 0.3
        
        return ConflictResolution(
            conflict_info=conflict,
            resolution_strategy="content_merge",
            resolved_content=merged_content,
            confidence=confidence,
            manual_review_required=confidence < 0.5
        )
    
    def _resolve_content_conflict_prefer_local(self, conflict: ConflictInfo) -> ConflictResolution:
        """Resolve conflict by preferring local content."""
        return ConflictResolution(
            conflict_info=conflict,
            resolution_strategy="prefer_local",
            resolved_content=conflict.local_content,
            confidence=0.9,
            manual_review_required=False
        )
    
    def _resolve_content_conflict_prefer_remote(self, conflict: ConflictInfo) -> ConflictResolution:
        """Resolve conflict by preferring remote content."""
        return ConflictResolution(
            conflict_info=conflict,
            resolution_strategy="prefer_remote",
            resolved_content=conflict.remote_content,
            confidence=0.9,
            manual_review_required=False
        )
    
    def _resolve_section_conflict_merge(self, conflict: ConflictInfo) -> ConflictResolution:
        """Merge conflicting sections intelligently."""
        # Try to merge sections by combining unique content
        local_content = conflict.local_content.strip()
        remote_content = conflict.remote_content.strip()
        
        if not local_content:
            merged_content = remote_content
            confidence = 1.0
        elif not remote_content:
            merged_content = local_content
            confidence = 1.0
        else:
            # Combine both with clear separation
            merged_content = f"{local_content}\n\n{remote_content}"
            confidence = 0.6
        
        return ConflictResolution(
            conflict_info=conflict,
            resolution_strategy="section_merge",
            resolved_content=merged_content,
            confidence=confidence,
            manual_review_required=confidence < 0.8
        )
    
    def _resolve_section_conflict_append(self, conflict: ConflictInfo) -> ConflictResolution:
        """Resolve section conflict by appending remote content."""
        merged_content = f"{conflict.local_content}\n\n--- From Remote ---\n{conflict.remote_content}"
        
        return ConflictResolution(
            conflict_info=conflict,
            resolution_strategy="section_append",
            resolved_content=merged_content,
            confidence=0.8,
            manual_review_required=False
        )
    
    def _resolve_json_conflict_deep_merge(self, conflict: ConflictInfo) -> ConflictResolution:
        """Perform deep merge of JSON objects."""
        try:
            local_obj = json.loads(conflict.local_content) if conflict.local_content else {}
            remote_obj = json.loads(conflict.remote_content) if conflict.remote_content else {}
            
            merged_obj = self._deep_merge_json(local_obj, remote_obj)
            merged_content = json.dumps(merged_obj, indent=2)
            
            return ConflictResolution(
                conflict_info=conflict,
                resolution_strategy="json_deep_merge",
                resolved_content=merged_content,
                confidence=0.8,
                manual_review_required=False
            )
        
        except json.JSONDecodeError:
            return ConflictResolution(
                conflict_info=conflict,
                resolution_strategy="json_deep_merge",
                resolved_content=conflict.local_content,
                confidence=0.0,
                manual_review_required=True
            )
    
    def _resolve_json_conflict_prefer_structure(self, conflict: ConflictInfo) -> ConflictResolution:
        """Resolve JSON conflict by preferring the more structured version."""
        try:
            local_obj = json.loads(conflict.local_content) if conflict.local_content else {}
            remote_obj = json.loads(conflict.remote_content) if conflict.remote_content else {}
            
            # Prefer the version with more keys/structure
            local_complexity = self._calculate_json_complexity(local_obj)
            remote_complexity = self._calculate_json_complexity(remote_obj)
            
            if local_complexity >= remote_complexity:
                resolved_content = conflict.local_content
                confidence = 0.7
            else:
                resolved_content = conflict.remote_content
                confidence = 0.7
            
            return ConflictResolution(
                conflict_info=conflict,
                resolution_strategy="json_prefer_structure",
                resolved_content=resolved_content,
                confidence=confidence,
                manual_review_required=False
            )
        
        except json.JSONDecodeError:
            return ConflictResolution(
                conflict_info=conflict,
                resolution_strategy="json_prefer_structure",
                resolved_content=conflict.local_content,
                confidence=0.0,
                manual_review_required=True
            )
    
    def _resolve_line_conflict_smart_merge(self, conflict: ConflictInfo) -> ConflictResolution:
        """Smart merge of line conflicts."""
        return self._resolve_content_conflict_merge(conflict)
    
    def _resolve_line_conflict_context_aware(self, conflict: ConflictInfo) -> ConflictResolution:
        """Context-aware resolution of line conflicts."""
        return self._resolve_content_conflict_merge(conflict)
    
    def _resolve_structure_conflict_preserve_both(self, conflict: ConflictInfo) -> ConflictResolution:
        """Preserve both conflicting structures."""
        merged_content = f"{conflict.local_content}\n\n# Alternative structure:\n{conflict.remote_content}"
        
        return ConflictResolution(
            conflict_info=conflict,
            resolution_strategy="preserve_both",
            resolved_content=merged_content,
            confidence=0.6,
            manual_review_required=True
        )
    
    def _resolve_structure_conflict_prioritize(self, conflict: ConflictInfo) -> ConflictResolution:
        """Prioritize one structure over another."""
        # Simple heuristic: prefer the longer/more detailed structure
        if len(conflict.local_content) >= len(conflict.remote_content):
            return ConflictResolution(
                conflict_info=conflict,
                resolution_strategy="prioritize_local",
                resolved_content=conflict.local_content,
                confidence=0.7,
                manual_review_required=False
            )
        else:
            return ConflictResolution(
                conflict_info=conflict,
                resolution_strategy="prioritize_remote",
                resolved_content=conflict.remote_content,
                confidence=0.7,
                manual_review_required=False
            )
    
    # Helper methods
    
    def _parse_markdown_sections(self, content: str) -> Dict[str, str]:
        """Parse markdown content into sections."""
        sections = {}
        current_section = "header"
        current_content = []
        
        for line in content.splitlines():
            if line.startswith('#'):
                # Save previous section
                if current_content:
                    sections[current_section] = '\n'.join(current_content)
                
                # Start new section
                current_section = line.strip()
                current_content = []
            else:
                current_content.append(line)
        
        # Save last section
        if current_content:
            sections[current_section] = '\n'.join(current_content)
        
        return sections
    
    def _find_matching_line(self, lines: List[str], target: str) -> Optional[int]:
        """Find the index of a matching line."""
        for i, line in enumerate(lines):
            if line == target:
                return i
        return None
    
    def _deep_merge_json(self, local: Any, remote: Any) -> Any:
        """Deep merge two JSON objects."""
        if isinstance(local, dict) and isinstance(remote, dict):
            merged = local.copy()
            for key, value in remote.items():
                if key in merged:
                    merged[key] = self._deep_merge_json(merged[key], value)
                else:
                    merged[key] = value
            return merged
        elif isinstance(local, list) and isinstance(remote, list):
            # Merge lists by combining unique items
            return list(dict.fromkeys(local + remote))
        else:
            # For primitive types, prefer remote
            return remote
    
    def _calculate_json_complexity(self, obj: Any, depth: int = 0) -> int:
        """Calculate complexity score for JSON object."""
        if isinstance(obj, dict):
            return sum(1 + self._calculate_json_complexity(v, depth + 1) for v in obj.values())
        elif isinstance(obj, list):
            return sum(self._calculate_json_complexity(item, depth + 1) for item in obj)
        else:
            return 1
    
    def _is_section_auto_resolvable(self, local: str, remote: str) -> bool:
        """Check if section conflict is auto-resolvable."""
        # Simple heuristic: if one is empty or they're very similar
        if not local.strip() or not remote.strip():
            return True
        
        # Check similarity
        local_words = set(local.lower().split())
        remote_words = set(remote.lower().split())
        
        if local_words and remote_words:
            similarity = len(local_words & remote_words) / len(local_words | remote_words)
            return similarity > 0.8
        
        return False
    
    def _is_content_auto_resolvable(self, local: str, remote: str) -> bool:
        """Check if content conflict is auto-resolvable."""
        # Simple heuristics for auto-resolution
        local_lines = local.splitlines()
        remote_lines = remote.splitlines()
        
        # If one is significantly shorter, might be resolvable
        if len(local_lines) < 3 or len(remote_lines) < 3:
            return True
        
        # If very similar (>80% common lines)
        common_lines = set(local_lines) & set(remote_lines)
        total_lines = set(local_lines) | set(remote_lines)
        
        if total_lines:
            similarity = len(common_lines) / len(total_lines)
            return similarity > 0.8
        
        return False
    
    def _is_array_auto_resolvable(self, local: List[Any], remote: List[Any]) -> bool:
        """Check if array conflict is auto-resolvable."""
        # Arrays are auto-resolvable if they can be merged without losing data
        local_set = set(str(item) for item in local)
        remote_set = set(str(item) for item in remote)
        
        # If one is subset of another
        return local_set.issubset(remote_set) or remote_set.issubset(local_set)
    
    def _apply_resolution(self, resolution: ConflictResolution) -> None:
        """Apply a conflict resolution to the file."""
        file_path = resolution.conflict_info.file_path
        
        if self.backup_enabled:
            # Create backup before applying resolution
            backup_path = file_path.with_suffix(f"{file_path.suffix}.conflict_backup")
            if not backup_path.exists():  # Don't overwrite existing backups
                import shutil
                shutil.copy2(file_path, backup_path)
        
        # Write resolved content
        file_path.write_text(resolution.resolved_content, encoding='utf-8')
    
    # Required abstract methods from BaseMigrator
    def migrate(self, source_version: str, target_version: str) -> MigrationResult:
        """Not applicable for conflict resolver."""
        return MigrationResult(
            status=MigrationStatus.FAILED,
            message="Conflict resolver does not support version migration"
        )
    
    def can_migrate(self, source_version: str, target_version: str) -> bool:
        """Not applicable for conflict resolver."""
        return False