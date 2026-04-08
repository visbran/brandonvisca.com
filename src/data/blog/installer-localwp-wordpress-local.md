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
# LocalWP : Ton lab WordPress en 5 min (guide complet 2025 + migration prod)

**⏱️ Temps de lecture : 8 minutes**

---

## Introduction

T'es encore en train de développer direct en prod comme un cowboy ? Genre tu testes ton nouveau plugin sur ton site live avec 10 000 visiteurs/jour ?

Spoiler : un jour, tu vas tout péter. Et tu vas pleurer.

**LocalWP**, c'est la solution pour arrêter de jouer à la roulette russe avec ton WordPress. Un environnement local complet en 5 minutes, sans se prendre la tête avec Apache, MySQL, et tous ces trucs chiants que personne ne veut configurer manuellement.

Dans ce guide, je te montre comment installer LocalWP, créer ton lab perso, et surtout : **comment migrer proprement vers la prod sans tout péter**.

## Table of content

### 🎯 Ce que tu vas apprendre :

✅ Installer LocalWP en 5 min chrono  
✅ Créer autant de sites WordPress que tu veux (tests à volonté)  
✅ Migrer vers la prod gratuitement (All-in-One WP Migration inside)  
✅ Troubleshooting : les 5 galères les plus courantes (et comment les buter)  
✅ Optimiser ton workflow dev/prod (parce que le temps c'est de l'argent)

💡 **Besoin d'un hébergement fiable pour ta migration ?**  
[O2Switch](https://www.o2switch.fr/) - Hébergeur français, support expert, migrations incluses. J'ai migré +20 sites dessus, jamais eu de soucis.

---

## Pourquoi LocalWP plutôt que XAMPP ou MAMP ?

### Le match LocalWP VS les dinosaures

**XAMPP/MAMP**, c'était cool... en 2010. Configuration manuelle, interfaces moches des années 2000, galères de certificats SSL, conflits de ports... Bref, la lose.

**LocalWP**, c'est le monde moderne :

✅ **5 minutes d'install** (versus 1h de galère avec XAMPP)  
✅ **SSL natif** - teste en HTTPS direct, pas de certificat à bidouiller  
✅ **Interface moderne** - enfin une UI qui date pas de l'époque MSN Messenger  
✅ **Plusieurs sites en parallèle** - crée 50 sites si ça te chante  
✅ **Snapshots intégrés** - retour arrière en un clic  
✅ **Migration en un clic** - export/import sans transpirer

XAMPP, c'était bien. Mais là, franchement, passe à autre chose.

### Pour qui c'est fait ?

- **Développeurs WordPress** (évident)
- **Designers** qui veulent tester des thèmes
- **Étudiants** en apprentissage
- **Freelances** qui gèrent plusieurs clients
- **Sysadmins** qui veulent un lab WordPress rapide

Même si t'es débutant, LocalWP simplifie tellement le process que tu seras opérationnel en 10 minutes. Promis.

---

## Installation de LocalWP (vraiment 5 minutes)

### Étape 1 : Téléchargement

Rends-toi sur **[localwp.com](https://localwp.com/)** et télécharge la version pour ton OS :

- Windows (64-bit uniquement)
- macOS (Intel ou M1/M2/M3)
- Linux (Debian/Ubuntu)

**Taille du fichier** : ~200 Mo (ça va, c'est raisonnable)

### Étape 2 : Installation

**macOS** :

```bash
# Ouvre le .dmg téléchargé
# Glisse LocalWP dans Applications
# Lance et autorise l'app (Sécurité → Autoriser)
```

**Windows** :

```bash
# Double-clic sur le .exe
# Suis l'assistant (Next, Next, Install)
# Lance LocalWP
```

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

### Étape 3 : Premier lancement

Au premier démarrage, LocalWP va :

1. Configurer son environnement interne
2. Installer les dépendances nécessaires
3. Créer les dossiers de travail

**Temps d'attente** : 30 secondes à 2 minutes selon ton PC.

---

## Créer ton premier site WordPress local

### Interface LocalWP : simple comme bonjour

Clique sur le gros bouton **"+ Create a new site"** (difficile de le rater).

**Choix 1 : Créer un nouveau site**

1. **Nom du site** : `mon-site-test` (évite les espaces et accents)
    
2. **Environnement** :
    
    - **Preferred** (recommandé) : Nginx + PHP 8.1 + MySQL 8.0
    - **Custom** : si t'as des besoins spécifiques (vieilles versions PHP, etc.)
3. **Configuration WordPress** :
    
    - **Username** : admin (ou ton pseudo)
    - **Password** : choisis un truc solide (même en local, prends l'habitude)
    - **Email** : ton@email.com
4. **Clique sur "Add Site"** et attends 30 secondes.
    

BOOM. Site créé. C'était dur, hein ?

### Accéder à ton site

Une fois le site créé, tu as 3 boutons magiques :

**🌐 Open site** : Ouvre ton site dans le navigateur  
**⚙️ WP Admin** : Accès direct au dashboard WordPress (sans login !)  
**📁 Open site shell** : Terminal pré-configuré dans le dossier du site

**URL locale** : `http://mon-site-test.local` (LocalWP gère le .local automatiquement)

---

## Mon workflow dev → prod (testé sur +50 sites)

Bon, maintenant que t'as un site local, on va parler du **vrai workflow** qui tient la route.

### Phase 1 : Développement local (sans stress)

```
LocalWP → Installe tes plugins
       → Teste ton thème
       → Importe du contenu de demo
       → Pète tout si tu veux, personne ne voit
```

**Avantage** : Tu peux faire n'importe quoi. Conflit de plugins ? Tu restart. CSS cassé ? Tu rollback. Base de données explosée ? Tu repars d'un snapshot.

C'est ton bac à sable. Amuse-toi.

### Phase 2 : Tests de migration (critique)

**Avant de migrer direct en prod** (et potentiellement tout péter), teste plutôt ton truc sur un environnement de staging.

Utilise la [migration WordPress avec All-in-One WP Migration](https://brandonvisca.com/migration-wordpress-all-in-one-guide-2025/) pour :

1. Exporter ton site local
2. Importer sur un second site LocalWP (simulation de prod)
3. Vérifier que tout fonctionne (liens, images, BDD)

**💡 Astuce de pro** : Crée un site LocalWP "staging" avec le même environnement que ta prod (même version PHP, même config Nginx). Tu éviteras les mauvaises surprises.

### Phase 3 : Déploiement production

Une fois que tout est validé en staging :

```bash
1. Export avec All-in-One WP Migration (fichier .wpress)
2. Envoi vers l'hébergement final
3. Import sur le site de prod
4. Vérifications finales (cache, permaliens, SSL)
5. Mise en ligne ✅
```

**Temps économisé** : ~2h par site  
**Risque de tout péter** : -95%

Une fois ton site migré en prod, ne néglige JAMAIS la sécurité. Consulte mon guide pour [sécuriser ton serveur Linux](https://brandonvisca.com/securite-de-votre-serveur-linux/) et éviter de te faire défoncer en 24h.

---

## Gérer tes sites avec LocalWP

### Outils intégrés (qui changent la vie)

**Database Manager** : Accès direct à Adminer (interface web MySQL)  
**Site Shell** : Terminal configuré dans le bon répertoire  
**Log Viewer** : Logs PHP/Nginx en direct (pratique pour debugger)  
**SSL Certificate** : Activé par défaut (test HTTPS natif)

### Commandes utiles dans Site Shell

```bash
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
```

**Bon à savoir** : LocalWP inclut WP-CLI nativement. Parfait pour automatiser tes tâches.

### Snapshots : ta machine à remonter le temps

**Avant toute manip risquée**, crée un snapshot :

1. Sélectionne ton site dans LocalWP
2. Onglet **Tools** → **Snapshots**
3. **Create snapshot** → Donne un nom explicite ("avant-modif-theme")
4. Attends 10-30 secondes

Si tu pètes tout, tu rollback en 2 clics. Magique.

---

## Les 5 galères LocalWP (et comment les buter)

### 🔴 Problème 1 : "Site Cannot Be Reached"

**Symptômes** : Impossible d'accéder au site local, erreur de connexion.

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

**Windows** : Vérifie que Skype ou autre soft ne squatte pas le port 80/443.

### 🔴 Problème 2 : Import All-in-One WP Migration qui plante

**Symptômes** : Import bloqué à 50%, timeout, erreur 500.

**Cause** : Limites PHP trop basses (mémoire, taille upload).

**Solution** :

```bash
# Éditer le php.ini de LocalWP
# Site → Tools → PHP → Open php.ini

# Modifier ces valeurs
upload_max_filesize = 512M
post_max_size = 512M
max_execution_time = 300
memory_limit = 512M

# Redémarrer le site dans LocalWP
```

Si ça bloque toujours, utilise la [migration WordPress manuelle](https://brandonvisca.com/migration-wordpress-all-in-one-guide-2025/) (FTP + SQL).

### 🔴 Problème 3 : Performance de merde

**Symptômes** : Site local lent comme la mort, 10 secondes pour charger une page.

**Solutions** :

✅ **Vire les images lourdes** en dev (remplace par des placeholders)  
✅ **Désactive les plugins inutiles** (builder lourd, cache, etc.)  
✅ **Active le mode "Fast CGI"** dans LocalWP (Tools → PHP)  
✅ **Augmente la RAM allouée** (Préférences → Advanced → Memory Limit)

**Astuce** : Exclue le dossier LocalWP de ton antivirus. Gain de perfs massif.

### 🔴 Problème 4 : Certificat SSL refusé

**Symptômes** : Chrome te bloque avec "Votre connexion n'est pas privée".

**Solution** :

1. Dans LocalWP : **SSL → Trust**
2. Redémarre Chrome/Firefox
3. Si ça bloque encore : ajoute l'exception manuellement

**macOS** : LocalWP ajoute automatiquement le certificat au Trousseau. Si ça marche pas, va dans Trousseau d'accès → Certificats → LocalWP → Toujours approuver.

### 🔴 Problème 5 : Base de données corrompue

**Symptômes** : "Error establishing database connection", site mort.

**Cause** : Arrêt brutal de LocalWP, crash, corruption de table MySQL.

**Solutions** :

1. **En local** : Rollback vers un snapshot (plus rapide)
2. **Si pas de snapshot** : Répare via Adminer

```sql
-- Ouvrir Database → Adminer
-- Sélectionner toutes les tables
-- Action → Réparer les tables
```

3. **Si vraiment mort** : Consulte mon guide complet pour [réparer une base de données WordPress corrompue](https://brandonvisca.com/wordpress-2-solutions-pour-reparer-une-base-de-donnee-corrompu/).

Mais franchement, en local, le plus simple : repars d'un snapshot. C'est pour ça qu'on en fait.

---

## LocalWP VS Docker : qui gagne ?

J'entends déjà les puristes Docker gueuler. Alors on va clarifier.

### LocalWP : le couteau suisse WordPress

**Points forts** : ✅ Installation en 5 min (versus 1h pour Docker)  
✅ Interface graphique (pas besoin de CLI)  
✅ SSL natif sans config  
✅ Parfait pour les non-sysadmins

**Points faibles** : ❌ Limité à WordPress  
❌ Moins flexible qu'une stack Docker custom  
❌ Pas de portabilité multi-environnements

### Docker : le tank personnalisable

**Points forts** : ✅ Contrôle total de la stack  
✅ Portabilité (même config en dev/staging/prod)  
✅ Multi-services (pas que WordPress)

**Points faibles** : ❌ Courbe d'apprentissage (docker-compose, Dockerfile...)  
❌ Plus long à configurer  
❌ Nécessite des connaissances système

### Mon verdict

**LocalWP** si :

- Tu veux du simple et rapide
- Tu fais QUE du WordPress
- Tu veux pas te prendre la tête

**Docker** si :

- Tu veux apprendre à gérer toute ton infra
- Tu as besoin de reproduire l'environnement prod à l'identique
- Tu veux héberger d'autres services en parallèle

💡 **Envie d'aller plus loin ?** Si Docker te branche et que tu veux auto-héberger tes propres services (Nextcloud, Jellyfin, etc.), check mon guide complet sur [Docker pour l'auto-hébergement](https://brandonvisca.com/docker-debutant-services-auto-heberger/).

---

## Optimisations avancées

### Activer Xdebug (pour les devs)

```bash
# Dans LocalWP : Site → Tools → PHP
# Cocher "Enable Xdebug"
# Redémarrer le site

# Vérifier dans phpinfo
http://mon-site-test.local/wp-admin/admin.php?page=health-check
```

### MailHog : tester les emails en local

LocalWP intègre **MailHog** nativement. Tous les emails envoyés par WordPress sont interceptés.

**Accès** : `http://mon-site-test.local:8025`

Parfait pour tester les notifications, confirmations d'inscription, etc. sans spammer de vrais comptes.

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

Pour des perfs au top en prod, configure correctement ton serveur. Mon guide sur la [configuration des blocs location Nginx](https://brandonvisca.com/nginx-location-bloc-et-securite/) va te faire gagner des précieuses millisecondes.

### Connecter LocalWP à un repo Git

```bash
# Ouvrir le Site Shell
cd app/public/wp-content/themes/mon-theme

# Initialiser Git
git init
git add .
git commit -m "Initial commit"

# Connecter au remote
git remote add origin https://github.com/user/mon-theme.git
git push -u origin main
```

**Workflow recommandé** :

- LocalWP pour le dev
- Git pour la gestion de version
- Déploiement automatisé vers prod (via GitHub Actions ou Deployer)

---

## FAQ : Questions fréquentes

### LocalWP est-il gratuit ?

**Oui**, totalement gratuit. Pas de version premium obligatoire, pas de limitations débiles.

Ils monétisent via les intégrations avec des hébergeurs (WP Engine, Flywheel). Mais l'outil lui-même : 100% gratuit.

### LocalWP fonctionne-t-il sur Windows/Mac/Linux ?

**Oui**, compatible avec les 3 OS majeurs :

- Windows 10/11 (64-bit uniquement)
- macOS 10.15+ (Intel et Apple Silicon)
- Linux (Debian/Ubuntu principalement)

### Puis-je avoir plusieurs sites en parallèle ?

**Oui**, autant que tu veux. J'ai personnellement 15 sites actifs sur mon LocalWP. Aucun problème de performance.

**Limite** : La RAM de ton PC. Chaque site consomme ~200-300 Mo.

### Comment migrer de LocalWP vers un hébergeur ?

Utilise **All-in-One WP Migration** (intégré dans tout WordPress) :

1. Export depuis LocalWP → Fichier .wpress
2. Envoi sur l'hébergement
3. Import via le plugin

Check mon [guide complet sur la migration WordPress](https://brandonvisca.com/migration-wordpress-all-in-one-guide-2025/) pour tous les détails.

### LocalWP VS Docker, lequel choisir ?

**LocalWP** : Simple, rapide, parfait pour WordPress uniquement.  
**Docker** : Flexible, puissant, mais nécessite des connaissances système.

Si tu débutes ou que tu fais juste du WordPress, choisis LocalWP. Si tu veux apprendre Docker et auto-héberger d'autres services, va sur Docker.

### Puis-je utiliser LocalWP pour des sites clients ?

**Oui**, absolument. C'est même recommandé :

- Développement local sans risque
- Tests clients sur ton environnement
- Migration vers leur hébergement quand validé

Beaucoup de freelances/agences utilisent LocalWP en production quotidienne.

### Les performances LocalWP sont-elles bonnes ?

**Oui**, tant que tu as une config PC décente :

- 8 Go RAM minimum (16 Go recommandé)
- SSD obligatoire (sinon c'est la galère)
- Processeur moderne (i5/Ryzen 5 ou mieux)

Avec ça, tu tournes fluide même avec 5-10 sites actifs.

---

## Conclusion : LocalWP, c'est le début du voyage

LocalWP, c'est **l'outil parfait** pour arrêter de développer en mode cowboy et adopter un workflow propre :

✅ **5 minutes d'install** (versus 1h avec XAMPP)  
✅ **Environnement complet** (Nginx, MySQL, PHP, SSL, MailHog...)  
✅ **Migration simplifiée** vers la production  
✅ **Gratuit et open-source** (pas d'arnaque cachée)

**Les points à retenir** :

1. Teste TOUJOURS en local avant de toucher à la prod
2. Utilise les snapshots avant toute manip risquée
3. Configure All-in-One WP Migration pour des migrations propres
4. Active Xdebug si tu es dev
5. Sécurise ta prod après migration (guide sécurité Linux)

### 🚀 Aller plus loin

LocalWP, c'est le début. Si tu veux vraiment reprendre le contrôle de ton infrastructure et arrêter de dépendre d'hébergeurs qui te facturent un rein, jette un œil à mon [guide complet sur l'auto-hébergement](https://brandonvisca.com/auto-hebergement-guide-complet-2025/).

C'est la prochaine étape logique : dev local avec LocalWP → déploiement sur ton propre serveur → économies massives + indépendance totale.

---

**💡 Ressources utiles :**

- [Site officiel LocalWP](https://localwp.com/)
- [Documentation LocalWP](https://localwp.com/help-docs/)
- [Forum support communautaire](https://localwp.com/community/)

**🔗 Articles complémentaires :**

- [Migration WordPress : guide complet All-in-One WP Migration](https://brandonvisca.com/migration-wordpress-all-in-one-guide-2025/)
- [Sécuriser son serveur Linux : le guide ultime](https://brandonvisca.com/securite-de-votre-serveur-linux/)
- [Docker pour débutants : 10 services à auto-héberger](https://brandonvisca.com/docker-debutant-services-auto-heberger/)
- [Configuration Nginx : blocs location et sécurité](https://brandonvisca.com/nginx-location-bloc-et-securite/)

