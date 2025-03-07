#!/usr/bin/env python3
"""
Test runner script for Freshservice API.

This script runs the test suite for the Freshservice API library.
"""
import os
import sys
import subprocess
import shutil


def run_tests():
    """Run the test suite."""
    print("Running Freshservice API test suite...")
    
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Change to the script directory
    os.chdir(script_dir)
    
    # Check if pytest is installed
    pytest_path = shutil.which("pytest")
    if not pytest_path:
        print("Error: pytest not found. Please install development dependencies:")
        print("pip install -e \".[dev]\"")
        print("or")
        print("pip install -r requirements.txt")
        return 1
    
    # Check if pytest-cov is installed
    try:
        import pytest_cov
    except ImportError:
        print("Warning: pytest-cov not found. Coverage reporting will not be available.")
        print("To enable coverage reporting, install pytest-cov:")
        print("pip install pytest-cov")
        print("or")
        print("pip install -e \".[dev]\"")
        print("or")
        print("pip install -r requirements.txt")
        
        # Run pytest without coverage options
        cmd = [pytest_path]
    else:
        # Run pytest with coverage options
        cmd = [pytest_path, "--cov=lib", "--cov-report=term-missing"]
    
    # Add any command line arguments
    cmd.extend(sys.argv[1:])
    
    print(f"Running command: {' '.join(cmd)}")
    
    # Run the tests
    result = subprocess.run(cmd)
    
    # Return the exit code
    return result.returncode


if __name__ == "__main__":
    sys.exit(run_tests())
