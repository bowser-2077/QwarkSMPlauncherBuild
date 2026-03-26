#!/bin/bash

# QwarkSMP Launcher Cross-Platform Build Script
# This script builds for all three platforms using Docker for cross-compilation

set -e

echo "🚀 Starting QwarkSMP Launcher cross-platform build..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() { echo -e "${BLUE}[INFO]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Check if we're in the right directory
if [ ! -f "launcher_gui.py" ]; then
    print_error "launcher_gui.py not found. Please run this script from the project root."
    exit 1
fi

# Create virtual environment
if [ ! -d "build_env" ]; then
    print_status "Creating build virtual environment..."
    python3 -m venv build_env
fi

source build_env/bin/activate

# Install requirements
print_status "Installing requirements..."
pip install -r requirements.txt
pip install pyinstaller

# Create build directory
BUILD_DIR="dist_build"
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"

# Create icon
print_status "Creating launcher icon..."
python3 -c "
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

# Function to build for specific platform
build_for_platform() {
    local platform=$1
    local target=$2
    
    print_status "Building for $platform..."
    
    # Create the target directory first
    mkdir -p "$BUILD_DIR/$target"
    
    # Use absolute paths for data files
    pyinstaller --onefile \
               --windowed \
               --name "QwarkSMPLauncher" \
               --icon "launcher_icon.png" \
               --add-data "$(pwd)/launcher_backend.py:." \
               --add-data "$(pwd)/requirements.txt:." \
               --distpath "$BUILD_DIR/$target" \
               --workpath "$BUILD_DIR/$target/build" \
               --specpath "$BUILD_DIR/$target" \
               launcher_gui.py
    
    if [ $? -eq 0 ]; then
        print_success "$platform build completed!"
    else
        print_error "$platform build failed!"
        return 1
    fi
}

# Build for current platform
CURRENT_OS=$(uname -s)
case "$CURRENT_OS" in
    Linux*)
        build_for_platform "Linux" "linux" "launcher_icon.png"
        ;;
    Darwin*)
        build_for_platform "macOS" "macos" "launcher_icon.png"
        ;;
    CYGWIN*|MINGW*|MSYS*)
        build_for_platform "Windows" "windows" "launcher_icon.png"
        ;;
    *)
        print_warning "Unknown OS: $CURRENT_OS"
        print_status "Building for Linux as default..."
        build_for_platform "Linux" "linux" "launcher_icon.png"
        ;;
esac

# Create distribution packages
print_status "Creating distribution packages..."

# Linux package
if [ -d "$BUILD_DIR/linux" ]; then
    cd "$BUILD_DIR/linux"
    mkdir -p "QwarkSMPLauncher-linux"
    cp "QwarkSMPLauncher" "QwarkSMPLauncher-linux/"
    cp "../../start_gui_fr.sh" "QwarkSMPLauncher-linux/"
    cp "../../README_FR.md" "QwarkSMPLauncher-linux/" 2>/dev/null || true
    
    # Create tar.gz
    tar -czf "QwarkSMPLauncher-linux.tar.gz" "QwarkSMPLauncher-linux/"
    cd ../../..
    print_success "Linux package created"
fi

# Windows package (if built)
if [ -d "$BUILD_DIR/windows" ]; then
    cd "$BUILD_DIR/windows"
    mkdir -p "QwarkSMPLauncher-windows"
    cp "QwarkSMPLauncher.exe" "QwarkSMPLauncher-windows/" 2>/dev/null || true
    cp "../../start_gui_fr.bat" "QwarkSMPLauncher-windows/" 2>/dev/null || true
    cp "../../README_FR.md" "QwarkSMPLauncher-windows/" 2>/dev/null || true
    
    if [ -f "QwarkSMPLauncher.exe" ]; then
        zip -r "QwarkSMPLauncher-windows.zip" "QwarkSMPLauncher-windows/"
        cd ../../..
        print_success "Windows package created"
    else
        cd ../../..
    fi
fi

# macOS package (if built)
if [ -d "$BUILD_DIR/macos" ]; then
    cd "$BUILD_DIR/macos"
    mkdir -p "QwarkSMPLauncher-macos"
    cp -r "QwarkSMPLauncher.app" "QwarkSMPLauncher-macos/" 2>/dev/null || true
    cp "../../start_gui_fr.sh" "QwarkSMPLauncher-macos/" 2>/dev/null || true
    cp "../../README_FR.md" "QwarkSMPLauncher-macos/" 2>/dev/null || true
    
    if [ -d "QwarkSMPLauncher.app" ]; then
        tar -czf "QwarkSMPLauncher-macos.tar.gz" "QwarkSMPLauncher-macos/"
        cd ../../..
        print_success "macOS package created"
    else
        cd ../../..
    fi
fi

# Clean up
print_status "Cleaning up..."
rm -f launcher_icon.png
rm -rf build_env

# Create release info only if it doesn't exist
if [ ! -f "$BUILD_DIR/RELEASE_INFO.txt" ]; then
    cat > "$BUILD_DIR/RELEASE_INFO.txt" << EOF
QwarkSMP Launcher - Cross-Platform Build
======================================

Build Date: $(date)
Build Platform: $(uname -s)

Platform-Specific Packages:
- Linux: QwarkSMPLauncher-linux.tar.gz
- Windows: QwarkSMPLauncher-windows.zip (if built on Windows)
- macOS: QwarkSMPLauncher-macos.tar.gz (if built on macOS)

Installation Instructions:
1. Download the package for your operating system
2. Extract the archive
3. Run the executable:
   - Linux: ./QwarkSMPLauncher
   - Windows: QwarkSMPLauncher.exe
   - macOS: Open QwarkSMPLauncher.app

System Requirements:
- No Python installation required (bundled)
- Java 21+ for Minecraft
- Internet connection for initial setup
- 2GB+ RAM recommended

Features:
- Modern PyQt6 desktop interface
- Username-based authentication with authlib-injector
- Automatic Minecraft 1.21.1 + Fabric setup
- Required mods auto-download
- System tray integration
- Background operation
- Cross-platform compatibility
- French localization

Technical Details:
- Built with PyInstaller for standalone executables
- All dependencies bundled
- No external dependencies required
EOF
fi

# Summary
print_success "Build process completed!"
echo ""
echo "📦 Distribution packages created in: $BUILD_DIR"
echo ""

# List created packages
if [ -f "$BUILD_DIR/linux/QwarkSMPLauncher-linux.tar.gz" ]; then
    echo "🐧 Linux: QwarkSMPLauncher-linux.tar.gz"
fi

if [ -f "$BUILD_DIR/windows/QwarkSMPLauncher-windows.zip" ]; then
    echo "🪟 Windows: QwarkSMPLauncher-windows.zip"
fi

if [ -f "$BUILD_DIR/macos/QwarkSMPLauncher-macos.tar.gz" ]; then
    echo "🍎 macOS: QwarkSMPLauncher-macos.tar.gz"
fi

echo ""
echo "📄 Release info: $BUILD_DIR/RELEASE_INFO.txt"
echo ""
print_success "Build artifacts ready for distribution!"
