---
title: "Hardening Linux : 10 commandes pour durcir ton serveur"
description: "Hardening Linux en 10 commandes : durcissez votre serveur en quelques minutes. SSH, pare-feu, mises à jour auto, audit sécurité. Guide pratique 2026."
pubDatetime: "2026-06-06T08:00:00.000Z"
author: Brandon Visca
tags:
  - linux
  - securite
  - intermediaire
  - hardening
  - sysadmin
  - commandes
featured: false
draft: false
ogImage: "" 
---
> 💡 **TL;DR**
> - Durcir un serveur Linux prend dix minutes avec dix commandes, sans être expert en sécurité
> - Pare-feu actif, SSH verrouillé, mises à jour automatiques et un audit rapide
> - Ces basiques éliminent 90 % des attaques automatisées qui scannent internet

## Pourquoi dix commandes suffisent

Les robots qui scanent internet ne cherchent pas à exploiter des zero-days sophistiqués. Ils testent des ports ouverts, des mots de passe faibles et des services obsolètes. En appliquant les basiques du hardening, tu passes sous leur radar. Ce guide est volontairement court et actionnable : chaque section donne une commande à copier-coller, une explication de ce qu'elle corrige, et un moyen de vérifier que ça fonctionne.

Si tu cherches une approche plus poussée avec Docker et Fail2Ban, lis plutôt mon [guide sécurité serveur Linux complet](/securite-de-votre-serveur-linux/). Celui-ci reste focalisé sur les commandes natives, sans container.

## 1. Mettre à jour le système

```bash
sudo apt update && sudo apt upgrade -y
```

C'est la commande la plus importante et la plus négligée. Un serveur avec des paquets non patchés est une cible facile. Sur Debian et Ubuntu, `unattended-upgrades` gère les mises à jour de sécurité automatiquement.

```bash
sudo apt install unattended-upgrades -y
sudo dpkg-reconfigure -plow unattended-upgrades
```

Vérifie que ça tourne :

```bash
sudo systemctl status unattended-upgrades
```

**Ce que ça corrige** : les CVE publiées dans les dépôts officiels. Le délai entre la publication d'un patch et son installation est le facteur de risque numéro un sur les serveurs auto-hébergés.

## 2. Activer le pare-feu UFW

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

Par défaut, tout est fermé sauf ce que tu autorises explicitement. UFW masque ton serveur aux scanners de ports. Si tu utilises Docker, attention : Docker contourne iptables par défaut et peut rendre tes ports conteneur accessibles malgré UFW. J'explique la solution complète dans mon article [UFW Docker : configurer le pare-feu sans casser les conteneurs](/ufw-docker-pare-feu-linux/).

Vérifie les règles :

```bash
sudo ufw status verbose
```

**Ce que ça corrige** : l'exposition accidentelle de services internes (base de données, dashboards d'admin) sur internet.

## 3. Durcir la configuration SSH

```bash
sudo nano /etc/ssh/sshd_config
```

Modifie ou ajoute :

```text
Port 2222
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
MaxAuthTries 3
ClientAliveInterval 300
ClientAliveCountMax 2
AllowUsers tonuser
```

Redémarre SSH :

```bash
sudo systemctl restart sshd
```

**Ce que ça corrige** : les attaques par force brute sur le port 22 avec le compte root. Changer le port réduit le bruit de 99 %. Désactiver les mots de passe et utiliser des clés SSH, ou mieux, des [passkeys SSH biométriques](/passkey-ssh-sshid/), rend l'accès quasi impossible à compromettre.

Vérifie que tu peux te reconnecter avant de fermer ta session actuelle. Sinon, tu te verrouilles dehors.

## 4. Configurer la politique de mots de passe

```bash
sudo chage -M 90 -m 7 -W 14 tonuser
sudo passwd -l root
```

La première ligne force un changement de mot de passe tous les 90 jours, avec un minimum de 7 jours entre deux changements et un avertissement 14 jours avant expiration. La seconde verrouille le compte root.

Pour une politique plus stricte à l'échelle du système, installe `libpam-pwquality` :

```bash
sudo apt install libpam-pwquality -y
```

Puis édite `/etc/security/pwquality.conf` pour imposer une longueur minimale et de la complexité.

**Ce que ça corrige** : les accès compromis via des credentials faibles ou réutilisés. Un mot de passe robuste est le dernier rempart quand une couche de sécurité tombe.

## 5. Renforcer les paramètres kernel avec sysctl

```bash
sudo nano /etc/sysctl.conf
```

Ajoute ou décommente :

```text
net.ipv4.conf.all.rp_filter=1
net.ipv4.conf.default.rp_filter=1
net.ipv4.icmp_echo_ignore_broadcasts=1
net.ipv4.conf.all.accept_source_route=0
net.ipv4.conf.default.accept_source_route=0
net.ipv4.conf.all.accept_redirects=0
net.ipv4.conf.default.accept_redirects=0
net.ipv4.conf.all.secure_redirects=0
net.ipv4.conf.default.secure_redirects=0
net.ipv4.tcp_syncookies=1
net.ipv4.ip_forward=0
kernel.randomize_va_space=2
```

Applique sans redémarrer :

```bash
sudo sysctl -p
```

**Ce que ça corrige** : le spoofing d'IP, les attaques par inondation SYN, le détournement de routage source et la désactivation de l'ASLR. Ces paramètres bloquent des vecteurs d'attaque réseau classiques sans impact sur les usages courants.

## 6. Sécuriser les permissions des fichiers sensibles

```bash
sudo chmod 600 /etc/ssh/sshd_config
sudo chmod 700 /root
sudo chmod 750 /home/tonuser
```

Les fichiers de configuration SSH doivent être lisibles uniquement par root. Le répertoire personnel de l'utilisateur doit être accessible à lui seul.

Vérifie les permissions actuelles :

```bash
sudo ls -la /etc/ssh/
```

**Ce que ça corrige** : la fuite d'informations via des fichiers lisibles par tout le monde. Un `sshd_config` lisible par un utilisateur non privilégié révèle ta configuration (port, utilisateurs autorisés, etc.).

## 7. Repérer les fichiers SUID et SGID suspects

```bash
sudo find / -perm /6000 -type f 2>/dev/null
```

Les binaires avec le bit SUID s'exécutent avec les privilèges du propriétaire, généralement root. Si un programme vulnérable possède ce bit, un attaquant peut escalader ses privilèges.

Audite la liste retournée. Tu devrais reconnaître les binaires légitimes (`passwd`, `sudo`, `ping`). Tout le reste mérite investigation.

Pour retirer le bit SUID d'un binaire suspect :

```bash
sudo chmod u-s /chemin/vers/binaire
```

**Ce que ça corrige** : l'escalade de privilèges locale. Beaucoup d'exploits publics nécessitent un binaire SUID mal configuré pour fonctionner.

## 8. Auditer les ports ouverts et les connexions actives

```bash
sudo ss -tulnp
```

Cette commande affiche tous les ports en écoute (`-l`), les connexions TCP et UDP (`-tu`), avec les noms des processus (`-p`) et sans résoudre les IPs en noms (`-n`).

Compare le résultat avec ce que tu attends voir : SSH, HTTP, HTTPS. Si un port inconnu apparaît, identifie le service derrière avec `sudo lsof -i :PORT`.

**Ce que ça corrige** : la présence de services oubliés ou mal configurés qui écoutent sur l'extérieur. C'est le point de départ de tout scan de vulnérabilité.

## 9. Activer l'audit avec auditd ou Lynis

```bash
sudo apt install lynis -y
sudo lynis audit system
```

Lynis scanne ton système et produit un rapport avec une note de durcissement et une liste de recommandations priorisées. C'est l'outil idéal pour passer d'un hardening empirique à un durcissement mesuré.

Pour une surveillance continue des événements sensibles, installe `auditd` :

```bash
sudo apt install auditd -y
sudo auditctl -w /etc/passwd -p wa -k identity_changes
sudo auditctl -w /etc/ssh/sshd_config -p wa -k ssh_config_changes
```

Consulte les logs d'audit :

```bash
sudo ausearch -k identity_changes
```

**Ce que ça corrige** : l'absence de traçabilité. Sans audit, tu ne sauras jamais quand un fichier critique a été modifié ou par qui.

## 10. Configurer Fail2Ban natif

```bash
sudo apt install fail2ban -y
sudo systemctl enable --now fail2ban
```

Fail2Ban lit les logs de services comme SSH et bannit automatiquement les IPs qui dépassent un seuil d'échecs. La configuration par défaut protège déjà SSH.

Pour un affinage, crée un fichier de configuration local :

```bash
sudo nano /etc/fail2ban/jail.local
```

```ini
[sshd]
enabled = true
port = 2222
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600
findtime = 600
```

Redémarre :

```bash
sudo systemctl restart fail2ban
sudo fail2ban-client status sshd
```

**Ce que ça corrige** : les attaques par dictionnaire et brute-force sur SSH. C'est le complément naturel des commandes 2 et 3. Si tu préfères une approche Docker, j'ai un [guide Fail2Ban en conteneur](/fail2ban-docker-securite-serveur/) qui isole le service sans toucher à l'hôte.

## Tableau récapitulatif

| # | Commande | Objectif | Fréquence |
|---|----------|----------|-----------|
| 1 | `apt upgrade` | Patch les CVE | Quotidienne (auto) |
| 2 | `ufw enable` | Ferme les ports inutiles | Une fois |
| 3 | Éditer `sshd_config` | Bloque root + mots de passe | Une fois |
| 4 | `chage` + `passwd -l` | Force la rotation des credentials | Une fois |
| 5 | `sysctl -p` | Renforce la stack réseau | Une fois |
| 6 | `chmod 600` sur fichiers sensibles | Empêche la fuite de conf | Une fois |
| 7 | `find / -perm /6000` | Repère les SUID suspects | Mensuelle |
| 8 | `ss -tulnp` | Inventaire des ports ouverts | Mensuelle |
| 9 | `lynis audit system` | Note de durcissement | Trimestrielle |
| 10 | `fail2ban-client status` | Bloque les brute-force | Continue |

## Vérifier que tout fonctionne

Une fois les dix commandes appliquées, teste depuis une machine externe :

```bash
nmap -p 22,2222,80,443 TON_IP
```

Le port 22 doit être fermé, le 2222 ouvert (si tu l'as changé), 80 et 443 ouverts. Aucun autre port ne doit apparaître.

Puis teste SSH :

```bash
ssh -p 2222 tonuser@TON_IP
```

La connexion doit fonctionner avec ta clé et rejeter les tentatives par mot de passe.

## Ce qu'il reste à faire

Ces dix commandes couvrent les fondations. Pour aller plus loin, pense à :

- Configurer un système de détection d'intrusion (AIDE, OSSEC).
- Centraliser les logs avec rsyslog ou un outil comme Beszel.
- Mettre en place des sauvegardes chiffrées et testées.
- Auditer régulièrement les comptes et groupes avec `cat /etc/passwd | grep /bin/bash`.

Le hardening n'est pas un état, c'est un processus. Relance `lynis` tous les trimestres et corrige les nouvelles alertes.
