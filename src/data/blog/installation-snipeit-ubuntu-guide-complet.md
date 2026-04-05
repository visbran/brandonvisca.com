---
title: "Installation SnipeIT Ubuntu : guide complet pour ne rien casser (tuto 2025)"
pubDatetime: "2025-10-03T12:38:51+02:00"
description: "nstallation SnipeIT Ubuntu 22.04/24.04 complète : guide LAMP, MySQL, Git, permissions et sécurité. Tuto installation SnipeIT Ubuntu étape par étape pour..."
tags:
  - snipeit
  - itsm
  - ubuntu
  - linux
  - lamp
  - mysql
  - laravel
  - installation
  - tutoriel
  - debutant
---

-----------
## Table des matières


  - [Un serveur Ubuntu récent](#un-serveur-ubuntu-recent)
  - [Une connexion SSH fonctionnelle](#une-connexion-ssh-fonctionnelle)
  - [Un nom de domaine (optionnel mais recommandé)](#un-nom-de-domaine-optionnel-mais-recommande)
- [Étape 1 : Préparer Ubuntu pour SnipeIT (stack LAMP)](#etape-1-preparer-ubuntu-pour-snipe-it-stack-lamp)
  - [Mise à jour du système](#mise-a-jour-du-systeme)
  - [Installation d’Apache](#installation-d-apache)
  - [Installation de PHP et ses extensions](#installation-de-php-et-ses-extensions)
  - [Installation de MySQL/MariaDB](#installation-de-my-sql-maria-db)
  - [Installation de Git et Composer](#installation-de-git-et-composer)
- [Étape 2 : Configurer MySQL pour SnipeIT](#etape-2-configurer-my-sql-pour-snipe-it)
  - [Connexion à MySQL](#connexion-a-my-sql)
  - [Création de la base et de l’utilisateur](#creation-de-la-base-et-de-lutilisateur)
- [Étape 3 : Installer SnipeIT Ubuntu via Git](#etape-3-installer-snipe-it-ubuntu-via-git)
  - [Clone du repo Git](#clone-du-repo-git)
  - [Pourquoi Git et pas un zip ?](#pourquoi-git-et-pas-un-zip)
- [Étape 4 : Configuration Laravel et permissions](#etape-4-configuration-laravel-et-permissions)
  - [Copie du fichier de configuration](#copie-du-fichier-de-configuration)
  - [Édition de la configuration](#edition-de-la-configuration)
  - [Permissions du répertoire](#permissions-du-repertoire)
- [Étape 5 : Installation des dépendances Composer](#etape-5-installation-des-dependances-composer)
  - [Génération de la clé d’application](#generation-de-la-cle-dapplication)
- [Étape 6 : Configuration Apache pour SnipeIT](#etape-6-configuration-apache-pour-snipe-it)
  - [Création du fichier de configuration](#creation-du-fichier-de-configuration)
  - [Activation du site et des modules](#activation-du-site-et-des-modules)
- [Étape 7 : Finaliser l’installation SnipeIT Ubuntu](#etape-7-finaliser-linstallation-snipe-it-ubuntu)
  - [Accès à l’interface web](#acces-a-linterface-web)
  - [Configuration étape par étape](#configuration-etape-par-etape)
- [Bonnes pratiques post-installation](#bonnes-pratiques-post-installation)
  - [1. Sauvegardes automatiques](#1-sauvegardes-automatiques)
  - [2. Activer HTTPS (SSL)](#2-activer-https-ssl)
  - [3. Restreindre l’accès par IP (si interne)](#3-restreindre-lacces-par-ip-si-interne)
  - [4. Mises à jour régulières](#4-mises-a-jour-regulieres)
- [Dépannage des erreurs courantes](#depannage-des-erreurs-courantes)
  - [Erreur 500 – Internal Server Error](#erreur-500-internal-server-error)
  - [Page blanche](#page-blanche)
  - [« No application encryption key has been specified »](#no-application-encryption-key-has-been-specified)
- [Où héberger ton installation SnipeIT Ubuntu ?](#ou-heberger-ton-installation-snipe-it-ubuntu)
  - [Pour débuter (PME < 50 utilisateurs)](#pour-debuter-pme-50-utilisateurs)
  - [Pour les plus exigeants](#pour-les-plus-exigeants)
  - [Pour les gros parcs (> 200 assets)](#pour-les-gros-parcs-200-assets)
- [Conclusion : installation SnipeIT Ubuntu réussie](#conclusion-installation-snipe-it-ubuntu-reussie)


Cette **installation SnipeIT Ubuntu** va couvrir Ubuntu 22.04 LTS et 24.04 LTS. On fait une installation native via Git (pas Docker), avec Apache, MySQL et toutes les bonnes pratiques de sécurité. Si tu cherches un tuto installation SnipeIT Ubuntu clair et sans bullshit, c’est parti.

L’installation SnipeIT sur Ubuntu, c’est pas sorcier… si tu sais ce que tu fais. Sinon, tu vas te retrouver avec des erreurs 500, des permissions foireuses et l’envie de tout effacer. Dans ce guide installation SnipeIT Ubuntu, on va faire ça proprement.

- - - - - -

Prérequis installation SnipeIT Ubuntu
-------------------------------------

Avant de foncer tête baissée dans cette **installation SnipeIT Ubuntu**, vérifie que tu as :

### Un serveur Ubuntu récent

- **Ubuntu 22.04 LTS** ou **24.04 LTS** (les versions stables)
- Minimum 2 Go RAM (4 Go c’est mieux)
- 20 Go d’espace disque minimum
- Accès root ou sudo

### Une connexion SSH fonctionnelle

Si tu ne sais pas encore bien configurer SSH, fonce lire mon guide sur [la sécurisation de ton serveur Linux](https://brandonvisca.com/securite-de-votre-serveur-linux/). Sérieusement, fais-le. Un serveur pas sécurisé, c’est une porte ouverte à tous les script kiddies du monde.

### Un nom de domaine (optionnel mais recommandé)

Genre `inventory.monentreprise.com`. Sinon tu peux utiliser l’IP du serveur, mais c’est moche et pas pro.

**À savoir :** On va faire une **installation SnipeIT Ubuntu** « basique » avec Apache dans ce guide. Si tu veux un setup production avec Nginx + reverse proxy + SSL, ce sera dans un prochain article dédié.

- - - - - -

Étape 1 : Préparer Ubuntu pour SnipeIT (stack LAMP)
---------------------------------------------------

LAMP, c’est l’acronyme pour **L**inux, **A**pache, **M**ySQL, **P**HP. C’est la stack requise pour cette **installation SnipeIT Ubuntu** (qui est une application Laravel PHP).

### Mise à jour du système

Première règle d’or : on met à jour avant d’installer quoi que ce soit.

```bash
sudo apt update && sudo apt upgrade -y

```

sudo apt install apache2 -y


Vérifie que ça tourne :

```bash
sudo systemctl status apache2

```

sudo apt install php php-bcmath php-common php-ctype php-curl php-fileinfo \
php-fpm php-gd php-iconv php-intl php-mbstring php-mysql php-soap \
php-xml php-zip php-ldap libapache2-mod-php -y


Oui, c’est une grosse ligne. Chaque extension a son rôle :

- `php-mysql` : pour parler à MySQL
- `php-gd` : pour manipuler les images (QR codes, etc.)
- `php-ldap` : pour l’intégration Active Directory (voir mon [guide Ubuntu + AD](https://brandonvisca.com/connecter-les-systemes-ubuntu-a-active-directory-en-utilisant-sssd/))
- `php-curl` : pour les requêtes HTTP
- Les autres : requis par Laravel

Vérifie la version installée :

```bash
php -v

```

sudo apt install mariadb-server -y


Sécurise l’installation :

```bash
sudo mysql_secure_installation

```

sudo apt install git unzip -y


Maintenant Composer :

```bash
curl -sS https://getcomposer.org/installer | php
sudo mv composer.phar /usr/local/bin/composer

```

composer --version


Tu dois voir `Composer version 2.x.x`.

- - - - - -

Étape 2 : Configurer MySQL pour SnipeIT
---------------------------------------

On va créer une base de données dédiée pour notre **installation SnipeIT Ubuntu**. **Jamais** utiliser la base `root` pour une application.

### Connexion à MySQL

```bash
sudo mysql -u root -p

```

CREATE DATABASE snipeit CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'snipeit'@'localhost' IDENTIFIED BY 'MotDePasseUltraSecurise123!';
GRANT ALL PRIVILEGES ON snipeit.* TO 'snipeit'@'localhost';
FLUSH PRIVILEGES;
EXIT;


**⚠️ IMPORTANT :** Change `MotDePasseUltraSecurise123!` par un vrai mot de passe costaud. Genre 20 caractères aléatoires. Note-le quelque part de sûr.

**Explication ligne par ligne :**

- `CREATE DATABASE` : crée la base de données avec encodage UTF-8 (pour les caractères accentués)
- `CREATE USER` : crée un utilisateur qui peut se connecter depuis localhost uniquement
- `GRANT ALL` : donne tous les droits sur la base `snipeit.*` à cet utilisateur
- `FLUSH PRIVILEGES` : recharge les permissions
- `EXIT` : tu sors de MySQL

- - - - - -

Étape 3 : Installer SnipeIT Ubuntu via Git
------------------------------------------

Cette étape est cruciale pour ton **installation SnipeIT Ubuntu**. On va cloner le repo officiel dans `/var/www/snipe-it`, le répertoire standard pour les applications web sur Ubuntu.

### Clone du repo Git

```bash
cd /var/www
sudo git clone https://github.com/snipe/snipe-it.git snipe-it

```

cd /var/www/snipe-it
sudo git pull


Avec un zip, tu dois tout retélécharger, réextract, reconfigurer. Git = efficace.

- - - - - -

Étape 4 : Configuration Laravel et permissions
----------------------------------------------

### Copie du fichier de configuration

SnipeIT fournit un fichier d’exemple `.env.example`. On va le copier en `.env` et le configurer.

```bash
cd /var/www/snipe-it
sudo cp .env.example .env

```

sudo nano .env


Trouve et modifie ces lignes :

```bash
# URL de ton SnipeIT (sans trailing slash)
APP_URL=http://ton-serveur.com
# ou http://192.168.1.100 si tu utilises l'IP

# Fuseau horaire (liste complète : https://www.php.net/manual/en/timezones.php)
APP_TIMEZONE='Europe/Paris'

# Configuration base de données
DB_DATABASE=snipeit
DB_USERNAME=snipeit
DB_PASSWORD=MotDePasseUltraSecurise123!

```

sudo chown -R www-data:www-data /var/www/snipe-it
sudo chmod -R 755 /var/www/snipe-it
sudo chmod -R 775 /var/www/snipe-it/storage
sudo chmod -R 775 /var/www/snipe-it/public/uploads


**Explication :**

- `chown -R` : change le propriétaire récursivement
- `chmod 755` : lecture/exécution pour tous, écriture pour le propriétaire
- `chmod 775` sur storage : Laravel doit pouvoir y écrire des logs et caches

**Erreur fréquente :** Mettre `chmod 777` partout. NE FAIS JAMAIS ÇA. C’est un trou de sécurité béant. Si tu vois ça dans un tuto, ferme l’onglet.

- - - - - -

Étape 5 : Installation des dépendances Composer
-----------------------------------------------

Composer va télécharger toutes les bibliothèques PHP dont SnipeIT a besoin.

```bash
cd /var/www/snipe-it
sudo -u www-data composer update --no-plugins --no-scripts
sudo -u www-data composer install --no-dev --prefer-source --no-plugins --no-scripts

```

sudo -u www-data php artisan key:generate


Tape `yes` quand il te demande si tu veux continuer. Cette commande va écrire une clé dans le fichier `.env` automatiquement.

- - - - - -

Étape 6 : Configuration Apache pour SnipeIT
-------------------------------------------

On va créer un VirtualHost Apache pour servir notre **installation SnipeIT Ubuntu**.

### Création du fichier de configuration

```bash
sudo nano /etc/apache2/sites-available/snipe-it.conf

```

<VirtualHost *:80>
    ServerName ton-serveur.com
    DocumentRoot /var/www/snipe-it/public

    <Directory /var/www/snipe-it/public>
        Options Indexes FollowSymLinks MultiViews
        AllowOverride All
        Require all granted
    </Directory>

    ErrorLog ${APACHE_LOG_DIR}/snipeit-error.log
    CustomLog ${APACHE_LOG_DIR}/snipeit-access.log combined
</VirtualHost>


**Remplace `ton-serveur.com`** par ton domaine ou l’IP de ton serveur.

**Explication :**

- `DocumentRoot` : pointe vers `/public`, pas `/var/www/snipe-it` (sécurité Laravel)
- `AllowOverride All` : permet au `.htaccess` de SnipeIT de fonctionner
- `Require all granted` : autorise l’accès (on sécurisera plus tard)

Sauvegarde et quitte.

### Activation du site et des modules

```bash
# Désactive le site par défaut
sudo a2dissite 000-default.conf

# Active le site SnipeIT
sudo a2ensite snipe-it.conf

# Active mod_rewrite (requis par Laravel)
sudo a2enmod rewrite

# Redémarre Apache
sudo systemctl restart apache2

```

sudo systemctl status apache2


Si c’est rouge avec une erreur, y’a une faute de syntaxe dans ton fichier de config. Relis-le.

- - - - - -

Étape 7 : Finaliser l’installation SnipeIT Ubuntu
-------------------------------------------------

### Accès à l’interface web

Ouvre ton navigateur et va sur :

- `http://ton-domaine.com` ou
- `http://IP-de-ton-serveur`

Tu devrais voir la page de pré-flight check de SnipeIT. C’est presque fini, ton **installation SnipeIT Ubuntu** touche au but !

### Configuration étape par étape

**1. Pré-flight Check**

SnipeIT vérifie que toutes les extensions PHP sont installées. Si un truc est rouge, retourne à l’étape 1 et installe ce qui manque.

Clique sur **« Next: Create Database Tables »**.

**2. Migration de la base de données**

SnipeIT va créer toutes les tables dans MySQL. Ça prend 10-30 secondes.

Clique sur **« Next: Create User »**.

**3. Création du compte admin**

Remplis :

- **Site Name** : Nom de ton entreprise
- **First Name** / **Last Name** : Ton nom
- **Email** : Ton email
- **Username** : admin (ou autre)
- **Password** : Un mot de passe **costaud** (minimum 12 caractères, avec chiffres et symboles)

Clique sur **« Next: Save User »**.

**4. Configuration finale**

Tu peux configurer :

- **Logo** : ton logo d’entreprise
- **Email Settings** : pour les notifications (on fera ça après)
- **Default Language** : Français

Clique sur **« Save Settings »**.

🎉 **Félicitations !** Ton **installation SnipeIT Ubuntu** est terminée et fonctionnelle.

👉 La prochaine étape ? Automatiser le remplissage de ton inventaire avec [SnipeAgent pour Windows](https://brandonvisca.com/snipeagent-automatiser-inventaire-windows-snipeit/). Fini la saisie manuelle, l’agent remplit ta base tout seul.

- - - - - -

Bonnes pratiques post-installation
----------------------------------

### 1. Sauvegardes automatiques

**Tu dois** sauvegarder :

- La base de données MySQL (`/var/lib/mysql/snipeit/`)
- Le fichier `.env` (`/var/www/snipe-it/.env`)
- Les uploads (`/var/www/snipe-it/public/uploads/`)

Script de sauvegarde simple :

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/snipeit"

# Backup MySQL
mysqldump -u root -p'MotDePasseRoot' snipeit > $BACKUP_DIR/snipeit_$DATE.sql

# Backup uploads
tar -czf $BACKUP_DIR/uploads_$DATE.tar.gz /var/www/snipe-it/public/uploads/

# Backup .env
cp /var/www/snipe-it/.env $BACKUP_DIR/env_$DATE.backup

```

<Directory /var/www/snipe-it/public>
    Options Indexes FollowSymLinks MultiViews
    AllowOverride All
    Require ip 192.168.1.0/24  # Ton réseau local
</Directory>


### 4. Mises à jour régulières

Tous les mois (ou quand une maj de sécurité sort) :

```bash
cd /var/www/snipe-it
sudo -u www-data php artisan down  # Mode maintenance
sudo git pull
sudo -u www-data composer install --no-dev --prefer-source
sudo -u www-data php artisan migrate
sudo -u www-data php artisan up  # Réactive

```

# Vérifie les logs Apache
sudo tail -f /var/log/apache2/snipeit-error.log

# Souvent, c'est les permissions storage/
sudo chmod -R 775 /var/www/snipe-it/storage
sudo chown -R www-data:www-data /var/www/snipe-it/storage


### Page blanche

**Cause :** PHP pas configuré correctement dans Apache.

**Solution :**

```bash
# Vérifie que mod_php est activé
sudo a2enmod php8.3  # Adapte selon ta version
sudo systemctl restart apache2

```

cd /var/www/snipe-it
sudo -u www-data php artisan key:generate


- - - - - -

Où héberger ton installation SnipeIT Ubuntu ?
---------------------------------------------

Tu n’as pas encore de serveur Ubuntu pour ton **installation SnipeIT** ? Voici mes recommandations testées :

### Pour débuter (PME < 50 utilisateurs)

**Hostinger VPS KVM 2** : 8,99€/mois

- 2 vCPU, 4 Go RAM, 100 Go SSD NVMe
- Ubuntu 22.04 ou 24.04 pré-installé
- Datacenter France/Pays-Bas
- Support français 24/7
- Parfait pour une **installation SnipeIT Ubuntu** + quelques services

### Pour les plus exigeants

**Webdock Premium** : 12€/mois

- 2 vCPU, 4 Go RAM, 160 Go NVMe
- Ubuntu optimisé pour Laravel
- Performance excellente
- Orienté développeur
- Backups automatiques inclus
- Idéal pour **installation SnipeIT Ubuntu** en production

### Pour les gros parcs (> 200 assets)

**DigitalOcean Droplet** : 18$/mois

- 2 vCPU, 4 Go RAM, 80 Go SSD
- Ubuntu 24.04 LTS
- Datacenter Europe
- Scalabilité facile
- API complète pour automatisation
- Recommandé pour **installation SnipeIT Ubuntu** haute disponibilité

- - - - - -

Conclusion : installation SnipeIT Ubuntu réussie
------------------------------------------------

Voilà, tu as maintenant une **installation SnipeIT Ubuntu** fonctionnelle et propre. Pas de Docker, pas de magie noire, juste une installation native sur Ubuntu qui marche du premier coup.

**Récap de cette installation SnipeIT Ubuntu :**   
  
✅ Stack LAMP configurée sur Ubuntu (Apache, MySQL, PHP)  
✅ SnipeIT cloné via Git (mises à jour faciles)  
✅ Base de données MySQL créée et sécurisée  
✅ Permissions correctement configurées pour Ubuntu  
✅ Premier compte admin créé

Cette **installation SnipeIT Ubuntu 22.04/24.04** est maintenant prête pour la production.

**Et maintenant ?**

Dans le **[prochain article](https://brandonvisca.com/configuration-avancee-snipeit-ldap-teams-automatisation/)** de cette série, on va passer à la vitesse supérieure :

- Configuration avancée de SnipeIT
- Intégration LDAP/Active Directory
- Pallier l’absence de network discovery avec Nmap + scripts
- Personnalisation des champs et workflows

Et si ton terminal ressemble encore à celui de Windows XP, fais un tour sur mon guide [Oh My Zsh + Powerlevel10k](https://brandonvisca.com/installation-oh-my-zsh-powerlevel10k-guide-complet/). Un bon admin, ça commence par un terminal qui envoie.

**💬 Un problème lors de l’installation ?** Balance ton erreur en commentaire, on va débugguer ça ensemble !
