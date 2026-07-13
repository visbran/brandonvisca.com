---
title: "nftables Docker : pare-feu nouvelle génération sous Linux"
description: "Guide nftables Docker : remplace iptables par un pare-feu moderne pour sécuriser tes conteneurs. Syntaxe claire, règles efficaces et compatibilité assurée."
pubDatetime: "2026-06-26T08:00:00.000Z"
modDatetime: "2026-06-26T08:00:00.000Z"
author: Brandon Visca
tags:
  - securite
  - linux
  - docker
  - nftables
  - pare-feu
  - intermediaire
featured: false
draft: false
focusKeyword: nftables docker
ogImage: ""
---
> 💡 **TL;DR**
> - nftables remplace iptables avec une syntaxe lisible, une meilleure perf et une gestion unifiée du filtrage
> - Docker s'appuie encore sur iptables par défaut, mais tu peux router tout le trafic conteneur vers nftables
> - Ce guide te montre comment configurer nftables pour Docker sans casser le réseau de tes conteneurs

## Pourquoi nftables et pas iptables

iptables, c'est le grand-père du pare-feu Linux. Il fonctionne, il est partout, mais il commence à sentir le moisi. Sa syntaxe est verbeuse, les règles s'accumulent dans des chaînes séparées (filter, nat, mangle), et la moindre modification demande de recharger toute la table. Quand tu as une cinquantaine de règles et que tu veux juste bloquer un port, tu transpires.

nftables, son successeur officiel depuis Linux 3.13, réunit tout dans un seul outil. Une syntaxe cohérente, des tables unifiées, des ensembles (sets) pour grouper des IP ou des ports, et une API netlink moderne. C'est plus rapide, plus lisible, et surtout : c'est l'avenir. Debian 12, Ubuntu 24.04, Fedora, tout le monde est passé à nftables en backend, même si la commande `iptables` existe encore via un wrapper de compatibilité.

Le problème, c'est Docker. Par défaut, il manipule directement les règles iptables pour créer ses bridges, ses NATs et ses port-forwardings. Quand tu installes Docker sur une machine fraîche, il injecte ses propres chaînes `DOCKER`, `DOCKER-ISOLATION`, `DOCKER-USER` dans iptables. Si tu configures nftables sans prendre ça en compte, tu te retrouves avec deux pare-feu qui se marchent sur les pieds. Résultat : soit Docker ne fonctionne plus, soit tes règles nftables sont contournées.

Si tu as déjà galéré avec [UFW et Docker](/ufw-docker-pare-feu-linux/), tu connais le concept. Docker ne passe pas par le pare-feu classique, il écrit directement dans les tables noyau. La différence avec nftables, c'est qu'on a plus de contrôle et qu'on peut tout centraliser proprement.

## Ce que Docker fait dans iptables (et pourquoi ça pose problème)

Quand tu lances un conteneur avec `-p 8080:80`, Docker fait trois choses dans iptables :

1. Il crée une règle DNAT dans la table `nat` pour rediriger le port 8080 de l'hôte vers le port 80 du conteneur
2. Il ajoute une règle dans la chaîne `FORWARD` de la table `filter` pour accepter ce trafic
3. Il masque (MASQUERADE) le trafic sortant des conteneurs pour qu'il utilise l'IP publique de l'hôte

Ces règles sont dynamiques. Elles apparaissent et disparaissent avec tes conteneurs. Si tu flushes iptables manuellement pour appliquer tes règles nftables, Docker perd sa connectivité réseau. Si tu laisses iptables tranquille et que tu configures nftables en parallèle, tu as deux systèmes de filtrage qui coexistent sans se parler.

La bonne nouvelle : nftables peut tout faire ce qu'iptables fait, et mieux. La mauvaise : il faut prendre le contrôle du réseau Docker pour que tout passe par nftables.

## La stratégie : isolation du bridge Docker

La méthode la plus propre consiste à désactiver la manipulation iptables par Docker et à gérer soi-même le NAT et le filtrage dans nftables. Docker expose un flag pour ça : `iptables: false` dans `/etc/docker/daemon.json`.

Attention : dès que tu désactives `iptables` dans Docker, tes conteneurs n'ont plus accès à internet et les ports mappés (`-p`) ne fonctionnent plus. Tu dois reconstruire toute la logique réseau dans nftables. C'est un peu de travail, mais une fois en place, c'est propre, versionnable et compréhensible.

Voici le plan :

1. Désactiver `iptables` dans Docker
2. Créer un bridge Docker personnalisé (ou utiliser `docker0`)
3. Configurer nftables avec une table qui gère l'input, le forward et le NAT
4. Ajouter des règles pour autoriser les conteneurs à sortir et pour mapper les ports entrants

## Étape 1 : désactiver iptables dans Docker

Crée ou modifie `/etc/docker/daemon.json` :

```json
{
  "iptables": false,
  "ip-forward": false,
  "userland-proxy": false
}
```

Redémarre Docker :

```bash
sudo systemctl restart docker
```

À partir de là, Docker ne touche plus à iptables. Tes conteneurs existants perdent probablement la connectivité, c'est normal.

## Étape 2 : configurer nftables pour Docker

Voici une configuration nftables complète qui gère un serveur avec Docker. Adapte l'interface publique (`eth0`) et le réseau des conteneurs (`172.17.0.0/16` pour `docker0`, ou ton sous-réseau custom).

Crée `/etc/nftables.conf` :

```nft
#!/usr/sbin/nft -f

flush ruleset

table inet filter {
    chain input {
        type filter hook input priority 0; policy drop;

        # Autoriser le loopback
        iif "lo" accept

        # Autoriser les connexions établies et liées
        ct state established,related accept

        # Autoriser le ping
        ip protocol icmp icmp type echo-request accept
        ip6 nexthdr icmpv6 icmpv6 type echo-request accept

        # SSH (adapte le port si besoin)
        tcp dport 22 accept

        # HTTP / HTTPS
        tcp dport { 80, 443 } accept

        # Ici, ajoute les ports mappés vers tes conteneurs
        # Exemple : Traefik sur 8080
        # tcp dport 8080 accept

        # Rejet explicite avec log (optionnel)
        log prefix "nftables dropped: " limit rate 5/second
        reject with icmpx type port-unreachable
    }

    chain forward {
        type filter hook forward priority 0; policy drop;

        # Autoriser le forwarding entre conteneurs et vers l'extérieur
        iifname "docker0" oifname "eth0" accept
        iifname "eth0" oifname "docker0" ct state established,related accept

        # Autoriser le forwarding entre conteneurs sur le même bridge
        iifname "docker0" oifname "docker0" accept
    }

    chain output {
        type filter hook output priority 0; policy accept;
    }
}

table ip nat {
    chain prerouting {
        type nat hook prerouting priority 0;

        # DNAT : rediriger les ports entrants vers les conteneurs
        # Exemple : port 8080 de l'hôte -> 172.17.0.2:80
        # tcp dport 8080 dnat to 172.17.0.2:80
    }

    chain postrouting {
        type nat hook postrouting priority 100;

        # Masquerade pour le trafic sortant des conteneurs
        oifname "eth0" ip saddr 172.17.0.0/16 masquerade
    }
}
```

Applique la configuration :

```bash
sudo nft -f /etc/nftables.conf
```

Pour rendre la config persistante au boot :

```bash
sudo systemctl enable nftables
```

## Étape 3 : mapper les ports vers tes conteneurs

Avec `iptables: false`, le flag `-p 8080:80` de `docker run` ne fait plus rien au niveau pare-feu. Il informe juste Docker qu'un port est exposé, mais le NAT doit être géré dans nftables.

Si tu as un conteneur Traefik à l'IP `172.17.0.2` qui écoute sur le port 80, ajoute cette règle dans la chaîne `prerouting` de ta table `nat` :

```nft
tcp dport 8080 dnat to 172.17.0.2:80
```

Pour trouver l'IP d'un conteneur :

```bash
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' nom_du_conteneur
```

Tu peux aussi utiliser un réseau Docker custom avec un subnet fixe pour avoir des IP prévisibles :

```bash
docker network create --subnet=172.20.0.0/16 mon-reseau
```

## Étape 4 : gérer les mises à jour sans tout casser

Le gros avantage de nftables sur iptables, c'est la gestion atomique. Tu peux tester ta configuration avant de l'appliquer :

```bash
sudo nft -c -f /etc/nftables.conf
```

Si la syntaxe est bonne, tu charges. Si tu te retranches, tu as toujours la console physique ou l'accès IPMI pour revenir en arrière. Sur un serveur distant, utilise `screen` ou `tmux` et programme un retour arrière automatique :

```bash
sudo sh -c 'sleep 120 && nft flush ruleset && nft -f /etc/nftables.conf.bak' &
sudo nft -f /etc/nftables.conf
```

Si tout va bien, tue le processus de secours. Si tu as perdu la connexion, il restaurera la config dans deux minutes.

## nftables vs UFW : que choisir avec Docker ?

Tu te demandes peut-être pourquoi s'embêter avec nftables alors que [UFW est simple](/ufw-docker-pare-feu-linux/) ? La réponse dépend de ton niveau et de tes besoins.

| Critère | UFW | nftables natif |
|---|---|---|
| Syntaxe | Simple, abstraite | Verbose mais logique et cohérente |
| Docker natif | Non (contournement nécessaire) | Oui, si tu désactives iptables dans Docker |
| Performance | Iptables en backend | Moteur natif, plus rapide |
| Lisibilité | Moyenne | Excellente avec des sets et des maps |
| Maintenance | Facile | Nécessite de comprendre le réseau Linux |

Si tu as un serveur avec trois conteneurs et que tu veux juste bloquer les ports inutiles, UFW suffit. Si tu veux un contrôle total du trafic, des règles complexes, du filtrage par groupe d'IP, ou si tu administres plusieurs serveurs, nftables est supérieur.

## Cas concret : homelab avec reverse proxy

Imagine ton homelab classique : un serveur avec [Caddy en reverse proxy](/caddy-docker-reverse-proxy-guide/), [WireGuard pour le VPN](/wireguard-docker-vpn-homelab/), et une dizaine de services en conteneur. Avec nftables, tu peux structurer ton pare-feu de manière logique :

- Tout le trafic entrant passe par Caddy (ports 80 et 443)
- Le port 22 (SSH) est accessible uniquement depuis ton IP fixe de bureau
- WireGuard (UDP 51820) est ouvert pour tes appareils mobiles
- Les conteneurs internes (base de données, cache Redis) ne sont pas exposés du tout
- Le forwarding entre conteneurs est autorisé uniquement sur le bridge Docker

Tu centralises tout dans un seul fichier nftables, lisible et versionnable. Pas de règles magiques injectées par Docker, pas de surprise quand tu rebootes.

Voici un exemple de set pour restreindre l'accès SSH :

```nft
set trusted_ssh {
    type ipv4_addr
    elements = { 192.168.1.10, 10.0.0.5 }
}

chain input {
    tcp dport 22 ip saddr @trusted_ssh accept
    tcp dport 22 drop
}
```

Tu ajoutes ou retires une IP en modifiant une seule ligne, sans réécrire toute la chaîne.

## Intégration avec Fail2Ban

Si tu utilises déjà [Fail2Ban pour protéger tes services](/fail2ban-docker-securite-serveur/), sache qu'il peut fonctionner avec nftables. Depuis la version 0.10, Fail2Ban supporte nativement un backend `nftables` qui crée des sets dynamiques pour bannir les IP.

Dans `jail.local` :

```ini
[DEFAULT]
banaction = nftables
banaction_allports = nftables[type=allports]
```

Fail2Ban ajoutera alors les IP bannies dans un set nftables temporaire, sans toucher à ta configuration statique. C'est élégant, propre, et ça ne rentre pas en conflit avec tes règles Docker.

## Pièges et erreurs courantes

**Docker ne démarre plus après avoir désactivé iptables**
C'est normal si tu as des conteneurs avec des ports mappés qui démarrent au boot. Désactive le démarrage auto des conteneurs concernés, configure nftables, puis relance Docker.

**Les conteneurs ne peuvent pas résoudre les noms de domaine**
Vérifie que le forwarding est bien activé au niveau du kernel et que ta règle de masquerade est correcte :

```bash
sysctl net.ipv4.ip_forward
```

Si ça retourne `0`, active-le :

```bash
sudo sysctl -w net.ipv4.ip_forward=1
```

Et rends-le persistant dans `/etc/sysctl.conf`.

**Le port mappé ne répond pas**
Vérifie trois choses : la règle DNAT dans nftables, l'IP du conteneur, et que le conteneur écoute bien sur `0.0.0.0` (pas sur `127.0.0.1`). C'est l'erreur la plus courante avec nginx ou Traefik dans un conteneur.

**nftables semble ne pas filtrer**
Assure-toi que nftables est chargé et que iptables n'est pas actif en parallèle. Sur certaines distributions, le wrapper iptables-nft peut créer des règles dans le backend nftables que tu ne vois pas avec `nft list ruleset`. Utilise `iptables-legacy` uniquement si tu sais ce que tu fais, ou mieux : désactive complètement iptables.

## Bonnes pratiques pour un pare-feu Docker solide

1. **Principe du moindre privilège** : n'ouvre que les ports strictement nécessaires. Ton portainer n'a pas besoin d'être exposé sur internet si tu y accèdes via WireGuard.

2. **Sépare les réseaux** : utilise des bridges Docker dédiés par famille de services (web, base de données, monitoring). Cela limite la surface d'attaque si un conteneur est compromis.

3. **Documente tes règles** : un commentaire dans le fichier nftables vaut mieux qu'une heure de debug six mois plus tard.

4. **Versionne ta config** : ton `nftables.conf` doit être dans un dépôt Git, comme ton `docker-compose.yml`.

5. **Teste régulièrement** : utilise `nmap` depuis une machine externe pour vérifier que seuls les ports attendus sont ouverts.

6. **Combine les outils** : nftables pour le pare-feu réseau, [Fail2Ban pour l'analyse de logs](/fail2ban-docker-securite-serveur/), et un [hardening système de base](/hardening-linux-10-commandes/) pour les couches basses.

## Conclusion : nftables docker, le futur du pare-feu Linux

nftables n'est pas qu'un remplacement d'iptables. C'est une opportunité de reprendre le contrôle total du réseau de tes conteneurs. Oui, ça demande un peu plus de travail initial qu'UFW. Oui, il faut comprendre comment Docker manipule le réseau sous le capot. Mais le résultat est un pare-feu lisible, performant et entièrement maîtrisé.

Dans un monde où Docker injecte des règles iptables opaques et où UFW se fait contourner, nftables est l'outil qui te remet aux commandes. Et si tu es déjà passé par le [durcissement de ton serveur Linux](/hardening-linux-10-commandes/), ajouter une couche nftables bien configurée est la dernière brique pour un homelab sérieusement sécurisé.

D'ailleurs, si tu envisages de remplacer Docker par une solution rootless, j'ai comparé [Podman vs Docker](/podman-vs-docker-rootless/) — le daemon-less et le rootless changent vraiment la donne.
