"""CLAUDE.md configuration file validator."""

import re
from pathlib import Path
from typing import List, Set, Dict, Any
import yaml

from .base import BaseValidator, ValidationResult, ValidationLevel


class ClaudeConfigValidator(BaseValidator):
    """Validator for CLAUDE.md configuration files."""
    
    def __init__(self, config_path: Path):
        super().__init__(config_path)
        self.yaml_references: Set[str] = set()
        self.missing_references: Set[str] = set()
        
    def validate(self) -> List[ValidationResult]:
        """Validate CLAUDE.md configuration file."""
        self.clear_results()
        
        if not self.config_path.exists():
            self.add_result(
                ValidationLevel.ERROR,
                f"CLAUDE.md file not found: {self.config_path}",
                file_path=self.config_path
            )
            return self.results
        
        try:
            content = self.config_path.read_text(encoding='utf-8')
        except Exception as e:
            self.add_result(
                ValidationLevel.ERROR,
                f"Failed to read CLAUDE.md file: {e}",
                file_path=self.config_path
            )
            return self.results
        
        # Validate structure and syntax
        self._validate_structure(content)
        self._validate_yaml_references(content)
        self._validate_sections(content)
        self._check_common_issues(content)
        
        return self.results
    
    def _validate_structure(self, content: str) -> None:
        """Validate basic file structure."""
        lines = content.split('\n')
        
        # Check for basic markdown structure
        has_header = any(line.startswith('#') for line in lines[:10])
        if not has_header:
            self.add_result(
                ValidationLevel.WARNING,
                "No markdown headers found in first 10 lines",
                suggestion="Add descriptive headers to organize your configuration"
            )
        
        # Check for empty file
        if not content.strip():
            self.add_result(
                ValidationLevel.ERROR,
                "CLAUDE.md file is empty",
                auto_fixable=True,
                suggestion="Add basic configuration structure"
            )
    
    def _validate_yaml_references(self, content: str) -> None:
        """Validate @include YAML references."""
        # Pattern to match @include statements
        include_pattern = r'@include\s+([^\s#]+)#?([^\s]*)'
        
        for line_num, line in enumerate(content.split('\n'), 1):
            matches = re.findall(include_pattern, line)
            for file_path, section in matches:
                self.yaml_references.add(file_path)
                self._validate_yaml_reference(file_path, section, line_num)
    
    def _validate_yaml_reference(self, file_path: str, section: str, line_num: int) -> None:
        """Validate a single YAML reference."""
        # Construct full path relative to config
        full_path = self.config_path.parent / file_path
        
        if not full_path.exists():
            self.missing_references.add(file_path)
            self.add_result(
                ValidationLevel.ERROR,
                f"Referenced YAML file not found: {file_path}",
                file_path=self.config_path,
                line_number=line_num,
                suggestion=f"Create the missing file at {full_path}"
            )
            return
        
        # Validate YAML syntax
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                yaml_content = yaml.safe_load(f)
        except yaml.YAMLError as e:
            self.add_result(
                ValidationLevel.ERROR,
                f"Invalid YAML syntax in {file_path}: {e}",
                file_path=full_path,
                line_number=line_num
            )
            return
        except Exception as e:
            self.add_result(
                ValidationLevel.ERROR,
                f"Failed to read YAML file {file_path}: {e}",
                file_path=full_path,
                line_number=line_num
            )
            return
        
        # Validate section reference if specified
        if section and yaml_content:
            if not self._section_exists_in_yaml(yaml_content, section):
                self.add_result(
                    ValidationLevel.ERROR,
                    f"Section '{section}' not found in {file_path}",
                    file_path=full_path,
                    line_number=line_num,
                    suggestion=f"Add section '{section}' to {file_path} or fix the reference"
                )
    
    def _section_exists_in_yaml(self, yaml_content: Dict[str, Any], section: str) -> bool:
        """Check if a section exists in YAML content."""
        if not isinstance(yaml_content, dict):
            return False
        return section in yaml_content
    
    def _validate_sections(self, content: str) -> None:
        """Validate common configuration sections."""
        required_sections = {
            'Core Configuration': r'##\s*Core Configuration',
            'Development': r'##\s*Development',
            'Rules': r'##\s*Rules'
        }
        
        for section_name, pattern in required_sections.items():
            if not re.search(pattern, content, re.IGNORECASE):
                self.add_result(
                    ValidationLevel.INFO,
                    f"Recommended section '{section_name}' not found",
                    suggestion=f"Consider adding a '{section_name}' section for better organization"
                )
    
    def _check_common_issues(self, content: str) -> None:
        """Check for common configuration issues."""
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            # Check for very long lines
            if len(line) > 200:
                self.add_result(
                    ValidationLevel.WARNING,
                    f"Very long line ({len(line)} characters)",
                    file_path=self.config_path,
                    line_number=line_num,
                    suggestion="Consider breaking long lines for better readability"
                )
            
            # Check for potential encoding issues
            try:
                line.encode('utf-8')
            except UnicodeEncodeError:
                self.add_result(
                    ValidationLevel.ERROR,
                    "Non-UTF-8 characters detected",
                    file_path=self.config_path,
                    line_number=line_num,
                    suggestion="Ensure all content is UTF-8 encoded"
                )
            
            # Check for malformed @include statements
            if '@include' in line and not re.match(r'@include\s+\S+', line):
                self.add_result(
                    ValidationLevel.ERROR,
                    "Malformed @include statement",
                    file_path=self.config_path,
                    line_number=line_num,
                    suggestion="Use format: @include path/to/file.yml#section"
                )
    
    def get_yaml_references(self) -> Set[str]:
        """Get all YAML references found in the file."""
        return self.yaml_references.copy()
    
    def get_missing_references(self) -> Set[str]:
        """Get all missing YAML references."""
        return self.missing_references.copy()