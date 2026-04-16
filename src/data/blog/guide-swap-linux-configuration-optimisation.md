---
title: "Swap Linux : guide complet pour configurer et optimiser en 2026"
description: "Guide complet swap Linux 2026 : configurer un fichier swap, ajuster la swappiness, redimensionner et surveiller l'utilisation mémoire."
pubDatetime: "2025-07-13T22:16:30+02:00"
modDatetime: "2026-04-16T00:00:00+01:00"
author: Brandon Visca
tags:
  - linux
  - swap
  - memoire
  - performance
  - swappiness
  - intermediaire
featured: false
draft: false
focusKeyword: Swap Linux
faqs:
  - question: "Quelle taille de swap choisir sous Linux ?"
    answer: "Pour un serveur avec moins de 4 Go de RAM, prévois 2x la RAM. Au-delà, 1x suffit avec un maximum de 8-16 Go. Sur un desktop avec 16 Go+, 2-4 Go suffisent comme filet de sécurité."
  - question: "Fichier swap ou partition swap : quelle différence ?"
    answer: "Le fichier swap se crée et se redimensionne à chaud sans toucher au partitionnement. La partition swap offre de légères performances supplémentaires sur HDD, mais l'écart est négligeable sur SSD. Le fichier swap est la méthode recommandée aujourd'hui."
  - question: "Comment vérifier que le swap est actif sous Linux ?"
    answer: "Lance sudo swapon --show : si la commande retourne une ligne avec ton fichier swap et sa taille, c'est actif. La commande free -h affiche aussi l'utilisation en temps réel dans la colonne Swap."
---
> 💡 **TL;DR** : Le swap sous Linux se configure mieux avec un fichier qu'une partition. Abaisse la swappiness à 10 sur un serveur, surveille avec `free -h` et `swapon --show`. Même avec 8 Go de RAM, 1 à 2 Go de swap restent une bonne pratique.

## Table des matières

Configurer le swap Linux correctement, ça fait la différence entre un serveur qui tient la charge et un qui freeze au mauvais moment. Spoiler : on va éviter les manipulations de partition à la hache et privilégier des méthodes qui ne casseront pas ton système en prod.

![](cat-memory-nusoh30j7qijy.gif)

## Swap Linux : pourquoi tu en as (vraiment) besoin

Le swap, c'est un peu comme ton canapé d'appoint quand ta belle-mère débarque à l'improviste : pas idéal, mais ça dépanne. Quand ta RAM est pleine, Linux balance intelligemment les données les moins utilisées vers cet espace de stockage temporaire.

> 📋 **À savoir :** Contrairement aux idées reçues, avoir du swap même avec beaucoup de RAM reste une bonne pratique. Linux s'en sert pour optimiser la gestion mémoire et éviter les crashs d'applications.

## Vérifier l'état actuel de ton swap

Avant de jouer les apprentis sorciers, on regarde ce qu'on a sous le capot :

```bash
# État actuel du swap
sudo swapon --show

# Utilisation mémoire globale
free -h

# Détail des partitions
lsblk
```

## Méthode recommandée : créer un fichier swap (pas une partition)

### Étape 1 : Créer le fichier swap

```bash
# Créer un fichier de 2 Go (ajuste selon tes besoins)
sudo fallocate -l 2G /swapfile

# Ou si fallocate n'est pas dispo :
sudo dd if=/dev/zero of=/swapfile bs=1024 count=2097152
```

### Étape 2 : Sécuriser les permissions

```bash
# Seul root peut lire/écrire le fichier
sudo chmod 600 /swapfile

# Vérifier les permissions
ls -lh /swapfile
```

### Étape 3 : Formater et activer

```bash
# Transformer le fichier en swap
sudo mkswap /swapfile

# Activer le swap
sudo swapon /swapfile

# Vérifier que ça marche
sudo swapon --show
```

### Étape 4 : Rendre permanent

Pour que le swap survive aux redémarrages, on l'ajoute dans `/etc/fstab` :

```bash
# Backup du fstab (au cas où)
sudo cp /etc/fstab /etc/fstab.bak

# Ajouter la ligne swap
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

## Optimiser les performances avec swappiness

```bash
# Voir la valeur actuelle
cat /proc/sys/vm/swappiness

# Temporaire : réduire l'utilisation du swap
sudo sysctl vm.swappiness=10

# Permanent : éditer /etc/sysctl.conf
echo 'vm.swappiness=10' | sudo tee -a /etc/sysctl.conf
```

Sur mes serveurs persos (Proxmox, VPS Oracle), j'utilise systématiquement une swappiness de 10 : ça laisse Linux gérer la mémoire sans basculer trop vite sur le disque.

**Bonnes pratiques :**

- **Serveur** : swappiness entre 1-10
- **Desktop** : swappiness entre 10-60
- **Jamais 0** : ça désactive complètement le swap, pas malin

La doc kernel officielle détaille le comportement exact de ce paramètre : [vm.swappiness (kernel.org)](https://www.kernel.org/doc/html/latest/admin-guide/sysctl/vm.html#swappiness)

## Gérer plusieurs fichiers swap (si tu as plusieurs disques)

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

## Redimensionner un fichier swap existant

```bash
# Désactiver le swap temporairement
sudo swapoff /swapfile

# Redimensionner (ici 4G)
sudo fallocate -l 4G /swapfile

# Recréer la signature swap
sudo mkswap /swapfile

# Réactiver
sudo swapon /swapfile
```

> ⚠️ **Attention :** Ne jamais faire ça sur un système en production sous charge. Privilégie les heures creuses ou une maintenance programmée.

Si tu galères avec des problèmes de partition ou de montage après ce genre d'opération, consulte mon guide sur le [dépannage montage partition et RAID en mode secours](https://brandonvisca.com/depannage-montage-partition-raid-linux-mode-secours/).

## Supprimer proprement un swap

Si tu veux nettoyer :

```bash
# Désactiver
sudo swapoff /swapfile

# Retirer de /etc/fstab (éditer manuellement)
sudo nano /etc/fstab

# Supprimer le fichier
sudo rm /swapfile
```

## Monitoring swap Linux

```bash
# Utilisation en temps réel
watch -n 1 'free -h && echo "---" && sudo swapon --show'

# Processus qui utilisent le plus de swap
for file in /proc/*/status ; do awk '/VmSwap|Name/{printf $2 " " $3}END{ print ""}' $file; done | sort -k 2 -n -r | head -10

# I/O du swap
iostat -x 1
```

## Cas d'usage pratiques

**Serveur web avec 2 GB RAM :** 2-4 GB de swap  
**Base de données :** 1-2x la RAM si < 8 GB, sinon 8-16 GB max  
**Conteneurs Docker :** au minimum 1 GB, plus si tu fais du build d'images

Si tu utilises des conteneurs, commence par mon [guide Docker pour débutants](https://brandonvisca.com/docker-debutant-services-auto-heberger/) pour le setup de base, puis passe à [la sécurisation des serveurs Linux](https://brandonvisca.com/securite-de-votre-serveur-linux/) pour durcir l'ensemble.

## Conclusion

Le swap n'est pas l'ennemi, c'est ton assurance-vie système. Bien configuré, il te sauvera la mise quand ta webapp Java décidera de bouffer toute la RAM d'un coup.

Retiens les essentiels : fichier swap plutôt que partition, swappiness à 10 sur serveur, permissions 600, et une entrée dans `/etc/fstab` pour la persistance. Pour le reste, `free -h` et `swapon --show` sont tes meilleurs amis au quotidien.

![](nbc-season-2-kenan-vnr3draqtz6mwyfxv0.gif)

## FAQ — Swap Linux

**Quelle taille de swap choisir sous Linux ?**  
Pour un serveur avec moins de 4 Go de RAM, prévois 2x la RAM. Au-delà, 1x suffit avec un maximum de 8-16 Go. Sur un desktop avec 16 Go+, 2-4 Go de swap suffisent comme filet de sécurité.

**Fichier swap ou partition swap : quelle différence ?**  
Le fichier swap se crée et se redimensionne à chaud, sans toucher au partitionnement. La partition swap offre des performances légèrement meilleures sur HDD rotatif, mais l'écart est négligeable sur SSD. Aujourd'hui, le fichier swap est la méthode recommandée dans tous les cas.

**Comment vérifier que le swap est actif sous Linux ?**  
Lance `sudo swapon --show` : si la commande retourne une ligne avec ton fichier swap et sa taille, c'est actif. `free -h` affiche aussi l'utilisation en temps réel dans la colonne "Swap".

## Pour aller plus loin

- [Sécuriser son serveur Linux : les bases](https://brandonvisca.com/securite-de-votre-serveur-linux/)
- [Modifier l'heure de son serveur Linux](https://brandonvisca.com/comment-modifier-heure-du-serveur-sous-linux/)
- [Doc officielle vm.swappiness (kernel.org)](https://www.kernel.org/doc/html/latest/admin-guide/sysctl/vm.html#swappiness)
