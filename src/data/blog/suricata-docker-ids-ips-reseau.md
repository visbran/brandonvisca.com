---
title: "Suricata Docker : IDS/IPS open-source pour sécuriser ton réseau"
description: "Suricata Docker, c'est un IDS/IPS open-source pour détecter les intrusions sur ton réseau, en écoute ou en blocage, sans y passer ta nuit."
pubDatetime: "2026-10-04T11:01:12+02:00"
modDatetime: "2026-10-03T08:00:00.000Z"
author: Brandon
tags:
  - securite
  - docker
  - hardening
  - intermediaire
featured: false
draft: false
focusKeyword: suricata docker
faqs:
  - question: "Suricata consomme combien de RAM sur un petit serveur ?"
    answer: "Ça dépend surtout du débit à analyser et du nombre de règles chargées. Surveille l'usage réel avec docker stats pendant quelques jours avant de tirer des conclusions."
  - question: "Suricata peut-il remplacer mon pare-feu ?"
    answer: "Non. Suricata analyse le contenu du trafic et alerte, il ne filtre pas les ports comme nftables ou UFW. Les deux se complètent : le pare-feu ferme les portes, Suricata surveille ce qui passe quand même."
  - question: "Pourquoi mon conteneur Suricata ne remonte aucune alerte ?"
    answer: "Vérifie d'abord que l'interface passée avec -i est celle qui porte réellement le trafic, puis que les règles sont chargées. Un conteneur en réseau bridge ne voit que son propre trafic, d'où le choix du mode host."
---
> 💡 **TL;DR**
> - Suricata Docker te donne un IDS/IPS open-source qui analyse le trafic de ton réseau et signale les comportements suspects
> - Lancé avec `--net=host` et deux capabilités réseau, il écoute ton interface sans toucher à tes autres conteneurs
> - Commence en IDS (alertes seulement), garde les règles à jour, et ne passe en IPS (blocage) qu'une fois tes faux positifs réglés

## Suricata Docker : un œil sur tout ce qui passe

Ton pare-feu filtre les ports. Parfait. Mais il ne sait pas si le paquet qui arrive sur le port 443 transporte une requête piégée, un scan de vulnérabilités ou un shell inversé déguisé en trafic web. Ce boulot revient à un IDS, et Suricata le fait très bien.

Suricata est un moteur de détection d'intrusion open-source, développé par l'OISF. Il lit le trafic, le décode protocole par protocole (HTTP, DNS, TLS, SSH, et d'autres), puis compare chaque flux à des règles. Quand une règle matche, il génère une alerte. Il peut aussi bloquer le paquet, si tu le lui demandes.

Pour un homelab, le plus propre reste le conteneur : rien à installer sur l'hôte, et tu supprimes tout en une commande. C'est l'approche de cet article. Suricata Docker répond à un besoin simple : voir ce qui se passe sur ton réseau sans transformer ton hôte en laboratoire.

Ça tombe bien, c'est aussi ce qui rend l'outil intéressant en autohébergement. Un seul conteneur, une seule interface à surveiller, et des logs que tu peux lire avec les outils que tu utilises déjà.

## Table des matières

## IDS ou IPS : la différence qui compte

IDS, pour Intrusion Detection System : il observe le trafic et te prévient. IPS, pour Intrusion Prevention System : il se place sur le chemin des paquets et peut les bloquer. Le moteur est le même, seul le mode de fonctionnement change.

Le piège classique, avec Suricata Docker comme avec n'importe quel IPS, c'est de passer directement en blocage. Une règle un peu trop large et tu coupes ton accès SSH ou ton reverse proxy sans comprendre pourquoi. En IDS, tu observes, tu ajustes, tu te trompes sans rien casser.

Et Snort, dans tout ça ? C'est l'autre gros nom du genre. Suricata accepte la plupart des règles écrites pour Snort, donc la bascule est simple si tu as déjà un jeu de règles. Côté architecture, Suricata a été pensé multi-thread dès le départ, et il sort ses événements en JSON (fichier eve.json) directement exploitable. Snort 3 a comblé une partie de l'écart. Choisis selon ce que tu sais déjà lire et maintenir, pas selon une guerre de chapelles.

## Lancer Suricata en Docker

Lancer Suricata Docker ne demande pas grand-chose, mais la commande compte, et chaque option a une raison. L'image de référence s'appelle `jasonish/suricata`. Elle est disponible en amd64 et en arm64. Vérifie les tags sur Docker Hub avant de figer une version : `latest` suit les mises à jour, un tag précis te donne de la stabilité.

Crée d'abord le dossier de logs, sinon Docker le créera en root :

```bash
mkdir -p logs
```

Puis lance le conteneur en mode écoute :

```bash
docker run --name=suricata --rm -it --net=host \
    --cap-add=net_admin --cap-add=net_raw --cap-add=sys_nice \
    -v $(pwd)/logs:/var/log/suricata \
    jasonish/suricata:latest -i eth0
```

Trois options comptent vraiment, et c'est là que la plupart des tutoriels vont trop vite. `--net=host` permet à Suricata de voir les interfaces de l'hôte. `net_admin` et `net_raw` lui donnent le droit d'ouvrir la capture de paquets. Sans elles, il n'arrive pas à capturer et tu n'as aucun message clair pour te guider. Remplace `eth0` par l'interface qui porte ton trafic : `ip -br a` te la liste en une seconde.

Reste une question avant de lancer : où placer le capteur ? Le bon endroit est celui où passe le trafic que tu veux voir. Sur un hôte unique qui héberge tes services exposés, l'interface principale suffit largement, et c'est ce qui couvre le plus de cas. Si tu veux surveiller les échanges entre conteneurs, il faut une interface de bridge dédiée, ce qui dépasse le cadre de cet article. Ne cherche pas la couverture parfaite dès le premier jour : commence petit, avec ce qui entre et sort, et étends ensuite si le besoin se confirme.

## Mode IDS : écouter sans bloquer

Dans un second terminal, suis les alertes en direct :

```bash
tail -f logs/eve.json | grep '"event_type":"alert"'
```

Avec Suricata Docker en écoute, chaque ligne de `eve.json` est un événement JSON. Les alertes portent le type `alert`, mais Suricata peut aussi journaliser les requêtes DNS, HTTP ou TLS si tu actives ces sorties dans `suricata.yaml`. Utile pour comprendre un événement après coup.

Au début, tu vas voir défiler du bruit : scans venus d'Internet, bots, tentatives de connexion. C'est normal, tout ce qui est exposé se fait scanner en permanence. L'objectif n'est pas de chasser chaque scan, mais de repérer les alertes qui concernent tes propres machines et les flux qui ne devraient pas exister.

### Comprendre une règle

Une règle Suricata a une structure fixe. Voici une règle de test, à mettre dans un fichier de règles locales référencé dans la section `rule-files` de `suricata.yaml` :

```
alert http any any -> $HOME_NET any (msg:"Test accès /admin"; flow:to_server; content:"/admin"; http.uri; sid:1000001; rev:1;)
```

Lue à voix haute : « alerte sur tout trafic HTTP venant de n'importe où, allant vers ton réseau interne, qui contient `/admin` dans l'URI ». Le `msg` est le texte qui apparaît dans l'alerte, le `sid` est l'identifiant unique (les règles locales commencent à 1000000 pour ne pas entrer en collision avec les jeux officiels), et `rev` est la révision.

Pour vérifier que la chaîne fonctionne, fais une requête HTTP vers un service de ton réseau avec `/admin` dans l'URL. L'alerte doit apparaître dans `eve.json` dans la seconde. Si rien ne vient, le problème est presque toujours l'interface ou le réseau, pas la règle.

## Passer en IPS : bloquer, avec précaution

⚠️ Le mode IPS peut couper ton réseau. Ne le fais pas sans avoir testé en IDS d'abord.

En IPS, le trafic doit passer par une file netfilter (NFQUEUE) : Suricata reçoit chaque paquet, décide, puis l'accepte ou le rejette. Côté hôte, il faut donc des règles iptables ou nftables qui redirigent le trafic vers cette file. Je ne te donne pas la commande ici : la syntaxe change selon que tu utilises nftables ou iptables, et une erreur coupe l'accès à la machine. La section IPS de la documentation officielle de Suricata détaille le cas à cas.

Côté règles, le mot-clé `drop` ne produit aucun effet en mode IDS : Suricata se contente de journaliser. Il n'agit qu'en IPS.

Mon conseil : une semaine en IDS. Tu listes les alertes récurrentes sur tes machines, tu désactives les faux positifs dans `disable.conf` de suricata-update, et seulement ensuite tu bascules sur `drop` pour les règles qui le méritent vraiment.

## Garder les règles à jour

Sans règles à jour, Suricata Docker ressemble à une alarme sans capteurs. Les menaces changent chaque semaine, et une règle écrite il y a un an ne reconnaît pas les attaques d'aujourd'hui. Le script `suricata-update` récupère les jeux de règles, par défaut ceux d'Emerging Threats en version ouverte. Dans le conteneur lancé plus haut, la mise à jour se fait depuis un second terminal :

```bash
docker exec -it --user suricata suricata suricata-update -f
docker exec suricata suricatasc -c reload-rules
```

La première commande télécharge les règles, la seconde demande à Suricata de les recharger sans redémarrer le conteneur. Mets ce duo dans une tâche cron quotidienne sur l'hôte, sinon tu finiras par oublier, et les règles vieillissent vite.

## Pièges fréquents

- **Mauvaise interface.** C'est le piège numéro un de Suricata Docker : le conteneur tourne, mais ne voit rien. Ton trafic passe peut-être par le bridge Docker ou par le Wi-Fi, pas par `eth0`. Vérifie avec `ip -br a` et avec le trafic réel.
- **Capabilités manquantes.** Sans `net_admin` et `net_raw`, la capture échoue. Relis la commande `docker run` avant de chercher ailleurs.
- **Réseau bridge.** Un conteneur en bridge ne voit que son propre trafic. Le mode host règle le problème, au prix d'une isolation réseau moindre pour ce conteneur.
- **Logs qui gonflent.** `eve.json` grossit vite si tu actives tous les types d'événements. Limite les sorties dans `suricata.yaml` et mets en place une rotation avec logrotate.
- **Attente d'une protection automatique.** Suricata détecte, il ne bannit pas. Pour réagir automatiquement aux IP qui scannent, regarde plutôt du côté de [Fail2Ban](/fail2ban-docker-securite-serveur/) ou de [CrowdSec](/crowdsec-docker-securite-collaborative/), qui agissent sur les logs ou les connexions.

## Conclusion

Suricata Docker est le moyen le plus simple de voir ce qui se passe sur ton réseau sans rien casser le premier jour. Commence en IDS, lis tes alertes pendant une semaine, règle les faux positifs, et ne bloque qu'ensuite.

Il ne remplace ni ton pare-feu ni ton filtrage de ports. Si [nftables](/nftables-docker-pare-feu-linux/) ou [UFW](/ufw-docker-pare-feu-linux/) gèrent déjà les portes, Suricata surveille ce qui passe par les fenêtres.
