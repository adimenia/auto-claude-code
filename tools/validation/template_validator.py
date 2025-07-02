"""Template compatibility and structure validator."""

from pathlib import Path
from typing import List, Dict, Any, Set
import json

from .base import BaseValidator, ValidationResult, ValidationLevel


class TemplateValidator(BaseValidator):
    """Validator for template structure and compatibility."""
    
    REQUIRED_FILES = {
        "CLAUDE.md": "Main configuration file",
        "settings.json": "Claude Code settings"
    }
    
    OPTIONAL_FILES = {
        "commands/": "Command library directory",
        "README.md": "Documentation",
        ".gitignore": "Git ignore file"
    }
    
    def __init__(self, config_path: Path):
        super().__init__(config_path)
        self.template_type = self._detect_template_type()
    
    def validate(self) -> List[ValidationResult]:
        """Validate template structure and compatibility."""
        self.clear_results()
        
        # Validate required files
        self._validate_required_files()
        
        # Validate directory structure
        self._validate_directory_structure()
        
        # Validate template-specific requirements
        self._validate_template_specific()
        
        # Check for common issues
        self._check_common_issues()
        
        return self.results
    
    def _detect_template_type(self) -> str:
        """Detect template type from configuration."""
        settings_file = self.config_path / "settings.json"
        
        if settings_file.exists():
            try:
                with open(settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                
                # Check for framework-specific indicators
                mcp_servers = settings.get("mcpServers", {})
                
                if "filesystem" in mcp_servers and "sqlite" in mcp_servers:
                    return "data-science"
                elif "filesystem" in mcp_servers:
                    return "web-framework"
                else:
                    return "general"
            except (json.JSONDecodeError, IOError):
                pass
        
        # Try to detect from CLAUDE.md content
        claude_file = self.config_path / "CLAUDE.md"
        if claude_file.exists():
            try:
                content = claude_file.read_text(encoding='utf-8').lower()
                
                if "fastapi" in content:
                    return "fastapi"
                elif "django" in content:
                    return "django"
                elif "flask" in content:
                    return "flask"
                elif "data science" in content or "jupyter" in content:
                    return "data-science"
                elif "cli" in content or "command line" in content:
                    return "cli-tool"
                elif "web scraping" in content or "scraping" in content:
                    return "web-scraping"
                else:
                    return "core"
            except IOError:
                pass
        
        return "unknown"
    
    def _validate_required_files(self) -> None:
        """Validate presence of required files."""
        for file_name, description in self.REQUIRED_FILES.items():
            file_path = self.config_path / file_name
            
            if not file_path.exists():
                self.add_result(
                    ValidationLevel.ERROR,
                    f"Required file missing: {file_name} ({description})",
                    file_path=file_path,
                    auto_fixable=True,
                    suggestion=f"Create {file_name} file"
                )
            elif file_path.is_file() and file_path.stat().st_size == 0:
                self.add_result(
                    ValidationLevel.WARNING,
                    f"Required file is empty: {file_name}",
                    file_path=file_path,
                    suggestion=f"Add content to {file_name}"
                )
    
    def _validate_directory_structure(self) -> None:
        """Validate template directory structure."""
        # Check for commands directory structure
        commands_dir = self.config_path / "commands"
        if commands_dir.exists():
            self._validate_commands_structure(commands_dir)
        else:
            self.add_result(
                ValidationLevel.INFO,
                "Commands directory not found",
                suggestion="Consider adding a commands/ directory with workflow templates"
            )
        
        # Check for proper file organization
        loose_files = [f for f in self.config_path.iterdir() 
                      if f.is_file() and f.suffix in ['.py', '.js', '.ts'] 
                      and f.name not in ['setup.py']]
        
        if loose_files:
            self.add_result(
                ValidationLevel.WARNING,
                f"Found loose code files in root: {[f.name for f in loose_files]}",
                suggestion="Consider organizing code files in appropriate subdirectories"
            )
    
    def _validate_commands_structure(self, commands_dir: Path) -> None:
        """Validate commands directory structure."""
        expected_categories = {
            "development", "documentation", "planning", 
            "quality", "utility", "workflow"
        }
        
        existing_categories = {d.name for d in commands_dir.iterdir() if d.is_dir()}
        
        # Check for common command categories
        missing_categories = expected_categories - existing_categories
        if missing_categories:
            self.add_result(
                ValidationLevel.INFO,
                f"Missing command categories: {list(missing_categories)}",
                suggestion="Consider adding these common command categories"
            )
        
        # Validate command files
        for category_dir in commands_dir.iterdir():
            if category_dir.is_dir():
                self._validate_command_category(category_dir)
    
    def _validate_command_category(self, category_dir: Path) -> None:
        """Validate command category directory."""
        md_files = list(category_dir.glob("*.md"))
        
        if not md_files:
            self.add_result(
                ValidationLevel.WARNING,
                f"Empty command category: {category_dir.name}",
                file_path=category_dir,
                suggestion=f"Add command templates to {category_dir.name}/ directory"
            )
        
        # Validate command file structure
        for md_file in md_files:
            self._validate_command_file(md_file)
    
    def _validate_command_file(self, command_file: Path) -> None:
        """Validate individual command file."""
        try:
            content = command_file.read_text(encoding='utf-8')
            
            # Check for basic markdown structure
            if not content.strip().startswith('#'):
                self.add_result(
                    ValidationLevel.WARNING,
                    f"Command file should start with markdown header: {command_file.name}",
                    file_path=command_file,
                    suggestion="Add # Title at the beginning of the command file"
                )
            
            # Check for command description
            if len(content.strip()) < 50:
                self.add_result(
                    ValidationLevel.INFO,
                    f"Command file seems minimal: {command_file.name}",
                    file_path=command_file,
                    suggestion="Consider adding more detailed command documentation"
                )
        
        except IOError:
            self.add_result(
                ValidationLevel.ERROR,
                f"Could not read command file: {command_file.name}",
                file_path=command_file
            )
    
    def _validate_template_specific(self) -> None:
        """Validate template-specific requirements."""
        if self.template_type == "fastapi":
            self._validate_fastapi_template()
        elif self.template_type == "django":
            self._validate_django_template()
        elif self.template_type == "flask":
            self._validate_flask_template()
        elif self.template_type == "data-science":
            self._validate_data_science_template()
        elif self.template_type == "cli-tool":
            self._validate_cli_template()
        elif self.template_type == "web-scraping":
            self._validate_web_scraping_template()
    
    def _validate_fastapi_template(self) -> None:
        """Validate FastAPI-specific requirements."""
        self._check_mcp_servers(["filesystem", "sqlite"], "FastAPI development")
        self._check_claude_content(["FastAPI", "async", "API"], "FastAPI")
    
    def _validate_django_template(self) -> None:
        """Validate Django-specific requirements."""
        self._check_mcp_servers(["filesystem", "sqlite"], "Django development")
        self._check_claude_content(["Django", "models", "views"], "Django")
    
    def _validate_flask_template(self) -> None:
        """Validate Flask-specific requirements."""
        self._check_mcp_servers(["filesystem"], "Flask development")
        self._check_claude_content(["Flask", "routes", "templates"], "Flask")
    
    def _validate_data_science_template(self) -> None:
        """Validate data science template requirements."""
        required_servers = ["filesystem", "sqlite", "memory"]
        self._check_mcp_servers(required_servers, "data science work")
        self._check_claude_content(["data", "analysis", "jupyter", "pandas"], "data science")
    
    def _validate_cli_template(self) -> None:
        """Validate CLI tool template requirements."""
        self._check_mcp_servers(["filesystem"], "CLI development")
        self._check_claude_content(["CLI", "command", "argparse", "click"], "CLI tool")
    
    def _validate_web_scraping_template(self) -> None:
        """Validate web scraping template requirements."""
        required_servers = ["filesystem", "memory"]
        self._check_mcp_servers(required_servers, "web scraping")
        self._check_claude_content(["scraping", "requests", "beautifulsoup", "selenium"], "web scraping")
    
    def _check_mcp_servers(self, required_servers: List[str], context: str) -> None:
        """Check for required MCP servers."""
        settings_file = self.config_path / "settings.json"
        if not settings_file.exists():
            return
        
        try:
            with open(settings_file, 'r', encoding='utf-8') as f:
                settings = json.load(f)
            
            mcp_servers = settings.get("mcpServers", {})
            existing_servers = set(mcp_servers.keys())
            missing_servers = set(required_servers) - existing_servers
            
            if missing_servers:
                self.add_result(
                    ValidationLevel.WARNING,
                    f"Missing recommended MCP servers for {context}: {list(missing_servers)}",
                    file_path=settings_file,
                    suggestion=f"Add {list(missing_servers)} MCP servers for better {context} support"
                )
        
        except (json.JSONDecodeError, IOError):
            pass
    
    def _check_claude_content(self, keywords: List[str], template_type: str) -> None:
        """Check CLAUDE.md content for template-specific keywords."""
        claude_file = self.config_path / "CLAUDE.md"
        if not claude_file.exists():
            return
        
        try:
            content = claude_file.read_text(encoding='utf-8').lower()
            missing_keywords = [kw for kw in keywords if kw.lower() not in content]
            
            if missing_keywords:
                self.add_result(
                    ValidationLevel.INFO,
                    f"CLAUDE.md might benefit from {template_type}-specific content: {missing_keywords}",
                    file_path=claude_file,
                    suggestion=f"Consider adding {template_type}-specific instructions and examples"
                )
        
        except IOError:
            pass
    
    def _check_common_issues(self) -> None:
        """Check for common template issues."""
        # Check for version information
        self._check_version_info()
        
        # Check for documentation
        self._check_documentation()
        
        # Check for git configuration
        self._check_git_setup()
    
    def _check_version_info(self) -> None:
        """Check for version information in configuration."""
        has_version = False
        
        # Check CLAUDE.md for version
        claude_file = self.config_path / "CLAUDE.md"
        if claude_file.exists():
            try:
                content = claude_file.read_text(encoding='utf-8')
                if "version" in content.lower() or "v2." in content or "v1." in content:
                    has_version = True
            except IOError:
                pass
        
        # Check settings.json for version
        settings_file = self.config_path / "settings.json"
        if settings_file.exists():
            try:
                with open(settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                if "version" in settings:
                    has_version = True
            except (json.JSONDecodeError, IOError):
                pass
        
        if not has_version:
            self.add_result(
                ValidationLevel.INFO,
                "No version information found in configuration",
                suggestion="Consider adding version information for better tracking"
            )
    
    def _check_documentation(self) -> None:
        """Check for documentation files."""
        readme_file = self.config_path / "README.md"
        
        if not readme_file.exists():
            self.add_result(
                ValidationLevel.INFO,
                "No README.md found",
                suggestion="Consider adding a README.md with setup and usage instructions"
            )
        elif readme_file.stat().st_size < 100:
            self.add_result(
                ValidationLevel.INFO,
                "README.md seems minimal",
                file_path=readme_file,
                suggestion="Consider expanding README.md with more detailed information"
            )
    
    def _check_git_setup(self) -> None:
        """Check for proper git setup."""
        gitignore_file = self.config_path / ".gitignore"
        
        if not gitignore_file.exists():
            self.add_result(
                ValidationLevel.INFO,
                "No .gitignore file found",
                suggestion="Consider adding .gitignore to exclude unnecessary files from version control"
            )
    
    def get_template_type(self) -> str:
        """Get detected template type."""
        return self.template_type
    
    def get_compatibility_score(self) -> float:
        """Calculate template compatibility score."""
        total_checks = len(self.results)
        if total_checks == 0:
            return 100.0
        
        errors = len([r for r in self.results if r.is_error])
        warnings = len([r for r in self.results if r.level == ValidationLevel.WARNING])
        
        # Calculate score
        error_penalty = errors * 20
        warning_penalty = warnings * 5
        
        score = max(0, 100 - error_penalty - warning_penalty)
        return min(100.0, score)