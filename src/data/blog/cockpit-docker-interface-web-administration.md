---
title: "Cockpit Docker : interface web d'administration Linux moderne"
description: "Cockpit Docker : installe l'interface web native Cockpit, ajoute le plugin cockpit-docker et pilote conteneurs, stockage et pare-feu depuis un navigateur."
pubDatetime: "2026-10-01T11:01:12+02:00"
modDatetime: "2026-09-30T08:00:00.000Z"
author: Brandon
tags:
  - linux
  - dashboard
  - stockage
  - intermediaire
featured: false
draft: false
focusKeyword: cockpit docker
faqs:
  - question: "Cockpit Docker consomme combien de ressources sur un serveur ?"
    answer: "Très peu. Cockpit lui-même est un démon C léger sans base de données, et le plugin cockpit-docker se contente de parler au socket Docker. Ça tourne sans souci sur un petit VPS ou un Raspberry Pi."
  - question: "Faut-il choisir entre cockpit docker et cockpit-podman ?"
    answer: "Ça dépend de ta distribution. Debian, Ubuntu et Arch proposent cockpit-docker pour piloter le démon Docker classique, tandis que Fedora et RHEL poussent cockpit-podman, aligné sur leur choix de Podman par défaut."
  - question: "Cockpit remplace-t-il complètement le terminal SSH ?"
    answer: "Non, et c'est volontaire. Cockpit affiche un terminal intégré dans le navigateur, mais il complète SSH pour les tâches visuelles, il ne le remplace pas pour le scripting ou l'automatisation."
---
> 💡 **TL;DR**
> - Cockpit est une interface web native pour administrer un serveur Linux (stockage, réseau, comptes, logs, mises à jour) sans rien installer en conteneur
> - Le plugin cockpit-docker ajoute la gestion des conteneurs Docker directement dans l'interface, en complément ou à la place de cockpit-podman sur Fedora/RHEL
> - Installation par le gestionnaire de paquets natif de ta distribution, accès via `https://ton-serveur:9090`, gratuit et sous licence LGPL

## Cockpit, l'interface qu'on croyait plus avoir besoin

Tu gères ton serveur Linux en SSH depuis des années. `htop` pour la charge, `journalctl` pour les logs, `nmtui` pour le réseau, `docker ps` pour les conteneurs. Ça marche, mais ça demande de connaître dix commandes et de jongler entre autant de terminaux.

Cockpit part d'un constat simple : administrer un serveur ne devrait pas obliger à choisir entre ligne de commande et confort visuel. C'est une interface web qui tourne directement sur ta machine, sans conteneur intermédiaire, sans agent lourd, et qui expose ce que tu fais déjà en SSH dans un tableau de bord lisible. Ajoute le module Docker et tu obtiens cockpit docker : le même confort pour tes conteneurs.

## Table des matières

## Qu'est-ce que Cockpit exactement

Cockpit est un projet porté par Red Hat, publié sous licence LGPL, avec le code source ouvert sur [cockpit-project.org](https://cockpit-project.org). Contrairement à Portainer ou aux dashboards qu'on installe en conteneur, Cockpit est **natif** : c'est un paquet système, un service `cockpit.socket`, qui parle directement à systemd, D-Bus et PolicyKit pour piloter la machine sans couche intermédiaire.

Il est packagé officiellement pour Fedora, Red Hat Enterprise Linux, Fedora CoreOS, CentOS, Debian, Ubuntu, Arch Linux, openSUSE Tumbleweed et SUSE Linux Enterprise Micro. Pas de build maison à bricoler, un simple `apt install` ou `dnf install` suffit.

Ce que Cockpit gère nativement, sans aucun module supplémentaire :

- **Ressources système** : graphiques CPU, RAM, disque et réseau en temps réel
- **Stockage** : disques, partitions, volumes LVM, RAID logiciel, montages NFS
- **Comptes utilisateurs** : création, groupes, clés SSH autorisées
- **Services systemd** : démarrage, arrêt, logs par unité
- **Mises à jour système** : visualisation et application des paquets en attente
- **Terminal intégré** : un vrai shell dans le navigateur, pour les cas où l'interface graphique ne suffit pas

C'est cette base solide qui rend cockpit docker intéressant : tu n'ajoutes pas un outil de plus à surveiller, tu étends un outil que tu as déjà pour ton serveur.

## Installer Cockpit sur ton serveur Linux

L'installation change peu d'une distribution à l'autre, Cockpit reste un paquet natif partout.

Sur Debian et Ubuntu :

```bash
sudo apt update
sudo apt install cockpit
sudo systemctl enable --now cockpit.socket
```

Sur Fedora et RHEL, Cockpit est souvent déjà présent par défaut. Si ce n'est pas le cas :

```bash
sudo dnf install cockpit
sudo systemctl enable --now cockpit.socket
```

Sur Arch Linux :

```bash
sudo pacman -S cockpit
sudo systemctl enable --now cockpit.socket
```

Une fois le service actif, direction `https://ton-serveur:9090` dans ton navigateur. Connecte-toi avec un compte système existant, celui que tu utilises déjà en SSH. Pas de mot de passe séparé à gérer, pas de compte admin à créer à part, Cockpit s'appuie sur PAM et les comptes Linux classiques.

⚠️ Le certificat TLS généré par défaut est auto-signé. Ton navigateur va te prévenir, et c'est normal sur un premier accès en local. Pour un accès depuis l'extérieur de ton réseau, passe par un reverse proxy avec un vrai certificat plutôt que d'exposer le 9090 brut sur internet.

## Ajouter la gestion cockpit docker avec le module dédié

Par défaut, l'interface de base ne sait rien faire avec tes conteneurs. Pour obtenir cockpit docker au sens où on l'entend en général, il faut installer le module dédié en plus du cœur Cockpit.

Sur Debian et Ubuntu :

```bash
sudo apt install cockpit-docker
sudo systemctl restart cockpit
```

Sur Arch Linux, le paquet `cockpit-docker` est disponible dans les dépôts officiels :

```bash
sudo pacman -S cockpit-docker
sudo systemctl restart cockpit
```

Sur Fedora et RHEL, la situation est différente. Red Hat pousse Podman comme moteur de conteneurs par défaut depuis plusieurs versions, et le module correspondant s'appelle `cockpit-podman` plutôt que cockpit docker :

```bash
sudo dnf install cockpit-podman
sudo systemctl restart cockpit
```

Une fois le module installé, recharge la page Cockpit dans ton navigateur : un nouvel onglet « Conteneurs » apparaît dans le menu latéral. Tu y retrouves la liste de tes conteneurs, leurs logs en direct, leurs statistiques CPU/mémoire, et la possibilité d'en démarrer, arrêter ou supprimer un sans taper une seule commande `docker`.

💡 Le module cockpit-docker lit le socket Docker local (`/var/run/docker.sock`). Ton utilisateur doit appartenir au groupe `docker`, ou se connecter à Cockpit avec un compte disposant des privilèges administrateur, sinon la liste des conteneurs reste vide.

## Ce que Cockpit gère en plus des conteneurs

L'intérêt réel de cockpit docker, c'est de ne pas rester isolé sur la gestion des conteneurs. Ton serveur a d'autres besoins, et Cockpit les couvre dans la même interface.

Côté réseau et pare-feu, Cockpit s'appuie sur firewalld pour gérer les zones et les services autorisés depuis l'interface graphique. Si tu préfères rester en ligne de commande pour ce point précis, mes articles sur [UFW Docker](/ufw-docker-pare-feu-linux/) et [nftables](/nftables-docker-pare-feu-linux/) couvrent les deux approches les plus courantes sous Linux, avec leurs subtilités propres aux conteneurs.

Côté temps système, Cockpit affiche l'état de la synchronisation NTP directement dans le tableau de bord général. Si l'horloge de ton serveur dérive, ça se voit en un coup d'œil, sans avoir à taper `timedatectl`. Pour un serveur NTP fiable derrière tes services conteneurisés, j'ai détaillé la mise en place avec [Chrony](/chrony-docker-serveur-ntp-homelab/).

Côté stockage, le module dédié montre tes disques physiques, tes volumes LVM et l'usage de chaque partition, avec des actions directes pour étendre un volume ou monter un partage réseau. C'est particulièrement pratique quand un conteneur commence à saturer un disque et que tu veux comprendre vite ce qui prend la place, sans enchaîner `df -h` et `du -sh` dans dix dossiers différents.

## Sécuriser l'accès à l'interface

Cockpit donne accès à des privilèges système complets une fois connecté. Ce n'est pas un outil à exposer sans réflexion, exactement comme le socket Docker que cockpit docker manipule en coulisses.

Trois réflexes simples avant de considérer l'installation terminée :

✅ Garde le port 9090 fermé au monde extérieur, accessible uniquement depuis ton réseau local ou via un VPN comme WireGuard ou Tailscale.

✅ Si un accès distant est vraiment nécessaire, passe par un reverse proxy avec authentification et certificat TLS valide plutôt que d'exposer Cockpit directement.

✅ Protège les tentatives de connexion répétées sur SSH et sur l'interface web avec [Fail2Ban](/fail2ban-docker-securite-serveur/), qui bloque automatiquement les adresses IP qui multiplient les essais infructueux.

Cockpit journalise chaque connexion et chaque action effectuée via l'interface, visible directement dans l'onglet logs. Ça vaut le coup d'y jeter un œil de temps en temps, surtout sur un serveur exposé au-delà de ton réseau local.

## Cockpit face à Portainer et Webmin

La comparaison revient souvent : pourquoi choisir cockpit docker plutôt que Portainer, qui reste la référence pour piloter des conteneurs en interface web ?

Portainer se concentre entièrement sur Docker et Kubernetes. Il tourne lui-même en conteneur, propose une gestion multi-hôtes avancée, des stacks Compose depuis l'interface, et une gestion fine des rôles utilisateurs. Si ton besoin s'arrête strictement aux conteneurs et que tu veux le maximum de fonctionnalités sur ce périmètre, Portainer reste plus complet que cockpit docker sur ce point précis.

Cockpit vise un périmètre différent : l'administration du serveur dans son ensemble, avec les conteneurs comme une brique parmi d'autres, pas comme la fonction principale. Pas de conteneur à maintenir pour faire tourner l'outil lui-même, pas de base de données à sauvegarder, une intégration directe avec systemd et PolicyKit.

Face à Webmin, la différence est plus nette encore. Webmin est plus ancien, avec une interface datée et une architecture à base de modules Perl. Cockpit est plus récent, plus léger visuellement, et son intégration avec systemd le rend plus cohérent sur les distributions modernes. Le module cockpit docker profite directement de cette base, sans les compromis d'un outil pensé pour une autre époque.

## Conclusion

Cockpit ne remplace pas ton terminal, et ce n'est pas son objectif. Ce qu'il apporte, c'est une vue d'ensemble de ton serveur, accessible depuis n'importe quel navigateur, sans bricolage supplémentaire. Ajoute cockpit docker par-dessus et tu obtiens un point d'entrée unique pour surveiller autant tes conteneurs que le système qui les héberge.

Si tu gères déjà un ou deux serveurs Linux en SSH pur, installer Cockpit prend cinq minutes et ne retire rien à ce que tu fais déjà. La vraie question, c'est combien de temps tu vas encore perdre à enchaîner les commandes avant de laisser cockpit docker afficher tout ça d'un seul coup d'œil.
