"""MCP server connectivity and configuration validator."""

import json
import subprocess
import socket
from pathlib import Path
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse

from .base import BaseValidator, ValidationResult, ValidationLevel


class MCPServerValidator(BaseValidator):
    """Validator for MCP server configurations and connectivity."""
    
    def __init__(self, config_path: Path):
        super().__init__(config_path)
        self.settings_file = config_path / "settings.json"
        self.mcp_file = config_path / ".mcp.json"
        self.mcp_servers: Dict[str, Dict[str, Any]] = {}
        
    def validate(self) -> List[ValidationResult]:
        """Validate MCP server configuration and connectivity."""
        self.clear_results()
        
        # Check for MCP configuration files
        config_file = None
        if self.mcp_file.exists():
            config_file = self.mcp_file
        elif self.settings_file.exists():
            config_file = self.settings_file
        else:
            self.add_result(
                ValidationLevel.WARNING,
                f"No MCP configuration found. Checked: {self.mcp_file}, {self.settings_file}",
                suggestion="Create .mcp.json or settings.json with MCP server configurations"
            )
            return self.results
        
        # Load and validate configuration file
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                settings = json.load(f)
        except json.JSONDecodeError as e:
            self.add_result(
                ValidationLevel.ERROR,
                f"Invalid JSON in configuration file: {e}",
                file_path=config_file,
                suggestion="Fix JSON syntax errors"
            )
            return self.results
        except Exception as e:
            self.add_result(
                ValidationLevel.ERROR,
                f"Failed to read configuration file: {e}",
                file_path=config_file
            )
            return self.results
        
        # Extract MCP servers configuration
        mcp_config = settings.get("mcpServers", {})
        if not mcp_config:
            self.add_result(
                ValidationLevel.INFO,
                "No MCP servers configured",
                suggestion="Add MCP servers to mcpServers section for enhanced functionality"
            )
            return self.results
        
        self.mcp_servers = mcp_config
        
        # Validate each MCP server
        for server_name, server_config in mcp_config.items():
            self._validate_server_config(server_name, server_config)
            self._test_server_connectivity(server_name, server_config)
        
        return self.results
    
    def _validate_server_config(self, server_name: str, config: Dict[str, Any]) -> None:
        """Validate MCP server configuration structure."""
        required_fields = ["command"]  # args is optional
        
        for field in required_fields:
            if field not in config:
                config_file = self.mcp_file if self.mcp_file.exists() else self.settings_file
                self.add_result(
                    ValidationLevel.ERROR,
                    f"MCP server '{server_name}' missing required field: {field}",
                    file_path=config_file,
                    suggestion=f"Add '{field}' to server configuration"
                )
        
        # Validate command field
        command = config.get("command")
        if command:
            if isinstance(command, str):
                self._validate_command_executable(server_name, command)
            else:
                config_file = self.mcp_file if self.mcp_file.exists() else self.settings_file
                self.add_result(
                    ValidationLevel.ERROR,
                    f"MCP server '{server_name}' command must be a string",
                    file_path=config_file,
                    suggestion="Change command to a string value"
                )
        
        # Validate args field
        args = config.get("args")
        if args and not isinstance(args, list):
            config_file = self.mcp_file if self.mcp_file.exists() else self.settings_file
            self.add_result(
                ValidationLevel.ERROR,
                f"MCP server '{server_name}' args must be a list",
                file_path=config_file,
                suggestion="Change args to a list of strings"
            )
        
        # Validate optional fields
        env = config.get("env")
        if env and not isinstance(env, dict):
            config_file = self.mcp_file if self.mcp_file.exists() else self.settings_file
            self.add_result(
                ValidationLevel.ERROR,
                f"MCP server '{server_name}' env must be an object",
                file_path=config_file,
                suggestion="Change env to an object with key-value pairs"
            )
        
        # Check for deprecated configurations
        if "url" in config:
            self.add_result(
                ValidationLevel.WARNING,
                f"MCP server '{server_name}' uses deprecated 'url' field",
                file_path=self.settings_file,
                suggestion="Use 'command' and 'args' instead of 'url'"
            )
    
    def _validate_command_executable(self, server_name: str, command: str) -> None:
        """Validate that the command is executable."""
        # Check if it's a full path
        if "/" in command or "\\" in command:
            command_path = Path(command)
            if not command_path.exists():
                self.add_result(
                    ValidationLevel.ERROR,
                    f"MCP server '{server_name}' command not found: {command}",
                    suggestion="Install the required package or fix the path"
                )
            elif not command_path.is_file():
                self.add_result(
                    ValidationLevel.ERROR,
                    f"MCP server '{server_name}' command is not a file: {command}",
                    suggestion="Ensure the command points to an executable file"
                )
        else:
            # Check if command is in PATH
            try:
                subprocess.run(['which', command], capture_output=True, check=True)
            except subprocess.CalledProcessError:
                self.add_result(
                    ValidationLevel.WARNING,
                    f"MCP server '{server_name}' command not found in PATH: {command}",
                    suggestion=f"Install {command} or provide full path to executable"
                )
            except Exception:
                # Fallback for non-Unix systems
                pass
    
    def _test_server_connectivity(self, server_name: str, config: Dict[str, Any]) -> None:
        """Test MCP server connectivity and basic functionality."""
        command = config.get("command")
        args = config.get("args", [])
        env = config.get("env", {})
        
        if not command:
            return
        
        try:
            # Try to start the server process briefly
            process = subprocess.Popen(
                [command] + args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env={**subprocess.os.environ, **env}
            )
            
            # Give it a moment to start
            try:
                stdout, stderr = process.communicate(timeout=2)
                if process.returncode is None:
                    process.terminate()
                    self.add_result(
                        ValidationLevel.INFO,
                        f"MCP server '{server_name}' started successfully",
                        metadata={"server_name": server_name}
                    )
                elif process.returncode != 0:
                    error_msg = stderr.decode('utf-8', errors='ignore')[:200]
                    self.add_result(
                        ValidationLevel.WARNING,
                        f"MCP server '{server_name}' exited with error: {error_msg}",
                        suggestion="Check server configuration and dependencies"
                    )
            except subprocess.TimeoutExpired:
                process.terminate()
                self.add_result(
                    ValidationLevel.INFO,
                    f"MCP server '{server_name}' is running (timeout reached)",
                    metadata={"server_name": server_name}
                )
        
        except FileNotFoundError:
            self.add_result(
                ValidationLevel.ERROR,
                f"MCP server '{server_name}' command not found: {command}",
                suggestion=f"Install required package for {command}"
            )
        except PermissionError:
            self.add_result(
                ValidationLevel.ERROR,
                f"MCP server '{server_name}' permission denied: {command}",
                suggestion="Check file permissions for the command"
            )
        except Exception as e:
            self.add_result(
                ValidationLevel.WARNING,
                f"MCP server '{server_name}' connectivity test failed: {e}",
                suggestion="Check server configuration and system requirements"
            )
    
    def _validate_server_url(self, server_name: str, url: str) -> None:
        """Validate server URL format and connectivity (for URL-based servers)."""
        try:
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                self.add_result(
                    ValidationLevel.ERROR,
                    f"MCP server '{server_name}' invalid URL format: {url}",
                    suggestion="Use format: protocol://host:port/path"
                )
                return
            
            # Test connectivity for HTTP/HTTPS URLs
            if parsed.scheme in ('http', 'https'):
                self._test_http_connectivity(server_name, url)
            elif parsed.scheme in ('ws', 'wss'):
                self._test_websocket_connectivity(server_name, url)
            
        except Exception as e:
            self.add_result(
                ValidationLevel.ERROR,
                f"MCP server '{server_name}' URL validation failed: {e}",
                suggestion="Check URL format and accessibility"
            )
    
    def _test_http_connectivity(self, server_name: str, url: str) -> None:
        """Test HTTP/HTTPS connectivity."""
        try:
            import urllib.request
            with urllib.request.urlopen(url, timeout=5) as response:
                if response.status == 200:
                    self.add_result(
                        ValidationLevel.INFO,
                        f"MCP server '{server_name}' HTTP connectivity OK",
                        metadata={"url": url, "status": response.status}
                    )
                else:
                    self.add_result(
                        ValidationLevel.WARNING,
                        f"MCP server '{server_name}' HTTP returned status {response.status}",
                        suggestion=f"Check server status at {url}"
                    )
        except Exception as e:
            self.add_result(
                ValidationLevel.WARNING,
                f"MCP server '{server_name}' HTTP connectivity failed: {e}",
                suggestion=f"Verify server is running at {url}"
            )
    
    def _test_websocket_connectivity(self, server_name: str, url: str) -> None:
        """Test WebSocket connectivity."""
        parsed = urlparse(url)
        host = parsed.hostname
        port = parsed.port or (443 if parsed.scheme == 'wss' else 80)
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((host, port))
            sock.close()
            
            if result == 0:
                self.add_result(
                    ValidationLevel.INFO,
                    f"MCP server '{server_name}' WebSocket port accessible",
                    metadata={"url": url, "host": host, "port": port}
                )
            else:
                self.add_result(
                    ValidationLevel.WARNING,
                    f"MCP server '{server_name}' WebSocket port not accessible",
                    suggestion=f"Check if server is running on {host}:{port}"
                )
        except Exception as e:
            self.add_result(
                ValidationLevel.WARNING,
                f"MCP server '{server_name}' WebSocket connectivity test failed: {e}",
                suggestion=f"Verify server accessibility at {url}"
            )
    
    def get_server_names(self) -> List[str]:
        """Get list of configured MCP server names."""
        return list(self.mcp_servers.keys())
    
    def get_server_config(self, server_name: str) -> Optional[Dict[str, Any]]:
        """Get configuration for a specific server."""
        return self.mcp_servers.get(server_name)