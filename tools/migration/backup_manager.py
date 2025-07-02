"""Backup and restore functionality for configuration management."""

import shutil
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import zipfile
import tempfile

from .base import BaseMigrator, MigrationResult, MigrationStatus


@dataclass
class BackupInfo:
    """Information about a configuration backup."""
    name: str
    timestamp: datetime
    path: Path
    size_bytes: int
    description: str
    files_count: int
    version: Optional[str] = None
    checksum: Optional[str] = None


class BackupManager(BaseMigrator):
    """Manages configuration backups and restores."""
    
    def __init__(self, config_path: Path, backup_enabled: bool = True):
        super().__init__(config_path, backup_enabled)
        self.backups_dir = config_path / ".claude" / "backups"
        self.backups_dir.mkdir(parents=True, exist_ok=True)
        
        # Files to include in backups
        self.backup_patterns = [
            "CLAUDE.md",
            ".mcp.json",
            ".claude/settings.json",
            ".claude/settings.local.json.example",
            ".claude/commands/**/*.md",
            ".claude/personas/**/*.md",
            ".version",
            ".metadata.json"
        ]
        
        # Files to exclude from backups
        self.exclude_patterns = [
            ".claude/backups/**",
            ".claude/settings.local.json",  # Personal settings
            ".claude/.cache/**",
            "**/__pycache__/**",
            "**/*.pyc",
            "**/node_modules/**"
        ]
    
    def create_backup(self, description: str = "") -> BackupInfo:
        """Create a new backup of the configuration.
        
        Args:
            description: Optional description for the backup
            
        Returns:
            BackupInfo object with backup details
            
        Raises:
            Exception: If backup creation fails
        """
        timestamp = datetime.now()
        backup_name = timestamp.strftime("backup_%Y%m%d_%H%M%S")
        backup_path = self.backups_dir / f"{backup_name}.zip"
        
        try:
            files_backed_up = 0
            total_size = 0
            
            with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                # Backup configuration files
                for pattern in self.backup_patterns:
                    files = self._get_files_by_pattern(pattern)
                    
                    for file_path in files:
                        if self._should_exclude_file(file_path):
                            continue
                        
                        # Calculate relative path for archive
                        rel_path = file_path.relative_to(self.config_path)
                        
                        # Add to zip
                        zip_file.write(file_path, rel_path)
                        files_backed_up += 1
                        total_size += file_path.stat().st_size
                
                # Add backup metadata
                metadata = {
                    "timestamp": timestamp.isoformat(),
                    "description": description,
                    "files_count": files_backed_up,
                    "total_size": total_size,
                    "version": self._get_current_version(),
                    "backup_patterns": self.backup_patterns,
                    "exclude_patterns": self.exclude_patterns
                }
                
                zip_file.writestr("backup_metadata.json", json.dumps(metadata, indent=2))
            
            # Create backup info
            backup_info = BackupInfo(
                name=backup_name,
                timestamp=timestamp,
                path=backup_path,
                size_bytes=backup_path.stat().st_size,
                description=description,
                files_count=files_backed_up,
                version=metadata.get("version")
            )
            
            # Log successful backup
            result = MigrationResult(
                status=MigrationStatus.SUCCESS,
                message=f"Backup created successfully: {backup_name}",
                backup_path=backup_path,
                files_affected=[backup_path]
            )
            self.add_result(result)
            
            return backup_info
            
        except Exception as e:
            # Clean up failed backup
            if backup_path.exists():
                backup_path.unlink()
            
            result = MigrationResult(
                status=MigrationStatus.FAILED,
                message=f"Failed to create backup: {e}",
                errors=[str(e)]
            )
            self.add_result(result)
            
            raise Exception(f"Backup creation failed: {e}")
    
    def restore_backup(self, backup_name: str, confirm: bool = False) -> MigrationResult:
        """Restore configuration from a backup.
        
        Args:
            backup_name: Name of the backup to restore
            confirm: Whether to proceed without confirmation
            
        Returns:
            MigrationResult indicating success or failure
        """
        backup_path = self.backups_dir / f"{backup_name}.zip"
        
        if not backup_path.exists():
            return MigrationResult(
                status=MigrationStatus.FAILED,
                message=f"Backup not found: {backup_name}",
                errors=[f"File not found: {backup_path}"]
            )
        
        if not confirm:
            return MigrationResult(
                status=MigrationStatus.FAILED,
                message="Restore cancelled - confirmation required",
                warnings=["Use confirm=True to proceed with restore"]
            )
        
        try:
            # Create a safety backup before restore
            safety_backup = self.create_backup(f"Pre-restore safety backup before {backup_name}")
            
            restored_files = []
            
            with zipfile.ZipFile(backup_path, 'r') as zip_file:
                # Read backup metadata
                try:
                    metadata_content = zip_file.read("backup_metadata.json")
                    metadata = json.loads(metadata_content.decode('utf-8'))
                except:
                    metadata = {}
                
                # Extract all files except metadata
                for member in zip_file.namelist():
                    if member == "backup_metadata.json":
                        continue
                    
                    target_path = self.config_path / member
                    
                    # Create parent directories
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    # Extract file
                    with zip_file.open(member) as source:
                        with open(target_path, 'wb') as target:
                            shutil.copyfileobj(source, target)
                    
                    restored_files.append(target_path)
            
            return MigrationResult(
                status=MigrationStatus.SUCCESS,
                message=f"Configuration restored from backup: {backup_name}",
                files_affected=restored_files,
                backup_path=safety_backup.path
            )
            
        except Exception as e:
            return MigrationResult(
                status=MigrationStatus.FAILED,
                message=f"Failed to restore backup {backup_name}: {e}",
                errors=[str(e)]
            )
    
    def list_backups(self) -> List[BackupInfo]:
        """List all available backups.
        
        Returns:
            List of BackupInfo objects sorted by timestamp (newest first)
        """
        backups = []
        
        for backup_file in self.backups_dir.glob("*.zip"):
            try:
                backup_info = self._get_backup_info(backup_file)
                if backup_info:
                    backups.append(backup_info)
            except Exception:
                # Skip corrupted backup files
                continue
        
        # Sort by timestamp, newest first
        backups.sort(key=lambda b: b.timestamp, reverse=True)
        return backups
    
    def delete_backup(self, backup_name: str) -> bool:
        """Delete a backup.
        
        Args:
            backup_name: Name of the backup to delete
            
        Returns:
            True if backup was deleted, False otherwise
        """
        backup_path = self.backups_dir / f"{backup_name}.zip"
        
        if not backup_path.exists():
            return False
        
        try:
            backup_path.unlink()
            return True
        except Exception:
            return False
    
    def cleanup_old_backups(self, keep_count: int = 10) -> int:
        """Remove old backups, keeping only the most recent ones.
        
        Args:
            keep_count: Number of backups to keep
            
        Returns:
            Number of backups deleted
        """
        backups = self.list_backups()
        
        if len(backups) <= keep_count:
            return 0
        
        backups_to_delete = backups[keep_count:]
        deleted_count = 0
        
        for backup in backups_to_delete:
            if self.delete_backup(backup.name):
                deleted_count += 1
        
        return deleted_count
    
    def get_backup_size_total(self) -> int:
        """Get total size of all backups in bytes.
        
        Returns:
            Total size in bytes
        """
        total_size = 0
        
        for backup_file in self.backups_dir.glob("*.zip"):
            try:
                total_size += backup_file.stat().st_size
            except:
                continue
        
        return total_size
    
    def export_backup(self, backup_name: str, export_path: Path) -> bool:
        """Export a backup to an external location.
        
        Args:
            backup_name: Name of the backup to export
            export_path: Path where to export the backup
            
        Returns:
            True if export was successful, False otherwise
        """
        backup_path = self.backups_dir / f"{backup_name}.zip"
        
        if not backup_path.exists():
            return False
        
        try:
            export_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(backup_path, export_path)
            return True
        except Exception:
            return False
    
    def import_backup(self, import_path: Path, backup_name: Optional[str] = None) -> BackupInfo:
        """Import a backup from an external location.
        
        Args:
            import_path: Path to the backup file to import
            backup_name: Optional name for the imported backup
            
        Returns:
            BackupInfo object for the imported backup
            
        Raises:
            Exception: If import fails
        """
        if not import_path.exists():
            raise Exception(f"Import file not found: {import_path}")
        
        # Generate backup name if not provided
        if not backup_name:
            timestamp = datetime.now()
            backup_name = f"imported_{timestamp.strftime('%Y%m%d_%H%M%S')}"
        
        target_path = self.backups_dir / f"{backup_name}.zip"
        
        try:
            # Copy the backup file
            shutil.copy2(import_path, target_path)
            
            # Get backup info
            backup_info = self._get_backup_info(target_path)
            if not backup_info:
                raise Exception("Invalid backup file format")
            
            return backup_info
            
        except Exception as e:
            # Clean up failed import
            if target_path.exists():
                target_path.unlink()
            raise Exception(f"Import failed: {e}")
    
    def _get_files_by_pattern(self, pattern: str) -> List[Path]:
        """Get files matching a pattern.
        
        Args:
            pattern: Glob pattern to match
            
        Returns:
            List of matching file paths
        """
        if "**" in pattern:
            # Recursive glob
            return list(self.config_path.rglob(pattern.replace("**/", "")))
        else:
            # Regular glob
            return list(self.config_path.glob(pattern))
    
    def _should_exclude_file(self, file_path: Path) -> bool:
        """Check if a file should be excluded from backup.
        
        Args:
            file_path: File path to check
            
        Returns:
            True if file should be excluded
        """
        rel_path = file_path.relative_to(self.config_path)
        
        for exclude_pattern in self.exclude_patterns:
            if rel_path.match(exclude_pattern) or str(rel_path).startswith(exclude_pattern.replace("**", "")):
                return True
        
        return False
    
    def _get_backup_info(self, backup_path: Path) -> Optional[BackupInfo]:
        """Get backup information from a backup file.
        
        Args:
            backup_path: Path to the backup file
            
        Returns:
            BackupInfo object or None if invalid
        """
        try:
            with zipfile.ZipFile(backup_path, 'r') as zip_file:
                # Try to read metadata
                metadata = {}
                try:
                    metadata_content = zip_file.read("backup_metadata.json")
                    metadata = json.loads(metadata_content.decode('utf-8'))
                except:
                    pass
                
                # Extract info from filename and file stats
                backup_name = backup_path.stem
                file_stats = backup_path.stat()
                
                # Parse timestamp from filename or metadata
                timestamp = datetime.fromtimestamp(file_stats.st_mtime)
                if "timestamp" in metadata:
                    try:
                        timestamp = datetime.fromisoformat(metadata["timestamp"])
                    except:
                        pass
                
                return BackupInfo(
                    name=backup_name,
                    timestamp=timestamp,
                    path=backup_path,
                    size_bytes=file_stats.st_size,
                    description=metadata.get("description", ""),
                    files_count=metadata.get("files_count", len(zip_file.namelist()) - 1),  # -1 for metadata
                    version=metadata.get("version"),
                    checksum=None  # TODO: Implement checksum calculation
                )
                
        except Exception:
            return None
    
    def _get_current_version(self) -> Optional[str]:
        """Get current configuration version.
        
        Returns:
            Version string or None if not found
        """
        try:
            from .version_manager import VersionManager
            version_manager = VersionManager(self.config_path)
            version = version_manager.detect_current_version()
            return str(version) if version else None
        except:
            return None
    
    # Required abstract methods from BaseMigrator
    def migrate(self, source_version: str, target_version: str) -> MigrationResult:
        """Not applicable for backup manager."""
        return MigrationResult(
            status=MigrationStatus.FAILED,
            message="Backup manager does not support migration operations"
        )
    
    def can_migrate(self, source_version: str, target_version: str) -> bool:
        """Not applicable for backup manager."""
        return False