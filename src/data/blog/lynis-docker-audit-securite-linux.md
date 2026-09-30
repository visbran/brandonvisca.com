---
title: "Lynis Docker : audit de sécurité automatisé pour Linux"
description: "Audite ton serveur avec Lynis Docker : scan système en conteneur, audit de Dockerfile, hardening index et automatisation, sans rien installer sur l'hôte."
pubDatetime: "2026-09-30T11:02:11+02:00"
modDatetime: "2026-09-29T08:00:00.000Z"
author: Brandon
tags:
  - securite
  - docker
  - hardening
  - ssh
  - intermediaire
featured: false
draft: false
focusKeyword: lynis docker
faqs:
  - question: "Lynis peut-il modifier ou casser la config de mon serveur pendant l'audit ?"
    answer: "Non, Lynis est en lecture seule : il lit les fichiers de config, les binaires et les processus pour générer des suggestions, sans jamais appliquer de correction lui-même."
  - question: "Faut-il lancer Lynis avec les droits root ?"
    answer: "En root, il accède aux modules noyau, aux comptes système et aux crontabs. Sans root, le scan tourne quand même mais une partie des tests passe en skipped faute de permissions."
  - question: "Un scan Lynis lancé depuis un conteneur voit-il vraiment tout l'hôte ?"
    answer: "Pas entièrement. Sans partage du namespace PID et sans montage du système de fichiers hôte en lecture seule, certains tests réseau et processus restent partiels."
---
> 💡 **TL;DR**
> - Lynis audite ton système Linux et calcule un hardening index, sans rien installer en dur sur l'hôte grâce à un conteneur jetable.
> - `lynis audit dockerfile` vérifie tes Dockerfile avant build : `USER` manquant, `ADD` au lieu de `COPY`, absence de `HEALTHCHECK`.
> - Le rapport sort dans `/var/log/lynis-report.dat`, avec une liste de suggestions numérotées à corriger une par une.

Lynis, c'est l'outil que je lance en premier sur n'importe quel serveur Linux que je viens de monter. Pas pour remplacer un pentest, mais pour repérer en cinq minutes les trucs bêtes : SSH mal configuré, permissions de fichiers trop larges, services qui traînent, mots de passe sans politique. Développé par CISOfy, gratuit et open source, il tourne depuis des années sur des milliers de serveurs et de containers CI.

Le souci classique : installer Lynis directement sur l'hôte, c'est un paquet de plus, une dépendance git de plus, un truc à mettre à jour à la main. Avec Lynis Docker, tu lances le scan depuis un conteneur jetable, tu récupères le rapport, et tu supprimes le conteneur derrière. Zéro trace, zéro paquet qui traîne. C'est ce workflow Lynis Docker que je détaille ici, plus l'audit de Dockerfile, qui est une fonctionnalité native de l'outil et clairement sous-utilisée.

## Table des matières

## Lynis Docker : ce que l'outil vérifie et ce qu'il ne fait pas

Le combo Lynis Docker recouvre en réalité deux usages différents qu'on mélange souvent :

1. **Auditer ton hôte** en lançant Lynis depuis un conteneur, pour ne rien installer en dur.
2. **Auditer un Dockerfile** avec la commande native `lynis audit dockerfile`, avant même de construire l'image.

Dans les deux cas, Lynis ne corrige rien tout seul. Il scanne, compare à des centaines de tests (plus de 300 dans les versions récentes), et sort une liste de suggestions classées par catégorie : authentification, réseau, logging, malware, stockage. Chaque suggestion a un identifiant du style `SSH-7408` que tu peux chercher directement dans la documentation CISOfy pour comprendre le pourquoi.

Ce qu'il ne fait pas : il ne scanne pas les vulnérabilités CVE des paquets installés en profondeur comme le ferait un scanner dédié, et il ne remplace pas un audit réseau externe. Pense-le comme un check-up de config, pas comme un scanner de vulnérabilités.

La version actuelle du projet est la 3.1.7, disponible sur le dépôt GitHub officiel `CISOfy/lynis`. La licence communautaire reste gratuite et complète pour l'essentiel des tests. CISOfy vend en plus une offre Lynis Enterprise avec rapports centralisés et scripts de remédiation, mais rien ne t'oblige à y passer pour un homelab ou un petit parc de serveurs.

## Auditer ton hôte avec Lynis Docker sans rien installer dessus

La méthode documentée par CISOfy elle-même repose sur une image Alpine minimaliste, dans laquelle tu clones le dépôt à chaque exécution. Pas d'image Docker officielle prête à l'emploi côté CISOfy, donc on construit ce workflow Lynis Docker soi-même, ce qui a l'avantage de toujours tirer la dernière version du dépôt.

Lance un conteneur Alpine temporaire :

```bash
mkdir -p lynis-report

docker run --rm -it \
  -v "$(pwd)/lynis-report:/lynis-report" \
  --pid=host \
  alpine:3.20 sh
```

Le flag `--pid=host` partage le namespace des processus de l'hôte avec le conteneur. Sans ça, Lynis ne voit que les process du conteneur lui-même, et une bonne partie des tests liés aux services actifs tombent en `skipped`.

Une fois dans le shell du conteneur, installe git et clone Lynis :

```sh
apk update && apk add git

git clone --depth 1 https://github.com/CISOfy/lynis
cd lynis

LANG=en LANGUAGE=en ./lynis audit system --no-colors \
  --logfile /lynis-report/lynis.log \
  --report-file /lynis-report/lynis-report.dat
```

Les variables `LANG` et `LANGUAGE` évitent des soucis d'encodage sur une base Alpine sans locale configurée. `--no-colors` rend la sortie lisible quand tu rediriges vers un fichier plutôt que vers un terminal.

⚠️ Ce montage ne donne pas une vision complète de l'hôte. Pour un audit poussé du système de fichiers (permissions, fichiers SUID, configs sous `/etc`), monte aussi la racine de l'hôte en lecture seule :

```bash
docker run --rm -it \
  -v "$(pwd)/lynis-report:/lynis-report" \
  -v /:/hostfs:ro \
  --pid=host \
  alpine:3.20 sh
```

Lynis détecte alors qu'il tourne dans un environnement conteneurisé et adapte certains tests, mais l'essentiel des vérifications sur `/hostfs` reste exploitable. C'est plus verbeux à mettre en place qu'un scan natif, mais ça évite de polluer l'hôte avec un paquet supplémentaire.

Une fois le scan terminé, quitte le conteneur avec `exit`. Le dossier `lynis-report/` sur ton hôte contient les deux fichiers, consultables sans rouvrir de conteneur.

## Auditer un Dockerfile avec Lynis Docker

C'est la partie la moins connue de Lynis Docker, et pourtant native. `lynis audit dockerfile` analyse un Dockerfile ligne par ligne et pointe les mauvaises pratiques avant même que tu lances un `docker build`.

Depuis le dossier cloné à l'étape précédente :

```sh
./lynis audit dockerfile /lynis-report/Dockerfile
```

Monte ton Dockerfile dans le conteneur d'audit avec un volume supplémentaire (`-v $(pwd)/Dockerfile:/lynis-report/Dockerfile:ro`) avant de lancer la commande. Lynis relève typiquement :

- L'absence d'instruction `USER` : ton conteneur tourne en root par défaut, ce qui élargit la surface d'attaque si le process principal est compromis.
- `ADD` utilisé là où `COPY` suffirait : `ADD` télécharge des URL et décompresse des archives automatiquement, deux comportements qu'on ne veut pas dans un build reproductible.
- Pas de `HEALTHCHECK` défini, ce qui empêche Docker et les orchestrateurs de détecter un conteneur bloqué mais toujours en vie.
- Des secrets potentiels copiés en dur dans une couche de l'image, visibles ensuite avec `docker history`.

Corrige un point à la fois, relance l'audit, et versionne ton Dockerfile corrigé. C'est un des rares contrôles de sécurité qui s'intègre proprement dans une CI, avant même que l'image existe.

## Lire le rapport et le hardening index

Le fichier `/lynis-report/lynis-report.dat` est un simple fichier clé=valeur, facile à parser en ligne de commande. Pour sortir rapidement les points d'amélioration :

```bash
grep "^suggestion" lynis-report/lynis-report.dat
```

Chaque ligne ressemble à ça :

```
suggestion[]=SSH-7408|Consider hardening SSH configuration|-|-|
```

Le champ après l'identifiant est une description courte. Cherche l'identifiant (ici `SSH-7408`) dans la documentation CISOfy pour la correction détaillée. Le score global, le hardening index, est sur une échelle de 0 à 100 :

```bash
grep "hardening_index" lynis-report/lynis-report.dat
```

Un serveur fraîchement installé tourne souvent entre 55 et 65. Après un premier passage de corrections (SSH, comptes, mots de passe, permissions), 75-80 est un objectif réaliste sans y passer des heures. Au-delà, chaque point demande de plus en plus de travail pour un gain de sécurité de plus en plus marginal, ne cours pas après le 100.

La plupart des suggestions réseau et pare-feu que Lynis remonte se corrigent directement avec [nftables](/nftables-docker-pare-feu-linux/) si tu veux du filtrage moderne par table, ou avec un [pare-feu UFW](/ufw-docker-pare-feu-linux/) si tu préfères une syntaxe plus simple devant tes conteneurs.

## Automatiser le scan Lynis Docker avec un cron

Lancer Lynis Docker à la main de temps en temps, c'est bien. L'automatiser en cron, c'est mieux : tu vois l'évolution du hardening index dans le temps, et tu attrapes une régression avant qu'elle traîne trop longtemps.

Crée un script `run-lynis-audit.sh` sur ton hôte :

```bash
#!/bin/bash
set -euo pipefail

REPORT_DIR="/opt/lynis-reports/$(date +%Y%m%d)"
mkdir -p "${REPORT_DIR}"

docker run --rm \
  -v "${REPORT_DIR}:/lynis-report" \
  -v /:/hostfs:ro \
  --pid=host \
  alpine:3.20 sh -c "
    apk add --no-cache git >/dev/null
    git clone --depth 1 https://github.com/CISOfy/lynis /tmp/lynis
    cd /tmp/lynis
    LANG=en LANGUAGE=en ./lynis audit system --no-colors \
      --logfile /lynis-report/lynis.log \
      --report-file /lynis-report/lynis-report.dat
  "

echo "Rapport disponible dans ${REPORT_DIR}"
```

Ajoute-le à ton crontab pour un passage hebdomadaire :

```bash
0 4 * * 1 /opt/lynis-reports/run-lynis-audit.sh >> /var/log/lynis-cron.log 2>&1
```

Si Lynis remonte des tentatives de connexion SSH suspectes dans ses logs, couple-le avec [Fail2Ban](/fail2ban-docker-securite-serveur/) pour bannir automatiquement les IP fautives, plutôt que de les traiter manuellement après coup. Et si tu débutes sur le sujet, mon [guide des 10 commandes de hardening Linux](/hardening-linux-10-commandes/) couvre les corrections les plus fréquentes que Lynis va te suggérer dès le premier scan.

## Lynis Docker face à Trivy : deux outils complémentaires, pas concurrents

Question qui revient souvent quand on parle de Lynis Docker : pourquoi pas juste Trivy ? Réponse courte : ce ne sont pas les mêmes couches.

- **Lynis** audite la configuration du système : SSH, comptes, permissions, logging, services actifs, et maintenant les Dockerfile.
- **[Trivy](/trivy-docker-scanner-vulnerabilites/)** scanne les vulnérabilités connues (CVE) dans les paquets d'une image ou d'un système de fichiers, avec une base de données mise à jour en continu.

Les deux sont complémentaires dans un pipeline sérieux : Trivy sur chaque image avant push vers ton registre, Lynis sur l'hôte et sur les Dockerfile en amont du build. L'un attrape les paquets vulnérables, l'autre attrape les erreurs de configuration qu'aucune base CVE ne référencera jamais.

## Dépannage des erreurs courantes avec Lynis Docker

**"Could not create temporary directory"** : le conteneur tourne avec un utilisateur sans droit d'écriture sur `/tmp`. Sur l'image Alpine du tutoriel, tu es root par défaut, donc ce message signale plutôt un volume monté en lecture seule qui inclut `/tmp` par erreur. Vérifie tes montages `-v`.

**Beaucoup de tests en "skipped"** : normal si tu n'as pas partagé `--pid=host` ni monté `/` en lecture seule. Lynis adapte son comportement à ce qu'il voit, et dans un conteneur isolé par défaut, il ne voit pas grand-chose de l'hôte.

**`apk add git` échoue avec un timeout** : le miroir Alpine par défaut est parfois lent depuis certains réseaux. Ajoute `--repository` avec un miroir plus proche, ou relance simplement la commande.

**Le hardening index ne bouge pas après des corrections** : relis le rapport précédent avant de corriger, certaines suggestions demandent un redémarrage de service (`sshd`, `auditd`) pour être prises en compte au scan suivant.

## Conclusion

Lynis Docker, c'est un scan jetable qui ne laisse rien derrière lui sur ton hôte, plus un audit de Dockerfile qui rattrape les erreurs avant le build. Ni l'un ni l'autre ne remplace un vrai audit de sécurité mené par un humain qui connaît ton infra, mais les deux attrapent la majorité des erreurs de configuration évidentes en quelques minutes, gratuitement.

Lance Lynis Docker une première fois pour avoir ta baseline, corrige les suggestions SSH et réseau en priorité, puis mets le scan en cron pour suivre l'évolution du hardening index dans le temps. C'est un des rares outils de sécurité où le rapport effort/bénéfice reste excellent même pour un homelab d'une seule machine.
