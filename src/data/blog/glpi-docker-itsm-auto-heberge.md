---
title: "GLPI Docker : ITSM complet auto-hébergé"
description: "Déploie GLPI avec Docker : tutoriel complet pour monter un ITSM auto-hébergé avec inventaire, helpdesk et ticketing en 20 minutes."
pubDatetime: "2026-06-27T08:00:00.000Z"
modDatetime: "2026-06-27T08:00:00.000Z"
author: Brandon Visca
tags:
  - intermediaire
  - auto-hebergement
  - docker
  - linux
  - glpi
featured: false
draft: false
focusKeyword: glpi docker
ogImage: ""
---
## Qu'est-ce que GLPI et pourquoi le dockeriser ?

GLPI, c'est le couteau suisse de l'ITSM open source. Inventaire de parc, helpdesk, gestion des tickets, suivi des licences, base de connaissances, réservations de matériel… tout y passe. C'est la solution française qui tourne depuis 2003 et qui refuse de mourir, malgré des interfaces qui piquent parfois les yeux.

Le problème avec GLPI, c'est son installation classique. Un serveur LAMP à configurer, des extensions PHP à activer, des droits de fichiers à régler, une base MySQL à créer à la main… Bref, une après-midi de perdue si tout se passe bien. Avec Docker, tu compresses ça en un docker-compose.yml de 40 lignes et un `docker compose up -d`. Vingt minutes plus tard, ton ITSM tourne.

Avant de choisir, j'ai comparé GLPI et Snipe-IT en détail dans [mon comparatif ITSM](/snipeit-vs-glpi-comparatif-itsm-inventaire-it/). Si tu hésites encore, lis ça d'abord.

## Prérequis

Tu vas avoir besoin de peu de choses :

- Une machine avec **Docker et Docker Compose** installés. Si ce n'est pas encore le cas, commence par [mon guide Docker pour débutants](/docker-debutant-services-auto-heberger/).
- **2 Go de RAM minimum** pour faire tourner GLPI + MariaDB sans que ça rame. 4 Go, c'est mieux.
- Un **nom de domaine ou une IP fixe** si tu veux y accéder depuis l'extérieur. En local, `localhost:8080` suffit.
- Quinze minutes devant toi.

GLPI est gourmand en ressources comparé à un simple wiki. MariaDB + PHP-Apache + les volumes, ça consomme. Ne tente pas ça sur un Raspberry Pi Zero.

## Docker Compose complet

Crée un dossier `glpi` et un fichier `docker-compose.yml` à l'intérieur :

```yaml
services:
  mariadb:
    image: mariadb:10.11
    container_name: glpi-mariadb
    restart: unless-stopped
    environment:
      MYSQL_ROOT_PASSWORD: changeme_root
      MYSQL_DATABASE: glpi
      MYSQL_USER: glpi
      MYSQL_PASSWORD: changeme_glpi
    volumes:
      - mariadb_data:/var/lib/mysql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5

  glpi:
    image: glpi/glpi:latest
    container_name: glpi
    restart: unless-stopped
    ports:
      - "8080:80"
    environment:
      GLPI_DB_HOST: mariadb
      GLPI_DB_NAME: glpi
      GLPI_DB_USER: glpi
      GLPI_DB_PASSWORD: changeme_glpi
      GLPI_DB_PORT: 3306
      GLPI_TIMEZONE: Europe/Paris
    volumes:
      - glpi_data:/var/www/html/files
      - glpi_plugins:/var/www/html/plugins
      - glpi_config:/var/www/html/config
    depends_on:
      mariadb:
        condition: service_healthy

volumes:
  mariadb_data:
  glpi_data:
  glpi_plugins:
  glpi_config:
```

Quelques points importants :

- `mariadb:10.11` : une version stable et éprouvée avec GLPI. MariaDB 11.x fonctionne aussi, mais 10.11 évite les surprises.
- `glpi/glpi:latest` : l'image officielle du projet GLPI, avec Apache et PHP préconfigurés.
- Les volumes sont persistants. Si tu détruis les conteneurs, tes données restent.
- `depends_on` avec `condition: service_healthy` évite que GLPI démarre avant que MariaDB soit prête.
- **Change les mots de passe** avant de lancer. `changeme_root` et `changeme_glpi`, c'est pour l'exemple.

Lance la stack :

```bash
cd glpi
docker compose up -d
```

Attends une minute que MariaDB initialise sa base et que GLPI démarre.

## Premier lancement et configuration de la base

Ouvre ton navigateur sur `http://localhost:8080` (ou l'IP de ta machine + `:8080`). Tu arrives sur l'assistant d'installation de GLPI.

1. **Choix de la langue** : Français, évidemment.
2. **Licence** : lis-la vite fait et accepte. C'est du GPL, pas un contrat d'âme.
3. **Prérequis** : l'image Docker embarque déjà tout ce qu'il faut (PHP intl, mbstring, mysqli, etc.). Tous les voyants devraient être verts. Si un truc est rouge, vérifie que tu utilises bien l'image officielle.
4. **Configuration de la base** :
   - Serveur : `mariadb`
   - Utilisateur : `glpi`
   - Mot de passe : celui que tu as mis dans `docker-compose.yml`
   - Base de données : `glpi`

Clique sur "Continuer". GLPI teste la connexion, crée ses tables, et te demande si tu veux envoyer des statistiques d'usage au projet. À toi de voir, moi je décoche.

À la fin de l'installation, GLPI te propose de te connecter. Les identifiants par défaut sont :

- **Utilisateur** : `glpi`
- **Mot de passe** : `glpi`

Oui, c'est débile. Oui, il faut le changer immédiatement.

## Sécurisation rapide

Une fois connecté, GLPI te hurle dans les notifications qu'il y a des mises à jour à faire et que la sécurité est à renforcer. Il a raison.

Va dans **Administration > Utilisateurs > glpi**. Modifie le mot de passe. Choisis quelque chose de solide, pas `Glpi123!`.

Puis va dans **Configuration > Générale > Système**. Vérifie que l'URL de l'application correspond à ton accès réel. Si tu passes par un reverse proxy (Caddy, Traefik, Nginx), mets l'URL publique ici. Sinon, GLPI génère des liens en `http://localhost:8080` et ça casse tout quand tu y accèdes de l'extérieur.

## Paramétrage rapide : entités, utilisateurs et tickets

GLPI sans configuration, c'est une usine à gaz vide. Voici le minimum pour que ça devienne utile.

### Créer une entité

Par défaut, tout est dans l'entité racine. Crée une entité pour ta structure dans **Administration > Entités**. Donne-lui un nom clair. Tous tes objets (ordinateurs, tickets, utilisateurs) vont s'y rattacher.

### Créer des utilisateurs

Va dans **Administration > Utilisateurs > Ajouter**. Tu peux créer des comptes locaux ou configurer une authentification LDAP/SSO plus tard. Pour tester, crée un utilisateur avec le profil "Standard" et un autre avec le profil "Technicien".

Le profil "Standard" peut ouvrir des tickets. Le profil "Technicien" peut les traiter. Simple.

### Configurer les catégories de tickets

Dans **Configuration > Intitulés > Catégories des tickets**, ajoute quelques catégories : "Matériel défectueux", "Logiciel", "Demande d'accès", "Réseau". C'est vide par défaut, et sans catégories, tes utilisateurs ne savent pas comment classer leurs demandes.

### Ouvrir un premier ticket

Déconnecte-toi et reconnecte-toi avec le compte "Standard". Clique sur **Assistance > Créer un ticket". Remplis le titre, choisis une catétoire, décris le problème. Valide.

Reconnecte-toi en admin ou technicien. Le ticket est là, avec une file d'attente, des priorités, des statuts. Tu viens de remplacer Excel + email pour le support IT. Félicitations.

## Inventaire : activer la remontée automatique

GLPI sans inventaire, c'est un helpdesk. Avec l'inventaire, c'est un ITSM complet. L'image Docker officielle embarque déjà le endpoint natif pour recevoir les données des agents GLPI.

Tu n'as rien à configurer côté serveur. L'endpoint `/front/inventory.php` est prêt. Tu dois juste déployer l'agent GLPI sur tes postes clients.

Si tu veux aussi déployer l'agent GLPI sur tes postes clients, j'ai un guide dédié sur [l'installation de l'agent GLPI avec Docker](/glpi-agent-docker-monitorer-postes/). L'agent scanne le hardware et les logiciels installés, puis envoie tout ça directement dans GLPI. En quelques minutes, tu vois apparaître tes machines dans **Parc > Ordinateurs**.

## Mise à jour de GLPI

Une nouvelle version de GLPI sort tous les deux ou trois mois. Avec Docker, la mise à jour est propre :

```bash
cd glpi
docker compose pull
docker compose up -d
```

L'image télécharge la dernière version, recrée le conteneur, et GLPI détecte automatiquement qu'une mise à jour de la base est nécessaire. Tu accèdes à l'interface, il te demande de valider la migration, et c'est reparti.

Avant chaque mise à jour, sauvegarde tes volumes :

```bash
docker run --rm -v glpi_mariadb_data:/data -v $(pwd):/backup alpine tar czf /backup/glpi-db-backup.tar.gz -C /data .
```

Oui, c'est relou. Mais perdre une base de tickets parce que t'as voulu gagner trente secondes, c'est pire.

## Intégration avec un reverse proxy (Caddy ou Traefik)

Si tu veux un accès en HTTPS avec un vrai nom de domaine, place Caddy ou Traefik devant GLPI. Pas besoin de toucher le conteneur GLPI.

Exemple avec Caddy (à adapter selon ton setup) :

```
glpi.tondomaine.com {
    reverse_proxy localhost:8080
}
```

Pense bien à mettre à jour l'**URL de l'application** dans la configuration GLPI après. Sinon, les liens dans les emails de notification restent en `http://localhost:8080` et tes utilisateurs te harcèlent parce que "le lien ne marche pas".

## FAQ

**Q : L'installation bloque sur "Impossible de se connecter à la base de données" ?**
Vérifie que MariaDB est bien démarrée avec `docker compose ps`. Le healthcheck doit être passé. Si tu es trop pressé et que tu ouvres GLPI avant que MariaDB soit prête, attends trente secondes et rafraîchis.

**Q : Je peux utiliser PostgreSQL au lieu de MariaDB ?**
Techniquement GLPI supporte PostgreSQL. En pratique, 90% des installations documentées utilisent MariaDB/MySQL. Si tu veux t'aventurer sur PostgreSQL, prépare-toi à chercher plus longtemps quand un truc coince.

**Q : Comment sauvegarder la base de données régulièrement ?**
Ajoute un conteneur `mariadb-dump` dans ton compose avec une tâche cron, ou utilise un outil comme [Beszel](/beszel-monitoring-docker/) ou un simple script cron sur l'hôte :

```bash
#!/bin/bash
docker exec glpi-mariadb mysqldump -u glpi -pchangeme_glpi glpi > /backup/glpi-$(date +%F).sql
```

**Q : GLPI est lent, que faire ?**
Premier réflexe : vérifie les ressources. GLPI + MariaDB sur 1 Go de RAM, ça rampe. Monte à 4 Go. Deuxième réflexe : active le cache dans **Configuration > Performances**. Troisième réflexe : vérifie que tu n'as pas laissé le mode debug activé.

**Q : L'image officielle n'existe plus ou ne marche pas ?**
L'image `glpi/glpi` est maintenue par le projet. Si jamais elle disparaît, l'image communautaire `diouxx/glpi` est la référence historique et reste disponible.

**Q : Puis-je mettre plusieurs instances GLPI sur la même machine ?**
Oui. Change le port externe dans le compose (par exemple `8081:80` pour la deuxième instance) et utilise des noms de volumes différents.

## Conclusion

Tu viens de monter un ITSM complet en auto-hébergement avec deux conteneurs et un fichier YAML. GLPI en Docker, c'est la fin des installations LAMP interminables. Tu as un helpdesk fonctionnel, une base d'inventaire prête à recevoir tes agents, et une stack qui se met à jour en deux commandes.

Le plus dur reste l'adoption par tes utilisateurs. Un outil ITSM, ça ne vaut que si les gens l'utilisquent. Commence petit : impose le pour les demandes de matériel. Une fois que tes collègues auront compris que c'est plus rapide qu'un email à tout le monde, le reste suivra.

Et toi, tu gères tes tickets avec quoi actuellement ? Excel ? Un Trello bancal ? Raconte en commentaire.
