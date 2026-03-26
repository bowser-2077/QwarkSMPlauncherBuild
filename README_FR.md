# Lanceur QwarkSMP Minecraft

Un lanceur Minecraft personnalisé pour le serveur QwarkSMP, avec configuration automatique et authentification simple par nom d'utilisateur.

## Fonctionnalités

- **Configuration Automatique** : Installation en un clic de Minecraft 1.21.1 avec Fabric
- **Gestion des Mods** : Téléchargement et installation automatiques des mods requis
- **Authentification Simple** : Connexion par nom d'utilisateur avec authlib-injector (pas de compte Microsoft requis)
- **Configuration Mémoire** : Allocation RAM ajustable (2-16 Go)
- **Persistance du Nom** : Mémorise votre nom d'utilisateur pour la prochaine fois
- **Interface Propre** : Interface web moderne et responsive
- **Multi-plateforme** : Fonctionne sur Windows, macOS et Linux

## Mods Requis

Le lanceur télécharge et installe automatiquement ces mods :

- autojoin-mod-1.0.0.jar
- cloth-config-15.0.140-fabric.jar
- fabric-api-0.116.9+1.21.1.jar
- modmenu-11.0.4.jar

## Authentification

Ce lanceur utilise **authlib-injector** pour l'authentification :
- **Pas de compte Microsoft requis** - entrez simplement votre nom d'utilisateur
- **Génération UUID automatique** basée sur votre nom d'utilisateur
- **Injection Authlib** pour l'authentification serveur
- **Persistance du nom** - mémorise votre nom d'utilisateur pour le prochain lancement

## Installation

1. Installez Python 3.10 ou supérieur
2. Installez les dépendances requises :
   ```bash
   pip install -r requirements.txt
   ```

## Utilisation

### Démarrage Rapide
1. Lancez le lanceur :
   ```bash
   ./start_gui.sh  # Linux/macOS
   # ou
   start_gui.bat    # Windows
   ```

2. Ouvrez votre navigateur et naviguez vers `http://localhost:5000`

3. Cliquez sur "Configurer le lanceur" pour installer Minecraft, Fabric et les mods requis

4. Entrez votre nom d'utilisateur (3-16 caractères) et cliquez sur "Lancer Minecraft"

### Démarrage Manuel
```bash
python launcher_gui.py
```

## Structure du Projet

```
QwarkSMPlauncher/
├── launcher_gui.py          # Application PyQt6
├── launcher_backend.py     # Logique principale du lanceur
├── requirements.txt        # Dépendances Python
├── start_gui.sh          # Script de démarrage Linux/macOS
├── start_gui.bat         # Script de démarrage Windows
├── README.md             # Ce fichier
├── build.sh              # Script de build Linux/macOS
├── build.bat             # Script de build Windows
└── doc.txt               # Documentation
```

## Configuration

### Allocation Mémoire
Le lanceur supporte l'allocation mémoire de 2Go à 16Go. Vous pouvez ajuster cela dans l'interface avant de lancer.

### Nom d'Utilisateur
- Entrez un nom d'utilisateur (3-16 caractères)
- Le nom est automatiquement sauvegardé pour la prochaine fois
- L'UUID est généré basé sur le nom d'utilisateur pour le mode hors-ligne

### Configuration Authlib
Le lanceur télécharge automatiquement authlib-injector depuis :
```
https://github.com/bowser-2077/CascadeMC/raw/refs/heads/main/libs/authlib-injector.jar
```

Et se connecte au serveur d'authentification à :
```
https://auth-demo.yushi.moe
```

## Points d'Accès API

- `GET /` - Interface principale du lanceur
- `GET /status` - Vérifier l'état de configuration
- `POST /setup` - Installer Minecraft, Fabric et les mods
- `GET /get_saved_username` - Obtenir le nom d'utilisateur sauvegardé
- `POST /launch` - Lancer Minecraft avec le nom d'utilisateur

## Dépannage

### Problèmes Courants

1. **Échec de l'Installation Minecraft**
   - Vérifiez la connexion internet
   - Assurez-vous d'avoir assez d'espace disque
   - Vérifiez que minecraft-launcher-lib est à jour

2. **Échec de l'Installation Fabric**
   - Assurez-vous que Minecraft 1.21.1 est installé en premier
   - Vérifiez les chargeurs de mods en conflit

3. **Échec du Téléchargement des Mods**
   - Vérifiez que les URLs des mods sont accessibles
   - Vérifiez la connexion internet
   - Assurez-vous que le dossier mods a les permissions d'écriture

4. **Échec du Téléchargement Authlib**
   - Vérifiez l'accès au dépôt GitHub
   - Vérifiez la connexion internet
   - Assurez-vous que le dossier libs a les permissions d'écriture

5. **Échec du Lancement**
   - Vérifiez que le nom d'utilisateur fait 3-16 caractères
   - Vérifiez l'installation Java
   - Assurez-vous d'avoir assez de RAM allouée

### Journaux

Vérifiez la sortie console pour les messages d'erreur détaillés et les informations de progression.

## Développement

Ce lanceur utilise :
- **Backend** : Python avec Flask et minecraft-launcher-lib
- **Frontend** : PyQt6 avec interface moderne
- **Authentification** : authlib-injector avec génération UUID hors-ligne
- **Serveur Auth** : auth-demo.yushi.moe (serveur de démonstration)

## Notes de Sécurité

- Aucune information d'identification Microsoft requise
- Le nom d'utilisateur est stocké localement uniquement
- Utilise un serveur d'authentification de démonstration
- Authlib-injector est téléchargé depuis une source de confiance

## Licence

Ce projet est destiné à un usage privé avec le serveur QwarkSMP.

## Support

Pour les problèmes et le support, veuillez contacter l'administrateur du serveur.
