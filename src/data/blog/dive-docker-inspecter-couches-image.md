---
title: "Dive Docker : inspecter les couches d'une image"
description: "Dive Docker analyse chaque couche d'une image, calcule son score d'efficacité et traque le gaspillage. Installation, usage CLI et intégration CI."
pubDatetime: "2026-11-23T11:00:54+01:00"
modDatetime: "2026-11-22T08:00:00.000Z"
author: Brandon
tags:
  - docker
  - ci-cd
  - guide
  - intermediaire
featured: false
draft: false
focusKeyword: dive docker
faqs:
  - question: "Dive docker fonctionne-t-il uniquement avec Docker ?"
    answer: "Non, dive docker peut aussi lire des images via Podman ou containerd grâce à l'option --source. Le nom vient de son usage historique, pas d'une dépendance stricte à Docker."
  - question: "Dive docker modifie-t-il l'image que j'analyse ?"
    answer: "Non, dive docker ouvre l'image en lecture seule. Il extrait les couches dans un répertoire temporaire pour les comparer, sans toucher à l'image source ni au registre."
  - question: "Comment utiliser dive docker sans interface interactive, par exemple en CI ?"
    answer: "Lance la commande avec la variable CI=true devant. Dive docker analyse l'image puis renvoie un code de sortie selon les seuils définis dans un fichier .dive-ci, sans ouvrir le TUI."
---
> 💡 **TL;DR**
> - Dive docker ouvre chaque couche d'une image Docker et calcule un score d'efficacité pour repérer ce qui gaspille de l'espace
> - Installation en une commande via Homebrew, apt ou le binaire officiel, gratuit et open source sous licence MIT
> - S'utilise en interactif avec un TUI ou en mode silencieux via `CI=true` pour bloquer un build qui dérape

## Dive docker : le scalpel pour fouiller tes images

Tu buildes une image, elle pèse 1,8 Go alors que ton code fait 40 Mo. Tu sais qu'il y a du gras quelque part, un cache apt mal nettoyé, une couche de build qui traîne, un `COPY .` trop large qui embarque ton `.git`. Mais sans outil, tu optimises à l'aveugle, tu changes deux lignes du Dockerfile, tu rebuild, tu croises les doigts.

Dive docker règle ce problème précis. Tu lui donnes le nom d'une image, il te montre chaque couche une par une, ce qu'elle ajoute, ce qu'elle supprime, et ce qui reste inutilement dupliqué entre deux couches. Chez moi c'est devenu un réflexe avant de pousser une image vers mon registre perso, deux minutes d'inspection contre des mois à trainer une image deux fois trop grosse sans jamais savoir pourquoi.

## Table des matières

## Dive, l'outil qui inspecte tes images

Dive est développé par wagoodman, publié sous licence MIT, donc gratuit et avec le code source ouvert. Il n'a rien d'officiel ni de natif à Docker : c'est un outil tiers en ligne de commande, écrit en Go, qui se greffe sur le daemon Docker (ou Podman, ou containerd) pour lire le contenu d'une image sans jamais la modifier.

La dernière version stable est la 0.13.1. Le projet n'enchaîne pas les releases à un rythme effréné, mais il reste actif : les commits et les corrections de bugs continuent sur le dépôt GitHub, notamment autour de la compatibilité avec les versions récentes de Docker. Ce n'est pas un projet mort, juste un projet mature qui ne casse rien à chaque mise à jour.

Concrètement, il fait deux choses :

- **Il affiche le contenu de chaque couche** : fichiers ajoutés, modifiés, supprimés, avec leur taille exacte
- **Il calcule un score d'efficacité** : la part de l'image qui n'est pas du gaspillage dû à des fichiers dupliqués ou effacés plus tard

Le détail qui compte : dans une image Docker, chaque instruction `RUN`, `COPY` ou `ADD` crée une couche. Si tu installes un paquet dans une couche puis que tu le supprimes dans la couche suivante, le poids du paquet reste dans l'image finale. Les couches s'empilent, elles ne s'effacent jamais entre elles. Dive docker rend ce mécanisme visible au lieu de le laisser invisible.

## Installer dive : Homebrew, apt, binaire

Plusieurs façons d'installer dive docker selon ton système, aucune ne demande de compte ni de clé API.

Sur macOS ou Linux avec Homebrew :

```bash
brew install dive
```

Sur Ubuntu ou Debian, via le paquet `.deb` publié sur la page des releases GitHub :

```bash
DIVE_VERSION=$(curl -sL "https://api.github.com/repos/wagoodman/dive/releases/latest" | grep '"tag_name":' | sed -E 's/.*"v([^"]+)".*/\1/')
curl -OL https://github.com/wagoodman/dive/releases/download/v${DIVE_VERSION}/dive_${DIVE_VERSION}_linux_amd64.deb
sudo apt install ./dive_${DIVE_VERSION}_linux_amd64.deb
```

Sur Arch Linux, le paquet est dans les dépôts officiels :

```bash
sudo pacman -S dive
```

Et si tu ne veux rien installer sur l'hôte, l'image officielle fait le travail, avec le socket Docker monté pour qu'elle voie tes images locales :

```bash
docker run --rm -it \
  -v /var/run/docker.sock:/var/run/docker.sock \
  wagoodman/dive:latest nginx:latest
```

⚠️ Si tu passes par le binaire Go directement (`go install github.com/wagoodman/dive@latest`), il te faut une version récente de Go installée. Les paquets système ou Homebrew évitent ce problème, privilégie-les si tu n'as pas déjà une toolchain Go sur la machine.

## Lancer dive et lire l'interface

La commande de base, sans fioriture :

```bash
dive nginx:latest
```

L'outil ouvre une interface en plein écran dans ton terminal, découpée en trois zones :

- **À gauche, la liste des couches** (`Image Layers`), avec leur taille et la commande Dockerfile qui les a créées
- **À droite en haut, le contenu de la couche sélectionnée** (`Current Layer Contents`), un arbre de fichiers où chaque entrée est marquée ajoutée, modifiée ou supprimée
- **En bas, le score global** (`Image Details`), avec le score d'efficacité, la taille totale et l'estimation des octets gaspillés

Tu navigues avec les flèches entre les couches, `Tab` pour basculer entre les panneaux, et `Ctrl+Space` pour afficher uniquement ce qui a changé dans la couche sélectionnée au lieu de l'arborescence complète. Pour quitter, `Ctrl+C`.

Si tu préfères construire puis analyser directement, il sait aussi lancer le build lui-même :

```bash
dive build -t mon-app:latest .
```

Ça t'évite l'aller-retour entre `docker build` et `dive`, pratique quand tu itères rapidement sur un Dockerfile.

## Comprendre le score d'efficacité et le gaspillage

Le chiffre qui compte vraiment en bas de l'écran, c'est le score d'efficacité. Un score proche de 100 % veut dire que presque rien n'est dupliqué entre tes couches. Un score qui chute signale qu'une partie de l'image contient des fichiers écrits puis effacés, ou écrasés plusieurs fois par des couches successives.

À côté, dive docker affiche une estimation en octets du gaspillage total. C'est souvent ce chiffre, plus que le pourcentage, qui te donne une idée concrète de la marge de manœuvre. Une image de 900 Mo avec 300 Mo de gaspillage, ça vaut le coup de creuser. La même image avec 15 Mo de gaspillage, tu as probablement déjà fait le plus gros du travail ailleurs.

✅ Astuce : commence toujours par la couche la plus lourde dans la liste de gauche, pas par la première. C'est presque toujours elle qui mérite l'attention, souvent une installation de paquets système ou une étape de build qui laisse des fichiers temporaires derrière elle.

Les images basées sur des gestionnaires de paquets volumineux (apt avec son cache, pip sans `--no-cache-dir`) sont les candidates les plus fréquentes à un mauvais score. Les images Alpine ou distroless partent avec un avantage mécanique : moins de fichiers système au départ, donc moins de place pour le gaspillage.

## Automatiser le contrôle en CI

Un contrôle manuel de temps en temps, c'est bien, mais ça n'empêche personne d'oublier de vérifier un jour où tout le monde est sous pression. Dive docker a un mode spécialement pensé pour ça.

Lancé normalement, il ouvre son interface interactive. Avec la variable d'environnement `CI=true`, il bascule en mode silencieux : pas de TUI, un résumé texte, et un code de sortie qui dépend de seuils que tu définis toi-même.

```bash
CI=true dive nginx:latest
```

Les seuils se configurent dans un fichier `.dive-ci` à la racine de ton projet :

```yaml
rules:
  lowestEfficiency: 0.95
  highestWastedBytes: 20MB
  highestUserWastedPercent: 0.10
```

Si l'un de ces seuils est dépassé, dive docker renvoie un code de retour différent de zéro, et ton job de CI échoue proprement. Sur GitHub Actions, ça s'intègre juste après le build :

```yaml
name: build
on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v4

      - name: Build de l'image
        run: docker build -t mon-app:${{ github.sha }} .

      - name: Installer dive
        run: |
          curl -OL https://github.com/wagoodman/dive/releases/latest/download/dive_0.13.1_linux_amd64.deb
          sudo apt install ./dive_0.13.1_linux_amd64.deb

      - name: Vérifier l'efficacité de l'image
        run: CI=true dive mon-app:${{ github.sha }}
```

Le job échoue avant même que l'image parte sur un registre, le meilleur moment pour corriger un Dockerfile qui a dérivé. Si tu gères déjà tes stacks avec [Dockge](/dockge-docker-gestionnaire-stacks-compose/), ce contrôle complète bien l'interface : Dockge t'aide à gérer le déploiement de tes compose, dive docker s'assure que ce que tu déploies n'est pas gonflé inutilement avant même d'atteindre cette étape.

## Réduire la taille d'une image avec dive

Une fois que l'outil t'a montré où est le gaspillage, les corrections suivent généralement les mêmes schémas.

**Nettoyer dans la même couche, pas dans la suivante.** Installer puis supprimer un paquet dans deux instructions `RUN` séparées ne libère rien, les deux couches s'empilent. Chaîne les commandes :

```dockerfile
RUN apt-get update && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/*
```

**Passer en multi-stage build.** Sépare l'étape de compilation, avec toute sa toolchain lourde, de l'image finale qui n'embarque que le binaire produit :

```dockerfile
FROM golang:1.26 AS builder
WORKDIR /app
COPY . .
RUN go build -o app .

FROM alpine:3.21
COPY --from=builder /app/app /usr/local/bin/app
ENTRYPOINT ["/usr/local/bin/app"]
```

**Vérifier ce qu'un `COPY .` embarque réellement.** Un `.dockerignore` absent ou incomplet fait souvent grimper une couche de plusieurs centaines de Mo avec un `.git`, un `node_modules`, ou des fichiers de build locaux qui n'ont rien à faire dans l'image.

Sur une image qui sert une base de données comme [Redis](/redis-docker-base-donnees-cle-valeur/), le gain est souvent minime, l'image officielle est déjà soignée. C'est plutôt sur tes propres images applicatives, celles qui empilent ton code, tes dépendances et parfois des outils de debug oubliés, que dive docker révèle le plus de marge.

## Limites de dive et alternatives

Dive docker fait une chose précise et la fait bien, mais il ne couvre pas tout.

- **Il ne scanne pas les vulnérabilités.** Dive docker parle de taille et de structure, pas de CVE. Pour ça, un scanner de sécurité dédié reste nécessaire, dive n'a jamais eu cette ambition.
- **Il n'inspecte que ce qui est déjà construit.** Il ne te dit rien sur le comportement runtime d'un conteneur, ses logs ou ses erreurs en production. Pour ça, [Dozzle](/dozzle-docker-visionneuse-logs-web/) reste l'outil plus adapté, puisqu'il suit les logs en temps réel une fois le conteneur lancé.
- **Il ne surveille pas les mises à jour amont.** Une image propre aujourd'hui peut devenir obsolète demain si l'image de base reçoit une nouvelle version. [DIUN](/diun-docker-notification-image-registry/) couvre cette partie, en t'alertant dès qu'une image change sur le registre, pendant que dive reste concentré sur ce qui se passe au moment du build.

Pour une vérification rapide sans ouvrir d'interface, `docker history --no-trunc mon-image` donne une liste brute des couches et de leurs tailles. C'est plus limité, aucun score, aucun détail fichier par fichier, mais ça dépanne quand tu veux juste un chiffre vite fait sans sortir l'artillerie.

Aucun de ces outils ne remplace dive docker, et l'inverse est vrai aussi. Chacun répond à une question différente sur le cycle de vie d'une image.

## Conclusion

Dive docker répond à une question simple que beaucoup de Dockerfiles laissent sans réponse : qu'est-ce qui occupe vraiment cette image, et où est-ce que ça se gaspille. Gratuit, sans inscription, une commande à lancer, et un résultat lisible en quelques minutes, que ce soit en interactif sur ton poste ou en silencieux dans une pipeline.

Lance-le sur ton image la plus lourde, regarde le score d'efficacité, et compare avec une image officielle équivalente. Tu seras probablement surpris de voir combien de Mo traînent depuis des mois sans que personne ne les ait jamais remarqués.
