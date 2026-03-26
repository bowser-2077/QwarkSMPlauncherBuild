@echo off
REM Script de Démarrage du Lanceur QwarkSMP pour Windows (Version GUI)

echo Démarrage du Lanceur QwarkSMP (GUI)...

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo Erreur : Python n'est pas installé. Veuillez installer Python 3.10 ou supérieur.
    pause
    exit /b 1
)

REM Vérifier si l'environnement virtuel existe
if not exist "venv" (
    echo Création de l'environnement virtuel...
    python -m venv venv
)

REM Activer l'environnement virtuel
call venv\Scripts\activate.bat

REM Vérifier si les dépendances sont installées
python -c "import PyQt6, minecraft_launcher_lib" >nul 2>&1
if errorlevel 1 (
    echo Installation des dépendances requises...
    pip install -r requirements.txt
)

REM Démarrer le lanceur GUI
echo Démarrage du Lanceur QwarkSMP GUI...
python launcher_gui.py

pause
