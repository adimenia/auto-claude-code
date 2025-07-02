"""Base classes for the validation system."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import List, Optional, Any, Dict


class ValidationLevel(Enum):
    """Validation severity levels."""
    INFO = "info"
    WARNING = "warning" 
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class ValidationResult:
    """Result of a validation check."""
    level: ValidationLevel
    message: str
    file_path: Optional[Path] = None
    line_number: Optional[int] = None
    suggestion: Optional[str] = None
    auto_fixable: bool = False
    metadata: Optional[Dict[str, Any]] = None
    
    @property
    def is_error(self) -> bool:
        """Check if result is an error or critical issue."""
        return self.level in (ValidationLevel.ERROR, ValidationLevel.CRITICAL)
    
    @property
    def is_warning_or_above(self) -> bool:
        """Check if result is warning level or above."""
        return self.level in (ValidationLevel.WARNING, ValidationLevel.ERROR, ValidationLevel.CRITICAL)


class BaseValidator(ABC):
    """Base class for all validators."""
    
    def __init__(self, config_path: Path):
        """Initialize validator with configuration path.
        
        Args:
            config_path: Path to the configuration directory or file
        """
        self.config_path = config_path
        self.results: List[ValidationResult] = []
    
    @abstractmethod
    def validate(self) -> List[ValidationResult]:
        """Run validation checks.
        
        Returns:
            List of validation results
        """
        pass
    
    def add_result(self, level: ValidationLevel, message: str, **kwargs) -> None:
        """Add a validation result.
        
        Args:
            level: Severity level
            message: Validation message
            **kwargs: Additional result parameters
        """
        result = ValidationResult(level=level, message=message, **kwargs)
        self.results.append(result)
    
    def clear_results(self) -> None:
        """Clear all validation results."""
        self.results.clear()
    
    def has_errors(self) -> bool:
        """Check if validation found any errors."""
        return any(result.is_error for result in self.results)
    
    def has_warnings(self) -> bool:
        """Check if validation found any warnings or above."""
        return any(result.is_warning_or_above for result in self.results)
    
    def get_errors(self) -> List[ValidationResult]:
        """Get only error-level results."""
        return [r for r in self.results if r.is_error]
    
    def get_warnings(self) -> List[ValidationResult]:
        """Get warning-level results."""
        return [r for r in self.results if r.level == ValidationLevel.WARNING]