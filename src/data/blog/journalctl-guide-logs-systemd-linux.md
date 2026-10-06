---
title: "Journalctl Linux : lire et filtrer les logs systemd comme un pro"
description: "Journalctl Linux sans prise de tête : filtrer les logs systemd par service, priorité, date et boot, rendre le journal persistant et limiter sa taille."
pubDatetime: "2026-10-06T11:01:11+02:00"
modDatetime: "2026-10-05T08:00:00.000Z"
author: Brandon
tags:
  - linux
  - sysadmin
  - terminal
  - monitoring
  - intermediaire
featured: false
draft: false
focusKeyword: journalctl linux
faqs:
  - question: "Pourquoi journalctl ne montre-t-il rien après un redémarrage ?"
    answer: "Le journal est peut-être volatile : il vit dans /run et disparaît au reboot. Crée /var/log/journal, puis redémarre systemd-journald pour le rendre persistant."
  - question: "Comment limiter la taille du journal systemd sur mon serveur ?"
    answer: "Utilise sudo journalctl --vacuum-size=500M pour rogner tout de suite, ou fixe SystemMaxUse dans /etc/systemd/journald.conf pour une limite permanente."
  - question: "Puis-je lire les logs systemd sans passer par sudo ?"
    answer: "Oui, si ton utilisateur appartient au groupe systemd-journal (et adm sur Debian et Ubuntu). Sinon, journalctl n'affiche que tes propres entrées."
---
> 💡 **TL;DR**
> - `journalctl` lit le journal binaire de systemd : les logs de tous les services, du noyau et des démarrages au même endroit
> - Filtre avec `-u` (service), `-p` (priorité), `-b` (démarrage) et `--since` / `--until` (plage horaire), suis le flux avec `-f`
> - Rends le journal persistant et borne-le (`SystemMaxUse`, `--vacuum-size`), sinon il ne survit pas au reboot ou grossit sans prévenir

## Journalctl Linux : le journal unique de systemd

Tu as un serveur qui rame, un service qui redémarre en boucle, et tu tapes `tail -f /var/log/syslog` par réflexe. Ça marche un temps. Puis tu découvres que la distribution a changé de fichier, que le service écrit ailleurs, et que les horodatages ne veulent plus rien dire sans fuseau horaire. Bienvenue dans le monde où systemd gère les logs.

Sur un système Linux moderne, `systemd-journald` récupère tout : sorties standard des services, messages du noyau, traces d'authentification. Il écrit le tout dans un format binaire indexé. Pour lire ce format, on passe par `journalctl`. Pas de grep sur un fichier texte géant, pas de logrotate à configurer à la main pour les messages systemd.

Le revers, c'est que le binaire ne se lit pas avec `cat`. Mais c'est justement ce qui permet des filtres précis sur l'unité, la priorité ou l'heure, en une seule ligne. Chez moi, c'est le premier réflexe dès qu'un LXC se comporte mal, avant même de toucher à la configuration.

Ce guide sur journalctl Linux part des commandes de base et va jusqu'à des cas de dépannage concrets. Les commandes sont les mêmes sur Debian, Ubuntu, Fedora ou Arch. Seuls quelques noms de services changent, comme `ssh` contre `sshd`. La référence reste la page de manuel (`man journalctl`), disponible en ligne sur [man7.org](https://man7.org/linux/man-pages/man1/journalctl.1.html), mais tu n'as pas besoin de la lire en entier pour être efficace.

## Table des matières

## Les bases : lire le journal sans se noyer

Sans option, la commande journalctl Linux affiche tout l'historique, du plus ancien au plus récent, dans un pager. Sur une machine qui tourne depuis six mois, c'est inutilisable. Commence donc par les options qui répondent à une question précise :

```bash
journalctl -n 50              # les 50 dernières entrées
journalctl -r -n 20           # les 20 dernières, la plus récente en haut
journalctl -f                 # suit le flux en direct, comme tail -f
journalctl --no-pager -n 50   # sortie brute dans le terminal, pratique pour un copier-coller
```

Pour une erreur qui vient de se produire, `-x` ajoute les explications du catalogue de messages quand elles existent, et `-e` place le curseur en fin de journal. La combinaison `journalctl -xe` est le réflexe après un échec de démarrage : elle ouvre directement les dernières erreurs, avec des liens d'aide quand systemd en connaît.

Le format de sortie se règle avec `-o`. Le défaut `short` reste lisible à l'œil. `short-iso` ajoute une date complète au format ISO, ce qui est utile quand tu compares deux machines. Pour une sortie exploitable dans un script, `-o json` produit une entrée JSON par ligne, et `-o json-pretty` la rend lisible à l'écran :

```bash
journalctl -u ssh -n 1 -o json-pretty
```

Une remarque au passage : journalctl Linux ouvre un pager (`less`) dès que la sortie dépasse la hauteur du terminal. Pour envoyer le résultat dans un fichier ou un pipe, pense au `--no-pager`, sinon tu vas te retrouver à quitter l'outil avec `q` dans un script qui attend une réponse.

## Filtrer par service, priorité et date

C'est là que journalctl Linux devient vraiment utile. Le filtre le plus courant est l'unité systemd, avec `-u`. Le suffixe `.service` est facultatif :

```bash
journalctl -u ssh
journalctl -u nginx -u docker
```

Deux `-u` affichent les deux unités, c'est un OU. En revanche, des filtres de types différents se combinent en ET : `-u ssh -p warning` ne montre que les avertissements SSH. Retiens cette logique, elle évite de fouiller 40 000 lignes pour rien.

Sur les distributions issues de RHEL, le service SSH s'appelle `sshd`, pas `ssh`. Si le journal semble vide, vérifie le nom exact avant de conclure qu'il ne s'est rien passé :

```bash
systemctl list-units --type=service | grep -i ssh
```

Pour la priorité, `-p` accepte les niveaux syslog : `emerg`, `alert`, `crit`, `err`, `warning`, `notice`, `info` et `debug`. Attention au sens : `-p err` affiche les erreurs et tout ce qui est plus grave que `err`, pas seulement les erreurs. Pour une plage, la syntaxe `-p warning..err` fonctionne aussi.

```bash
journalctl -p err -b
journalctl -u docker -p warning --since "1 hour ago"
```

Pour le temps, `--since` et `--until` acceptent une date absolue ou une formule relative. Le format `"2026-10-05 08:00"` marche aussi bien que `today` ou `"30 min ago"`, et les trois se combinent sans effort :

```bash
journalctl --since "2026-10-05 08:00" --until "2026-10-05 09:30"
journalctl --since today -p warning
```

Quand le service n'est pas une unité systemd, par exemple un script lancé à la main ou un binaire qui logue directement, le filtre `-t` (identifiant syslog) fait le job. Et pour aller plus loin, les champs du journal se filtrent directement : `journalctl _PID=1234` ou `journalctl _COMM=sshd`. Tu ne connais pas les noms de champs ? `journalctl -o verbose -n 1` les affiche tous pour une entrée.

## Boot et noyau : remonter dans le temps

Après un reboot forcé ou une coupure de courant, la première question est souvent : « qu'est-ce qui s'est passé juste avant ? ». Avec journalctl Linux, le filtre `-b` répond à ça. Sans argument, il limite la sortie au démarrage en cours. `-b -1` remonte au démarrage précédent, `-b -2` à celui d'avant, et ainsi de suite.

```bash
journalctl --list-boots
journalctl -b -1 -p err
```

`--list-boots` liste les démarrages connus avec leur identifiant et leurs dates. C'est le point de départ quand tu ne sais pas combien de reboots se sont enchaînés. Attention, ça ne marche que si le journal est persistant, on verra comment un peu plus bas.

Pour le noyau, `-k` (ou `--dmesg`) ne garde que les messages du noyau. C'est l'équivalent de `dmesg`, avec un avantage : ces messages sont aussi archivés et tu peux les consulter pour un démarrage passé. Si un disque commence à lâcher ou qu'un module fait des siennes, la première trace se trouve souvent là :

```bash
journalctl -k -b 0 -p warning
```

Un cas typique : un serveur qui freeze au démarrage sans raison apparente. Tu peux lire `journalctl -b -1 -p warning` juste après le redémarrage pour voir les dernières alertes avant le plantage. Si le journal n'est pas persistant, cette commande ne ramène rien, et c'est exactement le piège de la section suivante.

## Rendre le journal persistant et le borner

Le comportement par défaut de journalctl Linux dépend de la configuration. Quand `/var/log/journal` n'existe pas, le journal est stocké dans `/run`, donc en RAM, et disparaît au reboot. C'est pour ça que tu ne retrouves rien après un crash. Le réglage `Storage=auto` de `/etc/systemd/journald.conf` écrit sur disque si ce dossier existe. Le plus simple est donc de le créer, puis de redémarrer le service :

```bash
sudo mkdir -p /var/log/journal
sudo systemctl restart systemd-journald
```

Ensuite, il faut borner la taille. Le journal ne passe pas par logrotate, il s'auto-limite selon des seuils. Ces seuils se règlent dans `journald.conf` :

```ini
[Journal]
Storage=persistent
SystemMaxUse=500M
MaxRetentionSec=1month
```

`SystemMaxUse` fixe la taille maximale sur disque, `MaxRetentionSec` la durée de conservation. Après modification, un `sudo systemctl restart systemd-journald` suffit. Pour vérifier l'occupation actuelle, utilise `journalctl --disk-usage`.

Si le journal a déjà gonflé et que tu veux récupérer de la place tout de suite, deux options existent :

```bash
sudo journalctl --vacuum-size=500M
sudo journalctl --vacuum-time=2weeks
```

⚠️ Le `--vacuum` supprime définitivement les vieilles entrées. Vérifie d'abord ce que tu veux garder, un journal vidé ne se reconstitue pas.

Dernier point d'administration : lire le journal sans `sudo`. Ton utilisateur doit appartenir au groupe `systemd-journal`, et sur Debian et Ubuntu au groupe `adm` également. Ajoute-le avec `sudo usermod -aG systemd-journal $USER`, puis ouvre une nouvelle session, le groupe n'est pris en compte qu'à la connexion suivante.

## Dépannage : trois cas concrets

### Un service qui redémarre en boucle

Premier réflexe : `systemctl status` donne le code de sortie et les dernières lignes. Mais le vrai diagnostic se trouve souvent plus haut dans le journal, juste avant la première ligne « Failed ». Remonte de 100 lignes, pas de 10 :

```bash
systemctl status monservice
journalctl -u monservice -n 100 --no-pager
```

Si le plantage est intermittent, avec journalctl Linux en surveillance continue, lance `journalctl -u monservice -f` dans un second terminal et reproduis l'action qui le déclenche. Tu vois l'erreur au moment où elle tombe, pas trois heures plus tard.

### Un serveur qui ne démarre plus proprement

Quand un montage échoue au boot, le système bascule souvent en mode de secours. C'est là que le journal sert le plus, puisque le réseau et les services ne sont pas forcément disponibles. Le journal du démarrage précédent, avec `-b -1`, montre quel montage a échoué et pourquoi. Pour le cas d'une matrice RAID qui refuse de monter, le guide sur le [dépannage des montages RAID en mode de secours](/depannage-montage-partition-raid-linux-mode-secours/) reprend la procédure pas à pas.

### Des horodatages incohérents

Si les entrées du journal ne se suivent pas, ou si une alerte semble venir du futur, le problème vient rarement de journalctl. C'est l'horloge du serveur qui est fausse, ou le fuseau horaire mal réglé. Avant de chercher ailleurs, vérifie avec `timedatectl`, puis reprends le réglage décrit dans [le guide pour définir le fuseau horaire et synchroniser l'heure du serveur](/comment-modifier-heure-du-serveur-sous-linux/).

Si tu préfères une interface web, Cockpit affiche les mêmes données que journalctl Linux dans sa section dédiée aux logs. Ça ne remplace pas le terminal pour les filtres fins, mais c'est pratique pour un coup d'œil rapide, comme le montre [l'article sur Cockpit pour l'administration Docker](/cockpit-docker-interface-web-administration/).

## Conclusion

Trois réflexes suffisent pour 90 % des cas avec journalctl Linux. Filtre par unité avec `-u`, par priorité avec `-p` et par heure avec `--since`. Pour le passé, pense aux boots avec `-b -1` et `--list-boots`. Et règle le journal dès le début : dossier `/var/log/journal` pour la persistance, `SystemMaxUse` pour la taille.

Le reste, c'est de la pratique. La prochaine fois qu'un service plante, ne lance pas `tail` au hasard. Tape `journalctl -xe`, lis les dix dernières lignes, et tu auras déjà une piste.
