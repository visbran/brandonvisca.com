---
title: "Podman vs Docker : conteneurs rootless sans daemon"
description: "Podman vs Docker : découvre pourquoi Podman rootless sans daemon change la donne. Guide pratique avec installation, commandes et migration complète."
pubDatetime: "2026-07-13T08:00:00.000Z"
modDatetime: "2026-07-13T08:00:00.000Z"
author: Brandon Visca
tags:
  - docker
  - linux
  - intermediaire
  - securite
  - containerisation
featured: false
draft: false
focusKeyword: podman vs docker
faqs: []
ogImage: ""
---
> 💡 **TL;DR**
> - **C'est quoi ?** Podman est un moteur de conteneurs Linux daemonless et rootless, compatible CLI Docker
> - **Pourquoi ?** Pas de daemon root qui tourne en permanence, pas de socket Unix root exposé, sécurité renforcée par défaut
> - **Comment ?** Installe Podman, utilise `podman` à la place de `docker`, active le mode rootless et migre tes Compose existants

Tu connais Docker. Tu l'utilises tous les jours pour déployer tes services, tester des applis ou builder des images. C'est devenu l'outil standard de la containerisation.

Mais il y a un truc qui te chatouille depuis un moment : ce daemon qui tourne en permanence avec les droits root. Et ce socket Unix `/var/run/docker.sock` que chaque tuto te dit de monter dans tes conteneurs sans jamais vraiment expliquer pourquoi.

**Bonne nouvelle :** Podman existe. Et il fait exactement la même chose que Docker, sans daemon, sans root obligatoire, et avec une compatibilité de commandes quasi parfaite.

Dans cet article, on va voir ce qui différencie vraiment Podman de Docker, comment l'installer, comment l'utiliser au quotidien, et surtout si tu peux (et si tu dois) le remplacer complètement.

## Table des matières

## Docker, le daemon root qui pose problème

Docker est génial. Il a démocratisé les conteneurs et aujourd'hui c'est incontournable. Mais son architecture a une faille fondamentale pour la sécurité.

Quand tu installes Docker, tu installes un **daemon** (`dockerd`) qui tourne en permanence en tant que root. Ce daemon gère tout : le cycle de vie des conteneurs, le réseau, les volumes, les images. Et pour communiquer avec lui, le client Docker (`docker`) utilise un **socket Unix** situé à `/var/run/docker.sock`.

**Le problème ?** Ce socket appartient à root. Et quiconque a accès à ce socket a un contrôle total sur ta machine. C'est équivalent à donner les droits root sans mot de passe.

Tu veux voir à quel point c'est dangereux ? Monte ce socket dans un conteneur et exécute ça :

```bash
docker run -it -v /var/run/docker.sock:/var/run/docker.sock alpine sh
```

Depuis l'intérieur du conteneur, tu peux lister tous les conteneurs, lancer de nouveaux conteneurs avec `--privileged`, ou même monter le système de fichiers hôte. C'est une **évasion de conteneur en une commande**.

C'est pour ça que dans mon article sur [comment sécuriser Docker](/fail2ban-docker-securite-serveur/), je parle beaucoup de limiter les accès et de ne jamais exposer ce socket à la légère.

Mais imagine un outil qui te donne les mêmes fonctionnalités, sans ce daemon root omniprésent. C'est exactement ce que fait Podman.

## Qu'est-ce que Podman exactement ?

Podman est un moteur de conteneurs open-source développé par Red Hat. Il utilise la même technologie sous-jacente que Docker (les namespaces Linux, cgroups, et overlayfs), mais avec une architecture totalement différente.

**La différence clé :** Podman n'a pas de daemon.

Quand tu lances un conteneur avec Podman (`podman run`), le processus du conteneur est un **processus fils de ton shell**. Il n'y a pas de service root intermédiaire qui gère tout. C'est toi qui lances le conteneur, et le conteneur tourne avec tes droits.

Ça change tout :
- Pas de socket Unix root à protéger
- Pas de service qui crash et emporte tous tes conteneurs
- Pas de daemon qui consomme de la RAM en permanence
- La possibilité de faire du rootless (lancer des conteneurs sans être root)

Podman est aussi compatible avec l'API de Docker. Tu peux faire `alias docker=podman` et dans 90% des cas, ça fonctionne sans rien changer.

## Installer Podman en 2 minutes

### Fedora / RHEL / CentOS Stream

```bash
sudo dnf install -y podman podman-compose
```

Fedora est le terrain de jeu natif de Podman. L'intégration est parfaite.

### Debian / Ubuntu

```bash
sudo apt update
sudo apt install -y podman podman-compose
```

Depuis Debian 12 et Ubuntu 22.04, Podman est dans les dépôts officiels. Pas besoin d'ajouter de PPA.

### Arch Linux

```bash
sudo pacman -S podman podman-compose
```

### Vérifier l'installation

```bash
podman --version
podman info
```

Tu devrais voir la version installée et des infos sur ton stockage, ton réseau, et ta config rootless.

## Les commandes de base : Podman vs Docker

La magie de Podman, c'est que les commandes sont **presque identiques** à Docker. Voici les principales :

| Commande Docker | Commande Podman | Description |
| :--- | :--- | :--- |
| `docker run` | `podman run` | Lancer un conteneur |
| `docker ps` | `podman ps` | Lister les conteneurs actifs |
| `docker images` | `podman images` | Lister les images locales |
| `docker build` | `podman build` | Builder une image |
| `docker pull` | `podman pull` | Télécharger une image |
| `docker rm` | `podman rm` | Supprimer un conteneur |
| `docker rmi` | `podman rmi` | Supprimer une image |
| `docker logs` | `podman logs` | Voir les logs |
| `docker exec` | `podman exec` | Exécuter une commande dans un conteneur |
| `docker network` | `podman network` | Gérer les réseaux |
| `docker volume` | `podman volume` | Gérer les volumes |

**Exemple concret :** Tu veux lancer un serveur Nginx ?

```bash
podman run -d --name mon-nginx -p 8080:80 nginx:alpine
```

C'est exactement la même syntaxe qu'avec Docker.

Tu peux même créer un alias pour ne pas changer tes habitudes :

```bash
alias docker=podman
```

Mets ça dans ton `~/.bashrc` ou `~/.zshrc` et tu oublieras presque que tu n'utilises plus Docker.

## Le mode rootless : le vrai game changer

Le mode rootless est l'avantage numéro un de Podman. Il te permet de lancer des conteneurs **sans aucun droit root**.

### Comment ça marche ?

Quand tu fais `podman run` en tant qu'utilisateur normal, Podman crée un **user namespace**. À l'intérieur du conteneur, le processus pense tourner en tant que root (UID 0). Mais sur l'hôte, ce processus est en réalité exécuté avec ton UID utilisateur.

Podman utilise un mapping défini dans `/etc/subuid` et `/etc/subgid` pour cette traduction. Exemple de mapping :

```text
brandon:100000:65536
```

Ça signifie que l'UID 0 dans le conteneur = UID 100000 sur l'hôte. L'UID 1 = 100001, etc. Si un attaquant arrive à sortir du conteneur, il se retrouve avec un UID sans aucun droit sur le système hôte.

### Activer le mode rootless

Sur la plupart des distributions modernes, c'est déjà configuré. Vérifie :

```bash
cat /etc/subuid
cat /etc/subgid
```

Si ton utilisateur n'y figure pas, ajoute-le :

```bash
sudo usermod --add-subuids 100000-165535 --add-subgids 100000-165535 $USER
```

Puis teste :

```bash
podman run --rm alpine whoami
# retourne : root (mais root à l'intérieur du conteneur seulement)
```

### Les limites du rootless

Ce n'est pas magique non plus. En mode rootless :
- Tu ne peux pas binder des ports < 1024 sans configuration supplémentaire
- Le réseau est un peu plus limité (pas de pont réseau classique, Podman utilise slirp4netns)
- Certaines fonctionnalités avancées (comme `checkpoint/restore`) nécessitent le mode root

Mais pour 95% des usages quotidiens (héberger des services web, des bases de données, des outils), le rootless suffit amplement.

Si tu déploies des services Docker en production, le combo Podman rootless + [un pare-feu comme nftables](/nftables-docker-pare-feu-linux/) te donne une posture de sécurité bien supérieure à Docker classique.

## Podman Compose : remplacer Docker Compose

Docker Compose est l'outil standard pour définir des stacks multi-conteneurs. Podman peut l'utiliser aussi, avec `podman-compose`.

### Installation

Déjà fait si tu as suivi les commandes d'installation plus haut. Sinon :

```bash
pip3 install podman-compose
```

### Utilisation

Prends ton `docker-compose.yml` habituel et remplace simplement la commande :

```bash
# Avant
docker compose up -d

# Après
podman-compose up -d
```

`podman-compose` lit le fichier `docker-compose.yml`, crée un pod Podman (groupe logique de conteneurs), et lance tes services.

### Attention aux subtilités

Tout n'est pas 100% identique. Quelques pièges :
- `depends_on` dans Compose ne garantit pas que la base de données est prête, seulement qu'elle est démarrée. C'est vrai aussi avec Docker Compose, mais certains s'en aperçoivent en migrant
- Le réseau par défaut en rootless est différent. Les conteneurs peuvent communiquer via le nom de service, mais le DNS interne se comporte parfois différemment
- Les volumes nommés fonctionnent, mais leur emplacement physique est dans `~/.local/share/containers/storage/volumes/`

Si tu pars de zéro et que tu veux un [guide complet pour structurer tes projets Docker](/docker-debutant-services-auto-heberger/), tu peux appliquer les mêmes principes avec Podman sans presque rien changer.

## Tableau comparatif complet : Podman vs Docker

| Critère | Docker | Podman |
| :--- | :--- | :--- |
| **Architecture** | Daemon client-serveur | Daemonless, fork-exec direct |
| **Mode rootless** | Possible mais complexe (rootlesskit) | Natif et simple dès l'installation |
| **Socket Unix** | `/var/run/docker.sock` (root) | Aucun socket root requis |
| **Sécurité par défaut** | Nécessite des réglages manuels | Rootless et namespaces par défaut |
| **CLI** | `docker` | `podman` (compatible à 99%) |
| **Docker Compose** | `docker compose` natif | `podman-compose` (compatible) |
| **Orchestration** | Docker Swarm natif | Pas de Swarm, utilise Kubernetes ou systemd |
| **Images** | Compatible OCI | Compatible OCI, utilise les mêmes registres |
| **Pods** | Non natif | Natif (un pod = groupe de conteneurs partageant le réseau) |
| **Intégration systemd** | Complexe | Native (tu peux générer des unités systemd) |
| **Systèmes supportés** | Linux, macOS, Windows | Linux natif, macOS/Windows via machine virtuelle |
| **Écosystème** | Énorme, docs partout | Grandissant, très bien sur RHEL/Fedora |

Le point le plus fort de Podman est clair : **la sécurité par défaut**. Docker te laisse tout ouvert et c'est à toi de verrouiller. Podman verrouille par défaut et c'est à toi d'ouvrir si besoin.

## Migration de Docker vers Podman : le guide pratique

Tu veux basculer sans casser ton homelab ? Voici les étapes.

### Étape 1 : Installe Podman en parallèle

Ne désinstalle pas Docker tout de suite. Garde-le en backup.

```bash
sudo dnf install -y podman podman-compose  # ou apt/podman
```

### Étape 2 : Teste un conteneur simple

```bash
podman run --rm hello-world
```

Si ça marche, passe à la suite.

### Étape 3 : Crée l'alias

```bash
echo 'alias docker=podman' >> ~/.bashrc
source ~/.bashrc
```

### Étape 4 : Migre tes images

Podman peut utiliser les mêmes registres Docker Hub. Repull tes images :

```bash
podman pull nginx:alpine
podman pull postgres:16
```

### Étape 5 : Migre tes volumes

Docker stocke ses volumes dans `/var/lib/docker/volumes/`. Podman rootless les stocke dans `~/.local/share/containers/storage/volumes/`.

Pour un fichier de données simple (bind mount), aucun changement nécessaire. Si tu utilises des volumes nommés, tu devras recréer les données ou copier les dossiers.

### Étape 6 : Migre ton Docker Compose

Copie ton `docker-compose.yml` et teste :

```bash
podman-compose up -d
```

Si tu as des erreurs réseau, ajoute explicitement le réseau dans ton Compose :

```yaml
networks:
  mon-reseau:
    driver: bridge
```

### Étape 7 : Remplace Docker par Podman

Une fois que tout est stable :

```bash
sudo systemctl stop docker
sudo systemctl disable docker
sudo dnf remove docker-ce docker-ce-cli  # ou apt remove
```

**Conseil :** Fais ça progressivement. Migre un service, attends une semaine, puis migre le suivant. Ne bascule pas tout en production d'un coup.

## Les limites réelles de Podman

Podman n'est pas parfait. Voici les cas où Docker reste plus pertinent.

### Docker Desktop sur macOS et Windows

Sur Linux, Podman est natif. Sur macOS et Windows, Docker Desktop est bien plus intégré et fluide. Podman existe sur ces OS via `podman machine` (une VM Linux), mais l'expérience est moins polie.

Si tu es sur Mac ou Windows et que tu veux juste faire tourner des conteneurs sans te prendre la tête, Docker Desktop reste le plus simple.

### Docker Swarm

Podman ne remplace pas Docker Swarm. Si tu as un cluster Swarm avec plusieurs nœuds, tu dois migrer vers Kubernetes (ou utiliser d'autres outils d'orchestration).

Pour un homelab mono-serveur, ça ne change rien. Pour une infra multi-nœuds, c'est un vrai sujet.

### Intégrations CI/CD

Beaucoup de pipelines CI/CD utilisent `docker build` et `docker push`. Podman est compatible (`podman build`, `podman push`), mais certains runners CI sont configurés spécifiquement pour Docker et nécessitent des ajustements.

### Documentation et communauté

Docker a 10 ans d'avance sur la documentation. Quand tu cherches un problème sur Stack Overflow, 95% des réponses parlent de Docker. Avec Podman, tu dois parfois traduire mentalement la réponse.

Mais l'écart se réduit rapidement. Red Hat pousse fort sur Podman, et la documentation officielle est très complète.

## Podman et systemd : l'intégration parfaite

Un truc génial avec Podman : il peut générer des unités systemd à la volée.

Tu as un conteneur qui tourne ? Génère un service systemd :

```bash
podman generate systemd --new --name mon-nginx --files
```

Ça crée un fichier `container-mon-nginx.service` que tu peux copier dans `~/.config/systemd/user/` et activer :

```bash
systemctl --user daemon-reload
systemctl --user enable --now container-mon-nginx
```

Ton conteneur démarre automatiquement au boot, géré par systemd, sans aucun droit root. C'est propre, c'est standard, et ça remplace avantageusement les hacks avec `restart: unless-stopped` dans Docker Compose quand tu veux une gestion de service propre.

## Quand choisir Podman plutôt que Docker ?

Podman est clairement le meilleur choix dans ces situations :

- Tu veux **sécuriser ton homelab** sans effort supplémentaire
- Tu es sur **Fedora, RHEL ou AlmaLinux** (l'intégration est native)
- Tu préfères une architecture **sans daemon** (moins de surface d'attaque)
- Tu veux lancer des conteneurs en tant qu'utilisateur normal sans toucher à root
- Tu utilises **systemd** et tu veux gérer tes conteneurs comme des services système

Docker reste pertinent si :

- Tu es sur **macOS ou Windows** principalement
- Tu utilises **Docker Swarm** pour l'orchestration
- Ton équipe ou ton CI/CD est fortement ancré dans l'écosystème Docker
- Tu veux la **documentation la plus large possible** sans effort de traduction

## Conclusion

Podman n'est pas un jouet expérimental. C'est un outil mature, utilisé en production par Red Hat et des milliers d'administrateurs système. Il fait tout ce que fait Docker, avec une sécurité fondamentalement meilleure grâce à son architecture rootless et daemonless.

Si tu débutes dans la containerisation, mon conseil est simple : commence par [apprendre les bases avec Docker](/docker-debutant-services-auto-heberger/), car la documentation et les exemples sont partout. Mais dès que tu maîtrises les concepts, teste Podman. La migration est quasi transparente et le gain en sécurité est immédiat.

Pour un homelab ou un serveur de production, tourner des conteneurs sans daemon root et sans socket Unix exposé n'est pas un luxe. C'est une posture de sécurité de base que Podman te offre gratuitement. Docker est un excellent outil, mais Podman est l'évolution logique pour ceux qui prennent la sécurité au sérieux sans sacrifier la simplicité.
