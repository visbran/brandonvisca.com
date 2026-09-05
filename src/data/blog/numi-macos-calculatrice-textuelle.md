---
title: "Numi macOS : calculatrice textuelle qui comprend le langage naturel"
description: Découvre Numi, la calculatrice macOS qui comprend le langage naturel. Calculs unités, devises, dates et variables en texte brut. Guide complet 2026.
pubDatetime: 2026-09-05T08:00:00.000Z
modDatetime: 2026-09-05T08:00:00.000Z
author: Brandon
tags:
  - debutant
  - macos
  - productivite
featured: false
draft: false
focusKeyword: numi macos calculatrice textuelle
---
## Numi macOS : ta calculatrice enfin intelligente

T'es comme moi, tu détestes l'application Calculatrice native de macOS. Elle est moche, limitée, et dès que tu veux faire un calcul avec des unités ou des conversions, tu perds 10 minutes à googler des ratios. Entre nous, on mérite mieux.

C'est là que **Numi** entre en scène. Pas une calculatrice classique. Un éditeur de texte qui calcule. Tu tapes "15 dollars en euros" et bam, t'as ta réponse. Tu écris "3 heures + 45 minutes" et il te donne la durée totale. C'est exactement le genre d'outil qui te fait te demander pourquoi Apple ne l'a pas intégré nativement.

## Pourquoi Numi change la donne

Numi repose sur un principe simple : le langage naturel. Au lieu de cliquer sur des boutons ridiculement petits ou de taper des parenthèses imbriquées dans un terminal, tu écris ce que tu veux calculer comme si tu parlais à un pote.

Exemple concret : t'as besoin de savoir combien coûte ton abonnement serveur annuel. Avec Numi, tu tapes :

```
5 serveurs * 12 euros/mois * 12 months in euros/year
```

Et Numi te crache le total, converti, formaté. Pas besoin de passer par Google, pas besoin de Notes. Un seul outil, une seule fenêtre.

Ce qui fait la force de Numi, c'est qu'il comprend :

- **Les unités** : mètres, litres, watts, calories, pixels, whatever
- **Les devises** : conversion temps réel via des taux actualisés
- **Les dates et durées** : "25 décembre - aujourd'hui" te donne le nombre de jours restants
- **Les variables** : tu définis `salaire = 3000` puis `salaire * 0.75` pour voir ton net
- **Les bases numériques** : hex, bin, octal, pratique pour les devs

## Installation : rapide et propre

Télécharge Numi depuis [numi.app](https://numi.app) ou directement via Homebrew si t'es un vrai :

```bash
brew install --cask numi
```

L'app pèse ~15 Mo. Pas de framework Electron lourd qui bouffe ta RAM. C'est du Swift natif, ça démarre instantanément et ça consomme quasi rien en arrière-plan.

Au premier lancement, macOS va te demander des permissions d'accessibilité si tu veux utiliser le mode « calcul rapide » (on y revient après). Autorise-le, ça vaut le coup.

## Le langage naturel en action

Numi supporte une syntaxe incroyablement riche. Voici ce que tu peux taper directement dans la fenêtre principale :

### Calculs basiques avec unités

```
150 km / 2 hours in km/h
50 dollars * 3 in euros
100 GB / 5 MB/s in hours
```

Chaque ligne est indépendante. Tu peux avoir 50 calculs dans la même fenêtre, chacun avec son résultat. C'est propre, c'est lisible, c'est ta mémoire de calcul persistante.

### Variables et références

```
prix_ht = 199
quantite = 3
tva = 0.20
prix_ttc = prix_ht * quantite * (1 + tva)
prix_ttc
```

Toute la magie est là. Tu définis une variable simplement avec un `=`, tu la réutilises plus bas. Numi affiche toutes les valeurs intermédiaires et le résultat final. Parfait pour des estimations de projet, des simulations financières ou des calculs réseau.

### Dates et timezones

```
10 days + 2 hours to seconds
25 dec 2026 - today in days
now in UTC
15:00 CET to PST
```

Pour ceux qui gèrent des serveurs dans plusieurs fuseaux horaires ou des plannings d'incidents, c'est indispensable. Plus besoin d'aller sur timeanddate.com.

### Conversions systèmes numériques

```
0xFF in decimal
0b101010 in hex
42 in binary
```

Les développeurs embarqués et les admins réseau vont adorer. C'est instantané, ça évite les erreurs de transcription.

## Widget Notification Center : calcul sans ouvrir l'app

Numi propose un widget pour le Centre de Notifications. Glisse-le dans ta zone aujourd'hui et tu peux faire des calculs rapides sans ouvrir l'application principale.

C'est particulièrement utile quand tu dois juste convertir une devise ou faire une règle de trois. Un coup de trackpad vers la droite, tu tapes, tu vois le résultat, tu reprends ton travail.

Le widget est minimaliste mais il conserve l'essentiel : le langage naturel et les conversions rapides.

## Calcul rapide avec raccourci clavier

Active le mode « Global Shortcut » dans les préférences (Cmd + Shift + = par défaut). N'importe où sur ton Mac, tu presses le raccourci, une petite fenêtre flottante apparaît, tu tapes ton calcul, tu vois le résultat.

C'est mon usage quotidien. Je suis dans un navigateur, un terminal, une réunion Slack, j'ai besoin d'un chiffre, hop, raccourci, calcul, je ferme. Pas de fenêtre à gérer, pas d'alt-tab.

## Numi vs Spotlight

Oui, Spotlight fait des calculs. Tu peux taper `2+2` dans Cmd + Espace et ça marche. Mais Spotlight ne comprend pas les unités, ne gère pas les variables, ne convertit pas les devises, ne calcule pas les dates.

Spotlight c'est une calculette. Numi c'est un tableur textuel. Pas la même catégorie, pas la même productivité.

Si tu cherches un outil qui te fait gagner du temps sur des tâches récurrentes, budgétiser un projet, dimensionner une infra, convertir des specs, Numi est à des années-lumières devant.

## Astuces pro pour aller plus loin

### Export des résultats

Tu peux copier tout le contenu de ta feuille Numi (Cmd + A, Cmd + C) et le coller dans un mail ou un Markdown. Les calculs restent lisibles et les résultats sont conservés. C'est parfait pour documenter une estimation ou partager un dimensionnement.

### Précision et arrondis

Par défaut, Numi arrondit intelligemment. Mais si tu veux forcer la précision, utilise des parenthèses ou spécifie explicitement l'unité de sortie. Par exemple :

```
10 / 3 in decimal
pi * 2 meters in cm
```

### Personnalisation

Dans les préférences, tu peux choisir ton thème (clair, sombre, système), activer ou désactiver le son des touches, et configurer la mise à jour automatique des taux de change. Les devises se mettent à jour quotidiennement, pratique quand tu gères des coûts d'hébergement international.

### Historique persistant

Numi garde ton historique entre les sessions. T'as calculé un budget serveur il y a 3 semaines ? Tu rouvres l'app, c'est là. Chaque feuille est sauvegardée automatiquement. C'est ta mémoire de calcul externe.

## Cas d'usage réels pour ton homelab

Si t'as un homelab comme moi, Numi devient rapidement indispensable :

**Dimensionnement stockage** :
```
10 VMs * 40 GB * 1.2 (snapshot overhead) in TB
```

**Coût électrique estimé** :
```
2 servers * 150 watts * 24 hours * 30 days * 0.18 euros/kWh in euros
```

**Calcul bande passante** :
```
100 Mbps / 8 in MB/s
backup_size = 500 GB
backup_size / (12 MB/s) in hours
```

**Conversion subnet** :
```
2^8 - 2
/26 subnet = 64 IPs
/26 usable = 62 hosts
```

Aucun de ces calculs n'est agréable à faire dans la Calculatrice macOS. Avec Numi, c'est du texte brut, modifiable, documentable, partageable.

## Numi vs les alternatives

J'ai testé Soulver (l'ancêtre), Calcbot, et même des solutions web. Voici le verdict :

- **Soulver** : excellent aussi, mais payant à ~35€ et moins de fonctionnalités de conversions. L'interface est plus chargée.
- **Calcbot** : beau design, mais limité au calcul basique. Pas de variables, pas de dates.
- **Numi** : gratuit dans sa version de base, interface minimaliste, support natif des variables/devises/dates. Le meilleur rapport qualité/prix du marché.

Note : Numi propose une version Pro avec des thèmes supplémentaires et des fonctionnalités avancées. À ~15€, c'est raisonnable si tu l'utilises quotidiennement. La version gratuite couvre déjà 90% des besoins.

## Limites et points de vigilance

Numi n'est pas parfait. Quelques limites à connaître :

- **Pas de scripting** : tu ne peux pas écrire de vraies fonctions ou boucles. C'est intentionnel, Numi reste une calculatrice, pas un langage de programmation.
- **Dépendance internet pour les devises** : sans connexion, les conversions de devises ne fonctionnent pas. Les calculs purs restent disponibles offline.
- **Pas de partage cloud** : ton historique reste local. Pas de synchronisation iCloud ou autre. Si tu travailles sur plusieurs Macs, tu dois exporter/importer manuellement.

## Verdict : à installer dès maintenant

Numi est l'une de ces rares applications qui améliorent ton quotidien sans que tu aies à changer tes habitudes. Tu continues à taper du texte, mais maintenant il calcule pour toi.

Pour les devs, les sysadmins, les freelances qui font des devis, ou simplement ceux qui détestent la Calculatrice macOS, Numi est indispensable. Gratuit, léger, natif, puissant. Pas d'excuse pour ne pas l'essayer.

Installe-le via Homebrew, teste-le 10 minutes, et dis-moi pas que tu reviens en arrière.

---

## FAQ rapide

**Numi est-il gratuit ?**
Oui, la version de base est gratuite et très complète. La version Pro (~15€) ajoute des thèmes et options avancées.

**Numi fonctionne-t-il offline ?**
Les calculs standards oui. Les conversions de devises nécessitent une connexion internet pour les taux à jour.

**Peut-on utiliser Numi sur Windows ou Linux ?**
Oui ! Numi est disponible sur macOS, Windows et Linux. L'expérience est quasi identique sur les trois plateformes.

**Mes calculs sont-ils privés ?**
Totalement. Tout reste en local sur ta machine. Aucune donnée n'est envoyée vers des serveurs, hormis les requêtes de taux de change pour les devises.

**Y a-t-il un équivalent iOS ?**
Pas officiellement, mais la version web et le widget macOS permettent un usage proche sur iPad.
