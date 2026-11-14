---
title: "Tmux : le multiplexeur de terminal qui survit à tes déconnexions SSH"
description: "Tmux expliqué simplement : installation, raccourcis essentiels et fichier .tmux.conf pour garder tes sessions SSH actives après une coupure réseau."
pubDatetime: "2026-11-14T11:00:45+01:00"
modDatetime: "2026-11-13T08:00:00.000Z"
author: Brandon
tags:
  - linux
  - terminal
  - ssh
  - intermediaire
featured: false
draft: false
focusKeyword: tmux
faqs:
  - question: "Comment tuer une session tmux qui ne répond plus ?"
    answer: "Depuis un autre terminal, tape tmux kill-session -t nom_session. Si tu es coincé dedans et que rien ne bouge, Ctrl-b suivi de : puis kill-session fait la même chose sans quitter ton terminal."
  - question: "Tmux consomme-t-il beaucoup de RAM sur un petit VPS ?"
    answer: "Non, c'est l'un de ses gros points forts. Le serveur tmux tourne en quelques mégaoctets, même avec une dizaine de fenêtres ouvertes. Rien à voir avec un émulateur de terminal graphique."
  - question: "Deux admins peuvent-ils partager la même session tmux en même temps ?"
    answer: "Oui, c'est même un usage courant en pair-debugging. Les deux se connectent avec tmux attach -t nom_session sur la même machine, et chacun voit en temps réel ce que l'autre tape."
---
> 💡 **TL;DR**
> - Tmux garde tes programmes en vie sur le serveur même quand ta connexion SSH coupe, tu te rattaches à ta session exactement où tu l'as laissée
> - Un préfixe (`Ctrl-b` par défaut) suivi d'une touche pilote tout : fenêtres, panneaux, sessions, copier-coller
> - Un fichier `.tmux.conf` de 20 lignes suffit pour remapper le préfixe, activer la souris et afficher une barre de statut utile
> - Gratuit, open source, dans tous les dépôts de toutes les distributions depuis des années

## Tmux : pourquoi ton terminal a besoin d'un multiplexeur

Tu lances une migration de base de données sur un serveur distant, ta connexion SSH coupe à cause d'un routeur capricieux, et ton script de migration meurt avec elle. Ça te parle ? C'est exactement le problème que tmux résout, et il le résout depuis plus de vingt ans sans jamais changer de philosophie : un processus serveur tourne sur la machine distante, indépendant de ta connexion, et tu te contentes de t'y rattacher.

**Tmux** (Terminal Multiplexer) te permet d'ouvrir plusieurs fenêtres et plusieurs panneaux dans un seul terminal, de détacher une session en cours sans rien interrompre, et de la retrouver intacte des heures ou des jours plus tard. Chez moi, c'est devenu un réflexe avant même de taper la commande SSH : j'ouvre tmux, je travaille, et si ma box internet décide de redémarrer sans prévenir, mes commandes continuent de tourner tranquillement sur le serveur.

Projet mûr, licence ISC, maintenu activement sur GitHub avec des sorties régulières (la 3.8 est la version stable courante). Pas de version payante, pas de compte à créer, juste un binaire qui fait une chose et qui la fait bien.

## Table des matières

## Installer tmux sur ta distribution

Tmux est packagé quasiment partout. Pas besoin de compiler depuis les sources sauf si tu veux la toute dernière fonctionnalité sortie la semaine passée.

Sur Debian et Ubuntu :

```bash
sudo apt update && sudo apt install tmux
```

Sur Fedora, RHEL ou Rocky Linux :

```bash
sudo dnf install tmux
```

Sur Arch Linux :

```bash
sudo pacman -S tmux
```

Sur macOS, via Homebrew :

```bash
brew install tmux
```

Vérifie la version installée avant d'aller plus loin, certaines distributions traînent encore des paquets vieux de plusieurs années :

```bash
tmux -V
```

Si tu es bloqué sur une version antique (en dessous de 3.0), les barres de défilement et la détection automatique du thème clair/sombre du terminal ne seront pas disponibles. Rien de bloquant pour l'usage quotidien, mais garde-le en tête si un raccourci de ce guide ne réagit pas chez toi.

## Les concepts de base : sessions, fenêtres et panneaux

Tmux empile trois niveaux, et comprendre cette hiérarchie évite 90 % de la confusion des débutants.

- **Une session** regroupe tout le reste. C'est l'unité que tu détaches et rattaches. Une session par projet ou par serveur, c'est la pratique la plus saine.
- **Une fenêtre** vit dans une session, comme un onglet de navigateur. Tu peux en ouvrir autant que tu veux et basculer entre elles.
- **Un panneau** découpe une fenêtre en plusieurs zones de terminal côte à côte. Pratique pour surveiller des logs à gauche pendant que tu tapes des commandes à droite.

Démarre une première session nommée :

```bash
tmux new -s deploiement
```

Tu es dedans. Tape ta commande habituelle, lance un build, ce que tu veux. Pour te détacher sans rien tuer, le préfixe entre en jeu : `Ctrl-b` puis `d`. Tu retombes dans ton shell normal, et la session continue de tourner en arrière-plan sur la machine.

Pour la retrouver plus tard, depuis le même serveur :

```bash
tmux attach -t deploiement
```

Et si tu as oublié le nom ou que tu en as plusieurs qui tournent :

```bash
tmux ls
```

⚠️ Un piège classique : lancer tmux à l'intérieur d'une session tmux déjà ouverte, par exemple en te connectant en SSH vers un autre serveur depuis une session tmux locale qui tourne déjà. Le préfixe `Ctrl-b` ne sait plus à quelle couche s'adresser. La solution propre : donne un préfixe différent à l'une des deux instances, ou appuie deux fois sur `Ctrl-b` pour viser la couche la plus interne.

## Les raccourcis essentiels à connaître par cœur

Tout raccourci tmux commence par le préfixe, relâché, puis suivi d'une touche. Voici ceux que j'utilise vraiment, tous les jours, sans réfléchir :

| Raccourci | Action |
|---|---|
| `Ctrl-b d` | Détacher la session en cours |
| `Ctrl-b c` | Créer une nouvelle fenêtre |
| `Ctrl-b n` / `Ctrl-b p` | Fenêtre suivante / précédente |
| `Ctrl-b %` | Diviser le panneau verticalement |
| `Ctrl-b "` | Diviser le panneau horizontalement |
| `Ctrl-b flèche` | Se déplacer entre les panneaux |
| `Ctrl-b z` | Zoomer sur le panneau actif (plein écran temporaire) |
| `Ctrl-b x` | Fermer le panneau actif (avec confirmation) |
| `Ctrl-b [` | Entrer en mode copie (défilement et sélection) |
| `Ctrl-b ,` | Renommer la fenêtre active |

Le mode copie mérite un mot à part. Une fois dedans (`Ctrl-b [`), tu navigues avec les flèches ou les touches vi si tu les as activées, tu marques le début de la sélection avec `Espace`, la fin avec `Entrée`, et le texte part dans le presse-papiers interne de tmux. Pour le ressortir ailleurs dans un panneau : `Ctrl-b ]`.

💡 Astuce qui change la vie : renomme systématiquement tes fenêtres (`Ctrl-b ,`) avec le nom du service ou de la tâche en cours. Après trois jours avec dix fenêtres ouvertes appelées `bash`, `bash`, `bash`, tu me remercieras.

## Configurer tmux : ton fichier .tmux.conf

La configuration par défaut est fonctionnelle mais austère. Un fichier `~/.tmux.conf` suffit à la rendre confortable. Voici ma base, celle que je recopie sur chaque nouveau serveur :

```bash
# Remappe le préfixe sur Ctrl-a, moins loin des autres touches courantes
unbind C-b
set -g prefix C-a
bind C-a send-prefix

# Active la souris : clic pour changer de panneau, molette pour défiler
set -g mouse on

# Mode vi dans le copier-coller
setw -g mode-keys vi

# Numérotation des fenêtres à partir de 1, plus lisible sur le clavier
set -g base-index 1
setw -g pane-base-index 1

# Historique de défilement plus généreux
set -g history-limit 10000

# Barre de statut minimale : nom de session, heure, charge
set -g status-left "#[fg=green]#S "
set -g status-right "#[fg=yellow]%H:%M %d-%b-%y"

# Rafraîchir la config sans relancer le serveur tmux
bind r source-file ~/.tmux.conf \; display "Config rechargée"
```

Après modification, recharge sans quitter ta session en cours avec `Ctrl-a r` (ou `Ctrl-b r` si tu n'as pas remappé le préfixe).

Le mode vi en copie vaut le coup même si tu n'es pas un adepte de vi au quotidien : navigation au clavier pur, pas de souris nécessaire pour sélectionner un bloc de logs sur un serveur distant lent. Si tu veux pousser l'intégration terminal-éditeur plus loin, j'ai un guide pour [installer un thème Vim avec vim-plug](/installation-theme-vim-guide/) qui complète bien ce genre de setup clavier.

✅ Pour aller plus loin, le gestionnaire de plugins TPM (Tmux Plugin Manager) ajoute des extensions comme la sauvegarde automatique de session (`tmux-resurrect`) qui restaure toutes tes fenêtres après un reboot du serveur. Pas indispensable pour débuter, très confortable une fois que tu as adopté tmux au quotidien.

## Détacher une session et la retrouver après une coupure SSH

C'est la fonctionnalité qui justifie tout l'article. Sans tmux, une déconnexion SSH tue le processus parent et tout ce qu'il a lancé, sauf si tu as pensé à `nohup` ou `disown` avant coup, ce que personne ne fait systématiquement. Avec tmux, la question ne se pose plus.

Le flux de travail concret :

```bash
ssh admin@serveur.exemple.com
tmux new -s migration
# tu lances ta tâche longue, un rsync, un dump de base, un build
```

Ta connexion coupe. Peu importe la raison : wifi, VPN qui se recycle, laptop qui se met en veille. Le serveur, lui, s'en fiche. Ton processus continue. Tu te reconnectes :

```bash
ssh admin@serveur.exemple.com
tmux attach -t migration
```

Et tu retombes exactement où tu étais, avec le même historique de terminal affiché. Ça marche aussi très bien pendant une intervention en [mode secours après un problème de montage RAID](/depannage-montage-partition-raid-linux-mode-secours/) : tu lances les commandes `mdadm` longues dans une session tmux dédiée, et si ta liaison série ou ta console à distance a un hoquet, rien n'est perdu.

Un détail qui surprend souvent : `tmux attach` sans argument se rattache à la dernière session active si tu n'en as qu'une. Pratique pour aller plus vite, risqué si tu en as plusieurs et que tu tapes trop rapidement. Prends l'habitude de nommer tes sessions avec `-s`, ça évite de se rattacher à la mauvaise par réflexe.

## Cas pratiques et pièges classiques

Au quotidien, tmux sert à bien plus qu'éviter les coupures SSH. Quelques usages réels, pris dans mon propre setup :

**Surveillance pendant une opération lourde** : un panneau avec `htop`, un autre avec `tail -f` sur le log applicatif, un troisième pour taper tes commandes. Si tu soupçonnes que la swap commence à chauffer pendant l'opération, mon [guide sur la configuration et l'optimisation de la swap Linux](/guide-swap-linux-configuration-optimisation/) explique comment lire les bons compteurs au bon moment, directement dans un de ces panneaux.

**Sessions persistantes pour des outils d'administration web** : si tu gères un serveur avec [Cockpit pour l'administration Docker](/cockpit-docker-interface-web-administration/), garder un terminal tmux ouvert à côté du navigateur te permet de croiser les deux vues sans jamais perdre le contexte shell quand tu bascules entre les deux.

**Pair-debugging** : deux admins, même machine, même session tmux, chacun voit ce que l'autre tape en temps réel. Beaucoup plus direct qu'un partage d'écran pour du dépannage shell pur.

Les pièges qui reviennent le plus souvent :

- **Le copier-coller qui n'embarque pas les bons caractères** : sans `set -g mouse on`, une sélection à la souris copie dans le presse-papiers du terminal hôte, pas dans tmux. Les deux presse-papiers coexistent et ça crée de la confusion si tu ne sais pas lequel utiliser.
- **Les touches de fonction qui ne passent pas** : certains émulateurs de terminal interceptent des combinaisons avant qu'elles n'arrivent à tmux. Si un raccourci reste muet, teste-le dans un autre terminal avant de soupçonner ta config.
- **Oublier qu'une session détachée continue de consommer des ressources** : un processus oublié dans une fenêtre tmux abandonnée depuis trois mois, ça arrive. `tmux ls` de temps en temps sur un serveur partagé évite les mauvaises surprises.
- **Confondre `kill-session` et `kill-server`** : le premier ferme une session précise, le second coupe absolument tout ce qui tourne sous tmux sur la machine, toutes sessions confondues. Vérifie toujours le nom avant de valider.

La vraie question c'est de savoir si tmux doit remplacer `screen`, ton vieux réflexe d'admin système, ou les alternatives plus récentes comme Zellij. Dans les faits, tmux reste le choix par défaut sur la quasi-totalité des serveurs que tu croiseras chez un client ou un hébergeur, ce qui en fait aussi le plus rentable à apprendre : tu le retrouveras partout, préinstallé ou à une commande `apt install` de distance.

## Conclusion

Tmux ne fait qu'une chose : garder tes terminaux vivants, détachables, retrouvables. Mais cette seule chose change vraiment la façon de travailler en SSH, dès que tu dépasses la commande rapide de trente secondes. Vingt minutes pour apprendre le préfixe, les panneaux et un `.tmux.conf` minimal, et tu ne reviendras plus jamais à un terminal nu sur un serveur distant. Installe-le sur ton prochain serveur avant même d'y lancer quoi que ce soit, ça deviendra vite un réflexe comme un autre.
