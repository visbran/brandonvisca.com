#!/usr/bin/env python3
"""
Ajoute le bloc faqs: dans le frontmatter des articles qui n'en ont pas.
FAQs rédigées manuellement selon le titre + description + focusKeyword.
"""

import os, re, sys, yaml

BLOG_DIR = "src/data/blog"

# Format YAML du bloc faqs à injecter par slug
FAQS = {
    "10-outils-low-tech-macos-guide-complet": [
        ("Ces outils fonctionnent-ils sur Apple Silicon (M1/M2/M3/M4) ?",
         "Oui, tous les outils listés sont compilés nativement pour Apple Silicon. Aucune émulation Rosetta 2 nécessaire."),
        ("Puis-je les installer tous d'un coup via Homebrew ?",
         "Oui. Un Brewfile généré depuis ces outils permet d'installer tout l'environnement en une commande : brew bundle --file=Brewfile."),
        ("Ces outils sont-ils compatibles avec macOS Sequoia (2025) ?",
         "Oui, la liste a été vérifiée sur macOS Sequoia. Chaque outil est maintenu activement et reçoit des mises à jour régulières."),
    ],
    "activedirectory-transfere-des-roles-fsmo": [
        ("Peut-on transférer les rôles FSMO sans redémarrer le serveur ?",
         "Oui. Le transfert FSMO via ntdsutil ou PowerShell s'effectue à chaud, sans redémarrage du contrôleur de domaine source ni cible."),
        ("Que se passe-t-il si le DC portant les rôles FSMO tombe définitivement ?",
         "Il faut alors procéder à une saisie forcée (seize) des rôles depuis ntdsutil. Cette opération est irréversible — l'ancien DC ne peut plus rejoindre le domaine ensuite."),
        ("Combien de contrôleurs de domaine faut-il avant de redistribuer les rôles FSMO ?",
         "Au minimum 2 DC. Microsoft recommande de répartir les 5 rôles sur 2 DC : PDC Emulator + RID Master + Infrastructure Master sur le DC principal, Schema Master + Domain Naming Master sur le second."),
    ],
    "cling-recherche-fuzzy-fichiers-macos": [
        ("Cling est-il gratuit ?",
         "Oui, Cling est entièrement gratuit et open source. Il est disponible sur le Mac App Store et sur GitHub."),
        ("Quelle est la différence entre Cling et Spotlight ?",
         "Spotlight utilise une correspondance exacte des termes. Cling utilise la recherche fuzzy : tu peux taper des mots approximatifs, avec des fautes ou dans le désordre, et Cling trouve quand même le fichier."),
        ("Cling indexe-t-il les fichiers dans les dossiers cachés ou les volumes externes ?",
         "Par défaut, Cling cherche dans les emplacements standards de macOS. Tu peux configurer les dossiers indexés dans les préférences pour inclure volumes externes et dossiers personnalisés."),
    ],
    "clop-compression-images-videos-macos": [
        ("Clop est-il gratuit ?",
         "Clop est gratuit avec des fonctionnalités de base. Une version Pro (paiement unique ~15€) débloque la compression illimitée et les préréglages avancés."),
        ("Quels formats d'images et vidéos Clop supporte-t-il ?",
         "Clop supporte PNG, JPEG, WebP, GIF, HEIC pour les images, et MP4, MOV, AVI pour les vidéos. Il convertit aussi automatiquement vers WebP si configuré."),
        ("Clop compresse-t-il avec perte ou sans perte ?",
         "Les deux modes sont disponibles. Par défaut, Clop utilise une compression avec perte légère (qualité ~85%) invisible à l'œil nu mais qui réduit la taille de 50 à 80%."),
    ],
    "configuration-avancee-snipeit-ldap-teams-automatisation": [
        ("Faut-il une version payante de Snipe-IT pour utiliser LDAP ?",
         "Non. L'intégration LDAP/Active Directory est incluse dans la version open source gratuite de Snipe-IT. Aucun abonnement n'est requis."),
        ("Peut-on synchroniser Snipe-IT avec Active Directory en temps réel ?",
         "Pas en temps réel natif. La sync LDAP est déclenchée manuellement ou via cron job. Les modifications AD (nouveaux comptes, départs) sont importées au prochain cycle de synchronisation."),
        ("Les notifications Teams nécessitent-elles un abonnement Microsoft 365 ?",
         "Non. Les notifications passent par les webhooks entrants Teams, disponibles dans tous les plans Microsoft 365 y compris les plans gratuits Teams Essentials."),
    ],
    "content-security-policy-nginx-sans-casser-site": [
        ("Comment tester une CSP sans risquer de casser le site en production ?",
         "Utilise d'abord le header Content-Security-Policy-Report-Only avec une URL report-uri. Le navigateur signale les violations sans bloquer quoi que ce soit, ce qui te permet d'ajuster la politique avant de l'activer."),
        ("Ma CSP bloque Google Analytics ou Google Tag Manager, que faire ?",
         "Ajoute les domaines Google aux directives script-src et connect-src : 'https://www.googletagmanager.com' et 'https://www.google-analytics.com'. Pour GTM, le nonce-based CSP est la solution la plus propre."),
        ("Une CSP protège-t-elle contre toutes les attaques XSS ?",
         "Non, la CSP est une couche de défense supplémentaire, pas une solution complète. Elle réduit fortement l'impact d'une XSS en empêchant l'exécution de scripts non autorisés, mais ne remplace pas la validation des entrées."),
    ],
    "depannage-montage-partition-raid-linux-mode-secours": [
        ("Peut-on monter un RAID mdadm dégradé avec un seul disque fonctionnel ?",
         "Oui. La commande mdadm --assemble --force /dev/md0 /dev/sda1 force l'assemblage en mode dégradé. Le RAID est montable en lecture, mais rebuilder immédiatement sur un nouveau disque est impératif."),
        ("Comment identifier les membres d'un RAID en mode secours sans /etc/mdadm.conf ?",
         "Utilise mdadm --examine /dev/sdX sur chaque disque. La sortie affiche l'UUID du RAID, le nombre de membres et l'état de chaque disque. Tu peux reconstruire le tableau même sans configuration sauvegardée."),
        ("La commande mount -t ext4 échoue avec wrong fs type, que signifie cette erreur ?",
         "Cette erreur signifie que le système de fichiers n'est pas directement sur /dev/md0, mais sur une partition du RAID (ex: /dev/md0p1). Vérifie avec lsblk ou fdisk -l /dev/md0 pour voir les partitions du volume RAID."),
    ],
    "exploration-de-super-so-un-outil-de-site-web-personnalise-pour-notion": [
        ("Super.so est-il gratuit ?",
         "Super.so propose un essai gratuit de 14 jours. Ensuite, les plans payants commencent à 16$/mois (Basic) ou 24$/mois (Pro) avec domaine personnalisé, SEO avancé et analytics."),
        ("Peut-on utiliser Super.so avec un domaine personnalisé ?",
         "Oui, à partir du plan Basic. Tu configures ton DNS pour pointer vers les serveurs Super.so et le site est accessible sur ton domaine en quelques minutes."),
        ("Super.so est-il une bonne alternative à WordPress ou Ghost ?",
         "Pour un site vitrine ou un blog léger, oui. Super.so est idéal si ton contenu est déjà dans Notion. Pour un site e-commerce ou avec des plugins complexes, WordPress reste plus adapté."),
    ],
    "import-pst-outlook-365-guide-complet": [
        ("Peut-on importer un PST dans Outlook 365 sans installer le client lourd (desktop) ?",
         "Non, l'import PST natif nécessite Outlook desktop (Windows ou Mac). Outlook Web (OWA) ne supporte pas l'import PST. Des outils tiers comme XstReader permettent de lire un PST sans Outlook."),
        ("Quelle est la taille maximale d'un fichier PST supportée par Outlook 365 ?",
         "Outlook 365 supporte les PST jusqu'à 50 Go. Au-delà, l'import peut échouer ou être très lent. La recommandation Microsoft est de scinder les gros PST avant import."),
        ("Comment lire un fichier PST sans avoir Outlook installé ?",
         "XstReader (gratuit, open source) permet de lire les PST et OST sur Windows et Linux sans Outlook. Il supporte la recherche, l'export en EML et l'affichage des pièces jointes."),
    ],
    "independance-numerique-2025-guide-complet": [
        ("Quel serveur minimum pour faire tourner Nextcloud + Jellyfin + Vaultwarden ?",
         "Un Raspberry Pi 5 (8 Go RAM) ou un mini PC type Beelink (N100, 16 Go RAM) suffit pour un usage familial. Pour Jellyfin avec transcodage, prévoir un CPU avec Quick Sync ou une GPU dédiée."),
        ("Faut-il une adresse IP fixe pour auto-héberger ses services ?",
         "Non obligatoire. Des solutions comme Cloudflare Tunnel ou Tailscale permettent d'exposer ses services sans IP fixe ni ouverture de ports sur le routeur."),
        ("L'auto-hébergement est-il aussi fiable que Google Drive ou Gmail ?",
         "La fiabilité dépend de votre infrastructure. Avec des sauvegardes 3-2-1 et une alimentation ondulée (UPS), un homelab bien configuré peut atteindre 99.9% d'uptime. Google garantit 99.9% en SLA."),
    ],
    "installation-theme-vim-guide": [
        ("Le thème Catppuccin fonctionne-t-il dans un terminal sans interface graphique ?",
         "Oui, à condition que ton terminal supporte les 256 couleurs ou True Color. Ajoute set termguicolors dans ton .vimrc et vérifie que TERM=xterm-256color est défini."),
        ("Mon terminal n'affiche pas les bonnes couleurs après l'installation, pourquoi ?",
         "Le problème vient généralement de la variable TERM mal configurée. Assure-toi que ton terminal est déclaré comme xterm-256color ou tmux-256color si tu utilises tmux. Dans .vimrc : set t_Co=256."),
        ("Catppuccin est-il compatible avec NeoVim ?",
         "Oui. Il existe un plugin Catppuccin dédié à NeoVim (catppuccin/nvim) optimisé pour Lua et les plugins NeoVim modernes comme Telescope, Treesitter et LSP."),
    ],
    "installation-vim-guide-complet": [
        ("Quelle est la différence entre Vim et NeoVim ?",
         "NeoVim est un fork de Vim avec une architecture moderne : support Lua natif, LSP intégré, async par défaut et une API plus riche. Vim reste plus léger. Pour débuter, Vim est suffisant ; NeoVim s'impose pour un IDE complet."),
        ("vim-plug vs Vundle vs Lazy.nvim : lequel choisir ?",
         "Pour Vim classique, vim-plug est le gestionnaire le plus populaire : simple, rapide, supporte l'installation en parallèle. Vundle est obsolète. Pour NeoVim, Lazy.nvim est le standard actuel."),
        ("Comment sauvegarder et synchroniser ma configuration Vim entre machines ?",
         "Versionne ton .vimrc (et le dossier ~/.vim/plugged si nécessaire) dans un dépôt Git de dotfiles. Une commande git pull + vim +PlugInstall recrée l'environnement complet sur n'importe quelle machine."),
    ],
    "itsm-snipeit-alternative-excel-inventaire-it": [
        ("Snipe-IT est-il vraiment gratuit, même pour une entreprise ?",
         "Oui, Snipe-IT est open source (AGPL v3) et gratuit à auto-héberger sans limite d'actifs ni d'utilisateurs. Une version cloud hébergée est disponible à partir de 39,99$/mois si tu ne veux pas gérer l'infra."),
        ("Peut-on importer un inventaire Excel existant dans Snipe-IT ?",
         "Oui. Snipe-IT propose un import CSV natif. Il suffit de mapper les colonnes de ton Excel (nom, numéro de série, modèle, assignation) avec les champs Snipe-IT et d'importer le fichier depuis l'interface admin."),
        ("Combien d'actifs IT peut-on gérer avec Snipe-IT ?",
         "Il n'y a pas de limite technique. Des déploiements en production gèrent des dizaines de milliers d'actifs. La seule limite est les ressources du serveur qui héberge l'instance."),
    ],
    "ladybird-browser-le-navigateur-web-qui-refuse-de-se-soumettre-a-google-et-tant-mieux": [
        ("Ladybird est-il disponible au téléchargement aujourd'hui ?",
         "Des builds de développement sont disponibles sur GitHub pour Linux et macOS, mais Ladybird n'est pas encore prêt pour un usage quotidien. La première release stable est prévue pour 2026."),
        ("Ladybird utilise-t-il WebKit, Blink ou son propre moteur ?",
         "Ladybird utilise LibWeb, un moteur de rendu développé from scratch dans le cadre du projet SerenityOS. Il ne dépend ni de Blink (Chrome) ni de WebKit (Safari), ni de Gecko (Firefox)."),
        ("Ladybird accepte-t-il les extensions Chrome ou Firefox ?",
         "Non. Ladybird n'est pas compatible avec les extensions Chrome (Manifest V3) ni Firefox. Sa propre API d'extensions n'est pas encore définie — c'est prévu après la release stable de 2026."),
    ],
    "lunar-luminosite-ecrans-externes-macos": [
        ("Lunar est-il gratuit ?",
         "Lunar propose une version gratuite avec les fonctionnalités DDC de base. La version Pro (paiement unique ~23€) débloque le mode Adaptatif, la synchronisation multi-écrans et les automatisations avancées."),
        ("Mon écran n'est pas compatible DDC, Lunar peut-il quand même contrôler la luminosité ?",
         "Oui. Lunar propose un mode Overlay (gamma software) qui simule la réduction de luminosité via un calque sombre. Ce n'est pas aussi précis que DDC mais ça fonctionne sur n'importe quel écran."),
        ("Lunar fonctionne-t-il avec plusieurs écrans externes différents ?",
         "Oui. Lunar gère chaque écran indépendamment avec ses propres profils. Tu peux synchroniser la luminosité de tous les écrans ou les contrôler individuellement selon tes préférences."),
    ],
    "music-decoy-macos-bloquer-apple-music": [
        ("Music Decoy est-il totalement gratuit ?",
         "Oui, Music Decoy est gratuit et open source (disponible sur GitHub). Il ne demande aucun abonnement ni paiement unique."),
        ("Music Decoy bloque-t-il uniquement Apple Music ou aussi Spotify ?",
         "Music Decoy cible spécifiquement Apple Music (et l'ancienne app iTunes). Il s'enregistre comme handler par défaut de la touche Play pour intercepter les événements avant qu'Apple Music ne les reçoive."),
        ("Faut-il laisser Music Decoy dans les éléments de connexion macOS ?",
         "Oui. Music Decoy doit être actif en arrière-plan pour intercepter les touches média. Ajoute-le dans Réglages Système > Général > Éléments de connexion pour qu'il démarre automatiquement."),
    ],
    "nebula-sync-pihole-v6-installation-docker-guide": [
        ("Nebula-Sync est-il compatible avec Pi-hole v5 ?",
         "Non. Nebula-Sync est conçu spécifiquement pour Pi-hole v6 qui a changé son architecture d'API. Pour Pi-hole v5, utilise Gravity Sync qui reste compatible avec l'ancienne version."),
        ("Que se passe-t-il si le Pi-hole principal tombe pendant la synchronisation ?",
         "La synchronisation est unidirectionnelle (principal → réplicas). Si le principal est indisponible, les réplicas continuent de filtrer avec leur dernière liste synchronisée. Aucune donnée n'est perdue."),
        ("Peut-on synchroniser plus de 2 Pi-hole avec Nebula-Sync ?",
         "Oui. Nebula-Sync supporte un nombre illimité de réplicas. Il suffit d'ajouter les IPs et tokens API de chaque instance Pi-hole dans la configuration YAML."),
    ],
    "nextcloud-docker-installation-complete-2025": [
        ("Quelle quantité de RAM est nécessaire pour Nextcloud avec Docker ?",
         "Le minimum recommandé est 2 Go de RAM pour une instance personnelle. Pour 5-10 utilisateurs avec Office Online (Collabora), prévoir 4 Go minimum. 8 Go pour un usage familial confortable."),
        ("Peut-on accéder à Nextcloud depuis l'extérieur sans IP fixe ?",
         "Oui, via Cloudflare Tunnel (gratuit) ou Tailscale. Ces solutions évitent d'ouvrir des ports sur ton routeur et fonctionnent même avec une IP dynamique fournie par ton FAI."),
        ("Comment migrer mes fichiers depuis Google Drive vers Nextcloud ?",
         "Nextcloud propose une app officielle 'External Storage' pour importer depuis Google Drive. L'outil rclone permet aussi une migration batch en ligne de commande avec détection des doublons."),
    ],
    "nginx-location-bloc-et-securite": [
        ("Quelle est la priorité entre un bloc location exact (=) et un bloc regex ?",
         "L'ordre de priorité Nginx est : 1) location = (exact), 2) location ^~ (préfixe prioritaire), 3) location ~ ou ~* (regex, premier match gagne), 4) location /prefix (préfixe le plus long). Les blocs = court-circuitent toute évaluation regex."),
        ("Un bloc location s'applique-t-il récursivement aux sous-dossiers ?",
         "Non par défaut. Un bloc location /api/ s'applique à /api/ et ses sous-chemins (/api/v1/, /api/users/...) mais chaque sous-chemin peut être surchargé par un bloc location plus spécifique."),
        ("Comment déboguer un bloc location qui ne semble pas s'appliquer ?",
         "Active les logs de debug Nginx (error_log /var/log/nginx/debug.log debug;) et utilise nginx -T pour voir la configuration compilée. L'outil nginx-config-validator permet aussi de tester les règles de matching."),
    ],
    "nginx-permissions-policy-anti-bot": [
        ("Le header Permissions-Policy remplace-t-il l'ancien Feature-Policy ?",
         "Oui. Permissions-Policy est le successeur standardisé de Feature-Policy. La syntaxe a changé (plus de guillemets, nouvelle notation) mais le concept est identique. Feature-Policy est déprécié depuis Chrome 88."),
        ("Comment bloquer les bots sans affecter les vrais utilisateurs avec Permissions-Policy ?",
         "Permissions-Policy contrôle les APIs navigateur (caméra, micro, géolocalisation), pas le trafic bot. Pour bloquer les bots, combiner fail2ban sur les logs Nginx + règles de rate limiting + Cloudflare Bot Management."),
        ("Peut-on tester ma Permissions-Policy sans la mettre en production ?",
         "Oui. Dans Chrome DevTools, l'onglet Application > Permissions Policy affiche les permissions autorisées et bloquées sur la page courante. L'extension Security Headers permet aussi d'analyser les headers en temps réel."),
    ],
    "omarchy-distribution-linux-arch-hyprland": [
        ("Omarchy est-il compatible avec les cartes graphiques AMD et Intel (sans Nvidia) ?",
         "Oui. Omarchy est développé et testé principalement sur AMD (RDNA) et Intel (Iris Xe). Le support Nvidia existe mais est moins stable avec Hyprland sous Wayland — préférer les cartes AMD ou Intel."),
        ("Peut-on installer Omarchy sur une machine existante sans réinstaller Arch ?",
         "Omarchy est conçu comme une installation complète sur Arch Linux. Un script d'installation automatise tout depuis une Arch minimale. L'appliquer sur un Arch déjà configuré est possible mais non officiel."),
        ("Omarchy fonctionne-t-il bien sur laptop avec gestion de batterie ?",
         "Oui. Omarchy inclut power-profiles-daemon et auto-cpufreq pour la gestion d'énergie. La consommation en idle est comparable à d'autres distros Wayland modernes."),
    ],
    "proteger-nginx-fichiers-sensibles-et-uploads": [
        ("Faut-il recharger Nginx après chaque modification de configuration ?",
         "Oui. Utilise nginx -t pour valider la syntaxe, puis systemctl reload nginx (ou nginx -s reload) pour appliquer sans coupure de service. Le reload est graceful : les connexions actives ne sont pas interrompues."),
        ("Comment vérifier qu'un fichier sensible (.env, .git) est bien bloqué par Nginx ?",
         "Teste avec curl -I https://ton-site.com/.env. La réponse doit être 403 Forbidden ou 404 Not Found, jamais 200. Utilise aussi nikto -h ton-site.com pour un scan automatique des fichiers exposés."),
        ("Mon répertoire uploads autorise-t-il l'exécution PHP par défaut sur Nginx ?",
         "Avec Nginx seul : non, Nginx ne traite pas PHP sans configuration explicite (fastcgi_pass). Mais si php-fpm est configuré globalement, les scripts dans uploads/ peuvent être exécutés — il faut donc bloquer explicitement l'exécution dans ce dossier."),
    ],
    "quitter-google-auto-hebergement": [
        ("Combien coûte une infrastructure auto-hébergée par mois ?",
         "Entre 5€ et 20€/mois en électricité pour un mini PC ou Raspberry Pi. Un VPS chez Hetzner (2 vCPU, 4 Go RAM) coûte ~4€/mois et convient pour Nextcloud + Vaultwarden. Contre 60 à 120€/an pour Google One + 1Password + Plex."),
        ("Faut-il des compétences avancées en Linux pour quitter Google ?",
         "Les bases suffisent : savoir utiliser un terminal, éditer un fichier de configuration, lancer docker compose up. Des guides comme celui-ci couvrent chaque étape. L'apprentissage se fait progressivement."),
        ("L'auto-hébergement est-il aussi fiable que les services Google ?",
         "Avec de bonnes sauvegardes (règle 3-2-1) et une UPS, un homelab bien configuré peut atteindre 99.5 à 99.9% d'uptime. La différence principale : la maintenance est de ta responsabilité, pas de celle de Google."),
    ],
    "raycast-macos-outil-productivite-ultime": [
        ("Raycast est-il gratuit ?",
         "Oui. Raycast est gratuit avec toutes les fonctionnalités essentielles : launcher, extensions, snippets, clipboard history, window management. Raycast Pro (~8$/mois) ajoute l'IA, la sync cloud et les profils d'équipe."),
        ("Quelle est la différence entre Raycast et Alfred ?",
         "Alfred nécessite un Powerpack (35€ paiement unique) pour les Workflows. Raycast est gratuit avec un store d'extensions open source. Alfred est plus personnalisable niveau scripting ; Raycast a une meilleure UX par défaut et une communauté plus active."),
        ("Raycast remplace-t-il complètement Spotlight ?",
         "Oui. Raycast peut être configuré pour remplacer ⌘Space et prend en charge la recherche de fichiers, les calculs, les conversions et les actions système. Spotlight peut être désactivé sans perdre de fonctionnalité."),
    ],
    "reduire-taille-images-mac-webp": [
        ("La conversion en WebP dégrade-t-elle la qualité des images ?",
         "WebP avec qualité 85 (paramètre par défaut de cwebp) est visuellement identique au JPEG équivalent pour l'œil humain, avec 25 à 35% de taille en moins. WebP supporte aussi le mode lossless pour une qualité 100% préservée."),
        ("Safari et iOS supportent-ils bien le format WebP ?",
         "Oui, depuis Safari 14 (2020) et iOS 14. WebP est aujourd'hui supporté par tous les navigateurs modernes. Si tu dois supporter IE11 ou Safari < 14, prévois un fallback JPEG via la balise <picture>."),
        ("Peut-on convertir plusieurs images en batch avec cette méthode ?",
         "Oui. La méthode Automator décrite dans l'article traite une sélection de fichiers en batch. Pour des milliers d'images, un script shell avec une boucle for sur cwebp est plus rapide."),
    ],
    "securiser-nginx-avec-headers-http": [
        ("Ces headers HTTP causent-ils des problèmes avec WordPress ou Prestashop ?",
         "Certains oui. X-Frame-Options: DENY bloque les iframes — à remplacer par SAMEORIGIN pour les back-offices. Le header CSP est celui qui casse le plus souvent les plugins tiers : déployer en Report-Only d'abord."),
        ("Faut-il appliquer ces headers sur tous les virtual hosts Nginx ?",
         "Recommandé. Place les headers dans un fichier snippet (/etc/nginx/snippets/security-headers.conf) et inclus-le dans chaque virtual host avec include snippets/security-headers.conf;. Cela évite la duplication."),
        ("Comment vérifier que mes headers HTTP sont bien actifs sur mon site ?",
         "Utilise securityheaders.com (scan gratuit) ou curl -I https://ton-site.com | grep -i 'x-frame\\|strict\\|content-security'. Tu peux aussi inspecter l'onglet Réseau de Chrome DevTools sur n'importe quelle page."),
    ],
    "sendme-cli-transfert-fichiers-p2p-terminal": [
        ("Sendme fonctionne-t-il derrière un NAT strict ou un pare-feu d'entreprise ?",
         "Oui. Sendme utilise le protocole QUIC avec traversée NAT automatique via STUN/TURN. Dans les environnements très restrictifs, seul le port 443 en sortie est nécessaire."),
        ("Le transfert Sendme est-il chiffré de bout en bout ?",
         "Oui. Sendme utilise le chiffrement TLS 1.3 avec vérification d'intégrité BLAKE3 sur chaque chunk. Ni le serveur de relais ni un observateur réseau ne peut lire le contenu transféré."),
        ("Y a-t-il une limite de taille de fichier avec Sendme ?",
         "Pas de limite théorique. Sendme transfère les fichiers par chunks et supporte la reprise après coupure. Des transferts de plusieurs dizaines de Go ont été testés avec succès."),
    ],
    "snipeagent-automatiser-inventaire-windows-snipeit": [
        ("SnipeAgent fonctionne-t-il sans Active Directory ?",
         "Oui. SnipeAgent est un agent standalone qui s'exécute localement sur chaque machine Windows. Il ne dépend pas d'AD pour collecter et envoyer l'inventaire à Snipe-IT via l'API REST."),
        ("Peut-on déployer SnipeAgent sur tout un parc Windows via GPO ?",
         "Oui. SnipeAgent peut être packagé en MSI et déployé via une GPO d'installation de logiciel ou via un script PowerShell GPO. Le déploiement en masse sur des centaines de machines est documenté dans l'article."),
        ("SnipeAgent détecte-t-il les logiciels installés en plus du matériel ?",
         "Oui. SnipeAgent remonte le matériel (CPU, RAM, disques, carte réseau), le système d'exploitation (version, build, clé produit) et les logiciels installés (via le registre Windows)."),
    ],
    "uptime-kuma-2-0-monitoring-auto-heberge": [
        ("Uptime Kuma 2.0 est-il rétrocompatible avec les données de la version 1 ?",
         "Oui, avec migration. Uptime Kuma 2.0 fournit un outil de migration officiel qui convertit la base SQLite v1 vers MariaDB v2. La migration est documentée dans l'article avec les commandes exactes."),
        ("Combien de moniteurs peut-on créer gratuitement avec Uptime Kuma ?",
         "Il n'y a pas de limite. Uptime Kuma est open source et auto-hébergé — tu peux créer autant de moniteurs que ton serveur le permet. Des instances en prod surveillent plusieurs centaines de services."),
        ("Uptime Kuma supporte-t-il les alertes Telegram, Discord et Slack ?",
         "Oui. Uptime Kuma propose plus de 90 intégrations natives : Telegram, Discord, Slack, Teams, PagerDuty, email SMTP, ntfy, Signal et bien d'autres. Tout se configure depuis l'interface web sans fichier de config."),
    ],
    "uptimerobot-guide-complet-monitoring-infrastructure": [
        ("UptimeRobot est-il gratuit ?",
         "Oui. Le plan gratuit inclut 50 moniteurs, une vérification toutes les 5 minutes, les alertes email et une page de statut publique. Les plans payants (7$/mois) descendent à 1 minute de vérification et ajoutent les SMS."),
        ("Quelle est la fréquence minimale de vérification avec le plan gratuit ?",
         "5 minutes sur le plan gratuit. Les plans Solo (7$/mois) et Team (20$/mois) permettent des vérifications toutes les 60 secondes, essentielles pour les services critiques."),
        ("Peut-on créer une page de statut publique avec UptimeRobot ?",
         "Oui, inclus dans le plan gratuit. UptimeRobot génère une page de statut publique personnalisable avec logo et domaine custom. Elle affiche l'uptime en temps réel et les incidents passés."),
    ],
    "vanderplanki-sauvegarde-emails-gratuit-multiplateforme": [
        ("Vanderplanki supporte-t-il Gmail, Outlook et d'autres fournisseurs ?",
         "Oui. Vanderplanki supporte tous les fournisseurs IMAP standard : Gmail, Outlook, Proton Mail (via bridge), Fastmail, et tout serveur IMAP auto-hébergé (Dovecot, Postfix)."),
        ("Les emails sauvegardés par Vanderplanki sont-ils chiffrés ?",
         "Oui. Vanderplanki chiffre les sauvegardes avec AES-256 avant de les stocker. Seul ton mot de passe (ou clé) permet de déchiffrer les données — même l'équipe Vanderplanki ne peut pas accéder à tes emails."),
        ("Peut-on restaurer des emails depuis une sauvegarde Vanderplanki ?",
         "Oui. La restauration se fait depuis l'interface Vanderplanki : tu sélectionnes les emails ou dossiers à restaurer et les réimporter dans n'importe quel compte IMAP compatible."),
    ],
    "vaultwarden-docker-gestionnaire-mots-de-passe": [
        ("Vaultwarden est-il compatible avec les apps Bitwarden officielles ?",
         "Oui. Vaultwarden implémente l'API Bitwarden complète. Les apps Bitwarden (iOS, Android, Chrome, Firefox, macOS, Windows) se connectent à Vaultwarden en changeant uniquement l'URL du serveur dans les paramètres."),
        ("Faut-il une adresse IP fixe pour héberger Vaultwarden chez soi ?",
         "Non. Cloudflare Tunnel (gratuit) permet d'exposer Vaultwarden sur un domaine HTTPS sans IP fixe ni ouverture de ports. C'est la méthode recommandée pour les connexions depuis l'extérieur."),
        ("Comment migrer de 1Password vers Vaultwarden ?",
         "1Password permet d'exporter au format CSV ou .1pux. Bitwarden/Vaultwarden dispose d'un outil d'import natif qui supporte les exports 1Password, LastPass et KeePass. La migration prend moins de 5 minutes."),
    ],
    "warp-terminal-2025-iterm2-killer-ou-simple-hype-test-complet-ia": [
        ("Warp Terminal est-il gratuit ?",
         "Le plan Team est gratuit pour usage personnel (1 utilisateur). Les fonctionnalités IA (Warp AI, Agent Mode) sont incluses avec un quota mensuel. Des plans payants existent pour les équipes avec partage de Warp Drive."),
        ("Warp Terminal fonctionne-t-il sur Linux ?",
         "Oui. Warp est disponible sur macOS et Linux (Ubuntu, Fedora, Debian). La version Windows est en développement. Les fonctionnalités sont identiques sur les deux plateformes."),
        ("L'IA de Warp envoie-t-elle mes commandes vers le cloud ?",
         "Les commandes tapées dans le terminal ne sont pas envoyées automatiquement. Seules les requêtes explicites à Warp AI (via # ou le panneau IA) transmettent du contenu. Warp publie sa politique de données sur son site."),
    ],
    "wordpress-2-solutions-pour-reparer-une-base-de-donnee-corrompu": [
        ("Comment savoir si ma base de données WordPress est corrompue ?",
         "Les signes typiques : erreur 'Error establishing a database connection', tableaux manquants en phpMyAdmin, ou wp_posts qui n'existe plus. Lance CHECK TABLE wp_posts; dans phpMyAdmin — si le résultat est 'Corrupt', le problème est confirmé."),
        ("Peut-on réparer WordPress sans accès phpMyAdmin ?",
         "Oui. Ajoute define('WP_ALLOW_REPAIR', true); dans wp-config.php puis accède à https://ton-site.com/wp-admin/maint/repair.php. WordPress propose alors une réparation et une optimisation des tables sans phpMyAdmin."),
        ("La réparation de base MySQL WordPress supprime-t-elle des données ?",
         "La réparation (REPAIR TABLE) est non-destructive et tente de reconstruire les tables corrompues. En cas d'échec, la dernière option est la restauration depuis une sauvegarde. Toujours sauvegarder avant toute opération."),
    ],
}


def insert_faqs_in_frontmatter(content, faqs):
    """Insère le bloc faqs: avant la ligne --- de fermeture du frontmatter."""
    lines = content.split("\n")
    # Trouver la fin du frontmatter (deuxième ---)
    fm_end = -1
    count = 0
    for i, line in enumerate(lines):
        if line == "---":
            count += 1
            if count == 2:
                fm_end = i
                break

    if fm_end == -1:
        return content

    # Construire le bloc faqs
    faqs_lines = ["faqs:"]
    for q, a in faqs:
        faqs_lines.append(f'  - question: "{q}"')
        faqs_lines.append(f'    answer: "{a}"')

    new_lines = lines[:fm_end] + faqs_lines + lines[fm_end:]
    return "\n".join(new_lines)


def main(dry_run=False):
    done = 0
    for slug, faqs in FAQS.items():
        path = os.path.join(BLOG_DIR, f"{slug}.md")
        if not os.path.exists(path):
            print(f"  SKIP (not found): {slug}", file=sys.stderr)
            continue

        content = open(path, encoding="utf-8").read()
        if "faqs:" in content:
            print(f"  SKIP (already has faqs): {slug}")
            continue

        new_content = insert_faqs_in_frontmatter(content, faqs)

        if not dry_run:
            open(path, "w", encoding="utf-8").write(new_content)

        print(f"  ✓ {slug} ({len(faqs)} FAQs)")
        done += 1

    print(f"\n{'[DRY RUN] ' if dry_run else ''}{done} articles mis à jour.")


if __name__ == "__main__":
    dry = "--dry-run" in sys.argv or "-n" in sys.argv
    main(dry_run=dry)
