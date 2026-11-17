---
title: "Gitleaks : scanner les secrets oubliés dans tes dépôts Git"
description: "Gitleaks scanne l'historique de tes dépôts Git pour détecter les secrets oubliés : clés API, tokens et mots de passe, avant qu'une fuite n'arrive."
pubDatetime: "2026-11-17T11:01:54+01:00"
modDatetime: "2026-11-16T08:00:00.000Z"
author: Brandon
tags:
  - securite
  - git
  - ci-cd
  - intermediaire
featured: false
draft: false
focusKeyword: gitleaks
faqs:
  - question: "Un secret détecté par Gitleaks a déjà été poussé sur GitHub, que faire ?"
    answer: "Supprimer le fichier ne suffit pas, le secret reste dans l'historique git. Révoque la clé chez le fournisseur en priorité, puis réécris l'historique avec git filter-repo si besoin."
  - question: "Gitleaks va-t-il disparaître puisque le projet est feature complete ?"
    answer: "Non, les correctifs de sécurité continuent et trois co-mainteneurs communautaires assurent le suivi. Les nouvelles fonctionnalités, elles, partent vers Betterleaks, le projet successeur."
  - question: "Le hook pre-commit Gitleaks ralentit-il mes commits ?"
    answer: "Non, il ne scanne que le diff en attente, ça prend quelques millisecondes à quelques secondes selon la taille. Tu peux le sauter ponctuellement avec SKIP=gitleaks."
---
> 💡 **TL;DR**
> - Gitleaks scanne l'historique complet d'un dépôt git et détecte les secrets oubliés : clés API, tokens, mots de passe en clair dans un commit vieux de trois ans
> - Installation en une commande via Homebrew ou Docker, aucun compte ni inscription requise, licence MIT
> - S'intègre en hook pre-commit pour bloquer un secret avant qu'il parte, et en CI/CD via Gitleaks-Action pour rattraper ce qui passe malgré tout

## Gitleaks : le scanner qui retrouve les secrets planqués dans ton historique git

Tu push, tu respires. Et trois semaines plus tard tu réalises que le commit de "fix rapide" contenait la clé API de production en dur, parce que t'étais fatigué un vendredi soir et que tu as oublié de la sortir du code avant de committer. Le pire, c'est que supprimer le fichier au commit suivant ne change rien : le secret reste accessible pour quiconque clone le dépôt et remonte l'historique.

Gitleaks règle ce problème précis. Tu lui donnes un dépôt, il parcourt chaque commit, chaque branche, chaque diff, et il te sort la liste des secrets qui ressemblent à une clé API, un token AWS, une clé privée SSH ou un mot de passe en clair. Pas d'agent à installer sur un serveur distant, pas de tableau de bord SaaS à configurer, pas de compte à créer. Un binaire, une commande, un résultat lisible.

Chez moi, c'est passé de "truc que je lance de temps en temps par curiosité" à "étape obligatoire avant tout push" le jour où j'ai retrouvé un token d'API météo planqué dans un commit d'il y a huit mois, sur un dépôt que je croyais propre. Gitleaks l'a trouvé en moins de deux secondes.

## Table des matières

## Gitleaks, c'est quoi exactement

Gitleaks est un scanner de secrets open source, distribué sous licence MIT. Le projet a été créé par Zach Rice et vit aujourd'hui sous l'organisation GitHub `gitleaks`, maintenue par Truffle Security, la société derrière TruffleHog.

Il faut le dire clairement parce que ça change la façon dont tu dois regarder le projet : depuis le 21 mai 2026, le README de Gitleaks annonce que l'outil est "feature complete". Autrement dit, aucune nouvelle fonctionnalité n'arrivera, seulement des correctifs de sécurité. Zach Rice a quitté Truffle Security pour Aikido Security, où il développe désormais Betterleaks, le successeur pensé avec les leçons tirées de plusieurs années de maintenance de Gitleaks. Trois contributeurs de longue date (Richard Gomez, Braxton Plaxco et Ahrav Dutta) ont pris le relais comme co-mainteneurs pour que le projet continue de recevoir des patches.

Ça ne rend pas Gitleaks obsolète pour autant. C'est toujours l'outil le plus déployé de sa catégorie, avec une intégration pre-commit mature et une GitHub Action officielle, et la base de règles de détection existante couvre déjà l'immense majorité des fournisseurs courants (AWS, GCP, Stripe, Slack, GitHub lui-même). Mais si tu démarres un projet de scan de secrets aujourd'hui, garde un œil sur Betterleaks : c'est là que vont les futures améliorations de détection.

Concrètement, Gitleaks repose sur des règles regex et sur un calcul d'entropie pour repérer ce qui ressemble à un secret, même sans règle dédiée au fournisseur exact. Il couvre trois modes de scan :

- **`git`** : analyse l'historique complet d'un dépôt via `git log -p`, commit par commit
- **`dir`** (alias `files`) : analyse des fichiers ou un répertoire, sans tenir compte de git
- **`stdin`** : analyse un flux, pratique pour brancher Gitleaks sur une autre commande

## Installer Gitleaks : Homebrew, Docker, binaire

Trois façons d'installer Gitleaks selon ton système, aucune ne demande de compte.

Sur macOS ou Linux avec Homebrew, j'ai un guide complet sur [comment installer Homebrew sur macOS](/installation-homebrew-macos/) si tu n'as pas encore franchi le pas :

```bash
brew install gitleaks
```

Sans gestionnaire de paquets, récupère le binaire précompilé correspondant à ton système depuis la page des releases du dépôt officiel et place-le dans ton `PATH` :

```bash
mv gitleaks /usr/local/bin/
chmod +x /usr/local/bin/gitleaks
```

Et si tu préfères ne rien installer sur l'hôte, l'image officielle fait le travail, avec ton dépôt monté en volume :

```bash
docker run -v $(pwd):/repo zricethezav/gitleaks:latest git /repo
```

Pour builder depuis les sources, il faut Go et `make` :

```bash
git clone https://github.com/gitleaks/gitleaks.git
cd gitleaks
make build
```

## Scanner un dépôt avec Gitleaks : les commandes essentielles

La commande de base, lancée depuis la racine de ton dépôt :

```bash
gitleaks git -v
```

Le `-v` affiche la sortie détaillée : fichier, ligne, règle déclenchée, et le secret partiellement redacté par défaut. Sans argument de chemin, Gitleaks scanne le répertoire courant.

Pour analyser un répertoire de fichiers sans tenir compte de l'historique git, par exemple avant d'archiver un projet :

```bash
gitleaks dir ./mon-projet
```

Exporter le résultat en JSON pour l'exploiter ailleurs (ticket automatique, archivage, dashboard maison) :

```bash
gitleaks git --report-format json --report-path resultats.json
```

Masquer complètement le secret dans la sortie affichée, utile si tu partages le résultat avec quelqu'un d'autre sans lui donner accès au secret lui-même :

```bash
gitleaks git --redact
```

Et pour ne revérifier que ce qui est nouveau depuis un scan précédent, en ignorant les résultats déjà connus et traités :

```bash
gitleaks git --baseline-path ancien-rapport.json --report-path nouveau-rapport.json
```

✅ Astuce homelab : lance un premier scan complet sans filtre sur tes vieux dépôts perso, même ceux que tu crois propres. C'est souvent sur les projets de trois ou quatre ans que traînent les secrets les plus oubliés, du token d'API météo au mot de passe de base de données de test.

## Configurer les règles, les allowlists et les faux positifs

La configuration par défaut de Gitleaks couvre déjà une bonne centaine de règles pour les fournisseurs courants. Mais tu vas forcément tomber sur des faux positifs : une chaîne de test qui ressemble à une clé API, un exemple de documentation avec un token factice.

Un fichier `.gitleaks.toml` à la racine du dépôt te permet d'étendre ou de restreindre ce comportement :

```toml
[extend]
useDefault = true

[[rules.allowlists]]
targetRules = ["generic-api-key"]
regexes = ['''EXEMPLE_[A-Z0-9]+''']

[[allowlists]]
paths = ['''.*_test\.go$''']
```

Le bloc `[extend]` avec `useDefault = true` hérite de la configuration intégrée au lieu de repartir de zéro. Les blocs `[[rules.allowlists]]` ciblent une règle précise, alors que `[[allowlists]]` s'applique globalement, par exemple pour exclure tout un répertoire de tests.

Pour ignorer un secret précis déjà identifié sans toucher à la configuration globale, Gitleaks propose un fichier `.gitleaksignore` à la racine du dépôt. Chaque ligne correspond à l'empreinte (fingerprint) unique d'une détection, visible dans le rapport de scan :

```
3c3b3e1f8e9b2a1e4d:config/settings.py:generic-api-key:42
```

⚠️ Cette fonctionnalité reste marquée expérimentale dans la documentation officielle. Préfère l'allowlist dans `.gitleaks.toml` pour un cas récurrent, et réserve `.gitleaksignore` aux exceptions ponctuelles.

## Bloquer les secrets avant le commit et en CI/CD

Un scan manuel de temps en temps, c'est bien. Bloquer le secret avant qu'il ne quitte ta machine, c'est mieux. Gitleaks s'intègre nativement avec le framework pre-commit :

```yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.30.1
    hooks:
      - id: gitleaks
```

Installe ensuite le hook une fois pour toutes dans le dépôt :

```bash
pre-commit install
```

À partir de là, chaque `git commit` lance Gitleaks sur le diff en attente. S'il trouve un secret, le commit échoue et tu dois corriger avant de recommencer. Pour sauter le hook ponctuellement (un cas rare, un faux positif urgent à committer), préfixe la commande :

```bash
SKIP=gitleaks git commit -m "fix urgent"
```

Le hook local attrape l'essentiel, mais il ne protège que ta machine. Si un collègue committe sans l'avoir installé, ou pousse directement depuis une autre machine, rien ne l'arrête. C'est là que la CI/CD devient le filet de sécurité qui rattrape tout le monde.

Gitleaks sort par défaut avec le code 1 dès qu'il trouve une fuite, ce qui fait déjà échouer un job classique. L'action officielle `gitleaks/gitleaks-action` simplifie encore l'intégration sur GitHub :

```yaml
name: gitleaks
on: [push, pull_request]
jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
        with:
          fetch-depth: 0
      - uses: gitleaks/gitleaks-action@v3
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

Le `fetch-depth: 0` récupère tout l'historique git, indispensable sinon l'action ne voit que le dernier commit. Pour un dépôt sous un compte d'organisation, il faut en plus une licence gratuite ("Free Organization License Key", obtenue via le site officiel) passée en variable `GITLEAKS_LICENSE`. Les dépôts sous compte personnel n'en ont pas besoin.

## Gitleaks dans ta défense en profondeur

Gitleaks traite un problème précis : les secrets déjà écrits dans ton code, à un instant donné de l'historique. Il ne remplace aucune des autres couches de sécurité, il les complète.

Une fois le secret trouvé et révoqué, encore faut-il le partager correctement avec les personnes qui en ont besoin, sans repasser par Slack ou un fichier texte. Un outil comme ceux comparés dans [Partager un mot de passe sécurisé : 3 outils comparés](/partager-mot-de-passe-securise-comparatif/) évite de recréer le même problème ailleurs.

Côté réseau, Gitleaks ne voit rien de ce qui circule après coup. Pour la détection d'intrusion en continu sur ton infra, [Suricata en Docker](/suricata-docker-ids-ips-reseau/) surveille le trafic, là où Gitleaks s'arrête au code source avant déploiement. Et pour un audit plus large de la posture de sécurité d'une machine Linux, au-delà du simple code, [Lynis en Docker](/lynis-docker-audit-securite-linux/) complète le tableau en vérifiant la configuration système elle-même.

Aucun de ces outils ne se substitue aux autres. Gitleaks répond à "qu'est-ce qui traîne dans mon code". Les autres répondent à "qu'est-ce qui se passe sur mon réseau" ou "ma machine est-elle correctement durcie".

Gitleaks a ses limites, et il vaut mieux les connaître avant de lui faire une confiance aveugle. Il ne détecte que ce qui ressemble à un secret connu : une clé générée dans un format exotique peut lui échapper complètement. Les faux positifs existent, surtout sur du code généré ou des fixtures de test, d'où l'intérêt des allowlists. Et puisque le projet est feature complete, les nouveaux formats de secrets qui apparaîtront avec de nouveaux fournisseurs auront plus de chances d'être couverts d'abord par Betterleaks que par une mise à jour de règles côté Gitleaks.

## Conclusion

Gitleaks fait une chose précise et la fait bien depuis des années : fouiller ton historique git pour retrouver ce que tout le monde a oublié d'y laisser. Gratuit, sans inscription, une commande à taper, un hook pre-commit qui bloque le problème à la source et une action CI qui rattrape ce qui passe malgré tout.

Le statut "feature complete" du projet n'est pas une raison de l'ignorer, c'est juste un détail à garder en tête pour la suite : les patches de sécurité continuent, l'outil reste fiable aujourd'hui, mais si tu démarres un chantier neuf sur la détection de secrets dans deux ou trois ans, regarde où en est Betterleaks. En attendant, installe Gitleaks, lance un scan complet sur ton dépôt le plus ancien, et prépare-toi à être surpris de ce qui traîne parfois depuis des années sans que personne ne l'ait jamais vu.
