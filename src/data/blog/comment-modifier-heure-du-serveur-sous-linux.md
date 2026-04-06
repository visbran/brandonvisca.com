---
title: "Comment définir le fuseau horaire et synchroniser l'heure du serveur sous Linux"
pubDatetime: "2024-06-13T11:21:00+02:00"
description: "Apprenez à changer le fuseau horaire, définir le fuseau horaire et synchroniser l'heure du serveur sous Linux en utilisant timedatectl et NTP."
tags:
  - linux
  - sysadmin
  - debutant
  - ntp
  - guide
  - configuration
---

-----------
## Table des matières


- [Comment définir ou changer le fuseau horaire sous Linux](#comment-definir-ou-changer-le-fuseau-horaire-sous-linux)
  - [Vérifier le fuseau horaire actuel](#verifier-le-fuseau-horaire-actuel)
  - [Lister les fuseaux horaires disponibles](#lister-les-fuseaux-horaires-disponibles)
  - [Définir le fuseau horaire](#definir-le-fuseau-horaire)
- [Configurer le fuseau horaire sous Ubuntu](#configurer-le-fuseau-horaire-sous-ubuntu)
  - [Méthode 1 : Utiliser le terminal](#methode-1-utiliser-le-terminal)
  - [Méthode 2 : Utiliser timedatectl](#methode-2-utiliser-timedatectl)
  - [Méthode 3 : Utiliser l’interface graphique](#methode-3-utiliser-linterface-graphique)
- [Foire aux questions](#foire-aux-questions)
  - [Comment vérifier mon fuseau horaire actuel sous Linux ?](#faq-question-1754323292300)
  - [Comment lister tous les fuseaux horaires disponibles ?](#faq-question-1754323302983)
  - [Comment changer le fuseau horaire sous Ubuntu en utilisant le terminal ?](#faq-question-1754323326659)
- [Conclusion](#conclusion)



Comment synchroniser l’heure avec NTP
-------------------------------------

La synchronisation de l’heure de votre serveur avec le NTP garantit que l’horloge de votre système est toujours précise. La plupart des distributions Linux sont équipées de `systemd-timesyncd`, un client NTP léger.

Pour vérifier l’état actuel de la synchronisation de l’heure, utilisez la commande `timedatectl` :

```bash
timedatectl status

```

timedatectl set-ntp true


Pour vérifier plus en détail l’état de `systemd-timesyncd`, vous pouvez exécuter :

```bash
systemctl status systemd-timesyncd

```

systemctl start systemd-timesyncd
systemctl enable systemd-timesyncd


Pour des étapes plus détaillées, consultez [Comment définir ou changer le fuseau horaire sous Linux](https://linuxize.com/post/how-to-set-or-change-timezone-in-linux/).

Comment définir ou changer le fuseau horaire sous Linux
-------------------------------------------------------

### Vérifier le fuseau horaire actuel

Avant de changer votre fuseau horaire, vérifiez le fuseau horaire actuellement défini avec :

```bash
timedatectl

```

timedatectl list-timezones


Vous pouvez également explorer le contenu du répertoire `/usr/share/zoneinfo/` pour trouver votre fuseau horaire préféré.

### Définir le fuseau horaire

Pour définir le fuseau horaire de votre système à un emplacement spécifique, par exemple New York, utilisez la commande suivante :

```bash
timedatectl set-timezone Europe/Paris

```

ln -s /usr/share/zoneinfo/Europe/Paris /etc/localtime


Pour des instructions plus détaillées, visitez [Comment changer le fuseau horaire sous Linux](https://www.baeldung.com/linux/change-timezone).

Configurer le fuseau horaire sous Ubuntu
----------------------------------------

### Méthode 1 : Utiliser le terminal

Ouvrez le terminal et exécutez la commande suivante pour ouvrir une liste de fuseaux horaires :

```bash
tzselect

```

