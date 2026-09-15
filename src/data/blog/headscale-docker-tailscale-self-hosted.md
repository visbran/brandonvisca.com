---
title: "Headscale Docker : serveur Tailscale auto-hébergé (open-source)"
description: "Héberge ton propre control plane Tailscale avec Headscale Docker : Compose complet, comparatif Tailscale et limites à connaître avant de migrer."
pubDatetime: "2026-09-15T11:01:11+02:00"
modDatetime: "2026-09-14T08:00:00.000Z"
author: Brandon
tags:
  - reseau
  - docker
  - tailscale
  - intermediaire
featured: false
draft: false
focusKeyword: headscale docker
faqs:
  - question: "Headscale peut-il remplacer complètement le cloud Tailscale ?"
    answer: "Pour un usage homelab, oui dans la quasi-totalité des cas. Tu gardes MagicDNS, les ACLs, les subnet routes, les exit nodes et Tailscale SSH. Ce qui manque encore, c'est Funnel et Serve, encore en développement côté Headscale."
  - question: "Combien de RAM consomme un serveur Headscale ?"
    answer: "Très peu. C'est un seul binaire Go avec une base SQLite embarquée. Sur un tailnet de quelques dizaines d'appareils, compte une centaine de mégaoctets de RAM et une charge CPU quasi nulle en dehors des pics d'enregistrement."
  - question: "Que se passe-t-il si mon serveur Headscale tombe en panne ?"
    answer: "Les appareils déjà enregistrés gardent leur dernière configuration connue et continuent de communiquer en P2P si possible. Tu perds juste la capacité d'ajouter un appareil ou de modifier les ACLs tant que le serveur n'est pas restauré."
---
> 💡 **TL;DR**
> - Headscale docker auto-héberge le control plane Tailscale, compatible avec les clients officiels sans rien changer côté appareils
> - Compose minimal avec SQLite embarqué, un fichier `config.yaml` et deux ports à exposer
> - Comparatif complet avec le cloud Tailscale, fonctionnalités couvertes et limites actuelles (Funnel, Serve)

## Table des matières

Tu utilises déjà [Tailscale VPN mesh](/tailscale-vpn-mesh-homelab/) pour relier tes appareils sans ouvrir un port. Ça marche bien, mais il y a un détail qui te chatouille : le plan de contrôle, celui qui distribue les clés et connaît la topologie de ton réseau, tourne chez Tailscale Inc, pas chez toi. Pour un usage perso, c'est un compromis raisonnable. Pour un vrai homelab auto-hébergé jusqu'au bout, c'est la seule brique qui reste dans le cloud.

**Headscale docker** comble ce trou. C'est une réimplémentation open-source du serveur de coordination Tailscale, que tu fais tourner toi-même dans un conteneur. Les clients restent les mêmes : tu installes l'appli Tailscale officielle sur ton laptop, ton téléphone ou ton NAS, tu la pointes vers ton serveur Headscale au lieu du cloud public, et le mesh fonctionne à l'identique.

## Pourquoi passer par Headscale Docker plutôt que le cloud Tailscale

La question qui se pose direct : pourquoi se compliquer la vie si le plan gratuit Tailscale fonctionne déjà ?

Trois raisons reviennent chez les gens qui franchissent le pas. D'abord la souveraineté : aucune donnée de topologie, d'identité ou d'ACL ne quitte ton infra. Ensuite les limites du plan gratuit (3 utilisateurs, 100 appareils) qui deviennent un mur pour une asso, une petite structure ou un lab qui grossit vite. Enfin le côté paranoïaque assumé : si Tailscale Inc ferme demain, ton tailnet auto-hébergé continue de tourner sans rien demander à personne.

**Headscale docker** ne remplace pas le client Tailscale, seulement le serveur de coordination. C'est ce qui le rend indolore à adopter : zéro changement sur tes appareils, juste une URL de login différente.

## Headscale, c'est quoi exactement

Le projet est maintenu par Juan Font Alonso et Kristoffer Dalby avec une communauté de contributeurs, sous licence BSD-3-Clause. Le dépôt officiel est clair là-dessus : ce n'est pas un produit Tailscale Inc, même si un des mainteneurs travaille chez Tailscale et contribue avec leur accord. C'est un projet indépendant, gratuit, sans version payante.

Côté fonctionnalités, la parité avec le control plane officiel est déjà large : dual stack IPv4/IPv6, MagicDNS avec split DNS, ACLs et grants, subnet routers, exit nodes, Tailscale SSH, authentification via preauthkeys ou SSO OpenID Connect, et même Taildrop/Taildrive pour le partage de fichiers entre appareils.

Ce qui manque encore au moment où j'écris ces lignes : Funnel (exposition publique d'un service) et Serve sont listés comme en développement côté Headscale, tout comme les logs de flux réseau. Les groupes OIDC dans les politiques ACL ne sont pas non plus supportés. Si Funnel est central dans ton usage, garde un œil sur l'avancement du projet avant de migrer entièrement.

## Prérequis avant de déployer

Avant de lancer ton conteneur **headscale docker**, vérifie que tu as :

- Docker et Docker Compose sur un serveur avec une IP joignable par tes appareils (LAN ou VPS)
- Un nom de domaine ou sous-domaine pointant vers ce serveur, même auto-hébergé via [DuckDNS](/duckdns-docker-ddns-gratuit/) si ton IP publique change régulièrement
- Un reverse proxy devant Headscale pour servir le tout en HTTPS, les clients Tailscale exigeant un `login-server` en TLS valide
- Les binaires clients Tailscale déjà installés sur tes appareils, aucune modification supplémentaire n'est nécessaire

## Le Docker Compose Headscale

Voici le Compose minimal. L'image officielle est publiée sur Docker Hub (`headscale/headscale`) et sur le GitHub Container Registry (`ghcr.io/juanfont/headscale`), les deux pointent vers le même projet.

```yaml
services:
  headscale:
    image: headscale/headscale:latest
    container_name: headscale
    restart: unless-stopped
    command: serve
    ports:
      - "127.0.0.1:8080:8080"
      - "127.0.0.1:9090:9090"
    volumes:
      - ./config:/etc/headscale
      - headscale-data:/var/lib/headscale

volumes:
  headscale-data:
```

Le port 8080 sert l'API que les clients Tailscale contactent, le port 9090 expose les métriques Prometheus. Je les bind sur `127.0.0.1` volontairement : ton reverse proxy (Caddy, Traefik ou Nginx) fait le pont vers l'extérieur en HTTPS, Headscale lui-même ne gère pas TLS.

Le fichier `config/config.yaml` minimal ressemble à ça :

```yaml
server_url: https://headscale.tondomaine.fr
listen_addr: 0.0.0.0:8080
metrics_listen_addr: 0.0.0.0:9090

database:
  type: sqlite
  sqlite:
    path: /var/lib/headscale/db.sqlite

dns:
  magic_dns: true
  base_domain: tondomaine-interne.fr

noise:
  private_key_path: /var/lib/headscale/noise_private.key
```

`server_url` doit correspondre exactement à l'URL publique HTTPS de ton reverse proxy, sinon les clients n'arrivent pas à s'enregistrer. `base_domain` est le suffixe DNS interne de ton tailnet, indépendant de ton domaine public.

Lance le conteneur :

```bash
docker compose up -d
```

## Créer un utilisateur et connecter tes appareils

Une fois le conteneur up, tout se pilote via `docker exec`. D'abord, crée un utilisateur (un namespace logique, pas forcément une vraie personne) :

```bash
docker exec headscale headscale users create brandon
```

Génère ensuite une clé de pré-authentification pour enregistrer un appareil sans passer par un flux OIDC :

```bash
docker exec headscale headscale preauthkeys create --user brandon --expiration 24h --reusable
```

Sur l'appareil client, connecte-toi à ton serveur au lieu du cloud Tailscale :

```bash
sudo tailscale up --login-server https://headscale.tondomaine.fr --authkey tskey-auth-xxxxxxxx
```

Si tu préfères l'authentification interactive plutôt qu'une clé, omets `--authkey` : la commande te donne un lien à valider depuis l'interface web Headscale (activable dans la config).

Pour vérifier que tout le monde est bien connecté, liste les nœuds côté serveur :

```bash
docker exec headscale headscale nodes list
```

## Headscale vs Tailscale : le comparatif

| Critère | Tailscale (cloud) | Headscale Docker |
|---------|---------------------|-------------------|
| Control plane | Hébergé par Tailscale Inc | Auto-hébergé, ton conteneur |
| Coût | Gratuit jusqu'à 3 users / 100 devices | Gratuit et open-source, sans limite artificielle |
| MagicDNS | Oui | Oui |
| ACLs | Oui, JSON dans la console | Oui, fichier de policy local |
| Subnet routes / exit nodes | Oui | Oui |
| Tailscale SSH | Oui | Oui |
| Funnel (exposition publique) | Oui | En développement, absent pour l'instant |
| Interface web officielle | Console complète Tailscale | Basique, projets communautaires en complément |
| Dépendance à un tiers | Oui (plan de contrôle) | Non |
| Support commercial | Oui (plans payants) | Communautaire uniquement |

**Verdict** : si Funnel ou un support commercial sont non négociables pour toi, reste sur le cloud Tailscale. Si tu veux la souveraineté complète sur ton mesh et que tu acceptes de gérer toi-même la disponibilité du serveur, **headscale docker** couvre l'essentiel des usages homelab sans compromis notable.

## Sécurité et bonnes pratiques

Quelques réflexes avant de mettre ton tailnet en prod :

- **Sauvegarde la base SQLite régulièrement.** C'est le seul état persistant du serveur : perds-la et tu dois ré-enregistrer chaque appareil.
- **Protège `noise_private.key` et le reste du dossier `config/`.** Ce sont les clés qui identifient ton serveur auprès des clients.
- **Mets le reverse proxy en HTTPS strict.** Un `login-server` en HTTP clair n'est tout simplement pas accepté par les clients Tailscale récents.
- **Écris une politique ACL explicite** plutôt que de laisser tous les nœuds se parler par défaut. Le fichier de policy Headscale suit la même syntaxe que les ACLs Tailscale cloud, donc les exemples officiels sont réutilisables tels quels.
- **Garde l'image à jour.** Le projet publie des correctifs de sécurité régulièrement, comme tout logiciel qui gère de l'authentification réseau.

Si tu veux exposer un service précis de ton tailnet sur Internet en attendant que Funnel arrive côté Headscale, un [Cloudflare Tunnel](/cloudflare-tunnel-docker-homelab/) devant ce service précis reste la solution la plus simple, sans toucher à la configuration du tailnet entier.

## Dépannage rapide

### Le client reste bloqué sur "NeedsLogin"
Vérifie que `server_url` dans `config.yaml` correspond exactement à l'URL que le client contacte, protocole et port inclus. Un mismatch, même minime, bloque l'enregistrement.

### "connection refused" au moment du `tailscale up`
Le reverse proxy ne relaie probablement pas correctement vers le port 8080 du conteneur. Teste en local avec `curl http://127.0.0.1:8080/health` directement sur l'hôte Docker.

### Les appareils ne se voient pas entre eux
Regarde ta politique ACL. Par défaut, sans fichier de policy explicite, Headscale peut restreindre la communication inter-nœuds selon la configuration choisie. Ajoute une règle `accept` large pour tester, puis restreins.

### MagicDNS ne résout rien côté client
Vérifie que `magic_dns: true` est bien actif dans `config.yaml` et que le client a `--accept-dns=true` (comportement par défaut sauf changement manuel).

## Conclusion

**Headscale docker** referme la dernière dépendance cloud d'un mesh Tailscale : le plan de contrôle. Pour un homelab qui utilise déjà [Tsdproxy](/tsdproxy-docker-tailscale-proxy/) pour exposer ses conteneurs sur le tailnet, ajouter Headscale en dessous ferme la boucle complète, plus aucune brique réseau critique ne dépend d'un tiers.

Ce n'est pas gratuit en effort : tu deviens responsable de la disponibilité du serveur, des sauvegardes et des mises à jour de sécurité. Mais si l'auto-hébergement jusqu'au bout du réseau te motive, c'est le morceau qui manquait.
