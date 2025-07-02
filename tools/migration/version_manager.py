"""Version detection and comparison for configuration management."""

import re
import json
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple
from dataclasses import dataclass
from datetime import datetime
import hashlib


@dataclass
class Version:
    """Represents a configuration version."""
    major: int
    minor: int
    patch: int
    pre_release: Optional[str] = None
    build_metadata: Optional[str] = None
    
    def __str__(self) -> str:
        """String representation of version."""
        version_str = f"{self.major}.{self.minor}.{self.patch}"
        if self.pre_release:
            version_str += f"-{self.pre_release}"
        if self.build_metadata:
            version_str += f"+{self.build_metadata}"
        return version_str
    
    def __lt__(self, other: 'Version') -> bool:
        """Compare versions for sorting."""
        if not isinstance(other, Version):
            return NotImplemented
        
        # Compare major.minor.patch
        self_tuple = (self.major, self.minor, self.patch)
        other_tuple = (other.major, other.minor, other.patch)
        
        if self_tuple != other_tuple:
            return self_tuple < other_tuple
        
        # Handle pre-release comparison
        if self.pre_release is None and other.pre_release is None:
            return False
        if self.pre_release is None:
            return False  # Release > pre-release
        if other.pre_release is None:
            return True   # Pre-release < release
        
        return self.pre_release < other.pre_release
    
    def __eq__(self, other: 'Version') -> bool:
        """Check version equality."""
        if not isinstance(other, Version):
            return NotImplemented
        return (
            self.major == other.major and
            self.minor == other.minor and
            self.patch == other.patch and
            self.pre_release == other.pre_release
        )
    
    def __le__(self, other: 'Version') -> bool:
        """Less than or equal comparison."""
        return self < other or self == other
    
    def __gt__(self, other: 'Version') -> bool:
        """Greater than comparison."""
        return not (self < other or self == other)
    
    def __ge__(self, other: 'Version') -> bool:
        """Greater than or equal comparison."""
        return not self < other
    
    def is_compatible_with(self, other: 'Version') -> bool:
        """Check if versions are compatible (same major version)."""
        return self.major == other.major


@dataclass
class ConfigMetadata:
    """Metadata about a configuration."""
    version: Version
    created_at: datetime
    updated_at: datetime
    checksum: str
    template_type: str
    dependencies: List[str]
    author: Optional[str] = None
    description: Optional[str] = None


class VersionManager:
    """Manages configuration versions and metadata."""
    
    VERSION_FILE = ".version"
    METADATA_FILE = ".metadata.json"
    
    def __init__(self, config_path: Path):
        """Initialize version manager.
        
        Args:
            config_path: Path to configuration directory
        """
        self.config_path = config_path
        self.version_file = config_path / self.VERSION_FILE
        self.metadata_file = config_path / self.METADATA_FILE
    
    def parse_version(self, version_string: str) -> Version:
        """Parse version string into Version object.
        
        Args:
            version_string: Version string (e.g., "1.2.3-alpha+build.1")
            
        Returns:
            Version object
            
        Raises:
            ValueError: If version string is invalid
        """
        # Regex for semantic versioning
        pattern = r'^(\d+)\.(\d+)\.(\d+)(?:-([a-zA-Z0-9\-\.]+))?(?:\+([a-zA-Z0-9\-\.]+))?$'
        match = re.match(pattern, version_string.strip())
        
        if not match:
            raise ValueError(f"Invalid version string: {version_string}")
        
        major, minor, patch, pre_release, build_metadata = match.groups()
        
        return Version(
            major=int(major),
            minor=int(minor),
            patch=int(patch),
            pre_release=pre_release,
            build_metadata=build_metadata
        )
    
    def detect_current_version(self) -> Optional[Version]:
        """Detect current configuration version.
        
        Returns:
            Current version or None if not found
        """
        # Try to read version from version file
        if self.version_file.exists():
            try:
                version_str = self.version_file.read_text(encoding='utf-8').strip()
                return self.parse_version(version_str)
            except (ValueError, IOError):
                pass
        
        # Try to extract version from CLAUDE.md
        claude_file = self.config_path / "CLAUDE.md"
        if claude_file.exists():
            version = self._extract_version_from_claude_md(claude_file)
            if version:
                return version
        
        # Try to extract from settings.json
        settings_file = self.config_path / "settings.json"
        if settings_file.exists():
            version = self._extract_version_from_settings(settings_file)
            if version:
                return version
        
        return None
    
    def _extract_version_from_claude_md(self, claude_file: Path) -> Optional[Version]:
        """Extract version from CLAUDE.md file."""
        try:
            content = claude_file.read_text(encoding='utf-8')
            
            # Look for version patterns - be more specific to avoid documentation examples
            patterns = [
                r'version[:\s]+v?(\d+\.\d+\.\d+(?:-[a-zA-Z0-9\-\.]+)?(?:\+[a-zA-Z0-9\-\.]+)?)',
                r'SuperClaude v(\d+\.\d+\.\d+)',
            ]
            
            for pattern in patterns:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    try:
                        version_str = match.group(1)
                        
                        # Skip if this looks like a documentation example
                        context_before = content[max(0, match.start()-50):match.start()]
                        context_after = content[match.end():match.end()+50]
                        full_context = (context_before + match.group(0) + context_after).lower()
                        
                        # Skip documentation contexts
                        doc_indicators = [
                            'semantic versioning',
                            'version tagging', 
                            'example',
                            'e.g.',
                            'for example',
                            '(v1.2.3)',
                            'format:',
                            'like:',
                            'such as'
                        ]
                        
                        if any(indicator in full_context for indicator in doc_indicators):
                            continue  # Skip this match, it's documentation
                        
                        return self.parse_version(version_str)
                    except ValueError:
                        continue
        except IOError:
            pass
        
        return None
    
    def _extract_version_from_settings(self, settings_file: Path) -> Optional[Version]:
        """Extract version from settings.json file."""
        try:
            with open(settings_file, 'r', encoding='utf-8') as f:
                settings = json.load(f)
            
            version_str = settings.get('version')
            if version_str:
                return self.parse_version(version_str)
        except (json.JSONDecodeError, ValueError, IOError):
            pass
        
        return None
    
    def save_version(self, version: Version) -> None:
        """Save version to version file.
        
        Args:
            version: Version to save
        """
        self.version_file.write_text(str(version), encoding='utf-8')
    
    def calculate_config_checksum(self) -> str:
        """Calculate checksum of configuration files.
        
        Returns:
            SHA256 checksum of configuration content
        """
        hasher = hashlib.sha256()
        
        # Include main configuration files
        config_files = [
            "CLAUDE.md",
            "settings.json",
        ]
        
        # Add command files if they exist
        commands_dir = self.config_path / "commands"
        if commands_dir.exists():
            for cmd_file in commands_dir.rglob("*.md"):
                config_files.append(str(cmd_file.relative_to(self.config_path)))
        
        # Sort files for consistent checksum
        config_files.sort()
        
        for file_path in config_files:
            full_path = self.config_path / file_path
            if full_path.exists() and full_path.is_file():
                try:
                    content = full_path.read_bytes()
                    hasher.update(file_path.encode('utf-8'))
                    hasher.update(content)
                except IOError:
                    pass
        
        return hasher.hexdigest()
    
    def load_metadata(self) -> Optional[ConfigMetadata]:
        """Load configuration metadata.
        
        Returns:
            Configuration metadata or None if not found
        """
        if not self.metadata_file.exists():
            return None
        
        try:
            with open(self.metadata_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            version = self.parse_version(data['version'])
            created_at = datetime.fromisoformat(data['created_at'])
            updated_at = datetime.fromisoformat(data['updated_at'])
            
            return ConfigMetadata(
                version=version,
                created_at=created_at,
                updated_at=updated_at,
                checksum=data['checksum'],
                template_type=data['template_type'],
                dependencies=data.get('dependencies', []),
                author=data.get('author'),
                description=data.get('description')
            )
        except (json.JSONDecodeError, KeyError, ValueError, IOError):
            return None
    
    def save_metadata(self, metadata: ConfigMetadata) -> None:
        """Save configuration metadata.
        
        Args:
            metadata: Metadata to save
        """
        data = {
            'version': str(metadata.version),
            'created_at': metadata.created_at.isoformat(),
            'updated_at': metadata.updated_at.isoformat(),
            'checksum': metadata.checksum,
            'template_type': metadata.template_type,
            'dependencies': metadata.dependencies,
            'author': metadata.author,
            'description': metadata.description
        }
        
        with open(self.metadata_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    
    def create_metadata(self, version: Version, template_type: str, 
                       author: Optional[str] = None, 
                       description: Optional[str] = None) -> ConfigMetadata:
        """Create new configuration metadata.
        
        Args:
            version: Configuration version
            template_type: Type of template (e.g., 'fastapi', 'django')
            author: Author name
            description: Configuration description
            
        Returns:
            New ConfigMetadata object
        """
        now = datetime.now()
        checksum = self.calculate_config_checksum()
        
        return ConfigMetadata(
            version=version,
            created_at=now,
            updated_at=now,
            checksum=checksum,
            template_type=template_type,
            dependencies=[],
            author=author,
            description=description
        )
    
    def update_metadata(self, metadata: ConfigMetadata) -> ConfigMetadata:
        """Update existing metadata with current state.
        
        Args:
            metadata: Existing metadata to update
            
        Returns:
            Updated metadata
        """
        metadata.updated_at = datetime.now()
        metadata.checksum = self.calculate_config_checksum()
        return metadata
    
    def compare_versions(self, version1: Version, version2: Version) -> int:
        """Compare two versions.
        
        Args:
            version1: First version
            version2: Second version
            
        Returns:
            -1 if version1 < version2, 0 if equal, 1 if version1 > version2
        """
        if version1 < version2:
            return -1
        elif version1 == version2:
            return 0
        else:
            return 1
    
    def get_migration_path(self, source: Version, target: Version) -> List[Tuple[Version, Version]]:
        """Get migration path between versions.
        
        Args:
            source: Source version
            target: Target version
            
        Returns:
            List of version pairs representing migration steps
        """
        # For now, assume direct migration is possible
        # In the future, this could handle complex migration paths
        if source == target:
            return []
        
        return [(source, target)]
    
    def is_migration_needed(self) -> bool:
        """Check if migration is needed.
        
        Returns:
            True if configuration needs migration
        """
        current_version = self.detect_current_version()
        if not current_version:
            return True  # No version detected, assume migration needed
        
        metadata = self.load_metadata()
        if not metadata:
            return True  # No metadata, assume migration needed
        
        # Check if checksum matches (configuration changed)
        current_checksum = self.calculate_config_checksum()
        return current_checksum != metadata.checksum