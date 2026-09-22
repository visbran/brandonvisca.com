---
title: "Wazuh Docker : SIEM open source pour surveiller ton homelab"
description: "Wazuh Docker : installe ce SIEM open source sur ton homelab, détecte les intrusions, centralise les logs et compare-le à Suricata."
pubDatetime: "2026-09-13T11:01:11+02:00"
modDatetime: "2026-09-12T08:00:00.000Z"
author: Brandon
tags:
  - securite
  - docker
  - hardening
  - monitoring
  - guide
  - intermediaire
featured: false
draft: false
focusKeyword: wazuh docker
faqs:
  - question: "Wazuh Docker consomme combien de RAM sur un homelab ?"
    answer: "Compte au moins 8 Go de RAM pour le host et 4 coeurs CPU en single-node. L'indexeur (basé sur OpenSearch) est le composant le plus gourmand, surtout si tu gardes plusieurs mois d'historique d'événements."
  - question: "Wazuh peut-il remplacer Fail2Ban ou CrowdSec ?"
    answer: "Non, pas vraiment. Wazuh centralise et corrèle des événements de sécurité venus de partout, alors que Fail2Ban et CrowdSec bannissent des IPs en local. Les trois cohabitent très bien sur la même infra."
  - question: "Faut-il installer un agent Wazuh sur chaque machine du homelab ?"
    answer: "Oui si tu veux du monitoring endpoint complet (intégrité de fichiers, logs applicatifs, vulnérabilités). Sans agent, le manager ne voit que ce qui lui arrive par syslog, ce qui limite fortement la détection."
---
> 💡 **TL;DR**
> - Wazuh est un SIEM open source qui centralise les logs de tout ton homelab, détecte les intrusions et corrèle les événements en un seul dashboard
> - En Docker, ça se déploie en un `git clone` + génération de certificats + `docker compose up`, mais compte 8 Go de RAM et 4 coeurs pour que ça tourne sereinement
> - Ce n'est pas un remplaçant de Fail2Ban ou CrowdSec, c'est la couche de visibilité au-dessus, celle qui te dit ce qui s'est vraiment passé quand une alerte tombe

## Wazuh Docker : le SIEM open source qui te dit ce qui se passe sur ton réseau

Tu as un pare-feu, un reverse proxy, peut-être déjà Fail2Ban ou CrowdSec qui bannissent des IPs. Mais est-ce que tu sais vraiment ce qui se passe sur ton homelab quand tu dors ? Qui a tenté de se connecter en SSH, quel fichier système a été modifié cette nuit, quel conteneur tourne avec une CVE connue ?

C'est exactement le trou que **Wazuh** vient combler. Ce n'est pas un outil de blocage de plus. C'est un SIEM, un Security Information and Event Management, qui centralise tous les événements de sécurité de ton infra dans un seul endroit et te donne enfin une vue d'ensemble. Chez moi, c'est devenu le premier truc que j'ouvre le matin, avant même mon dashboard Grafana.

Dans ce guide, on installe Wazuh Docker de zéro, on comprend son architecture, on compare avec Suricata, et surtout on évite les pièges classiques (mot de passe par défaut, ports exposés) qui transforment ton SIEM en surface d'attaque supplémentaire.

## Table des matières

## Wazuh, c'est quoi exactement

Wazuh, c'est l'éditeur Wazuh, Inc. qui le développe, positionné comme une plateforme XDR et SIEM unifiée. Le projet est open source, sans coût de licence, et c'est justement ce qui le distingue des gros SIEM commerciaux type Splunk ou QRadar dont la facture explose avec le volume de logs ingérés.

L'architecture repose sur quatre briques qui communiquent entre elles :

- **Les agents** : de petits binaires installés sur chaque machine surveillée (serveur Linux, poste Windows, conteneur). Ils remontent logs, changements de fichiers et infos système.
- **Le manager** : le cerveau. Il reçoit les données des agents, applique des règles de détection, génère des alertes et décide de leur gravité.
- **L'indexeur** : basé sur OpenSearch, il stocke et indexe tous les événements pour que tu puisses les chercher rapidement, même des mois plus tard.
- **Le dashboard** : l'interface web, une déclinaison d'OpenSearch Dashboards, où tu visualises alertes, tendances et conformité.

Quand on parle de Wazuh Docker, on parle du même produit, simplement empaqueté en conteneurs plutôt qu'installé nativement sur un serveur dédié.

Concrètement, chaque agent installé sur une VM ou un LXC de ton homelab envoie ses événements au manager. Le manager les corrèle avec ses règles (des milliers, préchargées), et si un pattern d'attaque matche, une alerte remonte dans le dashboard avec un niveau de sévérité. Tu peux aussi faire tourner Wazuh sans agent sur certaines sources, en syslog pur, mais tu perds une bonne partie de la valeur du produit : le monitoring d'intégrité de fichiers et la détection de rootkits nécessitent l'agent.

## Wazuh vs Suricata : pas le même métier

C'est une confusion fréquente. Suricata est un IDS/IPS réseau : il inspecte le trafic qui passe sur ton réseau, paquet par paquet, et détecte des signatures d'attaques au niveau réseau (exploits connus, scans, exfiltration). Wazuh, lui, ne regarde pas le trafic réseau par défaut. Il regarde ce qui se passe **sur** les machines : logs d'authentification, intégrité de fichiers, configuration système, vulnérabilités installées.

| Critère | Suricata | Wazuh |
|---|---|---|
| Portée | Trafic réseau (paquets) | Endpoints (logs, fichiers, config) |
| Déploiement | Sur le lien réseau ou en miroir de port | Agent sur chaque machine + manager central |
| Détection | Signatures réseau, anomalies de trafic | Corrélation de logs, FIM, conformité, CVE |
| Complémentarité | Peut envoyer ses alertes vers Wazuh | Peut ingérer les logs Suricata comme source |

La bonne nouvelle, c'est que les deux se marient très bien. Suricata peut écrire ses alertes en JSON (eve.json), et un agent Wazuh peut lire ce fichier pour intégrer les détections réseau dans le même dashboard que le reste. Tu obtiens une vision réseau ET système au même endroit, sans dupliquer les outils de visualisation. Si ton homelab tourne déjà avec un pare-feu comme [UFW](/ufw-docker-pare-feu-linux/), Wazuh vient documenter ce que ce pare-feu bloque ou laisse passer, avec l'historique et la corrélation en plus.

## Installer Wazuh Docker avec Docker Compose

Avant de lancer ta stack Wazuh Docker, vérifie que ton host a de la marge. Le déploiement single-node officiel recommande au moins 4 coeurs et 8 Go de RAM, plus une cinquantaine de Go de stockage libre pour l'indexeur. Sur un Raspberry Pi ou une petite VM à 2 Go, ça ne décollera pas correctement, l'indexeur OpenSearch est gourmand.

Clone le dépôt officiel et place-toi dans le dossier single-node :

```bash
git clone https://github.com/wazuh/wazuh-docker.git -b v4.14.7
cd wazuh-docker/single-node/
```

Génère ensuite les certificats auto-signés nécessaires à la communication interne entre indexeur, manager et dashboard :

```bash
docker compose -f generate-indexer-certs.yml run --rm generator
```

Les certificats atterrissent dans `config/wazuh_indexer_ssl_certs/`. Si tu préfères tes propres certificats (une CA interne par exemple), tu peux les déposer dans ce dossier avec les noms attendus avant de lancer le stack.

Lance ensuite le tout en arrière-plan :

```bash
docker compose up -d
```

Laisse tourner une bonne minute, le temps que l'indexeur finisse son initialisation. Suis les logs si tu veux voir la progression :

```bash
docker compose logs -f wazuh.indexer
```

Une fois que ça s'est stabilisé, voici les ports que le stack expose et que tu dois connaître avant de toucher à ton pare-feu :

| Port | Usage |
|---|---|
| 443 | Dashboard web (HTTPS) |
| 1514/tcp, 1515/tcp | Communication agents |
| 514/udp | Réception syslog |
| 55000 | API du manager |
| 9200 | API de l'indexeur |

Ouvre `https://IP_DE_TON_SERVEUR` dans ton navigateur. Les identifiants par défaut sont `admin` / `SecretPassword`. Change-les immédiatement, on y revient juste après, c'est le piège numéro un de ce genre de stack. Une install Wazuh Docker avec les identifiants par défaut ouverte sur internet, c'est une invitation.

## Premiers pas avec Wazuh Docker en pratique

Une fois connecté, la toute première chose à faire, avant même d'ajouter un agent, c'est de changer le mot de passe admin et celui des comptes internes de l'indexeur (`kibanaserver`, `logstash`, etc. selon la version). Un SIEM avec des identifiants par défaut, c'est le comble de l'ironie.

Pour surveiller une machine, installe l'agent Wazuh dessus (paquet `.deb`, `.rpm` ou binaire selon la distro) et enregistre-le auprès du manager. Une fois l'agent actif, tu commences à voir remonter des événements concrets :

**Brute-force SSH.** Les tentatives de connexion échouées sur SSH déclenchent une règle Wazuh dès les premiers essais répétés, avec l'IP source, l'utilisateur ciblé et le nombre de tentatives. Si tu as déjà [Fail2Ban](/fail2ban-docker-securite-serveur/) ou [CrowdSec](/crowdsec-docker-securite-collaborative/) qui bannissent ces IPs, Wazuh te donne le contexte complet de l'attaque après coup, pas juste la ligne de log brute.

**Intégrité de fichiers (FIM).** Wazuh surveille en continu des répertoires sensibles (`/etc`, `/bin`, tes fichiers de config Docker) et alerte au moindre changement inattendu. C'est précieux pour détecter une modification silencieuse après compromission, le genre de truc qu'un simple `grep` dans les logs ne verra jamais.

**Détection de vulnérabilités.** Le module vulnerability detector compare les paquets installés sur tes agents avec des bases de CVE connues. Tu sais en un coup d'oeil quelle machine tourne avec une version d'OpenSSL vulnérable et qu'il faut patcher en urgence.

**Conformité et audit système.** Des modules type SCA (Security Configuration Assessment) vérifient que tes machines respectent des baselines de durcissement (CIS Benchmarks notamment), et te listent précisément ce qui cloche.

## Sécuriser ton install Wazuh Docker

Un SIEM mal exposé devient lui-même une cible de choix, il centralise justement toutes les données sensibles de ton infra. Quelques règles à respecter absolument :

⚠️ **Ne jamais exposer le dashboard directement sur internet sans authentification renforcée.** Passe par un reverse proxy avec une couche 2FA devant. Si tu utilises déjà [Authelia](/authelia-docker-authentification-2fa-homelab/) pour centraliser tes authentifications, mets-le devant le port 443 de Wazuh plutôt que de faire confiance au seul login/mot de passe intégré.

⚠️ **Restreindre les ports 1514/1515 et 55000 au réseau interne.** Seuls tes agents et toi-même avez besoin d'y accéder. Un pare-feu comme [UFW](/ufw-docker-pare-feu-linux/) devant ton host Docker limite ces ports au réseau local ou à un VPN, jamais à 0.0.0.0 ouvert sur internet.

✅ **Changer tous les mots de passe par défaut dès le premier démarrage**, y compris ceux des comptes internes de l'indexeur, pas seulement `admin`.

✅ **Sauvegarder le dossier `config/` et les volumes de données régulièrement.** Perdre l'historique d'un SIEM au mauvais moment (juste après un incident) est particulièrement douloureux pour l'investigation post-mortem.

## Limites et alternatives : CrowdSec, Fail2Ban

Wazuh Docker a un coût réel en ressources et en complexité de maintenance. L'indexeur OpenSearch demande de la RAM, les mises à jour majeures (la 5.0 était encore en beta au moment où j'écris ces lignes) demandent de la vigilance, et la courbe d'apprentissage pour écrire ses propres règles de détection n'est pas nulle. Sur un homelab avec deux ou trois services, c'est probablement disproportionné.

C'est là que la distinction avec CrowdSec et Fail2Ban devient importante. Ces deux outils bannissent des IPs en quasi temps réel à partir de logs locaux, avec un coût en ressources minime. Wazuh, lui, ne bannit rien par défaut : il observe, corrèle et alerte, sur l'ensemble de ton infra, avec un historique long. Les trois ne jouent pas dans la même catégorie et se complètent très bien : CrowdSec ou Fail2Ban en première ligne pour réagir vite, Wazuh en arrière-plan pour comprendre ce qui s'est réellement passé et détecter les signaux faibles qu'un simple bannissement d'IP ne verra jamais.

Si ton homelab tient sur une ou deux machines avec peu de surface d'attaque, commence par [CrowdSec](/crowdsec-docker-securite-collaborative/) ou [Fail2Ban](/fail2ban-docker-securite-serveur/), c'est plus léger et suffisant. Wazuh Docker devient pertinent à partir du moment où tu gères plusieurs serveurs, plusieurs conteneurs exposés, et que tu veux une vraie traçabilité en cas d'incident.

💡 À lire aussi : [Trivy Docker : scanner de vulnérabilités pour images et conteneurs](/trivy-docker-scanner-vulnerabilites/), dans la même veine que cet article.

## Conclusion

Wazuh Docker n'est pas le premier outil de sécurité à installer sur un homelab, mais c'est probablement le plus formateur. Une fois que tu vois défiler dans le dashboard les tentatives de brute-force, les changements de fichiers et les CVE de tes propres machines, tu comprends des choses sur ton infra que tu ignorais totalement avant.

Compte une aprem pour l'installation propre et la sécurisation initiale, et une bonne semaine pour affiner les règles et éviter le bruit des faux positifs. Le jeu en vaut la chandelle : un SIEM open source et gratuit qui rivalise avec des solutions commerciales à plusieurs milliers d'euros par an, ça ne se refuse pas. Ce guide Wazuh Docker t'a donné la base, à toi de l'adapter à ton infra et à tes propres règles de détection.
