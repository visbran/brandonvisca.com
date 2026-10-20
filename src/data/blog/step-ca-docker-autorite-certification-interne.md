---
title: "Step CA Docker : ta propre autorité de certification interne"
description: "Déploie step ca docker pour une autorité de certification interne : certificats TLS internes, ACME automatique et PKI self-hosted pour ton homelab."
pubDatetime: "2026-10-13T11:02:11+02:00"
modDatetime: "2026-10-12T08:00:00.000Z"
author: Brandon Visca
tags:
  - securite
  - hardening
  - reverse-proxy
  - ssh
  - guide
  - avance
featured: false
draft: false
focusKeyword: step ca docker
faqs:
  - question: "Combien ça consomme en RAM et CPU sur un homelab ?"
    answer: "Quasiment rien : step-ca est un petit binaire Go, il tourne avec 50 à 100 Mo de RAM et une fraction de cœur CPU, même avec plusieurs centaines de certificats émis chaque mois."
  - question: "Que se passe-t-il si je perds le volume ou le mot de passe de la CA racine ?"
    answer: "Tu perds la clé racine et dois réémettre toute ta PKI depuis zéro : sauvegarde le volume step et le mot de passe comme un secret critique, jamais comme un conteneur jetable."
  - question: "step-ca peut-il aussi émettre des certificats SSH, pas seulement TLS ?"
    answer: "Oui, en activant DOCKER_STEPCA_INIT_SSH=true dès l'initialisation : tu obtiens une seconde autorité dédiée aux certificats SSH courte durée pour tes utilisateurs et tes hôtes."
---
> 💡 **TL;DR**
> - step ca docker fait tourner Smallstep step-ca en conteneur pour émettre tes propres certificats TLS internes, sans jamais dépendre d'une CA publique
> - Initialisation en une commande via les variables DOCKER_STEPCA_INIT_*, puis un provisioner ACME pour que Caddy, Traefik ou nginx renouvellent seuls leurs certs
> - Le volume step est un secret critique à sauvegarder : perdu, c'est toute ta PKI interne qui repart de zéro

## Step CA Docker : pourquoi monter ta propre autorité interne

Chez moi, chaque service tourne en HTTPS. Même *arrière*, pas juste la façade exposée sur internet. Grafana, Proxmox, l'API interne du NAS, tout ça parle en TLS. Le problème, c'est que Let's Encrypt refuse obstinément de signer un certificat pour `grafana.lan` ou pour une IP privée. Logique : une CA publique ne peut pas vérifier que tu possèdes vraiment ce nom de domaine interne.

La solution, c'est de devenir ta propre autorité de certification. Et step ca docker, c'est exactement ça : le logiciel step-ca de Smallstep, packagé en conteneur, qui émet des certificats signés par une CA que tu contrôles de bout en bout. Tes navigateurs et tes services font confiance à ta CA racine une seule fois, et plus jamais d'avertissement rouge en ouvrant un dashboard interne.

On va pas se mentir, monter une PKI fait peur sur le papier. OpenSSL en ligne de commande, c'est l'enfer, trois pages de flags illisibles pour générer une simple paire de clés. step ca docker change la donne : une initialisation en une commande, un renouvellement automatique via ACME, et une CA intermédiaire qui protège la racine. Si tu bricoles déjà un homelab avec plusieurs services derrière un reverse proxy, c'est le genre de brique qui change vraiment le quotidien.

## Table des matières

## Step-ca, c'est quoi exactement

Smallstep Labs édite deux outils complémentaires : `step`, un CLI pour manipuler des certificats, et `step-ca`, le serveur qui fait tourner l'autorité elle-même. Le projet est open source et documenté sur smallstep.com, avec en face une offre commerciale (CA hébergée, support entreprise) pour qui veut déléguer la gestion.

Techniquement, step-ca expose une API HTTPS qui accepte des demandes de signature de certificats. Trois familles de clients peuvent lui parler :

- Le CLI `step`, pour un usage manuel ou scripté
- N'importe quel client ACME standard (Caddy, Traefik, certbot, acme.sh) pour du renouvellement automatique
- Des provisioners OIDC, pour authentifier des humains via ton SSO existant plutôt qu'avec un mot de passe partagé

La structure PKI repose sur deux niveaux : une CA racine, que tu génères une fois et que tu ranges au coffre, et une CA intermédiaire qui signe réellement les certificats au quotidien. Si l'intermédiaire est compromise un jour, tu la révoques et tu en génères une nouvelle sans toucher à la racine. C'est la pratique standard de toute PKI sérieuse, et step ca docker l'applique par défaut sans que tu aies à y penser.

## Installer step ca docker avec Docker Compose et initialiser la CA

L'image officielle s'appelle `smallstep/step-ca`. Un `docker-compose.yml` minimal ressemble à ça :

```yaml
services:
  step-ca:
    image: smallstep/step-ca:latest
    container_name: step-ca
    restart: unless-stopped
    ports:
      - "9000:9000"
    volumes:
      - step-data:/home/step
    environment:
      DOCKER_STEPCA_INIT_NAME: "Homelab CA"
      DOCKER_STEPCA_INIT_DNS_NAMES: "ca.lan,localhost"
      DOCKER_STEPCA_INIT_PROVISIONER_NAME: "admin"
      DOCKER_STEPCA_INIT_PASSWORD_FILE: "/home/step/secrets/password"

volumes:
  step-data:
```

Les variables `DOCKER_STEPCA_INIT_*` ne sont lues qu'au tout premier démarrage : elles initialisent la CA racine, l'intermédiaire, et un provisioner JWK nommé `admin`. Après ça, toute la configuration vit dans le volume `step-data`, monté sur `/home/step`. Pas de mot de passe en clair dans l'environnement en production : passe par un fichier monté et `DOCKER_STEPCA_INIT_PASSWORD_FILE`, le mot de passe en variable d'environnement brute traîne dans `docker inspect` et dans tes logs.

Premier lancement :

```bash
docker compose up -d
docker compose logs -f step-ca
```

Tu dois voir la CA annoncer qu'elle écoute sur le port 9000. Pour vérifier que tout a bien été généré, récupère le fingerprint du certificat racine :

```bash
docker compose exec step-ca step certificate fingerprint certs/root_ca.crt
```

Garde cette empreinte précieusement, c'est elle qui permet à un client de vérifier qu'il parle bien à ta CA et pas à un attaquant qui aurait usurpé l'adresse. Si tu dois la transmettre à un collègue plutôt que de la coller en clair dans un chat, un outil comme celui comparé dans [Yopass vs PrivateBin vs Password Pusher](/yopass-vs-privatebin-vs-password-pusher/) évite qu'elle traîne dans un historique de messages pour toujours.

Côté client, pour faire confiance à la CA et récupérer sa configuration en une commande :

```bash
step ca bootstrap --ca-url https://ca.lan:9000 --fingerprint <empreinte-récupérée>
```

Cette commande range le certificat racine et l'URL de la CA dans `~/.step/`. À partir de là, toute commande `step` ultérieure sur cette machine sait parler à ton autorité interne sans configuration supplémentaire.

## Activer ACME pour le renouvellement automatique des certificats

Générer un certificat à la main une fois, c'est sympa. Le renouveler à la main tous les trois mois sur quinze services, c'est l'enfer garanti, et le jour où tu oublies, ton dashboard affiche un cadenas barré devant tes utilisateurs. La vraie question, c'est comment automatiser ça, et la réponse s'appelle ACME, le même protocole que Let's Encrypt utilise pour l'internet public.

Ajoute un provisioner ACME à ta CA :

```bash
docker compose exec step-ca step ca provisioner add acme --type ACME
docker compose restart step-ca
```

Ta stack step ca docker expose alors un endpoint standard à cette adresse :

```
https://ca.lan:9000/acme/acme/directory
```

N'importe quel client ACME peut s'y abonner. Avec Caddy, ça tient en trois lignes de Caddyfile :

```
grafana.lan {
    tls {
        ca https://ca.lan:9000/acme/acme/directory
    }
    reverse_proxy localhost:3000
}
```

Avec Traefik, tu pointes le `caServer` de ton `certResolver` vers la même URL. Dès lors, ton reverse proxy demande, valide et renouvelle ses certificats seul, sans cron, sans script maison, sans que tu y repenses avant l'expiration suivante. Si tu protèges déjà tes services exposés avec [CrowdSec](/crowdsec-docker-securite-collaborative/), l'esprit est le même : réduire au maximum ce qui dépend d'une intervention manuelle, et donc d'un oubli humain.

Un détail qui coince souvent : la validation ACME de step-ca se fait en HTTP-01 ou TLS-ALPN-01 par défaut, donc elle suppose que la CA peut joindre le client sur le réseau pour vérifier la demande. En environnement purement interne sans challenge DNS configuré, assure-toi que le trafic entre le client et la CA n'est pas bloqué par un pare-feu trop zélé.

## Faire confiance au certificat racine sur tes clients et ton reverse proxy

Un certificat signé par ta CA ne vaut rien si personne ne fait confiance à cette CA. Trois cas de figure reviennent tout le temps :

**Navigateur desktop.** Exporte `root_ca.crt` depuis le volume et importe-le dans le magasin de certificats du système (trousseau sur macOS, certmgr sur Windows, `update-ca-certificates` sur Debian/Ubuntu après l'avoir copié dans `/usr/local/share/ca-certificates/`). Une fois fait, plus aucun avertissement sur aucun service qui présente un certificat signé par cette même CA.

**Conteneurs et scripts qui appellent tes services en HTTPS.** Monte le certificat racine dans l'image et pointe la variable d'environnement adaptée (`SSL_CERT_FILE` en Python, `NODE_EXTRA_CA_CERTS` en Node, `CURL_CA_BUNDLE` pour curl). Sans ça, chaque appel interne échoue avec une erreur de certificat non reconnu, même si le certificat du serveur est parfaitement valide.

**Mobile et IoT.** C'est la vraie limite d'une PKI maison : certains firmwares et certaines apps mobiles refusent d'installer une CA custom, ou l'acceptent seulement comme certificat "non fiable" avec des frictions. Pour ces appareils, prévois de garder un fallback en Let's Encrypt classique sur les endroits qui doivent rester accessibles sans manipulation côté client.

Si ton homelab tourne déjà sous [K3s](/k3s-docker-kubernetes-leger-homelab/), l'intégration suit la même logique : un cert-manager configuré avec un `ClusterIssuer` ACME pointé sur ta CA interne, et chaque Ingress récupère son certificat automatiquement, exactement comme un reverse proxy classique.

## Dépannage et limites à connaître

**"x509: certificate signed by unknown authority"** : le client n'a pas importé ton certificat racine, ou il regarde dans le mauvais magasin de certificats (système vs magasin applicatif, Firefox et Chrome n'utilisent pas toujours la même source selon l'OS).

**La CA ne redémarre pas après un changement de provisioner** : vérifie les logs avec `docker compose logs step-ca`. Neuf fois sur dix, c'est une erreur de syntaxe dans la configuration `/home/step/config/ca.json`, à inspecter directement dans le volume.

**Le fingerprint ne correspond pas à ce qu'attend `step ca bootstrap`** : tu as probablement réinitialisé le volume entre-temps, ce qui régénère une CA racine totalement différente. C'est voulu : step-ca refuse qu'un client fasse confiance silencieusement à une nouvelle racine sans revalidation explicite.

**Le volume de la CA racine, c'est le secret le plus critique de ton infra.** Sans backup, une corruption de disque ou une mauvaise commande `docker volume rm` et c'est toute ta PKI interne à reconstruire, tous les services à re-certifier, tous les clients à re-bootstrapper. Sauvegarde-le avec un outil chiffré et dédupliqué comme [BorgBackup](/borgbackup-docker-sauvegarde/), pas avec une copie occasionnelle qui traîne sur une clé USB. Et si tu dois stocker le mot de passe d'initialisation ailleurs que dans le fichier monté, un gestionnaire comme [Vaultwarden](/vaultwarden-docker-gestionnaire-mots-de-passe/) fait bien mieux qu'un fichier texte planqué sur le NAS.

Autre limite documentée par l'éditeur : une seule CA intermédiaire émettrice à la fois, pas de support SCEP dynamique, et des options de révocation active (CRL, OCSP) plus limitées que sur une PKI d'entreprise classique. Pour un homelab ou une petite infra pro, ça ne pèse pas lourd face au gain. Pour une PKI de production à grande échelle avec des contraintes de conformité strictes, regarde aussi l'offre hébergée de Smallstep avant de tout faire reposer sur un conteneur self-hosted.

💡 À lire aussi : [Asterisk Docker : serveur VoIP open-source complet](/asterisk-docker-serveur-voip-open-source/), dans la même veine que cet article.

## Conclusion

step ca docker, c'est la brique qui manque à beaucoup de homelabs : plus de certificats auto-signés qui font flipper le navigateur, plus de "accepter le risque et continuer" cliqué sans réfléchir dix fois par jour. Une CA interne propre, un provisioner ACME pour l'automatisation, et un reverse proxy qui gère ses certificats seul.

Spoiler : ça va marcher du premier coup si tu respectes une seule règle, sauvegarder le volume `step` comme n'importe quel autre secret critique de ton infra. Le reste, c'est de la configuration classique, et tu en as déjà vu bien pire en montant ton homelab.
