---
title: Dépannage des problèmes de montage de matrices RAID (mdadm) en mode de secours Linux
pubDatetime: "2025-03-13T11:37:18+01:00"
author: Brandon Visca
description: "Dépannez un montage RAID mdadm en mode secours Linux : diagnostic de l'erreur wrong fs type, découverte d'une partition cachée et solution complète."wrong fs type\" en découvrant que l'array RAID contenait une ta..."
tags:
  - linux
  - sysadmin
  - avance
  - raid
  - guide
  - depannage
---


- [Enquête initiale](#enquete-initiale)
- [L’aperçu critique](#lapercu-critique)
- [La solution](#la-solution)
- [Leçons apprises](#lecons-apprises)


![Illustration — Dépannage des problèmes de montage de matrices RAID (mdadm) ](no-nope-tracy-morgan-spfi6nabvuq5y.gif)

Aujourd’hui, je me suis retrouvé dans une situation stressante lorsque je n’ai pas pu accéder à ma matrice RAID en mode de secours. J’avais besoin de modifier un fichier critique situé dans `/etc/sudoers.d/`, mais je me heurtais constamment à des erreurs de montage :

```bash
mount: /mnt/recovery: wrong fs type, bad option, bad superblock on /dev/md126, missing codepage or helper program, or other error.

```

mdadm --detail /dev/md126
mdadm --detail /dev/md127


Les résultats ont montré que les deux matrices étaient en bon état – « State: clean » avec tous les périphériques « active sync ». Cela m’a indiqué que la configuration RAID elle-même n’était pas la source du problème.

L’aperçu critique

Après avoir tenté plusieurs commandes de montage de base sans succès, j’ai décidé de vérifier ce qui se trouvait réellement sur le périphérique RAID à l’aide de la commande `file` :

```bash
file -s /dev/md126

```

/dev/md126: DOS/MBR boot sector; partition 1 : ID=0xee, start-CHS (0x0,0,2), end-CHS (0x3ff,255,63), startsector 1, 4294967295 sectors, extended partition table (last)


La matrice RAID n’était pas formatée directement comme un système de fichiers. Au lieu de cela, elle contenait une table de partition, ce qui signifiait que je devais monter l’une des partitions à l’intérieur de la matrice RAID, et non la matrice elle-même.

La solution

La solution consistait à lister les partitions sur la matrice RAID :

```bash
fdisk -l /dev/md126

```

mount /dev/md126p1 /mnt/recovery


Après avoir trouvé la partition contenant mon système de fichiers racine, j’ai finalement pu accéder et modifier le fichier cible :

```bash
nano /mnt/recovery/etc/sudoers.d/gardeners

```
