# Scripts de Build du Lanceur QwarkSMP

Ce répertoire contient les scripts de build pour créer des exécutables autonomes pour différentes plateformes.

## Scripts de Build

### 1. `build.sh` (Linux/macOS)
Script de build multi-plateforme qui détecte le système d'exploitation actuel et construit pour cette plateforme.

```bash
./build.sh
```

### 2. `build.bat` (Windows)
Script de build spécifique à Windows avec commandes batch.

```cmd
build.bat
```

### 3. `build_all.sh` (Linux/macOS)
Script de build multi-plateforme amélioré avec meilleur packaging.

```bash
./build_all.sh
```

## Prérequis de Build

- Python 3.10+
- PyQt6
- PyInstaller (installé automatiquement)
- Pour la compilation croisée : Docker ou accès aux plateformes cibles

## Processus de Build

Les scripts de build vont :

1. **Créer un environnement de build isolé** - Environnement virtuel pour des builds propres
2. **Installer les dépendances** - Tous les packages requis incluant PyInstaller
3. **Générer l'icône du lanceur** - Icône personnalisée "Q" avec thème violet
4. **Construire l'exécutable** - Exécutable autonome avec PyInstaller
5. **Créer les packages de distribution** - Créer des archives spécifiques à la plateforme
6. **Générer les informations de release** - Documentation et instructions d'installation

## Structure de Sortie

```
dist_build/
├── linux/
│   ├── QwarkSMPLauncher-linux/
│   │   ├── QwarkSMPLauncher (exécutable)
│   │   ├── start_gui_fr.sh
│   │   └── README_FR.md
│   └── QwarkSMPLauncher-linux.tar.gz
├── windows/
│   ├── QwarkSMPLauncher-windows/
│   │   ├── QwarkSMPLauncher.exe
│   │   ├── start_gui_fr.bat
│   │   └── README_FR.md
│   └── QwarkSMPLauncher-windows.zip
├── macos/
│   ├── QwarkSMPLauncher-macos/
│   │   ├── QwarkSMPLauncher.app
│   │   ├── start_gui_fr.sh
│   │   └── README_FR.md
│   └── QwarkSMPLauncher-macos.tar.gz
└── RELEASE_INFO.txt
```

## Exécutables Spécifiques par Plateforme

### Linux
- **Fichier** : `QwarkSMPLauncher`
- **Package** : `QwarkSMPLauncher-linux.tar.gz`
- **Prérequis** : Aucun (Python inclus)

### Windows
- **Fichier** : `QwarkSMPLauncher.exe`
- **Package** : `QwarkSMPLauncher-windows.zip`
- **Prérequis** : Aucun (Python inclus)

### macOS
- **Fichier** : `QwarkSMPLauncher.app`
- **Package** : `QwarkSMPLauncher-macos.tar.gz`
- **Prérequis** : Aucun (Python inclus)

## Fonctionnalités des Exécutables Compilés

✅ **Autonome** - Aucune installation Python requise
✅ **Dépendances Incluses** - Toutes les bibliothèques incluses
✅ **Interface Moderne** - Interface PyQt6 avec thème sombre
✅ **Barre Système** - Support d'opération en arrière-plan
✅ **Multi-plateforme** - Fonctionne sur Windows, Linux, macOS
✅ **Taille Optimisée** - Packages de distribution optimisés
✅ **Intégration Icône** - Icône personnalisée du lanceur
✅ **Configuration Auto** - Installation Minecraft en un clic

## Utilisation

### Pour les Utilisateurs
1. Téléchargez le package approprié pour votre système d'exploitation
2. Extrayez l'archive
3. Lancez l'exécutable :
   - Linux : `./QwarkSMPLauncher`
   - Windows : `QwarkSMPLauncher.exe`
   - macOS : Ouvrir `QwarkSMPLauncher.app`

### Pour les Développeurs
1. Lancez le script de build approprié pour votre plateforme
2. Trouvez les packages de distribution dans `dist_build/`
3. Téléversez les packages pour distribution

## Build Multi-plateforme

Pour construire pour toutes les plateformes depuis une seule machine :

### Option 1 : Utiliser GitHub Actions
Configurez CI/CD pour construire automatiquement sur chaque plateforme.

### Option 2 : Utiliser Docker
Créez des conteneurs pour chaque plateforme cible.

### Option 3 : Builds Manuels
Lancez chaque script de build sur sa plateforme native.

## Dépannage

### Problèmes de Build
- Assurez-vous que Python 3.10+ est installé
- Vérifiez la connexion internet pour les téléchargements de dépendances
- Vérifiez l'installation PyQt6

### Problèmes d'Exécution
- Assurez-vous que Java 21+ est installé pour Minecraft
- Vérifiez les permissions système pour l'accès aux fichiers
- Vérifiez la connexion internet pour la configuration initiale

## Estimations de Taille

- **Linux** : ~50-80 Mo
- **Windows** : ~60-100 Mo  
- **macOS** : ~70-120 Mo

## Distribution

Les exécutables construits sont prêts pour :
- Distribution directe aux utilisateurs
- Téléversement vers services d'hébergement de fichiers
- Intégration avec gestionnaires de téléchargement
- Inclusion dans gestionnaires de packages (si désiré)

baguette
