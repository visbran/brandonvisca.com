---
title: "Omarchy Linux : j'ai testé la distro Arch clé en main"
description: "Omarchy Linux : la distro Arch avec Hyprland préconfigurée. Installation simplifiée, 11 thèmes, sécurité renforcée et outils dev inclus d'emblée."
pubDatetime: "2025-09-26T12:28:27+02:00"
modDatetime: 2026-05-17 00:00:00+02:00
author: Brandon Visca
tags:
  - linux
  - productivite
  - intermediaire
  - hyprland
  - arch-linux
  - guide
featured: false
draft: false
focusKeyword: Omarchy Linux
---
> 💡 **TL;DR** : Omarchy Linux v3.8.0 installe Arch + Hyprland clé en main. 11 thèmes, météo live, rappels intégrés, choix du browser/terminal/éditeur par défaut, outils dev prêts. Zéro config de départ.

Tu cherches une distribution Linux qui allie la puissance d'Arch à l'esthétique d'un bureau moderne ? Spoiler : Omarchy pourrait bien révolutionner ta façon de bosser.

Omarchy Linux, c'est cette distribution qui fait parler d'elle dans les cercles d'administrateurs systèmes éclairés. Basée sur Arch Linux mais avec un twist « omakase » (laissez au chef, en japonais), elle propose une expérience prête à l'emploi avec le gestionnaire de fenêtres tiling Hyprland.

Autrement dit : fini de passer trois semaines à configurer ton environnement de travail. Ici, tout fonctionne out-of-the-box, et en beauté.

## Table des matières

---

## Omarchy en résumé : Arch sans les larmes

Imagine Arch Linux, mais sans la galère de configuration habituelle. Omarchy embarque :

- **🎨 11 thèmes magnifiques** préconçus (Tokyo Night, Catppuccin, Gruvbox…)
- **⌨️ Navigation 100% clavier** avec des raccourcis logiques
- **🔒 Sécurité renforcée** (chiffrement disque obligatoire, firewall activé)
- **🛠️ Outils de développement** prêts à l'emploi (Neovim, Docker, Node.js…)
- **📦 Arch User Repository** intégré via `yay`

Le principe ? Tu installes, tu choisis ton thème, et tu bosses. Point.

![Illustration 1 — Omarchy four-way tiling](fourway-tiling.webp)

---

## Installation : plus simple qu'un YAML bien indenté

Contrairement à une installation Arch classique qui peut transformer même un sysadmin aguerri en zombie, Omarchy mise sur la simplicité.

![Menu d'installation d'Omarchy sur Arch](Omarchy-2025-10-14-at-20.30.23@2x.webp)

### Prérequis

- Une machine compatible UEFI
- Au moins 8 GB de RAM (16 GB recommandé)
- 50 GB d'espace disque minimum
- Secure Boot désactivé

> ⚠️ **Attention** : Omarchy ne supporte pas Secure Boot. Désactive-le dans ton BIOS avant de booter sur la clé USB, sinon l'installateur refusera de démarrer.

### Étapes d'installation

1. **[Télécharge l'ISO d'Omarchy](https://iso.omarchy.org/omarchy-3.8.0.iso)** — version actuelle v3.8.0 (SHA256 : `a9b271e8884dc123f0787e10cff3153dca7361cc6583edd1a3baa283a031f872`)
2. **Grave sur USB** avec [balenaEtcher](https://etcher.balena.io/#download-etcher)
3. **Boot** sur ta clé USB
4. **Lance l'installateur** Arch

Pour effectuer l'installation, rien de bien compliqué :

- Tu choisis ton langage de clavier
- Tu saisis ton nom d'utilisateur pour pouvoir te connecter
- Un bon mot de passe, évidemment !
- Il te propose de connecter Git, tu peux le faire ou passer si tu n'as pas envie maintenant
- Tu choisis ton fuseau horaire
- Un résumé de la configuration s'affiche, tu peux procéder à l'installation si tout est correct

![Interface de configuration de clavier](Omarchy-2025-10-14-at-20.31.31@2x.webp)

![Écran de connexion avec nom d'utilisateur](Omarchy-2025-10-14-at-20.32.03@2x.webp)

![Écran de configuration de compte utilisateur](Omarchy-2025-10-14-at-20.32.25@2x.webp)

![Illustration 2 — Omarchy](Omarchy-2025-10-14-at-20.33.01@2x.webp)

![Illustration 3 — Omarchy](Omarchy-2025-10-14-at-20.33.32@2x.webp)

![Illustration 4 — Omarchy](Omarchy-2025-10-14-at-20.33.44@2x.webp)

![Illustration 5 — Omarchy](Omarchy-2025-10-14-at-20.34.45@2x.webp)

---

## Premier démarrage : bienvenue dans le futur

Au premier lancement, tu tombes sur un bureau… vide. Normal ! Omarchy privilégie la navigation clavier.

### Raccourcis essentiels à retenir

| Raccourci | Action |
|---|---|
| `Super + Space` | Lanceur d'applications |
| `Super + Alt + Space` | Menu Omarchy |
| `Super + Return` | Terminal |
| `Super + B` | Navigateur |
| `Super + K` | Aide raccourcis |
| `Super + Ctrl + R` | Créer un rappel |
| `Super + Ctrl + Alt + W` | Météo détaillée |
| `Super + Ctrl + .` | Transcoder un fichier |

Le menu Omarchy (`Super + Alt + Space`) est ton nouveau meilleur ami. Depuis là, tu installes des packages, tu configures le système, tu changes de thème… Depuis v3.8.0, tu accèdes aussi à _Setup > Defaults_ pour choisir ton navigateur, ton terminal et ton éditeur par défaut — Chrome, Brave, Firefox, Zen, Foot, Ghostty, Neovim, Helix, Zed, tout y est.

---

## Les thèmes : 11 façons de rendre tes collègues jaloux

L'un des atouts majeurs d'Omarchy, ce sont ses thèmes intégrés qui changent **tout** : fond d'écran, couleurs du terminal, Neovim, notifications, barre de tâches…

### Mes favoris

- **Tokyo Night** : sombre et moderne, parfait pour les longues sessions de code
- **Catppuccin** : pastel et doux pour les yeux
- **Gruvbox** : le classique qui ne vieillit pas
- **Nord** : minimaliste et classe

![Illustration 6 — Omarchy thème Catppuccin](catppuccin.webp)

![Illustration 7 — Omarchy thème Kanagawa](kanagawa.webp)

Pour changer de thème : `Super + Ctrl + Shift + Space`

Tu peux même créer tes propres thèmes en copiant un thème existant dans `~/.config/omarchy/themes/` et en bidouillant les couleurs.

---

## Développement : l'environnement qui anticipe tes besoins

Omarchy embarque un stack complet pour le développement.

### Éditeurs

- Neovim avec LazyVim (éditeur principal) : si tu débutes avec Vim, mon [guide d'installation Vim](/installation-vim-guide-complet/) te donnera les bases
- Installation facile de VS Code, Cursor, Zed via le menu — Zed reçoit le theming Omarchy en temps réel depuis v3.8.0

### Environnements de développement

- Node.js, Bun, Deno pour JavaScript
- Ruby on Rails
- PHP avec frameworks populaires
- Docker et docker-compose

### Outils en ligne de commande

- `fzf` pour la recherche floue de fichiers
- `zoxide` pour la navigation intelligente
- `ripgrep` pour chercher dans les fichiers
- `lazygit` et `lazydocker` pour Git et Docker
- Terminal **Foot** disponible via _Install > Terminal_ : remarkably light, 1/5 de la mémoire d'Alacritty, avec theming Omarchy intégré

Si tu veux pousser encore plus loin, combine ça avec [Oh My Zsh + Powerlevel10k](/installation-oh-my-zsh-powerlevel10k-guide-complet/), le terminal devient franchement agréable à utiliser.

L'intégration est remarquable. Par exemple, dans Neovim, `Space Space` utilise fzf pour ouvrir rapidement n'importe quel fichier.

---

## Sécurité : Omarchy prend ça au sérieux

Contrairement à certaines distributions qui considèrent la sécurité comme optionnelle, Omarchy Linux l'impose :

- **Chiffrement disque obligatoire** avec LUKS (par défaut)
- **Firewall activé par défaut** (sauf ports SSH et LocalSend)
- **Rolling release** = correctifs de sécurité en temps réel
- **Isolation Docker** sécurisée via ufw-docker

> 💡 **Serveur headless ?** Depuis v3.8.0, tu peux installer sans chiffrement en appuyant sur `Ctrl + C` à l'étape de confirmation du disque. Pratique pour un redémarrage distant sans devoir saisir la passphrase LUKS au boot.

Cette approche rappelle celle que j'ai détaillée dans mon [guide de sécurisation des serveurs Linux](https://brandonvisca.com/securite-de-votre-serveur-linux/) : la sécurité doit être native, pas ajoutée après coup.

---

## Performance et monitoring

**btop** remplace htop avec style :

```bash
btop
```

### Configuration clavier avancée

Pour configurer plusieurs layouts ou options de clavier, modifie `~/.config/hypr/input.conf` :

```ini
kb_layout = us,fr
kb_options = compose:caps,grp:alts_toggle
```

### Ajuster l'échelle d'affichage

Pour les écrans non-4K, modifie `~/.config/hypr/hyprland.conf` :

```bash
env = GDK_SCALE,1  # Au lieu de 2 par défaut
```

### Installer des packages supplémentaires

Pour installer des logiciels via l'AUR :

```bash
yay -S firefox spotify-launcher discord
```

---

## Troubleshooting courant

**Applications trop grandes ?**

→ Modifie `GDK_SCALE` dans `hyprland.conf`

**Pas de son ?**

→ Vérifie la sortie audio : `Super + Alt + Space` > Setup > Audio

**Clavier français non reconnu ?**

→ Configure `kb_layout` dans les paramètres Hypr

Pour des problèmes plus complexes, la communauté sur GitHub est réactive et les développeurs accessibles.

---

## Conclusion : révolution ou simple évolution ?

J'ai installé Omarchy sur une machine de test en moins de 20 minutes, thème Tokyo Night actif, Neovim configuré, Docker qui tourne. Exactement ce que beaucoup d'entre nous attendaient : la puissance d'Arch sans les nuits blanches de configuration.

### Les plus

- ✅ Installation simplifiée
- ✅ Esthétique soignée et cohérente
- ✅ Sécurité native
- ✅ Productivité immédiate
- ✅ Écosystème Arch intact

### Les moins

- ❌ Courbe d'apprentissage Hyprland
- ❌ Jeune projet (stabilité à confirmer)
- ❌ Documentation encore limitée

Si tu cherches une distribution Linux qui combine productivité, sécurité et esthétique sans sacrifier la puissance d'Arch, Omarchy Linux mérite clairement ton attention.

Le concept « omakase » (laissez au chef) prend ici tout son sens : les développeurs ont fait les choix techniques à ta place, et franchement, ils ont plutôt bon goût.

---

Télécharge l'ISO, installe, et balance-nous un screenshot dans les commentaires avec ton thème préféré.

## Pour aller plus loin

- [Oh My Zsh + Powerlevel10k : transforme ton terminal](/installation-oh-my-zsh-powerlevel10k-guide-complet/)
- [Nebula-Sync : synchroniser plusieurs Pi-hole v6 gratuitement](/nebula-sync-pihole-v6-installation-docker-guide/)
- [Connecter Ubuntu à Active Directory avec SSSD](https://brandonvisca.com/connecter-les-systemes-ubuntu-a-active-directory-en-utilisant-sssd/)
- [Résolution des problèmes de montage RAID](https://brandonvisca.com/depannage-montage-partition-raid-linux-mode-secours/)
