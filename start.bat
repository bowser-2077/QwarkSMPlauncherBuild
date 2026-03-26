@echo off
REM QwarkSMP Launcher Startup Script for Windows

echo Starting QwarkSMP Launcher...

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
python -c "import flask, minecraft_launcher_lib" >nul 2>&1
if errorlevel 1 (
    echo Installing required dependencies...
    pip install -r requirements.txt
)

REM Start the launcher
echo Launching web interface...
echo Open your browser and navigate to http://localhost:5000
echo Press Ctrl+C to stop the launcher
echo.

python app.py

pause
