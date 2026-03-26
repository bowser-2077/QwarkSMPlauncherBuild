# QwarkSMP Launcher Build Scripts

This directory contains build scripts to create standalone executables for different platforms.

## Build Scripts

### 1. `build.sh` (Linux/macOS)
Cross-platform build script that detects the current OS and builds for that platform.

```bash
./build.sh
``

### 2. `build.bat` (Windows)
Windows-specific build script with batch commands.

```cmd
build.bat
```

### 3. `build_all.sh` (Linux/macOS)
Enhanced cross-platform build script with better packaging.

```bash
./build_all.sh
```

## Build Requirements

- Python 3.10+
- PyQt6
- PyInstaller (installed automatically)
- For cross-compilation: Docker or access to target platforms

## Build Process

The build scripts will:

1. **Create isolated build environment** - Virtual environment for clean builds
2. **Install dependencies** - All required packages including PyInstaller
3. **Generate launcher icon** - Custom "Q" icon with purple theme
4. **Build executable** - Standalone executable with PyInstaller
5. **Package distribution** - Create platform-specific archives
6. **Generate release info** - Documentation and installation instructions

## Output Structure

```
dist_build/
├── linux/
│   ├── QwarkSMPLauncher-linux/
│   │   ├── QwarkSMPLauncher (executable)
│   │   ├── start_gui.sh
│   │   └── README.md
│   └── QwarkSMPLauncher-linux.tar.gz
├── windows/
│   ├── QwarkSMPLauncher-windows/
│   │   ├── QwarkSMPLauncher.exe
│   │   ├── start_gui.bat
│   │   └── README.md
│   └── QwarkSMPLauncher-windows.zip
├── macos/
│   ├── QwarkSMPLauncher-macos/
│   │   ├── QwarkSMPLauncher.app
│   │   ├── start_gui.sh
│   │   └── README.md
│   └── QwarkSMPLauncher-macos.tar.gz
└── RELEASE_INFO.txt
```

## Platform-Specific Executables

### Linux
- **File**: `QwarkSMPLauncher`
- **Package**: `QwarkSMPLauncher-linux.tar.gz`
- **Requirements**: None (Python bundled)

### Windows
- **File**: `QwarkSMPLauncher.exe`
- **Package**: `QwarkSMPLauncher-windows.zip`
- **Requirements**: None (Python bundled)

### macOS
- **File**: `QwarkSMPLauncher.app`
- **Package**: `QwarkSMPLauncher-macos.tar.gz`
- **Requirements**: None (Python bundled)

## Features of Built Executables

✅ **Standalone** - No Python installation required
✅ **Bundled Dependencies** - All libraries included
✅ **Modern UI** - PyQt6 dark theme interface
✅ **System Tray** - Background operation support
✅ **Cross-Platform** - Works on Windows, Linux, macOS
✅ **Small Size** - Optimized distribution packages
✅ **Icon Integration** - Custom launcher icon
✅ **Auto-Setup** - One-click Minecraft installation

## Usage

### For Users
1. Download the appropriate package for your OS
2. Extract the archive
3. Run the executable:
   - Linux: `./QwarkSMPLauncher`
   - Windows: `QwarkSMPLauncher.exe`
   - macOS: Open `QwarkSMPLauncher.app`

### For Developers
1. Run the appropriate build script for your platform
2. Find distribution packages in `dist_build/`
3. Upload packages for distribution

## Cross-Platform Building

To build for all platforms from a single machine:

### Option 1: Use GitHub Actions
Set up CI/CD to build on each platform automatically.

### Option 2: Use Docker
Create containers for each target platform.

### Option 3: Manual Builds
Run each build script on its native platform.

## Troubleshooting

### Build Issues
- Ensure Python 3.10+ is installed
- Check internet connection for dependency downloads
- Verify PyQt6 installation

### Runtime Issues
- Ensure Java 21+ is installed for Minecraft
- Check system permissions for file access
- Verify internet connection for initial setup

## Size Estimates

- **Linux**: ~50-80 MB
- **Windows**: ~60-100 MB  
- **macOS**: ~70-120 MB

## Distribution

The built executables are ready for:
- Direct distribution to users
- Upload to file hosting services
- Integration with download managers
- Package manager inclusion (if desired)
