---
title: "Focalboard Docker : alternative Notion/Trello auto-hébergée"
description: "Guide focalboard docker complet : déploie Focalboard sous Docker pour un kanban self-hosted open-source. Alternative Notion et Trello auto-hébergée avec Docker Compose."
pubDatetime: "2026-07-05T08:00:00.000Z"
modDatetime: "2026-07-05T08:00:00.000Z"
author: Brandon
tags:
  - intermediaire
  - auto-hebergement
  - docker
  - focalboard
  - kanban
featured: false
draft: false
focusKeyword: focalboard docker
faqs: []
ogImage: ""
---
> 💡 **TL;DR**
> - Focalboard est un outil de gestion de projet type kanban open-source développé par Mattermost
> - Tu le déploies en 5 minutes avec Docker Compose (SQLite intégré, aucune base externe requise)
> - Interface propre : tableaux, vues liste, calendrier, templates, partage par lien, multi-utilisateurs
> - Parfait remplaçant auto-hébergé à Notion et Trello pour les équipes et les homelabs

## Table des matières

## Pourquoi se passer de Notion et Trello ?

Trello, c'est pratique. Tu crées un tableau, tu glisses-déposes des cartes, tu colores des labels. Le problème ? Ton data vit chez Atlassian. Notion, c'est encore pire : tes notes, tes bases de données relationnelles, tes workflows, tout est verrouillé dans un écosystème propriétaire américain avec une politique de confidentialité qui change plus souvent que ta crème solaire.

Les arguments contre les outils SaaS de gestion de projet se résument à trois points.

**Premier**, le prix. Trello te file dix tableaux gratuits, puis tu passes à 5 € par utilisateur et par mois. Avec une équipe de cinq personnes, ça fait 300 € par an pour des listes de tâches. Notion est "gratuit" jusqu'à ce que tu découvres que l'historique des versions est limité, que les fichiers uploadés plafonnent, et que l'API n'est accessible que sur les plans payants.

**Deuxième**, tes données. Tes backlogs, tes roadmaps, tes procédures internes, tout transite par des serveurs que tu ne contrôles pas. Le RGPD exige que tu documentes ces sous-traitances, que tu signes des DPAs, et que tu t'assures que les données ne quittent pas l'Union Européenne sans garanties adéquates. C'est chiant, coûteux, et inutile quand tu peux héberger toi-même.

**Troisième**, la dépendance. Quand Notion fait une panne (et ça arrive), toute ton équipe est à l'arrêt. Quand Trello change son interface sans prévenir, tu perds une demi-journée à retrouver tes marques. Avec un outil auto-hébergé, la seule panne possible est la tienne. Et au moins, tu sais qui réparer.

En 2026, l'auto-hébergement n'est plus une lubie de barbu. Un VPS à 5 €/mois, Docker qui tourne partout, et des outils comme Focalboard prouvent que tu peux remplacer des SaaS propriétaires par des solutions open-source sans compromis. Si tu cherches d'autres outils pour compléter ton homelab, j'ai aussi couvert [Memos pour les notes rapides](/memos-docker-notes-auto-heberge/) et [BookStack pour la documentation d'équipe](/bookstack-docker-wiki-equipe/).

## Qu'est-ce que Focalboard exactement ?

Focalboard est une application de gestion de projet open-source développée par l'équipe de Mattermost (la messagerie instantanée auto-hébergée). Le projet est sous licence AGPL-3.0, avec un dépôt actif sur GitHub (`mattermost/focalboard`). Il existe en deux versions : une **application desktop** (Windows, macOS, Linux) pour usage personnel, et une **version serveur web** que tu déploies toi-même pour ton équipe.

C'est la version serveur qui nous intéresse ici. Elle se présente comme une interface web propre, accessible depuis n'importe quel navigateur, et synchronisée entre tous tes appareils. Le concept est simple : des **tableaux kanban**, des **vues liste**, des **vues calendrier**, et des **templates** pour démarrer vite.

Voici ce que Focalboard propose concrètement :

- **Tableaux kanban** : colonnes personnalisables, cartes avec description, checklists, dates d'échéance, propriétés et labels colorés. Tu glisses-déposes, ça marche sur mobile et desktop.
- **Vues multiples** : chaque tableau peut s'afficher en kanban, en liste, en galerie ou en calendrier. Tu bascules d'une vue à l'autre en un clic sans dupliquer tes données.
- **Templates** : sprint agile, suivi de bugs, plan de contenu, gestion de projet client. Tu crées tes propres templates ou tu réutilises ceux intégrés.
- **Propriétés personnalisées** : texte, nombre, date, sélection multiple, URL, email, checkbox. Tu structures tes cartes comme dans Notion, sans la lourdeur.
- **Partage par lien** : tu peux partager un tableau en lecture seule avec une URL publique, ou inviter des utilisateurs avec des permissions spécifiques.
- **Multi-utilisateurs** : création de comptes, attribution de cartes, notifications de mention. Parfait pour une petite équipe.
- **Historique des cartes** : qui a déplacé quoi, quand et pourquoi. Pas de "j'ai perdu ma carte".
- **Import/Export** : tu peux importer des données depuis Trello, Notion et Asana via CSV. Tu exportes tes tableaux en archive pour sauvegarde ou migration.
- **Thème clair/sombre** : parce qu'un tableau kanban sur fond blanc à 23 h, c'est une agression visuelle.

L'image Docker officielle `mattermost/focalboard` est maintenue par l'équipe Mattermost. Elle est légère (~50 Mo), supporte amd64 et arm64, et inclut SQLite par défaut. Pas besoin de PostgreSQL ou de Redis pour démarrer. C'est ça qui rend Focalboard aussi accessible : tu montes le conteneur, tu accèdes à l'interface, tu crées ton premier tableau. Point.

Focalboard s'intègre aussi nativement avec Mattermost via un plugin. Si tu utilises déjà Mattermost pour la messagerie d'équipe, chaque canal peut avoir son propre tableau Focalboard intégré. C'est un bonus, pas une obligation.

## Prérequis

Avant de commencer, il te faut :

- Un serveur Linux avec **Docker** et **Docker Compose** installés (si ce n'est pas le cas, vois mon [guide Docker pour débutants](/docker-debutant-services-auto-heberger/))
- 1 cœur CPU et 512 Mo de RAM minimum (1 Go recommandé pour être confortable)
- 2 Go d'espace disque pour le système, puis selon tes tableaux et tes uploads
- Un **nom de domaine** ou sous-domaine pointant vers ton serveur (facultatif mais recommandé pour HTTPS)
- Un **reverse proxy** (Traefik, Caddy ou Nginx Proxy Manager) pour gérer les certificats SSL

Focalboard est économe. Un Raspberry Pi 4 avec 2 Go de RAM suffit pour une équipe de dix personnes sans problème. Sur un VPS de 1 cœur / 2 Go, il tourne tranquillement à côté d'autres services. Pour le mettre en perspective, c'est bien plus léger que [Zabbix pour monitorer ton infrastructure](/zabbix-docker-monitoring-infrastructure/) ou que [GLPI pour le ticketing](/glpi-docker-itsm-auto-heberge/).

## Déploiement Focalboard avec Docker Compose

Crée un dossier dédié et un fichier `docker-compose.yml` :

```bash
mkdir -p ~/focalboard && cd ~/focalboard
```

Voici le Docker Compose complet et prêt à l'emploi :

```yaml
services:
  focalboard:
    image: mattermost/focalboard:latest
    container_name: focalboard
    restart: unless-stopped
    ports:
      - "8000:8000"
    volumes:
      - ./data:/data
    environment:
      - FB_SERVERROOT=https://focalboard.tondomaine.com
      - FB_PORT=8000
      - FB_DBTYPE=sqlite3
      - FB_DBCONFIG=/data/focalboard.db
      - FB_TELEMETRY=false
      - FB_PROMETHEUS_ADDRESS=
```

Démarre la stack :

```bash
docker compose up -d
```

En 30 secondes, Focalboard est accessible sur `http://<IP_SERVEUR>:8000`. C'est tout. Pas de base de données externe à configurer, pas de migrations à lancer, pas de variables complexes à renseigner.

**Explication des variables d'environnement :**

- `FB_SERVERROOT` : l'URL publique de ton instance. Obligatoire pour que les liens et les partages fonctionnent correctement. Remplace par ton vrai domaine.
- `FB_PORT` : le port interne du conteneur. Laisse 8000 sauf si tu as un conflit.
- `FB_DBTYPE` : sqlite3 par défaut. Tu peux passer à postgres si tu veux une base plus robuste pour une grosse équipe.
- `FB_DBCONFIG` : chemin vers la base SQLite dans le volume persistant.
- `FB_TELEMETRY=false` : désactive la télémétrie. Par défaut, Focalboard envoie des métriques d'usage anonymes. Tu peux les couper ici.
- `FB_PROMETHEUS_ADDRESS=` : laisse vide pour désigner l'exposition des métriques Prometheus.

## Configuration initiale

À la première connexion, Focalboard te demande de créer un compte administrateur. Renseigne un email, un nom d'utilisateur et un mot de passe solide. Ce premier compte a les droits complets sur l'instance.

Ensuite, tu arrives sur un tableau d'accueil vide. Clique sur "+ Nouveau tableau" et choisis un template :

- **Projet** : colonnes À faire, En cours, Terminé
- **Suivi de bugs** : colonnes Nouveau, Confirmé, En cours, En test, Résolu
- **Roadmap** : colonnes par trimestre ou par sprint
- **Vide** : tu construis tout toi-même

Crée tes colonnes, ajoute des cartes, personnalise les propriétés. L'interface est intuitive : glisser-déposer, clic droit pour les options, icône en haut à droite pour changer de vue (kanban, liste, calendrier, galerie).

**Invitation d'utilisateurs** : dans le menu latéral, clique sur "Partager", puis "Inviter des utilisateurs". Tu peux générer un lien d'invitation ou envoyer des emails directs. Chaque nouvel utilisateur crée son propre compte.

**Personnalisation** : tu peux créer des labels colorés, des propriétés personnalisées (date, texte, nombre, sélection), et des filtres pour afficher uniquement les cartes qui t'intéressent. C'est là que Focalboard se rapproche de Notion : tu structures tes données comme tu veux, sans base de données relationnelle complexe.

## Fonctionnalités avancées et astuces

**Vues multiples**
Chaque tableau peut avoir plusieurs vues simultanées. Tu peux avoir une vue kanban pour le daily, une vue calendrier pour les deadlines, et une vue liste pour l'export. Les trois sont synchronisées : quand tu déplaces une carte dans la vue kanban, elle bouge aussi dans le calendrier. C'est magique et ça évite la duplication d'informations.

**Templates personnalisés**
Une fois que tu as construit un tableau qui te plaît, clique sur le menu "..." et "Enregistrer comme template". Il sera disponible pour tous les nouveaux tableaux. C'est pratique pour standardiser les processus d'équipe.

**Import depuis Trello/Notion**
Focalboard supporte l'import CSV. Exporte tes données depuis Trello (JSON → convertisseur en ligne) ou Notion (export CSV), puis importe directement dans un nouveau tableau. La correspondance des colonnes est automatique pour les champs standards.

**Notifications**
Focalboard envoie des notifications dans l'interface quand quelqu'un te mentionne dans une carte ou quand une date d'échéance approche. Ce n'est pas aussi poussé que les emails de Trello, mais ça fait le job pour une équipe collocée.

**Sauvegarde et export**
Dans le menu d'un tableau, tu trouves l'option "Exporter l'archive". Ça génère un fichier JSON contenant tout le tableau : cartes, propriétés, historique, commentaires. Garde ces archives dans un système de backup comme [Duplicati](/duplicati-docker-sauvegarde/) pour être tranquille.

## Passer à PostgreSQL (optionnel)

Si tu prévois d'utiliser Focalboard avec une équipe de plus de vingt personnes, SQLite peut montrer ses limites en écriture concurrente. Passer à PostgreSQL est simple.

Modifie ton `docker-compose.yml` :

```yaml
services:
  focalboard:
    image: mattermost/focalboard:latest
    container_name: focalboard
    restart: unless-stopped
    ports:
      - "8000:8000"
    volumes:
      - ./data:/data
    environment:
      - FB_SERVERROOT=https://focalboard.tondomaine.com
      - FB_PORT=8000
      - FB_DBTYPE=postgres
      - FB_DBCONFIG=postgres://focalboard:ton_mot_de_passe@db:5432/focalboard?sslmode=disable
    depends_on:
      - db

  db:
    image: postgres:15-alpine
    container_name: focalboard-db
    restart: unless-stopped
    volumes:
      - ./postgres-data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: focalboard
      POSTGRES_USER: focalboard
      POSTGRES_PASSWORD: ton_mot_de_passe
```

Recrée les conteneurs :

```bash
docker compose down
docker compose up -d
```

Note que cette migration ne transfère pas automatiquement tes données SQLite existantes. Pour migrer, exporte tes tableaux en archive depuis l'interface, puis réimporte-les après le changement de base.

## Reverse proxy et HTTPS

Comme tout service auto-hébergé, Focalboard doit passer par un reverse proxy pour être accessible en HTTPS depuis l'extérieur. Si tu utilises Caddy, ajoute simplement à ton `Caddyfile` :

```
focalboard.tondomaine.com {
    reverse_proxy localhost:8000
}
```

Avec Traefik, ajoute les labels Docker :

```yaml
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.focalboard.rule=Host(`focalboard.tondomaine.com`)"
      - "traefik.http.routers.focalboard.tls.certresolver=letsencrypt"
      - "traefik.http.services.focalboard.loadbalancer.server.port=8000"
```

N'oublie pas de mettre à jour `FB_SERVERROOT` avec ton vrai domaine, sinon les liens de partage resteront en localhost.

Si tu cherches un reverse proxy simple et léger, j'ai couvert [Zoraxy](/zoraxy-docker-reverse-proxy/) dans un article récent. C'est un bon candidat pour un homelab minimaliste.

## Sauvegarde

La sauvegarde de Focalboard est triviale puisqu'il utilise SQLite. Il suffit de copier le fichier de base et les uploads.

Script de backup quotidien :

```bash
#!/bin/bash
BACKUP_DIR="/backup/focalboard/$(date +%Y%m%d)"
mkdir -p "$BACKUP_DIR"
cp -r ~/focalboard/data "$BACKUP_DIR/"
tar czf "$BACKUP_DIR.tar.gz" -C "$BACKUP_DIR" .
rm -rf "$BACKUP_DIR"
find /backup/focalboard -name "*.tar.gz" -mtime +30 -delete
```

Si tu utilises PostgreSQL, pense à aussi lancer `pg_dump` :

```bash
docker exec focalboard-db pg_dump -U focalboard focalboard > focalboard-backup.sql
```

Intègre ça dans ton système de backup global. Pour une stratégie complète, vois mon article sur [Duplicati pour sauvegarder tes conteneurs Docker](/duplicati-docker-sauvegarde/).

## Limites à connaître

Focalboard n'est pas Notion. Il ne fait pas de bases de données relationnelles, de formules complexes, de wikis imbriqués ou d'automatisations webhook. Si ton workflow repose sur des relations entre tableaux, des rollups ou des intégrations Zapier, Focalboard ne suffira pas.

Ce qu'il fait, il le fait bien : kanban, suivi de tâches, planification simple, partage d'équipe. Pour la documentation structurée, [BookStack](/bookstack-docker-wiki-equipe/) reste meilleur. Pour les notes rapides, [Memos](/memos-docker-notes-auto-heberge/) est plus adapté. Focalboard trouve sa place entre les deux : l'organisation de projet visuelle et légère.

Le développement a ralenti depuis que Mattermost a recentré ses priorités sur la messagerie. Le projet reste fonctionnel et stable, mais n'attends pas de nouvelles fonctionnalités tous les mois. C'est un outil mature, pas une startup en hyper-croissance.

## Conclusion

Focalboard est l'outil qu'il te faut si tu veux un tableau kanban auto-hébergé sans payer un abonnement SaaS ni confier tes roadmaps à un serveur californien. Il se déploie en cinq minutes avec Docker, consomme quasi rien en ressources, et propose 80 % des fonctionnalités de Trello à 0 €. Les 20 % manquants sont les automatisations complexes et les intégrations tierces, mais pour une petite équipe ou un usage personnel, c'est largement suffisant. Tu installes ça sur ton serveur, tu invites tes collègues, et tu retournes au travail. Pas de compte d'entreprise, pas de limite de cartes, pas de surprise sur la facture. Juste un kanban qui marche et qui reste chez toi.
