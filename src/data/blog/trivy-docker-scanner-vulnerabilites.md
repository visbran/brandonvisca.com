---
title: "Trivy Docker : scanner de vulnérabilités pour images et conteneurs"
description: Trivy Docker scanne tes images pour CVE, secrets et configs dangereuses, gratuit et open source. Installation, commandes essentielles et CI/CD.
pubDatetime: "2026-09-22T11:01:12+02:00"
modDatetime: "2026-09-21T08:00:00.000Z"
author: Brandon
tags:
  - securite
  - docker
  - hardening
  - guide
  - intermediaire
featured: false
draft: false
focusKeyword: trivy docker
faqs:
  - question: "Trivy Docker fonctionne-t-il sans connexion internet ?"
    answer: "Non par défaut, il télécharge sa base de vulnérabilités au premier lancement. Tu peux la mettre en cache localement pour scanner ensuite en environnement isolé, tant que tu la rafraîchis régulièrement."
  - question: "Trivy Docker peut-il faire échouer un build en CI si une CVE critique traîne ?"
    answer: "Oui, c'est même sa raison d'être en pipeline. L'option --exit-code renvoie un code différent de zéro dès qu'une vulnérabilité correspond aux critères que tu as fixés, ce qui casse le job."
  - question: "Trivy Docker signale des CVE sans correctif disponible, dois-je m'en inquiéter ?"
    answer: "Pas forcément dans l'urgence. Une CVE sans fix publié ne se corrige pas plus vite en la fixant du regard. Filtre-la avec --ignore-unfixed pour te concentrer sur ce que tu peux réellement corriger."
---
> 💡 **TL;DR**
> - Trivy Docker scanne une image et liste ses CVE, ses secrets embarqués et ses mauvaises configurations, gratuit et open source (Apache-2.0)
> - Installation en une commande via Homebrew, apt ou le script officiel, aucune inscription ni clé API requise
> - S'intègre en CI/CD pour bloquer un build dès qu'une vulnérabilité critique passe, avec `--severity`, `--exit-code` et `--ignore-unfixed`

## Trivy Docker : ton scanner de vulnérabilités qui bosse avant la prod

Tu buildes une image, tu la pousses, elle tourne. Et dedans, il y a peut-être une lib OpenSSL vieille de deux ans avec une CVE critique que personne n'a jamais regardée. C'est le scénario classique : on soigne le Dockerfile, on optimise les layers, et on oublie que chaque paquet embarqué est une porte d'entrée potentielle.

Trivy Docker règle ce problème en une commande. Tu lui donnes le nom d'une image, il te sort la liste des vulnérabilités connues dedans, triées par gravité, avec le correctif disponible quand il existe. Pas d'agent à déployer, pas de compte à créer, pas de tableau de bord SaaS à configurer. Un binaire, une commande, un résultat.

Chez moi, c'est devenu un réflexe avant tout push d'image en prod sur le homelab. Deux secondes de scan contre des heures de nettoyage après coup si un scanner de vulnérabilités automatisé chez un tiers repère le problème avant toi. Le calcul est vite fait.

## Table des matières

## Trivy Docker, c'est quoi exactement

Trivy est développé par Aqua Security, une boîte spécialisée dans la sécurité cloud-native, et distribué sous licence Apache-2.0. Autrement dit : open source, gratuit, code auditable, pas de version bridée qui te pousse vers un abonnement.

Trivy Docker ne se limite pas aux CVE. Le même binaire couvre plusieurs scanners :

- **Vulnérabilités (CVE)** : paquets système et dépendances applicatives (npm, pip, gems, Go modules) dans l'image
- **Secrets** : clés API, tokens et mots de passe oubliés dans les layers ou les variables d'environnement
- **Mauvaises configurations** : fichiers Infrastructure as Code (Dockerfile, Kubernetes, Terraform) qui violent des bonnes pratiques connues
- **SBOM** : génération d'une nomenclature logicielle complète de l'image, utile pour la conformité

Pour du scan d'image pure, tu n'as besoin que du premier point. Mais savoir que le même outil couvre le reste, ça évite d'empiler trois scanners différents dans ta CI pour trois besoins qui se recoupent.

La dernière version stable au moment où j'écris ces lignes est la 0.74.0, sortie mi-août 2026. Le projet est actif, les mises à jour de la base de vulnérabilités sont quotidiennes.

## Installer Trivy Docker : Homebrew, apt, script officiel

Trois façons d'installer Trivy Docker selon ton système, aucune ne demande de compte.

Sur macOS ou Linux avec Homebrew :

```bash
brew install trivy
```

Sur Debian ou Ubuntu, via le dépôt apt officiel :

```bash
sudo apt-get install -y wget gnupg
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | gpg --dearmor | sudo tee /usr/share/keyrings/trivy.gpg > /dev/null
echo "deb [signed-by=/usr/share/keyrings/trivy.gpg] https://aquasecurity.github.io/trivy-repo/deb generic main" | sudo tee /etc/apt/sources.list.d/trivy.list
sudo apt-get update
sudo apt-get install -y trivy
```

⚠️ Si tu as configuré ce dépôt avant avril 2026, réimporte la clé GPG avec la commande `wget` ci-dessus. La version 0.70.0 a fait tourner les clés de signature des paquets deb et rpm, et un ancien trousseau fait échouer la vérification au prochain `apt-get update`.

Sans gestionnaire de paquets, le script d'installation officiel fait le travail, binaire posé directement dans `/usr/local/bin` :

```bash
curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sudo sh -s -- -b /usr/local/bin
```

Et si tu préfères ne rien installer du tout sur l'hôte, l'image officielle fait l'affaire, avec le socket Docker monté pour qu'elle voie tes images locales :

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy:latest image nginx:latest
```

## Scanner une image avec Trivy Docker : les commandes qui comptent

La commande de base, sans fioriture :

```bash
trivy image nginx:latest
```

Trivy Docker télécharge sa base de vulnérabilités au premier lancement (quelques centaines de Mo, mise en cache ensuite), puis crache un tableau avec le paquet concerné, la CVE, la sévérité et la version corrigée si elle existe. Sur une image Alpine minimaliste, ça prend deux à trois secondes une fois le cache chaud. Sur une image Ubuntu avec 400 paquets, compte plutôt 10 à 15 secondes.

Le vrai intérêt arrive avec le filtrage, parce qu'un scan brut sur une image un peu grosse te sort facilement 200 lignes, dont la moitié n'a aucun correctif publié et ne te sert à rien dans l'immédiat.

Ne garder que le critique et le haut niveau de gravité :

```bash
trivy image --severity CRITICAL,HIGH nginx:latest
```

Masquer les CVE sans correctif disponible, pour te concentrer sur ce que tu peux réellement traiter aujourd'hui :

```bash
trivy image --severity CRITICAL,HIGH --ignore-unfixed nginx:latest
```

Exporter le résultat en JSON pour l'exploiter ailleurs (dashboard, ticket automatique, archivage) :

```bash
trivy image --format json --output resultat.json nginx:latest
```

Et pour scanner uniquement les vulnérabilités, en désactivant les autres scanners si tu veux gagner du temps sur une image volumineuse :

```bash
trivy image --scanners vuln nginx:latest
```

✅ Astuce homelab : lance un premier scan sans filtre sur tes images maison pour voir l'ampleur des dégâts, puis affine avec `--severity` une fois que tu as une idée du volume. Filtrer trop tôt te cache des choses que tu devrais voir au moins une fois.

## Intégrer Trivy Docker dans une CI/CD

Un scan manuel de temps en temps, c'est bien. Un scan systématique à chaque build, c'est ce qui évite qu'une image vulnérable atterrisse en prod parce que tout le monde a oublié de vérifier ce jour-là.

Par défaut, Trivy Docker sort toujours avec un code de retour 0, même s'il trouve des CVE critiques. Logique : un simple audit ne doit pas casser ton terminal. Mais en CI, tu veux l'inverse, un exit code non nul qui fait échouer le job :

```bash
trivy image --severity CRITICAL,HIGH --ignore-unfixed --exit-code 1 mon-app:latest
```

Sur GitHub Actions, l'action officielle `aquasecurity/trivy-action` t'évite de gérer l'installation toi-même :

```yaml
name: build
on:
  push:
    branches: [main]
  pull_request:

jobs:
  build:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v4

      - name: Build de l'image
        run: docker build -t mon-app:${{ github.sha }} .

      - name: Scan Trivy Docker
        uses: aquasecurity/trivy-action@v0.36.0
        with:
          image-ref: "mon-app:${{ github.sha }}"
          format: table
          severity: CRITICAL,HIGH
          exit-code: "1"
```

Le job échoue proprement si une CVE critique ou haute traîne dans l'image, avant même que tu la pousses sur ton registre. C'est le moment idéal pour bloquer le problème, largement avant qu'un [reverse proxy Traefik](/traefik-reverse-proxy-docker/) ne l'expose sur internet.

## Trivy Docker et le reste de ta défense en profondeur

Trivy Docker traite un problème précis : ce qui est déjà emballé dans ton image au moment du build. Il ne remplace aucune des autres couches de sécurité de ton infra, il les complète.

Une fois l'image propre et déployée, la sécurité continue au niveau du runtime. Si tu fais tourner tes conteneurs en root par défaut, jette un œil à [Podman vs Docker en rootless](/podman-vs-docker-rootless/) : réduire les privilèges du process limite les dégâts d'une CVE que Trivy n'a pas encore vue passer, parce que la base de données a un jour de retard sur la publication.

Côté réseau, un pare-feu correctement configuré reste indispensable même avec des images saines. [UFW pour Docker](/ufw-docker-pare-feu-linux/) évite le classique piège des règles iptables de Docker qui contournent silencieusement ton pare-feu, un problème totalement indépendant du contenu de tes images.

Et pour la détection d'intrusion en continu, [CrowdSec en conteneur](/crowdsec-docker-securite-collaborative/) surveille les comportements suspects après coup, là où Trivy s'arrête à l'analyse statique avant déploiement. Les deux logiques sont complémentaires, pas concurrentes. Ajoute [Fail2Ban en Docker](/fail2ban-docker-securite-serveur/) si tu exposes des services avec authentification, pour bloquer le brute-force que ni Trivy ni un scan d'image ne verront jamais venir.

Aucun de ces outils ne remplace les autres. Trivy Docker répond à « qu'est-ce qui traîne dans mon image ». Les autres répondent à « qu'est-ce qui essaie de rentrer maintenant ».

## Les limites de Trivy Docker à connaître

Trivy Docker n'est pas magique, et il vaut mieux le savoir avant de lui faire une confiance aveugle.

- **Il ne détecte que le connu.** Une CVE référencée hier soir peut ne pas encore être dans la base au moment de ton scan. Zéro résultat ne veut pas dire zéro risque, ça veut dire zéro vulnérabilité *connue à cette date*.
- **Les faux positifs existent.** Un paquet peut être marqué vulnérable alors que le code vulnérable n'est jamais exécuté dans ton contexte. Ça arrive surtout sur de grosses distributions de base avec beaucoup de paquets inutilisés.
- **Beaucoup de CVE n'ont pas de correctif.** C'est frustrant de voir une liste rouge sans rien à faire dessus dans l'immédiat, d'où l'intérêt de `--ignore-unfixed` pour ne pas se noyer.
- **Une base plus légère change tout.** Une image Alpine ou distroless a mécaniquement moins de paquets, donc moins de surface pour Trivy à signaler. C'est souvent le vrai levier avant même de scanner : réduire ce qu'il y a à vérifier.

Un scan propre aujourd'hui n'est jamais une garantie permanente. Rescanner régulièrement les images en cours d'utilisation, pas seulement au moment du build, c'est ce qui rattrape les CVE découvertes après coup sur des dépendances qui n'ont pas bougé depuis des mois.

## Conclusion

Trivy Docker fait une chose et la fait bien : te dire ce qui ne va pas dans une image avant qu'elle ne devienne un problème en prod. Gratuit, sans inscription, une commande à taper, et un résultat exploitable immédiatement en local ou en CI.

Ça ne dispense de rien d'autre, ni du firewall, ni du rootless, ni de la détection d'intrusion. Mais c'est la vérification la moins chère à mettre en place et celle qui rapporte le plus vite. Installe-le, lance un scan sur ton image la plus critique, et regarde ce qui en sort. Tu seras surpris de ce qui traîne parfois depuis des mois sans que personne ne l'ait vu.
