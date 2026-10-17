---
title: "Filestash Docker : navigateur de fichiers web universel"
description: "Filestash Docker : déploie ce navigateur de fichiers universel qui connecte S3, FTP, SFTP, WebDAV et Google Drive depuis une interface unique."
pubDatetime: "2026-10-17T23:48:31+02:00"
modDatetime: "2026-10-17T08:00:00.000Z"
author: Brandon Visca
tags:
  - docker
  - auto-hebergement
  - stockage
  - intermediaire
featured: false
draft: false
focusKeyword: filestash docker
faqs:
  - question: "Filestash Docker est-il gratuit à utiliser ?"
    answer: "Oui, l'édition communautaire est open source sous licence AGPL-3.0, sans limite d'utilisateurs ni clé de licence. Filestash propose aussi une offre entreprise payante avec SSO, support et plugins sur mesure, réservée aux structures qui en ont besoin."
  - question: "Comment éviter qu'un inconnu prenne le contrôle admin au premier démarrage ?"
    answer: "La page /admin/setup accepte le premier visiteur comme administrateur. Fixe le mot de passe via la variable ADMIN_PASSWORD avant de lancer le conteneur, ou garde le port sur 127.0.0.1 et passe par un tunnel SSH tant que ce n'est pas fait."
  - question: "Filestash remplace-t-il File Browser ou Nextcloud ?"
    answer: "Pas vraiment le même usage. File Browser et Nextcloud hébergent et stockent eux-mêmes les fichiers, alors que Filestash sert de passerelle unifiée vers des stockages déjà existants comme S3, FTP, SFTP ou Google Drive, sans dupliquer les données."
---
> 💡 **TL;DR**
> - Filestash Docker est un navigateur de fichiers web qui se connecte à des stockages déjà existants (S3, FTP, SFTP, WebDAV, SMB, Google Drive, Git) au lieu d'en créer un nouveau
> - Installation en deux commandes avec le docker-compose.yml officiel, image `machines/filestash`, port 8334
> - Édition communautaire gratuite sous AGPL-3.0, sans limite d'utilisateurs, avec une offre entreprise en option
> - Un piège de sécurité à connaître absolument : la page `/admin/setup` donne le contrôle admin au premier visiteur

Tu as combien d'outils différents pour accéder à tes fichiers en ce moment ? Un client FTP pour le VPS, l'appli Google Drive sur le bureau, l'explorateur Windows pour le partage SMB du NAS, et peut-être un onglet Nextcloud ouvert en permanence pour le reste. Chez moi, c'était exactement ça jusqu'à ce que je tombe sur Filestash Docker : une seule interface web qui se branche directement sur tout ce que j'avais déjà, sans copier un seul fichier ailleurs.

## Table des matières

## Filestash, le navigateur de fichiers universel

Filestash est développé par Mickael Kerjean et publié sous licence AGPL-3.0 sur GitHub (`mickael-kerjean/filestash`). La différence avec la plupart des gestionnaires de fichiers web, c'est que Filestash ne stocke rien lui-même. Il se positionne comme un client auto-hébergé qui se connecte à des backends existants : ton bucket S3, ton serveur SFTP, ton partage SMB, ton compte Google Drive, ton dépôt Git.

Concrètement, ça veut dire que tu ne migres aucune donnée. Tu donnes à Filestash Docker les identifiants d'accès à un stockage qui existe déjà, et il t'affiche une interface de navigation moderne par-dessus, avec prévisualisation, upload, renommage, partage de liens. Si tu connais File Browser ou FileBrowser Quantum, la logique est différente : ces outils hébergent un dossier local qu'ils gèrent eux-mêmes, alors que Filestash Docker fait office de passerelle vers des sources de données qui restent où elles sont.

L'édition communautaire tourne sans clé de licence et sans limite d'utilisateurs. Le projet propose aussi une offre entreprise payante, avec authentification SSO, support commercial et plugins de stockage sur mesure, réservée aux équipes qui en ont vraiment besoin. Pour un homelab ou une petite structure, l'édition gratuite couvre largement le besoin.

## Les backends supportés par Filestash Docker

C'est le vrai argument de vente. Filestash embarque une vingtaine de connecteurs de stockage, activables un par un selon ton besoin :

- **Stockage objet et cloud** : S3 (et compatibles comme MinIO ou Backblaze), Azure Blob, Dropbox, Google Drive, Storj
- **Protocoles réseau classiques** : FTP, FTPS, SFTP, WebDAV, SMB, NFS, IPFS
- **Forges Git** : dépôts Git bruts, GitHub, GitLab, Gitea, Gogs
- **Autres** : LDAP, CalDAV, CardDAV, MySQL, SharePoint, Artifactory

Si tu héberges déjà ton code sur une instance [GitLab CE auto-hébergée](/gitlab-ce-docker-forge-cicd-complete/), le backend Git de Filestash s'y connecte directement : tu navigues dans tes dépôts depuis la même interface que tes autres fichiers, sans ouvrir un deuxième onglet.

Chaque backend se configure séparément depuis l'interface web de connexion, et tu peux en activer plusieurs en même temps. Un utilisateur peut donc se connecter à son compte S3 pendant que l'admin configure l'accès SMB pour une autre équipe, sans que les deux se gênent.

Filestash peut aussi fonctionner dans l'autre sens, en exposant tes fichiers via SFTP, S3, FTP, WebDAV ou MCP comme passerelle vers l'extérieur. C'est une fonctionnalité plus avancée, utile si tu veux donner un accès standardisé à un stockage qui n'en propose pas nativement, mais pas indispensable pour un usage de navigateur de fichiers classique.

## Installation de Filestash Docker avec Docker Compose

Crée un dossier dédié et récupère le fichier Compose officiel :

```bash
mkdir ~/filestash && cd ~/filestash
curl -O https://downloads.filestash.app/latest/docker-compose.yml
```

Le fichier ressemble à ceci :

```yaml
services:
  app:
    image: machines/filestash:latest
    restart: unless-stopped
    ports:
      - "8334:8334"
    volumes:
      - app-data:/app/data/state/

volumes:
  app-data:
```

Avant de lancer quoi que ce soit, lie les ports à la boucle locale pour éviter d'exposer Filestash sur toutes les interfaces réseau dès le premier démarrage :

```bash
sed -i 's/"8334:8334"/"127.0.0.1:8334:8334"/' docker-compose.yml
docker compose up -d
```

Toute la configuration de Filestash (connexions configurées, base SQLite, plugins activés) vit dans le volume monté sur `/app/data/state/`. C'est le seul répertoire à sauvegarder si tu veux pouvoir restaurer ton instance après un crash disque.

Si tu gères déjà plusieurs stacks Compose sur ton serveur, ajouter celle-ci à [Dockge](/dockge-docker-gestionnaire-stacks-compose/) t'évite de retaper les mêmes commandes SSH à chaque mise à jour d'image.

💡 Le projet propose en option un conteneur Collabora (`collabora/code`) sur le port 9980 pour éditer des documents Office directement dans le navigateur, sans quitter Filestash. C'est un plus confortable, mais totalement facultatif pour une simple navigation de fichiers.

## Sécuriser l'accès admin de Filestash

⚠️ Voici le point le plus important de cet article, et celui que la plupart des guides passent sous silence : Filestash n'a pas de mot de passe admin par défaut. La page `/admin/setup` attend simplement que quelqu'un s'y connecte pour devenir administrateur. Si ton port est accessible et que tu n'as pas encore configuré ce mot de passe, le premier visiteur, toi ou quelqu'un d'autre, prend le contrôle total de l'instance.

Deux façons de régler ça proprement.

### Fixer le mot de passe via une variable d'environnement

C'est l'option la plus sûre, puisqu'elle ne dépend pas d'une course de vitesse sur la page de configuration. Génère un hash bcrypt de ton mot de passe :

```bash
printf '%s' "TonMotDePasseSolide" | htpasswd -niBC 10 "" | tr -d ':\n' | sed 's/\$/$$/g'
```

La commande double chaque `$` du hash, nécessaire pour que Docker Compose ne les interprète pas comme des variables. Colle le résultat dans le service `app` de ton `docker-compose.yml` :

```yaml
    environment:
      - ADMIN_PASSWORD=<hash-bcrypt-ici>
```

Filestash applique cette variable à chaque démarrage. Un mot de passe changé depuis la console sera donc écrasé au redémarrage suivant si la variable reste définie, ce qui est plutôt une bonne nouvelle pour garder le contrôle.

### Passer par un tunnel SSH en attendant

Tant que le port reste lié à `127.0.0.1`, personne depuis l'extérieur ne peut atteindre `/admin/setup`. Ouvre un tunnel depuis ton poste pour configurer l'instance en toute tranquillité :

```bash
ssh -L 8334:127.0.0.1:8334 utilisateur@ton-serveur
```

Puis ouvre `http://127.0.0.1:8334/admin` dans ton navigateur local, fixe le mot de passe, et seulement après ça, décide si tu veux exposer Filestash plus largement derrière un reverse proxy TLS comme Caddy ou Nginx Proxy Manager.

## Filestash Docker vs File Browser et Nextcloud : lequel choisir

| Critère | Filestash Docker | File Browser | Nextcloud |
|---|---|---|---|
| Stocke les fichiers lui-même | Non, passerelle vers un backend existant | Oui, dossier local monté | Oui, base complète |
| Nombre de backends supportés | ~20 (S3, FTP, SFTP, SMB, Git, Drive...) | 1 (le dossier local) | Stockage local + quelques apps externes |
| Édition de documents Office | Oui, via Collabora en option | Non | Oui, intégrée |
| Licence | AGPL-3.0, édition entreprise payante | MIT | AGPL-3.0 |
| Ressources | Léger, une image Go | Très léger, ~20 Mo RAM | Lourd, PHP + base de données |

Mon avis après avoir testé les trois côte à côte : si tu veux centraliser l'accès à des stockages qui existent déjà un peu partout (un bucket S3 chez un fournisseur, un vieux serveur FTP, un compte Google Drive, ton NAS en SMB), Filestash Docker fait exactement ce travail-là et rien d'autre. File Browser reste plus simple si tu veux juste exposer un seul dossier local. Nextcloud garde l'avantage pour la collaboration complète (calendrier, contacts, édition partagée), au prix d'une infrastructure plus lourde.

## Cas d'usage concrets

### Centraliser l'accès à plusieurs stockages pour une petite équipe

Tu as un bucket S3 pour les sauvegardes, un serveur SFTP chez un prestataire et un dossier partagé en SMB sur le NAS du bureau. Plutôt que de distribuer trois clients différents à ton équipe, tu configures les trois connexions dans Filestash et chacun retrouve ses accès depuis la même interface web, avec ses propres permissions.

### Donner un accès lecture aux documents d'une autre application sans ouvrir son interface

Si tu fais tourner [Paperless-ngx](/paperless-ngx-docker-guide-auto-hebergement/) pour numériser tes documents administratifs, son dossier de stockage reste accessible en SMB ou en montage local. Brancher ce dossier sur Filestash te donne un accès de secours en lecture, pratique quand tu veux juste vérifier un fichier sans ouvrir toute l'interface OCR de Paperless-ngx.

### Remplacer un accès FTP legacy sans toucher au serveur en place

Certains hébergeurs ou prestataires n'exposent encore que du FTP brut. Plutôt que de forcer tout le monde à réinstaller un client FTP sur chaque poste, tu connectes ce FTP à Filestash et tout le monde navigue depuis un navigateur, avec HTTPS devant si tu mets un reverse proxy.

## Dépannage rapide

**Je n'arrive plus à configurer l'admin, quelqu'un d'autre a pris la main**

Si personne n'a fixé `ADMIN_PASSWORD` et qu'un visiteur indésirable a validé `/admin/setup` avant toi, la seule solution propre est de couper le conteneur, supprimer le contenu du volume d'état, puis relancer avec la variable d'environnement définie cette fois dès le départ :

```bash
docker compose down
docker volume rm filestash_app-data
docker compose up -d
```

Tu perds les connexions déjà configurées, donc autant fixer `ADMIN_PASSWORD` avant ce deuxième essai.

**Une connexion à un backend échoue**

Vérifie d'abord que le conteneur peut atteindre le service cible depuis l'intérieur de son réseau Docker, pas seulement depuis ta machine. Un pare-feu ou un groupe de sécurité qui bloque le trafic sortant du serveur est la cause la plus fréquente, bien avant un mauvais mot de passe.

**Je veux suivre ce qui se passe en temps réel**

```bash
docker compose logs -f app
```

Si tu fais tourner plusieurs conteneurs sur le même serveur et que tu veux une vue d'ensemble sans jongler entre les `docker compose logs` de chaque stack, [Dozzle](/dozzle-docker-visionneuse-logs-web/) te donne cette visibilité centralisée en quelques minutes d'installation.

## Conclusion

Filestash Docker ne remplace ni ton NAS, ni ton stockage S3, ni ton serveur FTP. Il se contente de leur donner une seule porte d'entrée commune, propre et moderne, sans dupliquer la moindre donnée. C'est exactement ce qu'il faut quand tes fichiers sont déjà éparpillés sur trois protocoles différents et que tu en as assez de jongler entre les clients.

Deux commandes pour l'installer, une variable d'environnement à ne surtout pas oublier pour le mot de passe admin, et tu as une interface unifiée pour accéder à tout ce que tu héberges déjà. Prends juste cinq minutes pour sécuriser `/admin/setup` avant d'exposer le port, le reste suit tout seul.
