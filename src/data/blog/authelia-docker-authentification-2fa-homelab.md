---
title: "Authelia Docker : authentification double facteur centralisée pour ton homelab"
description: "Authelia Docker : mets en place l'authentification 2FA centralisée pour tous tes services homelab. Guide complet Docker Compose, TOTP et SSO."
pubDatetime: 2026-09-07 08:00:00+00:00
modDatetime: "2026-09-07T08:00:00.000Z"
author: Brandon
tags:
  - intermediaire
  - securite
  - docker
  - auto-hebergement
  - hardening
featured: false
draft: false
focusKeyword: authelia docker
---
> 💡 **TL;DR**
> - Authelia Docker centralise l'authentification de tous tes services derrière un portail SSO avec 2FA TOTP
> - Un fichier `docker-compose.yml`, un `configuration.yml` et Nginx Proxy Manager : c'est tout ce qu'il faut
> - Chaque service exposé hérite de la 2FA sans modifier son code, Authelia fait le filtre en amont

## Pourquoi Authelia pour ton homelab ?

Tu as une dizaine de services auto-hébergés. Jellyfin, Gitea, Nextcloud, un tableau de bord, un gestionnaire de mots de passe. Certains ont une authentification intégrée, d'autres non. Nginx Proxy Manager te donne une auth basique par service, mais c'est un mot de passe séparé pour chaque, sans 2FA digne de ce nom.

Authelia Docker change ça. Un portail d'authentification unique devant tous tes services, avec la double authentification TOTP (Time-based One-Time Password) intégrée. Tu te connectes une fois, tu rentres le code de ton app d'authentification, et tu accèdes à tous les services autorisés sans retaper tes identifiants partout.

C'est du SSO (Single Sign-On) pour homelab. Pas besoin d'un compte Azure AD ou d'un Keycloak surdimensionné avec son cluster dédié.

Spoiler : si tu combines ça avec [Fail2Ban Docker](/fail2ban-docker-securite-serveur/) pour bloquer les tentatives de brute-force, ton setup devient sérieusement robuste face aux bots de scan.

## Table des matières

## Ce que fait Authelia exactement

Authelia s'intercale entre ton reverse proxy et tes services. Quand quelqu'un accède à `app.mondomaine.fr`, le reverse proxy interroge Authelia pour savoir si la session est valide. Si non, redirection vers la page de login Authelia. Si oui, accès accordé.

L'architecture tient en trois composants :

- **Authelia** : le serveur d'authentification, écoute sur le port 9091
- **Redis** : stockage de sessions (persistance des sessions entre redémarrages)
- **Le reverse proxy** : Nginx Proxy Manager ou Traefik, qui envoie les requêtes d'autorisation à Authelia avant de les laisser passer

Authelia supporte plusieurs méthodes de second facteur : TOTP (compatible Google Authenticator, Aegis, 2FAS), WebAuthn (YubiKey, passkeys hardware) et push notifications via Duo Security. Pour un homelab, TOTP suffit largement et ne dépend d'aucun service tiers.

Côté gestion des utilisateurs, deux options : un fichier YAML plat ou un annuaire LDAP. On va utiliser le fichier plat ici. LDAP, c'est quand tu as déjà un Active Directory ou un OpenLDAP dans ton infra.

Ce qui est pratique : Authelia ne touche pas aux services protégés. Jellyfin reste Jellyfin, Gitea reste Gitea. Le filtre se passe entièrement au niveau du reverse proxy. Tu peux activer ou désactiver la protection d'un service en deux clics dans NPM, sans redémarrer quoi que ce soit.

## Prérequis

Avant de commencer, vérifie que tu as :

- Docker et Docker Compose v2 sur ton serveur Linux
- Nginx Proxy Manager configuré et fonctionnel avec tes domaines
- Un sous-domaine dédié pour Authelia (`auth.mondomaine.fr` par exemple) pointant sur ton serveur
- Les ports 80 et 443 accessibles depuis l'extérieur via NPM
- Un réseau Docker partagé entre NPM et tes services (si ce n'est pas le cas, on le crée)

Côté pare-feu, si tu gères tes règles avec UFW et Docker coexistent dans ton setup, le guide [UFW Docker](/ufw-docker-pare-feu-linux/) te montre comment configurer le pare-feu sans que Docker court-circuite tes règles iptables.

Un serveur SMTP est optionnel pour démarrer. Sans SMTP, Authelia écrit les emails de réinitialisation de mot de passe et d'inscription TOTP dans un fichier texte que tu lis en SSH. Suffisant pour les premiers tests.

## Architecture : Authelia avec Nginx Proxy Manager

Le flux d'une requête protégée ressemble à ça :

```
Navigateur → NPM (443) → auth_request vers Authelia (9091)
                │
                ├── Authelia répond 200 → NPM laisse passer vers le service
                └── Authelia répond 401 → NPM redirige vers auth.mondomaine.fr
```

NPM joue le rôle de "forward auth proxy". Pour chaque proxy host à protéger, on ajoute un bloc Nginx `auth_request` qui délègue la décision à Authelia. Si la session est valide, le service est atteint. Sinon, l'utilisateur atterrit sur le portail de login.

Ce mécanisme est non intrusif : les services ne savent pas qu'Authelia existe. C'est entièrement géré par le reverse proxy.

## Docker Compose : déployer Authelia

Crée un dossier `authelia` avec cette structure :

```
authelia/
├── docker-compose.yml
├── config/
│   ├── configuration.yml
│   └── users_database.yml
```

Le `docker-compose.yml` :

```yaml
services:
  authelia:
    image: authelia/authelia:latest
    container_name: authelia
    restart: unless-stopped
    volumes:
      - ./config:/config
    environment:
      - TZ=Europe/Paris
    networks:
      - proxy

  redis:
    image: redis:alpine
    container_name: authelia_redis
    restart: unless-stopped
    volumes:
      - ./redis_data:/data
    networks:
      - proxy

networks:
  proxy:
    external: true
```

On suppose un réseau Docker `proxy` partagé avec NPM. Si ton réseau s'appelle différemment, adapte. Pour le créer :

```bash
docker network create proxy
```

> ⚠️ N'expose jamais le port 9091 d'Authelia directement sur l'hôte. Il doit rester interne, accessible uniquement depuis le réseau Docker, via NPM.

## Configurer Authelia : le fichier `configuration.yml`

C'est là que tout se joue. Voici un fichier minimal fonctionnel pour démarrer :

```yaml
server:
  host: 0.0.0.0
  port: 9091

log:
  level: info

jwt_secret: "REMPLACE_MOI_32_CHARS_MINIMUM"

default_redirection_url: "https://auth.mondomaine.fr"

authentication_backend:
  file:
    path: /config/users_database.yml
    password:
      algorithm: bcrypt

session:
  name: authelia_session
  secret: "REMPLACE_MOI_AUTRE_SECRET"
  expiration: 1h
  inactivity: 5m
  domain: mondomaine.fr
  redis:
    host: authelia_redis
    port: 6379

regulation:
  max_retries: 3
  find_time: 2m
  ban_time: 5m

storage:
  local:
    path: /config/db.sqlite3

notifier:
  filesystem:
    filename: /config/notification.txt

access_control:
  default_policy: deny
  rules:
    - domain: "auth.mondomaine.fr"
      policy: bypass
    - domain: "*.mondomaine.fr"
      policy: two_factor
```

Quelques explications sur les points clés :

**`jwt_secret` et `session.secret`** : génère des valeurs aléatoires solides. La commande `openssl rand -hex 32` te donne 64 caractères hexadécimaux, c'est parfait. Ne réutilise pas la même valeur pour les deux champs.

**`access_control`** : la politique `default_policy: deny` bloque tout ce qui n'est pas explicitement listé. La règle `bypass` sur `auth.mondomaine.fr` est indispensable : sans elle, Authelia essaie de s'authentifier elle-même pour accéder à son propre portail, ce qui crée une boucle de redirection infinie. `two_factor` exige mot de passe plus TOTP. `one_factor` n'exige que le mot de passe. `bypass` laisse passer sans aucune auth (utile pour les APIs internes ou les webhooks).

**`regulation`** : Authelia bloque un compte après 3 tentatives ratées sur 2 minutes. C'est complémentaire à [CrowdSec Docker](/crowdsec-docker-securite-collaborative/) si tu l'as déjà déployé pour la détection comportementale au niveau réseau.

**`storage.local`** : SQLite pour stocker les clés TOTP et les sessions. Parfait pour un homelab avec un seul nœud. Si tu passes sur plusieurs serveurs, bascule sur PostgreSQL.

**`notifier.filesystem`** : pour démarrer sans configurer un serveur SMTP, Authelia écrit les emails dans `/config/notification.txt`. Tu récupères les liens d'inscription TOTP en lisant ce fichier via SSH.

## Créer les utilisateurs

Le fichier `config/users_database.yml` :

```yaml
users:
  brandon:
    displayname: "Brandon"
    password: "$2b$12$HASH_BCRYPT_ICI"
    email: "brandon@mondomaine.fr"
    groups:
      - admins
      - users
```

Génère le hash bcrypt de ton mot de passe avec :

```bash
docker run authelia/authelia:latest authelia crypto hash generate bcrypt --password "TON_MOT_DE_PASSE"
```

Copie la valeur `Digest:` dans le champ `password`. Ne mets jamais le mot de passe en clair dans ce fichier, Authelia refuse de démarrer si le hash n'est pas valide.

## Intégrer Authelia dans Nginx Proxy Manager

### Proxy host pour Authelia

Dans NPM, crée un proxy host pour `auth.mondomaine.fr` qui pointe vers `authelia:9091`. Active SSL Let's Encrypt. C'est le seul endpoint d'Authelia exposé sur l'extérieur, tout le reste reste interne.

### Protéger un service

Pour chaque service à protéger, ouvre son proxy host dans NPM, onglet **Advanced**, et colle ce bloc :

```nginx
location /authelia {
    internal;
    set $upstream_authelia http://authelia:9091;
    proxy_pass_request_body off;
    proxy_pass $upstream_authelia/api/verify;
    proxy_set_header Content-Length "";
    proxy_set_header X-Original-URL $scheme://$http_host$request_uri;
    proxy_set_header X-Original-Method $request_method;
    proxy_set_header X-Forwarded-For $remote_addr;
    proxy_set_header X-Forwarded-Host $http_host;
    proxy_set_header X-Forwarded-Proto $scheme;
}

auth_request /authelia;
auth_request_set $target_url $scheme://$http_host$request_uri;
auth_request_set $user $upstream_http_remote_user;
auth_request_set $groups $upstream_http_remote_groups;
error_page 401 =302 https://auth.mondomaine.fr/?rd=$target_url;
```

Ce bloc est identique pour tous tes services. Copie-colle tel quel, en adaptant uniquement l'URL `auth.mondomaine.fr` à ton domaine.

## Enregistrer la 2FA TOTP

Lors du premier login sur un service protégé, Authelia te redirige sur son portail. Tu saisis ton mot de passe, et Authelia t'invite ensuite à configurer la double authentification.

Le processus :

1. Authelia envoie un lien d'inscription par email (ou l'écrit dans `notification.txt` si pas de SMTP)
2. Tu ouvres ce lien depuis ton navigateur
3. Tu scanes le QR code avec ton app TOTP (Aegis sur Android, 2FAS, ou Authenticator sur iOS)
4. Tu valides avec le premier code généré pour confirmer la synchronisation
5. La clé TOTP est stockée chiffrée dans la base SQLite

À partir de là, chaque connexion demande ton mot de passe puis le code à 6 chiffres. La session dure 1 heure par défaut, paramétrable dans `session.expiration`.

Bon conseil : si tu utilises [Vaultwarden](/vaultwarden-docker-gestionnaire-mots-de-passe/) pour gérer tes mots de passe, ajoute aussi les codes TOTP de secours dans un coffre-fort dédié. Perd ton téléphone, perd l'accès à tous tes services si tu n'as aucun backup.

## Dépannage

**Le portail ne s'affiche pas.** Vérifie que le conteneur tourne et qu'il n'y a pas d'erreur de config YAML :

```bash
docker logs authelia
```

La cause la plus fréquente est une indentation incorrecte dans `configuration.yml`. YAML est pointilleux sur les espaces. Valide rapidement avec :

```bash
python3 -c "import yaml; yaml.safe_load(open('config/configuration.yml'))" && echo "OK"
```

**NPM renvoie un 500 ou un 502 sur le bloc auth.** Authelia et NPM ne sont pas sur le même réseau Docker. Vérifie que les deux containers partagent bien le réseau `proxy` avec `docker inspect authelia | grep -A 10 Networks`.

**Boucle de redirection infinie sur le portail de login.** La règle `bypass` pour `auth.mondomaine.fr` est absente dans `access_control`. Sans elle, Authelia demande une authentification pour afficher sa propre page de login.

**Le code TOTP est toujours refusé.** Problème de dérive d'horloge. Authelia tolère une différence d'environ 30 secondes entre le serveur et le client. Vérifie la synchronisation NTP de ton hôte :

```bash
timedatectl status
```

Si tu veux gérer la synchronisation horaire de tout ton homelab de façon centralisée, j'ai un guide sur Chrony en Docker qui couvre ça proprement.

**Session perdue à chaque redémarrage Redis.** Le volume `./redis_data` n'est pas monté correctement. Vérifie avec `docker inspect authelia_redis | grep Mounts`. Sans volume persistant, Redis perd toutes les sessions en mémoire à l'arrêt.

> ⚠️ Garde toujours une session SSH active sur ton serveur pendant la configuration initiale. Si tu te bloques dehors, tu dois accéder directement aux fichiers de config pour désactiver la protection temporairement.

## Conclusion

Authelia Docker te donne un portail 2FA pour tout ton homelab en une après-midi de configuration. Un seul login, un seul code TOTP, accès à tous tes services protégés. Tes Jellyfin, Gitea et tableaux de bord ne sont plus accessibles en clair depuis l'extérieur.

La vraie question c'est : combien de services tu as laissé traîner exposés sans authentification correcte depuis des mois ? Avec Authelia, ajouter la protection sur un nouveau service prend deux minutes dans NPM.

Pour consolider encore la sécurité de ton homelab, combine Authelia avec [CrowdSec Docker](/crowdsec-docker-securite-collaborative/) pour la détection comportementale au niveau réseau et [UFW Docker](/ufw-docker-pare-feu-linux/) pour cloisonner ce qui n'a pas besoin d'être exposé.
