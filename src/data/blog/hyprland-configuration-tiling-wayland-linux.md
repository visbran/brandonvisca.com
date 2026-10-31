---
title: "Hyprland configuration : bureau tiling Wayland sous Linux, étape par étape"
description: "Hyprland configuration : installe ce compositeur Wayland tiling, règle gaps, animations, binds et règles de fenêtre, et le vrai statut face à Lua."
pubDatetime: "2026-10-31T11:01:11+01:00"
modDatetime: "2026-10-30T08:00:00.000Z"
author: Brandon
tags:
  - linux
  - sysadmin
  - tiling
  - terminal
  - intermediaire
featured: false
draft: false
focusKeyword: hyprland configuration
faqs:
  - question: "Hyprland fonctionne-t-il correctement avec une carte Nvidia ?"
    answer: "Oui, mais c'est le point le plus fragile du projet. Active les variables d'environnement recommandées par le wiki et vérifie ton pilote propriétaire, les cartes AMD et Intel restent plus simples en Wayland."
  - question: "Une erreur de syntaxe dans hyprland.conf bloque-t-elle tout le bureau ?"
    answer: "Non, Hyprland ignore la ligne fautive et démarre avec le reste de la configuration valide. Regarde les logs avec hyprctl pour repérer précisément quelle ligne a été rejetée."
  - question: "Faut-il redémarrer la session après avoir modifié sa configuration ?"
    answer: "Non, hyprctl reload recharge le fichier à chaud sans fermer tes fenêtres ni ta session. Un redémarrage complet n'est utile que si tu changes de pilote graphique ou de session Wayland entière."
---
> 💡 **TL;DR**
> - Hyprland configuration se fait dans un seul fichier texte, `~/.config/hypr/hyprland.conf`, organisé en sections `general`, `decoration`, `input` et des lignes `bind` pour le clavier
> - Gratuit et open source (licence BSD-3-Clause, projet `hyprwm` sur GitHub), installable via le gestionnaire de paquets de ta distribution, `pacman -S hyprland` sur Arch
> - Hyprland prépare un virage vers des configs en Lua depuis la version 0.55, et affiche déjà un avertissement de dépréciation sur `.conf` en 0.57 : le format texte marche encore, mais vérifie ta version avant de copier un tuto trop vieux

## Hyprland configuration : un compositeur Wayland qui tient ses promesses

Tu en as marre de GNOME qui bouffe de la RAM pour afficher trois fenêtres côte à côte ? Hyprland répond à un besoin précis : un compositeur Wayland en tiling dynamique, léger, qui te laisse composer ton bureau fenêtre par fenêtre au clavier plutôt qu'à coups de glisser-déposer. Le projet est maintenu par l'organisation `hyprwm` sur GitHub, publié en open source sous licence BSD-3-Clause, et il tourne autour des 39 000 étoiles. Gratuit, sans compte à créer, sans version payante qui débloque les vrais réglages.

Ce qui fait la différence avec i3 ou Sway, c'est l'esthétique. Hyprland configuration ne se limite pas à des rectangles qui s'empilent : flou derrière les fenêtres, coins arrondis, animations fluides sur chaque changement de workspace. Techniquement c'est un vrai compositeur Wayland, pas un gestionnaire de fenêtres X11 maquillé, ce qui veut dire un rendu natif, une gestion propre du multi-écran et du HiDPI, et zéro dépendance à Xwayland pour les applications qui parlent nativement Wayland.

## Table des matières

## Installer Hyprland et trouver le fichier de configuration

Sur Arch Linux, qui reste la distribution la plus naturelle pour Hyprland, une seule commande suffit :

```bash
sudo pacman -S hyprland
```

Les autres distributions proposent aussi des paquets, mais les noms et la fraîcheur des versions varient beaucoup d'un dépôt à l'autre. Avant de copier un tuto trouvé sur un forum, vérifie toujours le [guide d'installation officiel sur wiki.hypr.land](https://wiki.hypr.land/) pour la méthode recommandée sur ta distribution précise.

Une fois installé, lance une première fois ta session, puis repère le fichier qui porte toute ta configuration :

```bash
mkdir -p ~/.config/hypr
nvim ~/.config/hypr/hyprland.conf
```

Ce fichier unique, `hyprland.conf`, concentre tout : moniteurs, raccourcis, apparence, règles de fenêtre. Pas de panneau de préférences, pas de clics dans un menu. Tu écris ta configuration comme tu écrirais un script, et c'est exactement cette logique qui rend Hyprland configuration aussi puissante qu'intimidante au premier abord.

Avant d'aller plus loin, vérifie ta version exacte :

```bash
hyprctl version
```

Ce numéro compte. La syntaxe `hyprland.conf` a légèrement bougé plusieurs fois au fil des versions, et depuis peu, Hyprland encourage une bascule vers Lua. On y revient plus bas, mais retiens déjà ce réflexe : chaque exemple de ce guide, et de n'importe quel autre, doit être relu à la lumière de ton `hyprctl version`.

## Anatomie d'un hyprland.conf : general, decoration, animations

Voici la structure de base que je recommande pour démarrer une Hyprland configuration propre, à coller dans ton fichier et à ajuster section par section :

```ini
monitor=,preferred,auto,1

input {
    kb_layout = fr
    follow_mouse = 1
    sensitivity = 0
}

general {
    gaps_in = 5
    gaps_out = 10
    border_size = 2
    col.active_border = rgba(89b4faee)
    col.inactive_border = rgba(595959aa)
    layout = dwindle
}

decoration {
    rounding = 8
    blur {
        enabled = true
        size = 3
        passes = 1
    }
}

animations {
    enabled = true
}

dwindle {
    pseudotile = true
    preserve_split = true
}
```

Chaque bloc a un rôle précis. `general` fixe les espacements entre fenêtres (`gaps_in` entre deux fenêtres tiling, `gaps_out` vers les bords d'écran) et la couleur de la bordure active, pile ce qu'il te faut pour repérer d'un coup d'œil quelle fenêtre a le focus. `decoration` gère le flou et les coins arrondis, deux réglages purement cosmétiques mais qui changent complètement le ressenti du bureau. `dwindle` configure le layout par défaut : `pseudotile` garde une fenêtre à sa taille naturelle tant que tu ne la tiles pas explicitement, `preserve_split` évite que l'arbre de tiling se réorganise tout seul à chaque fermeture de fenêtre.

Chaque modification se recharge à chaud, sans fermer une seule fenêtre :

```bash
hyprctl reload
```

⚠️ Si `blur` et les animations font ramer ton laptop, c'est souvent un signe que la machine swap plus qu'elle ne devrait sous la charge du compositeur. J'ai détaillé comment ajuster ça proprement dans mon [guide swap Linux](/guide-swap-linux-configuration-optimisation/), en particulier le réglage de `swappiness` sur une machine qui fait tourner un compositeur graphique en plus du reste.

## Binds et dispatchers : reprendre le clavier en main

La vraie force d'un tiling WM, c'est de ne quasiment plus toucher la souris. Tout passe par des lignes `bind`, avec une touche modificatrice qu'on définit une fois pour toutes :

```ini
$mainMod = SUPER

bind = $mainMod, Return, exec, kitty
bind = $mainMod, Q, killactive
bind = $mainMod, F, togglefloating
bind = $mainMod, V, exec, ladybird
bind = $mainMod, 1, workspace, 1
bind = $mainMod, 2, workspace, 2
bind = $mainMod SHIFT, 1, movetoworkspace, 1
bind = $mainMod, left, movefocus, l
bind = $mainMod, right, movefocus, r
```

Chaque ligne suit le même schéma : modificateur, touche, dispatcher, paramètre éventuel. `exec` lance un programme, `killactive` ferme la fenêtre focus, `togglefloating` bascule une fenêtre entre tiling et flottante, `movefocus` déplace le focus dans une direction. `workspace` change d'espace de travail, `movetoworkspace` y déplace la fenêtre active sans te faire suivre.

Mon setup chez moi lance un navigateur minimaliste sur `$mainMod V`. J'utilise [Ladybird](/ladybird-browser-le-navigateur-web-qui-refuse-de-se-soumettre-a-google-et-tant-mieux/) justement parce qu'il reste léger et démarre vite, ce qui compte sur un bureau pensé pour la rapidité au clavier. Pour le terminal, Kitty ou Alacritty font tous les deux l'affaire, et si tu veux harmoniser les couleurs entre ton terminal, ton éditeur et Hyprland, j'ai un guide complet sur l'[installation du thème Catppuccin avec vim-plug](/installation-theme-vim-guide/) qui se marie parfaitement avec les couleurs `rgba()` qu'on vient de voir plus haut.

## Règles de fenêtre et gestion du tiling au quotidien

Certaines applications ne doivent jamais être tilées : un gestionnaire de volume, une boîte de dialogue, un lecteur vidéo flottant. La syntaxe actuelle pour les règles de fenêtre, après le retrait de l'ancien `windowrulev2`, se fait directement avec `windowrule` :

```ini
windowrule = float, class:^(pavucontrol)$
windowrule = float, class:^(blueman-manager)$
windowrule = size 800 600, class:^(pavucontrol)$
windowrule = workspace 3, class:^(discord)$
```

Chaque règle associe une action (`float`, `size`, `workspace`) à un sélecteur, le plus souvent la classe de la fenêtre. Pour trouver la classe exacte d'une application récalcitrante, lance `hyprctl clients` pendant qu'elle est ouverte : le champ `class` est écrit noir sur blanc dans la sortie.

Côté layout, Hyprland propose aussi `master` en alternative à `dwindle` (une fenêtre principale occupe la moitié de l'écran, les autres se partagent le reste) et un mode `monocle` qui passe une fenêtre en plein écran logique sans la sortir du tiling. Bascule entre les deux avec :

```ini
bind = $mainMod, M, layoutmsg, togglemaster
bind = $mainMod, P, pseudo
```

Bon, on va pas se mentir : les premières semaines, tu vas passer plus de temps à ajuster tes règles qu'à travailler. C'est normal, c'est même le but. Une Hyprland configuration qui te convient vraiment se construit par petites touches, pas en copiant un dotfiles GitHub entier le premier soir.

## Hyprland configuration chez Omarchy et le virage vers Lua

Omarchy, la distribution Arch pensée pour démarrer vite avec un bureau tiling déjà fonctionnel, embarque Hyprland préconfiguré par défaut. Tes propres réglages viennent se poser par-dessus les valeurs par défaut de la distribution dans ce même fichier `~/.config/hypr/hyprland.conf`, pensé pour survivre aux mises à jour sans que tu doives tout réécrire à chaque fois.

Spoiler : ça va bouger dans les mois qui viennent. Depuis la version 0.55, Hyprland accepte une configuration écrite en Lua en plus du format texte historique, et depuis la 0.56 puis la 0.57 sortie fin octobre 2026, le projet affiche un avertissement de dépréciation directement dans les logs quand tu utilises encore `.conf`. Le format texte continue de fonctionner au moment où j'écris ces lignes, mais la direction est claire. Des convertisseurs communautaires existent déjà pour traduire un `hyprland.conf` existant vers `hyprland.lua`, utiles le jour où tu voudras migrer sans tout retaper à la main.

La vraie question c'est : dois-tu migrer tout de suite ? Je dirais non, sauf si tu pars d'une installation toute neuve. Ta Hyprland configuration actuelle en `.conf` reste valide, documentée partout, et comprise par toutes les ressources existantes sur le sujet. Garde juste un œil sur `hyprctl version` et sur les notes de version avant chaque mise à jour majeure.

## Dépanner une configuration qui casse ton compositeur

Une ligne mal écrite dans `hyprland.conf` ne plante pas tout ton bureau. Hyprland ignore la section fautive et continue de démarrer avec le reste de la configuration valide, un comportement bien plus tolérant que celui de beaucoup d'autres compositeurs. Pour savoir précisément ce qui a été rejeté :

```bash
hyprctl reload
journalctl --user -u hyprland -n 50
```

Si un module de ta barre, comme l'horloge affichée par Waybar, se met à afficher une heure fausse après un changement de configuration réseau ou système, le souci vient rarement de Hyprland lui-même : va vérifier la synchronisation côté système, j'ai écrit un guide sur [comment régler le fuseau horaire et synchroniser l'heure du serveur sous Linux](/comment-modifier-heure-du-serveur-sous-linux/) qui couvre exactement ce cas.

✅ Garde toujours un second moyen d'accès à ta session avant de toucher à la configuration des moniteurs ou des pilotes graphiques : un `Ctrl+Alt+F3` vers un TTY texte te sauve la mise si l'écran reste noir après un `hyprctl reload` raté.

## Conclusion

Hyprland configuration demande un peu plus d'investissement qu'un bureau classique, mais le résultat tient ses promesses : léger, rapide au clavier, et visuellement à la hauteur des compositeurs les plus chargés. Commence par la structure de base de cet article, avance section par section, et laisse ton `hyprland.conf` grossir au rythme de tes vraies habitudes plutôt que d'un dotfiles téléchargé d'un coup. Et garde un œil sur le virage Lua, il ne presse pas encore, mais il arrive.
