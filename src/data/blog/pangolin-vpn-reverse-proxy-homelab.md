---
title: "Pangolin Docker : VPN + reverse proxy identity-aware"
description: "Pangolin Docker : déploie un reverse proxy identity-aware qui tunnelise tes services homelab en WireGuard, sans ouvrir un port entrant chez toi."
pubDatetime: "2026-10-27T11:01:11+01:00"
modDatetime: "2026-10-26T08:00:00.000Z"
author: Brandon
tags:
  - securite
  - docker
  - vpn
  - reverse-proxy
  - wireguard
  - intermediaire
featured: false
draft: false
focusKeyword: pangolin docker
faqs:
  - question: "Pangolin remplace-t-il complètement Cloudflare Tunnel ?"
    answer: "Fonctionnellement oui pour l'exposition sans port ouvert, mais tu héberges toi-même toute la chaîne. Plus de travail au départ, zéro dépendance à un tiers ensuite."
  - question: "Faut-il un VPS public pour utiliser Pangolin ?"
    answer: "Le composant central (Traefik, Gerbil) a besoin d'une IP publique fixe, typiquement un VPS. Newt côté homelab n'a besoin d'aucun port ouvert, même derrière un NAT classique."
  - question: "Que se passe-t-il si le VPS qui héberge Pangolin tombe ?"
    answer: "L'accès à toutes tes ressources est coupé tant que le VPS n'est pas relevé, il n'y a pas de bascule locale automatique. Prévois un monitoring externe sur ce serveur."
---
> 💡 **TL;DR**
> - Pangolin Docker est un reverse proxy identity-aware qui tunnelise tes services homelab en WireGuard, sans ouvrir aucun port entrant côté origine
> - L'architecture combine Traefik pour le proxy HTTP, Gerbil pour le tunnel WireGuard côté serveur, et Newt comme client léger côté homelab
> - Installation via le quick installer officiel, Community Edition gratuite sous AGPL-3, Enterprise Edition gratuite sous 100 000 $ de chiffre d'affaires annuel

## Pangolin Docker, un reverse proxy qui fait aussi VPN zero-trust

Tu as un service qui tourne dans ton homelab, un dashboard Grafana ou une instance Nextcloud, et tu veux y accéder depuis l'extérieur sans ouvrir un port chez toi. Deux réponses classiques existent déjà. La première : un tunnel WireGuard brut comme dans mon [guide WireGuard Docker](/wireguard-docker-vpn-homelab/), rapide à monter mais sans gestion d'identité, sans journal de connexion, sans contrôle fin de qui accède à quoi. La deuxième : Cloudflare Tunnel, zéro port ouvert aussi, mais ton trafic passe par l'infrastructure d'un tiers américain, point final.

Pangolin Docker se positionne entre les deux. C'est un reverse proxy auto-hébergé qui encapsule WireGuard pour relier un serveur public, un VPS typiquement, à tes réseaux privés, avec par-dessus une couche d'identité et de contrôle d'accès par ressource. Tu exposes `grafana.tondomaine.fr` sans qu'aucun port ne soit ouvert sur ta box, et tu décides qui peut s'y connecter, avec quelle méthode d'authentification.

Le projet est maintenu par l'organisation fosrl sur GitHub, sous la marque Fossorial, en double licence. La Community Edition est sous AGPL-3, complètement gratuite et open source, avec toutes les fonctionnalités de base. L'Enterprise Edition ajoute des options avancées sous la Fossorial Commercial License, gratuite elle aussi pour un usage perso ou une petite structure sous 100 000 dollars de chiffre d'affaires annuel brut, avec une clé de licence à récupérer même dans ce cas de figure.

## Table des matières

## L'architecture Pangolin Docker : Gerbil, Newt et Traefik

Pour comprendre ce que tu déploies avec Pangolin Docker, mieux vaut connaître les quatre briques qui composent la stack.

- **Pangolin** est le serveur de management central : dashboard web, identité, politiques d'accès, configuration des ressources
- **Traefik** fait le vrai travail de reverse proxy HTTP. Un plugin maison, Badger, s'intercale devant chaque requête pour vérifier l'authentification auprès de Pangolin avant de laisser passer
- **Gerbil** est le serveur WireGuard côté VPS. Il crée les peers pour chaque site et, quand le NAT hole punching échoue, fait relais lui-même
- **Newt** tourne côté homelab, sur ta machine ou ton NAS. C'est un client WireGuard en espace utilisateur qui ouvre deux connexions sortantes : un WebSocket vers le control plane pour recevoir sa config, et un tunnel WireGuard vers Gerbil pour le trafic

Le flux d'une requête dans une stack Pangolin Docker ressemble à ça : une visite sur `https://app.tondomaine.fr` arrive sur Traefik côté VPS, traverse le tunnel WireGuard jusqu'à Newt côté homelab, qui relaie vers le service local en `http://localhost:3000`. À aucun moment tu n'ouvres de port entrant chez toi, Newt ne fait que des connexions sortantes.

Détail important : un site Newt nouvellement installé n'expose rien par défaut. Tant que tu n'as pas créé explicitement une ressource (le couple domaine plus service interne), le trafic est refusé. C'est l'inverse d'un reverse proxy classique où tout ce qui est dans le `docker-compose.yml` devient accessible dès que le réseau est câblé.

## Prérequis et ouverture des ports pour Pangolin Docker

Avant de lancer l'installeur, prépare ces quatre éléments :

- Un serveur Linux avec accès root et une IP publique dédiée, Ubuntu 20.04+ ou Debian 11+ recommandés
- Un nom de domaine qui pointe vers cette IP, pour le dashboard et les ressources que tu exposeras
- Une adresse e-mail valide, utilisée pour les certificats Let's Encrypt et le compte admin
- Les ports ouverts côté pare-feu : `80/tcp` et `443/tcp` pour le HTTP, `51820/udp` pour le tunnel Gerbil, `21820/udp` pour les clients

Si tu gères ton pare-feu avec [nftables](/nftables-docker-pare-feu-linux/) plutôt qu'avec les iptables historiques, ouvre ces quatre ports avant de lancer l'installeur, pas après. Un symptôme classique d'un pare-feu mal configuré avec Pangolin Docker : le dashboard répond en HTTP, mais le tunnel WireGuard ne monte jamais parce que l'UDP 51820 est filtré en silence.

Côté homelab, Newt n'a besoin d'aucun port ouvert. Il initie toutes les connexions vers l'extérieur, donc même derrière un routeur grand public sans redirection de port, ça fonctionne.

## Installer Pangolin Docker avec le quick installer officiel

Pangolin Docker ne se déploie pas directement avec un `docker-compose.yml` que tu écris à la main. L'installeur officiel télécharge et configure tout, y compris les fichiers Compose, à l'endroit où tu le lances :

```bash
curl -fsSL https://static.pangolin.net/get-installer.sh | bash
sudo ./installer
```

Déplace d'abord l'installeur dans le dossier où tu veux que la stack vive, il y place tous ses fichiers de config.

L'installeur te pose une série de questions :

- **Édition** : Community ou Enterprise
- **Domaine de base** : par exemple `tondomaine.fr`
- **Domaine du dashboard** : par défaut `pangolin.tondomaine.fr`
- **E-mail Let's Encrypt** : pour la génération automatique des certificats
- **Tunneling Gerbil** : activé par défaut, laisse-le comme ça sauf cas très particulier
- **SMTP** : optionnel, utile si tu veux des notifications par e-mail

Une fois l'installation terminée, ouvre `https://pangolin.tondomaine.fr/auth/initial-setup` et récupère le jeton de configuration dans les logs :

```bash
sudo docker compose logs pangolin
```

Ce jeton te permet de créer ton compte admin, puis ta première organisation. Après ça, tout se passe dans le dashboard web.

## Premiers pas : organisation, site, ressources et authentification SSO

Dans Pangolin Docker, la hiérarchie est simple : une **organisation** contient plusieurs **sites**, chaque site représente un point d'entrée Newt vers un réseau (ton homelab, un VPS secondaire, le réseau du bureau), et chaque site expose zéro ou plusieurs **ressources** (un service HTTP ou TCP précis, avec son propre sous-domaine).

Pour créer ton premier site, télécharge le binaire Newt correspondant à ton OS, lance-le avec le token fourni par le dashboard, et attends qu'il apparaisse en ligne. Crée ensuite une ressource : domaine, port local, protocole. Tant que tu ne fais pas ça, rien n'est accessible depuis Internet, même si Newt est connecté.

Pour l'authentification, Pangolin propose plusieurs méthodes par ressource, indépendantes du compte admin : SSO via un fournisseur OIDC externe, code d'accès à usage unique, PIN partagé, ou authentification basique. Si tu veux du SSO propre sans dépendre d'un géant du cloud, une installation Pangolin Docker s'intègre avec un IDP léger comme [Pocket-ID](/pocket-id-docker-sso-leger/) : tu crées un client OIDC côté Pocket-ID, tu colles le Client ID et le secret dans Pangolin sous « Identity Providers », et chaque ressource protégée redirige vers cette authentification avant de laisser passer la requête.

Attention à un piège classique : si ton IDP tourne lui-même derrière une ressource Pangolin, ses propres endpoints d'authentification doivent être exemptés du contrôle d'accès, sinon tu te retrouves avec une boucle où Pangolin bloque l'appel qui doit justement vérifier l'identité.

## Pangolin Docker face à Firezone, Cloudflare Tunnel et WireGuard nu

| Critère | Pangolin Docker | Firezone | Cloudflare Tunnel | WireGuard nu |
|---|---|---|---|---|
| Modèle | Auto-hébergé, AGPL-3 | Auto-hébergé, Apache 2.0 | SaaS Cloudflare | Auto-hébergé |
| Transport | WireGuard (Gerbil/Newt) | WireGuard | Protocole propriétaire | WireGuard |
| Proxy HTTP intégré | Oui (Traefik) | Non | Oui | Non |
| Contrôle d'accès par ressource | Oui, par ressource | Oui, par policy | Limité (Access) | Non |
| IDP externe requis | Non, optionnel | Oui | Non | Non |
| Dépendance à un tiers | Aucune | Aucune | Totale (Cloudflare) | Aucune |

La vraie différence avec [Firezone](/firezone-docker-vpn-zero-trust/), c'est que Firezone exige un fournisseur d'identité OIDC ou SAML dès le départ, sans IDP il ne fonctionne pas. Pangolin Docker, lui, marche très bien avec juste un compte admin local et des ressources en PIN ou passcode, l'OIDC externe reste une option.

Face à Cloudflare Tunnel, l'argument est la souveraineté : zéro port ouvert dans les deux cas, mais chez Cloudflare le trafic transite et se déchiffre sur leur infrastructure, chez Pangolin Docker il reste sous ton contrôle du premier au dernier octet.

Et contre un WireGuard nu, la différence c'est tout ce qui est au-dessus du tunnel : dashboard, ressources par sous-domaine, logs de connexion, révocation en un clic. Si tu veux juste un tunnel point à point sans gestion web, reste sur WireGuard brut. Si tu gères plusieurs services pour plusieurs personnes, Pangolin Docker t'évite de régénérer des configs à la main à chaque changement.

## Sécurité, audit et dépannage pour Pangolin Docker

Quelques réflexes à prendre une fois la stack en place :

- **Sauvegarde la base** : la config des sites, ressources et utilisateurs vit dans une base de données selon ton installeur. Un dump régulier t'évite de tout reconfigurer après un crash disque
- **Limite les rôles admin** : ne donne le rôle administrateur qu'aux comptes qui en ont vraiment besoin, les autres utilisateurs n'ont accès qu'aux ressources qui leur sont assignées
- **Audite le serveur public** : ton VPS expose Traefik et Gerbil à Internet, c'est une surface d'attaque. Un passage régulier avec [Lynis](/lynis-docker-audit-securite-linux/) sur ce serveur repère vite une configuration SSH ou un service oublié qui ne devrait pas être là
- **Mets à jour régulièrement** : le projet évolue vite, les correctifs de sécurité sortent souvent, ne laisse pas traîner une version ancienne exposée publiquement

Côté dépannage, deux symptômes reviennent souvent avec Pangolin Docker.

**Le tunnel ne monte jamais** : vérifie que `51820/udp` est bien ouvert côté pare-feu du VPS, pas seulement côté Docker. Un `ss -ulnp` sur le serveur doit montrer Gerbil en écoute sur ce port.

**La ressource répond en 502** : Newt est probablement déconnecté, ou le port local indiqué dans la ressource ne correspond pas au port réel du service. Vérifie les logs du conteneur Newt côté homelab avant de chercher plus loin côté Pangolin.

## Conclusion

Pangolin Docker comble un vrai vide entre un WireGuard brut sans gestion et un SaaS comme Cloudflare Tunnel qui te fait dépendre d'un tiers. Tu gardes la main sur le tunnel, sur l'identité, et sur chaque ressource exposée, avec un installeur qui fait le gros du travail en quelques minutes.

Pour un homelab avec plusieurs services à exposer à plusieurs personnes, c'est plus confortable qu'une collection de configs WireGuard à la main. Si demain tu veux un zero-trust plus strict avec un IDP imposé dès l'authentification initiale, rien ne t'empêche de regarder du côté de Firezone en complément. Pour l'instant, lance l'installeur Pangolin Docker, crée ton premier site, et expose ta première ressource. Le reste suit tout seul.
