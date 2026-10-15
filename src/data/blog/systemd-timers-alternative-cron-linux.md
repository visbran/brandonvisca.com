---
title: "Systemd timer : l'alternative moderne à cron sous Linux"
description: "Systemd timer remplace cron sous Linux : syntaxe OnCalendar, création d'un .timer, Persistent, RandomizedDelaySec et comparatif complet avec crontab."
pubDatetime: "2026-10-12T11:01:12+02:00"
modDatetime: "2026-10-11T08:00:00.000Z"
author: Brandon Visca
tags:
  - linux
  - sysadmin
  - automation
  - intermediaire
featured: false
draft: false
focusKeyword: systemd timer
faqs:
  - question: "Un systemd timer consomme plus de ressources qu'une tâche cron ?"
    answer: "Non, l'écart est négligeable. Le timer est géré par systemd déjà en mémoire, et le service ne tourne que pendant l'exécution, exactement comme un script lancé par cron."
  - question: "Faut-il désinstaller cron pour passer aux systemd timers ?"
    answer: "Non, les deux coexistent sans conflit. Tu peux migrer service par service et garder cron pour les tâches ponctuelles que tu ne veux pas réécrire tout de suite."
  - question: "Comment savoir si un systemd timer a raté son exécution ?"
    answer: "Lance systemctl status sur le .timer et le .service associés, puis journalctl -u nom.service pour voir le dernier run et son code de sortie."
---
> 💡 **TL;DR**
> - Un systemd timer associe un fichier `.timer` (le quand) à un fichier `.service` (le quoi), contre une seule ligne illisible pour cron
> - `Persistent=true` rattrape les exécutions manquées après extinction, les logs passent par `journalctl`, et `systemctl list-timers` donne une vue d'ensemble que cron n'a jamais eue
> - Migration recommandée pour les tâches homelab importantes (sauvegardes, renouvellements), cron reste valable pour un script jetable sur un vieux serveur

Tu as sûrement une crontab qui traîne depuis des années, avec des lignes du genre `0 3 * * * /opt/backup.sh` que personne n'ose toucher. Ça marche, mais ça ne dit rien sur ce qui s'est passé à l'exécution, et si le serveur était éteint à 3h du matin, la sauvegarde a juste disparu. Le systemd timer règle ces deux problèmes nativement, sans dépendance externe, sur toute distribution qui tourne avec systemd. Cet article couvre la syntaxe, la création d'un timer complet, le dépannage, et un comparatif honnête avec cron pour savoir quand chacun a sa place.

## Table des matières

## Pourquoi un systemd timer plutôt que cron

cron fait le job depuis les années 1970, et pour une tâche simple sur un vieux serveur, il n'y a aucune raison de le remplacer. Mais dès que tu administres un homelab avec plusieurs services, les limites de cron deviennent gênantes.

Un systemd timer corrige trois points précis :

- **Les exécutions manquées** : si la machine est éteinte au moment où une tâche cron devait tourner, elle ne tourne jamais. `Persistent=true` sur un timer rattrape le coup au prochain démarrage.
- **Les logs éparpillés** : cron redirige la sortie par mail (souvent mal configuré) ou vers un fichier que tu dois gérer toi-même. Un systemd timer envoie tout dans le journal via `journalctl`, au même endroit que le reste de ton système.
- **Les dépendances** : cron ne sait pas attendre que le réseau soit monté avant de lancer un script. Un systemd timer peut s'ordonner après `network-online.target`, sans ajouter un `sleep 30` honteux en tête de script.

> ⚠️ **Portabilité**
> Un systemd timer ne fonctionne que sur une distribution avec systemd comme init. Si tu administres aussi du FreeBSD, des conteneurs minimalistes ou un vieux SysV, cron reste le plus petit dénominateur commun.

## Anatomie d'un systemd timer : le duo .timer et .service

Un systemd timer n'est jamais seul. Il active toujours une unité `.service` qui porte le même nom, sauf si tu précises autre chose avec `Unit=`. Deux fichiers, deux responsabilités :

- `monjob.timer` décrit **quand** déclencher
- `monjob.service` décrit **quoi** exécuter

Les deux vivent dans `/etc/systemd/system/` pour des unités système, ou `~/.config/systemd/user/` pour des timers utilisateur (pas besoin de `sudo`, pratique pour des scripts personnels).

Voici le service, volontairement minimal :

```ini
# /etc/systemd/system/backup-nextcloud.service
[Unit]
Description=Sauvegarde quotidienne Nextcloud

[Service]
Type=oneshot
ExecStart=/opt/scripts/backup-nextcloud.sh
User=backup
```

`Type=oneshot` dit à systemd que le process se termine normalement une fois le travail fini, contrairement à un service qui tourne en continu.

## Créer ton premier systemd timer

Passons au fichier `.timer` qui pilote ce service :

```ini
# /etc/systemd/system/backup-nextcloud.timer
[Unit]
Description=Déclenche la sauvegarde Nextcloud tous les jours à 3h

[Timer]
OnCalendar=*-*-* 03:00:00
Persistent=true
RandomizedDelaySec=300

[Install]
WantedBy=timers.target
```

Trois lignes font tout le travail. `OnCalendar` fixe l'horaire au format calendrier de systemd (on détaille la syntaxe juste après). `Persistent=true` déclenche le job au prochain démarrage si le serveur était éteint à 3h. `RandomizedDelaySec=300` étale le déclenchement sur une fenêtre de 5 minutes, utile si tu as dix timers qui visent tous minuit et que tu veux éviter un pic de charge disque.

Active le timer, pas le service (le service se lance tout seul quand le timer sonne) :

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now backup-nextcloud.timer
```

Vérifie qu'il est bien programmé :

```bash
systemctl list-timers backup-nextcloud.timer
```

La commande affiche la prochaine exécution, la dernière, et le temps restant. C'est déjà plus d'information que cron n'en a jamais donné de lui-même.

> 💡 **Astuce**
> Si tu édites ces fichiers avec vim et que tu veux une coloration syntaxique propre pour l'INI et le YAML qui t'entourent, [notre guide d'installation d'un thème vim](/installation-theme-vim-guide/) couvre la configuration de base avec vim-plug.

## La syntaxe OnCalendar, enfin expliquée

C'est le point qui bloque le plus de monde, alors qu'elle tient en quelques règles. Le format général est `JourSemaine Année-Mois-Jour Heure:Minute:Seconde`, et chaque champ accepte `*` (n'importe quelle valeur), des listes séparées par des virgules, ou des plages avec `..`.

Quelques exemples concrets :

```ini
# Tous les jours à minuit
OnCalendar=daily

# Toutes les heures
OnCalendar=hourly

# Du lundi au vendredi à 9h
OnCalendar=Mon..Fri 09:00:00

# Le 1er de chaque mois à 2h
OnCalendar=*-*-01 02:00:00

# Toutes les 15 minutes
OnCalendar=*:0/15
```

`daily`, `hourly`, `weekly` et `monthly` sont des raccourcis pour les formes longues équivalentes. Avant de déployer un systemd timer en production, valide toujours ta syntaxe :

```bash
systemd-analyze calendar "Mon..Fri 09:00:00"
```

La commande te dit si l'expression est valide et calcule la prochaine occurrence réelle. Ça évite de découvrir à 9h05 que ton systemd timer attendait un format légèrement différent.

Pour les tâches qui dépendent de l'horloge système plutôt que du calendrier, il existe aussi `OnBootSec=` (délai après démarrage) et `OnUnitActiveSec=` (délai après la dernière exécution), à combiner librement avec `OnCalendar=` dans la même section `[Timer]`.

## systemd timer vs cron : le comparatif sans filtre

| Critère | systemd timer | cron |
|---|---|---|
| Rattrapage après extinction | Oui, via `Persistent=true` | Non, l'exécution manquée est perdue |
| Logs | Centralisés dans `journalctl` | Mail ou fichier à gérer soi-même |
| Dépendances (réseau, montage) | Oui, via `After=` et les targets | Non, scripts bricolés avec `sleep` |
| Délai aléatoire anti-pic | `RandomizedDelaySec=` natif | Aucun, à coder dans le script |
| Portabilité | Linux avec systemd uniquement | Tout Unix, même sans systemd |
| Simplicité d'une tâche ponctuelle | Deux fichiers à créer | Une ligne dans `crontab -e` |
| Limites cgroup (CPU, mémoire) | Héritées de systemd directement | Aucune sans ajout externe |

Le vrai arbitrage, c'est le temps d'install contre la robustesse à long terme. Pour un script que tu lances une fois et que tu oublies, cron gagne : une ligne, zéro fichier supplémentaire. Pour une sauvegarde, un renouvellement de certificat ou tout ce qui doit absolument tourner même après un redémarrage surprise, le systemd timer vaut l'effort des deux fichiers.

Si tu dois synchroniser l'heure du serveur ou gérer le fuseau horaire avant de poser des `OnCalendar=` fiables, passe par [timedatectl plutôt que par les outils historiques](/comment-modifier-heure-du-serveur-sous-linux/). Un systemd timer réglé en heure locale sur un serveur mal synchronisé déclenchera tes jobs au mauvais moment, ce que cron a exactement le même défaut à partager, soit dit en passant.

## Cas concret : automatiser une sauvegarde avec un systemd timer

Prenons un exemple complet qui dépasse le simple `backup.sh`. Si tu [sauvegardes tes emails avec Vanderplanki](/vanderplanki-sauvegarde-emails-gratuit-multiplateforme/), tu peux déclencher cet export automatiquement plutôt que de le lancer à la main.

```ini
# /etc/systemd/system/export-emails.service
[Unit]
Description=Export automatique des emails via Vanderplanki

[Service]
Type=oneshot
ExecStart=/usr/local/bin/vanderplanki-export --config /etc/vanderplanki/export.conf
```

```ini
# /etc/systemd/system/export-emails.timer
[Unit]
Description=Lance l'export emails chaque nuit

[Timer]
OnCalendar=daily
Persistent=true
AccuracySec=1min

[Install]
WantedBy=timers.target
```

`AccuracySec=1min` ici n'a presque aucun effet visible, mais la valeur par défaut est déjà de 1 minute : systemd regroupe les réveils proches pour économiser l'énergie, utile sur un NUC ou un Raspberry Pi qui tourne 24/7.

## Dépannage : les commandes du quotidien

Un systemd timer qui ne se déclenche pas correctement se diagnostique en trois commandes, dans cet ordre.

D'abord, vérifier que le timer est actif et voir sa prochaine échéance :

```bash
systemctl list-timers --all
```

Ensuite, inspecter l'historique d'exécution du service associé :

```bash
systemctl status export-emails.service
```

Enfin, lire les logs détaillés si le service a échoué :

```bash
journalctl -u export-emails.service --since "1 day ago"
```

> ✅ **Erreur fréquente**
> Un `systemctl enable` sans `--now` active le timer pour le prochain démarrage, mais ne le démarre pas tout de suite. Si tu testes dans l'instant, utilise `systemctl start export-emails.timer` en plus, ou directement `enable --now` dès le départ.

Si tu veux une vue graphique plutôt que du texte dans un terminal SSH, [Cockpit donne une interface web pour surveiller les services systemd](/cockpit-docker-interface-web-administration/) sans retenir toutes ces commandes par cœur.

## Conclusion

Le systemd timer n'est pas un gadget de puriste systemd : c'est la version de cron qui aurait dû exister depuis le début, avec rattrapage des exécutions manquées, logs centralisés et dépendances explicites. Pour une tâche ponctuelle sur un vieux serveur, cron reste suffisant et plus rapide à écrire. Pour tout ce qui compte vraiment dans ton homelab (sauvegardes, renouvellements, exports automatiques), les deux fichiers `.timer` et `.service` sont un investissement de cinq minutes qui t'évite une mauvaise surprise le jour où le serveur redémarre sans prévenir.

Teste d'abord sur une tâche peu critique, valide ta syntaxe `OnCalendar` avec `systemd-analyze calendar`, et migre le reste à ton rythme. Les deux systèmes cohabitent très bien sur la même machine.
