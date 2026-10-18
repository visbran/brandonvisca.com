---
title: "Postfix Docker : serveur mail auto-hébergé complet"
description: "Déploie un serveur mail complet avec Postfix Docker : SMTP, Dovecot, DKIM et anti-spam, guide pas à pas pour ton homelab en 2026."
pubDatetime: "2026-10-18T11:06:14+02:00"
modDatetime: "2026-10-18T08:00:00.000Z"
author: Brandon Visca
tags:
  - auto-hebergement
  - docker
  - messagerie
  - dns
  - intermediaire
featured: false
draft: false
focusKeyword: postfix docker
faqs:
  - question: "Faut-il un serveur dédié pour faire tourner Postfix Docker ou un petit VPS suffit ?"
    answer: "Un petit VPS avec 1 à 2 vCPU et 2 Go de RAM suffit largement pour un usage personnel ou familial. Le vrai facteur limitant n'est pas la puissance, c'est la réputation de l'IP et l'accès au port 25 chez ton hébergeur."
  - question: "Comment éviter que mes mails envoyés depuis mon serveur Postfix Docker finissent en spam ?"
    answer: "Configure SPF, DKIM et DMARC sur ton domaine, demande un reverse DNS propre à ton hébergeur, et chauffe ta réputation en envoyant peu au début. Sans ces trois enregistrements DNS, même un Postfix parfaitement configuré finit en spam."
  - question: "Que se passe-t-il si mon serveur mail tombe pendant qu'un mail important arrive ?"
    answer: "Rien de grave dans l'immense majorité des cas. Le serveur expéditeur réessaie automatiquement pendant plusieurs jours, Postfix fait pareil pour les mails sortants. Le vrai risque, c'est une panne qui dure plusieurs jours sans backup."
---
> 💡 **TL;DR**
> - Monte ton propre serveur mail avec **Postfix Docker**, via l'image `docker-mailserver`, qui embarque Postfix, Dovecot, anti-spam et anti-virus
> - Déploiement en un `docker-compose.yml`, mais la vraie difficulté c'est la configuration DNS (SPF, DKIM, DMARC, PTR)
> - Compte entre une demi-journée et un week-end pour un serveur mail propre, livré, et pas dans les spams

## Pourquoi monter ton propre serveur mail avec Postfix Docker

Auto-héberger son mail, c'est un peu le boss final de l'auto-hébergement. Tu as déjà ton Nextcloud, ton Jellyfin, ton Nginx Proxy Manager qui tournent bien. Et puis vient cette question : pourquoi tu paies encore Gmail ou Outlook pour recevoir du texte ?

La réponse courte : parce que gérer un serveur mail, c'est gérer ta propre réputation sur Internet. Et c'est là que Postfix Docker change la donne. Postfix, c'est le MTA (Mail Transfer Agent) écrit par Wietse Venema, publié en 1998, et qui reste aujourd'hui l'un des serveurs mail les plus utilisés au monde, loin devant Sendmail dont il a pris la place sur la plupart des distributions Linux, Ubuntu compris. Son code source est disponible sur [postfix.org](https://www.postfix.org), toujours activement maintenu.

Le souci avec Postfix pris seul, c'est qu'il ne fait qu'une partie du boulot : envoyer et recevoir des mails en SMTP. Pour avoir une vraie boîte mail, il te faut aussi un serveur IMAP (Dovecot), un anti-spam, un anti-virus, et la gestion des certificats TLS. Compiler tout ça à la main sur un serveur nu, c'était le calvaire des admins sys des années 2000.

C'est exactement le problème que règle l'approche Postfix Docker avec le projet communautaire `docker-mailserver`. Tu récupères une image qui embarque Postfix, Dovecot, et toute la chaîne anti-spam, prête à tourner en conteneur. Le dépôt est disponible sur [github.com/docker-mailserver/docker-mailserver](https://github.com/docker-mailserver/docker-mailserver), sous licence MIT.

Spoiler : ça va marcher. Mais la partie Docker n'est pas la plus dure. La vraie difficulté d'un serveur Postfix Docker, c'est la configuration DNS autour. On y revient en détail plus bas.

## Table des matières

## Les prérequis avant de te lancer

Avant de taper la première commande, vérifie ces points. Ignorer un seul d'entre eux et ton serveur mail Postfix Docker finira dans les spams de tout le monde, ou pire, injoignable.

- **Un VPS avec une IP fixe**, idéalement chez un hébergeur qui autorise le port 25 sortant. Beaucoup de providers cloud grand public (AWS, Google Cloud, OVH sur certaines offres) bloquent ce port par défaut pour lutter contre le spam. Chez Hetzner ou Scaleway, ça passe généralement sans demande particulière.
- **Un nom de domaine** que tu contrôles, avec accès à la zone DNS. Pas de sous-domaine gratuit type `.freenom` : la réputation de ces domaines est en général déjà pourrie.
- **Un reverse DNS (PTR)** pointant de ton IP vers ton nom de domaine mail (ex: `mail.tondomaine.fr`). Demande-le à ton hébergeur, c'est souvent une option dans le panel.
- **Un peu de patience.** Monter la stack technique prend une heure. Chauffer ta réputation d'envoi et vérifier que tes mails arrivent bien chez Gmail, Outlook et les autres prend plusieurs jours.

Si tu débutes complètement avec Docker, je te renvoie vers les bases avant d'attaquer ce guide : les mêmes principes de volumes et de réseau que tu utilises pour gérer tes stacks Compose avec [Dockge](/dockge-docker-gestionnaire-stacks-compose/) s'appliquent ici.

## Architecture du stack : Postfix, Dovecot et compagnie

Un serveur mail Postfix Docker complet, ce n'est jamais un seul conteneur. Voici ce qui tourne dans la stack `docker-mailserver` :

- **Postfix** : réception et envoi en SMTP, avec authentification pour les clients mail.
- **Dovecot** : serveur IMAP et POP3, c'est lui qui stocke et sert les mails à ton client (Thunderbird, Apple Mail, ton téléphone).
- **Rspamd ou Amavis + SpamAssassin** : filtrage anti-spam sur les mails entrants.
- **ClamAV** : anti-virus avec mise à jour automatique des signatures.
- **OpenDKIM et OpenDMARC** : signature cryptographique des mails sortants et vérification de l'authenticité des mails entrants.
- **Fail2ban** : bannit les IP qui tentent de bruteforcer tes comptes.

Tout ça dans une seule image conteneurisée, configurée via un fichier `mailserver.env` et un script `setup.sh` fourni par le projet. Pas de base SQL externe à gérer : la configuration reste dans des fichiers plats, ce qui simplifie grandement les sauvegardes.

> 💡 Si tu veux garder un œil sur ce qui se passe dans tes conteneurs pendant la mise au point, [Dozzle](/dozzle-docker-visionneuse-logs-web/) te donne les logs en temps réel sans taper une seule commande `docker logs`. Très utile pour comprendre pourquoi un mail de test n'arrive pas.

## Déployer le serveur avec Docker Compose

On y va. Crée un dossier dédié :

```bash
mkdir -p ~/docker/mailserver && cd ~/docker/mailserver
```

Récupère les fichiers de référence du projet `docker-mailserver` :

```bash
curl -fsSL -o compose.yaml https://raw.githubusercontent.com/docker-mailserver/docker-mailserver/master/compose.yaml
curl -fsSL -o mailserver.env https://raw.githubusercontent.com/docker-mailserver/docker-mailserver/master/mailserver.env
curl -fsSL -o setup.sh https://raw.githubusercontent.com/docker-mailserver/docker-mailserver/master/setup.sh
chmod +x setup.sh
```

Ouvre `compose.yaml` et adapte au minimum le nom d'hôte :

```yaml
services:
  mailserver:
    image: ghcr.io/docker-mailserver/docker-mailserver:latest
    container_name: mailserver
    hostname: mail
    domainname: tondomaine.fr
    env_file: mailserver.env
    ports:
      - "25:25"
      - "143:143"
      - "465:465"
      - "587:587"
      - "993:993"
    volumes:
      - ./docker-data/dms/mail-data/:/var/mail/
      - ./docker-data/dms/mail-state/:/var/mail-state/
      - ./docker-data/dms/mail-logs/:/var/log/mail/
      - ./docker-data/dms/config/:/tmp/docker-mailserver/
      - /etc/localtime:/etc/localtime:ro
    restart: unless-stopped
    stop_grace_period: 1m
```

Les cinq ports exposés correspondent chacun à un usage précis : 25 pour le relais SMTP entre serveurs mail, 587 pour l'envoi authentifié depuis ton client (STARTTLS), 465 pour l'envoi en TLS direct, 143 et 993 pour la réception en IMAP (clair et TLS).

Lance la stack avec le script fourni, qui pilote Docker Compose pour toi :

```bash
./setup.sh email add toi@tondomaine.fr
```

Cette commande démarre le conteneur si besoin et te crée ta première boîte mail avec un mot de passe à définir. Pour ajouter des alias :

```bash
./setup.sh alias add contact@tondomaine.fr toi@tondomaine.fr
```

Un bon réflexe : utilise un gestionnaire de stacks visuel pour superviser le conteneur au quotidien plutôt que de retenir chaque commande `docker compose`. C'est exactement ce que propose [Dockge](/dockge-docker-gestionnaire-stacks-compose/), avec un éditeur du fichier Compose directement dans le navigateur.

## Configurer les DNS : SPF, DKIM, DMARC et PTR

C'est ici que neuf projets de serveur mail Postfix Docker sur dix finissent à la poubelle. Le conteneur peut être parfaitement configuré, si les DNS sont absents ou faux, tes mails n'arriveront jamais dans la boîte de réception de tes correspondants.

**Enregistrement MX**, pour dire aux autres serveurs mail où livrer :

```
tondomaine.fr.    MX    10    mail.tondomaine.fr.
```

**SPF**, pour autoriser explicitement ton IP à envoyer des mails pour ton domaine :

```
tondomaine.fr.    TXT    "v=spf1 mx -all"
```

**DKIM**, généré directement par `docker-mailserver` :

```bash
./setup.sh config dkim
```

La commande sort une clé publique à coller dans un enregistrement TXT du type `mail._domainkey.tondomaine.fr`. Sans DKIM, une grande partie des serveurs mail (Gmail en tête) classent directement tes mails en spam ou les rejettent.

**DMARC**, pour dire quoi faire des mails qui échouent aux deux contrôles précédents :

```
_dmarc.tondomaine.fr.    TXT    "v=DMARC1; p=quarantine; rua=mailto:toi@tondomaine.fr"
```

Commence en `p=quarantine` plutôt que `p=reject`, le temps de vérifier que tout fonctionne. Et n'oublie pas le **reverse DNS (PTR)** côté hébergeur, qui doit faire correspondre ton IP à `mail.tondomaine.fr`. C'est souvent le point que les gens oublient, et c'est souvent lui qui bloque tout.

Une fois les quatre enregistrements en place, teste ta configuration avec un outil de vérification SPF/DKIM/DMARC en ligne, ou directement en envoyant un mail à une adresse Gmail et en regardant les en-têtes du message reçu.

## Gérer tes comptes mail au quotidien

Une fois le serveur Postfix Docker en place, la gestion au quotidien passe par le script `setup.sh`. Voici les commandes que tu utiliseras le plus souvent :

```bash
# Lister les comptes
./setup.sh email list

# Changer un mot de passe
./setup.sh email update toi@tondomaine.fr

# Supprimer un compte
./setup.sh email del ancien@tondomaine.fr

# Lister les alias
./setup.sh alias list
```

Côté client, configure Thunderbird, Apple Mail ou ton client mobile avec :
- **Serveur entrant (IMAP)** : `mail.tondomaine.fr`, port 993, SSL/TLS
- **Serveur sortant (SMTP)** : `mail.tondomaine.fr`, port 587, STARTTLS

Si tu gères aussi une liste de diffusion ou une newsletter en parallèle, ton serveur Postfix Docker peut servir de relais SMTP pour [Listmonk](/listmonk-docker-newsletter-auto-hebergee/) au lieu de passer par un service externe payant. Même principe de contrôle total sur tes données, cette fois appliqué à l'envoi en masse.

## Sécuriser, surveiller et sauvegarder

Un serveur mail mal protégé, c'est une porte ouverte vers du spam envoyé en ton nom ou une boîte mail compromise. Quelques réflexes non négociables.

⚠️ **Mots de passe forts et authentification robuste.** Chaque compte mail doit avoir un mot de passe généré, pas un mot de passe réutilisé ailleurs. Fail2ban, inclus dans la stack, bannit automatiquement les IP qui tentent de deviner un mot de passe en boucle.

✅ **Mises à jour régulières de l'image.** Le conteneur embarque ClamAV et les règles anti-spam, qui doivent rester à jour :

```bash
cd ~/docker/mailserver
docker compose pull
docker compose up -d
```

✅ **Sauvegardes du volume de données.** Tes mails, tes comptes et tes clés DKIM vivent dans `docker-data/dms/`. Une sauvegarde régulière de ce dossier, chiffrée et stockée ailleurs que sur le serveur, est non négociable. Perdre une boîte mail professionnelle sans backup, ça peut littéralement couler une activité.

Si ton serveur mail notifie d'autres services de ton infra, par exemple des alertes de pipeline CI/CD depuis [GitLab CE](/gitlab-ce-docker-forge-cicd-complete/), assure-toi que ces notifications passent bien par ton relais SMTP maison et qu'elles ne finissent pas, elles non plus, dans les spams côté destinataire.

## Conclusion

Monter un serveur Postfix Docker, ce n'est plus le cauchemar de compilation que c'était il y a quinze ans. La partie conteneur se règle en une demi-journée avec `docker-mailserver`, Postfix, Dovecot et l'anti-spam livrés clé en main.

La vraie difficulté, et c'est elle qui décide si ton projet est un succès ou un échec, c'est la configuration DNS : SPF, DKIM, DMARC et reverse DNS. Sans ces quatre éléments bien réglés, même le Postfix le mieux configuré du monde finit systématiquement en spam.

Mon conseil : ne fais pas ça sur ta boîte mail professionnelle principale du premier coup. Teste sur un domaine secondaire, chauffe ta réputation, vérifie que Gmail et Outlook acceptent tes mails sans broncher. Une fois que c'est stable, migre en confiance. Ton indépendance vis-à-vis de Google et Microsoft, pour le prix d'un petit VPS, ça vaut largement l'effort du week-end.
