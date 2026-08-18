# Filebeat pour Raspberry Pi Zero W

Ce dépôt permet l'installation d'une version de FileBeat compatible avec l'architecture "armv6l" des Raspberry Pi Zero W.

Ce projet est séparé de "rasp-logs" afin d'éviter de devoir retélécharger FileBeat à chaque fois qu'une nouvelle version de "rasp-logs" doit être déployée.

# Installation

**Normalement, ce script ne devrait pas être téléchargé indépendamment. Cependant, si nécessaire, suivez le protocole suivant. Il est prévu pour être chargé par Ansible.**

Pour télécharger sur un Raspberry Pi Zero W la version de FileBeat, exécutez les commandes suivantes : 

```bash
git clone https://github.com/teddy-vltn/rasp/rasp-filebeat.git
```

```bash
cd rasp-filebeat
sudo chmod +x setup.sh
sudo ./setup.sh
```

FileBeat devrait désormais être démarré ou en cours de démarrage.

Vous pouvez vérifier son état en exécutant :

```bash
systemctl status filebeat.service
```








