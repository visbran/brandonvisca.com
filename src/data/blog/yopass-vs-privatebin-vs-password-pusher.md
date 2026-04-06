---
title: "Yopass vs PrivateBin vs Password Pusher : lequel choisir ? (2025)"
description: "Partager un mot de passe sécurisé depuis ton homelab : Yopass, PrivateBin ou Password Pusher ? Comparatif complet pour choisir lequel auto-héberger."
pubDatetime: 2026-03-14 00:00:00+01:00
author: Brandon Visca
tags:
  - securite
  - homelab
  - docker
  - auto-hebergement
  - intermediaire
featured: false
draft: false
focusKeyword: partager un mot de passe sécurisé
faqs:
  - question: "Quelle différence principale entre Yopass et PrivateBin ?"
    answer: "Yopass est minimaliste : idéal pour les secrets courts (mots de passe, tokens). PrivateBin supporte de longs textes, du code, des fichiers joints et offre plus d'options d'expiration."
  - question: "Password Pusher est-il adapté à un homelab ?"
    answer: "Oui, il se déploie en Docker en 5 minutes avec une interface soignée. Son inconvénient : chiffrement côté serveur (moins sécurisé que Yopass/PrivateBin qui chiffrent côté client)."
  - question: "Peut-on partager des fichiers avec ces outils ?"
    answer: "Yopass et PrivateBin supportent les pièces jointes. Password Pusher est limité au texte uniquement."
  - question: "Lequel choisir sans homelab ?"
    answer: "Utilise yopass.se (instance publique officielle) ou onetimesecret.com directement depuis le navigateur. Aucune installation requise, fonctionnel en 30 secondes."
---
# Yopass vs PrivateBin vs Password Pusher : lequel choisir? (2025)

Tu envoies encore des mots de passe par Slack ou par email ? Vas-y, continue. Et pendant que tu lis ce message, quelqu'un d'autre lit peut-être aussi ton historique de messages.

Le problème, c'est que tout le monde le fait. Le stagiaire qui arrive lundi, le client à qui tu livres un accès serveur, le collègue qui a besoin du compte admin en urgence. Et la réponse par défaut c'est toujours la même : un message Slack avec le mot de passe en clair, un email, ou pire — un Google Doc "partagé en privé".

Il existe des outils conçus exactement pour ça : partager un secret **une seule fois**, chiffré, avec autodestruction. J'ai testé les trois principaux — Yopass, PrivateBin et Password Pusher — pour te dire lequel mérite une place dans ton homelab.

Spoiler : Yopass pour 80% des cas. Mais ça dépend de ton contexte.

---

## 📑 Table des matières

1. [TL;DR — Tableau comparatif](#tldr-tableau-comparatif)
2. [Le vrai problème : pourquoi Slack et email c'est une mauvaise idée](#le-vrai-problème-pourquoi-slack-et-email-cest-une-mauvaise-idée)
3. [Yopass : la solution minimaliste qui fait le job](#yopass-la-solution-minimaliste-qui-fait-le-job)
4. [PrivateBin : le champion du zero-knowledge](#privatebin-le-champion-du-zero-knowledge)
5. [Password Pusher : l'option pour les équipes](#password-pusher-loption-pour-les-équipes)
6. [Le verdict : qui pour qui ?](#le-verdict-qui-pour-qui)
7. [FAQ](#faq)
8. [Conclusion](#conclusion)

## TL;DR — Tableau comparatif

| Critère                | Yopass                | PrivateBin       | Password Pusher        |
| ---------------------- | --------------------- | ---------------- | ---------------------- |
| **Chiffrement**        | AES côté client       | AES côté client  | Côté serveur           |
| **Autodestruction**    | ✅ 1h / 1j / 1 semaine | ✅ Configurable   | ✅ Par vues et/ou durée |
| **Partage fichiers**   | ✅                     | ✅                | ❌                      |
| **Interface**          | 🟢 Minimaliste        | 🟡 Sobre         | 🟢 Propre              |
| **Backend requis**     | Memcached ou Redis    | Aucun (fichiers) | BDD (SQLite/Postgres)  |
| **CLI dispo**          | ✅                     | ❌                | ❌                      |
| **Déploiement Docker** | ✅ Simple              | ✅ Simple         | ✅ Simple               |
| **Licence**            | Apache 2.0            | zlib/libpng      | GPL-3.0                |

**Mon choix par cas d'usage :**
- 🏆 **Usage général / homelab** → Yopass (simplicité + CLI)
- 🔒 **Besoin de zero-knowledge strict** → PrivateBin (zéro dépendance externe)
- 👥 **Équipe + stats d'utilisation** → Password Pusher (audit + comptes)


---

## Le vrai problème : pourquoi Slack et email c'est une mauvaise idée

Avant de comparer les outils, petit rappel de pourquoi tu lis cet article.

Quand tu envoies un mot de passe par messagerie instantanée ou par email :

- Il est **stocké en clair** dans l'historique des messages (souvent des années)
- Il est **indexé** par les serveurs de la plateforme (Slack, Google, Microsoft)
- Il peut être **compromis si le compte est piraté** bien après l'envoi
- Il est **visible par les admins** de la plateforme que tu utilises
- Il peut se **retrouver dans des exports** ou des backups que tu ne contrôles pas

La bonne pratique c'est simple : un secret partagé doit **s'autodétruire après lecture**. Et si possible, être **chiffré côté client** pour que même l'hébergeur ne puisse pas le lire.

C'est exactement ce que font ces trois outils.

⚠️ **Attention** : Ces outils ne remplacent pas un gestionnaire de mots de passe comme [Vaultwarden pour stocker tes mots de passe](https://brandonvisca.com/vaultwarden-docker-gestionnaire-mots-de-passe/) au quotidien. Ils servent uniquement à la **transmission ponctuelle** d'un secret vers quelqu'un d'autre.

---

## Yopass : la solution minimaliste qui fait le job

Yopass existe depuis 2014. C'est un projet Go open source (Apache 2.0), maintenu activement, avec 2600+ étoiles sur GitHub. L'idée est ultra-simple : tu colles ton secret, tu choisis une durée d'expiration, tu récupères un lien à usage unique.

### ✅ Points forts

**Le chiffrement se fait dans ton navigateur.** La clé de déchiffrement est intégrée dans le fragment URL (`#clé`), ce qui signifie qu'elle n'est **jamais envoyée au serveur**. Même si quelqu'un compromet l'instance Yopass que tu héberges, il ne peut pas lire les secrets en transit.

**Une CLI disponible.** C'est le seul des trois à proposer une interface en ligne de commande. Très utile pour automatiser l'envoi d'un secret depuis un script :

```bash
# Envoyer un secret depuis stdin
printf 'mon-mot-de-passe-super-secret' | yopass

# Partager un fichier entier
yopass --file /path/to/secret.conf

# Valable 1 jour, plusieurs lectures possibles
cat secret.txt | yopass --expiration=1d --one-time=false
```

**Le déploiement Docker est trivial.** Avec Memcached ou Redis en backend, ça tourne en 2 minutes.

**Aucun compte requis.** Ni pour créer, ni pour lire. Zéro friction pour le destinataire.

### ✗ Points faibles

- Backend obligatoire (Memcached ou Redis) — une dépendance de plus à gérer
- Interface vraiment très minimaliste (certains trouveront ça austère)
- Pas de statistiques d'utilisation ni de tableau de bord
- Durées d'expiration limitées à 1h / 1j / 1 semaine (pas de durée personnalisée)

### 💰 Prix réel

Gratuit et open source. Sur un VPS à 3-5€/mois, Yopass + Memcached consomme environ 30-50 Mo de RAM. Rien.

### 🎯 Cas d'usage idéal

Partage de mots de passe en équipe tech, intégration dans des scripts CI/CD, homelab personnel. Si tu veux de la simplicité sans te prendre la tête, c'est l'option par défaut.


### 🐳 Docker Compose Yopass (production-ready)

```yaml
services:
  yopass:
    image: jhaals/yopass:latest
    container_name: yopass
    restart: unless-stopped
    command: ["--database=memcached", "--memcached=memcached:11211", "--port=1337"]
    ports:
      - "127.0.0.1:1337:1337"
    depends_on:
      - memcached
    networks:
      - yopass-net

  memcached:
    image: memcached:alpine
    container_name: yopass-memcached
    restart: unless-stopped
    networks:
      - yopass-net

networks:
  yopass-net:
    driver: bridge
```

> Ensuite, pointe ton reverse proxy (Nginx, Caddy, Traefik) vers `127.0.0.1:1337`. Ajoute un certificat TLS — sans HTTPS, la clé de chiffrement dans l'URL se baladerait en clair.

💡 **Astuce** : Tu peux remplacer Memcached par Redis en changeant `--database=redis --redis=redis://redis:6379/0`. Redis a l'avantage de persister les données en cas de redémarrage — pratique si tu veux que les secrets avec expiration d'1 semaine survivent à un reboot.

---

## PrivateBin : le champion du zero-knowledge

PrivateBin, c'est l'héritier spirituel de ZeroBin. Même philosophie mais mieux maintenu, avec plus de fonctionnalités. Son argument principal : **zéro dépendance externe**. Pas de Redis, pas de Memcached — juste des fichiers plats (ou SQLite/MySQL si tu veux).

### ✅ Points forts

**Architecture vraiment zero-knowledge.** Comme Yopass, le chiffrement se fait côté navigateur avec AES-256 GCM. La clé n'est jamais transmise au serveur. Mais PrivateBin va plus loin : il chiffre aussi les **métadonnées** (heure de création, adresse IP du créateur, etc.).

**Aucune dépendance externe requise.** Un simple serveur PHP + stockage fichiers et c'est parti. Idéal si tu veux minimiser la surface d'attaque.

**Plus qu'un simple partage de mots de passe.** PrivateBin gère aussi le Markdown, la coloration syntaxique, et les discussions (style pastebin collaboratif). Utile pour partager des configs ou des scripts confidentiels.

**Durée d'expiration ultra-flexible.** De 5 minutes à 1 an, avec des options précises.

### ✗ Points faibles

- Pas de CLI — tout passe par l'interface web
- Interface un peu moins polie que Yopass ou Password Pusher
- Le mode "discussion" peut être déroutant pour un usage simple de partage de secret
- Configuration PHP à gérer si tu n'es pas à l'aise avec ça

### 💰 Prix réel

Gratuit, open source (zlib/libpng). Consommation mémoire quasi nulle — PHP + fichiers plats.

### 🎯 Cas d'usage idéal

Si tu as des **exigences de confidentialité élevées** (secteur médical, juridique, financier) ou si tu veux partager plus que des mots de passe (configs, clés SSH, certificats). PrivateBin est aussi le choix logique si tu n'as pas envie de gérer un service supplémentaire (Redis/Memcached).

### 🐳 Docker Compose PrivateBin

```yaml
services:
  privatebin:
    image: privatebin/nginx-fpm-alpine:latest
    container_name: privatebin
    restart: unless-stopped
    volumes:
      - privatebin-data:/srv/data
    ports:
      - "127.0.0.1:8080:8080"

volumes:
  privatebin-data:
```


---

## Password Pusher : l'option pour les équipes

Password Pusher (anciennement "pwpush.com") c'est une autre approche. Ici, l'accent est mis sur **l'expérience utilisateur** et les fonctionnalités orientées équipe : comptes utilisateurs, historique, statistiques, audit trail.

### ✅ Points forts

**Expiration par nombre de vues.** Tu peux définir qu'un secret expire après exactement 3 consultations, peu importe la durée. Très pratique si tu ne sais pas quand le destinataire va ouvrir le lien.

**Comptes utilisateurs et historique.** Tu peux voir tous les secrets que tu as créés, savoir s'ils ont été consultés, et les révoquer manuellement.

**Interface soignée.** C'est probablement l'interface la plus accessible des trois pour des utilisateurs non-techniques.

**Tableau de bord d'administration.** Si tu déploies ça pour une équipe entière, tu as une visibilité sur l'utilisation.

**Support des fichiers et des URLs.** En plus des textes, tu peux pousser des URLs à usage unique.

### ✗ Points faibles

- **Le chiffrement se fait côté serveur**, pas côté client. C'est la différence fondamentale avec Yopass et PrivateBin : l'hébergeur *peut* techniquement lire les secrets. Si tu héberges toi-même c'est OK, mais ça change l'équation de confiance.
- Plus lourd à déployer (Ruby on Rails + base de données)
- Consomme plus de ressources que les deux autres

### 💰 Prix réel

Gratuit et open source (GPL-3.0). Nécessite plus de RAM — prévoir 256-512 Mo pour Ruby on Rails + la base de données.

### 🎯 Cas d'usage idéal

Une équipe non-technique qui a besoin de partager des accès régulièrement, avec de la visibilité sur ce qui a été partagé. Si l'audit et l'historique comptent plus que le zero-knowledge strict, c'est le bon choix.

### 🐳 Docker Compose Password Pusher

```yaml
services:
  pwpush:
    image: pglombardo/pwpush:latest
    container_name: pwpush
    restart: unless-stopped
    environment:
      - DATABASE_URL=sqlite3:///app/db/pwpush.sqlite3
      - PWP__PW__EXPIRE_AFTER_DAYS_DEFAULT=7
      - PWP__PW__EXPIRE_AFTER_VIEWS_DEFAULT=5
    volumes:
      - pwpush-data:/app/db
    ports:
      - "127.0.0.1:5100:5100"

volumes:
  pwpush-data:
```

---

## Le verdict : qui pour qui ?

Voilà le moment de vérité.

**Choisis Yopass si :**
- Tu veux déployer ça rapidement sur ton homelab
- Tu as des scripts ou de l'automatisation (la CLI est un vrai plus)
- Tu gères la sécurité toi-même et tu veux du zero-knowledge
- Tu n'as pas besoin de comptes ou d'historique

**Choisis PrivateBin si :**
- Tu veux le maximum de confidentialité sans dépendance externe
- Tu partages autre chose que des mots de passe (configs, clés, scripts)
- Tu veux minimiser la surface d'attaque de ton infrastructure
- Tu as des contraintes réglementaires fortes (RGPD, secret professionnel)

**Choisis Password Pusher si :**
- Tu déploies pour une équipe entière, pas juste pour toi
- Des utilisateurs non-techniques doivent l'utiliser
- Tu veux un historique et la possibilité de révoquer des secrets
- Le zéro-knowledge strict n'est pas ton priorité principale

🔍 **À savoir** : les trois peuvent coexister sur le même serveur. Certains déploient Yopass pour usage quotidien et PrivateBin pour les cas nécessitant un niveau de confidentialité supérieur.


---

## FAQ

**Est-ce vraiment sécurisé d'envoyer un lien par email contenant la clé de déchiffrement ?**

Oui et non. Le lien contient la clé dans le fragment URL (`#`), qui n'est **jamais envoyé aux serveurs** ni loggué dans les accès HTTP. Mais si quelqu'un intercepte l'email avec le lien complet, il a accès au secret. La bonne pratique : envoie le lien par un canal, et confirme la réception par un autre canal avant que le secret s'autodétruise.

**Quelle différence entre chiffrement côté client et côté serveur ?**

Côté client (Yopass, PrivateBin) : le chiffrement se fait dans ton navigateur. Le serveur ne voit jamais le contenu en clair — même toi, si tu héberges l'instance, tu ne peux pas lire les secrets. Côté serveur (Password Pusher) : le serveur chiffre les données, mais la clé est aussi sur le serveur. Si quelqu'un compromet le serveur, il peut potentiellement accéder aux secrets.

**Ces outils remplacent-ils un gestionnaire de mots de passe ?**

Non, pas du tout. Pour stocker et accéder à tes mots de passe au quotidien, utilise un gestionnaire dédié comme [Vaultwarden pour stocker tes mots de passe](https://brandonvisca.com/vaultwarden-docker-gestionnaire-mots-de-passe/). Ces outils servent uniquement à la **transmission ponctuelle** d'un secret vers quelqu'un d'autre.

**Peut-on avoir plusieurs de ces services en même temps ?**

Oui, ils ne rentrent pas en conflit. Ça fait un peu beaucoup pour un homelab solo, mais dans un contexte pro avec différents besoins, c'est tout à fait raisonnable.

**Yopass nécessite-t-il obligatoirement Memcached ?**

Non, tu peux aussi utiliser Redis (`--database=redis`). Redis a l'avantage de persister les données sur disque, ce qui évite de perdre les secrets en cours de validité si le service redémarre.

---

## Conclusion

Tu n'as plus d'excuse pour envoyer des mots de passe en clair. Ces trois outils sont gratuits, open source, et se déploient en moins de 5 minutes avec Docker.

Mon setup perso : Yopass sur mon homelab, avec la CLI intégrée dans mes scripts d'administration. Pour un partage one-shot rapide depuis le terminal, c'est imbattable.

Pour l'équipe : PrivateBin si la confidentialité prime, Password Pusher si l'expérience utilisateur et l'historique comptent davantage.

Et si tu veux aller plus loin dans la sécurisation de ton infrastructure, jette un œil à mon guide pour [durcir ton serveur Linux](https://brandonvisca.com/securite-de-votre-serveur-linux/) — parce qu'un secret bien partagé sur un serveur mal sécurisé, c'est un peu comme une porte blindée sur une maison sans toit.

---
