---
title: "Gitea Docker : ton serveur Git auto-hébergé en 5 minutes"
description: Installe Gitea avec Docker pour héberger tes repos Git sur ton serveur. Guide complet gitea docker pour remplacer GitHub en auto-hébergement léger.
pubDatetime: 2026-06-01T07:00:00.000Z
author: Brandon Visca
tags:
  - intermediaire
  - auto-hebergement
  - docker
  - git
  - homelab
  - github-alternative
featured: false
draft: false
focusKeyword: gitea docker
faqs:
  - question: "Gitea est-il vraiment gratuit ?"
    answer: "Oui, Gitea est 100 % open source sous licence MIT. Tu peux l'auto-héberger gratuitement sur ton propre serveur sans limitation de repos, d'utilisateurs ou de bande passante."
  - question: "Puis-je migrer mes projets GitHub vers Gitea ?"
    answer: "Oui, Gitea intègre une fonction de migration depuis GitHub, GitLab, Bitbucket et d'autres forges. Elle clone les dépôts, conserve les issues, les PR/MR et les wikis selon les options choisies."
  - question: "Quelle base de données choisir pour Gitea Docker ?"
    answer: "SQLite suffit pour un usage personnel ou une petite équipe. Pour la production ou plus de 10 utilisateurs actifs, privilégie PostgreSQL avec un volume Docker dédié pour la persistance."
---
## Table des matières

---

## TL;DR

- Gitea est un serveur Git **open source et ultra-léger** — alternative crédible à GitHub, GitLab et Forgejo.
- Container officiel : `gitea/gitea:latest` (v1.26.2, licence MIT, ~300 Mo).
- Ports par défaut : **3000** (interface web) et **22** (Git SSH).
- Déploiement en 5 minutes avec Docker Compose + un volume `/data` persistant.
- SQLite pour commencer, PostgreSQL pour monter en charge proprement.
- Reverse proxy recommended pour le HTTPS et la sécurité.

---

## Pourquoi se faire son propre Git ?

Tu stockes ton code sur GitHub. Gratuit, rapide, tout le monde y est. Jusqu'au jour où Microsoft force une migration 2FA intrusive, où ton dépôt privé disparaît suite à une fausse manœuvre de modération automatisée, ou où tu réalises que chaque `git push` transite par des serveurs américains soumis au Cloud Act.

**L'auto-hébergement de Git, c'est pas de la paranoia.** C'est du pragmatisme :
- Tu contrôles 100 % de tes données et de ton historique.
- Pas de limitation d'espace ou de bande passante imposée par un tiers.
- Pas de risque de suspension arbitraire de compte pour une clause de service interprétée largement.
- CI/CD possible via Gitea Actions, webhooks ou couplage avec Drone.
- Tu peux l'héberger derrière un VPN, restreint à ton LAN ou exposé sur Internet — tu décides.

Gitea, c'est le moyen le plus rapide et le moins gourmand d'y arriver. Une VM avec 1 Go de RAM et un modeste CPU x86 suffisent amplement. Sur un Raspberry Pi 4, il tourne sans sourciller.

---

## Qu'est-ce que Gitea exactement ?

Gitea est une forge logicielle auto-hébergée écrite en Go. Elle reprend les fonctionnalités essentielles de GitHub dans une interface épurée et une empreinte mémoire ridiculement faible.

**Ce qu'il fait nativement :**
- Hébergement de dépôts Git (publics et privés, sans limite).
- Pull requests avec code review, commentaires inline et approbations.
- Issues intégrées avec labels, milestones, assignations et templates.
- Wiki intégré par dépôt (Markdown par défaut).
- Gitea Actions pour la CI/CD (syntaxe compatible workflows GitHub).
- Authentification locale, LDAP, OAuth2 (Google, GitHub, GitLab) et SAML.
- Webhooks, intégrations et API REST complète.
- Registry de packages (npm, PyPI, Docker, Helm, etc.).

**Ce qu'il ne fait pas (encore) :**
- Pas de Copilot intégré (évidemment).
- Pas de marketplace d'actions aussi riche que GitHub.
- Moins de plugins communautaires que GitLab.

La dernière version stable au moment de la rédaction : **v1.26.2**. Le projet est très actif sur GitHub (`go-gitea/gitea`), avec des releases mensuelles et une communauté solide. Licence MIT.

---

## Comparatif rapide : Gitea vs GitHub vs GitLab vs Forgejo

| Critère | Gitea | GitHub | GitLab CE | Forgejo |
|---|---|---|---|---|
| **Ressource** | Très légère (~300 Mo) | SaaS uniquement | Lourde (>4 Go RAM) | Très légère |
| **Installation** | Docker en 5 min | Inscription | Omnibus ou source | Fork de Gitea |
| **CI/CD intégrée** | Gitea Actions | GitHub Actions | GitLab CI/CD | Gitea Actions |
| **Interface** | Proche GitHub | Référence | Distincte | Proche Gitea |
| **Migrations ext.** | GitHub/GitLab/Bitbucket | Impossible | GitHub/GitLab uniquement | Gitea/Forgejo/GitHub |
| **Licence** | MIT | Propriétaire | MIT/EE | MIT |

**Quand choisir quoi :**
- Tu veux du SaaS clé en main sans la moindre maintenance ? **GitHub**.
- Tu veux une solution monolithique avec registry, CI et monitoring intégrés ? **GitLab**.
- Tu veux **un serveur Git léger, rapide à déployer et facile à maintenir** ? **Gitea**.
- Tu veux Gitea mais avec une gouvernance communautaire totalement indépendante ? **Forgejo** (fork né de désaccords sur la gouvernance de Gitea).

---

## Prérequis avant de commencer

- Docker Engine et Docker Compose (v2+) installés.
- Un serveur Linux (Debian, Ubuntu, AlmaLinux…), un NAS compatible Docker, ou un Raspberry Pi 4 avec 4 Go de RAM.
- Un dossier dédié pour persister les données (`./gitea/data` — ne le perd pas).
- Les ports **3000** et **222** (ou **22**) libres sur l'hôte.
- Un nom de domaine (recommandé) pour configurer le HTTPS via reverse proxy.
- Connaissances de base Docker et Git (clonage SSH, `docker compose`).

---

## Déploiement Gitea Docker avec SQLite et Docker Compose

C'est la configuration la plus simple pour démarrer immédiatement. Elle utilise SQLite comme backend : aucune base de données externe nécessaire, aucun service supplémentaire.

Crée un dossier dédié et un fichier `docker-compose.yml` :

```yaml
version: "3.8"

services:
  server:
    image: gitea/gitea:latest
    container_name: gitea
    environment:
      - USER_UID=1000
      - USER_GID=1000
      - GITEA__database__DB_TYPE=sqlite3
      - GITEA__database__PATH=/data/gitea/gitea.db
    restart: always
    networks:
      - gitea
    volumes:
      - ./gitea:/data
      - /etc/timezone:/etc/timezone:ro
      - /etc/localtime:/etc/localtime:ro
    ports:
      - "3000:3000"
      - "222:22"

networks:
  gitea:
```

Lance la stack :

```bash
mkdir -p /opt/gitea && cd /opt/gitea
docker compose up -d
```

En 20 à 30 secondes, Gitea est accessible sur `http://<IP_SERVEUR>:3000`.

> **Pourquoi mapper `222:22` et pas `22:22` ?** Le port 22 est souvent déjà utilisé par le daemon SSH de ton serveur. Mapper vers le port 222 sur l'hôte évite tout conflit. Tu pourras ajuster l'URL de clone SSH visible dans l'interface ensuite.

---

## Config initiale via l'interface web

À la première connexion (`http://IP:3000`), Gitea te demande de finaliser l'installation :

1. **Langue** : sélectionne Français.
2. **Type de base de données** : SQLite3 (déjà pré-rempli si la variable d'environnement est settée).
3. **Chemin des repos Git** : laisse `/data/git/repositories`.
4. **URL de base** : mets l'URL publique complète, ex : `https://git.tondomaine.fr`.
5. **Domaine SSH server** : l'IP publique ou le domaine pointant vers ton serveur.
6. **Port SSH server** : mets **222** si tu as utilisé le mapping ci-dessus. Gitea affichera alors les URLs de clone sous la forme :
   ```
   ssh://git@git.tondomaine.fr:222/utilisateur/projet.git
   ```
7. **Créer un compte administrateur** : choisis un nom d'utilisateur, un email et un mot de passe fort.
8. Clique sur **Installer Gitea**.

➡️ **Note importante :** si tu passes derrière un reverse proxy (Nginx Proxy Manager, Traefik, Caddy), renseigne l'URL HTTPS dans les paramètres *avant* l'installation pour éviter les liens internes cassés. Cela se fait soit via l'interface initiale (champ "URL de base"), soit via la variable d'environnement `GITEA__server__ROOT_URL`.

---

## Déploiement production avec PostgreSQL

Pour un usage à plusieurs développeurs ou en production, SQLite montre rapidement ses limites (verrouillage en écriture sur requêtes simultanées). Voici la stack complète avec PostgreSQL 16 et un healthcheck intégré.

```yaml
version: "3.8"

services:
  server:
    image: gitea/gitea:latest
    container_name: gitea
    environment:
      - USER_UID=1000
      - USER_GID=1000
      - GITEA__database__DB_TYPE=postgres
      - GITEA__database__HOST=db:5432
      - GITEA__database__NAME=gitea
      - GITEA__database__USER=gitea
      - GITEA__database__PASSWD=CHANGE_ME_STRONG_PASSWORD
    restart: always
    networks:
      - gitea
    volumes:
      - ./gitea:/data
      - /etc/timezone:/etc/timezone:ro
      - /etc/localtime:/etc/localtime:ro
    ports:
      - "3000:3000"
      - "222:22"
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:16-alpine
    container_name: gitea-db
    environment:
      - POSTGRES_USER=gitea
      - POSTGRES_PASSWORD=CHANGE_ME_STRONG_PASSWORD
      - POSTGRES_DB=gitea
    restart: always
    networks:
      - gitea
    volumes:
      - ./postgres:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U gitea -d gitea"]
      interval: 5s
      timeout: 5s
      retries: 5

networks:
  gitea:
```

Déploie avec :

```bash
cd /opt/gitea
docker compose up -d
```

Cette stack persiste aussi la base PostgreSQL dans le dossier `./postgres` local. **N'oublie jamais de sauvegarder ce dossier**, car il contient l'intégralité de tes métadonnées.

---

## Reverse Proxy HTTPS (Nginx Proxy Manager)

Ne laisse jamais Gitea en HTTP pur sur Internet. La méthode la plus simple pour ajouter du HTTPS est **Nginx Proxy Manager** (disponible lui aussi en Docker).

Dans NPM :
1. Ajoute un proxy host pointant vers `gitea:3000` (IP interne du conteneur ou `localhost:3000` si en réseau host).
2. Rentre ton domaine : `git.tondomaine.fr`.
3. Active "Block Common Exploits" et "Websockets Support".
4. Demande un certificat SSL via Let's Encrypt.
5. Enregistre.

Dans le fichier `docker-compose.yml` de Gitea, ajoute ces variables d'environnement pour indiquer à Gitea qu'il tourne derrière HTTPS :

```yaml
environment:
  - GITEA__server__ROOT_URL=https://git.tondomaine.fr/
  - GITEA__server__DOMAIN=git.tondomaine.fr
  - GITEA__server__SSH_DOMAIN=git.tondomaine.fr
```

Redémarre le conteneur et teste `https://git.tondomaine.fr`.

---

## SSH Git : configurer proprement le clone

Contrairement au web (HTTPS), le **Git SSH** nécessite que ton client connaisse le bon port et que ta clé publique soit enregistrée dans ton profil Gitea.

**1. Génère une clé SSH** (si tu n'en as pas encore) :

```bash
ssh-keygen -t ed25519 -C "ton@email.fr"
```

**2. Copie ta clé publique** dans Gitea : Profile → Settings → SSH/GPG Keys → Add Key.

**3. Clone en SSH avec le port mappé** :

```bash
git clone ssh://git@git.tondomaine.fr:222/tonuser/monprojet.git
```

**4. Pour éviter de préciser le port à chaque fois**, ajoute dans ton `~/.ssh/config` :

```
Host git.tondomaine.fr
    Port 222
    User git
    IdentityFile ~/.ssh/id_ed25519
```

Après ça, un simple `git clone git@git.tondomaine.fr:tonuser/monprojet.git` suffit. Ton terminal traitera automatiquement le port 222.

---

## Migrer un projet GitHub vers Gitea

Gitea intègre une fonction de migration native qui permet de cloner un dépôt externe en conservant (partiellement ou totalement) les métadonnées.

**Sur l'interface web :**
1. Clic sur le `+` en haut à droite → "Migrer un dépôt".
2. Sélectionne **GitHub** comme source.
3. Colle l'URL du dépôt : `https://github.com/utilisateur/projet`.
4. Si le dépôt est privé, génère un Personal Access Token sur GitHub et colle-le dans le champ dédié.
5. Coche les options à migrer : issues, PR, labels, milestones, wiki, releases.
6. Attends la fin de la synchronisation.

**En ligne de commande avec l'API :**

```bash
curl -X POST "https://git.tondomaine.fr/api/v1/repos/migrate" \
  -H "Authorization: token TA_TOKEN" \
  -d '{
    "clone_addr": "https://github.com/utilisateur/projet",
    "repo_name": "projet",
    "mirror": false,
    "issues": true,
    "pull_requests": true
  }'
```

---

## Sauvegarde et mise à jour de Gitea

**Sauvegarder**, c'est la base. Voici un script minimal pour dumper Gitea (à mettre dans un cron hebdomadaire) :

```bash
#!/bin/bash
DATE=$(date +%Y%m%d)
tar czvf /backup/gitea-data-${DATE}.tar.gz /opt/gitea/gitea
# Si tu utilises PostgreSQL, ajoute :
docker exec gitea-db pg_dump -U gitea gitea > /backup/gitea-db-${DATE}.sql
```

**Mise à jour en douceur :**

```bash
cd /opt/gitea
docker compose pull
docker compose up -d
```

Gitea gère ses migrations de schéma automatiquement au démarrage. Aucune action manuelle requise entre les versions mineures. Lis tout de même les notes de version (release notes) avant chaque `pull`, notamment si tu passes d'une version majeure à une autre.

---

## Sécurité : bonnes pratiques rapides

1. **Reverse proxy HTTPS obligatoire** : ne laisse jamais Gitea en HTTP sur Internet public. Traefik, Nginx Proxy Manager ou Caddy font le job en quelques clics.
2. **Fail2Ban** : protège le port 3000 contre les attaques par force brute sur le login. Un filtre spécifique existe pour Gitea dans les communautés Linux.
3. **Backups chiffrés et hors site** : stocke tes dumps sur un cloud externe chiffré (rclone avec la couche crypt, BorgBase, ou Kopia).
4. **Pas d'accès root** : les images officielles tournent avec `USER_UID=1000` par défaut. Ne modifies jamais cela sans raison impérieuse.
5. **ClamAV ou audit** : si tu autorises des utilisateurs externes à uploader des fichiers, scanne les pièces jointes.
6. **Tokens d'API** : limite leur durée de vie et révoque ceux qui ne sont plus utilisés.

---

## Troubleshooting courant

| Problème | Cause probable | Solution |
|---|---|---|
| `Permission denied` au clone SSH | Clé SSH non ajoutée ou mauvais port | Ajoute la clé dans Gitea Settings, vérifie `~/.ssh/config` |
| Boutons/liens cassés (HTTP au lieu de HTTPS) | `ROOT_URL` mal configurée | Stoppe le conteneur, ajoute `GITEA__server__ROOT_URL=https://...` |
| Interface web inaccessible | Port 3000 occupé ou firewall | `ss -tlnp`, `ufw allow 3000/tcp`, vérifie Docker |
| Repo en lecture seule après crash réseau | SQLite corrompu | Restaure ton backup, ou migre immédiatement vers PostgreSQL |
| Lenteur sur gros repository (>1 Go) | SQLite en saturation | Basculer vers PostgreSQL pour de meilleures performances |
| Erreur `database is locked` | Concurrents écritures SQLite | Passer à PostgreSQL sans hésiter |
| Images/avatars affichées en HTTP | Header `X-Forwarded-Proto` manquant | Active les headers forwarded dans ton reverse proxy |

---

## Conclusion

Installer Gitea en Docker, c'est 10 minutes top chrono pour récupérer la maîtrise totale de tes dépôts. C'est léger, solide, et le projet évolue très vite avec une communauté active. Pour un usage perso ou en petite équipe, la stack SQLite fait le job parfaitement. Pour un usage professionnel ou une charge soutenue, la stack PostgreSQL + reverse proxy HTTPS est le standard à adopter.

Arrête de dépendre de GitHub pour absolument tout. Ton code mérite mieux que d'être otage d'une plateforme propriétaire.
