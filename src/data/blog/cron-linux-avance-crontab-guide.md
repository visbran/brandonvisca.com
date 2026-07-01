---
title: "Cron Linux avancé : crontab, variables et pièges"
description: "Maîtrise cron et crontab sur Linux : syntaxe avancée, variables d'environnement, pièges classiques et cas pratiques pour planifier tes tâches sans souci."
pubDatetime: "2026-07-01T08:00:00.000Z"
modDatetime: "2026-07-01T08:00:00.000Z"
author: Brandon Visca
tags:
  - intermediaire
  - linux
  - sysadmin
  - cron
  - planification
featured: false
draft: false
focusKeyword: cron linux avance
ogImage: ""
---
> 💡 **TL;DR**
> - Cron est partout mais personne ne le comprend vraiment ; une bonne maîtrise évite des jobs qui tournent à 3h du matin pour rien
> - Les variables d'environnement dans crontab ne sont PAS celles de ton shell interactif : PATH, SHELL et MAILTO sont des pièges à connaître
> - Les spéciaux `@daily`, `@reboot`, `*/n` et le pourcent `%` ont des comportements surprenants qu'il faut anticiper
> - Ce guide couvre la syntaxe complète, les cas avancés et les erreurs qui font pleurer en production

## Introduction : pourquoi cron mérite un article dédié

Cron est l'un des outils les plus anciens et les plus utilisés sur Linux. Il tourne sur quasiment tous les serveurs du monde, planifie des backups, nettoie des logs, rafraîchit des certificats. Et pourtant, la plupart des sysadmins le configurent à l'aveugle en copiant une ligne Stack Overflow sans vraiment comprendre ce qui se passe.

Résultat : des jobs qui s'exécutent avec les mauvaises variables d'environnement, des scripts qui échouent silencieusement parce que `PATH` est vide, des serveurs qui spamment root toutes les cinq minutes avec des erreurs incompréhensibles. Ce n'est pas une fatalité. Cron est simple, mais il a des règles précises. Les connaître fait la différence entre un serveur qui tourne tranquille et une nuit de debug à 2h du matin.

Si tu cherches aussi à synchroniser l'heure de tes machines pour que tes cron jobs déclenchent au bon moment, j'ai un [guide sur Chrony Docker](/chrony-docker-serveur-ntp-homelab/) qui te montrera comment tenir une horloge précise. Et si tu débutes sur Linux, commence par mes [commandes de hardening essentielles](/hardening-linux-10-commandes/) avant d'automatiser quoi que ce soit.

## La syntaxe crontab en détail

Un fichier crontab contient une ligne par tâche. Chaque ligne suit ce format :

```bash
# minute heure_jour jour_mois mois jour_semaine commande
* * * * * /chemin/vers/script.sh
```

Les cinq premiers champs sont :

| Champ | Valeurs possibles | Exemples |
|-------|-------------------|----------|
| Minute | 0-59 | `0` = pile à l'heure |
| Heure | 0-23 | `2` = 2h du matin |
| Jour du mois | 1-31 | `1` = premier du mois |
| Mois | 1-12 ou noms | `1` = janvier |
| Jour de la semaine | 0-7 (0 et 7 = dimanche) | `1` = lundi |

Les astérisques `*` signifient "toutes les valeurs". Tu peux aussi utiliser des plages (`10-15`), des listes (`1,3,5`), des pas (`*/10`) et des noms de mois/jours en anglais (`jan`, `mon`).

Quelques exemples concrets :

```bash
# Toutes les 5 minutes
*/5 * * * * /opt/scripts/check-health.sh

# Tous les jours à 3h du matin
0 3 * * * /opt/scripts/backup-daily.sh

# Le premier lundi de chaque mois à 8h
0 8 1-7 * 1 /opt/scripts/rapport-mensuel.sh

# Toutes les heures en semaine, de 9h à 18h
0 9-18 * * 1-5 /opt/scripts/sync-data.sh
```

Le dernier exemple montre une combinaison plage + jour de la semaine. Attention : quand tu combines jour du mois ET jour de la semaine, cron les considère comme un OU, pas un ET. Si tu écris `0 8 1 * 1`, le job tourne le premier DU MOIS **ou** le premier LUNDI du mois. Pour un vrai "premier lundi", il faut une astuce ou un test dans le script.

## Les variables d'environnement dans crontab

Voici le piège numéro un. Quand cron exécute une tâche, il ne charge pas ton `.bashrc`, ton `.profile`, ni même `/etc/profile`. Il part d'un environnement minimaliste. Cela veut dire que `PATH` est souvent réduit à `/usr/bin:/bin`, que `HOME` est celui de l'utilisateur, mais que `SHELL` par défaut est `/bin/sh`, même si ton utilisateur utilise bash ou zsh.

Regarde un `crontab -e` typique d'un débutant qui plante :

```bash
* * * * * python3 /opt/scripts/alert.py
```

Chez toi, `python3` est dans `/usr/local/bin`. Sous cron, `PATH` ne contient pas `/usr/local/bin`. Le job échoue avec "command not found". Sans bruit, sans log apparent si tu n'as pas configuré `MAILTO`.

### Déclarer ses variables en haut de crontab

La bonne pratique : déclarer explicitement les variables en début de fichier :

```bash
SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
MAILTO=admin@example.com
HOME=/opt/scripts

# Tes jobs ici
0 3 * * * /opt/scripts/backup-daily.sh
*/5 * * * * /usr/local/bin/python3 /opt/scripts/monitor.py
```

| Variable | Rôle | Valeur conseillée |
|----------|------|-------------------|
| `SHELL` | Interpréteur qui exécute les commandes | `/bin/bash` si tu utilises des features bash |
| `PATH` | Chemins de recherche des binaires | Copie la sortie de `echo $PATH` dans ton shell |
| `MAILTO` | Adresse pour recevoir la sortie stdout/stderr | Une vraie adresse, ou `""` pour désactiver |
| `HOME` | Répertoire de travail du job | Le répertoire où tournent tes scripts |

**Astuce pro** : au lieu de deviner `PATH`, ouvre un shell interactif en tant que l'utilisateur cron et tape `echo $PATH`. Copie-colle cette valeur dans ton crontab. Ça élimine 80 % des erreurs "command not found".

### Le pourcent `%` : un caractère interdit ou presque

Dans une ligne crontab, le signe `%` a une signification spéciale : il sert de séparateur entre la commande et son entrée standard (stdin). Si ton script ou ta commande contient un `%` sans être échappé, tout ce qui suit est considéré comme stdin.

Exemple qui plante :

```bash
# FAUX : le % est interprété
0 2 * * * date +%Y-%m-%d > /tmp/backup-$(date +%Y%m%d).log
```

Corrige en échappant avec un backslash :

```bash
# CORRECT
0 2 * * * date +\%Y-\%m-\%d > /tmp/backup-$(date +\%Y\%m\%d).log
```

Ou mieux encore, encapsule la logique dans un script shell dédié et appelle-le depuis cron. Ça évite les acrobaties d'échappement.

## Les spéciaux `@` : raccourcis pratiques

Cron moderne (Vixie cron, cronie) supporte des raccourcis lisibles. Ils remplacent les cinq champs par un mot-clé.

| Raccourci | Signification | Équivalent |
|-----------|--------------|------------|
| `@reboot` | Au démarrage de la machine |, |
| `@yearly` | Une fois par an (1er janvier à 0h00) | `0 0 1 1 *` |
| `@monthly` | Une fois par mois (1er du mois à 0h00) | `0 0 1 * *` |
| `@weekly` | Une fois par semaine (dimanche à 0h00) | `0 0 * * 0` |
| `@daily` | Une fois par jour (à 0h00) | `0 0 * * *` |
| `@hourly` | Une fois par heure (à xx:00) | `0 * * * *` |

`@reboot` est particulièrement utile pour lancer des services qui ne méritent pas un systemd unit complet, ou pour des scripts d'initialisation rapides. Attention cependant : `@reboot` déclenche quand cron démarre, pas forcément quand tout le système est prêt. Si ton script dépend du réseau ou d'un service, ajoute une boucle de retry.

```bash
@reboot /opt/scripts/wait-for-network.sh && /opt/scripts/start-agent.sh
```

Et `@daily` à minuit ? Sur un serveur qui fait des backups, c'est le moment où tout le monde planifie ses tâches. Si tu as dix machines qui partent en backup à 0h00 pile, ton NAS va crier. Décale de quelques minutes (`13 2 * * *` par exemple), ou utilise un minute aléatoire.

## Les pièges classiques

### 1. Le PATH réduit

On l'a dit, mais c'est tellement courant que ça mérite une section dédiée. Si ton script utilise `jq`, `curl`, `docker`, `python3`, `node` ou tout binaire hors `/usr/bin:/bin`, il plantera sous cron. Solution : soit tu mets le chemin absolu (`/usr/bin/curl`), soit tu définis `PATH` en haut de crontab.

### 2. Les sorties non redirigées

Par défaut, cron envoie stdout et stderr par email à `root` (ou à l'utilisateur du crontab). Sur un desktop, tu t'en fiches peut-être. Sur un serveur sans MTA configuré, les emails s'accumulent dans `/var/spool/mail/` et finissent par remplir le disque.

Trois solutions :

```bash
# 1. Rediriger tout vers un fichier log
*/5 * * * * /opt/scripts/job.sh >> /var/log/cron-job.log 2>&1

# 2. Jeter la sortie si tu t'en fiches
*/5 * * * * /opt/scripts/job.sh > /dev/null 2>&1

# 3. Désactiver les emails avec MAILTO
MAILTO=""
*/5 * * * * /opt/scripts/job.sh
```

Personnellement, je préfère la solution 1 : un fichier de log daté, que je fais tourner avec logrotate. Comme ça, quand un job plante, j'ai une piste.

### 3. L'utilisateur qui n'est pas celui qu'on pense

`crontab -e` édite le crontab de l'utilisateur courant. `sudo crontab -e` édite celui de root. `/etc/crontab` et `/etc/cron.d/` peuvent spécifier un utilisateur après les cinq champs de temps :

```bash
# /etc/crontab ou /etc/cron.d/backup
0 3 * * * root /opt/scripts/backup.sh
0 4 * * * www-data /opt/scripts/cleanup-uploads.sh
```

Si tu mets un utilisateur dans un crontab utilisateur (`crontab -e` normal), cron va interpréter le nom d'utilisateur comme le début de la commande, et ça plantera. C'est un classique quand on copie-colle une ligne depuis `/etc/crontab`.

### 4. Le fuseau horaire

Cron utilise l'heure système locale. Si tu changes de fuseau horaire (`timedatectl set-timezone Europe/Paris`), les jobs s'adaptent. Mais si tu as des jobs critiques qui doivent tourner à une heure précise UTC, il faut gérer ça au niveau du script ou utiliser `TZ=UTC` avant la commande.

```bash
# Forcer UTC pour ce job
0 3 * * * TZ=UTC /opt/scripts/backup-utc.sh
```

Si tu veux comprendre comment gérer proprement les fuseaux horaires sur Linux, mon article sur [la modification de l'heure du serveur sous Linux](/comment-modifier-heure-du-serveur-sous-linux/) détaille `timedatectl` et les pièges de la synchronisation NTP.

### 5. Les droits sur le script

Un script avec les bons chemins mais sans bit d'exécution ne tournera pas :

```bash
chmod +x /opt/scripts/backup-daily.sh
```

Et n'oublie pas le shebang en première ligne (`#!/bin/bash` ou `#!/usr/bin/env python3`). Sans shebang, cron ne sait pas quel interpréteur utiliser, même si `SHELL` est défini dans le crontab.

## Cas avancés : run-parts, anacron et systemd timers

### run-parts : des répertoires de scripts

Sur Debian et Ubuntu, `/etc/cron.hourly/`, `/etc/cron.daily/`, `/etc/cron.weekly/` et `/etc/cron.monthly/` sont gérés par `run-parts`. Tu déposes un script exécutable dans le répertoire, et il tourne à la fréquence indiquée.

Règles de run-parts :
- Le nom du fichier ne doit contenir QUE des caractères alphanumériques, tirets et underscores. Pas de point, pas d'extension `.sh`.
- Le script doit être exécutable (`chmod +x`).

```bash
# Créer un script daily valide pour run-parts
sudo nano /etc/cron.daily/backup-mysql
sudo chmod +x /etc/cron.daily/backup-mysql
```

### Anacron : pour les machines qui ne tournent pas 24/7

Si tu as un laptop ou un NAS qui s'éteint la nuit, cron classique va rater les jobs prévus à 3h du matin. Anacron est là pour ça : il garde en mémoire la dernière exécution et lance le job au prochain démarrage s'il a été manqué.

Anacron est configuré dans `/etc/anacrontab` :

```bash
# période_en_jours délai_identificateur commande
7 10 backup.weekly /opt/scripts/backup-weekly.sh
```

Sur les systèmes modernes, cronie (RHEL/CentOS/Fedora) intègre anacron. Sur Debian, les paquets `anacron` et `cron` cohabitent. Si tu veux absolument que ton job tourne même après une coupure, anacron est ton ami.

### Systemd timers : l'alternative moderne

Si tu utilises une distribution moderne avec systemd, les timers sont une alternative puissante à cron. Ils offrent des avantages : journalisation native (`journalctl`), dépendances entre services, gestion des fuseaux horaires, et exécution manquée (Persistent=true).

Exemple minimal d'un timer systemd :

```ini
# /etc/systemd/system/backup-daily.timer
[Unit]
Description=Backup journalière

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
```

Et le service associé :

```ini
# /etc/systemd/system/backup-daily.service
[Unit]
Description=Script de backup journalier

[Service]
Type=oneshot
ExecStart=/opt/scripts/backup-daily.sh
```

Puis :

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now backup-daily.timer
systemctl list-timers
```

Je ne dis pas que systemd timers remplacent cron, cron reste universel et lisible, mais pour des infrastructures modernes, c'est une option à considérer.

## Sécuriser ses cron jobs

Un cron job mal sécurisé est une porte d'entrée. Quelques règles :

1. **Ne jamais mettre de secrets en clair dans un crontab**. Les fichiers crontab sont lisibles par root, mais aussi parfois par d'autres utilisateurs selon les permissions. Stocke les tokens dans des fichiers séparés avec des droits restreints (`chmod 600`).

2. **Verrouiller le crontab des utilisateurs non-trustés**. Crée `/etc/cron.deny` ou `/etc/cron.allow` pour contrôler qui peut créer des cron jobs. Si tu n'as que root et un utilisateur dédié `deploy`, whitelist-les :

```bash
# /etc/cron.allow
deploy
root
```

3. **Auditer régulièrement les crontabs**. Une commande simple pour lister tous les jobs cron sur le système :

```bash
for user in $(cut -f1 -d: /etc/passwd); do echo "=== $user ==="; crontab -u $user -l 2>/dev/null; done
```

4. **Limiter les droits du script**. Le script appelé par cron ne doit pas tourner en root s'il n'en a pas besoin. Crée un utilisateur dédié (`backup`, `monitoring`) avec les droits minimaux.

Ces bonnes pratiques s'inscrivent dans une stratégie de durcissement globale. Pour aller plus loin sur la sécurisation de ton serveur, je te renvoie vers mon article de [hardening Linux en 10 commandes](/hardening-linux-10-commandes/).

## Debugging : quand ça ne marche pas

La procédure de debug en quatre étapes :

1. **Vérifier que le job est bien chargé** : `crontab -l` pour l'utilisateur, ou `cat /etc/cron.d/monfichier`.
2. **Vérifier les logs système** : sur systemd, `journalctl -u cron` (Debian/Ubuntu) ou `journalctl -u crond` (RHEL). Sur des systèmes plus anciens, `/var/log/syslog` ou `/var/log/cron`.
3. **Lancer la commande à la main** dans le même environnement que cron :

```bash
env -i SHELL=/bin/sh HOME=/root PATH=/usr/bin:/bin /opt/scripts/job.sh
```

Cette commande simule l'environnement minimaliste de cron. Si ça plante ici, ça plantera sous cron.

4. **Ajouter du logging explicite** dans le script ou dans la ligne crontab :

```bash
*/5 * * * * /opt/scripts/job.sh >> /var/log/job.log 2>&1
```

Et n'oublie pas : cron n'envoie pas d'email si `MAILTO` n'est pas configuré et que la sortie est redirigée. Si tu ne vois rien nulle part, c'est souvent que le job n'a jamais été lu par cron, vérifie que le service tourne (`systemctl status cron`).

## Conclusion

Cron n'est pas compliqué, mais il est exigeant. Il exécute exactement ce que tu lui demandes, dans l'environnement que tu lui donnes, à l'heure que tu spécifies. Le problème, c'est que la plupart des gens supposent que cron "hérite" de leur shell interactif. Spoiler : non. PATH minimal, pas de `.bashrc`, pas de variables exportées à l'arrache.

La recette pour des cron jobs solides : chemin absolu pour les binaires, variables d'environnement explicites en haut du crontab, redirection des sorties vers un fichier log rotaté, et un test dans un environnement purifié avant de lancer en production. Ce n'est pas de la magie, c'est de la discipline. Et c'est exactement ce qui sépare un serveur qui tourne pendant des années de celui qui te réveille à 3h du matin avec un disque plein de mails d'erreur.
