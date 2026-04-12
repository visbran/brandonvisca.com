---
title: "Sécurité de votre serveur linux : Comment durcir un serveur sous linux ?"
description: "Guide complet pour renforcer la sécurité de votre serveur Linux : SSH, pare-feu ufw, fail2ban, mises à jour auto et surveillance des logs. Testé en prod."
pubDatetime: "2024-06-10T19:29:00+02:00"
modDatetime: "2026-04-12T00:00:00+01:00"
author: Brandon Visca
tags:
  - linux
  - securite
  - hardening
  - sysadmin
  - guide
  - avance
featured: false
draft: false
focusKeyword: sécurité de votre serveur linux
faqs:
  - question: "Qu'est-ce que le durcissement d'un serveur sous Linux ?"
    answer: "C'est l'ensemble des mesures de sécurité appliquées à un serveur pour minimiser les vulnérabilités : SSH durci, firewall, fail2ban, sysctl renforcés."
  - question: "Comment désactiver la connexion SSH en tant que root et modifier le port ?"
    answer: "Édite /etc/ssh/sshd_config : définis PermitRootLogin no et change le port 22 par un numéro personnalisé."
  - question: "Comment limiter l'accès à su uniquement au groupe admin ?"
    answer: "Crée un groupe admin et utilise dpkg-statoverride pour restreindre l'accès à /bin/su uniquement à ce groupe."
  - question: "Qu'est-ce que Fail2Ban ?"
    answer: "Fail2Ban analyse les logs et bannit automatiquement les IPs responsables d'attaques SSH et autres tentatives malveillantes."
---
Dans ce guide pratique, on va renforcer ensemble la sécurité de votre serveur Linux. De la configuration SSH au pare-feu en passant par les paramètres sysctl, on couvre toutes les mesures essentielles pour rendre ton serveur aussi résistant que possible.

![Illustration — Sécurité de votre serveur linux](image.gif)

Cette optimisation s'inscrit dans une démarche plus globale de gestion des ressources système — au même titre que la [configuration du swap Linux](https://brandonvisca.com/guide-swap-linux-configuration-optimisation/) qui permet d'éviter les dysfonctionnements en cas de saturation mémoire.

## Table des matières

## Sécurisation de la mémoire partagée

`/dev/shm` peut être utilisé dans une attaque contre un service en cours d'exécution, comme Apache ou Nginx. On va le monter avec des options restrictives.

Ouvre `/etc/fstab` :

```bash
sudo nano /etc/fstab
```

Ajoute ou modifie la ligne suivante :

```text
tmpfs     /dev/shm     tmpfs     defaults,noexec,nosuid,nodev     0     0
```

Recharge sans redémarrer :

```bash
sudo mount -o remount /dev/shm
```

## Durcissement de SSH – désactivation de la connexion en tant que root et changement de port

Le moyen le plus efficace de sécuriser SSH : désactiver la connexion root, désactiver l'authentification par mot de passe (clés uniquement), et changer le port par défaut.

> **Avant tout** : crée un utilisateur non-root avec accès sudo et configure ta clé SSH. Si tu perds l'accès SSH après modification, tu te retrouves bloqué.

Édite la configuration SSH :

```bash
sudo nano /etc/ssh/sshd_config
```

Modifie ou ajoute ces lignes :

```text
Port <TON_PORT>
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
AuthorizedKeysFile .ssh/authorized_keys
X11Forwarding no
AllowUsers <TON_UTILISATEUR>
```

> `Protocol 2` est désormais le seul protocole supporté depuis OpenSSH 7.0 (2015) — inutile de le spécifier.

Applique les changements :

```bash
sudo systemctl restart ssh
```

### Protéger su en limitant l'accès uniquement au groupe admin

```bash
sudo groupadd admin
sudo usermod -a -G admin <TON_UTILISATEUR>
sudo dpkg-statoverride --update --add root admin 4750 /bin/su
```

## Renforcer le réseau avec les paramètres sysctl

`/etc/sysctl.conf` contrôle les paramètres noyau. Ces réglages protègent contre l'usurpation d'IP, les attaques SYN flood et les redirections malveillantes.

Ouvre le fichier :

```bash
sudo nano /etc/sysctl.conf
```

Ajoute les lignes suivantes :

```ini
# Protection contre l'usurpation d'IP
net.ipv4.conf.all.rp_filter = 1
net.ipv4.conf.default.rp_filter = 1

# Ignorer les demandes de diffusion ICMP
net.ipv4.icmp_echo_ignore_broadcasts = 1

# Désactiver le routage des paquets source
net.ipv4.conf.all.accept_source_route = 0
net.ipv6.conf.all.accept_source_route = 0
net.ipv4.conf.default.accept_source_route = 0
net.ipv6.conf.default.accept_source_route = 0

# Ignorer les redirections envoyées
net.ipv4.conf.all.send_redirects = 0
net.ipv4.conf.default.send_redirects = 0

# Bloquer les attaques SYN
net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_max_syn_backlog = 2048
net.ipv4.tcp_synack_retries = 2
net.ipv4.tcp_syn_retries = 5

# Enregistrer les paquets « martiens »
net.ipv4.conf.all.log_martians = 1
net.ipv4.icmp_ignore_bogus_error_responses = 1

# Ignorer les redirections ICMP
net.ipv4.conf.all.accept_redirects = 0
net.ipv6.conf.all.accept_redirects = 0
net.ipv4.conf.default.accept_redirects = 0
net.ipv6.conf.default.accept_redirects = 0
```

Applique sans redémarrer :

```bash
sudo sysctl -p
```

> `net.ipv4.icmp_echo_ignore_all = 1` (bloquer tous les pings) est intentionnellement omis : ça casse les diagnostics réseau sans apporter de sécurité réelle sur un serveur bien configuré avec un pare-feu.

## Désactivez la récursion DNS ouverte et supprimez les informations de version – Serveur DNS BIND

Si tu fais tourner BIND9, désactive la récursion ouverte pour éviter d'être utilisé dans une attaque par amplification DNS.

```bash
sudo nano /etc/bind/named.conf.options
```

Dans la section `options { ... }` :

```text
recursion no;
version "Not Disclosed";
```

Redémarre BIND :

```bash
sudo systemctl restart bind9
```

## Prévenir l'usurpation d'IP

```bash
sudo nano /etc/host.conf
```

Ajoute :

```text
order bind,hosts
nospoof on
```

## Renforcez PHP pour la sécurité

> **Note :** le chemin varie selon la version PHP installée. Remplace `8.x` par ta version (`php -v`).

```bash
sudo nano /etc/php/8.x/apache2/php.ini
```

Modifie ou ajoute :

```ini
disable_functions = exec,system,shell_exec,passthru
expose_php = Off
display_errors = Off
html_errors = Off
```

> `register_globals`, `magic_quotes_gpc` et `track_errors` ont été supprimés respectivement en PHP 5.4, 5.4 et 8.0 — inutile de les définir sur une installation moderne.

Redémarre Apache :

```bash
sudo systemctl restart apache2
```

## Limitez la fuite d'informations Apache

```bash
sudo nano /etc/apache2/conf-available/security.conf
```

Modifie ou ajoute :

```apache
ServerTokens Prod
ServerSignature Off
TraceEnable Off
Header unset ETag
FileETag None
```

Active la configuration si besoin et redémarre :

```bash
sudo a2enconf security
sudo systemctl restart apache2
```

## Analysez les journaux et bannissez les hôtes suspects – Fail2Ban

> **DenyHosts est obsolète** : plus maintenu depuis 2014 et incompatible avec systemd. Utilise uniquement **Fail2Ban**, qui remplit le même rôle avec une bien meilleure intégration système.

Installation :

```bash
sudo apt install fail2ban
```

Crée une configuration locale — ne jamais modifier `jail.conf` directement, il est écrasé lors des mises à jour :

```bash
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
sudo nano /etc/fail2ban/jail.local
```

Configure la jail SSH (adapte le port si tu l'as changé) :

```ini
[sshd]
enabled  = true
port     = <TON_PORT_SSH>
filter   = sshd
logpath  = /var/log/auth.log
maxretry = 3
bantime  = 3600
findtime = 600
```

Pour recevoir des alertes email en cas de bannissement :

```ini
[DEFAULT]
destemail = ton@email.com
action = %(action_mwl)s
```

Démarre et active au démarrage :

```bash
sudo systemctl enable --now fail2ban
```

Vérifie l'état :

```bash
sudo fail2ban-client status
sudo fail2ban-client status sshd
```

## Conclusion — sécurité de votre serveur Linux en pratique

Ces mesures constituent une base solide pour tout serveur Linux exposé sur internet. L'ordre d'application compte : commence par SSH (tu ne veux pas te bloquer toi-même), puis sysctl, puis fail2ban.

Quelques rappels essentiels :

- Teste chaque changement SSH dans une **seconde session** avant de fermer la première
- Configure un pare-feu (`ufw` ou `iptables`) en complément — ce guide ne le couvre pas
- Mets à jour régulièrement : `sudo apt update && sudo apt upgrade`
- Surveille les logs : `journalctl -u ssh`, `sudo fail2ban-client status sshd`

## Articles connexes

- [Dépannage des problèmes de montage de matrices RAID (mdadm)](/depannage-montage-partition-raid-linux-mode-secours/)
- [Content-Security-Policy : Protéger votre site sans bloquer vos scripts](/content-security-policy-nginx-sans-casser-site/)
