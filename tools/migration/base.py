"""Base classes for the migration system."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import List, Optional, Any, Dict
from datetime import datetime


class MigrationStatus(Enum):
    """Migration operation status."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    SUCCESS = "success"
    FAILED = "failed"
    ROLLBACK_REQUIRED = "rollback_required"


@dataclass
class MigrationResult:
    """Result of a migration operation."""
    status: MigrationStatus
    message: str
    source_version: Optional[str] = None
    target_version: Optional[str] = None
    files_affected: List[Path] = None
    backup_path: Optional[Path] = None
    errors: List[str] = None
    warnings: List[str] = None
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.files_affected is None:
            self.files_affected = []
        if self.errors is None:
            self.errors = []
        if self.warnings is None:
            self.warnings = []
        if self.timestamp is None:
            self.timestamp = datetime.now()
    
    @property
    def is_success(self) -> bool:
        """Check if migration was successful."""
        return self.status == MigrationStatus.SUCCESS
    
    @property
    def has_errors(self) -> bool:
        """Check if migration has errors."""
        return len(self.errors) > 0 or self.status == MigrationStatus.FAILED
    
    @property
    def needs_rollback(self) -> bool:
        """Check if migration needs rollback."""
        return self.status == MigrationStatus.ROLLBACK_REQUIRED


class BaseMigrator(ABC):
    """Base class for all migration operations."""
    
    def __init__(self, config_path: Path, backup_enabled: bool = True):
        """Initialize migrator.
        
        Args:
            config_path: Path to configuration directory
            backup_enabled: Whether to create backups before migration
        """
        self.config_path = config_path
        self.backup_enabled = backup_enabled
        self.results: List[MigrationResult] = []
    
    @abstractmethod
    def migrate(self, source_version: str, target_version: str) -> MigrationResult:
        """Perform migration between versions.
        
        Args:
            source_version: Current version
            target_version: Target version
            
        Returns:
            Migration result
        """
        pass
    
    @abstractmethod
    def can_migrate(self, source_version: str, target_version: str) -> bool:
        """Check if migration is possible between versions.
        
        Args:
            source_version: Current version
            target_version: Target version
            
        Returns:
            True if migration is supported
        """
        pass
    
    def add_result(self, result: MigrationResult) -> None:
        """Add a migration result.
        
        Args:
            result: Migration result to add
        """
        self.results.append(result)
    
    def clear_results(self) -> None:
        """Clear all migration results."""
        self.results.clear()
    
    def get_failed_migrations(self) -> List[MigrationResult]:
        """Get failed migration results."""
        return [r for r in self.results if r.has_errors]
    
    def get_successful_migrations(self) -> List[MigrationResult]:
        """Get successful migration results.""" 
        return [r for r in self.results if r.is_success]