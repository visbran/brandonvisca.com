---
title: "BookStack Docker : wiki pour équipes"
description: "Déploie BookStack avec Docker Compose : wiki auto-hébergé, open-source et facile pour équipes. Guide complet, comparaison alternatives, reverse proxy."
pubDatetime: "2026-06-13T08:00:00.000Z"
author: Brandon Visca
tags:
  - docker
  - auto-hebergement
  - wiki
  - intermediaire
  - bookstack
featured: false
draft: false
ogImage: ""
---
> 💡 **TL;DR**
> - BookStack est un wiki open-source pensé pour les équipes, avec une organisation en étagères, livres et chapitres
> - Tu le déploies en 10 minutes avec Docker Compose (MariaDB + BookStack)
> - Interface WYSIWYG moderne, pas besoin de connaître le Markdown
> - Parfait remplaçant auto-hébergé à Confluence pour les PME et les homelabs
> - Docker Compose complet, tableau comparatif et reverse proxy inclus ci-dessous

## Table des matières

## Pourquoi un wiki auto-hébergé en 2026 ?

Tu connais la situation. Ton équipe (ou ton homelab perso) accumule des procédures, des documentations, des scripts et des connaissances métier dans :
- des Google Docs éparpillés sur dix comptes différents,
- des fichiers Markdown sur un dépôt Git que personne ne sait mettre à jour,
- des notes Notion partagées avec ton ex-collègue qui a encore les droits d'admin,
- ou pire, un Confluence Atlassian qui coûte plus cher que ton serveur et qui rame à chaque recherche.

La documentation structurée, c'est le ciment des équipes techniques. Quand quelqu'un part en vacances, quand un nouveau dev arrive, quand ton NAS plante à 3 h du matin et que tu dois retrouver la procédure de restauration : tu as besoin d'un wiki centralisé, rapide, et qui n'appartient à personne d'autre que toi.

BookStack répond exactement à ce besoin. C'est un wiki open-source développé en PHP par Dan Brown, sous licence MIT, avec plus de 14 000 stars sur GitHub. L'approche est astucieuse : au lieu d'une arborescence de dossiers à la Wikipedia (qui devient vite un bazar), BookStack organise la connaissance en **étagères**, **livres** et **chapitres**. C'est intuitive, visuel, et même ton collègue commercial comprend comment ça marche en deux minutes.

Dans mon [guide auto-hébergement complet](/auto-hebergement-guide-complet-2025/), je recommande un wiki comme service fondamental d'une infrastructure personnelle. BookStack est celui que je déploie systématiquement quand on me demande un outil de documentation interne sans budget ni cloud.

## Qu'est-ce que BookStack exactement ?

BookStack n'est pas juste un autre wiki. Il a été conçu avec une idée simple : que la documentation soit écrite par des humains, pas par des développeurs en quête de la syntaxe Markdown parfaite.

Voici ce qu'il propose concrètement :

- **Éditeur WYSIWYG complet** : tu écris comme dans Word, avec des images drag-and-drop, des tableaux, des blocs de code avec coloration syntaxique. Pas besoin de retenir que `**texte**` c'est gras.
- **Organisation en étagères, livres, chapitres et pages** : tu crées une étagère "Infrastructure", un livre "Docker", un chapitre "Reverse Proxy", et des pages dedans. C'est clair, c'est beau, c'est logique.
- **Permissions granulaires** : par rôle, par livre, par chapitre. Tu peux masquer certaines procédures sensibles aux externes.
- **Recherche full-text** : rapide, pertinente, avec prévisualisation. L'indexation se fait en arrière-plan.
- **LDAP et SSO** : Active Directory, SAML2, OIDC, Google OAuth, GitHub OAuth. Ton wiki se connecte à ton annuaire existant sans bidouille.
- **Export PDF/ePub/HTML** : pour archiver ou partager une documentation hors ligne.
- **Historique des révisions** : qui a modifié quoi et quand. Annulation possible en un clic.
- **API REST** : pour automatiser, migrer ou synchroniser depuis d'autres outils.
- **Multilingue** : interface traduite en français, anglais, allemand, espagnol, etc.
- **Thème clair/sombre** : parce que personne n'aime écrire une procédure à minuit sur fond blanc.

L'image Docker officielle `linuxserver/bookstack` est maintenue par LinuxServer.io, une communauté de référence pour les conteneurs auto-hébergés. Elle supporte amd64, arm64 et armhf. Elle inclut toutes les dépendances PHP nécessaires, le serveur web Nginx intégré, et une configuration simplifiée par variables d'environnement.

Si tu débutes avec Docker, commence par mon article sur [les services essentiels à auto-héberger](/docker-debutant-services-auto-heberger/) pour comprendre l'écosystème. BookStack s'intègre parfaitement dans cette stack.

## Prérequis

- Un serveur Linux avec Docker et Docker Compose installés (Docker Engine 24+ recommandé)
- 1 cœur CPU et 1 Go de RAM minimum (2 Go recommandés avec MariaDB)
- 5 Go d'espace disque pour le système, puis selon tes documents
- Un nom de domaine (ou sous-domaine) pointant vers ton serveur si tu veux HTTPS
- Un reverse proxy (Caddy, Traefik ou Nginx Proxy Manager) pour gérer les certificats SSL

BookStack n'est pas gourmand. Un Raspberry Pi 4 avec 4 Go de RAM suffit pour une équipe de dix personnes sans problème. Pour une PME ou un usage intensif, un petit VPS de 2 cœurs / 4 Go est confortable.

## Déploiement BookStack avec Docker Compose

Crée un dossier dédié et un fichier `docker-compose.yml` :

```bash
mkdir -p ~/bookstack && cd ~/bookstack
```

Voici le Docker Compose complet et prêt à l'emploi :

```yaml
version: "3.8"

services:
  bookstack:
    image: lscr.io/linuxserver/bookstack:latest
    container_name: bookstack
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/Paris
      - APP_URL=https://wiki.tondomaine.com
      - DB_HOST=bookstack_db
      - DB_PORT=3306
      - DB_USER=bookstack
      - DB_PASS=super-secret-password
      - DB_DATABASE=bookstackdb
    volumes:
      - ./bookstack_app_data:/config
    ports:
      - 6875:80
    restart: unless-stopped
    depends_on:
      - bookstack_db

  bookstack_db:
    image: lscr.io/linuxserver/mariadb:latest
    container_name: bookstack_db
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/Paris
      - MYSQL_ROOT_PASSWORD=root-secret-password
      - MYSQL_DATABASE=bookstackdb
      - MYSQL_USER=bookstack
      - MYSQL_PASSWORD=super-secret-password
    volumes:
      - ./bookstack_db_data:/config
    restart: unless-stopped
```

Quelques explications sur les choix :

- `PUID=1000` et `PGID=1000` : force l'UID/GID de ton utilisateur Linux pour éviter les problèmes de permissions sur les volumes. Adapte selon ton système (`id $USER`).
- `APP_URL` : l'URL publique de ton wiki. BookStack l'utilise pour générer les liens et les emails. Ne laisse pas l'IP locale ici si tu passes par un reverse proxy.
- `DB_PASS` et `MYSQL_PASSWORD` : doivent être identiques. Change les mots de passe par défaut avant de lancer.
- Le port exposé est `6875` en HTTP interne. C'est ton reverse proxy qui gérera le HTTPS externe.

Lance le stack :

```bash
docker compose up -d
```

Attends 30 secondes que MariaDB initialise la base, puis accède à `http://IP-du-serveur:6875`. Les identifiants par défaut sont :
- **Email** : `admin@admin.com`
- **Mot de passe** : `password`

Change immédiatement le mot de passe dans Paramètres > Profil.

### Avec un reverse proxy Caddy

Si tu utilises [Caddy avec Docker](/caddy-docker-reverse-proxy-guide/), ajoute simplement ce bloc dans ton Caddyfile :

```caddy
wiki.tondomaine.com {
    reverse_proxy bookstack:6875
}
```

Caddy gère automatiquement les certificats Let's Encrypt. Pas de certbot, pas de renouvellement manuel.

### Avec Nginx Proxy Manager

Dans l'interface web de [Nginx Proxy Manager](/nginx-proxy-manager-docker-guide/) :
1. Ajoute un proxy host : `wiki.tondomaine.com`
2. Forward hostname : `bookstack`
3. Forward port : `6875`
4. Active "Block Common Exploits" et "Request a new SSL Certificate"
5. Force SSL et HSTS

## Configuration initiale et premiers pas

Une fois connecté, prends le temps de configurer les bases avant d'inviter ton équipe.

**1. Modifier les paramètres généraux**
Va dans Paramètres > Paramètres de l'application. Change :
- le nom de l'application (ex: "Wiki IT Interne")
- la langue par défaut en Français
- le fuseau horaire Europe/Paris
- le thème par défaut si tu préfères le sombre

**2. Créer la structure documentaire**
Pense en termes d'étagères métiers. Par exemple :
- Étagère "Infrastructure" : livre "Réseau", livre "Docker", livre "Sécurité"
- Étagère "Procédures" : livre "Onboarding", livre "Pannes", livre "Mises à jour"
- Étagère "Développement" : livre "API Interne", livre "Frontend", livre "CI/CD"

**3. Gérer les utilisateurs et les rôles**
Dans Paramètres > Utilisateurs :
- crée des groupes (Admin, Éditeur, Lecteur)
- importe les utilisateurs via CSV ou connecte LDAP si tu as un annuaire d'entreprise
- attribue des permissions par étagère. Par exemple, masque l'étagère "Sécurité" aux lecteurs externes.

**4. Activer les exports**
Dans Paramètres > Export, active PDF et HTML. Utile pour générer une documentation offline avant une intervention sur site.

**5. Personnaliser la page d'accueil**
BookStack permet de définir une page d'accueil personnalisée avec du HTML simple. C'est l'endroit idéal pour mettre les liens vers les procédures les plus consultées.

## BookStack vs les alternatives : tableau comparatif

| Critère | BookStack | Confluence | Wiki.js | Outline | MediaWiki |
|---------|-----------|------------|---------|---------|-----------|
| **Licence** | MIT (open-source) | Propriétaire (payant) | AGPL-3.0 | BSL (source disponible) | GPL-2.0+ |
| **Auto-hébergé** | Oui | Non (Cloud/Server payant) | Oui | Oui (self-hosted payant) | Oui |
| **Gratuit** | Totalement | 10 utilisateurs max (Cloud) | Oui | Non (licence obligatoire) | Oui |
| **Interface** | WYSIWYG moderne | WYSIWYG, lourd | Markdown + WYSIWYG | Markdown, très design | Wiki-texte brut |
| **Support Markdown** | Partiel (via éditeur) | Oui | Natif | Natif | Non (syntaxe wiki) |
| **Permissions** | Granulaires (étagères/livres) | Très avancées | Granulaires | Par collection | Basiques (groupes) |
| **LDAP / SSO** | Oui (AD, SAML2, OIDC) | Oui (natif Atlassian) | Oui (LDAP, SAML, OAuth) | Oui (Google, Slack, Azure) | Oui (via extensions) |
| **Docker officiel** | Oui (`linuxserver/bookstack`) | Non | Oui (`requarks/wiki`) | Oui (Docker Compose complet) | Oui (`mediawiki`) |
| **App mobile** | Responsive web | Application native | Responsive web | Application iOS | Responsive web |
| **Ressources RAM** | ~256 Mo (avec DB) | 2 Go+ (Server) | ~512 Mo | ~1 Go+ | ~512 Mo |
| **Facilité d'usage** | Très intuitive | Moyenne (courbe d'apprentissage) | Bonne | Excellente (UI moderne) | Technique |
| **Recherche** | Full-text intégrée | Power Search (Cloud) | Elasticsearch | Full-text PostgreSQL | Moteur MediaWiki |

Mon verdict pour un homelab ou une PME :

- **BookStack** : le meilleur rapport facilité / puissance / coût. WYSIWYG, organisation intuitive, LDAP, Docker simple. C'est mon choix par défaut.
- **Confluence** : si tu es déjà dans l'écosystème Atlassian et que tu as le budget. Sinon, c'est overpriced pour ce que ça fait.
- **Wiki.js** : excellent si ton équipe est technique et préfère le Markdown. Moins intuitif pour les profils non-développeurs.
- **Outline** : magnifique, mais la licence BSL impose un paiement pour l'auto-hébergement au-delà de 500 utilisateurs. Dommage.
- **MediaWiki** : la référence historique (Wikipedia), mais l'interface fait peur en 2026. Réservé aux puristes.

Pour stocker les mots de passe de l'équipe, [Vaultwarden](/vaultwarden-docker-gestionnaire-mots-de-passe/) s'intègre très bien en complément d'un wiki d'entreprise. Même principe : auto-hébergé, open-source, Docker.

## Sécuriser l'accès et les données

Un wiki contient souvent des informations sensibles. Voici les mesures de base à appliquer.

**HTTPS partout**
Ne laisse jamais BookStack en HTTP. Ton reverse proxy doit forcer le HTTPS, activer HSTS et bloquer les versions obsolètes de TLS. Caddy le fait nativement. Avec Traefik ou NPM, c'est un simple toggle.

**Sauvegardes automatisées**
Le volume `./bookstack_app_data` contient les uploads et la config. Le volume `./bookstack_db_data` contient la base MariaDB. Sauvegarde-les avec [Duplicati](/duplicati-docker-sauvegarde/) ou un script cron rsync.

```bash
#!/bin/bash
# backup-bookstack.sh
DATE=$(date +%Y%m%d_%H%M%S)
tar czf "/backup/bookstack_app_$DATE.tar.gz" ~/bookstack/bookstack_app_data
docker exec bookstack_db mysqldump -u bookstack -psuper-secret-password bookstackdb > "/backup/bookstack_db_$DATE.sql"
```

**Mises à jour**
LinuxServer.io publie des mises à jour régulières. Mets à jour une fois par semaine :

```bash
cd ~/bookstack
docker compose pull
docker compose up -d
```

**Fail2ban**
Si tu exposes BookStack sur Internet, protège-toi contre les attaques par force brute sur la page de connexion. [Fail2ban avec Docker](/fail2ban-docker-securite-serveur/) peut surveiller les logs Nginx et bannir les IP abusives après cinq tentatives ratées.

**Authentification double facteur**
BookStack supporte le TOTP (Google Authenticator, Authy, etc.). Active-le pour tous les comptes admin dans Paramètres > Sécurité.

## Intégrations et astuces avancées

**Brancher un système de fichiers**
Si tu veux attacher des fichiers lourds (ISO, archives) sans encombrer la base, monte un volume supplémentaire dans le conteneur et configure BookStack pour l'utiliser comme stockage de fichiers personnalisé. Alternative : utilise [File Browser](/filebrowser-docker-gestionnaire-fichiers/) à côté et linke les fichiers partagés.

**Lier à ta gestion documentaire**
Pour les PDF scannés et la gestion documentaire, [Paperless-ngx](/paperless-ngx-docker-guide-auto-hebergement/) complète BookStack sur les documents administratifs. Mon workflow : Paperless stocke et OCRise les factures, BookStack documente les procédures métier.

**Notifications Slack / Discord**
Via l'API REST de BookStack et un webhook Discord, tu peux notifier ton channel technique à chaque création ou modification de page critique. C'est un simple script Python lancé en tâche cron ou via [n8n](/n8n-docker-workflow-automation/).

**Personnalisation CSS**
Dans Paramètres > Personnalisation, tu peux injecter du CSS custom pour harmoniser les couleurs avec ta charte graphique ou cacher des éléments que tu ne souhaites pas afficher aux utilisateurs.

## Migration depuis un autre wiki

Si tu viens de Confluence, d'un MediaWiki ou d'une collection de fichiers Markdown, il existe des scripts communautaires pour importer vers BookStack via son API REST. Le processus standard :

1. Exporte tes données au format HTML ou Markdown depuis l'ancien outil
2. Utilise un script Python (disponible sur le repo GitHub de BookStack) pour pousser chaque page via l'API
3. Recrée manuellement la structure en étagères et livres
4. Réattribue les permissions utilisateurs

La migration d'un MediaWiki est la plus pénible à cause du format wiki-texte. Depuis Confluence, l'export HTML se réimporte relativement bien avec un peu de nettoyage regex.

## FAQ

**Puis-je utiliser PostgreSQL à la place de MariaDB ?**
Oui, BookStack supporte officiellement MySQL/MariaDB et PostgreSQL. Modifie simplement les variables `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASS` et change l'image du service DB pour `postgres:15-alpine`.

**Est-ce que BookStack gère les images et les pièces jointes ?**
Oui. Les fichiers sont stockés dans le volume `/config` du conteneur. Tu peux aussi configurer un stockage S3 (MinIO, AWS) si tu préfères externaliser.

**Peut-on écrire en Markdown ?**
L'éditeur principal est WYSIWYG, mais BookStack propose un mode Markdown alternatif dans les paramètres d'édition, et il convertit automatiquement le Markdown collé depuis le presse-papiers.

**Le service est-il accessible hors ligne ?**
Si tu l'héberges en local sans reverse proxy public, oui, il est accessible depuis ton réseau local. Pour un accès distant, il te faut soit un VPN (WireGuard), soit une exposition HTTPS publique via reverse proxy.

**Puis-je dupliquer une page ou un livre entier ?**
Oui, la fonction "Copier" existe au niveau de la page, du chapitre et du livre. C'est pratique pour créer des templates de procédures.

**BookStack est-il traduit en français ?**
Oui, l'interface est entièrement traduite en français. La langue se change dans les paramètres utilisateur ou globaux.
