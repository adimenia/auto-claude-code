"""Smart configuration migration and upgrade system for auto-claude-code.

This module provides intelligent migration capabilities for Claude Code configurations,
including version detection, smart diffing, backup/restore, and conflict resolution.
"""

from .base import BaseMigrator, MigrationResult, MigrationStatus
from .version_manager import VersionManager, Version
from .backup_manager import BackupManager, BackupInfo
from .conflict_resolver import ConflictResolver, ConflictInfo, ConflictResolution, ConflictType
from .upgrade_assistant import UpgradeAssistant
from .diff_engine import SmartDiffEngine

__all__ = [
    "BaseMigrator",
    "MigrationResult",
    "MigrationStatus", 
    "VersionManager",
    "Version",
    "BackupManager",
    "BackupInfo",
    "ConflictResolver",
    "ConflictInfo",
    "ConflictResolution", 
    "ConflictType",
    "UpgradeAssistant",
    "SmartDiffEngine",
]