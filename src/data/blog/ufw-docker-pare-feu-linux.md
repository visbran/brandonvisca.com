---
title: "UFW Docker : configurer le pare-feu sans casser les conteneurs"
description: "Guide UFW Docker : pare-feu Linux simple qui fonctionne avec tes conteneurs. Règles, pièges iptables et solution complète."
pubDatetime: "2026-06-03T08:00:00.000Z"
modDatetime: "2026-06-03T14:00:00.000Z"
author: Brandon Visca
tags:
  - linux
  - docker
  - securite
  - debutant
featured: false
draft: false
---
**TL;DR** — UFW est le pare-feu le plus simple sous Linux, mais Docker contourne ses règles en manipulant iptables directement. Résultat : tes ports exposés restent accessibles depuis l'extérieur même si UFW dit le contraire. On va configurer UFW correctement avec Docker pour que tes règles de pare-feu soient réellement respectées, sans bloquer les conteneurs qui doivent communiquer entre eux.

## Pourquoi UFW et Docker ne s'entendent pas

Quand tu installes UFW (`ufw enable`) et que tu bloques tout sauf SSH et HTTP, tu t'attends à ce que seuls ces ports soient ouverts. Sauf que Docker ne passe pas par UFW. Il injecte ses propres règles directement dans `iptables`, en amont de la chaîne `ufw-user-input`. Autrement dit, UFW dit "non" et Docker dit "oui" juste derrière. Le "oui" de Docker gagne.

C'est un comportement documenté mais trompeur. Tu configures UFW, tu regardes `ufw status` qui affiche une belle liste de ports fermés, et pourtant `nmap` depuis une machine externe te montre que le port 8080 de ton conteneur Traefik est bien ouvert. Parce que Docker a créé une règle `DOCKER` dans `iptables` qui accepte tout ce qui arrive sur les ports mappés (`-p 8080:8080`).

Si tu as déjà mis en place [Fail2Ban avec Docker](/fail2ban-docker-securite-serveur/), tu sais que la sécurité réseau en conteneurs demande de comprendre comment iptables fonctionne derrière. UFW n'est pas différent : il faut un réglage supplémentaire.

## UFW, iptables, nftables : que choisir ?

| Critère | UFW | iptables brut | nftables | Docker (réseau natif) |
|---------|-----|---------------|----------|----------------------|
| **Abstraction** | Syntaxe simple (`allow 22`) | Règles complexes, chaînes multiples | Syntaxe moderne, tables unifiées | Réseau bridge/NAT automatique |
| **Compatibilité Docker** | Cassée par défaut | Fonctionne si bien configuré | Fonctionne sur Debian 12+ / Ubuntu 24+ | Fonctionne, mais ouvre tout |
| **Courbe d'apprentissage** | Très faible | Élevée | Modérée | Faible pour l'usage basique |
| **Granularité** | Ports et IPs | Tout est possible | Tout est possible | Par conteneur, par réseau |
| **Maintenance** | Facile | Verbeuse, sujette aux erreurs | Plus propre qu'iptables | Zéro config nécessaire |
| **Cas d'usage idéal** | Serveur perso, homelab | Firewall d'entreprise, routing complexe | Nouveaux projets, Debian 12+ | Développement local uniquement |

Mon avis : pour un serveur auto-hébergé avec Docker, **UFW reste le meilleur compromis**. À condition de corriger le problème iptables. iptables brut est surpuissant mais inutilement complexe quand on veut juste bloquer quelques ports. nftables est l'avenir, mais la plupart des tutos et scripts tiers (y compris Docker lui-même) parlent encore iptables.

Si tu débutes avec Docker, commence par mon guide [Docker pour débutants](/docker-debutant-services-auto-heberger/) avant d'attaquer le pare-feu. Comprendre les réseaux bridge et host simplifie tout ce qui suit.

## Comment Docker manipule iptables

Quand tu lances un conteneur avec un port mappé (`-p 8080:80`), Docker fait trois choses dans iptables :

1. **Règle NAT** : dans la chaîne `PREROUTING` de la table `nat`, il redirige le trafic entrant sur le port 8080 vers l'IP interne du conteneur.
2. **Règle FORWARD** : dans la chaîne `DOCKER` de la table `filter`, il accepte le trafic forwardé vers l'interface bridge du conteneur.
3. **Masquerade** : dans la chaîne `POSTROUTING`, il masque l'IP source du conteneur avec l'IP de l'hôte.

Ces règles sont créées dynamiquement au démarrage du daemon Docker et mises à jour à chaque `docker run`. Elles sont insérées **avant** les règles UFW, ce qui fait que UFW ne les voit même pas. Le paquet entre, passe le NAT, est forwardé par Docker, et UFW n'est jamais consulté pour ce flux.

Tu peux le vérifier toi-même :

```bash
sudo iptables -t filter -L -v -n --line-numbers | grep DOCKER
```

Tu verras une chaîne `DOCKER` avec des règles `ACCEPT` pour chaque réseau bridge actif. Et une chaîne `DOCKER-ISOLATION` qui empêche les conteneurs de communiquer entre réseaux bridge sans autorisation explicite.

## La solution : désactiver l'iptables managé par Docker

Le réglage le plus propre et le plus stable est de dire à Docker de ne plus toucher à iptables. C'est une option du daemon Docker, donc tu la configures une fois et elle s'applique à tous les conteneurs.

### Étape 1 : Créer ou éditer le daemon.json

```bash
sudo nano /etc/docker/daemon.json
```

Ajoute (ou complète) :

```json
{
  "iptables": false
}
```

Si le fichier contient déjà d'autres options (comme `"data-root"` ou `"log-driver"`), fusionne proprement :

```json
{
  "data-root": "/var/lib/docker",
  "log-driver": "json-file",
  "iptables": false
}
```

### Étape 2 : Redémarrer Docker

```bash
sudo systemctl restart docker
```

Attention : le redémarrage coupe temporairement tous les conteneurs. Fais ça en maintenance, pas en plein milieu d'un streaming Jellyfin.

### Étape 3 : Configurer UFW normalement

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

Résultat : Docker ne crée plus de règles iptables. Le trafic entrant est traité par UFW comme n'importe quel autre trafic. Si un conteneur écoute sur le port 8080 mais que tu n'as pas fait `ufw allow 8080`, le port est fermé.

### Le problème du NAT interne

Quand tu désactives `iptables` dans Docker, les conteneurs perdent leur accès NAT à internet. Un `apt update` depuis un conteneur échoue parce que les paquets ne peuvent plus être masqués par l'hôte.

Solution : ajouter manuellement la règle de masquerade pour le réseau bridge de Docker.

```bash
sudo iptables -t nat -A POSTROUTING -s 172.17.0.0/16 ! -o docker0 -j MASQUERADE
```

Et pour la rendre persistante au reboot, installe `iptables-persistent` :

```bash
sudo apt install iptables-persistent
sudo netfilter-persistent save
```

Cette approche est fiable mais demande de comprendre les plages IP de Docker. Le réseau bridge par défaut est `172.17.0.0/16`. Si tu crées des réseaux personnalisés (`docker network create`), adapte la règle.

## Alternative : le script ufw-docker

Si tu ne veux pas désactiver iptables dans Docker (parce que tu utilises des réseaux complexes ou Swarm), il existe une solution intermédiaire : le script `ufw-docker` de Chaifeng. Il modifie les chaînes iptables pour placer UFW **devant** les règles Docker.

Installation :

```bash
sudo wget -O /usr/local/bin/ufw-docker \
  https://github.com/chaifeng/ufw-docker/raw/master/ufw-docker
sudo chmod +x /usr/local/bin/ufw-docker
```

Puis modifie UFW pour qu'il inspecte les paquets avant le NAT Docker :

```bash
sudo ufw-docker install
```

Cette commande modifie `/etc/ufw/after.rules` pour ajouter des règles qui bloquent les ports Docker par défaut, sauf ceux que tu exposes explicitement.

Pour autoriser un port de conteneur spécifique :

```bash
sudo ufw-docker allow traefik 80
sudo ufw-docker allow jellyfin 8096
```

Le script fonctionne bien, mais il ajoute une couche de complexité. C'est un bon compromis si tu ne veux pas toucher au `daemon.json`. Personnellement, je préfère la solution `iptables: false` sur un serveur perso. Plus simple, moins de dépendances, et tu gardes le contrôle total.

## Docker Compose avec UFW

Voici un `docker-compose.yml` type qui fonctionne avec UFW et `iptables: false`. Il montre un reverse proxy (Traefik), un service web et une base de données.

```yaml
services:
  traefik:
    image: traefik:v3.0
    container_name: traefik
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - ./traefik:/etc/traefik
    networks:
      - proxy
    command:
      - --api.dashboard=false
      - --providers.docker=true
      - --providers.docker.exposedbydefault=false
      - --entrypoints.web.address=:80
      - --entrypoints.websecure.address=:443

  whoami:
    image: traefik/whoami
    container_name: whoami
    restart: unless-stopped
    networks:
      - proxy
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.whoami.rule=Host(`whoami.tondomaine.fr`)"
      - "traefik.http.routers.whoami.entrypoints=web"

  db:
    image: postgres:16-alpine
    container_name: db
    restart: unless-stopped
    environment:
      POSTGRES_USER: app
      POSTGRES_PASSWORD: changeme
      POSTGRES_DB: appdb
    volumes:
      - db_data:/var/lib/postgresql/data
    networks:
      - backend

volumes:
  db_data:

networks:
  proxy:
    driver: bridge
  backend:
    driver: bridge
    internal: true
```

Points clés :

- **Ports exposés** : seuls `80` et `443` sont mappés sur l'hôte. UFW contrôle ces ports comme des ports natifs.
- **Réseau `backend: internal: true`** : la base de données n'a aucun accès externe, même pas de NAT. Elle communique uniquement avec les services du même réseau `backend`. C'est la meilleure pratique de sécurité Docker : isole les services qui n'ont pas besoin d'internet.
- **Pas de port mappé pour PostgreSQL** : le port 5432 n'est pas exposé sur l'hôte, donc UFW n'a même pas à s'en occuper. C'est invisible depuis l'extérieur.

Avec `iptables: false` dans le daemon, Traefik reçoit bien le trafic sur 80/443 parce que UFW les autorise. `whoami` est accessible via Traefik mais pas directement. La base est complètement hermétique.

## Tableau récapitulatif : ports avec et sans UFW Docker

| Scénario | `iptables: true` (par défaut) | `iptables: false` + UFW | Script `ufw-docker` |
|----------|------------------------------|------------------------|---------------------|
| Port 8080 mappé, UFW fermé | **Ouvert** (Docker bypass UFW) | **Fermé** (UFW contrôle) | **Fermé** (sauf si `ufw-docker allow`) |
| Port 8080 mappé, UFW ouvert | Ouvert | Ouvert | Ouvert |
| Communication inter-conteneurs | Fonctionne (NAT Docker) | Nécessite règle POSTROUTING | Fonctionne |
| Accès internet conteneurs | Fonctionne | Nécessite MASQUERADE manuel | Fonctionne |
| Complexité | Zéro (mais trompeur) | Faible (une règle iptables) | Modérée (script tiers) |
| Reboot persistant | Oui | Nécessite `iptables-persistent` | Oui |

Mon choix pour un serveur auto-hébergé : **`iptables: false` + règle POSTROUTING manuelle + UFW classique**. C'est le plus propre, le plus prévisible et ça ne dépend pas d'un script externe.

## Vérifier que tes règles fonctionnent

Ne crois pas `ufw status`. Teste depuis l'extérieur.

Depuis une machine externe :

```bash
nmap -p 22,80,443,8080,5432 ton-ip-publique
```

Tu dois voir `open` uniquement sur 22, 80, 443 (et éventuellement d'autres ports que tu as explicitement autorisés). Tout le reste doit être `filtered` ou `closed`.

Depuis le serveur, vérifie les chaînes iptables :

```bash
sudo iptables -L -v -n
```

Si `iptables: false` est actif, tu ne dois pas voir de chaîne `DOCKER` dans la table `filter`. Seules les chaînes UFW (`ufw-user-input`, `ufw-before-input`, etc.) doivent apparaître.

Pour tester la connectivité internet des conteneurs :

```bash
docker run --rm alpine ping -c 3 1.1.1.1
```

Si ça échoue, ta règle POSTROUTING manque ou est mal configurée.

## Bonnes pratiques de sécurité réseau avec Docker

**Un conteneur = un réseau quand c'est possible.** Ne mets pas tout dans le réseau bridge par défaut. Crée des réseaux dédiés (`frontend`, `backend`, `database`) et n'expose que ce qui doit l'être.

**Évite `network_mode: host`.** Ça contourne tout le système de ports mappés et expose directement les ports du conteneur sur l'hôte. Seule exception : Fail2Ban en `host` pour manipuler iptables. Pour le reste, c'est une mauvaise idée de sécurité.

**Utilise `internal: true` pour les bases de données.** Comme dans le `docker-compose.yml` ci-dessus. Un réseau interne n'a pas de passerelle par défaut. Le conteneur ne peut pas initier de connexion sortante, ce qui limite l'impact en cas de compromission.

**Limite les `ports` dans Compose.** Chaque ligne `- "XXXX:YYYY"` est un trou dans ton pare-feu. Si un service est accessible via un reverse proxy (Traefik, Nginx Proxy Manager), il n'a pas besoin d'être mappé sur l'hôte. Traefik communique avec lui via le réseau Docker interne.

Et pour surveiller que tes règles firewall ne bloquent pas tes services par inadvertance, [Beszel](/beszel-monitoring-docker/) est pratique. Il te montre en temps réel si un conteneur devient injoignable.

## Troubleshooting courant

**"J'ai bloqué un port avec UFW mais il reste ouvert"**
→ Docker injecte encore des règles iptables. Vérifie `sudo iptables -L | grep DOCKER`. Si tu vois des règles Docker, `iptables: false` n'est pas actif. Redémarre le daemon Docker.

**"Mes conteneurs n'ont plus internet après `iptables: false`"**
→ La règle POSTROUTING MASQUERADE manque. Ajoute-la et sauvegarde avec `netfilter-persistent`.

**"UFW bloque les connexions entre conteneurs sur le même réseau"**
→ UFW ne bloque pas le trafic interne bridge par défaut. Si ça arrive, c'est que tu as une règle UFW très restrictive ou un `DEFAULT_FORWARD_POLICY=DROP` dans `/etc/default/ufw`. Laisse `DEFAULT_FORWARD_POLICY=ACCEPT` pour le trafic bridge interne.

**"Docker Compose échoue au démarrage avec `iptables: false`"**
→ Certains plugins Docker (réseaux overlay, Swarm) nécessitent iptables. Sur un serveur solo avec Compose, ce n'est pas le cas. Si tu es en Swarm, garde `iptables: true` et utilise plutôt le script `ufw-docker`.

## Conclusion

UFW et Docker peuvent coexister, mais pas sans réglage. La configuration par défaut de Docker rend UFW inefficace pour les ports mappés. En désactivant la gestion iptables de Docker et en ajoutant une règle POSTROUTING manuelle, tu récupères le contrôle de ton pare-feu sans sacrifier la connectivité des conteneurs.

C'est une ligne de config dans `/etc/docker/daemon.json`, une règle iptables et UFW redevient fiable. Pour un serveur auto-hébergé, c'est le meilleur ratio simplicité/sécurité. UFW n'est qu'une couche : voir mon guide [sécuriser son serveur Linux](/securite-de-votre-serveur-linux/) pour le durcissement complet.
