# Configuration Docker pour Logstash

## Plugins
- logstash-output-mongodb : Installation de la version 3.1.5 pour assurer la compatibilité avec MongoDB 5.0 et éviter des erreurs connues.

## Dépendances
- tzdata : Pour les réglages de fuseau horaire.
- netbase : Pour la prise en charge des protocoles réseau et éviter des erreurs de chargement des protocoles natifs.

## Config 
### Input
La section input spécifie que Logstash doit écouter les données entrantes via le protocole Beats sur le port 5044.

```conf
input {
  beats {
    port => 5044
  }
}
```

### Filter

La section filter utilise un filtre grok pour extraire et structurer les données des messages entrants selon un modèle spécifique.

```conf
filter {
  grok {
    match => { "message" => "%{WORD:hostname},%{NUMBER:timestamp:float},%{NUMBER:major:int},%{NUMBER:minor:int},%{NUMBER:tx_power:int},%{NUMBER:rssi:int}" }
  }
}
```

### Output

La section output envoie les données structurées vers une base de données MongoDB. Les détails de connexion et de collection sont fournis via des variables d'environnement.

```conf
output {
  mongodb {
    uri => "${MONGODB_URI}"
    database => "${MONGODB_DATABASE}"
    collection => "${LOGSTASH_LOGS_COLLECTION}"
    codec => "json"
  }
}
```