#!/bin/bash

# Script de Démarrage du Lanceur QwarkSMP (Version GUI)

echo "Démarrage du Lanceur QwarkSMP (GUI)..."

# Vérifier si Python est installé
if ! command -v python3 &> /dev/null; then
    echo "Erreur : Python 3 n'est pas installé. Veuillez installer Python 3.10 ou supérieur."
    exit 1
fi

# Vérifier si l'environnement virtuel existe
if [ ! -d "venv" ]; then
    echo "Création de l'environnement virtuel..."
    python3 -m venv venv
fi

# Activer l'environnement virtuel
source venv/bin/activate

# Vérifier si les dépendances sont installées
if ! python -c "import PyQt6, minecraft_launcher_lib" &> /dev/null; then
    echo "Installation des dépendances requises..."
    pip install -r requirements.txt
fi

# Démarrer le lanceur GUI
echo "Démarrage du Lanceur QwarkSMP GUI..."
python launcher_gui.py
