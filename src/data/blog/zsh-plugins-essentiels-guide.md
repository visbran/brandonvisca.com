---
title: "Zsh Plugins essentiels : 7 plugins que j'utilise tous les jours"
description: "Les 7 zsh plugins essentiels que j'utilise chaque jour : git, autosuggestions, syntax-highlighting, sudo, extract. Guide Oh My Zsh 2026 complet."
pubDatetime: "2026-06-09T06:00:00.000Z"
modDatetime: "2026-06-09T00:00:00+01:00"
author: Brandon Visca
tags:
  - linux
  - productivite
  - intermediaire
  - zsh
  - guide
featured: false
draft: false
focusKeyword: zsh plugins essentiels
faqs:
  - question: "Dois-je utiliser Oh My Zsh pour installer ces plugins ?"
    answer: "Non, mais c'est bien plus simple. Sans OMZ, tu dois cloner chaque dépôt manuellement, sourcer les fichiers dans ton .zshrc et gérer les dépendances toi-même. Avec OMZ, c'est un ajout dans le tableau plugins=() et un reload."
  - question: "zsh-autosuggestions et zsh-syntax-highlighting sont-ils inclus dans Oh My Zsh ?"
    answer: "Non, ce sont des plugins tiers qu'il faut installer séparément. Les plugins OMZ natifs comme git, sudo ou extract sont déjà présents dans le dépôt officiel. Les plugins tiers se clonent généralement dans ~/.oh-my-zsh/custom/plugins/."
  - question: "Est-ce que trop de plugins ralentissent le terminal ?"
    answer: "Potentiellement oui, si tu en charges 20 au démarrage. Les 7 plugins de cet article sont légers. Powerlevel10k est beaucoup plus gourmand en comparaison qu'un plugin comme colored-man-pages."
  - question: "Puis-je utiliser ces plugins avec zsh pur, sans Oh My Zsh ?"
    answer: "Oui, absolument. Aucun de ces plugins n'est strictement dépendant d'OMZ. Tu peux les sourcer manuellement dans ton .zshrc. Oh My Zsh n'est qu'un wrapper qui automatise l'installation et le chargement."
  - question: "Comment vérifier quel plugin ralentit mon terminal ?"
    answer: "Ajoute zsh/zprof en début et fin de ton .zshrc, puis lance zsh -i -c exit. Ça affiche un profil de démarrage avec le temps passé dans chaque composant. C'est le meilleur outil de diagnostic."
---
> 💡 **TL;DR**
> - Les plugins Zsh divisent par 10 le nombre de frappes clavier nécessaires au quotidien
> - 3 plugins OMZ natifs indispensables : git, sudo, extract + 2 plugins tiers : autosuggestions et syntax-highlighting
> - Colored-man-pages et command-not-found complètent le combo pour un terminal qui pense à ta place
> - Installation en 10 minutes si tu as déjà [Oh My Zsh](/installation-oh-my-zsh-powerlevel10k-guide-complet/) d'installé

T'as passé un quart d'heure à configurer Oh My Zsh, à choisir un thème clinquant genre Powerlevel10k, et tu te dis que c'est bon, t'as le terminal ultime ? Eh bien non. Le thème, c'est juste la peinture. Les plugins, c'est le moteur. Et si tu roules sans plugins, tu conduis une caisse sans volant assisté ni GPS.

Je vais te montrer les 7 zsh plugins essentiels que j'utilise tous les jours. Ceux qui m'évitent de taper 50 lignes en plus chaque jour, ceux qui m'empêchent d'oublier un sudo quand je suis en mode automatique pilote, et ceux qui détectent mes erreurs avant même que j'appuie sur Entrée.

Avant de commencer, si tu viens d'arriver et que tu n'as pas encore installé Oh My Zsh, j'ai un [guide complet d'installation Oh My Zsh + Powerlevel10k](/installation-oh-my-zsh-powerlevel10k-guide-complet/) qui te met la route. Sur macOS, je passe mes journées dans le terminal, donc j'ai aussi testé les alternatives : mon [comparatif Warp vs iTerm2](/warp-terminal-2025-iterm2-killer-ou-simple-hype-test-complet-ia/) donne mon verdict après deux mois d'usage intensif.

## Table des matières

## Plugin n°1 : git : le cerveau de ton workflow

Ça peut paraître évident, mais le plugin `git` d'Oh My Zsh reste le meilleur gain de productivité au kilo. Sans lui, tu tapes `git status`, `git branch`, `git checkout` à longueur de journée. Avec lui, tout devient un alias de 2 ou 3 caractères.

Voici ceux que j'utilise en boucle :

| Alias | Commande réelle | À quoi ça sert |
|-------|-----------------|----------------|
| `gst` | `git status` | Voir l'état du repo en un coup d'oeil |
| `ga`  | `git add` | Stager un fichier |
| `gc`  | `git commit` | Commiter avec message |
| `gco` | `git checkout` | Changer de branche ou restaurer un fichier |
| `gl`  | `git pull` | Récupérer les changements |
| `gp`  | `git push` | Envoyer sur le remote |
| `gd`  | `git diff` | Voir les différences |
| `glog`| `git log --oneline --decorate --graph`| Historique propre en arbre |

En pratique, quand je travaille sur un projet avec plusieurs branches, je fais `gst` toutes les 30 secondes pour voir l'état, `gco feature/nouveau-truc` pour switcher, `ga .` pour tout stager rapidement, `gc -m "fix: correction du parser"` pour commiter, puis `gp` pour push. Sans ces alias, je passerais mon temps à taper `git` en entier. Le plugin intègre aussi des alias pour `git stash` (`gsta`), `git reset` (`grh`), `git rebase` (`grb`) et `git merge` (`gm`).

Mon préféré reste `glog` qui affiche un arbre Git avec des couleurs et des decorations branch/tag en une ligne compacte. Quand tu bosses en équipe et que tu dois comprendre qui a fait quoi et où les branches ont divergé, c'est indispensable.

Si tu fais beaucoup de `git diff`, `gd` ouvre ton `diff` configuré. Si tu utilises `git diff --cached`, c'est `gdc`. Le nombre d'alias est phénoménal, et ils suivent des conventions mnémoniques cohérentes.

**Installation :** déjà inclus dans OMZ. Tu l'actives dans `~/.zshrc` :

```bash
plugins=(git)
```

## Plugin n°2 : zsh-autosuggestions : la mémoire externe

Celui-là, c'est mon préféré. Quand tu commences à taper une commande, une suggestion transparente apparaît à droite du curseur, grisée. Tu appuies sur la flèche droite et bam, c'est rempli automatiquement.

C'est basé sur ton historique. Si tu as déjà tapé `docker compose up -d --build` la semaine dernière, tu n'as plus qu'à écrire `dock` et la suggestion remplit le reste. C'est de la mémoire à court terme extériorisée.

Le gain de temps est absurde quand tu bosses sur des projets récurrents. `ssh root@mon-serveur-production`, `rsync -avz --delete ./dist/ /var/www/`, `systemctl restart nginx` : tout revient d'un coup. Quand je configure un nouveau serveur, je tapais habituellement `ssh -i ~/.ssh/id_ed25519 deploy@monserveur.com -p 2222`. Après le premier usage, un simple `ssh dep` + flèche droite suffit.

Techniquement, il y a plusieurs stratégies de suggestion : `history` (défaut, basé sur l'historique global), `completion` (basé sur les résultats de completion Zsh), et `match_prev_cmd` (suggère des commandes similaires au contexte actuel). La plupart des utilisateurs restent sur `history` qui est la plus intuitive.

**Installation (manuelle) :**

```bash
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
```

Ensuite, ajoute-le dans ton `.zshrc` :

```bash
plugins=(git zsh-autosuggestions)
```

Pour configurer la couleur de la suggestion (par défaut c'est trop clair sur certains fonds), ajoute dans ton `.zshrc` après le chargement d'OMZ :

```bash
ZSH_AUTOSUGGEST_HIGHLIGHT_STYLE="fg=8"
```

## Plugin n°3 : zsh-syntax-highlighting : le correcteur préventif

Ce plugin colore chaque partie de ta commande en temps réel pendant que tu tapes. Les commandes valides passent au vert, les chemins existants au bleu, les chaines au rouge. Si tu te trompes dans le nom d'une commande, elle reste rouge, et tu le vois avant même d'appuyer sur Entrée.

C'est un tampon anti-bêtise incroyable. Tu tapes `gut status` ? Reste rouge. `cd /var/wwww/nginx` ? Le chemin est rouge parce qu'il n'existe pas. `rm -rf / tmp/fichier` ? Tu vois immédiatement l'espace parasite avant le slash.

C'est aussi pédagogique. Quand tu découvres une nouvelle commande avec des arguments complexes, le coloriage t'aide à comprendre la structure sans passer 10 minutes sur la doc.

**Installation (manuelle) :**

```bash
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
```

Dans `.zshrc` :

```bash
plugins=(git zsh-autosuggestions zsh-syntax-highlighting)
```

Attention : ce plugin doit être le dernier de la liste. Oui, l'ordre compte dans le chargement Zsh.

## Plugin n°4 : sudo : quand tu oublies systématiquement

Tu tapes une commande longue et complexe genre `apt update && apt upgrade -y`, tu appuies sur Entrée, et là le terminal te crache sa moutarde : "Permission denied". Tu as oublié le `sudo` au début.

Sans plugin, tu dois soit re-taper toute la commande avec `sudo` devant, soit faire `sudo !!` qui répète la commande précédente. Avec le plugin `sudo` d'OMZ, tu appuies simplement deux fois sur la touche Échap (ou une fois sur Alt+S selon ta config), et `sudo` s'insère automatiquement au début de la ligne.

```bash
$ apt update && apt upgrade -y
Permission denied
$ [appuie deux fois sur Échap]
$ sudo apt update && apt upgrade -y
```

Ça paraît anodin, mais quand ça t'arrive 15 fois par jour parce que tu switches entre ton user normal et des tâches d'admin, ces deux frappes économisées font la différence. C'est un plugin OMZ natif, zéro config, zéro overhead.

**Installation :**

```bash
plugins=(git zsh-autosuggestions zsh-syntax-highlighting sudo)
```

## Plugin n°5 : extract : une commande pour tout décompresser

Tu télécharges un fichier, tu dois l'extraire, et là commence le jeu des formats. `.tar.gz` ? Il faut `tar xzvf`. `.zip` ? C'est `unzip`. `.tar.bz2` ? `tar xjvf`. `.7z` ? Il faut p7zip. Tu passes ton temps à rechercher la syntaxe exacte sur Stack Overflow, surtout quand le flag `-f` de tar change selon que le fichier est au format gzip, bzip2 ou xz.

Le plugin `extract` d'Oh My Zsh résout ça définitivement. Tu tapes `extract monfichier.tar.gz`, `extract monfichier.zip`, `extract monfichier.7z`, peu importe le format, il détecte et extrait automatiquement.

Les formats supportés incluent : tar, gz, bz2, zip, rar, 7z, deb, rpm, jar, ear, war, iso et même les `.dmg` sur macOS. C'est OMZ natif, ça marche out of the box, et ça remplace une demi-douzaine de neurones que tu consacrais à mémoriser des syntaxes d'extraction.

Petite nuance cependant : `extract` ne fait que décompresser. Si tu décompresses un tar.gz et que tu veux le repackager, pas de plugin miracle, il faut retourner à `tar czvf`. Mais pour la lecture archivage, c'est le jour et la nuit.

**Installation :**

```bash
plugins=(git zsh-autosuggestions zsh-syntax-highlighting sudo extract)
```

## Plugin n°6 : command-not-found : le correcteur orthographique du terminal

Tu tapes `htop` et le système te répond "commande introuvable". Tu ne sais pas si c'est un paquet manquant ou si tu as fait une faute de frappe. Le plugin `command-not-found` te dit exactement quel paquet installer pour obtenir cette commande.

```bash
$ htop
zsh: command not found: htop
The program 'htop' is currently not installed. You can install it by typing:
sudo apt install htop
```

C'est particulièrement utile sur des machines neuves ou des conteneurs Docker minimalistes où tu ne sais jamais ce qui est préinstallé, typiquement quand tu débarques sur un serveur fraîchement provisionné pour le [durcir avec quelques commandes de base](/hardening-linux-10-commandes/). Au lieu de chercher pendant dix minutes, tu as la réponse instantanément.

**Installation (plugin natif OMZ) :**

```bash
plugins=(git zsh-autosuggestions zsh-syntax-highlighting sudo extract command-not-found)
```

## Plugin n°7 : colored-man-pages : la doc lisible enfin

Les pages de manuel, c'est pratique, mais visuellement c'est le désert. Un bloc de texte monochrome de 500 lignes sur fond noir, sans hiérarchie, sans couleur pour distinguer les sections des options. Le plugin `colored-man-pages` applique une coloration syntaxique aux man pages : les titres de sections en gras, les options en couleur, les chemins highlightés.

Le résultat ? Tu trouves l'information 3 fois plus vite. Quand tu cherches la syntaxe d'une option particulière dans `man rsync` ou `man sshd_config`, les yeux accrochent immédiatement sur les sections colorées. C'est un plugin OMZ natif, zéro config, et il rend la doc utilisable au lieu de la subir.

**Installation (plugin natif OMZ) :**

```bash
plugins=(git zsh-autosuggestions zsh-syntax-highlighting sudo extract command-not-found colored-man-pages)
```

Après tout ça, reload le shell :

```bash
source ~/.zshrc
```

## Ma config perso complète pour copier-coller

Voici à quoi ressemble la ligne `plugins` dans mon `.zshrc` au quotidien :

```bash
plugins=(
  git
  zsh-autosuggestions
  zsh-syntax-highlighting
  sudo
  extract
  command-not-found
  colored-man-pages
)
```

Et le bloc de configuration associé :

```bash
# Couleur des suggestions (gris foncé)
ZSH_AUTOSUGGEST_HIGHLIGHT_STYLE="fg=8"

# Accepter une suggestion avec la flèche droite
bindkey "^[[C" forward-char
```

## Pourquoi pas plus de plugins ?

Tu peux charger 15 plugins si tu veux. Mais chaque plugin ajoute du temps de démarrage. Oh My Zsh est déjà assez lourd à l'origine. Les 7 plugins ci-dessus sont choisis pour leur ratio gain/temps d'exécution maximal.

Si tu veux vérifier ce qui ralentit ton terminal, ajoute ça en haut de ton `.zshrc` :

```bash
zmodload zsh/zprof
```

Et ça en bas :

```bash
zprof
```

Relance un terminal, et tu auras un profil complet du temps passé dans chaque composant. C'est le meilleur outil pour auditer ta config.

J'ai testé des plugins comme `web-search`, `thefuck`, `copypath` au fil du temps. Certains sont sympas mais ajoutent du bruit pour peu de gain. Ceux que je mentionne ici sont ceux qui survivent à l'épreuve du temps dans mon workflow quotidien.

`thefuck` par exemple corrige ta commande précédente quand tu fais une faute de frappe. Tu tapes `gut status`, une seconde plus tard tu te tapes le front, tu écris `fuck` et il corrige en `git status`. C'est marrant cinq minutes, mais tu passes ton temps à écrire `fuck` dans ton terminal en visio-conférence, ce qui n'est pas toujours idéal dans un contexte professionnel.

`copypath` copie le chemin absolu du fichier sous le curseur dans le presse-papiers. `web-search` lance une recherche Google depuis le terminal. Ce sont des gadgets plus que des outils indispensables.

Le plugin `fzf` mérite une mention honorable. Il transforme `Ctrl+R` en interface floue pour chercher dans ton historique. C'est extrêmement puissant, mais il faut installer `fzf` en plus, et il change radicalement l'expérience de recherche historique. Si tu veux aller plus loin, c'est probablement la prochaine étape après les 7 plugins de base.

Ce que je retiens de tout ça : un plugin vaut le coup quand il supprime une friction que tu rencontres plusieurs fois par jour. Pas quand il fait quelque chose de cool une fois par mois.

## Conclusion

Un terminal bien configuré, ce n'est pas juste un prompt joli avec des icônes. C'est un environnement qui anticipe tes besoins, qui corrige tes erreurs avant qu'elles n'arrivent, et qui te fait économiser des centaines de frappes clavier chaque semaine.

Les 7 plugins que je viens de te présenter ne demandent pas de réapprendre des raccourcis impossibles. Ils s'intègrent naturellement dans ce que tu fais déjà. Tu vas les oublier comme installés, et tu vas les manquer immédiatement si tu dois travailler sur une machine sans eux.

Installe-les, teste-les une semaine, et dis-moi lequel est devenu indispensable pour toi. Mon pronostic : ce sera `zsh-autosuggestions` pour 90% des lecteurs. Et pour les 10% restants, `sudo`.

## Pour aller plus loin

- [Installer Oh My Zsh + Powerlevel10k : le guide complet](/installation-oh-my-zsh-powerlevel10k-guide-complet/), la base à avoir avant ces plugins
- [Warp vs iTerm2 : mon comparatif après deux mois](/warp-terminal-2025-iterm2-killer-ou-simple-hype-test-complet-ia/), quel terminal pour héberger tout ça
- [Documentation officielle des plugins Oh My Zsh](https://github.com/ohmyzsh/ohmyzsh/wiki/Plugins), la liste exhaustive des plugins natifs
