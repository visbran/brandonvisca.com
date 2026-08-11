---
title: "PostgreSQL Docker : la base de données préférée des devs"
description: "Déploie PostgreSQL Docker en 10 minutes : stack complète avec persistance, healthcheck, sauvegarde automatisée et optimisation pour ton homelab."
pubDatetime: "2026-08-11T08:00:00.000Z"
modDatetime: "2026-08-11T08:00:00.000Z"
author: Brandon Visca
tags:
  - docker
  - postgresql
  - base-de-donnees
  - intermediaire
  - auto-hebergement
featured: false
draft: false
focusKeyword: postgresql docker
ogImage: "" 
---
> **TL;DR**
> - PostgreSQL est la base de données relationnelle open-source la plus avancée, avec un moteur ACID strict, le support JSON natif, et une fiabilité légendaire en production.
> - Une stack Docker Compose avec persistance des données, healthcheck et variables d'environnement externes suffit a lancer une instance production-ready en 5 minutes.
> - Configure des sauvegardes automatisees avec `pg_dump`, optimise la memoire via `shared_buffers`, et isole chaque application dans sa propre base et son propre utilisateur.

## Pourquoi PostgreSQL plutot que MariaDB ou MySQL ?

MariaDB et MySQL dominent le web classique. Mais quand tu montes un homelab avec des applications modernes comme NocoDB, Outline, ou des outils devops, PostgreSQL devient souvent le choix par defaut. Ce n'est pas un hasard : c'est la base de donnees preferee des developpeurs depuis des annees, et ce n'est pas que de la hype.

Voici ce qui fait la difference en pratique :

- **Conformite SQL stricte** : PostgreSQL respecte les standards SQL plus que MariaDB/MySQL. Moins de surprises quand tu migrer une requete d'un projet a un autre.
- **Types de donnees avances** : tableaux, JSONB, UUID, range types, full-text search integre. Tu peux stocker et interroger des documents JSON sans sortir de la base.
- **Fiabilite ACID** : les transactions sont veritablement atomiques, avec un controle de concurrence multiversion (MVCC) qui evite les locks inutiles.
- **Extensibilite** : PostGIS pour la geolocalisation, pg_trgm pour la recherche approximative, pgcrypto pour le chiffrement. Des extensions qui transforment PostgreSQL en une boite a outils.
- **Licence** : PostgreSQL est sous licence MIT-like (PostgreSQL License). Zero restriction commerciale, zero clause proprietaire.

Dans un environnement Docker, PostgreSQL brille particulierement. L'image officielle `postgres` est legere, bien maintenue, et expose un healthcheck natif. Tu peux monter un conteneur en quelques minutes, brancher tes applis, et ne plus y penser. Si tu hesites encore entre [MariaDB et PostgreSQL](/mariadb-docker-base-de-donnees/), la regle simple est : applis web classiques = MariaDB, applis modernes, data complexe, ou devops = PostgreSQL.

## Prerequis et architecture minimale

Avant de balancer ton `docker-compose.yml`, assure-toi que ton serveur tient la route :

- **1 coeur CPU** minimum (2 recommandes si tu empiles d'autres conteneurs).
- **1 Go de RAM** pour PostgreSQL seul, **2 Go** si tu ajoutes des services comme BookStack ou NocoDB par-dessus.
- **10 Go d'espace disque** pour la base, les WAL (Write-Ahead Logs), et les backups.
- Docker et Docker Compose installes. Si ce n'est pas encore fait, commence par mon [guide Docker pour debutants](/docker-debutant-services-auto-heberger/) pour poser les bases.

PostgreSQL stocke ses donnees dans `/var/lib/postgresql/data`. Sans volume Docker, un `docker compose down -v` efface tout. C'est le premier piege a eviter, et c'est aussi le plus commun.

## Stack Docker Compose complete

Voici une configuration production-ready, pas un POC bidon. Elle inclut :

- L'image PostgreSQL officielle stable (version 16 LTS).
- Un healthcheck natif pour que les services dependants attendent que la base soit prete.
- Un reseau dedie isole.
- Des variables d'environnement externes via un fichier `.env`.
- Un volume nomme pour la persistance.

Cree un dossier `postgres-stack` et ajoute ce `docker-compose.yml` :

```yaml
version: "3.9"

services:
  postgres:
    image: postgres:16-alpine
    container_name: postgres
    restart: unless-stopped
    env_file:
      - .env
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backup:/backup
      - ./conf/postgres.conf:/etc/postgresql/postgresql.conf:ro
    networks:
      - db_network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U $${POSTGRES_USER} -d $${POSTGRES_DB}"]
      start_period: 10s
      interval: 10s
      timeout: 5s
      retries: 3

volumes:
  postgres_data:

networks:
  db_network:
    driver: bridge
```

Et le fichier `.env` a cote :

```bash
POSTGRES_DB=app_database
POSTGRES_USER=app_user
POSTGRES_PASSWORD=un-mot-de-passe-ultra-fort-ici
PGDATA=/var/lib/postgresql/data
TZ=Europe/Paris
```

**Points importants :**

- `restart: unless-stopped` : si le serveur redemarre, PostgreSQL remonte tout seul.
- `env_file` : evite d'ecrire les mots de passe en clair dans le `docker-compose.yml`.
- Le healthcheck utilise `pg_isready`, l'outil natif PostgreSQL. Il verifie que le serveur accepte les connexions sur la base specifiee, pas seulement qu'il a demarre.
- Le volume `./backup:/backup` permet de declencher des dumps depuis l'interieur du conteneur ou de les copier facilement vers l'hote.
- `PGDATA` force le repertoire des donnees. Pratique si tu veux verifier rapidement ou PostgreSQL ecrit.

## Optimisation memoire et performance

Par defaut, PostgreSQL Docker tourne avec une configuration ultra-conservative. Si tu as plus de 2 Go de RAM sur ton serveur, tu vas vouloir ajuster quelques parametres critiques.

Cree le fichier `conf/postgres.conf` :

```ini
# Memoire
shared_buffers = 256MB
effective_cache_size = 768MB
work_mem = 16MB
maintenance_work_mem = 128MB

# WAL et checkpoint
wal_buffers = 16MB
checkpoint_completion_target = 0.9
max_wal_size = 2GB
min_wal_size = 512MB

# Connexions
max_connections = 100

# Logging
log_destination = 'stderr'
logging_collector = on
log_directory = '/var/log/postgresql'
log_filename = 'postgresql-%Y-%m-%d.log'
log_min_duration_statement = 1000ms
```

**Explications :**

- `shared_buffers` : c'est le cache RAM pour les donnees et les index. Regle-la a environ 25% de la RAM totale du serveur. Avec 2 Go de RAM, 256MB est un bon debut.
- `effective_cache_size` : aide l'optimiseur de requetes a estimer ce qui est deja en cache. 50-75% de la RAM totale est une bonne heuristique.
- `work_mem` : memoire allouee par operation de tri ou de hachage. 16MB evite les ecritures disque temporaires sur la plupart des requetes.
- `max_wal_size` et `min_wal_size` : controlent la frequence des checkpoints. Des valeurs plus elevees reduisent les pics d'I/O au prix d'un leger risque en cas de crash.

Monte ce fichier en read-only (`:ro`) dans le conteneur. Modifie le fichier, puis `docker compose restart postgres` pour appliquer.

## Securiser l'acces

PostgreSQL expose le port 5432. Meme derriere un firewall, minimise la surface d'attaque autant que possible.

### Pas de port expose sur l'hote

Si tes applications sont aussi en Docker sur le meme reseau, **ne mappe pas le port 5432** sur l'hote. Supprime cette ligne du `docker-compose.yml` :

```yaml
# PAS CA
ports:
  - "5432:5432"
```

Les autres conteneurs communiquent via le reseau interne `db_network`. Aucune raison d'exposer PostgreSQL au monde exterieur, meme en local.

Si tu dois absolument t'y connecter depuis l'exterieur (ex : DBeaver sur ton poste local), utilise un tunnel SSH plutot qu'un mapping de port brut. C'est plus sur et ca evite d'ouvrir un port supplementaire sur ton firewall.

### Utilisateurs dedies par application

Jamais le super-utilisateur `postgres` pour les applis. Le `docker-compose.yml` ci-dessus cree un utilisateur `app_user` limite a `app_database`. C'est l'utilisateur que tu passes a Nextcloud, Wallabag, ou tout autre service.

Si tu ajoutes un service supplementaire plus tard, connecte-toi au conteneur et cree un nouvel utilisateur et une nouvelle base :

```bash
docker exec -it postgres psql -U postgres

CREATE DATABASE nextcloud WITH ENCODING 'UTF8' LC_COLLATE='en_US.utf8' LC_CTYPE='en_US.utf8' TEMPLATE=template0;
CREATE USER nextcloud WITH ENCRYPTED PASSWORD 'mot-de-passe-fort';
GRANT ALL PRIVILEGES ON DATABASE nextcloud TO nextcloud;
\q
```

Une base = un utilisateur = une surface d'attaque limitee. C'est la regle d'or.

## Sauvegarde automatisee

La persistance Docker, c'est bien. La sauvegarde externe, c'est mieux. Un volume corrompu, un RAID qui lache, une fausse manip `docker volume rm`, et c'est fini.

### Script de dump quotidien

Cree `backup/backup-postgres.sh` :

```bash
#!/bin/bash
set -euo pipefail

BACKUP_DIR="/backup"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=7

echo "[$(date)] Demarrage backup PostgreSQL..."

pg_dump -U "${POSTGRES_USER}" -d "${POSTGRES_DB}" -Fc \
  > "${BACKUP_DIR}/postgres_backup_${DATE}.dump"

echo "[$(date)] Backup termine : postgres_backup_${DATE}.dump"

# Rotation : suppression des backups de plus de 7 jours
find "${BACKUP_DIR}" -name "postgres_backup_*.dump" -mtime +${RETENTION_DAYS} -delete

echo "[$(date)] Rotation terminee."
```

Rends-le executable :

```bash
chmod +x backup/backup-postgres.sh
```

Puis execute-le depuis le conteneur via un cron sur l'hote :

```bash
# Sur l'hote, edite le crontab
crontab -e

# Ajoute cette ligne pour un backup tous les jours a 3h du matin
0 3 * * * cd /chemin/vers/postgres-stack && docker compose exec -T postgres /backup/backup-postgres.sh >> /var/log/postgres-backup.log 2>&1
```

Le flag `-T` est essentiel : il desactive le TTY, sinon cron plante. Le fichier de log te permet de surveiller les echecs silencieux.

### Sauvegarde globale avec pg_dumpall

Si tu geres plusieurs bases dans le meme conteneur, utilise `pg_dumpall` pour tout capturer d'un coup :

```bash
docker exec -it postgres pg_dumpall -U postgres | gzip > backup/postgres_all_$(date +%Y%m%d).sql.gz
```

### Restauration

Si tu dois restaurer une base specifique :

```bash
# Copie le backup dans le conteneur
docker cp postgres_backup_20260811_030000.dump postgres:/tmp/

# Restaure
docker exec -it postgres pg_restore -U app_user -d app_database --clean --if-exists /tmp/postgres_backup_20260811_030000.dump
```

Teste ta restauration au moins une fois. Un backup non teste, c'est juste de l'espoir.

## Connexion et administration

### Depuis un autre conteneur

Un service comme NocoDB ou BookStack se connecte avec ces variables :

```yaml
environment:
  DB_HOST: postgres
  DB_PORT: 5432
  DB_NAME: app_database
  DB_USER: app_user
  DB_PASSWORD: ${POSTGRES_PASSWORD}
```

Le nom du service (`postgres`) est resolu automatiquement par le DNS interne Docker. Pas besoin d'IP, pas besoin de port expose.

### Depuis l'hote

Si tu as besoin de jeter un oeil depuis le terminal de l'hote :

```bash
docker exec -it postgres psql -U app_user -d app_database
```

Pas besoin d'installer PostgreSQL Client sur ton hote. Tout passe par le conteneur.

### Commandes psql pratiques

Voici les commandes que tu utiliseras au quotidien :

```sql
-- Lister les bases
\l

-- Se connecter a une base
\c app_database

-- Lister les tables
\dt

-- Decrire une table
\d nom_table

-- Voir les connexions actives
SELECT * FROM pg_stat_activity;

-- Taille des bases
SELECT pg_database.datname, pg_size_pretty(pg_database_size(pg_database.datname)) AS size FROM pg_database;

-- Quitter
\q
```

### Interface web (optionnel)

Si tu preferes un GUI, [pgAdmin](https://www.pgadmin.org/) ou Adminer en Docker font le job. Pour pgAdmin, ajoute juste ca a ton `docker-compose.yml` :

```yaml
  pgadmin:
    image: dpage/pgadmin4:latest
    container_name: pgadmin
    restart: unless-stopped
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@localhost.local
      PGADMIN_DEFAULT_PASSWORD: admin123
    ports:
      - "5050:80"
    networks:
      - db_network
```

Accede via `http://IP:5050`. Si tu utilises un reverse proxy, mets-le derriere un sous-domaine avec HTTPS au lieu d'exposer le port 5050 brut.

## Mise a jour de PostgreSQL

Les mises a jour de base de donnees, c'est le moment ou tu transpires. PostgreSQL 16 vers 16.1 ? Gossellement sans souci. Mais d'une version majeure a l'autre (16 vers 17), le format des donnees binaires peut changer.

### Procedure securisee

1. **Dump complet** avant toute chose. Oui, c'est chiant. Oui, ca sauve des vies.
2. Lis les notes de release de l'image Docker officielle (`postgres` sur Docker Hub).
3. Met a jour le tag dans le `docker-compose.yml` :
   ```yaml
   image: postgres:17-alpine
   ```
4. Redeploie :
   ```bash
   docker compose pull
   docker compose up -d
   ```
5. Verifie les logs :
   ```bash
   docker logs --tail 50 postgres
   ```

Si tu utilises Watchtower, configure une politique de mise a jour conservative. Une base de donnees qui redemarre toute seule en pleine nuit sans backup prealable, c'est une mauvaise blague.

## Monitoring basique

Tu n'as pas besoin de Zabbix pour surveiller une base PostgreSQL isolee. Quelques commandes simples suffisent.

### Etat du conteneur

```bash
docker compose ps
docker stats postgres --no-stream
```

### Logs en temps reel

```bash
docker logs -f --tail 100 postgres
```

### Metriques SQL rapides

```sql
-- Connexions actives
SELECT count(*) FROM pg_stat_activity WHERE state = 'active';

-- Requetes lentes (> 1 seconde)
SELECT * FROM pg_stat_activity WHERE state = 'active' AND now() - query_start > interval '1 second';

-- Taille des tables (top 10)
SELECT schemaname, relname, pg_size_pretty(pg_total_relation_size(relid))
FROM pg_stat_user_tables
ORDER BY pg_total_relation_size(relid) DESC
LIMIT 10;
```

### Healthcheck personnalise

Si le healthcheck natif ne te suffit pas, tu peux en ajouter un second qui verifie qu'une table specifique est accessible :

```yaml
healthcheck:
  test: ["CMD-SHELL", "psql -U app_user -d app_database -c 'SELECT 1' || exit 1"]
  interval: 30s
  timeout: 10s
  retries: 3
```

## Cas d'usage concrets dans ton homelab

PostgreSQL est le ciment de nombreuses applications auto-hebergees modernes. Voici les stacks ou je l'utilise regulierement :

- **NocoDB** : interface spreadsheet sur ta base SQL. PostgreSQL est une des cibles supportees nativement et c'est souvent le choix recommande pour la robustesse.
- **Outline** : wiki moderne auto-heberge. Outline exige PostgreSQL et Redis.
- **BookStack** : wiki d'equipe. BookStack supporte MariaDB et PostgreSQL. Si tu cherches une experience plus stricte avec les donnees, PostgreSQL est preferable.
- **Wallabag** : lecteur d'articles offline. PostgreSQL est le choix par defaut dans la documentation officielle.
- **Authentik** : fournisseur d'identite open-source. PostgreSQL est obligatoire pour stocker les utilisateurs et les policies.

L'avantage d'avoir une instance PostgreSQL centrale, c'est que tu partages les ressources. Pas besoin de lancer un conteneur de base de donnees pour chaque appli. Un conteneur PostgreSQL bien configure, et tu branches tout dessus.

## Depannage des erreurs courantes

### "Connection refused" ou "could not connect to server"

Le conteneur n'est pas encore pret. Attends quelques secondes apres le `docker compose up -d`. Si ca persiste, verifie les logs avec `docker logs postgres`. Causes frequentes : mauvais `POSTGRES_PASSWORD` a l'init (changer le mot de passe dans `.env` apres le premier demarrage ne suffit pas, il faut recreer le volume), ou conflit de port si tu as expose 5432 sur l'hote.

### "role does not exist"

Tu essaies de te connecter avec un utilisateur qui n'existe pas. Verifie que tu as bien cree l'utilisateur avec `CREATE USER`, ou que le `.env` correspond au premier demarrage. PostgreSQL initialise la base au premier lancement uniquement.

### Le conteneur redemarre en boucle

```bash
docker logs postgres
```

Causes frequentes :
- Mauvaises permissions sur le volume (`chown -R 999:999 postgres_data` si besoin, car PostgreSQL tourne sous l'UID 999).
- Conflit de port 5432 deja utilise sur l'hote (si tu as mappe le port).
- Donnees corrompues suite a un arret brutal. Verifie les logs et force un recovery si necessaire.

### Lenteurs soudaines

Verifie le slow query log. Ajoute des index si necessaire. Si le conteneur manque de RAM, Linux va swapper et tout ralentir. Augmente `shared_buffers` ou ajoute de la RAM au serveur.

## Conclusion

PostgreSQL avec Docker, c'est pas sorcier. Une image stable, un volume persistant, un `.env` propre, et tu as la base de donnees relationnelle la plus fiable du monde open-source prete a servir tes applications auto-hebergees. La cle, c'est de ne pas negliger les bases : healthcheck, backup automatise, et utilisateurs dedies par service.

Si tu deployes plusieurs applis sur ton serveur, centraliser PostgreSQL est le choix le plus efficace. Moins de conteneurs, moins de ressources gaspillees, et une maintenance simplifiee. Ce n'est pas le setup le plus hype du monde, mais c'est celui qui fonctionne jour apres jour sans te reveiller a 3h du matin.
