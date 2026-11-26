---
title: "2FAuth Docker : tes codes 2FA hors du téléphone"
description: "2FAuth Docker : déploie ce gestionnaire 2FA auto-hébergé, migre tes comptes TOTP et reprends le contrôle de tes codes sans Google Authenticator."
pubDatetime: "2026-11-26T11:00:22+01:00"
modDatetime: "2026-11-25T08:00:00.000Z"
author: Brandon
tags:
  - securite
  - docker
  - hardening
  - intermediaire
featured: false
draft: false
focusKeyword: 2fauth docker
faqs:
  - question: "Que se passe-t-il si je perds mon téléphone avec mes codes 2FA actuels ?"
    answer: "Avec 2FAuth, le téléphone n'est plus le seul point de défaillance : tes secrets TOTP vivent dans la base de l'instance. Tu génères les codes depuis n'importe quel navigateur connecté, à condition d'avoir sauvegardé la base et l'APP_KEY ailleurs que sur ce même téléphone."
  - question: "2FAuth gère-t-il aussi Steam Guard et les codes HOTP, pas seulement TOTP ?"
    answer: "Oui. En plus du TOTP standard, 2FAuth sait générer des codes HOTP (compteur plutôt que temps) et reconnaît le format spécifique de Steam Guard, directement depuis le même coffre que tes autres comptes."
  - question: "2FAuth Docker est-il assez léger pour tourner sur un Raspberry Pi ou un petit NAS ?"
    answer: "Oui. L'image officielle est publiée pour amd64, arm64 et arm/v7, et s'appuie par défaut sur SQLite sans base de données séparée à faire tourner. L'empreinte reste modeste comparée à une stack avec PostgreSQL ou MySQL à côté."
---
> 💡 **TL;DR**
> - 2FAuth Docker remplace ton app TOTP mobile par un coffre web auto-hébergé, accessible depuis n'importe quel navigateur
> - Un conteneur, un volume, une variable APP_KEY : le déploiement tient dans un `docker-compose.yml`
> - Derrière un reverse proxy HTTPS obligatoire, avec migration depuis Google Authenticator ou Aegis en quelques minutes

## 2FAuth Docker : reprendre la main sur tes codes 2FA

Ton app d'authentification mobile a un défaut qu'on remarque trop tard : elle vit sur un seul appareil. Perds ton téléphone, casse l'écran, change de smartphone sans faire l'export à temps, et tu te retrouves à rouvrir un ticket de support sur chaque service pour réinitialiser ta double authentification. Authy a fermé son client desktop il y a quelques années, Google Authenticator ne propose qu'une synchronisation cloud fermée, et aucune des deux ne te laisse inspecter ou sauvegarder tes secrets proprement.

2FAuth Docker règle ce problème en sortant les codes du téléphone. C'est une application web auto-hébergée, développée par Bubka et publiée en open-source sur GitHub, qui fait exactement ce que fait ton app mobile : générer des codes TOTP, HOTP et Steam Guard à partir d'un secret partagé. La différence, c'est que le coffre tourne chez toi, dans un conteneur, accessible depuis ton ordinateur, ta tablette ou ton téléphone via un navigateur.

Chez moi, le déclic est venu après avoir dû ressaisir une dizaine de 2FA à la main suite à un changement de téléphone. Avec 2FAuth Docker, ce scénario devient juste : je restaure un volume et une variable d'environnement, et tout est de retour.

## Table des matières

## Ce que fait 2FAuth, et ce qu'il ne fait pas

2FAuth n'est pas un gestionnaire de mots de passe. C'est un gestionnaire de secondes clés, strictement dédié à la double authentification. Concrètement, il couvre :

- **TOTP** (Time-based One-Time Password) : le standard utilisé par la quasi-totalité des services qui proposent la 2FA par app
- **HOTP** (HMAC-based, basé sur un compteur plutôt que sur le temps), moins courant mais encore présent sur certains équipements
- **Steam Guard** : le format propriétaire utilisé par Steam, reconnu nativement
- **Comptes multi-utilisateurs** avec des coffres isolés : chaque utilisateur a ses propres secrets chiffrés, utile si plusieurs personnes de ta famille ou de ton équipe partagent l'instance
- **Verrouillage automatique de session**, contrôle de la visibilité des codes à l'écran, et journaux d'audit sur les accès et les générations de codes
- **Connexion par mot de passe ou passkey**, avec support du SSO et d'un mode proxy d'authentification pour déléguer le login à un service tiers
- **Import** depuis d'autres applications (via QR code ou lien `otpauth://`), export et sauvegarde de la base
- Des **extensions navigateur** et une **API** pour scripter la récupération des codes

Techniquement, 2FAuth est construit en Laravel et stocke ses données dans une base SQLite par défaut, le tout dans un unique conteneur. Pas de base externe à provisionner, pas de dépendance à un fournisseur cloud. C'est volontairement minimaliste, et c'est exactement ce qu'on attend d'un outil qui manipule des secrets aussi sensibles.

Ce que 2FAuth Docker ne fait pas : il ne remplace pas un gestionnaire de mots de passe type Vaultwarden, et il ne protège pas lui-même l'accès réseau à son interface. Ça reste ton travail, via un reverse proxy et un pare-feu correct.

## Prérequis pour installer 2FAuth Docker

Avant de lancer le conteneur, vérifie que tu as :

- Docker et Docker Compose v2 sur un serveur Linux (ou un NAS qui supporte les conteneurs)
- Un nom de domaine ou sous-domaine dédié, même en local, pour pouvoir passer en HTTPS derrière un reverse proxy
- Un endroit sûr pour stocker une sauvegarde (clé de chiffrement et base de données), hors de l'appareil qui sert à générer les codes au quotidien
- Idéalement, un accès VPN ou un reverse proxy avec authentification en amont si tu comptes exposer l'instance sur Internet

> ⚠️ 2FAuth décode et affiche des secrets TOTP en clair dans le navigateur. N'expose jamais une instance 2FAuth Docker en HTTP simple sur Internet, même temporairement pour tester.

## Déployer 2FAuth Docker avec Docker Compose

Crée un dossier dédié avec ce `docker-compose.yml` :

```yaml
services:
  2fauth:
    image: 2fauth/2fauth:latest
    container_name: 2fauth
    restart: unless-stopped
    ports:
      - "8000:8000"
    environment:
      - APP_NAME=2FAuth
      - APP_ENV=production
      - APP_URL=https://2fa.mondomaine.fr
      - APP_KEY=REMPLACE_MOI
      - DB_CONNECTION=sqlite
      - DB_DATABASE=/2fauth/database/database.sqlite
      - TZ=Europe/Paris
    volumes:
      - ./2fauth:/2fauth
```

La variable `APP_KEY` est obligatoire : sans elle, le conteneur refuse de démarrer, et c'est elle qui chiffre tous tes secrets au repos. Génère-la avant le premier lancement :

```bash
docker run -it --rm --entrypoint /usr/bin/php 2fauth/2fauth artisan key:generate --show
```

Colle la valeur retournée dans `APP_KEY`, puis démarre :

```bash
docker compose up -d
```

Ouvre `http://IP_DU_SERVEUR:8000` (en HTTPS une fois le reverse proxy en place) et crée le premier compte administrateur. À partir de là, l'interface ressemble à une app TOTP classique : un bouton pour ajouter un compte, un scan de QR code ou une saisie manuelle du secret, et la liste de tes codes qui se rafraîchit toutes les 30 secondes.

> ✅ Le volume `./2fauth` contient la base SQLite et les fichiers de l'app. C'est tout ce qu'il faut sauvegarder pour restaurer une instance 2FAuth Docker complète ailleurs, à condition de garder la même `APP_KEY`.

Si tu changes un jour la clé, ne la perds jamais sans migration : utilise la variable `APP_PREVIOUS_KEYS` pour lister les anciennes clés et laisser 2FAuth rechiffrer les secrets avec la nouvelle, sinon tous les comptes stockés deviennent illisibles.

## Migrer tes comptes vers 2FAuth Docker

La bascule depuis Google Authenticator, Aegis ou une autre app TOTP mobile se fait compte par compte, puisque la plupart des apps ne permettent pas un export groupé exploitable directement.

Deux méthodes marchent pour chaque compte :

1. **Depuis le service d'origine** : la plupart des sites affichent à nouveau le QR code d'inscription à la 2FA si tu demandes une réinitialisation de ta double authentification. Scanne-le directement dans 2FAuth plutôt que dans ton app mobile.
2. **Depuis l'app mobile existante**, si elle propose un export lisible (lien `otpauth://` ou QR code de migration) : certaines apps l'affichent dans leurs réglages de sauvegarde, à copier-coller ou rescanner dans 2FAuth.

Fais-le service par service, pas en masse : tu valides à chaque fois que le nouveau code généré par 2FAuth correspond bien à celui attendu, avant de supprimer l'ancienne entrée de ton app mobile. Garde ton ancienne app installée tant que la migration complète n'est pas vérifiée. Perdre l'accès à un compte parce que la migration a raté sur un seul service, ça arrive, et c'est évitable avec cette prudence.

Une fois tout basculé, pense à désinscrire 2FAuth des deux rôles qu'il ne doit pas jouer : coffre-fort de mots de passe (ça reste le travail de Vaultwarden ou équivalent) et unique copie de tes secrets (exporte régulièrement la base).

## Sécuriser l'accès à 2FAuth Docker

Un gestionnaire de 2FA mal protégé, c'est la pire cible possible pour un attaquant : il donne accès au second facteur de tous tes comptes d'un coup. Trois réflexes avant de considérer le déploiement terminé.

**Mets un reverse proxy HTTPS devant, pas de port exposé en clair.** Si tu as déjà [Traefik v3](/traefik-reverse-proxy-docker/) sur ton homelab, un simple label suffit pour router `2fa.mondomaine.fr` vers le conteneur avec un certificat Let's Encrypt automatique. Le port 8000 ne doit jamais sortir directement sur Internet.

**Ajoute une couche d'authentification en amont si tu exposes l'instance.** 2FAuth supporte un mode proxy d'authentification, pensé pour recevoir l'identité d'un utilisateur déjà validé par un fournisseur SSO en amont. Si tu as [Pocket-ID](/pocket-id-docker-sso-leger/) déployé pour centraliser tes connexions OpenID Connect, c'est le genre de brique qui s'intègre naturellement devant 2FAuth Docker, en plus du mot de passe propre à l'application.

**Scanne l'image avant chaque mise à jour.** [Trivy](/trivy-docker-scanner-vulnerabilites/) te donne en une commande la liste des CVE connues dans l'image `2fauth/2fauth`, utile sur un outil qui manipule des secrets aussi sensibles. Et si tu veux un état des lieux plus large de la sécurité du serveur qui héberge le conteneur, [Lynis](/lynis-docker-audit-securite-linux/) complète bien l'audit côté système.

> ⚠️ Ne mets jamais 2FAuth Docker et son reverse proxy sur un réseau Docker accessible par des conteneurs que tu ne maîtrises pas. Isole-le dans son propre réseau, avec seulement le reverse proxy en face.

## Dépannage de 2FAuth Docker

**Le conteneur redémarre en boucle.** Regarde les logs en premier :

```bash
docker logs 2fauth
```

La cause la plus fréquente est une `APP_KEY` absente ou mal formée. Elle doit correspondre exactement au format attendu par Laravel, généré par la commande `artisan key:generate`, jamais tapée à la main.

**Les comptes existants deviennent illisibles après une mise à jour.** Tu as changé `APP_KEY` sans passer par `APP_PREVIOUS_KEYS`. Si tu as encore l'ancienne valeur, remets-la temporairement dans `APP_PREVIOUS_KEYS`, redémarre, laisse 2FAuth rechiffrer, puis retire-la.

**Erreur de permissions sur le volume.** Le conteneur tourne avec un utilisateur non-root. Vérifie les droits du dossier monté :

```bash
sudo chown -R 1000:1000 ./2fauth
```

**Les codes générés ne correspondent jamais à ceux attendus par le service.** Vérifie la synchronisation horaire de l'hôte : le TOTP dépend d'une horloge juste à quelques secondes près.

```bash
timedatectl status
```

Un décalage NTP, même petit, suffit à désynchroniser tous les codes générés par 2FAuth Docker.

## Conclusion

2FAuth Docker déplace ton second facteur d'un téléphone fragile vers une instance que tu contrôles, sauvegardes et restaures comme n'importe quel autre service auto-hébergé. La migration prend une soirée, service par service, et une fois en place tu n'as plus jamais à rouvrir un ticket de support parce que tu as changé de smartphone.

Bon, on va pas se mentir : un outil qui concentre tous tes seconds facteurs mérite la même rigueur que ton gestionnaire de mots de passe. Reverse proxy HTTPS, sauvegarde de la base et de l'`APP_KEY` ailleurs que sur le serveur lui-même, et une vraie authentification en amont si tu l'exposes. Avec ça, 2FAuth Docker devient un des services les plus tranquilles de ton homelab, pas le plus fragile.
