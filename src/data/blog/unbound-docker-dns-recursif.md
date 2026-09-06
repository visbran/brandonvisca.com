---
title: "Unbound Docker DNS récursif auto-hébergé et performant"
description: "Déployez Unbound Docker DNS récursif et cache open-source pour accélérer vos requêtes, valider DNSSEC et gagner en souveraineté réseau."
pubDatetime: "2026-07-25T08:00:00.000Z"
modDatetime: "2026-07-25T08:00:00.000Z"
author: Brandon
tags:
  - reseau
  - docker
  - intermediaire
  - securite
featured: false
draft: false
focusKeyword: unbound docker dns récursif
ogImage: ""
---
> 💡 **TL;DR**
> - Unbound est un validateur DNS récursif et cache open-source développé par NLnet Labs.
> - En le conteneurisant avec Docker Compose, vous obtenez un resolver DNS local performant en quelques minutes.
> - C'est un complément idéal à un bloqueur comme [AdGuard Home](/adguard-home-docker-guide-2026/) : Unbound résout, AdGuard filtre.

## Table des matières

## Pourquoi héberger son propre resolver DNS

Chaque fois que vous ouvrez une page web, votre machine envoie une requête DNS pour traduire un nom de domaine en adresse IP. Par défaut, cette requête part vers le serveur DNS de votre FAI, un Google 8.8.8.8 ou un Cloudflare 1.1.1.1. C'est rapide, mais vous dépendez d'un tiers et vous laissez trainer vos requêtes de résolution chez eux.

Unbound change la donne. C'est un resolver DNS récursif et cache qui tourne chez vous. Il va lui-même interroger les serveurs racine de l'Internet, puis les TLD, puis les autoritaires, pour remonter la réponse. Résultat : vous ne dépendez plus d'un DNS public, vous validez DNSSEC sur votre propre infrastructure et vous cachez agressivement les réponses pour accélérer considérablement les requêtes suivantes.

Bref, Unbound ne filtre pas comme [AdGuard Home](/adguard-home-docker-guide-2026/). Il résout. Et c'est déjà énorme.

## Présentation d'Unbound

Unbound est un projet développé par NLnet Labs, la même maison qui maintient NSD et autres joyaux de l'infrastructure Internet. Distribué sous licence BSD, il est conçu pour la sécurité, la performance et la conformité aux standards. Contrairement à dnsmasq qui fait du forwarding vers un upstream, Unbound est un vrai résolveur récursif : il remonte la chaîne DNS depuis les root hints jusqu'au serveur autoritaire du domaine demandé.

Voici ce qu'il apporte nativement :

- **Validation DNSSEC** : il vérifie la signature cryptographique des réponses pour s'assurer qu'elles n'ont pas été altérées en route.
- **QNAME minimisation** (RFC 7816) : il n'envoie que le strict minimum d'informations aux serveurs intermédiaires, réduisant la fuite de données de navigation.
- **Cache agressif** : une fois une réponse obtenue, elle est stockée en local avec TTL respecté. Les requêtes suivantes sont quasi instantanées.
- **DNS-over-TLS (DoT)** : il peut chiffrer les requêtes sortantes vers un upstream de confiance.
- **Root hints** : il utilise la liste officielle des serveurs racine, pas un forwarder externe.

Pour l'homelab, c'est un outil de souveraineté réseau redoutable. Et en Docker, c'est un jeu d'enfant à déployer.

## Unbound vs dnsmasq vs AdGuard Home : qui fait quoi

On confond souvent les outils DNS parce qu'ils tournent tous sur le port 53. Pourtant, leur rôle est fondamentalement différent :

| Outil | Rôle principal | Résolution récursive | Filtrage publicitaire | Cache |
|-------|---------------|----------------------|----------------------|-------|
| **Unbound** | Resolver DNS récursif | Oui, natif | Non | Oui, très agressif |
| **dnsmasq** | Forwarder DNS / DHCP | Non, relaye vers upstream | Non | Oui, léger |
| **AdGuard Home** | DNS filtrant avec UI | Non, relaye vers upstream | Oui, listes intégrées | Oui |

La confusion vient du fait qu'on peut chaîner ces outils. Par exemple, faire pointer AdGuard Home vers Unbound comme upstream. AdGuard fait le filtrage et le joli tableau de bord, Unbound fait la vraie résolution récursive. C'est d'ailleurs la stack idéale pour un [homelab robuste](/wireguard-docker-vpn-homelab/) : souveraineté + contrôle + sécurité.

## Docker Compose : déployer Unbound en 5 minutes

L'image `mvance/unbound` est une des plus fiables et maintenues pour faire tourner Unbound en conteneur. Elle embarque une configuration de base fonctionnelle avec DNSSEC activé, QNAME minimisation et cache optimisé.

Vérifions les tags disponibles au moment où j'écris ces lignes : `1.22.0`, `1.21.1`, `1.21.0`, `1.20.0` et `latest`. Pour un environnement de production, je recommande de pinner sur une version explicite plutôt que `latest`.

Créez votre `docker-compose.yml` :

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

Le port 53 UDP est essentiel car DNS utilise majoritairement UDP. La capacité `NET_BIND_SERVICE` permet au conteneur non-root de binder sur un port privilégié. `no-new-privileges:true` est une bonne habitude de sécurité Docker.

Pourquoi choisir `mvance/unbound` plutôt qu'une image Alpine générique ? Cette image est maintenue par un contributeur actif de la communauté Unbound, elle embarque les root hints à jour, le fichier de trust anchor DNSSEC et une configuration de base déjà optimisée pour Docker. Vous pouvez aussi construire votre propre image à partir de `alpine:latest` avec le paquet `unbound`, mais vous devrez alors gérer vous-même les root hints et les permissions du conteneur. Pour débuter, `mvance/unbound` est le chemin de moindre résistance.

Ensuite, créez votre `unbound.conf` personnalisé :

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
```

Démarrez le conteneur :

```bash
docker compose up -d
```

Vérifiez qu'il répond correctement depuis votre hôte ou une machine du réseau local :

```bash
dig @localhost google.com
```

Si vous voyez une réponse avec le flag `ad` (authenticated data) dans la section flags, c'est que DNSSEC est bien validé. Sinon, vérifiez que le fichier `root.key` est bien généré dans le volume.

## Configurer vos clients pour utiliser Unbound

Une fois le conteneur actif, vous devez rediriger les requêtes DNS de vos appareils vers l'IP de votre serveur Docker.

Sur un routeur OpenWrt ou pfSense, renseignez l'IP de votre hôte Docker comme DNS unique. Sur vos postes Linux, modifiez `/etc/resolv.conf` ou utilisez systemd-resolved pour pointer vers votre instance Unbound. Si vous êtes en remote, pensez à sécuriser l'accès via un tunnel [WireGuard](/wireguard-docker-vpn-homelab/) ou un [Cloudflare Tunnel](/cloudflare-tunnel-docker-homelab/) plutôt que d'exposer le port 53 sur Internet.

Dans un setup avec AdGuard Home en frontal, configurez simplement l'upstream DNS d'AdGuard avec l'IP interne de votre conteneur Unbound (par exemple `10.0.0.5:53`). AdGuard filtre, Unbound résout, vous dormez sur vos deux oreilles.

Pour un déploiement Docker Compose intégré, vous pouvez même les mettre sur le même réseau bridge personnalisé et utiliser le nom de service comme upstream :

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

Puis dans l'interface AdGuard Home, définissez l'upstream `unbound:53`. Le trafic DNS reste entièrement interne au réseau Docker, sans jamais sortir de votre serveur. C'est élégant, performant et totalement découplé des DNS publics.

### Vérifier que tout fonctionne

Après avoir redirigé vos clients, testez avec plusieurs outils :

```bash
# Test de résolution classique
dig @192.168.1.100 google.com

# Vérifier DNSSEC (flag 'ad' doit apparaître)
dig @192.168.1.100 dnssec-failed.org

# Mesurer le temps de réponse
dig @192.168.1.100 +stats cloudflare.com | grep "Query time"
```

Le premier appel à un domaine inconnu prendra 20 à 60 millisecondes. Le second, grâce au cache, tombera sous la milliseconde. C'est là toute la magie d'un resolver local bien nourri.

## Sécuriser avec DNSSEC et QNAME minimisation

Deux fonctionnalités font toute la différence entre un DNS de base et Unbound bien configuré.

**DNSSEC** garantit l'intégrité des réponses. Quand un domaine est signé, Unbound remonte la chaîne de confiance depuis la racine jusqu'au domaine et vérifie chaque signature. Si une réponse est falsifiée, Unbound la rejette. C'est une protection contre le DNS spoofing et certaines attaques Man-in-the-Middle. Notez que si DNSSEC échoue pour un domaine non signé, Unbound retourne quand même la réponse ; il n'est pas bloquant, juste vigilant.

**QNAME minimisation** réduit la fuite de données. Sans elle, votre resolver envoie le nom de domaine complet à chaque serveur intermédiaire (par exemple, demander à `.com` : "où est google.com ?"). Avec QNAME minimisation, il demande d'abord seulement "qui gère .com ?", puis "qui gère google.com ?", sans révéler le full query aux étapes précédentes. C'est défini dans la RFC 7816 et activé par défaut dans la configuration ci-dessus.

## DNS-over-TLS : chiffrer les requêtes sortantes

Par défaut, Unbound fait de la résolution récursive en clair vers les serveurs racine et autoritaires. Si vous voulez chiffrer le trafic entre votre resolver et le reste du monde, vous pouvez configurer Unbound pour qu'il utilise DNS-over-TLS (DoT) vers un upstream de confiance pour les zones spécifiques, tout en gardant la résolution récursive pour le reste.

Dans la pratique, la plupart des utilisateurs conservent Unbound en mode récursif pur et ajoutent éventuellement une clause `forward-zone` pour certains TLD problématiques ou pour les requêtes internes. Voici un exemple de forward sécurisé vers Quad9 en DoT :

```conf
forward-zone:
    name: "."
    forward-ssl-upstream: yes
    forward-addr: 9.9.9.9@853
    forward-addr: 149.112.112.112@853
```

Attention : activer un forward global transforme Unbound en simple forwarder et annule l'intérêt de la résolution récursive directe. Utilisez cette config avec parcimonie, par exemple uniquement si votre FAI bloque les requêtes sortantes sur le port 53.

## Cas d'usage concrets dans un homelab

Unbound n'est pas qu'un toy DNS pour geeks. Il résout des vrais problèmes :

- **DNS central du réseau local** : au lieu de configurer chaque appareil avec 1.1.1.1, vous pointez tout vers Unbound. Vous contrôlez la résolution, vous cachez localement, vous réduisez la latence perçue.
- **Fallback Pi-hole / AdGuard** : si votre filtreur DNS tombe, Unbound peut prendre le relais en mode direct. Ou inversement, utilisez Unbound comme upstream exclusif d'AdGuard pour ne jamais dépendre de Google ni Cloudflare.
- **Réduction de latence** : après quelques heures d'utilisation, le cache d'Unbound contient déjà la majorité des domaines que vous consultez régulièrement. Les requêtes passent de 20-50 ms à moins de 1 ms.
- **Résolution interne** : en combinant Unbound avec des zones privées, vous pouvez résoudre vos propres domaines internes (`nas.local`, `pve.homelab`) sans passer par un DNS public.

## Monitoring et maintenance

Unbound expose des statistiques via une commande interne. Vous pouvez les consulter avec :

```bash
docker exec unbound unbound-control stats_noreset
```

Cette commande renvoie des indicateurs précis : nombre de requêtes servies depuis le cache, taux de réponses NXDOMAIN, temps moyen de résolution, état des threads. Pour un homelab, les métriques essentielles à surveiller sont le cache hit ratio (idéalement au-dessus de 80 % après quelques jours) et le nombre de requêtes rejetées pour cause de validation DNSSEC échouée. Si ce dernier grimpe soudainement, vérifiez que votre fichier `root.key` est à jour et que l'horloge système est synchronisée, DNSSEC est exigeant sur la précision temporelle.

Si vous souhaitez des métriques Prometheus, des exporters existent comme `github.com/letsencrypt/unbound_exporter`. Pour un homelab classique, un simple check avec `dig` dans un cron et un webhook vers votre dashboard [Beszel](/beszel-monitoring-docker/) ou [Netdata](/netdata-docker/) suffit amplement.

Voici un script de check minimal à placer dans votre crontab pour valider que le resolver répond toujours et que DNSSEC fonctionne :

```bash
#!/bin/bash
DNS_IP="192.168.1.100"

# Test résolution + DNSSEC flag
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

Le cache persiste dans le volume Docker, donc un redémarrage du conteneur ne le vide pas. Pensez à mettre à jour périodiquement les root hints et le trust anchor :

```bash
docker exec unbound unbound-anchor
```

## Conclusion

Unbound est l'outil qu'il manquait à votre stack réseau. Léger, sécurisé, véritablement récursif et open-source, il vous rend souverain sur la résolution DNS de votre infrastructure. Conteneurisé avec Docker Compose, il s'intègre en cinq minutes dans un homelab existant et devient rapidement invisible tant il fait bien son travail.

Associez-le à un bloqueur comme AdGuard Home, sécurisez l'accès avec un tunnel VPN ou Cloudflare, et vous obtenez une chaîne DNS complète : filtrage, résolution récursive, validation DNSSEC, chiffrement possible. Pas besoin de faire confiance à Google pour savoir où se trouve votre propre NAS.

Le DNS, c'est la fondation de tout. Autant en reprendre le contrôle.
