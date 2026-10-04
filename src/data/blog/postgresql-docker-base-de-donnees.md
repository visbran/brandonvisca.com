---
title: "PostgreSQL Docker : la base de données préférée des devs"
description: "Déploie PostgreSQL Docker en 10 minutes : stack complète avec persistance, healthcheck, sauvegarde automatisée et optimisation pour ton homelab."
pubDatetime: "2026-08-11T08:00:00.000Z"
modDatetime: "2026-10-04T00:00:00+02:00"
author: Brandon Visca
tags:
  - docker
  - base-de-donnees
  - intermediaire
  - auto-hebergement
featured: false
draft: false
focusKeyword: postgresql docker
ogImage: "" 
faqs:
  - question: "Faut-il exposer le port 5432 de PostgreSQL ?"
    answer: "Non si tes applications tournent en Docker sur le même réseau : elles joignent la base par son nom de service. Pour un client comme DBeaver sur ton poste, passe par un tunnel SSH."
  - question: "Comment sauvegarder PostgreSQL en Docker ?"
    answer: "Avec pg_dump pour une base, ou pg_dumpall pour toutes les bases du conteneur, lancé par un cron sur l'hôte via docker compose exec -T. Teste la restauration au moins une fois."
  - question: "Comment régler la mémoire de PostgreSQL ?"
    answer: "Le principal levier est shared_buffers, à environ 25 % de la RAM du serveur, avec effective_cache_size entre 50 et 75 %. Place ces réglages dans un fichier de configuration monté en lecture seule."
  - question: "Peut-on passer à une version majeure en changeant juste le tag de l'image ?"
    answer: "Non. Entre deux versions majeures, par exemple de 16 à 17, le format des fichiers de données change et le nouveau conteneur refuse de démarrer sur l'ancien volume. Il faut un dump complet, puis une restauration dans un volume neuf (ou pg_upgrade)."
---
> 💡 **TL;DR**
> - PostgreSQL est la base de données relationnelle open-source la plus avancée, avec un moteur ACID strict, le support JSON natif, et une fiabilité légendaire en production.
> - Une stack Docker Compose avec persistance des données, healthcheck et variables d'environnement externes suffit à lancer une instance production-ready en 5 minutes.
> - Configure des sauvegardes automatisées avec `pg_dump`, optimise la mémoire via `shared_buffers`, et isole chaque application dans sa propre base et son propre utilisateur.

## Table des matières

## Pourquoi PostgreSQL plutôt que MariaDB ou MySQL ?

MariaDB et MySQL dominent le web classique. Mais quand tu montes un homelab avec des applications modernes comme NocoDB, Outline, ou des outils devops, PostgreSQL devient souvent le choix par défaut. Ce n'est pas un hasard : c'est la base de données préférée des développeurs depuis des années, et ce n'est pas que de la hype.

Voici ce qui fait la différence en pratique :

- **Conformité SQL stricte** : PostgreSQL respecte les standards SQL plus que MariaDB/MySQL. Moins de surprises quand tu migres une requête d'un projet à un autre.
- **Types de données avancés** : tableaux, JSONB, UUID, range types, full-text search intégré. Tu peux stocker et interroger des documents JSON sans sortir de la base.
- **Fiabilité ACID** : les transactions sont véritablement atomiques, avec un contrôle de concurrence multiversion (MVCC) qui évite les locks inutiles.
- **Extensibilité** : PostGIS pour la géolocalisation, pg_trgm pour la recherche approximative, pgcrypto pour le chiffrement. Des extensions qui transforment PostgreSQL en une boîte à outils.
- **Licence** : PostgreSQL est sous licence PostgreSQL, proche de la MIT. Zéro restriction commerciale, zéro clause propriétaire.

Dans un environnement Docker, PostgreSQL brille particulièrement. L'image officielle `postgres` est légère, bien maintenue, et fournit `pg_isready` pour les healthchecks. Tu peux monter un conteneur en quelques minutes, brancher tes applis, et ne plus y penser. Si tu hésites encore entre [MariaDB et PostgreSQL](/mariadb-docker-base-de-donnees/), la règle simple est : applis web classiques = MariaDB, applis modernes, data complexe, ou devops = PostgreSQL.

## Prérequis et architecture minimale

Avant de balancer ton `docker-compose.yml`, assure-toi que ton serveur tient la route :

- **1 cœur CPU** minimum (2 recommandés si tu empiles d'autres conteneurs).
- **1 Go de RAM** pour PostgreSQL seul, **2 Go** si tu ajoutes des services comme BookStack ou NocoDB par-dessus.
- **10 Go d'espace disque** pour la base, les WAL (Write-Ahead Logs), et les backups.
- Docker et Docker Compose installés. Si ce n'est pas encore fait, commence par mon [guide Docker pour débutants](/docker-debutant-services-auto-heberger/) pour poser les bases.

Jusqu'à la version 17, PostgreSQL stocke ses données dans `/var/lib/postgresql/data`. Sans volume monté à cet endroit, elles disparaissent avec le conteneur. Et attention à `docker compose down -v` : l'option `-v` supprime aussi les volumes nommés. C'est le premier piège à éviter, et c'est aussi le plus commun.

## Stack Docker Compose complète

Voici une configuration production-ready, pas un POC bidon. Elle inclut :

- L'image PostgreSQL officielle en version 16 (chaque version majeure est maintenue cinq ans).
- Un healthcheck pour que les services dépendants attendent que la base soit prête.
- Un fichier de configuration personnalisé, réellement chargé au démarrage.
- Un réseau dédié isolé.
- Des variables d'environnement externes via un fichier `.env`.
- Un volume nommé pour la persistance.

Crée un dossier `postgres-stack` et ajoute ce `docker-compose.yml` :

```yaml
services:
  postgres:
    image: postgres:16-alpine
    container_name: postgres
    restart: unless-stopped
    command: postgres -c config_file=/etc/postgresql/postgresql.conf
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

Et le fichier `.env` à côté :

```bash
POSTGRES_USER=admin
POSTGRES_PASSWORD=un-mot-de-passe-ultra-fort-ici
POSTGRES_DB=app_database
TZ=Europe/Paris
```

**Points importants :**

- `POSTGRES_USER` crée le **super-utilisateur** de l'instance, avec tous les droits. Il remplace le rôle `postgres` par défaut : avec ce `.env`, `psql -U postgres` répond que le rôle n'existe pas. Réserve ce compte à l'administration et ne le donne jamais à une application (on crée des utilisateurs dédiés plus bas).
- `POSTGRES_USER`, `POSTGRES_PASSWORD` et `POSTGRES_DB` ne servent qu'au **premier démarrage**, quand le volume est vide. Les modifier ensuite dans `.env` ne change rien à une base déjà initialisée.
- `command` charge le fichier `postgres.conf` monté dans le conteneur. Sans cette ligne, le fichier est présent mais ignoré.
- `restart: unless-stopped` : si le serveur redémarre, PostgreSQL remonte tout seul.
- `env_file` : évite d'écrire les mots de passe en clair dans le `docker-compose.yml`.
- Le healthcheck utilise `pg_isready`, l'outil natif PostgreSQL. Il vérifie que le serveur accepte les connexions sur la base spécifiée, pas seulement qu'il a démarré.
- Le volume `./backup:/backup` permet de déclencher des dumps depuis l'intérieur du conteneur et de les retrouver directement sur l'hôte.

## Optimisation mémoire et performance

Par défaut, PostgreSQL tourne avec une configuration ultra-conservative. Si tu as plus de 2 Go de RAM sur ton serveur, tu vas vouloir ajuster quelques paramètres critiques.

Crée le fichier `conf/postgres.conf` :

```ini
# Réseau : indispensable avec un fichier de config personnalisé,
# sinon PostgreSQL n'écoute qu'en local et les autres conteneurs ne le joignent pas
listen_addresses = '*'

# Mémoire
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

# Logs : sur stderr, donc lisibles avec docker logs
log_destination = 'stderr'
log_min_duration_statement = 1000ms
```

**Explications :**

- `listen_addresses` : ce fichier remplace entièrement la configuration par défaut de l'image, qui écoute sur toutes les interfaces. Sans cette ligne, PostgreSQL n'accepte plus que les connexions locales au conteneur.
- `shared_buffers` : c'est le cache RAM pour les données et les index. Règle-le à environ 25 % de la RAM totale du serveur. Avec 1 Go de RAM, 256MB est un bon début.
- `effective_cache_size` : aide l'optimiseur de requêtes à estimer ce qui est déjà en cache. 50 à 75 % de la RAM totale est une bonne heuristique.
- `work_mem` : mémoire allouée par opération de tri ou de hachage. 16MB évite les écritures disque temporaires sur la plupart des requêtes.
- `max_wal_size` et `min_wal_size` : contrôlent la fréquence des checkpoints. Des valeurs plus élevées réduisent les pics d'I/O, au prix d'une reprise plus longue après un crash.
- `log_min_duration_statement` : journalise les requêtes de plus d'une seconde. C'est ton slow query log.

Le fichier est monté en lecture seule (`:ro`). Pour appliquer une modification, édite-le puis lance `docker compose restart postgres`.

## Sécuriser l'accès

PostgreSQL écoute sur le port 5432. Même derrière un firewall, minimise la surface d'attaque autant que possible.

### Pas de port exposé sur l'hôte

Si tes applications sont aussi en Docker sur le même réseau, **ne mappe pas le port 5432** sur l'hôte. Le `docker-compose.yml` ci-dessus n'en a pas, et c'est voulu. N'ajoute pas ça :

```yaml
# PAS ÇA
ports:
  - "5432:5432"
```

Les autres conteneurs communiquent via le réseau interne `db_network`. Aucune raison d'exposer PostgreSQL au monde extérieur, même en local.

Si tu dois absolument t'y connecter depuis l'extérieur (ex : DBeaver sur ton poste local), utilise un tunnel SSH plutôt qu'un mapping de port brut. C'est plus sûr et ça évite d'ouvrir un port supplémentaire sur ton firewall.

### Utilisateurs dédiés par application

Jamais le super-utilisateur pour les applis. Pour chaque service, crée un utilisateur et rends-le **propriétaire** de sa base :

```bash
docker exec -it postgres psql -U admin -d postgres
```

```sql
CREATE USER nextcloud WITH PASSWORD 'mot-de-passe-fort';
CREATE DATABASE nextcloud OWNER nextcloud;
\q
```

Pour la base `app_database` créée au premier démarrage, crée son utilisateur puis transfère-lui la propriété :

```sql
CREATE USER app_user WITH PASSWORD 'mot-de-passe-fort';
ALTER DATABASE app_database OWNER TO app_user;
```

Pourquoi `OWNER` plutôt qu'un `GRANT ALL PRIVILEGES ON DATABASE` ? Depuis PostgreSQL 15, ce `GRANT` ne donne plus le droit de créer des tables dans le schéma `public` : l'application se connecte, puis échoue à sa première migration. Le propriétaire de la base, lui, a ce droit.

Une base = un utilisateur = une surface d'attaque limitée. C'est la règle d'or.

## Sauvegarde automatisée

La persistance Docker, c'est bien. La sauvegarde externe, c'est mieux. Un volume corrompu, un RAID qui lâche, une fausse manip `docker volume rm`, et c'est fini.

### Script de dump quotidien

Crée `backup/backup-postgres.sh` :

```bash
#!/bin/sh
set -eu

BACKUP_DIR="/backup"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=7

echo "[$(date)] Démarrage backup PostgreSQL..."

pg_dump -U "${POSTGRES_USER}" -d "${POSTGRES_DB}" -Fc \
  > "${BACKUP_DIR}/postgres_backup_${DATE}.dump"

echo "[$(date)] Backup terminé : postgres_backup_${DATE}.dump"

# Rotation : suppression des backups de plus de 7 jours
find "${BACKUP_DIR}" -name "postgres_backup_*.dump" -mtime +${RETENTION_DAYS} -delete

echo "[$(date)] Rotation terminée."
```

Le script tourne avec `sh` : l'image Alpine n'embarque pas `bash`. Rends-le exécutable :

```bash
chmod +x backup/backup-postgres.sh
```

Puis exécute-le dans le conteneur via un cron sur l'hôte :

```bash
# Sur l'hôte, édite le crontab
crontab -e

# Ajoute cette ligne pour un backup tous les jours à 3h du matin
0 3 * * * cd /chemin/vers/postgres-stack && docker compose exec -T postgres /backup/backup-postgres.sh >> /var/log/postgres-backup.log 2>&1
```

Le flag `-T` est essentiel : il désactive le TTY, sinon la commande échoue sous cron. Le fichier de log te permet de surveiller les échecs silencieux.

### Sauvegarde globale avec pg_dumpall

Si tu gères plusieurs bases dans le même conteneur, utilise `pg_dumpall` pour tout capturer d'un coup, rôles compris :

```bash
docker exec postgres pg_dumpall -U admin | gzip > backup/postgres_all_$(date +%Y%m%d).sql.gz
```

Pas de `-it` ici : avec un TTY, Docker ajoute des retours chariot dans la sortie et le dump compressé devient inutilisable.

### Restauration

Si tu dois restaurer une base spécifique depuis un dump du script (il est déjà dans le dossier `backup`, monté sur `/backup`) :

```bash
docker exec -it postgres pg_restore -U admin -d app_database --clean --if-exists /backup/postgres_backup_20260811_030000.dump
```

Teste ta restauration au moins une fois. Un backup non testé, c'est juste de l'espoir.

## Connexion et administration

### Depuis un autre conteneur

Un service comme NocoDB ou BookStack se connecte avec l'utilisateur dédié, jamais avec le super-utilisateur :

```yaml
environment:
  DB_HOST: postgres
  DB_PORT: 5432
  DB_NAME: app_database
  DB_USER: app_user
  DB_PASSWORD: ${APP_DB_PASSWORD}
```

Le nom du service (`postgres`) est résolu automatiquement par le DNS interne Docker. Pas besoin d'IP, pas besoin de port exposé. Le conteneur de l'application doit simplement rejoindre le réseau `db_network`.

### Depuis l'hôte

Si tu as besoin de jeter un œil depuis le terminal de l'hôte :

```bash
docker exec -it postgres psql -U admin -d app_database
```

Pas besoin d'installer le client PostgreSQL sur ton hôte. Tout passe par le conteneur.

### Commandes psql pratiques

Voici les commandes que tu utiliseras au quotidien :

```sql
-- Lister les bases
\l

-- Se connecter à une base
\c app_database

-- Lister les tables
\dt

-- Décrire une table
\d nom_table

-- Voir les connexions actives
SELECT * FROM pg_stat_activity;

-- Taille des bases
SELECT pg_database.datname, pg_size_pretty(pg_database_size(pg_database.datname)) AS size FROM pg_database;

-- Quitter
\q
```

### Interface web (optionnel)

Si tu préfères un GUI, [pgAdmin](https://www.pgadmin.org/) ou Adminer en Docker font le job. Pour pgAdmin, ajoute juste ça à ton `docker-compose.yml` :

```yaml
  pgadmin:
    image: dpage/pgadmin4:latest
    container_name: pgadmin
    restart: unless-stopped
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@localhost.local
      PGADMIN_DEFAULT_PASSWORD: change-moi
    ports:
      - "5050:80"
    networks:
      - db_network
```

Accède via `http://IP:5050`. Si tu utilises un reverse proxy, mets-le derrière un sous-domaine avec HTTPS au lieu d'exposer le port 5050 brut.

## Mise à jour de PostgreSQL

Les mises à jour de base de données, c'est le moment où tu transpires. Il y a deux cas très différents.

### Version mineure (16.x vers 16.y)

Aucun risque pour les données : le format des fichiers ne change pas au sein d'une version majeure. Le tag `16-alpine` suit déjà la dernière version mineure, un simple pull suffit :

```bash
docker compose pull
docker compose up -d
docker logs --tail 50 postgres
```

### Version majeure (16 vers 17 ou au-delà)

Là, **changer le tag ne suffit pas**. Le format des fichiers de données change d'une version majeure à l'autre : un conteneur `postgres:17` refuse de démarrer sur un volume initialisé en 16. Il faut exporter les données, puis les réimporter dans un volume neuf.

1. **Dump complet** avec l'ancienne version, rôles compris :
   ```bash
   docker exec postgres pg_dumpall -U admin > backup/upgrade_$(date +%Y%m%d).sql
   ```
2. **Arrête la stack sans supprimer le volume** (pas de `-v`) :
   ```bash
   docker compose down
   ```
3. **Pointe vers un nouveau volume et la nouvelle image.** Dans le `docker-compose.yml`, remplace `postgres_data` par un nouveau nom (par exemple `postgres_data_17`), dans le service comme dans la section `volumes`, puis change le tag :
   ```yaml
   image: postgres:17-alpine
   ```
   À partir de **PostgreSQL 18**, l'image range ses données sous `/var/lib/postgresql/18/docker` : monte alors le volume sur `/var/lib/postgresql` et non plus sur `/var/lib/postgresql/data`.
4. **Démarre** : la nouvelle instance s'initialise à vide avec ton `.env`.
   ```bash
   docker compose up -d
   ```
5. **Réimporte le dump** une fois le conteneur `healthy` :
   ```bash
   docker exec -i postgres psql -U admin -d postgres < backup/upgrade_20260811.sql
   ```
   Des erreurs du type « role admin already exists » sont normales : ces objets ont déjà été créés par l'initialisation.
6. **Vérifie** tes bases et tes applications. Garde l'ancien volume quelques jours avant de le supprimer avec `docker volume rm`.

Pour les grosses bases, `pg_upgrade` évite l'export complet, mais il demande les binaires des deux versions dans le même conteneur : le dump et la restauration restent la méthode la plus simple en Docker.

Si tu utilises Watchtower, exclus le conteneur PostgreSQL ou épingle sa version majeure. Une base de données qui redémarre toute seule en pleine nuit sans backup préalable, c'est une mauvaise blague.

## Monitoring basique

Tu n'as pas besoin de Zabbix pour surveiller une base PostgreSQL isolée. Quelques commandes simples suffisent.

### État du conteneur

```bash
docker compose ps
docker stats postgres --no-stream
```

### Logs en temps réel

```bash
docker logs -f --tail 100 postgres
```

### Métriques SQL rapides

```sql
-- Connexions actives
SELECT count(*) FROM pg_stat_activity WHERE state = 'active';

-- Requêtes lentes (> 1 seconde)
SELECT * FROM pg_stat_activity WHERE state = 'active' AND now() - query_start > interval '1 second';

-- Taille des tables (top 10)
SELECT schemaname, relname, pg_size_pretty(pg_total_relation_size(relid))
FROM pg_stat_user_tables
ORDER BY pg_total_relation_size(relid) DESC
LIMIT 10;
```

### Healthcheck personnalisé

Si le healthcheck natif ne te suffit pas, tu peux le remplacer par une vraie requête sur la base de l'application :

```yaml
healthcheck:
  test: ["CMD-SHELL", "psql -U app_user -d app_database -c 'SELECT 1' || exit 1"]
  interval: 30s
  timeout: 10s
  retries: 3
```

## Cas d'usage concrets dans ton homelab

PostgreSQL est le ciment de nombreuses applications auto-hébergées modernes. Voici les stacks où je l'utilise régulièrement :

- **NocoDB** : interface spreadsheet sur ta base SQL. PostgreSQL est une des cibles supportées nativement et c'est souvent le choix recommandé pour la robustesse.
- **Outline** : wiki moderne auto-hébergé. Outline exige PostgreSQL et Redis.
- **BookStack** : wiki d'équipe. BookStack supporte MariaDB et PostgreSQL. Si tu cherches une expérience plus stricte avec les données, PostgreSQL est préférable.
- **Wallabag** : lecteur d'articles offline. PostgreSQL est le choix par défaut dans la documentation officielle.
- **Authentik** : fournisseur d'identité open-source. PostgreSQL est obligatoire pour stocker les utilisateurs et les policies.

L'avantage d'avoir une instance PostgreSQL centrale, c'est que tu partages les ressources. Pas besoin de lancer un conteneur de base de données pour chaque appli. Un conteneur PostgreSQL bien configuré, et tu branches tout dessus.

## Dépannage des erreurs courantes

### "Connection refused" ou "could not connect to server"

Le conteneur n'est pas encore prêt : attends quelques secondes après le `docker compose up -d` et regarde `docker logs postgres`. Si ça persiste et que seuls les autres conteneurs échouent, vérifie `listen_addresses = '*'` dans `postgres.conf` et que l'application est bien sur le réseau `db_network`.

### "password authentication failed"

Le mot de passe de `.env` ne correspond pas à celui de la base. Ces variables ne sont lues qu'au premier démarrage : changer `POSTGRES_PASSWORD` après coup n'a aucun effet. Modifie le mot de passe dans la base avec `ALTER USER admin WITH PASSWORD '...';`, ou recrée le volume si l'instance est encore vide.

### "role does not exist"

Tu te connectes avec un utilisateur qui n'existe pas. Avec ce `.env`, le super-utilisateur s'appelle `admin` et le rôle `postgres` n'existe pas. Pour les utilisateurs d'application, vérifie que tu les as bien créés avec `CREATE USER`.

### Le conteneur redémarre en boucle

```bash
docker logs postgres
```

Causes fréquentes :
- Un volume initialisé avec une autre version majeure : le message parle de fichiers de données incompatibles. Voir la section mise à jour.
- Une erreur dans `postgres.conf` : le log indique la ligne en cause.
- Mauvaises permissions sur un dossier monté depuis l'hôte : il doit appartenir à l'utilisateur `postgres` du conteneur, UID 70 sur l'image Alpine (999 sur l'image Debian).
- Données corrompues suite à un arrêt brutal : restaure le dernier dump.

### Lenteurs soudaines

Regarde les requêtes journalisées par `log_min_duration_statement` dans `docker logs`, et ajoute des index si nécessaire. Si le conteneur manque de RAM, Linux va swapper et tout ralentir : réduis `shared_buffers` ou ajoute de la RAM au serveur.

💡 À lire aussi : [Redis Docker : déployer une base de données clé-valeur ultra-rapide](/redis-docker-base-donnees-cle-valeur/), dans la même veine que cet article.

## Conclusion

PostgreSQL avec Docker, c'est pas sorcier. Une image stable, un volume persistant, un `.env` propre, et tu as la base de données relationnelle la plus fiable du monde open-source prête à servir tes applications auto-hébergées. La clé, c'est de ne pas négliger les bases : healthcheck, backup automatisé, et utilisateurs dédiés par service.

Si tu déploies plusieurs applis sur ton serveur, centraliser PostgreSQL est le choix le plus efficace. Moins de conteneurs, moins de ressources gaspillées, et une maintenance simplifiée. Ce n'est pas le setup le plus hype du monde, mais c'est celui qui fonctionne jour après jour sans te réveiller à 3h du matin.
