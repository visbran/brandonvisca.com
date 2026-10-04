---
title: Dépannage des problèmes de montage de matrices RAID (mdadm) en mode de secours Linux
description: "mount refuse ta matrice RAID mdadm en mode secours avec « wrong fs type » ? Elle contient sans doute une table de partitions : monte md126p1, pas md126."
pubDatetime: "2025-03-13T11:37:18+01:00"
author: Brandon Visca
tags:
  - linux
  - sysadmin
  - stockage
  - avance
featured: false
draft: false
focusKeyword: RAID
faqs:
  - question: "Pourquoi mount renvoie-t-il wrong fs type sur une matrice RAID saine ?"
    answer: "La matrice peut contenir une table de partitions au lieu d'un système de fichiers. mdadm la voit clean, mais il n'y a rien à monter directement sur /dev/md126 : il faut monter une de ses partitions."
  - question: "Comment savoir ce que contient la matrice RAID ?"
    answer: "file -s /dev/md126 indique s'il s'agit d'un système de fichiers ou d'une table de partitions, et fdisk -l /dev/md126 liste les partitions présentes."
  - question: "Comment monter la bonne partition en mode secours ?"
    answer: "Après fdisk -l, monte la partition qui porte le système de fichiers racine, par exemple mount /dev/md126p1 /mnt/recovery. Tu peux ensuite modifier tes fichiers sous /mnt/recovery."
---
> 💡 **TL;DR**
> - `mount` refuse la matrice avec "wrong fs type, bad option, bad superblock" alors que `mdadm --detail` la donne « clean »
> - `file -s /dev/md126` montre une table de partition : la matrice n'est pas formatée directement, elle contient des partitions
> - Monte la partition et pas la matrice : `fdisk -l /dev/md126` puis `mount /dev/md126p1 /mnt/recovery`

![507](no-nope-tracy-morgan-spfi6nabvuq5y.gif)

Aujourd’hui, je me suis retrouvé dans une situation stressante lorsque je n’ai pas pu accéder à ma matrice RAID en mode de secours. J’avais besoin de modifier un fichier critique situé dans `/etc/sudoers.d/`, mais je me heurtais constamment à des erreurs de montage :

```bash
mount: /mnt/recovery: wrong fs type, bad option, bad superblock on /dev/md126, missing codepage or helper program, or other error.
```

```bash
mdadm --detail /dev/md126
mdadm --detail /dev/md127
```

Les résultats ont montré que les deux matrices étaient en bon état, « State: clean » avec tous les périphériques « active sync ». Cela m’a indiqué que la configuration RAID elle-même n’était pas la source du problème.

## L’aperçu critique

Après avoir tenté plusieurs commandes de montage de base sans succès, j’ai décidé de vérifier ce qui se trouvait réellement sur le périphérique RAID à l’aide de la commande `file` :

```bash
file -s /dev/md126

/dev/md126: DOS/MBR boot sector; partition 1 : ID=0xee, start-CHS (0x0,0,2), end-CHS (0x3ff,255,63), startsector 1, 4294967295 sectors, extended partition table (last)
```

La matrice RAID n’était pas formatée directement comme un système de fichiers. Au lieu de cela, elle contenait une table de partition, ce qui signifiait que je devais monter l’une des partitions à l’intérieur de la matrice RAID, et non la matrice elle-même.

💡 À lire aussi : [Cockpit Docker : interface web d'administration Linux moderne](/cockpit-docker-interface-web-administration/), dans la même veine que cet article.

## La solution

La solution consistait à lister les partitions sur la matrice RAID :

```bash
fdisk -l /dev/md126

mount /dev/md126p1 /mnt/recovery
```

Après avoir trouvé la partition contenant mon système de fichiers racine, j’ai finalement pu accéder et modifier le fichier cible :

```bash
nano /mnt/recovery/etc/sudoers.d/gardeners

```

