# Serveur Web Flask pour Raspberry Pi

Permet d'exécuter un petit serveur web utilisant Flask afin de pouvoir demander par commande l'état de certains services afin de savoir quels services sont hors ligne ou en ligne.

Pour l'installer:
```
git clone https://github.com/teddy-vltn/rasp/rasp-webserver
cd rasp-webserver
sudo chmod +x setup.sh
sudo ./setup.sh
```

Ensuite, pour savoir si un service est en ligne ou non :
```
http://<ip_raspberry>:5000/status?service_name=<nom_du_service>
```

On peut aussi savoir pour plusieurs services en même temps :
```
http://<ip_raspberry>:5000/status?service_name=<nom_du_service1>&service_name=<nom_du_service2>
```

Par exemple si on veut savoir si `FileBeat` et `rasplogs` sont en ligne:
```
http://<ip_raspberry>:5000/status?service_name=filebeat&service_name=rasplogs
```