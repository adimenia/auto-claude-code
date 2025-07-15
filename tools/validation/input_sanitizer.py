"""Comprehensive input validation and sanitization utilities."""

import re
import json
import yaml
import html
import urllib.parse
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, Tuple
from dataclasses import dataclass
from enum import Enum
import logging

from .base import ValidationResult, ValidationLevel


class InputType(Enum):
    """Types of input validation."""
    TEXT = "text"
    EMAIL = "email"
    URL = "url"
    PATH = "path"
    JSON = "json"
    YAML = "yaml"
    COMMAND = "command"
    FILENAME = "filename"
    USERNAME = "username"
    SERVER_NAME = "server_name"
    SQL_QUERY = "sql_query"
    REGEX = "regex"
    VERSION = "version"
    IP_ADDRESS = "ip_address"
    PORT = "port"


@dataclass
class SanitizationRule:
    """Configuration for input sanitization rules."""
    input_type: InputType
    max_length: Optional[int] = None
    min_length: Optional[int] = None
    allowed_chars: Optional[str] = None
    disallowed_chars: Optional[str] = None
    required_patterns: Optional[List[str]] = None
    forbidden_patterns: Optional[List[str]] = None
    normalize_whitespace: bool = True
    strip_html: bool = True
    escape_sql: bool = True
    case_sensitive: bool = True
    custom_validator: Optional[callable] = None


@dataclass
class SanitizationResult:
    """Result of input sanitization."""
    original_value: str
    sanitized_value: str
    is_valid: bool
    validation_errors: List[str]
    security_issues: List[str]
    applied_transformations: List[str]


class InputSanitizer:
    """Comprehensive input sanitization and validation system."""
    
    # Security-sensitive patterns to block
    DANGEROUS_PATTERNS = {
        'sql_injection': [
            r'(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|EXECUTE)\b)',
            r'(UNION\s+SELECT)',
            r'(;\s*DROP\s+TABLE)',
            r'(--\s*)',
            r'(/\*[\s\S]*?\*/)',
            r'(\';\s*--)',
            r'(\'\s*OR\s*\'\d*\'\s*=\s*\'\d*)',
        ],
        'xss': [
            r'(<script[^>]*>.*?</script>)',
            r'(javascript:)',
            r'(on\w+\s*=)',
            r'(<iframe[^>]*>)',
            r'(<object[^>]*>)',
            r'(<embed[^>]*>)',
            r'(eval\s*\()',
            r'(expression\s*\()',
        ],
        'path_traversal': [
            r'(\.\.\/)',
            r'(\.\.\\)',
            r'(%2e%2e%2f)',
            r'(%2e%2e\\)',
            r'(\.\.%2f)',
            r'(\.\.%5c)',
        ],
        'command_injection': [
            r'(\||\;|\&|\$\(|\`)',
            r'(&&|\|\|)',
            r'(>\s*\/)',
            r'(<\s*\/)',
            r'(\$\{[^}]*\})',
        ],
        'server_side_includes': [
            r'(<!--\s*#\s*exec)',
            r'(<!--\s*#\s*include)',
            r'(<!--\s*#\s*config)',
            r'(<!--\s*#\s*set)',
        ]
    }
    
    # Safe character sets for different input types
    SAFE_CHARS = {
        InputType.USERNAME: r'[a-zA-Z0-9_\-\.]',
        InputType.FILENAME: r'[a-zA-Z0-9_\-\.\s]',
        InputType.SERVER_NAME: r'[a-zA-Z0-9_\-\.]',
        InputType.VERSION: r'[0-9\.\-]',
        InputType.TEXT: r'[a-zA-Z0-9\s\.\,\!\?\-\_\(\)\[\]\{\}]',
    }
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """Initialize the input sanitizer.
        
        Args:
            logger: Optional logger instance for audit trails
        """
        self.logger = logger or logging.getLogger(__name__)
        self.validation_cache: Dict[str, SanitizationResult] = {}
        
    def sanitize_input(self, value: Any, input_type: InputType, 
                      rules: Optional[SanitizationRule] = None) -> SanitizationResult:
        """Sanitize and validate input based on type and rules.
        
        Args:
            value: Input value to sanitize
            input_type: Type of input validation to apply
            rules: Optional custom sanitization rules
            
        Returns:
            SanitizationResult with sanitized value and validation info
        """
        # Convert to string if not already
        if value is None:
            value = ""
        original_value = str(value)
        
        # Check cache first
        cache_key = f"{input_type.value}:{hash(original_value)}"
        if cache_key in self.validation_cache:
            return self.validation_cache[cache_key]
        
        # Apply default rules if none provided
        if rules is None:
            rules = self._get_default_rules(input_type)
        
        # Initialize result
        result = SanitizationResult(
            original_value=original_value,
            sanitized_value=original_value,
            is_valid=True,
            validation_errors=[],
            security_issues=[],
            applied_transformations=[]
        )
        
        # Apply sanitization steps
        result = self._apply_length_validation(result, rules)
        result = self._apply_character_validation(result, rules)
        result = self._apply_pattern_validation(result, rules)
        result = self._apply_security_checks(result, input_type)
        result = self._apply_transformations(result, rules)
        result = self._apply_type_specific_validation(result, input_type)
        result = self._apply_custom_validation(result, rules)
        
        # Cache result
        self.validation_cache[cache_key] = result
        
        # Log security issues
        if result.security_issues:
            self.logger.warning(f"Security issues detected in input: {result.security_issues}")
        
        return result
    
    def _get_default_rules(self, input_type: InputType) -> SanitizationRule:
        """Get default sanitization rules for input type."""
        rules = {
            InputType.TEXT: SanitizationRule(
                input_type=input_type,
                max_length=1000,
                min_length=0,
                forbidden_patterns=self.DANGEROUS_PATTERNS['xss'],
                normalize_whitespace=True,
                strip_html=True
            ),
            InputType.EMAIL: SanitizationRule(
                input_type=input_type,
                max_length=254,
                min_length=5,
                required_patterns=[r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'],
                normalize_whitespace=True,
                case_sensitive=False
            ),
            InputType.URL: SanitizationRule(
                input_type=input_type,
                max_length=2048,
                min_length=7,
                required_patterns=[r'^https?://[^\s/$.?#].[^\s]*$'],
                forbidden_patterns=self.DANGEROUS_PATTERNS['xss'],
                normalize_whitespace=True
            ),
            InputType.PATH: SanitizationRule(
                input_type=input_type,
                max_length=4096,
                min_length=1,
                forbidden_patterns=self.DANGEROUS_PATTERNS['path_traversal'],
                normalize_whitespace=True
            ),
            InputType.JSON: SanitizationRule(
                input_type=input_type,
                max_length=1048576,  # 1MB
                normalize_whitespace=False,
                strip_html=False,
                escape_sql=False
            ),
            InputType.YAML: SanitizationRule(
                input_type=input_type,
                max_length=1048576,  # 1MB
                normalize_whitespace=False,
                strip_html=False,
                escape_sql=False
            ),
            InputType.COMMAND: SanitizationRule(
                input_type=input_type,
                max_length=1024,
                forbidden_patterns=self.DANGEROUS_PATTERNS['command_injection'],
                normalize_whitespace=True
            ),
            InputType.FILENAME: SanitizationRule(
                input_type=input_type,
                max_length=255,
                min_length=1,
                allowed_chars=self.SAFE_CHARS[InputType.FILENAME],
                forbidden_patterns=self.DANGEROUS_PATTERNS['path_traversal'],
                normalize_whitespace=True
            ),
            InputType.USERNAME: SanitizationRule(
                input_type=input_type,
                max_length=64,
                min_length=2,
                allowed_chars=self.SAFE_CHARS[InputType.USERNAME],
                normalize_whitespace=True
            ),
            InputType.SERVER_NAME: SanitizationRule(
                input_type=input_type,
                max_length=253,
                min_length=1,
                allowed_chars=self.SAFE_CHARS[InputType.SERVER_NAME],
                required_patterns=[r'^[a-zA-Z0-9][a-zA-Z0-9\-\.]*[a-zA-Z0-9]$'],
                normalize_whitespace=True
            ),
            InputType.VERSION: SanitizationRule(
                input_type=input_type,
                max_length=32,
                min_length=1,
                allowed_chars=self.SAFE_CHARS[InputType.VERSION],
                required_patterns=[r'^\d+(\.\d+)*([a-zA-Z0-9\-]*)?$'],
                normalize_whitespace=True
            ),
            InputType.IP_ADDRESS: SanitizationRule(
                input_type=input_type,
                max_length=45,  # IPv6 max length
                min_length=7,   # IPv4 min length
                required_patterns=[
                    r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$',  # IPv4
                    r'^(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$'  # IPv6
                ],
                normalize_whitespace=True
            ),
            InputType.PORT: SanitizationRule(
                input_type=input_type,
                max_length=5,
                min_length=1,
                allowed_chars=r'[0-9]',
                required_patterns=[r'^[1-9][0-9]*$'],
                normalize_whitespace=True
            )
        }
        
        return rules.get(input_type, SanitizationRule(input_type=input_type))
    
    def _apply_length_validation(self, result: SanitizationResult, 
                               rules: SanitizationRule) -> SanitizationResult:
        """Apply length validation rules."""
        length = len(result.sanitized_value)
        
        if rules.min_length is not None and length < rules.min_length:
            result.is_valid = False
            result.validation_errors.append(f"Input too short: {length} < {rules.min_length}")
        
        if rules.max_length is not None and length > rules.max_length:
            result.is_valid = False
            result.validation_errors.append(f"Input too long: {length} > {rules.max_length}")
            # Truncate if too long
            result.sanitized_value = result.sanitized_value[:rules.max_length]
            result.applied_transformations.append("truncated_to_max_length")
        
        return result
    
    def _apply_character_validation(self, result: SanitizationResult, 
                                  rules: SanitizationRule) -> SanitizationResult:
        """Apply character validation rules."""
        if rules.allowed_chars:
            # Remove disallowed characters
            pattern = f"[^{rules.allowed_chars}]"
            original_value = result.sanitized_value
            result.sanitized_value = re.sub(pattern, '', result.sanitized_value)
            
            if result.sanitized_value != original_value:
                result.applied_transformations.append("removed_disallowed_chars")
        
        if rules.disallowed_chars:
            # Remove explicitly disallowed characters
            pattern = f"[{re.escape(rules.disallowed_chars)}]"
            original_value = result.sanitized_value
            result.sanitized_value = re.sub(pattern, '', result.sanitized_value)
            
            if result.sanitized_value != original_value:
                result.applied_transformations.append("removed_forbidden_chars")
        
        return result
    
    def _apply_pattern_validation(self, result: SanitizationResult, 
                                rules: SanitizationRule) -> SanitizationResult:
        """Apply pattern validation rules."""
        flags = 0 if rules.case_sensitive else re.IGNORECASE
        
        # Check required patterns
        if rules.required_patterns:
            for pattern in rules.required_patterns:
                if not re.search(pattern, result.sanitized_value, flags):
                    result.is_valid = False
                    result.validation_errors.append(f"Input doesn't match required pattern: {pattern}")
        
        # Check forbidden patterns
        if rules.forbidden_patterns:
            for pattern in rules.forbidden_patterns:
                if re.search(pattern, result.sanitized_value, flags):
                    result.is_valid = False
                    result.security_issues.append(f"Input matches forbidden pattern: {pattern}")
        
        return result
    
    def _apply_security_checks(self, result: SanitizationResult, 
                             input_type: InputType) -> SanitizationResult:
        """Apply security-specific validation checks."""
        # Check for common attack patterns
        for attack_type, patterns in self.DANGEROUS_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, result.sanitized_value, re.IGNORECASE):
                    result.is_valid = False
                    result.security_issues.append(f"Potential {attack_type} detected: {pattern}")
        
        # Check for suspicious encodings
        if '%' in result.sanitized_value:
            try:
                decoded = urllib.parse.unquote(result.sanitized_value)
                if decoded != result.sanitized_value:
                    # Check decoded content for attacks
                    for attack_type, patterns in self.DANGEROUS_PATTERNS.items():
                        for pattern in patterns:
                            if re.search(pattern, decoded, re.IGNORECASE):
                                result.security_issues.append(f"URL-encoded {attack_type} detected")
            except Exception:
                pass
        
        return result
    
    def _apply_transformations(self, result: SanitizationResult, 
                            rules: SanitizationRule) -> SanitizationResult:
        """Apply transformation rules."""
        original_value = result.sanitized_value
        
        if rules.normalize_whitespace:
            # Normalize whitespace
            result.sanitized_value = re.sub(r'\s+', ' ', result.sanitized_value.strip())
            if result.sanitized_value != original_value:
                result.applied_transformations.append("normalized_whitespace")
        
        if rules.strip_html:
            # Strip HTML tags
            result.sanitized_value = html.escape(result.sanitized_value)
            if result.sanitized_value != original_value:
                result.applied_transformations.append("escaped_html")
        
        if not rules.case_sensitive:
            # Convert to lowercase
            result.sanitized_value = result.sanitized_value.lower()
            if result.sanitized_value != original_value:
                result.applied_transformations.append("converted_to_lowercase")
        
        return result
    
    def _apply_type_specific_validation(self, result: SanitizationResult, 
                                      input_type: InputType) -> SanitizationResult:
        """Apply type-specific validation."""
        if input_type == InputType.JSON:
            try:
                json.loads(result.sanitized_value)
            except json.JSONDecodeError as e:
                result.is_valid = False
                result.validation_errors.append(f"Invalid JSON: {e}")
        
        elif input_type == InputType.YAML:
            try:
                yaml.safe_load(result.sanitized_value)
            except yaml.YAMLError as e:
                result.is_valid = False
                result.validation_errors.append(f"Invalid YAML: {e}")
        
        elif input_type == InputType.PATH:
            try:
                path = Path(result.sanitized_value)
                # Check for dangerous path patterns
                if path.is_absolute() and not str(path).startswith('/tmp/'):
                    # Allow absolute paths only in safe directories
                    allowed_roots = ['/tmp/', '/var/tmp/', '/home/', '/Users/']
                    if not any(str(path).startswith(root) for root in allowed_roots):
                        result.security_issues.append("Absolute path outside allowed directories")
                
                # Check for path traversal attempts
                resolved = path.resolve()
                if '..' in path.parts:
                    result.security_issues.append("Path traversal attempt detected")
                    
            except Exception as e:
                result.validation_errors.append(f"Invalid path: {e}")
        
        elif input_type == InputType.PORT:
            try:
                port = int(result.sanitized_value)
                if port < 1 or port > 65535:
                    result.is_valid = False
                    result.validation_errors.append(f"Port number out of range: {port}")
            except ValueError:
                result.is_valid = False
                result.validation_errors.append("Invalid port number")
        
        return result
    
    def _apply_custom_validation(self, result: SanitizationResult, 
                               rules: SanitizationRule) -> SanitizationResult:
        """Apply custom validation function if provided."""
        if rules.custom_validator:
            try:
                is_valid, error_message = rules.custom_validator(result.sanitized_value)
                if not is_valid:
                    result.is_valid = False
                    result.validation_errors.append(f"Custom validation failed: {error_message}")
            except Exception as e:
                result.validation_errors.append(f"Custom validator error: {e}")
        
        return result
    
    def sanitize_user_input(self, prompt: str, input_type: InputType, 
                          rules: Optional[SanitizationRule] = None, 
                          max_attempts: int = 3) -> str:
        """Safely collect and sanitize user input with validation.
        
        Args:
            prompt: Input prompt for user
            input_type: Type of input validation
            rules: Optional custom rules
            max_attempts: Maximum validation attempts
            
        Returns:
            Sanitized and validated input string
            
        Raises:
            ValueError: If input validation fails after max attempts
        """
        for attempt in range(max_attempts):
            try:
                user_input = input(prompt).strip()
                result = self.sanitize_input(user_input, input_type, rules)
                
                if result.is_valid:
                    if result.applied_transformations:
                        print(f"Input sanitized: {', '.join(result.applied_transformations)}")
                    return result.sanitized_value
                else:
                    print(f"Invalid input: {'; '.join(result.validation_errors)}")
                    if result.security_issues:
                        print(f"Security issues: {'; '.join(result.security_issues)}")
                    
                    if attempt < max_attempts - 1:
                        print(f"Please try again ({attempt + 1}/{max_attempts})")
                    
            except KeyboardInterrupt:
                raise
            except Exception as e:
                print(f"Input error: {e}")
                if attempt < max_attempts - 1:
                    print(f"Please try again ({attempt + 1}/{max_attempts})")
        
        raise ValueError(f"Failed to get valid input after {max_attempts} attempts")
    
    def sanitize_file_content(self, content: str, file_type: str) -> SanitizationResult:
        """Sanitize file content based on file type.
        
        Args:
            content: File content to sanitize
            file_type: Type of file (json, yaml, md, etc.)
            
        Returns:
            SanitizationResult with sanitized content
        """
        type_mapping = {
            'json': InputType.JSON,
            'yaml': InputType.YAML,
            'yml': InputType.YAML,
            'md': InputType.TEXT,
            'txt': InputType.TEXT,
            'py': InputType.TEXT,
            'sh': InputType.COMMAND,
            'bat': InputType.COMMAND,
            'cmd': InputType.COMMAND,
        }
        
        input_type = type_mapping.get(file_type.lower(), InputType.TEXT)
        return self.sanitize_input(content, input_type)
    
    def validate_configuration(self, config: Dict[str, Any]) -> List[ValidationResult]:
        """Validate configuration dictionary for security issues.
        
        Args:
            config: Configuration dictionary to validate
            
        Returns:
            List of validation results
        """
        results = []
        
        def validate_recursive(obj: Any, path: str = "") -> None:
            if isinstance(obj, dict):
                for key, value in obj.items():
                    current_path = f"{path}.{key}" if path else key
                    
                    # Validate keys
                    key_result = self.sanitize_input(key, InputType.TEXT)
                    if not key_result.is_valid:
                        results.append(ValidationResult(
                            level=ValidationLevel.ERROR,
                            message=f"Invalid configuration key '{key}': {'; '.join(key_result.validation_errors)}",
                            metadata={"path": current_path}
                        ))
                    
                    # Recursively validate values
                    validate_recursive(value, current_path)
                    
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    validate_recursive(item, f"{path}[{i}]")
                    
            elif isinstance(obj, str):
                # Validate string values
                str_result = self.sanitize_input(obj, InputType.TEXT)
                if not str_result.is_valid:
                    results.append(ValidationResult(
                        level=ValidationLevel.ERROR,
                        message=f"Invalid configuration value at '{path}': {'; '.join(str_result.validation_errors)}",
                        metadata={"path": path, "value": obj}
                    ))
                
                if str_result.security_issues:
                    results.append(ValidationResult(
                        level=ValidationLevel.CRITICAL,
                        message=f"Security issues in configuration value at '{path}': {'; '.join(str_result.security_issues)}",
                        metadata={"path": path, "value": obj}
                    ))
        
        validate_recursive(config)
        return results
    
    def clear_cache(self) -> None:
        """Clear the validation cache."""
        self.validation_cache.clear()
    
    def get_cache_stats(self) -> Dict[str, int]:
        """Get cache statistics."""
        return {
            'cache_size': len(self.validation_cache),
            'cache_hits': getattr(self, '_cache_hits', 0),
            'cache_misses': getattr(self, '_cache_misses', 0)
        }


# Convenience functions for common validation tasks
def sanitize_filename(filename: str) -> str:
    """Sanitize a filename for safe use."""
    sanitizer = InputSanitizer()
    result = sanitizer.sanitize_input(filename, InputType.FILENAME)
    return result.sanitized_value


def sanitize_path(path: str) -> str:
    """Sanitize a file path for safe use."""
    sanitizer = InputSanitizer()
    result = sanitizer.sanitize_input(path, InputType.PATH)
    return result.sanitized_value


def sanitize_json(json_content: str) -> Tuple[str, bool]:
    """Sanitize JSON content and return (content, is_valid)."""
    sanitizer = InputSanitizer()
    result = sanitizer.sanitize_input(json_content, InputType.JSON)
    return result.sanitized_value, result.is_valid


def sanitize_yaml(yaml_content: str) -> Tuple[str, bool]:
    """Sanitize YAML content and return (content, is_valid)."""
    sanitizer = InputSanitizer()
    result = sanitizer.sanitize_input(yaml_content, InputType.YAML)
    return result.sanitized_value, result.is_valid


def validate_user_input(value: str, input_type: InputType) -> bool:
    """Quick validation of user input."""
    sanitizer = InputSanitizer()
    result = sanitizer.sanitize_input(value, input_type)
    return result.is_valid