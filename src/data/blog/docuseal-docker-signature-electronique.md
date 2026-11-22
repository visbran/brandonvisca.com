---
title: "DocuSeal Docker : signature électronique auto-hébergée"
description: "Déploie DocuSeal Docker avec Docker Compose : installation, sécurisation et alternative gratuite à DocuSign pour signer tes PDF."
pubDatetime: "2026-11-22T11:01:54+01:00"
modDatetime: "2026-11-21T08:00:00.000Z"
author: Brandon
tags:
  - auto-hebergement
  - reverse-proxy
  - base-de-donnees
  - sauvegarde
  - intermediaire
featured: false
draft: false
focusKeyword: docuseal docker
faqs:
  - question: "DocuSeal Docker consomme-t-il beaucoup de ressources ?"
    answer: "Non. Le conteneur seul tourne avec 1 vCPU et 512 Mo de RAM sans souci. Si tu ajoutes PostgreSQL à côté, compte plutôt 1 Go de RAM pour l'ensemble de la stack."
  - question: "Que se passe-t-il si le certificat HTTPS automatique échoue ?"
    answer: "Vérifie d'abord que ton DNS pointe bien vers le serveur avant de lancer la commande HOST=. Si ça bloque, passe par ton reverse proxy habituel et laisse-le gérer le TLS à la place du conteneur."
  - question: "Les signatures DocuSeal ont-elles une valeur légale ?"
    answer: "Oui, DocuSeal implémente la signature électronique simple au sens eIDAS et ESIGN, avec horodatage et traçabilité des événements. Pour des actes nécessitant une signature qualifiée, il faut un prestataire de confiance certifié en plus."
---
> 💡 **TL;DR**
> - DocuSeal Docker te donne une signature électronique légalement valable, auto-hébergée via Docker Compose, sans dépendre de DocuSign
> - Projet open source sous licence AGPLv3, gratuit en self-hosted, image `docuseal/docuseal` avec SQLite par défaut (PostgreSQL conseillé en prod)
> - Compte 15 minutes pour un déploiement fonctionnel derrière ton reverse proxy, logo et SSO réservés au plan Pro payant

## DocuSeal Docker : stop payer DocuSign pour signer un PDF

Chez moi, la case « signature électronique » revenait tous les deux ou trois mois : un bail, un devis de prestation, une décharge pour un pote qui m'emprunte du matos. Je passais par DocuSign en version gratuite limitée, ou pire, par un PDF annoté à la main et renvoyé par mail. Ça fonctionne, mais ça coûte un abonnement ou ça sent l'amateurisme face à un client.

DocuSeal Docker règle les deux problèmes d'un coup. C'est un conteneur que tu lances sur ton serveur, avec une interface de signature propre, des champs à glisser-déposer sur le PDF, un workflow multi-signataires, et surtout : tes contrats restent chez toi, pas sur les serveurs d'un éditeur américain. Dans ce guide, on installe DocuSeal Docker avec Docker Compose, on configure le premier document, et on le sécurise pour un usage réel.

## Table des matières

## Qu'est-ce que DocuSeal Docker exactement

DocuSeal est un projet open source maintenu par l'organisation `docusealco` sur GitHub, distribué sous licence AGPLv3 avec des termes additionnels sur l'usage commercial du code. Concrètement : tu peux l'héberger et l'utiliser gratuitement sans limite d'utilisateurs ni de documents, mais si tu modifies le code pour en faire un service revendu à des tiers, la licence t'oblige à republier tes modifications.

Fonctionnellement, DocuSeal couvre les bases d'une plateforme de signature : upload d'un PDF, placement de champs (signature, date, texte, case à cocher), envoi d'un lien de signature par email, suivi du statut, et export du document final scellé avec un certificat d'audit. Pas de scan papier, pas d'aller-retour par mail avec des paraphes approximatifs.

Voici où DocuSeal Docker se situe face aux solutions connues :

| Critère | DocuSeal (self-hosted) | DocuSign | Documenso |
|---|---|---|---|
| Licence | AGPLv3, open source | Propriétaire | MIT, open source |
| Prix self-hosted | Gratuit (Pro à 20 $/utilisateur/mois) | Non applicable | Gratuit |
| Base de données | SQLite ou PostgreSQL/MySQL | Cloud propriétaire | PostgreSQL |
| Marque blanche | Oui (plan Pro uniquement) | Oui (payant) | Oui |
| API et webhooks | Payants en self-hosted | Payants | Inclus |

Le plan open source suffit largement pour un usage perso ou une petite structure : signature légale, conservation illimitée, dix types de champs. Les envois en masse, les rappels automatiques et le SSO restent réservés au plan Pro facturé 240 $ par utilisateur et par an. Si tu veux comparer avec une autre brique d'auto-hébergement documentaire, j'ai aussi écrit un guide sur [Paperless-ngx](/paperless-ngx-docker-guide-auto-hebergement/) pour archiver et indexer tout ce qui passe par ton scanner.

## Installer DocuSeal Docker avec Docker Compose

Avant de lancer DocuSeal Docker, il te faut : un serveur Linux avec Docker Engine et le plugin Compose installés, un nom de domaine qui pointe vers ce serveur si tu veux du HTTPS automatique, et idéalement un volume dédié pour stocker la base et les fichiers.

Si Docker n'est pas encore présent sur ta machine :

```bash
curl -sSL https://get.docker.com | sh
```

Pour un premier test rapide, un simple `docker run` suffit :

```bash
mkdir -p ~/docuseal/data
sudo docker run -d --name docuseal \
  -p 3000:3000 \
  -v ~/docuseal/data:/data \
  docuseal/docuseal
```

Par défaut, DocuSeal Docker stocke tout dans une base SQLite logée dans `/data`. Ça marche très bien pour tester, mais en production je préfère basculer sur PostgreSQL pour avoir des sauvegardes propres et éviter les soucis de verrouillage sous charge. Récupère le fichier `docker-compose.yml` officiel :

```bash
curl https://raw.githubusercontent.com/docusealco/docuseal/master/docker-compose.yml > docker-compose.yml
```

Puis adapte-le pour pointer vers une base Postgres séparée :

```yaml
services:
  docuseal:
    image: docuseal/docuseal
    container_name: docuseal
    restart: unless-stopped
    ports:
      - "3000:3000"
    volumes:
      - ./data:/data
    environment:
      - DATABASE_URL=postgres://docuseal:motdepasse@postgres:5432/docuseal
    depends_on:
      - postgres

  postgres:
    image: postgres:16-alpine
    container_name: docuseal-postgres
    restart: unless-stopped
    environment:
      - POSTGRES_USER=docuseal
      - POSTGRES_PASSWORD=motdepasse
      - POSTGRES_DB=docuseal
    volumes:
      - ./pgdata:/var/lib/postgresql/data
```

Lance ensuite la stack. Si tu veux que DocuSeal Docker gère lui-même le certificat HTTPS via un domaine public, la variable `HOST` fait le travail :

```bash
sudo HOST=signature.tondomaine.com docker compose up -d
```

Le conteneur émet alors automatiquement un certificat TLS, à condition que le DNS pointe déjà vers ton serveur et que le port 443 soit ouvert. Si tu préfères garder la main sur le TLS, saute cette variable et mets DocuSeal Docker derrière ton reverse proxy habituel, en l'exposant uniquement sur le réseau Docker interne.

## Premiers pas : compte admin, template et envoi d'une signature

Une fois le conteneur démarré, ouvre l'URL configurée dans ton navigateur. Le premier écran te demande de créer le compte administrateur : email, mot de passe, et le nom de ton organisation. Ce compte a tous les droits, donc active une authentification forte derrière lui dès que possible.

Depuis le tableau de bord, la logique est simple :

1. Clique sur **Nouveau modèle**, upload ton PDF (contrat, devis, décharge)
2. Glisse les champs sur le document : signature, date, texte libre, case à cocher
3. Attribue chaque champ à un rôle signataire si plusieurs personnes doivent intervenir
4. Enregistre le modèle, puis clique sur **Envoyer** en renseignant l'email du ou des signataires

Le signataire reçoit un lien, pas de compte à créer de son côté. Il signe depuis son navigateur, sur mobile comme sur desktop, et toi tu reçois une notification avec le PDF final scellé et un certificat d'audit listant les horodatages, adresses IP et actions effectuées. Pratique pour prouver qu'un document n'a pas été signé sous la contrainte d'un simple copier-coller d'image.

## Passer DocuSeal Docker en production

Une fois le fonctionnement validé, quelques réglages séparent un labo d'une installation que tu peux montrer à un client.

⚠️ **Ne jamais exposer DocuSeal Docker directement sur internet sans TLS.** Les liens de signature contiennent des jetons d'accès : en clair, n'importe qui qui intercepte le trafic peut signer à la place du destinataire.

Côté sauvegarde, deux éléments à couvrir : le volume `/data` qui contient les PDF et les fichiers temporaires, et la base PostgreSQL si tu l'as mise en place. Un simple dump planifié suffit pour commencer :

```bash
docker exec docuseal-postgres pg_dump -U docuseal docuseal > backup-docuseal.sql
```

Pour les mises à jour, la routine classique :

```bash
docker compose pull
docker compose up -d
```

✅ Teste toujours la mise à jour sur une copie de la base avant de l'appliquer en prod, surtout si tu es resté plusieurs mois sans mettre à jour l'image : les migrations de schéma peuvent s'accumuler.

Si tu gères plusieurs stacks Compose sur le même serveur, je te recommande de piloter tout ça depuis une interface plutôt qu'en SSH permanent. Mon guide sur [Dockge](/dockge-docker-gestionnaire-stacks-compose/) explique comment éditer et redémarrer tes fichiers `docker-compose.yml` depuis le navigateur, DocuSeal compris.

## DocuSeal Docker dans ton stack homelab

DocuSeal Docker ne vit pas tout seul, il s'intègre naturellement avec ce que tu as probablement déjà en place.

Pour le suivi en temps réel du conteneur sans taper `docker logs -f` à répétition dès qu'un envoi de signature échoue, j'utilise [Dozzle](/dozzle-docker-visionneuse-logs-web/) : une visionneuse de logs web qui liste tous tes conteneurs, DocuSeal Docker inclus, avec recherche en direct. Ça aide à comprendre pourquoi un email de notification n'est pas parti, souvent un souci de configuration SMTP.

Une fois les documents signés et exportés, deux options pour les ranger. Soit tu les archives automatiquement dans [Paperless-ngx](/paperless-ngx-docker-guide-auto-hebergement/), qui les indexe par OCR et te permet de les retrouver par mot-clé des années plus tard. Soit tu veux juste un accès rapide depuis n'importe quel appareil : [Filestash](/filestash-docker-navigateur-fichiers-web/) te donne un navigateur de fichiers web universel pour parcourir le dossier `/data` monté sur ton serveur.

La question qui revient souvent : faut-il connecter DocuSeal Docker à un SSO pour ne pas multiplier les comptes admin. En self-hosted gratuit, le SSO n'est pas inclus, il faudra passer sur le plan Pro ou se contenter d'un compte admin par organisation.

## Limites et points de vigilance

Avant de tout migrer vers DocuSeal Docker, quelques points à connaître.

La version open source n'inclut ni envoi en masse, ni rappels automatiques, ni SSO/SAML : ces fonctions restent derrière le plan Pro payant, que tu sois en cloud ou en self-hosted. Pour une utilisation perso ou une petite équipe qui envoie quelques documents par semaine, ça ne manque pas. Pour une agence qui envoie des centaines de contrats par mois, le calcul économique penche vite vers le Pro.

La licence AGPLv3 mérite aussi réflexion si tu comptes un jour exposer DocuSeal comme un service à des clients externes : la clause copyleft réseau peut t'obliger à republier le code modifié. Pour un usage interne, ça ne te concerne pas.

Enfin, l'envoi d'email dépend entièrement de ta propre configuration SMTP. Pas de serveur mail fiable configuré, pas de notification de signature qui arrive, et tes signataires restent bloqués sur un lien qu'ils n'ont jamais reçu.

## Conclusion

DocuSeal Docker coche la case que je cherchais depuis un moment : signer des documents proprement sans payer un abonnement mensuel pour trois signatures par trimestre. L'installation via Docker Compose prend un quart d'heure, la base PostgreSQL encaisse la charge d'une petite structure, et le certificat d'audit généré à chaque signature tient la route face à un client qui demande des garanties.

Si ton usage reste perso ou pour une petite équipe, la version open source suffit largement. Lance le conteneur, branche-le à ton reverse proxy, et le prochain devis que tu envoies se signera sans quitter ton propre serveur.
