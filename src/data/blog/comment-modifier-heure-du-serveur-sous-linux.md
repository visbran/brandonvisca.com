---
title: "Comment définir le fuseau horaire et synchroniser l'heure du serveur sous Linux"
description: "Apprenez à changer le fuseau horaire, définir le fuseau horaire et synchroniser l'heure du serveur sous Linux en utilisant timedatectl et NTP."
pubDatetime: "2024-06-13T11:21:00+02:00"
modDatetime: "2026-04-25T00:00:00+01:00"
author: Brandon Visca
tags:
  - linux
  - ubuntu
  - ntp
  - fuseau-horaire
  - timedatectl
  - debutant
featured: false
draft: false
focusKeyword: heure du serveur sous linux
faqs:
  - question: "Comment vérifier mon fuseau horaire actuel sous Linux ?"
    answer: "Lance timedatectl dans le terminal. La ligne Time zone affiche le fuseau actuel, et NTP service indique si la synchronisation est active."
  - question: "Comment lister tous les fuseaux horaires disponibles ?"
    answer: "Tape timedatectl list-timezones. Pour filtrer sur la France : timedatectl list-timezones | grep Europe."
  - question: "Comment changer le fuseau horaire sous Ubuntu en utilisant le terminal ?"
    answer: "Lance timedatectl set-timezone Europe/Paris (remplace Europe/Paris par ton fuseau horaire). Pas besoin de redémarrer le système."
---
> 💡 **TL;DR**
> - `timedatectl` est ton outil principal pour gérer fuseau horaire et synchro NTP sous Linux
> - Active la synchro avec `timedatectl set-ntp true`, change le fuseau avec `timedatectl set-timezone Europe/Paris`
> - `systemd-timesyncd` suffit pour la plupart des usages ; passe à chrony si tu as besoin d'une précision sub-milliseconde

Garder la date et l'heure de ton système précises, c'est la base de plein d'opérations : journalisation, cron jobs, certificats TLS, logs corrélés entre machines... Surtout si tu [auto-héberges des services](/auto-hebergement-guide-complet-2025/), et un décalage horaire peut faire planter des renouvellements de certificats ou corrompre des logs. Cet article couvre comment définir ou changer le fuseau horaire sous Linux, synchroniser l'heure de ton serveur avec NTP, et les commandes à connaître absolument.

![Synchronisation NTP Linux](https://media4.giphy.com/media/26Do6la9cIiHvIwMM/giphy.gif?cid=7941fdc6pnk6cs7qnembjdx4x1mxp0ll1p00n5uszui5sssz&ep=v1_gifs_search&rid=giphy.gif&ct=g)

## Table des matières

## Comment synchroniser l'heure du serveur sous Linux

La synchronisation de l'heure de ton serveur avec NTP garantit que l'horloge de ton système est toujours précise. La plupart des distributions Linux embarquent `systemd-timesyncd`, un client NTP léger qui fonctionne sans configuration.

Pour vérifier l'état actuel de la synchronisation :

```bash
timedatectl status
```

Si le service NTP est inactif, active-le avec :

```bash
timedatectl set-ntp true
```

Pour vérifier plus en détail l'état de `systemd-timesyncd` :

```bash
systemctl status systemd-timesyncd
```

S'il est désactivé, lance-le :

```bash
systemctl start systemd-timesyncd
systemctl enable systemd-timesyncd
```

Sur mon homelab Proxmox, j'ai testé `systemd-timesyncd` et `chrony` côte à côte. Pour un VPS ou un serveur de fichiers classique, `timesyncd` fait très bien le job. Si tu as des besoins de précision sub-milliseconde (NFS, Kerberos, cluster haute dispo), passe à chrony.

> ⚠️ **Attention — Kerberos et Active Directory**
> Kerberos tolère un décalage d'horloge de 5 minutes maximum entre le client et le contrôleur de domaine. Au-delà, l'authentification échoue silencieusement. Si tu [connectes Ubuntu à Active Directory](/connecter-les-systemes-ubuntu-a-active-directory-en-utilisant-sssd/), vérifie la synchro NTP en priorité.

Pour les détails de configuration avancée, consulte la [documentation officielle systemd-timesyncd](https://www.freedesktop.org/software/systemd/man/latest/systemd-timesyncd.service.html).

## Comment définir ou changer le fuseau horaire sous Linux

### Vérifier le fuseau horaire actuel

Avant de changer ton fuseau horaire, vérifie ce qui est actuellement défini :

```bash
timedatectl
```

### Lister les fuseaux horaires disponibles

Pour lister tous les fuseaux horaires disponibles :

```bash
timedatectl list-timezones
```

Tu peux aussi explorer le contenu du répertoire `/usr/share/zoneinfo/` pour trouver ton fuseau préféré. Pour filtrer sur l'Europe uniquement :

```bash
timedatectl list-timezones | grep Europe
```

### Définir le fuseau horaire

Pour définir le fuseau horaire de ton système :

```bash
timedatectl set-timezone Europe/Paris
```

Cette commande crée un lien symbolique de `/usr/share/zoneinfo/` vers `/etc/localtime`. Tu peux aussi le faire manuellement :

```bash
ln -s /usr/share/zoneinfo/Europe/Paris /etc/localtime
```

## Configurer le fuseau horaire sous Ubuntu

### Méthode 1 : Utiliser le terminal

Lance la commande interactive `tzselect` :

```bash
tzselect
```

Suis les invites pour sélectionner ton continent, ton pays, puis ton fuseau horaire.

### Méthode 2 : Utiliser timedatectl

C'est la méthode recommandée. `timedatectl set-timezone` est plus rapide et plus scriptable que `tzselect`.

### Méthode 3 : Utiliser l'interface graphique

Si tu es sur un poste de travail Ubuntu avec GNOME, va dans **Paramètres > Date & Heure** et sélectionne ton fuseau sur la carte.

## Foire aux questions

### Comment vérifier mon fuseau horaire actuel sous Linux ?

Lance `timedatectl` dans le terminal. La ligne `Time zone` affiche le fuseau actuel, et `NTP service` indique si la synchronisation est active.

### Comment lister tous les fuseaux horaires disponibles ?

Tape `timedatectl list-timezones`. Pour filtrer sur la France : `timedatectl list-timezones | grep Europe`.

### Comment changer le fuseau horaire sous Ubuntu en utilisant le terminal ?

Lance `timedatectl set-timezone Europe/Paris` (remplace `Europe/Paris` par ton fuseau horaire). Pas besoin de redémarrer le système.

## Conclusion

Deux commandes suffisent pour gérer l'heure de ton serveur Linux : `timedatectl` pour tout consulter et configurer, et `timedatectl set-ntp true` pour activer la synchro. Le reste se gère tout seul via `systemd-timesyncd`. Si tu administres un homelab ou un VPS, prends l'habitude de vérifier la synchro NTP à chaque nouvelle install. Ça évite des bugs incompréhensibles liés au décalage horaire, notamment dans les logs ou les renouvellements de certificats Let's Encrypt.

La configuration de l'heure fait partie des bases à avoir en place avant d'ouvrir des services au réseau, au même titre que [sécuriser ton serveur Linux](/securite-de-votre-serveur-linux/).

## Pour aller plus loin

- [Documentation officielle systemd-timesyncd](https://www.freedesktop.org/software/systemd/man/latest/systemd-timesyncd.service.html)
- [Dépannage montage partition RAID Linux en mode secours](/depannage-montage-partition-raid-linux-mode-secours/) (pour quand ton serveur ne démarre plus)
- [Guide swap Linux : configuration et optimisation](/guide-swap-linux-configuration-optimisation/)
