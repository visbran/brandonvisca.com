---
title: "Memos Docker : ton bloc-notes auto-hébergé (alternative à Google Keep)"
description: "Guide memos docker complet : installe Memos avec Docker Compose pour des notes rapides auto-hébergées, Markdown natif, et alternative à Google Keep."
pubDatetime: "2026-06-17T08:00:00.000Z"
modDatetime: "2026-06-17T08:00:00.000Z"
author: Brandon Visca
tags:
  - docker
  - auto-hebergement
  - intermediaire
  - productivite
  - notes
featured: false
draft: false
focusKeyword: memos docker
ogImage: "" 
---
> 💡 **TL;DR**
> - Memos est un bloc-notes auto-hébergé ultra-léger, open-source et pensé pour les notes rapides
> - Tu le déploies en 3 minutes avec Docker Compose (SQLite intégré, zéro dépendance externe)
> - Support Markdown natif, tags, recherche full-text, partage public/privé et API REST
> - Parfait remplaçant auto-hébergé à Google Keep pour les geeks et les homelabs
> - Docker Compose complet, tableau comparatif et reverse proxy inclus ci-dessous

## Table des matières

## Pourquoi un bloc-notes auto-hébergé en 2026 ?

Tu connais ce moment. Tu viens de résoudre un bug obscure sur ton serveur, tu as trouvé la commande exacte qui marche, et tu te dis "je vais noter ça quelque part pour la prochaine fois". Tu ouvres Google Keep, tu colles ta commande, tu ajoutes un titre rapide. Six mois plus tard, tu cherches cette note. Google Keep te propose trois résultats qui n'ont rien à voir, une recette de cookies et une liste de courses de 2023. Ta commande est perdue dans le chaos algorithmique.

Le problème des notes cloud SaaS, c'est triple. D'abord, tes données ne sont pas vraiment à toi : elles vivent sur des serveurs américains, soumises à des politiques de confidentialité qui changent chaque trimestre. Ensuite, la recherche est conçue pour le grand public, pas pour des snippets techniques : elle ignore la syntaxe, les flags de commande et les chemins de fichiers. Enfin, l'interface est pensée pour des listes de courses, pas pour des blocks de code avec coloration syntaxique.

Memos est la réponse minimaliste à ce problème. C'est un bloc-notes auto-hébergé développé par l'équipe usememos, sous licence MIT, avec plus de 30 000 stars sur GitHub. L'approche est radicalement simple : une interface web propre, du Markdown natif, des tags, une recherche rapide, et zéro complexité inutile. Tu l'installes sur ton serveur, tes notes restent chez toi, et personne ne te facture à la tête d'utilisateur.

Dans mon [guide des services essentiels à auto-héberger](/docker-debutant-services-auto-heberger/), je recommande de commencer par les outils de productivité. Memos est celui que je déploie systématiquement après Vaultwarden et Nextcloud : il coûte quasi rien en ressources, il est instantanément utile, et il remplace une dépendance Google ou Apple en moins de temps qu'il ne faut pour dire "iCloud Sync".

## Qu'est-ce que Memos exactement ?

Memos n'est pas un wiki. Ce n'est pas une base de connaissances structurée. Ce n'est pas un Notion-like avec des bases de données relationnelles. C'est un bloc-notes. Un vrai. Tu ouvres l'interface, tu écris, tu tagues, tu publies ou tu gardes privé. Point barre.

Voici ce qu'il propose concrètement :

- **Éditeur Markdown natif** : tu écris en Markdown pur, avec prévisualisation live. Les blocs de code ont la coloration syntaxique automatique. Les images sont drag-and-drop. C'est instantané.
- **Tags** : un système de tags simple et puissant. `#docker`, `#nginx`, `#backup`, `#procédure`. Tu retrouves tout en deux clics.
- **Recherche full-text** : rapide, pertinente, qui cherche dans le contenu Markdown, les tags et les dates. Pas d'algorithme magique, juste une recherche qui fonctionne.
- **Partage public/privé** : chaque note peut être privée (visible que par toi) ou publique avec une URL partageable. C'est pratique pour envoyer une procédure à un collègue sans lui donner accès à tout ton bloc-notes.
- **Multi-utilisateur** : tu peux créer plusieurs comptes utilisateurs avec des espaces séparés. Parfait pour partager un serveur entre famille ou équipe sans mélanger les notes.
- **API REST complète** : pour automatiser la création de notes depuis tes scripts, tes pipelines CI/CD ou tes outils de monitoring.
- **Webhooks** : pour déclencher des actions externes à chaque nouvelle note (notification Slack, sync vers Git, etc.).
- **SQLite intégré** : pas besoin de PostgreSQL, MariaDB ou Redis. La base est un simple fichier SQLite dans un volume Docker. C'est ça qui rend Memos si léger.
- **Import/Export** : exporte toutes tes notes au format Markdown compressé (ZIP). Importe depuis d'autres outils en convertissant simplement en fichiers Markdown.
- **Thème clair/sombre** : parce qu'écrire une procédure à 2 h du matin sur fond blanc, c'est un crime contre l'humanité.

L'image Docker officielle `ghcr.io/usememos/memos:latest` est maintenue activement. Elle supporte amd64 et arm64. La taille de l'image est ridicule (~30 Mo), le démarrage est instantané, et la consommation mémoire tourne autour de 50 Mo au repos.

Si tu cherches un wiki structuré pour équipe avec des étagères, des livres et des permissions granulaires, [BookStack avec Docker](/bookstack-docker-wiki-equipe/) est beaucoup plus adapté. Si tu veux une base de connaissances collaborative avec un éditeur bloc type Notion, [Outline avec Docker](/outline-docker-wiki-auto-heberge/) est une alternative solide. Mais si ton besoin est juste de jeter des notes rapides, des commandes shell, des snippets de code et des idées sans y réfléchir, j'ai aussi couvert [Memos avec Docker](/memos-docker-notes-auto-heberge/), un bloc-notes auto-hébergé ultra-léger et minimaliste.

## Prérequis

- Un serveur Linux avec Docker et Docker Compose installés (Docker Engine 24+ recommandé)
- 1 cœur CPU et 256 Mo de RAM minimum (512 Mo recommandés pour être confortable)
- 1 Go d'espace disque pour le système, puis selon tes notes et tes images
- Un nom de domaine ou sous-domaine pointant vers ton serveur si tu veux HTTPS
- Un reverse proxy (Caddy, Traefik ou Nginx Proxy Manager) pour gérer les certificats SSL

Memos est ridiculement léger. Un Raspberry Pi Zero 2 W suffit pour une utilisation personnelle. Pour une petite équipe ou un usage intensif, un VPS de 1 cœur / 1 Go est largement confortable. C'est l'un des services Docker les plus économes en ressources que je connaisse.

Si tu débutes avec Docker et que tout ça te paraît flou, commence par mon article sur [les services essentiels à auto-héberger avec Docker](/docker-debutant-services-auto-heberger/). Il t'explique les bases de Docker Compose, les volumes, les reverse proxy et les bonnes pratiques. Une fois que tu as ces bases, Memos est un excellent premier service pour te faire la main.

## Déploiement Memos Docker avec Docker Compose

Crée un dossier dédié et un fichier `docker-compose.yml` :

```bash
mkdir -p ~/memos && cd ~/memos
```

Voici le Docker Compose complet et prêt à l'emploi :

```yaml
services:
  memos:
    image: ghcr.io/usememos/memos:latest
    container_name: memos
    volumes:
      - ./memos_data:/var/opt/memos
    ports:
      - "5230:5230"
    restart: unless-stopped
```

C'est tout. Pas de base de données externe, pas de cache Redis, pas de configuration d'environnement complexe. Juste un volume pour persister le fichier SQLite et un port exposé.

Lance le conteneur :

```bash
docker compose up -d
```

Attends 5 secondes que le service démarre, puis accède à `http://IP-du-serveur:5230`. Le premier utilisateur qui s'inscrit devient automatiquement administrateur.

### Avec un reverse proxy Caddy

Si tu utilises [Caddy avec Docker](/caddy-docker-reverse-proxy-guide/), ajoute simplement ce bloc dans ton Caddyfile :

```caddy
notes.tondomaine.com {
    reverse_proxy memos:5230
}
```

Caddy gère automatiquement les certificats Let's Encrypt. Pas de certbot, pas de renouvellement manuel.

### Avec Nginx Proxy Manager

Dans l'interface web de [Nginx Proxy Manager](/nginx-proxy-manager-docker-guide/) :
1. Ajoute un proxy host : `notes.tondomaine.com`
2. Forward hostname : `memos`
3. Forward port : `5230`
4. Active "Block Common Exploits" et "Request a new SSL Certificate"
5. Force SSL et HSTS

### Avec Traefik

Si tu utilises Traefik, ajoute ces labels au service dans ton docker-compose.yml :

```yaml
services:
  memos:
    image: ghcr.io/usememos/memos:latest
    container_name: memos
    volumes:
      - ./memos_data:/var/opt/memos
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.memos.rule=Host(`notes.tondomaine.com`)"
      - "traefik.http.routers.memos.entrypoints=websecure"
      - "traefik.http.routers.memos.tls.certresolver=letsencrypt"
    restart: unless-stopped
    networks:
      - traefik
```

## Configuration initiale et premiers pas

Une fois connecté pour la première fois, prends le temps de configurer ces éléments avant de remplir ton bloc-notes.

**1. Créer ton compte admin**
Le premier utilisateur inscrit est automatiquement admin. Choisis un email sérieux et un mot de passe fort. Active le 2FA dans les paramètres de sécurité si tu exposes Memos sur Internet.

**2. Définir ta structure de tags**
Avant de créer des notes, réfléchis à tes tags principaux. Voici ce que j'utilise personnellement :
- `#docker` : commandes, docker-compose, astuces conteneurs
- `#nginx` : config vhost, SSL, reverse proxy
- `#backup` : procédures de sauvegarde, scripts rsync
- `#procédure` : checklists, runbooks, étapes à suivre
- `#snippet` : bouts de code réutilisables
- `#idee` : idées d'articles, de projets, de tools à tester

Les tags sont le cœur de l'organisation dans Memos. Plus tu les utilises systématiquement, plus ta recherche devient efficace.

**3. Configurer les paramètres généraux**
Dans Paramètres > Système :
- change le nom de l'instance (ex: "Notes Homelab")
- active le thème sombre si tu préfères
- configure la langue (français disponible)
- active ou désactive l'inscription publique selon ton usage

**4. Créer les premières notes**
Commence par tes notes les plus consultées. Par exemple :
- "Commande Docker utiles" avec un bloc de code contenant `docker system prune -a`, `docker compose logs -f`, etc.
- "Procédure mise à jour serveur" avec les étapes dans l'ordre
- "Liste des ports utilisés" avec un tableau Markdown de tes services et leurs ports

**5. Tester le partage public**
Crée une note test, passe-la en public, copie l'URL de partage et vérifie qu'elle s'affiche correctement sans authentification. C'est utile pour partager des procédures avec des collègues ou la communauté.

## Memos vs les alternatives : tableau comparatif

|| Critère | Memos | Google Keep | Standard Notes | Joplin |
||---------|-------|-------------|----------------|--------|
|| **Licence** | MIT (open-source) | Propriétaire (Google) | AGPL-3.0 | MIT (open-source) |
|| **Auto-hébergé** | Oui | Non | Oui (payant pour sync) | Oui (gratuit) |
|| **Gratuit** | Totalement | Oui (avec pubs/tracking) | Basique gratuit | Totalement |
|| **Interface** | Minimaliste, Markdown | Cartes colorées, visuel | Texte brut, austère | Rich text + Markdown |
|| **Support Markdown** | Natif et principal | Non | Natif | Natif + WYSIWYG |
|| **Coloration syntaxique** | Oui | Non | Non | Oui |
|| **Tags** | Oui, simples et rapides | Oui (labels couleur) | Oui | Oui |
|| **Recherche** | Full-text rapide | Algorithme Google | Full-text chiffré | Full-text locale |
|| **Partage public** | Oui (URL par note) | Oui (collaboration) | Non | Non (synchro Joplin Cloud) |
|| **API REST** | Oui | Non (Google Keep API limitée) | Non | Non |
|| **Base de données** | SQLite intégrée | Cloud Google | Local chiffrée | Local SQLite |
|| **Ressources RAM** | ~50 Mo | N/A (cloud) | ~100 Mo | ~200 Mo |
|| **App mobile** | Web responsive (PWA) | Native iOS/Android | Native iOS/Android | Native iOS/Android |
|| **Export** | Markdown ZIP | Google Takeout | Markdown/JSON | Markdown/JEX |
|| **Facilité d'usage** | Très intuitive | Très intuitive | Technique (chiffrement) | Bonne |

Mon verdict pour un homelab ou une utilisation technique :

- **Memos** : le meilleur compromis entre légèreté, souveraineté et simplicité. Markdown natif, API REST, partage public, SQLite intégré. C'est mon choix par défaut pour des notes rapides auto-hébergées.
- **Google Keep** : si tu n'as pas de serveur et que tu t'en fiches de la confidentialité. L'interface est sympa pour des listes de courses, mais c'est inutile pour du technique.
- **Standard Notes** : excellent si le chiffrement de bout en bout est ta priorité absolue. Mais l'interface est austère, la sync auto-hébergée est payante, et il n'y a pas de partage public.
- **Joplin** : très complet avec le plugin ecosystem, l'éditeur riche et le Web Clipper. Parfait pour des notes longues et structurées. Mais il est plus lourd, plus complexe à auto-héberger (besoin de Joplin Server pour la sync), et l'interface est moins agréable pour des notes rapides.

Pour stocker tes mots de passe, [Vaultwarden avec Docker](/vaultwarden-docker-gestionnaire-mots-de-passe/) reste l'indispensable complément. Pour gérer tes bookmarks, [Linkding avec Docker](/linkding-docker-bookmarks/) fait le job. Memos complète cette stack productivité auto-hébergée par la prise de notes rapide.

## Sécuriser l'accès et les données

Un bloc-notes contient souvent des informations sensibles : mots de passe temporaires, commandes d'accès, procédures internes. Voici les mesures de base à appliquer.

**HTTPS partout**
Ne laisse jamais Memos en HTTP si tu l'exposes sur Internet. Ton reverse proxy doit forcer le HTTPS, activer HSTS et bloquer les versions obsolètes de TLS. Caddy le fait nativement. Avec Traefik ou NPM, c'est un simple toggle.

**Sauvegardes automatisées**
Le volume `./memos_data` contient le fichier SQLite et les fichiers uploadés. C'est un simple dossier à sauvegarder :

```bash
#!/bin/bash
# backup-memos.sh
DATE=$(date +%Y%m%d_%H%M%S)
tar czf "/backup/memos_$DATE.tar.gz" ~/memos/memos_data
```

Si tu veux une solution plus complète, [Duplicati avec Docker](/duplicati-docker-sauvegarde/) peut sauvegarder ce volume chiffré vers un stockage cloud ou un NAS.

**Mises à jour**
L'équipe Memos publie des mises à jour régulières. Mets à jour une fois par semaine :

```bash
cd ~/memos
docker compose pull
docker compose up -d
```

**Fail2ban**
Si tu exposes Memos sur Internet, protège-toi contre les attaques par force brute sur la page de connexion. [Fail2ban avec Docker](/fail2ban-docker-securite-serveur/) peut surveiller les logs du reverse proxy et bannir les IP abusives après cinq tentatives ratées.

**Authentification double facteur**
Memos supporte le TOTP (Google Authenticator, Authy, Bitwarden Authenticator, etc.). Active-le dans les paramètres de sécurité dès que possible.

**Restreindre les inscriptions**
Par défaut, n'importe qui peut s'inscrire si ton instance est publique. Désactive l'inscription publique dans les paramètres système et crée les comptes utilisateurs toi-même.

## Intégrations et astuces avancées

**Brancher un webhook Slack/Discord**
Dans les paramètres de Memos, configure un webhook vers ton channel Discord ou Slack. Chaque nouvelle note publique déclenche une notification. C'est pratique pour partager automatiquement des procédures avec l'équipe.

**Automatiser avec l'API REST**
L'API de Memos est simple et documentée. Voici un exemple en Python pour créer une note depuis un script :

```python
import requests

API_URL = "https://notes.tondomaine.com/api/v1/memos"
TOKEN = "ton-api-token"

memo = {
    "content": "# Procédure de backup\n\n```bash\nrsync -avz /data /backup\n```",
    "visibility": "PRIVATE"
}

response = requests.post(
    API_URL,
    headers={"Authorization": f"Bearer {TOKEN}"},
    json=memo
)
print(response.json())
```

Tu peux générer un token API dans les paramètres utilisateur de Memos.

**Utiliser comme PWA sur mobile**
Memos est une webapp responsive. Sur iOS ou Android, ouvre Memos dans Safari/Chrome, ajoute-le à l'écran d'accueil. Il se comporte comme une application native avec une interface adaptée au mobile.

**Importer depuis Google Keep**
Exporte tes notes Google Keep via Google Takeout (format HTML/JSON). Convertis-les en fichiers Markdown avec un script Python ou un outil comme `keep-to-markdown`, puis importe-les dans Memos. Le processus n'est pas natif, mais c'est faisable en une heure de scripting.

**Lier avec un gestionnaire de fichiers**
Pour les pièces jointes lourdes ou les archives de documents, [File Browser avec Docker](/filebrowser-docker-gestionnaire-fichiers/) s'intègre bien à côté de Memos. Tu stockes les fichiers dans File Browser et tu références les liens dans tes notes Memos.

**Personnalisation CSS**
Memos permet d'injecter du CSS personnalisé via les paramètres d'administration. Tu peux ajuster la typographie, les couleurs, ou masquer des éléments que tu ne souhaites pas afficher.

## FAQ

**Puis-je utiliser PostgreSQL à la place de SQLite ?**
Non, Memos utilise exclusivement SQLite. C'est un choix architectural délibéré pour maintenir la simplicité et la légèreté. Si tu as besoin d'une base PostgreSQL, regarde du côté de Outline ou Wiki.js.

**Est-ce que Memos gère les images et les pièces jointes ?**
Oui. Les fichiers uploadés sont stockés dans le volume `/var/opt/memos` du conteneur. Tu peux uploader des images, des PDF, des archives directement dans une note.

**Peut-on écrire en Markdown étendu ?**
Memos supporte le Markdown standard (CommonMark) avec des extensions pour les tableaux, les blocs de code avec coloration syntaxique, et les tâches checklists. Pas de Mermaid ou de LaTeX natif pour l'instant.

**Le service est-il accessible hors ligne ?**
Memos est une webapp. Si tu l'héberges en local sans exposition publique, il est accessible depuis ton réseau local. Pour un accès distant hors ligne, il te faut un VPN (WireGuard) ou une exposition HTTPS publique via reverse proxy.

**Puis-je migrer mes notes vers un autre outil ?**
Oui, l'export ZIP de Memos contient tes notes au format Markdown brut. Tu peux les importer dans Joplin, Obsidian, ou tout autre outil compatible Markdown en quelques minutes.

**Memos est-il traduit en français ?**
Oui, l'interface est entièrement traduite en français. La langue se change dans les paramètres utilisateur ou globaux.
