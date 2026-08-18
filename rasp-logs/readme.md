# rasp-logs

Ce projet contient un script Python qui permet aux Raspberry Pi de cloner un projet mis à jour depuis le serveur NUC. Le script Python est également utilisé pour logger les données des capteurs connectés aux Raspberry Pi.

## Installation

### Raspberry Pi

#### Prérequis

- Python 3.7
- pip
- git
- flask
- bluepy (linux)
- pre-commit (dev)
- pyObjc (dev-darwin)

#### Installation

1. Cloner le projet

##### Raspberry PI

2. Installer les dépendances avec la commande `pip3 install -r requirements/prod.txt`

##### MacOS (only dev)

2. Installer les dépendances avec la commande `pip3 install -r requirements/dev-darwin.txt`

##### Linux/Windows (only dev)

2. Installer les dépendances avec la commande `pip3 install -r requirements/dev.txt`

## Documentation

### Structure du projet

- `main.py` : Script principal
- `requirements.txt` : Dépendances du projet
- `README.md` : Documentation du projet
- `config.json` : Fichier de configuration du projet
- `logs/` : Dossier contenant les logs du projet
- `lib/` : Dossier contenant les sources du projet
  - `settings.py` : Module de gestion de la configuration
  - `logger.py` : Module de gestion des logs
  - `scanner.py` : Module de gestion du scanner Bluetooth
  - `utils.py` : Module de fonctions utilitaires
  - `linux/` : Dossier contenant le code faisant appel aux commandes Linux
    - `blescanner.py` : Module de gestion du scanner Bluetooth sous Linux
  - `macos/` : Dossier contenant le code faisant appel aux commandes MacOS afin de pouvoir tester le script sur un ordinateur Apple
    - `blescanner.py` : Module de gestion du scanner Bluetooth sous MacOS
  - `models/` : Dossier contenant les classes
    - `ibeacon.py` : Classe représentant un iBeacon

### Configuration

Le fichier `config.json` contient la configuration du projet. Il est possible de modifier les paramètres suivants :
- `log_cache_size` : Nombre de lignes de logs à conserver en mémoire
- `major_filter_signal` : Filtre sur le major des iBeacons

### Logs

Les logs sont stockés sous deux formats :
- `logs.txt` : Logs des horaires d'action du script
- `data.csv` : Logs des données des iBeacons détectés

#### Format de sauvegarde du fichier `data.csv`

Le fichier `data.csv` contient les données des iBeacons détectés. Chaque ligne correspond à un iBeacon détecté. Les données sont séparées par des virgules.

Le format de chaque ligne est le suivant :
```identity,timestamp,major,minor,tx_power,rssi```
