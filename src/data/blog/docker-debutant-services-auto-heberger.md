---
title: "Docker pour les débutants : 10 services essentiels à auto-héberger en 2025"
pubDatetime: "2025-10-22T16:12:41+02:00"
description: "Docker pour débutants : guide simple avec 10 services prêts à déployer. Exemples docker-compose inclus, zéro prise de tête !"
tags:
  - docker
  - auto-hebergement
  - homelab
  - linux
  - guide
  - debutant
faqs:
  - question: "Docker vs LXC vs VM, quelle différence ?"
    answer: "Docker : conteneurs applicatifs ultra-légers. LXC : conteneurs système (mini-VMs). VM : machine virtuelle complète avec OS, très lourd."
  - question: "Mes conteneurs Docker utilisent beaucoup de RAM, c'est normal ?"
    answer: "Docker alloue la RAM par conteneur. Solution : limiter la RAM par conteneur (mem_limit), utiliser des images alpine, ou fermer les services inutilisés."
  - question: "Puis-je faire tourner Docker sur un Raspberry Pi ?"
    answer: "Oui. Beaucoup d'images disponibles en architecture ARM. Services lourds (Jellyfin avec transcodage) limités, mais Nextcloud/Vaultwarden tournent parfaitement."
  - question: "Comment migrer mes conteneurs Docker vers un autre serveur ?"
    answer: "Arrêter les conteneurs (docker compose down), copier le dossier docker vers le nouveau serveur, relancer (docker compose up -d)."
---

Tu as entendu parler de Docker partout. « C’est l’avenir », « Tous les devs l’utilisent », « Tu devrais apprendre Docker ».

Mais quand tu cherches des tutos, tu tombes sur des explications cryptiques avec des schémas de conteneurs, d’images, de volumes, et tu te demandes pourquoi faire simple quand on peut faire compliqué ?

**Bonne nouvelle :** Docker, c’est en fait super simple. Et dans cet article, on va le prouver en déployant 10 services concrets en quelques lignes de commandes.

Pas de théorie inutile. Que du concret.

---

## Table des matières

TL;DR : Docker en 3 phrases
---

- **C’est quoi ?** Une façon de lancer des applications dans des « boîtes » isolées
- **Pourquoi ?** Installation en 2 minutes, pas de conflit entre logiciels, facile à supprimer
- **Comment ?** Un fichier `docker-compose.yml` + une commande = service opérationnel

---
