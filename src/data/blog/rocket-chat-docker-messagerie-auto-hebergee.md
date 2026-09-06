---
title: "Rocket.Chat Docker : messagerie collaborative auto-hébergée"
description: "Guide complet rocket.chat docker pour déployer Rocket.Chat avec Docker Compose. Messagerie collaborative auto-hébergée et sécurisée."
pubDatetime: "2026-08-16T06:00:00.000Z"
modDatetime: "2026-08-16T06:00:00.000Z"
author: Brandon Visca
tags:
  - auto-hebergement
  - intermediaire
  - docker
  - linux
  - homelab
  - messagerie
featured: false
draft: false
focusKeyword: rocket.chat docker
ogImage: ""
---
> 💡 **TL;DR**
> - Rocket.Chat est une messagerie collaborative open source auto-hébergeable, alternative sérieuse à Slack et Teams
> - Un stack Docker Compose minimal avec MongoDB suffit pour démarrer en quelques minutes
> - Le déploiement nécessite une base MongoDB, un reverse proxy et une gestion des backups pour la prod

## Table des matières

## Rocket.Chat : la messagerie collaborative que tu contrôles

Si tu en as marre de payer un abonnement Slack à prix d'or pour ton équipe de cinq personnes, ou si tu refuses de confier tes conversations professionnelles aux serveurs de Microsoft, il est temps de passer à l'auto-hébergement. [Rocket.Chat](https://www.rocket.chat/) est une plateforme de messagerie collaborative open source qui offre exactement ce que tu attends d'un outil de chat d'équipe, sans la facture mensuelle et avec tes données chez toi.

Contrairement à Mattermost, son concurrent open source plus minimaliste, Rocket.Chat se positionne comme une plateforme complète de communication d'entreprise : chat en temps réel, appels vidéo, partage de fichiers, intégrations OAuth, bots, et même du live chat pour ton site web. Si tu débutes dans l'auto-hébergement et que tu cherches une première messagerie à héberger, j'ai déjà couvert [les bases du déploiement Docker](/docker-debutant-services-auto-heberger/) dans un guide dédié. Rocket.Chat est une étape au-dessus : ça reste accessible, mais il faut gérer une base de données MongoDB et quelques paramètres de sécurité.

Dans cet article, on déploie Rocket.Chat avec Docker Compose sur un serveur Linux, on le sécurise derrière un reverse proxy, on configure les backups, et on évoque les pièges classiques auxquels tu ne penseras pas avant qu'ils ne te mordent.

## Pourquoi choisir Rocket.Chat plutôt que Slack ou Teams ?

Avant d'ouvrir un terminal, posons la question : pourquoi s'embêter à auto-héberger une messagerie alors que Slack fonctionne bien et que Teams est souvent déjà inclus dans ton abonnement Office ?

**La souveraineté des données.** Tes conversations, tes fichiers partagés, tes métadonnées, tout reste sur ton serveur. Pas de clauses d'utilisation opaques, pas de data mining déguisé, pas de surprise concernant l'entraînement de modèles d'IA sur tes échanges internes.

**Le coût.** Pour une petite équipe, Rocket.Chat en édition communautaire est gratuit. Pas de limite arbitraire de 10 000 messages d'historique. Pas de facture qui grimpe dès que tu veux une intégration SAML.

**La flexibilité.** Tu peux l'héberger sur ton VPS, ton NAS, ton Raspberry Pi (avec des limitations évidentes), ou même en air-gappé dans ton réseau d'entreprise. Tu décides quand mettre à jour, quels modules activer, et quels utilisateurs créer.

**Les fonctionnalités natives.** Contrairement à Mattermost qui pousse vers l'édition payante pour des options avancées, Rocket.Chat Community embarque déjà les appels vidéo Jitsi, le live chat, les webhooks entrants et sortants, et un éditeur de workflows basique.

## Prérequis et architecture

Avant de lancer le `docker compose up`, vérifie que ton serveur dispose des ressources nécessaires. Rocket.Chat est gourmand en RAM, surtout au premier démarrage où il initialise MongoDB et compile les assets.

| Ressource | Minimum recommandé |
|-----------|-------------------|
| CPU       | 2 cœurs           |
| RAM       | 4 Go (2 Go si sec) |
| Stockage  | 20 Go SSD         |
| OS        | Linux avec Docker |

L'architecture est simple mais stricte : Rocket.Chat dépend impérativement de MongoDB. Pas de MySQL, pas de PostgreSQL, Mongo uniquement. On va utiliser MongoDB 6.0 en replica set (même s'il n'y a qu'un seul nœud), car c'est un prérequis technique de Rocket.Chat depuis la version 5.x.

## Le docker-compose.yml pour rocket.chat docker

Crée un dossier dédié, par exemple `/opt/rocketchat`, et place-y ce fichier `docker-compose.yml` :

```yaml
version: '3.8'

services:
  rocketchat:
    image: rocketchat/rocket.chat:6.12
    container_name: rocketchat
    restart: unless-stopped
    environment:
      - PORT=3000
      - ROOT_URL=https://chat.tondomaine.fr
      - MONGO_URL=mongodb://mongo:27017/rocketchat?replicaSet=rs0
      - MONGO_OPLOG_URL=mongodb://mongo:27017/local?replicaSet=rs0
    depends_on:
      - mongo
    ports:
      - "3000:3000"
    volumes:
      - rocketchat-uploads:/app/uploads

  mongo:
    image: mongo:6.0
    container_name: rocketchat-mongo
    restart: unless-stopped
    command: >
      mongod --oplogSize 128 --replSet rs0
    volumes:
      - mongo-data:/data/db

  mongo-init:
    image: mongo:6.0
    container_name: rocketchat-mongo-init
    depends_on:
      - mongo
    restart: on-failure
    entrypoint: >
      bash -c "
        sleep 10 &&
        mongosh --host mongo:27017 --eval \"
          rs.initiate({
            _id: 'rs0',
            members: [{ _id: 0, host: 'mongo:27017' }]
          })
        \"
      "

volumes:
  rocketchat-uploads:
  mongo-data:
```

Quelques points critiques :

- `ROOT_URL` doit être l'URL publique complète avec le protocole. Si tu ne la configures pas correctement, les notifications push et les intégrations vont générer des liens cassés.
- `MONGO_URL` inclut explicitement `?replicaSet=rs0`. Sans ça, Rocket.Chat refuse de démarrer à partir de la version 6.
- Le service `mongo-init` initialise le replica set. C'est un conteneur jetable qui s'arrête après son travail, `restart: on-failure` évite qu'il boucle en erreur si MongoDB n'est pas encore prêt.

Pour tester rapidement sans HTTPS en local, tu peux remplacer `ROOT_URL` par `http://localhost:3000`. Mais en production, oublie le HTTP non sécurisé. Mets un reverse proxy en face.

## Déploiement pas à pas

Lance l'initialisation de MongoDB, puis démarre Rocket.Chat :

```bash
cd /opt/rocketchat
docker compose up -d mongo
sleep 15
docker compose up -d mongo-init
sleep 5
docker compose up -d rocketchat
```

Attends environ une minute pour le premier démarrage. Rocket.Chat compile alors les assets et initialise la base. Tu peux suivre la progression avec :

```bash
docker logs -f rocketchat
```

Quand tu vois `➔ +---------------------------------------------------+` suivi de `➔ |                  SERVER RUNNING                   |`, c'est bon. Ouvre ton navigateur sur `http://IP_DU_SERVEUR:3000`.

La première visite te demande de créer un compte administrateur. C'est le moment de choisir un mot de passe costaud. Pas de "admin123", on est des professionnels.

## Mise en place du reverse proxy HTTPS

Exposer Rocket.Chat directement sur le port 3000 en HTTP, c'est acceptable pour un test de dix minutes. Pour une utilisation réelle, tu dois passer par un reverse proxy avec TLS. Si tu ne sais pas par où commencer, j'ai déjà publié un guide sur [Caddy comme reverse proxy Docker](/caddy-docker-reverse-proxy-guide/) qui est probablement la solution la plus simple aujourd'hui.

Avec Caddy, tu ajoutes simplement dans ton `Caddyfile` :

```caddy
chat.tondomaine.fr {
    reverse_proxy rocketchat:3000
}
```

Et dans le `docker-compose.yml` de Rocket.Chat, tu retires le mapping de port `3000:3000` pour le remplacer par un réseau partagé avec Caddy :

```yaml
networks:
  default:
    name: caddy-network
    external: true
```

Pense à adapter `ROOT_URL` avec ton domaine HTTPS. Sans cette cohérence, les emails de confirmation et les liens de réinitialisation de mot de passe ne fonctionneront pas.

## Sauvegardes : ne néglige pas MongoDB

Sauvegarder Rocket.Chat, c'est sauvegarder MongoDB. Les fichiers uploadés sont dans `/app/uploads` (monté en volume Docker), mais le cœur de ton instance, comptes, salons, messages, permissions, vit entièrement dans la base de données.

Crée un script de backup quotidien `/opt/rocketchat/backup.sh` :

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/opt/backups/rocketchat"
mkdir -p "$BACKUP_DIR"

docker exec rocketchat-mongo mongodump --out /data/backup/$DATE

docker cp rocketchat-mongo:/data/backup/$DATE "$BACKUP_DIR/"
docker exec rocketchat-mongo rm -rf /data/backup/$DATE

tar czf "$BACKUP_DIR/rocketchat_${DATE}.tar.gz" -C "$BACKUP_DIR" $DATE
rm -rf "$BACKUP_DIR/$DATE"

find "$BACKUP_DIR" -name "rocketchat_*.tar.gz" -mtime +7 -delete
```

Rends-le exécutable et planifie-le avec `crontab -e` :

```bash
chmod +x /opt/rocketchat/backup.sh
0 3 * * * /opt/rocketchat/backup.sh >> /var/log/rocketchat-backup.log 2>&1
```

Pour restaurer une sauvegarde, c'est l'inverse :

```bash
docker exec -i rocketchat-mongo mongorestore --drop /data/backup/20260816_030000/rocketchat
```

Si tu veux aller plus loin sur la stratégie de sauvegarde globale de ton homelab, j'ai détaillé [BorgBackup en conteneur Docker](/borgbackup-docker-sauvegarde/) dans un article précédent. C'est un excellent complément pour externaliser tes backups vers un NAS distant.

## Sécuriser l'instance

Le premier réflexe après l'installation : verrouiller les accès. Rocket.Chat expose par défaut une API REST très riche. Si tu ne prends pas quelques précautions, tu vas te faire scanner par des bots en moins de temps qu'il n'en faut pour dire "CVE".

**Forcer HTTPS.** Même si Caddy ou Traefik gère le TLS, configure `Force SSL` dans les paramètres généraux de Rocket.Chat. Ça évite les connexions en clair accidentelles.

**Restreindre l'inscription.** Par défaut, n'importe qui peut créer un compte. Va dans *Administration → Settings → Accounts → Registration* et désactive l'inscription publique. Passe en invitation uniquement ou en authentification OAuth via ton Keycloak, GitLab ou GitHub.

**Activer le rate limiting.** Dans *Administration → Settings → Rate Limiter*, limite les tentatives de connexion. C'est basique mais efficace contre les attaques par force brute.

**Firewall et ports.** Ne laisse pas le port 3000 ouvert sur Internet. Seul ton reverse proxy doit être accessible depuis l'extérieur. Pour aller plus loin, [CrowdSec en conteneur Docker](/crowdsec-docker-securite-collaborative/) peut filtrer les IPs malveillantes à l'échelle de tout ton homelab.

**Mises à jour.** Rocket.Chat publie des correctifs de sécurité réguliers. Inscris-toi aux alertes de sécurité officielles et prévois une procédure de mise à jour testée. Ne mets jamais à jour MongoDB sans vérifier la matrice de compatibilité de Rocket.Chat.

## Utilisation avancée : quelques fonctionnalités sympas

Une fois l'instance stable, explore ce que Rocket.Chat propose nativement sans module payant.

**Les canaux et les discussions.** Tu peux créer des canaux publics (visibles par tous) ou privés (invitation uniquement), ainsi que des discussions éphémères au sein d'un canal. C'est pratique pour ne pas polluer le fil principal avec un sujet ponctuel.

**Les intégrations.** Rocket.Chat supporte les webhooks entrants et sortants. Tu peux connecter GitLab pour recevoir une notification à chaque push, ou brancher n'importe quel service capable de faire du HTTP. Il y a aussi un store d'apps officiel, mais attention : certaines apps gratuites deviennent payantes sans préavis.

**Le live chat.** Tu peux intégrer un widget de chat sur ton site web pour le support client. Les conversations arrivent directement dans ton instance Rocket.Chat, dans un canal dédié. C'est une alternative open source aux Intercom et Crisp payants.

**Les apps mobiles.** Rocket.Chat a des applications iOS et Android natives. Elles se connectent à ton instance auto-hébergée sans problème, à condition que `ROOT_URL` soit correctement configuré avec un domaine public accessible.

**Le mode Omnichannel.** Au-delà du simple chat, tu peux connecter des boîtes email, des comptes WhatsApp Business, ou même des canaux SMS. C'est l'équivalent d'un Zendesk maison. La configuration demande du temps, mais c'est entièrement gratuit en édition communautaire.

## Pièges et erreurs classiques

Après avoir déployé plusieurs instances de Rocket.Chat, voici les écueils que j'ai rencontrés et qui font perdre des heures.

**MongoDB en replica set obligatoire.** Si tu tentes de lancer Rocket.Chat avec une simple instance MongoDB sans `rs.initiate()`, il va crasher avec une erreur cryptique sur le *oplog*. Toujours initialiser le replica set, même mono-nœud.

**ROOT_URL mal configurée.** C'est la cause numéro un des liens cassés. Si ton instance est accessible via `https://chat.tondomaine.fr` mais que `ROOT_URL` vaut `http://localhost:3000`, tous les liens dans les emails, les notifications et les prévisualisations de liens seront invalides.

**Mémoire insuffisante sur un petit VPS.** Rocket.Chat + MongoDB sur un VPS à 2 Go de RAM, c'est jouable mais ça swap. Les premiers démarrages peuvent durer plusieurs minutes et déclencher des timeouts de health check. Augmente la RAM ou active un swap fichier si tu n'as pas le choix.

**Les volumes Docker non persistés.** Si tu oublies de monter `rocketchat-uploads` en volume, tous les fichiers uploadés disparaîtront au prochain `docker compose down`. C'est évident quand on le sait, mais c'est aussi la panne la plus frustrante.

**Mises à jour sautées.** Passer de la 5.x à la 6.x sans suivre les notes de version officielles, c'est l'assurance de planter ta base MongoDB. Rocket.Chat est exigeant sur les versions de MongoDB compatibles. Lis toujours le changelog avant de `docker compose pull`.

## Alternative : Mattermost ou Element ?

Rocket.Chat n'est pas le seul acteur du marché de la messagerie auto-hébergée. Si tu cherches une alternative, j'ai aussi testé [Mattermost en Docker](/mattermost-docker-chat-equipe/) dans un article dédié. Mattermost est plus léger, plus rapide au démarrage, et son interface est très proche de Slack. En contrepartie, il est moins riche en fonctionnalités natives et pousse plus fort vers la version Enterprise.

Rocket.Chat reste mon choix quand j'ai besoin d'une plateforme complète : chat, vidéo, live chat, omnichannel, workflows. Si tu veux juste un Slack-like pur et simple, Mattermost est peut-être plus adapté. Si la décentralisation et la fédération te parlent plus, oriente-toi vers [Element/Matrix](/element-matrix-docker-messagerie/).

## Conclusion

Déployer Rocket.Chat avec Docker, c'est reprendre le contrôle de sa messagerie d'équipe sans sacrifier le confort. Le stack est accessible, bien documenté, et les fonctionnalités de l'édition communautaire couvrent largement les besoins d'une petite structure. L'investissement principal n'est pas technique, le `docker-compose.yml` tient en une page, mais organisationnel : penser aux backups, aux mises à jour, et à la gestion des utilisateurs.

Si tu hésites encore à franchir le pas de l'auto-hébergement, n'oublie pas que [mon guide complet de l'auto-hébergement](/auto-hebergement-guide-complet-2025/) couvre tout ce qu'il faut savoir pour monter ton propre infrastructure, de la boîte Linux au reverse proxy en passant par les certificats SSL.

Rocket.Chat n'est pas une solution magique, mais c'est un outil solide, mature et véritablement open source. Ton équipe mérite une messagerie qui ne dépend pas d'un abonnement cloud.
