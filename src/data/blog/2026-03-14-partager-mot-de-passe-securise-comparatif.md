---
title: "Partager un mot de passe en toute sécurité : Password.link vs OneTimeSecret vs PrivateBin (2025)"
pubDatetime: "2026-03-14T00:00:00+00:00"
author: Brandon Visca
description: "Tu envoies encore des mots de passe par Slack ou email ? Mauvaise idée. J'ai comparé Password.link, OneTimeSecret et PrivateBin pour trouver la meilleur..."
tags:
  - securite
  - password
  - outils
  - auto-hebergement
  - comparatif
draft: false
---

T'as déjà envoyé un mot de passe par Slack ou par email ? On l'a tous fait. Et on l'a tous regretté — ou on devrait.

Le problème : ces messages restent dans des historiques, des serveurs de messagerie, des logs. Quelqu'un qui accède à la boîte mail de ton collègue six mois plus tard peut toujours lire le mot de passe root de ton serveur. Sympa.

La solution ? Des **liens auto-destructeurs** : tu crées un lien chiffré qui s'efface dès qu'il est ouvert. Une lecture, et c'est mort. J'ai testé les trois principales options — **Password.link**, **OneTimeSecret** et **PrivateBin** (auto-hébergé) — pour te dire laquelle colle à ton usage.


## TL;DR — Le comparatif en un coup d'œil

| Critère | Password.link | OneTimeSecret | PrivateBin |
|---|---|---|---|
| **Prix (gratuit)** | 8 secrets/mois | Illimité | Gratuit (self-hosted) |
| **Chiffrement** | AES-256-GCM (client-side) | TLS + stockage chiffré | AES-256 (zéro connaissance) |
| **Self-hosted** | ❌ Non | ✅ Oui (open source) | ✅ Oui (open source) |
| **Pièces jointes** | ✅ (plans payants) | ❌ | ✅ |
| **Notifications** | ✅ (Slack, webhook, email) | ❌ | ❌ |
| **API REST** | ✅ | ✅ | ✅ |
| **Facilité** | 🟢 Très simple | 🟢 Simple | 🟡 Installation requise |
| **Idéal pour** | Équipes IT, pros | Particuliers, devs | Homelabbers, paranos 🙂 |

**Mon verdict rapide :**
- **Usage ponctuel, solo** → OneTimeSecret (gratuit illimité)
- **Équipe IT qui veut des notifs** → Password.link
- **Tu veux tout contrôler** → PrivateBin en self-hosted

## Table of content



## Pourquoi tu NE dois plus envoyer des credentials par email

Avant de rentrer dans le vif, petit rappel utile.

Quand tu envoies un mot de passe par email ou Slack :
- Il est stocké sur les serveurs de ta messagerie
- Il peut trainer dans des exports de logs
- Il est visible dans l'historique de conversation
- Il peut être indexé par des outils de backup

Un lien auto-destructeur règle tout ça : **une seule lecture, puis effacement définitif**. Même si quelqu'un intercepte le lien après coup, il ne voit qu'une page "secret déjà consulté".

Si tu gères des mots de passe au quotidien, jette aussi un œil à mon article sur [Vaultwarden, le gestionnaire de mots de passe auto-hébergé](https://brandonvisca.com/vaultwarden-docker-gestionnaire-mots-de-passe/). C'est complémentaire : Vaultwarden pour le stockage long terme, un lien auto-destructeur pour le partage ponctuel.



## Password.link — Le plus complet pour les équipes

Password.link existe depuis 2016. C'est l'un des rares services du genre à proposer un chiffrement **côté client** (dans le navigateur) avant même que les données touchent leurs serveurs. En clair : même eux ne peuvent pas lire tes secrets.

### ✅ Ce que j'ai apprécié

**Chiffrement sérieux.** Le processus génère deux clés aléatoires de 18 caractères dans le navigateur. La clé publique est embarquée dans le lien, la clé privée part côté serveur. Sans les deux, impossible de déchiffrer. Pas de JavaScript externe non plus — pas de risque d'injection de script malveillant.

**Les notifications.** C'est là que Password.link se distingue vraiment. Tu sais exactement quand ton lien a été ouvert — via email, Slack ou webhook. Utile quand tu envoies des credentials à un client et que tu veux confirmer qu'il les a bien reçus.

**Secret Request.** Fonctionnalité intéressante : tu envoies un lien à quelqu'un pour qu'il te transmette *ses* infos sensibles de manière sécurisée. Pratique pour les onboardings.

**Géo-blocking et whitelist IP.** Sur les plans payants, tu peux restreindre l'accès à certains pays ou adresses IP. Niveau paranoïa : élevé (mais dans le bon sens).

### ✗ Les limites

**Le plan gratuit est très restrictif.** 8 secrets par mois, c'est vite atteint si tu travailles en équipe. Après ça, il faut sortir la carte bancaire.

**Pas de self-hosting.** Tu fais confiance à leur infra. Ils ont l'air sérieux (conformité GDPR, no-logging), mais pour les entreprises avec des exigences strictes, ça peut bloquer.

**Les prix montent vite.** Basic à 40$/mois pour 100 secrets, c'est honnête pour une équipe. Mais le plan Pro à 85$/mois pour 1 000 secrets, c'est clairement un positionnement entreprise.

### 💰 Tarifs (vérifiés en mars 2026)

| Plan | Prix | Secrets/mois | Équipe |
|---|---|---|---|
| Free | 0$ | 8 | 1 |
| Basic | 40$/mois | 100 | 5 |
| Advanced | 65$/mois | 400 | 10 |
| Pro | 85$/mois | 1 000 | 20 |

> Tous les prix hors TVA. Paiement via Chargebee.

### 🎯 Idéal pour

Les équipes IT qui ont besoin de traçabilité : savoir *qui* a ouvert *quoi* et *quand*. Aussi parfait pour les freelances et prestataires qui gèrent des credentials clients.


## OneTimeSecret — Le vétéran open source

OneTimeSecret c'est la référence historique du secteur. Open source depuis le départ, auto-hébergeable, et la version gratuite est **vraiment gratuite** — pas de limite de secrets.


### ✅ Ce que j'ai apprécié

**Gratuit sans limite.** Le plan Basic est à 0€/mois et permet de créer autant de secrets que tu veux. Pas de quota, pas de frein. Pour un usage personnel ou d'une petite équipe, c'est imbattable.

**Open source et auditable.** Le code est disponible sur GitHub (2,7k stars). Tu peux vérifier exactement ce qui se passe avec tes données. C'est une garantie de transparence que les solutions propriétaires ne peuvent pas offrir.

**Choix de la région.** Serveurs EU ou US selon tes contraintes RGPD. Pour une entreprise française, pouvoir choisir l'hébergement EU c'est un vrai plus.

**Self-hosting possible.** Si tu veux aller plus loin, tu peux déployer ta propre instance. On y revient dans la section PrivateBin, mais c'est une option viable pour les homelabbers.

### ✗ Les limites

**Interface un peu datée.** Ça marche, mais c'est pas ce qu'on appelle une expérience utilisateur moderne. Password.link est clairement plus soigné visuellement.

**Pas de notifications.** Contrairement à Password.link, tu ne sais pas si ton destinataire a ouvert le lien. Pour un usage critique, c'est un vrai manque.

**Pas de pièces jointes.** Texte uniquement. Si tu dois partager un fichier de configuration ou une clé SSH complète, il faudra coller le contenu directement.

**Plan payant limité.** L'Identity Plus à 35€/mois débloque les domaines custom et le branding. Mais il manque les fonctionnalités avancées (notifications, API étendue) que Password.link propose.

### 💰 Tarifs (vérifiés en mars 2026)

| Plan | Prix | Domaines custom | Expiration |
|---|---|---|---|
| Basic | 0€/mois | 1 inclus | 14 jours max |
| Identity Plus | 35€/mois | Illimités | 30 jours max |

> Données hébergées en EU par défaut. Option US disponible.

### 🎯 Idéal pour

Les devs et sysadmins solo qui veulent un outil gratuit, fiable et sans prise de tête. Aussi excellent pour les entreprises qui ont besoin d'un hébergement EU et d'un audit de code possible.


## PrivateBin — Le choix des self-hosters

PrivateBin, c'est l'option pour ceux qui ne font confiance à personne — y compris aux hébergeurs. Le principe : **chiffrement zéro-connaissance** dans le navigateur, le serveur ne voit jamais le contenu en clair.

💡 **À savoir :** PrivateBin n'est pas un SaaS, c'est une application à déployer soi-même. Si tu n'as pas de serveur ou d'infra homelab, passe ton chemin — ou lis la suite quand même pour la culture.

### ✅ Ce que j'ai apprécié

**Zéro confiance requise.** La clé de déchiffrement ne transite jamais par le serveur. Elle est stockée dans le fragment d'URL (après le `#`), que le navigateur ne transmet pas au serveur. Techniquement, même toi tu ne peux pas lire ce que tu héberges.

**Pièces jointes chiffrées.** Tu peux joindre des fichiers. Chiffrés, évidemment.

**Discussions chiffrées.** PrivateBin propose aussi un mode "discussion" — comme Password.link, mais en self-hosted.

**Déploiement Docker simple.**

```bash
docker run -d \
  --name privatebin \
  -p 8080:8080 \
  -v ./data:/srv/data \
  privatebin/nginx-fpm-alpine
```

C'est tout. Accès sur `http://localhost:8080`. Configure un reverse proxy nginx devant et c'est propre.

### ✗ Les limites

**Tu gères tout toi-même.** Mises à jour, sauvegardes, disponibilité. Si ton serveur tombe, ton service tombe. C'est le deal habituel du self-hosting.

**Pas de notifications.** Comme OneTimeSecret, tu ne sais pas si le lien a été ouvert.

**Pas d'interface de gestion.** Pas de dashboard, pas d'historique. C'est by design — mais ça peut déranger en contexte professionnel.

### 💰 Tarifs

**Gratuit.** Open source (licence Zlib). Tu paies uniquement ton hébergement.

Un VPS à 5-6€/mois suffit largement. Si tu as déjà un homelab avec un reverse proxy, le coût marginal est zéro.

### 🎯 Idéal pour

Les homelabbers et les admins qui veulent contrôle total et confidentialité maximale. Aussi parfait pour les entreprises avec des politiques strictes "pas de SaaS tiers pour les credentials".

⚠️ **Attention :** Si tu déploies PrivateBin en self-hosted, assure-toi de configurer HTTPS correctement. Un lien auto-destructeur sur HTTP, c'est un peu comme une porte blindée avec une fenêtre ouverte à côté.


## Le verdict : qui doit utiliser quoi ?


**Choisis Password.link si :**
- Tu travailles en équipe et tu as besoin de savoir qui a ouvert quoi
- Tu envoies régulièrement des credentials à des clients
- Tu veux des notifications Slack ou webhook intégrées
- Tu peux justifier 40-85$/mois selon la taille de l'équipe

**Choisis OneTimeSecret si :**
- Tu veux un outil gratuit, sans limite, sans friction
- Tu cherches une option open source avec hébergement EU
- Tu n'as pas besoin de notifications
- Tu veux pouvoir auditer le code ou self-héberger plus tard

**Choisis PrivateBin si :**
- Tu as déjà un homelab ou un serveur
- Tu veux un contrôle total sur tes données
- Ta politique interne interdit les SaaS tiers pour les credentials
- Tu as besoin de partager des fichiers chiffrés


## FAQ

**Est-ce que ces services chiffrent vraiment mes données ?**

Password.link et PrivateBin font du chiffrement côté client (dans le navigateur), ce qui signifie que le serveur ne voit jamais le contenu en clair. OneTimeSecret chiffre les données au repos, mais la clé est gérée côté serveur — c'est moins strict techniquement, mais suffisant pour la grande majorité des usages.

**Que se passe-t-il si mon destinataire n'ouvre pas le lien avant expiration ?**

Le secret est automatiquement effacé à l'expiration. Aucun accès n'est possible, même par les équipes de ces services. Pense à vérifier avec ton destinataire qu'il a bien reçu le lien.

**Puis-je protéger le lien par un mot de passe supplémentaire ?**

Oui, les trois solutions permettent d'ajouter un mot de passe d'accès. C'est une double protection utile : même si le lien est intercepté, il faut connaître le mot de passe pour le déchiffrer.

**OneTimeSecret est-il vraiment gratuit ?**

Oui, le plan Basic d'OneTimeSecret est gratuit sans restriction de volume. Tu peux créer autant de secrets que tu veux. Le plan payant (35€/mois) n'est utile que si tu veux des domaines custom ou du branding.

**Peut-on utiliser ces outils sans créer de compte ?**

Pour Password.link et OneTimeSecret, tu peux créer des secrets sans compte (avec des limitations). PrivateBin ne nécessite aucun compte par design.


## Conclusion

Envoyer un mot de passe par Slack ou email en 2025, c'est comme laisser ta clé sous le paillasson. Ça marche... jusqu'au jour où ça ne marche plus.

Les trois outils présentés ici règlent le problème proprement :
- **OneTimeSecret** pour commencer sans payer
- **Password.link** pour les équipes qui ont besoin de traçabilité
- **PrivateBin** pour les homelabbers qui veulent tout contrôler

Et si tu veux aller plus loin dans la sécurisation de tes mots de passe au quotidien, l'étape suivante c'est un gestionnaire dédié. Mon article sur [Vaultwarden Docker](https://brandonvisca.com/vaultwarden-docker-gestionnaire-mots-de-passe/) te montre comment déployer ta propre instance en moins d'une heure.

## Articles connexes

- [Partager un mot de passe en toute sécurité : Password.link v](/partager-mot-de-passe-securise-comparatif/)
- [Vaultwarden avec Docker : Gestionnaire de Mots de Passe Grat](/vaultwarden-docker-gestionnaire-mots-de-passe/)
