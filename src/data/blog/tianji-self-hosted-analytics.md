---
title: "Tianji analytics : pourquoi j'ai lâché Google Analytics pour du self-hosted"
description: "Tianji analytics : l'outil self-hosted qui remplace Google Analytics, Uptime Kuma et Netdata. Open-source, privacy-friendly, zéro cookie banner."
pubDatetime: "2026-05-12T18:00:00+02:00"
modDatetime: 2026-05-17 00:00:00+01:00
author: Brandon Visca
tags:
  - intermediaire
  - auto-hebergement
  - docker
  - vie-privee
  - monitoring
  - guide
featured: false
draft: false
focusKeyword: Tianji analytics
faqs:
  - question: "Tianji est-il gratuit ?"
    answer: "Oui, c'est open-source sous licence Apache 2.0 et totalement gratuit en self-hosted."
  - question: "Faut-il des compétences techniques pour utiliser Tianji ?"
    answer: "Un minimum. Le déploiement se fait via Docker, donc il faut savoir manipuler un VPS et un docker-compose."
  - question: "Tianji remplace-t-il vraiment Google Analytics ?"
    answer: "Pour le suivi de base des visiteurs, oui. Pour les fonctionnalités avancées GA4 (attribution, audiences, remarketing), c'est plus limité, mais souvent suffisant pour un blog ou un site vitrine."
  - question: "Quelles sont les différences avec Umami ?"
    answer: "Tianji est inspiré d'Umami mais intègre en plus l'uptime monitoring, le server status, les surveys et le telemetry. C'est un hub tout-en-un, pas juste de l'analytics."
---
> 💡 **TL;DR** : Tianji analytics est une alternative open-source à Google Analytics, 100% self-hosted. Il combine analytics, uptime monitoring et server status dans un seul container Docker. Pas de cookie, pas de bannière RGPD, zéro coût.

## Table des matières

## Pourquoi je me suis dit "stop" avec Google Analytics

Tu connais le feeling. Tu te connectes à Google Analytics, tu vois ton dashboard avec 47 menus, 12 pop-ups "nouvelle fonctionnalité", et toute ta journée est partie.

Pire : depuis GA4, c'est devenu **illisible** pour un site perso. Les rapports sont faits pour des équipes marketing de 20 personnes, pas pour toi qui veux juste savoir si ton article sur Docker a fait 200 vues hier.

Et puis il y a la **privacy**. Le RGPD, les bannières de cookies, les consent managers à 30$/mois... Tout ça pour traquer des visiteurs qui cliquent "Refuser" de toute façon.

Si toi aussi tu cherches à [quitter Google et reprendre le contrôle de tes données](/quitter-google-auto-hebergement/), tu es au bon endroit. J'ai testé Umami, Plausible, Matomo. C'est bien. Mais j'ai fini par tomber sur **Tianji analytics**. Et là, ça a cliqué.

---

## Tianji analytics : c'est quoi exactement

La solution **Tianji analytics** (GitHub : [msgbyte/tianji](https://github.com/msgbyte/tianji)) se définit comme un **"All-in-One Insight Hub"**. Traduction : c'est pas juste un outil d'analytics. C'est **analytics + uptime monitoring + server status + surveys + telemetry**, le tout dans une seule app.

Créé en août 2023 par l'équipe de [msgbyte](https://msgbyte.com/), le projet a déjà récolté **plus de 3000 étoiles** sur GitHub et sort des mises à jour quasi hebdomadaires (dernière version : v1.31.25, mai 2026). La stack est moderne : Node.js, TypeScript, Prisma, Next.js.

Le concept est simple : au lieu d'installer 4 services différents (Umami pour les stats, Uptime Kuma pour la dispo, Prometheus pour le serveur, Typeform pour les sondages), **Tianji regroupe tout**. C'est lightweight, c'est open-source sous licence Apache 2.0, et ça s'installe en 5 minutes avec Docker.

> 💡 **Astuce** : tu peux tester Tianji sans rien installer sur [tianji.dev](https://tianji.dev). L'instance de démo est ouverte, tu as accès à tous les modules.

---

## Les 4 piliers de Tianji

### 1. Website Analytics

Le cœur du produit. Un script léger à intégrer dans ton HTML : **pas de cookie, pas de bannière RGPD nécessaire**. Tianji traque les pages vues, les referrers, les navigateurs, les pays, les devices. Le dashboard est épuré, lisible en 10 secondes. Pas de funnel analytics, pas de cohortes, pas de ML-driven insights bullshit. **Juste les données qui comptent.**

### 2. Uptime Monitor

Tu peux monitorer la disponibilité de tes sites et services. Ping HTTP, checks TCP, notifications quand ça tombe. C'est moins complet qu'un Uptime Kuma configuré à fond, mais pour surveiller 5-10 endpoints, **c'est largement suffisant**, et c'est dans la même interface.

### 3. Server Status

Un agent léger à installer sur tes serveurs pour remonter la charge CPU, la RAM, le disk usage, la latence réseau. Inspiré de Prometheus/Grafana mais **sans la complexité**. Tu vois l'état de tes VPS en temps réel dans le même dashboard que tes stats web.

### 4. Surveys & Telemetry

Tianji intègre un système de sondages et un module telemetry (pour les projets open-source qui veulent savoir combien de gens déploient leur app). C'est niche, mais **hyper pratique** si tu développes un SaaS ou un outil à héberger soi-même.

Bonus : il y a aussi le **Lighthouse report** intégré, des **webhooks**, du suivi **UTM**, et une **API ouverte** pour brancher tes propres outils.

---

## Pourquoi je préfère Tianji à Google Analytics

### Privacy native

Tianji analytics est **self-hosted**. Tes données restent sur ton serveur. Pas de Google qui les récupère pour alimenter ses profils publicitaires. Pas de cookie tiers. **Pas de bannière de consentement** sur ton site. Tu ne partages rien avec personne. Le RGPD devient un non-sujet.

### All-in-One

Avant Tianji, mon stack monitoring ressemblait à ça :
- Umami pour les stats
- [Uptime Kuma](/uptime-kuma-2-0-monitoring-auto-heberge/) pour la dispo
- Netdata pour le serveur
- 3 dashboards, 3 logins, 3 containers Docker

Avec Tianji, **c'est un seul container**. Un seul login. Un seul dashboard. Je gagne du temps, de la RAM, et surtout du mental load.

### Interface lisible

Le dashboard Tianji est fait pour des humains. Tu ouvres la page, tu vois immédiatement :
- Combien de visites aujourd'hui
- Quelles pages sont populaires
- Si tes serveurs sont up
- Si ton site est lent

**Pas besoin d'un master en data science.**

### Stack moderne et maintenue

TypeScript, Prisma, Next.js : c'est du code propre, documenté, avec une CI qui tourne. Les releases sortent régulièrement. La communauté est active sur GitHub. Ce n'est pas un projet mort depuis 2022.

### Gratuit

C'est open-source Apache 2.0. **Zéro coût**, zéro freemium, zéro "upgrade to Pro pour voir les données de plus de 30 jours".

---

## La mise en place (spoiler : c'est rapide)

Tianji analytics s'installe avec Docker Compose. Si tu débutes avec Docker, jette un œil à mon [guide Docker pour débutants](/docker-debutant-services-auto-heberger/) avant de continuer. Sinon, voilà un `docker-compose.yml` minimaliste, deux services : l'app et une base PostgreSQL.

```yaml
version: '3'
services:
  tianji:
    image: moonrailgun/tianji
    ports:
      - "12345:12345"
    environment:
      DATABASE_URL: postgresql://tianji:tianji@postgres:5432/tianji
      JWT_SECRET: ta-cle-aleatoire
      ALLOW_REGISTER: "false"
    depends_on:
      - postgres
    restart: always
  postgres:
    image: postgres:15.4-alpine
    environment:
      POSTGRES_DB: tianji
      POSTGRES_USER: tianji
      POSTGRES_PASSWORD: tianji
    volumes:
      - tianji-db-data:/var/lib/postgresql/data
    restart: always
volumes:
  tianji-db-data:
```

Tu changes le `JWT_SECRET`, tu lances `docker compose up -d`, et tu accèdes à `http://ton-vps:12345`. **C'est tout.** Pas de configuration Cloud complexe, pas de compte Google à créer.

> ⚠️ **Attention** : change le `JWT_SECRET` par une vraie clé aléatoire avant de déployer (`openssl rand -hex 32` fait le boulot). La valeur de l'exemple est publique : n'importe qui peut usurper ta session si tu la gardes.

Alternative si tu veux zéro config : déploiement one-click sur [Hostinger](https://www.hostinger.com/vps/docker-hosting?compose_url=https://github.com/msgbyte/tianji/), [Sealos](https://cloud.sealos.io/?openapp=system-template%3FtemplateName%3Dtianji) ou [RepoCloud](https://repocloud.io/details/?app_id=270).

---

## Les limites (parce qu'il faut être honnête)

Tianji n'est **pas un remplaçant 1:1 de Google Analytics 4**. Si tu as besoin de :
- Attribution multi-canal avancée
- Audiences remarketing
- Intégration Google Ads / Search Console
- Funnels de conversion complexes
- Prédiction ML du churn

...alors GA4 (ou Mixpanel, Amplitude) reste pertinent.

Mais pour **un blog, un site vitrine, un portfolio, un petit SaaS** ? Tianji couvre 95% des besoins, sans la charge mentale et l'overhead privacy de Google.

---

## FAQ

### Tianji est-il gratuit ?

Oui, c'est open-source sous licence Apache 2.0 et totalement gratuit en self-hosted.

### Faut-il des compétences techniques pour utiliser Tianji ?

Un minimum. Le déploiement se fait via Docker, donc il faut savoir manipuler un VPS et un docker-compose.

### Tianji remplace-t-il vraiment Google Analytics ?

Pour le suivi de base des visiteurs, oui. Pour les fonctionnalités avancées GA4 (attribution, audiences, remarketing), c'est plus limité, mais souvent suffisant pour un blog ou un site vitrine.

### Quelles sont les différences avec Umami ?

Tianji est inspiré d'Umami mais intègre en plus l'uptime monitoring, le server status, les surveys et le telemetry. C'est un hub tout-en-un, pas juste de l'analytics.

---

## Conclusion

Si tu en as marre du bloat de Google Analytics, des bannières de cookies, et du tracking invasif, **Tianji analytics est une option solide**. C'est pas parfait, c'est pas aussi puissant que GA4, mais c'est **100x plus agréable à utiliser** au quotidien.

Et le fait que ce soit self-hosted, privacy-friendly, et tout-en-un ? Ça fait toute la différence.

Tu peux tester la démo sur [tianji.dev](https://tianji.dev) et installer ton instance depuis [GitHub](https://github.com/msgbyte/tianji). Ça prend littéralement 10 minutes.

---

## Pour aller plus loin

- [Uptime Kuma 2.0 : le monitoring auto-hébergé qui remplace les services payants](/uptime-kuma-2-0-monitoring-auto-heberge/)
- [Docker pour les débutants : 10 services essentiels à auto-héberger](/docker-debutant-services-auto-heberger/)
- [Pourquoi j'ai quitté Google (et comment tu peux faire pareil)](/quitter-google-auto-hebergement/)
