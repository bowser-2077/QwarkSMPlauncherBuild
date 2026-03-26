# QwarkSMP Minecraft Launcher

A custom Minecraft launcher for QwarkSMP server, featuring automatic setup and simple username authentication.

## Featuress

- **Automatic Setup**: One-click installation of Minecraft 1.21.1 with Fabric
- **Mod Management**: Automatic download and installation of required mods
- **Simple Authentication**: Username-based login with authlib-injector (no Microsoft account required)
- **Memory Configuration**: Adjustable RAM allocation (2-16 GB)
- **Username Persistence**: Remembers your username for next time
- **Clean Interface**: Modern, responsive web-based interface
- **Cross-Platform**: Works on Windows, macOS, and Linux

## Required Mods

The launcher automatically downloads and installs these mods:

- autojoin-mod-1.0.0.jar
- cloth-config-15.0.140-fabric.jar
- fabric-api-0.116.9+1.21.1.jar
- modmenu-11.0.4.jar

## Authentication

This launcher uses **authlib-injector** for authentication:
- **No Microsoft account required** - just enter your username
- **Automatic UUID generation** based on your username
- **Authlib injection** for server authentication
- **Username persistence** - remembers your username for next launch

## Installation

1. Install Python 3.10 or higher
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Quick Start
1. Run the launcher:
   ```bash
   ./start.sh  # Linux/macOS
   # or
   start.bat    # Windows
   ```

2. Open your browser and navigate to `http://localhost:5000`

3. Click "Setup Launcher" to install Minecraft, Fabric, and required mods

4. Enter your username (3-16 characters) and click "Launch Minecraft"

### Manual Start
```bash
python app.py
```

## Project Structure

```
QwarkSMPlauncher/
├── app.py                 # Flask web application
├── launcher_backend.py    # Core launcher logic
├── requirements.txt       # Python dependencies
├── start.sh              # Linux/macOS startup script
├── start.bat             # Windows startup script
├── README.md             # This file
└── doc.txt               # Documentation
```

## Configuration

### Memory Allocation
The launcher supports memory allocation from 2GB to 16GB. You can adjust this in the interface before launching.

### Username
- Enter any username (3-16 characters)
- Username is automatically saved for next time
- UUID is generated based on username for offline mode

### Authlib Configuration
The launcher automatically downloads authlib-injector from:
```
https://github.com/bowser-2077/CascadeMC/raw/refs/heads/main/libs/authlib-injector.jar
```

And connects to the auth server at:
```
https://auth-demo.yushi.moe
```

## API Endpoints

- `GET /` - Main launcher interface
- `GET /status` - Check setup status
- `POST /setup` - Install Minecraft, Fabric, and mods
- `GET /get_saved_username` - Get saved username
- `POST /launch` - Launch Minecraft with username

## Troubleshooting

### Common Issues

1. **Minecraft Installation Fails**
   - Check internet connection
   - Ensure sufficient disk space
   - Verify minecraft-launcher-lib is up to date

2. **Fabric Installation Fails**
   - Ensure Minecraft 1.21.1 is installed first
   - Check for conflicting mod loaders

3. **Mod Download Fails**
   - Verify mod URLs are accessible
   - Check internet connection
   - Ensure mods directory has write permissions

4. **Authlib Download Fails**
   - Check GitHub repository access
   - Verify internet connection
   - Ensure libs directory has write permissions

5. **Launch Fails**
   - Verify username is 3-16 characters
   - Check Java installation
   - Ensure sufficient RAM allocation

### Logs

Check the console output for detailed error messages and progress information.

## Development

This launcher uses:
- **Backend**: Python with Flask and minecraft-launcher-lib
- **Frontend**: HTML5, CSS3, and JavaScript
- **Authentication**: authlib-injector with offline UUID generation
- **Auth Server**: auth-demo.yushi.moe (demo server)

## Security Notes

- No Microsoft account credentials required
- Username is stored locally only
- Uses demo auth server for authentication
- Authlib-injector is downloaded from trusted source

## License

This project is for private use with with QwarkSMP server.

## Support

For issues and support, please contact the server administrator.
