---
title: "Samba Docker : partage de fichiers Windows/Linux"
description: Monte un serveur Samba Docker avec docker-compose pour partager des fichiers entre Windows, Linux et macOS en quelques minutes, sans prise de tête.
pubDatetime: "2026-10-19T11:02:11+02:00"
modDatetime: "2026-10-18T08:00:00.000Z"
author: Brandon
tags:
  - linux
  - docker
  - stockage
  - hardening
  - intermediaire
featured: false
draft: false
focusKeyword: samba docker
faqs:
  - question: "Quelle image Samba Docker choisir en 2026 ?"
    answer: "Évite dperson/samba, abandonnée depuis plusieurs années. Pars sur ghcr.io/servercontainers/samba, qui reçoit encore des correctifs et des tests automatisés régulièrement."
  - question: "Mon partage Samba Docker est invisible depuis Windows 11, pourquoi ?"
    answer: "Windows ne découvre plus les partages via NetBIOS. Active le service WSDD2 de l'image, ou connecte-toi directement par l'adresse IP du conteneur dans l'explorateur."
  - question: "Faut-il exposer le port 445 de Samba Docker sur internet ?"
    answer: "Non, jamais. Le protocole SMB n'est pas conçu pour ça et attire les scans automatisés. Garde-le sur ton réseau local, derrière ton pare-feu et ton VPN."
---
> 💡 **TL;DR**
> - Un conteneur Samba Docker partage des fichiers entre Windows, Linux et macOS sans installer Samba sur l'hôte et sans polluer le système
> - L'image `dperson/samba`, longtemps la référence, est abandonnée depuis des années : pars sur `ghcr.io/servercontainers/samba`, encore maintenue
> - Un `docker-compose.yml`, quelques variables d'environnement pour les comptes et les partages, et les bons UID/GID suffisent à tout faire tourner

## Samba Docker : ton partage de fichiers Windows/Linux sans prise de tête

Tu as un NAS maison, un serveur Linux qui traîne, ou juste un conteneur en plus sur ta machine, et tu veux que ton PC Windows, ton Mac et ton serveur Linux puissent tous lire et écrire dans le même dossier. La réponse historique à ce problème s'appelle Samba, l'implémentation libre du protocole SMB qu'utilise Windows depuis toujours. Le projet existe depuis les années 90, il est développé et maintenu par une communauté mondiale active, et sa version stable actuelle tourne autour de la branche 4.25.

Le monter en Docker plutôt qu'en paquet système change tout. Tu isoles la configuration, tu la versionnes dans un `docker-compose.yml`, et tu peux la déplacer d'une machine à l'autre en changeant deux lignes. Chez moi, ce Samba Docker sert surtout à centraliser les sauvegardes de mes VM et à partager un dossier de travail entre mon poste Linux et le PC Windows de la maison. Spoiler : ça prend dix minutes à monter, le vrai travail c'est de comprendre les permissions.

## Table des matières

## Quelle image Docker choisir pour Samba

Il n'existe pas d'image Docker officielle publiée par l'équipe Samba elle-même. Le site [samba.org](https://www.samba.org/) distribue les sources et les paquets systèmes, pas de conteneur. Tout ce que tu trouveras vient de la communauté, et c'est là que la plupart des tutoriels te mènent vers une impasse.

L'image `dperson/samba`, sur Docker Hub, a été pendant longtemps LA référence pour monter un partage Samba Docker rapidement. Le problème, c'est qu'elle n'a plus reçu de mise à jour depuis plus de cinq ans. Pas de correctif de sécurité, pas de suivi des versions récentes de Samba. Elle fonctionne encore, elle tourne même sur des milliers de serveurs, mais tu bâtis ton partage de fichiers sur une base qui ne bougera plus.

L'alternative sérieuse aujourd'hui, c'est `ghcr.io/servercontainers/samba`. Le projet est actif, basé sur Alpine, disponible en multi-architecture (x86 et ARM, donc ton Raspberry Pi ou ton petit NAS ARM peuvent aussi en profiter), et chaque image publiée passe désormais par un test fonctionnel de `smbd` avant d'être poussée. C'est ce que j'utilise, et c'est celle que je recommande pour tout nouveau déploiement. Si tu préfères Podman à Docker, le même `docker-compose.yml` fonctionne quasiment tel quel, j'en parle dans mon comparatif [Podman vs Docker : conteneurs rootless sans daemon](/podman-vs-docker-rootless/).

## Installer Samba avec docker-compose

Crée un dossier pour ton projet, avec un sous-dossier qui contiendra les fichiers partagés :

```bash
mkdir -p samba-docker/data/partage
cd samba-docker
```

Puis le `docker-compose.yml` :

```yaml
services:
  samba:
    image: ghcr.io/servercontainers/samba
    container_name: samba
    hostname: nas-maison
    restart: unless-stopped
    environment:
      ACCOUNT_brandon: "motdepasse_a_changer"
      UID_brandon: "1000"
      SAMBA_CONF_WORKGROUP: "WORKGROUP"
      SAMBA_VOLUME_CONFIG_partage: "[partage];path=/shares/partage;valid users=brandon;read only=no;guest ok=no"
    ports:
      - "445:445"
    volumes:
      - ./data/partage:/shares/partage
    cap_add:
      - CAP_NET_ADMIN
```

Lance-le :

```bash
docker compose up -d
```

Ce `docker compose up -d` suffit à démarrer ton Samba Docker avec un utilisateur et un partage. Sur Linux, tu montes le partage avec `smbclient` ou directement dans ton gestionnaire de fichiers via `smb://ip-du-serveur/partage`. Sur Windows, tape `\\ip-du-serveur\partage` dans l'explorateur. Sur macOS, Cmd+K dans le Finder puis la même adresse en `smb://`.

## Créer des utilisateurs, des groupes et des partages

L'image fonctionne presque entièrement par variables d'environnement, ce qui la rend facile à scripter ou à piloter depuis un fichier `.env`. Les plus utiles :

- `ACCOUNT_<utilisateur>` : crée le compte, la valeur est le mot de passe
- `UID_<utilisateur>` : fixe l'UID numérique du compte, à faire correspondre à l'UID réel sur ton hôte
- `GROUP_<nom>` : crée un groupe avec le GID donné en valeur
- `GROUPS_<utilisateur>` : rattache l'utilisateur à un ou plusieurs groupes existants, séparés par des virgules
- `SAMBA_VOLUME_CONFIG_<nom>` : décrit un partage complet, avec le chemin, les droits et les utilisateurs autorisés

Pour plusieurs utilisateurs et plusieurs partages, tu empiles simplement les variables. Exemple avec une famille et deux dossiers séparés :

```yaml
environment:
  ACCOUNT_brandon: "motdepasse1"
  UID_brandon: "1000"
  ACCOUNT_julie: "motdepasse2"
  UID_julie: "1001"
  GROUP_famille: "2000"
  GROUPS_brandon: "famille"
  GROUPS_julie: "famille"
  SAMBA_VOLUME_CONFIG_prive: "[prive];path=/shares/prive;valid users=brandon;read only=no"
  SAMBA_VOLUME_CONFIG_commun: "[commun];path=/shares/commun;valid users=@famille;read only=no"
```

Note le `@famille` devant le nom du groupe dans `valid users` : c'est la syntaxe Samba classique pour autoriser un groupe entier plutôt qu'un seul compte. ✅ Pense à monter un volume Docker distinct par ligne `path=` que tu déclares, sinon le dossier n'existera jamais dans le conteneur et le partage refusera toute connexion.

## Permissions UID/GID : le piège qui bloque tout le monde

C'est le point qui fait perdre le plus de temps avec Samba Docker, et de loin. Les fichiers que ton conteneur écrit héritent de l'UID que tu as donné à l'utilisateur Samba, pas de celui de ton compte sur l'hôte. Si ton compte Linux a l'UID 1000 et que tu as déclaré `UID_brandon: "1000"`, tout va bien, tu pourras relire et modifier les fichiers depuis l'hôte sans souci. Si tu as laissé un UID par défaut qui ne correspond à rien chez toi, tu vas te retrouver avec des fichiers appartenant à un utilisateur fantôme, illisibles depuis ton shell.

⚠️ Vérifie ton UID réel avant de toucher au `docker-compose.yml` :

```bash
id -u
```

Fais correspondre cette valeur à la variable `UID_<utilisateur>` du conteneur, et le problème disparaît. Si tu migres un partage existant depuis un vieux NAS ou un ancien serveur Samba installé nativement, regarde aussi les permissions Unix classiques (`chmod`, `chown`) sur le dossier monté : Samba respecte toujours les droits du système de fichiers sous-jacent, en plus de ses propres règles `valid users`.

## Sécuriser, surveiller et dépanner ton partage Samba

Le protocole SMB a une mauvaise réputation historique, pas totalement injustifiée. La règle de base avec ce Samba Docker : le port 445 reste sur ton réseau local, jamais exposé directement sur internet. Si tu as besoin d'y accéder depuis l'extérieur, passe par un VPN plutôt que par une redirection de port sur ta box.

Sur le pare-feu de l'hôte, limite l'accès au port 445 aux sous-réseaux que tu connais. J'ai un guide dédié sur [UFW Docker : configurer le pare-feu sans casser les conteneurs](/ufw-docker-pare-feu-linux/) si tu veux restreindre ça proprement sans bloquer le trafic normal entre conteneurs. Si ton Samba Docker est quand même accessible depuis un réseau plus large (bureau, campus, colocation), ajoute une protection contre le brute-force avec [Fail2Ban Docker : bloquer les attaques brute-force automatiquement](/fail2ban-docker-securite-serveur/), qui sait surveiller les logs Samba au même titre que SSH.

Pour la surveillance dans le temps, un simple `docker logs samba` dépanne à chaud, mais si tu veux de vraies alertes (conteneur qui redémarre en boucle, disque qui se remplit), connecte-le à ton stack de supervision avec [Grafana Prometheus Docker : monitoring pro pour 0€](/grafana-prometheus-docker-monitoring-pro/). Et si certains utilisateurs n'ont besoin que d'un accès web simple sans configurer de client SMB, [File Browser Docker : ton gestionnaire de fichiers web auto-hébergé](/filebrowser-docker-gestionnaire-fichiers/) peut pointer sur le même volume et servir de complément, pas de remplacement.

Côté dépannage, trois erreurs reviennent sans cesse :

- **`NT_STATUS_LOGON_FAILURE`** à la connexion : mot de passe faux, ou compte créé après coup sans redémarrer le conteneur. Redémarre le service après toute modification des variables `ACCOUNT_`.
- **Accès refusé en écriture alors que la connexion fonctionne** : c'est presque toujours l'UID/GID mal aligné vu plus haut, vérifie les permissions du dossier monté depuis l'hôte.
- **Le partage n'apparaît pas tout seul dans l'explorateur Windows** : Windows n'utilise plus la découverte NetBIOS par défaut. Active le service WSDD2 inclus dans l'image, ou connecte-toi directement avec `\\adresse-ip\partage` sans attendre qu'il apparaisse dans le réseau.

## Conclusion

Monter un Samba Docker n'a rien de compliqué une fois que tu as choisi la bonne image et compris comment les UID circulent entre l'hôte et le conteneur. La vraie décision qui compte, c'est d'écarter les images abandonnées au profit d'une base encore maintenue, et de garder ce service loin d'internet. Avec ça posé, le reste n'est que des lignes de `docker-compose.yml` à ajuster selon tes utilisateurs et tes dossiers.
