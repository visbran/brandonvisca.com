---
title: "DIUN Docker : être alerté quand une image change sur le registre"
description: "DIUN Docker surveille tes images et alerte dès qu'une nouvelle version sort sur le registre, sans mise à jour auto. L'alternative à Watchtower, archivé."
pubDatetime: "2026-11-18T11:01:54+01:00"
modDatetime: "2026-11-17T08:00:00.000Z"
author: Brandon Visca
tags:
  - docker
  - monitoring
  - automation
  - intermediaire
featured: false
draft: false
focusKeyword: diun docker
faqs:
  - question: "DIUN Docker consomme combien de ressources sur mon serveur ?"
    answer: "Quasiment rien. Le binaire Go tourne en quelques Mo de RAM, même avec plusieurs dizaines de conteneurs surveillés et un cycle de vérification toutes les 6 heures."
  - question: "DIUN Docker peut-il mettre à jour mes conteneurs automatiquement ?"
    answer: "Non, et c'est volontaire. DIUN Docker notifie, il ne touche jamais à ce qui tourne. Pour appliquer la mise à jour, c'est toi qui lances docker compose pull puis up -d."
  - question: "Que devient Watchtower, et dois-je migrer tout de suite ?"
    answer: "Le dépôt containrrr/watchtower a été archivé le 17 décembre 2025 et n'est plus maintenu. Il continuera de tourner, mais sans correctif : migrer vers DIUN Docker n'est pas urgent, juste raisonnable."
---
> 💡 **TL;DR**
> - DIUN Docker surveille tes conteneurs et t'envoie une notification dès qu'une nouvelle image apparaît sur le registre, sans jamais toucher à ce qui tourne
> - Watchtower, l'outil de mise à jour automatique le plus connu, est archivé depuis le 17 décembre 2025 : DIUN Docker devient le choix par défaut pour qui veut juste être prévenu
> - Installation en un `docker-compose.yml`, configuration par labels sur chaque conteneur, notifications vers Discord, Telegram, ntfy, email et une cinquantaine d'autres canaux

## DIUN Docker : la vigie qui remplace Watchtower

Tu as un homelab avec vingt, trente, cinquante conteneurs. Chacun a sa propre image, son propre tag, son propre rythme de sortie. Tu ne vas pas vérifier à la main chaque registre pour savoir si une nouvelle version est dispo. Bon, on va pas se mentir, personne ne fait ça sérieusement plus de deux semaines.

C'est exactement le job de **DIUN Docker** (prononcé « *do I need an update?* », l'acronyme donne le ton). Le projet, maintenu par crazy-max sous licence MIT, se connecte au socket Docker, liste les conteneurs en cours d'exécution, interroge leur registre d'origine, et compare le digest de l'image locale avec celui publié. Dès qu'il détecte un changement, il t'envoie une notification. Rien de plus, rien de moins.

La différence avec Watchtower, c'est que DIUN ne redémarre jamais un conteneur à ta place. Il te laisse décider du moment et de la méthode. Pour un service de prod ou une base de données, c'est exactement le niveau de contrôle que tu veux.

## Table des matières

## Watchtower est mort, DIUN Docker prend le relais

La vraie question c'est : pourquoi migrer maintenant ? Réponse courte : le dépôt GitHub `containrrr/watchtower` a été archivé par son propriétaire le 17 décembre 2025. La page affiche un bandeau « This project is no longer maintained ». Il tourne encore sur des milliers de serveurs, mais plus aucune faille ne sera corrigée, plus aucun provider de registre ne sera ajouté.

Watchtower avait un mérite : il automatisait tout, du pull à la relance du conteneur. Mais cette automatisation totale fait justement peur à pas mal d'admins. Un conteneur qui se met à jour seul, un dimanche à 3h du matin, pendant que tu dors, ça peut casser une appli qui dépend d'une version précise d'une lib. DIUN inverse la logique : il te prévient, tu décides.

⚠️ Si tu utilises encore Watchtower en prod, rien ne t'oblige à l'arrêter aujourd'hui. Il n'est pas cassé, juste figé. Mais c'est le bon moment pour basculer la supervision vers DIUN Docker avant le prochain problème de compatibilité non corrigé.

## Installer DIUN Docker avec Docker Compose

L'image officielle est publiée sur Docker Hub (`crazymax/diun`) et sur le GitHub Container Registry (`ghcr.io/crazy-max/diun`). Crée un dossier dédié :

```bash
mkdir -p ~/docker/diun && cd ~/docker/diun
```

Voici le `docker-compose.yml` de base, celui que je fais tourner chez moi :

```yaml
services:
  diun:
    image: crazymax/diun:latest
    container_name: diun
    command: serve
    restart: unless-stopped
    volumes:
      - "./data:/data"
      - "/var/run/docker.sock:/var/run/docker.sock:ro"
    environment:
      - "TZ=Europe/Paris"
      - "DIUN_WATCH_WORKERS=20"
      - "DIUN_WATCH_SCHEDULE=0 */6 * * *"
      - "DIUN_WATCH_JITTER=30s"
      - "DIUN_PROVIDERS_DOCKER=true"
      - "DIUN_PROVIDERS_DOCKER_WATCHBYDEFAULT=false"
    labels:
      - "diun.enable=true"
```

Le montage du socket Docker en lecture seule (`:ro`) suffit : DIUN n'a besoin que de lister les conteneurs et lire leurs métadonnées, jamais d'en créer ou d'en supprimer. C'est un argument de sécurité qui compte, surtout si ton [Dockge Docker : gérer tes stacks Compose depuis une interface web](/dockge-docker-gestionnaire-stacks-compose/) héberge déjà une dizaine de stacks sensibles sur la même machine.

Lance le tout :

```bash
docker compose up -d
docker compose logs -f diun
```

Les logs te montrent immédiatement les premiers conteneurs analysés. Le volume `./data` stocke une base bbolt (une base clé-valeur embarquée, pas de serveur externe à gérer) qui garde en mémoire les derniers digests connus pour chaque image. Sans elle, DIUN renotifierait à chaque redémarrage.

## Configurer la surveillance : providers, planning et labels

Par défaut, `DIUN_PROVIDERS_DOCKER_WATCHBYDEFAULT=false` signifie que DIUN ignore tous les conteneurs sauf ceux explicitement marqués. C'est le comportement que je recommande : tu choisis service par service ce qui mérite une alerte, plutôt que de te faire noyer de notifications sur des conteneurs jetables ou des outils de test.

Pour activer la surveillance d'un service, ajoute simplement un label dans son propre `docker-compose.yml` :

```yaml
services:
  paperless:
    image: ghcr.io/paperless-ngx/paperless-ngx:latest
    container_name: paperless
    labels:
      - "diun.enable=true"
```

Si tu héberges déjà [Paperless-ngx : votre bureau numérique auto-hébergé avec OCR](/paperless-ngx-docker-guide-auto-hebergement/), c'est typiquement le genre de service où tu veux savoir qu'une nouvelle version existe sans qu'elle se déploie seule, le temps de lire le changelog.

Les labels disponibles vont plus loin que le simple `diun.enable` :

- `diun.watch_repo=true` : surveille tous les tags de l'image, pas seulement celui que tu utilises. Utile pour repérer une nouvelle branche majeure.
- `diun.sort_tags=semver` : trie les tags détectés selon le versionnage sémantique plutôt que par ordre alphabétique brut.
- `diun.max_tags=10` : limite le nombre de tags suivis, pour éviter de télécharger des centaines de manifestes sur une image qui publie un tag par commit.
- `diun.include_tags` et `diun.exclude_tags` : des expressions régulières séparées par des points-virgules, pour ne garder que les tags stables et exclure les `nightly`, `rc`, `beta`.
- `diun.notify_on=new;update` : choisit si l'alerte part sur une nouvelle image (`new`) et/ou une mise à jour de digest (`update`).

Pour la planification, `DIUN_WATCH_SCHEDULE` accepte une syntaxe cron classique. Toutes les 6 heures est un bon compromis. Vérifier toutes les 5 minutes n'apporte rien sauf à flinguer ton quota de requêtes sur Docker Hub, qui applique un rate limit par IP pour les comptes anonymes.

Si ta stack tourne avec [Redis Docker : déployer une base de données clé-valeur ultra-rapide](/redis-docker-base-donnees-cle-valeur/) ou avec [Vikunja Docker : gestionnaire de tâches auto-hébergé (alternative Todoist)](/vikunja-docker-gestionnaire-taches/) derrière, le même label `diun.enable=true` suffit, pas besoin de dupliquer la config DIUN Docker ailleurs.

## Notifications : Discord, Telegram, ntfy et compagnie

C'est là que DIUN tape fort par rapport à Watchtower. Les métadonnées envoyées sont riches : nom de l'image, tag, ancien et nouveau digest, lien direct vers le registre, plateforme (`linux/amd64`, `linux/arm64`...), et même les métadonnées custom que tu définis via `diun.metadata.*`.

Les canaux supportés couvrent à peu près tout ce qu'un homelab utilise : Discord, Slack, Telegram, Gotify, ntfy, Pushover, Matrix, Rocket.Chat, email SMTP, webhook générique, script shell local, et Apprise pour couvrir une cinquantaine de services additionnels. Exemple de config pour Discord dans `diun.yml` (monté dans `/data` si tu préfères le fichier à des variables d'environnement) :

```yaml
notif:
  discord:
    webhookURL: "https://discord.com/api/webhooks/XXX/YYY"
    renderFields: true
    mentions:
      - "@everyone"
```

Je te conseille de tester le canal avant de l'oublier pendant des mois : un webhook Discord invalide et tu ne sais jamais quand une image a changé. Le moyen le plus simple, c'est de forcer manuellement un cycle de vérification :

```bash
docker exec diun diun check
```

Cette commande relance une analyse immédiate sans attendre le prochain créneau du cron, pratique pour valider ta config juste après l'avoir modifiée.

✅ Astuce : regroupe tes notifications par canal selon la criticité. Les services exposés sur Internet vers un canal qui sonne vraiment (Telegram, Pushover), les outils internes vers un canal plus discret (email, ntfy en silencieux).

## DIUN Docker vs Watchtower : le vrai comparatif

Le tableau ci-dessous résume la différence qui compte vraiment entre les deux outils.

| Critère | DIUN Docker | Watchtower |
|---|---|---|
| Action sur l'image | Notifie seulement | Met à jour et relance le conteneur |
| Statut du projet | Actif, maintenu par crazy-max | Archivé depuis le 17/12/2025 |
| Accès au socket Docker | Lecture seule possible | Lecture-écriture (nécessaire pour recréer) |
| Providers | Docker, Swarm, Kubernetes, Nomad, Containerd, fichier statique | Docker et Swarm |
| Richesse des notifications | Digest, tag, plateforme, lien registre | Nom du conteneur, ancienne/nouvelle image |

Si ton besoin, c'est de dormir tranquille sans jamais toucher à un `docker compose pull`, Watchtower répondait à ça, et continuera de fonctionner tel quel tant que l'API des registres ne change pas. Mais pour tout ce qui touche à des services où une mise à jour non contrôlée peut casser une migration de base de données ou un format de config, DIUN Docker est clairement le choix le plus sain. Et comme le projet derrière Watchtower n'avance plus, le fossé va continuer de se creuser.

Spoiler : ça va marcher dans les deux sens de la combinaison. Rien n'empêche de garder Watchtower sur deux ou trois conteneurs jetables qui te servent de bac à sable, et DIUN Docker partout ailleurs pour garder la main.

## Dépannage : quand DIUN Docker reste silencieux

### Aucune notification ne part jamais

Vérifie d'abord que le conteneur ciblé porte bien le label `diun.enable=true`, et que `DIUN_PROVIDERS_DOCKER_WATCHBYDEFAULT` n'est pas resté à `false` sans label sur le service concerné. Ensuite, regarde les logs :

```bash
docker compose logs -f diun
```

Si tu gères plusieurs stacks en parallèle, [Dozzle Docker : visionneuse de logs Docker en temps réel via web](/dozzle-docker-visionneuse-logs-web/) te donne une vue centralisée sans avoir à taper cette commande sur chaque hôte.

### DIUN Docker signale une erreur 429 sur Docker Hub

Le rate limit anonyme de Docker Hub est strict : 100 requêtes par 6 heures par IP pour un compte non authentifié. Avec une vingtaine d'images surveillées, tu le dépasses vite. Crée un compte Docker Hub gratuit et renseigne les identifiants dans `regopts` :

```yaml
regopts:
  - selector: "docker.io"
    username: "ton_compte"
    password: "ton_token_dacces"
```

Utilise un token d'accès généré depuis les paramètres de sécurité du compte, jamais ton mot de passe principal en clair dans un fichier de config.

### Trop de notifications sur des tags qui ne m'intéressent pas

C'est le symptôme classique d'un `diun.watch_repo=true` posé sans `diun.include_tags`. Resserre le filtre pour ne garder que les tags stables :

```yaml
labels:
  - "diun.watch_repo=true"
  - "diun.include_tags=^[0-9]+\\.[0-9]+\\.[0-9]+$"
  - "diun.exclude_tags=rc;beta;nightly;dev"
```

### La base de données grossit sans fin

Le fichier `diun.db` dans `/data` garde l'historique de tous les manifestes analysés. Sur plusieurs années et des dizaines d'images en `watch_repo`, ça peut prendre quelques dizaines de Mo, rarement plus. Si tu veux repartir propre, arrête le conteneur, supprime le fichier, relance : DIUN reconstruit sa base au premier cycle, au prix d'un batch de notifications « new » sur tout ce qu'il redécouvre.

## Conclusion

DIUN Docker fait une seule chose, et il la fait bien : te dire quand une image bouge, sans jamais décider à ta place de l'appliquer. Dans un contexte où l'alternative historique vient de fermer boutique, ce n'est plus juste une question de préférence personnelle, c'est devenu le choix par défaut pour qui garde un minimum de contrôle sur sa prod.

Mon setup actuel : DIUN Docker sur le socket en lecture seule, un label sur chaque service qui compte vraiment, des notifications Telegram pour ce qui est exposé et un canal ntfy discret pour le reste. Dix minutes à mettre en place, et tu ne rates plus jamais une mise à jour de sécurité qui traîne depuis trois semaines sans que tu le saches.
