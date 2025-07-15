"""Demonstration of comprehensive input validation system."""

from pathlib import Path
from .input_sanitizer import InputSanitizer, InputType
from .secure_input import SecureInputHandler, SecurePrompt
from .mcp_validator import MCPServerValidator
import json


def demo_basic_validation():
    """Demonstrate basic input validation."""
    print("=== Basic Input Validation Demo ===")
    
    sanitizer = InputSanitizer()
    
    # Test various input types
    test_cases = [
        ("Valid email", "user@example.com", InputType.EMAIL),
        ("Invalid email", "not-an-email", InputType.EMAIL),
        ("Valid URL", "https://example.com", InputType.URL),
        ("XSS attempt", "<script>alert('xss')</script>", InputType.TEXT),
        ("SQL injection", "'; DROP TABLE users; --", InputType.TEXT),
        ("Command injection", "ls; rm -rf /", InputType.COMMAND),
        ("Path traversal", "../../../etc/passwd", InputType.PATH),
        ("Valid filename", "document.txt", InputType.FILENAME),
        ("Invalid filename", "../../../etc/passwd", InputType.FILENAME),
        ("Valid port", "8080", InputType.PORT),
        ("Invalid port", "99999", InputType.PORT),
    ]
    
    for description, input_value, input_type in test_cases:
        result = sanitizer.sanitize_input(input_value, input_type)
        
        print(f"\n{description}: '{input_value}'")
        print(f"  Type: {input_type.value}")
        print(f"  Valid: {result.is_valid}")
        
        if result.sanitized_value != input_value:
            print(f"  Sanitized: '{result.sanitized_value}'")
        
        if result.validation_errors:
            print(f"  Validation errors: {result.validation_errors}")
        
        if result.security_issues:
            print(f"  🔒 Security issues: {result.security_issues}")
        
        if result.applied_transformations:
            print(f"  Transformations: {result.applied_transformations}")


def demo_configuration_validation():
    """Demonstrate configuration validation."""
    print("\n=== Configuration Validation Demo ===")
    
    sanitizer = InputSanitizer()
    
    # Test configuration with security issues
    malicious_config = {
        "project_name": "<script>alert('xss')</script>",
        "database_url": "'; DROP TABLE users; --",
        "server_command": "rm -rf /",
        "file_path": "../../../etc/passwd",
        "servers": {
            "web": {
                "url": "javascript:alert('xss')",
                "command": "python; rm -rf /"
            }
        }
    }
    
    print("Testing malicious configuration...")
    results = sanitizer.validate_configuration(malicious_config)
    
    for result in results:
        level_icon = {
            'info': 'ℹ️',
            'warning': '⚠️',
            'error': '❌',
            'critical': '🔒'
        }.get(result.level.value, '❓')
        
        print(f"{level_icon} {result.level.value.upper()}: {result.message}")
        if result.metadata:
            print(f"  Path: {result.metadata.get('path', 'N/A')}")
    
    # Test safe configuration
    safe_config = {
        "project_name": "my-safe-project",
        "database_url": "postgresql://localhost:5432/mydb",
        "server_command": "python",
        "file_path": "/home/user/project/script.py",
        "servers": {
            "web": {
                "url": "https://example.com",
                "command": "python"
            }
        }
    }
    
    print("\nTesting safe configuration...")
    results = sanitizer.validate_configuration(safe_config)
    
    if not results:
        print("✅ Configuration is safe!")
    else:
        for result in results:
            level_icon = {
                'info': 'ℹ️',
                'warning': '⚠️',
                'error': '❌',
                'critical': '🔒'
            }.get(result.level.value, '❓')
            
            print(f"{level_icon} {result.level.value.upper()}: {result.message}")


def demo_file_validation():
    """Demonstrate file content validation."""
    print("\n=== File Content Validation Demo ===")
    
    sanitizer = InputSanitizer()
    
    # Test JSON file validation
    json_files = [
        ("Safe JSON", '{"name": "safe-project", "version": "1.0.0"}'),
        ("Malicious JSON", '{"name": "<script>alert(\\"xss\\")</script>", "command": "rm -rf /"}'),
        ("Invalid JSON", '{"name": "project", "version": invalid}'),
    ]
    
    for description, content in json_files:
        print(f"\n{description}:")
        result = sanitizer.sanitize_file_content(content, "json")
        
        print(f"  Valid: {result.is_valid}")
        if result.validation_errors:
            print(f"  Validation errors: {result.validation_errors}")
        if result.security_issues:
            print(f"  🔒 Security issues: {result.security_issues}")


def demo_mcp_validation():
    """Demonstrate MCP server validation."""
    print("\n=== MCP Server Validation Demo ===")
    
    # Create a temporary settings file for testing
    test_config = {
        "mcpServers": {
            "safe-server": {
                "command": "python",
                "args": ["-m", "mcp_server"]
            },
            "malicious-server": {
                "command": "python; rm -rf /",
                "args": ["<script>alert('xss')</script>"]
            },
            "invalid-server": {
                "command": 123,  # Invalid type
                "args": "not a list"
            }
        }
    }
    
    # Create temporary config file
    import tempfile
    with tempfile.TemporaryDirectory() as temp_dir:
        config_path = Path(temp_dir)
        settings_file = config_path / "settings.json"
        
        with open(settings_file, 'w') as f:
            json.dump(test_config, f, indent=2)
        
        # Validate MCP servers
        validator = MCPServerValidator(config_path)
        results = validator.validate()
        
        print(f"Found {len(results)} validation issues:")
        for result in results:
            level_icon = {
                'info': 'ℹ️',
                'warning': '⚠️',
                'error': '❌',
                'critical': '🔒'
            }.get(result.level.value, '❓')
            
            print(f"{level_icon} {result.level.value.upper()}: {result.message}")
            if result.suggestion:
                print(f"  💡 Suggestion: {result.suggestion}")


def demo_secure_input_handling():
    """Demonstrate secure input handling (interactive)."""
    print("\n=== Secure Input Handling Demo ===")
    print("This would demonstrate interactive secure input handling.")
    print("In a real scenario, this would safely collect user input with validation.")
    
    # Example of how secure input would be used
    handler = SecureInputHandler()
    
    print("\nExample secure input configurations:")
    
    # Email input example
    email_prompt = SecurePrompt(
        message="Enter your email address",
        input_type=InputType.EMAIL,
        required=True,
        max_attempts=3
    )
    print(f"Email prompt: {email_prompt.message} (validates as {email_prompt.input_type.value})")
    
    # URL input example
    url_prompt = SecurePrompt(
        message="Enter server URL",
        input_type=InputType.URL,
        default_value="https://localhost:8080",
        required=False
    )
    print(f"URL prompt: {url_prompt.message} (validates as {url_prompt.input_type.value})")
    
    # Path input example
    path_prompt = SecurePrompt(
        message="Enter file path",
        input_type=InputType.PATH,
        required=True,
        max_attempts=3
    )
    print(f"Path prompt: {path_prompt.message} (validates as {path_prompt.input_type.value})")


def main():
    """Run all validation demos."""
    print("🔒 Comprehensive Input Validation System Demo")
    print("=" * 50)
    
    demo_basic_validation()
    demo_configuration_validation()
    demo_file_validation()
    demo_mcp_validation()
    demo_secure_input_handling()
    
    print("\n" + "=" * 50)
    print("✅ Demo completed successfully!")
    print("The input validation system is ready for use.")


if __name__ == "__main__":
    main()