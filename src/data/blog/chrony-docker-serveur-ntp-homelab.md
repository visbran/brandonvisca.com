---
title: "Chrony Docker : serveur NTP précis pour ton homelab"
description: Déploie un serveur NTP précis avec Chrony sous Docker. Synchronisation temps Linux, config complète et comparatif chrony vs ntpd vs timesyncd.
pubDatetime: "2026-06-24T08:00:00.000Z"
modDatetime: "2026-06-24T08:00:00.000Z"
author: Brandon Visca
tags:
  - linux
  - docker
  - chrony
  - ntp
  - intermediaire
  - reseau
featured: false
draft: false
focusKeyword: chrony docker
faqs:
  - question: "Pourquoi choisir Chrony plutôt que systemd-timesyncd ?"
    answer: "Chrony offre une précision supérieure (jusqu'à quelques microsecondes), gère mieux les réseaux instables, conserve l'horloge correcte pendant les déconnexions, et peut servir de serveur NTP pour tout ton réseau local. systemd-timesyncd est un client simple, suffisant pour un poste de travail mais limité pour un homelab."
  - question: "Chrony Docker consomme-t-il beaucoup de ressources ?"
    answer: "Non. Chrony est extrêmement léger : environ 2 à 5 Mo de RAM, CPU quasi nul en temps normal, et zéro stockage disque significatif. C'est l'un des services Docker les plus économes que tu puisses faire tourner."
  - question: "Dois-je ouvrir un port sur mon pare-feu pour le serveur NTP ?"
    answer: "Oui, si tu veux que tes appareils locaux ou externes se synchronisent avec ton serveur. Le port UDP 123 est le standard NTP. Si tu ne veux synchroniser que l'hôte Docker lui-même, le port n'a pas besoin d'être exposé publiquement."
ogImage: ""
---
> 💡 **TL;DR**
> - Un serveur NTP local élimine les décalages d'horloge entre tes machines et tes logs
> - Chrony est plus précis et plus robuste que systemd-timesyncd ou ntpd classique
> - Tu le déploies en un conteneur Docker de 5 Mo avec un docker-compose.yml de 20 lignes
> - Cet article donne la config complète, les explications sur la synchro temps, et un tableau comparatif

## Table des matières

## Pourquoi un serveur NTP dans ton homelab ?

Quand tu as trois serveurs, un NAS, un routeur, un Raspberry Pi et un laptop qui se connectent à ton homelab, chacun a sa propre idée de l'heure exacte. À quelques secondes près, ce n'est pas grave. Sauf que quand tu regardes tes logs, quand tu débugges une erreur qui touche plusieurs services, ou quand tu configures une réplication de base de données, ces quelques secondes deviennent un cauchemar.

Imagine que Nextcloud logue une erreur à 14:23:17 et que ton reverse proxy Caddy l'enregistre à 14:23:22. Tu passes 20 minutes à chercher pourquoi les timestamps ne correspondent pas, alors que les deux machines ont juste des horloges désynchronisées. Ça m'est arrivé. Ça t'arrivera.

Un serveur NTP local résout ce problème de façon élégante. Toutes tes machines se synchronisent sur une source unique, hébergée chez toi. Tu réduis la dépendance aux serveurs publics, tu améliores la latence (un serveur local répond en millisecondes, pas en dizaines de millisecondes), et tu gardes un contrôle total sur la source de temps. Si tu débutes avec Docker, mon [guide Docker pour débutants](/docker-debutant-services-auto-heberger/) te donnera les bases avant d'attaquer cette stack.

Et quand tu choisis un serveur NTP, tu choisis Chrony.

## Chrony, c'est quoi exactement ?

Chrony est un implémentation NTP (Network Time Protocol) moderne qui remplace avantageusement le vénérable ntpd. Il est maintenu activement, intégré dans les distributions Linux modernes (Debian 12, Ubuntu 24.04, RHEL 9), et conçu pour les machines qui ne sont pas toujours en ligne ou qui vivent derrière des réseaux domestiques.

La différence fondamentale avec ntpd : Chrony n'essaie pas de corriger l'horloge système en une seule fois. Il ajuste progressivement la fréquence de l'oscillateur local pour que le temps s'écoule un peu plus vite ou un peu plus lentement, jusqu'à ce que la synchronisation soit atteinte. C'est plus doux, plus précis, et moins perturbant pour les applications sensibles au temps.

Chrony gère aussi mieux les réseaux à latence variable. Quand ta connexion Internet est partagée entre un téléchargement, un stream et un backup, la latence vers les serveurs NTP publics fluctue. ntpd interprète ces variations comme de l'erreur de temps et peut dégrader la qualité de sa synchronisation. Chrony utilise un algorithme de filtrage plus intelligent qui ignore les mesures aberrantes et privilégie les tendances stables.

Pour un homelab, c'est exactement ce qu'il te faut. Tu n'as pas un datacenter avec une connexion dédiée et symétrique. Tu as une box Fibre ou ADSL, des pics de latence, et des redémarrages occasionnels. Chrony s'adapte à ce chaos là où ntpd aurait tendance à dériver.

## Chrony vs ntpd vs systemd-timesyncd : le comparatif

| Critère | Chrony | ntpd | systemd-timesyncd |
|---------|--------|------|-------------------|
| **Précision** | Excellente (microsecondes) | Bonne (millisecondes) | Basique (secondes) |
| **Réseaux instables** | Excellent filtrage | Dégradation rapide | Acceptable |
| **Serveur NTP** | Oui, natif | Oui, natif | Non, client uniquement |
| **Hors ligne** | Estime le temps avec l'horloge locale | Dérive plus vite | Dérive rapidement |
| **Consommation** | Très faible (~2-5 Mo RAM) | Modérée | Très faible |
| **Courbe d'apprentissage** | Faible | Élevée (fichiers complexes) | Nulle |
| **Intégration Docker** | Excellente (image légère) | Complexe | Impossible (client seul) |
| **Cas d'usage idéal** | Homelab, serveur local | Datacenter traditionnel | Poste de travail |

Mon avis est clair : pour un homelab Docker, **Chrony est le choix par défaut**. systemd-timesyncd est pratique sur un laptop ou un desktop, mais il ne peut pas servir de serveur pour tes autres machines. ntpd fonctionne, mais il est plus lourd à configurer et moins tolérant aux réseaux domestiques. Si tu cherches à sécuriser l'ensemble de ton stack, j'ai un [guide UFW Docker](/ufw-docker-pare-feu-linux/) qui couvre la configuration réseau autour de tes conteneurs.

## Prérequis

Avant de lancer ton conteneur Chrony, vérifie ces quelques points :

- Un serveur Docker fonctionnel avec Docker Compose (si ce n'est pas fait, mon [guide Docker pour débutants](/docker-debutant-services-auto-heberger/) est le point de départ)
- Le port UDP 123 disponible sur l'hôte (ou un autre port si tu le remappes)
- Les droits root ou sudo pour gérer le réseau et les capabilities du conteneur
- Une connexion Internet pour la synchronisation initiale avec les pools NTP publics
- Optionnel : un nom de domaine ou une IP fixe pour que tes appareils locaux pointent vers ton serveur

Note sur le port : NTP utilise le port UDP 123 par défaut. Si ton hôte est déjà un client NTP (systemd-timesyncd ou chrony natif), le port 123 est probablement occupé. Tu dois soit désactiver le service NTP natif, soit mapper le conteneur sur un autre port (ex: 1234:123) et configurer tes clients en conséquence. Pour un usage interne, un port alternatif fonctionne parfaitement.

## Docker Compose complet pour ton serveur NTP

Voici le fichier `docker-compose.yml` prêt à l'emploi. Il utilise l'image officielle `cturra/chrony`, légère, maintenue, et préconfigurée avec les pools NTP publics. C'est le cœur de ton déploiement **chrony docker**.

```yaml
version: "3.8"

services:
  chrony:
    image: cturra/chrony:latest
    container_name: chrony
    restart: unless-stopped
    cap_add:
      - SYS_TIME
    ports:
      - "123:123/udp"
    environment:
      - NTP_SERVERS=pool.ntp.org,0.pool.ntp.org,1.pool.ntp.org,2.pool.ntp.org
      - LOG_LEVEL=0
    volumes:
      - chrony-data:/var/lib/chrony
    networks:
      - chrony-net

volumes:
  chrony-data:

networks:
  chrony-net:
    driver: bridge
```

### Explications ligne par ligne

**cap_add: SYS_TIME** : Chrony a besoin de modifier l'horloge système. Sans cette capability, le conteneur ne peut pas ajuster le temps de l'hôte et la synchronisation échoue silencieusement. C'est le seul privilege élevé nécessaire.

**ports: 123:123/udp** : NTP fonctionne en UDP, pas en TCP. Le mapping redirige le port 123 UDP de l'hôte vers le port 123 du conteneur. Si le port 123 est déjà pris sur l'hôte, change le premier nombre (ex: `1234:123/udp`).

**environment NTP_SERVERS** : La liste des serveurs NTP publics vers lesquels Chrony va se synchroniser. pool.ntp.org est un pool mondial qui redirige automatiquement vers les serveurs les plus proches. Tu peux remplacer par des serveurs régionaux (fr.pool.ntp.org, ch.pool.ntp.org) ou des serveurs internes si tu en as déjà un.

**LOG_LEVEL=0** : Le niveau de journalisation. 0 est le mode par défaut (infos et erreurs). Tu peux passer à 1 pour des logs plus détaillés si tu débugges.

**volumes chrony-data** : Chrony stocke sa base de dérive de l'horloge (drift file) dans `/var/lib/chrony`. Ce fichier permet à Chrony de maintenir une correction correcte même après un redémarrage du conteneur. Sans volume persistant, Chrony repart à zéro à chaque redémarrage et la convergence est plus lente.

### Lancer le conteneur

```bash
cd /chemin/vers/ton/docker-compose
sudo docker compose up -d
```

Vérifie que le conteneur tourne :

```bash
sudo docker logs chrony
```

Tu dois voir des lignes indiquant la synchronisation avec les serveurs NTP et le statut de l'horloge. Exemple de sortie :

```
2026-06-24T08:15:01Z chronyd version 4.5 starting
2026-06-24T08:15:01Z Disabled control of system clock
2026-06-24T08:15:02Z Selected source 162.159.200.123 (pool.ntp.org)
2026-06-24T08:15:02Z System clock wrong by 0.123456 seconds
```

### Vérifier la synchronisation depuis l'hôte

```bash
chronyc -h 127.0.0.1 tracking
```

Ou depuis l'intérieur du conteneur :

```bash
docker exec -it chrony chronyc tracking
```

La sortie te donne l'IP du serveur de référence, le décalage actuel (en secondes), la fréquence de l'horloge, et le statut de synchronisation. Si tu vois `Leap status : Normal`, tout est bon.

## Configurer tes clients pour utiliser ton serveur local

Le serveur tourne. Maintenant, il faut que tes machines locales s'y connectent. Voici les méthodes par système d'exploitation.

### Linux (systemd-timesyncd)

Édite `/etc/systemd/timesyncd.conf` :

```ini
[Time]
NTP=192.168.1.100
FallbackNTP=pool.ntp.org
```

Remplace `192.168.1.100` par l'IP de ton serveur Docker. Puis :

```bash
sudo systemctl restart systemd-timesyncd
sudo timedatectl status
```

### Linux (Chrony natif)

Édite `/etc/chrony/chrony.conf` et ajoute :

```
server 192.168.1.100 iburst
```

Puis :

```bash
sudo systemctl restart chronyd
sudo chronyc tracking
```

### Windows (PowerShell admin)

```powershell
w32tm /config /manualpeerlist:"192.168.1.100" /syncfromflags:manual /reliable:yes /update
Restart-Service w32time
w32tm /resync
```

Si tu administres un domaine Active Directory, sache que Windows gère déjà la synchro temps via w32time et que ton PDC Emulator doit pointer vers une source NTP fiable. J'explique toute la config dans mon guide [NTP pour Active Directory](/ntp-active-directory-synchroniser-domaines/).

### macOS

```bash
sudo sntp -sS 192.168.1.100
```

Pour une configuration permanente, utilise `systemsetup` ou le panneau Date & Heure.

### Routeurs et équipements réseau

La plupart des routeurs domestiques (OpenWrt, pfSense, OPNsense) permettent de définir un serveur NTP personnalisé dans leur interface web. Pointe-les vers l'IP de ton serveur Docker. C'est particulièrement utile pour les logs du routeur et les règles de firewall horodatées.

## Sécurité et bonnes pratiques

Un serveur NTP expose le port UDP 123. C'est un protocole léger et historiquement utilisé dans des attaques par amplification (NTP monlist). Voici comment sécuriser ton déploiement.

**Désactiver monlist et restrict** : L'image cturra/chrony désactive monlist par défaut. Chrony ne supporte pas cette commande legacy de toute façon, donc le risque d'amplification est nul avec cette image.

**Limiter l'accès à ton réseau local** : Si tu n'as pas besoin d'exposer ton serveur NTP à Internet, configure le pare-feu de l'hôte pour bloquer le port 123 UDP depuis l'extérieur. Avec UFW :

```bash
sudo ufw allow from 192.168.1.0/24 to any port 123 proto udp
sudo ufw deny 123/udp
```

Si tu cherches à sécuriser davantage ton serveur Docker, j'ai un [guide WireGuard Docker](/wireguard-docker-vpn-homelab/) qui te permet de créer un tunnel VPN pour accéder à tes services sans les exposer publiquement. C'est le complément naturel d'un serveur NTP local.

**Ne pas synchroniser avec une seule source** : Même si ton serveur local est la source principale pour tes clients, le serveur Chrony lui-même doit se synchroniser avec plusieurs sources externes (au moins 3 ou 4). Cela évite qu'une source corrompue ou compromise injecte une heure fausse dans tout ton réseau. Le pool.ntp.org est conçu pour ça : il te donne accès à des centaines de serveurs redondants.

**Monitoring simple** : Ajoute un check dans ton monitoring (Uptime Kuma, Beszel, ou un simple [cron job](/cron-linux-avance-crontab-guide/)) qui vérifie que `chronyc tracking` retourne un statut normal. Si le conteneur redémarre ou perd sa connexion, tu veux le savoir avant que tes logs ne partent en vrille.

## Dépannage des problèmes courants

### Le conteneur ne démarre pas (port déjà utilisé)

```bash
sudo ss -ulnp | grep 123
```

Si tu vois `systemd-timesyncd` ou `chronyd` natif, arrête-les :

```bash
sudo systemctl stop systemd-timesyncd
sudo systemctl disable systemd-timesyncd
```

### La synchronisation est lente après le premier démarrage

C'est normal. Chrony a besoin de plusieurs mesures (souvent 5 à 10 minutes) pour évaluer la qualité des sources et commencer à ajuster l'horloge. Laisse tourner. Le drift file persistant accélère cette phase après les redémarrages suivants.

### Les clients ne se synchronisent pas

Vérifie que le port UDP 123 est bien ouvert sur le firewall de l'hôte Docker. UFW ou iptables bloquent souvent le UDP par défaut. Teste la connectivité depuis un client :

```bash
ntpdate -q 192.168.1.100
```

Ou avec `chronyc` :

```bash
chronyc -h 192.168.1.100 sources
```

### Le conteneur redémarre en boucle

Vérifie les logs avec `docker logs --tail 50 chrony`. Les causes fréquentes : capability SYS_TIME manquante, image incompatible avec l'architecture (ARM vs x86_64), ou erreur de syntaxe dans le docker-compose.yml.

## Conclusion

Un serveur NTP local, c'est un de ces services que tu installes une fois et que tu oublies ensuite. Mais quand il est absent, tu le regrette à chaque fois que tu compares des logs, que tu débugges une réplication, ou que tu remarques que ton NAS a décidé qu'il était 14:47 alors que ton serveur disait 14:45.

Chrony en Docker est la solution la plus simple et la plus élégante pour un homelab. Un conteneur de 5 Mo, un docker-compose.yml de 20 lignes, et tu as une source de temps précise et fiable pour tout ton réseau. Pas besoin d'installer des paquets natifs sur chaque machine, pas de conflits de versions, pas de configuration système à maintenir. Tu montes le conteneur, tu pointes tes clients, et tu oublies. Et si tu cherches à automatiser encore plus ton infrastructure Proxmox, j'ai publié un guide sur les [Proxmox VE Helper Scripts](/proxmox-ve-helper-scripts-community/) qui te permettent d'installer des LXC préconfigurés en un clic.

C'est exactement ce que l'auto-hébergement fait de mieux : prendre le contrôle d'un service basique, le rendre plus fiable que la solution par défaut, et le maintenir avec une complexité proche de zéro.
