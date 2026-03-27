import os
import json
import subprocess
import threading
import uuid
import requests
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import minecraft_launcher_lib
from minecraft_launcher_lib import exceptions

class QwarkLauncher:
    def __init__(self):
        self.minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory()
        self.version = "1.21.1"
        self.mod_loader = "fabric"
        self.profile_name = "QwarkSMP"
        
        # Custom instance directory
        self.instance_directory = os.path.join(self.minecraft_directory, "QwarkSMP")
        
        # Authlib configuration
        self.authlib_jar_path = os.path.join(self.instance_directory, "libs", "authlib-injector.jar")
        self.authlib_url = "https://auth-demo.yushi.moe"
        self.authlib_download_url = "https://github.com/bowser-2077/CascadeMC/raw/refs/heads/main/libs/authlib-injector.jar"
        self.username_file = os.path.join(self.instance_directory, "username.txt")
        
        # Mods to download
        self.mods = [
            # Core mods
            "https://github.com/bowser-2077/QwarkSMPmods/raw/refs/heads/main/fabric-api-0.116.9+1.21.1.jar",
            "https://github.com/bowser-2077/QwarkSMPmods/raw/refs/heads/main/cloth-config-15.0.140-fabric.jar",
            "https://github.com/bowser-2077/QwarkSMPmods/raw/refs/heads/main/modmenu-11.0.4.jar",
            "https://github.com/bowser-2077/QwarkSMPmods/raw/refs/heads/main/autojoin-mod-1.0.0.jar",
            # Performance mods
            "https://cdn.modrinth.com/data/AANobbMI/versions/u1OEbNKx/sodium-fabric-0.6.13%2Bmc1.21.1.jar",
            "https://cdn.modrinth.com/data/NNAgCjsB/versions/zzguHbcL/entityculling-fabric-1.10.0-mc1.21.1.jar",
            "https://cdn.modrinth.com/data/YL57xq9U/versions/zsoi0dso/iris-fabric-1.8.8%2Bmc1.21.1.jar",
            "https://cdn.modrinth.com/data/uXXizFIs/versions/sOzRw3CG/ferritecore-7.0.3-fabric.jar",
            "https://cdn.modrinth.com/data/OmQzuQFa/versions/BSvW2cAf/LazyDFU-%5BUNOFFICIAL%5D-1.21.jar"
        ]
        
        # Ensure directories exist
        self.ensure_directories()
        
    def ensure_directories(self):
        """Create necessary directories"""
        directories = [
            self.minecraft_directory,
            self.instance_directory,
            os.path.join(self.instance_directory, "mods"),
            os.path.join(self.instance_directory, "versions"),
            os.path.join(self.instance_directory, "libraries"),
            os.path.join(self.instance_directory, "assets"),
            os.path.join(self.instance_directory, "libs")
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
    
    def get_offline_uuid(self, username):
        """Generate offline UUID from username"""
        return str(uuid.uuid3(uuid.NAMESPACE_DNS, username)).replace("-", "")
    
    def save_username(self, username):
        """Save username for next time"""
        try:
            with open(self.username_file, 'w') as f:
                f.write(username)
        except Exception as e:
            print(f"Failed to save username: {e}")
    
    def load_username(self):
        """Load saved username"""
        try:
            if os.path.exists(self.username_file):
                with open(self.username_file, 'r') as f:
                    return f.read().strip()
        except Exception as e:
            print(f"Failed to load username: {e}")
        return ""
    
    def download_authlib_injector(self, progress_callback=None) -> bool:
        """Download authlib-injector.jar"""
        try:
            if progress_callback:
                progress_callback("Downloading authlib-injector...")
            
            response = requests.get(self.authlib_download_url, stream=True)
            response.raise_for_status()
            
            # Ensure libs directory exists
            os.makedirs(os.path.dirname(self.authlib_jar_path), exist_ok=True)
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(self.authlib_jar_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if progress_callback and total_size > 0:
                            progress = (downloaded / total_size) * 100
                            progress_callback(f"Downloading authlib-injector: {progress:.1f}%")
            
            return True
        except Exception as e:
            print(f"Failed to download authlib-injector: {str(e)}")
            return False
    
    
    def download_mod(self, url: str, progress_callback=None) -> bool:
        """Download a single mod file"""
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            filename = url.split('/')[-1]
            mod_path = os.path.join(self.instance_directory, "mods", filename)
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(mod_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if progress_callback and total_size > 0:
                            progress = (downloaded / total_size) * 100
                            progress_callback(f"Downloading {filename}: {progress:.1f}%")
            
            return True
        except Exception as e:
            print(f"Failed to download {url}: {str(e)}")
            return False
    
    def download_all_mods(self, progress_callback=None) -> Dict[str, bool]:
        """Download all required mods"""
        results = {}
        total_mods = len(self.mods)
        
        for i, mod_url in enumerate(self.mods):
            if progress_callback:
                progress_callback(f"Downloading mod {i+1}/{total_mods}")
            
            filename = mod_url.split('/')[-1]
            results[filename] = self.download_mod(mod_url, progress_callback)
        
        return results
    
    def install_minecraft(self, progress_callback=None) -> bool:
        """Install Minecraft 1.21.1"""
        try:
            if progress_callback:
                progress_callback("Installing Minecraft 1.21.1...")
            
            minecraft_launcher_lib.install.install_minecraft_version(
                self.version, 
                self.minecraft_directory,
                callback={"setStatus": progress_callback} if progress_callback else None
            )
            
            return True
        except Exception as e:
            print(f"Failed to install Minecraft: {str(e)}")
            return False
    
    def install_fabric(self, progress_callback=None) -> bool:
        """Install Fabric mod loader"""
        try:
            if progress_callback:
                progress_callback("Installing Fabric mod loader...")
            
            # Get the fabric mod loader
            fabric_loader = minecraft_launcher_lib.mod_loader.get_mod_loader("fabric")
            
            # Install fabric for 1.21.1
            installed_version = fabric_loader.install(
                self.version,
                self.minecraft_directory,
                callback={"setStatus": progress_callback} if progress_callback else None
            )
            
            if progress_callback:
                progress_callback(f"Fabric installed: {installed_version}")
            
            return True
        except Exception as e:
            print(f"Failed to install Fabric: {str(e)}")
            return False
    
    def get_installed_version(self) -> str:
        """Get the installed version string for launching"""
        try:
            fabric_loader = minecraft_launcher_lib.mod_loader.get_mod_loader("fabric")
            latest_loader = fabric_loader.get_latest_loader_version(self.version)
            return f"fabric-loader-{latest_loader}-{self.version}"
        except Exception:
            # Fallback to the standard format
            return f"fabric-loader-0.18.5-{self.version}"
    
    def launch_minecraft(self, username: str, max_ram_gb: int = 4, progress_callback=None) -> bool:
        """Launch Minecraft with authlib injection"""
        try:
            if progress_callback:
                progress_callback("Preparing launch...")
            
            # Save username for next time
            self.save_username(username)
            
            # Ensure authlib-injector is downloaded
            if not os.path.exists(self.authlib_jar_path):
                if not self.download_authlib_injector(progress_callback):
                    return False
            
            # Create launch options
            options = {
                "username": username,
                "uuid": self.get_offline_uuid(username),
                "token": "fake-token",
                "jvmArguments": [
                    f"-Xmx{max_ram_gb}G",
                    f"-Xms{max_ram_gb}G",
                    f"-javaagent:{self.authlib_jar_path}={self.authlib_url}"
                ],
                "launcherName": "QwarkSMP Launcher",
                "launcherVersion": "1.0.0"
            }
            
            # Get installed fabric version
            installed_version = self.get_installed_version()
            
            # Get launch command
            command = minecraft_launcher_lib.command.get_minecraft_command(
                installed_version,
                self.minecraft_directory,  # Use main minecraft directory for versions
                options
            )
            
            if progress_callback:
                progress_callback("Launching Minecraft...")
            
            # Launch Minecraft in a separate thread (no terminal window)
            def launch():
                try:
                    # Hide terminal window by using appropriate launch method
                    if os.name == 'nt':  # Windows
                        startupinfo = subprocess.STARTUPINFO()
                        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                        startupinfo.wShowWindow = subprocess.SW_HIDE
                        subprocess.run(command, cwd=self.instance_directory, startupinfo=startupinfo)
                    else:  # Linux/macOS
                        subprocess.run(command, cwd=self.instance_directory, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                except Exception as e:
                    if progress_callback:
                        progress_callback(f"Launch failed: {str(e)}")
            
            thread = threading.Thread(target=launch)
            thread.daemon = True
            thread.start()
            
            return True
        except Exception as e:
            print(f"Failed to launch Minecraft: {str(e)}")
            return False
    
    def is_setup_complete(self) -> bool:
        """Check if the launcher is fully set up"""
        mods_dir = os.path.join(self.instance_directory, "mods")
        
        # Check if Minecraft is installed
        if not minecraft_launcher_lib.utils.is_version_valid(self.version, self.minecraft_directory):
            return False
        
        # Check if Fabric is installed
        try:
            fabric_loader = minecraft_launcher_lib.mod_loader.get_mod_loader("fabric")
            if not fabric_loader.is_minecraft_version_supported(self.version):
                return False
        except:
            return False
        
        # Check if mods exist
        mod_files = [url.split('/')[-1] for url in self.mods]
        for mod_file in mod_files:
            if not os.path.exists(os.path.join(mods_dir, mod_file)):
                return False
        
        # Check if authlib-injector exists
        if not os.path.exists(self.authlib_jar_path):
            return False
        
        return True
    
    def get_setup_status(self) -> Dict[str, bool]:
        """Get detailed setup status"""
        mods_dir = os.path.join(self.instance_directory, "mods")
        mod_files = [url.split('/')[-1] for url in self.mods]
        
        return {
            "minecraft_installed": minecraft_launcher_lib.utils.is_version_valid(self.version, self.minecraft_directory),
            "fabric_installed": self._check_fabric_installed(),
            "mods_downloaded": all(os.path.exists(os.path.join(mods_dir, mod_file)) for mod_file in mod_files),
            "authlib_downloaded": os.path.exists(self.authlib_jar_path)
        }
    
    def _check_fabric_installed(self) -> bool:
        """Check if Fabric is properly installed"""
        try:
            fabric_loader = minecraft_launcher_lib.mod_loader.get_mod_loader("fabric")
            return fabric_loader.is_minecraft_version_supported(self.version)
        except:
            return False
