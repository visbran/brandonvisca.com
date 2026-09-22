---
title: "Installer Tianji : l'analytics auto-hébergé"
description: "Installer Tianji pas à pas : LXC Proxmox ou Docker, script de suivi sur un site statique, et la collecte sans exposer ton instance sur Internet."
pubDatetime: "2026-05-12T18:00:00+02:00"
modDatetime: 2026-09-22 21:30:00+02:00
author: Brandon Visca
tags:
  - intermediaire
  - auto-hebergement
  - docker
  - securite
  - monitoring
  - guide
featured: false
draft: false
focusKeyword: installer Tianji
faqs:
  - question: "Faut-il exposer Tianji sur Internet pour suivre un site public ?"
    answer: "Non. Le script de suivi tourne dans le navigateur du visiteur, donc un point d'entrée public est nécessaire, mais ça peut être un proxy sur ton propre domaine. Tianji reste joignable uniquement depuis ton réseau local ou ton VPN."
  - question: "Pourquoi tous mes visiteurs apparaissent-ils aux États-Unis ?"
    answer: "Tianji fait confiance à l'en-tête cf-connecting-ip en priorité. Si tu passes par un Worker ou une Function Cloudflare, cet en-tête est réécrit avec l'IP de sortie de Cloudflare. Il faut transmettre l'IP du visiteur dans un en-tête dédié et le déclarer avec la variable CLIENT_IP_HEADER."
  - question: "LXC Proxmox ou Docker : que choisir ?"
    answer: "Docker Compose si tu veux le chemin officiel, documenté et identique partout. Le script LXC de la communauté Proxmox si tu préfères un conteneur système dédié, avec sa propre base PostgreSQL et un vzdump pour la sauvegarde."
  - question: "Tianji remplace-t-il vraiment Google Analytics ?"
    answer: "Pour un blog ou un site vitrine, oui. Pour l'attribution multi-canal, les audiences de remarketing ou l'intégration Google Ads, non : GA4 reste nécessaire."
  - question: "Quelles sont les différences avec Umami ?"
    answer: "Tianji est inspiré d'Umami mais ajoute l'uptime monitoring, le server status, les sondages et la télémétrie. C'est un hub tout-en-un, pas seulement de l'analytics."
---
> 💡 **TL;DR**
> - Alternative open-source à Google Analytics, auto-hébergée, sans cookie ni bannière RGPD
> - Installation en LXC Proxmox ou en Docker Compose, en une dizaine de minutes
> - Le point que personne n'explique : collecter les visites **sans exposer** ton instance sur Internet
> - Deux pièges vécus : la base pas prête au démarrage, et la géolocalisation qui met tout le monde aux États-Unis

## Table des matières

## Pourquoi j'ai remplacé Google Analytics

Tu connais le feeling. Tu te connectes à Google Analytics, tu vois un tableau de bord avec 47 menus, 12 pop-ups « nouvelle fonctionnalité », et ta journée est partie.

Depuis GA4, c'est devenu **illisible** pour un site perso. Les rapports sont faits pour des équipes marketing de 20 personnes, pas pour toi qui veux juste savoir si ton article sur Docker a fait 200 vues hier.

Et puis il y a la vie privée. Le RGPD, les bannières de cookies, les gestionnaires de consentement à 30 $ par mois… tout ça pour pister des visiteurs qui cliquent « Refuser » de toute façon.

Si toi aussi tu cherches à [quitter Google et reprendre le contrôle de tes données](/quitter-google-auto-hebergement/), tu es au bon endroit. J'ai testé Umami, Plausible et Matomo. C'est bien. J'ai fini sur **Tianji**, et cet article est le guide que j'aurais voulu lire : l'installation, le branchement sur un site statique, et surtout la partie que les autres tutoriels passent sous silence, comment collecter les visites sans ouvrir son instance au monde entier.

---

## Ce que fait Tianji

Tianji ([msgbyte/tianji](https://github.com/msgbyte/tianji) sur GitHub) se présente comme un « All-in-One Insight Hub ». En clair, quatre outils dans une seule application :

| Module | Ce que ça remplace |
|---|---|
| **Website Analytics** | Umami, Plausible, GA4 |
| **Uptime Monitor** | [Uptime Kuma](/uptime-kuma-2-0-monitoring-auto-heberge/), UptimeRobot |
| **Server Status** | Netdata, un bout de Prometheus |
| **Surveys & Telemetry** | Typeform, la télémétrie maison d'un projet open-source |

Le projet est sous licence Apache 2.0, écrit en TypeScript avec Prisma et Next.js, et les versions sortent régulièrement. Avant Tianji, mon monitoring, c'était trois services, trois identifiants, trois tableaux de bord. Maintenant c'est un seul.

![Vue d'ensemble de Tianji : visiteurs, pages vues et graphique des 7 derniers jours](tianji-self-hosted-analytics-1.webp)

> 💡 **Astuce** : tu peux essayer Tianji sans rien installer sur [tianji.dev](https://tianji.dev), l'instance de démonstration est ouverte.

---

## Installer Tianji : deux chemins possibles

### Installer Tianji en LXC sur Proxmox

C'est ce que j'utilise. Le script de la communauté [Proxmox VE Helper-Scripts](https://community-scripts.org/scripts?q=analytic) crée un conteneur Debian avec PostgreSQL et Tianji en service systemd, sans Docker :

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/community-scripts/ProxmoxVE/main/ct/tianji.sh)"
```

Le script demande les ressources du conteneur, 2 vCPU et 2 Go de RAM suffisent largement, puis il fait le reste. À la fin, l'interface répond sur `http://IP-DU-LXC:12345`.

Deux choses à savoir pour la suite : la base s'appelle `tianji_db` (et pas `tianji`, ça m'a fait chercher), et le service se pilote comme n'importe quel service systemd :

```bash
systemctl status tianji
systemctl status postgresql@17-main   # si la base tombe, Tianji tombe avec
journalctl -u tianji -n 100 --no-pager
```

### Installer Tianji avec Docker Compose

Le chemin officiel, valable sur un VPS comme sur une machine du salon. Si tu débutes, passe d'abord par mon [guide Docker pour débutants](/docker-debutant-services-auto-heberger/).

```yaml
services:
  tianji:
    image: moonrailgun/tianji:1.26.1
    ports:
      - "12345:12345"
    environment:
      DATABASE_URL: postgresql://tianji:tianji@postgres:5432/tianji
      JWT_SECRET: remplace-moi
      ALLOW_REGISTER: "false"
      ALLOW_OPENAPI: "true"
    depends_on:
      postgres:
        condition: service_healthy
    restart: always
  postgres:
    image: postgres:15.4-alpine
    environment:
      POSTGRES_DB: tianji
      POSTGRES_USER: tianji
      POSTGRES_PASSWORD: tianji
    volumes:
      - tianji-db-data:/var/lib/postgresql/data
    restart: always
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U tianji -d tianji"]
      interval: 5s
      timeout: 5s
      retries: 20
volumes:
  tianji-db-data:
```

> ⚠️ **Change le `JWT_SECRET`** avant de déployer : `openssl rand -hex 32`. La valeur d'exemple est publique, donc n'importe qui pourrait forger une session valide sur ton instance.

**Le `healthcheck` n'est pas décoratif.** Sans lui, Tianji démarre avant PostgreSQL, la migration Prisma échoue et le conteneur reste muet :

```text
Error: P1001: Can't reach database server at `postgres:5432`
```

Le conteneur tourne, le port répond… mais rien ne s'affiche. Avec `condition: service_healthy`, le problème disparaît.

Ensuite, `docker compose up -d`, puis `http://ton-serveur:12345`. Tu crées ton compte, tu ajoutes ton site, et Tianji te donne un script de suivi à coller dans ton HTML.

![Vue détaillée d'un site dans Tianji : vues, visiteurs, taux de rebond et courbe du trafic](tianji-self-hosted-analytics-2.webp)

---

## Brancher le script sur un site statique

Tianji te donne quelque chose comme ça :

```html
<script async defer src="https://tianji.example.com/tracker.js" data-website-id="ton-identifiant"></script>
```

Le script est cookieless, il n'a besoin d'aucune bannière de consentement. Quelques attributs valent le détour :

| Attribut | Effet |
|---|---|
| `data-domains` | Limite le suivi à une liste de domaines, pratique pour ne pas compter tes previews de déploiement |
| `data-do-not-track` | Respecte le réglage « Do Not Track » du navigateur |
| `data-host-url` | Force l'adresse de collecte, si elle diffère de celle du script |

Sans `data-host-url`, le script envoie les visites **au dossier d'où il a été chargé**. C'est ce détail qui rend possible tout ce qui suit.

> ⚠️ **Piège si ton site est construit en CI.** Sur un site statique déployé par GitHub Actions, les variables d'environnement de ton hébergeur ne sont pas forcément lues au moment du build. Chez moi, l'identifiant du site vivait dans les variables Cloudflare Pages, la fonction serveur les voyait bien… mais la balise `<script>` n'apparaissait pas dans le HTML. Il a fallu déclarer la variable dans le workflow lui-même.

---

## Collecter sans exposer son instance

Voilà le vrai sujet. Mon Tianji tourne sur un LXC du réseau local, joignable uniquement par VPN. Or le script de suivi s'exécute dans le navigateur de visiteurs qui, eux, sont sur Internet. Pointer le script sur une adresse locale ne marche pas : les visiteurs ne joignent pas ton LAN, et chaque page déclenche une erreur dans leur console.

Il faut donc **un point d'entrée public**, mais ça n'oblige pas à exposer l'interface d'administration de Tianji. Voici le montage que j'utilise :

```text
navigateur → https://ton-site.fr/stats/*     (proxy sur ton propre domaine)
           → https://collecte.ton-site.fr    (tunnel + contrôle d'accès)
           → http://localhost:12345          (Tianji, chez toi)
```

Trois bénéfices immédiats :

1. **Aucun port ouvert** chez toi : le tunnel établit une connexion sortante.
2. **Tianji injoignable** sans le jeton de service : sans lui, le nom d'hôte public répond `403`.
3. **Requêtes first-party** : comme tout part de ton domaine, les bloqueurs de publicité laissent passer beaucoup plus de visites.

### Le proxy, avec une liste blanche

La pièce centrale tient en quelques lignes. C'est une fonction serverless (ici Cloudflare Pages, mais le principe vaut pour Netlify ou un bloc Nginx) qui ne relaie **que trois chemins** :

```js
const ALLOWED = new Map([
  ["tracker.js", ["GET", "HEAD"]],
  ["api/website/send", ["POST"]],
  ["api/website/batch", ["POST"]],
]);
```

Tout le reste renvoie `404`. Concrètement, `/stats/login` ne mène nulle part : l'interface d'administration n'est pas atteignable par ce chemin, même si quelqu'un devine l'URL.

La fonction ajoute ensuite les en-têtes du jeton de service (`CF-Access-Client-Id` et `CF-Access-Client-Secret`, stockés en variables chiffrées) et supprime les `set-cookie` des réponses.

### L'ordre des opérations compte

Crée **le contrôle d'accès avant le DNS**. Dans l'autre sens, ton nom d'hôte reste ouvert quelques minutes, le temps que tu configures la règle. Donc :

1. Un jeton de service, puis une règle qui n'autorise que lui, puis l'application rattachée au nom d'hôte.
2. Le tunnel, avec une règle d'entrée limitée à ce seul nom d'hôte, le reste en `404`.
3. Le DNS en dernier.

Et pour vérifier, trois commandes :

```bash
curl -o /dev/null -w '%{http_code}\n' https://collecte.ton-site.fr/tracker.js   # 403 attendu
curl -o /dev/null -w '%{http_code}\n' https://ton-site.fr/stats/tracker.js      # 200
curl -o /dev/null -w '%{http_code}\n' https://ton-site.fr/stats/login           # 404
```

### Le piège de la géolocalisation

Une fois en place, mes premières visites sont remontées… **toutes des États-Unis**. Y compris une visite de test envoyée depuis la France.

La cause est dans le code de Tianji (`src/server/utils/detect.ts`) :

```ts
export function getIpAddress(req) {
  if (process.env.CLIENT_IP_HEADER && req.headers[process.env.CLIENT_IP_HEADER]) {
    return String(req.headers[process.env.CLIENT_IP_HEADER]);
  } else if (req.headers['cf-connecting-ip']) {
    return String(req.headers['cf-connecting-ip']);
  }
  return getClientIp(req);
}
```

Tianji fait confiance à `cf-connecting-ip` en priorité. Or Cloudflare **réécrit cet en-tête** sur les requêtes sortantes d'un Worker : Tianji recevait donc l'adresse de sortie de Cloudflare, aux États-Unis.

La solution tient dans la première branche du code : transmettre l'IP du visiteur dans un en-tête à toi, et le déclarer à Tianji.

```ini
; /etc/systemd/system/tianji.service.d/client-ip.conf
[Service]
Environment=CLIENT_IP_HEADER=x-visitor-ip
```

En Docker, c'est une ligne dans `environment:`. Côté proxy, tu recopies l'IP du visiteur dans cet en-tête avant de relayer. Après ça, mes visites sont reparties en France, ville comprise.

> ⚠️ **Le revers** : avec ce réglage, quiconque peut joindre Tianji directement peut annoncer l'adresse IP de son choix. Ça reste acceptable tant que seul ton proxy, authentifié, et ton réseau local y ont accès. Ça ne le serait pas sur une instance ouverte à tous.

---

## Les limites, parce qu'il faut être honnête

Tianji n'est pas un remplaçant au millimètre de GA4. Si tu as besoin d'attribution multi-canal, d'audiences de remarketing, d'une intégration Google Ads ou de tunnels de conversion, reste sur GA4 ou passe sur Matomo.

Autres points à connaître avant de t'engager :

- **L'interface est en anglais**, sans traduction française à ce jour.
- **PostgreSQL est un point de défaillance unique** : si la base tombe, tu perds la collecte. Pense au `pg_dump` régulier, les données analytiques ne se rattrapent pas.
- **Les visites bloquées restent bloquées** : le passage en first-party aide, mais un bloqueur agressif passe quand même à travers.

Pour un blog, un site vitrine ou un portfolio, ça couvre l'essentiel sans la charge mentale de Google.

---

## FAQ

### Faut-il exposer Tianji sur Internet pour suivre un site public ?

Non. Le script de suivi tourne dans le navigateur du visiteur, donc un point d'entrée public est nécessaire, mais ça peut être un proxy sur ton propre domaine. Tianji reste joignable uniquement depuis ton réseau local ou ton VPN.

### Pourquoi tous mes visiteurs apparaissent-ils aux États-Unis ?

Tianji fait confiance à l'en-tête `cf-connecting-ip` en priorité. Si tu passes par un Worker ou une Function Cloudflare, cet en-tête est réécrit avec l'IP de sortie de Cloudflare. Il faut transmettre l'IP du visiteur dans un en-tête dédié et le déclarer avec la variable `CLIENT_IP_HEADER`.

### LXC Proxmox ou Docker : que choisir ?

Docker Compose si tu veux le chemin officiel, documenté et identique partout. Le script LXC de la communauté Proxmox si tu préfères un conteneur système dédié, avec sa propre base PostgreSQL et un vzdump pour la sauvegarde.

### Tianji remplace-t-il vraiment Google Analytics ?

Pour un blog ou un site vitrine, oui. Pour l'attribution multi-canal, les audiences de remarketing ou l'intégration Google Ads, non : GA4 reste nécessaire.

### Quelles sont les différences avec Umami ?

Tianji est inspiré d'Umami mais ajoute l'uptime monitoring, le server status, les sondages et la télémétrie. C'est un hub tout-en-un, pas seulement de l'analytics.

---

## Conclusion

Installer Tianji prend dix minutes. Le brancher proprement sur un site public en prend trente de plus, et c'est là que se joue la différence entre « j'ai des statistiques » et « j'ai des statistiques sans avoir ouvert mon homelab à Internet ».

Retiens les trois points qui m'ont coûté du temps : le `healthcheck` sur la base, la variable d'environnement qui doit être présente **au moment du build** pour un site statique, et `CLIENT_IP_HEADER` sans quoi toute ta géolocalisation est fausse.

Le reste, c'est du confort : un tableau de bord lisible, aucune bannière de cookies, et des données qui restent chez toi.

---

## Pour aller plus loin

- [Uptime Kuma 2.0 : le monitoring auto-hébergé qui remplace les services payants](/uptime-kuma-2-0-monitoring-auto-heberge/)
- [Docker pour les débutants : 10 services essentiels à auto-héberger](/docker-debutant-services-auto-heberger/)
- [Pourquoi j'ai quitté Google (et comment tu peux faire pareil)](/quitter-google-auto-hebergement/)
- [Cloudflare Tunnel avec Docker : exposer un service sans ouvrir de port](/cloudflare-tunnel-docker-homelab/)

💡 À lire aussi : [Wazuh Docker : SIEM open source pour surveiller ton homelab](/wazuh-docker-siem-securite-homelab/), dans la même veine que cet article.

## Articles connexes

- [Immich Docker remplace Google Photos ? Guide complet 2026](/immich-docker/)
- [Jellyfin avec Docker : Ton Netflix Gratuit en 30 Min (Économise 378€/an)](/jellyfin-docker-alternative-netflix-gratuite/)
- [Nextcloud avec Docker : Ton Cloud Perso en 1h (Adieu Google Drive !)](/nextcloud-docker-installation-complete-2025/)
- [Technitium DNS Server : installe ton bloqueur de pubs libre (2026)](/technitium-dns-server/)
