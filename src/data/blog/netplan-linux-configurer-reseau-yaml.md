---
title: "Netplan Linux : configurer le réseau en YAML simplement"
description: "Netplan Linux : configure les interfaces réseau Ubuntu et Debian en YAML, IP statique, DHCP, nameservers et routes, avec apply et try en sécurité."
pubDatetime: "2026-10-21T11:02:11+02:00"
modDatetime: "2026-10-20T08:00:00.000Z"
author: Brandon Visca
tags:
  - linux
  - reseau
  - dns
  - intermediaire
featured: false
draft: false
focusKeyword: netplan linux
faqs:
  - question: "Netplan Linux fonctionne-t-il aussi sur Debian, ou seulement sur Ubuntu ?"
    answer: "Les deux. Netplan est né chez Canonical et vient par défaut sur Ubuntu depuis la 17.10, mais le paquet netplan.io est aussi disponible sur Debian et sur Arch Linux via les dépôts officiels."
  - question: "Une commande netplan apply mal écrite peut-elle me couper l'accès SSH ?"
    answer: "Oui, c'est le vrai risque. Une adresse ou une route fausse te fait perdre la connexion immédiatement. Passe toujours par netplan try avant un apply définitif sur un serveur distant."
  - question: "Faut-il redémarrer le serveur après avoir modifié un fichier Netplan ?"
    answer: "Non dans la grande majorité des cas, netplan apply suffit à chaud. Un redémarrage reste utile seulement si tu as supprimé un bridge ou un bond qui refuse de se détacher proprement."
---
> 💡 **TL;DR**
> - Netplan Linux centralise la configuration réseau d'Ubuntu et Debian dans des fichiers YAML lisibles, au lieu de jongler entre `ifupdown`, `nmtui` et des scripts maison
> - Un fichier décrit l'état voulu (DHCP, IP statique, routes, DNS), et `netplan apply` traduit ça vers systemd-networkd ou NetworkManager en coulisses
> - `netplan try` applique la config avec un retour arrière automatique après 120 secondes si tu ne confirmes rien, pile ce qu'il faut avant de risquer ta session SSH

## Netplan Linux, la fin du bazar des fichiers réseau à la main

Tu as déjà édité `/etc/network/interfaces` à la main, redémarré le service réseau en croisant les doigts, et espéré que la syntaxe exacte de la route par défaut te revienne de mémoire ? Netplan Linux existe pour arrêter ce petit jeu. C'est la couche d'abstraction que Canonical a introduite avec Ubuntu 17.10 pour remplacer l'ancien système basé sur `ifupdown`, et qui est devenue le standard par défaut sur toutes les versions récentes d'Ubuntu, serveur comme desktop.

Le principe est simple : tu décris l'état réseau que tu veux dans un fichier YAML, et Netplan génère la configuration adaptée pour le moteur qui tourne vraiment en dessous, `systemd-networkd` sur un serveur ou `NetworkManager` sur un poste de travail. Tu ne parles plus directement à ces moteurs, tu parles à Netplan, et Netplan traduit.

## Table des matières

## Qu'est-ce que Netplan Linux exactement

Netplan Linux n'est pas un service réseau en soi, c'est un générateur de configuration. Le projet est développé par Canonical, publié en open source sous licence GPL, avec le code hébergé sur GitHub sous l'organisation `canonical`. Après plusieurs années en version 0.x, le projet a franchi le cap de la version 1.0 stable en 2024, et les dépôts Ubuntu et Debian récents distribuent désormais des versions de la branche 1.2.

Concrètement, Netplan lit tes fichiers YAML dans `/etc/netplan/`, les transforme en configuration native pour le backend choisi, puis applique cette configuration. Il existe deux backends possibles :

- **`systemd-networkd`** : le choix par défaut sur Ubuntu Server et sur la majorité des installations headless. Léger, rapide, pas d'interface graphique derrière.
- **`NetworkManager`** : le choix par défaut sur Ubuntu Desktop, plus adapté à un poste qui change souvent de réseau Wi-Fi.

Le renderer se déclare dans le fichier YAML lui-même, au niveau global ou par interface. Si rien n'est précisé, Netplan Linux retombe sur le renderer par défaut de ta distribution.

💡 Mon setup chez moi : tous mes serveurs Debian et Ubuntu tournent en `networkd`, mon laptop reste en `NetworkManager`. Pas de raison de changer ça tant que tu n'as pas un besoin précis.

## Où vivent les fichiers de configuration

Les fichiers YAML de Netplan Linux vivent dans trois emplacements, lus dans cet ordre de priorité croissante :

```text
/lib/netplan/    # fichiers fournis par des paquets
/etc/netplan/    # tes fichiers, ceux que tu édites
/run/netplan/    # configuration temporaire, effacée au reboot
```

En pratique, tu travailles presque toujours dans `/etc/netplan/`. Ubuntu Server y installe un fichier par défaut, généralement nommé `00-installer-config.yaml` ou `50-cloud-init.yaml` selon la méthode d'installation. Tu peux soit l'éditer directement, soit ajouter un fichier séparé numéroté plus haut, par exemple `01-netcfg.yaml`, pour que Netplan Linux le fusionne par-dessus.

⚠️ Ces fichiers peuvent contenir des identifiants Wi-Fi ou des clés VPN en clair. La documentation officielle de Netplan recommande de les garder en `chmod 600`, lisibles uniquement par root. Un `ls -l /etc/netplan/` qui affiche des droits ouverts à tout le monde est un vrai problème de sécurité, pas un détail.

## Configurer une interface en DHCP

Le cas le plus simple : une interface qui récupère son adresse automatiquement. Crée ou édite un fichier dans `/etc/netplan/`, par exemple `01-netcfg.yaml` :

```yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    ens18:
      dhcp4: true
```

Remplace `ens18` par le nom réel de ton interface, visible avec `ip link` ou `ip a`. Les noms d'interfaces modernes suivent la convention de nommage prédictible de systemd (`ens18`, `enp2s0`, `eth0` sur les configurations plus anciennes), donc vérifie toujours avant de copier un exemple tel quel.

Pour générer la configuration sans encore l'appliquer, lance :

```bash
sudo netplan generate
```

Cette commande valide la syntaxe YAML et produit les fichiers de configuration pour le backend choisi, sans toucher à l'état réseau actif. C'est une bonne première vérification avant d'aller plus loin.

## Passer en IP statique : adresses, routes et DNS

Pour un serveur, le DHCP n'est pas toujours souhaitable. Tu veux une IP fixe, une route par défaut explicite, et des résolveurs DNS précis. Voici un fichier complet avec Netplan Linux en IP statique :

```yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    enp2s0:
      addresses:
        - 192.168.10.20/24
      routes:
        - to: default
          via: 192.168.10.1
      nameservers:
        search:
          - lan.local
        addresses:
          - 192.168.10.53
          - 1.1.1.1
```

Quelques points à retenir sur cette syntaxe :

- `addresses` attend une adresse avec son préfixe CIDR, pas de masque séparé. `192.168.10.20/24`, pas `192.168.10.20` avec un `netmask` à côté.
- `to: default` désigne la route par défaut, équivalent de `0.0.0.0/0`. C'est plus lisible que l'ancienne syntaxe `gateway4` que Netplan Linux a dépréciée.
- `nameservers.addresses` accepte plusieurs serveurs DNS, essayés dans l'ordre. Ici un résolveur local et Cloudflare en secours.
- `nameservers.search` liste les domaines de recherche, utile si tu résous des noms courts sur ton réseau local comme `proxmox` au lieu de `proxmox.lan.local`.

Si ton serveur gère aussi le temps système, le DNS n'est que la moitié de l'histoire réseau : j'ai détaillé la mise en place d'un résolveur de temps fiable avec [Chrony Docker](/chrony-docker-serveur-ntp-homelab/), qui s'appuie justement sur une résolution DNS saine pour contacter ses pools NTP.

## Appliquer la configuration sans couper ta session SSH

C'est le moment où Netplan Linux devient vraiment utile, ou vraiment dangereux. Si tu es connecté en SSH sur le serveur que tu configures, une erreur dans l'adresse ou la route peut te couper l'accès immédiatement, sans filet. La vraie question c'est : comment tester sans te retrouver à devoir rebrancher un écran physique.

La réponse s'appelle `netplan try` :

```bash
sudo netplan try
```

Cette commande applique la nouvelle configuration tout de suite, puis attend une confirmation. Si tu ne réponds rien dans les 120 secondes par défaut, Netplan Linux annule automatiquement et restaure l'ancienne configuration. Si ta connexion SSH venait de sauter à cause d'une mauvaise adresse, elle revient toute seule, et tu n'as rien cassé.

✅ Sur un serveur distant, prends l'habitude de toujours passer par `netplan try` avant un `netplan apply` définitif. Le délai se règle avec `--timeout`, utile si ta configuration inclut du bonding ou du STP qui prend plus d'une minute à se stabiliser.

Une fois que la configuration te convient, confirme avec Entrée, ou applique directement sans phase de test :

```bash
sudo netplan apply
```

`netplan apply` régénère la configuration backend, relance `systemd-networkd` ou `NetworkManager`, et réattache les interfaces qui ont besoin de passer par les règles de renommage udev. Spoiler : ça va marcher dans l'immense majorité des cas, mais garde toujours une deuxième voie d'accès (console Proxmox, iDRAC, iLO) la première fois que tu touches à une IP de production.

## Dépanner une configuration qui refuse de s'appliquer

Bon, on va pas se mentir, ça arrive à tout le monde de se planter sur l'indentation YAML ou sur un nom de clé. Quelques réflexes avant de paniquer :

1. **Valide la syntaxe d'abord** avec `sudo netplan generate`, qui te renvoie une erreur de parsing claire si un fichier est mal formé, sans rien appliquer.
2. **Vérifie l'état réellement actif** avec `sudo netplan status`, qui affiche la configuration en cours par interface, pas juste ce qui est écrit sur disque.
3. **Repère le mauvais fichier** si tu en as plusieurs dans `/etc/netplan/` : Netplan Linux les fusionne par ordre alphabétique, et un fichier plus récent peut silencieusement écraser une clé d'un fichier plus ancien.
4. **Un bridge ou un bond fantôme** qui ne disparaît pas après suppression de sa définition YAML est un bug connu de `netplan apply`, qui ne retire pas les interfaces virtuelles déjà créées. Supprime-la manuellement avec `ip link delete` ou redémarre.

Si malgré tout tu perds l'accès réseau complet et que tu dois intervenir en mode de secours pour restaurer un fichier de configuration depuis une sauvegarde locale, la logique de dépannage ressemble beaucoup à celle que j'ai détaillée pour les [problèmes de montage RAID en mode secours Linux](/depannage-montage-partition-raid-linux-mode-secours/) : accès console direct, puis correction à froid avant tout redémarrage.

## Sécuriser les fichiers YAML et comparer avec les alternatives

Netplan Linux n'est pas la seule façon de gérer le réseau sous Linux, et ça vaut le coup de savoir où il se situe.

Face à **NetworkManager en ligne de commande** (`nmcli`), Netplan Linux reste plus lisible pour une configuration statique posée une fois pour toutes sur un serveur. `nmcli` garde l'avantage sur un poste qui change souvent de réseau, avec des profils de connexion basculés à la volée.

Face à **l'ancien `/etc/network/interfaces`**, il n'y a pas vraiment de débat sur Ubuntu récent : ce mécanisme est maintenu pour compatibilité, mais Netplan Linux est le chemin officiel depuis 2017, avec une syntaxe commune entre serveurs et postes de travail.

Face à une interface graphique comme **Cockpit**, les deux se complètent plutôt qu'ils ne s'opposent. Si tu préfères visualiser ton réseau et tes interfaces sans retenir la syntaxe YAML par cœur, j'ai détaillé l'installation de [Cockpit pour l'administration Linux](/cockpit-docker-interface-web-administration/), qui affiche et modifie la config réseau sous le capot via NetworkManager.

Côté sécurité, trois points à vérifier une fois ta configuration en place :

- `chmod 600` sur chaque fichier YAML dans `/etc/netplan/`, surtout ceux qui contiennent un mot de passe Wi-Fi ou une clé VPN.
- Si tu administres plusieurs machines à distance, privilégie un accès par VPN plutôt que d'exposer SSH ou les interfaces d'administration directement sur internet. J'utilise [Headscale en auto-hébergé](/headscale-docker-tailscale-self-hosted/) pour ça sur mon propre réseau, en remplacement d'un Tailscale géré par un tiers.
- Si ton réseau passe par un routeur dédié plutôt que directement par ton serveur Linux, la configuration côté routeur suit une logique différente mais complémentaire, que j'ai couverte dans mon article sur [OpenWrt comme firmware de routeur homelab](/openwrt-firmware-routeur-homelab/).

## Conclusion

Netplan Linux ne révolutionne pas la mise en réseau sous Linux, il la rend juste lisible et reproductible. Un fichier YAML versionnable dans `git`, une syntaxe commune entre DHCP et IP statique, et deux commandes, `try` puis `apply`, qui te protègent du scénario classique où tu te coupes toi-même l'accès à ton propre serveur.

Si tu gères encore tes interfaces à coups de `ifconfig` et de fichiers oubliés, prends dix minutes pour migrer ton premier serveur vers Netplan Linux. Commence par un fichier simple, teste avec `netplan try`, et tu ne reviendras pas en arrière.
