---
title: "NocoDB Docker : alternative auto-hébergée à Airtable"
description: "NocoDB Docker : déploie ta base de données type Airtable en auto-hébergement. Guide complet avec PostgreSQL, Docker Compose et import CSV."
pubDatetime: "2026-05-30T06:00:00.000Z"
modDatetime: "2026-05-31T00:00:00+01:00"
author: Brandon Visca
tags:
  - debutant
  - docker
  - auto-hebergement
  - productivite
  - guide
  - nocodb
featured: false
draft: false
focusKeyword: nocodb docker
faqs:
  - question: "NocoDB est-il vraiment gratuit ?"
    answer: "Oui. L'édition auto-hébergée est open-source et gratuite, sans limite de lignes ni de collaborateurs. Tu n'es limité que par ton propre serveur."
  - question: "Peut-on migrer ses données Airtable vers NocoDB ?"
    answer: "Oui, en passant par un export CSV d'Airtable que tu réimportes dans NocoDB. Il n'existe pas encore d'import direct 100 % natif depuis un export JSON Airtable."
  - question: "NocoDB fonctionne-t-il avec MySQL en plus de PostgreSQL ?"
    answer: "Oui. NocoDB se branche sur PostgreSQL, MySQL et MariaDB. Tes données restent dans ta base SQL, NocoDB n'ajoute qu'une couche visuelle."
timezone: Europe/Paris
---
> 💡 **TL;DR** — NocoDB en bref :
> - Alternative open-source et auto-hébergée à Airtable, posée au-dessus de ta propre base SQL (PostgreSQL, MySQL, MariaDB).
> - Stack Docker Compose NocoDB + PostgreSQL opérationnelle en moins de 10 minutes.
> - Vues grille, kanban et formulaire, import CSV et API REST auto — tes données restent chez toi, sans lock-in.

## Table des matières

## Tu payes Airtable alors que tu pourrais self-hoster gratuitement ?

On va pas se mentir : Airtable, c'est magique. Des bases en mode tableur, des vues en kanban, des liens entre tables, des formulaires… Le problème ? Quand tu commences à t'y habituer et que tes projets grossissent, le pricing te rattrape comme un coup de pied aux culs. Les limitations gratuites deviennent vite étouffantes, et tes données restent planquées sur les serveurs de quelqu'un d'autre.

Heureusement, il existe une alternative open-source qui te permet de reprendre le contrôle : **NocoDB**. L'idée est simple — transformer n'importe quelle base de données SQL (MySQL, PostgreSQL, MariaDB…) en interface visuelle de type spreadsheet, exactement comme Airtable ou Notion Database. Et le meilleur dans tout ça : tu peux l'héberger toi-même avec Docker en quelques minutes.

Si tu débutes avec Docker, sache que cette stack est un excellent premier projet appliqué. Tu peux d'ailleurs commencer par lire mon [guide complet pour débuter avec Docker](/docker-debutant-services-auto-heberger/) si tu veux comprendre les bases avant d'attaquer.

Dans ce tuto, on va voir comment déployer NocoDB avec Docker Compose et PostgreSQL, comment configurer ta première base, importer des données et — surtout — ce que ça vaut vraiment comparé aux autres solutions du marché.

## Qu'est-ce que NocoDB exactement ?

NocoDB est un outil de base de données **no-code / low-code** open-source qui se place au-dessus d'une base de données relationnelle existante. Concrètement, il te offre une interface graphique dans le navigateur pour :

- Créer des tables et des colonnes (texte, nombre, date, lien vers une autre table, etc.)
- Switche entre différentes vues : Grille, Kanban, Formulaire, Galerie
- Gérer les permissions utilisateur et les rôles
- Générer une API REST automatiquement sur chaque table
- Importer et exporter facilement en CSV

C'est un peu le cousin opensource d'Airtable, mais avec une philosophie différente : tes données restent dans **ta** base SQL. NocoDB ne fait que proposer une couche d'abstraction visuelle au-dessus. Si demain tu décides d'abandonner NocoDB, tes données sont toujours là, propres et accessibles via PostgreSQL. Pas de lock-in vendeur, pas de format propriétaire.

L'outil est développé en Node.js (NestJS côté serveur) et Vue.js, il consomme peu de ressources et tourne très bien sur un petit VPS ou même un Raspberry Pi 4 pour des usages modestes.

## Pourquoi l'auto-héberger plutôt que d'utiliser le cloud ?

Là aussi, pas besoin de rentrer dans le débat philosophique pendant quatre heures. L'auto-hébergement de NocoDB présente trois avantages concrets :

**1. Pas de limites artificielles**
Nombre de lignes illimité, fichiers joints limités uniquement par ton disque, pas de restriction sur le nombre de collaborateurs. Tu es chez toi.

**2. Confidentialité et souveraineté**
Si tu gères un inventaire matériel sensible, un planning staffé ou un CRM client, tu n'as pas forcément envie que ces infos transitent par des serveurs californiens.

**3. Coût**
Un VPS de 4€/mois chez Hetzner ou un vieux NUC dans un coin de ton salon suffisent amplement pour faire tourner NocoDB + PostgreSQL sans sourciller.

Bien sûr, cela implique que tu assumes la maintenance : sauvegardes, mises à jour, sécurisation du serveur. Si tu débutes dans l'auto-hébergement, mon [guide complet pour reprendre le contrôle de tes données](/auto-hebergement-guide-complet-2025/) devrait t'intéresser.

## Les prérequis pour ce tuto

Pour suivre ce guide, tu auras besoin de :

- Un serveur ou une machine avec **Docker et Docker Compose** installés
- Environ **2 Go de RAM** disponibles (NocoDB + PostgreSQL s'en sortent très bien avec ça)
- **Un reverse proxy** (facultatif mais fortement recommandé pour le HTTPS). Si tu veux une solution simple, jette un œil à mon article sur [Traefik en Docker](/traefik-reverse-proxy-docker/)
- Un minimum de confiance en toi — on va faire ça ensemble, promis

## Installation avec Docker Compose

On va partir sur une stack complète et propre : **PostgreSQL** pour stocker les données, **NocoDB** pour l'interface, et deux volumes Docker pour la persistance.

### Le stack complet PostgreSQL + NocoDB

Crée un répertoire pour ton projet et un fichier `docker-compose.yml` à l'intérieur :

```bash
mkdir ~/nocodb
nano ~/nocodb/docker-compose.yml
```

Colle-y ce contenu :

```yaml
version: '3.8'

services:
  nocodb:
    image: nocodb/nocodb:latest
    container_name: nocodb
    restart: unless-stopped
    ports:
      - "8080:8080"
    environment:
      - NC_DB=pg://nocodb-db:5432?u=nocodb&p=changeMoiUnMotDePasseFort&d=nocodb
      - NC_AUTH_JWT_SECRET=${NC_JWT_SECRET:-uneChaineUltraSecreteAChanger}
    depends_on:
      nocodb-db:
        condition: service_healthy
    volumes:
      - nocodb-data:/usr/src/app/data

  nocodb-db:
    image: postgres:15-alpine
    container_name: nocodb-db
    restart: unless-stopped
    environment:
      - POSTGRES_DB=nocodb
      - POSTGRES_USER=nocodb
      - POSTGRES_PASSWORD=changeMoiUnMotDePasseFort
    volumes:
      - pg-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U nocodb -d nocodb"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  nocodb-data:
  pg-data:
```

**Quelques explications rapides :**

- `NC_DB` est la chaîne de connexion vers PostgreSQL. Elle suit le format `pg://host:port?u=user&p=pass&d=db`.
- `NC_AUTH_JWT_SECRET` sert à signer les tokens d'authentification. Pense à la remplacer par un vrai secret en production (tu peux générer une chaîne aléatoire avec `openssl rand -hex 32`).
- Le `healthcheck` sur Postgres garantit que NocoDB ne démarre pas avant que la base soit prête, évitant ainsi les erreurs de connexion aléatoires.

### Premier lancement et vérifications

Lance la stack :

```bash
cd ~/nocodb
docker compose up -d
```

Attends environ 20 à 30 secondes le temps que PostgreSQL s'initialise et que NocoDB démarre. Vérifie que les conteneurs tournent bien :

```bash
docker compose ps
```

Tu devrais voir les deux services `Up` et `healthy`.

Ouvre ensuite ton navigateur à l'adresse `http://IP_DE_TON_SERVEUR:8080`. Si tout va bien, NocoDB te propose de créer un compte administrateur.

Si tu exposes ça sur Internet, **passes obligatoirement par un reverse proxy avec HTTPS**. Traefik, Nginx Proxy Manager, Caddy… peu importe, mais ne laisse jamais une application web en plain HTTP sur le web. Si tu ne sais pas comment faire, suis le guide Traefik mentionné plus haut.

## Configuration initiale : ta première base en 2 minutes

Une fois connecté, l'interface NocoDB est épurée et intuitive. Voici comment commencer sans te prendre la tête.

### Créer une base et une table

1. Clique sur **"New Project"** (ou "Nouveau Projet" selon la langue)
2. Choisir **"Create new base"** — cela crée une base PostgreSQL dédiée sous le capot
3. Donne un nom à ta base, par exemple `inventaire-homelab`
4. NocoDB te place directement dans la vue grille avec une table par défaut. Renomme-la en cliquant sur le nom en haut

Tu peux ensuite ajouter des colonnes : texte, nombre, email, date, case à cocher, lien vers une autre table, etc. Le menu est contextuel et te guide pas à pas.

### Importer des données depuis Airtable ou CSV

NocoDB sait nativement importer des fichiers **CSV** et des exports Airtable (format CSV aussi). Pour tester rapidement :

1. Prépare un fichier CSV propre avec une première ligne d'en-têtes (sans accents ni espaces dans les noms de colonnes, c'est plus sûr)
2. Dans NocoDB, clique droit sur l'espace de travail à gauche → **Import**
3. Suis l'assistant et mappe les colonnes

Concernant Airtable spécifiquement, il n'existe pas encore d'import direct 100 % natif depuis un export JSON. La méthode la plus fiable reste de passer par un export CSV d'Airtable, que tu réimportes ensuite dans NocoDB. C'est une opération manuelle, mais elle fonctionne très bien pour des bases de taille moyenne.

Pour les bases très complexes avec plein de relations et de pièces jointes, il faudra mettre les mains dans le cambouis et réétablrir manuellement les liens. C'est le prix de la liberté.

## Cas d'usage concrets pour ton homelab

NocoDB brille particulièrement dans des cas où on a besoin d'une structure de données relationnelle sans pour autant écrire du SQL à la main. Voici trois usages qui cartonnent chez les auto-hébergeurs.

### Inventaire IT

Tu as un rack de serveurs, une poignée de Raspberry Pi traînant sur l'étagère et trois NAS qui se ressemblent ? Crée une base NocoDB avec les tables suivantes :

- **Machines** : nom, IP, type (serveur physique / VM / conteneur), emplacement rack, date d'achat
- **Disques** : modèle, capacité, date d'achat, état SMART, lié à une machine
- **Licenses** : logiciel, clé de licence, date d'expiration, coût

Tu obtiens un inventaire consultable depuis n'importe quel navigateur, partageable avec ton équipe, et totalement sous ton contrôle. Aucun Excel sur un NAS à l'abandon, aucun Google Sheet qui fuite.

### Gestion de projets

Besoin d'un kanban simple sans la surcharge de Jira ou la limitation d'Airtable ? Une base NocoDB avec une vue Kanban sur le statut des tâches suffit largement :

- Table **Tâches** : titre, description, statut (À faire / En cours / Terminé), priorité, date échéance
- Table **Projets** : nom, client, date de début, date de fin
- Lien entre les deux tables pour savoir quelles tâches vont avec quel projet

Tu peux créer des formulaires publics pour que des collègues soumettent des tickets sans jamais voir la base entière.

### CRM mini

Pas besoin de payer HubSpot 50€/mois pour suivre tes prospects. Une base **Prospects** avec nom, email, entreprise, statut (piste / contacté / en négociation / signé / perdu), montant estimé et date de dernier contact te donne déjà une vision claire de ton pipeline.

Bien sûr, ça ne remplace pas un vrai CRM avec automations d'emails et intégrations HubSpot. Mais pour un freelance ou une petite équipe, c'est rudement efficace.

## Les limites et les alternatives self-hosted

Je te préviens tout de suite : NocoDB n'est pas un clone parfait d'Airtable. Il y a des zones de turbulences à connaître pour ne pas être déçu.

### Ce qui accroche encore

- **Les formules** sont moins riches que chez Airtable. Les calculs avancés ou les rollups complexes peuvent coincer.
- **Les automations** n'existent pas en natif dans NocoDB. Pas de "si ça change, envoie un mail". Pour ce genre de workflow, tu devras brancher [n8n en Docker](/n8n-docker-workflow-automation/) ou un équivalent par API.
- **L'interface** est propre mais moins polie. Quelques micro-lags, des traductions parfois incomplètes, des détails d'UX qui rappellent que c'est un projet communautaire.
- **Les pièces jointes** sont stockées localement par défaut. Pense à prévoir de l'espace disque et une stratégie de backup.

### Les autres joueurs du marché

Si NocoDB ne te convient pas, trois alternatives sérieuses existent dans l'écosystème self-hosted :

**Baserow** — Probablement le plus proche d'Airtable en termes d'UX. L'interface est moderne, les formulaires sont bien foutus et le support des formules est plus avancé. Contrepartie : l'édition open-source manque quelques features payantes (comme les SSO ou les permissions granulaires de niveau ligne). Baserow est Docker-native et se déploie aussi facilement.

**Grist** — Davantage orienté "spreadsheet programmable". Très puissant si tu aimes les formules Python embarquées et la logique de données structurée. Moins sexy visuellement, mais parfait pour les geeks qui veulent un Excel relationnel auto-hébergé.

**Teable** — Une solution plus jeune qui mise sur la rapidité et l'interface. Moins mature que NocoDB ou Baserow, mais si tu cherches purement de la performance et du design, cela vaut le coup de suivre son évolution.

Mon conseil ? Déploie NocoDB d'abord, joue avec pendant une semaine sur un vrai cas d'usage. Si tu butes sur des limites bloquantes, migre vers Baserow. Les deux utilisent PostgreSQL, donc la bascule est envisageable sans réécriture totale.

## FAQ

### NocoDB est-il vraiment gratuit ?

Oui. L'édition auto-hébergée est open-source et gratuite, sans limite de lignes ni de collaborateurs. Tu n'es limité que par ton propre serveur.

### Peut-on migrer ses données Airtable vers NocoDB ?

Oui, en passant par un export CSV d'Airtable que tu réimportes dans NocoDB. Il n'existe pas encore d'import direct 100 % natif depuis un export JSON Airtable.

### NocoDB fonctionne-t-il avec MySQL en plus de PostgreSQL ?

Oui. NocoDB se branche sur PostgreSQL, MySQL et MariaDB. Tes données restent dans ta base SQL, NocoDB n'ajoute qu'une couche visuelle.

## Conclusion

NocoDB est une excellente porte d'entrée vers l'auto-hébergement de bases de données relationnelles. Il ne remplacera pas Airtable pour les équipes avancées qui vivent dans les automations, mais pour l'auto-hébergeur ou le petit entrepreneur qui veut un outil solide, gratuit et sans lock-in, c'est du solide.

Le combo **Docker Compose + PostgreSQL** que je t'ai filé dans cet article te donne une stack propre en moins de 10 minutes. Tu restes maître de tes données, tu limites les coûts, et tu apprends au passage comment structurer une base SQL sans écrire une seule requête.

Allez, assez lu. Ouvre un terminal, copie le compose, et lance-toi. Et si tu bloques sur un truc, tu sais où me trouver.

---

Besoin d'autres outils pour ton homelab dockerisé ? Jette un œil à mon article sur [les services Docker accessibles même aux débutants](/docker-debutant-services-auto-heberger/). Tu y trouveras des idées pour aller plus loin.
