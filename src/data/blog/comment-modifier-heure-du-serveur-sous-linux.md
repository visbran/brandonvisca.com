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
faqs:
  - question: "Comment vérifier mon fuseau horaire actuel sous Linux ?"
    answer: "Utilise timedatectl pour voir le fuseau horaire et l'état de la synchronisation NTP."
  - question: "Comment lister tous les fuseaux horaires disponibles ?"
    answer: "Tape timedatectl list-timezones ou explore le répertoire /usr/share/zoneinfo/"
  - question: "Comment changer le fuseau horaire sous Ubuntu en utilisant le terminal ?"
    answer: "Utilise timedatectl set-timezone Europe/Paris (remplace par ton fuseau horaire)."
---

# Comment définir le fuseau horaire et synchroniser l'heure du serveur sous Linux

Garder la date et l'heure de votre système précises est crucial pour diverses opérations, allant de la journalisation aux tâches d'automatisation. Cet article couvre comment définir ou changer le fuseau horaire sous Linux, synchroniser l'heure de votre serveur avec le NTP (Network Time Protocol), et d'autres tâches connexes.

![](https://media4.giphy.com/media/26Do6la9cIiHvIwMM/giphy.gif?cid=7941fdc6pnk6cs7qnembjdx4x1mxp0ll1p00n5uszui5sssz&ep=v1_gifs_search&rid=giphy.gif&ct=g)

## Table of content

## Comment synchroniser l'heure avec NTP

La synchronisation de l'heure de votre serveur avec le NTP garantit que l'horloge de votre système est toujours précise. La plupart des distributions Linux sont équipées de `systemd-timesyncd`, un client NTP léger.

Pour vérifier l'état actuel de la synchronisation de l'heure, utilisez la commande `timedatectl` :

```bash
timedatectl status

```

Si le service NTP est inactif, activez-le avec :

```bash
timedatectl set-ntp true

```

Pour vérifier plus en détail l'état de `systemd-timesyncd`, vous pouvez exécuter :

```bash
systemctl status systemd-timesyncd

```

S'il est désactivé, activez-le avec :

```bash
systemctl start systemd-timesyncd
systemctl enable systemd-timesyncd

```

Pour des étapes plus détaillées, consultez [Comment définir ou changer le fuseau horaire sous Linux](https://linuxize.com/post/how-to-set-or-change-timezone-in-linux/).

## Comment définir ou changer le fuseau horaire sous Linux

### Vérifier le fuseau horaire actuel

Avant de changer votre fuseau horaire, vérifiez le fuseau horaire actuellement défini avec :

```bash
timedatectl

```

### Lister les fuseaux horaires disponibles

Pour lister tous les fuseaux horaires disponibles, utilisez :

```bash
timedatectl list-timezones

```

Vous pouvez également explorer le contenu du répertoire `/usr/share/zoneinfo/` pour trouver votre fuseau horaire préféré.

### Définir le fuseau horaire

Pour définir le fuseau horaire de votre système à un emplacement spécifique, par exemple New York, utilisez la commande suivante :

```bash
timedatectl set-timezone Europe/Paris

```

Cette commande crée un lien symbolique de `/usr/share/zoneinfo/` vers `/etc/localtime`. Alternativement, vous pouvez créer ce lien manuellement :

```bash
ln -s /usr/share/zoneinfo/Europe/Paris /etc/localtime

```

Pour des instructions plus détaillées, visitez [Comment changer le fuseau horaire sous Linux](https://www.baeldung.com/linux/change-timezone).

## Configurer le fuseau horaire sous Ubuntu

### Méthode 1 : Utiliser le terminal

Ouvrez le terminal et exécutez la commande suivante pour ouvrir une liste de fuseaux horaires :

```bash
tzselect

```

Suivez les invites pour sélectionner votre pays et fuseau horaire.

### Méthode 2 : Utiliser timedatectl

Une autre méthode consiste à utiliser la commande `timedatectl`, comme expliqué ci-dessus.

### Méthode 3 : Utiliser l'interface graphique

Si vous préférez utiliser une interface graphique, allez dans Paramètres > Date & Heure et sélectionnez votre fuseau horaire sur la carte.

Pour plus de détails, consultez [Comment changer le fuseau horaire sous Ubuntu (3 méthodes faciles)](https://www.hostinger.com/tutorials/how-to-change-timezone-in-ubuntu/).

## Foire aux questions

### Comment vérifier mon fuseau horaire actuel sous Linux ?

Vous pouvez vérifier votre fuseau horaire actuel en exécutant la commande `timedatectl` dans le terminal.

### Comment lister tous les fuseaux horaires disponibles ?

Pour lister tous les fuseaux horaires disponibles, utilisez la commande `timedatectl list-timezones`.

### Comment changer le fuseau horaire sous Ubuntu en utilisant le terminal ?

Pour changer le fuseau horaire sous Ubuntu, vous pouvez utiliser la commande `timedatectl set-timezone` suivie de votre fuseau horaire souhaité.

## Conclusion

Gérer les paramètres d'heure et de fuseau horaire de votre système est essentiel pour maintenir des journaux précis et le bon fonctionnement du système. En utilisant des outils comme `timedatectl` et NTP, vous pouvez vous assurer que l'horloge de votre système Linux est toujours précise. Pour des guides plus complets, consultez des sources comme le [guide de Rackspace sur la configuration de la date, de l'heure et du fuseau horaire sur un serveur Linux](https://docs.rackspace.com/docs/set-the-date-and-time-timezone-on-a-linux-server) ou le [guide de wikiHow sur le changement de fuseau horaire sous Linux](https://www.wikihow.com/Change-the-Timezone-in-Linux).


**Meta Description:** Apprenez à changer le fuseau horaire, définir le fuseau horaire et synchroniser l'heure du serveur sous Linux en utilisant `timedatectl` et NTP. Suivez notre guide détaillé pour garder vos systèmes Linux précis.
