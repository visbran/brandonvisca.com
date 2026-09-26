---
title: "Portainer Docker : interface web pour gérer tes conteneurs facilement"
description: "Guide Portainer Docker complet : installe l'interface web, gère conteneurs, volumes et stacks sans ligne de commande, en dix minutes chrono."
pubDatetime: "2026-09-26T11:01:12+02:00"
modDatetime: "2026-09-25T08:00:00.000Z"
author: Brandon
tags:
  - docker
  - auto-hebergement
  - dashboard
  - intermediaire
featured: false
draft: false
focusKeyword: portainer docker
faqs:
  - question: "Portainer Docker consomme combien de ressources sur mon serveur ?"
    answer: "Très peu. L'image portainer-ce fait une trentaine de Mo et le conteneur tourne confortablement avec 512 Mo de RAM et un cœur CPU, même sur un Raspberry Pi ou un petit VPS."
  - question: "Puis-je gérer plusieurs serveurs Docker depuis une seule instance Portainer ?"
    answer: "Oui. Tu ajoutes chaque hôte comme environnement distant via l'agent Portainer ou une connexion Edge, et tu bascules de l'un à l'autre depuis le même tableau de bord."
  - question: "Portainer CE gratuit a-t-il de vraies limites face à la version Business ?"
    answer: "CE gère un nombre illimité d'environnements pour un usage perso ou petite équipe. BE ajoute RBAC avancé, SSO, support pro : inutile tant que tu es seul sur ton homelab."
---
> 💡 **TL;DR**
> - Portainer Docker te donne une interface web complète pour gérer conteneurs, images, volumes et réseaux sans taper une seule commande docker
> - Installation en une stack Docker Compose, accessible en HTTPS sur le port 9443 en moins de dix minutes
> - L'éditeur de stacks te permet de déployer n'importe quel projet Docker Compose directement depuis le navigateur, copier-coller inclus

## Table des matières

## Qu'est-ce que Portainer et pourquoi l'installer avec Docker

Tu gères ton homelab en SSH depuis six mois. `docker ps`, `docker logs`, `docker compose up -d`, tu connais la chanson par cœur. Mais dès que tu veux montrer ton install à quelqu'un, vérifier l'état de dix conteneurs d'un coup d'œil ou juste éviter de taper la même commande pour la centième fois, la ligne de commande montre ses limites.

Portainer résout exactement ça. C'est une interface web open source qui se branche sur ton démon Docker et te donne un tableau de bord complet : liste des conteneurs avec leur état en temps réel, logs consultables en un clic, gestion des volumes et réseaux, et un éditeur de stacks pour déployer du Docker Compose sans quitter le navigateur. Installer Portainer Docker sur ton serveur, c'est transformer une flotte de conteneurs opaque en quelque chose de lisible.

L'éditeur derrière le projet est Portainer.io, société qui maintient le logiciel depuis 2015 avec des releases régulières. Le code de la version Community est open source sous licence zlib, hébergé publiquement, et l'image officielle `portainer/portainer-ce` est mise à jour à chaque sortie. Ce n'est pas un projet abandonné qu'on redécouvre : c'est un standard du monde Docker, au même titre que Watchtower ou Traefik.

Ce que Portainer Docker fait concrètement pour toi au quotidien :

- **Vue d'ensemble** : tous tes conteneurs, leur statut, leur consommation CPU et RAM, sur un seul écran.
- **Logs en direct** : plus besoin de `docker logs -f`, tu cliques sur un conteneur et tu lis le flux.
- **Console intégrée** : un terminal dans le navigateur pour rentrer dans un conteneur sans SSH.
- **Éditeur de stacks** : colle un `docker-compose.yml`, clique sur déployer, c'est fait.
- **Gestion des volumes et réseaux** : crée, inspecte, supprime sans mémoriser la syntaxe exacte.
- **Registres privés** : connecte ton registre Docker Hub ou un registre self-hosted.
- **Templates d'applications** : une bibliothèque de conteneurs prêts à déployer en un clic.

## Portainer CE vs Portainer BE : quelle version choisir

Deux éditions existent, et le choix est vite tranché pour un homelab.

| Critère | Portainer CE | Portainer BE |
|---------|--------------|--------------|
| Prix | Gratuit | Payant, licence par nœud |
| Licence | Open source (zlib) | Propriétaire |
| Gestion multi-hôtes | Oui, via agents | Oui, avec RBAC avancé |
| Authentification | Locale, LDAP basique | SSO, OAuth, Active Directory |
| Support | Communauté, GitHub | Support professionnel contractuel |
| Cible | Homelab, petites équipes | Entreprises, production critique |

Pour un usage perso ou une petite structure, Portainer CE couvre tout ce dont tu as besoin : gestion illimitée de conteneurs, environnements multiples, éditeur de stacks, templates. La version Business ajoute du contrôle d'accès granulaire et du support contractuel, utile si tu gères une flotte de serveurs pour un client avec des obligations de SLA. Pour ton homelab, reste sur Portainer CE : c'est celle qu'on installe dans ce guide.

## Prérequis avant d'installer Portainer Docker

- Un serveur Linux avec Docker Engine installé et fonctionnel (version récente recommandée)
- Docker Compose v2 (`docker compose version` doit répondre)
- Accès root ou sudo, Docker devant lire `/var/run/docker.sock`
- 512 Mo de RAM et un cœur CPU suffisent largement au repos
- Un nom de domaine ou sous-domaine si tu veux exposer l'interface en HTTPS avec un reverse proxy

Portainer Docker est léger. Un Raspberry Pi 4 ou un petit VPS à quelques euros par mois fait très bien l'affaire, même avec une dizaine de conteneurs supervisés en parallèle.

## Installer Portainer Docker avec Docker Compose

Crée un dossier dédié :

```bash
mkdir -p ~/portainer && cd ~/portainer
```

Voici le fichier `docker-compose.yml` officiel, tel que documenté par Portainer.io :

```yaml
services:
  portainer:
    image: portainer/portainer-ce:lts
    container_name: portainer
    restart: unless-stopped
    security_opt:
      - no-new-privileges:true
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - portainer_data:/data
    ports:
      - "8000:8000"
      - "9443:9443"

volumes:
  portainer_data:
    name: portainer_data
```

Lance-le :

```bash
docker compose up -d
```

Le port 9443 sert l'interface web en HTTPS, le port 8000 est réservé au tunnel des agents Edge (tu peux le retirer si tu ne gères qu'un seul hôte). Le volume `portainer_data` stocke la base interne de Portainer : utilisateurs, environnements, configuration des stacks.

Ouvre `https://ton-serveur:9443`. Ton navigateur va râler sur un certificat auto-signé, c'est normal au premier lancement : accepte l'exception. Portainer Docker te demande alors de créer ton compte administrateur avec un mot de passe d'au moins 12 caractères. Fais-le tout de suite, la fenêtre pour créer ce compte se referme après quelques minutes pour des raisons de sécurité.

### Exposer Portainer avec un reverse proxy

Pour un accès propre en HTTPS sans certificat auto-signé, ajoute Portainer derrière Caddy :

```caddyfile
portainer.tondomaine.com {
    reverse_proxy localhost:9443 {
        transport http {
            tls_insecure_skip_verify
        }
    }
}
```

Si tu veux exposer ton instance Portainer Docker à distance sans ouvrir de port sur ta box, jette un œil à mon guide [Cloudflare Tunnel Docker : accède à ton homelab sans IP publique](/cloudflare-tunnel-docker-homelab/). C'est la méthode que j'utilise chez moi pour administrer mes conteneurs depuis n'importe où sans exposer directement le serveur sur Internet.

## Premiers pas dans l'interface

Une fois connecté, Portainer te montre l'écran "Home" avec la liste de tes environnements Docker. Clique sur "local" pour entrer dans ton hôte.

Tu arrives sur le tableau de bord : nombre de conteneurs actifs et arrêtés, images stockées, volumes, réseaux. Chaque chiffre est cliquable et t'amène directement à la liste correspondante.

Dans **Containers**, tu vois chaque conteneur avec son statut (running, stopped, unhealthy), son image et ses ports exposés. Un clic sur le nom ouvre les détails : logs, stats en temps réel, variables d'environnement, et un bouton "Console" pour ouvrir un terminal dedans directement depuis le navigateur. Pratique pour inspecter un fichier de config sans faire un `docker exec` depuis un terminal SSH.

Dans **Images**, tu retrouves toutes les images téléchargées, avec leur taille et la possibilité de les supprimer pour libérer de l'espace disque. Un bouton "Build a new image" permet même de construire une image depuis un Dockerfile collé dans l'interface.

Dans **Volumes** et **Networks**, tu gères le stockage persistant et la connectivité entre conteneurs sans mémoriser la syntaxe `docker volume create` ou `docker network create`. Utile quand tu débogues pourquoi deux conteneurs ne se voient pas sur le même réseau.

⚠️ Un point qui piège beaucoup de monde : supprimer un conteneur depuis Portainer ne supprime pas son volume associé si celui-ci est nommé. Vérifie toujours l'onglet **Volumes** avant de nettoyer, sinon tu accumules des volumes orphelins qui grignotent ton disque en silence.

## Déployer une stack complète depuis Portainer

C'est la fonctionnalité qui change vraiment la donne face au SSH. Va dans **Stacks** puis **Add stack**. Donne un nom, colle ton fichier `docker-compose.yml`, et clique sur **Deploy the stack**.

Portainer Docker télécharge les images, crée les volumes et réseaux définis, et démarre les conteneurs, exactement comme le ferait `docker compose up -d` en ligne de commande. La différence, c'est que tu gardes un historique versionné de chaque stack, tu peux l'éditer et la redéployer en changeant une seule ligne, et tu vois l'état de tous les conteneurs qui la composent regroupés ensemble plutôt qu'éparpillés dans la liste globale.

Deux exemples concrets tirés de mes propres déploiements. J'ai collé le compose de [Transmission Docker : client torrent ultra-léger avec interface web](/transmission-docker-client-torrent/) directement dans l'éditeur de stacks, ajusté les chemins de volumes pour mon NAS, et déployé en trente secondes sans ouvrir de terminal. Même chose pour [BookStack Docker : wiki pour équipes](/bookstack-docker-wiki-equipe/) : stack collée, variables d'environnement ajustées dans l'interface, déployée.

✅ Astuce que j'utilise systématiquement : nomme tes stacks avec un préfixe cohérent (`prod-`, `test-`, `media-`) pour t'y retrouver quand tu en as une vingtaine. Portainer trie alphabétiquement, un mauvais nommage devient vite illisible.

## Sécuriser ton installation Portainer Docker

Portainer Docker a un accès direct à `/var/run/docker.sock`, ce qui revient concrètement à un accès root sur ta machine hôte. Un conteneur qui peut piloter Docker peut créer un nouveau conteneur privilégié et sortir de son isolement. Ce n'est pas une faille, c'est le fonctionnement normal du socket Docker, mais ça veut dire que l'accès à Portainer doit être traité avec le même sérieux qu'un accès SSH root.

Checklist avant de mettre ton instance en usage régulier :

- **Mot de passe fort et unique** pour le compte administrateur, stocké dans un gestionnaire de mots de passe
- **HTTPS obligatoire**, jamais d'accès HTTP nu sur Internet
- **Pas d'exposition directe** : passe par un reverse proxy ou un tunnel plutôt que d'ouvrir le port 9443 sur ta box
- **Comptes séparés** par utilisateur si plusieurs personnes administrent le serveur, avec des rôles limités plutôt qu'un partage du compte admin
- **Mises à jour régulières** de l'image `portainer/portainer-ce`, les correctifs de sécurité sortent au fil des versions

Pour durcir encore l'accès, je recommande de coupler ton reverse proxy avec [CrowdSec Docker : sécurité collaborative contre les attaques](/crowdsec-docker-securite-collaborative/), qui bloque automatiquement les tentatives de bruteforce sur l'interface de connexion. Et comme la base `portainer_data` contient la configuration de tous tes environnements et utilisateurs, sauvegarde-la avec le même soin que le reste : mon guide [Duplicati Docker : sauvegarde chiffrée auto-hébergée](/duplicati-docker-sauvegarde/) couvre exactement ce genre de volume à ne pas perdre.

## Dépannage courant

### Le conteneur Portainer ne démarre pas

```bash
docker compose logs portainer
```

Vérifie que le socket `/var/run/docker.sock` existe bien et que l'utilisateur qui lance `docker compose` a les droits dessus. Un montage manquant ou un chemin mal orthographié dans le `docker-compose.yml` est la cause la plus fréquente.

### Impossible d'accéder à l'interface sur le port 9443

```bash
sudo ss -tlnp | grep 9443
```

Si rien n'écoute, le conteneur a probablement crashé au démarrage : relis les logs. Si un autre service occupe déjà le port, change-le côté hôte dans le compose, par exemple `"9444:9443"`.

### La fenêtre de création du compte admin a expiré

Portainer ferme cette fenêtre après quelques minutes d'inactivité pour éviter qu'un tiers ne s'approprie une instance fraîchement déployée. Il faut alors recréer le conteneur avec un volume vierge :

```bash
docker compose down
docker volume rm portainer_data
docker compose up -d
```

⚠️ Cette opération efface toute la configuration existante : environnements, stacks enregistrées, comptes. À réserver à une première installation, jamais à une instance déjà en production.

### Un environnement distant reste "Unreachable"

Vérifie que l'agent Portainer tourne bien sur la machine distante et que le port utilisé pour la communication (9001 par défaut pour l'agent) n'est pas bloqué par un firewall entre les deux hôtes.

## Conclusion

Portainer Docker ne remplace pas la ligne de commande, il la complète. Tu gardes le contrôle total via SSH quand tu en as besoin, mais pour le quotidien, l'interface web te fait gagner un temps fou : voir l'état de dix conteneurs d'un regard, consulter des logs sans te souvenir du nom exact d'un conteneur, déployer une stack en collant un fichier plutôt qu'en jonglant avec des chemins.

L'installation prend dix minutes, l'image est légère, et la version Community couvre largement les besoins d'un homelab. Si tu gères plus de trois ou quatre services Docker chez toi, c'est probablement l'outil qui te manque encore.

Sécurise l'accès dès le départ, HTTPS et mot de passe fort ne sont pas négociables vu le niveau d'accès que Portainer a sur ta machine. Une fois ça posé, ouvre l'éditeur de stacks et déploie ton prochain conteneur sans toucher un terminal.
