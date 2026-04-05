---
title: 10 Extensions Raycast indispensables pour développeurs et sysadmins
pubDatetime: "2025-10-13T17:08:33+02:00"
description: 10 Extensions Raycast indispensables pour devs et sysadmins (2025)
tags:
  - raycast
  - macos
  - productivite
  - devops
  - docker
  - github
  - homebrew
  - guide
---


## Table des matières

-----------------------------------------------------

Si t’as lu [mon article précédent sur Raycast](https://brandonvisca.com/raycast-macos-outil-productivite-ultime/), tu sais déjà que c’est **la bombe absolue** pour la productivité sur macOS.

Mais ce que beaucoup ignorent, c’est que **le vrai pouvoir de Raycast**, c’est son **Store d’extensions**. Plus de 1000 extensions gratuites, open source, créées par la communauté.

Et spoiler : certaines de ces extensions vont **littéralement changer ta vie de dev ou sysadmin**.

Aujourd’hui, on va voir les **10 extensions que j’utilise tous les jours** et qui me font gagner un temps fou. Avec des exemples concrets, du code, et surtout : zéro bullshit.

Que tu sois dev frontend, backend, DevOps ou admin système, il y a forcément un truc pour toi ici.

- - - - - -

Pré-requis : Installer et configurer Raycast
--------------------------------------------

Avant de foncer tête baissée dans les extensions, assure-toi d’avoir :

1. **Raycast installé** (si c’est pas fait, [va lire l’article 1](https://brandonvisca.com/raycast-macos-outil-productivite-ultime/))
2. **Le raccourci configuré** (perso je suis sur ⌘ + Espace)
3. **Un compte Raycast** (optionnel mais recommandé pour le cloud sync)

> **À savoir :** Toutes les extensions listées ici sont **100% gratuites**. Pas de paywall, pas de surprise.

- - - - - -

Top 10 des extensions pour développeurs
---------------------------------------

### 1. 🐙 GitHub : ton dépôt dans ta poche

**Pourquoi c’est indispensable :**  
Plus besoin d’ouvrir ton navigateur pour checker tes PRs, issues ou repos. Tout est accessible en 2 secondes depuis Raycast.

**Ce que tu peux faire :**

- Lister tes repos
- Voir tes Pull Requests (ouvertes, mergées, draft)
- Créer une issue
- Rechercher dans le code
- Voir les notifications GitHub

**Installation :**

⌘ + Espace → Tape "store" → Cherche "GitHub" → Install


**Configuration :**  
Lors du premier lancement, Raycast va te demander un token GitHub. Voici comment le créer :

1. Va sur [github.com/settings/tokens](https://github.com/settings/tokens)
2. Clique sur « Generate new token (classic) »
3. Coche les permissions : `repo`, `notifications`, `user`
4. Copie le token généré
5. Colle-le dans Raycast

**Commandes utiles :**

```bash
gh               → Ouvre le menu GitHub
gh pr            → Voit tes Pull Requests
gh issues        → Liste tes issues
gh repos         → Browse tes repos
gh notifications → Check tes notifs


docker              → Menu principal
docker containers   → Liste des containers
docker images       → Liste des images
docker volumes      → Gestion des volumes
docker compose      → Gérer tes stacks


**Cas d’usage concret :**  
T’es en train de dev, ton container Postgres plante. Au lieu d’ouvrir Docker Desktop (qui rame), tu fais :

⌘ + Espace → docker → "postgres" → Restart


**Boom. 3 secondes.**

> **Pro tip :** Configure un alias `dk` pour l’extension Docker. Tu gagneras encore plus de temps.

- - - - - -

### 3. 🍺 Brew : fini les `brew install` interminables

**Pourquoi c’est indispensable :**  
Homebrew, c’est génial. Mais taper `brew search`, `brew install`, `brew upgrade` dans le terminal, c’est lourd.

**Ce que tu peux faire :**

- Rechercher des packages
- Installer des apps (casks)
- Mettre à jour tes formulas
- Désinstaller proprement
- Voir les outdated packages

**Installation :**

⌘ + Espace → "store" → "Brew" → Install


**Commandes utiles :**

```bash
brew search     → Chercher un package
brew install    → Installer direct
brew outdated   → Packages à mettre à jour
brew upgrade    → Update tout
brew search     → Chercher un package
brew install    → Installer direct
brew outdated   → Packages à mettre à jour
brew upgrade    → Update tout
port           → Liste tous les ports
port 3000      → Voir qui écoute sur le port 3000
port kill 3000 → Tuer le process sur 3000

**Scénario classique :**  
Ton serveur Node ne démarre pas parce qu’un autre process est déjà sur le port 3000.

Avant :

```bash
lsof -ti:3000 | xargs kill -9

```

# ~/.ssh/config
Host production
    HostName 192.168.1.100
    User root
    Port 22

Host staging
    HostName staging.example.com
    User deploy
    IdentityFile ~/.ssh/id_rsa_staging


**Utilisation :**

⌘ + Espace → ssh → "production" → Enter


Raycast ouvre iTerm/Terminal et lance la connexion.

**Fini les `ssh root@192.168.1.100` à rallonge.**

> **Bon à savoir :** Cette extension fonctionne avec iTerm2, Terminal, Warp, et Alacritty.

- - - - - -

### 8. 📝 Hashnode : publier des articles techniques

**Pourquoi c’est cool :**  
Si tu écris des articles tech sur Hashnode, tu peux les gérer directement depuis Raycast.

**Ce que tu peux faire :**

- Voir tes drafts
- Publier un article
- Voir les stats
- Gérer les commentaires

**Installation :**

⌘ + Espace → "store" → "Hashnode" → Install


**Configuration :**  
Tu auras besoin d’un token Hashnode (disponible dans tes settings).

**Commandes utiles :**

hashnode           → Menu principal
hashnode drafts    → Voir tes brouillons
hashnode publish   → Publier un article
hashnode stats     → Analytics


**Cas d’usage :**  
Tu viens de finir un article dans Notion/Obsidian. Au lieu d’aller sur Hashnode :

⌘ + Espace → hashnode publish → Colle ton markdown → Publish


- - - - - -

### 9. 🦊 GitLab : pour les rebelles anti-GitHub

**Pourquoi c’est indispensable :**  
Si ton entreprise utilise GitLab (ou si t’es un puriste de l’auto-hébergement), cette extension est pour toi.

**Ce que tu peux faire :**

- Voir tes Merge Requests
- Gérer les issues
- Browse tes projets
- Check les pipelines CI/CD
- Voir les snippets

**Installation :**

⌘ + Espace → "store" → "GitLab" → Install


**Configuration :**  
Tu dois fournir l’URL de ton instance GitLab + un token.

**Commandes utiles :**

gitlab            → Menu principal
gitlab mr         → Merge Requests
gitlab pipelines  → Voir les CI/CD
gitlab issues     → Issues ouvertes


**Mon workflow :**  
Je bosse sur un projet client hébergé sur GitLab. Chaque jour :

⌘ + Espace → gitlab mr → Je vois les MRs à review


Résultat : je suis **beaucoup plus réactif** sur les reviews.

- - - - - -

### 10. 🎨 Color Picker : la pipette ultime

**Pourquoi c’est indispensable :**  
Que tu sois dev frontend ou que tu bidouilles des designs, tu as besoin de récupérer des couleurs à l’écran.

**Ce que tu peux faire :**

- Picker une couleur n’importe où sur ton écran
- Convertir entre formats (HEX, RGB, HSL, etc.)
- Créer des palettes
- Voir l’historique des couleurs

**Installation :**

⌘ + Espace → "store" → "Color Picker" → Install


**Configuration :**  
Configure un hotkey (moi c’est ⌘ + Shift + C).

**Utilisation :**

⌘ + Shift + C → Clique sur une couleur → Elle est copiée


**Formats supportés :**

- HEX : `#3B82F6`
- RGB : `rgb(59, 130, 246)`
- HSL : `hsl(217, 91%, 60%)`
- CSS Variable : `--color-blue-500`

**Cas d’usage :**  
Tu veux reproduire une couleur d’un site concurrent :

⌘ + Shift + C → Clique sur l'élément → Colle dans ton CSS


- - - - - -

Mentions honorables (extensions bonus)
--------------------------------------

Voici d’autres extensions qui méritent le détour :

| Extension | Utilité | Pour qui ? |
|---|---|---|
| **Spotify** | Contrôler la musique sans quitter le code | Tous |
| **Notion** | Rechercher dans tes pages Notion | Teams |
| **Tower** | Ouvrir tes repos Git dans Tower | Git GUI users |
| **Ruler** | Mesurer des distances à l'écran | Designers |
| **Ray.so** | Créer des screenshots de code stylés | Blogueurs tech |
| **Kubernetes** | Gérer tes clusters K8s | DevOps |
| **Terraform** | Run des commandes Terraform | Infra as Code |
| **HTTP Codes** | Checker les codes HTTP (200, 404…) | Devs API |


Comment installer et configurer une extension
---------------------------------------------

**Processus universel :**

1. **Ouvre le Store** `⌘ + Espace → Tape "store"`
2. **Cherche l’extension** `Tape le nom (ex: "docker")`
3. **Installe** `Clique sur "Install" ou appuie sur Enter`
4. **Configure (si nécessaire)**
  - Certaines extensions demandent des tokens (GitHub, GitLab…)
  - D’autres fonctionnent out-of-the-box
5. **Utilise** `⌘ + Espace → Tape la commande de l'extension`

> **Erreur fréquente :** Si une extension ne marche pas, vérifie que l’app associée est bien installée (Docker Desktop, VS Code, etc.).

- - - - - -

Créer sa propre extension (pour les curieux)
--------------------------------------------

Si tu veux aller plus loin, Raycast te permet de **créer tes propres extensions** en TypeScript + React.

**Pourquoi créer une extension ?**

- Automatiser un workflow spécifique à ton entreprise
- Intégrer un outil interne
- Contribuer à la communauté

**Stack technique :**

- **React** pour l’UI
- **TypeScript** pour le code
- **Node.js** pour l’exécution

**Pour démarrer :**

```bash
# Installer le CLI Raycast
npm install -g @raycast/api

# Créer une nouvelle extension
raycast create my-extension

# Lancer en mode dev
npm run dev

```

