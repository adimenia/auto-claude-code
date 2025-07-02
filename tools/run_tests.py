#!/usr/bin/env python3
"""Test runner script for the validation and migration systems."""

import sys
import subprocess
import argparse
from pathlib import Path


def run_tests(test_type="all", verbose=False, coverage=False, fast=False):
    """Run tests with specified options.
    
    Args:
        test_type: Type of tests to run ('all', 'unit', 'integration', 'validation', 'migration')
        verbose: Whether to run in verbose mode
        coverage: Whether to generate coverage report
        fast: Whether to skip slow tests
    """
    # Base pytest command
    cmd = [sys.executable, "-m", "pytest"]
    
    # Add test path
    tests_dir = Path(__file__).parent / "tests"
    
    # Determine which tests to run
    if test_type == "all":
        cmd.append(str(tests_dir))
    elif test_type == "unit":
        cmd.extend(["-m", "unit"])
        cmd.append(str(tests_dir))
    elif test_type == "integration":
        cmd.extend(["-m", "integration"])
        cmd.append(str(tests_dir))
    elif test_type == "validation":
        cmd.append(str(tests_dir / "test_validation.py"))
    elif test_type == "migration":
        cmd.append(str(tests_dir / "test_migration.py"))
    else:
        print(f"Unknown test type: {test_type}")
        return 1
    
    # Add options
    if verbose:
        cmd.append("-v")
    
    if fast:
        cmd.extend(["-m", "not slow"])
    
    if coverage:
        cmd.extend([
            "--cov=validation",
            "--cov=migration", 
            "--cov-report=html",
            "--cov-report=term-missing"
        ])
    
    # Run tests
    print(f"Running command: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, cwd=Path(__file__).parent)
        return result.returncode
    except KeyboardInterrupt:
        print("\nTests interrupted by user")
        return 130
    except Exception as e:
        print(f"Error running tests: {e}")
        return 1


def check_dependencies():
    """Check if required test dependencies are available."""
    missing_deps = []
    
    try:
        import pytest
    except ImportError:
        missing_deps.append("pytest")
    
    try:
        import rich
    except ImportError:
        print("Warning: Rich not available, some tests may be skipped")
    
    if missing_deps:
        print(f"Missing required dependencies: {', '.join(missing_deps)}")
        print("Install with: pip install pytest")
        return False
    
    return True


def main():
    """Main entry point for test runner."""
    parser = argparse.ArgumentParser(description="Run validation and migration tests")
    
    parser.add_argument(
        "test_type",
        nargs="?",
        default="all",
        choices=["all", "unit", "integration", "validation", "migration"],
        help="Type of tests to run"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Run in verbose mode"
    )
    
    parser.add_argument(
        "-c", "--coverage",
        action="store_true",
        help="Generate coverage report"
    )
    
    parser.add_argument(
        "-f", "--fast",
        action="store_true",
        help="Skip slow tests"
    )
    
    parser.add_argument(
        "--check-deps",
        action="store_true",
        help="Check test dependencies and exit"
    )
    
    args = parser.parse_args()
    
    if args.check_deps:
        if check_dependencies():
            print("All required dependencies are available")
            return 0
        else:
            return 1
    
    # Check dependencies before running tests
    if not check_dependencies():
        return 1
    
    # Run tests
    return run_tests(
        test_type=args.test_type,
        verbose=args.verbose,
        coverage=args.coverage,
        fast=args.fast
    )


if __name__ == "__main__":
    sys.exit(main())