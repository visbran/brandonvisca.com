---
title: "Code Server Docker : VS Code dans ton navigateur auto-hébergé"
description: "Guide code server docker : déploie VS Code auto-hébergé dans ton navigateur. Docker Compose, sécurité et reverse proxy inclus."
pubDatetime: "2026-08-12T08:00:00.000Z"
modDatetime: "2026-08-12T08:00:00.000Z"
author: Brandon Visca
tags:
  - debutant
  - auto-hebergement
  - docker
  - vscode
  - productivite
featured: false
draft: false
focusKeyword: code server docker
ogImage: ""
---
> 💡 **TL;DR**
> - Code-Server projette VS Code dans ton navigateur : mêmes extensions, mêmes raccourcis, zéro installation locale
> - Une image Docker officielle, un volume pour tes projets, et tu codes depuis n'importe quel appareil
> - Parfait pour coder sur une tablette, un Chromebook, ou depuis un serveur headless sans bureau graphique
> - Docker Compose complet + sécurité + reverse proxy inclus ci-dessous

## Pourquoi Code-Server en 2026 ?

Tu as un serveur auto-hébergé. Une machine headless dans un coin, un VPS pas cher, ou un Raspberry Pi 4. Tu veux y coder sans installer X11, sans VNC qui rame, sans SSH -X qui te fait pleurer devant un terminal qui freeze à chaque caractère tapé.

**Code-Server** résout ce problème. C'est VS Code (le vrai, pas une imitation) compilé pour tourner dans un navigateur web. Tu ouvres une URL, tu as ton éditeur avec tes extensions, tes thèmes, ton terminal intégré, et tes projets montés directement depuis le serveur.

Le projet est maintenu par Coder (la boîte derrière Coder/coder), avec plus de 70 000 stars sur GitHub, des mises à jour régulières et une image Docker officielle multi-architecture (amd64, arm64). C'est du VS Code open-source (code-server) servi via un serveur web Node.js, pas un émulateur ou un bidouillage Electron.

Dans mon [guide auto-hébergement complet](/auto-hebergement-guide-complet-2025/), je recommande toujours d'avoir un environnement de développement accessible depuis n'importe où. Code-Server, c'est exactement ça. Pas besoin d'installer VS Code sur chaque machine, pas besoin de synchroniser les extensions, pas de "ça marche sur mon Mac mais pas sur le PC du boulot".

## Qu'est-ce que Code-Server exactement ?

Code-Server prend le cœur de VS Code (le moteur Monaco, le système d'extensions, le terminal intégré) et l'embarque dans une application web. Voici ce que tu obtiens concrètement :

- **Éditeur VS Code complet** : IntelliSense, coloration syntaxique, snippets, multi-curseur, refactoring. C'est le même moteur que l'application de bureau.
- **Extensions du marketplace** : tu installes Prettier, ESLint, Python, Docker, GitLens, copilot, exactement comme en local. Certaines extensions avec composants natifs (type live share avec audio) sont limitées, mais 95 % fonctionnent.
- **Terminal intégré** : un vrai shell bash/zsh/fish dans un panel en bas. Tu compiles, tu lances des scripts, tu gères Git, tout sans quitter l'onglet.
- **Port forwarding** : tu lances un serveur de dev sur le port 3000 dans le terminal, Code-Server te génère une URL locale ou publique pour le voir dans un navigateur.
- **Git intégré** : staging, commit, push, pull, gestion des branches, résolution de conflits. Tout via l'interface VS Code standard.
- **Workspace persistant** : tes paramètres utilisateur, tes extensions installées et ton layout d'interface sont sauvegardés. Tu reconnectes, c'est exactement comme tu l'as laissé.

L'image Docker officielle `codercom/code-server:latest` inclut tout le runtime Node.js nécessaire, le serveur web et VS Code prépackagé. Tu montes tes projets via volume, tu choisis ton mot de passe, et tu bosses.

## Code-Server vs les alternatives : tableau comparatif

| Outil | VS Code natif | Interface web | Docker officiel | Terminal intégré | Extensions | Ressources |
|-------|---------------|---------------|-----------------|-------------------|------------|------------|
| **Code-Server** | Oui (code OSS) | Oui | Oui (`codercom/code-server`) | Oui | 95 % du marketplace | ~256 Mo RAM |
| **Gitpod** | Oui | Oui | Non (SaaS) | Oui | Oui | SaaS payant |
| **GitHub Codespaces** | Oui | Oui | Non (SaaS) | Oui | Oui | SaaS payant |
| **Theia** | Inspiration VS Code | Oui | Oui (`theiaide/theia`) | Oui | Limité (OpenVSX) | ~512 Mo RAM |
| **JupyterLab** | Non | Oui | Oui (`jupyter`) | Oui | Extensions Python | ~256 Mo RAM |
| **SSH + Vim/Neovim** | Non | Non | N/A | Oui | Plugins Vim | Négligeable |

Mon choix pour un homelab auto-hébergé : **Code-Server** quand tu veux l'expérience VS Code complète sans dépendre d'un service cloud. GitHub Codespaces et Gitpod sont excellents mais facturés à l'heure et hébergés chez eux. Theia est une bonne alternative open-source mais moins mature sur les extensions VS Code. JupyterLab reste le roi du Python/data science, mais c'est pas un IDE généraliste.

## Prérequis

- Un serveur Linux avec Docker et Docker Compose installés
- Un dossier de projets à monter dans le conteneur
- Un reverse proxy pour l'exposition HTTPS (Caddy, Traefik, ou Nginx Proxy Manager)
- Un nom de domaine ou sous-domaine si tu veux HTTPS

Si tu débutes avec Docker, mon article sur [les services essentiels à auto-héberger](/docker-debutant-services-auto-heberger/) liste les bases à maîtriser avant d'ajouter Code-Server dans ta stack.

## Installation avec Docker Compose

Crée un dossier dédié et le fichier `docker-compose.yml` :

```bash
mkdir -p ~/code-server && cd ~/code-server
```

Voici le Docker Compose complet et prêt à l'emploi :

```yaml
services:
  code-server:
    image: codercom/code-server:latest
    container_name: code-server
    restart: unless-stopped
    user: "1000:1000"
    environment:
      - TZ=Europe/Paris
      - PASSWORD=ton-mot-de-passe-ultra-securise
      # Décommente pour désactiver l'authentification (PAS recommandé sur Internet)
      # - AUTH=none
    volumes:
      - /path/to/your/projects:/home/coder/project
      - ./config:/home/coder/.local/share/code-server
    ports:
      - "8080:8080"
```

Quelques explications sur les choix :

- `user: "1000:1000"` : exécute le conteneur avec tes permissions (remplace par `id $USER` pour connaître ton UID/GID). Sans ça, Code-Server ne pourra pas écrire dans tes fichiers de projet.
- `PASSWORD` : le mot de passe pour te connecter à l'interface. Change-le immédiatement. Ne mets pas "password123".
- `/path/to/your/projects:/home/coder/project` : monte ton dossier de projets dans le workspace de Code-Server. C'est là que tu verras tes fichiers dans l'explorateur.
- `./config:/home/coder/.local/share/code-server` : persiste tes paramètres utilisateur, tes extensions installées et ton historique. Sinon, tout disparaît au redémarrage.
- Le port exposé est `8080` en HTTP interne. Ton reverse proxy gérera le HTTPS externe.

Lance le conteneur :

```bash
cd ~/code-server
docker compose up -d
```

Accède à `http://IP_DU_SERVEUR:8080` et connecte-toi avec le mot de passe défini dans la variable `PASSWORD`.

## Configuration avancée : extensions et paramètres utilisateur

### Pr-installer des extensions

Au lieu d'installer manuellement Prettier à chaque redémarrage, tu peux précharger des extensions via un fichier de configuration. Crée un fichier `settings.json` dans ton volume config :

```bash
mkdir -p ~/code-server/config
cat > ~/code-server/config/settings.json << 'EOF'
{
  "workbench.colorTheme": "Dark+",
  "editor.fontSize": 14,
  "editor.formatOnSave": true,
  "terminal.integrated.defaultProfile.linux": "bash",
  "extensions.autoCheckUpdates": false
}
EOF
```

Pour pré-installer des extensions au démarrage, utilise une image personnalisée ou monte un script d'installation. Le plus simple reste d'installer via l'interface une fois, car le volume config les persiste.

### Ajouter des outils dans le conteneur

L'image de base contient le minimum. Si tu veux Node.js, Python, Git, ou des CLI supplémentaires, tu as deux options :

**Option A : étendre l'image Docker**

Crée un `Dockerfile` à côté du `docker-compose.yml` :

```dockerfile
FROM codercom/code-server:latest

USER root
RUN apt-get update && apt-get install -y \
    git \
    curl \
    python3 \
    python3-pip \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

USER coder
```

Modifie le `docker-compose.yml` :

```yaml
services:
  code-server:
    build: .
    container_name: code-server
    # ... reste identique
```

**Option B : monter les binaires de l'hôte**

Si tes outils sont déjà installés sur le serveur hôte, monte-les en volume :

```yaml
    volumes:
      - /path/to/your/projects:/home/coder/project
      - ./config:/home/coder/.local/share/code-server
      - /usr/bin/git:/usr/bin/git:ro
```

C'est moins propre mais fonctionne pour des binaires statiques.

## Sécuriser Code-Server

### 1. Changer le mot de passe par défaut

C'est la base. Le mot de passe dans `PASSWORD` est ton unique ligne de défense si tu exposes le service. Utilise un passphrase de 20+ caractères, généré par ton gestionnaire de mots de passe.

### 2. Ne jamais exposer le port brut sur Internet

Code-Server ne gère pas le HTTPS natif de manière robuste. Ne laisse jamais le port 8080 ouvert sur Internet sans reverse proxy TLS. Utilise Caddy, Traefik ou Nginx Proxy Manager.

### 3. Limiter les permissions du conteneur

Ajoute ces options de sécurité dans le `docker-compose.yml` :

```yaml
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    cap_add:
      - CHOWN
      - SETGID
      - SETUID
```

### 4. Filtrer par IP (si accès local uniquement)

Si tu n'utilises Code-Server que depuis ton réseau local ou via VPN, bloque l'accès externe au niveau du firewall :

```bash
sudo ufw deny 8080/tcp
sudo ufw allow from 192.168.1.0/24 to any port 8080
```

### 5. Utiliser un tunnel au lieu d'ouvrir un port

Si tu n'as pas d'IP publique fixe ou si tu veux éviter d'ouvrir des ports, [Cloudflare Tunnel](/cloudflare-tunnel-docker-homelab/) est la solution. Tu crées un tunnel sortant, tu obtiens une URL publique sécurisée, et aucun port entrant n'est exposé.

## Reverse proxy avec Caddy

Pour exposer Code-Server en HTTPS avec un joli nom de domaine, voici la config Caddy à ajouter dans ton `Caddyfile` :

```caddy
code.tondomaine.com {
    reverse_proxy code-server:8080
}
```

Assure-toi que le conteneur Code-Server et Caddy sont sur le même réseau Docker. Si tu utilises Docker Compose séparés, crée un réseau externe :

```yaml
networks:
  caddy:
    external: true
```

Et ajoute dans le service Code-Server :

```yaml
    networks:
      - caddy
```

Caddy gère automatiquement les certificats Let's Encrypt. Pas de certbot, pas de renouvellement manuel.

## Reverse proxy avec Nginx Proxy Manager

Dans l'interface web de [Nginx Proxy Manager](/nginx-proxy-manager-docker-guide/) :

1. Ajoute un proxy host : `code.tondomaine.com`
2. Forward hostname : `code-server`
3. Forward port : `8080`
4. Active "Block Common Exploits" et "Request a new SSL Certificate"
5. Force SSL et HSTS

NPM gère le renouvellement Let's Encrypt automatique. Le setup prend 2 minutes.

## Accès distant sans IP publique

Ton FAI te met derrière un CGNAT ? Tu n'as pas envie d'ouvrir des ports ? Déploie Cloudflare Tunnel à côté de Code-Server :

```yaml
services:
  cloudflared:
    image: cloudflare/cloudflared:latest
    container_name: cloudflared-code
    restart: unless-stopped
    command: tunnel --no-autoupdate run --token TON_TOKEN
```

Dans le dashboard Cloudflare Zero Trust, crée un tunnel, récupère le token, et ajoute une route vers `http://code-server:8080`. Tu obtiens `https://code.tondomaine.com` accessible depuis n'importe où, sans IP fixe, sans ouverture de ports.

J'ai détaillé le processus complet dans mon guide [Cloudflare Tunnel Docker](/cloudflare-tunnel-docker-homelab/). C'est la méthode que j'utilise personnellement pour tous mes services d'édition distants.

## Cas d'usage concrets

### Coder depuis un iPad ou un Chromebook

Ouvre Safari ou Chrome sur ton iPad, va sur `https://code.tondomaine.com`, connecte-toi. Tu as un VS Code complet avec terminal intégré. Tu peux coder en Python, JavaScript, Go, Rust depuis une tablette. Le clavier Bluetooth fait le reste.

### Environnement de développement standardisé pour une équipe

Tu as une équipe de 5 développeurs. Chacun a un Mac, un Windows, ou un Linux différent. Au lieu de gérer 5 setups Node.js qui partent en sucette, tu déploies Code-Server sur un serveur commun. Tout le monde travaille dans le même environnement, avec les mêmes versions d'outils.

### Édition rapide sur un serveur headless

Tu SSH sur ton serveur pour modifier un fichier de config. Tu oublies la syntaxe de sed, tu abandonne et tu ouvres Code-Server à la place. Double-clic sur le fichier, édition visuelle, sauvegarde. C'est plus rapide que Nano quand tu ne connais pas les raccourcis.

## Mise à jour

Coder publie des mises à jour régulières. Mets à jour une fois par semaine :

```bash
cd ~/code-server
docker compose pull
docker compose up -d
```

Le volume config persiste tes extensions et paramètres. Le volume projets persiste ton code. Tu ne perds rien.

## Sauvegardes

Tes projets sont sur le système hôte (dans `/path/to/your/projects`), donc sauvegarde-les comme tu le ferais normalement. Le volume config contient tes extensions et paramètres VS Code. Sauvegarde-le aussi si tu veux éviter de tout reconfigurer après un crash :

```bash
tar czf code-server-config-backup.tar.gz ~/code-server/config
```

Pour une stratégie de sauvegarde complète de tes conteneurs, j'ai publié un guide sur [Duplicati Docker](/duplicati-docker-sauvegarde/) qui gère le chiffrement et l'envoi vers le cloud.

## FAQ

**Code-Server est-il gratuit ?**
Oui. Code-Server est open-source sous licence MIT. L'image Docker est publique et gratuite. Coder vend une version cloud managée (Coder/coder), mais code-server en lui-même est 100 % gratuit.

**Puis-je utiliser GitHub Copilot ?**
Oui. Installe l'extension GitHub Copilot depuis le marketplace VS Code dans Code-Server. Connecte-toi avec ton compte GitHub. Ça marche exactement comme en local.

**Les extensions payantes fonctionnent-elles ?**
Certaines extensions du marketplace VS Code officiel nécessitent un compte Microsoft et ne fonctionnent pas dans code-server (ex : certaines extensions Azure propriétaires). La majorité des extensions open-source fonctionnent parfaitement.

**Code-Server supporte-t-il le debug ?**
Oui. Le debugging fonctionne pour la plupart des langages (Python, Node.js, Go, Rust, C++). Tu configures un `launch.json` comme en VS Code local.

**Puis-je utiliser une base de données dans Code-Server ?**
Code-Server est un éditeur, pas un serveur de BDD. Mais comme tu es dans un conteneur Docker, tu peux lancer un conteneur MariaDB ou PostgreSQL à côté et y accéder depuis le terminal intégré. J'ai publié des guides pour [MariaDB Docker](/mariadb-docker-base-de-donnees/) et [PostgreSQL Docker](/postgresql-docker-base-de-donnees/) si tu veux une stack complète.

**Le terminal intégré est-il un vrai shell ?**
Oui. C'est un vrai TTY connecté au conteneur. Tu peux lancer `htop`, `docker`, `git`, `npm`, `python`, tout ce que tu veux. Si le binaire n'est pas dans l'image, étends-la comme montré plus haut.

**Code-Server est-il traduit en français ?**
L'interface est la même que VS Code desktop. Tu changes la langue dans les paramètres (`Ctrl+Shift+P` > "Configure Display Language" > Français).

**Puis-je dupliquer mon setup VS Code local ?**
Oui. Exporte tes paramètres VS Code local (fichier `settings.json` et dossier `extensions`), copie-les dans le volume config de Code-Server, et tu retrouves ton environnement exact.
