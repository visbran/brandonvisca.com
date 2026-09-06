---
title: "MariaDB Docker : base de données robuste pour tes services"
description: "Déploie MariaDB Docker en 10 minutes : stack complète, persistance des données, sauvegarde automatisée et optimisation pour ton homelab."
pubDatetime: "2026-08-07T08:00:00.000Z"
modDatetime: "2026-08-07T08:00:00.000Z"
author: Brandon
tags:
  - docker
  - mariadb
  - mysql
  - base-de-donnees
  - intermediaire
  - auto-hebergement
featured: false
draft: false
focusKeyword: mariadb docker
ogImage: "" 
---
> 💡 **TL;DR**
> - MariaDB est un fork open-source de MySQL, plus rapide et 100% compatible, idéal pour remplacer MySQL dans tes stacks Docker.
> - Une stack Compose minimaliste avec persistance des données, healthcheck et variables d'environnement sécurisées suffit à 90% des cas.
> - Configure des sauvegardes automatiques et des optimisations mémoire pour éviter les surprises en production.

## Table des matières

## Pourquoi MariaDB plutôt que MySQL ?

MySQL appartient à Oracle. MariaDB, c'est le fork communautaire créé par le fondateur original de MySQL après le rachat. Si tu veux rester dans l'écosystème open-source pur, le choix est vite fait.

Mais au-delà de la philosophie, MariaDB apporte des gains réels :

- **Performances** : le moteur Aria et l'optimiseur de requêtes sont plus agressifs que ceux de MySQL Community.
- **Compatibilité** : MariaDB est un drop-in replacement. Tu remplaces `mysql:8` par `mariadb:11`, et dans 99% des cas, ça marche sans toucher une ligne de code.
- **Licence** : GPL v2, pas de clauses propriétaires qui traînent.
- **Fonctionnalités** : JSON natif amélioré, galera cluster intégré, virtual columns, et une gestion des connexions plus légère.

Dans un environnement Docker, c'est particulièrement pertinent. Tu n'as pas besoin d'installer un client MySQL sur ton hôte, ni de gérer des dépendances système. Une image containerisée propre, un volume pour la persistance, et tu es opérationnel.

## Prérequis et architecture minimale

Avant de balancer un `docker-compose.yml`, vérifie que ton serveur tient la route :

- **1 cœur CPU** minimum (2 recommandés si tu as plusieurs services dessus).
- **1 Go de RAM** pour MariaDB seul, **2 Go** si tu empiles d'autres conteneurs comme [BookStack](/bookstack-docker-wiki-equipe/) ou [PhotoPrism](/photoprism-docker-galerie-photo/).
- **10 Go d'espace disque** pour la base + les logs et backups.
- Docker et Docker Compose installés. Si ce n'est pas encore fait, jette un œil à mon [guide Docker pour débutants](/docker-debutant-services-auto-heberger/) pour poser les bases proprement.

MariaDB, c'est une base de données relationnelle classique. Elle stocke les données dans `/var/lib/mysql`. Sans volume Docker, un `docker compose down` efface tout. C'est le premier piège à éviter.

## Stack Docker Compose complète

Voici une configuration production-ready, pas un POC bidon. Elle inclut :

- Une image MariaDB officielle stable (LTS).
- Un healthcheck pour que les services dépendants attendent que la base soit prête.
- Un réseau dédié isolé.
- Des variables d'environnement externes via un fichier `.env`.
- Un volume nommé pour la persistance.

Crée un dossier `mariadb-stack` et ajoute ce `docker-compose.yml` :

```yaml
version: "3.9"

services:
  mariadb:
    image: mariadb:11.4
    container_name: mariadb
    restart: unless-stopped
    env_file:
      - .env
    volumes:
      - mariadb_data:/var/lib/mysql
      - ./backup:/backup
      - ./conf/custom.cnf:/etc/mysql/conf.d/custom.cnf:ro
    networks:
      - db_network
    healthcheck:
      test: ["CMD", "healthcheck.sh", "--connect", "--innodb_initialized"]
      start_period: 10s
      interval: 10s
      timeout: 5s
      retries: 3

volumes:
  mariadb_data:

networks:
  db_network:
    driver: bridge
```

Et le fichier `.env` à côté :

```bash
MARIADB_ROOT_PASSWORD=ton-mot-de-passe-root-ultra-securise
MARIADB_DATABASE=app_database
MARIADB_USER=app_user
MARIADB_PASSWORD=un-autre-mot-de-passe-fort
TZ=Europe/Paris
```

**Points importants :**

- `restart: unless-stopped` : si le serveur redémarre, MariaDB remonte tout seul.
- `env_file` : évite d'écrire les mots de passe en clair dans le `docker-compose.yml`.
- Le healthcheck utilise le script interne `healthcheck.sh` de l'image officielle. Plus fiable qu'un `mysqladmin ping` maison.
- Le volume `./backup:/backup` te permet de déclencher des dumps depuis l'intérieur du conteneur ou de les copier facilement.

## Optimisation mémoire et performance

Par défaut, MariaDB Docker tourne avec une config ultra-conservative. Si tu as plus de 2 Go de RAM, tu vas vouloir ajuster quelques paramètres.

Crée le fichier `conf/custom.cnf` :

```ini
[mysqld]
# Mémoire
innodb_buffer_pool_size = 512M
innodb_log_file_size = 128M
innodb_flush_log_at_trx_commit = 2

# Connexions
max_connections = 100
wait_timeout = 600
interactive_timeout = 600

# Performance
query_cache_type = 1
query_cache_size = 64M
tmp_table_size = 64M
max_heap_table_size = 64M

# Logs
slow_query_log = 1
slow_query_log_file = /var/lib/mysql/slow.log
long_query_time = 2
```

**Explications :**

- `innodb_buffer_pool_size` : c'est le cache RAM pour les données et les index. Règle-la à environ 50-70% de la RAM totale du conteneur si MariaDB est seul. Avec 2 Go de RAM sur le serveur, 512M est un bon début.
- `innodb_flush_log_at_trx_commit = 2` : moins sûr que `1` (flush à chaque transaction), mais bien plus rapide. Acceptable pour un homelab.
- `query_cache_size` : met en cache les résultats de requêtes identiques. Utile si tu as des applis qui répètent les mêmes SELECT.

Monte ce fichier en read-only (`:ro`) dans le conteneur. Si tu vebles la config, tu modifies le fichier, puis `docker compose restart mariadb`.

## Sécuriser l'accès

MariaDB expose le port 3306. Même si tu es derrière un firewall, minimise la surface d'attaque.

### Pas de port exposé sur l'hôte

Si tes applications sont aussi en Docker sur le même réseau, **ne mappe pas le port 3306** sur l'hôte. Supprime cette ligne du `docker-compose.yml` :

```yaml
# PAS ÇA
ports:
  - "3306:3306"
```

Les autres conteneurs communiquent via le réseau interne `db_network`. Aucune raison d'exposer MySQL au monde extérieur, même en local.

Si tu dois absolument t'y connecter depuis l'extérieur (ex : DBeaver sur ton poste local), utilise un tunnel SSH via [Passkey et SSH](/passkey-ssh-sshid/) plutôt qu'un mapping de port brut. C'est plus sûr et ça évite d'ouvrir un port supplémentaire sur ton firewall.

### Utilisateurs dédiés par application

Jamais le root pour les applis. Le `docker-compose.yml` ci-dessus crée un utilisateur `app_user` limité à `app_database`. C'est l'utilisateur que tu passes à Nextcloud, Wallabag, ou tout autre service.

Si tu ajoutes un service supplémentaire plus tard, crée un nouvel utilisateur et une nouvelle base :

```bash
docker exec -it mariadb mariadb -u root -p

CREATE DATABASE nextcloud CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'nextcloud'@'%' IDENTIFIED BY 'mot-de-passe-fort';
GRANT ALL PRIVILEGES ON nextcloud.* TO 'nextcloud'@'%';
FLUSH PRIVILEGES;
EXIT;
```

Une base = un utilisateur = une surface d'attaque limitée.

## Sauvegarde automatisée

La persistance Docker, c'est bien. La sauvegarde externe, c'est mieux. Un volume corrompu, un RAID qui lâche, une fausse manip `docker volume rm`, bam, c'est fini.

### Script de dump quotidien

Crée `backup/backup-mariadb.sh` :

```bash
#!/bin/bash
set -euo pipefail

BACKUP_DIR="/backup"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=7

echo "[$(date)] Démarrage backup MariaDB..."

mysqldump -u root -p"${MARIADB_ROOT_PASSWORD}" --all-databases --single-transaction --routines --events \
  | gzip > "${BACKUP_DIR}/mariadb_backup_${DATE}.sql.gz"

echo "[$(date)] Backup terminé : mariadb_backup_${DATE}.sql.gz"

# Rotation : suppression des backups de plus de 7 jours
find "${BACKUP_DIR}" -name "mariadb_backup_*.sql.gz" -mtime +${RETENTION_DAYS} -delete

echo "[$(date)] Rotation terminée."
```

Rends-le exécutable :

```bash
chmod +x backup/backup-mariadb.sh
```

Puis exécute-le depuis le conteneur via un cron sur l'hôte :

```bash
# Sur l'hôte, édite le crontab de l'utilisateur docker
crontab -e

# Ajoute cette ligne pour un backup tous les jours à 3h du matin
0 3 * * * cd /chemin/vers/mariadb-stack && docker compose exec -T mariadb /backup/backup-mariadb.sh >> /var/log/mariadb-backup.log 2>&1
```

Le flag `-T` est important : il désactive le TTY, sinon cron plante. Le fichier de log te permet de surveiller les échecs.

### Restauration

Si tu dois restaurer une base spécifique :

```bash
# Copie le backup dans le conteneur
docker cp mariadb_backup_20260807_030000.sql.gz mariadb:/tmp/

# Restaure
docker exec -it mariadb bash -c "zcat /tmp/mariadb_backup_20260807_030000.sql.gz | mariadb -u root -p"
```

Teste ta restauration au moins une fois. Un backup non testé, c'est juste de l'espoir.

## Connexion et administration

### Depuis un autre conteneur

Un service comme [NocoDB](/nocodb-docker-airtable-alternative/) ou BookStack se connecte avec ces variables :

```yaml
environment:
  DB_HOST: mariadb
  DB_PORT: 3306
  DB_NAME: app_database
  DB_USER: app_user
  DB_PASSWORD: ${MARIADB_PASSWORD}
```

Le nom du service (`mariadb`) est résolu automatiquement par le DNS interne Docker.

### Depuis l'hôte

Si tu as besoin de jeter un œil depuis le terminal de l'hôte :

```bash
docker exec -it mariadb mariadb -u root -p
```

Pas besoin d'installer MySQL Client sur ton hôte. Tout passe par le conteneur.

### Interface web (optionnel)

Si tu préfères un GUI, [Adminer](https://www.adminer.org/) ou phpMyAdmin en Docker font le job. Pour Adminer, ajoute juste ça à ton `docker-compose.yml` :

```yaml
  adminer:
    image: adminer:latest
    container_name: adminer
    restart: unless-stopped
    ports:
      - "8080:8080"
    networks:
      - db_network
```

Accède via `http://IP:8080`, serveur = `mariadb`, et tes identifiants. Si tu utilises [Traefik](/traefik-reverse-proxy-docker/), mets-le derrière un sous-domaine avec HTTPS au lieu d'exposer le port 8080 brut.

## Mise à jour de MariaDB

Les mises à jour de base de données, c'est le moment où tu transpires. MariaDB 11.4 vers 11.5 ? Généralement sans souci. Mais d'une majeure à l'autre, la structure interne peut changer.

### Procédure sécurisée

1. **Dump complet** avant toute chose. Oui, c'est chiant. Oui, ça sauve des vies.
2. Lis les notes de release de l'image Docker officielle (`mariadb` sur Docker Hub).
3. Met à jour le tag dans le `docker-compose.yml` :
   ```yaml
   image: mariadb:11.5
   ```
4. Redéploie :
   ```bash
   docker compose pull
   docker compose up -d
   ```
5. Vérifie les logs :
   ```bash
   docker logs --tail 50 mariadb
   ```

Si tu utilises [Watchtower](/watchtower-mise-a-jour-docker-auto/), configure une politique de mise à jour conservative. Une base de données qui redémarre toute seule en pleine nuit sans backup préalable, c'est une mauvaise blague.

## Monitoring basique

Tu n'as pas besoin de [Zabbix](/zabbix-docker-monitoring-infrastructure/) pour surveiller une base MariaDB isolée. Quelques commandes simples suffisent.

### État du conteneur

```bash
docker compose ps
docker stats mariadb --no-stream
```

### Logs en temps réel

```bash
docker logs -f --tail 100 mariadb
```

### Métriques SQL rapides

```sql
-- Taille des bases
SELECT table_schema AS "Database", 
ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS "Size (MB)" 
FROM information_schema.tables 
GROUP BY table_schema;

-- Connexions actives
SHOW STATUS LIKE 'Threads_connected';

-- Requêtes lentes
SHOW GLOBAL STATUS LIKE 'Slow_queries';
```

### Healthcheck personnalisé

Si le healthcheck natif ne te suffit pas, tu peux en ajouter un second qui vérifie qu'une base spécifique est accessible :

```yaml
healthcheck:
  test: ["CMD", "mariadb", "-u", "app_user", "-p${MARIADB_PASSWORD}", "-D", "app_database", "-e", "SELECT 1"]
  interval: 30s
  timeout: 10s
  retries: 3
```

## Cas d'usage concrets dans ton homelab

MariaDB est le ciment de nombreuses applications auto-hébergées. Voici les stacks où je l'utilise régulièrement :

- **[BookStack](/bookstack-docker-wiki-equipe/)** : wiki d'équipe. MariaDB stocke les pages, les utilisateurs et les permissions.
- **[PhotoPrism](/photoprism-docker-galerie-photo/)** : galerie photo. MariaDB gère les métadonnées EXIF et les albums.
- **[NocoDB](/nocodb-docker-airtable-alternative/)** : interface spreadsheet sur ta base SQL. MariaDB est une des cibles supportées nativement.
- **Nextcloud** : cloud personnel. MariaDB ou PostgreSQL, au choix. MariaDB est souvent plus simple à configurer.
- **Wallabag** : lecteur d'articles offline.

L'avantage d'avoir une instance MariaDB centrale, c'est que tu partages les ressources. Pas besoin de lancer un PostgreSQL pour chaque appli. Un conteneur MariaDB bien tune, et tu branches tout dessus.

## Dépannage des erreurs courantes

### "Can't connect to local MySQL server through socket"

Tu essayes de te connecter depuis l'hôte avec `mysql` sans préciser l'hôte. Depuis l'hôte, utilise toujours `docker exec` pour entrer dans le conteneur. Ou connecte-toi en TCP si tu as exposé le port.

### "Access denied for user"

Vérifie que tu utilises le bon mot de passe et le bon hôte. Dans Docker, les utilisateurs sont souvent créés avec `'user'@'%'`, ce qui accepte n'importe quel hôte. Mais si tu as créé `'user'@'localhost'`, ça ne marchera pas depuis un autre conteneur.

### Le conteneur redémarre en boucle

```bash
docker logs mariadb
```

Causes fréquentes :
- Mauvais permissions sur le volume (`chown -R 999:999 mariadb_data` si besoin).
- Conflit de port 3306 déjà utilisé sur l'hôte (si tu as mappé le port).
- Base de données corrompue suite à un arrêt brutal. Lance un `mariadb-check --all-databases` depuis le conteneur.

### Lenteurs soudaines

Vérifie le slow query log (`/var/lib/mysql/slow.log` dans le conteneur). Ajoute des index si nécessaire. Si le conteneur manque de RAM, Linux va swapper et tout ralentir. Augmente `innodb_buffer_pool_size` ou ajoute de la RAM.

## Conclusion

MariaDB avec Docker, c'est pas sorcier. Une image stable, un volume persistant, un `.env` propre, et tu as une base de données relationnelle prête à servir tes applications auto-hébergées. La clé, c'est de ne pas négliger les bases : healthcheck, backup automatisé, et utilisateurs dédiés par service.

Si tu déploies plusieurs applis sur ton serveur, centraliser MariaDB est le choix le plus efficace. Moins de conteneurs, moins de ressources gaspillées, et une maintenance simplifiée. Ce n'est pas le setup le plus hype du monde, mais c'est celui qui fonctionne jour après jour sans te réveiller à 3h du matin.

Et si tu hésites entre MariaDB et PostgreSQL, j'ai aussi publié un guide complet sur [PostgreSQL avec Docker](/postgresql-docker-base-de-donnees/) avec healthcheck, sauvegarde et tuning.
