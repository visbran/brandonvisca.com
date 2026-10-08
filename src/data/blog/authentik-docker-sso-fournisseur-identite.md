---
title: "Authentik Docker : SSO et fournisseur d'identité pour ton homelab"
description: "Authentik docker : déploie ce fournisseur d'identité self-hosted en Docker Compose, configure le SSO et compare-le à Authelia pour ton homelab."
pubDatetime: "2026-10-08T11:01:11+02:00"
modDatetime: "2026-10-07T08:00:00.000Z"
author: Brandon
tags:
  - securite
  - docker
  - reverse-proxy
  - ldap
  - guide
  - intermediaire
featured: false
draft: false
focusKeyword: authentik docker
faqs:
  - question: "Authentik docker consomme combien de ressources sur mon homelab ?"
    answer: "Authentik Security recommande 2 CPU cores et 2 Go de RAM minimum pour le serveur, la base PostgreSQL et Redis inclus. Compte plutôt 1 Go de marge si tu ajoutes des outposts."
  - question: "Authentik vs Authelia : lequel choisir pour mon reverse proxy ?"
    answer: "Authelia reste plus léger et se configure en YAML pour du forward-auth pur. Authentik vise plus large avec une interface web complète, SAML, OIDC et LDAP natifs."
  - question: "Je perds l'accès au compte admin akadmin, comment je le récupère ?"
    answer: "Tu peux relancer un flow de récupération via la ligne de commande dans le conteneur server, ou recréer un utilisateur admin directement en base PostgreSQL en dernier recours."
---
> 💡 **TL;DR**
> - Authentik docker se déploie avec un seul fichier `compose.yml` officiel : PostgreSQL, Redis, server et worker, prêt en 10 minutes
> - C'est un fournisseur d'identité complet (OIDC, SAML, LDAP, SCIM) avec interface web, à la différence d'Authelia qui reste un forward-auth minimaliste en YAML
> - Un seul SSO pour Nextcloud, Grafana, Proxmox et tout ton reverse proxy : plus de mots de passe différents partout dans ton homelab

## Authentik docker : centralise enfin tes connexions

Tu as combien de mots de passe différents pour tes services self-hosted ? Moi j'en avais quinze avant de migrer sur un SSO. Un pour Nextcloud, un pour Grafana, un pour le Proxmox, un pour le NAS. Chez moi, ça finissait toujours pareil : mot de passe oublié, reset, recommencer.

**Authentik** règle ce problème. C'est un fournisseur d'identité (identity provider) auto-hébergé, développé par Authentik Security Inc., open source et gratuit dans sa version communautaire. Tu te connectes une fois, et toutes tes applications compatibles OIDC, SAML ou LDAP te reconnaissent automatiquement. Fini le mot de passe différent par service.

## Table des matières

## Pourquoi un SSO change la donne dans un homelab

Le SSO (Single Sign-On), c'est le principe du portail unique. Tu t'authentifies sur Authentik, et derrière, chaque application fait confiance au jeton qu'Authentik lui transmet. Pas de duplication de comptes, pas de mot de passe à retenir par service.

Dans un homelab, ça résout trois douleurs concrètes :

- **La gestion des comptes** : tu crées un utilisateur une fois, tu lui donnes accès aux bons groupes, et il entre partout où il doit entrer
- **La révocation immédiate** : un accès compromis ou un départ de collaborateur, tu coupes à la source, pas service par service
- **Le MFA centralisé** : tu actives la double authentification une fois sur Authentik, elle protège toute ta stack, pas juste l'app qui la propose nativement

Authentik docker encaisse large : il parle OpenID Connect, SAML 2.0, LDAP et SCIM. Si ton appli ne supporte qu'un vieux LDAP d'entreprise ou le dernier standard OIDC, Authentik sait faire le pont.

## Authentik vs Authelia : lequel choisir

C'est la question qu'on me pose le plus quand je parle SSO self-hosted. Les deux sont open source, les deux marchent avec un reverse proxy, mais leur philosophie diverge complètement.

**Authelia** reste minimaliste. Un fichier YAML, un binaire léger, pensé pour du forward-auth devant Nginx ou Traefik. Pas d'interface d'admin flashy, pas de gestion complexe de groupes. Si tu veux juste protéger trois services avec un login unique et du MFA, Authelia fait le job sans bouffer de RAM.

**Authentik** vise plus large. Interface web complète pour gérer utilisateurs, groupes, applications et policies sans toucher à un fichier de config. Support natif de SAML et SCIM que tu ne trouveras pas chez Authelia. La contrepartie : plus de conteneurs (PostgreSQL, Redis, server, worker), plus de RAM, plus de surface à maintenir.

Mon conseil honnête : si tu protèges juste ton Grafana et ton Portainer, Authelia. Si tu veux un vrai fournisseur d'identité pour dix services et plus, avec rotation de groupes et gestion fine des permissions, Authentik docker vaut le détour. Si tu veux encore plus léger qu'Authelia pour du simple SSO OIDC, regarde aussi [Pocket-ID](/pocket-id-docker-sso-leger/), pensé justement pour les petits homelabs qui n'ont pas besoin de la lourdeur d'Authentik.

## Installation Docker Compose pas à pas

Authentik Security publie un fichier `compose.yml` officiel, prêt à l'emploi. Pas besoin de bricoler toi-même les cinq conteneurs à la main.

Crée un dossier dédié et récupère le fichier :

```bash
mkdir authentik && cd authentik
wget https://docs.goauthentik.io/compose.yml
```

Génère les secrets obligatoires dans un fichier `.env` à côté :

```bash
echo "PG_PASS=$(openssl rand -base64 36 | tr -d '\n')" >> .env
echo "AUTHENTIK_SECRET_KEY=$(openssl rand -base64 60 | tr -d '\n')" >> .env
```

Le `PG_PASS` protège la base PostgreSQL interne, le `AUTHENTIK_SECRET_KEY` signe les sessions et les jetons. Ne les partage avec personne, et surtout, ne les commit jamais dans un repo Git public.

Si tu veux exposer Authentik directement sur les ports 80 et 443 plutôt que les ports internes 9000 et 9443, ajoute dans `.env` :

```bash
echo "COMPOSE_PORT_HTTP=80" >> .env
echo "COMPOSE_PORT_HTTPS=443" >> .env
```

Lance la stack :

```bash
docker compose pull
docker compose up -d
```

Compte deux minutes pour que PostgreSQL initialise ses tables et que le worker termine ses migrations. Authentik Security recommande 2 CPU cores et 2 Go de RAM minimum pour l'ensemble des conteneurs. Sur un petit nœud Proxmox, ça reste raisonnable, mais ne le colle pas sur un Raspberry Pi 3 qui tourne déjà autre chose.

## Premier login et configuration de base

Rends-toi sur `http://ton-serveur:9000/if/flow/initial-setup/` pour créer le compte administrateur `akadmin`. Choisis un mot de passe long, c'est la porte d'entrée de tout ton SSO.

Une fois connecté à l'interface d'admin, les trois notions à comprendre avant de brancher la première application :

- **Provider** : le protocole d'authentification (OAuth2/OIDC, SAML, LDAP). Tu en crées un par application ou par groupe d'applications compatibles
- **Application** : l'objet qui lie un provider à une icône, une URL de lancement et des règles d'accès
- **Policy** : les conditions d'accès. Qui a le droit de se connecter à quoi, et sous quelles conditions (groupe, MFA obligatoire, horaires)

Le flow par défaut suffit pour démarrer. Tu pourras affiner les stages (étapes de connexion) plus tard, une fois que tu maîtrises la logique de base.

## Brancher une première application sur le SSO

Prenons un cas concret : connecter Grafana à Authentik en OIDC.

Dans Authentik, crée un provider OAuth2/OIDC. Note le `Client ID` et le `Client Secret` générés, et renseigne l'URL de redirection de Grafana, en général `https://grafana.tondomaine.fr/login/generic_oauth`.

Côté Grafana, dans `grafana.ini` :

```ini
[auth.generic_oauth]
enabled = true
name = Authentik
client_id = <ton client id>
client_secret = <ton client secret>
scopes = openid profile email
auth_url = https://auth.tondomaine.fr/application/o/authorize/
token_url = https://auth.tondomaine.fr/application/o/token/
api_url = https://auth.tondomaine.fr/application/o/userinfo/
```

Redémarre Grafana, et le bouton "Sign in with Authentik" apparaît sur la page de login. Même logique pour Nextcloud, Portainer ou n'importe quel service qui parle OIDC ou SAML : tu crées un provider, tu colles les identifiants, tu testes.

Si ton reverse proxy protège déjà plusieurs services avec des règles communes, pense à coupler ça avec [CrowdSec](/crowdsec-docker-securite-collaborative/) devant ta stack : Authentik gère qui a le droit d'entrer, CrowdSec bloque ceux qui tentent de forcer la porte.

## Dépannage : les erreurs courantes

**"Invalid redirect URI"** : l'URL de callback configurée côté application ne correspond pas exactement à celle déclarée dans le provider Authentik. Vérifie le `https://` et l'absence de slash final en trop.

**Le worker reste en boucle de redémarrage** : neuf fois sur dix, c'est `AUTHENTIK_SECRET_KEY` manquant ou mal généré dans le `.env`. Relance `docker compose down && docker compose up -d` après correction.

**Connexion LDAP qui échoue depuis une vieille application** : Authentik docker a besoin d'un outpost LDAP dédié, un conteneur séparé du server principal. Déploie-le depuis l'interface admin, section Outposts, puis relie-le à ton provider LDAP.

**Page blanche après mise à jour** : vide le cache Redis avec `docker compose restart redis` avant de paniquer. C'est souvent juste une session de cache corrompue après un changement de version.

## Cas concrets dans un homelab

**Accès unique pour toute la stack monitoring.** Grafana, Prometheus et Uptime Kuma derrière un seul login Authentik, avec un groupe "monitoring" qui a accès, et le reste de la famille qui n'y touche pas.

**Portail d'accueil pour la famille.** Un groupe "famille" avec accès limité à Jellyfin et Nextcloud, un groupe "admin" avec accès à tout, policies différentes selon le groupe.

**MFA forcé sur les services sensibles.** Tu configures une policy qui exige la double authentification uniquement pour le provider lié à ton gestionnaire de mots de passe. Si tu utilises [Vaultwarden](/vaultwarden-docker-gestionnaire-mots-de-passe/), le coupler à un SSO avec MFA obligatoire ferme une des dernières portes ouvertes de ton homelab.

**Audit des connexions.** L'interface admin liste chaque authentification, échec compris. Pratique pour repérer une tentative de brute-force avant qu'elle n'aboutisse.

## Conclusion

Authentik docker demande un peu plus d'efforts qu'Authelia pour démarrer, mais le retour sur investissement arrive vite dès que tu dépasses cinq ou six services self-hébergés. Un seul login, une seule politique de sécurité, une seule porte à auditer.

Commence petit : connecte Grafana ou Nextcloud en premier, valide que le flow OIDC marche, puis ajoute le reste de ta stack service par service. Tu n'as pas besoin de tout migrer le jour un.
