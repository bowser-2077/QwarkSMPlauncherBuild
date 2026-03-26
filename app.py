from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import threading
import json
import os
from launcher_backend import QwarkLauncher

app = Flask(__name__)
CORS(app)

# Global launcher instance
launcher = QwarkLauncher()

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QwarkSMP Launcher</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .launcher-container {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            max-width: 500px;
            width: 90%;
            backdrop-filter: blur(10px);
        }

        .header {
            text-align: center;
            margin-bottom: 30px;
        }

        .header h1 {
            color: #333;
            font-size: 2.5em;
            margin-bottom: 10px;
            background: linear-gradient(45deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .header p {
            color: #666;
            font-size: 1.1em;
        }

        .status-section {
            margin-bottom: 30px;
        }

        .status-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px;
            margin-bottom: 10px;
            background: #f8f9fa;
            border-radius: 10px;
            border-left: 4px solid #ddd;
        }

        .status-item.complete {
            border-left-color: #28a745;
        }

        .status-item.incomplete {
            border-left-color: #dc3545;
        }

        .status-item.pending {
            border-left-color: #ffc107;
        }

        .status-text {
            font-weight: 500;
            color: #333;
        }

        .status-indicator {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #ddd;
        }

        .status-indicator.complete {
            background: #28a745;
        }

        .status-indicator.incomplete {
            background: #dc3545;
        }

        .status-indicator.pending {
            background: #ffc107;
            animation: pulse 1.5s infinite;
        }

        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }

        .controls-section {
            margin-bottom: 30px;
        }

        .username-selector {
            margin-bottom: 20px;
        }

        .username-selector label {
            display: block;
            margin-bottom: 10px;
            font-weight: 500;
            color: #333;
        }

        .username-selector input {
            width: 100%;
            padding: 12px;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            font-size: 16px;
            background: white;
            transition: border-color 0.3s;
        }

        .username-selector input:focus {
            outline: none;
            border-color: #667eea;
        }

        .ram-selector {
            margin-bottom: 20px;
        }

        .ram-selector label {
            display: block;
            margin-bottom: 10px;
            font-weight: 500;
            color: #333;
        }

        .ram-selector select {
            width: 100%;
            padding: 12px;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            font-size: 16px;
            background: white;
            cursor: pointer;
            transition: border-color 0.3s;
        }

        .ram-selector select:focus {
            outline: none;
            border-color: #667eea;
        }

        .btn {
            width: 100%;
            padding: 15px;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            margin-bottom: 10px;
        }

        .btn-primary {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
        }

        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
        }

        .btn-primary:disabled {
            background: #ccc;
            cursor: not-allowed;
            transform: none;
            box-shadow: none;
        }

        .btn-secondary {
            background: #6c757d;
            color: white;
        }

        .btn-secondary:hover {
            background: #5a6268;
        }

        .progress-section {
            display: none;
            margin-bottom: 30px;
        }

        .progress-bar {
            width: 100%;
            height: 8px;
            background: #e9ecef;
            border-radius: 4px;
            overflow: hidden;
            margin-bottom: 10px;
        }

        .progress-fill {
            height: 100%;
            background: linear-gradient(45deg, #667eea, #764ba2);
            width: 0%;
            transition: width 0.3s;
        }

        .progress-text {
            text-align: center;
            color: #666;
            font-size: 14px;
        }

        .login-section {
            display: none;
            margin-bottom: 30px;
        }

        .login-btn {
            background: #0078d4;
            color: white;
        }

        .login-btn:hover {
            background: #106ebe;
        }

        .message {
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            text-align: center;
        }

        .message.success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }

        .message.error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }

        .message.info {
            background: #d1ecf1;
            color: #0c5460;
            border: 1px solid #bee5eb;
        }

        .footer {
            text-align: center;
            margin-top: 30px;
            color: #666;
            font-size: 14px;
        }

        .hidden {
            display: none !important;
        }
    </style>
</head>
<body>
    <div class="launcher-container">
        <div class="header">
            <h1>QwarkSMP Launcher</h1>
            <p>Minecraft 1.21.1</p>
        </div>

        <div id="message" class="message hidden"></div>

        <div class="status-section">
            <div id="minecraft-status" class="status-item incomplete">
                <span class="status-text">Minecraft 1.21.1</span>
                <div class="status-indicator incomplete"></div>
            </div>
            <div id="fabric-status" class="status-item incomplete">
                <span class="status-text">Fabric Mods</span>
                <div class="status-indicator incomplete"></div>
            </div>
            <div id="mods-status" class="status-item incomplete">
                <span class="status-text">Mods Requis</span>
                <div class="status-indicator incomplete"></div>
            </div>
            <div id="authlib-status" class="status-item incomplete">
                <span class="status-text">Authlib Injector (Requis)</span>
                <div class="status-indicator incomplete"></div>
            </div>
        </div>

        <div class="controls-section">
            <div class="username-selector">
                <label for="username-input">Pseudo:</label>
                <input type="text" id="username-input" placeholder="Nom D'utilisateur" maxlength="16">
            </div>
            <div class="ram-selector">
                <label for="ram-select">Ram Allouée:</label>
                <select id="ram-select">
                    <option value="2">2 GB RAM</option>
                    <option value="4" selected>4 GB RAM</option>
                    <option value="6">6 GB RAM</option>
                    <option value="8">8 GB RAM</option>
                    <option value="12">12 GB RAM</option>
                    <option value="16">16 GB RAM</option>
                </select>
            </div>
        </div>

        <div class="progress-section" id="progress-section">
            <div class="progress-bar">
                <div class="progress-fill" id="progress-fill"></div>
            </div>
            <div class="progress-text" id="progress-text">Chargement...</div>
        </div>


        <div class="action-buttons">
            <button id="setup-btn" class="btn btn-primary" onclick="startSetup()">Installer Les Dépendences</button>
            <button id="launch-btn" class="btn btn-primary hidden" onclick="launchGame()">Lancer Le Jeu</button>
            <button id="retry-btn" class="btn btn-secondary hidden" onclick="retrySetup()">Réessayer</button>
        </div>

        <div class="footer">
            <p>QwarkSMP Launcher v1.0.1</p>
        </div>
    </div>

    <script>
        let setupInProgress = false;
        let savedUsername = "";

        // Check status on page load
        window.onload = function() {
            checkStatus();
        };

        function checkStatus() {
            fetch('/status')
                .then(response => response.json())
                .then(data => {
                    updateStatusDisplay(data);
                    if (data.setup_complete) {
                        showLaunchButton();
                    }
                    // Load saved username
                    if (!savedUsername) {
                        loadSavedUsername();
                    }
                })
                .catch(error => {
                    console.error('Error checking status:', error);
                });
        }

        function updateStatusDisplay(status) {
            // Minecraft status
            const minecraftStatus = document.getElementById('minecraft-status');
            updateStatusItem(minecraftStatus, status.minecraft_installed);

            // Fabric status
            const fabricStatus = document.getElementById('fabric-status');
            updateStatusItem(fabricStatus, status.fabric_installed);

            // Mods status
            const modsStatus = document.getElementById('mods-status');
            updateStatusItem(modsStatus, status.mods_downloaded);
            
            // Authlib status
            const authlibStatus = document.getElementById('authlib-status');
            updateStatusItem(authlibStatus, status.authlib_downloaded);
        }

        function updateStatusItem(element, complete) {
            const indicator = element.querySelector('.status-indicator');
            
            element.classList.remove('complete', 'incomplete', 'pending');
            indicator.classList.remove('complete', 'incomplete', 'pending');
            
            if (complete) {
                element.classList.add('complete');
                indicator.classList.add('complete');
            } else {
                element.classList.add('incomplete');
                indicator.classList.add('incomplete');
            }
        }

        function showMessage(message, type) {
            const messageEl = document.getElementById('message');
            messageEl.textContent = message;
            messageEl.className = `message ${type}`;
            messageEl.classList.remove('hidden');
            
            // Hide message after 5 seconds
            setTimeout(() => {
                messageEl.classList.add('hidden');
            }, 5000);
        }

        function showProgress(show) {
            const progressSection = document.getElementById('progress-section');
            progressSection.style.display = show ? 'block' : 'none';
        }

        function updateProgress(text, percentage = null) {
            const progressText = document.getElementById('progress-text');
            const progressFill = document.getElementById('progress-fill');
            
            progressText.textContent = text;
            if (percentage !== null) {
                progressFill.style.width = percentage + '%';
            }
        }

        function setButtonsDisabled(disabled) {
            const setupBtn = document.getElementById('setup-btn');
            const launchBtn = document.getElementById('launch-btn');
            const retryBtn = document.getElementById('retry-btn');
            
            setupBtn.disabled = disabled;
            launchBtn.disabled = disabled;
            retryBtn.disabled = disabled;
        }

        function showLaunchButton() {
            document.getElementById('setup-btn').classList.add('hidden');
            document.getElementById('launch-btn').classList.remove('hidden');
            document.getElementById('retry-btn').classList.add('hidden');
        }

        function showRetryButton() {
            document.getElementById('setup-btn').classList.add('hidden');
            document.getElementById('launch-btn').classList.add('hidden');
            document.getElementById('retry-btn').classList.remove('hidden');
        }

        function startSetup() {
            if (setupInProgress) return;
            
            setupInProgress = true;
            setButtonsDisabled(true);
            showProgress(true);
            updateProgress('Starting setup...', 0);

            fetch('/setup', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showMessage('Setup completed successfully!', 'success');
                    showLaunchButton();
                    checkStatus();
                } else {
                    showMessage('Setup failed: ' + data.error, 'error');
                    showRetryButton();
                }
            })
            .catch(error => {
                console.error('Setup error:', error);
                showMessage('Setup failed: ' + error.message, 'error');
                showRetryButton();
            })
            .finally(() => {
                setupInProgress = false;
                setButtonsDisabled(false);
                showProgress(false);
            });
        }

        function retrySetup() {
            document.getElementById('setup-btn').classList.remove('hidden');
            document.getElementById('retry-btn').classList.add('hidden');
            startSetup();
        }

        function loadSavedUsername() {
            fetch('/get_saved_username')
                .then(response => response.json())
                .then(data => {
                    if (data.username) {
                        savedUsername = data.username;
                        document.getElementById('username-input').value = data.username;
                    }
                })
                .catch(error => {
                    console.error('Error loading username:', error);
                });
        }

        function launchGame() {
            const usernameInput = document.getElementById('username-input');
            const username = usernameInput.value.trim();
            
            if (!username) {
                showMessage('Please enter a username', 'error');
                usernameInput.focus();
                return;
            }
            
            if (username.length < 3 || username.length > 16) {
                showMessage('Username must be between 3 and 16 characters', 'error');
                usernameInput.focus();
                return;
            }
            
            const ramSelect = document.getElementById('ram-select');
            const maxRam = parseInt(ramSelect.value);
            
            setButtonsDisabled(true);
            showMessage('Launching Minecraft...', 'info');
            
            fetch('/launch', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: username,
                    max_ram_gb: maxRam
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showMessage('Minecraft launched successfully!', 'success');
                    // Close launcher after a delay
                    setTimeout(() => {
                        window.close();
                    }, 3000);
                } else {
                    showMessage('Launch failed: ' + data.error, 'error');
                    setButtonsDisabled(false);
                }
            })
            .catch(error => {
                console.error('Launch error:', error);
                showMessage('Launch failed: ' + error.message, 'error');
                setButtonsDisabled(false);
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Serve the main launcher interface"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/status')
def get_status():
    """Get current setup status"""
    try:
        status = launcher.get_setup_status()
        return jsonify({
            "success": True,
            "setup_complete": launcher.is_setup_complete(),
            **status
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

@app.route('/setup', methods=['POST'])
def setup_launcher():
    """Setup the launcher (install Minecraft, Fabric, and mods)"""
    def progress_callback(message):
        # Store progress in a global variable for polling
        app.config['progress_message'] = message
    
    try:
        # Install Minecraft
        if not launcher.install_minecraft(progress_callback):
            return jsonify({
                "success": False,
                "error": "Failed to install Minecraft"
            })
        
        # Install Fabric
        if not launcher.install_fabric(progress_callback):
            return jsonify({
                "success": False,
                "error": "Failed to install Fabric"
            })
        
        # Download mods
        mod_results = launcher.download_all_mods(progress_callback)
        failed_mods = [mod for mod, success in mod_results.items() if not success]
        
        if failed_mods:
            return jsonify({
                "success": False,
                "error": f"Failed to download mods: {', '.join(failed_mods)}"
            })
        
        return jsonify({
            "success": True,
            "message": "Setup completed successfully"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

@app.route('/progress')
def get_progress():
    """Get current progress message"""
    progress = app.config.get('progress_message', 'Idle')
    return jsonify({"progress": progress})

@app.route('/get_saved_username')
def get_saved_username():
    """Get saved username"""
    try:
        username = launcher.load_username()
        return jsonify({
            "success": True,
            "username": username
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })


@app.route('/launch', methods=['POST'])
def launch_minecraft():
    """Launch Minecraft"""
    try:
        data = request.get_json()
        username = data.get('username')
        max_ram_gb = data.get('max_ram_gb', 4)
        
        def progress_callback(message):
            app.config['launch_progress'] = message
        
        success = launcher.launch_minecraft(username, max_ram_gb, progress_callback)
        
        return jsonify({
            "success": success,
            "message": "Minecraft launched" if success else "Failed to launch Minecraft"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
