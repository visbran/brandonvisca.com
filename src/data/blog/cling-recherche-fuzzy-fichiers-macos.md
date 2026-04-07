---
title: "Cling : Recherche fuzzy fichiers 10x plus rapide"
description: "Recherche fichiers mac rapide avec Cling : fuzzy search instantané, tolérant aux fautes de frappe. Alternative Spotlight gratuite et open-source."
pubDatetime: "2025-11-27T00:00:00+01:00"
author: Brandon Visca
tags:
  - macos
  - recherche
  - fichiers
  - fuzzy-search
  - low-tech
  - debutant
featured: false
draft: false
focusKeyword: recherche fichiers mac rapide
faqs:
  - question: "Quelle différence entre Cling et Spotlight ?"
    answer: "Spotlight indexe le contenu des fichiers (lent à démarrer, nécessite une indexation). Cling fait une recherche fuzzy sur les noms de fichiers : instantané, tolérant aux fautes de frappe, sans délai."
  - question: "Cling fonctionne-t-il sur les dossiers réseau (NAS, SMB) ?"
    answer: "Oui, si le dossier réseau est monté sur ton Mac, Cling peut le scanner. Les performances dépendent de ta connexion réseau et de la taille du NAS."
  - question: "Cling remplace-t-il fzf ou fd en terminal ?"
    answer: "Cling est une interface graphique au-dessus de ces outils. Si tu travailles uniquement en terminal, fzf reste plus flexible. Cling est idéal pour une recherche rapide sans quitter le contexte visuel."
  - question: "Cling est-il gratuit ?"
    answer: "Oui, Cling est gratuit et open-source, développé par Low-Tech Guys. Aucun abonnement ni version payante."
---
# Cling : Recherche fuzzy fichiers 10x plus rapide

![](https://res.cloudinary.com/dlkn3lxkk/image/upload/v1765283142/brandonviscacom/CleanShot_2025-12-09_at_13.16.42_2x_x8liqi.jpg)

---

## Table des matières

## Introduction : Spotlight, c'est bien... pour 2010

**Le problème** : Tu cherches ce fichier `docker-compose.yaml` que tu as modifié hier. Tu tapes "docker compose" dans Spotlight.

**Ce que Spotlight te propose** :
1. Définition web "Docker Compose"
2. Apps tierces qui n'ont rien à voir
3. Résultats Siri suggestions
4. Ton fichier... en 15ème position (si tu as de la chance)

**Résultat** : 30 secondes perdues à scroller dans des résultats inutiles.

**Pire encore** : Tu as mal tapé `dockr compse` ? Spotlight ne trouve rien. Zero tolérance aux fautes de frappe.

Et si je te disais qu'il existe **un outil qui trouve n'importe quel fichier en <1 seconde**, même si tu tapes le nom approximativement, avec des fautes, et que **ça cherche aussi dans les fichiers système, dotfiles, et caches** ignorés par Spotlight ?

Bienvenue dans le monde de **Cling**, l'outil de recherche fuzzy qui va te faire oublier Spotlight pour toujours.

💡 **Ce que tu vas apprendre dans ce guide** :
- Installer Cling en 2 minutes (gratuit et open source)
- Recherche fuzzy : trouve des fichiers même avec des fautes de frappe
- Actions rapides : ouvrir, copier, renommer, QuickLook en 1 touche
- Créer tes propres scripts custom
- Différences avec Spotlight, Raycast, Alfred, Find Any File

Let's go ! 🚀

---

## TL;DR : Cling en 30 secondes

**Le problème** : Spotlight lent + pas de tolérance aux fautes

**La solution** : Cling = Recherche fuzzy ultra-rapide

| Recherche | Spotlight | Cling |
|-----------|-----------|-------|
| "dckr cmp" | ❌ Aucun résultat | ✅ docker-compose.yaml |
| Dotfiles (.zshrc) | ❌ Ignorés | ✅ Trouvés instantanément |
| Vitesse | 2-5 secondes | <0.5 seconde |
| Fichiers système | ❌ Exclus | ✅ Tous indexés |

**Résultat concret** : 5 min/jour gagnées = **30h économisées/an**

**Installation** : 1 commande Homebrew

**Prix** : 100% gratuit et open source

---

## Qu'est-ce que Cling ?

**Cling**, c'est l'alternative macOS à [Everything](https://www.voidtools.com/) (légendaire outil Windows), développée par [Low Tech Guys](https://lowtechguys.com/).

![](https://res.cloudinary.com/dlkn3lxkk/image/upload/v1765283430/brandonviscacom/CleanShot_2025-12-09_at_13.30.14_2x_dtrfzm.jpg)

### Le concept en une phrase

**Instant fuzzy find any file, act on it in the same instant.**

Cling indexe **tout ton système de fichiers** en mémoire (y compris fichiers système, dotfiles, caches) et te permet de chercher avec un **algorithme fuzzy** ultra-tolérant.

### Pourquoi c'est génial ?

✅ **Recherche fuzzy** : `dckr cmp` trouve `docker-compose.yaml`
✅ **Instantané** : Résultats en <500ms même avec 1M+ fichiers
✅ **Tout est indexé** : Fichiers système, dotfiles, .git, node_modules, caches
✅ **Actions clavier** : Ouvrir, copier path, renommer, delete sans souris
✅ **Scripts custom** : Crée tes propres actions avec n'importe quel langage
✅ **Gratuit et open source** : Code sur GitHub, pas de paywall

### Les chiffres qui parlent

- **Index en mémoire** : 300 Mo à 2 Go selon la taille de ton disque
- **Première indexation** : 1-5 minutes (puis incrémental en arrière-plan)
- **Vitesse recherche** : Sub-seconde même avec 1M fichiers
- **Compatibilité** : macOS 14+ (Sonoma, Sequoia)
- **Open source** : [GitHub](https://github.com/FuzzyIdeas/Cling)

---

## Fuzzy search, c'est quoi ? (Explication simple)

**Fuzzy search** = Recherche "floue" qui tolère les approximations.

**Exemples concrets** :

| Tu tapes | Cling trouve |
|----------|--------------|
| `dckr cmp` | `docker-compose.yaml` |
| `rcnfg` | `raycast-config.json` |
| `bsh prf` | `.bash_profile` |
| `obsdn` | `Obsidian.app`, `obsidian-notes/` |

**Comment ça marche** :
1. Cling extrait les **caractères clés** de ta recherche
2. Il cherche des fichiers qui **contiennent ces caractères dans le bon ordre**
3. Il rank les résultats par **pertinence**

**Analogie** : C'est comme Google qui corrige "gogle" en "google". Mais pour les noms de fichiers.

💡 **Différence avec Spotlight** : Spotlight nécessite une correspondance exacte. Cling est tolérant.

---

## Installation de Cling : 2 méthodes

### Méthode 1 : Homebrew (recommandée)

Si tu as Homebrew ([sinon, installe-le](https://brandonvisca.com/installation-homebrew-macos/)) :

```bash
# Installation en une ligne
brew install --cask thelowtechguys-cling
```

![](https://res.cloudinary.com/dlkn3lxkk/image/upload/v1765283084/brandonviscacom/CleanShot_2025-12-09_at_13.15.30_2x_e6a81v.jpg)

**Avantages** :
- Mises à jour automatiques
- Désinstallation propre
- Gestion centralisée

⚠️ **Pas encore Homebrew ?** → [Guide installation Homebrew macOS](/installation-homebrew-macos/)

---

### Méthode 2 : Download direct

1. **Télécharge Cling** : [lowtechguys.com/cling](https://lowtechguys.com/cling/)
2. **Glisse `Cling.app` dans `/Applications`**
3. **Premier lancement** : Clic droit > Ouvrir
4. **Autorise les permissions** : Full Disk Access (pour indexer tout)

![](https://res.cloudinary.com/dlkn3lxkk/image/upload/v1765283469/brandonviscacom/CleanShot_2025-12-09_at_13.17.34_2x_la0t47.jpg)

💡 **Important** : Cling **nécessite Full Disk Access** pour indexer les fichiers système, dotfiles, etc. Sans ça, il sera limité comme Spotlight.

---

## Configuration essentielle en 5 minutes

### Première utilisation : Indexation initiale

Au premier lancement :

1. **Cling indexe ton disque** : 1-5 minutes selon la taille
2. **Tu peux utiliser l'app pendant** : Indexation en arrière-plan
3. **Barre de progression** : Visible en haut de la fenêtre Cling

![](https://res.cloudinary.com/dlkn3lxkk/image/upload/v1765283470/brandonviscacom/CleanShot_2025-12-09_at_13.17.41_2x_cnowb3.jpg)

**Consommation CPU** : 100% sur plusieurs cores pendant 1-5 min. **C'est normal**. Après, CPU à 0% en arrière-plan.

**Consommation RAM** : 300 Mo à 2 Go selon ton nombre de fichiers. Cling libère la RAM quand la fenêtre est en arrière-plan (swap vers disque).

---

### Réglages de base recommandés

**Hotkey global** : Configure un raccourci pour ouvrir Cling n'importe où.

```
Recommandation : Cmd+k (Find)
Alternative : Cmd+Opt+Space (si tu veux remplacer Spotlight)
```

**Exclusions** : Cling respecte `.fsignore` (comme `.gitignore`).

**Fichier** : `~/.fsignore`

**Exemple** :
```bash
# Exclusions recommandées
node_modules/
.git/objects/
Library/Caches/
*.log
*.tmp
```

💡 **Pourquoi exclure** : Réduire la taille de l'index + accélérer les recherches.

---

### Interface : Navigation clavier uniquement

Cling est **100% clavier-centric**. Pas besoin de souris.

**Raccourcis essentiels** :

| Touche        | Action                       |
| ------------- | ---------------------------- |
| `Cmd+K`       | Ouvrir Cling (hotkey global) |
| `Type`        | Recherche fuzzy instantanée  |
| `↑ ↓`         | Naviguer dans les résultats  |
| `Enter`       | Ouvrir le fichier            |
| `Cmd+Enter`   | Ouvrir dans Finder           |
| `Space`       | QuickLook preview            |
| `Cmd+C`       | Copier le chemin absolu      |
| `Cmd+Shift+C` | Copier le nom du fichier     |
| `Cmd+D`       | Delete (avec confirmation)   |
| `Esc`         | Fermer Cling                 |

---

## Utilisation : 4 workflows puissants

### Workflow 1 : Recherche fuzzy basique

**Scénario** : Tu cherches ton fichier de config Docker Compose.

**Avant Cling (Spotlight)** :
```
1. Cmd+Space
2. Tape "docker-compose.yaml"
3. Scroll dans 15 résultats inutiles
4. Clique sur le bon fichier
Temps : 30 secondes
```

**Avec Cling** :
```
1. Cmd+K (ouvre Cling)
2. Tape "dckr cmp"
3. Enter
Temps : 3 secondes
```

**Résultat** : `docker-compose.yaml` s'ouvre dans VS Code (ou ton éditeur par défaut).

---

### Workflow 2 : Fichiers système et dotfiles

**Scénario** : Tu dois modifier ton `.zshrc` caché dans `~/.config/`.

**Avant Cling (Spotlight)** :
```
Spotlight ne trouve PAS les dotfiles par défaut
→ Tu dois ouvrir Terminal
→ cd ~
→ nano .zshrc
Temps : 20 secondes
```

**Avec Cling** :
```
1. Cmd+K
2. Tape "zshrc"
3. Enter
Temps : 2 secondes
```

**Bonus** : Cling trouve **tous** les `.zshrc` sur ton système (y compris ceux dans `~/Documents/dotfiles/` pour backup).

---

### Workflow 3 : Actions rapides

**Scénario** : Tu veux copier le chemin absolu d'un fichier pour le coller dans un script.

**Avant Cling** :
```
1. Finder > Localiser le fichier
2. Clic droit > Get Info
3. Sélectionner et copier le chemin
Temps : 15 secondes
```

**Avec Cling** :
```
1. Cmd+K
2. Tape nom du fichier
3. Cmd+C (copie le chemin)
Temps : 3 secondes
```

**Chemin copié** : `/Users/brandon/Projects/blog/docker-compose.yaml`

**Autres actions rapides** :

| Raccourci | Action |
|-----------|--------|
| `Cmd+Shift+C` | Copie nom fichier seul |
| `Cmd+Opt+C` | Copie chemin relatif |
| `Cmd+R` | Renommer (batch rename si multi-sélection) |
| `Space` | QuickLook (preview sans ouvrir) |
| `Cmd+O` | Ouvrir avec... (choix app) |

---

### Workflow 4 : Scripts custom

**Scénario** : Tu veux compresser plusieurs fichiers sélectionnés en `.tar.gz` en 1 raccourci.

**Setup script custom** :

1. **Crée un script** : `~/Scripts/compress.sh`

```bash
#!/bin/bash
# $@ contient tous les fichiers sélectionnés dans Cling

tar -czf ~/Desktop/archive.tar.gz "$@"
notify "Compression terminée"
```

2. **Configure dans Cling** :
   - Settings > Custom Actions
   - Ajoute `~/Scripts/compress.sh`
   - Assigne hotkey : `Cmd+Shift+Z`

3. **Utilisation** :
   - Cling > Sélectionne 5 fichiers (Cmd+Click)
   - `Cmd+Shift+Z`
   - Archive créée sur le Desktop

**Possibilités infinies** :
- Upload vers S3
- Conversion images (ImageMagick)
- Git commit files sélectionnés
- Envoi par email
- Upload FTP/SFTP

💡 **Langage** : Bash, Python, Ruby, Node, Go... ce que tu veux.

---

## Fonctionnalités avancées

### 1. Quick Filters (filtres prédéfinis)

**Problème** : Tu cherches seulement des fichiers `.md` modifiés cette semaine.

**Solution** : Quick Filters.

**Exemples de filtres** :

| Filtre | Résultat |
|--------|----------|
| `.md` | Tous les Markdown |
| `!node_modules` | Exclut node_modules |
| `modified:1w` | Modifiés dernière semaine |
| `size:>10M` | Fichiers > 10 Mo |
| `type:image` | Images uniquement |

**Combinaison** :
```
docker .yml modified:1d
→ Fichiers YAML contenant "docker" modifiés aujourd'hui
```

---

### 2. Recherche dans volumes externes

**Problème** : Tu as un disque externe USB avec des archives. Spotlight ne l'indexe pas toujours.

**Cling** : Indexe **automatiquement** tous les volumes montés (USB, réseau, Time Machine).

**Utilisation** :
```
1. Branche ton disque USB "Backups"
2. Cling le détecte et l'indexe en 30 secondes
3. Cherche normalement : "backup-2024"
4. Résultats instantanés
```

💡 **Bonus** : Cling garde l'index en cache. Si tu rebranches le disque, pas besoin de réindexer.

---

### 3. Batch operations (opérations groupées)

**Problème** : Tu dois renommer 50 fichiers avec un pattern.

**Solution** : Sélection multiple + Batch rename.

**Workflow** :
```
1. Cling > Cherche "screenshot-"
2. Cmd+A (sélectionne tous les résultats)
3. Cmd+R (batch rename)
4. Pattern : screenshot-{date}-{n}.png
5. Enter → 50 fichiers renommés
```

**Autres batch ops** :
- Delete multiple (avec confirmation)
- Copier vers dossier
- Déplacer vers dossier
- Change permissions

---

### 4. Syntaxe de recherche avancée

Cling supporte une syntaxe puissante (héritée de `fd` et `fzf`).

**Exemples** :

| Syntaxe | Résultat |
|---------|----------|
| `^docker` | Commence par "docker" |
| `yaml$` | Finit par "yaml" |
| `!test` | Exclut "test" |
| `'exact match'` | Correspondance exacte |
| `file1 | file2` | OU logique |

**Cas d'usage** :
```
^README !node_modules .md$
→ Fichiers README.md excluant node_modules
```

---

## Cling vs les alternatives

### Cling vs Spotlight (macOS natif)

| Critère | Cling | Spotlight |
|---------|-------|-----------|
| **Fuzzy search** | ✅ Tolérant fautes | ❌ Exacte uniquement |
| **Fichiers système** | ✅ Dotfiles, caches, .git | ❌ Ignorés |
| **Vitesse** | ⚡ <500ms | 🐌 2-5 secondes |
| **Actions clavier** | ✅ Nombreuses | ⚠️ Limitées |
| **Scripts custom** | ✅ Illimités | ❌ |
| **Volumes externes** | ✅ Auto-indexés | ⚠️ Parfois non indexés |
| **RAM** | ⚠️ 300Mo-2Go | ✅ Indexation disque |

**Verdict** : Cling gagne sur **vitesse, fuzzy, et fichiers système**. Spotlight gagne sur **RAM usage**.

**Usage idéal** :
- **Spotlight** : Recherches générales, docs, emails
- **Cling** : Fichiers code, config, dotfiles, power users

---

### Cling vs Raycast / Alfred

| Critère | Cling | Raycast | Alfred |
|---------|-------|---------|--------|
| **Focus** | Recherche fichiers uniquement | Launcher complet | Launcher + workflows |
| **Fuzzy search** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| **Fichiers système** | ✅ Tous | ⚠️ Limités | ⚠️ Limités |
| **Vitesse** | ⚡ Plus rapide | 🐌 Bon | 🐌 Bon |
| **Scripts custom** | ✅ Natifs | ✅ Extensions | ✅ Workflows |
| **Prix** | Gratuit | Gratuit (Pro 96$/an) | Gratuit (Powerpack 59€) |

**Verdict** : Cling est **spécialisé** dans la recherche de fichiers. Raycast/Alfred sont des **launchers complets** avec plein d'autres features.

**Usage idéal** :
- **Cling** : Recherche fichiers pure (dev, sysadmin)
- **Raycast** : Launcher + snippets + extensions + clipboard
- **Alfred** : Workflows complexes + automation

Tu peux utiliser [Raycast](/raycast-macos-outil-productivite-ultime/) pour les commandes ET Cling pour les fichiers. Pas de conflit.

---

### Cling vs Find Any File / EasyFind

| Critère | Cling | Find Any File | EasyFind |
|---------|-------|---------------|----------|
| **Fuzzy search** | ✅ | ❌ | ❌ |
| **Vitesse** | ⚡ Index RAM | 🐌 Index disque | 🐌 Scan temps réel |
| **Résultats affichés** | ⚠️ 30-100 max | ✅ Tous (milliers) | ✅ Tous |
| **Actions rapides** | ✅ Nombreuses | ⚠️ Basiques | ⚠️ Basiques |
| **Scripts custom** | ✅ | ❌ | ❌ |
| **Prix** | Gratuit | Gratuit | Gratuit |

**Verdict** : Find Any File et EasyFind sont **excellents pour chercher TOUS les fichiers** matchant un critère complexe. Cling est **optimisé pour trouver 1 fichier rapidement** et agir dessus.

**Usage idéal** :
- **Cling** : "Je cherche CE fichier docker-compose.yaml"
- **Find Any File** : "Montre-moi TOUS les fichiers .log > 10Mo modifiés cette semaine"

---

### Cling vs Everything (Windows)

| Critère | Cling | Everything (Windows) |
|---------|-------|----------------------|
| **Vitesse** | ⚡ Très rapide | ⚡ **Le plus rapide** |
| **Plateforme** | macOS uniquement | Windows uniquement |
| **Fuzzy search** | ✅ | ⚠️ Via plugin |
| **Index** | RAM | Disque (MFT) |
| **Résultats** | 30-100 max | Millions affichables |

**Verdict** : Everything reste **le roi absolu** sur Windows (utilise la MFT NTFS = instantané). Cling est la **meilleure approximation sur macOS**.

---

## Cas d'usage concrets

### Cas 1 : Développeur fullstack

**Contexte** : 10+ projets actifs, 50+ repos GitHub, configs partout.

**Avant Cling** :
```
Je cherche un docker-compose.yaml
→ Finder > Cherche dans ~/Projects
→ Trop de résultats
→ cd dans Terminal
→ find . -name "docker-compose.yaml"
Temps : 1 minute
```

**Avec Cling** :
```
Cmd+k > "dckr cmp project-x"
→ Résultat instantané
→ Enter → Ouvre dans VS Code
Temps : 3 secondes
```

**Gain quotidien** : 20 recherches/jour × 57 sec = **19 min/jour** = **115h/an**

---

### Cas 2 : Admin système (dotfiles & configs)

**Contexte** : Configs système éparpillées, dotfiles cachés, logs système.

**Cas d'usage fréquent** : Modifier `.zshrc` rapidement.

**Avant Cling** :
```
Terminal > cd ~
nano .zshrc
(ou je ne me rappelle plus si c'est dans ~ ou ~/.config/)
Temps : 15 secondes
```

**Avec Cling** :
```
Cmd+k > "zshrc"
→ Tous les .zshrc trouvés (dont backups)
→ Sélectionne le bon
→ Enter
Temps : 2 secondes
```

**Bonus** : Cling trouve aussi les backups dans `~/dotfiles/` ou Time Machine.

---

### Cas 3 : Créateur de contenu (screenshots & assets)

**Contexte** : 1000+ screenshots, assets éparpillés, nommage incohérent.

**Problème** : Retrouver un screenshot spécifique de "Arc Browser settings".

**Avant Cling** :
```
Finder > Screenshots
→ Scroll dans 1000 fichiers
→ Preview un par un
Temps : 5 minutes
```

**Avec Cling** :
```
Cmd+k > "arc sttngs"
→ Fuzzy match : "screenshot-arc-settings-2024.png"
→ Space (QuickLook preview)
→ Enter (ouvre)
Temps : 5 secondes
```

**Workflow batch** : Sélectionne 10 screenshots → Cmd+Shift+Z → Script compresse en ZIP.

---

### Cas 4 : Data analyst (CSV, logs, datasets)

**Contexte** : Datasets CSV éparpillés, logs de jobs, exports Excel.

**Problème** : Retrouver le CSV `sales-2024-Q3.csv` dans 50+ dossiers.

**Avec Cling** :
```
Cmd+k > "sales 2024 .csv"
→ Tous les CSVs "sales" de 2024
→ Quick Filter : modified:1m (dernier mois)
→ Résultats réduits à 3 fichiers
→ Space (preview contenu)
→ Enter
```

---

## Troubleshooting : Les pièges à éviter

### Problème 1 : Cling ne trouve pas mes fichiers

**Symptômes** : Tu cherches un fichier que tu **sais** existe, mais Cling ne le trouve pas.

**Causes possibles** :
1. **Full Disk Access non accordé**
2. **Fichier dans un dossier exclu** (`.fsignore`)
3. **Index pas encore complet** (première indexation en cours)

**Solutions** :

**A. Vérifie Full Disk Access**
```
Réglages Système > Confidentialité > Full Disk Access
→ Coche Cling
→ Relance Cling
```

**B. Vérifie `.fsignore`**
```bash
cat ~/.fsignore

# Si le dossier est exclu, commente la ligne
# node_modules/  ← Exclu
```

**C. Force ré-indexation**
```
Cling > Settings > Re-index now
→ Attends 1-5 min
```

---

### Problème 2 : Cling consomme trop de RAM

**Symptôme** : Cling utilise 2-3 Go de RAM en permanence.

**Cause** : Trop de fichiers indexés (notamment `node_modules/`, `.git/objects/`, caches).

**Solution** : Exclusions agressives.

**Fichier** : `~/.fsignore`

```bash
# Exclusions recommandées pour réduire RAM
node_modules/
.git/objects/
Library/Caches/
Library/Logs/
*.log
*.tmp
.DS_Store
```

**Résultat** : Index passe de 2 Go à 500 Mo.

💡 **Note** : Quand Cling est en arrière-plan, macOS swap l'index vers disque (libère RAM).

---

### Problème 3 : Recherche ne fonctionne pas (PTY leak)

**Symptôme** : Après quelques heures, Cling ne répond plus aux recherches.

**Cause** : Bug connu (PTY leak) dans certaines versions.

**Workaround officiel** :
```
Settings > Auto-restart every 12 hours
→ Cling redémarre automatiquement pour éviter le leak
```

**Alternative** : Relance Cling manuellement (Cmd+Q puis relance).

💡 **Statut** : Les devs travaillent sur un fix définitif.

---

### Problème 4 : Trop de résultats, impossible de trouver

**Symptôme** : Recherche "config" retourne 500+ résultats, limite à 30 affichés.

**Solutions** :

**A. Affine la recherche**
```
❌ "config"
✅ "dckr cfg" (fuzzy + mots-clés)
✅ "config .yml !test" (exclut test)
```

**B. Utilise Quick Filters**
```
config modified:1w .yml
→ Configs YAML modifiés dernière semaine
```

**C. Augmente la limite (Settings)**
```
Settings > Max results : 100
(par défaut 30)
```

---

## Limitations à connaître

**Cling n'est PAS** :

❌ **Un outil de recherche par contenu** : Cling cherche par **nom de fichier** uniquement, pas dans le contenu
   - Pour ça → `grep`, `ripgrep`, ou EasyFind

❌ **Un remplaçant total de Spotlight** : Spotlight cherche aussi emails, contacts, apps
   - Cling = fichiers uniquement

❌ **Optimisé pour chercher TOUS les fichiers** : Limite 30-100 résultats affichés
   - Pour ça → Find Any File (affiche milliers de résultats)

❌ **Léger en RAM** : 300Mo-2Go en mémoire
   - Si RAM limitée → Stick avec Spotlight ou EasyFind

**Cling EST** :

✅ Parfait pour **trouver 1 fichier rapidement** et agir dessus
✅ Idéal pour **power users** qui connaissent approximativement le nom
✅ Excellent pour **fichiers système, dotfiles, configs**
✅ Génial pour **workflows clavier uniquement**

---

## Conclusion : Faut-il installer Cling ?

**La réponse courte : OUI**, si tu es **développeur, sysadmin, ou power user**.

**Les 3 raisons d'installer Cling maintenant** :

1. ✅ **Recherche fuzzy ultra-rapide** : Trouve n'importe quel fichier en <1 sec
2. ✅ **Gratuit et open source** : Pas de paywall, code sur GitHub
3. ✅ **Fichiers système inclus** : Dotfiles, caches, .git que Spotlight ignore

**Ce que j'aime** :
- Fuzzy search tolérant (fautes de frappe OK)
- Vitesse incroyable (<500ms même avec 1M fichiers)
- Actions clavier puissantes (copier path, renommer, QuickLook)
- Scripts custom (possibilités infinies)
- Gratuit et open source
- Compatible M1/M2/M3/M4

**Ce qui pourrait être mieux** :
- Limite 30-100 résultats affichés (pas comme Everything Windows)
- Consommation RAM (300Mo-2Go)
- Bug PTY leak (workaround = auto-restart)
- Pas de recherche par contenu (nom de fichier uniquement)
- Courbe apprentissage (syntaxe avancée)

**Mon verdict perso** : J'utilise Cling **depuis 6 mois** pour chercher mes fichiers de config, dotfiles, et scripts. Combiné avec [rcmd](/rcmd-alternative-cmd-tab-macos/), [Clop](/2025-11-27-clop-compression-images-videos-macos/), et [Lunar](/2025-11-27-lunar-luminosite-ecrans-externes-macos/), c'est le **quatuor Low-Tech Guys parfait**.

**Pour qui c'est un must** :
- ✅ Développeurs (configs, dotfiles, repos)
- ✅ Sysadmins (fichiers système, logs)
- ✅ Power users (workflow clavier)
- ✅ Créateurs de contenu (retrouver assets rapidement)

**Pour qui c'est optionnel** :
- ⚠️ Utilisateurs occasionnels (Spotlight suffit)
- ⚠️ RAM limitée (<8 Go)
- ⚠️ Besoin de recherche par contenu (utilise `grep` ou EasyFind)

**ROI** : Si tu cherches 10 fichiers par jour et que Cling te fait gagner 30 sec par recherche → **5 min/jour** = **30h/an**. Pour **0€**.

Alors, prêt à chercher tes fichiers comme un ninja ? 🥷

---

## 🔗 Articles connexes qui pourraient t'intéresser

- **[rcmd : Le raccourci qui tue Cmd+Tab](/rcmd-alternative-cmd-tab-macos/)** : Switch entre apps ultra-rapidement
- **[Clop : Compression automatique](/2025-11-27-clop-compression-images-videos-macos/)** : Optimise tes fichiers en arrière-plan
- **[Lunar : Contrôle luminosité écrans externes](/2025-11-27-lunar-luminosite-ecrans-externes-macos/)** : DDC natif pour tes moniteurs
- **[Raycast : L'outil qui transforme macOS](/raycast-macos-outil-productivite-ultime/)** : Launcher complet (complémentaire à Cling)
- **[Installation Homebrew sur macOS](/installation-homebrew-macos/)** : Indispensable pour installer Cling

---

## 💡 Ressources utiles

- [Site officiel Cling](https://lowtechguys.com/cling/)
- [GitHub Cling (open source)](https://github.com/FuzzyIdeas/Cling)
- [fd (outil Rust sous-jacent)](https://github.com/sharkdp/fd)
- [fzf (fuzzy finder)](https://github.com/junegunn/fzf)
- [Low Tech Guys (tous leurs outils)](https://lowtechguys.com/)

---
