---
title: "Termius : Le Client SSH Moderne qui Envoie PuTTY à la Retraite (Guide 2025)"
pubDatetime: "2025-11-22T19:10:57+01:00"
description: "Termius révolutionne la gestion SSH sur Windows. Alternative moderne à PuTTY avec sync cloud, SFTP intégré et interface intuitive. Guide complet 2025."
tags:
  - termius
  - ssh
  - putty-alternative
  - windows
  - linux
  - devops
  - sysadmin
  - terminal
  - guide
  - intermediaire
---

Si vous utilisez encore **PuTTY** pour vous connecter en SSH à vos serveurs en 2025, cet article va vous faire gagner 30 minutes par jour. Non, ce n’est pas du clickbait. Termius, c’est ce qui se passe quand un client SSH rencontre le 21ème siècle : interface moderne, synchronisation cloud, gestion intelligente des clés… Bref, tout ce que PuTTY aurait dû devenir s’il n’était pas resté coincé en 1999.

Pourquoi PuTTY mérite sa retraite (et vous méritez mieux)
---------------------------------------------------------

Soyons honnêtes : PuTTY a fait le job pendant 20 ans. Mais en 2025, **gérer vos serveurs ne devrait pas ressembler à une séance de torture médiévale**. Voici ce que PuTTY ne fait toujours pas :

- **Synchronisation entre appareils** : Vos configs restent prisonnières d’une seule machine
- **Interface moderne** : On dirait Windows 95 a vomi sur votre écran
- **Gestion native des clés SSH** : Vous devez jongler avec PuTTYgen comme un clown triste
- **Organisation des connexions** : Bonne chance pour retrouver le bon serveur parmi vos 47 configs
- **Multi-plateforme** : Windows uniquement, parce que pourquoi faire simple ?

Termius, lui, fait tout ça. Et bien plus encore.

Termius en 30 secondes : Le pitch
---------------------------------

Termius est un **client SSH moderne et cross-platform** (Windows, macOS, Linux, iOS, Android) qui transforme la gestion de vos serveurs en expérience fluide. Imaginez avoir accès à tous vos serveurs depuis n’importe quel appareil, avec vos clés SSH synchronisées, vos snippets de commandes prêts à l’emploi, et une interface qui ne pique pas les yeux.

Développé par Termius Corporation, l’outil existe en version gratuite (largement suffisante pour la plupart des usages) et en versions payantes pour les besoins professionnels ou en équipe.

**Le verdict rapide** : Si vous gérez plus de 3 serveurs régulièrement ou si vous travaillez depuis plusieurs machines, Termius va vous changer la vie. Point.

- - - - - -

-----------
## Table des matières


- [Termius en 30 secondes : Le pitch](#termius-en-30-secondes-le-pitch)
- [Installation sur Windows : 3 minutes chrono](#installation-sur-windows-3-minutes-chrono)
  - [Méthode 1 : Via le Microsoft Store (recommandé)](#methode-1-via-le-microsoft-store-recommande)
  - [Méthode 2 : Téléchargement direct](#methode-2-telechargement-direct)
  - [Premier lancement : Configuration de base](#premier-lancement-configuration-de-base)
- [Configuration : Ajouter votre premier serveur](#configuration-ajouter-votre-premier-serveur)
  - [La méthode rapide (authentification par mot de passe)](#la-methode-rapide-authentification-par-mot-de-passe)
  - [La méthode pro (authentification par clé SSH)](#la-methode-pro-authentification-par-cle-ssh)
- [Les fonctionnalités qui tuent (et pourquoi vous allez les adorer)](#les-fonctionnalites-qui-tuent-et-pourquoi-vous-allez-les-adorer)
  - [1. Organisation intelligente avec groupes et tags](#1-organisation-intelligente-avec-groupes-et-tags)
  - [2. Snippets : Vos commandes favorites à portée de main](#2-snippets-vos-commandes-favorites-a-portee-de-main)
  - [3. Split View : Gérer plusieurs serveurs simultanément](#3-split-view-gerer-plusieurs-serveurs-simultanement)
  - [4. Port Forwarding intégré](#4-port-forwarding-integre)
  - [5. SFTP intégré : Transférer des fichiers sans WinSCP](#5-sftp-integre-transferer-des-fichiers-sans-win-scp)
  - [6. Autocomplete et historique des commandes](#6-autocomplete-et-historique-des-commandes)
- [Version gratuite vs payante : Ce qu’il faut savoir](#version-gratuite-vs-payante-ce-quil-faut-savoir)
  - [🆓 Termius Starter (Gratuit)](#%F0%9F%86%93-termius-starter-gratuit)
  - [💼 Termius Pro (10$/mois ou 100$/an)](#%F0%9F%92%BC-termius-pro-10-mois-ou-100-an)
  - [👥 Termius Team (20$/utilisateur/mois)](#%F0%9F%91%A5-termius-team-20-utilisateur-mois)
  - [🏢 Termius Business (30$/utilisateur/mois)](#%F0%9F%8F%A2-termius-business-30-utilisateur-mois)
- [Cas d’usage concrets : Quand Termius brille vraiment](#cas-dusage-concrets-quand-termius-brille-vraiment)
  - [Scénario 1 : L’admin sys freelance](#scenario-1-ladmin-sys-freelance)
  - [Scénario 2 : L’étudiant en apprentissage](#scenario-2-letudiant-en-apprentissage)
  - [Scénario 3 : L’équipe DevOps](#scenario-3-lequipe-dev-ops)
- [Termius vs les alternatives : Le match](#termius-vs-les-alternatives-le-match)
  - [Termius vs PuTTY](#termius-vs-pu-tty)
  - [Termius vs MobaXterm](#termius-vs-moba-xterm)
  - [Termius vs OpenSSH natif (Windows Terminal)](#termius-vs-open-ssh-natif-windows-terminal)
- [Bonnes pratiques et tips pour exploiter Termius comme un pro](#bonnes-pratiques-et-tips-pour-exploiter-termius-comme-un-pro)
  - [1. Utilisez des noms de serveurs explicites](#1-utilisez-des-noms-de-serveurs-explicites)
  - [2. Codez vos environnements avec des couleurs](#2-codez-vos-environnements-avec-des-couleurs)
  - [3. Créez un snippet « status global »](#3-creez-un-snippet-status-global)
  - [4. Activez l’authentification à deux facteurs (2FA)](#4-activez-lauthentification-a-deux-facteurs-2-fa)
  - [5. Faites des sauvegardes de vos clés privées](#5-faites-des-sauvegardes-de-vos-cles-privees)
- [Les petits défauts (parce qu’il faut être honnête)](#les-petits-defauts-parce-quil-faut-etre-honnete)
  - [1. Pas open-source](#1-pas-open-source)
  - [2. La version gratuite sans sync peut frustrer](#2-la-version-gratuite-sans-sync-peut-frustrer)
  - [3. Performance sur des sessions très lentes](#3-performance-sur-des-sessions-tres-lentes)
- [Installation de Mosh sur votre serveur (bonus tip)](#installation-de-mosh-sur-votre-serveur-bonus-tip)
- [Sécurité : Termius est-il sûr ?](#securite-termius-est-il-sur)
  - [Chiffrement](#chiffrement)
  - [Audit et certifications](#audit-et-certifications)
  - [Recommandations](#recommandations)
- [FAQ : Les questions qu’on me pose tout le temps](#faq-les-questions-quon-me-pose-tout-le-temps)
  - [Termius fonctionne-t-il sur Linux ?](#termius-fonctionne-t-il-sur-linux)
  - [Peut-on utiliser Termius sans connexion Internet ?](#peut-on-utiliser-termius-sans-connexion-internet)
  - [Termius remplace-t-il complètement un terminal classique ?](#termius-remplace-t-il-completement-un-terminal-classique)
  - [Y a-t-il une réduction étudiante ou open-source ?](#y-a-t-il-une-reduction-etudiante-ou-open-source)
  - [Puis-je importer mes sessions PuTTY dans Termius ?](#puis-je-importer-mes-sessions-pu-tty-dans-termius)
- [Pour aller plus loin : Intégrations et workflows avancés](#pour-aller-plus-loin-integrations-et-workflows-avances)
  - [Intégration avec AWS, Azure, DigitalOcean](#integration-avec-aws-azure-digital-ocean)
  - [Automatisation avec Termius API (Team/Business)](#automatisation-avec-termius-api-team-business)
- [Conclusion : Termius en vaut-il la peine en 2025 ?](#conclusion-termius-en-vaut-il-la-peine-en-2025)
- [Pour aller encore plus loin](#pour-aller-encore-plus-loin)


Installation sur Windows : 3 minutes chrono
-------------------------------------------

### Méthode 1 : Via le Microsoft Store (recommandé)

La plus simple, et probablement la plus sûre :

1. Ouvrez le **Microsoft Store**
2. Recherchez « Termius »
3. Cliquez sur **Installer**
4. Lancez l’application

**Avantage** : Mises à jour automatiques, installation propre, désinstallation facile.

### Méthode 2 : Téléchargement direct

Si vous préférez le faire à l’ancienne :

1. Allez sur [termius.com/download/windows](https://termius.com/download/windows)
2. Téléchargez l’installeur `.exe`
3. Lancez l’installation (Next, Next, Finish, vous connaissez la chanson)

**Note** : L’installeur pèse environ 80 Mo. Connexion potable requise.

### Premier lancement : Configuration de base

Au premier démarrage, Termius vous propose de créer un compte gratuit. **Créez-le**. Même si vous pensez ne pas en avoir besoin maintenant, vous me remercierez plus tard quand vous voudrez accéder à vos serveurs depuis votre smartphone à 2h du matin parce qu’un service est tombé.

L’inscription est gratuite et ne demande qu’une adresse email. Pas de carte bancaire, pas de période d’essai qui expire.

Configuration : Ajouter votre premier serveur
---------------------------------------------

### La méthode rapide (authentification par mot de passe)

Pour ceux qui sont pressés ou qui débutent :

1. Cliquez sur le **+** en haut à gauche
2. Sélectionnez **New Host**
3. Remplissez les champs : 
  - **Hostname** : L’IP ou le nom de domaine de votre serveur
  - **Port** : 22 (par défaut) ou votre port SSH personnalisé
  - **Username** : Votre utilisateur SSH
  - **Password** : Votre mot de passe
4. Cliquez sur **Save**
5. Double-cliquez sur votre serveur pour vous connecter

**Trop facile.** Mais on peut faire mieux.

### La méthode pro (authentification par clé SSH)

Si vous suivez un minimum les bonnes pratiques de sécurité (et vous devriez, surtout si vous avez lu mon [guide complet sur la sécurisation d’un serveur Linux](https://brandonvisca.com/securite-de-votre-serveur-linux/)), vous utilisez déjà des clés SSH.

Termius gère ça comme un chef :

1. Cliquez sur **Keychain** dans le menu de gauche
2. Cliquez sur **+ → New Key**
3. Deux options : 
  - **Import** : Importez une clé existante (format PEM, OpenSSH)
  - **Generate** : Laissez Termius générer une nouvelle paire de clés
4. Si vous générez une nouvelle clé : 
  - Choisissez **ED25519** (plus sûr et plus rapide que RSA 2048)
  - Ajoutez une **passphrase** (important pour la sécurité)
  - Donnez-lui un **nom explicite** (« clé-prod-2025 », pas « key1 »)
5. **Copiez la clé publique** et ajoutez-la sur votre serveur dans `~/.ssh/authorized_keys`
6. Lors de la création de votre host, sélectionnez cette clé dans le menu déroulant **Keys**

**Astuce de pro** : Termius peut même **pousser automatiquement** votre clé publique sur le serveur lors de la première connexion. Magique.

Les fonctionnalités qui tuent (et pourquoi vous allez les adorer)
-----------------------------------------------------------------

### 1. Organisation intelligente avec groupes et tags

Vous gérez plusieurs clients ? Différents environnements (dev, staging, prod) ? Termius vous laisse créer des **groupes** et des **tags** pour tout organiser.

**Exemple d’arborescence** :

```bash
📁 Clients
  ├── 📁 Client A
  │   ├── 🖥️ Prod Web (tag: production)
  │   ├── 🖥️ Prod DB (tag: production, database)
  │   └── 🖥️ Dev (tag: development)
  └── 📁 Homelab
      ├── 🖥️ Proxmox
      ├── 🖥️ NAS
      └── 🖥️ Pi-hole

```

sudo apt update && sudo apt upgrade -y && sudo apt autoremove -y


**État des conteneurs Docker** :

```bash
docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

```

df -h | grep -E '^/dev'


**Logs en temps réel (Nginx)** :

```bash
tail -f /var/log/nginx/access.log

```

echo "=== SYSTÈME ===" && \
uname -a && \
uptime && \
echo "" && \
echo "=== DISQUE ===" && \
df -h | grep -E '^/dev' && \
echo "" && \
echo "=== MÉMOIRE ===" && \
free -h && \
echo "" && \
echo "=== DOCKER (si installé) ===" && \
docker ps 2>/dev/null || echo "Docker non installé"


**Nom du snippet** : `status`

Tapez `status` + Enter, et vous avez toutes les infos critiques. Pratique pour un check rapide.

### 4. Activez l’authentification à deux facteurs (2FA)

Si vous utilisez la version Pro/Team et que vos connexions sont synchronisées dans le cloud, **activez le 2FA** sur votre compte Termius.

**Comment** :

1. Menu utilisateur (en haut à droite) → **Settings**
2. **Security** → **Two-Factor Authentication**
3. Scannez le QR code avec Authy, Google Authenticator ou Bitwarden

**Pourquoi** : Vos serveurs valent bien plus que les 30 secondes nécessaires pour setup le 2FA.

### 5. Faites des sauvegardes de vos clés privées

Même avec la sync cloud, **gardez une copie offline** de vos clés privées SSH. Sur une clé USB chiffrée, dans un gestionnaire de mots de passe ([comme Vaultwarden que j’auto-héberge](https://brandonvisca.com/vaultwarden-docker-gestionnaire-mots-de-passe/)), ou dans un coffre-fort numérique.

**Règle d’or** : Si Termius disparaît demain, vous devez pouvoir accéder à vos serveurs.

Les petits défauts (parce qu’il faut être honnête)
--------------------------------------------------

### 1. Pas open-source

Contrairement à OpenSSH ou PuTTY, Termius est **propriétaire**. Vous devez faire confiance à l’entreprise pour la gestion de vos credentials, même si tout est chiffré côté client (AES-256).

**Mitigation** : Ne stockez jamais de clés SSH ultra-sensibles (genre prod bancaire) uniquement dans Termius cloud. Gardez des backups offline.

### 2. La version gratuite sans sync peut frustrer

Si vous travaillez depuis plusieurs machines (PC bureau + laptop + smartphone), ne **pas** avoir la sync cloud en gratuit, c’est limite frustrant. Vous devez reconfigurer tout manuellement sur chaque appareil.

**Solution** : Soit vous payez les 100$/an, soit vous utilisez un gestionnaire de config Git pour vos fichiers SSH (plus technique).

### 3. Performance sur des sessions très lentes

Sur des connexions SSH via 4G pourrie ou satellite, Termius peut être légèrement plus lent que PuTTY qui est ultra-minimaliste. On parle de millisecondes, mais ça compte si vous êtes sur une liaison à 28 kbps au milieu du Sahara.

**Alternative** : Utilisez **Mosh** (Mobile Shell) à la place de SSH. Termius le supporte nativement et c’est fait exactement pour ça.

Installation de Mosh sur votre serveur (bonus tip)
--------------------------------------------------

**Mosh**, c’est SSH en mieux pour les connexions instables. Ça résiste aux changements d’IP (utile si vous passez du Wi-Fi à la 4G), aux latences, et ça reste connecté même si votre laptop hiberne.

**Installation rapide sur Ubuntu/Debian** :

```bash
sudo apt update && sudo apt install mosh -y

```

sudo ufw allow 60000:61000/udp


**Dans Termius** :

- Clic droit sur votre host → **Edit**
- **SSH** → Changez en **Mosh**
- Connectez-vous

**Résultat** : Une connexion qui survit à tout. Indispensable si vous administrez vos serveurs depuis un train ou un café.

Sécurité : Termius est-il sûr ?
-------------------------------

**La vraie question** : Peut-on faire confiance à Termius avec nos clés SSH et credentials ?

**Réponse courte** : Oui, dans le cadre d’un usage raisonnable.

**Réponse longue** :

### Chiffrement

- **Local** : Toutes les données sensibles (clés privées, mots de passe) sont chiffrées **localement** avec AES-256 avant d’être envoyées au cloud
- **Cloud** : Le stockage utilise également AES-256
- **Zero-knowledge** : Termius affirme ne pas avoir accès à vos données déchiffrées (votre mot de passe maître n’est jamais envoyé)

### Audit et certifications

- Termius n’est **pas open-source**, donc pas d’audit public du code
- L’entreprise est basée aux **États-Unis** (juridiction à prendre en compte selon vos besoins)
- <s>Pas de certification SOC2/ISO27001 publiquement affichée (au moment de l’écriture)</s> **C’est fait depuis, il sont [certifié SOC2](https://termius.com/security)**

### Recommandations

Pour un **usage standard** (PME, freelance, homelab) : ✅ Go

Pour un **usage ultra-sensible** (production critique, données RGPD/HIPAA/financières) :

- ⚠️ Évaluez les risques
- ⚠️ Ne stockez pas vos clés privées les plus critiques dans le cloud Termius
- ⚠️ Préférez une solution self-hosted si la compliance l’exige

**Mon avis personnel** : J’utilise Termius pour gérer mes serveurs perso, mes VPS clients, et mon homelab. Pour mes rares serveurs ultra-critiques, je garde les clés hors du cloud et je les gère manuellement. C’est un compromis pragmatique entre sécurité et productivité.

FAQ : Les questions qu’on me pose tout le temps
-----------------------------------------------

### Termius fonctionne-t-il sur Linux ?

**Oui.** Disponible en .deb (Ubuntu/Debian), .rpm (Fedora/Red Hat), Snap, et AppImage.

**Mais** : Sur Linux, la concurrence est rude (Tilix, Alacritty, Kitty…). L’intérêt de Termius, c’est surtout si vous avez **plusieurs OS** et que vous voulez la sync.

### Peut-on utiliser Termius sans connexion Internet ?

**Oui** pour les connexions SSH locales.

**Non** pour la sync cloud (logique) et certaines features comme l’autocomplete avancé qui dépend du cloud.

**En pratique** : Une fois vos serveurs configurés, vous pouvez bosser offline sans souci.

### Termius remplace-t-il complètement un terminal classique ?

**Non.** Termius est un **client SSH**, pas un terminal système local.

Pour du dev local (compilation, git, scripts), vous utiliserez toujours PowerShell, CMD, ou Windows Terminal.

Termius, c’est **uniquement** pour vos connexions distantes (serveurs, VPS, NAS, Raspberry Pi…).

### Y a-t-il une réduction étudiante ou open-source ?

**Étudiants** : Oui, via le **GitHub Student Developer Pack**. Accès gratuit à Termius Pro pendant vos études.

**Projets open-source** : Termius propose un programme « Termius for Open Source » avec accès gratuit aux fonctionnalités Pro. [Détails ici](https://termius.com/for-open-source).

### Puis-je importer mes sessions PuTTY dans Termius ?

**Pas directement**, mais vous pouvez :

1. Exporter vos sessions PuTTY depuis le registre Windows
2. Utiliser un script de conversion (cherchez « putty to termius converter » sur GitHub)
3. Ou recréer vos connexions manuellement (l’occasion de faire le ménage)

**Honnêtement** : Si vous avez moins de 20 serveurs, autant recréer à la main. Ça prend 10 minutes et vous repartez sur des bases propres.

Pour aller plus loin : Intégrations et workflows avancés
--------------------------------------------------------

### Intégration avec AWS, Azure, DigitalOcean

Termius peut se connecter à votre compte cloud et **importer automatiquement** vos instances :

- **AWS** : Via IAM credentials, récupère vos instances EC2
- **Azure** : Import de vos VMs
- **DigitalOcean** : Import de vos droplets

**Avantage** : Vos serveurs cloud sont ajoutés automatiquement. Si vous créez/supprimez des instances, Termius se met à jour.

**Comment** :

1. Menu **Integrations**
2. Choisissez votre provider
3. Authentifiez-vous
4. Boom, toutes vos machines apparaissent

**Limite** : Fonctionnalité réservée aux **plans payants** (Pro et au-dessus).

### Automatisation avec Termius API (Team/Business)

Les plans Team et Business offrent une **API REST** pour automatiser :

- Création de connexions via script
- Déploiement de configurations en masse
- Intégration avec vos outils de provisionning (Terraform, Ansible)

**Exemple de cas d’usage** : Vous spinnez 50 serveurs avec Terraform. Un script post-deploy appelle l’API Termius pour ajouter automatiquement les 50 connexions SSH avec les bonnes clés et les bons tags.

**Documentation** : [Termius API Docs](https://termius.com/documentation)

Conclusion : Termius en vaut-il la peine en 2025 ?
--------------------------------------------------

**Réponse courte** : Oui, si vous gérez plus de 3 serveurs ou si vous travaillez depuis plusieurs appareils.

**Réponse nuancée** :

- **Pour un débutant qui découvre SSH** : Termius gratuit est **parfait**. Interface claire, pas de prise de tête avec PuTTYgen, et ça ne coûte rien. Go.
- **Pour un admin sys freelance/salarié** : Termius Pro (100$/an) est un **investissement rentable**. Vous gagnez facilement 30 min/jour en productivité, soit ~130h/an. À vous de faire le calcul.
- **Pour une équipe IT** : Termius Team/Business apporte une **vraie valeur** en termes de collaboration, audit, et conformité. Comparez avec le coût d’une erreur en prod ou d’un audit raté.
- **Pour un puriste du libre** : Termius **n’est pas pour vous**. Restez sur OpenSSH + terminal classique, ou regardez du côté de [Tilix](https://github.com/gnunn1/tilix) (Linux) ou [iTerm2](https://brandonvisca.com/iterm2-guide-configuration-macos-2025/) (macOS).

Mais si vous êtes étudiant, débutant, ou que vous avez juste 2-3 serveurs perso, **la version gratuite fera le job**. Testez, vous verrez bien.

- - - - - -

Pour aller encore plus loin
---------------------------

Maintenant que vous avez Termius bien configuré, il est temps de sécuriser sérieusement vos serveurs SSH. Parce qu’avoir un beau client SSH, c’est bien, mais si votre serveur se fait rooter en 10 minutes par un bot chinois, ça sert à rien.

Je vous recommande de lire mon [guide complet sur la sécurisation d’un serveur Linux](https://brandonvisca.com/securite-de-votre-serveur-linux/), où je détaille :

- Comment changer le port SSH (et pourquoi ça compte)
- Configuration de Fail2Ban pour bannir les bots
- Désactivation de la connexion root
- Mise en place de l’authentification par clé uniquement
- Durcissement global du système

Et si vous comptez auto-héberger des services sur vos serveurs (Nextcloud, Jellyfin, Pi-hole…), jetez un œil à mon [guide ultime de l’auto-hébergement 2025](https://brandonvisca.com/auto-hebergement-guide-complet-2025/). Vous y trouverez tout pour monter une infrastructure perso solide, sécurisée, et qui vous fera économiser 500€/an en abonnements cloud.

**Bon SSH, et que le ping soit avec vous. 🚀**
