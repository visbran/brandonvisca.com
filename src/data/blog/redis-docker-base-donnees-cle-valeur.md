---
title: "Redis Docker : déployer une base de données clé-valeur ultra-rapide"
description: "Redis Docker en pratique : installation, docker-compose, persistance RDB/AOF, sécurité et cas d'usage cache/session pour ton homelab."
pubDatetime: "2026-09-28T11:02:11+02:00"
modDatetime: "2026-09-27T08:00:00.000Z"
author: Brandon
tags:
  - docker
  - base-de-donnees
  - intermediaire
featured: false
draft: false
focusKeyword: redis docker
faqs:
  - question: "Redis Docker perd-il mes données au redémarrage du container ?"
    answer: "Sans volume monté sur /data, oui, tout disparaît. Avec un volume et la persistance RDB ou AOF activée, tes données survivent aux redémarrages et aux mises à jour d'image."
  - question: "Combien de RAM consomme un container Redis Docker ?"
    answer: "Ça dépend entièrement du volume de données que tu stockes, mais le processus lui-même est très léger, quelques Mo à vide. Fixe une limite avec maxmemory pour éviter toute surprise."
  - question: "Faut-il exposer le port 6379 de Redis Docker sur internet ?"
    answer: "Non, jamais directement. Redis n'a pas été conçu pour affronter internet sans protection. Passe par un réseau Docker interne ou un tunnel type Tailscale/Cloudflare pour l'administration à distance."
---
> 💡 **TL;DR**
> - Redis Docker se lance en une commande, mais une vraie config passe par un `docker-compose.yml` avec volume et mot de passe.
> - La persistance se joue sur deux mécanismes complémentaires : les snapshots RDB et le journal AOF.
> - Jamais de port 6379 exposé sur internet sans mot de passe ni pare-feu, Redis n'a pas été pensé pour ça.

Tu cherches une base de données rapide pour du cache, des sessions ou des files d'attente, et le mot "Redis" revient dans toutes les conversations depuis dix ans. Normal, c'est devenu le couteau suisse de la donnée en mémoire. Et avec Docker, tu le déploies proprement, isolé, sans polluer ton système avec des dépendances. On va voir comment le monter correctement, pas juste avec un `docker run` qu'on oublie derrière soi.

## Table des matières

## Redis Docker : c'est quoi et pourquoi l'utiliser

Redis, c'est une base de données clé-valeur qui vit entièrement en mémoire. Pas de tables, pas de jointures SQL, juste des paires clé-valeur ultra rapides à lire et écrire. Tu stockes une session utilisateur, un compteur, une file de tâches, un résultat de requête coûteux à recalculer, et Redis te le ressort en microsecondes.

Chez moi, Redis Docker sert de couche cache devant plusieurs applis auto-hébergées : ça évite de retaper les mêmes requêtes lourdes en base et ça accélère franchement les temps de réponse. C'est aussi le backend de sessions de pas mal d'outils web, et la brique de base d'un système de files d'attente pour du traitement asynchrone.

Un point à connaître avant de te lancer : depuis la version 8.0, Redis est distribué sous triple licence, RSALv2, SSPLv1 ou AGPLv3. Les versions antérieures à 7.4 restaient en BSD 3 clauses, une licence open source classique. Ça ne change rien pour un usage perso ou homelab, mais si tu bosses dans une boîte qui redistribue du logiciel, c'est un point à vérifier avec ton service juridique.

L'image officielle sur Docker Hub couvre toutes les versions récentes, avec des variantes Debian et Alpine pour chaque release. C'est cette image qu'on va utiliser.

## Installation : lancer Redis Docker en une commande

Pour tester vite fait, une seule ligne suffit :

```bash
docker run -d --name redis -p 6379:6379 redis:8-alpine
```

Ça télécharge l'image, lance le container en arrière-plan et expose le port 6379 sur ta machine hôte. Tu peux vérifier que ça tourne avec `docker exec -it redis redis-cli ping`, qui doit te répondre `PONG`.

Le souci de cette commande, c'est qu'elle ne persiste rien et n'a aucun mot de passe. Utile pour un test de cinq minutes, dangereuse pour un vrai usage. On passe à la vraie config.

## Docker Compose : la configuration propre pour durer

Un `docker-compose.yml` te donne un déploiement reproductible, avec volume et réseau dédiés :

```yaml
services:
  redis:
    image: redis:8-alpine
    container_name: redis
    restart: unless-stopped
    command: redis-server --requirepass ${REDIS_PASSWORD} --appendonly yes --maxmemory 256mb --maxmemory-policy allkeys-lru
    ports:
      - "127.0.0.1:6379:6379"
    volumes:
      - redis-data:/data
    networks:
      - backend

volumes:
  redis-data:

networks:
  backend:
```

Quelques choix qui comptent dans ce fichier. Le port est mappé uniquement sur `127.0.0.1`, donc inaccessible depuis l'extérieur de la machine hôte, seuls les autres containers du réseau `backend` peuvent y accéder directement. Le `--requirepass` impose un mot de passe, à définir dans un fichier `.env` à côté du compose :

```bash
echo "REDIS_PASSWORD=$(openssl rand -base64 24)" > .env
```

`--maxmemory` fixe une limite dure, ici 256 Mo, et `--maxmemory-policy allkeys-lru` dit à Redis d'évincer les clés les moins récemment utilisées quand cette limite est atteinte, plutôt que de planter ou refuser les écritures. Pour un usage cache pur, c'est le comportement qu'on veut.

Lance le tout avec :

```bash
docker compose up -d
```

## Sécuriser ton Redis Docker

Redis part du principe qu'il tourne dans un environnement de confiance, pas exposé directement. Trois réflexes à avoir.

D'abord, jamais de port publié en `0.0.0.0` sur une interface publique. Si tu dois administrer Redis à distance, passe par un tunnel plutôt que d'ouvrir le port au monde entier, exactement le même principe que pour n'importe quel service admin de ton homelab avec [Cloudflare Tunnel](/cloudflare-tunnel-docker-homelab/).

Ensuite, mets toujours un mot de passe avec `requirepass`, même en interne. Un container compromis sur le même réseau Docker ne doit pas pouvoir vider ton cache ou lire tes sessions sans authentification.

Enfin, si ton serveur est accessible depuis internet pour d'autres services, une couche de détection d'intrusion en amont limite la casse en cas de scan ou de tentative de brute force sur tes ports ouverts, un rôle que joue bien [CrowdSec](/crowdsec-docker-securite-collaborative/) sur le reste de ta stack.

## Persistance des données : RDB, AOF et sauvegarde

Par défaut, Redis vit en mémoire. Sans configuration de persistance, un `docker restart` ou un crash te fait tout perdre. Deux mécanismes existent, et tu peux les combiner.

**RDB** (Redis Database) prend des snapshots complets de la mémoire à intervalles réguliers. Rapide à charger au redémarrage, mais tu perds les écritures survenues entre deux snapshots.

**AOF** (Append Only File) journalise chaque commande d'écriture au fil de l'eau. Plus robuste, moins de perte de données en cas de crash, mais le fichier grossit plus vite et le redémarrage est un peu plus lent le temps de rejouer le journal.

Dans l'exemple de compose plus haut, `--appendonly yes` active l'AOF. Pour du cache pur et rejouable depuis ta base principale, tu peux t'en passer et accepter la perte au redémarrage. Pour des données que tu ne veux pas recalculer, garde l'AOF actif.

Le volume `redis-data:/data` contient à la fois les fichiers RDB et AOF. Sauvegarde-le comme n'importe quel volume de données important, avec un outil qui gère le chiffrement et la rétention, par exemple [Duplicati](/duplicati-docker-sauvegarde/) pointé sur ce volume.

## Utiliser Redis : premières commandes avec redis-cli

Une fois le container up, connecte-toi avec le mot de passe défini :

```bash
docker exec -it redis redis-cli -a "$REDIS_PASSWORD"
```

Quelques commandes de base pour prendre en main la logique clé-valeur :

```bash
SET session:42 "utilisateur_connecte"
GET session:42
EXPIRE session:42 3600
TTL session:42
DEL session:42
```

`SET` et `GET` posent et lisent une valeur. `EXPIRE` fixe une durée de vie en secondes, pratique pour des sessions ou des tokens temporaires qui doivent s'auto-nettoyer. `TTL` te dit combien de temps il reste avant expiration, `DEL` supprime.

Pour des structures plus riches que de simples chaînes, Redis gère aussi des listes, des sets, des hash et des sorted sets nativement, sans bibliothèque tierce. Un `HSET` pour stocker un objet, un `LPUSH` pour une file d'attente, un `ZADD` pour un classement trié par score.

## Cas d'usage concrets pour ton homelab

Redis Docker trouve sa place dans plusieurs scénarios courants chez qui bricole son infra.

**Cache applicatif** : devant une appli qui interroge une base SQL lourde, tu mets en cache les résultats de requêtes fréquentes. Le gain de latence se sent tout de suite sur des pages qui recalculent les mêmes agrégats à chaque visite.

**Sessions web** : plutôt que de stocker les sessions utilisateur en fichiers sur disque ou dans la base principale, Redis les garde en mémoire avec expiration automatique. Plusieurs instances d'une même appli peuvent alors partager le même état de session.

**Files d'attente légères** : pour du traitement asynchrone simple, une notification à envoyer, une image à retraiter, les listes Redis avec `LPUSH`/`BRPOP` font un système de queue basique sans monter un vrai message broker.

**Rate limiting** : un compteur avec expiration par IP ou par clé API te donne un limiteur de débit fonctionnel en quelques lignes, sans base de données dédiée.

Si tu gères déjà des outils qui accumulent des requêtes répétées, comme une surveillance de site avec [Changedetection](/changedetection-docker-surveillance-web/), une couche de cache Redis devant peut réduire la charge sur les sites surveillés et sur ta propre infra.

## Limites et points de vigilance

Redis n'est pas une base de données relationnelle et ne remplace pas PostgreSQL ou MySQL pour des données structurées avec relations complexes. Il n'a pas de vraies transactions ACID au sens SQL, même s'il propose des mécanismes proches avec `MULTI`/`EXEC`.

Le stockage en mémoire a un coût, ta base de données ne peut pas dépasser la RAM disponible sans configuration de swap ou de clustering, ce qui n'est pas la voie recommandée. Surveille ta consommation mémoire avec `INFO memory` dans `redis-cli` si tu stockes des volumes de données croissants.

Enfin, sans persistance activée, un crash ou une mise à jour d'image te fait perdre le contenu en mémoire. Ce n'est pas un défaut, c'est un choix de conception assumé par Redis, mais il faut le connaître avant de s'en servir pour autre chose que du cache jetable.

## Conclusion

Redis Docker coche toutes les cases pour qui veut une base clé-valeur rapide sans usine à gaz : une image officielle bien maintenue, une config qui tient en un fichier compose, et des cas d'usage concrets dès le premier déploiement. Mot de passe, volume persistant, réseau interne, ces trois réflexes suffisent à passer d'un test jetable à un service fiable dans ta stack.

Lance ton premier container, teste `SET` et `GET`, et branche-le sur l'appli qui en a le plus besoin. Tu verras vite pourquoi ce petit outil traîne dans autant de stacks depuis si longtemps.
