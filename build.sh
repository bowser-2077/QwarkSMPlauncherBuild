#!/bin/bash

# QwarkSMP Launcher Build Script - Cross-Platform Build
# This script creates executables for Windows, Linux, and macOS

set -e

echo "🚀 Starting QwarkSMP Launcher cross-platform build..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "launcher_gui.py" ]; then
    print_error "launcher_gui.py not found. Please run this script from the project root."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "build_env" ]; then
    print_status "Creating build virtual environment..."
    python3 -m venv build_env
fi

# Activate build environment
print_status "Activating build environment..."
source build_env/bin/activate

# Install requirements
print_status "Installing requirements..."
pip install -r requirements.txt
pip install pyinstaller

# Create build directory
BUILD_DIR="dist_build"
if [ -d "$BUILD_DIR" ]; then
    print_status "Cleaning previous builds..."
    rm -rf "$BUILD_DIR"
fi
mkdir -p "$BUILD_DIR"

# Function to build for specific platform
build_platform() {
    local platform=$1
    local icon_option=$2
    
    print_status "Building for $platform..."
    
    if [ -n "$icon_option" ]; then
        pyinstaller --onefile \
                   --windowed \
                   --name "QwarkSMPLauncher" \
                   --icon "$icon_option" \
                   --add-data "launcher_backend.py:." \
                   --add-data "requirements.txt:." \
                   --distpath "$BUILD_DIR/$platform" \
                   --workpath "$BUILD_DIR/$platform/build" \
                   --specpath "$BUILD_DIR/$platform" \
                   launcher_gui.py
    else
        pyinstaller --onefile \
                   --windowed \
                   --name "QwarkSMPLauncher" \
                   --add-data "launcher_backend.py:." \
                   --add-data "requirements.txt:." \
                   --distpath "$BUILD_DIR/$platform" \
                   --workpath "$BUILD_DIR/$platform/build" \
                   --specpath "$BUILD_DIR/$platform" \
                   launcher_gui.py
    fi
    
    if [ $? -eq 0 ]; then
        print_success "Build for $platform completed successfully!"
    else
        print_error "Build for $platform failed!"
        return 1
    fi
}

# Create a simple icon (if no icon provided)
create_icon() {
    print_status "Creating simple launcher icon..."
    python3 -c "
import sys
from PyQt6.QtWidgets import QApplication, QLabel
from PyQt6.QtGui import QPixmap, QPainter, QColor, QFont, QIcon
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
}

# Create icon
create_icon

# Build for current platform first
CURRENT_OS=$(uname -s)
case "$CURRENT_OS" in
    Linux*)
        print_status "Detected Linux system"
        build_platform "linux" "launcher_icon.png"
        ;;
    Darwin*)
        print_status "Detected macOS system"
        build_platform "macos" "launcher_icon.png"
        ;;
    CYGWIN*|MINGW*|MSYS*)
        print_status "Detected Windows system"
        build_platform "windows" "launcher_icon.png"
        ;;
    *)
        print_warning "Unknown OS: $CURRENT_OS"
        print_status "Building for Linux as default..."
        build_platform "linux" "launcher_icon.png"
        ;;
esac

# Create distribution packages
print_status "Creating distribution packages..."

# Linux package
if [ -d "$BUILD_DIR/linux" ]; then
    cd "$BUILD_DIR/linux"
    mkdir -p "QwarkSMPLauncher-linux"
    cp "QwarkSMPLauncher" "QwarkSMPLauncher-linux/"
    cp "../../../start_gui.sh" "QwarkSMPLauncher-linux/"
    cp "../../../README.md" "QwarkSMPLauncher-linux/" 2>/dev/null || true
    
    # Create tar.gz
    tar -czf "QwarkSMPLauncher-linux.tar.gz" "QwarkSMPLauncher-linux/"
    cd ../../..
    print_success "Linux package created: $BUILD_DIR/linux/QwarkSMPLauncher-linux.tar.gz"
fi

# Windows package (if on Windows)
if [ -d "$BUILD_DIR/windows" ]; then
    print_status "Windows build detected, creating package..."
    cd "$BUILD_DIR/windows"
    mkdir -p "QwarkSMPLauncher-windows"
    cp "QwarkSMPLauncher.exe" "QwarkSMPLauncher-windows/"
    cp "../../../start_gui.bat" "QwarkSMPLauncher-windows/"
    cp "../../../README.md" "QwarkSMPLauncher-windows/" 2>/dev/null || true
    
    # Create zip
    zip -r "QwarkSMPLauncher-windows.zip" "QwarkSMPLauncher-windows/"
    cd ../../..
    print_success "Windows package created: $BUILD_DIR/windows/QwarkSMPLauncher-windows.zip"
fi

# macOS package (if on macOS)
if [ -d "$BUILD_DIR/macos" ]; then
    print_status "macOS build detected, creating package..."
    cd "$BUILD_DIR/macos"
    mkdir -p "QwarkSMPLauncher-macos"
    cp -r "QwarkSMPLauncher.app" "QwarkSMPLauncher-macos/"
    cp "../../../start_gui.sh" "QwarkSMPLauncher-macos/"
    cp "../../../README.md" "QwarkSMPLauncher-macos/" 2>/dev/null || true
    
    # Create tar.gz
    tar -czf "QwarkSMPLauncher-macos.tar.gz" "QwarkSMPLauncher-macos/"
    cd ../../..
    print_success "macOS package created: $BUILD_DIR/macos/QwarkSMPLauncher-macos.tar.gz"
fi

# Clean up
print_status "Cleaning up temporary files..."
rm -f launcher_icon.png
rm -rf build_env

# Summary
print_success "Build process completed!"
echo ""
echo "📦 Distribution packages created in: $BUILD_DIR"
echo ""

if [ -d "$BUILD_DIR/linux" ]; then
    echo "🐧 Linux: $BUILD_DIR/linux/QwarkSMPLauncher-linux.tar.gz"
fi

if [ -d "$BUILD_DIR/windows" ]; then
    echo "🪟 Windows: $BUILD_DIR/windows/QwarkSMPLauncher-windows.zip"
fi

if [ -d "$BUILD_DIR/macos" ]; then
    echo "🍎 macOS: $BUILD_DIR/macos/QwarkSMPLauncher-macos.tar.gz"
fi

echo ""
print_status "Build artifacts are ready for distribution!"

# Create release info
cat > "$BUILD_DIR/RELEASE_INFO.txt" << EOF
QwarkSMP Launcher - Build Information
====================================

Build Date: $(date)
Build Platform: $(uname -s)

Contents:
- Standalone executable (no Python installation required)
- All dependencies bundled
- Original launcher files for reference

Installation:
1. Extract the appropriate package for your OS
2. Run the executable:
   - Linux: ./QwarkSMPLauncher
   - Windows: QwarkSMPLauncher.exe
   - macOS: Open QwarkSMPLauncher.app

Requirements:
- No Python installation needed
- Java 21+ required for Minecraft
- Internet connection for initial setup

Features:
- Modern PyQt6 interface
- Username-based authentication
- Automatic setup and mod management
- System tray integration
- Cross-platform compatibility
EOF

print_success "Release information created: $BUILD_DIR/RELEASE_INFO.txt"
