---
title: "Certimate Docker : renouvellement auto des certificats SSL"
description: "Déploie Certimate Docker pour gérer et renouveler automatiquement tes certificats SSL Let's Encrypt. Guide complet avec Docker Compose."
pubDatetime: "2026-08-09T08:00:00.000Z"
modDatetime: "2026-08-09T08:00:00.000Z"
author: Brandon Visca
tags:
  - docker
  - securite
  - certificat-ssl
  - letsencrypt
  - auto-hebergement
  - intermediaire
featured: false
draft: false
focusKeyword: certimate docker
faqs:
  - question: "Certimate remplace-t-il un reverse proxy comme Caddy ou Traefik ?"
    answer: "Non. Certimate génère et renouvelle les certificats SSL, mais il ne route pas le trafic. Il complète un reverse proxy en fournissant les certificats que celui-ci utilise."
  - question: "Puis-je utiliser Certimate avec Nginx Proxy Manager ?"
    answer: "Oui. Tu génères le certificat dans Certimate, puis tu l'exportes au format PEM pour l'importer manuellement dans Nginx Proxy Manager. C'est moins automatique que Caddy, mais ça fonctionne."
  - question: "Quelle est la différence entre le challenge HTTP-01 et DNS-01 ?"
    answer: "HTTP-01 valide que tu contrôles le domaine via un fichier accessible sur le port 80. DNS-01 crée un enregistrement TXT dans la zone DNS, ce qui permet de générer des certificats wildcard et de fonctionner derrière un firewall."
  - question: "Où sont stockés les certificats générés par Certimate ?"
    answer: "Dans le volume Docker de Certimate, par défaut sous /app/data. Tu dois monter ce volume en persistance pour ne pas perdre tes certificats lors d'un redémarrage du conteneur."
ogImage: "" 
---
> 💡 **TL;DR**
> - Certimate est un gestionnaire de certificats SSL ACME auto-hébergé qui renouvelle automatiquement tes certificats Let's Encrypt
> - Contrairement à Caddy ou Traefik, Certimate ne fait pas reverse proxy : il génère les certificats que tu réutilises où tu veux
> - Stack Docker Compose prête, configuration via interface web, support HTTP-01 et DNS-01 avec des dizaines de providers

## Table des matières

## Pourquoi Certimate quand on a déjà Caddy ?

Tu connais sûrement [Caddy](/caddy-docker-reverse-proxy-guide/), ce serveur web en Go qui gère le HTTPS tout seul. Ou peut-être [Nginx Proxy Manager](/nginx-proxy-manager-docker-guide/) avec son interface graphique cliquable. Ou Traefik avec ses labels Docker. Tous ces outils génèrent et renouvellent des certificats SSL. Alors pourquoi ajouter Certimate dans la stack ?

La réponse est simple : **Certimate découple la gestion des certificats du routage du trafic.** Caddy, Traefik et Nginx Proxy Manager font les deux à la fois. Certimate ne fait qu'une chose, mais il la fait bien : il obtient, stocke et renouvelle tes certificats SSL via le protocole ACME (Let's Encrypt, Buypass, ZeroSSL, etc.). Ensuite, tu réutilises ces certificats où tu veux : dans un reverse proxy manuel, sur un NAS, sur un équipement réseau, ou même pour des services qui n'ont aucune gestion ACME intégrée.

Certimate est écrit en Go, open-source, sous licence MIT. Il expose une interface web propre et unifiée pour gérer plusieurs providers ACME, plusieurs domaines, et plusieurs méthodes de validation (HTTP-01, DNS-01, ALPN-01). Le projet est activement maintenu, avec un support étendu pour les providers DNS cloud (Cloudflare, DigitalOcean, OVH, Gandi, etc.). C'est l'outil idéal quand tu veux centraliser la gestion de tes certificats sans être prisonnier d'un reverse proxy particulier.

Ce qui m'a convaincu de passer à Certimate Docker : la possibilité de générer un certificat wildcard (`*.mon-domaine.fr`) via DNS-01 avec Cloudflare, et de l'exporter pour l'utiliser sur un équipement qui ne sait pas parler ACME. Caddy et Traefik ne te donnent pas ce contrôle aussi facilement.

## Certimate vs les alternatives : tableau de bord

| Outil | Reverse proxy | Gestion ACME | Interface web | Export certificats | Docker |
|-------|---------------|--------------|---------------|-------------------|--------|
| **Certimate** | Non | Oui (multi-providers) | Oui, dédiée | Oui (PEM, PFX) | `certimate/certimate` |
| **Caddy** | Oui | Oui (intégré) | Non (config fichier) | Limité | `caddy` |
| **Traefik** | Oui | Oui (intégré) | Tableau de bord limité | Limité | `traefik` |
| **Nginx Proxy Manager** | Oui | Oui (intégré) | Oui complète | Manuel | `jc21/nginx-proxy-manager` |
| **Certbot** | Non | Oui (CLI uniquement) | Non | Oui | `certbot/certbot` |

Mon verdict : **Certimate** si tu veux une interface web dédiée à la gestion des certificats, sans lien avec le routage. **Caddy** si tu veux le setup le plus simple (un seul outil fait tout). **Nginx Proxy Manager** si tu préfères cliquer pour configurer tes reverse proxies. **Certbot** si tu aimes les scripts et que tu n'as pas besoin d'interface.

## Architecture et prérequis

Certimate fonctionne en trois couches :

1. **L'interface web** : tu configures tes domaines, providers ACME et méthodes de validation via un dashboard responsive.
2. **Le moteur ACME** : il dialogue avec Let's Encrypt (ou autre) pour obtenir et renouveler les certificats.
3. **Le stockage** : SQLite par défaut, avec les certificats et clés privées chiffrées au repos.

**Prérequis :**
- Un serveur Linux avec Docker et Docker Compose
- Un nom de domaine pointant vers ton serveur (pour HTTP-01) ou un accès à la zone DNS (pour DNS-01)
- Les ports 80 et 443 disponibles si tu utilises HTTP-01, ou un provider DNS supporté pour DNS-01
- Un accès sortant HTTPS vers les serveurs ACME (Let's Encrypt, etc.)

Si tu es derrière un CGNAT ou que tu ne peux pas ouvrir le port 80, le challenge DNS-01 est ton ami. Et si tu cherches une solution pour exposer ton homelab sans IP publique, [Cloudflare Tunnel](/cloudflare-tunnel-docker-homelab/) reste une excellente alternative.

## Installation avec Docker Compose

Crée un dossier dédié et le fichier `docker-compose.yml` :

```yaml
services:
  certimate:
    image: certimate/certimate:latest
    container_name: certimate
    restart: unless-stopped
    ports:
      - "8080:8080"
    environment:
      - TZ=Europe/Paris
    volumes:
      - ./data:/app/data
```

Puis lance le conteneur :

```bash
docker compose up -d
```

Certimate démarre sur le port 8080. Ouvre ton navigateur sur `http://IP_DU_SERVEUR:8080` et crée un compte administrateur lors du premier lancement. L'interface est en anglais mais reste très intuitive.

**Note importante sur le stockage :** Le volume `./data:/app/data` est obligatoire. Sans ça, tes certificats et ta base de données disparaissent à chaque redémarrage du conteneur. Ce dossier contient à la fois la base SQLite et les clés privées. Protège-le comme il se doit : `chmod 700 ./data` sur l'hôte.

## Configuration pas à pas de Certimate Docker

### Étape 1 : Ajouter un provider ACME

Va dans **Settings > ACME Providers** et ajoute Let's Encrypt (staging ou production). Le staging te permet de tester sans te faire rate-limiter. Passe en production quand tout est ok.

Tu peux aussi ajouter ZeroSSL ou Buypass si tu veux diversifier tes sources de certificats. La plupart des providers ACME publics sont gratuits pour un usage personnel. Let's Encrypt reste le plus fiable et le plus utilisé, avec un support quasi universel chez les clients ACME.

### Étape 2 : Configurer un provider DNS

Pour le challenge DNS-01, Certimate supporte des dizaines de providers : Cloudflare, DigitalOcean, DuckDNS, Gandi, GoDaddy, OVH, Porkbun, Namecheap, Hetzner, Linode, et bien d'autres. Va dans **Settings > DNS Providers**, choisis ton provider, et renseigne ton token API.

Avec Cloudflare, tu as besoin d'un **Global API Key** ou d'un **API Token** avec les droits `Zone:Edit` sur la zone concernée. C'est la méthode la plus fiable pour générer des certificats wildcard. Voici un exemple de configuration avec Cloudflare :

- **Provider** : Cloudflare
- **API Token** : ton token Cloudflare avec droits `Zone:Read` et `DNS:Edit`
- **Zone** : le nom de domaine racine (ex: `mon-domaine.fr`)

Certimate va automatiquement créer l'enregistrement TXT `_acme-challenge.mon-domaine.fr` avec la valeur requise par Let's Encrypt, attendre la propagation DNS, puis lancer la validation.

### Étape 3 : Créer un certificat

Va dans **Certificates > Add Certificate** :

1. **Domaine** : entre ton domaine, par exemple `mon-service.mon-domaine.fr` ou `*.mon-domaine.fr` pour un wildcard
2. **Provider ACME** : sélectionne Let's Encrypt Production
3. **Challenge type** : choisis HTTP-01 ou DNS-01 selon ta situation
4. **DNS Provider** : sélectionne ton provider configuré à l'étape 2 (uniquement pour DNS-01)
5. **Auto-renewal** : laisse activé (c'est le cœur du produit)

Clique sur **Save** puis **Request Certificate**.

Certimate va alors dialoguer avec Let's Encrypt, passer le challenge, et stocker le certificat. Tu vois l'état en temps réel dans l'interface. Si ça échoue, les logs du conteneur sont explicites :

```bash
docker logs certimate
```

Les erreurs les plus fréquentes :
- **DNS propagation too slow** : ton provider DNS met trop de temps à propager le TXT. Attends 2-3 minutes et réessaie.
- **Unauthorized** : le token API n'a pas les droits suffisants. Vérifie les permissions sur la zone DNS.
- **Timeout** : Certimate ne peut pas atteindre les serveurs ACME. Vérifie que le pare-feu de sortant autorise le HTTPS vers `acme-v02.api.letsencrypt.org`.

### Étape 4 : Vérifier le renouvellement automatique

Certimate vérifie les certificats quotidiennement et renouvelle automatiquement ceux qui expirent dans moins de 30 jours. Tu n'as rien à configurer. Dans l'interface, chaque certificat affiche sa date d'expiration et son statut de renouvellement.

Tu peux aussi forcer un renouvellement manuel depuis le tableau de bord si tu as besoin d'un certificat frais avant une migration ou un changement de configuration. Le renouvellement est transparent : Certimate remplace l'ancien certificat par le nouveau dans sa base de données sans interruption de service pour les applications qui l'utilisent.

## Utiliser les certificats ailleurs

C'est là que Certimate devient intéressant. Une fois le certificat généré, tu peux l'exporter dans **Certificates > [ton certificat] > Download**.

Tu obtiens trois fichiers :
- `certificate.pem` : le certificat public
- `private.key` : la clé privée
- `ca.pem` : la chaîne de certification intermédiaire

Tu peux les utiliser directement dans n'importe quel reverse proxy ou serveur web :

```nginx
# Exemple Nginx
ssl_certificate /path/to/certificate.pem;
ssl_certificate_key /path/to/private.key;
```

Pour Nginx Proxy Manager, importe le certificat manuellement via l'interface SSL > Custom. Ce n'est pas aussi automatisé que Caddy, mais ça te donne un contrôle total sur la chaîne de certification.

Certimate supporte aussi l'export au format PFX pour les environnements Windows et les équipements réseau qui ne comprennent que ce format. C'est utile si tu veux déployer un certificat sur un pare-feu pfSense, un routeur MikroTik, ou un serveur Windows IIS.

## Intégration avec un reverse proxy Nginx manuel

Si tu préfères garder le contrôle total sur ta configuration Nginx sans passer par un gestionnaire graphique, Certimate + Nginx pur est un combo redoutable. Voici un exemple de configuration complète :

```yaml
# docker-compose.yml
services:
  certimate:
    image: certimate/certimate:latest
    container_name: certimate
    restart: unless-stopped
    ports:
      - "127.0.0.1:8080:8080"
    volumes:
      - ./certimate-data:/app/data
      - ./certs-output:/app/certs

  nginx:
    image: nginx:alpine
    container_name: nginx
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./certs-output:/etc/nginx/certs:ro
```

Dans Certimate, configure un **Deploy Target** qui copie les certificats frais dans `/app/certs` (monté sur `./certs-output`). Nginx lit ensuite ces fichiers et sert le HTTPS. Quand Certimate renouvelle le certificat, il met à jour les fichiers et tu recharges Nginx avec un simple `docker exec nginx nginx -s reload`.

C'est plus verbeux que Caddy, mais tu contrôles chaque détail de la chaîne TLS : les ciphers, les versions de protocole, les headers de sécurité. Si tu veux aller plus loin sur la sécurisation de Nginx, j'ai un guide complet sur les [headers HTTP de sécurité](/securiser-nginx-avec-headers-http/).

## Notifications et monitoring

Certimate intègre des notifications webhook pour te prévenir en cas d'échec de renouvellement. Va dans **Settings > Notifications** et configure un webhook Discord, Slack, ou une URL générique.

Le payload envoyé est un JSON simple avec le statut du certificat, le domaine concerné, et l'erreur éventuelle. C'est minimaliste mais suffisant pour brancher un système d'alerting existant. Un exemple de payload :

```json
{
  "event": "certificate.renewal.failed",
  "domain": "mon-service.mon-domaine.fr",
  "error": "DNS propagation timeout after 120s"
}
```

Pour un monitoring plus complet de ton infrastructure, tu peux coupler ça avec [Uptime Kuma](/uptime-kuma-2-0-monitoring-auto-heberge/) qui surveille la validité SSL de tes endpoints en parallèle. Uptime Kuma te prévient si un certificat expire ou si un service devient indisponible, tandis que Certimate te prévient si le renouvellement lui-même échoue.

## Sécurité et bonnes pratiques

- **Ne jamais exposer Certimate sur Internet** sans reverse proxy et authentification. L'interface d'administration contient tes tokens API DNS et tes clés privées.
- **Utiliser un firewall restrictif** : le port 8080 doit être accessible uniquement depuis ton réseau local ou via un VPN. Si tu as besoin d'y accéder de l'extérieur, passe par un tunnel sécurisé.
- **Sauvegarder le volume `./data`** : c'est là que tout se passe. Un backup quotidien de ce dossier suffit à restaurer l'intégralité de ta gestion de certificats. BorgBackup est parfait pour ça.
- **Privilégier DNS-01** quand c'est possible : il ne nécessite pas d'ouvrir le port 80, et il permet les certificats wildcard.
- **Tester en staging** avant de passer en production : Let's Encrypt rate-limite les erreurs. Fais tes essais sur leurs serveurs de staging pour éviter de te bloquer pendant une heure.
- **Changer le mot de passe par défaut** : Certimate te demande de créer un compte au premier démarrage, mais vérifie que le mot de passe est solide et unique. Stocke-le dans ton gestionnaire de mots de passe.
- **Restreindre les permissions du volume** : le dossier `./data` doit appartenir à l'utilisateur qui exécute le conteneur, avec des permissions en lecture/écriture restreintes (`chmod 700` et `chown` sur l'UID du conteneur).

## Conclusion

Certimate est l'outil qu'il manquait à ton homelab si tu veux centraliser la gestion des certificats SSL sans lier ça à un reverse proxy particulier. Il est léger, rapide, et son interface web est bien pensée. Le support du DNS-01 avec Cloudflare et autres providers en fait un allié redoutable pour les certificats wildcard.

Si tu es déjà sur Caddy ou Traefik, Certimate n'est pas indispensable. Mais si tu gères plusieurs reverse proxies, des équipements réseau, ou des services qui n'ont pas de gestion ACME native, il devient rapidement essentiel. Le renouvellement automatique est fiable, les notifications te tiennent au courant, et l'export des certificats te donne une liberté que les reverse proxy intégrés n'offrent pas. Adopter Certimate dans ton stack Docker, c'est choisir la modularité et le contrôle plutôt que la simplicité noire.
