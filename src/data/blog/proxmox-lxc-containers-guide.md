---
title: "Proxmox LXC : des conteneurs légères pour ton homelab sans la lourdeur des VM"
description: "Guide complet Proxmox LXC : créer, configurer et sécuriser des conteneurs Linux. Beaucoup plus légers que des VM, parfaits pour ton homelab débutant."
pubDatetime: 2026-05-06 10:00:00+02:00
modDatetime: 2026-05-06 10:00:00+02:00
author: Brandon Visca
tags:
  - proxmox
  - lxc
  - homelab
  - linux
  - auto-hebergement
  - debutant
featured: false
draft: false
focusKeyword: proxmox lxc
faqs:
  - question: "Un conteneur LXC est-il une VM ?"
    answer: "Non. Un LXC partage le kernel de l'hôte. C'est plus léger qu'une VM traditionnelle, mais moins isolé. Pour un homelab, c'est souvent un bon compromis."
  - question: "Peut-on installer Docker dans un conteneur LXC ?"
    answer: "Oui, mais il faut activer la création de conteneurs imbriqués. Ce n'est pas recommandé en production, mais ça fonctionne très bien en homelab."
  - question: "Proxmox LXC est-il plus léger qu'une VM ?"
    answer: "Bien plus léger. Un LXC démarre en quelques secondes et consomme moins de RAM car il partage le kernel avec l'hôte."
  - question: "Quelles distributions sont compatibles avec Proxmox LXC ?"
    answer: "Proxmox propose des templates pour Debian, Ubuntu, Alpine, CentOS, Rocky Linux et d'autres. Alpine est le plus léger (environ 15 Mo)."
---
> 💡 **TL;DR** — Ce qu'il faut retenir :
> - Un LXC partage le kernel de l'hôte et consomme bien moins de ressources qu'une VM.
> - Proxmox te fournit des templates prêts à l'emploi : création en 30 secondes.
> - Parfait pour des services légers : DNS, monitoring, reverse proxy, VPN.
> - Docker dans un LXC, c'est possible mais demande une option spécifique.

La [documentation officielle Proxmox sur les conteneurs LXC](https://pve.proxmox.com/wiki/Linux_Container) reste la référence technique pour aller plus loin.

## Table des matières

## Pourquoi les LXC changent la donne en homelab

Quand tu commences ton homelab, la première chose que tu fais, c'est créer des VM. Des tas de VM. Une pour Nextcloud, une pour Vaultwarden, une pour le DNS, une pour le monitoring. Ton Proxmox en compte bientôt 10, 15, 20. Et là, ton serveur commence à tousser.

Les VMs, c'est top. L'isolation est parfaite, chacune a son propre kernel, son propre système d'exploitation. Mais tout ce confort a un prix : chaque VM bouffe de la RAM juste pour tourner à vide. Une Debian minimale, c'est déjà 512 Mo de RAM consommés rien que pour dire bonjour.

Les **conteneurs LXC** (Linux Containers), c'est la solution du paresseux efficace. Au lieu de virtualiser un système entier avec son kernel, tu partages celui de l'hôte. Résultat : un LXC démarre en 2 secondes, consomme une vingtaine de Mo de RAM, et tu peux en faire tourner une dizaine sur du matériel qui peinerait avec 3 VMs.

Si tu débutes en homelab et que ton serveur n'a que 8 Go de RAM, les LXC vont littéralement sauver ton expérience. Tu vas pouvoir héberger [Docker avec tes services](/docker-debutant-services-auto-heberger/), ton [reverse proxy Traefik](/traefik-reverse-proxy-docker/) et ton [cloud Nextcloud](/nextcloud-docker-installation-complete-2025/) sans faire suer ta machine.

## VM vs LXC : arrêtez de vous battre, voici la vérité

Il y a deux clans chez les self-hosters : l'équipe VM et l'équipe Docker/LXC. Les premiers disent que sans VM, c'est pas sécurisé. Les seconds répondent qu'avec des VMs, tu gasilles des ressources. Voici le tableau comparatif qui règle le débat une bonne fois pour toutes.

| Critère | VM | LXC |
|---|---|---|
| Isolation | Complète (kernel séparé) | Partage le kernel hôte |
| Démarrage | 30-60 secondes | 2-5 secondes |
| RAM à vide | 256-1024 Mo | 15-64 Mo |
| Taille disque | 4-10 Go | 500 Mo-2 Go |
| Sécurité | Très haute | Bonne (dépend de la conf) |
| Complexité | Standard | Ultra simple |
| Docker natif | Oui | Besoin d'une option |

La conclusion est simple : si tu héberges un service critique accessible depuis Internet (site web public, mail), privilégie une VM ou un LXC **unprivilégié** bien configuré. Si c'est pour ton usage perso en local, LXC sans hésiter.

## Les prérequis (y en a presque pas)

Avant de créer ton premier conteneur, il te faut :

- Un serveur Proxmox VE installé et fonctionnel (même sur un vieux PC)
- Un accès à l'interface web (`https://ip-de-ton-serveur:8006`)
- Un template OS téléchargé (Proxmox en propose plein gratuitement)
- Environ 2 Go de RAM libres sur l'hôte

Si tu n'as pas encore installé Proxmox, ce n'est pas le sujet d'aujourd'hui. Mais sache que l'installation tient sur une clé USB et se fait en 10 minutes montre en main.

## Créer son premier conteneur en 30 secondes

Connecte-toi à l'interface web de Proxmox. Choisis ton nœud dans le menu de gauche. Clique sur **Create CT**.

Proxmox te pose quelques questions. Voici mes réponses type pour un LXC de base :

| Paramètre | Valeur recommandée |
|---|---|
| Hostname | `ct-dns` ou `ct-reverse-proxy` |
| Password | Un truc fort, pas `123456` s'il te plaît |
| Template | `debian-12-standard` (stable et bien supporté) |
| Disque | 4 Go, format ZFS ou LVM selon ton stockage |
| CPU | 1 core |
| RAM | 256 Mo (oui, c'est suffisant pour un service léger) |
| Réseau | DHCP pour commencer, IP fixe ensuite |

Clique sur **Finish**. Et voilà. Ton LXC est créé. C'était pas plus compliqué que ça.

Tu peux le démarrer en cliquant sur le bouton **Start** de l'interface. Ensuite, ouvre la console intégrée : tu as un terminal Debian fonctionnel, root, prêt à recevoir tes commandes.

## Configurer le réseau pour ne pas perdre ton conteneur

Par défaut, Proxmox attribue une IP via DHCP. Ça marche, mais c'est le chaos quand tu as 10 LXC et que tu ne sais plus qui a quelle IP.

Voici la méthode pour fixer une IP statique directement dans la configuration du conteneur, sans toucher aux fichiers internes. Dans l'interface Proxmox, clique sur ton LXC, va dans l'onglet **Network**.

Si tu utilises le bridge standard `vmbr0`, voici la config type :

| Paramètre | Valeur |
|---|---|
| Name | `eth0` |
| Bridge | `vmbr0` |
| IPv4 | Static |
| IPv4/CIDR | `192.168.1.50/24` |
| Gateway (IPv4) | `192.168.1.1` |

Pense à adapter le réseau à ton propre LAN. Redémarre le conteneur pour que la config soit prise en compte. Tu peux maintenant te connecter en SSH via l'IP fixe.

## Gérer les ressources sans te prendre la tête

Un LXC n'a pas de mémoire graphique, pas de complexité. Il consomme ce que tu lui donnes. Mais par défaut, il peut utiliser toute la CPU disponible sur l'hôte.

Dans l'interface Proxmox, onglet **Resources**, tu peux limiter :
- **Memory** : 256 Mo pour un service léger, 512 Mo pour un service moyen
- **Swap** : 512 Mo (évite les OOM kills)
- **CPU limit** : laisse 1 core pour un DNS, 2 pour un reverse proxy chargé
- **Cores** : cocher la case **Enable nesting** si tu veux Docker dans le LXC

Cette case **Enable nesting** est cruciale. Sans elle, Docker refusera de s'installer. Avec elle, tu peux faire tourner des conteneurs Docker à l'intérieur d'un conteneur LXC. On appelle ça des **conteneurs imbriqués**. C'est un peu inception, mais ça marche très bien en homelab.

Docker dans un LXC ? Attention quand même

On parle souvent de Docker et de LXC comme si c'était des rivaux. En réalité, ils sont complémentaires. Mon setup préféré en homelab, c'est celui-ci :

- **LXC** pour les services système : DNS, monitoring, VPN, reverse proxy
- **VM** pour les plateformes lourdes : Nextcloud avec sa base de données, Jellyfin avec le transcodage
- **Docker** directement sur l'hôte Proxmox (ou dans une VM dédiée) pour les applis web

Si tu veux absolument mettre Docker dans un LXC, voici la procédure. Dans l'interface Proxmox, onglet **Options**, double-clique sur **Features**. Coche :
- **Nesting**
- **NFS** (si tu veux monter des partages)

Redémarre le conteneur. Installe Docker selon la méthode classique. Ça marche.

Mais attention : ce n'est pas recommandé pour un environnement de production. La sécurité est moins solide qu'une VM. En homelab perso ? Fais-toi plaisir.

## Sécuriser tes conteneurs (même si c'est pour toi)

Un LXC partage le kernel avec l'hôte. Ça signifie qu'une élévation de privilèges dans un LXC mal configuré peut théoriquement atteindre l'hôte. Voici les règles de base pour dormir tranquille.

### Désactiver l'accès root par mot de passe

Dans chaque LXC, installe une clé SSH et désactive la connexion root par mot de passe :

```bash
sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin no/' /etc/ssh/sshd_config
systemctl restart sshd
```

Crée un utilisateur normal, ajoute-le au groupe `sudo`, et utilise `sudo` pour les opérations admin.

### Activer les mises à jour automatiques

Un LXC oublié, c'est un LXC vulnérable. Debian propose un paquet qui gère ça tout seul :

```bash
apt install unattended-upgrades
```

Vérifie que le fichier `/etc/apt/apt.conf.d/50unattended-upgrades` contient bien les lignes pour les mises à jour de sécurité. Par défaut, c'est le cas.

### Gérer les snapshots avant toute modification

Proxmox te permet de faire des **snapshots** de tes LXC en un clic. Avant chaque grosse mise à jour, prends un snapshot. Si ça plante, tu restaures en 10 secondes.

Clique sur ton LXC, onglet **Snapshots**, **Take Snapshot**. Donne-lui un nom explicite : `avant-maj-docker` par exemple. Tu gagneras un temps fou le jour où tout part en sucette.

## Cas d'usage typiques pour tes premiers LXC

Tu ne sais pas par où commencer ? Voici les services que je recommande de lancer en LXC plutôt qu'en VM.

### 1. DNS local (Pi-hole ou AdGuard Home)

Un DNS ne consomme rien. 64 Mo de RAM suffisent. Un LXC Debian + AdGuard Home, et tu bloques les pubs sur tout ton réseau.

### 2. Reverse proxy (Traefik ou Nginx Proxy Manager)

Si tu as déjà suivi mon guide sur [Traefik en Docker](/traefik-reverse-proxy-docker/), tu sais que c'est le cerveau de ton homelab. Le faire tourner dans un LXC léger est pertinent.

### 3. Monitoring (Uptime Kuma)

Uptime Kuma surveille tes services et t'alerte quand quelque chose tombe. Il consomme presque rien.

### 4. VPN (WireGuard ou Tailscale)

Un petit LXC pour ton VPN d'accès à distance. 128 Mo de RAM, un peu de CPU, et tu accèdes à ton réseau depuis n'importe où.

## Conclusion

Les conteneurs LXC sur Proxmox, c'est le sweet spot entre la lourdeur des VMs et la complexité de Kubernetes. Tu gardes un vrai système d'exploitation, tu peux y installer ce que tu veux, mais tu consommes 10 fois moins de ressources.

Mon conseil pour débuter : commence par 2 ou 3 LXC pour tes services les plus simples. Un DNS, un reverse proxy, un monitoring. Quand tu seras à l'aise, tu pourras en ajouter d'autres ou tester des VMs pour les plateformes plus lourdes.

Et n'oublie pas : un snapshot avant chaque modification. C'est la règle d'or du self-hoster. Pas de snapshot, pas de chocolat.
