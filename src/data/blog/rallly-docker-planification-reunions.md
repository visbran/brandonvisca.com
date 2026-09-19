---
title: "Rallly Docker : planification de réunions auto-hébergée (alternative Doodle)"
description: "Rallly Docker : héberge ton propre outil de sondage de réunions avec docker-compose, alternative libre à Doodle, HTTPS automatique inclus."
pubDatetime: "2026-09-19T11:02:12+02:00"
modDatetime: "2026-09-18T08:00:00.000Z"
author: Brandon
tags:
  - docker
  - auto-hebergement
  - guide
  - intermediaire
featured: false
draft: false
focusKeyword: rallly docker
faqs:
  - question: "Faut-il un compte pour voter à un sondage Rallly ?"
    answer: "Non. Les participants ouvrent le lien du sondage, cliquent sur leurs créneaux disponibles et valident, sans inscription ni mot de passe. Seul toi, l'organisateur, as besoin d'un compte."
  - question: "Combien de RAM faut-il pour héberger Rallly avec Docker ?"
    answer: "La doc officielle annonce 2 Go de RAM minimum pour la stack complète (app, Postgres, stockage S3, reverse proxy). En pratique, un petit VPS ou une VM homelab suffit largement."
  - question: "Peut-on brancher Rallly sur un reverse proxy Traefik ou Caddy déjà existant ?"
    answer: "Oui, en mettant PROXY_MODE sur external dans le .env. Rallly n'ouvre alors que le port de l'app en interne, et c'est ton reverse proxy externe qui gère le HTTPS et le domaine."
---
> 💡 **TL;DR**
> - Rallly est un outil de sondage de dates open-source (licence AGPLv3), l'alternative libre à Doodle : tu crées un sondage, tes participants votent sans créer de compte
> - Installation Rallly Docker recommandée en une commande via le CLI officiel, qui embarque l'app, Postgres, du stockage S3 et un reverse proxy avec HTTPS automatique
> - Une installation manuelle en docker-compose reste possible si tu as déjà un Traefik ou un Caddy qui tourne chez toi

## Table des matières

## Pourquoi auto-héberger un outil de sondage de dates

Tu connais le rituel. Il faut caler une réunion à six, tu ouvres Doodle, tu crées ton sondage, et tu te prends un mur de pub avant que les colonnes de créneaux s'affichent. Ou alors tu passes en version payante juste pour retirer les pubs et masquer les votes des autres. Pour un besoin aussi basique que "quel jour ça t'arrange", ça fait cher payé en frustration.

Le souci de fond, c'est que Doodle et ses cousins collectent les adresses mail et les habitudes de dispo de tout le monde, pas juste les tiennes. Tes collègues, ta famille, tes clients : tout ce petit monde vote sur un service dont tu ne contrôles ni la rétention des données ni la politique de revente à des tiers.

Il existe une alternative propre à ce problème : **Rallly**. C'est un outil de sondage de dates open-source, développé par Luke Vella et maintenu par Stack Snap Ltd, sous licence AGPLv3. Tu l'auto-héberges en Docker, tu crées tes sondages depuis ton propre domaine, et personne d'autre que toi ne voit qui a voté quoi.

Dans le même esprit que [Actual Budget en Docker](/actual-budget-docker-gestion-budget/) ou [Authelia pour sécuriser tes services maison](/authelia-docker-authentification-2fa-homelab/), Rallly fait partie de ces petits outils qui remplacent un SaaS gratuit-mais-pas-vraiment par une brique que tu contrôles de bout en bout.

## Rallly Docker : installation avec le CLI officiel

La méthode recommandée par l'éditeur pour un déploiement Rallly Docker, c'est le script d'installation officiel. Il embarque tout ce qu'il faut sur une seule machine : l'application, une base PostgreSQL, du stockage compatible S3 (via Garage) pour les pièces jointes, et un reverse proxy Traefik qui gère le HTTPS avec Let's Encrypt automatiquement.

Connecte-toi en SSH sur ton serveur ou ta VM homelab, assure-toi que Docker tourne, puis lance :

```bash
curl -fsSL https://get.rallly.co | bash
```

Le script clone le dépôt `lukevella/rallly-selfhosted`, te pose quelques questions (ton nom de domaine, ton adresse mail pour les notifications Let's Encrypt), génère les secrets automatiquement avec openssl, puis démarre la stack.

Si tu préfères garder la main sur chaque étape plutôt que de lancer un script depuis Internet dans un shell root, l'équivalent manuel :

```bash
git clone https://github.com/lukevella/rallly-selfhosted.git
cd rallly-selfhosted
./rallly.sh setup
./rallly.sh start
```

`./rallly.sh setup` copie le `.env.example` vers `.env`, te demande ton domaine et ton mail, et génère `SECRET_PASSWORD`. `./rallly.sh start` lève les conteneurs. Comptez deux minutes avant que Traefik obtienne son certificat et que l'appli réponde sur `https://ton-domaine.com`.

⚠️ Avant de lancer quoi que ce soit, pointe l'enregistrement DNS de ton sous-domaine (`rallly.tondomaine.com`) vers l'IP publique de ton serveur, et ouvre les ports 80 et 443. Sans ça, Let's Encrypt ne pourra jamais valider ton domaine.

Prérequis serveur annoncés par la doc officielle : 2 Go de RAM minimum, Docker 19.03 ou plus récent, ports 80 et 443 libres, `openssl` installé (déjà présent sur la plupart des distros).

## Installation manuelle avec docker-compose

Si tu as déjà un Traefik ou un Caddy central qui route tout ton homelab, la stack tout-en-un du CLI fait doublon. Voici une installation manuelle qui ne déploie que l'app Rallly et sa base Postgres, sans reverse proxy intégré.

Crée un dossier dédié :

```bash
mkdir -p ~/rallly && cd ~/rallly
```

Le `docker-compose.yml` :

```yaml
services:
  rallly:
    image: lukevella/rallly:4
    container_name: rallly
    restart: unless-stopped
    depends_on:
      rallly_db:
        condition: service_healthy
    environment:
      - DATABASE_URL=postgres://rallly:${DB_PASSWORD}@rallly_db:5432/rallly
      - SECRET_PASSWORD=${SECRET_PASSWORD}
      - NEXT_PUBLIC_BASE_URL=https://rallly.tondomaine.com
      - SUPPORT_EMAIL=admin@tondomaine.com
    ports:
      - "3000:3000"

  rallly_db:
    image: postgres:14-alpine
    container_name: rallly_db
    restart: unless-stopped
    environment:
      - POSTGRES_USER=rallly
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_DB=rallly
    volumes:
      - db-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U rallly"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  db-data:
```

Crée un fichier `.env` à côté, avec les deux secrets référencés dans le compose :

```bash
echo "DB_PASSWORD=$(openssl rand -base64 24)" > .env
echo "SECRET_PASSWORD=$(openssl rand -base64 32)" >> .env
```

`SECRET_PASSWORD` chiffre les sessions et les cookies, il doit faire au moins 32 caractères, ne le regénère jamais après le premier démarrage sinon tous les comptes sont déconnectés de force. Lance la stack :

```bash
docker compose up -d
```

Rallly applique ses migrations Prisma automatiquement au démarrage, pas de commande manuelle à lancer. Vérifie les logs si l'appli met du temps à répondre :

```bash
docker compose logs -f rallly
```

## Configuration du fichier .env

Que tu passes par le CLI ou par ton propre compose, le comportement de Rallly se pilote entièrement par variables d'environnement. Les plus utiles au quotidien :

- `SUPPORT_EMAIL` : adresse affichée aux utilisateurs qui ont un souci
- `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PWD`, `NOREPLY_EMAIL` : nécessaires si tu veux les notifications par mail et la connexion par lien magique
- `SMTP_SECURE` : à passer sur `true` si ton SMTP tourne en TLS implicite (port 465)
- `REGISTRATION_ENABLED` : à `false` une fois que ton compte organisateur est créé, si tu ne veux pas que n'importe qui s'inscrive
- `ALLOWED_EMAILS` : liste blanche séparée par des virgules, pour restreindre la création de compte à ton domaine mail
- `EMAIL_LOGIN_ENABLED` : active ou coupe la connexion par lien magique envoyé par mail

💡 Sans configuration SMTP, Rallly fonctionne quand même : tu peux créer et partager des sondages. C'est juste les notifications et la connexion par mail qui restent indisponibles.

## Sécuriser l'accès avec un reverse proxy externe

Si tu es parti sur l'installation manuelle plutôt que sur le CLI (qui embarque déjà Traefik), il te faut router le HTTPS toi-même. Passe `PROXY_MODE=external` dans ton `.env`, et déclare un bloc Caddy classique :

```
rallly.tondomaine.com {
  reverse_proxy localhost:3000
}
```

Ne laisse jamais le port 3000 exposé nu sur Internet. Rallly ne fait pas de rate limiting intégré sur les tentatives de connexion à ton compte organisateur, c'est le job du reverse proxy ou d'un [Fail2Ban en Docker](/fail2ban-docker-securite-serveur/) devant.

Si plusieurs personnes de ton entourage doivent créer des sondages (pas juste toi), pense à mettre l'app derrière une authentification centralisée plutôt que de distribuer des comptes Rallly à tout le monde. [Authelia en Docker](/authelia-docker-authentification-2fa-homelab/) fait exactement ça : un portail 2FA devant tes services internes, Rallly compris.

## Sauvegarde et mise à jour

Toute la donnée qui compte vit dans la base Postgres : les sondages, les votes, les comptes. Avec l'installation CLI, une commande suffit :

```bash
./rallly.sh backup
```

Le script dépose un `.sql.gz` horodaté dans `./backups/`. Pour restaurer :

```bash
gunzip < backups/rallly_2026-09-18.sql.gz | docker compose exec -T db psql -U postgres rallly
```

Avec l'installation manuelle, un simple `pg_dump` suffit, et rien ne t'empêche de brancher ce dump dans ta routine [Duplicati](/duplicati-docker-sauvegarde/) existante pour le chiffrer et l'envoyer hors site :

```bash
docker compose exec rallly_db pg_dump -U rallly rallly > rallly-backup-$(date +%F).sql
```

Pour la mise à jour, le CLI encapsule tout :

```bash
./rallly.sh update
```

En manuel, c'est le classique `docker compose pull && docker compose up -d`. Les migrations de base tournent automatiquement au redémarrage, tu n'as rien d'autre à faire. Lis quand même le changelog GitHub avant une montée de version majeure (le tag d'image passe de `lukevella/rallly:4` à `lukevella/rallly:5` par exemple), les breaking changes sont documentés là.

## Rallly vs Doodle vs Crab Fit

| Outil | Auto-hébergé | Compte requis pour voter | Licence | Pub | Historique illimité |
|-------|--------------|---------------------------|---------|-----|----------------------|
| **Rallly** | Oui, Docker | Non | AGPLv3, libre | Non | Oui, gratuit en self-host |
| **Doodle** | Non (SaaS) | Non | Propriétaire | Oui, en gratuit | Limité sans abonnement Pro |
| **Crab Fit** | Non (SaaS) | Non | Open-source côté code, pas de self-host packagé | Non | Oui |
| **Framadate** | Oui (instance associative ou perso) | Non | AGPLv3 | Non | Oui |

Rallly se distingue par son interface soignée et sa gestion de compte organisateur (tu retrouves tous tes sondages passés, tu peux les archiver). Framadate reste une alternative solide si tu veux quelque chose d'encore plus minimaliste et que tu n'as pas envie de gérer Docker toi-même, en rejoignant une instance associative existante.

Rallly Pro, la version payante éditée par Stack Snap Ltd, ajoute la personnalisation de marque et retire l'attribution "Powered by Rallly" en bas de page. Rien de tout ça ne concerne l'instance auto-hébergée : en self-host, tu as déjà toutes les fonctionnalités, gratuitement, à vie.

## Conclusion

Rallly Docker coche toutes les cases d'un bon candidat homelab : une seule commande pour l'installer avec le CLI officiel, une base Postgres classique à sauvegarder, un HTTPS qui se configure tout seul si tu veux, et un vrai reverse proxy externe si tu préfères garder la main. Pas de pub, pas de compte forcé pour tes participants, pas de dépendance à un service tiers qui change ses conditions tous les six mois.

La vraie question c'est pas "pourquoi auto-héberger un outil de sondage de dates", c'est plutôt "pourquoi j'ai mis autant de temps à le faire". Quinze minutes de setup, et Doodle sort de ta vie numérique pour de bon.
