---
title: "Swap Linux : comment ne pas transformer ton serveur en escargot asthmatique"
pubDatetime: "2025-07-13T22:16:30+02:00"
author: Brandon Visca
description: "Guide pratique pour configurer, optimiser et gérer le swap sous Linux. Fichiers swap, swappiness, redimensionnement et monitoring avancé."
tags:
  - linux
  - sysadmin
  - intermediaire
  - performance
  - guide
  - swap
---


- [Vérifier l’état actuel de ton swap](#verifier-letat-actuel-de-ton-swap)
- [Méthode recommandée : créer un fichier swap (pas une partition)](#methode-recommandee-creer-un-fichier-swap-pas-une-partition)
  - [Étape 1 : Créer le fichier swap](#etape-1-creer-le-fichier-swap)
  - [Étape 2 : Sécuriser les permissions](#etape-2-securiser-les-permissions)
  - [Étape 3 : Formater et activer](#etape-3-formater-et-activer)
  - [Étape 4 : Rendre permanent](#etape-4-rendre-permanent)
- [Optimiser les performances avec swappiness](#optimiser-les-performances-avec-swappiness)
- [Gérer plusieurs fichiers swap (si tu as plusieurs disques)](#gerer-plusieurs-fichiers-swap-si-tu-as-plusieurs-disques)
- [Redimensionner un fichier swap existant](#redimensionner-un-fichier-swap-existant)
- [Supprimer proprement un swap](#supprimer-proprement-un-swap)
- [Monitoring et debug](#monitoring-et-debug)
- [Cas d’usage pratiques](#cas-dusage-pratiques)
- [En résumé](#en-resume)


Spoiler : on va éviter les manipulations de partition à la hache et privilégier des méthodes qui ne casseront pas ton système en prod.

![Illustration 1 — Swap Linux](cat-memory-nusoh30j7qijy.gif)

**Qu’est-ce que le swap et pourquoi tu en as (vraiment) besoin**

Le swap, c’est un peu comme ton canapé d’appoint quand ta belle-mère débarque à l’improviste : pas idéal, mais ça dépanne. Quand ta RAM est pleine, Linux balance intelligemment les données les moins utilisées vers cet espace de stockage temporaire.

**📋 À savoir :**  
*Contrairement aux idées reçues, avoir du swap même avec beaucoup de RAM reste une bonne pratique. Linux s’en sert pour optimiser la gestion mémoire et éviter les crashs d’applications.*

**Vérifier l’état actuel de ton swap**

Avant de jouer les apprentis sorciers, on regarde ce qu’on a sous le capot :

```bash
# État actuel du swap
sudo swapon --show

# Utilisation mémoire globale
free -h

# Détail des partitions
lsblk

```

# Créer un fichier de 2Go (ajuste selon tes besoins)
sudo fallocate -l 2G /swapfile

# Ou si fallocate n'est pas dispo :
sudo dd if=/dev/zero of=/swapfile bs=1024 count=2097152


### **Étape 2 : Sécuriser les permissions**

```bash
# Seul root peut lire/écrire le fichier
sudo chmod 600 /swapfile

# Vérifier les permissions
ls -lh /swapfile

```

# Transformer le fichier en swap
sudo mkswap /swapfile

# Activer le swap
sudo swapon /swapfile

# Vérifier que ça marche
sudo swapon --show


### **Étape 4 : Rendre permanent**

Pour que le swap survive aux redémarrages, on l’ajoute dans `/etc/fstab` :

```bash
# Backup du fstab (au cas où)
sudo cp /etc/fstab /etc/fstab.bak

# Ajouter la ligne swap
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

```

# Voir la valeur actuelle
cat /proc/sys/vm/swappiness

# Temporaire : réduire l'utilisation du swap
sudo sysctl vm.swappiness=10

# Permanent : éditer /etc/sysctl.conf
echo 'vm.swappiness=10' | sudo tee -a /etc/sysctl.conf


**💡 Bonnes pratiques :**

- **Serveur** : swappiness entre 1-10
- **Desktop** : swappiness entre 10-60
- **Jamais 0** : ça désactive complètement le swap, pas malin

**Gérer plusieurs fichiers swap (si tu as plusieurs disques)**

Tu peux avoir plusieurs fichiers swap et jouer avec les priorités :

```bash
# Créer un second fichier swap sur un autre disque
sudo fallocate -l 4G /mnt/fast-ssd/swapfile2
sudo chmod 600 /mnt/fast-ssd/swapfile2
sudo mkswap /mnt/fast-ssd/swapfile2

# Activer avec priorité élevée (plus le chiffre est haut, plus prioritaire)
sudo swapon --priority=5 /mnt/fast-ssd/swapfile2
sudo swapon --priority=1 /swapfile

# Dans /etc/fstab :
# /swapfile none swap sw,pri=1 0 0
# /mnt/fast-ssd/swapfile2 none swap sw,pri=5 0 0

```

# Désactiver le swap temporairement
sudo swapoff /swapfile

# Redimensionner (ici 4G)
sudo fallocate -l 4G /swapfile

# Recréer la signature swap
sudo mkswap /swapfile

# Réactiver
sudo swapon /swapfile


**⚠️ Attention :**  
*Ne jamais faire ça sur un système en production sous charge. Privilégie les heures creuses ou une maintenance programmée.*

**Supprimer proprement un swap**

Si tu veux nettoyer :

```bash
# Désactiver
sudo swapoff /swapfile

# Retirer de /etc/fstab (éditer manuellement)
sudo nano /etc/fstab

# Supprimer le fichier
sudo rm /swapfile

```

# Utilisation en temps réel
watch -n 1 'free -h && echo "---" && sudo swapon --show'

# Processus qui utilisent le plus de swap
for file in /proc/*/status ; do awk '/VmSwap|Name/{printf $2 " " $3}END{ print ""}' $file; done | sort -k 2 -n -r | head -10

# I/O du swap
iostat -x 1


**Cas d’usage pratiques**

**Serveur web avec 2GB RAM :** 2-4GB de swap  
**Base de données :** 1-2x la RAM si &lt; 8GB, sinon 8-16GB max  
**Conteneurs Docker :** au minimum 1GB, plus si tu fais du build d’images

Si tu utilises des conteneurs, pense à consulter mon guide sur [la sécurisation des serveurs Linux](https://brandonvisca.com/securite-de-votre-serveur-linux/) pour une approche globale de l’optimisation système.

**En résumé**

✅ **Privilégie les fichiers swap** aux partitions  
⚙️ **Ajuste la swappiness** selon ton usage  
🎯 **Surveille l’utilisation** avec `free` et `htop`  
🔒 **Sécurise les permissions** (chmod 600)  
💡 **Dimensionne intelligemment** selon ton workload

Le swap n’est pas l’ennemi, c’est ton assurance-vie système. Bien configuré, il te sauvera la mise quand ta webapp Java décidera de bouffer toute la RAM d’un coup.

![Capture d'écran — Étape 4 Rendre permanent](nbc-season-2-kenan-vnr3draqtz6mwyfxv0.gif)Pour aller plus loin dans l’optimisation système, mon article sur [la modification de l’heure serveur Linux](https://brandonvisca.com/comment-modifier-heure-du-serveur-sous-linux/) couvre d’autres aspects essentiels de l’administration.

## Articles connexes

- [UptimeRobot : Le Guide Complet pour Surveiller Votre Infrast](/uptimerobot-guide-complet-monitoring-infrastructure/)
- [SnipeIT vs GLPI : David contre Goliath dans l'arène de l'ITS](/snipeit-vs-glpi-comparatif-itsm-inventaire-it/)
