"""Health check dashboard with Rich console interface."""

from pathlib import Path
from typing import List, Dict, Any, Optional
import time
from datetime import datetime

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.text import Text
    from rich.layout import Layout
    from rich.live import Live
    from rich.tree import Tree
    from rich.columns import Columns
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

from .base import BaseValidator, ValidationResult, ValidationLevel
from .claude_validator import ClaudeConfigValidator
from .mcp_validator import MCPServerValidator
from .auto_fixer import AutoFixer


class HealthChecker:
    """Comprehensive health checker with Rich console interface."""
    
    def __init__(self, config_path: Path, console: Optional[Console] = None):
        """Initialize health checker.
        
        Args:
            config_path: Path to configuration directory
            console: Rich console instance (optional)
        """
        self.config_path = config_path
        self.console = console or Console() if RICH_AVAILABLE else None
        self.validators: List[BaseValidator] = []
        self.results: Dict[str, List[ValidationResult]] = {}
        self.auto_fixer = AutoFixer(config_path)
        
        # Initialize validators
        self._setup_validators()
    
    def _setup_validators(self) -> None:
        """Set up all validators."""
        # CLAUDE.md validator
        claude_file = self.config_path / "CLAUDE.md"
        if claude_file.exists():
            self.validators.append(ClaudeConfigValidator(claude_file))
        
        # MCP server validator
        self.validators.append(MCPServerValidator(self.config_path))
    
    def run_health_check(self, verbose: bool = False) -> Dict[str, List[ValidationResult]]:
        """Run comprehensive health check.
        
        Args:
            verbose: Show detailed progress
            
        Returns:
            Dictionary of validation results by validator type
        """
        if not RICH_AVAILABLE:
            return self._run_health_check_simple(verbose)
        
        self.results.clear()
        
        if verbose and self.console:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self.console,
                transient=True,
            ) as progress:
                for validator in self.validators:
                    validator_name = validator.__class__.__name__
                    task = progress.add_task(f"Validating {validator_name}...", total=None)
                    
                    results = validator.validate()
                    self.results[validator_name] = results
                    
                    progress.update(task, completed=True)
        else:
            for validator in self.validators:
                validator_name = validator.__class__.__name__
                results = validator.validate()
                self.results[validator_name] = results
        
        return self.results
    
    def _run_health_check_simple(self, verbose: bool = False) -> Dict[str, List[ValidationResult]]:
        """Run health check without Rich interface."""
        self.results.clear()
        
        for validator in self.validators:
            validator_name = validator.__class__.__name__
            if verbose:
                print(f"Running {validator_name}...")
            
            results = validator.validate()
            self.results[validator_name] = results
        
        return self.results
    
    def display_health_report(self, show_all: bool = False) -> None:
        """Display comprehensive health report.
        
        Args:
            show_all: Show all results including INFO level
        """
        if not RICH_AVAILABLE:
            self._display_simple_report(show_all)
            return
        
        if not self.console:
            return
        
        # Create summary
        summary = self._create_summary()
        self.console.print(summary)
        
        # Display detailed results
        for validator_name, results in self.results.items():
            if not results:
                continue
            
            filtered_results = [r for r in results if show_all or r.level != ValidationLevel.INFO]
            if not filtered_results:
                continue
            
            panel = self._create_validator_panel(validator_name, filtered_results)
            self.console.print(panel)
    
    def _display_simple_report(self, show_all: bool = False) -> None:
        """Display simple text report."""
        total_errors = sum(len([r for r in results if r.is_error]) for results in self.results.values())
        total_warnings = sum(len([r for r in results if r.level == ValidationLevel.WARNING]) for results in self.results.values())
        
        print(f"\n=== Health Check Report ===")
        print(f"Errors: {total_errors}")
        print(f"Warnings: {total_warnings}")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        for validator_name, results in self.results.items():
            filtered_results = [r for r in results if show_all or r.level != ValidationLevel.INFO]
            if not filtered_results:
                continue
            
            print(f"\n--- {validator_name} ---")
            for result in filtered_results:
                level_symbol = "❌" if result.is_error else "⚠️" if result.level == ValidationLevel.WARNING else "ℹ️"
                print(f"{level_symbol} {result.message}")
                if result.suggestion:
                    print(f"   💡 {result.suggestion}")
    
    def _create_summary(self) -> Panel:
        """Create summary panel."""
        total_errors = sum(len([r for r in results if r.is_error]) for results in self.results.values())
        total_warnings = sum(len([r for r in results if r.level == ValidationLevel.WARNING]) for results in self.results.values())
        total_info = sum(len([r for r in results if r.level == ValidationLevel.INFO]) for results in self.results.values())
        
        # Overall status
        if total_errors > 0:
            status = "[red]❌ ERRORS FOUND[/red]"
            status_color = "red"
        elif total_warnings > 0:
            status = "[yellow]⚠️  WARNINGS[/yellow]"
            status_color = "yellow"
        else:
            status = "[green]✅ HEALTHY[/green]"
            status_color = "green"
        
        # Create summary table
        table = Table(show_header=False, box=None, padding=(0, 1))
        table.add_row("Status:", status)
        table.add_row("Errors:", f"[red]{total_errors}[/red]" if total_errors > 0 else "0")
        table.add_row("Warnings:", f"[yellow]{total_warnings}[/yellow]" if total_warnings > 0 else "0")
        table.add_row("Info:", str(total_info))
        table.add_row("Checked:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        return Panel(
            table,
            title="🔍 Configuration Health Check",
            border_style=status_color,
            padding=(1, 2)
        )
    
    def _create_validator_panel(self, validator_name: str, results: List[ValidationResult]) -> Panel:
        """Create panel for validator results."""
        # Group results by level
        errors = [r for r in results if r.is_error]
        warnings = [r for r in results if r.level == ValidationLevel.WARNING]
        info = [r for r in results if r.level == ValidationLevel.INFO]
        
        content = []
        
        # Add errors
        if errors:
            content.append("[red]❌ Errors:[/red]")
            for result in errors:
                content.append(f"  • {result.message}")
                if result.suggestion:
                    content.append(f"    💡 [dim]{result.suggestion}[/dim]")
            content.append("")
        
        # Add warnings
        if warnings:
            content.append("[yellow]⚠️  Warnings:[/yellow]")
            for result in warnings:
                content.append(f"  • {result.message}")
                if result.suggestion:
                    content.append(f"    💡 [dim]{result.suggestion}[/dim]")
            content.append("")
        
        # Add info
        if info:
            content.append("[blue]ℹ️  Information:[/blue]")
            for result in info:
                content.append(f"  • {result.message}")
            content.append("")
        
        panel_color = "red" if errors else "yellow" if warnings else "blue"
        
        return Panel(
            "\n".join(content).rstrip(),
            title=f"📋 {validator_name}",
            border_style=panel_color,
            padding=(1, 2)
        )
    
    def get_health_score(self) -> float:
        """Calculate overall health score (0-100).
        
        Returns:
            Health score percentage
        """
        total_checks = sum(len(results) for results in self.results.values())
        if total_checks == 0:
            return 100.0
        
        errors = sum(len([r for r in results if r.is_error]) for results in self.results.values())
        warnings = sum(len([r for r in results if r.level == ValidationLevel.WARNING]) for results in self.results.values())
        
        # Calculate score (errors weight more than warnings)
        error_penalty = errors * 10
        warning_penalty = warnings * 2
        
        score = max(0, 100 - error_penalty - warning_penalty)
        return min(100.0, score)
    
    def get_fixable_issues(self) -> List[ValidationResult]:
        """Get list of auto-fixable issues.
        
        Returns:
            List of results that can be auto-fixed
        """
        fixable = []
        for results in self.results.values():
            fixable.extend([r for r in results if r.auto_fixable])
        return fixable
    
    def has_critical_issues(self) -> bool:
        """Check if there are critical issues that need attention.
        
        Returns:
            True if critical issues exist
        """
        for results in self.results.values():
            if any(r.level == ValidationLevel.CRITICAL for r in results):
                return True
        return False
    
    def get_recommendations(self) -> List[str]:
        """Get list of recommendations for improving configuration.
        
        Returns:
            List of recommendation strings
        """
        recommendations = []
        
        for results in self.results.values():
            for result in results:
                if result.suggestion and result.suggestion not in recommendations:
                    recommendations.append(result.suggestion)
        
        return recommendations
    
    def save_report(self, output_path: Path, format: str = "json") -> None:
        """Save health report to file.
        
        Args:
            output_path: Path to save report
            format: Report format ('json' or 'text')
        """
        if format == "json":
            self._save_json_report(output_path)
        else:
            self._save_text_report(output_path)
    
    def _save_json_report(self, output_path: Path) -> None:
        """Save report as JSON."""
        import json
        
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "health_score": self.get_health_score(),
            "has_critical_issues": self.has_critical_issues(),
            "summary": {
                "total_errors": sum(len([r for r in results if r.is_error]) for results in self.results.values()),
                "total_warnings": sum(len([r for r in results if r.level == ValidationLevel.WARNING]) for results in self.results.values()),
                "total_info": sum(len([r for r in results if r.level == ValidationLevel.INFO]) for results in self.results.values())
            },
            "validators": {}
        }
        
        for validator_name, results in self.results.items():
            report_data["validators"][validator_name] = [
                {
                    "level": result.level.value,
                    "message": result.message,
                    "file_path": str(result.file_path) if result.file_path else None,
                    "line_number": result.line_number,
                    "suggestion": result.suggestion,
                    "auto_fixable": result.auto_fixable
                }
                for result in results
            ]
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2)
    
    def _save_text_report(self, output_path: Path) -> None:
        """Save report as text."""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("Configuration Health Check Report\n")
            f.write("=" * 40 + "\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Health Score: {self.get_health_score():.1f}%\n\n")
            
            for validator_name, results in self.results.items():
                if not results:
                    continue
                
                f.write(f"{validator_name}\n")
                f.write("-" * len(validator_name) + "\n")
                
                for result in results:
                    level_name = result.level.value.upper()
                    f.write(f"[{level_name}] {result.message}\n")
                    if result.suggestion:
                        f.write(f"  Suggestion: {result.suggestion}\n")
                    f.write("\n")
                
                f.write("\n")
    
    def auto_fix_issues(self, dry_run: bool = False) -> Dict[str, Any]:
        """Automatically fix common configuration issues.
        
        Args:
            dry_run: If True, show what would be fixed without making changes
            
        Returns:
            Dictionary with auto-fix results
        """
        if not self.results:
            self.run_health_check()
        
        all_results = []
        for results in self.results.values():
            all_results.extend(results)
        
        fixable_issues = self.auto_fixer.get_fixable_issues(all_results)
        
        if not fixable_issues:
            return {
                'fixable_issues_found': 0,
                'fixes_applied': 0,
                'dry_run': dry_run,
                'message': 'No auto-fixable issues found'
            }
        
        if dry_run:
            return {
                'fixable_issues_found': len(fixable_issues),
                'fixes_applied': 0,
                'dry_run': True,
                'message': f'Found {len(fixable_issues)} auto-fixable issues',
                'issues': [{'file': str(r.file_path), 'message': r.message} for r in fixable_issues]
            }
        
        # Apply fixes for each file
        fix_results = []
        files_processed = set()
        
        for result in fixable_issues:
            if result.file_path and result.file_path not in files_processed:
                file_results = self.auto_fixer.auto_fix_file(
                    result.file_path, 
                    [r for r in all_results if r.file_path == result.file_path]
                )
                fix_results.extend(file_results)
                files_processed.add(result.file_path)
        
        # Re-run health check to verify fixes
        self.run_health_check()
        
        fix_summary = self.auto_fixer.get_fix_summary()
        
        return {
            'fixable_issues_found': len(fixable_issues),
            'fixes_applied': fix_summary['successful_fixes'],
            'fixes_failed': fix_summary['failed_fixes'],
            'dry_run': False,
            'success_rate': fix_summary['success_rate'],
            'backups_created': fix_summary['backups_created'],
            'message': f"Applied {fix_summary['successful_fixes']} fixes successfully"
        }
    
    def display_auto_fix_report(self, fix_result: Dict[str, Any]) -> None:
        """Display auto-fix results.
        
        Args:
            fix_result: Result from auto_fix_issues()
        """
        if not RICH_AVAILABLE:
            self._display_simple_auto_fix_report(fix_result)
            return
        
        if not self.console:
            return
        
        # Create auto-fix summary panel
        if fix_result['dry_run']:
            title = "🔧 Auto-Fix Preview (Dry Run)"
            color = "blue"
            status_text = f"Found {fix_result['fixable_issues_found']} fixable issues"
        else:
            title = "🔧 Auto-Fix Results"
            if fix_result['fixes_applied'] > 0:
                color = "green"
                status_text = f"Successfully applied {fix_result['fixes_applied']} fixes"
            else:
                color = "yellow"
                status_text = "No fixes were applied"
        
        table = Table(show_header=False, box=None, padding=(0, 1))
        table.add_row("Fixable Issues:", str(fix_result['fixable_issues_found']))
        table.add_row("Fixes Applied:", str(fix_result['fixes_applied']))
        
        if not fix_result['dry_run']:
            table.add_row("Success Rate:", f"{fix_result.get('success_rate', 0):.1f}%")
            if fix_result.get('backups_created', 0) > 0:
                table.add_row("Backups Created:", str(fix_result['backups_created']))
        
        table.add_row("Status:", status_text)
        
        panel = Panel(
            table,
            title=title,
            border_style=color,
            padding=(1, 2)
        )
        
        self.console.print(panel)
    
    def _display_simple_auto_fix_report(self, fix_result: Dict[str, Any]) -> None:
        """Display simple auto-fix report."""
        print(f"\n=== Auto-Fix Report ===")
        print(f"Fixable Issues Found: {fix_result['fixable_issues_found']}")
        print(f"Fixes Applied: {fix_result['fixes_applied']}")
        if not fix_result['dry_run']:
            print(f"Success Rate: {fix_result.get('success_rate', 0):.1f}%")
        print(f"Status: {fix_result['message']}")