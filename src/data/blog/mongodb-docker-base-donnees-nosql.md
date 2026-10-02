---
title: "MongoDB Docker : base de données NoSQL pour applications modernes"
description: "Déploie MongoDB Docker avec docker-compose : image officielle, authentification, sauvegarde et bonnes pratiques pour ta base NoSQL auto-hébergée."
pubDatetime: "2026-10-02T11:02:12+02:00"
modDatetime: "2026-10-01T08:00:00.000Z"
author: Brandon
tags:
  - docker
  - base-de-donnees
  - sauvegarde
  - stockage
  - intermediaire
featured: false
draft: false
focusKeyword: mongodb docker
faqs:
  - question: "MongoDB Docker tourne-t-il correctement sur un Raspberry Pi ou un petit VPS ?"
    answer: "Oui, mais prévois au moins 1 à 2 Go de RAM. MongoDB charge son index en mémoire (WiredTiger), donc sous 512 Mo tu vas voir des swaps et des lenteurs dès que ta collection grossit un peu."
  - question: "Comment protéger un conteneur MongoDB Docker contre les accès non authentifiés ?"
    answer: "Définis MONGO_INITDB_ROOT_USERNAME et MONGO_INITDB_ROOT_PASSWORD dès le premier démarrage, ne publie jamais le port 27017 directement sur internet, et passe par un réseau Docker interne ou un tunnel VPN."
  - question: "Faut-il choisir MongoDB ou PostgreSQL pour un nouveau projet auto-hébergé ?"
    answer: "Si ton schéma change souvent ou que tu stockes des documents imbriqués (JSON, logs, catalogues produits), MongoDB simplifie la vie. Pour des données relationnelles avec des jointures fréquentes, PostgreSQL reste le choix le plus sûr."
---
> 💡 **TL;DR**
> - MongoDB Docker se déploie en un `docker compose up -d` avec l'image officielle `mongo`, sans installation système
> - Authentification obligatoire via `MONGO_INITDB_ROOT_USERNAME` / `MONGO_INITDB_ROOT_PASSWORD`, volume persistant pour ne rien perdre au redémarrage
> - Base NoSQL orientée documents, parfaite pour du JSON imbriqué, des catalogues ou des logs applicatifs

## MongoDB, c'est quoi et pourquoi le dockeriser

MongoDB, c'est une base de données NoSQL orientée documents. Au lieu de lignes et de colonnes comme sur MySQL ou PostgreSQL, tu stockes des documents au format BSON (une variante binaire de JSON). Pas de schéma rigide à définir à l'avance, pas de migration douloureuse à chaque fois que ton appli évolue. T'ajoutes un champ, il est là. Point.

C'est édité par MongoDB Inc., sous licence SSPL pour l'édition Community, qui reste gratuite et open-source. L'édition Community suffit largement pour un homelab ou une appli perso, Atlas (le service cloud managé de l'éditeur) n'entre pas en jeu ici puisqu'on parle d'auto-hébergement.

La vraie question c'est : pourquoi passer par Docker plutôt qu'une installation classique sur ton serveur ? Parce que MongoDB Docker t'évite d'installer des dépendances système, de gérer des dépôts APT tiers, et de polluer ton OS. Un conteneur, un volume, et tu peux le supprimer ou le mettre à jour sans toucher au reste de ta stack. Si tu héberges déjà d'autres services avec Docker (genre un wiki d'équipe avec [BookStack](/bookstack-docker-wiki-equipe/)), ajouter MongoDB Docker à côté prend cinq minutes.

Typiquement, tu vas en avoir besoin pour une appli Node.js avec Mongoose, un backend qui stocke des objets JSON variables, ou un projet qui ingère des logs avec des structures changeantes. Chez moi, je m'en sers pour des petits projets de scraping où la forme des données bouge à chaque itération. Un schéma SQL figé m'aurait fait perdre des heures en migrations.

## Table des matières

## Déployer MongoDB Docker avec docker-compose

L'image officielle `mongo` est maintenue activement sur Docker Hub, avec plus d'un milliard de pulls. La branche stable recommandée pour un déploiement sérieux reste la 8.0, la 9.0 vient tout juste de sortir et je préfère la laisser mûrir un peu avant de la mettre en prod chez un lecteur. Voici un `docker-compose.yml` fonctionnel pour ton setup MongoDB Docker :

```yaml
services:
  mongodb:
    image: mongo:8.0
    container_name: mongodb
    restart: unless-stopped
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: change_moi_vraiment
      MONGO_INITDB_DATABASE: monapp
    volumes:
      - ./mongodb/data:/data/db
      - ./mongodb/config:/data/configdb
    ports:
      - "27017:27017"
```

Quelques points qui comptent :

- `MONGO_INITDB_ROOT_USERNAME` et `MONGO_INITDB_ROOT_PASSWORD` sont indissociables. Les deux présents, MongoDB démarre avec l'authentification activée. Un seul des deux, et rien ne se passe.
- `volumes` pointe vers `/data/db`, c'est là que vivent tes vraies données. Sans ce volume, tu perds tout au premier `docker compose down`.
- Ne publie le port 27017 sur `ports` que si tu as vraiment besoin d'y accéder depuis l'extérieur du réseau Docker. Si une autre appli du même `docker-compose.yml` doit s'y connecter, elle le fait déjà via le nom du service `mongodb`, pas besoin d'exposer quoi que ce soit.

Lance la stack :

```bash
cd ~/docker/mongodb
docker compose up -d
docker compose logs -f mongodb
```

Le premier démarrage crée l'utilisateur root et initialise la base `monapp`. Compte quelques secondes avant que le conteneur réponde aux connexions.

## Se connecter à ta base avec mongosh

Pour interagir avec ton conteneur MongoDB Docker en ligne de commande, utilise `mongosh`, le shell officiel qui a remplacé l'ancien `mongo` CLI :

```bash
docker exec -it mongodb mongosh -u admin -p change_moi_vraiment --authenticationDatabase admin
```

Une fois connecté, tu peux créer une collection et insérer un document pour vérifier que tout fonctionne :

```javascript
use monapp
db.utilisateurs.insertOne({ nom: "Brandon", role: "admin", actif: true })
db.utilisateurs.find()
```

Pas de `CREATE TABLE`, pas de définition de colonnes. Tu insères, MongoDB range. C'est tout l'intérêt d'une base orientée documents : ta structure de données suit ton code, pas l'inverse.

Si tu préfères une interface graphique plutôt que le terminal, MongoDB Compass (gratuit, disponible sur mongodb.com) se connecte directement à ton conteneur via l'URI `mongodb://admin:change_moi_vraiment@ton-serveur:27017`.

## Sécuriser ton conteneur MongoDB

Par défaut, sans les variables d'authentification, MongoDB Docker accepte n'importe quelle connexion sans mot de passe. C'est le genre d'oubli qui remplit les logs de bots en quelques heures si le port traîne sur internet. Scanner les instances MongoDB ouvertes, c'est un classique pour n'importe quel script kiddie.

Checklist avant de mettre en prod :

- ✅ `MONGO_INITDB_ROOT_USERNAME` et `MONGO_INITDB_ROOT_PASSWORD` définis avec un vrai mot de passe, pas `admin123`
- ✅ Port 27017 jamais exposé directement sur internet. Si tu dois y accéder à distance, passe par un VPN ou un [tunnel Cloudflare](/cloudflare-tunnel-docker-homelab/) plutôt que d'ouvrir une redirection de port
- ✅ Un utilisateur applicatif dédié par base, avec des droits limités (`readWrite` sur sa base, pas `root`)
- ✅ Les logs du conteneur surveillés pour repérer des tentatives de connexion suspectes

⚠️ Si tu héberges plusieurs services exposés sur le même serveur, couple ton MongoDB Docker à un outil comme [CrowdSec](/crowdsec-docker-securite-collaborative/) pour bloquer automatiquement les IP qui scannent tes ports en masse. Ça ne remplace pas une bonne config réseau, mais ça ajoute une couche utile.

Crée un utilisateur applicatif limité depuis `mongosh` :

```javascript
use monapp
db.createUser({
  user: "appuser",
  pwd: "un_autre_mot_de_passe_solide",
  roles: [{ role: "readWrite", db: "monapp" }]
})
```

Ton appli se connecte ensuite avec ce compte, jamais avec le compte root.

## Sauvegarder et restaurer tes données

Un volume Docker protège tes données d'un redémarrage de conteneur, pas d'un disque qui lâche. La sauvegarde reste indispensable, et MongoDB fournit ses propres outils pour ça.

Dump complet de la base :

```bash
docker exec mongodb mongodump --username admin --password change_moi_vraiment --authenticationDatabase admin --out /data/backup
```

Le dump atterrit dans le conteneur, à toi de le sortir vers ton hôte :

```bash
docker cp mongodb:/data/backup ./backups/$(date +%Y%m%d)
```

Pour la restauration :

```bash
docker exec -i mongodb mongorestore --username admin --password change_moi_vraiment --authenticationDatabase admin /data/backup
```

Si tu veux automatiser ces sauvegardes sans réinventer un script cron fragile, [Duplicati](/duplicati-docker-sauvegarde/) peut chiffrer et envoyer ton dossier de dumps vers un stockage distant à intervalle régulier. L'astuce, c'est de laisser `mongodump` tourner en cron local pour générer le dump, puis de laisser Duplicati s'occuper du chiffrement et de l'envoi hors site.

✅ Teste tes restaurations de temps en temps sur un conteneur jetable. Une sauvegarde que tu n'as jamais restaurée n'est pas une sauvegarde, c'est un pari.

## Monitoring et dépannage courant

### Le conteneur refuse de démarrer

```bash
docker compose logs mongodb
```

La cause la plus fréquente : un volume de données corrompu après un arrêt brutal, ou un conflit de port 27017 déjà utilisé par une autre instance. Vérifie avec `sudo lsof -i :27017` côté hôte.

### Connexion refusée malgré un conteneur qui tourne

Vérifie que tu passes bien `--authenticationDatabase admin` dans ta commande de connexion. C'est l'erreur numéro un : oublier cette option fait échouer l'authentification même avec le bon mot de passe.

### Consommation mémoire qui explose

MongoDB utilise le moteur WiredTiger, qui garde une bonne partie de son cache en RAM par défaut (50 % de la RAM disponible moins 1 Go, grossièrement). Sur un petit serveur partagé avec d'autres conteneurs, limite ce cache explicitement :

```yaml
    command: ["mongod", "--wiredTigerCacheSizeGB", "0.5"]
```

Ajoute cette ligne dans ton service `mongodb` du `docker-compose.yml` si tu tournes sur une petite VM ou un Raspberry Pi.

## MongoDB vs PostgreSQL : quand choisir le NoSQL

Je vois souvent la question revenir : pourquoi ne pas juste utiliser PostgreSQL avec son type `jsonb`, qui gère très bien les documents aussi ?

Honnêtement, pour la majorité des projets perso, PostgreSQL fait le job et reste mon choix par défaut. Mais MongoDB Docker a du sens quand :

- Ton schéma change vraiment souvent, sans structure prévisible
- Tu stockes des documents fortement imbriqués (catalogues produits avec variantes, logs applicatifs, événements)
- Tu veux du sharding horizontal natif pour scaler sur plusieurs nœuds plus tard
- Ton équipe ou ta stack (souvent Node.js avec Mongoose) travaille déjà en JSON de bout en bout

À l'inverse, si tes données sont relationnelles avec des jointures fréquentes (facturation, inventaire avec des relations many-to-many), reste sur du SQL. Ce n'est pas une question de mode, c'est une question de forme de tes données.

## Conclusion

Déployer MongoDB Docker, c'est l'affaire d'un `docker-compose.yml` bien configuré, d'un volume persistant, et d'une authentification activée dès le premier démarrage. Rien de sorcier, mais les trois erreurs classiques (pas de volume, pas d'auth, port exposé sur internet) suffisent à transformer ton homelab en terrain de jeu pour bots.

Prends cinq minutes de plus pour créer un utilisateur applicatif dédié et planifier tes sauvegardes avec `mongodump`. Ton futur toi, le jour où un disque lâche, te remerciera. Et si tu construis une stack applicative complète autour, n'hésite pas à regarder comment d'autres services auto-hébergés comme [Transmission](/transmission-docker-client-torrent/) ou [Droppy](/droppy-partage-images-auto-heberge/) gèrent leur propre persistance à côté, ça donne des idées d'architecture pour organiser tes volumes Docker proprement.
