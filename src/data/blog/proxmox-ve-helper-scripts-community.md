---
title: "Proxmox VE Helper Scripts : installer des LXC en 1 clic"
description: Découvrez les Proxmox VE Helper Scripts pour déployer des conteneurs LXC en un clic. Guide pratique, sécurité et commandes copier-coller.
pubDatetime: 2026-07-15 08:00:00+00:00
modDatetime: 2026-07-15 08:00:00+00:00
author: Brandon Visca
tags:
  - debutant
  - linux
  - proxmox
  - lxc
  - sysadmin
  - auto-hebergement
featured: false
draft: false
focusKeyword: proxmox ve helper scripts
ogImage: "" 
---
> 💡 **TL;DR**
> - Les **Proxmox VE Helper Scripts** (anciennement tteck/Proxmox) permettent de déployer des conteneurs LXC préconfigurés en une seule commande.
> - Le projet est désormais maintenu par **community-scripts/ProxmoxVE** après l'archivage du repo original par tteck.
> - Toujours vérifier le code source sur GitHub avant d'exécuter un script : `curl | bash` sans contrôle, c'est jouer avec le feu.

## Table des matières

## Qu'est-ce que Proxmox VE Helper Scripts ?

Proxmox VE est une plateforme de virtualisation open-source ultra-populaire dans les homelabs. Elle combine la virtualisation complète (KVM/QEMU) et la virtualisation légère (LXC) dans une interface web unique. Le point de friction ? Configurer manuellement un conteneur LXC, installer les dépendances, régler les permissions et sécuriser le tout prend facilement 20 à 40 minutes.

Les **Proxmox VE Helper Scripts** sont un ensemble de scripts Bash open-source qui automatisent ce processus. En une seule commande, tu crées un conteneur LXC, configures le réseau, installe le service demandé et appliques les hardenings de base. Le résultat : un service fonctionnel en moins de 3 minutes, sans intervention manuelle.

Le projet a été lancé par **tteck** sur GitHub sous le repo `tteck/Proxmox`. Il est rapidement devenu la référence absolue pour les administrateurs système et les passionnés d'auto-hébergement. En 2024, tteck a archivé son repository. La communauté a alors forké le projet sous l'organisation **community-scripts/ProxmoxVE**, qui en assure désormais la maintenance active et l'évolution.

## Pourquoi c'est un game-changer

Avant les helper scripts, déployer un service sur Proxmox impliquait :

1. Créer manuellement le conteneur LXC via l'interface web
2. Se connecter en SSH au nœud Proxmox
3. Entrer dans le conteneur (`pct enter <id>`)
4. Mettre à jour les paquets, installer les dépendances
5. Configurer le service (fichiers de conf, permissions, utilisateurs)
6. Ouvrir les ports, configurer le pare-feu
7. Vérifier que tout fonctionne

Avec les helper scripts, cette procédure entière est condensée en une seule ligne de commande exécutée depuis le shell du nœud Proxmox. Le script gère la création du conteneur, l'installation des paquets, la configuration du service et même l'ajout de fonctionnalités avancées (mise à jour automatique, sauvegarde, intégration reverse proxy).

C'est particulièrement utile quand tu veux tester rapidement un outil sans polluer ton infrastructure existante. Tu lances le script, tu testes le service pendant une heure, et si ça ne te convient pas, tu supprimes le conteneur en deux clics. Zero residue.

Si tu débutes avec Docker et l'auto-hébergement, j'ai publié un [guide complet pour héberger tes premiers services avec Docker](/docker-debutant-services-auto-heberger/) qui complète parfaitement cette approche Proxmox + LXC.

## Prérequis

- Un nœud Proxmox VE fonctionnel (version 7.x ou 8.x recommandée)
- Accès root ou sudo sur le nœud Proxmox (les scripts s'exécutent sur l'hôte, pas dans le conteneur)
- Une connexion Internet active (les scripts téléchargent les paquets depuis les dépôts Debian/Ubuntu)
- Comprendre que ces scripts créent des conteneurs LXC **privilégiés** par défaut (tu peux opter pour un conteneur unprivilégié sur certains scripts)

## Installation d'un LXC en 1 clic : l'exemple Docker

Prenons le cas le plus courant : tu veux un conteneur LXC dédié à Docker, avec Docker Compose préinstallé, pour héberger tous tes services sans les mélanger avec l'hôte Proxmox.

Connecte-toi en SSH à ton nœud Proxmox et exécute :

```bash
bash -c "$(wget -qLO - https://github.com/community-scripts/ProxmoxVE/raw/main/ct/docker.sh)"
```

Le script va :

1. Télécharger le template Debian 12 ou Ubuntu 22.04 LTS
2. Créer un conteneur LXC avec les ressources par défaut (2 CPU, 2048 Mo RAM, 8 Go disque)
3. Installer Docker CE et Docker Compose
4. Configurer les permissions pour que l'utilisateur root du conteneur puisse gérer Docker
5. Afficher un récapitulatif avec l'IP du conteneur et les commandes utiles

Le conteneur est prêt en environ 2 minutes. Tu peux alors te connecter avec :

```bash
pct enter <ID_DU_CONTENEUR>
```

Vérifie l'installation :

```bash
docker --version
docker compose version
```

Tu peux immédiatement créer un répertoire `/opt/stacks/` et y placer tes fichiers `docker-compose.yml`. Si tu cherches des idées de services à déployer, mon guide sur [Chrony avec Docker pour un serveur NTP précis](/chrony-docker-serveur-ntp-homelab/) ou celui sur [GLPI avec Docker pour un ITSM auto-hébergé](/glpi-docker-itsm-auto-heberge/) sont de bons points de départ.

## Autres exemples populaires

Le repo community-scripts propose des centaines de scripts. Voici ceux que je déploie le plus régulièrement :

### Home Assistant OS

```bash
bash -c "$(wget -qLO - https://github.com/community-scripts/ProxmoxVE/raw/main/ct/homeassistant.sh)"
```

Crée un conteneur LXC avec Home Assistant Core ou Home Assistant Container. La version OS (supervised) est aussi disponible via un script dédié. Pratique pour la domotique sans avoir à gérer un Raspberry Pi séparé.

### Nextcloud

```bash
bash -c "$(wget -qLO - https://github.com/community-scripts/ProxmoxVE/raw/main/ct/nextcloud.sh)"
```

Déploie Nextcloud avec Apache, MariaDB, Redis et Let's Encrypt préconfigurés. Le script gère même la création de la base de données et l'utilisateur dédié.

### Pi-hole

```bash
bash -c "$(wget -qLO - https://github.com/community-scripts/ProxmoxVE/raw/main/ct/pihole.sh)"
```

Conteneur LXC avec Pi-hole prêt à filtrer le DNS de tout ton réseau. Le script configure le port 53 et les règles firewall nécessaires.

### WireGuard

```bash
bash -c "$(wget -qLO - https://github.com/community-scripts/ProxmoxVE/raw/main/ct/wireguard.sh)"
```

VPN WireGuard dans un conteneur LXC isolé. Le script génère les clés et te demande le nombre de clients à créer. J'ai aussi couvert [WireGuard avec Docker dans un guide dédié](/wireguard-docker-vpn-homelab/) si tu préfères une approche conteneurisée classique.

### AdGuard Home

```bash
bash -c "$(wget -qLO - https://github.com/community-scripts/ProxmoxVE/raw/main/ct/adguard.sh)"
```

Alternative à Pi-hole avec une interface plus moderne et le support DoH/DoT natif.

## Sécurité : ne jamais faire confiance aveuglément

C'est le moment de mettre les points sur les i. Exécuter `bash -c "$(wget -qLO - ... )"` télécharge un script depuis Internet et l'exécute immédiatement avec les privilèges root. C'est l'équivalent numérique de laisser entrer un inconnu chez toi en lui donnant les clés.

### Bonnes pratiques de sécurité

**1. Lire le script avant de l'exécuter**

Remplace `bash -c` par un téléchargement local :

```bash
wget -qLO /tmp/docker.sh https://github.com/community-scripts/ProxmoxVE/raw/main/ct/docker.sh
cat /tmp/docker.sh
```

Lis les 50 premières lignes. Vérifie qu'il télécharge bien depuis les dépôts officiels (github.com/community-scripts/ProxmoxVE), pas depuis un domaine louche.

**2. Vérifier le hash ou la signature si disponible**

Le repo community-scripts n'offre pas encore de signatures GPG sur tous les scripts, mais les fichiers sont versionnés et publics. Compare la dernière version avec le commit officiel sur GitHub.

**3. Isoler les conteneurs LXC**

Par défaut, les scripts créent des conteneurs **privilégiés** (l'option `unprivileged=0` dans la configuration LXC). Cela signifie que le conteneur partage le même namespace utilisateur que l'hôte. Si un service compromis échappe du conteneur, il a accès à l'hôte Proxmox.

Quand c'est possible (certains scripts le proposent), choisis l'option **unprivileged** (`unprivileged=1`). Le conteneur utilise alors des UID/GID mappés, ce qui limite drastiquement l'impact d'une évasion.

Pour les services exposés sur Internet (Nextcloud, Vaultwarden...), renforce la sécurité avec un pare-feu bien configuré. Mon article sur [nftables avec Docker](/nftables-docker-pare-feu-linux/) détaille une approche moderne applicable aussi à la protection de ton hôte Proxmox.

**4. Snapshots avant modifications**

Avant d'exécuter un helper script sur un conteneur existant (update script), crée un snapshot Proxmox :

```bash
vzdump <CTID> --mode snapshot --compress zstd
```

Si la mise à jour casse quelque chose, tu restaures en 30 secondes.

**5. Ne pas exposer les ports LXC directement sur Internet**

Utilise un reverse proxy (Traefik, Nginx Proxy Manager, Caddy) sur un autre conteneur pour router le trafic. N'ouvre jamais directement le port 80/443 d'un conteneur LXC vers Internet sans couche de protection intermédiaire.

## Fonctionnalités avancées des scripts

Les helper scripts ne se limitent pas à l'installation initiale. Ils proposent aussi :

### Scripts de mise à jour

Chaque service installé via helper script dispose généralement d'un script de mise à jour intégré. Depuis le conteneur, exécute :

```bash
update
```

Le script vérifie la dernière version disponible, télécharge les mises à jour et redémarre le service. C'est aussi simple que ça.

### Sauvegarde et restauration

Certains scripts intègrent des fonctions de backup vers NFS, Samba ou Proxmox Backup Server. C'est configurable lors de l'installation interactive.

### Personnalisation des ressources

Lors de l'exécution, le script te demande :
- L'ID du conteneur (ou en propose un libre automatiquement)
- La quantité de RAM
- Le nombre de cœurs CPU
- La taille du disque
- L'adresse IP (DHCP ou statique)

Tu peux donc adapter chaque conteneur à tes besoins sans éditer manuellement la configuration.

## Limites et points d'attention

### Pas de haute disponibilité native

Les conteneurs LXC créés par les scripts sont des instances uniques. Si tu veux du clustering Proxmox avec HA et migration live, il faut configurer manuellement le Ceph ou un stockage partagé. Les helper scripts ne gèrent pas cette partie.

### Dépendance à la communauté

Après le fork tteck -> community-scripts, le projet est sain et actif. Mais c'est un projet communautaire sans garantie commerciale. Si un script est abandonné ou contient un bug, la résolution dépend de la réactivité des contributeurs.

### Conteneurs privilégiés par défaut

Comme mentionné plus haut, le choix par défaut de conteneurs privilégiés facilite l'installation mais réduit l'isolation de sécurité. Pour un homelab personnel derrière un firewall, le risque est acceptable. Pour un environnement professionnel ou exposé, privilégie les conteneurs unprivilégiés et adapte les scripts manuellement.

## Conclusion

Les Proxmox VE Helper Scripts sont l'outil qui manquait à l'écosystème Proxmox. Ils transforment une procédure de 30 minutes en une commande de 2 minutes, sans sacrifier la qualité de la configuration. Le fork community-scripts/ProxmoxVE a pris le relais de manière professionnelle après l'arrêt du projet original par tteck, et la collection de scripts couvre aujourd'hui plus de 150 services différents.

La règle d'or reste inchangée : exécute toujours les scripts en comprenant ce qu'ils font, vérifie le code source sur GitHub, et garde des snapshots sous le coude. Avec ces précautions, les helper scripts deviendront rapidement ton meilleur allié pour faire évoluer ton homelab sans friction.
