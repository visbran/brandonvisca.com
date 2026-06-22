---
title: "Actual Budget Docker : gestionnaire de budget open-source auto-hébergé"
description: "Guide actual budget docker complet : déployez Actual Budget, gestionnaire budget open-source auto-hébergé et alternative à YNAB."
pubDatetime: "2026-06-22T08:00:00.000Z"
modDatetime: "2026-06-22T08:00:00.000Z"
author: Brandon Visca
tags:
  - docker
  - auto-hebergement
  - finance
  - debutant
featured: false
draft: false
focusKeyword: actual budget docker
ogImage: ""
---
> 💡 **TL;DR**
> - Actual Budget est un gestionnaire de budget open-source basé sur la méthode des enveloppes, fork spirituel de YNAB 4
> - Tu le déploies en 5 minutes avec Docker Compose, SQLite intégré, zéro base de données externe obligatoire
> - Interface web moderne, apps mobiles iOS/Android, sync bancaire via GoCardless (banques FR compatibles)
> - Alternative 100 % gratuite et auto-hébergée à YNAB (14,99 $/mois) et plus simple que Firefly III
> - Docker Compose complet, tableau comparatif et checklist sécurité inclus ci-dessous

## Table des matières

## Pourquoi un gestionnaire de budget auto-hébergé en 2026 ?

Tu ouvres ton application bancaire. Tu vois un virement de 47,32 € chez Amazon. Tu te demandes ce que t'as acheté. Tu cherches dans tes mails. Rien. Tu as dépensé 47,32 € sans t'en rendre compte. Et c'est le troisième chargeur USB-C cette année.

Le problème des banques en ligne, c'est qu'elles te montrent ce que tu as dépensé, pas ce que tu peux dépenser. Elles te donnent un historique, pas un plan. Tu vois ton solde descendre sans savoir si tu vas finir à découvert le 28 du mois.

Actual Budget résout ce problème avec le **budget par enveloppes** (zero-based budgeting). Chaque euro qui rentre se voit assigner un job précis : loyer, courses, essence, épargne, loisirs. Quand l'enveloppe "loisirs" est vide, c'est fini. Pas de découvert surprise, pas de fin de mois angoissante.

C'est la même philosophie que YNAB (You Need A Budget), le logiciel propriétaire américain à 14,99 $/mois. Sauf qu'Actual Budget est **open-source**, **gratuit**, et **auto-hébergé**. Tes données financières restent chez toi. Et si tu as déjà monté ton homelab avec Docker, l'installation prend cinq minutes.

Dans mon [guide des services essentiels à auto-héberger avec Docker](/docker-debutant-services-auto-heberger/), je recommande de commencer par les outils de productivité. Mais une fois que tu as Vaultwarden, Nextcloud et Homer en place, il manque encore quelque chose : la maîtrise de tes finances. Actual Budget est le chaînon manquant.

## Qu'est-ce que Actual Budget et pourquoi le déployer avec Docker ?

Actual Budget est un logiciel de budgeting personnel développé par James Long et l'équipe Actual Budget. Le projet est open-source sous licence BSD-3-Clause, avec le code source disponible sur GitHub (`actualbudget/actual`). L'image Docker officielle est `actualbudget/actual-server`, maintenue activement avec des releases régulières. Déployer **actual budget docker** sur ton serveur te donne un outil financier complet, chiffré et auto-hébergé en quelques minutes.

Contrairement à un simple tracker de dépenses, Actual Budget implémente la méthode des enveloppes à la lettre :

- **Budget par enveloppes** : tu crées des catégories (loyer, courses, transport, loisirs, épargne) et tu répartis ton revenu mensuel dedans. Quand une enveloppe est vide, tu arrêtes de dépenser dans cette catégorie.
- **Rapprochement bancaire** : importe des fichiers OFX, QFX, QIF, CSV ou connecte-toi via GoCardless pour synchroniser automatiquement les transactions.
- **Règles de catégorisation automatique** : tu définis des règles ("si le libellé contient 'CARREFOUR', catégorie Courses") et Actual Budget classe les transactions tout seul.
- **Gestion des objectifs** : fixe des objectifs mensuels ou annuels par catégorie. Actual Budget calcule automatiquement combien il manque.
- **Transferts entre enveloppes** : si tu dépenses moins en courses ce mois-ci, tu transfères le surplus vers l'épargne. Le total reste constant, seule la répartition change.
- **Support multi-comptes** : compte courant, livret A, PEL, compte joint. Tu vois tout dans une seule interface.
- **Apps mobiles** : applications iOS et Android natives pour saisir une dépense au vol. Le sync se fait via ton serveur auto-hébergé.
- **Rapports et graphiques** : visualisation des dépenses par catégorie, évolution du net worth, cash flow mensuel.
- **Import YNAB4** : si tu étais sur l'ancienne version desktop de YNAB, tu peux importer ton budget complet.
- **Chiffrement de bout en bout** : tes données sont chiffrées côté client avant d'être stockées sur le serveur.

Le serveur est écrit en Node.js et utilise SQLite par défaut (PostgreSQL optionnel pour les setups avancés). L'image Docker fait environ 200 Mo, démarre en quelques secondes, et consomme moins de 100 Mo de RAM au repos.

Si tu cherches à noter tes dépenses rapides ou des idées de budgets avant de les structurer dans Actual Budget, j'ai aussi couvert [Memos avec Docker](/memos-docker-notes-auto-heberge/), un bloc-notes auto-hébergé ultra-léger et minimaliste parfait pour des notes rapides.

## Actual Budget vs YNAB vs Firefly III : tableau comparatif

| Critère | Actual Budget | YNAB | Firefly III |
|---------|---------------|------|-------------|
| **Prix** | Gratuit (open-source) | 14,99 $/mois ou 109 $/an | Gratuit (open-source) |
| **Hébergement** | Auto-hébergé (chez toi) | Cloud obligatoire (US) | Auto-hébergé (chez toi) |
| **Méthode** | Enveloppes (zero-based) | Enveloppes (zero-based) | Comptabilité traditionnelle |
| **Bank sync France** | GoCardless (compatible) | Plaid (non dispo FR) | GoCardless (plugin) |
| **Interface** | Web moderne + apps mobiles | Web + apps mobiles | Web uniquement |
| **Docker officiel** | Oui (`actualbudget/actual-server`) | Non (SaaS uniquement) | Oui (`fireflyiii/core`) |
| **Complexité** | Débutant | Débutant | Intermédiaire/avancé |
| **Chiffrement** | E2E côté client | Cloud (tiers de confiance) | Serveur uniquement |
| **Import bancaire** | OFX, QFX, QIF, CSV, GoCardless | Plaid (US/UK/CA) | CSV, GoCardless (plugin) |
| **License** | BSD-3-Clause | Propriétaire | AGPL-3.0 |
| **Communauté** | GitHub actif, Discord | Grand mais payant | GitHub actif |

Mon verdict pour un homelab francophone : **Actual Budget**. Parce que c'est le seul outil qui combine la méthode des enveloppes (la plus efficace pour ne plus finir à découvert), le sync bancaire français via GoCardless, l'auto-hébergement Docker simple, et le chiffrement E2E. YNAB est excellent mais propriétaire, cloud-only et inaccessible en France pour le bank sync. Firefly III est puissant mais orienté comptabilité avec bilan, actifs et passifs, c'est overkill si tu veux juste budgéter ton argent du mois.

## Prérequis

- Un serveur Linux avec Docker et Docker Compose installés (Docker Engine 24+ recommandé)
- 1 cœur CPU et 512 Mo de RAM minimum (1 Go recommandé pour le confort)
- 2 Go d'espace disque pour l'application et la base SQLite
- Un nom de domaine ou sous-domaine si tu veux HTTPS en frontal
- Un reverse proxy (Caddy, Traefik ou Nginx Proxy Manager) pour gérer les certificats SSL
- Un mot de passe fort pour le chiffrement (garde-le dans ton gestionnaire de mots de passe)

Actual Budget est incroyablement léger. Un Raspberry Pi 4 avec 2 Go de RAM suffit largement pour gérer un budget familial complet avec sync mobile. Pour un usage confortable, un petit VPS de 1 cœur / 1 Go est amplement suffisant.

## Installation avec Docker Compose

Crée un dossier dédié et un fichier `docker-compose.yml` :

```bash
mkdir -p ~/actual-budget && cd ~/actual-budget
```

Voici le Docker Compose complet et prêt à l'emploi :

```yaml
services:
  actual-server:
    image: actualbudget/actual-server:latest
    container_name: actual-budget
    restart: unless-stopped
    ports:
      - "5006:5006"
    volumes:
      - ./data:/data
    environment:
      - ACTUAL_LOGIN_METHOD=password
      - ACTUAL_PORT=5006
      - ACTUAL_SERVER_FILES=/data/server-files
      - ACTUAL_USER_FILES=/data/user-files
```

Lance le conteneur :

```bash
docker compose up -d
```

Vérifie que tout tourne :

```bash
docker compose logs -f
```

Tu dois voir un message indiquant que le serveur écoute sur le port 5006. Si c'est bon, ouvre `http://ton-serveur:5006` dans ton navigateur.

### Avec un reverse proxy Caddy (HTTPS automatique)

Si tu utilises Caddy comme reverse proxy (ce que je recommande), ajoute ceci à ton `Caddyfile` :

```caddyfile
budget.tondomaine.com {
    reverse_proxy localhost:5006
}
```

Relance Caddy :

```bash
docker compose -f /path/to/caddy/docker-compose.yml restart
```

### Avec Traefik (labels Docker)

Si tu utilises Traefik, ajoute ces labels au service dans ton `docker-compose.yml` :

```yaml
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.actual.rule=Host(`budget.tondomaine.com`)"
      - "traefik.http.routers.actual.entrypoints=websecure"
      - "traefik.http.routers.actual.tls.certresolver=letsencrypt"
      - "traefik.http.services.actual.loadbalancer.server.port=5006"
```

## Configuration initiale

### 1. Créer ton premier budget

À la première connexion, Actual Budget te demande de créer un fichier de budget. Choisis un nom ("Budget Perso", "Budget Famille") et un mot de passe de chiffrement. **Ce mot de passe est critique** : sans lui, tes données sont illisibles. Stocke-le dans ton gestionnaire de mots de passe (Vaultwarden si tu l'as déployé).

### 2. Configurer tes comptes

Crée tes comptes bancaires dans l'interface :

- Compte courant
- Livret d'épargne
- PEL ou autres placements

Pour chaque compte, indique le solde actuel. Actual Budget va s'en servir comme point de départ.

### 3. Créer tes catégories (enveloppes)

Voici un exemple de structure pour un budget mensuel :

| Catégorie | Budget mensuel |
|-----------|----------------|
| Loyer / Crédit | 800 € |
| Courses | 400 € |
| Transport (essence, pass) | 150 € |
| Factures (élec, eau, internet, tel) | 200 € |
| Loisirs | 100 € |
| Santé | 50 € |
| Épargne d'urgence | 200 € |
| Vacances | 100 € |
| Divers | 100 € |

Clique sur "Add Category" pour chaque enveloppe et renseigne le montant mensuel. Actual Budget calcule automatiquement si ton total dépasse tes revenus.

### 4. Activer le sync bancaire (optionnel)

Actual Budget supporte GoCardless pour le sync bancaire européen :

1. Crée un compte sur [gocardless.com/bank-account-data](https://gocardless.com/bank-account-data/)
2. Récupère ton `secretId` et `secretKey`
3. Dans Actual Budget, va dans Settings > Global Settings > Bank Sync
4. Colle tes credentials et clique sur "Link Account"

**Banques françaises compatibles** : BNP Paribas, Société Générale, Crédit Mutuel, CIC, Banque Postale, Hello bank!, Boursorama, Fortuneo, Monabanq, ING Direct.

### 5. Configurer les règles de catégorisation

Dans l'onglet "Rules", crée des règles pour classifier automatiquement tes transactions :

- Si le payee contient "CARREFOUR" ou "AUCHAN" ou "LIDL" → Catégorie "Courses"
- Si le payee contient "TOTAL" ou "SHELL" → Catégorie "Transport"
- Si le payee contient "FREE" ou "ORANGE" ou "SFR" → Catégorie "Factures"

Ces règles s'appliquent aux nouvelles transactions importées automatiquement.

### 6. Importer un budget existant

Si tu utilisais YNAB 4, exporte ton budget au format JSON et importe-le via Settings > Import. Pour un import bancaire (OFX, QIF, CSV), va dans l'onglet du compte, clique sur "Import Transactions" et sélectionne ton fichier.

## Sauvegarde de tes données financières

Tes données sont stockées dans le volume `./data` du conteneur. Si le disque lâche, tu perds ton historique financier complet. **Ne néglige pas la sauvegarde.**

J'ai détaillé toute la méthode dans mon guide [Duplicati Docker : sauvegarde chiffrée auto-hébergée](/duplicati-docker-sauvegarde/). Configure un backup quotidien du dossier `~/actual-budget/data` vers ton NAS ou un cloud chiffré. Actual Budget étant en SQLite, le backup est un simple copie de fichiers.

Pour un backup manuel rapide :

```bash
cd ~/actual-budget && tar czf /backup/actual-budget-$(date +%Y%m%d).tar.gz data/
```

## Checklist sécurité

- [ ] **HTTPS obligatoire** : ne jamais exposer Actual Budget en HTTP sur Internet. Utilise Caddy, Traefik ou Nginx Proxy Manager avec Let's Encrypt.
- [ ] **Mot de passe de chiffrement fort** : minimum 16 caractères, stocké dans un gestionnaire de mots de passe. Sans ce mot de passe, tes données sont perdues à jamais.
- [ ] **Firewall** : le port 5006 ne doit être accessible que par le reverse proxy local. Bloque l'accès direct depuis l'extérieur avec UFW ou le firewall de ton hébergeur.
- [ ] **Backups chiffrés** : sauvegarde le dossier `data/` quotidiennement avec Duplicati ou Restic. Chiffre les backups avec AES-256.
- [ ] **Mises à jour régulières** : vérifie les nouvelles versions d'`actualbudget/actual-server` et met à jour via `docker compose pull && docker compose up -d`.
- [ ] **Authentification serveur** : si plusieurs personnes utilisent le serveur, crée des comptes séparés. Chaque utilisateur a son propre fichier de budget chiffré.
- [ ] **GoCardless credentials** : stocke ton `secretId` et `secretKey` dans un gestionnaire de mots de passe, jamais en clair dans un fichier texte.
- [ ] **Logs** : surveille les logs Docker (`docker compose logs -f`) pour détecter les tentatives de connexion anormales.
- [ ] **Snapshot avant update** : fais un backup manuel avant chaque mise à jour majeure du conteneur.

## Dépannage courant

### Le conteneur ne démarre pas

**Symptôme** : `docker compose ps` montre le conteneur en état `Restarting`.

**Solution** :

```bash
docker compose logs actual-server
ls -la ~/actual-budget/data
sudo chown -R $USER:$USER ~/actual-budget/data
docker compose up -d
```

**Cause fréquente** : permissions incorrectes sur le dossier `data`.

### L'interface web ne répond pas

**Symptôme** : `http://ton-serveur:5006` retourne un timeout.

**Solution** :

```bash
sudo lsof -i :5006
# Si occupé, change le port dans docker-compose.yml
ports:
  - "5007:5006"
```

### Le sync mobile ne fonctionne pas

**Solution** :

1. Vérifie que ton serveur est accessible en HTTPS depuis Internet
2. Utilise l'URL complète dans l'app : `https://budget.tondomaine.com`
3. Vérifie que le mot de passe de chiffrement est identique sur l'app et le web
4. Vérifie que les WebSockets sont relayés par ton reverse proxy

### Les transactions importées sont en double

**Solution** : supprime les doublons manuellement. Pour les imports futurs, utilise "Skip existing transactions".

### GoCardless ne synchronise plus

**Solution** : reconnecte-toi à GoCardless (tokens de 90 jours), puis Settings > Bank Sync > Refresh Connection.

### La base de données est corrompue

**Solution** : restaure depuis le dernier backup :

```bash
cd ~/actual-budget && docker compose down
tar xzf /backup/actual-budget-dernier.tar.gz
docker compose up -d
```

**Prévention** : backup quotidien avec Duplicati.

## FAQ : Actual Budget Docker

### Actual Budget est-il vraiment gratuit ?

Oui. Actual Budget est open-source sous licence BSD-3-Clause. Tu peux l'installer gratuitement sur ton serveur sans limite d'utilisateurs ni de budgets. Il n'y a aucun abonnement, aucune fonctionnalité payante, aucune publicité.

### Puis-je utiliser Actual Budget sans Docker ?

Oui, tu peux installer Actual Budget directement via Node.js ou le télécharger comme application desktop. Mais Docker reste la méthode la plus simple pour l'auto-hébergement : une commande, un volume, et c'est prêt. Pas besoin de gérer les dépendances Node.js ni les mises à jour manuelles.

### Actual Budget fonctionne-t-il avec les banques françaises ?

Oui, via GoCardless. Les banques suivantes sont compatibles : BNP Paribas, Société Générale, Crédit Mutuel, CIC, Banque Postale, Hello bank!, Boursorama, Fortuneo, Monabanq, ING Direct. Le sync automatique récupère tes transactions sans que tu aies à les saisir à la main.

### Quelle est la différence entre Actual Budget et YNAB ?

Les deux utilisent la méthode des enveloppes. La différence clé : YNAB est propriétaire, cloud-only, payant (14,99 $/mois) et sans sync bancaire français. Actual Budget est open-source, auto-hébergé, gratuit, et compatible GoCardless pour les banques européennes.

### Puis-je migrer depuis YNAB 4 ?

Oui. Actual Budget supporte l'import JSON depuis YNAB 4 (la version desktop). Tes catégories, transactions et soldes sont conservés. Va dans Settings > Import et sélectionne ton fichier JSON exporté.

### Combien de RAM consomme Actual Budget avec Docker ?

Moins de 100 Mo de RAM au repos. L'image Docker fait environ 200 Mo. C'est l'un des gestionnaires de budget les plus légers que tu puisses auto-héberger. Un Raspberry Pi 4 avec 2 Go de RAM suffit largement.

### Est-ce que mes données sont vraiment chiffrées ?

Oui. Actual Budget utilise un chiffrement de bout en bout côté client. Tes données sont chiffrées dans ton navigateur avant d'être envoyées au serveur. Même si quelqu'un accède à la base SQLite sur ton serveur, il ne peut rien lire sans ton mot de passe de chiffrement.

### Que faire si je perds mon mot de passe de chiffrement ?

Tu perds l'accès à tes données. Il n'y a pas de "mot de passe oublié" ni de backdoor. C'est le prix du chiffrement E2E. Stocke ton mot de passe dans un gestionnaire de mots de passe comme Vaultwarden.

## Conclusion

Actual Budget est l'outil qu'il manquait à ton homelab. Pas un tracker de dépenses anonyme qui te juge après coup, mais un véritable système de budgeting qui te dit **à l'avance** où va ton argent. La méthode des enveloppes est la plus efficace que j'ai testée pour ne plus finir à découvert, et Actual Budget la rend accessible sans facturer 15 dollars par mois.

L'installation Docker est ridiculement simple. Une image, un port, un volume. Cinq minutes et tu as un outil financier complet, chiffré, syncable avec ta banque française, et hébergé chez toi. Si tu cherches un moyen concret de reprendre le contrôle de tes données personnelles, commencer par ses finances est un excellent choix.

N'oublie pas : un service auto-hébergé sans backup, c'est un service provisoire. Configure Duplicati pour sauvegarder ton dossier `data/` avant d'aller dormir. Et si tu veux noter tes dépenses rapides ou des idées de budgets avant de les structurer dans Actual Budget, j'ai aussi couvert [Memos avec Docker](/memos-docker-notes-auto-heberge/), un bloc-notes auto-hébergé ultra-léger et minimaliste parfait pour des notes rapides.

Maintenant, ouvre ton terminal, crée ton dossier `~/actual-budget`, et dis adieu aux fins de mois surprises.
