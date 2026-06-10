---
title: "Duplicati Docker : sauvegarde chiffrée auto-hébergée"
description: Installe Duplicati via Docker pour sauvegarder et chiffrer tes données localement. Docker Compose complet, protocoles cloud supportés et astuces de config.
pubDatetime: "2026-06-03T08:00:00.000Z"
modDatetime: "2026-06-03T08:00:00.000Z"
author: Brandon Visca
tags:
  - intermediaire
  - auto-hebergement
  - docker
  - backup
  - sauvegarde
featured: false
draft: false
---
**TL;DR** — Duplicati via Docker te permet de sauvegarder chiffrées tes données vers n'importe quel stockage local ou cloud. Docker Compose complet, UI web sur le port 8200, chiffrement AES-256 et aucune ligne de commande nécessaire après l'install.

## Pourquoi Duplicati en 2026 ?

Tu as monté ton [serveur Nextcloud](/nextcloud-docker-installation-complete-2025/), hébergé tes mots de passe avec [Vaultwarden](/vaultwarden-docker-gestionnaire-mots-de-passe/) et déployé une demi-douzaine de services Docker. Tout roule. Jusqu'au jour où un disque lâche, une fausse manip efface un volume ou un ransomware chiffre ton NAS. Sans backup, ton homelab devient un cimetière de données en quelques secondes.

Duplicati est un outil de sauvegarde open-source développé en C# sur .NET. Le projet vit sur GitHub sous le nom `duplicati/duplicati` avec environ 14 600 stars, maintenu activement : dernière mise à jour en juin 2026. La licence est LGPL-2.1. L'image officielle `duplicati/duplicati` sur Docker Hub est fraîche (tag `latest` mis à jour en avril 2026, support amd64). Autant dire que le projet est solide et pas près de mourir.

Ce qui fait la force de Duplicati : il chiffre tes backups localement avec AES-256 avant de les envoyer vers la destination. Même si ton cloud se fait pirater, tes données restent illisibles sans le mot de passe. Il supporte une dizaine de protocoles (S3, SFTP, FTP, WebDAV, Backblaze B2, Wasabi, Google Drive, SMB, SSH) et il gère la compression, la déduplication et les versions incrémentales. Tu peux restaurer un fichier datant de mardi 14h en trois clics depuis l'interface web.

Dans mon [guide auto-hébergement complet](/auto-hebergement-guide-complet-2025/), je répète un mantra : un service auto-hébergé sans backup, c'est un service provisoire. Duplicati transforme ce provisoire en pérenne.

## Duplicati vs les alternatives : tableau comparatif

| Outil | Chiffrement | Interface | Docker officiel | Protocoles | Compétence requise |
|-------|-------------|-----------|-----------------|------------|-------------------|
| **Duplicati** | AES-256, GPG | Web UI complète | Oui (`duplicati/duplicati`) | 10+ (S3, SFTP, SMB, Drive…) | Débutant |
| **Restic** | AES-256-CTR | CLI seule (ou third-party) | Oui (`restic`) | S3, SFTP, REST… | Avancée |
| **BorgBackup** | AES-256 | CLI + Vorta (GUI desktop) | Oui (`borgmatic`) | SSH, local | Avancée |
| **Kopia** | AES-256-GCM | CLI + UI optionnelle | Oui (`kopia/kopia`) | S3, SFTP, SMB… | Intermédiaire |
| **rsync + cron** | Aucun | Aucune | Non (natif Linux) | SSH | Avancée |

Mon choix pour un homelab Dockerisé : **Duplicati**. Parce que l'interface web est intuitive, l'image Docker est officielle, et tu peux configurer une sauvegarde planifiée sans écrire un script shell. Restic et Borg sont plus puissants mais demandent de la patience. rsync n'est pas un vrai système de backup : pas de versions, pas de chiffrement, pas de compression native.

## Prérequis

- Un serveur Linux avec Docker et Docker Compose installés.
- Un dossier source contenant les données à sauvegarder (volumes Docker, dossiers hôte, etc.).
- Une destination de stockage : local, NAS, ou service cloud compatible.
- Un mot de passe solide pour le chiffrement (garde-le dans ton gestionnaire de mots de passe).

## Installation avec Docker Compose

Crée un dossier dédié et le fichier `docker-compose.yml` :

```yaml
services:
  duplicati:
    image: duplicati/duplicati:latest
    container_name: duplicati
    restart: unless-stopped
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/Paris
      - DUPLICATI__WEBSERVICE_PASSWORD=change_moi_maintenant
      - DUPLICATI__DISABLE_UPDATE_NOTIFICATION=true
    volumes:
      - ./config:/config
      - /path/to/your/data:/source/data:ro
      - /var/lib/docker/volumes:/source/docker-volumes:ro
    ports:
      - "8200:8200"
```

Quelques explications :

- `PUID` / `PGID` : adapte à l'utilisateur propriétaire de tes données (`id $USER` pour connaître les valeurs).
- `/source/data` : monte en lecture seule (`:ro`) les dossiers à sauvegarder. Tu peurs ajouter autant de volumes que nécessaire.
- `/source/docker-volumes` : astuce utile pour sauvegarder les volumes nommés Docker depuis `/var/lib/docker/volumes` (nécessite souvent root).
- `DUPLICATI__WEBSERVICE_PASSWORD` : définis un mot de passe pour protéger l'interface web. Par défaut, Duplicati n'en demande pas. Ne laisse jamais le port 8200 exposé sur Internet sans mot de passe ou sans VPN/reverse-proxy.

Lance le conteneur :

```bash
cd /opt/duplicati
docker compose up -d
```

L'interface web est accessible sur `http://<ip-serveur>:8200`. Si tu utilises un reverse proxy comme Traefik ou Nginx Proxy Manager, ajoute une route sécurisée avec authentification basique ou whitelist IP.

## Configuration de la première sauvegarde

Lance l'assistant « Ajouter une sauvegarde » depuis le tableau de bord. Les étapes suivent une logique simple :

**1. Sélection des données**
Coche les dossiers montés dans `/source/`. Si tu as exposé `/var/lib/docker/volumes`, tu peux sélectionner les volumes nommés un par un. Évite de sauvegarder le dossier `config` de Duplicati lui-même vers la même destination, cela crée des boucles inutiles.

**2. Destination du stockage**
Choisis le protocole : S3, SFTP, WebDAV, Google Drive, Backblaze B2, Wasabi, SMB… Renseigne tes identifiants ou tes clés API. Duplicati te propose un test de connexion avant de valider. Ne néglige pas cette étape, elle évite les backups fantômes.

**3. Planification**
Définis la fréquence : quotidienne, hebdomadaire ou personnalisée via une syntaxe cron. Pour un homelab, une sauvegarde incrémentale quotidienne à 2h du matin est un bon compromis. Les incrémentales ne transfèrent que les blocs modifiés, ce qui économise la bande passante et l'espace distant.

**4. Règles de rétention**
Paramètre clé : combien de versions conserver ? Une politique simple et efficace :

- Conserver toutes les versions pendant 1 mois.
- Conserver une version par semaine pendant 3 mois.
- Conserver une version par mois pendant 1 an.

Cela te donne un historique fin pour les restore récents et une couverture long terme sans exploser la taille du stockage.

**5. Chiffrement**
Coche « Chiffrement AES-256 » et choisis un mot de passe robuste (20+ caractères, mélange de lettres, chiffres, symboles). Ce mot de passe est la clé de voûte : si tu le perds, tes backups sont irrécupérables. Stocke-le dans ton gestionnaire de mots de passe préféré.

## Les backends supportés

Duplicati n'impose aucun écosystème. Voici les destinations les plus courantes :

| Destination | Avantage | Inconvénient |
|-------------|----------|--------------|
| **SFTP / SSH** | Natif sur tout serveur Linux | Nécessite une machine distante toujours allumée |
| **SMB / CIFS** | Parfait pour un NAS domestique | Pas de chiffrement réseau natif (sauf VPN) |
| **S3 (MinIO, AWS)** | Standard cloud, scalable | Coût si volume élevé sur AWS |
| **Backblaze B2** | Prix très bas (0,005 $/Go/mois) | Nécessite des clés API |
| **Wasabi** | Pas de frais de sortie | Engagement 90 jours minimum |
| **Google Drive** | Pratique si tu as de l'espace | Limite API, dépendance Google |
| **WebDAV** | Compatible Nextcloud, ownCloud | Plus lent que S3 ou SFTP |
| **Local / USB** | Gratuit, offline | Pas redondant, risque physique |

Mon conseil : combine un stockage local (NAS ou disque USB monté sur le serveur) avec un stockage distant (Backblaze B2 ou un serveur SFTP chez un hébergeur). Règle de l'3-2-1 : trois copies, deux supports, un hors site.

## Restauration et vérification d'intégrité

Duplicati intègre un outil de restauration dans l'UI. Tu naviques dans les versions, tu coches les fichiers ou dossiers à récupérer, tu choisis la destination (originale ou nouvelle) et tu lances. C'est aussi simple qu'un gestionnaire de fichiers.

Ne te contente pas de configurer : teste ta restauration. Une sauvegarde non testée est une loterie. Prévois une restauration mensuelle d'un fichier aléatoire pour vérifier que le backup n'est pas corrompu et que le mot de passe fonctionne.

Duplicati génère également des rapports d'intégrité (`test` et `verify`) que tu peux automatiser. Dans l'onglet Avancé, active les notifications par email ou webhook si un backup échoue. Un backup silencieux qui ne tourne plus, c'est le cauchemar de tout admin.

## Astuces et pièges à éviter

**Volume des conteneurs Docker :** si tu sauvegardes `/var/lib/docker/volumes` en root, assure-toi que le conteneur Duplicati tourne avec les bonnes permissions. Sinon, monte les volumes explicitement dans `docker-compose.yml`.

**Backup de la base de données :** si tu sauvegardes une base PostgreSQL ou MariaDB utilisée par Nextcloud ou Vaultwarden, ne copie pas les fichiers bruts pendant que la base est active. Utilise un pre-backup script (pg_dump, mysqldump) ou les outils natifs de Duplicati pour exécuter des commandes avant/après le backup.

**Exposition du port 8200 :** ne met jamais Duplicati en face d'Internet sans mot de passe, sans VPN ou sans reverse proxy avec authentification. L'interface permet de lire, restaurer et supprimer des backups. C'est une cible idéale.

**Mise à jour de l'image :** Duplicati prévient quand une nouvelle version est disponible. Avec Docker, il suffit de faire :

```bash
docker compose pull
docker compose up -d
```

**Nommage des jobs :** donne des noms explicites à tes sauvegardes (« Backup Nextcloud Quotidien », « Backup Docker Volumes Hebdo ») pour t'y retrouver quand tu as dix jobs qui tournent.

## Conclusion

Duplicati est l'outil de backup qu'il manquait à ton stack Docker. Il est open-source, chiffré, polyvalent et suffisamment simple pour ne pas te demander un doctorat en administration système. L'image Docker officielle est à jour, la communauté est active et les fonctionnalités couvrent 95 % des besoins d'un homelab.

Installe-le ce weekend. Configure une sauvegarde vers ton NAS et une autre vers un cloud froid. Teste une restauration. Et dors enfin tranquille, sachant que ton Vaultwarden, ton Nextcloud et tes données Docker sont à l'abri. Si tu cherches une solution pour héberger tes propres photos sans passer par Google, j'ai testé [PhotoPrism](/photoprism-docker-galerie-photo/) — la reconnaissance faciale est bluffante.

Questions ou configs avancées ? Les commentaires sont ouverts.
