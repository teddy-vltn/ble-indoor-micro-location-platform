# NUC Web

Ce projet est une application web pour la configuration, visualisation et orchestration de l'environnement de micro-localisation du NUC.

## Problème
- La carte fonctionne mal sur Safari mais marche comme prévu sur les navigateurs basé sur Chromium

## i18n

Afin d'utiliser au mieux i18n et pouvoir éditer les langages différents on peut utiliser l'extension i18n-ally https://github.com/lokalise/i18n-ally

## Fonctionnalités

Ce tableau de bord permet :

- Gestion de l'inventaire des Raspberry Pi, incluant l'ajout, la modification et la suppression de dispositifs.
- Gestion du graphe des possibles avec utilisation et manipulation de fichiers SVG pour définir et visualiser le plan de l'environnement, incluant le zoom et le déplacement​​.
- Surveillance de l’état de l’environnement, incluant le statut en ligne/hors ligne des Raspberry Pi et l’état de la remontée des données​​.
- Gestion des profils de configuration, permettant la création de plusieurs configurations spécifiques et le basculement entre elles pour des expérimentations dans divers environnements​​.
- Visualisation en temps réel des déplacements des joueurs sur le graphe des possibles et suivi de leurs interactions avec l'environnement​​.
- Orchestration et gestion des services, avec la possibilité de lancer des scripts Ansible directement depuis le tableau de bord​​.

## Configuration

Afin de configuer l'adresse de l'API nécessaire au tableau de bord pour fonctionner il faut vous rendre dans le fichier .env et mettre à jour la variable d'environnement :

```bash
API_URL="http://{IP}:{PORT}"
```

## Installation 

Afin d'installer les dépendances requises, il faut tout d'abord :

```bash
npm install
```

Et ensuite afin de lancer localement le tableau de bord :

```bash
npm start
```