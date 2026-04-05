---
title: "Auto-hébergement : Le guide ultime 2025 pour reprendre contrôle de vos données"
pubDatetime: "2025-10-22T15:44:27+02:00"
description: "Découvrez l'auto-hébergement en 2025 : guide complet pour débutants, du choix du matériel aux premiers services. Reprenez le contrôle de vos données !"
tags:
  - auto-hebergement
  - homelab
  - self-hosting
  - docker
  - nextcloud
  - vaultwarden
  - jellyfin
  - linux
  - guide
  - debutant
---

Tu en as marre de payer Google, Microsoft et Apple pour stocker tes photos de vacances ? Fatigué de voir tes données personnelles transformées en carburant publicitaire ? Envie de comprendre comment fonctionne vraiment un serveur ?

Bienvenue dans le monde de l’**auto-hébergement**.

Spoiler : c’est moins compliqué que tu le crois, et une fois que tu auras goûté à la liberté d’héberger tes propres services, tu ne pourras plus revenir en arrière.

TL;DR : L’auto-hébergement en 3 points
--------------------------------------

- **C’est quoi ?** Héberger soi-même ses services (cloud, mail, sites…) au lieu de dépendre de Google/Microsoft
- **Pour qui ?** Débutants curieux, passionnés de tech, admins qui veulent apprendre
- **Budget ?** De 0€ (vieux PC) à 50€/mois (VPS pro)

----------
## Table des matières


- [L’auto-hébergement, c’est quoi exactement ?](#lauto-hebergement-cest-quoi-exactement)
  - [Pourquoi les gens s’y mettent en 2025 ?](#pourquoi-les-gens-sy-mettent-en-2025)
- [Les 3 façons de se lancer dans l’auto-hébergement](#les-3-facons-de-se-lancer-dans-lauto-hebergement)
  - [Option 1 : Le homelab physique (chez toi)](#option-1-le-homelab-physique-chez-toi)
      - [Budget mini (~100€)](#budget-mini-100-%E2%82%AC)
      - [Budget intermédiaire (~250€)](#budget-intermediaire-250-%E2%82%AC)
      - [Budget confirmé (~500€)](#budget-confirme-500-%E2%82%AC)
  - [Avantages du homelab physique](#avantages-du-homelab-physique)
  - [Inconvénients du homelab physique](#inconvenients-du-homelab-physique)
  - [Option 2 : Le VPS (serveur cloud)](#option-2-le-vps-serveur-cloud)
  - [Avantages du VPS](#avantages-du-vps)
  - [Inconvénients du VPS](#inconvenients-du-vps)
  - [Option 3 : Le combo gagnant (homelab + VPS)](#option-3-le-combo-gagnant-homelab-vps)
      - [Chez toi (homelab)](#chez-toi-homelab)
      - [Sur VPS](#sur-vps)
  - [Avantages du combo](#avantages-du-combo)
  - [Inconvénients du combo](#inconvenients-du-combo)
- [Les prérequis avant de commencer](#les-prerequis-avant-de-commencer)
  - [Compétences techniques](#competences-techniques)
      - [Niveau débutant (suffisant pour commencer)](#niveau-debutant-suffisant-pour-commencer)
      - [Niveau intermédiaire (pour aller plus loin)](#niveau-intermediaire-pour-aller-plus-loin)
      - [Niveau avancé (pour les architectures complexes)](#niveau-avance-pour-les-architectures-complexes)
  - [Matériel / Budget](#materiel-budget)
      - [Setup minimal homelab (~105€)](#setup-minimal-homelab-105-%E2%82%AC)
      - [Setup minimal VPS (~82€/an)](#setup-minimal-vps-82-%E2%82%AC-an)
      - [Setup intermédiaire homelab (~300€)](#setup-intermediaire-homelab-300-%E2%82%AC)
  - [Connexion Internet](#connexion-internet)
      - [Pour homelab physique (obligatoire)](#pour-homelab-physique-obligatoire)
      - [Pour VPS (aucune contrainte)](#pour-vps-aucune-contrainte)
- [Les 5 premiers services à auto-héberger (par ordre de difficulté)](#les-5-premiers-services-a-auto-heberger-par-ordre-de-difficulte)
  - [1. Uptime Kuma — Monitoring ultra-simple 🟢](#1-uptime-kuma-monitoring-ultra-simple-%F0%9F%9F%A2)
  - [2. Nextcloud — Ton cloud personnel 🟡](#2-nextcloud-ton-cloud-personnel-%F0%9F%9F%A1)
  - [3. Vaultwarden — Gestionnaire de mots de passe 🟢](#3-vaultwarden-gestionnaire-de-mots-de-passe-%F0%9F%9F%A2)
  - [4. Jellyfin — Ton Netflix maison 🟡](#4-jellyfin-ton-netflix-maison-%F0%9F%9F%A1)
  - [5. Immich — Alternative à Google Photos 🟡](#5-immich-alternative-a-google-photos-%F0%9F%9F%A1)
- [Erreurs fréquentes des débutants (et comment les éviter)](#erreurs-frequentes-des-debutants-et-comment-les-eviter)
  - [❌ Erreur 1 : Tout exposer sur Internet sans sécurité](#%E2%9D%8C-erreur-1-tout-exposer-sur-internet-sans-securite)
  - [❌ Erreur 2 : Pas de backups](#%E2%9D%8C-erreur-2-pas-de-backups)
  - [❌ Erreur 3 : Vouloir tout faire d’un coup](#%E2%9D%8C-erreur-3-vouloir-tout-faire-dun-coup)
  - [❌ Erreur 4 : Négliger la documentation](#%E2%9D%8C-erreur-4-negliger-la-documentation)
  - [❌ Erreur 5 : Ignorer les logs](#%E2%9D%8C-erreur-5-ignorer-les-logs)
- [La checklist pour démarrer (étape par étape)](#la-checklist-pour-demarrer-etape-par-etape)
  - [✅ Semaine 1 : Préparer le terrain](#%E2%9C%85-semaine-1-preparer-le-terrain)
  - [✅ Semaine 2 : Premier service](#%E2%9C%85-semaine-2-premier-service)
  - [✅ Semaine 3 : Cloud personnel](#%E2%9C%85-semaine-3-cloud-personnel)
  - [✅ Semaine 4 : Sécurité et backups](#%E2%9C%85-semaine-4-securite-et-backups)
- [Ressources pour aller plus loin](#ressources-pour-aller-plus-loin)
  - [📚 Articles complémentaires sur ce site](#%F0%9F%93%9A-articles-complementaires-sur-ce-site)
  - [🌐 Communautés francophones](#%F0%9F%8C%90-communautes-francophones)
  - [📖 Guides externes](#%F0%9F%93%96-guides-externes)
  - [📺 Chaînes YouTube recommandées](#%F0%9F%93%BA-chaines-you-tube-recommandees)
  - [🛠️ Outils utiles](#%F0%9F%9B%A0%EF%B8%8F-outils-utiles)
- [Conclusion : Prêt à devenir indépendant ?](#conclusion-pret-a-devenir-independant)
  - [Ce que tu vas gagner](#ce-que-tu-vas-gagner)
  - [La suite du programme](#la-suite-du-programme)
- [FAQ : Les questions que tout le monde se pose](#faq-les-questions-que-tout-le-monde-se-pose)
  - [C’est vraiment nécessaire d’avoir des compétences en Linux ?](#faq-question-1761134142319)
  - [Ça coûte combien par mois ?](#faq-question-1761134153187)
  - [C’est légal d’héberger ses propres services ?](#faq-question-1761134174614)
  - [Mon FAI va me bloquer si j’héberge un serveur ?](#faq-question-1761134183426)
  - [Mes données sont-elles vraiment plus en sécurité chez moi ?](#faq-question-1761134203543)
  - [Que se passe-t-il si mon disque dur tombe en panne ?](#faq-question-1761134255505)
  - [Puis-je auto-héberger mes mails ?](#faq-question-1761134264569)
  - [Docker ou installation native ?](#faq-question-1761134310450)
  - [Combien de temps ça prend pour tout mettre en place ?](#faq-question-1761134322824)
  - [Puis-je utiliser Windows ou macOS comme serveur ?](#faq-question-1761134343536)


L’auto-hébergement, c’est quoi exactement ?
-------------------------------------------

L’auto-hébergement (ou « self-hosting » pour les anglophones), c’est le fait d’**héberger ses propres services numériques** sur du matériel qu’on contrôle, plutôt que de passer par des plateformes tierces.

Concrètement :

- **Au lieu de** Google Drive 👉 **Tu héberges** Nextcloud
- **Au lieu de** Gmail 👉 **Tu héberges** ton propre serveur mail
- **Au lieu de** LastPass 👉 **Tu héberges** Bitwarden
- **Au lieu de** Netflix 👉 **Tu héberges** Jellyfin avec ta bibliothèque perso

### Pourquoi les gens s’y mettent en 2025 ?

**1. Vie privée**  
Tes données restent chez toi, point final. Pas de télémétrie, pas d’analyse comportementale, pas de revente à des tiers.

**2. Contrôle total**  
Tu décides des features, des backups, des mises à jour. Si une app ajoute une fonctionnalité que tu détestes, tu n’es pas obligé de l’installer.

**3. Apprentissage**  
Tu comprends comment fonctionne Internet « pour de vrai ». Serveurs, réseaux, bases de données, reverse proxy… tout devient concret.

**4. Économies à long terme**  
Tu paies 10€/mois pour Google One, 10€/mois pour Dropbox, 5€/mois pour un gestionnaire de mots de passe… Avec un VPS à 10€/mois, tu héberges tout.

**5. Satisfaction personnelle**  
Oui, c’est geek, mais c’est satisfaisant de dire « J’ai mon propre cloud » au lieu de « Je suis sur iCloud ».

> **À savoir :**  
> L’auto-hébergement n’est pas une religion. Tu peux mélanger : garder Gmail pour les mails importants, mais héberger ton Nextcloud pour tes fichiers. L’important, c’est de choisir consciemment.

- - - - - -

Les 3 façons de se lancer dans l’auto-hébergement
-------------------------------------------------

### Option 1 : Le homelab physique (chez toi)

**C’est quoi ?**  
Un serveur ou mini-PC qui tourne 24/7 chez toi, dans un placard, sous ton bureau, ou dans une vraie baie serveur si tu veux faire les choses bien.

**Matériel recommandé selon ton budget :**

#### Budget mini (~100€)

- **[Raspberry Pi 4 (8 Go RAM)](https://amzn.to/4hjTznG)** : ~80€
- [Carte microSD 64 Go](https://amzn.to/475NBDD) : ~10€
- [Alimentation officielle](https://amzn.to/48DezDJ) : ~10€
- **[Total : ~100€](https://amzn.to/4hnci1y)**

**Avantages :** Consommation électrique très faible (3-5W), silencieux, parfait pour débuter.  
**Limites :** RAM limitée, pas de virtualisation avancée.

#### Budget intermédiaire (~250€)

- **[Mini-PC Intel N100](https://amzn.to/42PvzTE)** (type Beelink, GMKtec) : ~200€ 
  - 16 Go RAM
  - 512 Go SSD NVMe
  - Consommation ~15W
- **Total : ~200-250€**

**Avantages :** Bien plus puissant qu’un Raspberry Pi, peut faire tourner 10-15 services Docker facilement.  
**Limites :** Pas extensible (RAM/stockage soudés sur certains modèles).

#### Budget confirmé (~500€)

- **[Serveur Dell PowerEdge ](https://amzn.to/475NUON)ou HP ProLiant d’occasion** : ~300-500€ 
  - 32-64 Go RAM
  - Plusieurs disques durs (RAID possible)
  - Processeur Xeon
- **Total : ~300-500€ + électricité (~20-30€/mois)**

**Avantages :** Puissance énorme, RAID matériel, évolutif, peut virtualiser des dizaines de VMs.  
**Limites :** Bruyant, consomme beaucoup, prend de la place.

### Avantages du homelab physique

✅ **Données 100% chez toi** : Aucun tiers n’a accès  
✅ **Pas de coûts mensuels récurrents** : Juste l’électricité  
✅ **Idéal pour apprendre** : Tu touches le matériel, tu comprends mieux  
✅ **Extensible** : Tu peux ajouter des disques, de la RAM

### Inconvénients du homelab physique

❌ **Dépend de ta connexion Internet** : Si ta box plante, tes services sont inaccessibles de l’extérieur  
❌ **Consommation électrique** : Entre 5€/mois (Raspberry) et 30€/mois (gros serveur)  
❌ **Bruit** : Les vrais serveurs sont bruyants (ventilateurs)  
❌ **Configuration réseau** : Il faut ouvrir des ports sur ta box (ou utiliser un VPN)

**Pour qui ?**  
Les curieux qui veulent comprendre le matériel, ceux qui ont une bonne connexion fibre, les paranos de la vie privée, ceux qui aiment bidouiller.

- - - - - -

### Option 2 : Le VPS (serveur cloud)

**C’est quoi ?**  
Un serveur virtuel loué chez un hébergeur, accessible 24/7 depuis Internet, avec une vraie adresse IP publique.

**Hébergeurs recommandés (testés personnellement) :**

| Hébergeur | Prix/mois | RAM | CPU | Stockage | Bande passante | Idéal pour |
|---|---|---|---|---|---|---|
| **Hostinger VPS** | 8,99€ | 4 Go | 2 vCPU | 100 Go NVMe | Illimitée | Débutants, support FR |
| **Contabo VPS S** | 5,99€ | 4 Go | 2 vCPU | 100 Go SSD | 32 To/mois | Meilleur rapport qualité/prix |
| **Hetzner CPX11** | 4,51€ | 2 Go | 2 vCPU | 40 Go NVMe | 20 To/mois | Minimaliste, datacenter DE |
| **OVH VPS Starter** | 6€ | 2 Go | 1 vCPU | 40 Go SSD | Illimitée | Support FR, datacenter FR |

**Mon choix perso :** Contabo pour le rapport qualité/prix, ou Hostinger si tu veux du support en français.

### Avantages du VPS

✅ **Toujours accessible** : Bande passante illimitée, uptime 99,9%  
✅ **Pas de matériel à gérer** : Pas de panne hardware, pas de bruit  
✅ **Backups automatiques disponibles** : Souvent en option  
✅ **Idéal si ta connexion Internet est pourrie**  
✅ **Évolutif** : Tu peux upgrader RAM/CPU en 2 clics

### Inconvénients du VPS

❌ **Coût mensuel récurrent** : Entre 5€ et 20€/mois selon tes besoins  
❌ **Données hébergées chez un tiers** : Même si tu les contrôles, elles ne sont pas physiquement chez toi  
❌ **Limites de stockage** : Si tu veux stocker 2 To de photos, ça coûte cher

**Pour qui ?**  
Ceux qui veulent des services accessibles de partout, les débutants qui n’ont pas de matériel, ceux qui testent avant d’investir dans du physique, ceux qui veulent un serveur « qui marche » sans se prendre la tête.

> **Important :** Si tu choisis un VPS, commence directement par sécuriser ton serveur. J’ai un guide complet sur [la sécurisation d’un serveur Linux](https://brandonvisca.com/securite-de-votre-serveur-linux/) que tu devrais lire avant de faire quoi que ce soit d’autre.

- - - - - -

### Option 3 : Le combo gagnant (homelab + VPS)

**C’est quoi ?**  
Héberger chez toi les services « lourds » (fichiers, médias), et sur un VPS les services « critiques » (mails, monitoring, reverse proxy).

**Exemple de setup combo :**

#### Chez toi (homelab)

- **Nextcloud** : Stockage de fichiers (Go illimités)
- **Jellyfin** : Serveur média (films, séries)
- **Immich** : Backup photos (ta bibliothèque complète)
- **Paperless-ngx** : GED documentaire

#### Sur VPS

- **Uptime Kuma** : Monitoring de tous tes services
- **WireGuard** : VPN pour accéder à ton homelab de l’extérieur
- **Nginx Proxy Manager** : Reverse proxy central
- **Vaultwarden** : Gestionnaire de mots de passe (critique)

### Avantages du combo

✅ **Le meilleur des deux mondes**  
✅ **Résilience** : Si ta box tombe, les services critiques restent up  
✅ **Optimisation des coûts** : Stockage massif chez toi, services légers sur VPS  
✅ **Sécurité renforcée** : Ton homelab n’est pas directement exposé sur Internet

### Inconvénients du combo

❌ **Plus complexe à gérer au début**  
❌ **Coût combo** : Matériel + VPS (~15-25€/mois + investissement initial)  
❌ **Nécessite de bonnes connaissances réseau** (VPN, tunnels, reverse proxy)

**Pour qui ?**  
Les utilisateurs confirmés qui veulent une vraie infrastructure, ceux qui autohébergent « sérieusement », les admins sys qui veulent reproduire une infra pro à la maison.

- - - - - -

Les prérequis avant de commencer
--------------------------------

Avant de te lancer tête baissée, voici ce que tu dois avoir (ou apprendre).

### Compétences techniques

#### Niveau débutant (suffisant pour commencer)

- ✅ Savoir te connecter en SSH à un serveur
- ✅ Comprendre les bases de Linux (cd, ls, mkdir, nano)
- ✅ Ne pas paniquer devant le terminal noir
- ✅ Savoir chercher une erreur sur Google (oui, c’est une compétence)

#### Niveau intermédiaire (pour aller plus loin)

- ✅ Maîtriser Docker et docker-compose
- ✅ Comprendre les bases des réseaux (IP, ports, DNS, NAT)
- ✅ Savoir lire des logs d’erreur et débugger
- ✅ Configurer un firewall (UFW, iptables)

#### Niveau avancé (pour les architectures complexes)

- ✅ Proxmox et virtualisation
- ✅ Reverse proxy (Nginx, Traefik)
- ✅ VPN (WireGuard, OpenVPN)
- ✅ Orchestration (Docker Swarm, Kubernetes)

**Si tu débutes :**  
Pas de panique ! Chaque article que je publie est pensé pour les débutants. Tu apprendras au fur et à mesure. Rome ne s’est pas faite en un jour, et ton homelab non plus.

- - - - - -

### Matériel / Budget

#### Setup minimal homelab (~105€)

- Raspberry Pi 4 (8 Go) → ~80€
- Carte SD 64 Go → ~15€
- Alimentation → ~10€
- **Total : ~105€**

**Ce que tu peux faire avec :**

- Nextcloud (cloud perso léger)
- Vaultwarden (mots de passe)
- Uptime Kuma (monitoring)
- Pi-hole (blocage pub réseau)

#### Setup minimal VPS (~82€/an)

- Contabo VPS S → 5,99€/mois
- Nom de domaine (.fr ou .com) → ~10€/an
- **Total : ~82€/an (soit 6,83€/mois)**

**Ce que tu peux faire avec :**

- Tous les services Docker légers
- Reverse proxy avec SSL
- 5-10 services simultanés

#### Setup intermédiaire homelab (~300€)

- Mini-PC Intel N100 → ~200€
- Disque dur externe 2 To → ~60€
- Switch réseau Gigabit → ~20€
- **Total : ~280€**

**Ce que tu peux faire avec :**

- 10-15 services Docker
- Proxmox avec plusieurs VMs
- Stockage confortable

- - - - - -

### Connexion Internet

#### Pour homelab physique (obligatoire)

- ✅ **Fibre ou ADSL stable** : Upload > 10 Mbps recommandé (5 Mbps minimum)
- ✅ **IP publique** : La plupart des box grand public l’ont
- ✅ **Accès à l’interface de ta box** : Pour ouvrir des ports ou configurer le DMZ
- ✅ **Pas de CGNAT** : Si ton FAI utilise le Carrier-Grade NAT, l’auto-hébergement devient compliqué

**Comment vérifier ton upload ?**  
Va sur [Fast.com](https://fast.com/) ou [nPerf](https://www.nperf.com/) et regarde la vitesse d’upload.

#### Pour VPS (aucune contrainte)

N’importe quelle connexion suffit. Même une 4G pourrie, car tu administres le serveur, tu ne l’héberges pas physiquement.

- - - - - -

Les 5 premiers services à auto-héberger (par ordre de difficulté)
-----------------------------------------------------------------

### 1. Uptime Kuma — Monitoring ultra-simple 🟢

**C’est quoi ?**  
Un outil de monitoring pour vérifier que tes services sont bien en ligne. Interface magnifique, notifications par email/Discord/Telegram.

**Pourquoi commencer par ça ?**

- Installation en 2 minutes
- Interface visuelle splendide
- Utile dès le début pour surveiller tout le reste
- Tu vois immédiatement si un service tombe

**Difficulté :** 🟢 Débutant  
**Docker :** Oui, installation triviale  
**RAM nécessaire :** 512 Mo

**Ce que tu vas apprendre :**

- Lancer un conteneur Docker
- Accéder à une interface web
- Configurer des checks HTTP/HTTPS

- - - - - -

### 2. Nextcloud — Ton cloud personnel 🟡

**C’est quoi ?**  
L’alternative open source à Google Drive / Dropbox. Synchronisation de fichiers, calendrier, contacts, notes, galerie photos.

**Pourquoi ?**  
C’est LE service signature de l’auto-hébergement. Si tu n’héberges qu’un seul service dans ta vie, c’est celui-là.

**Difficulté :** 🟡 Intermédiaire  
**Docker :** Oui, avec base de données  
**Espace disque :** Selon tes besoins (100 Go+ recommandé)  
**RAM nécessaire :** 2 Go minimum

**Ce que tu vas apprendre :**

- Déployer une app avec base de données
- Configurer un reverse proxy
- Gérer des volumes Docker
- Synchroniser des fichiers entre devices

**Apps recommandées à installer :**

- Memories (alternative Google Photos)
- Contacts
- Calendar
- Notes

- - - - - -

### 3. Vaultwarden — Gestionnaire de mots de passe 🟢

**C’est quoi ?**  
Une version allégée de Bitwarden (mais 100% compatible avec toutes les apps officielles Bitwarden). Stocke tous tes mots de passe de manière chiffrée.

**Pourquoi ?**  
Fini les mots de passe « 123456 » réutilisés partout. Et contrairement à LastPass, tu gardes le contrôle total de tes identifiants.

**Difficulté :** 🟢 Débutant  
**Docker :** Oui, très simple  
**RAM nécessaire :** 512 Mo suffisent

**Ce que tu vas apprendre :**

- Auto-héberger un service critique de sécurité
- Configurer HTTPS (obligatoire pour les apps mobiles)
- Gérer des tokens d’admin

**Apps disponibles :**

- Extension navigateur (Chrome, Firefox, Safari)
- Apps mobiles (iOS, Android)
- Apps desktop (Windows, Mac, Linux)

- - - - - -

### 4. Jellyfin — Ton Netflix maison 🟡

**C’est quoi ?**  
Un serveur média pour tes films, séries, musique. Open source, sans télémétrie, sans pub.

**Pourquoi ?**  
Parce que c’est satisfaisant d’avoir son propre Netflix avec sa bibliothèque perso. Et c’est légal si tu possèdes les médias.

**Difficulté :** 🟡 Intermédiaire  
**Docker :** Oui  
**Espace disque :** Beaucoup (dépend de ta bibliothèque)  
**RAM nécessaire :** 2 Go minimum (4 Go si transcodage)

**Ce que tu vas apprendre :**

- Organiser une bibliothèque média
- Configurer les métadonnées automatiques (TMDB, TVDB)
- Gérer les profils utilisateurs
- Transcoder à la volée (si ton CPU le supporte)

- - - - - -

### 5. Immich — Alternative à Google Photos 🟡

**C’est quoi ?**  
Une app de backup et d’organisation de photos avec reconnaissance faciale, géolocalisation, et recherche intelligente. Le Google Photos qu’on peut héberger chez soi.

**Pourquoi ?**  
Google Photos, c’est pratique, mais tes photos sont analysées par leurs algos (et potentiellement utilisées pour entraîner des modèles). Immich fait pareil, mais chez toi.

**Difficulté :** 🟡 Intermédiaire  
**Docker :** Oui, avec plusieurs conteneurs  
**Espace disque :** Selon ta bibliothèque photo (50 Go+ minimum)  
**RAM nécessaire :** 4 Go minimum

**Ce que tu vas apprendre :**

- Déployer une stack complexe (app + base de données + Redis + machine learning)
- Configurer l’upload automatique mobile
- Gérer les albums partagés

**Apps mobiles :**  
iOS et Android, avec synchronisation automatique en arrière-plan.

- - - - - -

Erreurs fréquentes des débutants (et comment les éviter)
--------------------------------------------------------

### ❌ Erreur 1 : Tout exposer sur Internet sans sécurité

**Le problème :**  
Tu ouvres tous les ports sur ta box (22 pour SSH, 80/443 pour HTTP/HTTPS, et 15 autres), tu mets des mots de passe faibles, et en moins de 24h, tu te fais scanner par des bots du monde entier.

**Les symptômes :**

- Des milliers de tentatives de connexion SSH dans les logs
- Des scans de ports automatiques
- Dans le pire des cas : ton serveur devient un bot dans un botnet

**La solution :**

1. **Utilise un VPN** (WireGuard ou Tailscale) pour accéder à tes services
2. **Ou un reverse proxy avec authentification** (Nginx Proxy Manager + Authelia)
3. **Change le port SSH** (22 → 2222 par exemple)
4. **Installe Fail2ban** pour bannir les IPs suspectes
5. **Utilise des clés SSH** au lieu de mots de passe

**Important :** Lis absolument mon guide sur [comment sécuriser un serveur Linux](https://brandonvisca.com/securite-de-votre-serveur-linux/) avant d’exposer quoi que ce soit sur Internet.

- - - - - -

### ❌ Erreur 2 : Pas de backups

**Le problème :**  
Ton disque dur lâche, et tu perds 3 ans de photos de famille, tous tes mots de passe, et ta config Nextcloud.

**Les symptômes :**

- Panique totale
- Dépression post-perte-de-données
- Promesse à soi-même de « ne plus jamais recommencer »

**La solution :**  
Respecte la règle du **3-2-1** :

- **3** copies de tes données
- Sur **2** supports différents (disque local + cloud/NAS)
- **1** copie hors site (chez un pote, cloud chiffré, ou datacenter)

**Outils de backup recommandés :**

- **Restic** : Backups incrémentaux chiffrés vers cloud (Backblaze B2, Wasabi, S3)
- **Duplicati** : Interface web, compatible tous les clouds
- **Proxmox Backup Server** : Si tu utilises Proxmox
- **Rsync + Cron** : La méthode old-school qui marche toujours

**Fréquence recommandée :**

- Données critiques (mots de passe, configs) : Quotidien
- Photos/documents : Hebdomadaire
- Médias (films/séries) : Pas besoin (tu peux les re-télécharger)

- - - - - -

### ❌ Erreur 3 : Vouloir tout faire d’un coup

**Le problème :**  
Tu installes 15 services le premier jour, tu ne comprends rien à comment ils communiquent, tu mélanges tout, et tu abandonnes par frustration.

**Les symptômes :**

- Terminal ouvert avec 20 onglets
- 15 docker-compose.yml que tu ne comprends pas
- Confusion totale entre les ports, les volumes, les réseaux
- Démotivation

**La solution :**  
Commence par **UN service** à la fois. Maîtrise-le complètement avant de passer au suivant.

**Ordre recommandé :**

1. **Semaine 1** : Uptime Kuma (monitoring)
2. **Semaine 2** : Portainer (gestion Docker)
3. **Semaine 3** : Nextcloud ou Vaultwarden
4. **Semaine 4** : Nginx Proxy Manager + HTTPS
5. **Puis** : Les autres services au fur et à mesure

**Philosophie :** Mieux vaut 3 services qui marchent bien qu’on comprend, que 15 services cassés qu’on ne maîtrise pas.

- - - - - -

### ❌ Erreur 4 : Négliger la documentation

**Le problème :**  
Tu installes tout de tête, sans rien noter. 6 mois plus tard, un service plante, et tu ne sais plus comment tu l’avais configuré.

**Les symptômes :**

- « Mais j’avais fait comment déjà pour configurer ça ? »
- Impossibilité de reproduire une install
- Perte de temps énorme en reverse-engineering

**La solution :**  
Documente TOUT au fur et à mesure, même si ça te semble évident.

**Outils de documentation :**

- **Notion** : Base de connaissances perso
- **Obsidian** : Notes markdown locales
- **Un simple fichier README.md** dans chaque dossier de service
- **Bookstack** : Wiki auto-hébergé

**Ce qu’il faut noter :**

- Les commandes utilisées
- Les fichiers de config modifiés
- Les ports utilisés par chaque service
- Les mots de passe (dans un gestionnaire chiffré, évidemment)
- Les problèmes rencontrés et leurs solutions

- - - - - -

### ❌ Erreur 5 : Ignorer les logs

**Le problème :**  
Un service ne marche pas, tu cherches pendant des heures sur Google, alors que l’erreur est clairement indiquée dans les logs.

**Les symptômes :**

- Perte de temps énorme
- Frustration
- Sentiment d’impuissance

**La solution :**  
**LIS LES LOGS AVANT TOUT LE RESTE.**

```bash
# Docker
docker logs nom-conteneur
docker logs -f nom-conteneur  # Mode suivi en temps réel

# Système Linux
sudo journalctl -u nom-service
sudo tail -f /var/log/syslog

```

