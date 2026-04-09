---
title: "Clop : Compresse tes images et vidéos automatiquement sur macOS (gratuit)"
pubDatetime: "2025-11-27T00:00:00+00:00"
author: Brandon Visca
description: "Découvre Clop, l'outil qui compresse automatiquement tes images et vidéos dès que tu les copies. Fini les fichiers trop lourds pour les emails et Slack...."
tags:
  - macos
  - productivite
  - debutant
  - multimedia
  - guide
  - compression
---

![Illustration 1 — Clop](https://res.cloudinary.com/dlkn3lxkk/image/upload/v1765130954/brandonviscacom/CleanShot_2025-12-07_at_19.07.06_2x_kfnaxs.webp)
*Légende : Interface Clop - compression automatique en arrière-plan*


## Introduction : Le drame des fichiers trop lourds

![Capture d'écran — Introduction Le drame des fichiers trop lourds](https://lowtechguys.com/static/video/screenshot-copy-optimise-paste-in-email.mp4)

On connaît tous cette situation frustrante :

Tu prends un screenshot sur ton Mac. 3840x2160 pixels, **8 Mo**. Tu veux l'envoyer par email ou Slack.

**"Fichier trop volumineux."**

Alors tu ouvres Photoshop, ou Preview, tu exportes en qualité réduite, tu attends, tu re-testes... **5 minutes perdues** pour un simple screenshot.

Et si je te disais qu'il existe un outil qui **compresse automatiquement** tout ce que tu copies dans ton clipboard, **sans que tu aies à faire quoi que ce soit** ?

**Le pitch** :
- Tu fais un screenshot → Clop le compresse instantanément
- Tu copies une image → Clop l'optimise en arrière-plan
- Tu enregistres un screencast → Clop réduit la vidéo de 90% automatiquement

**Résultat** : Tes fichiers passent de 8 Mo à 800 Ko. **Qualité visuelle identique**. Zéro effort de ta part.

Bienvenue dans le monde de **Clop**, l'optimiseur magique qui va te faire gagner des heures (et des gigas de stockage).

💡 **Ce que tu vas apprendre dans ce guide** :
- Installer Clop en 2 minutes (gratuit jusqu'à 5 fichiers/session)
- Configuration pour compression automatique clipboard
- Optimiser images, vidéos, PDFs et GIFs
- Intégration avec CleanShot X, Shottr, Dropzone
- Alternatives et comparaisons (ImageOptim, TinyPNG, etc.)

Let's go ! 🚀

## Table of content



## Qu'est-ce que Clop ?

**Clop** (de "Clipboard Optimizer"), c'est un outil développé par [Low Tech Guys](https://lowtechguys.com/) qui optimise automatiquement **images, vidéos, PDFs et contenus clipboard** sur macOS.

![Capture d'écran — Quest-ce que Clop](https://lowtechguys.com/static/video/screenshot-copy-optimise-paste-in-email.mp4)
### Le concept en une phrase

**Copy large, paste small, send fast.**

Dès que tu copies une image ou fais un screenshot, Clop la compresse en arrière-plan. Quand tu colles, c'est la version optimisée qui arrive. Transparent. Automatique. Magique.

### Pourquoi c'est génial ?

✅ **Compression automatique** : Tu ne touches à rien, Clop bosse en arrière-plan
✅ **Qualité préservée** : Algorithmes intelligents (pngquant, mozjpeg, etc.)
✅ **Multi-formats** : PNG, JPEG, HEIC, GIF, MP4, MOV, PDF
✅ **Apple Silicon optimisé** : Utilise le Media Engine chip (M1/M2/M3/M4)
✅ **Gratuit** : Jusqu'à 5 fichiers/session (largement suffisant pour la plupart)

### Les chiffres qui parlent

**Réductions moyennes constatées** :
- **Screenshots PNG** : 8 Mo → 800 Ko (90% de réduction)
- **Screencasts MOV** : 50 Mo → 5 Mo (90% de réduction)
- **Photos JPEG** : 5 Mo → 1 Mo (80% de réduction)
- **PDFs** : 10 Mo → 2 Mo (80% de réduction)

**Qualité** : Perte visuelle imperceptible à l'œil nu dans 95% des cas.


## Installation de Clop : 3 méthodes

### Méthode 1 : Homebrew (recommandée)

![Capture d'écran — Méthode 1 Homebrew recommandée](https://res.cloudinary.com/dlkn3lxkk/image/upload/v1765131079/brandonviscacom/CleanShot_2025-12-07_at_19.08.07_2x_ylt3yj.webp)

Si tu as Homebrew installé ([sinon, va lire mon guide Homebrew](https://brandonvisca.com/installation-homebrew-macos/)) :

```bash
# Installation en une ligne
brew install --cask clop
```

**Avantages** :
- Mises à jour automatiques
- Désinstallation propre
- Gestion centralisée

⚠️ **Pas encore Homebrew ?** → [[installation-homebrew-macos|Guide installation Homebrew macOS]]


### Méthode 3 : Installation manuelle

1. **Télécharge Clop** : [lowtechguys.com/clop](https://lowtechguys.com/clop/)
2. **Glisse `Clop.app` dans `/Applications`**
3. **Premier lancement** : Clic droit > Ouvrir
4. **Autorise les permissions** : Accessibilité + Enregistrement écran (si vidéos)

![Capture d'écran — Méthode 3 Installation manuelle](https://res.cloudinary.com/dlkn3lxkk/image/upload/v1765131528/brandonviscacom/CleanShot_2025-12-07_at_19.17.08_2x_ljkmyp.webp)

💡 **Astuce** : Active "Lancer au démarrage" dans les préférences. Clop doit tourner en permanence pour être efficace.


## Configuration essentielle en 5 minutes

![Capture d'écran — Configuration essentielle en 5 minutes](https://res.cloudinary.com/dlkn3lxkk/image/upload/v1765131553/brandonviscacom/CleanShot_2025-12-07_at_19.17.25_2x_nl8u7q.jpg)

### Première utilisation : Setup de base

Au premier lancement, Clop te demande :

1. **Accessibilité** : Autoriser pour surveiller le clipboard
2. **Enregistrement écran** (optionnel) : Pour optimiser les screencasts automatiquement
3. **Mode d'optimisation** : Automatique (recommandé) vs Manuel

![Capture d'écran — Première utilisation Setup de base](https://res.cloudinary.com/dlkn3lxkk/image/upload/v1765131983/brandonviscacom/CleanShot_2025-12-07_at_19.24.17_2x_wvwlkl.webp)

### Réglages recommandés pour débutants

```
✅ Automatic optimization : Enabled
✅ Launch at login : Enabled
✅ Optimize clipboard images : Enabled
✅ Optimize videos : Enabled (si tu fais des screencasts)
✅ Show floating preview : Enabled (pour voir le résultat)
✅ Aggressive optimization : Disabled (pour commencer)
```

**Pourquoi ces réglages ?**
- Optimisation automatique = zéro friction
- Floating preview = tu vois ce que Clop fait (rassurant)
- Aggressive OFF = tu gardes une qualité maximale

💡 **Pour les power users** : Active "Aggressive optimization" si tu veux des fichiers encore plus petits (perte qualité légèrement perceptible).


## Utilisation : 3 workflows magiques

### Workflow 1 : Screenshots automatiques

**Le problème** : Tu fais 20 screenshots par jour pour ton blog/docs/emails. Chacun fait 5-8 Mo.

**Avec Clop** :

1. Tu fais ton screenshot (Cmd+Shift+4)
2. Clop détecte l'image dans le clipboard
3. Compression automatique en 0.5 seconde
4. Tu colles (Cmd+V) → Version optimisée !

**Résultat** : Screenshot qui passerait pas dans un email ? Maintenant il passe. Simple.


### Workflow 2 : Screencasts (enregistrements écran)

**Le problème** : Tu enregistres une démo de 2 minutes. Fichier MOV de 80 Mo. Impossible à envoyer.

**Avec Clop** :

1. Tu fais ton screencast (Cmd+Shift+5)
2. Tu arrêtes l'enregistrement
3. **Clop l'optimise automatiquement** pendant que tu continues à bosser
4. Une miniature flottante apparaît avec le fichier optimisé (8 Mo)
5. Tu glisses-déposes dans Slack/email/Notion

**Gain** : 80 Mo → 8 Mo. **90% de réduction**. Qualité visuelle identique.

**Bonus** : Clop utilise le **Media Engine** de ton Mac (M1/M2/M3/M4) pour encoder sans bouffer le CPU. Batterie préservée.


### Workflow 3 : Drag & Drop intelligent

![Capture d'écran — Workflow 3 Drag Drop intelligent](https://lowtechguys.com/static/video/screenshot-copy-optimise-paste-in-email.mp4)

**Le problème** : Tu as 10 images à compresser avant de les uploader sur ton site WordPress.

**Avec Clop** :

1. Ouvre la **Drop Zone** de Clop (icône menu bar)
2. Glisse tes 10 images dans la zone
3. Clop les compresse en batch
4. Tu récupères les versions optimisées prêtes à uploader

**Alternative** : Configure Clop pour surveiller un dossier (ex: `~/Downloads`). Tout ce qui y tombe est automatiquement optimisé.


## Fonctionnalités avancées

### 1. Downscaling intelligent

![Capture d'écran — 1 Downscaling intelligent](https://lowtechguys.com/static/video/screenshot-downscale-in-email.mp4)

**Problème** : Ton screenshot fait 3840x2160 (4K) mais tu n'as besoin que de 1920x1080 pour un article de blog.

**Solution Clop** :

1. Après compression, un **bouton flottant** apparaît
2. Clique dessus → Options de downscaling
3. Choisis : 90%, 75%, 50%, 25% ou résolution custom
4. Clop redimensionne + re-compresse

**Résultat** : Screenshot 4K de 8 Mo → Image 1080p de 200 Ko. **96% de réduction**.


### 2. Conversion de formats

Clop convertit automatiquement les formats moins compatibles :

- **HEIC** (iPhone) → **JPEG** (universel)
- **TIFF** → **PNG**
- **MOV** → **MP4** (plus compatible web)

**Cas d'usage** : Tu reçois des photos iPhone en HEIC. Tu les copies. Clop les convertit en JPEG automatiquement. Tu colles dans Gmail. Ça marche.


### 3. Crop et aspect ratio

Tu peux **cropper** images et vidéos directement depuis le floating preview :

1. Clique sur le thumbnail flottant
2. Choisis "Crop"
3. Sélectionne une zone ou un aspect ratio (16:9, 4:3, 1:1, custom)
4. Clop crop + re-optimise

**Gain de temps** : Plus besoin d'ouvrir un éditeur séparé.


### 4. Intégration macOS Shortcuts

**Pour les power users** : Clop s'intègre avec **Shortcuts.app**.

![Capture d'écran — 4 Intégration macOS Shortcuts](https://res.cloudinary.com/dlkn3lxkk/image/upload/v1765132833/brandonviscacom/CleanShot_2025-12-07_at_19.39.51_2x_eo4rbc.jpg)

**Exemples de workflows** :

**A. Optimisation automatique des photos avant email**
```
1. Sélectionne photos dans Finder
2. Raccourci Shortcuts : "Optimize and Email"
3. Clop optimise → Ouvre Mail avec photos attachées
```

**B. Pipeline YouTube**
```
1. Enregistre screencast
2. Clop optimise vidéo
3. Shortcuts upload sur Google Drive automatiquement
```

**C. Batch processing dossier complet**
```
1. Sélectionne dossier avec 100 images
2. Shortcuts appelle Clop SDK
3. Toutes les images optimisées en 30 secondes
```


### 5. Folders watching (surveillance de dossiers)

![Capture d'écran — 5 Folders watching surveillance de dossiers](https://res.cloudinary.com/dlkn3lxkk/image/upload/v1765133052/brandonviscacom/CleanShot_2025-12-07_at_19.42.54_2x_cfmbrq.webp)

Configure Clop pour **surveiller des dossiers spécifiques** :

**Setup** :
1. Préférences Clop > Folders
2. Ajoute un dossier (ex: `~/Screenshots`)
3. Choisis l'action : Optimiser + remplacer OU Optimiser + copier ailleurs

**Cas d'usage** : Tu sauvegardes tous tes screenshots dans un dossier. Clop les optimise automatiquement dès qu'ils apparaissent. Zéro manipulation manuelle.


### 6. Intégration CleanShot X / Shottr

Si tu utilises **CleanShot X** ou **Shottr** (apps screenshots premium), Clop s'intègre nativement :

**Configuration** :
1. Dans CleanShot X : Active "Copy to clipboard after capture"
2. Clop détecte les screenshots CleanShot
3. Optimisation automatique avant que tu colles

**Résultat** : Tu gardes la qualité CleanShot, mais avec des fichiers 10x plus petits.

Tu utilises déjà [[reduire-taille-images-mac-webp|WebP sur macOS]] ? Combine Clop + WebP pour des gains encore plus importants.


## Clop vs les alternatives : Le match

### Clop vs ImageOptim

| Critère | Clop | ImageOptim |
|---------|------|------------|
| **Automatisation** | ✅ Clipboard + folders | ❌ Drag & drop manuel |
| **Vidéos** | ✅ MP4, MOV, GIF | ❌ Images uniquement |
| **PDFs** | ✅ Optimisation PDF | ❌ Non supporté |
| **Prix** | 💰 Gratuit (5 fichiers/session) ou 15$ lifetime | 💰 Gratuit complet |
| **Interface** | 🎯 Floating preview + drop zone | 🗂️ Fenêtre classique |

**Verdict** : ImageOptim est excellent pour du batch processing manuel, mais Clop gagne sur l'**automatisation** et le **support multi-formats**.

**Usage idéal** : Utilise Clop au quotidien (clipboard automatique) + ImageOptim pour optimiser un dossier entier de 500 images ponctuellement.


### Clop vs TinyPNG / Squoosh

| Critère | Clop | TinyPNG | Squoosh |
|---------|------|---------|---------|
| **Localisation** | 🖥️ App native macOS | ☁️ Service web | ☁️ Service web |
| **Formats** | PNG, JPEG, HEIC, GIF, MP4, MOV, PDF | PNG, JPEG | Tous formats images |
| **Automatisation** | ✅ Clipboard + folders | ❌ Upload manuel | ❌ Upload manuel |
| **Batch processing** | ✅ Drag & drop | ✅ Jusqu'à 20 fichiers | ❌ Un par un |
| **Prix** | Gratuit (limité) ou 15$ | Gratuit (limité) ou 25$/an | Gratuit complet |

**Verdict** : TinyPNG et Squoosh sont pratiques pour un usage ponctuel, mais **Clop gagne sur la productivité** (pas besoin d'ouvrir un navigateur, tout est automatique).


### Clop vs Compressor / HandBrake (vidéos)

| Critère | Clop | Compressor | HandBrake |
|---------|------|-----------|-----------|
| **Simplicité** | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| **Automatisation** | ✅ Compression auto screencasts | ❌ Manuel | ❌ Manuel |
| **Vitesse** | ⚡ Utilise Media Engine (M1+) | 🐌 CPU intensif | 🐌 CPU/GPU |
| **Presets vidéo** | 🎯 1 preset optimisé | 🎛️ 50+ presets | 🎛️ 100+ presets |
| **Prix** | 15$ lifetime | 50$ (part Logic Pro) | Gratuit open source |

**Verdict** : Pour des **screencasts rapides**, Clop est imbattable. Pour de l'**encodage vidéo pro** avec contrôle total, HandBrake reste le roi.


## Cas d'usage concrets

### Cas 1 : Blogueur / Créateur de contenu (mon cas)

**Problème** : J'écris 10-15 articles par mois avec 15-20 screenshots chacun. Fichiers trop lourds pour WordPress (limite 10 Mo/fichier).

**Avec Clop** :

```
Workflow quotidien :
1. Screenshot d'un terminal (Cmd+Shift+4)
2. Clop compresse : 6 Mo → 600 Ko
3. Je colle dans Obsidian
4. Upload vers WordPress : aucun problème

Gain : Plus de message "fichier trop lourd"
Temps gagné : 5 min par article = 50-75 min/mois
```

Je combine Clop avec mon workflow [[reduire-taille-images-mac-webp|WebP macOS]] pour des images encore plus optimisées.


### Cas 2 : Support technique / Documentation

**Problème** : Tu envoies 20-30 screenshots par jour à tes collègues/clients par email ou Slack. Les pièces jointes font exploser les boîtes mail.

**Avec Clop** :

```
Avant Clop :
- Screenshot : 8 Mo
- Email bloqué : "Fichier trop volumineux"
- Export manuel Preview : 2 minutes
- Re-test : 1 minute
Total : 3 minutes par screenshot

Avec Clop :
- Screenshot : 8 Mo → 800 Ko (auto)
- Colle dans email : 0 secondes
Total : 0 secondes supplémentaires

Gain sur 20 screenshots/jour : 1 heure par jour
```


### Cas 3 : Créateur YouTube / Vidéaste

**Problème** : Tu enregistres des screencasts pour tes tutos. Fichiers MOV de 500 Mo - 2 Go. Upload YouTube interminable.

**Avec Clop** :

```
Screencast 10 min :
- MOV original : 1.5 Go
- Clop optimise : 150 Mo (90% réduc)
- Upload YouTube : 15 min au lieu de 2h

Bonus :
- Utilise Media Engine (M1/M2)
- Batterie non impactée
- Qualité 1080p préservée
```


### Cas 4 : Designer / Graphiste

**Problème** : Tu partages des mockups et wireframes avec clients. Fichiers PNG énormes. Clients ouvrent sur téléphone = galère.

**Avec Clop** :

```
Workflow client :
1. Export Figma : PNG 4K, 12 Mo
2. Copie dans clipboard
3. Clop compresse + downscale à 1080p
4. Colle dans email : 1.2 Mo
5. Client ouvre sur iPhone : instantané

Alternative sans Clop :
1. Export Figma
2. Ouvre Photoshop
3. "Save for Web"
4. Ajuste qualité manuellement
5. Export
Total : 5 minutes par fichier
```


## Troubleshooting : Les pièges à éviter

### Problème 1 : Clop ne détecte pas mes screenshots

**Symptôme** : Tu fais un screenshot, rien ne se passe.

**Causes possibles** :
1. Clop n'est pas lancé
2. Permissions Accessibilité non accordées
3. App de screenshot tierce (CleanShot X) configurée pour ne pas copier dans clipboard

**Solutions** :

1. **Vérifie que Clop tourne** : Icône dans menu bar visible ?
2. **Permissions** : Réglages Système > Confidentialité > Accessibilité → Coche Clop
3. **CleanShot X** : Active "Copy to clipboard after capture"


### Problème 2 : Qualité dégradée visible

**Symptôme** : Tes images compressées ont des artefacts visibles (pixellisation, banding).

**Solutions** :

1. **Désactive "Aggressive optimization"** dans les préférences
2. **Augmente la qualité** : Préférences > Quality slider à 90%
3. **Pour photos** : Utilise JPEG quality 85% minimum

💡 **Astuce** : Pour des photos artistiques où chaque détail compte, désactive Clop temporairement (icône menu bar > Pause).


### Problème 3 : Clop ralentit mon Mac

**Symptôme** : Ventilateurs qui tournent, Mac qui lag pendant la compression.

**Causes** :
- Compression de vidéos 4K massives
- Aggressive optimization activé sur de très gros fichiers

**Solutions** :

1. **Désactive l'optimisation vidéo** si tu ne fais pas de screencasts
2. **Limite la résolution** : Préférences > Max resolution 1080p
3. **Sur Mac Intel** : Réduis le nombre de fichiers traités simultanément

💡 **Note** : Sur Apple Silicon (M1+), le Media Engine encode les vidéos sans CPU → aucun ralentissement.


### Problème 4 : Licence ne reste pas activée (version payante)

**Symptôme** : Clop redemande la licence à chaque redémarrage.

**Solution officielle** :

```bash
# Supprimer les fichiers de licence corrompus
rm -rf "$HOME/Library/Application Support/Clop/"*
killall Clop
open -a Clop

# Puis réactive avec ta clé
```

**Vérifier que Paddle n'est pas bloqué** :
- Ouvre Safari : [v3.paddleapi.com/3.2/license/verify](https://v3.paddleapi.com/3.2/license/verify)
- Si ça charge → OK
- Si erreur → Ton firewall (Little Snitch, LuLu) bloque Paddle

⚠️ **Note** : Ce problème ne concerne que la version payante. La version gratuite n'a pas de licence.


## Version gratuite vs Pro : Faut-il payer ?

### Version gratuite (0€)

**Limitations** :
- ✅ Optimisation clipboard automatique
- ✅ Images, vidéos, PDFs
- ✅ Downscaling et crop
- ❌ **Limite : 5 fichiers par session**

**C'est suffisant si** :
- Tu fais 5-10 screenshots par jour max
- Usage occasionnel
- Tu veux tester avant d'acheter


### Version Pro (15$ lifetime)

**Ce que tu gagnes** :
- ✅ **Optimisations illimitées**
- ✅ Folders watching (surveillance dossiers)
- ✅ Batch processing sans limite
- ✅ Priority support

**Ça vaut le coup si** :
- Tu fais +20 screenshots par jour
- Tu crées du contenu régulièrement (blog, YouTube, docs)
- Tu veux automatiser complètement ton workflow

**Mon avis perso** : 15$ lifetime pour une app que j'utilise 50 fois par jour ? **No brainer**. C'est le prix de 2 cafés Starbucks.

**Alternative** : Clop est aussi disponible sur **Setapp** (abonnement 10$/mois pour 240+ apps). Si tu utilises déjà Setapp, c'est inclus.


## Alternatives si Clop ne te convient pas

### 1. ImageOptim (gratuit, images uniquement)

**Pour qui** : Batch processing d'images, pas besoin d'automatisation

- [Site officiel ImageOptim](https://imageoptim.com/)
- Gratuit, open source
- Excellents algos de compression
- Mais : Drag & drop manuel, pas de vidéos


### 2. Squoosh (gratuit, web)

**Pour qui** : Usage ponctuel, pas d'installation

- [squoosh.app](https://squoosh.app/)
- Tous formats images
- Comparaison avant/après visuelle
- Mais : Web only, pas d'automatisation


### 3. HandBrake (gratuit, vidéos pro)

**Pour qui** : Encodage vidéo avancé avec contrôle total

- [handbrake.fr](https://handbrake.fr/)
- 100+ presets vidéo
- Open source
- Mais : Complexe, pas d'automatisation screencasts


### 4. TinyPNG (freemium, web)

**Pour qui** : Compression PNG/JPEG simple

- [tinypng.com](https://tinypng.com/)
- Excellent ratio compression/qualité
- API disponible
- Mais : 20 fichiers max gratuit, web only


## Conclusion : Faut-il installer Clop ?

**La réponse courte : OUI**, si tu manipules images/vidéos régulièrement sur macOS.

**Les 3 raisons d'installer Clop maintenant** :

1. ✅ **C'est automatique** : Tu copies, Clop compresse, tu colles. Zéro friction.
2. ✅ **C'est gratuit** : Version free largement suffisante pour débuter (5 fichiers/session)
3. ✅ **Gain de temps massif** : 1-2 heures économisées par semaine

**Ce que j'aime** :
- Automatisation totale (clipboard + folders)
- Compression intelligente (perte qualité imperceptible)
- Support multi-formats (images, vidéos, PDFs)
- Utilise le Media Engine (Apple Silicon) → batterie préservée
- Interface minimaliste (floating preview discret)

**Ce qui pourrait être mieux** :
- Version gratuite limitée à 5 fichiers/session (mais 15$ lifetime = bon deal)
- Aggressive mode peut dégrader la qualité photos artistiques
- Pas de presets avancés comme HandBrake (mais c'est voulu, simplicité first)

**Mon verdict perso** : J'utilise Clop **tous les jours depuis 8 mois**. Combiné avec [[rcmd-alternative-cmd-tab-macos|rcmd]] et [[reduire-taille-images-mac-webp|WebP]], c'est le trio gagnant productivité macOS.

**Temps d'adaptation** : 0 seconde. Tu installes, tu configures une fois, tu oublies. Ça tourne en arrière-plan.

**ROI** : Si tu fais 20 screenshots par jour et que Clop te fait gagner 30 secondes par screenshot, ça fait **10 minutes par jour** = **60 heures par an**. Pour 0€ (ou 15$ si version Pro).

Alors, prêt à dire adieu aux fichiers trop lourds ? 🚀


## 🔗 Articles connexes qui pourraient t'intéresser

- **[[reduire-taille-images-mac-webp|Réduire la taille des images Mac avec WebP]]** : Combine Clop + WebP pour une compression ultime
- **[[rcmd-alternative-cmd-tab-macos|rcmd : Le raccourci qui tue Cmd+Tab]]** : Switch entre apps ultra-rapidement
- **[[raycast-macos-outil-productivite-ultime|Raycast : L'outil qui transforme macOS]]** : Launcher complet pour automatiser tes workflows
- **[[installation-homebrew-macos|Installation Homebrew sur macOS]]** : Indispensable pour installer Clop et autres outils


## 💡 Ressources utiles

- [Site officiel Clop](https://lowtechguys.com/clop/)
- [GitHub Clop (open source)](https://github.com/FuzzyIdeas/Clop)
- [Clop sur Mac App Store](https://apps.apple.com/app/clop/id1611554949)
- [Clop SDK (pour devs)](https://github.com/FuzzyIdeas/ClopSDK)
- [Low Tech Guys (tous leurs outils)](https://lowtechguys.com/)

## Articles connexes

- [Magnet macOS : Le gestionnaire de fenêtres qui va transforme](/magnet-macos-gestionnaire-fenetres-guide-complet/)
- [Ice : L'alternative gratuite à Bartender qui révolutionne vo](/ice-macos-gestionnaire-barre-menu-gratuit-2025/)
