#!/bin/bash
# Vibing Agent Engine Launcher (Linux/Mac)
# This script starts the autonomous agent engine

echo "==================================================================="
echo "  Vibing Agent Engine - Starting..."
echo "==================================================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 not found! Please install Python 3.9 or higher"
    exit 1
fi

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Launch the agent engine
cd "$SCRIPT_DIR"
python3 launcher.py

echo ""
echo "Agent Engine completed"
echo ""
