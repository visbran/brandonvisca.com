---
title: "Snapper Btrfs : snapshots et rollback Linux sans réinstaller"
description: "Snapper Btrfs : crée des snapshots automatiques, compare les changements et reviens en arrière en une commande, sans réinstaller ton système Linux."
pubDatetime: "2026-11-25T11:02:24+01:00"
modDatetime: "2026-11-23T08:00:00.000Z"
author: Brandon
tags:
  - linux
  - sysadmin
  - stockage
  - sauvegarde
  - avance
featured: false
draft: false
focusKeyword: snapper btrfs
faqs:
  - question: "Snapper Btrfs fonctionne-t-il sur un système qui n'est pas en Btrfs ?"
    answer: "Non. Snapper peut créer des snapshots LVM, mais tout ce qui est rollback bootable et snapshots instantanés sans espace dupliqué repose sur Btrfs. Sur ext4 ou XFS, tu perds l'essentiel de l'intérêt de l'outil."
  - question: "Un rollback avec Snapper Btrfs touche-t-il aussi /home ?"
    answer: "Seulement si /home est sur le même sous-volume que la racine, ce qui est déconseillé. En pratique /home vit dans son propre sous-volume non concerné par le rollback, tu ne perds donc pas tes documents."
  - question: "Combien d'espace disque prennent les snapshots Snapper Btrfs ?"
    answer: "Très peu au départ grâce au copy-on-write : seuls les blocs modifiés sont dupliqués. Ça grossit avec le temps si tu gardes des dizaines de snapshots anciens, d'où l'intérêt du nettoyage automatique."
---
> 💡 **TL;DR**
> - Btrfs fait des snapshots quasi instantanés et quasi gratuits en espace disque, Snapper les automatise et les range proprement
> - `snapper rollback` restaure tout le système à l'état d'un snapshot sans réinstaller quoi que ce soit, même si la machine ne démarre plus, grâce à `grub-btrfs`
> - Installation en une commande (`apt`, `dnf` ou `pacman`), configuration en dix minutes, et tu as un vrai filet de sécurité avant chaque mise à jour risquée

## Snapper Btrfs : la machine à remonter le temps de ton serveur Linux

Tu connais la scène. Tu lances une mise à jour de paquets un vendredi soir, un pilote ou une dépendance casse ton système, et tu te retrouves à minuit en train de chercher une clé USB de secours. Chez moi, ça m'est arrivé une fois de trop. Depuis, chaque machine Linux qui compte tourne sur Btrfs avec Snapper configuré dessus, et ce genre de soirée n'existe plus.

Snapper Btrfs, c'est la combinaison entre un système de fichiers qui sait faire des copies instantanées de lui-même (Btrfs) et un outil qui pilote ces copies, les range, les compare et les restaure (Snapper). Le résultat : tu annules une mise à jour foireuse, un fichier de config cassé ou une purge malheureuse en une commande, sans toucher à un CD de réinstallation. Spoiler : ça va marcher, et nettement plus vite qu'une restauration de sauvegarde classique.

## Table des matières

## Btrfs et les snapshots : le principe en deux minutes

Btrfs est un système de fichiers copy-on-write. En clair : quand tu modifies un fichier, Btrfs n'écrase pas le bloc original, il écrit le nouveau bloc ailleurs et met à jour les pointeurs. Un snapshot, c'est juste un gel de ces pointeurs à un instant donné. Il ne coûte quasiment rien à la création, parce qu'il ne copie aucune donnée : il partage les blocs existants avec le système « live », et seuls les blocs qui changent ensuite sont dupliqués.

Concrètement, ça veut dire que tu peux avoir des dizaines de snapshots sur ta racine sans voir ton disque se remplir d'un coup. C'est radicalement différent d'une sauvegarde classique façon `rsync` ou `tar`, qui duplique tout à chaque fois. Un snapshot Btrfs se crée en une fraction de seconde, même sur un disque qui contient des centaines de giga de données.

Snapper, lui, ne fait pas les snapshots à la place de Btrfs. Il orchestre : il décide quand créer un snapshot, comment le nommer, combien de temps le garder, et il te donne les commandes pour comparer et restaurer. Sans Snapper, tu peux toujours faire du Btrfs brut avec `btrfs subvolume snapshot`, mais tu te retrouves vite avec une pile de snapshots sans nom et sans politique de nettoyage. Snapper Btrfs, c'est la couche qui rend l'outil réellement utilisable au quotidien.

⚠️ Un point qui piège pas mal de monde : un snapshot Btrfs n'est pas une sauvegarde. Il vit sur le même disque physique que les données qu'il protège. Si le disque meurt, tes snapshots meurent avec. Pour une vraie sauvegarde hors machine, regarde plutôt du côté de [Vanderplanki pour tes emails](/vanderplanki-sauvegarde-emails-gratuit-multiplateforme/) ou d'un outil dédié qui envoie ailleurs. Snapper Btrfs, c'est ton filet de sécurité local, pas ton plan de reprise après sinistre.

## Installer Snapper selon ta distribution

Snapper est un projet open source maintenu par la communauté openSUSE, publié sous licence GPL-2.0, et il est entièrement gratuit. Sur openSUSE Tumbleweed et Leap, il est déjà présent par défaut dès que la racine est en Btrfs : YaST s'en occupe pendant l'installation. Sur les autres distributions, c'est natif au système de fichiers (Btrfs est dans le noyau), mais Snapper lui-même reste un paquet tiers à installer à la main.

**Ubuntu et Debian :**

```bash
sudo apt update
sudo apt install snapper
```

**Fedora et RHEL-like :**

```bash
sudo dnf install snapper
```

Sur Fedora, tu peux aussi installer `python3-dnf-plugin-snapper` pour que `dnf` crée automatiquement un snapshot avant et après chaque transaction de paquets, sur le même principe que `zypper` sous openSUSE.

**Arch Linux :**

```bash
sudo pacman -S snapper
```

Sur Arch, ajoute en plus `snap-pac` si tu veux que Snapper Btrfs s'accroche aux transactions `pacman` :

```bash
sudo pacman -S snap-pac
```

Dans tous les cas, vérifie d'abord que ta racine tourne bien sur Btrfs avec `findmnt -t btrfs /`. Si la commande ne renvoie rien, Snapper n'a rien à piloter : il te faudrait reformater, ce qui sort largement du cadre d'un simple article de blog.

## Créer une configuration et ton premier snapshot

Snapper fonctionne par « configurations » : chacune associe un nom à un sous-volume Btrfs précis, avec sa propre politique de rétention. La config `root`, pour la racine du système, est la plus courante.

```bash
sudo snapper -c root create-config /
sudo snapper list-configs
```

Une fois la config créée, tu peux lister les snapshots existants, qui seront vides au début :

```bash
sudo snapper -c root list
```

Et créer ton premier snapshot manuel, avec une description qui te servira plus tard :

```bash
sudo snapper -c root create -d "avant mise a jour du noyau"
```

Si `root` est ta config par défaut, tu peux d'ailleurs omettre `-c root` dans la plupart des commandes. Je le laisse explicite ici parce que c'est plus lisible une fois que tu gères plusieurs configs, par exemple une pour `/` et une pour `/var/lib/docker` si ce dernier vit sur son propre sous-volume.

✅ Prends l'habitude de lancer un snapshot manuel avant toute modification risquée : mise à jour majeure, changement de configuration réseau avec [Netplan en YAML](/netplan-linux-configurer-reseau-yaml/), ou ajustement de [la swap et de sa configuration](/guide-swap-linux-configuration-optimisation/). Ça prend deux secondes et ça t'évite une soirée pourrie.

## Comparer deux snapshots et annuler un changement précis

La vraie question, c'est souvent : qu'est-ce qui a changé entre deux moments donnés ? Snapper Btrfs répond à ça sans avoir besoin de tout restaurer. `snapper list` te donne les numéros des snapshots :

```bash
sudo snapper list
```

Pour voir les fichiers modifiés entre les snapshots 3 et 5 :

```bash
sudo snapper status 3..5
```

Tu obtiens une liste avec des codes courts (`c.....` pour un contenu modifié, par exemple). Pour creuser un fichier précis :

```bash
sudo snapper diff 3..5 /etc/fstab
```

Et si tu veux annuler seulement ce changement, sans toucher au reste du système :

```bash
sudo snapper undochange 3..5 /etc/fstab
```

Sans le chemin du fichier à la fin, `undochange` annule tous les changements détectés entre les deux snapshots, pas seulement un fichier. C'est puissant, mais ça mérite un `status` avant pour savoir précisément ce que tu es sur le point d'annuler. Et contrairement à un rollback complet, `undochange` ne prévient pas le noyau des fichiers déjà ouverts : un service qui a chargé l'ancienne version en mémoire peut avoir besoin d'un redémarrage pour voir le changement.

## Rollback complet avec Snapper Btrfs : revenir en arrière sans réinstaller

Là où Snapper Btrfs change vraiment la donne, c'est le rollback intégral. Plutôt que de restaurer fichier par fichier, tu bascules le sous-volume racine entier sur l'état d'un snapshot donné.

```bash
sudo snapper rollback
```

Sans argument, cette commande utilise le snapshot le plus récent comme référence et crée un nouveau sous-volume par défaut à partir de lui. Un snapshot supplémentaire est créé au passage, qui capture l'état juste avant le rollback : si tu te plantes dans le choix, tu peux toujours revenir en arrière du rollback lui-même.

Pour cibler un snapshot précis plutôt que le dernier :

```bash
sudo snapper rollback 7
```

Le rollback ne modifie rien « à chaud » : il change la racine par défaut que le bootloader doit monter au prochain démarrage. Il faut donc redémarrer pour que le changement prenne effet :

```bash
sudo reboot
```

Au redémarrage, ton système repart exactement comme au moment du snapshot 7 : paquets, fichiers de config, tout. Si l'incident qui t'a forcé à faire ce rollback s'est produit pendant que tu administrais la machine à distance, c'est le même genre de rigueur que pour un [dépannage de montage RAID en mode secours](/depannage-montage-partition-raid-linux-mode-secours/) : tu veux une méthode fiable, pas une improvisation à 2h du matin.

💡 Un détail qui a son importance avec Snapper Btrfs : `/home` et les données applicatives lourdes (bases de données, conteneurs) devraient vivre dans des sous-volumes séparés de la racine. Comme ça, un rollback de `/` ne touche ni tes documents personnels ni les données de production, seulement le système lui-même.

## Démarrer sur un snapshot cassé : grub-btrfs et le nettoyage automatique

Sur openSUSE, le GRUB2 fourni sait directement démarrer sur un ancien snapshot Btrfs depuis le menu de démarrage, ce qui est précieux quand le système ne boote plus du tout après une mise à jour du noyau. Sur Ubuntu, Debian ou Arch, cette intégration n'existe pas nativement : c'est le rôle du projet tiers [grub-btrfs](https://github.com/Antynea/grub-btrfs), qui ajoute automatiquement une entrée de menu GRUB par snapshot disponible.

Sur Arch, le paquet est dans le dépôt communautaire :

```bash
sudo pacman -S grub-btrfs
```

Sur Ubuntu et Debian, il se compile depuis les sources :

```bash
sudo apt install git make inotify-tools
git clone https://github.com/Antynea/grub-btrfs.git
cd grub-btrfs
sudo make install
```

Un daemon optionnel, `grub-btrfsd`, surveille le dossier des snapshots et régénère le menu GRUB à chaque création ou suppression, sans que tu aies à relancer `update-grub` toi-même. Active-le avec `systemctl enable --now` si ton installeur ne l'a pas fait pour toi, puis vérifie son état avant de faire confiance au menu de démarrage.

Côté nettoyage, Snapper Btrfs sait aussi faire le ménage seul. Chaque config a des réglages `NUMBER_LIMIT`, `TIMELINE_LIMIT_HOURLY`, `TIMELINE_LIMIT_DAILY` qui bornent le nombre de snapshots conservés :

```bash
sudo snapper -c root set-config "TIMELINE_CREATE=yes" "TIMELINE_LIMIT_HOURLY=5" "TIMELINE_LIMIT_DAILY=7" "NUMBER_LIMIT=10"
```

⚠️ Sans politique de nettoyage, les snapshots s'accumulent et finissent par retenir des blocs qu'un `btrfs balance` ou un simple `df` auraient envie de libérer. Sur une machine avec peu d'espace disque, surveille l'usage réel avec `btrfs filesystem usage /` plutôt que de te fier à `df` seul, qui sous-estime souvent la réalité du copy-on-write.

Deux autres limites à garder en tête. D'abord, Snapper Btrfs ne protège pas contre une panne disque : c'est un outil de retour arrière rapide, pas une sauvegarde externe. Ensuite, un rollback complet redémarre forcément la machine, ce qui veut dire une coupure de service si c'est un serveur en production : planifie-le comme une maintenance, pas comme une action à chaud sur un système qui tourne. Si tu administres déjà ta flotte de conteneurs via [Cockpit, l'interface web d'administration Linux](/cockpit-docker-interface-web-administration/), pense à documenter la procédure de rollback au même endroit que tes autres runbooks d'astreinte.

## Conclusion

Snapper Btrfs ne remplace pas une vraie stratégie de sauvegarde, mais il couvre un besoin que peu d'outils adressent aussi bien : revenir en arrière vite, sans réinstaller, sans restaurer un gros fichier tar depuis un disque externe. Dix minutes d'installation, une politique de nettoyage réglée une fois, et tu as un vrai filet de sécurité qui se déclenche avant chaque mise à jour un peu risquée.

Mon setup perso : un snapshot timeline toutes les heures, un snapshot manuel avant chaque opération qui touche au noyau ou à la configuration réseau, et `grub-btrfs` pour pouvoir démarrer sur n'importe lequel si le pire arrive. Bon, on va pas se mentir, ça n'empêche pas toutes les galères. Mais la prochaine fois qu'une mise à jour casse ton système un vendredi soir, tu fermes l'ordinateur, tu dors, et tu fais `snapper rollback` le lendemain matin avec un café plutôt qu'une clé USB.
