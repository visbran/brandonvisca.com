---
title: "Linkding Docker : gestionnaire de bookmarks auto-hébergé"
description: "Guide Linkding Docker : déploie ton gestionnaire de bookmarks auto-hébergé en 2 minutes. Alternative open-source légère à Pinboard et Pocket."
pubDatetime: "2026-06-08T08:00:00.000Z"
modDatetime: "2026-06-09T00:00:00+01:00"
author: Brandon Visca
tags:
  - docker
  - auto-hebergement
  - homelab
  - debutant
  - productivite
  - guide
featured: false
draft: false
focusKeyword: linkding docker
faqs:
  - question: "Linkding fonctionne-t-il sans PostgreSQL ?"
    answer: "Oui, Linkding utilise SQLite par défaut. Pour des charges importantes ou du multi-user, PostgreSQL est recommandé, mais l'image Docker fonctionne en SQLite out of the box sans base externe."
  - question: "Puis-je importer mes bookmarks Pinboard, Pocket ou navigateur ?"
    answer: "Oui, via un fichier Netscape HTML (format standard d'export de bookmarks). L'import se fait directement depuis l'interface web de Linkding."
  - question: "Linkding consomme-t-il beaucoup de ressources ?"
    answer: "Non, Linkding est extrêmement sobre : environ 100 Mo de RAM avec l'image Docker officielle. C'est un des gestionnaires de bookmarks les plus légers du marché auto-hébergé."
  - question: "Existe-t-il une API pour automatiser l'ajout de liens ?"
    answer: "Oui, Linkding expose une API REST complète. De plus, il offre une page d'ajout rapide et un bookmarklet pour sauvegarder un site en un clic depuis le navigateur."
  - question: "Linkding est-il multi-utilisateur ?"
    answer: "Par défaut non, mais l'option LD_ENABLE_AUTH_PROXY permet une authentification multi-user via un reverse proxy comme Caddy ou Traefik."
---
> 💡 **TL;DR**
> - Gestionnaire de bookmarks open-source et auto-hébergé qui archive tes liens automatiquement
> - Un `docker-compose.yml` de 20 lignes avec SQLite : opérationnel en 2 minutes
> - Zéro euro, licence MIT, environ 100 Mo de RAM (tourne sur un Raspberry Pi)

Tu collectionnes des liens dans 4 navigateurs différents, 3 services cloud, et un fichier texte sur le bureau ? Tu paies Pinboard depuis 2012 et t'es tanné du modèle SaaS qui change les règles quand ça l'arrange ? Tu regrettes l'époque où délicieux.icio.us existait sans te vendre à Mozilla ?

Bonne nouvelle : **Linkding** existe. C'est un gestionnaire de bookmarks open-source, écrit en Django, avec une interface épurée en Tailwind CSS. Tu le déploies chez toi en Docker, tu gardes le contrôle total de tes données, et il consomme si peu de ressources que tu peux le faire tourner sur un Raspberry Pi sans broncher.

Dans cet article, on installe Linkding avec Docker Compose (version simple SQLite), on configure l'import de bookmarks, on active l'archive automatique, et on compare honnêtement les alternatives du marché.

Si tu débutes en auto-hébergement, commence par mon [guide Docker pour débutants](/docker-debutant-services-auto-heberger/) pour bien poser les bases. Et si tu cherches d'autres outils de productivité auto-hébergés, j'ai aussi testé [Miniflux pour le RSS](/miniflux-docker-lecteur-rss-guide/) et [Gitea pour le versionning](/gitea-serveur-git-docker-auto-hebergement/).

## Table des matières

## Pourquoi auto-héberger ses bookmarks en 2026 ?

Les services de bookmarks commerciaux ont un problème structurel : ils dépendent de modèles économiques qui changent. Pinboard, autrefois vendu comme "l'alternative simple à Delicious", est devenu payant à vie, puis a accumulé des années de bugs et de retard. Pocket a été racheté par Mozilla, traque ta lecture, et intègre un algo de suggestions que personne n'a demandé. Chrome synchronise tes bookmarks, mais bon, tu confies tes données à Google, ce qui n'est pas exactement un modèle de souveraineté numérique.

**Les trois raisons de switcher à Linkding :**

1. **Souveraineté des données**, Tes bookmarks restent sur ton serveur. Pas d'API tierce qui ferme, pas de changement de CGU surprise.
2. **Légèreté**, Linkding pèse moins d'une centaine de mégaoctets en RAM. Compare avec un Nextcloud ou un Wallabag gonflés par leurs dépendances PHP.
3. **Fonctionnalités ciblées**, Tagging, archive automatique des pages (HTML snapshot), API REST, import/export Netscape HTML. Rien de superflu, tout ce qu'il faut.

L'archive automatique est particulièrement intéressante : Linkding télécharge une copie statique de la page web que tu bookmarkes. Si le lien meurt (404, site fermé, paywall), tu conserves une version lisible chez toi. C'est le genre de feature qui semble anodine jusqu'au jour où tu cherches un tuto technique et que le blog a disparu.

## Prérequis

Avant de lancer le Docker Compose, assure-toi d'avoir :

- Un serveur avec Docker et Docker Compose installés (voir mon [guide Docker débutant](/docker-debutant-services-auto-heberger/) si besoin)
- Un nom de domaine pointant vers ton serveur (ou un reverse proxy local si tu restes en LAN)
- Docker Engine 20.10+ et Compose v2+ (testé avec la stack actuelle)
- Optionnel mais recommandé : un reverse proxy HTTPS (j'utilise [Caddy dans cet exemple](/caddy-docker-reverse-proxy-guide/))

Linkding fonctionne parfaitement avec SQLite, donc tu n'as pas besoin d'une base de données externe pour démarrer. Si tu prends plus de 10 000 bookmarks et plusieurs utilisateurs, alors oui, migre vers PostgreSQL. Mais pour un usage personnel standard, SQLite suffit amplement.

## Docker Compose : le setup minimal

Voici le fichier `docker-compose.yml` pour déployer Linkding. Une seule image, zéro dépendance, prêt à tourner.

```yaml
version: "3.8"

services:
  linkding:
    image: sissbruecker/linkding:latest
    container_name: linkding
    restart: unless-stopped
    ports:
      - "9090:9090"
    volumes:
      - ./data:/etc/linkding/data
    environment:
      - LD_SUPERUSER_NAME=admin
      - LD_SUPERUSER_PASSWORD=Ch4ngeM01nten4nt!
      - LD_DISABLE_BACKGROUND_TASKS=False
      - LD_ENABLE_REQUEST_LOGS=False
```

**Explication ligne par ligne :**

- `image: sissbruecker/linkding:latest`, L'image officielle, maintenue par l'auteur du projet. Elle est mise à jour régulièrement et reste légère (~300 Mo).
- `container_name: linkding`, Pour identifier facilement le conteneur avec `docker ps`.
- `restart: unless-stopped`, Le conteneur redémarre automatiquement après un reboot du serveur, sauf si tu l'arrêtes explicitement.
- `ports: "9090:9090"`, Expose le port 9090 du conteneur sur le port 9090 de l'hôte. Si tu passes par un reverse proxy, ce port reste en interne et tu n'exposes que le reverse proxy.
- `volumes: ./data:/etc/linkding/data`, Persiste la base SQLite et les archives HTML sur le disque local dans un dossier `./data`. Sans ce volume, tes bookmarks disparaissent dès que le conteneur est recréé.
- `LD_SUPERUSER_NAME` et `LD_SUPERUSER_PASSWORD`, Crée automatiquement un compte admin au premier démarrage. **Change ce mot de passe immédiatement**, c'est du clair dans le YAML mais nécessaire pour l'initialisation.
- `LD_DISABLE_BACKGROUND_TASKS=False`, Active les tâches d'arrière-plan, notamment l'archive automatique des pages web. Mets `True` si tu veux un serveur ultra-minimal sans snapshots.
- `LD_ENABLE_REQUEST_LOGS=False`, Désactive les logs de requêtes HTTP pour alléger les logs. Mets à `True` si tu debugues.

Si tu veux sécuriser un minimum le truc, ne laisse pas le port 9090 ouvert sur internet. Jette plutôt un œil à mon guide [UFW avec Docker](/ufw-docker-pare-feu-linux/) pour configurer un pare-feu propre, ou passe directement par un reverse proxy HTTPS avec [Caddy](/caddy-docker-reverse-proxy-guide/).

## Déploiement et premiers pas

```bash
# Crée le dossier de projet
mkdir -p ~/linkding && cd ~/linkding

# Crée le fichier docker-compose.yml ci-dessus
nano docker-compose.yml

# Lance le service
docker compose up -d

# Vérifie que le conteneur tourne
docker ps | grep linkding

# Récupère les logs au besoin
docker compose logs -f
```

Après le premier démarrage, connecte-toi à `http://IP-DU-SERVEUR:9090` (ou via ton reverse proxy) avec les identifiants définis dans `LD_SUPERUSER_NAME` et `LD_SUPERUSER_PASSWORD`.

**Premiers réglages à faire dans l'interface :**

1. Change le mot de passe admin dans Settings > Change Password
2. Active l'archive automatique : Settings > General > "Create snapshots for bookmarked websites" → cocher
3. Configure le bookmarklet (dans le menu en haut à droite) pour ajouter des liens en un clic depuis ton navigateur

Le bookmarklet est un petit bouton que tu glisses dans la barre de favoris de ton navigateur. Quand tu es sur une page à sauvegarder, un clic sur ce bouton ouvre Linkding avec l'URL et le titre pré-remplis. C'est le workflow le plus rapide.

## Import et export de bookmarks

Linkding utilise le format **Netscape Bookmark File Format** (fichier HTML avec une structure `DL > DT > A`). C'est le format standard exporté par Chrome, Firefox, Safari, Pinboard, Pocket (via des convertisseurs), et quasiment tous les gestionnaires de bookmarks.

**Importer depuis Chrome :**

1. Chrome > Menu > Favoris > Gestionnaire de favoris > ⋮ > Exporter les favoris → sauvegarde en HTML
2. Dans Linkding : Settings > Import > choisir le fichier HTML > Import

**Depuis Pinboard :**

1. Pinboard > Settings > Backup > Export > Format : HTML (Netscape)
2. Import dans Linkding de la même manière

L'import conserve les tags si le fichier source les inclut. Si des tags sont absents, Linkding les ignore silencieusement sans planter.

**Export** se fait aussi depuis Settings > Export. Tu récupères un fichier HTML que tu peux réimporter n'importe où. C'est ce qu'on appelle la portabilité des données, et c'est un point fort des projets open-source bien fichus.

## L'API REST et les automatismes

Linkding expose une API REST complète documentée à `/api/`. Toutes les opérations CRUD sur les bookmarks sont disponibles via token d'authentification.

**Générer un token API :**

Va dans Settings > API. Tu récupères une clé REST API Key à utiliser dans l'en-tête `Authorization: Token <ta_clé>`.

**Exemple : ajouter un bookmark via curl**

```bash
curl -X POST http://localhost:9090/api/bookmarks/ \
  -H "Authorization: Token ta_clé_api" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://brandonvisca.com",
    "title": "Brandon Visca - Blog tech",
    "description": "Blog homelab et auto-hébergement",
    "tag_names": ["auto-hebergement", "blog"]
  }'
```

Tu peux automatiser l'ajout de liens depuis n'importe quel script, extension de navigateur, ou service tiers compatible. Certains utilisateurs couplent ça avec des flux RSS ou des raccourcis iOS pour envoyer un lien vers Linkding en un swipe.

## Sécuriser l'accès

Linkding n'intègre pas de HTTPS natif. Tu dois donc le placer derrière un reverse proxy à certificat valide. Pour un setup rapide et propre, je recommande [Caddy Docker](/caddy-docker-reverse-proxy-guide/) avec ce bloc dans ton Caddyfile :

```caddyfile
bookmarks.tondomaine.com {
    reverse_proxy localhost:9090
}
```

Si tu veux une couche de sécurité supplémentaire :

- Active l'authentification basique de Caddy ou ajoute un middleware SSO via Traefik
- Restreint l'IP d'accès dans le pare-feu avec [UFW](/ufw-docker-pare-feu-linux/)
- Change le mot de passe superuser régulièrement
- Garde Linkding à jour : `docker compose pull && docker compose up -d`

Pour les options avancées (authentification via header proxy, multi-user), consulte la [documentation officielle de Linkding sur GitHub](https://github.com/sissbruecker/linkding). Dans la majorité des cas, un simple Caddyfile + UFW suffit à sécuriser un usage personnel.

## Tableau comparatif : Linkding vs les alternatives

| Critère | Linkding | Pinboard | Wallabag | Shaarli | Pocket (Mozilla) |
|---------|----------|----------|----------|---------|-------------------|
| **Hébergement** | Auto-hébergé | SaaS payant | Auto-hébergé | Auto-hébergé | SaaS gratuit (tracking) |
| **Licence** | MIT | Propriétaire | MIT | zlib | Propriétaire |
| **Prix** | Gratuit | ~$25/année | Gratuit | Gratuit | Gratuit (données) |
| **Stack technique** | Django + SQLite/PG | Inconnu | PHP + MariaDB | PHP + SQLite | Propriétaire |
| **Taille Docker** | ~300 Mo image, ~100 Mo RAM | N/A | ~1 Go image, 300+ Mo RAM | ~100 Mo RAM | N/A |
| **Archive automatique** | Oui (HTML snapshot) | Non | Oui (fulltext) | Non | Oui (mode lecture) |
| **API REST** | Oui | Oui ($) | Oui | Non | Limitée |
| **Import Netscape HTML** | Oui | Oui | Oui | Oui | Non (fermé) |
| **Bookmarklet** | Oui | Oui | Oui | Oui | Extension navigateur |
| **Multi-user** | Optionnel | Oui | Oui | Oui | Non |
| **Open-source** | Oui | Non | Oui | Oui | Non |
| **Mobile / Responsive** | Oui | Oui | Via PWA | Oui | Apps natives |

**Quand choisir quoi ?**

- **Linkding** : tu veux une solution auto-hébergée, légère, sans base de données complexe, avec archivage automatique. L'usage personnel simple et efficace.
- **Pinboard** : tu veux zéro maintenance et tu es prêt à payer pour un service qui ne bouge pas. Mais attention aux retards de développement connus.
- **Wallabag** : tu cherches principalement de la lecture différée avec parsing de texte complet (comme Pocket). C'est un lecteur d'articles, pas un gestionnaire de bookmarks pur.
- **Shaarli** : tu veux un truc en PHP très léger, sans base de données externe, avec une esthétique brute et fonctionnelle. C'est le linkding des années 2010.
- **Pocket** : tu tiens absolument aux apps mobiles officielles et aux recommandations algorithmiques. En échange, tu cèdes tes données de lecture.

Mon avis perso : si tu as déjà un serveur Docker qui tourne pour [Miniflux](/miniflux-docker-lecteur-rss-guide/) ou [Gitea](/gitea-serveur-git-docker-auto-hebergement/), ajouter Linkding ne coûte que quelques dizaines de mégaoctets de RAM. L'effort est quasi nul et le gain en souveraineté est réel.

## Astuces et bonnes pratiques

**Garder ses archives propres**

L'archive automatique génère des fichiers HTML statiques dans le volume persistant. Si tu bookmarkes massivement, surveille l'espace disque avec `du -sh ./data` ou via [Beszel pour monitorer ton serveur](/beszel-monitoring-docker/). Les snapshots peuvent peser plusieurs mégaoctets chacun selon la complexité des pages.

**Mettre à jour sans perdre de données**

```bash
cd ~/linkding
docker compose pull
docker compose up -d
```

Le volume `./data` persiste la base SQLite et les archives entre les recréations de conteneur. Ne supprime jamais ce dossier sans backup.

**Backup régulier**

Le dossier `./data` contient tout. Une simple copie rsync ou un [backup Duplicati](/duplicati-docker-sauvegarde/) suffit. Le fichier principal est `db.sqlite3`, mais pense aussi à sauvegarder le sous-dossier `assets` qui contient les archives HTML.

```bash
# Backup manuel simple
tar czf linkding-backup-$(date +%F).tar.gz ./data
```

**Personnaliser le port**

Si le port 9090 est déjà pris, change simplement la partie gauche du mapping :

```yaml
ports:
  - "8085:9090"
```

**Ne pas exposer directement sur internet**

Comme pour tous les services Docker, préfère un reverse proxy (Caddy, Traefik, Nginx Proxy Manager) avec HTTPS plutôt que d'exposer le port 9090 brut. C'est la règle d'or de l'auto-hébergement : un seul point d'entrée HTTPS sécurisé, derrière un pare-feu configuré correctement.

Si tu cherches à durcir la sécurité de ton serveur, jette un œil à mon [hardening Linux en 10 commandes](/hardening-linux-10-commandes/) pour un vernis rapide et efficace.

## Conclusion

Linkding est l'un de ces outils qui font exactement ce qu'on leur demande, sans artifices ni usine à gaz. Il gère tes bookmarks, les archive automatiquement, expose une API propre, et se déploie en un temps record avec Docker. La balance effort/bénéfice est parfaitement équilibrée : 2 minutes de setup pour un service que tu utiliseras pendant des années.

Si tu es sérieux sur ton auto-hébergement, Linkding mérite une place dans ta stack. Il remplace élégamment Pinboard, réconcilie tes bookmarks éparpillés, et t'offre la tranquillité de savoir que tes liens ne disparaîtront pas avec un changement de politique d'une boîte californienne.

Maintenant, à toi de jouer. Crée ton dossier, copie le Compose, lance le conteneur, et importe tes 2000 bookmarks oubliés depuis 2014. Tu me remercieras quand le prochain service SaaS fermera ses portes.

## Pour aller plus loin

- [Linkding sur GitHub](https://github.com/sissbruecker/linkding), code source, releases et documentation officielle
- [Caddy Docker : reverse proxy HTTPS](/caddy-docker-reverse-proxy-guide/), pour exposer Linkding proprement en HTTPS
- [Miniflux : lecteur RSS auto-hébergé](/miniflux-docker-lecteur-rss-guide/), le complément idéal à tes bookmarks dans une stack souveraine