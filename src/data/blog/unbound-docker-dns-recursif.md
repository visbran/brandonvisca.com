---
title: "Unbound Docker DNS récursif auto-hébergé et performant"
description: "Unbound Docker DNS récursif : déploie un résolveur et cache open source pour accélérer tes requêtes, valider DNSSEC et te passer des DNS publics."
pubDatetime: "2026-07-25T08:00:00.000Z"
modDatetime: "2026-10-04T00:00:00+02:00"
author: Brandon Visca
tags:
  - reseau
  - docker
  - intermediaire
  - securite
featured: false
draft: false
focusKeyword: unbound docker dns récursif
ogImage: ""
faqs:
  - question: "Quelle différence entre Unbound et AdGuard Home ?"
    answer: "AdGuard Home filtre les requêtes et les relaie vers un serveur DNS en amont. Unbound résout lui-même les noms en interrogeant les serveurs racine, puis ceux des domaines. Les deux se combinent : AdGuard filtre, Unbound résout."
  - question: "Comment utiliser Unbound comme serveur amont d'AdGuard Home ?"
    answer: "Mets les deux conteneurs sur le même réseau Docker et indique unbound:53 comme upstream dans AdGuard Home. Les requêtes DNS restent alors internes à ton serveur."
  - question: "Comment vérifier que DNSSEC fonctionne ?"
    answer: "Interroge Unbound avec dig, par exemple dig @localhost suivi d'un domaine signé : le flag ad dans la réponse indique que DNSSEC a été validé. Sinon, vérifie la présence du fichier root.key."
  - question: "Faut-il configurer un forward vers un DNS public ?"
    answer: "Non. Un forward global sur la zone racine transforme Unbound en simple relais et lui fait perdre l'intérêt de la résolution récursive. Réserve forward-zone à des cas précis, comme des zones internes."
---
> 💡 **TL;DR**
> - Unbound est un résolveur DNS récursif, validant et cache, open source, développé par NLnet Labs.
> - En le conteneurisant avec Docker Compose, tu obtiens un résolveur DNS local performant en quelques minutes.
> - C'est un complément idéal à un bloqueur comme [AdGuard Home](/adguard-home-docker-guide-2026/) : Unbound résout, AdGuard filtre.

## Table des matières

## Pourquoi héberger ton propre résolveur DNS

Chaque fois que tu ouvres une page web, ta machine envoie une requête DNS pour traduire un nom de domaine en adresse IP. Par défaut, cette requête part vers le serveur DNS de ton FAI, un Google 8.8.8.8 ou un Cloudflare 1.1.1.1. C'est rapide, mais tu dépends d'un tiers et tu laisses traîner tes requêtes de résolution chez lui.

Unbound change la donne. C'est un résolveur DNS récursif et cache qui tourne chez toi. Il interroge lui-même les serveurs racine d'Internet, puis ceux des TLD, puis les serveurs faisant autorité, pour remonter la réponse. Résultat : tu ne dépends plus d'un DNS public, tu valides DNSSEC sur ta propre infrastructure et tu gardes les réponses en cache pour accélérer nettement les requêtes suivantes.

Bref, Unbound ne filtre pas comme [AdGuard Home](/adguard-home-docker-guide-2026/). Il résout. Et c'est déjà énorme.

## Présentation d'Unbound

Unbound est développé par NLnet Labs, la même maison qui maintient NSD et d'autres briques de l'infrastructure d'Internet. Distribué sous licence BSD, il est conçu pour la sécurité, la performance et le respect des standards. Contrairement à dnsmasq, qui relaie les requêtes vers un serveur amont, Unbound est un vrai résolveur récursif : il remonte la chaîne DNS depuis les serveurs racine jusqu'au serveur qui fait autorité pour le domaine demandé.

Voici ce qu'il apporte nativement :

- **Validation DNSSEC** : il vérifie la signature cryptographique des réponses pour s'assurer qu'elles n'ont pas été altérées en route.
- **QNAME minimisation** (RFC 7816) : il n'envoie que le strict minimum d'informations aux serveurs intermédiaires, ce qui limite la fuite de tes données de navigation.
- **Cache** : une fois une réponse obtenue, elle est gardée en mémoire en respectant son TTL. Les requêtes suivantes sont quasi instantanées.
- **DNS-over-TLS (DoT)** : il peut chiffrer les requêtes sortantes vers un serveur amont de confiance.
- **Root hints** : il part de la liste officielle des serveurs racine, pas d'un DNS public.

Pour un homelab, c'est un outil de souveraineté réseau redoutable. Et en Docker, c'est un jeu d'enfant à déployer.

## Unbound vs dnsmasq vs AdGuard Home : qui fait quoi

On confond souvent les outils DNS parce qu'ils tournent tous sur le port 53. Pourtant, leur rôle est fondamentalement différent :

| Outil | Rôle principal | Résolution récursive | Filtrage publicitaire | Cache |
|-------|---------------|----------------------|----------------------|-------|
| **Unbound** | Résolveur DNS récursif | Oui, natif | Non | Oui, configurable |
| **dnsmasq** | Relais DNS / DHCP | Non, relaie vers un serveur amont | Non | Oui, léger |
| **AdGuard Home** | DNS filtrant avec interface | Non, relaie vers un serveur amont | Oui, listes intégrées | Oui |

La confusion vient du fait qu'on peut chaîner ces outils. Par exemple, faire pointer AdGuard Home vers Unbound comme serveur amont : AdGuard fait le filtrage et le joli tableau de bord, Unbound fait la vraie résolution récursive. C'est d'ailleurs la stack idéale pour un [homelab robuste](/wireguard-docker-vpn-homelab/) : souveraineté, contrôle et sécurité.

## Docker Compose : déployer Unbound en 5 minutes

L'image communautaire `mvance/unbound` est l'une des plus utilisées pour faire tourner Unbound en conteneur. Elle embarque une configuration de base fonctionnelle avec DNSSEC activé et QNAME minimisation.

Au moment où j'écris ces lignes, les tags disponibles sont `1.22.0`, `1.21.1`, `1.21.0`, `1.20.0` et `latest`. En production, épingle une version explicite plutôt que `latest`.

Crée ton `docker-compose.yml` :

```yaml
services:
  unbound:
    image: mvance/unbound:1.22.0
    container_name: unbound
    restart: unless-stopped
    ports:
      - "53:53/tcp"
      - "53:53/udp"
    volumes:
      - ./unbound.conf:/opt/unbound/etc/unbound/unbound.conf:ro
      - unbound-data:/opt/unbound/etc/unbound/var
    environment:
      - PUID=1000
      - PGID=1000
    cap_add:
      - NET_BIND_SERVICE
    security_opt:
      - no-new-privileges:true
    networks:
      - dns-net

volumes:
  unbound-data:

networks:
  dns-net:
    driver: bridge
```

Le port 53 en UDP est essentiel, car DNS passe majoritairement par UDP. La capacité `NET_BIND_SERVICE` permet au conteneur non-root d'écouter sur un port privilégié. `no-new-privileges:true` est une bonne habitude de sécurité Docker.

Pourquoi `mvance/unbound` plutôt qu'une image Alpine générique ? Elle embarque les root hints, le fichier de trust anchor DNSSEC et une configuration de base déjà adaptée à Docker. Tu peux aussi construire ta propre image à partir d'`alpine` avec le paquet `unbound`, mais tu devras alors gérer toi-même les root hints et les permissions du conteneur. Pour débuter, `mvance/unbound` est le chemin le plus simple.

Ensuite, crée ton `unbound.conf` personnalisé :

```conf
server:
    verbosity: 1
    num-threads: 2
    interface: 0.0.0.0
    port: 53
    do-ip4: yes
    do-ip6: no
    do-udp: yes
    do-tcp: yes
    access-control: 127.0.0.0/8 allow
    access-control: 10.0.0.0/8 allow
    access-control: 172.16.0.0/12 allow
    access-control: 192.168.0.0/16 allow
    access-control: 0.0.0.0/0 refuse
    hide-identity: yes
    hide-version: yes
    qname-minimisation: yes
    harden-glue: yes
    harden-dnssec-stripped: yes
    harden-referral-path: yes
    unwanted-reply-threshold: 10000
    val-clean-additional: yes
    edns-buffer-size: 1232
    prefetch: yes
    prefetch-key: yes
    cache-min-ttl: 300
    cache-max-ttl: 86400
    msg-cache-slabs: 2
    rrset-cache-slabs: 2
    infra-cache-slabs: 2
    key-cache-slabs: 2
    rrset-cache-size: 128m
    msg-cache-size: 64m
    so-rcvbuf: 1m
    so-sndbuf: 1m
    private-address: 10.0.0.0/8
    private-address: 172.16.0.0/12
    private-address: 192.168.0.0/16

    # DNSSEC validation
    auto-trust-anchor-file: /opt/unbound/etc/unbound/var/root.key
    val-permissive-mode: no

    # Root hints
    root-hints: /opt/unbound/etc/unbound/var/root.hints

    # Logging
    log-queries: no
    logfile: ""
    use-syslog: no

    # Performance
    outgoing-range: 8192
    num-queries-per-thread: 4096

# Nécessaire pour unbound-control (statistiques), en local uniquement
remote-control:
    control-enable: yes
    control-interface: 127.0.0.1
    control-use-cert: no
```

Démarre le conteneur :

```bash
docker compose up -d
```

Vérifie qu'il répond correctement depuis ton hôte ou une machine du réseau local :

```bash
dig @localhost cloudflare.com
```

Si tu vois le flag `ad` (authenticated data) dans la section flags, DNSSEC est bien validé : `cloudflare.com` est un domaine signé. Sinon, vérifie que le fichier `root.key` est bien présent dans le volume.

## Configurer tes clients pour utiliser Unbound

Une fois le conteneur actif, redirige les requêtes DNS de tes appareils vers l'IP de ton serveur Docker.

Sur un routeur OpenWrt ou pfSense, renseigne l'IP de ton hôte Docker comme unique serveur DNS. Sur tes postes Linux, modifie `/etc/resolv.conf` ou passe par systemd-resolved pour pointer vers ton instance Unbound. Pour un accès à distance, passe par un tunnel [WireGuard](/wireguard-docker-vpn-homelab/) plutôt que d'exposer le port 53 sur Internet : un résolveur ouvert à tous sert vite de relais aux attaques par amplification.

Dans un setup avec AdGuard Home en frontal, configure simplement le serveur amont d'AdGuard avec l'IP interne de ton conteneur Unbound (par exemple `10.0.0.5:53`). AdGuard filtre, Unbound résout, et tu dors sur tes deux oreilles.

Pour un déploiement Docker Compose intégré, tu peux même les mettre sur le même réseau bridge personnalisé et utiliser le nom de service comme serveur amont :

```yaml
# Extrait du compose AdGuard Home
services:
  adguardhome:
    image: adguard/adguardhome:v0.107.61
    networks:
      - dns-net
    # ...

  unbound:
    image: mvance/unbound:1.22.0
    networks:
      - dns-net
    # ...
```

Puis, dans l'interface d'AdGuard Home, définis le serveur amont `unbound:53`. Le trafic DNS reste entièrement interne au réseau Docker, sans jamais sortir de ton serveur. C'est propre, performant et totalement découplé des DNS publics.

### Vérifier que tout fonctionne

Après avoir redirigé tes clients, teste avec plusieurs commandes :

```bash
# Test de résolution classique (flag 'ad' attendu sur un domaine signé)
dig @192.168.1.100 cloudflare.com

# Vérifier que DNSSEC rejette un domaine volontairement mal signé : réponse SERVFAIL attendue
dig @192.168.1.100 dnssec-failed.org

# Mesurer le temps de réponse
dig @192.168.1.100 +stats cloudflare.com | grep "Query time"
```

Le premier appel à un domaine inconnu prend quelques dizaines de millisecondes. Le second, servi par le cache, tombe sous la milliseconde. C'est tout l'intérêt d'un résolveur local.

## Sécuriser avec DNSSEC et QNAME minimisation

Deux fonctionnalités font toute la différence entre un DNS de base et un Unbound bien configuré.

**DNSSEC** garantit l'intégrité des réponses. Quand un domaine est signé, Unbound remonte la chaîne de confiance depuis la racine jusqu'au domaine et vérifie chaque signature. Si la validation échoue, Unbound ne renvoie pas la réponse falsifiée mais une erreur SERVFAIL : c'est une protection contre l'empoisonnement de cache et certaines attaques de type man-in-the-middle. Les domaines qui ne sont pas signés du tout, eux, sont résolus normalement, sans le flag `ad`.

**QNAME minimisation** réduit la fuite de données. Sans elle, ton résolveur envoie le nom de domaine complet à chaque serveur intermédiaire (par exemple, il demande à `.com` : « où est google.com ? »). Avec QNAME minimisation, il demande d'abord seulement « qui gère .com ? », puis « qui gère google.com ? », sans révéler la requête complète aux étapes précédentes. C'est défini dans la RFC 7816 et activé dans la configuration ci-dessus.

## DNS-over-TLS : chiffrer les requêtes sortantes

Par défaut, Unbound fait de la résolution récursive en clair vers les serveurs racine et ceux qui font autorité. Si tu veux chiffrer le trafic entre ton résolveur et le reste du monde, tu peux configurer Unbound pour qu'il passe en DNS-over-TLS (DoT) vers un serveur amont de confiance pour certaines zones, tout en gardant la résolution récursive pour le reste.

Dans la pratique, la plupart des utilisateurs gardent Unbound en mode récursif pur et ajoutent éventuellement une clause `forward-zone` pour certains domaines ou pour les requêtes internes. Voici un exemple de relais chiffré vers Quad9 en DoT :

```conf
forward-zone:
    name: "."
    forward-ssl-upstream: yes
    forward-addr: 9.9.9.9@853
    forward-addr: 149.112.112.112@853
```

Attention : un forward sur la zone `"."` transforme Unbound en simple relais et annule l'intérêt de la résolution récursive. Utilise cette configuration avec parcimonie, par exemple uniquement si ton FAI bloque les requêtes sortantes sur le port 53.

## Cas d'usage concrets dans un homelab

Unbound n'est pas un jouet pour geeks. Il résout de vrais problèmes :

- **DNS central du réseau local** : au lieu de configurer chaque appareil avec 1.1.1.1, tu pointes tout vers Unbound. Tu contrôles la résolution, tu caches localement, tu réduis la latence perçue.
- **Serveur amont d'AdGuard Home ou de Pi-hole** : utilise Unbound comme unique serveur amont de ton filtreur pour ne plus dépendre de Google ni de Cloudflare.
- **Réduction de latence** : après quelques heures d'utilisation, le cache d'Unbound contient déjà la plupart des domaines que tu consultes régulièrement. Les requêtes passent de plusieurs dizaines de millisecondes à moins d'une.
- **Résolution interne** : avec des zones locales, tu peux résoudre tes propres noms internes (`nas.home.arpa`, `pve.home.arpa`) sans passer par un DNS public.

## Monitoring et maintenance

Unbound expose des statistiques via `unbound-control`, activé par la section `remote-control` de la configuration ci-dessus :

```bash
docker exec unbound unbound-control stats_noreset
```

Cette commande renvoie des indicateurs précis : nombre de requêtes servies depuis le cache, réponses NXDOMAIN, temps moyen de résolution, état des threads. Pour un homelab, les métriques essentielles sont le taux de réponses servies par le cache et le nombre de requêtes en échec de validation DNSSEC. Si ce dernier grimpe soudainement, vérifie que ton fichier `root.key` est à jour et que l'horloge du serveur est synchronisée : DNSSEC est exigeant sur l'heure.

Si tu veux des métriques Prometheus, il existe des exporters, comme `github.com/letsencrypt/unbound_exporter`. Pour un homelab classique, un simple check avec `dig` dans un cron, relié à ton outil de supervision ([Beszel](/beszel-monitoring-docker/) ou [Netdata](/netdata-docker/)), suffit amplement.

Voici un script de vérification minimal à placer dans ta crontab, pour contrôler que le résolveur répond toujours et que DNSSEC fonctionne :

```bash
#!/bin/bash
DNS_IP="192.168.1.100"

# Test DNSSEC : un domaine volontairement mal signé doit être rejeté
if dig @$DNS_IP +dnssec dnssec-failed.org | grep -q "SERVFAIL"; then
    echo "DNSSEC OK — domaine invalide bien rejeté"
else
    echo "ALERTE : DNSSEC non fonctionnel"
fi

# Test latence
LATENCY=$(dig @$DNS_IP +stats +nocmd google.com | awk '/Query time/{print $4}')
if [ "$LATENCY" -gt 100 ]; then
    echo "Latence élevée : ${LATENCY} ms"
else
    echo "Latence OK : ${LATENCY} ms"
fi
```

Le cache d'Unbound vit **en mémoire** : un redémarrage du conteneur le vide, et il se reconstitue au fil des requêtes. Le volume ne conserve que les fichiers de travail, comme `root.key`. Pour garder le cache d'un redémarrage à l'autre, il faudrait le module `cachedb` avec un backend Redis, ce qui est rarement utile en homelab.

Le trust anchor DNSSEC (`root.key`) est tenu à jour automatiquement grâce à `auto-trust-anchor-file`. Pour le réinitialiser à la main, par exemple après une longue période hors ligne :

```bash
docker exec unbound unbound-anchor -a /opt/unbound/etc/unbound/var/root.key
```

💡 À lire aussi : [Authelia Docker : authentification double facteur centralisée pour ton homelab](/authelia-docker-authentification-2fa-homelab/), dans la même veine que cet article.

💡 À lire aussi : [Headscale Docker : serveur Tailscale auto-hébergé (open-source)](/headscale-docker-tailscale-self-hosted/), dans la même veine que cet article.

## Conclusion

Unbound est l'outil qu'il manquait à ta stack réseau. Léger, sécurisé, véritablement récursif et open source, il te rend souverain sur la résolution DNS de ton infrastructure. Conteneurisé avec Docker Compose, il s'intègre en cinq minutes dans un homelab existant et se fait vite oublier tant il fait bien son travail.

Associe-le à un bloqueur comme AdGuard Home, garde l'accès distant derrière un VPN, et tu obtiens une chaîne DNS complète : filtrage, résolution récursive, validation DNSSEC, chiffrement possible. Pas besoin de faire confiance à Google pour savoir où se trouve ton propre NAS.

Le DNS, c'est la fondation de tout. Autant en reprendre le contrôle.
