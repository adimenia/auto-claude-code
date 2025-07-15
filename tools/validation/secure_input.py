"""Secure input handling utilities for setup and configuration."""

import os
import sys
import getpass
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, Callable
from dataclasses import dataclass

from .input_sanitizer import InputSanitizer, InputType, SanitizationRule


@dataclass
class SecurePrompt:
    """Configuration for secure input prompts."""
    message: str
    input_type: InputType
    default_value: Optional[str] = None
    required: bool = True
    mask_input: bool = False
    validation_rules: Optional[SanitizationRule] = None
    choices: Optional[List[str]] = None
    max_attempts: int = 3
    help_text: Optional[str] = None


class SecureInputHandler:
    """Secure input handler with comprehensive validation and sanitization."""
    
    def __init__(self, sanitizer: Optional[InputSanitizer] = None):
        """Initialize secure input handler.
        
        Args:
            sanitizer: Optional InputSanitizer instance
        """
        self.sanitizer = sanitizer or InputSanitizer()
        self.input_history: List[Dict[str, Any]] = []
        
    def secure_input(self, prompt: SecurePrompt) -> str:
        """Securely collect and validate user input.
        
        Args:
            prompt: SecurePrompt configuration
            
        Returns:
            Sanitized and validated input
            
        Raises:
            ValueError: If validation fails after max attempts
            KeyboardInterrupt: If user cancels input
        """
        if prompt.help_text:
            print(f"ℹ️  {prompt.help_text}")
        
        if prompt.choices:
            print(f"Valid choices: {', '.join(prompt.choices)}")
        
        for attempt in range(prompt.max_attempts):
            try:
                # Display prompt with default value
                display_prompt = prompt.message
                if prompt.default_value:
                    display_prompt += f" (default: {prompt.default_value})"
                display_prompt += ": "
                
                # Get input (masked if needed)
                if prompt.mask_input:
                    user_input = getpass.getpass(display_prompt)
                else:
                    user_input = input(display_prompt).strip()
                
                # Use default if no input provided
                if not user_input and prompt.default_value:
                    user_input = prompt.default_value
                
                # Check if input is required
                if prompt.required and not user_input:
                    print("❌ This field is required.")
                    continue
                
                # Validate choices
                if prompt.choices and user_input not in prompt.choices:
                    print(f"❌ Invalid choice. Valid options: {', '.join(prompt.choices)}")
                    continue
                
                # Sanitize and validate input
                result = self.sanitizer.sanitize_input(
                    user_input, 
                    prompt.input_type, 
                    prompt.validation_rules
                )
                
                if result.is_valid:
                    # Log successful input (without sensitive data)
                    self._log_input(prompt, user_input if not prompt.mask_input else "[MASKED]", True)
                    
                    # Show applied transformations
                    if result.applied_transformations:
                        print(f"✅ Input sanitized: {', '.join(result.applied_transformations)}")
                    
                    return result.sanitized_value
                else:
                    # Show validation errors
                    print(f"❌ Invalid input: {'; '.join(result.validation_errors)}")
                    
                    if result.security_issues:
                        print(f"🔒 Security issues detected: {'; '.join(result.security_issues)}")
                    
                    if attempt < prompt.max_attempts - 1:
                        print(f"Please try again ({attempt + 1}/{prompt.max_attempts})")
                    
            except KeyboardInterrupt:
                print("\n❌ Input cancelled by user.")
                raise
            except Exception as e:
                print(f"❌ Input error: {e}")
                if attempt < prompt.max_attempts - 1:
                    print(f"Please try again ({attempt + 1}/{prompt.max_attempts})")
        
        # Log failed input attempt
        self._log_input(prompt, "[FAILED]", False)
        raise ValueError(f"Failed to get valid input after {prompt.max_attempts} attempts")
    
    def secure_yes_no(self, message: str, default: bool = True) -> bool:
        """Securely collect yes/no input.
        
        Args:
            message: Question to ask user
            default: Default answer if user just presses enter
            
        Returns:
            True for yes, False for no
        """
        default_text = "Y/n" if default else "y/N"
        prompt = SecurePrompt(
            message=f"{message} ({default_text})",
            input_type=InputType.TEXT,
            default_value="yes" if default else "no",
            required=False,
            choices=["yes", "no", "y", "n", "Y", "N"],
            max_attempts=3
        )
        
        response = self.secure_input(prompt).lower()
        return response in ["yes", "y"]
    
    def secure_choice(self, message: str, choices: List[str], 
                     default: Optional[str] = None) -> str:
        """Securely collect choice from list of options.
        
        Args:
            message: Question to ask user
            choices: List of valid choices
            default: Default choice if user just presses enter
            
        Returns:
            Selected choice
        """
        prompt = SecurePrompt(
            message=message,
            input_type=InputType.TEXT,
            default_value=default,
            required=default is None,
            choices=choices,
            max_attempts=3
        )
        
        return self.secure_input(prompt)
    
    def secure_path(self, message: str, must_exist: bool = False, 
                   create_if_missing: bool = False) -> Path:
        """Securely collect and validate file path.
        
        Args:
            message: Question to ask user
            must_exist: Whether path must already exist
            create_if_missing: Whether to create path if it doesn't exist
            
        Returns:
            Validated Path object
        """
        def path_validator(path_str: str) -> tuple[bool, str]:
            try:
                path = Path(path_str)
                
                if must_exist and not path.exists():
                    return False, "Path does not exist"
                
                if create_if_missing and not path.exists():
                    try:
                        path.mkdir(parents=True, exist_ok=True)
                    except OSError as e:
                        return False, f"Cannot create path: {e}"
                
                return True, ""
            except Exception as e:
                return False, f"Invalid path: {e}"
        
        rules = SanitizationRule(
            input_type=InputType.PATH,
            custom_validator=path_validator
        )
        
        prompt = SecurePrompt(
            message=message,
            input_type=InputType.PATH,
            validation_rules=rules,
            max_attempts=3
        )
        
        path_str = self.secure_input(prompt)
        return Path(path_str)
    
    def secure_password(self, message: str, min_length: int = 8, 
                       require_complexity: bool = True) -> str:
        """Securely collect password with validation.
        
        Args:
            message: Question to ask user
            min_length: Minimum password length
            require_complexity: Whether to require complex passwords
            
        Returns:
            Validated password
        """
        def password_validator(password: str) -> tuple[bool, str]:
            if len(password) < min_length:
                return False, f"Password must be at least {min_length} characters"
            
            if require_complexity:
                has_upper = any(c.isupper() for c in password)
                has_lower = any(c.islower() for c in password)
                has_digit = any(c.isdigit() for c in password)
                has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
                
                if not (has_upper and has_lower and has_digit and has_special):
                    return False, "Password must contain uppercase, lowercase, digit, and special character"
            
            return True, ""
        
        rules = SanitizationRule(
            input_type=InputType.TEXT,
            min_length=min_length,
            custom_validator=password_validator
        )
        
        prompt = SecurePrompt(
            message=message,
            input_type=InputType.TEXT,
            mask_input=True,
            validation_rules=rules,
            max_attempts=3
        )
        
        return self.secure_input(prompt)
    
    def secure_email(self, message: str, default: Optional[str] = None) -> str:
        """Securely collect and validate email address.
        
        Args:
            message: Question to ask user
            default: Default email if user just presses enter
            
        Returns:
            Validated email address
        """
        prompt = SecurePrompt(
            message=message,
            input_type=InputType.EMAIL,
            default_value=default,
            required=default is None,
            max_attempts=3
        )
        
        return self.secure_input(prompt)
    
    def secure_url(self, message: str, default: Optional[str] = None, 
                  allowed_schemes: Optional[List[str]] = None) -> str:
        """Securely collect and validate URL.
        
        Args:
            message: Question to ask user
            default: Default URL if user just presses enter
            allowed_schemes: List of allowed URL schemes (default: http, https)
            
        Returns:
            Validated URL
        """
        if allowed_schemes is None:
            allowed_schemes = ["http", "https"]
        
        def url_validator(url: str) -> tuple[bool, str]:
            if not any(url.startswith(f"{scheme}://") for scheme in allowed_schemes):
                return False, f"URL must start with one of: {', '.join(f'{s}://' for s in allowed_schemes)}"
            return True, ""
        
        rules = SanitizationRule(
            input_type=InputType.URL,
            custom_validator=url_validator
        )
        
        prompt = SecurePrompt(
            message=message,
            input_type=InputType.URL,
            default_value=default,
            validation_rules=rules,
            required=default is None,
            max_attempts=3
        )
        
        return self.secure_input(prompt)
    
    def secure_port(self, message: str, default: Optional[int] = None, 
                   min_port: int = 1, max_port: int = 65535) -> int:
        """Securely collect and validate port number.
        
        Args:
            message: Question to ask user
            default: Default port if user just presses enter
            min_port: Minimum allowed port
            max_port: Maximum allowed port
            
        Returns:
            Validated port number
        """
        def port_validator(port_str: str) -> tuple[bool, str]:
            try:
                port = int(port_str)
                if port < min_port or port > max_port:
                    return False, f"Port must be between {min_port} and {max_port}"
                return True, ""
            except ValueError:
                return False, "Port must be a number"
        
        rules = SanitizationRule(
            input_type=InputType.PORT,
            custom_validator=port_validator
        )
        
        prompt = SecurePrompt(
            message=message,
            input_type=InputType.PORT,
            default_value=str(default) if default else None,
            validation_rules=rules,
            required=default is None,
            max_attempts=3
        )
        
        return int(self.secure_input(prompt))
    
    def secure_multiline(self, message: str, end_marker: str = "END") -> str:
        """Securely collect multiline input.
        
        Args:
            message: Question to ask user
            end_marker: Marker to end multiline input
            
        Returns:
            Validated multiline input
        """
        print(f"{message}")
        print(f"(Enter '{end_marker}' on a new line to finish)")
        
        lines = []
        while True:
            try:
                line = input()
                if line.strip() == end_marker:
                    break
                lines.append(line)
            except KeyboardInterrupt:
                print("\n❌ Input cancelled by user.")
                raise
        
        content = "\n".join(lines)
        result = self.sanitizer.sanitize_input(content, InputType.TEXT)
        
        if not result.is_valid:
            print(f"❌ Invalid input: {'; '.join(result.validation_errors)}")
            if result.security_issues:
                print(f"🔒 Security issues: {'; '.join(result.security_issues)}")
            raise ValueError("Invalid multiline input")
        
        return result.sanitized_value
    
    def _log_input(self, prompt: SecurePrompt, value: str, success: bool) -> None:
        """Log input attempt for audit trail."""
        log_entry = {
            "prompt": prompt.message,
            "input_type": prompt.input_type.value,
            "value": value,
            "success": success,
            "masked": prompt.mask_input,
            "timestamp": __import__("datetime").datetime.now().isoformat()
        }
        
        self.input_history.append(log_entry)
        
        # Keep only last 100 entries
        if len(self.input_history) > 100:
            self.input_history = self.input_history[-100:]
    
    def get_input_history(self) -> List[Dict[str, Any]]:
        """Get input history for audit purposes."""
        return self.input_history.copy()
    
    def clear_input_history(self) -> None:
        """Clear input history."""
        self.input_history.clear()


# Global instance for easy access
_secure_input_handler = SecureInputHandler()

# Convenience functions
def secure_input(message: str, input_type: InputType = InputType.TEXT, 
                default: Optional[str] = None, required: bool = True) -> str:
    """Quick secure input function."""
    prompt = SecurePrompt(
        message=message,
        input_type=input_type,
        default_value=default,
        required=required
    )
    return _secure_input_handler.secure_input(prompt)

def secure_yes_no(message: str, default: bool = True) -> bool:
    """Quick yes/no input function."""
    return _secure_input_handler.secure_yes_no(message, default)

def secure_choice(message: str, choices: List[str], default: Optional[str] = None) -> str:
    """Quick choice input function."""
    return _secure_input_handler.secure_choice(message, choices, default)

def secure_path(message: str, must_exist: bool = False, create_if_missing: bool = False) -> Path:
    """Quick path input function."""
    return _secure_input_handler.secure_path(message, must_exist, create_if_missing)

def secure_email(message: str, default: Optional[str] = None) -> str:
    """Quick email input function."""
    return _secure_input_handler.secure_email(message, default)

def secure_url(message: str, default: Optional[str] = None) -> str:
    """Quick URL input function."""
    return _secure_input_handler.secure_url(message, default)

def secure_port(message: str, default: Optional[int] = None) -> int:
    """Quick port input function."""
    return _secure_input_handler.secure_port(message, default)