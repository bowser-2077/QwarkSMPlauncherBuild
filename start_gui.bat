@echo off
REM QwarkSMP Launcher Startup Script for Windows (GUI Version)

echo Starting QwarkSMP Launcher (GUI)...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed. Please install Python 3.10 or higher.
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if requirements are installed
python -c "import PyQt6, minecraft_launcher_lib" >nul 2>&1
if errorlevel 1 (
    echo Installing required dependencies...
    pip install -r requirements.txt
)

REM Start GUI launcher
echo Starting QwarkSMP Launcher GUI...
python launcher_gui.py

pause
