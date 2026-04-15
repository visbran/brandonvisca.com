---
title: "Compresser images Mac en WebP : méthode qui économise 70% d'espace"
description: "Compresser images Mac en WebP avec cwebp et Automator. Méthode gratuite, clic droit dans le Finder, gain 50 à 80% de taille. Tuto étape par étape."
pubDatetime: "2025-06-12T20:41:20+02:00"
modDatetime: "2026-04-15T00:00:00+01:00"
author: Brandon Visca
tags:
  - webp
  - macos
  - homebrew
  - automator
  - guide
  - debutant
featured: false
draft: false
focusKeyword: compresser images mac
---
> 💡 **TL;DR**
> - `cwebp` via Homebrew + une action Automator = compression WebP en clic droit dans le Finder
> - Gain moyen de 50 à 80% sur JPEG et PNG, sans perte de qualité visible
> - Installation en 10 minutes, zéro logiciel payant

Tu as 200 photos de vacances à 8 Mo chacune. Résultat : 1,6 Go d'espace bouffé, des temps de chargement interminables et un iCloud qui sature.

La réalité : 90% de tes images sont **sur-dimensionnées** pour leur usage réel. Une photo Instagram n'a pas besoin de peser 5 Mo, une image de blog peut faire 200 Ko au lieu de 2 Mo.

**La solution :** le format WebP divise le poids de tes images par 2 à 5 sans aucune différence visible à l'œil nu. macOS ne sait pas le faire nativement, mais `cwebp` + Automator, si.

## Table des matières

## Pourquoi tes images sont-elles si lourdes ?

### Le problème technique expliqué simplement

**JPEG/PNG = formats anciens :**

- JPEG : créé en 1992 (oui, ça date !)
- PNG : optimisé pour la transparence, pas la compression
- **Résultat :** beaucoup de « gras » dans le fichier

**WebP = format moderne :**

- Développé par Google en 2010
- Compression **25 à 80% plus efficace**
- Supporté par tous les navigateurs modernes
- **Même qualité visuelle**

### Comparaison concrète

| Format | Taille fichier | Temps de chargement |
|:--:|:--:|:--:|
| JPEG original | 2,4 Mo | 8 secondes |
| PNG optimisé | 1,8 Mo | 6 secondes |
| **WebP** | **0,7 Mo** | **2 secondes** |

> 💡 **Impact réel :** Sur un site de 50 images, tu passes de 120 Mo à 35 Mo. Tes visiteurs te remercieront.

---

## Compresser images Mac en WebP : la méthode automatique

Voici ce qu'on va construire :

1. **Installation de `cwebp`** (2 minutes)
2. **Création d'une action « clic droit »** dans le Finder via Automator (5 minutes)
3. **Test sur tes vraies images** (2 minutes)

**Résultat final :** tu sélectionnes des images → clic droit → conversion WebP automatique.

---

## Étape 1 : Installer cwebp via Homebrew

### Prérequis : Homebrew

Si tu n'as pas encore Homebrew sur ton Mac, commence par 👉 **[ce guide complet d'installation d'Homebrew sur macOS](https://brandonvisca.com/installation-homebrew-macos/)**.

### Installation

```bash
brew install webp
```

Vérifie que ça s'est bien passé :

```bash
cwebp -version
# Devrait afficher : 1.3.2 (ou plus récent)
```

> 🧠 **Pourquoi `cwebp` ?** C'est l'outil **officiel de Google** pour WebP. Plus fiable et performant que les alternatives tierces ou les apps payantes.

---

## Étape 2 : Créer l'action Automator

### Lancement d'Automator

1. **Applications** → **Automator** → **Nouvelle action rapide**
2. **Configuration** (en haut à droite) :
   - Le flux reçoit : **fichiers image**
   - Dans : **Finder**

### Le script à coller

Glisse **« Exécuter un script Shell »** et colle ce code :

```bash
for FILE in "$@"
do
  /opt/homebrew/bin/cwebp -q 85 "$FILE" -o "${FILE%.*}.webp"
done
```

⚠️ **Si ton Mac est Intel** (pas Apple Silicon), le chemin de `cwebp` est différent : remplace `/opt/homebrew/bin/cwebp` par `/usr/local/bin/cwebp`. Vérifie avec `which cwebp` dans le Terminal.

### Sauvegarde

Sauvegarde l'action avec un nom parlant, par exemple **"Convertir en WebP"**. Elle apparaîtra dans le menu clic droit du Finder sur toutes tes images.

---

## Étape 3 : Tester sur tes images

Sélectionne une ou plusieurs images dans le Finder → clic droit → **Actions rapides** → **Convertir en WebP**.

Les fichiers `.webp` sont créés dans le même dossier, les originaux sont conservés. À toi de supprimer les originaux une fois satisfait du résultat.

---

## Ajuster la qualité selon l'usage

Le paramètre `-q` contrôle le compromis qualité/poids :

```bash
# Photos réseaux sociaux (compression agressive)
-q 60    # Gain: ~80%, qualité acceptable

# Images de blog/e-commerce (équilibré)
-q 85    # Gain: ~70%, qualité excellente

# Portfolio/galerie pro (compression légère)
-q 95    # Gain: ~40%, qualité maximale
```

### Mode compression extrême

Pour maximiser les gains, remplace la ligne de compression dans le script par :

```bash
/opt/homebrew/bin/cwebp -q 75 -m 6 -sharp_yuv -af "$FILE" -o "${FILE%.*}.webp"
# -m 6 : méthode de compression maximale
# -sharp_yuv : améliore les détails fins
# -af : filtre anti-aliasing
```

---

## Dépannage

### `cwebp` non trouvé dans Automator

Automator n'hérite pas du PATH du Terminal. Utilise le chemin absolu :

```bash
which cwebp
# Copie le chemin affiché et remplace dans le script
```

### Réinstallation propre

```bash
brew uninstall webp
brew install webp
```

---

## Impact concret sur tes projets

### Site web / Blog

**Avant :** 50 images × 2 Mo = 100 Mo  
**Après :** 50 images × 0,6 Mo = 30 Mo  
**Gain :** site 3× plus rapide, meilleur score Google PageSpeed

### Stockage iCloud/Google

**Avant :** 1000 photos = 8 Go  
**Après :** 1000 photos = 2,4 Go  
**Gain :** 5,6 Go récupérés

### Envoi par email

**Avant :** 1 photo = pièce jointe refusée  
**Après :** 5 photos = envoi instantané

### Batch processing d'un dossier entier

```bash
find ~/Pictures -name "*.jpg" -exec /opt/homebrew/bin/cwebp -q 85 {} -o {}.webp \;
```

---

## Conclusion

`cwebp` + Automator, c'est la combinaison la plus simple pour arrêter de subir des images trop lourdes sur Mac. Zéro abonnement, zéro interface complexe. Juste un clic droit et c'est réglé.

Dans mon workflow, j'applique ce script sur toutes les captures d'écran avant de les publier sur le blog. Ça prend deux secondes et ça fait souvent passer des fichiers de 800 Ko à 150 Ko.

**Prochaine étape :** si tu veux aller plus loin dans l'automatisation macOS, jette un œil à Raycast. Les workflows s'enchaînent naturellement avec ce genre d'outil.

---

## Pour aller plus loin

- [Installer Homebrew sur macOS](https://brandonvisca.com/installation-homebrew-macos/) – prérequis de ce tuto
- [Documentation officielle cwebp](https://developers.google.com/speed/webp/docs/cwebp) – toutes les options de compression
- [Raycast : outil de productivité ultime sur macOS](https://brandonvisca.com/raycast-macos-outil-productivite-ultime/) – pour aller encore plus loin dans l'automatisation
