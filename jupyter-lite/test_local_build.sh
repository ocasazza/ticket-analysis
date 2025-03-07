#!/bin/bash
# This script tests the JupyterLite build process locally

# Ensure we have the right Python/pip commands
PYTHON_CMD=""
PIP_CMD=""

# Check for python3/pip3 first
if command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
    if command -v pip3 &>/dev/null; then
        PIP_CMD="pip3"
    elif command -v python3 -m pip &>/dev/null; then
        PIP_CMD="python3 -m pip"
    fi
# Then check for python/pip
elif command -v python &>/dev/null; then
    PYTHON_CMD="python"
    if command -v pip &>/dev/null; then
        PIP_CMD="pip"
    elif command -v python -m pip &>/dev/null; then
        PIP_CMD="python -m pip"
    fi
fi

# Check if we found Python and pip
if [ -z "$PYTHON_CMD" ]; then
    echo "Error: Python not found. Please install Python 3."
    exit 1
fi

if [ -z "$PIP_CMD" ]; then
    echo "Error: pip not found. Please make sure pip is installed with your Python."
    echo "You may need to run: $PYTHON_CMD -m ensurepip --upgrade"
    exit 1
fi

echo "Using Python: $PYTHON_CMD"
echo "Using pip: $PIP_CMD"

echo "Installing required dependencies..."
$PIP_CMD install --upgrade pip wheel || { echo "Failed to upgrade pip"; exit 1; }
$PIP_CMD install jupyterlite-core || { echo "Failed to install jupyterlite-core"; exit 1; }
$PIP_CMD install -e . || { echo "Failed to install package from setup.py"; exit 1; }

echo "Creating data directories..."
# Copy to content directory (for Jupyter notebooks access)
mkdir -p content/data/fresh_service_tickets
cp -r ../data/fresh_service_tickets/*.csv content/data/fresh_service_tickets/ 2>/dev/null || echo "Could not copy data files to content (this is normal if running locally first time)"

# Copy to static/files directory (for direct file access in JupyterLite)
mkdir -p static/files/data/fresh_service_tickets
cp -r ../data/fresh_service_tickets/*.csv static/files/data/fresh_service_tickets/ 2>/dev/null || echo "Could not copy data files to static (this is normal if running locally first time)"

# Print list of files to verify
echo "Files in content/data/fresh_service_tickets:"
ls -la content/data/fresh_service_tickets/ 2>/dev/null || echo "No files found in content directory"

echo "Files in static/files/data/fresh_service_tickets:"
ls -la static/files/data/fresh_service_tickets/ 2>/dev/null || echo "No files found in static directory"

echo "Building JupyterLite..."
# Use the command with pyproject.toml configuration
$PYTHON_CMD -m jupyterlite build --config pyproject.toml || { 
    echo "Failed to build JupyterLite."
    echo "You can try running directly with verbose output:"
    echo "$PYTHON_CMD -m jupyterlite build --config pyproject.toml --debug"
    exit 1
}

if [ -d "_output" ]; then
    echo "Build successful! The _output directory was created."
    
    # Create directories in the output directory to match expected paths in the notebook
    echo "Copying data files directly to output..."
    mkdir -p _output/files/data/fresh_service_tickets
    cp -r ../data/fresh_service_tickets/*.csv _output/files/data/fresh_service_tickets/
    
    # List files to verify
    echo "Files in _output/files/data/fresh_service_tickets:"
    ls -la _output/files/data/fresh_service_tickets/
    
    echo "You can now test by running:"
    echo "$PYTHON_CMD -m http.server 8765 -d _output"
    echo "Then open your browser to http://localhost:8765"
else
    echo "Warning: The _output directory was not created. Build may have failed."
    echo "Check the error messages above and try again."
    exit 1
fi
