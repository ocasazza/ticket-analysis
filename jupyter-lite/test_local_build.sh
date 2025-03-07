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
$PIP_CMD install -r requirements.txt || { echo "Failed to install from requirements.txt"; exit 1; }
$PIP_CMD install jupyterlite || { echo "Failed to install jupyterlite"; exit 1; }

echo "Creating data directory..."
mkdir -p content/data
cp -r ../data/fresh_service_tickets content/data/ 2>/dev/null || echo "Could not copy data files (this is normal if running locally first time)"

echo "Building JupyterLite..."
$PYTHON_CMD -m jupyterlite build || { 
    echo "Failed to build JupyterLite."
    echo "You may need to check for any errors above or try installing manually:" 
    echo "$PIP_CMD install jupyterlite"
    exit 1
}

if [ -d "_output" ]; then
    echo "Build successful! The _output directory was created."
    echo "You can now test by running:"
    echo "$PYTHON_CMD -m http.server 8765 -d _output"
    echo "Then open your browser to http://localhost:8765"
else
    echo "Warning: The _output directory was not created. Build may have failed."
    echo "Check the error messages above and try again."
    exit 1
fi
