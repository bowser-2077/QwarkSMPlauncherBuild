#!/bin/bash

# QwarkSMP Launcher Startup Script (GUI Version)

echo "Starting QwarkSMP Launcher (GUI)..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3.10 or higher."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Check if requirements are installed
if ! python -c "import PyQt6, minecraft_launcher_lib" &> /dev/null; then
    echo "Installing required dependencies..."
    pip install -r requirements.txt
fi

# Start GUI launcher
echo "Starting QwarkSMP Launcher GUI..."
python launcher_gui.py
