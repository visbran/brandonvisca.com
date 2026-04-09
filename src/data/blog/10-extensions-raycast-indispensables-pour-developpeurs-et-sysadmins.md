---
title: 10 Extensions Raycast indispensables pour développeurs et sysadmins
description: "Docker, GitHub, SSH, Brew : 10 extensions Raycast pour transformer ton workflow dev/sysadmin. Guide complet avec installation et config."
pubDatetime: "2025-10-13T17:08:33+02:00"
author: Brandon Visca
tags:
  - raycast
  - macos
  - productivite
  - devops
  - docker
  - intermediaire
featured: true
draft: false
focusKeyword: Extensions Raycast
faqs:
  - question: "Les extensions Raycast sont-elles gratuites ?"
    answer: "La plupart sont gratuites et open-source. Raycast lui-même est gratuit, les extensions viennent du store officiel. Raycast Pro (8$/mois) débloque l'IA intégrée."
  - question: "Faut-il un compte Raycast pour utiliser les extensions ?"
    answer: "Non, aucun compte n'est requis pour les extensions de base. Le compte est uniquement nécessaire pour Raycast Pro et la synchronisation des paramètres."
  - question: "Les extensions fonctionnent-elles sur Apple Silicon (M1/M2/M3) ?"
    answer: "Oui, Raycast et toutes ses extensions sont compatibles nativement avec Intel et Apple Silicon sans aucune configuration supplémentaire."
  - question: "Puis-je utiliser Raycast en parallèle d'Alfred ?"
    answer: "Oui, les deux peuvent coexister. Assigne des raccourcis différents (ex: ⌥Space pour l'un, ⌘Space pour l'autre) pour éviter les conflits."
---

## Introduction : Le Store Raycast, un trésor inexploité

Si t'as lu [mon article précédent sur Raycast](https://brandonvisca.com/raycast-macos-outil-productivite-ultime/), tu sais déjà que c'est **la bombe absolue** pour la productivité sur macOS.

Mais ce que beaucoup ignorent, c'est que **le vrai pouvoir de Raycast**, c'est son **Store d'extensions**. Plus de 1000 extensions gratuites, open source, créées par la communauté.

Et spoiler : certaines de ces extensions vont **littéralement changer ta vie de dev ou sysadmin**.

Aujourd'hui, on va voir les **10 extensions que j'utilise tous les jours** et qui me font gagner un temps fou. Avec des exemples concrets, du code, et surtout : zéro bullshit.

Que tu sois dev frontend, backend, DevOps ou admin système, il y a forcément un truc pour toi ici.

---

## Table des matières

---

## Pré-requis : Installer et configurer Raycast

Avant de foncer tête baissée dans les extensions, assure-toi d'avoir :

1. **Raycast installé** (si c'est pas fait, [va lire l'article 1](https://brandonvisca.com/raycast-macos-outil-productivite-ultime/))
2. **Le raccourci configuré** (perso je suis sur ⌘ + Espace)
3. **Un compte Raycast** (optionnel mais recommandé pour le cloud sync)

> **À savoir :** Toutes les extensions listées ici sont **100% gratuites**. Pas de paywall, pas de surprise.

---

## Top 10 des extensions pour développeurs

### 1. 🐙 GitHub : ton dépôt dans ta poche

**Pourquoi c'est indispensable :**  
Plus besoin d'ouvrir ton navigateur pour checker tes PRs, issues ou repos. Tout est accessible en 2 secondes depuis Raycast.

**Ce que tu peux faire :**

- Lister tes repos
- Voir tes Pull Requests (ouvertes, mergées, draft)
- Créer une issue
- Rechercher dans le code
- Voir les notifications GitHub

**Installation :**

```
⌘ + Espace → Tape "store" → Cherche "GitHub" → Install
```

**Configuration :**  
Lors du premier lancement, Raycast va te demander un token GitHub. Voici comment le créer :

1. Va sur [github.com/settings/tokens](https://github.com/settings/tokens)
2. Clique sur "Generate new token (classic)"
3. Coche les permissions : `repo`, `notifications`, `user`
4. Copie le token généré
5. Colle-le dans Raycast

**Commandes utiles :**

```
gh               → Ouvre le menu GitHub
gh pr            → Voit tes Pull Requests
gh issues        → Liste tes issues
gh repos         → Browse tes repos
gh notifications → Check tes notifs
```

**Mon workflow :**  
Chaque matin, je tape `gh pr` pour voir mes PRs en attente. Gain de temps : **5 minutes par jour** (facile).

---

### 2. 🐳 Docker : gérer tes containers en 3 touches

**Pourquoi c'est indispensable :**  
Si tu bosses avec Docker (et soyons réalistes, qui ne le fait pas en 2025 ?), cette extension est un **must absolu**.

**Ce que tu peux faire :**

- Lister tes containers (running/stopped)
- Start/Stop/Restart un container
- Voir les logs en temps réel
- Supprimer des images
- Voir l'utilisation ressources

**Installation :**

```
⌘ + Espace → "store" → "Docker" → Install
```

**Configuration :**  
Aucune ! Si Docker Desktop tourne, ça marche direct.

**Commandes utiles :**

```
docker              → Menu principal
docker containers   → Liste des containers
docker images       → Liste des images
docker volumes      → Gestion des volumes
docker compose      → Gérer tes stacks
```

**Cas d'usage concret :**  
T'es en train de dev, ton container Postgres plante. Au lieu d'ouvrir Docker Desktop (qui rame), tu fais :

```
⌘ + Espace → docker → "postgres" → Restart
```

**Boom. 3 secondes.**

> **Pro tip :** Configure un alias `dk` pour l'extension Docker. Tu gagneras encore plus de temps.

---

### 3. 🍺 Brew : fini les `brew install` interminables

**Pourquoi c'est indispensable :**  
Homebrew, c'est génial. Mais taper `brew search`, `brew install`, `brew upgrade` dans le terminal, c'est lourd.

**Ce que tu peux faire :**

- Rechercher des packages
- Installer des apps (casks)
- Mettre à jour tes formulas
- Désinstaller proprement
- Voir les outdated packages

**Installation :**

```
⌘ + Espace → "store" → "Brew" → Install
```

**Commandes utiles :**

```
brew search     → Chercher un package
brew install    → Installer direct
brew outdated   → Packages à mettre à jour
brew upgrade    → Update tout
```

**Exemple d'utilisation :**  
Tu veux installer `htop` :

```
⌘ + Espace → brew search htop → Install
```

Raycast lance l'installation en background. Tu reçois une notif quand c'est fini.

**Pas besoin d'ouvrir le terminal.** Magique.

---

### 4. 🔌 Port Manager : killer de ports récalcitrants

**Pourquoi c'est indispensable :**  
"Error: Port 3000 already in use." **Rage.**

Avec Port Manager, tu vois qui squatte quel port et tu le kill en 1 clic.

**Ce que tu peux faire :**

- Lister tous les ports ouverts
- Voir quel process utilise un port
- Killer un process directement
- Filtrer par port ou nom

**Installation :**

```
⌘ + Espace → "store" → "Port Manager" → Install
```

**Commandes utiles :**

```
port           → Liste tous les ports
port 3000      → Voir qui écoute sur le port 3000
port kill 3000 → Tuer le process sur 3000
```

**Scénario classique :**  
Ton serveur Node ne démarre pas parce qu'un autre process est déjà sur le port 3000.

Avant :

```bash
lsof -ti:3000 | xargs kill -9
```

Maintenant :

```
⌘ + Espace → port 3000 → Kill Process
```

**C'est le jour et la nuit.**

---

### 5. 💻 VS Code Project Manager : switcher entre projets

**Pourquoi c'est indispensable :**  
Si tu bosses sur plusieurs projets (client, side project, boulot), tu perds un temps fou à naviguer dans tes dossiers.

**Ce que tu peux faire :**

- Lister tous tes projets VS Code récents
- Ouvrir un projet en 1 seconde
- Créer de nouveaux projets
- Accéder à la Command Palette VS Code

**Installation :**

```
⌘ + Espace → "store" → "Visual Studio Code" → Install
```

**Configuration :**  
Aucune si VS Code est installé normalement.

**Commandes utiles :**

```
code              → Liste de tes projets récents
code extensions   → Browse les extensions VS Code
code settings     → Accès aux settings
```

**Mon workflow :**  
Je travaille sur 5 projets différents chaque semaine. Au lieu de faire :

```bash
cd ~/projets/client-truc
code .
```

Je fais :

```
⌘ + Espace → code → "client-truc" → Enter
```

**Gain de temps estimé : 10 minutes par jour.**

---

### 6. 🎨 Tailwind CSS : la doc à portée de main

**Pourquoi c'est indispensable :**  
Si tu utilises Tailwind (et franchement, qui ne l'utilise pas ?), cette extension est un **game changer**.

**Ce que tu peux faire :**

- Rechercher une classe Tailwind
- Voir la définition CSS
- Browse les couleurs Tailwind
- Accéder à la doc officielle
- Chercher dans Tailwind UI

**Installation :**

```
⌘ + Espace → "store" → "Tailwind CSS" → Install
```

**Commandes utiles :**

```
tw               → Menu Tailwind
tw flex          → Recherche les classes flex
tw colors        → Palette de couleurs
tw docs          → Ouvre la doc
```

**Cas d'usage :**  
T'es en train de coder un composant et tu sais plus si c'est `justify-center` ou `items-center`.

Au lieu d'ouvrir la doc :

```
⌘ + Espace → tw justify → Tu vois toutes les classes justify-*
```

**Plus rapide. Plus efficace.**

---

### 7. 🔐 SSH Manager : connexion serveur en 1 seconde

**Pourquoi c'est indispensable :**  
Si t'es sysadmin ou DevOps, tu te connectes à des serveurs 50 fois par jour. Cette extension te sauve la vie.

**Ce que tu peux faire :**

- Lister tes connexions SSH (parse ton `~/.ssh/config`)
- Se connecter à un serveur en 1 clic
- Gérer tes clés SSH
- Créer de nouvelles connexions

**Installation :**

```
⌘ + Espace → "store" → "SSH Manager" → Install
```

**Configuration :**  
L'extension lit automatiquement ton fichier `~/.ssh/config`.

**Exemple de config SSH :**

```bash
# ~/.ssh/config
Host production
    HostName 192.168.1.100
    User root
    Port 22

Host staging
    HostName staging.example.com
    User deploy
    IdentityFile ~/.ssh/id_rsa_staging
```

**Utilisation :**

```
⌘ + Espace → ssh → "production" → Enter
```

Raycast ouvre iTerm/Terminal et lance la connexion.

**Fini les `ssh root@192.168.1.100` à rallonge.**

> **Bon à savoir :** Cette extension fonctionne avec iTerm2, Terminal, Warp, et Alacritty.

---

### 8. 📝 Hashnode : publier des articles techniques

**Pourquoi c'est cool :**  
Si tu écris des articles tech sur Hashnode, tu peux les gérer directement depuis Raycast.

**Ce que tu peux faire :**

- Voir tes drafts
- Publier un article
- Voir les stats
- Gérer les commentaires

**Installation :**

```
⌘ + Espace → "store" → "Hashnode" → Install
```

**Configuration :**  
Tu auras besoin d'un token Hashnode (disponible dans tes settings).

**Commandes utiles :**

```
hashnode           → Menu principal
hashnode drafts    → Voir tes brouillons
hashnode publish   → Publier un article
hashnode stats     → Analytics
```

**Cas d'usage :**  
Tu viens de finir un article dans Notion/Obsidian. Au lieu d'aller sur Hashnode :

```
⌘ + Espace → hashnode publish → Colle ton markdown → Publish
```

---

### 9. 🦊 GitLab : pour les rebelles anti-GitHub

**Pourquoi c'est indispensable :**  
Si ton entreprise utilise GitLab (ou si t'es un puriste de l'auto-hébergement), cette extension est pour toi.

**Ce que tu peux faire :**

- Voir tes Merge Requests
- Gérer les issues
- Browse tes projets
- Check les pipelines CI/CD
- Voir les snippets

**Installation :**

```
⌘ + Espace → "store" → "GitLab" → Install
```

**Configuration :**  
Tu dois fournir l'URL de ton instance GitLab + un token.

**Commandes utiles :**

```
gitlab            → Menu principal
gitlab mr         → Merge Requests
gitlab pipelines  → Voir les CI/CD
gitlab issues     → Issues ouvertes
```

**Mon workflow :**  
Je bosse sur un projet client hébergé sur GitLab. Chaque jour :

```
⌘ + Espace → gitlab mr → Je vois les MRs à review
```

Résultat : je suis **beaucoup plus réactif** sur les reviews.

---

### 10. 🎨 Color Picker : la pipette ultime

**Pourquoi c'est indispensable :**  
Que tu sois dev frontend ou que tu bidouilles des designs, tu as besoin de récupérer des couleurs à l'écran.

**Ce que tu peux faire :**

- Picker une couleur n'importe où sur ton écran
- Convertir entre formats (HEX, RGB, HSL, etc.)
- Créer des palettes
- Voir l'historique des couleurs

**Installation :**

```
⌘ + Espace → "store" → "Color Picker" → Install
```

**Configuration :**  
Configure un hotkey (moi c'est ⌘ + Shift + C).

**Utilisation :**

```
⌘ + Shift + C → Clique sur une couleur → Elle est copiée
```

**Formats supportés :**

- HEX : `#3B82F6`
- RGB : `rgb(59, 130, 246)`
- HSL : `hsl(217, 91%, 60%)`
- CSS Variable : `--color-blue-500`

**Cas d'usage :**  
Tu veux reproduire une couleur d'un site concurrent :

```
⌘ + Shift + C → Clique sur l'élément → Colle dans ton CSS
```

---

## Mentions honorables (extensions bonus)

Voici d'autres extensions qui méritent le détour :

|Extension|Utilité|Pour qui ?|
|---|---|---|
|**Spotify**|Contrôler la musique sans quitter le code|Tous|
|**Notion**|Rechercher dans tes pages Notion|Teams|
|**Tower**|Ouvrir tes repos Git dans Tower|Git GUI users|
|**Ruler**|Mesurer des distances à l'écran|Designers|
|**Ray.so**|Créer des screenshots de code stylés|Blogueurs tech|
|**Kubernetes**|Gérer tes clusters K8s|DevOps|
|**Terraform**|Run des commandes Terraform|Infra as Code|
|**HTTP Codes**|Checker les codes HTTP (200, 404...)|Devs API|

---

## Comment installer et configurer une extension

**Processus universel :**

1. **Ouvre le Store**
    
    ```
    ⌘ + Espace → Tape "store"
    ```
    
2. **Cherche l'extension**
    
    ```
    Tape le nom (ex: "docker")
    ```
    
3. **Installe**
    
    ```
    Clique sur "Install" ou appuie sur Enter
    ```
    
4. **Configure (si nécessaire)**
    
    - Certaines extensions demandent des tokens (GitHub, GitLab...)
    - D'autres fonctionnent out-of-the-box
5. **Utilise**
    
    ```
    ⌘ + Espace → Tape la commande de l'extension
    ```
    

> **Erreur fréquente :** Si une extension ne marche pas, vérifie que l'app associée est bien installée (Docker Desktop, VS Code, etc.).

---

## Créer sa propre extension (pour les curieux)

Si tu veux aller plus loin, Raycast te permet de **créer tes propres extensions** en TypeScript + React.

**Pourquoi créer une extension ?**

- Automatiser un workflow spécifique à ton entreprise
- Intégrer un outil interne
- Contribuer à la communauté

**Stack technique :**

- **React** pour l'UI
- **TypeScript** pour le code
- **Node.js** pour l'exécution

**Pour démarrer :**

```bash
# Installer le CLI Raycast
npm install -g @raycast/api

# Créer une nouvelle extension
raycast create my-extension

# Lancer en mode dev
npm run dev
```

**Ressources :**

- [Documentation officielle](https://developers.raycast.com/)
- [Exemples sur GitHub](https://github.com/raycast/extensions)
- [Communauté Slack](https://raycast.com/community)

**Spoiler :** Je prépare un article dédié à la création d'extensions custom. Stay tuned.

---

## Conclusion : Ton workflow va changer

Voilà, t'as maintenant **10 extensions ultra-puissantes** qui vont transformer ta façon de bosser sur macOS.

**Récap rapide :**

1. **GitHub** → PRs et repos en 2 secondes
2. **Docker** → Gérer tes containers sans Docker Desktop
3. **Brew** → Installer des apps en un clic
4. **Port Manager** → Killer les ports récalcitrants
5. **VS Code Project Manager** → Switcher entre projets
6. **Tailwind CSS** → La doc toujours dispo
7. **SSH Manager** → Connexion serveur instantanée
8. **Hashnode** → Publier des articles techniques
9. **GitLab** → Alternative à GitHub
10. **Color Picker** → Récupérer des couleurs partout

**Mon challenge pour toi :**  
Installe **au moins 3 de ces extensions** cette semaine et utilise-les pendant 5 jours. Je te garantis que tu ne reviendras jamais en arrière.

**Prochaine étape :**  
Dans l'article 3, on va voir comment **créer ses propres scripts Raycast** pour automatiser des tâches spécifiques. Du débutant au script ninja.

Si t'es passionné d'outils de productivité comme moi, jette aussi un œil à mes articles sur [Arc Browser](https://brandonvisca.com/arc-browser-alternatives-apres-abandon/) ou [la sécurisation de serveurs Nginx](https://brandonvisca.com/securiser-nginx-avec-headers-http/).

---

## 🔗 Articles connexes qui pourraient t'intéresser

- **[Raycast : L'outil qui transforme macOS en machine de productivité ultime](https://brandonvisca.com/raycast-macos-outil-productivite-ultime/)** : L'article 1 de la série, si t'as atterri ici direct
- **[Arc Browser : 7 alternatives après son abandon](https://brandonvisca.com/arc-browser-alternatives-apres-abandon/)** : Pour un navigateur aussi productif que Raycast
- **[Sécuriser Nginx avec les headers HTTP](https://brandonvisca.com/securiser-nginx-avec-headers-http/)** : Si tu gères des serveurs web

---

## 💡 Ressources utiles

- [Raycast Store](https://raycast.com/store) : Toutes les extensions disponibles
- [Documentation officielle](https://manual.raycast.com/)
- [GitHub - Extensions Raycast](https://github.com/raycast/extensions)
- [API Raycast](https://developers.raycast.com/)

## Articles connexes

- [Shutter Encoder Mac : Alternative Gratuite à HandBrake (Comp](/shutter-encoder-mac-alternative-handbrake/)
- [Oh My Zsh + Powerlevel10k : Transformez votre terminal en ma](/installation-oh-my-zsh-powerlevel10k-guide-complet/)
