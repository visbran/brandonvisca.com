---
title: "Sécurité de votre serveur linux : Comment durcir un serveur sous linux ?"
pubDatetime: "2024-06-10T19:29:00+02:00"
author: Brandon Visca
description: "Dans ce guide pratique où nous allons renforcer ensemble la sécurité de votre serveur Linux. De l'installation de votre système à l'application des dern..."
tags:
  - linux
  - securite
  - avance
  - sysadmin
  - guide
  - hardening
faqs:
  - question: "Qu'est-ce que le durcissement d'un serveur sous Linux ?"
    answer: "C'est l'ensemble des mesures de sécurité appliquées à un serveur pour minimiser les vulnérabilités : SSH durci, firewall, fail2ban, sysctl renforcés."
  - question: "Comment désactiver la connexion SSH en tant que root et modifier le port ?"
    answer: "Édite /etc/ssh/sshd_config : définis PermitRootLogin no et change le port 22 par un numéro personnalisé."
  - question: "Comment limiter l'accès à su uniquement au groupe admin ?"
    answer: "Crée un groupe admin et utilise dpkg-statoverride pour restreindre l'accès à /bin/su uniquement à ce groupe."
  - question: "Qu'est-ce que DenyHosts et Fail2Ban ?"
    answer: "DenyHosts et Fail2Ban sont des outils qui analysent les logs et bannissent automatiquement les IPs des attaques SSH et autres tentatives malveillantes."
---

Dans ce guide pratique où nous allons renforcer ensemble la sécurité de votre serveur Linux. De l’installation de votre système à l’application des dernières mesures de sécurité, nous allons passer par toutes les étapes nécessaires pour rendre votre serveur aussi sûr que possible.

![Illustration — Sécurité de votre serveur linux](image.gif)  
Assurez-vous de dimensionner en fonction des ressources disponibles, du nombre d’utilisateurs susceptibles de se connecter et de la taille des adhésions aux groupes.

Cette optimisation s’inscrit dans une démarche plus globale de gestion des ressources système — au même titre que la [configuration du swap Linux](https://brandonvisca.com/guide-swap-linux-configuration-optimisation/) qui permet d’éviter les dysfonctionnements en cas de saturation mémoire.

- - - - - -

Sommaire :

- [Durcissement de SSH – désactivation de la connexion en tant que root et changement de port](#durcissement-de-ssh-desactivation-de-la-connexion-en-tant-que-root-et-changement-de-port)
- [Protéger su en limitant l’accès uniquement au groupe admin](#proteger-su-en-limitant-lacces-uniquement-au-groupe-admin)
- [Désactivez la récursion DNS ouverte et supprimez les informations de version – Serveur DNS BIND](#desactivez-la-recursion-dns-ouverte-et-supprimez-les-informations-de-version-serveur-dns-bind)
- [Prévenir l’usurpation d’IP](#prevenir-lusurpation-d-ip)
- [Renforcez PHP pour la sécurité](#renforcez-php-pour-la-securite)
- [Limitez la fuite d’informations Apache](#limitez-la-fuite-dinformations-apache)
- [Analysez les journaux et bannissez les hôtes suspects – DenyHosts et Fail2Ban](#analysez-les-journaux-et-bannissez-les-hotes-suspects-deny-hosts-et-fail-2-ban)
- [Conclusion](#%F0%9F%8E%AF-cas-pratique-securiser-une-stack-dauto-hebergement)
  - [Le scénario : Tu auto-héberges tes services](#le-scenario-tu-auto-heberges-tes-services)
  - [Le problème ? Sans les bonnes pratiques qu’on vient de voir, ton serveur devient une passoire](#le-probleme-sans-les-bonnes-pratiques-quon-vient-de-voir-ton-serveur-devient-une-passoire)
  - [Application directe des sections précédentes](#application-directe-des-sections-precedentes)
  - [Tu veux appliquer tout ça sur une vraie stack ?](#tu-veux-appliquer-tout-ca-sur-une-vraie-stack)
  - [💡 Pourquoi ce cas pratique est important ?](#%F0%9F%92%A1-pourquoi-ce-cas-pratique-est-important)
- [Conclusion](#conclusion)
- [FAQ](#faq)
  - [1. Qu’est-ce que le durcissement d’un serveur sous Linux?](#faq-question-1752438381428)
  - [2. Comment sécuriser la mémoire partagée?](#faq-question-1752438401696)
  - [3. Comment puis-je désactiver la connexion SSH en tant que root et modifier le port?](#faq-question-1752438453510)
  - [4. Comment puis-je limiter l’accès à su uniquement au groupe admin?](#faq-question-1752438501119)
  - [5. Qu’est-ce que DenyHosts et Fail2Ban?](#faq-question-1752438518488)


Sécurisation de la mémoire partagée

- /dev/shm peut être utilisé dans une attaque contre un service en cours d’exécution, tel que httpd. Modifiez /etc/fstab pour le rendre plus sécurisé.
- Ouvrez une fenêtre de terminal et entrez ce qui suit :

```bash
sudo vi /etc/fstab

```

tmpfs     /dev/shm     tmpfs     defaults,noexec,nosuid     0     0


Durcissement de SSH – désactivation de la connexion en tant que root et changement de port

- Le moyen le plus simple de sécuriser SSH est de désactiver la connexion en tant que root et de changer le port SSH pour quelque chose de différent du port standard 22.
- Avant de désactiver la connexion root, créez un nouvel utilisateur SSH et assurez-vous que l’utilisateur appartient au groupe admin (voir l’étape 4. ci-dessous concernant le groupe admin).
- Si vous changez le port SSH, ouvrez également le nouveau port que vous avez choisi sur le pare-feu et fermez le port 22.
- Ouvrez une fenêtre de terminal et entrez :

```bash
sudo vi /etc/ssh/sshd_config

```

Port <ENTREZ VOTRE PORT>
Protocol 2
PermitRootLogin no
DebianBanner no


- Redémarrez le serveur SSH, ouvrez une fenêtre de terminal et entrez :

```bash
sudo /etc/init.d/ssh restart

```

sudo groupadd admin
sudo usermod -a -G admin <VOTRE NOM D'UTILISATEUR ADMIN>
sudo dpkg-statoverride --update --add root admin 4750 /bin/su


Renforcer le réseau avec les paramètres sysctl
==============================================

- Le fichier /etc/sysctl.conf contient tous les paramètres sysctl.
- Pour empêcher le routage source des paquets entrants et enregistrer les IP mal formées, entrez ce qui suit dans une fenêtre de terminal :

```bash
sudo vi /etc/sysctl.conf
```

Ajoutez ensuite les lignes suivantes dans le fichier :

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

# Ignore send redirects
net.ipv4.conf.all.send_redirects = 0
net.ipv4.conf.default.send_redirects = 0

# Bloquer les attaques SYN
net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_max_syn_backlog = 2048
net.ipv4.tcp_synack_retries = 2
net.ipv4.tcp_syn_retries = 5

# Enregistrer les Martiens
net.ipv4.conf.all.log_martians = 1
net.ipv4.icmp_ignore_bogus_error_responses = 1

# Ignorer les redirections ICMP
net.ipv4.conf.all.accept_redirects = 0
net.ipv6.conf.all.accept_redirects = 0
net.ipv4.conf.default.accept_redirects = 0
net.ipv6.conf.default.accept_redirects = 0

# Ignorer les pings dirigés
net.ipv4.icmp_echo_ignore_all = 1
```

- Pour recharger sysctl avec les derniers changements, entrez :

```bash
sudo sysctl -p

```

sudo vi /etc/bind/named.conf.options


- Ajoutez ce qui suit à la section Options :

```bash
recursion no;
version "Not Disclosed";

```

sudo /etc/init.d/bind9 restart


Prévenir l’usurpation d’IP

- Ouvrez un terminal et entrez ce qui suit :

```bash
sudo vi /etc/host.conf

```

order bind,hosts
nospoof on


Renforcez PHP pour la sécurité

- Modifiez le fichier php.ini :

```bash
sudo vi /etc/php5/apache2/php.ini

```

disable_functions = exec,system,shell_exec,passthru
register_globals = Off
expose_php = Off
display_errors = Off
track_errors = Off
html_errors = Off
magic_quotes_gpc = Off


- Redémarrez le serveur Apache. Ouvrez un terminal et entrez ce qui suit :

```bash
sudo /etc/init.d/apache2 restart

```

sudo vi /etc/apache2/conf.d/security


- Ajoutez ou modifiez les lignes suivantes et sauvegardez :

```bash
ServerTokens Prod
ServerSignature Off
TraceEnable Off
Header unset ETag
FileETag None

```

sudo /etc/init.d/apache2 restart


Analysez les journaux et bannissez les hôtes suspects – DenyHosts et Fail2Ban

- [DenyHosts](http://denyhosts.sourceforge.net/) est un programme python qui bloque automatiquement les attaques SSH en ajoutant des entrées à /etc/hosts.deny. DenyHosts informera également les administrateurs Linux sur les hôtes offensants, les utilisateurs attaqués et les connexions suspectes.
- Ouvrez un terminal et entrez ce qui suit :

```bash
sudo apt-get install denyhosts

```

sudo vi /etc/denyhosts.conf


- Changez les valeurs suivantes selon les besoins sur votre serveur :

```bash
ADMIN_EMAIL = root@localhost
SMTP_HOST = localhost
SMTP_PORT = 25
#SMTP_USERNAME=foo
#SMTP_PASSWORD=bar
SMTP_FROM = DenyHosts nobody@localhost
#SYSLOG_REPORT=YES

```

sudo apt-get install fail2ban


- Après l’installation, modifiez le fichier de configuration /etc/fail2ban/jail.local et créez les règles de filtre selon les besoins.
- Pour modifier les paramètres, ouvrez une fenêtre de terminal et entrez :

```bash
sudo vi /etc/fail2ban/jail.conf

```

[ssh]

enabled  = true
port     = ssh
filter   = sshd
logpath  = /var/log/auth.log
maxretry = 3


- Si vous avez choisi un port SSH non standard à l’étape 3, vous devez alors changer le paramètre de port dans fail2ban de ssh qui par défaut est le port 22, à votre nouveau numéro de port, par exemple si vous avez choisi 1234 alors port = 1234

```bash
[ssh]

enabled  = true
port     = <ENTREZ VOTRE NUMÉRO DE PORT SSH ICI>
filter   = sshd
logpath  = /var/log/auth.log
maxretry = 3

```

destemail = root@localhost


- et changez la ligne suivante de :

```bash
action = %(action_)s

```

action = %(action_mwl)s


- Vous pouvez également créer des filtres de règles pour les différents services que vous souhaiteriez que fail2ban surveille qui n’est pas fourni par défaut.

```bash
sudo vi /etc/fail2ban/jail.local

```

sudo /etc/init.d/fail2ban restart


- Vous pouvez également vérifier l’état avec.

```bash
sudo fail2ban-client status

```

## Articles connexes

- [Dépannage des problèmes de montage de matrices RAID (mdadm) ](/depannage-montage-partition-raid-linux-mode-secours/)
- [Content-Security-Policy : Protéger votre site sans bloquer v](/content-security-policy-nginx-sans-casser-site/)
