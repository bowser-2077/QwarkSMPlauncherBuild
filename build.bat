@echo off
REM QwarkSMP Launcher Build Script for Windows

echo 🚀 Starting QwarkSMP Launcher Windows build...

REM Check if launcher_gui.py exists
if not exist "launcher_gui.py" (
    echo [ERROR] launcher_gui.py not found. Please run this script from the project root.
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "build_env" (
    echo [INFO] Creating build virtual environment...
    python -m venv build_env
)

REM Activate build environment
echo [INFO] Activating build environment...
call build_env\Scripts\activate.bat

REM Install requirements
echo [INFO] Installing requirements...
pip install -r requirements.txt
pip install pyinstaller

REM Create build directory
set BUILD_DIR=dist_build
if exist "%BUILD_DIR%" (
    echo [INFO] Cleaning previous builds...
    rmdir /s /q "%BUILD_DIR%"
)
mkdir "%BUILD_DIR%"

REM Create icon
echo [INFO] Creating launcher icon...
python -c "
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPixmap, QPainter, QColor, QFont
from PyQt6.QtCore import Qt

app = QApplication([])
pixmap = QPixmap(256, 256)
pixmap.fill(QColor('#667eea'))
painter = QPainter(pixmap)
painter.setPen(QColor('#ffffff'))
painter.setFont(QFont('Arial', 160, QFont.Weight.Bold))
painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, 'Q')
painter.end()
pixmap.save('launcher_icon.png')
app.quit()
"

REM Build for Windows
echo [INFO] Building for Windows...
pyinstaller --onefile ^
           --windowed ^
           --name "QwarkSMPLauncher" ^
           --icon "launcher_icon.png" ^
           --add-data "launcher_backend.py;." ^
           --add-data "requirements.txt;." ^
           --distpath "%BUILD_DIR%\windows" ^
           --workpath "%BUILD_DIR%\windows\build" ^
           --specpath "%BUILD_DIR%\windows" ^
           launcher_gui.py

if %ERRORLEVEL% neq 0 (
    echo [ERROR] Windows build failed!
    pause
    exit /b 1
)

echo [SUCCESS] Windows build completed successfully!

REM Create distribution package
echo [INFO] Creating Windows distribution package...
cd "%BUILD_DIR%\windows"
mkdir "QwarkSMPLauncher-windows"
copy "QwarkSMPLauncher.exe" "QwarkSMPLauncher-windows\"
copy "..\..\start_gui.bat" "QwarkSMPLauncher-windows\"
copy "..\..\README.md" "QwarkSMPLauncher-windows\" 2>nul

REM Create zip
echo [INFO] Creating ZIP package...
powershell -command "Compress-Archive -Path 'QwarkSMPLauncher-windows' -DestinationPath 'QwarkSMPLauncher-windows.zip'"
cd ..\..

echo [SUCCESS] Windows package created: %BUILD_DIR%\windows\QwarkSMPLauncher-windows.zip

REM Clean up
echo [INFO] Cleaning up temporary files...
del /f launcher_icon.png
rmdir /s /q build_env

REM Create release info
echo [INFO] Creating release information...
(
echo QwarkSMP Launcher - Build Information
echo ====================================
echo.
echo Build Date: %date% %time%
echo Build Platform: Windows
echo.
echo Contents:
echo - Standalone executable ^(no Python installation required^)
echo - All dependencies bundled
echo - Original launcher files for reference
echo.
echo Installation:
echo 1. Extract QwarkSMPLauncher-windows.zip
echo 2. Run QwarkSMPLauncher.exe
echo.
echo Requirements:
echo - No Python installation needed
echo - Java 21+ required for Minecraft
echo - Internet connection for initial setup
echo.
echo Features:
echo - Modern PyQt6 interface
echo - Username-based authentication
echo - Automatic setup and mod management
echo - System tray integration
echo - Cross-platform compatibility
) > "%BUILD_DIR%\RELEASE_INFO.txt"

echo.
echo 🎉 Build process completed!
echo.
echo 📦 Distribution package created: %BUILD_DIR%\windows\QwarkSMPLauncher-windows.zip
echo.
echo 📄 Release information: %BUILD_DIR%\RELEASE_INFO.txt
echo.
echo [SUCCESS] Build artifacts are ready for distribution!
pause
