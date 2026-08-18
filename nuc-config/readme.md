# NUC

Ce projet contient tous les modules nécessaires au bon fonctionnement de l'environnement de micro-localisation en quasi temps réel, tels que :
- Graph Positioning
- API
- Base de données
- Orchestration Ansible

## Lancer l'environnement

Le projet a été entièrement dockerisé, permettant de lancer facilement l'environnement. Pour cela, Docker doit être installé sur votre machine.

Ensuite, lancez l'environnement avec la commande suivante : ```docker compose up```

## Problème de connexion entre la borne ORBI et le NUC

Il arrive souvent que le pont réseau entre le routeur ORBI et le NUC ne s'établisse pas correctement. Pour résoudre ce problème, exécutez le script suivant : ```./setup/init-forwading.sh```

## Structure

Le dossier ansible contient tout les scripts nécessaire au bon fonctionnement d'Ansible et de l'orchestration générale du projet.

## Comment ajouter un nouveau Raspberry dans notre environnement

Tout d'abord pour ajouter un raspberry dans notre environnement il va falloir récupérer son adresse ip statique. Si le nommage du Raspberry suit la règle de tout les autres Raspberry alors sont adresse IP devrait être tel que: 192.168.1.1XX. On peut alors venir ajouter son adresse IP au DNS dans `setup/dns` dans le fichier `hosts` et lancer le script `install.sh`.

