"""Upgrade assistant for configuration migration."""

from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from .base import BaseMigrator, MigrationResult, MigrationStatus
from .version_manager import VersionManager, Version
from .diff_engine import SmartDiffEngine, ConfigChange
from .backup_manager import BackupManager


@dataclass
class UpgradeStep:
    """Represents a single upgrade step."""
    description: str
    action: str  # 'copy', 'modify', 'delete', 'create'
    source_path: Optional[Path] = None
    target_path: Optional[Path] = None
    content: Optional[str] = None
    backup_required: bool = True


class UpgradeAssistant(BaseMigrator):
    """Assists with configuration upgrades and migrations."""
    
    def __init__(self, config_path: Path, backup_enabled: bool = True):
        super().__init__(config_path, backup_enabled)
        self.version_manager = VersionManager(config_path)
        self.diff_engine = SmartDiffEngine()
        self.backup_manager = BackupManager(config_path, backup_enabled)
        
        # Template versions and upgrade paths
        self.template_versions = {
            "1.0.0": "Initial template version",
            "1.1.0": "Added persona support and improved MCP configuration",
            "1.2.0": "Enhanced security settings and validation",
            "2.0.0": "Major restructure with new command system",
            "2.0.1": "Enhanced validation and migration system"
        }
    
    def check_for_upgrades(self) -> Optional[str]:
        """Check if upgrades are available.
        
        Returns:
            Latest available version or None if up to date
        """
        current_version = self.version_manager.detect_current_version()
        if not current_version:
            return list(self.template_versions.keys())[-1]  # Latest version
        
        # Find newer versions
        available_versions = [
            self.version_manager.parse_version(v) for v in self.template_versions.keys()
        ]
        available_versions.sort()
        
        for version in available_versions:
            if version > current_version:
                return str(version)
        
        return None
    
    def get_upgrade_preview(self, target_version: str) -> Dict[str, Any]:
        """Get preview of changes for an upgrade.
        
        Args:
            target_version: Target version to upgrade to
            
        Returns:
            Dictionary with upgrade preview information
        """
        current_version = self.version_manager.detect_current_version()
        
        preview = {
            "current_version": str(current_version) if current_version else "unknown",
            "target_version": target_version,
            "upgrade_available": True,
            "changes_summary": {},
            "risks": [],
            "backup_recommended": True,
            "estimated_time": "< 1 minute"
        }
        
        # Simulate changes (in a real implementation, this would compare with actual templates)
        if current_version and str(current_version) < target_version:
            preview["changes_summary"] = {
                "files_modified": ["CLAUDE.md", "settings.json"],
                "files_added": [".version", ".metadata.json"],
                "files_removed": [],
                "mcp_servers_updated": True,
                "personas_added": True
            }
            
            # Assess risks
            if target_version.startswith("2."):
                preview["risks"].append("Major version upgrade - may require manual review")
            
            preview["estimated_time"] = "1-2 minutes"
        
        return preview
    
    def perform_upgrade(self, target_version: str, create_backup: bool = True) -> MigrationResult:
        """Perform configuration upgrade.
        
        Args:
            target_version: Version to upgrade to
            create_backup: Whether to create backup before upgrade
            
        Returns:
            Migration result
        """
        current_version = self.version_manager.detect_current_version()
        
        try:
            # Create backup if requested
            backup_info = None
            if create_backup and self.backup_enabled:
                backup_info = self.backup_manager.create_backup(
                    f"Pre-upgrade backup from {current_version} to {target_version}"
                )
            
            # Generate upgrade steps
            upgrade_steps = self._generate_upgrade_steps(current_version, target_version)
            
            # Execute upgrade steps
            affected_files = []
            for step in upgrade_steps:
                try:
                    affected_file = self._execute_upgrade_step(step)
                    if affected_file:
                        affected_files.append(affected_file)
                except Exception as e:
                    # Rollback on failure
                    if backup_info:
                        self.backup_manager.restore_backup(backup_info.name, confirm=True)
                    
                    return MigrationResult(
                        status=MigrationStatus.FAILED,
                        message=f"Upgrade failed at step: {step.description}",
                        source_version=str(current_version) if current_version else None,
                        target_version=target_version,
                        errors=[str(e)],
                        backup_path=backup_info.path if backup_info else None
                    )
            
            # Update version information
            new_version = self.version_manager.parse_version(target_version)
            self.version_manager.save_version(new_version)
            
            # Update metadata
            metadata = self.version_manager.load_metadata()
            if metadata:
                metadata.version = new_version
                metadata = self.version_manager.update_metadata(metadata)
                self.version_manager.save_metadata(metadata)
            
            return MigrationResult(
                status=MigrationStatus.SUCCESS,
                message=f"Successfully upgraded from {current_version} to {target_version}",
                source_version=str(current_version) if current_version else None,
                target_version=target_version,
                files_affected=affected_files,
                backup_path=backup_info.path if backup_info else None
            )
            
        except Exception as e:
            return MigrationResult(
                status=MigrationStatus.FAILED,
                message=f"Upgrade failed: {e}",
                source_version=str(current_version) if current_version else None,
                target_version=target_version,
                errors=[str(e)]
            )
    
    def rollback_upgrade(self, backup_name: str) -> MigrationResult:
        """Rollback to a previous configuration using backup.
        
        Args:
            backup_name: Name of backup to restore
            
        Returns:
            Migration result
        """
        return self.backup_manager.restore_backup(backup_name, confirm=True)
    
    def get_upgrade_history(self) -> List[Dict[str, Any]]:
        """Get history of upgrades performed.
        
        Returns:
            List of upgrade records
        """
        # In a real implementation, this would read from a history file
        # For now, return basic information from backups
        backups = self.backup_manager.list_backups()
        
        history = []
        for backup in backups:
            if "upgrade" in backup.description.lower():
                history.append({
                    "timestamp": backup.timestamp.isoformat(),
                    "description": backup.description,
                    "version": backup.version,
                    "backup_name": backup.name
                })
        
        return history
    
    def _generate_upgrade_steps(self, current_version: Optional[Version], 
                               target_version: str) -> List[UpgradeStep]:
        """Generate steps needed for upgrade.
        
        Args:
            current_version: Current version
            target_version: Target version
            
        Returns:
            List of upgrade steps
        """
        steps = []
        
        # Basic upgrade steps (in a real implementation, these would be more sophisticated)
        
        # Step 1: Update version metadata
        steps.append(UpgradeStep(
            description="Update version metadata",
            action="create",
            target_path=self.config_path / ".version",
            content=target_version
        ))
        
        # Step 2: Update configuration metadata
        steps.append(UpgradeStep(
            description="Update configuration metadata",
            action="modify",
            target_path=self.config_path / ".metadata.json"
        ))
        
        # Step 3: Add new features based on version
        if target_version >= "1.1.0":
            steps.append(UpgradeStep(
                description="Add persona support to configuration",
                action="modify",
                target_path=self.config_path / "CLAUDE.md"
            ))
        
        if target_version >= "1.2.0":
            steps.append(UpgradeStep(
                description="Enhance security settings",
                action="modify",
                target_path=self.config_path / ".claude" / "settings.json"
            ))
        
        return steps
    
    def _execute_upgrade_step(self, step: UpgradeStep) -> Optional[Path]:
        """Execute a single upgrade step.
        
        Args:
            step: Upgrade step to execute
            
        Returns:
            Path of affected file or None
            
        Raises:
            Exception: If step execution fails
        """
        if step.action == "create":
            if step.target_path and step.content:
                step.target_path.parent.mkdir(parents=True, exist_ok=True)
                step.target_path.write_text(step.content, encoding='utf-8')
                return step.target_path
        
        elif step.action == "modify":
            if step.target_path and step.target_path.exists():
                # For now, just update timestamp to simulate modification
                # In a real implementation, this would apply specific changes
                content = step.target_path.read_text(encoding='utf-8')
                step.target_path.write_text(content, encoding='utf-8')
                return step.target_path
        
        elif step.action == "copy":
            if step.source_path and step.target_path:
                step.target_path.parent.mkdir(parents=True, exist_ok=True)
                import shutil
                shutil.copy2(step.source_path, step.target_path)
                return step.target_path
        
        elif step.action == "delete":
            if step.target_path and step.target_path.exists():
                step.target_path.unlink()
                return step.target_path
        
        return None
    
    # Required abstract methods from BaseMigrator
    def migrate(self, source_version: str, target_version: str) -> MigrationResult:
        """Perform migration between versions."""
        return self.perform_upgrade(target_version)
    
    def can_migrate(self, source_version: str, target_version: str) -> bool:
        """Check if migration is possible."""
        try:
            source_ver = self.version_manager.parse_version(source_version)
            target_ver = self.version_manager.parse_version(target_version)
            return target_ver >= source_ver
        except:
            return False