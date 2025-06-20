# CLI Tool Project - Claude Configuration

## Project Overview
This is a command-line interface (CLI) tool project designed for building robust, user-friendly command-line applications. The project emphasizes modern CLI best practices including intuitive command structure, comprehensive help systems, and cross-platform compatibility.

**Key Technologies:**
- **Click/Typer**: Modern Python CLI frameworks with automatic help generation
- **Rich**: Beautiful terminal output with colors, tables, and progress bars
- **Colorama**: Cross-platform colored terminal text
- **ConfigArgParse**: Configuration file and environment variable support
- **PyInstaller/cx_Freeze**: Standalone executable creation
- **pytest**: Testing framework for CLI applications
- **setuptools/Poetry**: Package management and distribution

## Architecture & Patterns

### Directory Structure
```
project/
├── src/
│   ├── cli_tool/
│   │   ├── __init__.py
│   │   ├── main.py           # Main CLI entry point
│   │   ├── cli.py            # CLI command definitions
│   │   ├── commands/         # Command modules
│   │   │   ├── __init__.py
│   │   │   ├── init.py       # Initialization commands
│   │   │   ├── process.py    # Processing commands
│   │   │   └── config.py     # Configuration commands
│   │   ├── core/             # Core functionality
│   │   │   ├── __init__.py
│   │   │   ├── config.py     # Configuration handling
│   │   │   ├── logger.py     # Logging setup
│   │   │   ├── exceptions.py # Custom exceptions
│   │   │   └── utils.py      # Utility functions
│   │   ├── models/           # Data models
│   │   │   ├── __init__.py
│   │   │   └── data.py       # Data structures
│   │   └── output/           # Output formatting
│   │       ├── __init__.py
│   │       ├── formatters.py # Output formatters
│   │       └── templates.py  # Output templates
├── tests/
│   ├── __init__.py
│   ├── test_cli.py           # CLI command tests
│   ├── test_commands/        # Command-specific tests
│   ├── test_core/            # Core functionality tests
│   └── fixtures/             # Test data and fixtures
├── docs/                     # Documentation
│   ├── usage.md              # Usage examples
│   ├── installation.md       # Installation guide
│   └── configuration.md      # Configuration options
├── configs/                  # Configuration files
│   ├── default.yaml          # Default configuration
│   └── examples/             # Example configurations
├── scripts/                  # Build and utility scripts
│   ├── build.py              # Build script
│   └── release.py            # Release automation
├── requirements.txt          # Dependencies
├── pyproject.toml           # Modern Python configuration
├── setup.py                 # Legacy setup file
├── README.md                # Project documentation
└── .env.example             # Environment variables template
```

### CLI Design Patterns
- **Command groups**: Organize related commands into logical groups
- **Subcommands**: Hierarchical command structure (tool command subcommand)
- **Options vs Arguments**: Use options for optional parameters, arguments for required input
- **Configuration cascade**: CLI args → Environment vars → Config file → Defaults
- **Progressive disclosure**: Simple commands by default, advanced options available
- **Consistent interface**: Similar patterns across all commands
- **Help system**: Comprehensive help text and examples

## Development Workflow

### Common Commands
```bash
# Development installation
pip install -e .
pip install -e .[dev]
poetry install
poetry install --with dev

# Run CLI tool
python -m cli_tool --help
cli-tool --help                    # If installed
python src/cli_tool/main.py --help # Direct execution

# CLI testing
python -m cli_tool command --dry-run
cli-tool --config configs/test.yaml command
cli-tool --verbose command args

# Testing
pytest
pytest -v                          # Verbose output
pytest --cov=src tests/           # With coverage
pytest tests/test_cli.py          # Specific test file
pytest -k "test_command"          # Run specific tests

# Code quality
black src/ tests/                 # Code formatting
isort src/ tests/                 # Import sorting
flake8 src/ tests/                # Linting
mypy src/                         # Type checking

# Building executables
pyinstaller --onefile src/cli_tool/main.py
python -m PyInstaller --onefile --name cli-tool src/cli_tool/main.py
cx_Freeze setup.py build

# Package building
python setup.py sdist bdist_wheel
poetry build
twine upload dist/*               # Upload to PyPI
```

### Development Process
1. **Design CLI interface** - Define commands, arguments, and options
2. **Implement core logic** - Build the underlying functionality
3. **Create command handlers** - Connect CLI interface to core logic
4. **Add configuration support** - File-based and environment configuration
5. **Implement output formatting** - Rich terminal output and multiple formats
6. **Write comprehensive tests** - Unit tests and integration tests
7. **Add documentation** - Help text, usage examples, and guides
8. **Package for distribution** - Wheels, executables, and installation

### Git Workflow
- **Feature branches**: `feature/add-export-command`
- **Command organization**: Separate commits for each command implementation
- **Documentation**: Update help text and README with new features
- **Testing**: Include tests for all new commands and options
- **Release preparation**: Version bumping and changelog updates

## Code Quality & Standards

### Python Code Style
- **Follow PEP 8** with Black formatting
- **Type hints**: Use for all function parameters and returns
- **Docstrings**: Google style with examples for CLI functions
- **Error handling**: User-friendly error messages and proper exit codes
- **Logging**: Structured logging with configurable verbosity levels

### CLI Design Standards
- **Consistent naming**: Use kebab-case for commands and options
- **Clear help text**: Descriptive help for every command and option
- **Sensible defaults**: Reasonable default values for all options
- **Input validation**: Validate all user input with helpful error messages
- **Output consistency**: Consistent output format across commands
- **Progress feedback**: Show progress for long-running operations
- **Graceful failures**: Handle errors gracefully with useful messages

### Configuration Standards
- **Multiple sources**: Support CLI args, env vars, and config files
- **Validation**: Validate all configuration values
- **Documentation**: Document all configuration options
- **Environment-specific**: Support different configs for different environments
- **Backwards compatibility**: Maintain config compatibility across versions

## Testing Strategy

### Test Types
```python
# Command testing with Click testing
from click.testing import CliRunner
from cli_tool.cli import cli

def test_help_command():
    runner = CliRunner()
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert 'Usage:' in result.output

def test_command_with_args():
    runner = CliRunner()
    result = runner.invoke(cli, ['process', '--input', 'test.txt'])
    assert result.exit_code == 0
    assert 'Processing completed' in result.output

# Integration testing
def test_full_workflow(tmp_path):
    # Test complete command workflow
    input_file = tmp_path / "input.txt"
    input_file.write_text("test data")
    
    runner = CliRunner()
    result = runner.invoke(cli, [
        'process',
        '--input', str(input_file),
        '--output', str(tmp_path / "output.txt")
    ])
    assert result.exit_code == 0

# Configuration testing
def test_config_loading():
    config = load_config('configs/test.yaml')
    assert config.get('verbose') is False
    assert config.get('output_format') == 'json'
```

### CLI Testing Patterns
- **Click TestRunner**: Use Click's built-in testing utilities
- **Temporary directories**: Test file operations in isolated environments
- **Mock external dependencies**: Mock APIs, databases, and file systems
- **Exit code validation**: Ensure proper exit codes for success/failure
- **Output validation**: Test both stdout and stderr output

## Environment Variables

### Configuration Variables
```bash
# Application settings
CLI_TOOL_CONFIG_FILE=~/.config/cli-tool/config.yaml
CLI_TOOL_LOG_LEVEL=INFO
CLI_TOOL_OUTPUT_FORMAT=json
CLI_TOOL_VERBOSE=false
CLI_TOOL_DRY_RUN=false

# Input/Output settings
CLI_TOOL_INPUT_DIR=./input
CLI_TOOL_OUTPUT_DIR=./output
CLI_TOOL_TEMP_DIR=/tmp/cli-tool

# External services
CLI_TOOL_API_URL=https://api.example.com
CLI_TOOL_API_KEY=your-api-key
CLI_TOOL_DATABASE_URL=sqlite:///data.db

# Performance settings
CLI_TOOL_MAX_WORKERS=4
CLI_TOOL_BATCH_SIZE=100
CLI_TOOL_TIMEOUT=30

# Development settings
CLI_TOOL_DEBUG=false
CLI_TOOL_PROFILE=false
```

### Configuration File Support
```yaml
# config.yaml
general:
  verbose: false
  log_level: INFO
  output_format: json

input:
  directory: ./input
  file_pattern: "*.txt"
  recursive: true

output:
  directory: ./output
  filename_template: "{name}_{timestamp}.json"
  overwrite: false

processing:
  max_workers: 4
  batch_size: 100
  timeout: 30
```

## Command Design Patterns

### Click Framework Examples
```python
import click
from rich.console import Console
from rich.progress import track

console = Console()

@click.group()
@click.option('--config', '-c', help='Configuration file path')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
@click.option('--dry-run', is_flag=True, help='Show what would be done')
@click.pass_context
def cli(ctx, config, verbose, dry_run):
    """CLI Tool for data processing and automation."""
    ctx.ensure_object(dict)
    ctx.obj['config'] = load_config(config)
    ctx.obj['verbose'] = verbose
    ctx.obj['dry_run'] = dry_run

@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--output', '-o', help='Output file path')
@click.option('--format', type=click.Choice(['json', 'csv', 'yaml']), default='json')
@click.pass_context
def process(ctx, input_file, output, format):
    """Process input file and generate output."""
    if ctx.obj['dry_run']:
        console.print(f"[yellow]Would process: {input_file}[/yellow]")
        return
    
    # Processing logic with progress bar
    items = load_items(input_file)
    results = []
    
    for item in track(items, description="Processing..."):
        result = process_item(item)
        results.append(result)
    
    save_results(results, output, format)
    console.print(f"[green]✓[/green] Processed {len(items)} items")
```

### Error Handling Patterns
```python
class CLIError(Exception):
    """Base exception for CLI errors."""
    pass

def handle_cli_error(func):
    """Decorator for consistent error handling."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except CLIError as e:
            console.print(f"[red]Error:[/red] {e}", err=True)
            sys.exit(1)
        except KeyboardInterrupt:
            console.print("\n[yellow]Operation cancelled by user[/yellow]", err=True)
            sys.exit(130)
        except Exception as e:
            console.print(f"[red]Unexpected error:[/red] {e}", err=True)
            if ctx.obj.get('verbose'):
                console.print_exception()
            sys.exit(1)
    return wrapper
```

## Output & Formatting

### Rich Terminal Output
```python
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
from rich.panel import Panel

console = Console()

def display_results(data):
    """Display results in a formatted table."""
    table = Table(title="Processing Results")
    table.add_column("ID", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Duration", style="yellow")
    
    for item in data:
        table.add_row(
            str(item.id),
            item.status,
            f"{item.duration:.2f}s"
        )
    
    console.print(table)

def show_progress(items):
    """Show progress for long operations."""
    with Progress() as progress:
        task = progress.add_task("Processing...", total=len(items))
        
        for item in items:
            process_item(item)
            progress.update(task, advance=1)
```

### Multiple Output Formats
```python
def format_output(data, format_type):
    """Format output in specified format."""
    if format_type == 'json':
        return json.dumps(data, indent=2)
    elif format_type == 'yaml':
        return yaml.dump(data, default_flow_style=False)
    elif format_type == 'csv':
        return generate_csv(data)
    elif format_type == 'table':
        return generate_table(data)
    else:
        raise CLIError(f"Unsupported format: {format_type}")
```

## Critical Rules

### CLI Design Requirements
- ⚠️ **ALWAYS** provide comprehensive help text for every command and option
- ⚠️ **ALWAYS** validate user input and provide clear error messages
- ⚠️ **NEVER** fail silently - always provide feedback to the user
- ⚠️ **ALWAYS** use proper exit codes (0 for success, non-zero for errors)
- ⚠️ **ALWAYS** support --help and --version options
- ⚠️ **NEVER** require users to remember complex command syntax

### Error Handling Requirements
- ⚠️ **ALWAYS** catch and handle exceptions gracefully
- ⚠️ **ALWAYS** provide actionable error messages
- ⚠️ **NEVER** show raw Python tracebacks to end users
- ⚠️ **ALWAYS** log detailed errors for debugging (when verbose enabled)
- ⚠️ **ALWAYS** handle Ctrl+C (KeyboardInterrupt) gracefully
- ⚠️ **NEVER** leave temporary files or resources uncleaned

### Configuration Requirements
- ⚠️ **ALWAYS** support multiple configuration sources (CLI, env, file)
- ⚠️ **ALWAYS** validate configuration values
- ⚠️ **NEVER** hardcode paths or environment-specific values
- ⚠️ **ALWAYS** provide sensible defaults for all options
- ⚠️ **NEVER** store secrets in configuration files without encryption
- ⚠️ **ALWAYS** document all configuration options

### Cross-Platform Requirements
- ⚠️ **ALWAYS** use pathlib for file path operations
- ⚠️ **ALWAYS** test on multiple operating systems
- ⚠️ **NEVER** assume specific shell or terminal capabilities
- ⚠️ **ALWAYS** handle different line ending conventions
- ⚠️ **NEVER** use platform-specific shell commands without alternatives

## Common Commands Reference

### Daily Development
```bash
# Install in development mode
pip install -e .[dev]

# Run CLI tool locally
python -m cli_tool --help
python -m cli_tool command --verbose

# Test specific functionality
python -m cli_tool command --dry-run
python -m cli_tool --config configs/test.yaml command

# Run tests
pytest -v --cov=src tests/

# Code quality checks
black src/ tests/ && isort src/ tests/ && flake8 src/ tests/
```

### Build and Distribution
```bash
# Build wheel package
python setup.py sdist bdist_wheel
poetry build

# Build standalone executable
pyinstaller --onefile --name cli-tool src/cli_tool/main.py

# Test installation
pip install dist/*.whl
cli-tool --version

# Upload to PyPI
twine upload dist/*
```

### Testing and Debugging
```bash
# Run with verbose output
cli-tool --verbose command

# Run with configuration file
cli-tool --config configs/debug.yaml command

# Test with dry run
cli-tool --dry-run command args

# Profile performance
python -m cProfile -o profile.stats -m cli_tool command
```

## Claude-Specific Instructions

### Code Generation Preferences
- **Always** use Click or Typer for CLI framework implementation
- **Always** include comprehensive help text and examples
- **Include** proper error handling with user-friendly messages
- **Add** type hints and docstrings for all functions
- **Use** Rich library for beautiful terminal output
- **Include** configuration file support with validation
- **Add** logging with configurable verbosity levels

### CLI Interface Design
- **Start** with clear command structure and logical grouping
- **Include** both simple and advanced usage patterns
- **Add** progress indicators for long-running operations
- **Use** consistent option naming and behavior across commands
- **Include** examples in help text and documentation
- **Support** both interactive and non-interactive usage

### Testing Focus
- **Include** Click TestRunner for command testing
- **Add** integration tests for complete workflows
- **Test** error conditions and edge cases
- **Validate** exit codes and output format
- **Include** configuration file testing
- **Test** cross-platform compatibility patterns

### Distribution Considerations
- **Support** multiple installation methods (pip, standalone executable)
- **Include** proper package metadata and entry points
- **Add** version management and update checking
- **Consider** dependencies and package size optimization
- **Include** installation and usage documentation
- **Add** example configurations and use cases