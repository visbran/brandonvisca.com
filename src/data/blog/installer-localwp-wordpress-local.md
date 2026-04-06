---
title: "LocalWP : Ton lab WordPress en 5 min (guide complet 2025 + migration prod)"
pubDatetime: "2025-02-24T19:12:37+01:00"
description: "LocalWP, c''est ton lab WordPress en local sans se faire chier avec XAMPP. Installe, teste, pète tout, et déploie en prod quand c''est carré. Guide comp..."
tags:
  - developpement
  - linux
  - macos
  - windows
  - guide
  - debutant
faqs:
  - question: "LocalWP est-il gratuit ?"
    answer: "Oui, 100% gratuit sans version premium obligatoire ni limitations. Monétisé via intégrations avec hébergeurs."
  - question: "LocalWP fonctionne-t-il sur Windows/Mac/Linux ?"
    answer: "Oui, compatible Windows 10/11 (64-bit), macOS 10.15+ (Intel/Apple Silicon), et Linux (Debian/Ubuntu)."
  - question: "Puis-je avoir plusieurs sites en parallèle ?"
    answer: "Oui, autant que tu veux. Consommation ~200-300 Mo par site. La limite est la RAM de ton PC."
  - question: "Comment migrer de LocalWP vers un hébergeur ?"
    answer: "Utilise All-in-One WP Migration : export depuis LocalWP → fichier .wpress → import sur l'hébergement."
---

Introduction
---

T’es encore en train de développer direct en prod comme un cowboy ? Genre tu testes ton nouveau plugin sur ton site live avec 10 000 visiteurs/jour ?

Spoiler : un jour, tu vas tout péter. Et tu vas pleurer.

**LocalWP**, c’est la solution pour arrêter de jouer à la roulette russe avec ton WordPress. Un environnement local complet en 5 minutes, sans se prendre la tête avec Apache, MySQL, et tous ces trucs chiants que personne ne veut configurer manuellement.

Dans ce guide, je te montre comment installer LocalWP, créer ton lab perso, et surtout : **comment migrer proprement vers la prod sans tout péter**.

---

### 🎯 Ce que tu vas apprendre :

✅ Installer LocalWP en 5 min chrono  
✅ Créer autant de sites WordPress que tu veux (tests à volonté)  
✅ Migrer vers la prod gratuitement (All-in-One WP Migration inside)  
✅ Troubleshooting : les 5 galères les plus courantes (et comment les buter)  
✅ Optimiser ton workflow dev/prod (parce que le temps c’est de l’argent)

💡 **Besoin d’un hébergement fiable pour ta migration ?**  
[O2Switch](https://www.o2switch.fr/) – Hébergeur français, support expert, migrations incluses. J’ai migré +20 sites dessus, jamais eu de soucis.

---
## Table des matières


  - [🎯 Ce que tu vas apprendre :](#%F0%9F%8E%AF-ce-que-tu-vas-apprendre)
- [Pourquoi LocalWP plutôt que XAMPP ou MAMP ?](#pourquoi-local-wp-plutot-que-xampp-ou-mamp)
  - [Le match LocalWP VS les dinosaures](#le-match-local-wp-vs-les-dinosaures)
  - [Pour qui c’est fait ?](#pour-qui-cest-fait)
- [Installation de LocalWP (vraiment 5 minutes)](#installation-de-local-wp-vraiment-5-minutes)
  - [Étape 1 : Téléchargement](#etape-1-telechargement)
  - [Étape 2 : Installation](#etape-2-installation)
  - [Étape 3 : Premier lancement](#etape-3-premier-lancement)
- [Créer ton premier site WordPress local](#creer-ton-premier-site-word-press-local)
  - [Interface LocalWP : simple comme bonjour](#interface-local-wp-simple-comme-bonjour)
  - [Accéder à ton site](#acceder-a-ton-site)
- [Mon workflow dev → prod (testé sur +50 sites)](#mon-workflow-dev-%E2%86%92-prod-teste-sur-50-sites)
  - [Phase 1 : Développement local (sans stress)](#phase-1-developpement-local-sans-stress)
  - [Phase 2 : Tests de migration (critique)](#phase-2-tests-de-migration-critique)
  - [Phase 3 : Déploiement production](#phase-3-deploiement-production)
- [Gérer tes sites avec LocalWP](#gerer-tes-sites-avec-local-wp)
  - [Outils intégrés (qui changent la vie)](#outils-integres-qui-changent-la-vie)
  - [Commandes utiles dans Site Shell](#commandes-utiles-dans-site-shell)
  - [Snapshots : ta machine à remonter le temps](#snapshots-ta-machine-a-remonter-le-temps)
- [Les 5 galères LocalWP (et comment les buter)](#les-5-galeres-local-wp-et-comment-les-buter)
  - [🔴 Problème 1 : « Site Cannot Be Reached »](#%F0%9F%94%B4-probleme-1-site-cannot-be-reached)
  - [🔴 Problème 2 : Import All-in-One WP Migration qui plante](#%F0%9F%94%B4-probleme-2-import-all-in-one-wp-migration-qui-plante)
  - [🔴 Problème 3 : Performance de merde](#%F0%9F%94%B4-probleme-3-performance-de-merde)
  - [🔴 Problème 4 : Certificat SSL refusé](#%F0%9F%94%B4-probleme-4-certificat-ssl-refuse)
  - [🔴 Problème 5 : Base de données corrompue](#%F0%9F%94%B4-probleme-5-base-de-donnees-corrompue)
- [LocalWP VS Docker : qui gagne ?](#local-wp-vs-docker-qui-gagne)
  - [LocalWP : le couteau suisse WordPress](#local-wp-le-couteau-suisse-word-press)
  - [Docker : le tank personnalisable](#docker-le-tank-personnalisable)
  - [Mon verdict](#mon-verdict)
- [Optimisations avancées](#optimisations-avancees)
  - [Activer Xdebug (pour les devs)](#activer-xdebug-pour-les-devs)
  - [MailHog : tester les emails en local](#mail-hog-tester-les-emails-en-local)
  - [Configuration Nginx custom](#configuration-nginx-custom)
  - [Connecter LocalWP à un repo Git](#connecter-local-wp-a-un-repo-git)
- [FAQ : Questions fréquentes](#faq-questions-frequentes)
  - [LocalWP est-il gratuit ?](#local-wp-est-il-gratuit)
  - [LocalWP fonctionne-t-il sur Windows/Mac/Linux ?](#local-wp-fonctionne-t-il-sur-windows-mac-linux)
  - [Puis-je avoir plusieurs sites en parallèle ?](#puis-je-avoir-plusieurs-sites-en-parallele)
  - [Comment migrer de LocalWP vers un hébergeur ?](#comment-migrer-de-local-wp-vers-un-hebergeur)
  - [LocalWP VS Docker, lequel choisir ?](#local-wp-vs-docker-lequel-choisir)
  - [Puis-je utiliser LocalWP pour des sites clients ?](#puis-je-utiliser-local-wp-pour-des-sites-clients)
  - [Les performances LocalWP sont-elles bonnes ?](#les-performances-local-wp-sont-elles-bonnes)
- [Conclusion : LocalWP, c’est le début du voyage](#conclusion-local-wp-cest-le-debut-du-voyage)
  - [🚀 Aller plus loin](#%F0%9F%9A%80-aller-plus-loin)
  - [🎓 Formation à venir](#%F0%9F%8E%93-formation-a-venir)


Pourquoi LocalWP plutôt que XAMPP ou MAMP ?
---

### Le match LocalWP VS les dinosaures

**XAMPP/MAMP**, c’était cool… en 2010. Configuration manuelle, interfaces moches des années 2000, galères de certificats SSL, conflits de ports… Bref, la lose.

**LocalWP**, c’est le monde moderne :

✅ **5 minutes d’install** (versus 1h de galère avec XAMPP)  
✅ **SSL natif** – teste en HTTPS direct, pas de certificat à bidouiller  
✅ **Interface moderne** – enfin une UI qui date pas de l’époque MSN Messenger  
✅ **Plusieurs sites en parallèle** – crée 50 sites si ça te chante  
✅ **Snapshots intégrés** – retour arrière en un clic  
✅ **Migration en un clic** – export/import sans transpirer

XAMPP, c’était bien. Mais là, franchement, passe à autre chose.

### Pour qui c’est fait ?

- **Développeurs WordPress** (évident)
- **Designers** qui veulent tester des thèmes
- **Étudiants** en apprentissage
- **Freelances** qui gèrent plusieurs clients
- **Sysadmins** qui veulent un lab WordPress rapide

Même si t’es débutant, LocalWP simplifie tellement le process que tu seras opérationnel en 10 minutes. Promis.

---

Installation de LocalWP (vraiment 5 minutes)
---

### Étape 1 : Téléchargement

Rends-toi sur **[localwp.com](https://localwp.com/)** et télécharge la version pour ton OS :

- Windows (64-bit uniquement)
- macOS (Intel ou M1/M2/M3)
- Linux (Debian/Ubuntu)

**Taille du fichier** : ~200 Mo (ça va, c’est raisonnable)

### Étape 2 : Installation

**macOS** :

```bash
# Ouvre le .dmg téléchargé
# Glisse LocalWP dans Applications
# Lance et autorise l'app (Sécurité → Autoriser)

```

# Double-clic sur le .exe
# Suis l'assistant (Next, Next, Install)
# Lance LocalWP


**Linux** (Debian/Ubuntu) :

```bash
# Installe les dépendances
sudo apt update
sudo apt install libgtk-3-0 libnotify4 libnss3 libxss1 libxtst6 xdg-utils libatspi2.0-0 libappindicator3-1 libsecret-1-0

# Installe LocalWP
sudo dpkg -i local-*.deb

# Si erreurs de dépendances
sudo apt --fix-broken install

```

LocalWP → Installe tes plugins
       → Teste ton thème
       → Importe du contenu de demo
       → Pète tout si tu veux, personne ne voit


**Avantage** : Tu peux faire n’importe quoi. Conflit de plugins ? Tu restart. CSS cassé ? Tu rollback. Base de données explosée ? Tu repars d’un snapshot.

C’est ton bac à sable. Amuse-toi.

### Phase 2 : Tests de migration (critique)

**Avant de migrer direct en prod** (et potentiellement tout péter), teste plutôt ton truc sur un environnement de staging.

Utilise la [migration WordPress avec All-in-One WP Migration](https://brandonvisca.com/migration-wordpress-all-in-one-guide-2025/) pour :

1. Exporter ton site local
2. Importer sur un second site LocalWP (simulation de prod)
3. Vérifier que tout fonctionne (liens, images, BDD)

**💡 Astuce de pro** : Crée un site LocalWP « staging » avec le même environnement que ta prod (même version PHP, même config Nginx). Tu éviteras les mauvaises surprises.

### Phase 3 : Déploiement production

Une fois que tout est validé en staging :

```bash
1. Export avec All-in-One WP Migration (fichier .wpress)
2. Envoi vers l'hébergement final
3. Import sur le site de prod
4. Vérifications finales (cache, permaliens, SSL)
5. Mise en ligne ✅

```

# Lister les plugins installés
wp plugin list

# Activer/désactiver un plugin
wp plugin activate mon-plugin
wp plugin deactivate mon-plugin

# Mettre à jour WordPress
wp core update

# Importer du contenu de démo
wp plugin install wordpress-importer --activate
wp import contenu.xml --authors=create

# Réinitialiser la BDD (attention, destructif !)
wp db reset --yes


**Bon à savoir** : LocalWP inclut WP-CLI nativement. Parfait pour automatiser tes tâches.

### Snapshots : ta machine à remonter le temps

**Avant toute manip risquée**, crée un snapshot :

1. Sélectionne ton site dans LocalWP
2. Onglet **Tools** → **Snapshots**
3. **Create snapshot** → Donne un nom explicite (« avant-modif-theme »)
4. Attends 10-30 secondes

Si tu pètes tout, tu rollback en 2 clics. Magique.

---

Les 5 galères LocalWP (et comment les buter)
---

### 🔴 Problème 1 : « Site Cannot Be Reached »

**Symptômes** : Impossible d’accéder au site local, erreur de connexion.

**Causes** :

- Ports 80/443 déjà utilisés par un autre service
- Pare-feu/antivirus qui bloque
- Service LocalWP planté

**Solutions** :

```bash
# Vérifier les ports utilisés (macOS/Linux)
sudo lsof -i :80
sudo lsof -i :443

# Killer un processus qui bloque
sudo kill -9 PID

# Redémarrer LocalWP
# Préférences → Advanced → Reset Site Router

```

# Éditer le php.ini de LocalWP
# Site → Tools → PHP → Open php.ini

# Modifier ces valeurs
upload_max_filesize = 512M
post_max_size = 512M
max_execution_time = 300
memory_limit = 512M

# Redémarrer le site dans LocalWP


Si ça bloque toujours, utilise la [migration WordPress manuelle](https://brandonvisca.com/migration-wordpress-all-in-one-guide-2025/) (FTP + SQL).

### 🔴 Problème 3 : Performance de merde

**Symptômes** : Site local lent comme la mort, 10 secondes pour charger une page.

**Solutions** :

✅ **Vire les images lourdes** en dev (remplace par des placeholders)  
✅ **Désactive les plugins inutiles** (builder lourd, cache, etc.)  
✅ **Active le mode « Fast CGI »** dans LocalWP (Tools → PHP)  
✅ **Augmente la RAM allouée** (Préférences → Advanced → Memory Limit)

**Astuce** : Exclue le dossier LocalWP de ton antivirus. Gain de perfs massif.

### 🔴 Problème 4 : Certificat SSL refusé

**Symptômes** : Chrome te bloque avec « Votre connexion n’est pas privée ».

**Solution** :

1. Dans LocalWP : **SSL → Trust**
2. Redémarre Chrome/Firefox
3. Si ça bloque encore : ajoute l’exception manuellement

**macOS** : LocalWP ajoute automatiquement le certificat au Trousseau. Si ça marche pas, va dans Trousseau d’accès → Certificats → LocalWP → Toujours approuver.

### 🔴 Problème 5 : Base de données corrompue

**Symptômes** : « Error establishing database connection », site mort.

**Cause** : Arrêt brutal de LocalWP, crash, corruption de table MySQL.

**Solutions** :

1. **En local** : Rollback vers un snapshot (plus rapide)
2. **Si pas de snapshot** : Répare via Adminer

```bash
-- Ouvrir Database → Adminer
-- Sélectionner toutes les tables
-- Action → Réparer les tables

```

# Dans LocalWP : Site → Tools → PHP
# Cocher "Enable Xdebug"
# Redémarrer le site

# Vérifier dans phpinfo
http://mon-site-test.local/wp-admin/admin.php?page=health-check


### MailHog : tester les emails en local

LocalWP intègre **MailHog** nativement. Tous les emails envoyés par WordPress sont interceptés.

**Accès** : `http://mon-site-test.local:8025`

Parfait pour tester les notifications, confirmations d’inscription, etc. sans spammer de vrais comptes.

### Configuration Nginx custom

```bash
# Éditer la config Nginx
Site → Tools → Nginx → Open nginx.conf

# Exemple : ajouter une règle de cache
location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}

# Redémarrer Nginx
Site → Stop → Start

```

# Ouvrir le Site Shell
cd app/public/wp-content/themes/mon-theme

# Initialiser Git
git init
git add .
git commit -m "Initial commit"

# Connecter au remote
git remote add origin https://github.com/user/mon-theme.git
git push -u origin main


**Workflow recommandé** :

- LocalWP pour le dev
- Git pour la gestion de version
- Déploiement automatisé vers prod (via GitHub Actions ou Deployer)

---

FAQ : Questions fréquentes
---

### LocalWP est-il gratuit ?

**Oui**, totalement gratuit. Pas de version premium obligatoire, pas de limitations débiles.

Ils monétisent via les intégrations avec des hébergeurs (WP Engine, Flywheel). Mais l’outil lui-même : 100% gratuit.

### LocalWP fonctionne-t-il sur Windows/Mac/Linux ?

**Oui**, compatible avec les 3 OS majeurs :

- Windows 10/11 (64-bit uniquement)
- macOS 10.15+ (Intel et Apple Silicon)
- Linux (Debian/Ubuntu principalement)

### Puis-je avoir plusieurs sites en parallèle ?

**Oui**, autant que tu veux. J’ai personnellement 15 sites actifs sur mon LocalWP. Aucun problème de performance.

**Limite** : La RAM de ton PC. Chaque site consomme ~200-300 Mo.

### Comment migrer de LocalWP vers un hébergeur ?

Utilise **All-in-One WP Migration** (intégré dans tout WordPress) :

1. Export depuis LocalWP → Fichier .wpress
2. Envoi sur l’hébergement
3. Import via le plugin

Check mon [guide complet sur la migration WordPress](https://brandonvisca.com/migration-wordpress-all-in-one-guide-2025/) pour tous les détails.

### LocalWP VS Docker, lequel choisir ?

**LocalWP** : Simple, rapide, parfait pour WordPress uniquement.  
**Docker** : Flexible, puissant, mais nécessite des connaissances système.

Si tu débutes ou que tu fais juste du WordPress, choisis LocalWP. Si tu veux apprendre Docker et auto-héberger d’autres services, va sur Docker.

### Puis-je utiliser LocalWP pour des sites clients ?

**Oui**, absolument. C’est même recommandé :

- Développement local sans risque
- Tests clients sur ton environnement
- Migration vers leur hébergement quand validé

Beaucoup de freelances/agences utilisent LocalWP en production quotidienne.

### Les performances LocalWP sont-elles bonnes ?

**Oui**, tant que tu as une config PC décente :

- 8 Go RAM minimum (16 Go recommandé)
- SSD obligatoire (sinon c’est la galère)
- Processeur moderne (i5/Ryzen 5 ou mieux)

Avec ça, tu tournes fluide même avec 5-10 sites actifs.

---

Conclusion : LocalWP, c’est le début du voyage
---

LocalWP, c’est **l’outil parfait** pour arrêter de développer en mode cowboy et adopter un workflow propre :

✅ **5 minutes d’install** (versus 1h avec XAMPP)  
✅ **Environnement complet** (Nginx, MySQL, PHP, SSL, MailHog…)  
✅ **Migration simplifiée** vers la production  
✅ **Gratuit et open-source** (pas d’arnaque cachée)

**Les points à retenir** :

1. Teste TOUJOURS en local avant de toucher à la prod
2. Utilise les snapshots avant toute manip risquée
3. Configure All-in-One WP Migration pour des migrations propres
4. Active Xdebug si tu es dev
5. Sécurise ta prod après migration (guide sécurité Linux)

### 🚀 Aller plus loin

LocalWP, c’est le début. Si tu veux vraiment reprendre le contrôle de ton infrastructure et arrêter de dépendre d’hébergeurs qui te facturent un rein, jette un œil à mon [guide complet sur l’auto-hébergement](https://brandonvisca.com/auto-hebergement-guide-complet-2025/).

C’est la prochaine étape logique : dev local avec LocalWP → déploiement sur ton propre serveur → économies massives + indépendance totale.

### 🎓 Formation à venir

Je prépare une formation **« Homelab Weekend »** pour apprendre à gérer toute ton infra (WordPress, Nextcloud, Jellyfin, monitoring, sauvegardes…) en un week-end.

📧 **Rejoins la liste d’attente** pour être prévenu du lancement (+ bonus offert aux early birds)

<noscript> Remarque : JavaScript est requis pour ce contenu.</noscript>  <script>var formDisplay=1;var nfForms=nfForms||[];var form=[];form.id='3_1';form.settings={"objectType":"Form Setting","editActive":"1","title":"Newsletter Subscription","created_at":"2025-04-28 22:34:49","form_title":"Newsletter Subscription","default_label_pos":"above","show_title":"0","clear_complete":"1","hide_complete":"1","logged_in":"0","seq_num":"","wrapper_class":"","element_class":"","form_title_heading_level":"3","key":"","add_submit":"0","changeEmailErrorMsg":"Veuillez saisir une adresse de messagerie valide. Ex\u00a0: jean.dupont@gmail.com","changeDateErrorMsg":"Veuillez saisir une date valide\u00a0!","confirmFieldErrorMsg":"Ces champs doivent correspondre\u00a0!","fieldNumberNumMinError":"Erreur de nombre min.","fieldNumberNumMaxError":"Erreur de nombre max.","fieldNumberIncrementBy":"Veuillez incr\u00e9menter par ","formErrorsCorrectErrors":"Veuillez corriger les erreurs avant d\u2019envoyer ce formulaire.","validateRequiredField":"Ce champ est obligatoire.","honeypotHoneypotError":"Erreur Honeypot","fieldsMarkedRequired":"Les champs marqu\u00e9s d\u2019un <span class=&quot;ninja-forms-req-symbol&quot;>*<\/span> sont obligatoires","currency":"","unique_field_error":"A form with this value has already been submitted.","not_logged_in_msg":"","sub_limit_msg":"The form has reached its submission limit.","calculations":[],"formContentData":["email_1742537865771","hcaptcha_1764087246501","envoyer_1760894781061"],"objectDomain":"display","drawerDisabled":"","allow_public_link":0,"embed_form":"","ninjaForms":"Ninja Forms","fieldTextareaRTEInsertLink":"Ins\u00e9rer un lien","fieldTextareaRTEInsertMedia":"Ins\u00e9rer un m\u00e9dia","fieldTextareaRTESelectAFile":"S\u00e9lectionnez un fichier","formHoneypot":"Si vous \u00eates un \u00eatre humain et que vous voyez ce champ, veuillez le laisser vide.","fileUploadOldCodeFileUploadInProgress":"T\u00e9l\u00e9versement du fichier en cours.","fileUploadOldCodeFileUpload":"T\u00c9L\u00c9VERSEMENT DE FICHIER","currencySymbol":"&euro;","thousands_sep":"\u00a0","decimal_point":",","siteLocale":"fr_FR","dateFormat":"d\/m\/Y","startOfWeek":"1","of":"sur","previousMonth":"Mois pr\u00e9c\u00e9dent","nextMonth":"Mois suivant","months":["Janvier","F\u00e9vrier","Mars","Avril","Mai","Juin","Juillet","Ao\u00fbt","Septembre","Octobre","Novembre","D\u00e9cembre"],"monthsShort":["Jan","F\u00e9v","Mar","Avr","Mai","Juin","Juil","Ao\u00fb","Sep","Oct","Nov","D\u00e9c"],"weekdays":["Dimanche","Lundi","Mardi","Mercredi","Jeudi","Vendredi","Samedi"],"weekdaysShort":["Dim","Lun","Mar","Mer","Jeu","Ven","Sam"],"weekdaysMin":["Di","Lu","Ma","Me","Je","Ve","Sa"],"recaptchaConsentMissing":"reCaptcha validation couldn't load.","recaptchaMissingCookie":"reCaptcha v3 validation couldn't load the cookie needed to submit the form.","recaptchaConsentEvent":"Accept reCaptcha cookies before sending the form.","currency_symbol":"","beforeForm":"","beforeFields":"","afterFields":"","afterForm":""};form.fields=[{"objectType":"Field","objectDomain":"fields","editActive":false,"order":1,"idAttribute":"id","type":"email","label":"","key":"email_1742537865771","label_pos":"above","required":1,"default":"","placeholder":"Ton email","container_class":"","element_class":"","admin_label":"","help_text":"","custom_name_attribute":"email","personally_identifiable":1,"value":"","drawerDisabled":false,"field_label":"","field_key":"email_1742537865771","id":"7_1","beforeField":"","afterField":"","parentType":"email","element_templates":["email","input"],"old_classname":"","wrap_template":"wrap"},{"objectType":"Field","objectDomain":"fields","editActive":false,"order":3,"idAttribute":"id","label":"","type":"hcaptcha","container_class":"","element_class":"","label_visibility":"invisible","size":"compact","theme":"dark","key":"hcaptcha_1764087246501","drawerDisabled":false,"id":"21_1","beforeField":"","afterField":"","value":"","label_pos":"above","parentType":"textbox","element_templates":["hcaptcha","input"],"old_classname":"","wrap_template":"wrap","site_key":"7b920900-edae-4336-a252-e6dcbfc82b20"},{"objectType":"Field","objectDomain":"fields","editActive":false,"order":4,"idAttribute":"id","type":"submit","label":"Envoyer","processing_label":"En cours de traitement","container_class":"","element_class":"","key":"envoyer_1760894781061","admin_label":"","drawerDisabled":false,"field_label":"Subscribe","field_key":"subscribe_1742537911109","id":"8_1","beforeField":"","afterField":"","value":"","label_pos":"above","parentType":"textbox","element_templates":["submit","button","input"],"old_classname":"","wrap_template":"wrap-no-label"}];nfForms.push(form);</script>- - - - - -

**💡 Ressources utiles :**

- [Site officiel LocalWP](https://localwp.com/)
- [Documentation LocalWP](https://localwp.com/help-docs/)
- [Forum support communautaire](https://localwp.com/community/)

**🔗 Articles complémentaires :**

- [Migration WordPress : guide complet All-in-One WP Migration](https://brandonvisca.com/migration-wordpress-all-in-one-guide-2025/)
- [Sécuriser son serveur Linux : le guide ultime](https://brandonvisca.com/securite-de-votre-serveur-linux/)
- [Docker pour débutants : 10 services à auto-héberger](https://brandonvisca.com/docker-debutant-services-auto-heberger/)
- [Configuration Nginx : blocs location et sécurité](https://brandonvisca.com/nginx-location-bloc-et-securite/)

---

*Article mis à jour en novembre 2025 – Testé sur LocalWP 8.0+ / WordPress 6.7+*
