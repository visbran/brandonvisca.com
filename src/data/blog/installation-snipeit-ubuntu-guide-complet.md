---
title: "Installation SnipeIT Ubuntu : guide complet pour ne rien casser (tuto 2025)"
pubDatetime: "2025-10-03T12:38:51+02:00"
author: Brandon Visca
description: "Installez SnipeIT sur Ubuntu 22.04/24.04 : guide LAMP, MySQL, Git et permissions. Déployez votre ITSM d'inventaire IT en moins d'une heure, pas à pas."
tags:
  - linux
  - sysadmin
  - debutant
  - snipeit
  - docker
  - guide
---

**Méta description :** Installation SnipeIT Ubuntu 22.04/24.04 complète : guide LAMP, MySQL, Git, permissions et sécurité. Tuto installation SnipeIT Ubuntu étape par étape pour débutants.

---

Tu cherches un guide **d'installation SnipeIT Ubuntu** qui fonctionne vraiment ? Tu es au bon endroit. Après avoir lu mon [comparatif SnipeIT vs GLPI](https://brandonvisca.com/snipeit-vs-glpi-comparatif-itsm-inventaire-it/), tu es convaincu que SnipeIT c'est l'outil qu'il te faut. Maintenant, on va l'installer sur Ubuntu sans casser ton serveur.

Cette **installation SnipeIT Ubuntu** va couvrir Ubuntu 22.04 LTS et 24.04 LTS. On fait une installation native via Git (pas Docker), avec Apache, MySQL et toutes les bonnes pratiques de sécurité. Si tu cherches un tuto installation SnipeIT Ubuntu clair et sans bullshit, c'est parti.

L'installation SnipeIT sur Ubuntu, c'est pas sorcier... si tu sais ce que tu fais. Sinon, tu vas te retrouver avec des erreurs 500, des permissions foireuses et l'envie de tout effacer. Dans ce guide installation SnipeIT Ubuntu, on va faire ça proprement.

## Table of content

---

## Prérequis installation SnipeIT Ubuntu

Avant de foncer tête baissée dans cette **installation SnipeIT Ubuntu**, vérifie que tu as :

### Un serveur Ubuntu récent
- **Ubuntu 22.04 LTS** ou **24.04 LTS** (les versions stables)
- Minimum 2 Go RAM (4 Go c'est mieux)
- 20 Go d'espace disque minimum
- Accès root ou sudo

### Une connexion SSH fonctionnelle
Si tu ne sais pas encore bien configurer SSH, fonce lire mon guide sur [la sécurisation de ton serveur Linux](https://brandonvisca.com/securite-de-votre-serveur-linux/). Sérieusement, fais-le. Un serveur pas sécurisé, c'est une porte ouverte à tous les script kiddies du monde.

### Un nom de domaine (optionnel mais recommandé)
Genre `inventory.monentreprise.com`. Sinon tu peux utiliser l'IP du serveur, mais c'est moche et pas pro.

**À savoir :** On va faire une **installation SnipeIT Ubuntu** "basique" avec Apache dans ce guide. Si tu veux un setup production avec Nginx + reverse proxy + SSL, ce sera dans un prochain article dédié.

---

## Étape 1 : Préparer Ubuntu pour SnipeIT (stack LAMP)

LAMP, c'est l'acronyme pour **L**inux, **A**pache, **M**ySQL, **P**HP. C'est la stack requise pour cette **installation SnipeIT Ubuntu** (qui est une application Laravel PHP).

### Mise à jour du système

Première règle d'or : on met à jour avant d'installer quoi que ce soit.

```bash
sudo apt update && sudo apt upgrade -y
```

Ça va prendre 2-5 minutes selon ton serveur. Va te chercher un café.

### Installation d'Apache

Apache, c'est le serveur web qui va servir SnipeIT aux utilisateurs.

```bash
sudo apt install apache2 -y
```

Vérifie que ça tourne :

```bash
sudo systemctl status apache2
```

Tu dois voir un truc vert avec "active (running)". Si c'est rouge, y'a un problème. Google est ton ami.

### Installation de PHP et ses extensions

SnipeIT tourne sur Laravel, qui tourne sur PHP. On a besoin de PHP 8.1 minimum (8.3 c'est encore mieux).

```bash
sudo apt install php php-bcmath php-common php-ctype php-curl php-fileinfo \
php-fpm php-gd php-iconv php-intl php-mbstring php-mysql php-soap \
php-xml php-zip php-ldap libapache2-mod-php -y
```

Oui, c'est une grosse ligne. Chaque extension a son rôle :
- `php-mysql` : pour parler à MySQL
- `php-gd` : pour manipuler les images (QR codes, etc.)
- `php-ldap` : pour l'intégration Active Directory (voir mon [guide Ubuntu + AD](https://brandonvisca.com/connecter-les-systemes-ubuntu-a-active-directory-en-utilisant-sssd/))
- `php-curl` : pour les requêtes HTTP
- Les autres : requis par Laravel

Vérifie la version installée :

```bash
php -v
```

Tu dois voir quelque chose comme `PHP 8.3.x`. Si c'est 7.x, t'es sur une vieille version d'Ubuntu. Upgrade ton serveur.

### Installation de MySQL/MariaDB

**Pour les débutants :** MySQL, c'est une base de données. C'est là que SnipeIT va stocker tous tes assets, utilisateurs, etc. MariaDB, c'est un fork open source de MySQL (même chose, mais gratuit et libre).

```bash
sudo apt install mariadb-server -y
```

Sécurise l'installation :

```bash
sudo mysql_secure_installation
```

Réponds aux questions :
- **Enter current password for root** : Appuie sur Entrée (pas de mot de passe par défaut)
- **Set root password?** : Y (et choisis un mot de passe **costaud**)
- **Remove anonymous users?** : Y
- **Disallow root login remotely?** : Y
- **Remove test database?** : Y
- **Reload privilege tables?** : Y

**Erreur fréquente :** Oublier le mot de passe root MySQL. Note-le MAINTENANT dans ton gestionnaire de mots de passe. Pas sur un Post-It.

### Installation de Git et Composer

Git pour cloner SnipeIT, Composer pour gérer les dépendances PHP.

```bash
sudo apt install git unzip -y
```

Maintenant Composer :

```bash
curl -sS https://getcomposer.org/installer | php
sudo mv composer.phar /usr/local/bin/composer
```

Vérifie :

```bash
composer --version
```

Tu dois voir `Composer version 2.x.x`.

---

## Étape 2 : Configurer MySQL pour SnipeIT

On va créer une base de données dédiée pour notre **installation SnipeIT Ubuntu**. **Jamais** utiliser la base `root` pour une application.

### Connexion à MySQL

```bash
sudo mysql -u root -p
```

Entre le mot de passe root que tu as défini juste avant.

### Création de la base et de l'utilisateur

**Pour les débutants :** On va créer une "boîte" (database) où SnipeIT va ranger ses données, et un "utilisateur" qui aura accès uniquement à cette boîte. C'est le principe de moindre privilège.

```sql
CREATE DATABASE snipeit CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'snipeit'@'localhost' IDENTIFIED BY 'MotDePasseUltraSecurise123!';
GRANT ALL PRIVILEGES ON snipeit.* TO 'snipeit'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

**⚠️ IMPORTANT :** Change `MotDePasseUltraSecurise123!` par un vrai mot de passe costaud. Genre 20 caractères aléatoires. Note-le quelque part de sûr.

**Explication ligne par ligne :**
- `CREATE DATABASE` : crée la base de données avec encodage UTF-8 (pour les caractères accentués)
- `CREATE USER` : crée un utilisateur qui peut se connecter depuis localhost uniquement
- `GRANT ALL` : donne tous les droits sur la base `snipeit.*` à cet utilisateur
- `FLUSH PRIVILEGES` : recharge les permissions
- `EXIT` : tu sors de MySQL

---

## Étape 3 : Installer SnipeIT Ubuntu via Git

Cette étape est cruciale pour ton **installation SnipeIT Ubuntu**. On va cloner le repo officiel dans `/var/www/snipe-it`, le répertoire standard pour les applications web sur Ubuntu.

### Clone du repo Git

```bash
cd /var/www
sudo git clone https://github.com/snipe/snipe-it.git snipe-it
```

Ça va télécharger les ~100 Mo de code. Patience.

### Pourquoi Git et pas un zip ?

Avec Git, les mises à jour c'est :
```bash
cd /var/www/snipe-it
sudo git pull
```

Avec un zip, tu dois tout retélécharger, réextract, reconfigurer. Git = efficace.

---

## Étape 4 : Configuration Laravel et permissions

### Copie du fichier de configuration

SnipeIT fournit un fichier d'exemple `.env.example`. On va le copier en `.env` et le configurer.

```bash
cd /var/www/snipe-it
sudo cp .env.example .env
```

### Édition de la configuration

```bash
sudo nano .env
```

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

**Bon à savoir :** Le fichier `.env` contient des secrets (mots de passe, clés API). JAMAIS le commit dans Git. Heureusement, SnipeIT a déjà mis `.env` dans `.gitignore`.

Sauvegarde avec `Ctrl+O`, `Entrée`, puis `Ctrl+X`.

### Permissions du répertoire

C'est LA partie où 90% des gens se plantent. Apache tourne avec l'utilisateur `www-data`. Il faut que cet utilisateur puisse écrire dans certains dossiers.

```bash
sudo chown -R www-data:www-data /var/www/snipe-it
sudo chmod -R 755 /var/www/snipe-it
sudo chmod -R 775 /var/www/snipe-it/storage
sudo chmod -R 775 /var/www/snipe-it/public/uploads
```

**Explication :**
- `chown -R` : change le propriétaire récursivement
- `chmod 755` : lecture/exécution pour tous, écriture pour le propriétaire
- `chmod 775` sur storage : Laravel doit pouvoir y écrire des logs et caches

**Erreur fréquente :** Mettre `chmod 777` partout. NE FAIS JAMAIS ÇA. C'est un trou de sécurité béant. Si tu vois ça dans un tuto, ferme l'onglet.

---

## Étape 5 : Installation des dépendances Composer

Composer va télécharger toutes les bibliothèques PHP dont SnipeIT a besoin.

```bash
cd /var/www/snipe-it
sudo -u www-data composer update --no-plugins --no-scripts
sudo -u www-data composer install --no-dev --prefer-source --no-plugins --no-scripts
```

**Attention :** On lance Composer avec `sudo -u www-data` pour que les fichiers créés appartiennent à `www-data`. Si tu le lances en root, tu vas avoir des problèmes de permissions après.

Ça va prendre 5-10 minutes. Va chercher un autre café.

Tu vas voir des warnings du style "Do not run Composer as root". C'est normal, on utilise `sudo -u www-data` pour contourner ça.

### Génération de la clé d'application

Laravel utilise une clé pour chiffrer les données sensibles (sessions, cookies, etc.).

```bash
sudo -u www-data php artisan key:generate
```

Tape `yes` quand il te demande si tu veux continuer. Cette commande va écrire une clé dans le fichier `.env` automatiquement.

---

## Étape 6 : Configuration Apache pour SnipeIT

On va créer un VirtualHost Apache pour servir notre **installation SnipeIT Ubuntu**.

### Création du fichier de configuration

```bash
sudo nano /etc/apache2/sites-available/snipe-it.conf
```

Colle ça dedans :

```apache
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
```

**Remplace `ton-serveur.com`** par ton domaine ou l'IP de ton serveur.

**Explication :**
- `DocumentRoot` : pointe vers `/public`, pas `/var/www/snipe-it` (sécurité Laravel)
- `AllowOverride All` : permet au `.htaccess` de SnipeIT de fonctionner
- `Require all granted` : autorise l'accès (on sécurisera plus tard)

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

Vérifie qu'Apache est OK :

```bash
sudo systemctl status apache2
```

Si c'est rouge avec une erreur, y'a une faute de syntaxe dans ton fichier de config. Relis-le.

---

## Étape 7 : Finaliser l'installation SnipeIT Ubuntu

### Accès à l'interface web

Ouvre ton navigateur et va sur :
- `http://ton-domaine.com` ou
- `http://IP-de-ton-serveur`

Tu devrais voir la page de pré-flight check de SnipeIT. C'est presque fini, ton **installation SnipeIT Ubuntu** touche au but !

### Configuration étape par étape

**1. Pré-flight Check**

SnipeIT vérifie que toutes les extensions PHP sont installées. Si un truc est rouge, retourne à l'étape 1 et installe ce qui manque.

Clique sur **"Next: Create Database Tables"**.

**2. Migration de la base de données**

SnipeIT va créer toutes les tables dans MySQL. Ça prend 10-30 secondes.

Clique sur **"Next: Create User"**.

**3. Création du compte admin**

Remplis :
- **Site Name** : Nom de ton entreprise
- **First Name** / **Last Name** : Ton nom
- **Email** : Ton email
- **Username** : admin (ou autre)
- **Password** : Un mot de passe **costaud** (minimum 12 caractères, avec chiffres et symboles)

Clique sur **"Next: Save User"**.

**4. Configuration finale**

Tu peux configurer :
- **Logo** : ton logo d'entreprise
- **Email Settings** : pour les notifications (on fera ça après)
- **Default Language** : Français

Clique sur **"Save Settings"**.

🎉 **Félicitations !** Ton **installation SnipeIT Ubuntu** est terminée et fonctionnelle.

---

## Bonnes pratiques post-installation

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

Mets ça dans un cron qui tourne tous les jours.

### 2. Activer HTTPS (SSL)

**Ne lance JAMAIS SnipeIT en production sans HTTPS.** Les mots de passe passeraient en clair sur le réseau.

On fera un guide dédié avec Let's Encrypt + Nginx dans un prochain article.

### 3. Restreindre l'accès par IP (si interne)

Si SnipeIT n'est accessible que depuis ton réseau interne :

```apache
<Directory /var/www/snipe-it/public>
    Options Indexes FollowSymLinks MultiViews
    AllowOverride All
    Require ip 192.168.1.0/24  # Ton réseau local
</Directory>
```

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

**Bonnes pratiques :** Teste TOUJOURS les mises à jour sur un serveur de dev avant de les passer en prod.

---

## Dépannage des erreurs courantes

### Erreur 500 - Internal Server Error

**Cause :** Problème de permissions ou de configuration.

**Solution :**
```bash
# Vérifie les logs Apache
sudo tail -f /var/log/apache2/snipeit-error.log

# Souvent, c'est les permissions storage/
sudo chmod -R 775 /var/www/snipe-it/storage
sudo chown -R www-data:www-data /var/www/snipe-it/storage
```

### Page blanche

**Cause :** PHP pas configuré correctement dans Apache.

**Solution :**
```bash
# Vérifie que mod_php est activé
sudo a2enmod php8.3  # Adapte selon ta version
sudo systemctl restart apache2
```

### "No application encryption key has been specified"

**Cause :** Tu as oublié de générer la clé APP_KEY.

**Solution :**
```bash
cd /var/www/snipe-it
sudo -u www-data php artisan key:generate
```

---

## Où héberger ton installation SnipeIT Ubuntu ?

Tu n'as pas encore de serveur Ubuntu pour ton **installation SnipeIT** ? Voici mes recommandations testées :

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

---

## Conclusion : installation SnipeIT Ubuntu réussie

Voilà, tu as maintenant une **installation SnipeIT Ubuntu** fonctionnelle et propre. Pas de Docker, pas de magie noire, juste une installation native sur Ubuntu qui marche du premier coup.

**Récap de cette installation SnipeIT Ubuntu :**
✅ Stack LAMP configurée sur Ubuntu (Apache, MySQL, PHP)  
✅ SnipeIT cloné via Git (mises à jour faciles)  
✅ Base de données MySQL créée et sécurisée  
✅ Permissions correctement configurées pour Ubuntu  
✅ Premier compte admin créé

Cette **installation SnipeIT Ubuntu 22.04/24.04** est maintenant prête pour la production.

**Et maintenant ?**

Dans le **prochain article** de cette série, on va passer à la vitesse supérieure :
- Configuration avancée de SnipeIT
- Intégration LDAP/Active Directory
- Pallier l'absence de network discovery avec Nmap + scripts
- Personnalisation des champs et workflows

En attendant, si tu veux sécuriser ton installation avec Nginx + reverse proxy + SSL, surveille le blog, un guide dédié arrive bientôt.

Et si ton terminal ressemble encore à celui de Windows XP, fais un tour sur mon guide [Oh My Zsh + Powerlevel10k](https://brandonvisca.com/installation-oh-my-zsh-powerlevel10k-guide-complet/). Un bon admin, ça commence par un terminal qui envoie.

### Liens internes intégrés :
1. [Comparatif SnipeIT vs GLPI](https://brandonvisca.com/snipeit-vs-glpi-comparatif-itsm-inventaire-it/) ← Article 2
2. [Sécurisation de ton serveur Linux](https://brandonvisca.com/securite-de-votre-serveur-linux/)
3. [Guide Ubuntu + Active Directory](https://brandonvisca.com/connecter-les-systemes-ubuntu-a-active-directory-en-utilisant-sssd/)
4. [Oh My Zsh + Powerlevel10k](https://brandonvisca.com/installation-oh-my-zsh-powerlevel10k-guide-complet/)

### Liens externes (documentation) :
- https://snipe-it.readme.io/docs/installation
- https://github.com/snipe/snipe-it

## Articles connexes

- [ITSM : pourquoi votre Excel va vous rendre fou](/itsm-snipeit-alternative-excel-inventaire-it/)
- [SnipeIT vs GLPI : David contre Goliath dans l'arène de l'ITSM](/snipeit-vs-glpi-comparatif-itsm-inventaire-it/)
- [Auto-hébergement : Le guide ultime 2025](/auto-hebergement-guide-complet-2025/)
