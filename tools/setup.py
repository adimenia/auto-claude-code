#!/usr/bin/env python3
"""
Claude Code Configuration Setup Tool

Interactive tool for setting up Claude Code configurations with framework-specific templates.
Supports FastAPI, Django, Flask, Data Science, CLI Tool, and Web Scraping projects.
"""

import json
import os
import shutil
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
import argparse
import shutil
from typing import Optional
try:
    from rich.console import Console
    from rich.prompt import Prompt, Confirm
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.syntax import Syntax
    HAS_RICH = True
except ImportError:
    HAS_RICH = False
    print("⚠️  Rich library not found. Install with: pip install rich")
    print("   Falling back to basic text interface...")
try:
    import questionary
    HAS_QUESTIONARY = True
except ImportError:
    HAS_QUESTIONARY = False
    if HAS_RICH:
        console.print("💡 [dim]Install questionary for enhanced autocomplete: pip install questionary[/dim]")

# Initialize console
if HAS_RICH:
    console = Console()
else:
    class SimpleConsole:
        def print(self, text, style=None, **kwargs):
            print(text)
        def input(self, prompt):
            return input(prompt)
    console = SimpleConsole()


class ClaudeSetupTool:
    """Interactive setup tool for Claude Code configurations."""
    
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.repo_root = self.script_dir.parent
        self.templates_dir = self.repo_root / "templates" / "project" / "frameworks"
        self.current_dir = Path.cwd()
        
        # Available frameworks
        self.frameworks = {
            "core": {
                "name": "Core Python",
                "description": "General-purpose Python project with modern development tools",
                "use_cases": ["Libraries", "Utilities", "Research", "Learning", "Custom apps"],
                "tech_stack": ["Python", "pytest", "Black", "mypy", "setuptools/Poetry"]
            },
            "fastapi": {
                "name": "FastAPI",
                "description": "Modern async web framework for building high-performance APIs",
                "use_cases": ["REST APIs", "Microservices", "Real-time applications"],
                "tech_stack": ["FastAPI", "Uvicorn", "SQLAlchemy", "Alembic", "Pydantic"]
            },
            "django": {
                "name": "Django",
                "description": "Full-featured web framework for rapid development",
                "use_cases": ["Web applications", "Admin interfaces", "Content management"],
                "tech_stack": ["Django", "Django ORM", "Templates", "Admin", "Forms"]
            },
            "flask": {
                "name": "Flask",
                "description": "Lightweight and flexible web framework",
                "use_cases": ["Microservices", "Simple APIs", "Prototypes"],
                "tech_stack": ["Flask", "Jinja2", "SQLAlchemy", "Flask-WTF", "Blueprints"]
            },
            "data-science": {
                "name": "Data Science",
                "description": "Machine learning and data analysis workflows",
                "use_cases": ["ML models", "Data analysis", "Research", "Jupyter notebooks"],
                "tech_stack": ["Pandas", "NumPy", "Scikit-learn", "Jupyter", "MLflow"]
            },
            "cli-tool": {
                "name": "CLI Tool",
                "description": "Command-line applications and automation tools",
                "use_cases": ["Command-line apps", "Automation scripts", "Developer tools"],
                "tech_stack": ["Click", "Typer", "Rich", "PyInstaller", "ConfigArgParse"]
            },
            "web-scraping": {
                "name": "Web Scraping",
                "description": "Ethical web scraping and data extraction",
                "use_cases": ["Data extraction", "Web automation", "Research"],
                "tech_stack": ["Requests", "BeautifulSoup", "Scrapy", "Selenium", "Playwright"]
            }
        }
        
        # Configuration options
        self.databases = {
            "postgresql": "PostgreSQL (Recommended for production)",
            "mysql": "MySQL/MariaDB",
            "sqlite": "SQLite (Good for development)",
            "none": "No database needed"
        }
        
        self.environments = {
            "development": "Development (Local machine)",
            "staging": "Staging (Pre-production)",
            "production": "Production (Live environment)"
        }
    def _get_project_name_suggestions(self) -> List[str]:
        """Generate smart project name suggestions."""
        suggestions = []
        
        # Current directory name
        current_name = self.current_dir.name
        if current_name and current_name != '.':
            suggestions.append(current_name)
        
        # Git repository name
        try:
            import subprocess
            result = subprocess.run(['git', 'remote', 'get-url', 'origin'], check=True, capture_output=True, text=True, timeout=2)
            if result.returncode == 0:
                git_url = result.stdout.strip()
                if git_url:
                    repo_name = git_url.split('/')[-1].replace('.git', '')
                    if repo_name and repo_name not in suggestions:
                        suggestions.append(repo_name)
        except Exception:
            pass
        
        # Common defaults
        defaults = ["my-awesome-project", "claude-project", "new-project"]
        for default in defaults:
            if default not in suggestions:
                suggestions.append(default)
        
        return suggestions[:8]
    def configure_command_library(self, config: Dict[str, Any], mode: str) -> Dict[str, Any]:
        """Configure command library installation options."""
        command_config = {}
        
        if HAS_QUESTIONARY:
            questionary.print("\n🔧 Claude Code Command Library Setup", style="bold fg:#61afef")
            questionary.print("Install pre-built commands for common development tasks", style="fg:#6c7086")
            
            # Global vs Project installation choice
            install_global = questionary.confirm(
                "Install global command library to ~/.claude/commands/?",
                default=True
            ).ask()
            command_config["install_global"] = install_global
            
            if install_global:
                questionary.print("✨ Global commands will be available as /user:command-name", style="fg:#98c379")
            
            # Project commands installation
            install_project = questionary.confirm(
                "Install project-specific commands to .claude/commands/?",
                default=True
            ).ask()
            command_config["install_project"] = install_project
            
            if install_project:
                questionary.print("🎯 Project commands will be available as /project:command-name", style="fg:#98c379")
                
                # Command categories selection
                categories = [
                    questionary.Choice("Planning (analyze requirements, create architecture)", "planning", checked=True),
                    questionary.Choice("Development (create features, fix bugs, refactor)", "development", checked=True),
                    questionary.Choice("Quality (code review, security check, performance)", "quality", checked=True),
                    questionary.Choice("Documentation (create docs, update README, API docs)", "documentation", checked=True),
                    questionary.Choice("Workflow (commit changes, create PR, deploy)", "workflow", checked=True),
                    questionary.Choice("Utility (cleanup code, update deps, backup)", "utility", checked=True)
                ]
                
                selected_categories = questionary.checkbox(
                    "Select command categories to install:",
                    choices=categories
                ).ask()
                
                command_config["categories"] = selected_categories or ["workflow", "quality"]  # Minimal default
            
        elif HAS_RICH:
            console.print(f"\n[bold blue]🔧 Claude Code Command Library Setup[/bold blue]")
            console.print("[dim]Install pre-built commands for common development tasks[/dim]")
            
            command_config["install_global"] = Confirm.ask("Install global command library?", default=True)
            command_config["install_project"] = Confirm.ask("Install project commands?", default=True)
            
            if command_config["install_project"]:
                # Simple category selection for Rich
                console.print("[bold]Available categories:[/bold]")
                console.print("1. Planning  2. Development  3. Quality")
                console.print("4. Documentation  5. Workflow  6. Utility")
                
                categories_input = Prompt.ask(
                    "Select categories (comma-separated numbers, default: all)",
                    default="1,2,3,4,5,6"
                )
                
                try:
                    category_map = {
                        "1": "planning", "2": "development", "3": "quality",
                        "4": "documentation", "5": "workflow", "6": "utility"
                    }
                    selected_numbers = [n.strip() for n in categories_input.split(",")]
                    command_config["categories"] = [category_map[n] for n in selected_numbers if n in category_map]
                except:
                    command_config["categories"] = ["planning", "development", "quality", "documentation", "workflow", "utility"]
        
        else:
            print("\n🔧 Claude Code Command Library Setup")
            print("Install pre-built commands for common development tasks")
            
            install_global = input("Install global command library? (Y/n): ").strip().lower() not in ['n', 'no']
            command_config["install_global"] = install_global
            
            install_project = input("Install project commands? (Y/n): ").strip().lower() not in ['n', 'no']
            command_config["install_project"] = install_project
            
            if install_project:
                print("Categories: planning, development, quality, documentation, workflow, utility")
                categories_input = input("Select categories (comma-separated, default: all): ").strip()
                if categories_input:
                    command_config["categories"] = [c.strip() for c in categories_input.split(",")]
                else:
                    command_config["categories"] = ["planning", "development", "quality", "documentation", "workflow", "utility"]
        
        config["command_library"] = command_config
        return config
    
    def configure_personas(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Configure persona installation options."""
        persona_config = {}
        
        if HAS_QUESTIONARY:
            questionary.print("\n🎭 Claude Code Personas Setup", style="bold fg:#61afef")
            questionary.print("Install pre-built personas for specialized tasks", style="fg:#6c7086")
            
            install_personas = questionary.confirm(
                "Install personas to .claude/personas/?",
                default=True
            ).ask()
            persona_config["install_personas"] = install_personas
            
            if install_personas:
                questionary.print("✨ Personas will be available as /persona persona-name", style="fg:#98c379")
                
                # Persona selection
                personas = [
                    questionary.Choice("Architect", "architect", checked=True),
                    questionary.Choice("Developer", "developer", checked=True),
                    questionary.Choice("Tester", "tester", checked=True),
                ]
                
                selected_personas = questionary.checkbox(
                    "Select personas to install:",
                    choices=personas
                ).ask()
                
                persona_config["personas"] = selected_personas or []
            
        elif HAS_RICH:
            console.print(f"\n[bold blue]🎭 Claude Code Personas Setup[/bold blue]")
            console.print("[dim]Install pre-built personas for specialized tasks[/dim]")
            
            persona_config["install_personas"] = Confirm.ask("Install personas?", default=True)
            
            if persona_config["install_personas"]:
                # Simple persona selection for Rich
                console.print("[bold]Available personas:[/bold]")
                console.print("1. Architect  2. Developer  3. Tester")
                
                personas_input = Prompt.ask(
                    "Select personas (comma-separated numbers, default: all)",
                    default="1,2,3"
                )
                
                try:
                    persona_map = {
                        "1": "architect", "2": "developer", "3": "tester"
                    }
                    selected_numbers = [n.strip() for n in personas_input.split(",")]
                    persona_config["personas"] = [persona_map[n] for n in selected_numbers if n in persona_map]
                except:
                    persona_config["personas"] = ["architect", "developer", "tester"]
        
        else:
            print("\n🎭 Claude Code Personas Setup")
            print("Install pre-built personas for specialized tasks")
            
            install_personas = input("Install personas? (Y/n): ").strip().lower() not in ['n', 'no']
            persona_config["install_personas"] = install_personas
            
            if install_personas:
                print("Personas: architect, developer, tester")
                personas_input = input("Select personas (comma-separated, default: all): ").strip()
                if personas_input:
                    persona_config["personas"] = [p.strip() for p in personas_input.split(",")]
                else:
                    persona_config["personas"] = ["architect", "developer", "tester"]
        
        config["personas"] = persona_config
        return config
    
    def install_command_library(self, config: Dict[str, Any], target_dir: Path):
        """Install command library based on configuration."""
        command_config = config.get("command_library", {})
        
        if not command_config:
            return
        
        if HAS_QUESTIONARY:
            questionary.print("\n📦 Installing command library...", style="fg:#6c7086")
        elif HAS_RICH:
            console.print("\n[dim]📦 Installing command library...[/dim]")
        else:
            print("\n📦 Installing command library...")
        
        # Install global commands
        if command_config.get("install_global", False):
            self.install_global_commands(config)
        
        # Install project commands
        if command_config.get("install_project", False):
            categories = command_config.get("categories", [])
            self.install_project_commands(config, target_dir, categories)
        
    def install_personas(self, config: Dict[str, Any], target_dir: Path):
        """Install personas based on configuration."""
        persona_config = config.get("personas", {})
        
        if not persona_config or not persona_config.get("install_personas", False):
            return
        
        if HAS_QUESTIONARY:
            questionary.print("\n🎭 Installing personas...", style="fg:#6c7086")
        elif HAS_RICH:
            console.print("\n[dim]🎭 Installing personas...[/dim]")
        else:
            print("\n🎭 Installing personas...")
        
        personas_to_install = persona_config.get("personas", [])
        source_personas_dir = self.repo_root / "templates" / "personas"
        target_personas_dir = target_dir / ".claude" / "personas"
        target_personas_dir.mkdir(parents=True, exist_ok=True)
        
        installed_count = 0
        for persona_name in personas_to_install:
            source_file = source_personas_dir / f"{persona_name}.md"
            target_file = target_personas_dir / f"{persona_name}.md"
            if source_file.exists() and not target_file.exists():
                shutil.copy2(source_file, target_file)
                installed_count += 1
        
        if installed_count > 0:
            if HAS_QUESTIONARY:
                questionary.print(f"✅ Installed {installed_count} personas to .claude/personas/", style="fg:#98c379")
                questionary.print("   Usage: /persona persona-name", style="fg:#6c7086")
            elif HAS_RICH:
                console.print(f"[green]✅ Installed {installed_count} personas[/green]")
                console.print("[dim]   Usage: /persona persona-name[/dim]")
            else:
                print(f"✅ Installed {installed_count} personas to .claude/personas/")
                print("   Usage: /persona persona-name")
        
    def _get_recommended_servers(self, framework: str) -> List[str]:
        """Get recommended MCP servers for framework."""
        recommendations = {
            "fastapi": ["postgresql", "fetch", "context7", "puppeteer", "magic"],
            "django": ["postgresql", "fetch", "context7", "puppeteer", "magic"],
            "flask": ["sqlite", "fetch", "context7", "puppeteer", "magic"],
            "data-science": ["context7", "puppeteer", "magic"],
            "cli-tool": ["filesystem", "context7", "puppeteer", "magic"],
            "web-scraping": ["fetch", "filesystem", "context7", "puppeteer", "magic"],
            "core": ["filesystem", "context7", "puppeteer", "magic"]
        }
        return recommendations.get(framework, ["filesystem", "context7", "puppeteer", "magic"])
    
    def install_global_commands(self, config: Dict[str, Any]):
        """Install commands to user's global directory."""
        global_commands_dir = Path.home() / ".claude" / "commands"
        global_commands_dir.mkdir(parents=True, exist_ok=True)
        
        source_commands_dir = self.repo_root / "templates" / "global" / "commands"
        
        if not source_commands_dir.exists():
            if HAS_QUESTIONARY:
                questionary.print(f"⚠️ Command library not found at {source_commands_dir}", style="fg:#f9e2af")
            return
        
        installed_count = 0
        
        # Copy all command categories to global
        categories = ["planning", "development", "quality", "documentation", "workflow", "utility"]
        
        for category in categories:
            category_source = source_commands_dir / category
            if category_source.exists():
                category_target = global_commands_dir / category
                category_target.mkdir(exist_ok=True)
                
                for command_file in category_source.glob("*.md"):
                    target_file = category_target / command_file.name
                    if not target_file.exists():  # Don't overwrite existing commands
                        shutil.copy2(command_file, target_file)
                        installed_count += 1
        
        if installed_count > 0:
            if HAS_QUESTIONARY:
                questionary.print(f"✅ Installed {installed_count} global commands to ~/.claude/commands/", style="fg:#98c379")
                questionary.print("   Usage: /user:command-name", style="fg:#6c7086")
            elif HAS_RICH:
                console.print(f"[green]✅ Installed {installed_count} global commands[/green]")
                console.print("[dim]   Usage: /user:command-name[/dim]")
            else:
                print(f"✅ Installed {installed_count} global commands to ~/.claude/commands/")
                print("   Usage: /user:command-name")
        else:
            if HAS_QUESTIONARY:
                questionary.print("✅ Global commands are already up to date.", style="fg:#98c379")
            elif HAS_RICH:
                console.print("[green]✅ Global commands are already up to date.[/green]")
            else:
                print("✅ Global commands are already up to date.")
    def install_project_commands(self, config: Dict[str, Any], target_dir: Path, categories: List[str]):
        """Install project-specific commands."""
        project_commands_dir = target_dir / ".claude" / "commands"
        project_commands_dir.mkdir(parents=True, exist_ok=True)
        
        source_commands_dir = self.repo_root / "templates" / "global" / "commands"
        
        if not source_commands_dir.exists():
            return
        
        framework = config.get("framework", "core")
        installed_count = 0
        
        # Framework-specific command selection
        framework_commands = {
            "fastapi": {
                "development": ["create-feature", "fix-bug"],
                "quality": ["check-all", "security-check"],
                "documentation": ["api-docs"],
                "workflow": ["commit-changes", "create-pr"],
                "utility": ["cleanup-code"]
            },
            "django": {
                "development": ["create-feature", "fix-bug"],
                "quality": ["check-all", "security-check"],
                "documentation": ["create-docs"],
                "workflow": ["commit-changes", "create-pr"],
                "utility": ["cleanup-code"]
            },
            "data-science": {
                "planning": ["analyze-requirements"],
                "development": ["create-feature"],
                "quality": ["check-all"],
                "documentation": ["create-docs"],
                "workflow": ["commit-changes"],
                "utility": ["cleanup-code"]
            },
            "cli-tool": {
                "development": ["create-feature", "fix-bug"],
                "quality": ["check-all"],
                "workflow": ["commit-changes"],
                "utility": ["cleanup-code"]
            }
        }
        
        # Universal commands available for all frameworks
        universal_commands = {
            "planning": ["analyze-requirements"],
            "development": ["create-feature", "fix-bug"],
            "quality": ["check-all", "code-review"],
            "documentation": ["create-docs", "update-readme"],
            "workflow": ["commit-changes", "create-pr"],
            "utility": ["cleanup-code", "update-deps"]
        }
        
        # Get framework-specific commands or fall back to universal
        commands_to_install = framework_commands.get(framework, universal_commands)
        
        for category in categories:
            if category in commands_to_install:
                category_source = source_commands_dir / category
                if category_source.exists():
                    for command_name in commands_to_install[category]:
                        command_file = category_source / f"{command_name}.md"
                        if command_file.exists():
                            target_file = project_commands_dir / f"{command_name}.md"
                            if not target_file.exists():
                                shutil.copy2(command_file, target_file)
                                installed_count += 1
        
        if installed_count > 0:
            if HAS_QUESTIONARY:
                questionary.print(f"✅ Installed {installed_count} project commands to .claude/commands/", style="fg:#98c379")
                questionary.print("   Usage: /project:command-name", style="fg:#6c7086")
            elif HAS_RICH:
                console.print(f"[green]✅ Installed {installed_count} project commands[/green]")
                console.print("[dim]   Usage: /project:command-name[/dim]")
            else:
                print(f"✅ Installed {installed_count} project commands to .claude/commands/")
                print("   Usage: /project:command-name")
    def list_available_commands(self, target_dir: Path):
        """List all available commands for the user."""
        commands_found = []
        
        # Check global commands
        global_commands_dir = Path.home() / ".claude" / "commands"
        if global_commands_dir.exists():
            for category_dir in global_commands_dir.iterdir():
                if category_dir.is_dir():
                    for command_file in category_dir.glob("*.md"):
                        commands_found.append(f"/user:{command_file.stem}")
        
        # Check project commands
        project_commands_dir = target_dir / ".claude" / "commands"
        if project_commands_dir.exists():
            for command_file in project_commands_dir.glob("*.md"):
                commands_found.append(f"/project:{command_file.stem}")
        
        if commands_found and HAS_QUESTIONARY:
            questionary.print(f"\n🎯 Available Commands ({len(commands_found)} total):", style="bold")
            
            # Group commands by type
            user_commands = [cmd for cmd in commands_found if cmd.startswith("/user:")]
            project_commands = [cmd for cmd in commands_found if cmd.startswith("/project:")]
            
            if user_commands:
                questionary.print("   Global Commands:", style="fg:#61afef")
                for cmd in sorted(user_commands):
                    questionary.print(f"     {cmd}", style="fg:#6c7086")
            
            if project_commands:
                questionary.print("   Project Commands:", style="fg:#98c379")
                for cmd in sorted(project_commands):
                    questionary.print(f"     {cmd}", style="fg:#6c7086")
                    
            questionary.print("\n💡 Use these commands in Claude Code to automate your workflow!", style="fg:#f9e2af")
        
        elif commands_found:
            print(f"\n🎯 Available Commands ({len(commands_found)} total):")
            for cmd in sorted(commands_found):
                print(f"   {cmd}")
            print("\n💡 Use these commands in Claude Code to automate your workflow!")
    
    def validate_mcp_servers(self, selected_servers: List[str]):
        """Check MCP server availability and provide guidance."""
        if not selected_servers:
            return
        
        if HAS_QUESTIONARY:
            questionary.print("🔍 Checking MCP server availability...", style="fg:#6c7086")
        elif HAS_RICH:
            console.print("🔍 Checking MCP server availability...", style="dim")
        else:
            print("🔍 Checking MCP server availability...")
        
        missing_servers = []
        for server in selected_servers:
            if not self._is_mcp_server_available(server):
                missing_servers.append(server)
        
        if missing_servers:
            if HAS_QUESTIONARY:
                questionary.print(f"⚠️ Missing MCP servers: {', '.join(missing_servers)}", style="fg:#f9e2af")
                
                install_missing = questionary.confirm(
                    "Automatically install missing MCP servers?",
                    default=True
                ).ask()
                
                if install_missing:
                    self._install_missing_mcp_servers(missing_servers)
                else:
                    self._show_installation_instructions(missing_servers)
            elif HAS_RICH:
                console.print(f"[yellow]⚠️ Missing MCP servers: {', '.join(missing_servers)}[/yellow]")
                install_missing = Confirm.ask("Automatically install missing MCP servers?", default=True)
                if install_missing:
                    self._install_missing_mcp_servers(missing_servers)
                else:
                    self._show_installation_instructions(missing_servers)
            else:
                print(f"⚠️ Missing MCP servers: {', '.join(missing_servers)}")
                install_missing = input("Automatically install missing MCP servers? (Y/n): ").strip().lower() not in ['n', 'no']
                if install_missing:
                    self._install_missing_mcp_servers(missing_servers)
                else:
                    self._show_installation_instructions(missing_servers)
        else:
            if HAS_QUESTIONARY:
                questionary.print("✅ All selected MCP servers are available!", style="fg:#98c379")
            elif HAS_RICH:
                console.print("[green]✅ All selected MCP servers are available![/green]")
            else:
                print("✅ All selected MCP servers are available!")
    def _is_mcp_server_available(self, server: str) -> bool:
        """Check if an MCP server is available on the system."""
        # Common MCP server packages
        server_packages = {
            "postgresql": "@modelcontextprotocol/server-postgres",
            "mysql": "@modelcontextprotocol/server-mysql",
            "sqlite": "@modelcontextprotocol/server-sqlite", 
            "fetch": "@modelcontextprotocol/server-fetch",
            "filesystem": "@modelcontextprotocol/server-filesystem",
            "context7": "@upstash/context7-mcp",
            "puppeteer": "puppeteer-mcp-server",
            "magic": "@magicuidesign/mcp",
            "brave-search": "@modelcontextprotocol/server-brave-search"
        }
        
        package_name = server_packages.get(server)
        if not package_name:
            return True  # Unknown server, assume available
        
        try:
            import subprocess
            result = subprocess.run(
                ['npm', 'list', '-g', package_name], 
                capture_output=True, 
                text=True, 
                timeout=5
            )
            return result.returncode == 0
        except:
            return False  # Can't check, assume not available
    def _show_installation_instructions(self, servers: List[str]):
        """Show installation commands for missing servers."""
        instructions = {
            "postgresql": "npm install -g @modelcontextprotocol/server-postgres",
            "mysql": "npm install -g @modelcontextprotocol/server-mysql",
            "sqlite": "npm install -g @modelcontextprotocol/server-sqlite",
            "fetch": "npm install -g @modelcontextprotocol/server-fetch",
            "filesystem": "npm install -g @modelcontextprotocol/server-filesystem",
            "context7": "npm install -g @upstash/context7-mcp",
            "puppeteer": "npm install -g puppeteer-mcp-server",
            "magic": "npm install -g @magicuidesign/mcp",
            "brave-search": "npm install -g @modelcontextprotocol/server-brave-search"
        }
        
        if HAS_QUESTIONARY:
            questionary.print("\n📦 Installation Commands:", style="bold")
            for server in servers:
                if server in instructions:
                    questionary.print(f"  {server}: {instructions[server]}", style="fg:#98c379")
                else:
                    questionary.print(f"  {server}: Installation method unknown", style="fg:#6c7086")
        elif HAS_RICH:
            console.print("\n[bold]📦 Installation Commands:[/bold]")
            for server in servers:
                if server in instructions:
                    console.print(f"  [green]{server}[/green]: {instructions[server]}")
                else:
                    console.print(f"  [dim]{server}[/dim]: Installation method unknown")
        else:
            print("\n📦 Installation Commands:")
            for server in servers:
                if server in instructions:
                    print(f"  {server}: {instructions[server]}")
                else:
                    print(f"  {server}: Installation method unknown")
    
    def _install_missing_mcp_servers(self, servers: List[str]):
        """Install missing MCP servers using npm."""
        if not servers:
            return

        if HAS_QUESTIONARY:
            questionary.print("\n📦 Installing missing MCP servers...", style="bold")
        elif HAS_RICH:
            console.print("\n[bold]📦 Installing missing MCP servers...[/bold]")
        else:
            print("\n📦 Installing missing MCP servers...")

        server_packages = {
            "postgresql": "@modelcontextprotocol/server-postgres",
            "mysql": "@modelcontextprotocol/server-mysql",
            "sqlite": "@modelcontextprotocol/server-sqlite", 
            "fetch": "@modelcontextprotocol/server-fetch",
            "filesystem": "@modelcontextprotocol/server-filesystem",
            "context7": "@upstash/context7-mcp",
            "puppeteer": "puppeteer-mcp-server",
            "magic": "@magicuidesign/mcp",
            "brave-search": "@modelcontextprotocol/server-brave-search"
        }

        for server in servers:
            package_name = server_packages.get(server)
            if not package_name:
                if HAS_QUESTIONARY:
                    questionary.print(f"  {server}: Unknown package name, skipping.", style="fg:#f9e2af")
                elif HAS_RICH:
                    console.print(f"  [yellow]{server}[/yellow]: Unknown package name, skipping.")
                else:
                    print(f"  {server}: Unknown package name, skipping.")
                continue

            install_command = f"npm install -g {package_name}"
            if HAS_QUESTIONARY:
                questionary.print(f"  Installing {server} ({package_name})...", style="fg:#6c7086")
            elif HAS_RICH:
                console.print(f"  [dim]Installing {server} ({package_name})...[/dim]")
            else:
                print(f"  Installing {server} ({package_name})...")

            try:
                import subprocess
                result = subprocess.run(
                    install_command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    check=True,
                    timeout=300 # 5 minutes timeout for installation
                )
                if HAS_QUESTIONARY:
                    questionary.print(f"  ✅ {server} installed successfully.", style="fg:#98c379")
                elif HAS_RICH:
                    console.print(f"  [green]✅ {server} installed successfully.[/green]")
                else:
                    print(f"  ✅ {server} installed successfully.")
            except subprocess.CalledProcessError as e:
                if HAS_QUESTIONARY:
                    questionary.print(f"  ❌ Failed to install {server}: {e.stderr}", style="fg:#f38ba8")
                elif HAS_RICH:
                    console.print(f"  [red]❌ Failed to install {server}: {e.stderr}[/red]")
                else:
                    print(f"  ❌ Failed to install {server}: {e.stderr}")
            except subprocess.TimeoutExpired:
                if HAS_QUESTIONARY:
                    questionary.print(f"  ❌ Installation of {server} timed out.", style="fg:#f38ba8")
                elif HAS_RICH:
                    console.print(f"  [red]❌ Installation of {server} timed out.[/red]")
                else:
                    print(f"  ❌ Installation of {server} timed out.")
            except Exception as e:
                if HAS_QUESTIONARY:
                    questionary.print(f"  ❌ An unexpected error occurred during {server} installation: {e}", style="fg:#f38ba8")
                elif HAS_RICH:
                    console.print(f"  [red]❌ An unexpected error occurred during {server} installation: {e}[/red]")
                else:
                    print(f"  ❌ An unexpected error occurred during {server} installation: {e}")
    def get_default_projects_dir(self):
        """Get smart default for project creation."""
        home = Path.home()
        
        # Common project directory patterns (order matters - preference)
        common_dirs = [
            home / "Projects",
            home / "Code", 
            home / "Development",
            home / "projects",
            home / "code",
            home / "workspace",
            home / "dev"
        ]
        
        # Use first existing directory
        for dir_path in common_dirs:
            if dir_path.exists() and dir_path.is_dir():
                return dir_path
        
        # If none exist, default to ~/Projects (will be created)
        return home / "Projects"
    
    def handle_project_directory_creation(self):
        """Handle optional project directory creation with smart defaults."""
        
        if HAS_QUESTIONARY:
            create_new = questionary.confirm(
                "Create new project directory?",
                default=False
            ).ask()
            
            if create_new:
                default_parent = self.get_default_projects_dir()
                project_name = questionary.text(
                    "Project directory name:",
                    default="my-claude-project"
                ).ask()
                
                project_dir = default_parent / project_name
                
                if default_parent.exists():
                    questionary.print(f"📁 Will create: {project_dir}", style="fg:#6c7086")
                    questionary.print(f"   (using existing {default_parent.name}/ directory)", style="fg:#6c7086")
                else:
                    questionary.print(f"📁 Will create: {project_dir}", style="fg:#6c7086")
                    questionary.print(f"   (will create {default_parent.name}/ directory)", style="fg:#6c7086")
                
                use_location = questionary.confirm(
                    "Use this location?",
                    default=True
                ).ask()
                
                if not use_location:
                    custom_path = questionary.path(
                        "Choose parent directory:",
                        default=str(Path.home())
                    ).ask()
                    project_dir = Path(custom_path) / project_name
                
                if project_dir.exists():
                    overwrite = questionary.confirm(
                        f"Directory '{project_dir}' already exists. Continue?"
                    ).ask()
                    if not overwrite:
                        return self.handle_project_directory_creation()
                
                # Create parent directory if it doesn't exist
                project_dir.parent.mkdir(parents=True, exist_ok=True)
                
                # Create project directory and change to it
                project_dir.mkdir(parents=True, exist_ok=True)
                os.chdir(project_dir)
                
                # 🔥 FIX: Update self.current_dir to reflect the directory change
                self.current_dir = Path.cwd()
                
                questionary.print(f"✅ Created and moved to: {project_dir}", style="fg:#98c379")
    
    def run_interactive_setup_enhanced(self):
        """Enhanced setup with questionary integration and command library."""
        try:
            self.display_banner()
            
            # NEW: Handle optional project directory creation
            self.handle_project_directory_creation()
            
            # Existing setup steps...
            mode = self.detect_usage_mode()
            framework = self.select_framework()
            config = self.configure_project(framework, mode)
            
            # NEW: Configure command library
            config = self.configure_command_library(config, mode)
            
            # NEW: Configure personas
            config = self.configure_personas(config)
            
            # Validate MCP servers
            #self.validate_mcp_servers(config["mcp_servers"])
            
            # Load and customize templates
            templates = self.load_template_files(framework)
            customized_templates = self.customize_templates(templates, config)
            
            # Get target directory with enhanced support
            if HAS_QUESTIONARY:
                path = questionary.path(
                    "📁 Select target directory:",
                    default=str(self.current_dir),
                    validate=lambda x: Path(x).parent.exists() or "Parent directory must exist"
                ).ask()
                target_dir = Path(path) if path else self.current_dir
                
                if target_dir.name != config["project_name"]:
                    create_subdir = questionary.confirm(
                        f'Create a subdirectory named \'{config["project_name"]}\' in this location?'
                    ).ask()
                    if create_subdir:
                        target_dir = target_dir / config["project_name"]

            elif HAS_RICH:
                use_current = Confirm.ask(
                    f"Create configuration in current directory ({self.current_dir})?",
                    default=True
                )
                if not use_current:
                    custom_path = Prompt.ask("Enter target directory path", default=str(self.current_dir))
                    target_dir = Path(custom_path)
                else:
                    target_dir = self.current_dir
            else:
                use_current = input(f"Create configuration in current directory ({self.current_dir})? (Y/n): ").strip().lower()
                if use_current in ['n', 'no']:
                    custom_path = input(f"Enter target directory path (default: {self.current_dir}): ").strip()
                    target_dir = Path(custom_path) if custom_path else self.current_dir
                else:
                    target_dir = self.current_dir
            
            # Create target directory if needed
            target_dir.mkdir(parents=True, exist_ok=True)
            
            # Write configuration files
            self.write_files(customized_templates, target_dir, config)
            
            # NEW: Install command library
            self.install_command_library(config, target_dir)
            
            # NEW: Install personas
            self.install_personas(config, target_dir)
            
            # NEW: List available commands
            self.list_available_commands(target_dir)
            
            # Display next steps
            self.display_next_steps(config, target_dir)
            
        except KeyboardInterrupt:
            if HAS_QUESTIONARY:
                questionary.print("\n❌ Setup cancelled by user", style="fg:#f38ba8")
            elif HAS_RICH:
                console.print("\n[yellow]Setup cancelled by user[/yellow]")
            else:
                print("\nSetup cancelled by user")
            sys.exit(1)
        except Exception as e:
            if HAS_QUESTIONARY:
                questionary.print(f"\n💥 Error: {e}", style="bold fg:#f38ba8")
            elif HAS_RICH:
                console.print(f"\n[red]Error: {e}[/red]")
            else:
                print(f"\nError: {e}")
            sys.exit(1)

    def display_banner(self):
        """Display welcome banner."""
        if HAS_RICH:
            banner = Panel.fit(
                "[bold blue]🚀 Claude Code Configuration Setup Tool[/bold blue]\n\n"
                "[dim]Interactive tool for setting up framework-specific Claude Code configurations[/dim]",
                border_style="blue"
            )
            console.print(banner)
        else:
            print("=" * 60)
            print("🚀 Claude Code Configuration Setup Tool")
            print("Interactive tool for setting up framework-specific Claude Code configurations")
            print("=" * 60)

    def display_frameworks(self):
        """Display available frameworks in a table."""
        if HAS_RICH:
            table = Table(title="Available Frameworks", show_header=True)
            table.add_column("Framework", style="cyan", no_wrap=True)
            table.add_column("Description", style="white")
            table.add_column("Main Use Cases", style="green")
            
            for key, framework in self.frameworks.items():
                use_cases = ", ".join(framework["use_cases"][:2])
                if len(framework["use_cases"]) > 2:
                    use_cases += "..."
                
                table.add_row(
                    f"[bold]{framework['name']}[/bold]",
                    framework["description"],
                    use_cases
                )
            
            console.print(table)
        else:
            print("\nAvailable Frameworks:")
            print("-" * 40)
            for key, framework in self.frameworks.items():
                print(f"• {framework['name']}: {framework['description']}")

    def select_framework(self) -> str:
        """Interactive framework selection."""
        self.display_frameworks()
        
        if HAS_RICH:
            framework_choices = list(self.frameworks.keys())
            choice = Prompt.ask(
                "\n[bold]Select a framework[/bold]",
                choices=framework_choices,
                default="core"
            )
        else:
            print(f"\nAvailable options: {', '.join(self.frameworks.keys())}")
            while True:
                choice = input("Select a framework (default: core): ").strip().lower()
                if not choice:
                    choice = "core"
                if choice in self.frameworks:
                    break
                print(f"Invalid choice. Please select from: {', '.join(self.frameworks.keys())}")
        
        return choice

    def detect_usage_mode(self) -> str:
        """Detect if this is a solo or team project."""
        if HAS_RICH:
            console.print("\n[bold blue]🤔 How will you be using this project?[/bold blue]")
            
            mode = Prompt.ask(
                "\n[bold]Select usage mode[/bold]",
                choices=["solo", "team", "unsure"],
                default="solo"
            )
        else:
            print("\n🤔 How will you be using this project?")
            print("1. Personal project (just for me)")
            print("2. Team project (shared with others)")
            print("3. Not sure / Let me choose later")
            
            while True:
                choice = input("Select option (1/2/3) [1]: ").strip()
                if not choice or choice == "1":
                    mode = "solo"
                    break
                elif choice == "2":
                    mode = "team"
                    break
                elif choice == "3":
                    mode = "unsure"
                    break
                else:
                    print("Invalid choice. Please enter 1, 2, or 3.")
        
        if mode == "unsure":
            if HAS_RICH:
                console.print("\n[dim]💡 Tip: You can always upgrade a personal project to team mode later[/dim]")
                use_solo = Confirm.ask("Start with personal project setup?", default=True)
            else:
                print("\n💡 Tip: You can always upgrade a personal project to team mode later")
                use_solo = input("Start with personal project setup? (Y/n): ").strip().lower()
                use_solo = use_solo not in ['n', 'no']
            mode = "solo" if use_solo else "team"
        
        return mode

    def check_global_settings(self) -> bool:
        """Check if global Claude Code settings exist."""
        global_settings_path = Path.home() / ".claude" / "settings.json"
        return global_settings_path.exists()

    def setup_global_settings(self) -> Dict[str, Any]:
        """Setup global Claude Code settings for team mode."""
        if HAS_RICH:
            console.print("\n[bold blue]🔍 Checking your global Claude Code settings...[/bold blue]")
        else:
            print("\n🔍 Checking your global Claude Code settings...")
        
        if self.check_global_settings():
            if HAS_RICH:
                console.print("[green]✅ Global settings found at ~/.claude/settings.json[/green]")
                update_global = Confirm.ask("Update global settings?", default=False)
            else:
                print("✅ Global settings found at ~/.claude/settings.json")
                update_global = input("Update global settings? (y/N): ").strip().lower() in ['y', 'yes']
            
            if not update_global:
                return {}
        else:
            if HAS_RICH:
                console.print("[yellow]❌ No global settings found at ~/.claude/settings.json[/yellow]")
                console.print("[dim]ℹ️  Global settings apply to ALL your Claude Code projects[/dim]")
                setup_global = Confirm.ask("Set up global settings for your development environment?", default=True)
            else:
                print("❌ No global settings found at ~/.claude/settings.json")
                print("ℹ️  Global settings apply to ALL your Claude Code projects")
                setup_global = input("Set up global settings for your development environment? (Y/n): ").strip().lower()
                setup_global = setup_global not in ['n', 'no']
            
            if not setup_global:
                return {}
        
        # Collect global settings
        global_config = {}
        
        if HAS_RICH:
            console.print("\n[bold green]=== Global Configuration Setup ===[/bold green]")
            console.print("[dim]These settings will apply to ALL your projects:[/dim]")
            
            # Organization/Company
            organization = Prompt.ask("Organization/Company name (optional)", default="")
            if organization:
                global_config["organization"] = organization
            
            # Common MCP servers
            console.print("\n[bold]Common MCP servers for all projects:[/bold]")
            console.print("✅ git (version control)")
            console.print("✅ time (timestamps and scheduling)")
            console.print("✅ filesystem (file operations)")
            
            add_auth = Confirm.ask("Add company authentication server?", default=False)
            if add_auth:
                auth_url = Prompt.ask("Company auth URL", default="https://auth.company.com")
                global_config["auth_url"] = auth_url
            
        else:
            print("\n=== Global Configuration Setup ===")
            print("These settings will apply to ALL your projects:")
            
            organization = input("Organization/Company name (optional): ").strip()
            if organization:
                global_config["organization"] = organization
            
            print("\nCommon MCP servers for all projects:")
            print("✅ git (version control)")
            print("✅ time (timestamps and scheduling)")
            print("✅ filesystem (file operations)")
            
            add_auth = input("Add company authentication server? (y/N): ").strip().lower() in ['y', 'yes']
            if add_auth:
                auth_url = input("Company auth URL [https://auth.company.com]: ").strip()
                global_config["auth_url"] = auth_url or "https://auth.company.com"
        
        # Create global settings
        self.create_global_settings(global_config)
        
        if HAS_RICH:
            console.print("\n[green]✅ Created ~/.claude/settings.json with your global preferences[/green]")
        else:
            print("\n✅ Created ~/.claude/settings.json with your global preferences")
        
        return global_config

    def create_global_settings(self, config: Dict[str, Any]):
        """Create global Claude Code settings file."""
        global_settings_dir = Path.home() / ".claude"
        global_settings_dir.mkdir(exist_ok=True)
        
        global_settings = {
            "permissions": {
                "allow": [
                    "Bash(git*)",
                    "Bash(python*)",
                    "Bash(pip*)",
                    "Edit(*.py)",
                    "Edit(*.md)",
                    "Edit(*.json)",
                    "Edit(*.yaml)",
                    "Edit(*.yml)",
                    "Read(**/*.py)",
                    "Read(**/*.md)"
                ],
                "deny": [
                    "Bash(rm -rf*)",
                    "Bash(sudo*)",
                    "Edit(.env)",
                    "Edit(**/secrets/**)"
                ]
            },
            "env": {
                "PYTHONDONTWRITEBYTECODE": "1",
                "PYTHONUNBUFFERED": "1"
            }
        }
        
        if config.get("organization"):
            global_settings["env"]["ORGANIZATION"] = config["organization"]
        
        if config.get("auth_url"):
            global_settings["env"]["COMPANY_AUTH_URL"] = config["auth_url"]
        
        global_settings_path = global_settings_dir / "settings.json"
        global_settings_path.write_text(json.dumps(global_settings, indent=2))

    def configure_project(self, framework: str, mode: str) -> Dict[str, Any]:
        """Configure project-specific settings based on mode."""
        config = {
            "framework": framework,
            "mode": mode,
            "project_name": "",
            "database": "postgresql",
            "environment": "development",
            "mcp_servers": [],
            "custom_settings": {},
            "create_local_template": False
        }
        
        if mode == "team":
            if HAS_RICH:
                console.print(f"\n[bold green]🏢 Configuring {self.frameworks[framework]['name']} Team Project[/bold green]")
            else:
                print(f"\n🏢 Configuring {self.frameworks[framework]['name']} Team Project")
        else:
            if HAS_RICH:
                console.print(f"\n[bold green]⚙️ Configuring {self.frameworks[framework]['name']} Project[/bold green]")
            else:
                print(f"\n⚙️ Configuring {self.frameworks[framework]['name']} Project")
        
        # Project name - ADD QUESTIONARY TIER
        if HAS_QUESTIONARY:
            suggestions = self._get_project_name_suggestions()
            config["project_name"] = questionary.autocomplete(
                "📝 Project name:",
                choices=suggestions,
                default=suggestions[0] if suggestions else f"my-{framework}-project",
                validate=lambda x: len(x.strip()) > 0 or "Project name cannot be empty"
            ).ask() or f"my-{framework}-project"
        elif HAS_RICH:
            default_name = f"my-{framework}-project" if framework != "core" else "my-python-project"
            config["project_name"] = Prompt.ask("Project name", default=default_name)
        else:
            default_name = f"my-{framework}-project" if framework != "core" else "my-python-project"
            config["project_name"] = input(f"Project name (default: {default_name}): ").strip()
            if not config["project_name"]:
                config["project_name"] = default_name
        
        # Database selection (skip for CLI tools) - ADD QUESTIONARY TIER
        if framework not in ["cli-tool"]:
            default_db = "sqlite" if mode == "solo" else "postgresql"
            if HAS_QUESTIONARY:
                db_choices = list(self.databases.keys())
                config["database"] = questionary.select(
                    "🗄️ Database type:",
                    choices=db_choices,
                    default=default_db
                ).ask() or default_db
            elif HAS_RICH:
                db_choices = list(self.databases.keys())
                config["database"] = Prompt.ask("Database type", choices=db_choices, default=default_db)
            else:
                print(f"\nDatabase options: {', '.join(self.databases.keys())}")
                db_choice = input(f"Database type (default: {default_db}): ").strip().lower()
                config["database"] = db_choice if db_choice in self.databases else default_db
        
        # Environment - ADD QUESTIONARY TIER
        if HAS_QUESTIONARY:
            env_choices = list(self.environments.keys())
            config["environment"] = questionary.select(
                "🌍 Environment:",
                choices=env_choices,
                default="development"
            ).ask() or "development"
        elif HAS_RICH:
            env_choices = list(self.environments.keys())
            config["environment"] = Prompt.ask("Environment", choices=env_choices, default="development")
        else:
            print(f"\nEnvironment options: {', '.join(self.environments.keys())}")
            env_choice = input("Environment (default: development): ").strip().lower()
            config["environment"] = env_choice if env_choice in self.environments else "development"
        
        # MCP servers
        self.configure_mcp_servers(config, framework, mode)
        self.validate_mcp_servers(config["mcp_servers"])
        
        # Team-specific options - ADD QUESTIONARY TIER
        if mode == "team":
            if HAS_QUESTIONARY:
                config["create_local_template"] = questionary.confirm(
                    "Create personal overrides template?",
                    default=True
                ).ask()
            elif HAS_RICH:
                config["create_local_template"] = Confirm.ask("Create personal overrides template?", default=True)
            else:
                create_template = input("Create personal overrides template? (Y/n): ").strip().lower()
                config["create_local_template"] = create_template not in ['n', 'no']
        
        return config

    def configure_mcp_servers(self, config: Dict[str, Any], framework: str, mode: str):
        """Configure MCP servers based on framework and mode."""
        default_servers = {
            "core": ["filesystem", "context7", "puppeteer", "magic"],
            "fastapi": ["postgresql", "fetch", "context7", "puppeteer", "magic"],
            "django": ["postgresql", "fetch", "context7", "puppeteer", "magic"],
            "flask": ["postgresql", "fetch", "context7", "puppeteer", "magic"],
            "data-science": ["postgresql", "context7", "puppeteer", "magic"],
            "cli-tool": ["filesystem", "context7", "puppeteer", "magic"],
            "web-scraping": ["fetch", "postgresql", "filesystem", "context7", "puppeteer", "magic"]
        }
        
        available_servers = [
            "postgresql", "mysql", "sqlite", "fetch", "filesystem", 
            "context7", "puppeteer", "magic", "brave-search"
        ]
        
        recommended = default_servers.get(framework, [])
        
        if mode == "solo":
            # Simplified MCP server selection for solo developers
            if HAS_QUESTIONARY:
                # Show recommended servers first
                print(f"\n🔧 MCP servers for {framework} development:")
                for server in recommended:
                    print(f"✅ {server}")
                
                add_more = questionary.confirm(
                    "Add more servers?", 
                    default=False
                ).ask()
                
                if add_more:
                    # Use checkbox for multi-select
                    choices = []
                    for server in available_servers:
                        choices.append(questionary.Choice(
                            title=server,
                            value=server,
                            checked=(server in recommended)
                        ))
                    
                    selected = questionary.checkbox(
                        "Select MCP servers:",
                        choices=choices
                    ).ask()
                    config["mcp_servers"] = selected if selected else recommended
                else:
                    config["mcp_servers"] = recommended
                    
            elif HAS_RICH:
                console.print(f"\n[bold]MCP servers for {framework} development:[/bold]")
                for server in recommended:
                    console.print(f"✅ {server}")
                
                add_more = Confirm.ask("Add more servers?", default=False)
                if add_more:
                    console.print(f"Available servers: {', '.join(available_servers)}")
                    servers_input = Prompt.ask("Enter additional servers (comma-separated)", default="")
                    additional = [s.strip() for s in servers_input.split(",") if s.strip()]
                    config["mcp_servers"] = recommended + additional
                else:
                    config["mcp_servers"] = recommended
            else:
                print(f"\nMCP servers for {framework} development:")
                for server in recommended:
                    print(f"✅ {server}")
                
                add_more = input("Add more servers? (y/N): ").strip().lower() in ['y', 'yes']
                if add_more:
                    print(f"Available servers: {', '.join(available_servers)}")
                    servers_input = input("Enter additional servers (comma-separated): ").strip()
                    if servers_input:
                        additional = [s.strip() for s in servers_input.split(",")]
                        config["mcp_servers"] = recommended + additional
                    else:
                        config["mcp_servers"] = recommended
                else:
                    config["mcp_servers"] = recommended
        
        else:  # team mode
            # Full MCP server configuration for teams
            if HAS_QUESTIONARY:
                print(f"\n🏢 Team MCP servers for {framework} projects:")
                print(f"Recommended: {', '.join(recommended)}")
                for server in recommended:
                    print(f"✅ {server}")
                
                # Team-specific servers
                add_company_servers = questionary.confirm(
                    "Add company-specific servers?", 
                    default=False
                ).ask()
                
                company_servers = []
                if add_company_servers:
                    print("✅ company-security-scanner (security validation)")
                    company_servers.append("company-security-scanner")
                
                use_recommended = questionary.confirm(
                    "Use recommended team settings?", 
                    default=True
                ).ask()
                
                if use_recommended:
                    config["mcp_servers"] = recommended + company_servers
                else:
                    # Use checkbox for custom selection
                    all_servers = available_servers + company_servers
                    choices = []
                    for server in all_servers:
                        choices.append(questionary.Choice(
                            title=server,
                            value=server,
                            checked=(server in recommended + company_servers)
                        ))
                    
                    selected = questionary.checkbox(
                        "Select MCP servers for team:",
                        choices=choices
                    ).ask()
                    config["mcp_servers"] = selected if selected else recommended
                    
            elif HAS_RICH:
                console.print(f"\n[bold]Team MCP servers for {framework} projects:[/bold]")
                console.print(f"[dim]Recommended: {', '.join(recommended)}[/dim]")
                for server in recommended:
                    console.print(f"✅ {server}")
                
                # Team-specific servers
                add_company_servers = Confirm.ask("Add company-specific servers?", default=False)
                company_servers = []
                if add_company_servers:
                    console.print("✅ company-security-scanner (security validation)")
                    company_servers.append("company-security-scanner")
                
                use_recommended = Confirm.ask("Use recommended team settings?", default=True)
                if use_recommended:
                    config["mcp_servers"] = recommended + company_servers
                else:
                    console.print(f"Available servers: {', '.join(available_servers)}")
                    servers_input = Prompt.ask("Enter MCP servers (comma-separated)", default=', '.join(recommended))
                    config["mcp_servers"] = [s.strip() for s in servers_input.split(",")]
            else:
                print(f"\nTeam MCP servers for {framework} projects:")
                print(f"Recommended: {', '.join(recommended)}")
                for server in recommended:
                    print(f"✅ {server}")
                
                add_company_servers = input("Add company-specific servers? (y/N): ").strip().lower() in ['y', 'yes']
                company_servers = []
                if add_company_servers:
                    print("✅ company-security-scanner (security validation)")
                    company_servers.append("company-security-scanner")
                
                use_recommended = input("Use recommended team settings? (Y/n): ").strip().lower()
                if use_recommended not in ['n', 'no']:
                    config["mcp_servers"] = recommended + company_servers
                else:
                    print(f"Available servers: {', '.join(available_servers)}")
                    servers_input = input(f"Enter servers (comma-separated, default: {', '.join(recommended)}): ").strip()
                    if servers_input:
                        config["mcp_servers"] = [s.strip() for s in servers_input.split(",")]
                    else:
                        config["mcp_servers"] = recommended

    def load_template_files(self, framework: str) -> Dict[str, str]:
        """Load template files for the specified framework."""
        framework_dir = self.templates_dir / framework
        
        if not framework_dir.exists():
            raise FileNotFoundError(f"Framework template not found: {framework}")
        
        templates = {}
        
        # Load template files
        template_files = ["CLAUDE.md", "settings.json", ".mcp.json"]
        for file_name in template_files:
            file_path = framework_dir / file_name
            if file_path.exists():
                templates[file_name] = file_path.read_text(encoding='utf-8')
            else:
                console.print(f"[yellow]Warning: Template file not found: {file_name}[/yellow]")
        
        return templates

    def customize_templates(self, templates: Dict[str, str], config: Dict[str, Any]) -> Dict[str, str]:
        """Customize templates based on configuration."""
        customized = {}
        
        for file_name, content in templates.items():
            if file_name == ".mcp.json":
                # Customize MCP configuration
                customized[file_name] = self.customize_mcp_config(content, config)
            elif file_name == "settings.json":
                # Customize settings
                customized[file_name] = self.customize_settings(content, config)
            else:
                # CLAUDE.md - minimal customization for now
                customized[file_name] = content.replace(
                    "# {Framework} Project - Claude Configuration",
                    f"# {config['project_name']} - Claude Configuration"
                )
        
        return customized

    def customize_mcp_config(self, content: str, config: Dict[str, Any]) -> str:
        """Customize MCP configuration based on selected servers."""
        try:
            mcp_config = json.loads(content)
            
            # New MCP server configurations
            new_mcp_servers = {
                "context7": {
                    "command": "npx",
                    "args": ["-y", "@upstash/context7-mcp"]
                },
                "puppeteer": {
                    "command": "npx",
                    "args": ["-y", "puppeteer-mcp-server"],
                    "env": {}
                },
                "magic": {
                    "command": "npx",
                    "args": ["-y", "@magicuidesign/mcp@latest"]
                }
            }
            
            # Filter servers based on selection
            selected_servers = config.get("mcp_servers", [])
            filtered_servers = {}
            
            for server_name in selected_servers:
                if server_name in new_mcp_servers:
                    filtered_servers[server_name] = new_mcp_servers[server_name]
            
            mcp_config["mcpServers"] = filtered_servers
            
            # Update database connection string if applicable
            if config.get("database") and config["database"] != "none":
                db_type = config["database"]
                if db_type in filtered_servers:
                    # Update connection string placeholder
                    if "env" in filtered_servers[db_type]:
                        conn_key = next(
                            (k for k in filtered_servers[db_type]["env"].keys() 
                             if "CONNECTION_STRING" in k), None
                        )
                        if conn_key:
                            # Keep placeholder for user to fill in
                            pass
            
            return json.dumps(mcp_config, indent=2)
        
        except json.JSONDecodeError:
            console.print("[red]Warning: Could not parse MCP configuration[/red]")
            return content

    def customize_settings(self, content: str, config: Dict[str, Any]) -> str:
        """Customize settings.json based on configuration."""
        try:
            settings = json.loads(content)
            
            # Update environment variables based on config
            if "env" in settings:
                if config.get("environment") == "production":
                    settings["env"]["DEBUG"] = "False"
                    if "DJANGO_DEBUG" in settings["env"]:
                        settings["env"]["DJANGO_DEBUG"] = "False"
                elif config.get("environment") == "development":
                    settings["env"]["DEBUG"] = "True"
                    if "DJANGO_DEBUG" in settings["env"]:
                        settings["env"]["DJANGO_DEBUG"] = "True"
            
            return json.dumps(settings, indent=2)
        
        except json.JSONDecodeError:
            console.print("[red]Warning: Could not parse settings configuration[/red]")
            return content

    def write_files(self, templates: Dict[str, str], target_dir: Path, config: Dict[str, Any]):
        """Write template files to target directory based on mode."""
        mode = config.get("mode", "solo")
        
        if HAS_RICH:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                total_files = len(templates)
                if mode == "team" and config.get("create_local_template"):
                    total_files += 1  # For local settings template
                if mode == "team":
                    total_files += 1  # For .gitignore update
                
                task = progress.add_task("Writing configuration files...", total=total_files)
                
                for file_name, content in templates.items():
                    file_path = target_dir / file_name
                    
                    # Create .claude directory for settings.json
                    if file_name == "settings.json":
                        claude_dir = target_dir / ".claude"
                        claude_dir.mkdir(exist_ok=True)
                        file_path = claude_dir / file_name
                    
                    file_path.write_text(content, encoding='utf-8')
                    progress.update(task, advance=1)
                    
                    if HAS_RICH:
                        console.print(f"[green]✅[/green] Created {file_path.relative_to(target_dir)}")
                
                # Team mode: Create additional files
                if mode == "team":
                    # Create local settings template
                    if config.get("create_local_template"):
                        self.create_local_settings_template(target_dir, config)
                        progress.update(task, advance=1)
                        console.print(f"[green]✅[/green] Created .claude/settings.local.json.example")
                    
                    # Update .gitignore
                    self.update_gitignore(target_dir)
                    progress.update(task, advance=1)
                    console.print(f"[green]✅[/green] Updated .gitignore")
        else:
            print("Writing configuration files...")
            for file_name, content in templates.items():
                file_path = target_dir / file_name
                
                # Create .claude directory for settings.json
                if file_name == "settings.json":
                    claude_dir = target_dir / ".claude"
                    claude_dir.mkdir(exist_ok=True)
                    file_path = claude_dir / file_name
                
                file_path.write_text(content, encoding='utf-8')
                print(f"✅ Created {file_path.relative_to(target_dir)}")
            
            # Team mode: Create additional files
            if mode == "team":
                if config.get("create_local_template"):
                    self.create_local_settings_template(target_dir, config)
                    print("✅ Created .claude/settings.local.json.example")
                
                self.update_gitignore(target_dir)
                print("✅ Updated .gitignore")

    def create_local_settings_template(self, target_dir: Path, config: Dict[str, Any]):
        """Create a template for personal local settings."""
        claude_dir = target_dir / ".claude"
        claude_dir.mkdir(exist_ok=True)
        
        local_template = {
            "permissions": {
                "allow": [
                    "Bash(custom-personal-commands*)"
                ],
                "deny": [
                ]
            },
            "env": {
                "DEBUG_MODE": "true",
                "PERSONAL_API_KEY": "your-api-key-here",
                "LOCAL_DATA_PATH": "/path/to/your/local/data"
            }
        }
        
        # Framework-specific personal settings
        framework = config.get("framework", "core")
        if framework == "fastapi":
            local_template["env"]["API_PORT"] = "8001"
            local_template["env"]["DATABASE_URL"] = "postgresql://localhost/personal_dev"
        elif framework == "django":
            local_template["env"]["DJANGO_DEBUG"] = "True"
            local_template["env"]["DJANGO_SECRET_KEY"] = "your-local-secret-key"
        elif framework == "data-science":
            local_template["env"]["JUPYTER_PORT"] = "8889"
            local_template["env"]["DATA_DIR"] = "/path/to/your/datasets"
        
        # Add header comment
        header_comment = """// Personal overrides for this project - NOT committed to Git
// Copy this file to settings.local.json and customize for your needs
// Add personal API keys, local paths, and individual preferences here

"""
        
        local_template_path = claude_dir / "settings.local.json.example"
        content = header_comment + json.dumps(local_template, indent=2)
        local_template_path.write_text(content)

    def update_gitignore(self, target_dir: Path):
        """Update .gitignore to exclude local settings."""
        gitignore_path = target_dir / ".gitignore"
        
        gitignore_additions = [
            "",
            "# Claude Code local settings (personal, not committed)",
            ".claude/settings.local.json",
            "",
            "# Environment variables with secrets",
            ".env",
            ".env.local",
            ".env.*.local"
        ]
        
        if gitignore_path.exists():
            content = gitignore_path.read_text()
            if ".claude/settings.local.json" not in content:
                content += "\n" + "\n".join(gitignore_additions)
                gitignore_path.write_text(content)
        else:
            # Create new .gitignore
            base_gitignore = [
                "# Byte-compiled / optimized / DLL files",
                "__pycache__/",
                "*.py[cod]",
                "*$py.class",
                "",
                "# Virtual environments",
                "venv/",
                ".venv/",
                "env/",
                ".env/",
                "",
                "# IDE",
                ".vscode/",
                ".idea/",
                "*.swp",
                "*.swo",
                "",
                "# OS",
                ".DS_Store",
                "Thumbs.db"
            ] + gitignore_additions
            
            gitignore_path.write_text("\n".join(base_gitignore))

    def display_next_steps(self, config: Dict[str, Any], target_dir: Path):
        """Enhanced next steps with command library information."""
        framework_name = self.frameworks[config["framework"]]["name"]
        mode = config.get("mode", "solo")
        command_config = config.get("command_library", {})
        
        if HAS_QUESTIONARY:
            questionary.print(f"\n🎉 {framework_name} project setup complete!", style="bold fg:#98c379")
            
            # File summary
            questionary.print("\n📁 Generated Files:", style="bold")
            questionary.print("  • CLAUDE.md - Project-specific Claude instructions", style="fg:#6c7086")
            questionary.print("  • .claude/settings.json - Permissions and environment", style="fg:#6c7086") 
            questionary.print("  • .mcp.json - MCP server configuration", style="fg:#6c7086")
            
            if command_config.get("install_project"):
                questionary.print("  • .claude/commands/ - Project command library", style="fg:#6c7086")
            
            if config.get("personas", {}).get("install_personas"):
                questionary.print("  • .claude/personas/ - Persona library", style="fg:#6c7086")
            
            # Command library summary
            if command_config.get("install_global") or command_config.get("install_project"):
                questionary.print("\n🔧 Command Library Installed:", style="bold fg:#61afef")
                
                if command_config.get("install_global"):
                    questionary.print("  • Global commands: ~/.claude/commands/ (use /user:command-name)", style="fg:#98c379")
                
                if command_config.get("install_project"):
                    categories = command_config.get("categories", [])
                    questionary.print(f"  • Project commands: .claude/commands/ (use /project:command-name)", style="fg:#98c379")
                    questionary.print(f"  • Categories: {', '.join(categories)}", style="fg:#6c7086")
            
            # Next steps
            questionary.print("\n🚀 Next Steps:", style="bold")
            questionary.print("  1. Review CLAUDE.md for project-specific guidance", style="fg:#6c7086")
            questionary.print("  2. MCP servers installed (if missing)", style="fg:#6c7086")
            questionary.print("  3. Start Claude Code: claude", style="fg:#6c7086")
            questionary.print("  4. Try a command: /project:create-feature or /user:check-all", style="fg:#6c7086")
            questionary.print("  5. Let Claude follow CLAUDE.md to set up your project!", style="fg:#6c7086")
            
            questionary.print("\n💡 Pro tip: Use /project:analyze-requirements to plan your next feature!", style="fg:#f9e2af")
            
        else:
            # Fallback for Rich/basic display
            print(f"\n🎉 {framework_name} project setup complete!")
            print("\n📁 Generated Files:")
            print("  • CLAUDE.md - Project-specific Claude instructions")
            print("  • .claude/settings.json - Permissions and environment")
            print("  • .mcp.json - MCP server configuration")
            
            if command_config.get("install_project"):
                print("  • .claude/commands/ - Project command library")
            
            print("\n🚀 Next Steps:")
            print("  1. Review CLAUDE.md for project-specific guidance")
            print("  2. Start Claude Code: claude")
            print("  3. Try commands like /project:create-feature")
            print("  4. Let Claude set up your project structure!")

    def display_team_next_steps(self, framework_name: str, target_dir: Path, config: Dict[str, Any]):
        """Display next steps for team developers."""
        if HAS_RICH:
            next_steps = f"""[bold green]🎉 Team Setup Complete![/bold green]

Your {framework_name} project is configured for team collaboration.

[bold]📋 Configuration Summary:[/bold]
• ~/.claude/settings.json → Your global company standards
• .claude/settings.json → Team {framework_name} settings (commit this)
• .claude/settings.local.json.example → Personal overrides template

[bold]🚀 Team Workflow:[/bold]
1. Commit team settings: [dim]git add .claude/settings.json CLAUDE.md .mcp.json[/dim]
2. Copy: [dim]cp .claude/settings.local.json.example .claude/settings.local.json[/dim]
3. Add personal settings to settings.local.json (NOT committed)
4. Team members get: Global + Team + Personal settings

[bold]📁 What Gets Shared vs Personal:[/bold]
┌─────────────────────┬─────────────────────────────────────────────┬──────────────┐
│ File                │ Purpose                                     │ Commit to Git│
├─────────────────────┼─────────────────────────────────────────────┼──────────────┤
│ CLAUDE.md           │ {framework_name} + team standards          │ Yes (shared) │
│ .claude/settings.json│ Team {framework_name} permissions         │ Yes (shared) │
│ .mcp.json           │ Team MCP servers                           │ Yes (shared) │
│ .gitignore          │ Updated to exclude personal settings      │ Yes (shared) │
├─────────────────────┼─────────────────────────────────────────────┼──────────────┤
│ .claude/settings.   │ Personal overrides template               │ No (template)│
│   local.json.example│ • Copy to settings.local.json             │              │
│                     │ • Add personal API keys, paths            │              │
└─────────────────────┴─────────────────────────────────────────────┴──────────────┘

[bold]🔒 Security Note:[/bold]
• .claude/settings.local.json is in .gitignore (never committed)
• Store sensitive data (API keys) in settings.local.json only
• Global company settings are each person's responsibility

[dim]Happy collaborative coding! 🚀[/dim]"""
            
            panel = Panel(next_steps, border_style="green", title="Team Success")
            console.print(panel)
        else:
            print("\n" + "=" * 60)
            print("🎉 Team Setup Complete!")
            print(f"\nYour {framework_name} project is configured for team collaboration.")
            print(f"\nConfiguration Summary:")
            print("• ~/.claude/settings.json → Global company standards")
            print(f"• .claude/settings.json → Team {framework_name} settings (commit)")
            print("• .claude/settings.local.json.example → Personal template")
            print(f"\nTeam Workflow:")
            print("1. Commit team settings to Git")
            print("2. Copy local settings template")
            print("3. Add personal settings (not committed)")
            print("4. Team members get layered configuration")
            print("\nHappy collaborative coding! 🚀")

    def run_interactive_setup(self):
        """Run the interactive setup process with adaptive mode detection."""
        try:
            self.display_banner()
            
            # Detect usage mode (solo vs team)
            mode = self.detect_usage_mode()
            
            # Setup global settings for team mode
            global_config = {}
            if mode == "team":
                global_config = self.setup_global_settings()
            
            # Framework selection
            framework = self.select_framework()
            
            # Project configuration (now includes mode)
            config = self.configure_project(framework, mode)
            config.update(global_config)  # Merge global config
            
            # Load templates
            if HAS_RICH:
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    console=console
                ) as progress:
                    task = progress.add_task("Loading templates...", total=1)
                    templates = self.load_template_files(framework)
                    progress.update(task, advance=1)
            else:
                print("Loading templates...")
                templates = self.load_template_files(framework)
            
            # Customize templates
            customized_templates = self.customize_templates(templates, config)
            
            # Determine target directory
            target_dir = self.current_dir
            if HAS_RICH:
                use_current = Confirm.ask(
                    f"Create configuration in current directory ({target_dir})?",
                    default=True
                )
                if not use_current:
                    custom_path = Prompt.ask("Enter target directory path", default=str(target_dir))
                    target_dir = Path(custom_path)
            else:
                use_current = input(f"Create configuration in current directory ({target_dir})? (Y/n): ").strip().lower()
                if use_current in ['n', 'no']:
                    custom_path = input(f"Enter target directory path (default: {target_dir}): ").strip()
                    if custom_path:
                        target_dir = Path(custom_path)
            
            # Create target directory if it doesn't exist
            target_dir.mkdir(parents=True, exist_ok=True)
            
            # Write files (now mode-aware)
            self.write_files(customized_templates, target_dir, config)
            
            # Display next steps (now mode-aware)
            self.display_next_steps(config, target_dir)
            
        except KeyboardInterrupt:
            if HAS_RICH:
                console.print("\n[yellow]Setup cancelled by user[/yellow]")
            else:
                print("\nSetup cancelled by user")
            sys.exit(1)
        except Exception as e:
            if HAS_RICH:
                console.print(f"[red]Error: {e}[/red]")
            else:
                print(f"Error: {e}")
            sys.exit(1)

    def run_cli_setup(self, args):
        """Run non-interactive setup from command line arguments."""
        try:
            mode = args.mode or "solo"
            
            config = {
                "framework": args.framework,
                "mode": mode,
                "project_name": args.project_name or (f"my-{args.framework}-project" if args.framework != "core" else "my-python-project"),
                "database": args.database or ("sqlite" if mode == "solo" else "postgresql"),
                "environment": args.environment or "development",
                "mcp_servers": args.mcp_servers.split(",") if args.mcp_servers else [],
                "custom_settings": {},
                "create_local_template": args.create_local_template if hasattr(args, 'create_local_template') else False
            }
            
            # Setup global settings for team mode if requested
            if mode == "team" and args.setup_global:
                global_config = self.setup_global_settings()
                config.update(global_config)
            
            # Load and customize templates
            templates = self.load_template_files(config["framework"])
            customized_templates = self.customize_templates(templates, config)
            
            # Write files
            target_dir = Path(args.output_dir) if args.output_dir else self.current_dir
            target_dir.mkdir(parents=True, exist_ok=True)
            self.write_files(customized_templates, target_dir, config)
            
            if HAS_RICH:
                console.print(f"[green]✓ Configuration created in {target_dir}[/green]")
                if mode == "team":
                    console.print("[dim]Note: For team mode, remember to commit shared settings and set up personal overrides[/dim]")
            else:
                print(f"✓ Configuration created in {target_dir}")
                if mode == "team":
                    print("Note: For team mode, remember to commit shared settings and set up personal overrides")
                
        except Exception as e:
            if HAS_RICH:
                console.print(f"[red]Error: {e}[/red]")
            else:
                print(f"Error: {e}")
            sys.exit(1)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Claude Code Configuration Setup Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode (recommended)
  python setup.py
  
  # Solo developer setup
  python setup.py --framework core --project-name my-library --mode solo
  
  # Team setup with global settings
  python setup.py --framework fastapi --mode team --setup-global --create-local-template
  
  # Non-interactive team setup
  python setup.py --framework data-science --mode team --database postgresql --non-interactive
        """
    )
    
    # Mode selection
    parser.add_argument(
        "--mode",
        choices=["solo", "team"],
        help="Usage mode: solo (personal project) or team (shared project)"
    )
    
    # Framework selection
    parser.add_argument(
        "--framework",
        choices=["core", "fastapi", "django", "flask", "data-science", "cli-tool", "web-scraping"],
        help="Framework to set up"
    )
    
    # Project configuration
    parser.add_argument("--project-name", help="Project name")
    parser.add_argument(
        "--database",
        choices=["postgresql", "mysql", "sqlite", "none"],
        help="Database type"
    )
    parser.add_argument(
        "--environment",
        choices=["development", "staging", "production"],
        help="Target environment"
    )
    parser.add_argument(
        "--mcp-servers",
        help="Comma-separated list of MCP servers to include"
    )
    parser.add_argument(
        "--output-dir",
        help="Output directory for configuration files"
    )
    
    # Team mode options
    parser.add_argument(
        "--setup-global",
        action="store_true",
        help="Set up global Claude Code settings (team mode only)"
    )
    parser.add_argument(
        "--create-local-template",
        action="store_true",
        help="Create personal settings template (team mode only)"
    )
    
    # Mode selection
    parser.add_argument(
        "--non-interactive",
        action="store_true",
        help="Run in non-interactive mode (requires --framework)"
    )
    
    args = parser.parse_args()
    
    # Initialize setup tool
    setup_tool = ClaudeSetupTool()
    
    # Check if we have the templates directory
    if not setup_tool.templates_dir.exists():
        if HAS_RICH:
            console.print(f"[red]Error: Templates directory not found at {setup_tool.templates_dir}[/red]")
            console.print("[dim]Make sure you're running this script from the awesome-claude-code repository.[/dim]")
        else:
            print(f"Error: Templates directory not found at {setup_tool.templates_dir}")
            print("Make sure you're running this script from the awesome-claude-code repository.")
        sys.exit(1)
    
    # Run setup
    if args.non_interactive:
        if not args.framework:
            parser.error("--framework is required in non-interactive mode")
        setup_tool.run_cli_setup(args)
    else:
       setup_tool.run_interactive_setup_enhanced()


if __name__ == "__main__":
    main()
