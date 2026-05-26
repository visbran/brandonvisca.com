---
title: "Nginx Proxy Manager : reverse proxy en 5 min avec Docker"
description: "Nginx Proxy Manager Docker : reverse proxy en quelques clics, SSL Let's Encrypt auto, auth basique et bonnes pratiques homelab."
pubDatetime: "2026-05-26T06:00:00Z"
modDatetime: "2026-05-26T00:00:00+01:00"
author: Brandon Visca
tags:
  - intermediaire
  - docker
  - reverse-proxy
  - ssl
  - nginx
  - auto-hebergement
featured: false
draft: false
focusKeyword: nginx proxy manager docker
---
> 💡 **TL;DR** — Nginx Proxy Manager avec Docker :
> - SSL Let's Encrypt auto en quelques clics, renouvellement transparent tous les 90 jours
> - Reverse proxy multi-services depuis une interface web, zéro fichier conf à éditer
> - Auth HTTP et restrictions IP intégrées nativement, sans plugin externe

## Table des matières

## Pourquoi Nginx Proxy Manager ?

Si tu auto-héberges plusieurs services (Nextcloud, Plex, Grafana, vaultwarden…), tu finis vite à gérer des dizaines de ports, des certificats SSL qui expirent et des fichiers de conf Nginx imbitables. 😵‍💫

**Nginx Proxy Manager** (NPM) résout tout ça via une interface web claire. Tu crée un point d'entrée unique, tu rediriges les domaines vers les bons conteneurs, et les certificats Let's Encrypt se renouvellent tout seuls. Pas besoin de toucher au terminal à chaque nouveau service.

- Image Docker officielle : `jc21/nginx-proxy-manager:latest`
- Repo GitHub : [NginxProxyManager/nginx-proxy-manager](https://github.com/NginxProxyManager/nginx-proxy-manager), 247M+ pulls, dernière version v2.14.0 (février 2026)
- Licence MIT, gratuit et actif

## Prérequis

- Un serveur Linux avec [Docker + Docker Compose v2](/docker-debutant-services-auto-heberger/) installés
- Un domaine (ou sous-domaine) pointant vers ton serveur
- Les ports 80 et 443 ouverts sur ton firewall / routeur
- Une session SSH en root ou avec `sudo`

## Installation avec Docker Compose

Crée le dossier et le fichier :

```bash
mkdir -p ~/npm && cd ~/npm
```

<aside class="notion-callout notion-blue-callout">
💡 Mon dossier racine des projets Docker est `~/npm`. Si tu préfères un autre chemin, adapte le volume.
</aside>

Copie ce `docker-compose.yml` :

```yaml
services:
  npm:
    image: jc21/nginx-proxy-manager:latest
    container_name: npm
    restart: unless-stopped
    ports:
      - "80:80"
      - "81:81"
      - "443:443"
    volumes:
      - ./data:/data
      - ./letsencrypt:/etc/letsencrypt
    environment:
      - TZ=Europe/Paris
      # Les identifiants par défaut, change-les au premier login
      - INITIAL_ADMIN_EMAIL=admin@example.com
      - INITIAL_ADMIN_PASSWORD=changeme
```

Lance le conteneur :

```bash
docker compose up -d
```

Premier accès : http://`TON_IP`:81 (ou `http://npm.tondomaine.fr:81` si tu as déjà configuré le DNS).

> Identifiants par défaut :
> - **Email** : `admin@example.com`
> - **Password** : `changeme`

⚠️ **Change immédiatement le mot de passe** dans Settings → Users.

## Configuration du reverse proxy

### 1. Créer un proxy host

Va dans l'onglet **Hosts → Proxy Hosts → Add Proxy Host**.

| Champ | Valeur |
|---|---|
| Domain Names | `monapp.tondomaine.fr` |
| Scheme | `http` |
| Forward Hostname / IP | `172.17.0.1` (IP de la passerelle Docker) |
| Forward Port | `8080` (port interne du service) |

💡 Si ton service est un autre conteneur Docker sur le même réseau `bridge` par défaut, utilise `172.17.0.1`. Sur un réseau Docker custom, utilise le nom du conteneur (ex: `nextcloud`) et le port exposé par celui-ci.

### 2. SSL Let's Encrypt automatique

Dans la même fenêtre, onglet **SSL** :

1. Coche **Request a new SSL Certificate**
2. Coche **Force SSL** (redirection automatique http → https)
3. Coche **HSTS Enabled**
4. Coche **I Agree to the Let's Encrypt Terms of Service**
5. **Email Address for Let's Encrypt** : ton email
6. Clique **Save**

Le certificat est généré et le renouvellement se fait tout seul tous les 90 jours. Tu n'as plus à y penser.

### 3. Redirection www ↔ non-www

Onglet **Advanced** du proxy host, ajoute dans la zone **Custom Nginx Configuration** :

```nginx
if ($host = www.tondomaine.fr) {
    return 301 https://tondomaine.fr$request_uri;
}
```

Ou l'inverse si tu préfères le www. Ça évite le duplicate content SEO.

## Authentification basique (Basic Auth)

NPM intègre une auth HTTP native sans plugin externe.

1. Va dans **Access Lists → Add Access List**
2. Nom : `internal-access`
3. Satisfy Any : ❌
4. **Authorization**: clique **Add**, rentre un user/password
5. Sauvegarde

Puis dans ton proxy host → onglet **Access** → **Access List** → sélectionne `internal-access`.

Tu peux aussi ajouter des restrictions IP (whitelist) dans la même access list.

## Bonnes pratiques et astuces

- **Passe NPM sur un réseau Docker dédié** (`docker network create npm`) pour pouvoir référencer les conteneurs par leur hostname interne
- **Bloque le port 81 sur l'extérieur** via ton firewall si tu n'y accèdes que via un tunnel SSH ou VPN
- **Sauvegarde les volumes** `./data` et `./letsencrypt` avec [restic](https://restic.net/) ou [duplicacy](https://duplicacy.com/)
- **Active le logs forwarding** vers une stack ELK/Graylog si tu surveilles les accès

Pour le durcissement HTTPS, complète avec les [headers HTTP sécurisés Nginx](/securiser-nginx-avec-headers-http/) — HSTS étendu, X-Frame-Options, CSP.

## Troubleshooting

### Certificat Let's Encrypt qui échoue

- Vérifie que le DNS pointe bien sur ton IP publique : `dig monapp.tondomaine.fr`
- Vérifie que les ports 80 et 443 sont ouverts : `nc -zv tondomaine.fr 80`
- Let's Encrypt a une limite de 5 certificats identiques par semaine. Attends un peu si tu as trop forçé.

### Erreur 502 Bad Gateway

- Le service cible écoute-t-il bien sur le bon port ? `docker ps` pour vérifier
- Si le conteneur cible est sur un réseau Docker custom, NPM doit être sur le même réseau
- Le firewall du serveur bloque-t-il le port interne ? `ss -tlnp | grep 8080`

### Impossible de joindre l'interface d'admin

- Vérifie que le conteneur tourne : `docker logs npm`
- Le port 81 est-il libre sur le host ? `ss -tlnp | grep 81`
- Si tu as un autre service sur le port 81, modifie la binding du port dans le `docker-compose.yml` : `"8081:81"`

### Le certificat n'a pas renouvelé

- Dans NPM, va dans **SSL Certificates → Renew Now** manuellement pour tester
- Vérifie que le conteneur est bien accessible depuis l'extérieur sur le port 80 (c'est là que Let's Encrypt ping)

## Conclusion

Nginx Proxy Manager transforme la gestion d'un reverse proxy en une opération de quelques clics. Tu gagnes du temps, tu limites les erreurs de conf manuelle, et tes certificats SSL se gèrent sans intervention. Parfait pour un homelab qui grossit.

Si tu cherches une alternative sans interface web, regarde [Traefik avec Docker](/traefik-reverse-proxy-docker/) — configuration déclarative, intégration native avec les labels Docker.

---

> 🛡️ **Stack testée** : Debian 12, Docker 28.x, Docker Compose v2, Nginx Proxy Manager v2.14.0

## Pour aller plus loin

- [Traefik avec Docker : reverse proxy déclaratif](/traefik-reverse-proxy-docker/)
- [Sécuriser Nginx avec les headers HTTP](/securiser-nginx-avec-headers-http/)
- [CSP Nginx sans casser son site](/content-security-policy-nginx-sans-casser-site/)
