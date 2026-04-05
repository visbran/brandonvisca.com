---
title: "Vaultwarden avec Docker : Gestionnaire de Mots de Passe Gratuit (Adieu 1Password !)"
pubDatetime: "2025-10-26T22:16:05+01:00"
description: "Installe Vaultwarden avec Docker en 15 min. Alternative 1Password/Bitwarden gratuite, économise 36€/an. Guide 2025 complet + sécurité maximale."
tags:
  - vaultwarden
  - bitwarden
  - docker
  - docker-compose
  - gestionnaire-mots-de-passe
  - securite
  - auto-hebergement
  - homelab
  - 1password-alternative
  - guide
  - intermediaire
---

🎯 TL;DR
-------

Tu paies 1Password (36€/an), Dashlane (40€/an) ou LastPass (36€/an) pour gérer tes mots de passe ? Spoiler : tu peux héberger **Vaultwarden** (alternative Bitwarden) pour 0€ si tu as déjà un serveur.

**Ce que tu vas apprendre :**

- Installer Vaultwarden avec Docker en 15 minutes
- Synchroniser mots de passe sur tous tes appareils (PC, mobile, navigateur)
- Générer des mots de passe ultra-sécurisés automatiquement
- Partager des identifiants en famille/équipe (coffres partagés)
- Économiser 36-60€/an en virant ton abonnement gestionnaire de mots de passe
- Garder le contrôle TOTAL de tes données sensibles

**Prérequis :**

- Un serveur Linux (VPS, Raspberry Pi, NAS, ou serveur existant)
- 512 Mo RAM minimum (oui, c’est très léger !)
- Docker installé
- Un nom de domaine (pour HTTPS, indispensable pour la sécurité)
- 15 minutes de ton temps

- - - - - -

-----------

- [Pourquoi un gestionnaire de mots de passe, déjà ?](#pourquoi-un-gestionnaire-de-mots-de-passe-deja)
  - [La vraie question : T’utilises quoi actuellement ?](#la-vraie-question-tutilises-quoi-actuellement)
- [Vaultwarden vs Bitwarden : Quelle différence ?](#vaultwarden-vs-bitwarden-quelle-difference)
  - [Petite histoire technique](#petite-histoire-technique)
- [Vaultwarden vs 1Password vs Dashlane vs LastPass](#vaultwarden-vs-1-password-vs-dashlane-vs-last-pass)
- [Le calcul économique](#le-calcul-economique)
- [Avant de commencer : Comprendre la sécurité](#avant-de-commencer-comprendre-la-securite)
  - [Comment ça marche, le chiffrement ?](#comment-ca-marche-le-chiffrement)
  - [Le Master Password : TA responsabilité](#le-master-password-ta-responsabilite)
- [Installation Vaultwarden avec Docker : Setup en 15 min](#installation-vaultwarden-avec-docker-setup-en-15-min)
  - [Étape 1 : Préparer le serveur](#etape-1-preparer-le-serveur)
  - [Étape 2 : Docker Compose](#etape-2-docker-compose)
  - [Étape 3 : 🔐 Sécurisation du Token Admin (NOUVELLE MÉTHODE – v1.28.0+)](#etape-3-generer-l-admin-token)
      - [Génération du Token Sécurisé](#generation-du-token-securise)
      - [Configuration avec Fichier .env (RECOMMANDÉ)](#configuration-avec-fichier-env-recommande)
            - [Fichier .env](#fichier-env)
            - [Fichier docker-compose.yml](#fichier-docker-compose-yml)
      - [Vérification de la Configuration](#verification-de-la-configuration)
  - [Étape 4 : Configurer les inscriptions](#etape-4-configurer-les-inscriptions)
  - [Étape 5 : Lancer Vaultwarden](#etape-5-lancer-vaultwarden)
- [Configuration HTTPS avec Nginx Proxy Manager](#configuration-https-avec-nginx-proxy-manager)
  - [Ajouter le proxy Vaultwarden](#ajouter-le-proxy-vaultwarden)
- [Créer ton premier compte](#creer-ton-premier-compte)
  - [Via l’interface web](#via-linterface-web)
  - [Interface d’administration](#interface-dadministration)
- [Apps & Extensions : Synchroniser partout](#apps-extensions-synchroniser-partout)
  - [🌐 Extensions navigateur](#%F0%9F%8C%90-extensions-navigateur)
  - [📱 Apps mobiles](#%F0%9F%93%B1-apps-mobiles)
  - [💻 Apps desktop](#%F0%9F%92%BB-apps-desktop)
- [Utilisation quotidienne : Les cas d’usage](#utilisation-quotidienne-les-cas-dusage)
  - [1. Enregistrer un nouveau mot de passe](#1-enregistrer-un-nouveau-mot-de-passe)
  - [2. Se connecter automatiquement](#2-se-connecter-automatiquement)
  - [3. Partager des identifiants en famille](#3-partager-des-identifiants-en-famille)
  - [4. Générer un mot de passe ultra-sécurisé](#4-generer-un-mot-de-passe-ultra-securise)
  - [5. Activer l’authentification à deux facteurs (2FA)](#5-activer-lauthentification-a-deux-facteurs-2-fa)
- [Sécurité avancée](#securite-avancee)
  - [Activer le 2FA sur ton compte Vaultwarden](#activer-le-2-fa-sur-ton-compte-vaultwarden)
  - [Audit de sécurité de tes mots de passe](#audit-de-securite-de-tes-mots-de-passe)
- [Backup & Restauration](#backup-restauration)
  - [Exporter tes données (backup manuel)](#exporter-tes-donnees-backup-manuel)
  - [Restaurer depuis backup](#restaurer-depuis-backup)
- [Cas d’usage réels](#cas-dusage-reels)
  - [Scénario 1 : Particulier solo](#scenario-1-particulier-solo)
  - [Scénario 2 : Famille (4 personnes)](#scenario-2-famille-4-personnes)
  - [Scénario 3 : Petite entreprise (8 employés)](#scenario-3-petite-entreprise-8-employes)
- [Problèmes courants & Solutions](#problemes-courants-solutions)
  - [❌ « Impossible de se connecter au serveur »](#%E2%9D%8C-impossible-de-se-connecter-au-serveur)
  - [❌ « Master Password oublié »](#%E2%9D%8C-master-password-oublie)
  - [❌ Apps mobiles : remplissage auto ne marche pas](#%E2%9D%8C-apps-mobiles-remplissage-auto-ne-marche-pas)
  - [❌ Sync lente entre appareils](#%E2%9D%8C-sync-lente-entre-appareils)
  - [❌ Problème : « Invalid admin token »](#probleme-invalid-admin-token)
  - [❌ Problème : « You are using a plain text ADMIN\_TOKEN »](#probleme-you-are-using-a-plain-text-admin-token)
- [🎊 Conclusion : Le dernier pilier de ton indépendance](#maillage-interne-stack-complete-dindependance)
  - [🚀 Et maintenant ?](#%F0%9F%9A%80-et-maintenant)


Pourquoi un gestionnaire de mots de passe, déjà ?
-------------------------------------------------

### La vraie question : T’utilises quoi actuellement ?

**Option 1 : Le même mot de passe partout** 🤦‍♂️

- Mot de passe : `Azerty123!`
- Utilisé sur : Gmail, Facebook, Amazon, Banque…
- Sécurité : **0/10**
- Si un site se fait pirater → **TOUS tes comptes tombent**

**Option 2 : Mots de passe dans le navigateur**

- Chrome/Firefox mémorise tout
- Sécurité : **4/10**
- Problèmes : 
  - ❌ Pas de génération automatique sécurisée
  - ❌ Pas de partage famille
  - ❌ Vulnérable si ton PC se fait pirater
  - ❌ Synchronisation limitée

**Option 3 : Post-it / Fichier Excel** 🙈

- Liste de mots de passe dans `passwords.xlsx`
- Sécurité : **1/10**
- Commentaire : On ne juge pas, mais… vraiment, arrête ça.

**Option 4 : Gestionnaire commercial** (1Password, Dashlane…)

- ✅ Sécurité correcte
- ✅ Apps partout
- ❌ **36-60€/an** à vie
- ❌ Tes mots de passe stockés chez eux (confiance obligatoire)

**Option 5 : Vaultwarden auto-hébergé** 🏆

- ✅ Sécurité **maximale** (coffre-fort chiffré end-to-end)
- ✅ Apps iOS/Android/Windows/Mac/Linux/Extensions navigateur
- ✅ **Gratuit** à vie
- ✅ **Tes données chez toi**, pas aux USA

- - - - - -

Vaultwarden vs Bitwarden : Quelle différence ?
----------------------------------------------

### Petite histoire technique

**Bitwarden** = Gestionnaire de mots de passe open source créé en 2016

- Client officiel : Gratuit
- Serveur officiel : Gratuit (limité) ou 10$/an (Premium)

**Vaultwarden** (ex-Bitwarden\_RS) = Implémentation alternative du serveur Bitwarden

- Écrit en Rust (hyper léger et performant)
- **100% compatible** avec les apps Bitwarden officielles
- **Toutes les fonctionnalités Premium gratuites**
- Consomme 100x moins de ressources (512 Mo RAM vs 2 Go pour Bitwarden officiel)

💡 **En gros :** Tu utilises les apps **Bitwarden officielles** (iOS, Android, extensions navigateur…) mais connectées à **ton serveur Vaultwarden** au lieu du serveur Bitwarden.com.

**Résultat :** Fonctionnalités Premium + contrôle total + gratuit.

- - - - - -

Vaultwarden vs 1Password vs Dashlane vs LastPass
------------------------------------------------

Critère | Vaultwarden | 1Password | Dashlane | LastPass | Bitwarden Cloud | **Prix** | 🟢 Gratuit | 🔴 36€/an | 🔴 40€/an | 🟡 36€/an | 🟢 10$/an | **Open source** | 🟢 Oui | 🔴 Non | 🔴 Non | 🔴 Non | 🟢 Oui | **Auto-hébergé** | 🟢 Oui | 🔴 Non | 🔴 Non | 🔴 Non | 🟡 Possible | **Vie privée** | 🟢 100% toi | 🔴 Canada | 🔴 USA | 🔴 USA | 🟡 USA | **Apps mobiles** | 🟢 Gratuites | 🟢 Incluses | 🟢 Incluses | 🟢 Gratuites | 🟢 Gratuites | **Partage famille** | 🟢 Illimité | 🟡 5 pers. | 🟡 6 pers. | 🟡 6 pers. | 🟡 6 pers. | **2FA intégré** | 🟢 Oui (TOTP) | 🟢 Oui | 🟢 Oui | 🟡 Payant | 🟡 Premium | **Audit sécurité** | 🟡 Communauté | 🟢 Pro | 🟢 Pro | 🟡 Moyen | 🟢 Pro | **Facilité setup** | 🟡 Technique | 🟢 Facile | 🟢 Facile | 🟢 Facile | 🟢 Facile | 

**Verdict :**

- **Tu veux simple et assisté** → 1Password (mais tu paies)
- **Tu veux pas héberger toi-même** → Bitwarden Cloud (10$/an)
- **Tu veux gratuit + contrôle total + premium** → **Vaultwarden** ✅

- - - - - -

Le calcul économique
--------------------

**Gestionnaires commerciaux :**

- 1Password Famille : 5€/mois = **60€/an**
- Dashlane Premium : 3,33€/mois = **40€/an**
- LastPass Premium : 3€/mois = **36€/an**
- NordPass Premium : 1,49€/mois = **18€/an**

💰 **Sur 10 ans : 180-600€**

**Vaultwarden auto-hébergé :**

- Si serveur existant (Nextcloud/Jellyfin) : **0€/an**
- Si VPS dédié 512 Mo RAM : **24€/an** (2€/mois)

💰 **Économie sur 10 ans : 156-576€**

Et surtout, **tes mots de passe ne sont JAMAIS chez un tiers**.

- - - - - -

Avant de commencer : Comprendre la sécurité
-------------------------------------------

### Comment ça marche, le chiffrement ?

**Architecture Vaultwarden :**

1. **Sur ton appareil** : 
  - Tu tapes ton **Master Password** (le SEUL mot de passe à retenir)
  - L’app génère une **clé de chiffrement** depuis ce mot de passe
  - Tous tes mots de passe sont **chiffrés avec cette clé**
  - L’app envoie au serveur : données chiffrées + hash du Master Password
2. **Sur le serveur (ton Vaultwarden)** : 
  - Stocke les données **déjà chiffrées**
  - Ne peut **jamais déchiffrer** tes mots de passe
  - Sert juste de **boîte aux lettres sécurisée**
3. **Si ton serveur se fait pirater** : 
  - Le hacker récupère… des données chiffrées illisibles
  - Sans ton Master Password, **impossible de déchiffrer**
  - (Sauf si ton Master Password est « 123456 », évidemment)

💡 **Principe clé :** Le serveur est « zero-knowledge » = il ne connaît JAMAIS tes mots de passe en clair.

- - - - - -

### Le Master Password : TA responsabilité

⚠️ **ULTRA-CRITIQUE** : Si tu perds ton Master Password, **personne ne peut t’aider**.

**Pas de « mot de passe oublié »** comme sur Facebook. C’est le prix de la sécurité.

**Comment créer un bon Master Password :**

❌ **Mauvais :**

- `Azerty123!` (9 caractères, dictionnaire)
- `JeAimeLesChats2024` (mot de passe, pas passphrase)

✅ **Bon :**

- `Cheval-Batterie-Agrafe-Correcte` (méthode XKCD, 4 mots aléatoires)
- `Tr0uv3-M01-D@ns-Un-C@f3-@-P@r1s` (phrase perso modifiée)
- `9MonChien!Adore$LesCrepes7Bretonnes` (phrase + chiffres + symboles)

**Recommandation :**

- Minimum **12 caractères**
- Mix majuscules, minuscules, chiffres, symboles
- Mémorisable (tu vas le taper 10x/jour)
- **Écris-le sur papier** et mets-le dans un coffre/tiroir fermé (backup physique)

- - - - - -

Installation Vaultwarden avec Docker : Setup en 15 min
------------------------------------------------------

### Étape 1 : Préparer le serveur

```bash
# Si Docker pas installé (sinon skip)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
newgrp docker

# Créer la structure
mkdir -p ~/vaultwarden/data
cd ~/vaultwarden
touch .env

```

nano docker-compose.yml


**Configuration homelab-ready :**

```bash
services:
  vaultwarden:
    image: vaultwarden/server:latest
    # Pense à changer latest par la dernière version stable
    container_name: vaultwarden
    restart: unless-stopped
    
    ports:
      - "8000:80"  # Interface web
    
    volumes:
      - ./data:/data
    
    environment:
      # Domaine public (IMPORTANT pour les apps mobiles)
      - DOMAIN=https://vault.ton-domaine.fr
      
      # Admin token (généré ci-dessous)
      - ADMIN_TOKEN=${VAULTWARDEN_ADMIN_TOKEN}
      
      # Timezone
      - TZ=Europe/Paris
      
      # Sécurité : désactive les inscriptions publiques
      - SIGNUPS_ALLOWED=false
      
      # Autoriser les invitations par email (optionnel)
      - INVITATIONS_ALLOWED=true
      - SMTP_HOST=smtp.example.com
      - SMTP_FROM=vaultwarden@ton-domaine.fr
      - SMTP_PORT=587
      - SMTP_SECURITY=starttls
      - SMTP_USERNAME=ton-email@example.com
      - SMTP_PASSWORD=ton-mot-de-passe-smtp
      
      # Websocket (pour sync temps réel)
      - WEBSOCKET_ENABLED=true
      
      # Logs
      - LOG_LEVEL=info
      
      # Limiter les tentatives de connexion
      - LOGIN_RATELIMIT_MAX_BURST=10
      - LOGIN_RATELIMIT_SECONDS=60
    
    networks:
      - vaultwarden-network

networks:
  vaultwarden-network:
    driver: bridge

```

docker exec -it vaultwarden /vaultwarden hash --preset owasp

**Option 2 : Via un conteneur temporaire**

```bash
docker run --rm -it vaultwarden/server /vaultwarden hash --preset owasp
```

Enter password: ********
Re-enter password: ********
$argon2id$v=19$m=19456,t=2,p=1$cXpKdUxHSWhlaUs1QVVsSStkbTRPQVFPSmdpamFCMHdvYjVkWTVKaDdpYz0$E1UgBKjUCD2Roy0jdHAJvXihugpG+N9WcAaR8P6Qn/8

**💡 À savoir :** La chaîne qui commence par `$argon2id$v=19$...` est ton hash. C’est cette valeur que tu vas utiliser dans ton fichier `.env`.

- - - - - -

#### Configuration avec Fichier .env (RECOMMANDÉ)

Pour un environnement de dev ou homelab, l’utilisation d’un fichier `.env` est une bonne pratique. Ça évite d’exposer des variables sensibles directement dans le `docker-compose.yml` et ça facilite la gestion.

**Structure des fichiers :**

```bash
/vaultwarden/
├── .env
├── docker-compose.yml
└── data/
```

nano .env

**Contenu du .env :**

```bash
# ⚠️ IMPORTANT : Utilise des guillemets simples ' ' pour éviter les problèmes d'interpolation
VAULTWARDEN_ADMIN_TOKEN='$argon2id$v=19$m=19456,t=2,p=1$cXpKdUxHSWhlaUs1QVVsSStkbTRPQVFPSmdpamFCMHdvYjVkWTVKaDdpYz0$E1UgBKjUCD2Roy0jdHAJvXihugpG+N9WcAaR8P6Qn/8'
```

ADMIN_TOKEN=${VAULTWARDEN_ADMIN_TOKEN}

#### Vérification de la Configuration

Avant de lancer ton conteneur, vérifie que Docker Compose lit bien ton `.env` :

```bash
docker compose config
```

WARNING: The argon2id variable is not set. Defaulting to a blank string.
WARNING: The v variable is not set. Defaulting to a blank string.

**→ **Houston, on a un problème.** Tes guillemets sont mal configurés dans le `.env` ou le fichier n’est pas lu correctement.**

- - - - - -

### Étape 4 : Configurer les inscriptions

**Stratégie recommandée :**

```bash
# Option 1 : Désactiver complètement (tu créeras les comptes via admin)
SIGNUPS_ALLOWED=false
INVITATIONS_ALLOWED=true  # Tu invites par email

# Option 2 : Autoriser temporairement (pour toi, puis tu désactives)
SIGNUPS_ALLOWED=true
# → Tu crées ton compte
# → Tu remets à false
# → Tu relances : docker compose restart vaultwarden

```

# Démarrer
docker compose up -d

# Vérifier
docker ps
docker compose logs -f vaultwarden


✅ **Test rapide :** Ouvre `http://ton-ip-serveur:8000`

Si tu vois la page de connexion Vaultwarden, c’est bon ! 🎉

⚠️ **ATTENTION** : Pour l’instant c’est en HTTP.   
**NE CRÉE PAS ENCORE DE COMPTE**. On configure HTTPS d’abord (sinon ton Master Password part en clair sur le réseau).

- - - - - -

Configuration HTTPS avec Nginx Proxy Manager
--------------------------------------------

**Si tu as déjà NPM** (installé pour Nextcloud/Jellyfin), tu vas juste ajouter un nouveau proxy.

**Si tu n’as pas NPM**, consulte l’[article Nextcloud](https://brandonvisca.com/nextcloud-docker-installation-complete-2025/) pour l’installer (5 minutes).

### Ajouter le proxy Vaultwarden

1. **NPM Dashboard** → **Hosts** → **Proxy Hosts** → **Add Proxy Host**
2. **Details :**
  - Domain Names : `vault.ton-domaine.fr`
  - Scheme : `http`
  - Forward Hostname / IP : `vaultwarden` (ou IP serveur)
  - Forward Port : 8000
  - ✅ Websockets Support (important pour la sync temps réel)
  - ✅ Block Common Exploits
3. **SSL :**
  - ✅ Request a new SSL Certificate
  - ✅ Force SSL
  - ✅ HTTP/2 Support
  - ✅ HSTS Enabled (extra sécurité)
4. **Advanced (optionnel mais recommandé) :**

```bash
# Headers de sécurité
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "same-origin" always;

# Timeout (Vaultwarden est rapide, pas besoin de gros timeout)
proxy_connect_timeout 10;
proxy_send_timeout 10;
proxy_read_timeout 10;

```

K8#mL2@pN9!qR4$tV7&wX1%yZ5^aC3*bD6


Bon courage au hacker pour craquer ça. 😂

- - - - - -

### 5. Activer l’authentification à deux facteurs (2FA)

**Scénario** : Tu veux protéger ton compte Gmail avec 2FA.

1. **Gmail** → Paramètres → Sécurité → **Activer la validation en 2 étapes**
2. Choisis : **Application d’authentification**
3. Gmail affiche un **QR code**
4. **Vaultwarden** : 
  - Trouve ton identifiant Gmail dans le coffre
  - **Modifier** → **Code d’authentification (TOTP)**
  - Clique sur **📷 Scanner QR code** (depuis mobile) OU copie la clé manuelle
  - **Sauvegarder**
5. **Gmail** : Entre le code à 6 chiffres affiché par Vaultwarden → **Valider**

🎉 **Vaultwarden génère maintenant les codes 2FA automatiquement !**

💡 **Plus besoin de Google Authenticator/Authy** → Vaultwarden fait tout.

- - - - - -

Sécurité avancée
----------------

### Activer le 2FA sur ton compte Vaultwarden

**Scénario** : Quelqu’un vole ton Master Password. Sans 2FA, il accède à tout. Avec 2FA, il est bloqué. 🛡️

1. **Interface web** → **Paramètres** → **Sécurité** → **Authentification à deux étapes**
2. **Choix de la méthode** : **Option 1 : Authenticator (TOTP) – Recommandé**
  - Utilise une app type **Aegis** (Android, open source) ou **Raivo OTP** (iOS)
  - Scanne le QR code avec l’app
  - Entre le code de vérification → **Activer**
  
  **Option 2 : Clé de sécurité matérielle (Yubikey)**
  - Si tu as une Yubikey (~50€)
  - Plus sécurisé que TOTP (protection physique)
  
  **Option 3 : Email** (moins sécurisé, mais mieux que rien) 
  - Reçois un code par email à chaque connexion
3. **Codes de secours** : 
  - Vaultwarden génère des **codes de récupération uniques**
  - **IMPRIME-LES** et range-les dans un tiroir fermé
  - Si tu perds ton 2FA, ces codes te sauveront

🎉 **Ton compte Vaultwarden est maintenant ultra-sécurisé !**

- - - - - -

### Audit de sécurité de tes mots de passe

**Scénario** : Tu veux vérifier quels sont tes mots de passe faibles/réutilisés.

1. **Interface web** → **Outils** → **Rapports**
2. **Rapports disponibles** : 
  - **Mots de passe exposés** : Vérifie si tes mots de passe sont dans des fuites (HaveIBeenPwned)
  - **Mots de passe réutilisés** : Liste les mots de passe utilisés sur plusieurs sites
  - **Mots de passe faibles** : Détecte les mots de passe courts/simples
  - **Mots de passe inactifs** : Identifiants non utilisés depuis longtemps
  - **2FA non configuré** : Sites critiques sans 2FA
3. **Corriger** : 
  - Clique sur un identifiant faible → **Modifier** → **Générer un nouveau mot de passe** → Change-le sur le site

💡 **Fais cet audit 1x/an** pour maintenir une hygiène de sécurité parfaite.

- - - - - -

Backup & Restauration
-------------------------

### Exporter tes données (backup manuel)

⚠️ **IMPORTANT** : Le backup de Vaultwarden = tes mots de passe. **Protège-le comme de l’or**.

**Méthode 1 : Export chiffré (recommandé)**

1. **Interface web** → **Outils** → **Exporter le coffre**
2. **Format de fichier** : `.json (chiffré)`
3. **Master Password** : Entre-le pour déverrouiller
4. **Exporter** → Télécharge `vaultwarden_export_encrypted.json`
5. **Stockage du backup** : 
  - ✅ Disque dur externe chiffré (Veracrypt, LUKS)
  - ✅ Coffre-fort physique
  - ❌ Cloud non chiffré (Dropbox, Google Drive…)
  - ⚠️ Si cloud : chiffre le fichier avant (7-Zip avec mot de passe, GPG…)

**Méthode 2 : Backup base de données Docker**

```bash
# Backup du volume data
cd ~/vaultwarden
tar -czf vaultwarden-backup-$(date +%Y-%m-%d).tar.gz ./data

# Copier ailleurs (NAS, autre serveur...)
scp vaultwarden-backup-*.tar.gz user@nas:/backups/vaultwarden/

```

# Réinstaller Docker
curl -fsSL https://get.docker.com | sh

# Recréer la structure
mkdir -p ~/vaultwarden && cd ~/vaultwarden

# Copier le docker-compose.yml (tu l'as sauvegardé à part, hein ?)

# Extraire le backup
tar -xzf vaultwarden-backup-2025-XX-XX.tar.gz

# Lancer Vaultwarden
docker compose up -d


🎉 **Tous tes mots de passe sont de retour !**

- - - - - -

Cas d’usage réels
-----------------

### Scénario 1 : Particulier solo

**Setup :**

- Vaultwarden sur VPS existant (déjà Nextcloud/Jellyfin)
- 0€ supplémentaire

**Collection :**

- 120 identifiants (Gmail, Amazon, banques, forums, streaming…)
- 2FA activé sur 15 comptes critiques

**Économie :**

- Avant : 1Password = **36€/an**
- Après : **0€/an**
- 💰 **Gain sur 10 ans : 360€**

**Bénéfices** :

- Fini les « mot de passe oublié »
- Génération automatique de mots de passe ultra-sécurisés
- Remplissage automatique sur tous les appareils

- - - - - -

### Scénario 2 : Famille (4 personnes)

**Setup :**

- Vaultwarden sur Raspberry Pi 4 à la maison
- 0€ (déjà le Pi pour d’autres services)

**Utilisation :**

- **Papa** : 80 identifiants perso
- **Maman** : 65 identifiants perso
- **Ado 1** : 40 identifiants
- **Ado 2** : 35 identifiants
- **Partagés** : Netflix, Disney+, Wifi, NAS familial

**Organisation** :

- Coffre perso pour chacun (privé)
- Organisation « Famille » pour les services partagés
- Contrôle parental : les ados n’ont pas accès aux identifiants bancaires

**Économie :**

- Avant : 1Password Famille = **60€/an**
- Après : **0€/an**
- 💰 **Gain sur 10 ans : 600€**

- - - - - -

### Scénario 3 : Petite entreprise (8 employés)

**Setup :**

- Vaultwarden sur VPS 2 Go RAM (4€/mois)
- **48€/an**

**Utilisation :**

- Coffres individuels pour chaque employé
- Organisations : 
  - « Réseaux sociaux » (CM + Direction)
  - « Serveurs » (IT uniquement)
  - « Admin » (Comptabilité + RH)

**Sécurité** :

- 2FA obligatoire pour tous (Yubikey fournie à chacun)
- Audit mensuel des mots de passe faibles
- Révocation immédiate en cas de départ d’employé

**Économie :**

- Avant : 1Password Teams = 8 x 5€/mois = **480€/an**
- Après : **48€/an**
- 💰 **Gain : 432€/an → 4 320€ sur 10 ans**

- - - - - -

Problèmes courants & Solutions
----------------------------------

### ❌ « Impossible de se connecter au serveur »

**Symptômes :**

- L’extension/app affiche : « Cannot connect to the server »
- Timeout

**Solutions :**

1. **Vérifie que Vaultwarden tourne** : `docker ps # Tu dois voir 'vaultwarden' en 'Up'`
2. **Vérifie l’URL** : 
  - HTTPS activé ? `https://vault.ton-domaine.fr` (pas `http://`)
  - DNS configuré ? `ping vault.ton-domaine.fr`
3. **Check les logs** : `docker compose logs -f vaultwarden`

- - - - - -

### ❌ « Master Password oublié »

**Symptôme :** Tu as oublié ton Master Password. 😱

**Réalité dure :**

- ❌ **Aucune récupération possible**
- ❌ Même toi (l’admin serveur) ne peux pas réinitialiser
- ❌ Tes mots de passe sont perdus définitivement

**Solutions de secours** :

1. **Si tu as un backup chiffré exporté** : 
  - Impossible de déchiffrer sans Master Password
  - Perdu aussi 😢
2. **Si tu as une session encore ouverte quelque part** : 
  - Ordinateur/mobile où tu es encore connecté
  - **IMMÉDIATEMENT** : 
      - Va dans Paramètres → **Changer le Master Password**
      - Entre un nouveau Master Password
      - Exporte tout en `.json` déchiffré
      - Crée un nouveau compte avec le nouveau Master Password
      - Réimporte tout
3. **Prévention** : 
  - Écris ton Master Password sur **papier** (oui, vraiment)
  - Range-le dans un tiroir/coffre fermé
  - Ou utilise l’**indication de mot de passe** (indice sans révéler le mot de passe)

- - - - - -

### ❌ Apps mobiles : remplissage auto ne marche pas

**Symptôme :** L’app ne propose pas de remplir les mots de passe.

**Solutions** :

**iOS :**

Réglages → Mots de passe → Remplissage auto
→ Vérifie que Bitwarden est sélectionné
→ Désactive iCloud Keychain si activé (conflit)


**Android :**

Paramètres → Système → Langues et saisie
→ Services de saisie automatique → Bitwarden
→ OU Paramètres → Mots de passe → Gestionnaire de mots de passe
→ Sélectionne Bitwarden


- - - - - -

### ❌ Sync lente entre appareils

**Symptôme :** Tu ajoutes un mot de passe sur PC, il n’apparaît pas sur mobile après 5 minutes.

**Solution :**

1. **Vérifie Websocket** : `# Dans docker-compose.yml WEBSOCKET_ENABLED=true # Doit être à true`
2. **Force la sync manuelle** : 
  - Extension navigateur : Icône Bitwarden → **⟳ Synchroniser**
  - App mobile : Menu → **Paramètres** → **Synchroniser**
3. **Redémarre Vaultwarden** : `docker compose restart vaultwarden`

### ❌ Problème : « Invalid admin token »

**Cause :** Token mal copié ou guillemets incorrects dans le `.env`.

**Solution :**

1. Vérifie que tu as bien copié **tout** le hash (de `$argon2id$...` jusqu’à la fin)
2. Assure-toi d’utiliser des guillemets simples `' '` dans le `.env`
3. Pas d’espaces avant ou après le `=`

### ❌ Problème : « You are using a plain text ADMIN\_TOKEN »

**Cause :** Tu as modifié le token via l’interface web d’administration ET tu utilises encore une variable d’environnement.

**Solution :** Les paramètres définis via l’interface web **prennent le dessus** sur les variables d’environnement. Si tu veux revenir aux variables d’environnement, tu dois :

1. Supprimer le fichier `config.json` dans `/data`
2. Ou modifier le hash directement via l’interface admin

**⚠️ Ne touche PAS au `config.json` manuellement.** Ça peut tout casser. Passe toujours par l’interface ou les variables d’environnement.

- - - - - -

🎊 Conclusion : Le dernier pilier de ton indépendance
----------------------------------------------------

Félicitations ! Tu viens d’installer **le service le plus critique de ton infrastructure** : ton gestionnaire de mots de passe.

Pourquoi le plus critique ? Parce que c’est lui qui sécurise **tous les autres**. Sans Vaultwarden (ou équivalent), tu ne peux pas gérer sereinement Nextcloud, Jellyfin, et tous les services que tu vas déployer.

**Tu as maintenant le dernier pilier.**

Si tu as suivi mes tutos précédents, tu devrais avoir :

- ✅ Nextcloud (stockage cloud)
- ✅ Jellyfin (streaming perso)
- ✅ Vaultwarden (gestionnaire de mots de passe)

C’est **la stack d’indépendance numérique complète**. Tu remplaces Google Drive, Netflix ET LastPass avec des services que tu contrôles à 100%.

**Économie annuelle : 534€** (j’ai fait le calcul).

### 🚀 Et maintenant ?

Si tu veux une **vue d’ensemble de cette architecture**, comprendre comment ces 3 services s’interconnectent et suivre une roadmap progressive pour les sécuriser et les optimiser :

👉 **[Consulte le guide complet d’indépendance numérique 2025](https://brandonvisca.com/independance-numerique-2025-guide-complet/)**

Tu y trouveras :

- La checklist des 30 jours pour tout mettre en place
- Les scripts d’automatisation
- Les bonnes pratiques de sauvegarde
- La stratégie de sécurisation globale

*Spoiler : Ce n’est que le début. Il reste Prometheus+Grafana pour le monitoring, Uptime Kuma pour les alertes, et plein d’autres services à découvrir.*
