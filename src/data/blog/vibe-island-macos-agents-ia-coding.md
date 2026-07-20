---
title: "Vibe Island : le panneau notch macOS pour surveiller tes agents IA de code"
description: "Open Island, fork open-source de Vibe Island : un panneau macOS natif dans la notch pour surveiller Claude Code, Codex et Cursor sans quitter ta fenêtre."
pubDatetime: "2026-07-18T08:00:00.000Z"
modDatetime: "2026-07-18T08:00:00.000Z"
author: Brandon
tags:
  - macos
  - productivite
  - debutant
  - open-island
  - vibe-coding
  - agent-ia
featured: false
draft: false
focusKeyword: vibe island macos
ogImage: ""
---
> 💡 **TL;DR**
> - Open Island est le fork open-source (GPL v3) de Vibe Island, une app macOS qui s'installe dans la notch pour surveiller tes agents IA de code
> - Tu vois l'état de Claude Code, Codex, Cursor et autres directement dans la barre de menu, sans quitter ton IDE
> - Gratuit, local-first, pas de compte, pas de télémetrie : tu télécharges, tu compiles (ou tu prends le .app), ça marche
> - Parfait complément à ton [terminal Warp avec Agent Mode](/warp-terminal-2025-iterm2-killer-ou-simple-hype-test-complet-ia/) ou ton setup [Raycast macOS](/raycast-macos-outil-productivite-ultime/)

## Table des matières

## Le problème quand tu vibecode à fond

On est en 2026, et si tu codes encore sans agent IA collé à ton terminal, tu perds du temps. Claude Code, Codex CLI, Cursor, Gemini CLI, OpenCode... Ces outils tournent en fond, te proposent des refactos, exécutent des tests, push des commits, et parfois te demandent une validation en plein milieu d'une session. Le truc, c'est que toutes ces conversations se passent dans le terminal. Et si tu travailles sur un autre écran, une autre app, ou que tu es en pleine réunion, tu rates les prompts d'approbation ou tu oublies que ton agent est encore en train de tourner.

C'est exactement le genre de friction inutile qu'on subit quand on laisse l'IA s'installer dans nos workflows sans lui donner une place visible. Le terminal reste caché derrière treize fenêtres, l'agent tourne dans le vide, et toi tu fais autre chose en pensant que c'est fini. Spoiler : ce n'est pas fini, et il vient d'écraser ton `package.json` parce que tu n'as pas vu la demande de confirmation.

## Qu'est-ce que Vibe Island (la référence)

Vibe Island est une application macOS native développée en SwiftUI/AppKit qui s'installe dans la **Dynamic Island** (ou la notch des MacBook plus récents) pour afficher un panneau de contrôle dédié aux agents IA de code. Tu vois en temps réel :

- L'état de la session active (en cours, en attente, terminée)
- Les demandes de permission (écrire un fichier, exécuter une commande, push Git)
- Un bouton pour revenir instantanément au bon terminal
- La progression des tâches longues

L'app est payante : **19,99 USD**, vendue sur le site officiel (vibeisland.app). C'est une app propriétaire, bien fichue, mais qui demande à l'utilisateur de payer pour quelque chose qui, à la base, pourrait être un utilitaire système.

Et c'est là que les choses deviennent intéressantes.

## Open Island : le fork qui dit "pourquoi payer ?"

Un développeur sous le pseudo **Octane0411** a sorti **Open Island** sur GitHub. C'est un fork open-source sous licence **GPL v3** de Vibe Island, avec le même objectif : un panneau macOS dans la notch/top bar pour surveiller tes agents IA de code. Mais cette fois, c'est gratuit, local-first, et tu contrôles tout.

Le repo compte déjà plus de **1 600 étoiles** à l'heure où j'écris ces lignes, ce qui montre que le besoin était réel. Le slogan du projet résume bien la démarche : *"Why pay for a closed-source app just to monitor your coding agents ?"*

Contrairement à beaucoup de projets "open-source" qui sont en réalité des SaaS déguisés, Open Island est **100 % offline**. Pas de serveur, pas de télémetrie, pas de compte utilisateur. Tu clones, tu compiles avec Xcode, et tu as un `.app` natif sur ton Mac. Même si tu ne veux pas compiler toi-même, les releases GitHub fournissent un binaire prêt à l'emploi.

## Ce que ça fait concrètement

Open Island s'installe comme un agent de la barre de menu macOS. Une fois lancé, il détecte automatiquement les sessions actives de tes agents IA et affiche un petit panneau compact dans la zone de la notch (ou à côté si tu as un Mac sans notch).

Voici ce que tu vois à l'écran :

### Statut de session en temps réel

L'icône change de couleur selon l'état :
- **Vert** : l'agent travaille
- **Orange** : en attente d'une permission ou d'une validation
- **Gris** : aucune session active

Tu n'as plus besoin de jongler entre les bureaux virtuels pour vérifier si Claude Code a fini sa refacto.

### Gestion des permissions

Quand l'agent demande à écrire un fichier sensible ou à exécuter une commande système, Open Island affiche une notification discrète dans la notch. Tu peux approuver ou refuser directement depuis le panneau, sans retourner dans le terminal. C'est particulièrement utile quand tu fais tourner des sessions longues et que tu ne veux pas rester scotché à ta fenêtre de code.

### Jump-back instantané

Le feature killer : un clic sur le panneau te ramène directement sur la bonne fenêtre de terminal, avec le bon onglet, au bon moment. Si tu utilises plusieurs terminaux (ce qui est mon cas avec [iTerm2 configuré à la sauce power user](/iterm2-guide-configuration-macos-2025/)), ce bouton évite de chercher pendant trois minutes où ton agent a décidé de s'installer.

### Compatibilité multi-agent

Open Island supporte nativement plusieurs outils :
- **Claude Code** (cc)
- **Codex CLI** (OpenAI)
- **Cursor** (en mode agent)
- **Gemini CLI**
- **OpenCode**

Et plusieurs terminaux :
- Terminal.app (le basique macOS)
- iTerm2
- Ghostty
- Kitty
- WezTerm
- tmux / screen sessions

L'intégration se fait par parsing des processus et des fichiers de session, sans plugin à installer dans chaque terminal.

## Comment l'installer

Je te préviens tout de suite : ce n'est **pas** une app Docker. Pas de `docker compose up`, pas de volume à monter, pas de port à exposer. C'est une application macOS native, et elle s'installe comme n'importe quel autre logiciel macOS.

### Méthode 1 : Télécharger le binaire (recommandé)

1. Va sur la page [Releases du repo GitHub](https://github.com/Octane0411/open-vibe-island/releases)
2. Télécharge le dernier `.dmg` ou `.zip`
3. Glisse l'app dans ton dossier Applications
4. Ouvre les Préférences Système → Confidentialité et sécurité → Accessibilité → ajoute Open Island
5. Lance l'app, elle apparaît dans la barre de menu

### Méthode 2 : Compiler depuis les sources (pour les curieux)

Si tu veux vraiment tout contrôler ou modifier le comportement :

```bash
git clone https://github.com/Octane0411/open-vibe-island.git
cd open-vibe-island
open OpenIsland.xcodeproj
```

Puis build avec Xcode (nécessite macOS 14+ et Xcode 15+). Le projet est en SwiftUI + AppKit, propre et bien structuré. Même si tu n'es pas développeur iOS, le code est lisible.

## Vibe Island vs Open Island : le comparatif rapide

| Critère | Vibe Island (payant) | Open Island (OSS) |
|---------|---------------------|-------------------|
| Prix | 19,99 $ USD | Gratuit |
| Licence | Propriétaire | GPL v3 |
| Local-first | Oui | Oui |
| Télémetrie | Non précisée | Aucune |
| Code source | Fermé | Ouvert sur GitHub |
| Agents supportés | cc, Codex, Cursor | cc, Codex, Cursor, Gemini CLI, OpenCode |
| Mise à jour | Dépend du dev | Communautaire, PR acceptées |
| Personnalisation | Limitée | Forkable, moddable |

Si tu es du genre à payer pour soutenir un dev indépendant, Vibe Island est une option honnête. Si tu préfères garder le contrôle, avoir accès au code, et ne pas sortir la carte bleue pour un utilitaire système, Open Island est une alternative parfaitement viable. À fonctionnalités quasi identiques, le choix est vite vu.

## Pourquoi ça me parle en tant qu'homelabbeur

Dans mon workflow, j'ai souvent plusieurs sessions qui tournent en parallèle. Une session Claude Code sur un projet de refonte du blog en [Astro](/auto-hebergement-guide-complet-2025/), une session Codex sur un script d'automatisation du [backup](/duplicati-docker-sauvegarde/), et parfois un agent Cursor sur un side project. Sans outil de surveillance, je perds le fil.

Open Island me permet de garder un œil sur tout ça sans saturer mon espace de travail. C'est léger, natif, et ça ne consomme pratiquement pas de ressources. En moyenne, l'app utilise moins de 50 Mo de RAM et 0 % de CPU au repos. Comparé à Electron qui dévore la moitié de ton Mac pour afficher une page web déguisée en app, c'est le jour et la nuit.

Et comme tout tourne en local, pas de peur que mes prompts ou mes sessions fuient vers un serveur tiers. Dans un monde où on balance nos lignes de code à des API extérieures, garder un minimum de contrôle sur l'interface de surveillance, c'est déjà ça.

## Les limites à connaître

Open Island n'est pas magique. Voici les frictions que j'ai rencontrées :

- **macOS uniquement** : pas de version Windows ou Linux. Si tu codes sur plusieurs OS, ce n'est pas l'outil universel.
- **Nécessite une notch ou un espace top bar** : sur un Mac sans notch (MacBook Air M1 par exemple), le panneau s'affiche dans la barre de menu classique. Ça marche, mais c'est moins sexy.
- **Détection par processus** : si tu renommes tes processus agents ou si tu utilises un wrapper custom, la détection automatique peut rater. Il faut parfois ajouter manuellement le pattern de détection dans les prefs.
- **Pas d'intégration IDE** : pour l'instant, ça ne communique pas directement avec VS Code, JetBrains ou Neovim. C'est lié au terminal, pas à l'éditeur.
- **GPL v3** : si tu veux l'utiliser dans un contexte pro ou l'intégrer à un produit commercial, pense aux implications de la licence.

Même avec ces limites, pour un usage personnel sur macOS, c'est un outil qui gagne à être connu.

## Idées d'amélioration (si tu veux contribuer)

Le projet est ouvert aux contributions. Quelques idées qui me trottent dans la tête :

- Une API locale pour exposer le statut des agents à d'autres outils (par exemple afficher le statut dans une [barre de menu custom](/ice-macos-gestionnaire-barre-menu-gratuit-2025/))
- Un mode "focus" qui masque toutes les notifications sauf les approbations critiques
- Support des agents auto-hébergés (Ollama, LM Studio) pour ceux qui font tourner leurs modèles en local dans leur [homelab](/auto-hebergement-guide-complet-2025/)
- Un widget pour [Boring.Notch](/boring-notch-macbook-dynamic-island/) pour fusionner les deux univers

Si tu sais coder en Swift, le repo est accueillant et les issues bien tagguées.

## Conclusion

Open Island prouve qu'on n'a pas besoin de payer 20 dollars pour obtenir un outil de surveillance d'agents IA sur macOS. Le fork GPL v3 d'Octane0411 offre la même expérience que Vibe Island, avec l'avantage d'être gratuit, inspectable et modifiable. Dans un écosystème où on nous vend de plus en plus des abonnements pour des fonctionnalités système, avoir une alternative open-source qui tourne en local et respecte ta vie privée, c'est une bouffée d'air frais.

Si tu codes avec Claude Code, Codex ou Cursor sur Mac, essaie-le. Ça prend cinq minutes à installer, ça ne mange pas de pain, et ça te fera gagner plus de temps que tu ne l'imagines. Parce qu'à la fin, le vrai luxe quand on code avec une IA, ce n'est pas de payer pour une interface jolie : c'est de ne jamais perdre le fil de ce que ton agent est en train de faire.
