import sys
import os
import threading
import time
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtCore import pyqtSignal, QObject
import minecraft_launcher_lib
from launcher_backend import QwarkLauncher

class WorkerSignals(QObject):
    progress = pyqtSignal(str)
    finished = pyqtSignal(bool, str)
    status_updated = pyqtSignal(dict)

class SetupWorker(QRunnable):
    def __init__(self, launcher):
        super().__init__()
        self.launcher = launcher
        self.signals = WorkerSignals()

    def run(self):
        try:
            # Install Minecraft
            self.signals.progress.emit("Installing Minecraft 1.21.1...")
            if not self.launcher.install_minecraft(self.signals.progress.emit):
                self.signals.finished.emit(False, "Failed to install Minecraft")
                return

            # Install Fabric
            self.signals.progress.emit("Installing Fabric mod loader...")
            if not self.launcher.install_fabric(self.signals.progress.emit):
                self.signals.finished.emit(False, "Failed to install Fabric")
                return

            # Download mods
            self.signals.progress.emit("Downloading required mods...")
            mod_results = self.launcher.download_all_mods(self.signals.progress.emit)
            failed_mods = [mod for mod, success in mod_results.items() if not success]
            
            if failed_mods:
                self.signals.finished.emit(False, f"Failed to download mods: {', '.join(failed_mods)}")
                return

            # Download authlib-injector
            self.signals.progress.emit("Downloading authlib-injector...")
            if not self.launcher.download_authlib_injector(self.signals.progress.emit):
                self.signals.finished.emit(False, "Failed to download authlib-injector")
                return

            self.signals.finished.emit(True, "Setup completed successfully!")

        except Exception as e:
            self.signals.finished.emit(False, f"Setup failed: {str(e)}")

class LaunchWorker(QRunnable):
    def __init__(self, launcher, username, max_ram):
        super().__init__()
        self.launcher = launcher
        self.username = username
        self.max_ram = max_ram
        self.signals = WorkerSignals()

    def run(self):
        try:
            success = self.launcher.launch_minecraft(self.username, self.max_ram, self.signals.progress.emit)
            self.signals.finished.emit(success, "Minecraft launched!" if success else "Failed to launch Minecraft")
        except Exception as e:
            self.signals.finished.emit(False, f"Launch failed: {str(e)}")

class StatusIndicator(QLabel):
    def __init__(self, text):
        super().__init__(text)
        self.setStyleSheet("""
            QLabel {
                font-size: 12px;
                font-weight: 500;
                padding: 8px 12px;
                border-radius: 6px;
                background-color: #f0f0f0;
                border: 1px solid #d0d0d0;
            }
        """)
        self.set_incomplete()

    def set_complete(self):
        self.setStyleSheet("""
            QLabel {
                font-size: 12px;
                font-weight: 500;
                padding: 8px 12px;
                border-radius: 6px;
                background-color: #d4edda;
                border: 1px solid #c3e6cb;
                color: #155724;
            }
        """)
        self.setText("✓ " + self.text().replace("✓ ", "").replace("⏬ ", "").replace("⚠ ", ""))

    def set_incomplete(self):
        self.setStyleSheet("""
            QLabel {
                font-size: 12px;
                font-weight: 500;
                padding: 8px 12px;
                border-radius: 6px;
                background-color: #f8d7da;
                border: 1px solid #f5c6cb;
                color: #721c24;
            }
        """)
        self.setText("⏬ " + self.text().replace("✓ ", "").replace("⏬ ", "").replace("⚠ ", ""))

    def set_pending(self):
        self.setStyleSheet("""
            QLabel {
                font-size: 12px;
                font-weight: 500;
                padding: 8px 12px;
                border-radius: 6px;
                background-color: #fff3cd;
                border: 1px solid #ffeaa7;
                color: #856404;
            }
        """)
        self.setText("⚠ " + self.text().replace("✓ ", "").replace("⏬ ", "").replace("⚠ ", ""))

class QwarkSMPLauncher(QMainWindow):
    def __init__(self):
        super().__init__()
        self.launcher = QwarkLauncher()
        self.threadpool = QThreadPool()
        self.minecraft_process = None
        self.init_ui()
        self.update_status()
        self.setup_system_tray()

    def init_ui(self):
        self.setWindowTitle("Lanceur QwarkSMP")
        self.setFixedSize(500, 650)
        self.setWindowIcon(self.create_icon())
        
        # Set modern dark theme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QLabel {
                color: #ffffff;
                font-size: 14px;
            }
            QLineEdit {
                background-color: #404040;
                border: 2px solid #555555;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                color: #ffffff;
            }
            QLineEdit:focus {
                border-color: #667eea;
            }
            QComboBox {
                background-color: #404040;
                border: 2px solid #555555;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                color: #ffffff;
                min-width: 150px;
            }
            QComboBox:focus {
                border-color: #667eea;
            }
            QComboBox::drop-down {
                background-color: #404040;
                border: 1px solid #555555;
            }
            QComboBox QAbstractItemView {
                background-color: #404040;
                color: #ffffff;
                selection-background-color: #667eea;
            }
            QPushButton {
                background-color: #667eea;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: 600;
                color: #ffffff;
            }
            QPushButton:hover {
                background-color: #5a6fd8;
            }
            QPushButton:pressed {
                background-color: #4a5fc8;
            }
            QPushButton:disabled {
                background-color: #6c757d;
                color: #adb5bd;
            }
            QProgressBar {
                border: 2px solid #555555;
                border-radius: 8px;
                text-align: center;
                color: #ffffff;
                font-size: 12px;
                padding: 2px;
            }
            QProgressBar::chunk {
                background-color: #667eea;
                border-radius: 6px;
            }
        """)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Title
        title_label = QLabel("Lanceur QwarkSMP")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: 700;
                color: #667eea;
                margin-bottom: 10px;
            }
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        subtitle_label = QLabel("Minecraft 1.21.1 avec Fabric")
        subtitle_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #888888;
                margin-bottom: 20px;
            }
        """)
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle_label)

        # Status section
        status_group = QGroupBox("État de l'installation")
        status_group.setStyleSheet("""
            QGroupBox {
                font-size: 14px;
                font-weight: 600;
                color: #ffffff;
                border: 2px solid #555555;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        status_layout = QVBoxLayout(status_group)
        status_layout.setSpacing(10)

        self.minecraft_status = StatusIndicator("Minecraft 1.21.1")
        self.fabric_status = StatusIndicator("Chargeur de mods Fabric")
        self.mods_status = StatusIndicator("Mods requis (4)")
        self.authlib_status = StatusIndicator("Injecteur Authlib")

        status_layout.addWidget(self.minecraft_status)
        status_layout.addWidget(self.fabric_status)
        status_layout.addWidget(self.mods_status)
        status_layout.addWidget(self.authlib_status)

        layout.addWidget(status_group)

        # Configuration section
        config_group = QGroupBox("Configuration de lancement")
        config_group.setStyleSheet("""
            QGroupBox {
                font-size: 14px;
                font-weight: 600;
                color: #ffffff;
                border: 2px solid #555555;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        config_layout = QFormLayout(config_group)
        config_layout.setSpacing(15)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Entrez votre nom d'utilisateur")
        self.username_input.setMaxLength(16)
        self.username_input.textChanged.connect(self.on_username_changed)
        config_layout.addRow("Nom d'utilisateur:", self.username_input)

        self.ram_combo = QComboBox()
        self.ram_combo.addItems(["2 GB", "4 GB", "6 GB", "8 GB", "12 GB", "16 GB"])
        self.ram_combo.setCurrentIndex(1)  # Default to 4 GB
        config_layout.addRow("Mémoire:", self.ram_combo)

        layout.addWidget(config_group)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        # Progress label
        self.progress_label = QLabel("")
        self.progress_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #888888;
                margin: 10px 0;
            }
        """)
        self.progress_label.setVisible(False)
        layout.addWidget(self.progress_label)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        self.setup_btn = QPushButton("Configurer le lanceur")
        self.setup_btn.clicked.connect(self.start_setup)
        self.setup_btn.setFixedHeight(45)

        self.launch_btn = QPushButton("Lancer Minecraft")
        self.launch_btn.clicked.connect(self.launch_minecraft)
        self.launch_btn.setFixedHeight(45)
        self.launch_btn.setVisible(False)

        button_layout.addWidget(self.setup_btn)
        button_layout.addWidget(self.launch_btn)

        layout.addLayout(button_layout)

        # Load saved username
        saved_username = self.launcher.load_username()
        if saved_username:
            self.username_input.setText(saved_username)

    def create_icon(self):
        # Create a simple icon
        pixmap = QPixmap(32, 32)
        pixmap.fill(QColor("#667eea"))
        painter = QPainter(pixmap)
        painter.setPen(QPen(QColor("#ffffff"), 2))
        painter.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "Q")
        painter.end()
        return QIcon(pixmap)

    def on_username_changed(self, text):
        # Enable/disable launch button based on username validity
        valid = len(text.strip()) >= 3 and len(text.strip()) <= 16
        self.launch_btn.setEnabled(valid and self.launcher.is_setup_complete())

    def update_status(self):
        """Update status indicators"""
        status = self.launcher.get_setup_status()
        
        if status["minecraft_installed"]:
            self.minecraft_status.set_complete()
        else:
            self.minecraft_status.set_incomplete()

        if status["fabric_installed"]:
            self.fabric_status.set_complete()
        else:
            self.fabric_status.set_incomplete()

        if status["mods_downloaded"]:
            self.mods_status.set_complete()
        else:
            self.mods_status.set_incomplete()

        if status["authlib_downloaded"]:
            self.authlib_status.set_complete()
        else:
            self.authlib_status.set_incomplete()

        # Show launch button if everything is ready
        if self.launcher.is_setup_complete():
            self.launch_btn.setVisible(True)
            self.setup_btn.setText("Réinstaller les composants")
            self.on_username_changed(self.username_input.text())

    def start_setup(self):
        """Start the setup process"""
        self.setup_btn.setEnabled(False)
        self.launch_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_label.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        self.progress_label.setText("Démarrage de la configuration...")

        # Reset status to pending
        self.minecraft_status.set_pending()
        self.fabric_status.set_pending()
        self.mods_status.set_pending()
        self.authlib_status.set_pending()

        # Start setup worker
        worker = SetupWorker(self.launcher)
        worker.signals.progress.connect(self.update_progress)
        worker.signals.finished.connect(self.setup_finished)
        self.threadpool.start(worker)

    def launch_minecraft(self):
        """Launch Minecraft"""
        username = self.username_input.text().strip()
        
        if not username:
            QMessageBox.warning(self, "Nom d'utilisateur invalide", "Veuillez entrer un nom d'utilisateur (3-16 caractères).")
            return

        if len(username) < 3 or len(username) > 16:
            QMessageBox.warning(self, "Nom d'utilisateur invalide", "Le nom d'utilisateur doit contenir entre 3 et 16 caractères.")
            return

        self.setup_btn.setEnabled(False)
        self.launch_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_label.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        self.progress_label.setText("Lancement de Minecraft...")

        # Get RAM value
        ram_text = self.ram_combo.currentText()
        max_ram = int(ram_text.split()[0])

        # Minimize to system tray during launch
        self.showMinimized()

        # Start launch worker
        worker = LaunchWorker(self.launcher, username, max_ram)
        worker.signals.progress.connect(self.update_progress)
        worker.signals.finished.connect(self.launch_finished)
        self.threadpool.start(worker)

    def update_progress(self, message):
        """Update progress display"""
        self.progress_label.setText(message)
        QApplication.processEvents()

    def setup_finished(self, success, message):
        """Handle setup completion"""
        self.progress_bar.setVisible(False)
        self.progress_label.setVisible(False)
        self.setup_btn.setEnabled(True)
        
        if success:
            QMessageBox.information(self, "Configuration terminée", message)
            self.update_status()
        else:
            QMessageBox.critical(self, "Échec de la configuration", message)

    def launch_finished(self, success, message):
        """Handle launch completion"""
        self.progress_bar.setVisible(False)
        self.progress_label.setVisible(False)
        self.setup_btn.setEnabled(True)
        
        if success:
            QMessageBox.information(self, "Lancement réussi", "Minecraft lancé avec succès!\n\nLe lanceur sera réduit en arrière-plan.\nRestaurez-le depuis la barre système quand Minecraft fermera.")
            
            # Keep launcher alive but minimized
            # Don't close automatically - let user close manually
            self.on_username_changed(self.username_input.text())
        else:
            QMessageBox.critical(self, "Échec du lancement", message)
            self.on_username_changed(self.username_input.text())

    def setup_system_tray(self):
        """Setup system tray functionality"""
        if QSystemTrayIcon.isSystemTrayAvailable():
            # Create tray icon
            tray_icon = QIcon(self.create_icon())
            
            # Create tray menu
            tray_menu = QMenu()
            
            # Show/Hide action
            self.show_action = QAction("Afficher le lanceur", self)
            self.show_action.triggered.connect(self.show_from_tray)
            tray_menu.addAction(self.show_action)
            
            tray_menu.addSeparator()
            
            # Exit action
            exit_action = QAction("Quitter", self)
            exit_action.triggered.connect(self.close)
            tray_menu.addAction(exit_action)
            
            # Create tray icon
            self.tray_icon = QSystemTrayIcon(tray_icon)
            self.tray_icon.setContextMenu(tray_menu)
            self.tray_icon.setToolTip("Lanceur QwarkSMP")
            
            # Connect double-click to show window
            self.tray_icon.activated.connect(self.tray_icon_activated)
            
            self.tray_icon.show()
    
    def tray_icon_activated(self, reason):
        """Handle tray icon activation"""
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.show_from_tray()
    
    def show_from_tray(self):
        """Show window from system tray"""
        self.showNormal()
        self.raise_()
        self.activateWindow()
    
    def changeEvent(self, event):
        """Handle window state changes"""
        if event.type() == QEvent.Type.WindowStateChange:
            if self.isMinimized():
                if hasattr(self, 'tray_icon') and self.tray_icon.isVisible():
                    # Hide window when minimized
                    self.hide()
                    # Update tray menu
                    self.show_action.setText("Show Launcher")
        event.accept()
    
    def closeEvent(self, event):
        """Handle application close"""
        # Save username before closing
        username = self.username_input.text().strip()
        if username:
            self.launcher.save_username(username)
        
        # Check if Minecraft is running
        if self.minecraft_process and self.minecraft_process.poll() is None:
            # Minecraft is still running, ask user
            reply = QMessageBox.question(
                self, 
                "Minecraft en cours d'exécution", 
                "Minecraft est toujours en cours d'exécution. Êtes-vous sûr de vouloir fermer le lanceur ?\n\nCela n'affectera pas votre jeu.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                event.ignore()
                return
        
        event.accept()

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("QwarkSMP Launcher")
    app.setOrganizationName("QwarkSMP")
    
    # Check if another instance is running
    if len(sys.argv) > 1 and sys.argv[1] == "--single":
        # Find existing window and bring to front
        for widget in QApplication.topLevelWidgets():
            if isinstance(widget, QwarkSMPLauncher):
                widget.raise_()
                widget.activateWindow()
                return
    
    launcher = QwarkSMPLauncher()
    launcher.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
