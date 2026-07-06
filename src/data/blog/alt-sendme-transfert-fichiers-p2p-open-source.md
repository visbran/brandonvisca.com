---
title: "Alt-SendMe : L'Arme Secrète pour Partager des Fichiers Sans Espionnage (Guide 2026)"
description: "Alt-SendMe transfert fichiers en P2P : alternative gratuite à WeTransfer, chiffrement de bout en bout, aucune limite de taille. Guide complet 2026."
pubDatetime: "2026-07-06T00:00:00+01:00"
author: Brandon Visca
tags:
  - homelab
  - linux
  - macos
  - intermediaire
  - guide
featured: false
draft: false
focusKeyword: alt-sendme
faqs:
  - question: "Quelle est la différence entre Alt-SendMe et Sendme CLI ?"
    answer: "Alt-SendMe est une application desktop avec interface graphique, développée par tonyantony300. Sendme CLI est l'outil en ligne de commande officiel développé par l'équipe Iroh. Les deux utilisent la même technologie et sont interopérables : un ticket généré par l'un fonctionne avec l'autre."
  - question: "Alt-SendMe est-il vraiment gratuit ?"
    answer: "Oui, le projet est open source sous licence AGPL-3.0, sans compte à créer ni frais cachés. Les serveurs relay publics (utilisés en secours si la connexion directe échoue) sont fournis gratuitement par le projet Iroh."
  - question: "Puis-je l'utiliser commercialement ?"
    answer: "Oui, la licence AGPL-3.0 autorise l'usage commercial. Si tu modifies le code et le redistribues, tu dois partager tes modifications sous la même licence (copyleft)."
  - question: "Quelle est la taille maximale d'un fichier transférable ?"
    answer: "Aucune limite logicielle. La seule contrainte est l'espace disque du destinataire et ta bande passante disponible."
  - question: "Puis-je héberger mon propre serveur relay ?"
    answer: "Oui. Le dépôt GitHub fournit les fichiers de déploiement (Docker Compose) pour un relay auto-hébergé, configurable ensuite dans Settings puis Network de l'application."
  - question: "Que faire si mon pare-feu bloque la connexion ?"
    answer: "Alt-SendMe utilise QUIC, qui repose sur UDP. Certains pare-feux d'entreprise ou réseaux publics stricts bloquent ce trafic. Un VPN (WireGuard par exemple) contourne généralement ce blocage."
---
> 💡 **TL;DR**
> - Alt-SendMe transfère des fichiers en P2P direct entre deux machines, sans serveur cloud intermédiaire
> - Chiffrement de bout en bout (QUIC + TLS 1.3), aucune limite de taille, pas de compte à créer
> - Interface graphique Windows/macOS/Linux/Android, interopérable avec Sendme CLI en ligne de commande

Tu dois envoyer un fichier volumineux et tu hésites entre WeTransfer qui bride tout, Google Drive qui indexe tes données, ou un truc en ligne de commande qui te fait fuir ? **Alt-SendMe** règle ce dilemme avec une interface graphique simple, posée sur la même techno P2P que Sendme CLI.

## Table des matières

## Alt-SendMe vs Sendme CLI : quelle différence ?

Il existe deux outils distincts mais parfaitement compatibles, tous deux basés sur **Iroh**, la stack P2P développée par l'équipe iroh.computer :

**Sendme CLI**, par l'équipe Iroh elle-même : outil en ligne de commande, pensé pour les scripts et l'automatisation. J'en ai fait [un guide dédié](https://brandonvisca.com/sendme-cli-transfert-fichiers-p2p-terminal/) si le terminal ne te fait pas peur.

**Alt-SendMe**, par le développeur indépendant tonyantony300 : application desktop avec interface graphique, pensée pour l'usage quotidien sans taper une seule commande.

Les deux utilisent la même technologie sous le capot et sont **100% interopérables** : un ticket généré par Alt-SendMe fonctionne dans Sendme CLI, et inversement.

**Lequel choisir ?**

- **Alt-SendMe** si tu veux une interface visuelle, pour un usage ponctuel ou si tu débutes
- **Sendme CLI** si tu veux automatiser ou intégrer ça dans des scripts et du cron
- **Les deux** si tu es un power user : GUI pour l'occasionnel, CLI pour les tâches répétitives

## Le problème que tu connais déjà

Un fichier volumineux à envoyer, et les options classiques déçoivent toutes à leur manière.

**Email** : 25 Mo de limite chez Gmail, 50 Mo chez Outlook. Compression obligatoire, galère assurée pour tout ce qui dépasse une poignée de photos.

**WeTransfer** : le forfait gratuit plafonne à 2 Go, les fichiers passent par leurs serveurs, le lien expire au bout de quelques jours même si le destinataire ne l'a pas encore ouvert.

**Google Drive ou OneDrive** : un compte requis des deux côtés, indexation par l'hébergeur, vitesse bridée sans abonnement payant.

**LocalSend** : très bien en réseau local, mais ça ne fonctionne pas sur internet (NAT, firewall).

Alt-SendMe couvre ce que ces solutions ne font pas en même temps : rapidité, confidentialité, taille illimitée, simplicité.

## Le concept en 30 secondes

Imagine AirDrop, mais qui marche entre n'importe quelle plateforme et sur internet, pas seulement en réseau local.

1. Tu glisses-déposes un fichier dans Alt-SendMe
2. L'app génère un ticket, un code unique
3. Tu envoies ce ticket à ton destinataire (chat, SMS, email)
4. Il colle le ticket dans son Alt-SendMe
5. Transfert direct entre vos deux machines

Pas d'intermédiaire qui stocke tes données, pas de limite de taille imposée par un forfait.

## Comment Alt-SendMe connecte deux machines

### NAT hole punching et relay de secours

Les deux machines se déclarent d'abord auprès d'un relay public pour traverser NAT et firewalls. Une fois le contact établi, Alt-SendMe tente une connexion directe QUIC entre les deux appareils, plus rapide et sans intermédiaire.

Si la connexion directe échoue (firewall d'entreprise trop restrictif par exemple), le transfert continue via le relay, mais reste chiffré de bout en bout : le relay ne voit que des paquets chiffrés, jamais le contenu.

### Chiffrement et vérification d'intégrité

Tout le trafic passe en **QUIC** (le protocole derrière HTTP/3) avec chiffrement **TLS 1.3**. Chaque bloc de données est vérifié par un hash **BLAKE3** : si un bit est corrompu en route, Alt-SendMe le détecte et retélécharge automatiquement le morceau concerné, sans relancer tout le transfert.

## Installation

La dernière version au moment de cet article est la **v0.4.2**. Récupère toujours la version courante sur la [page des releases GitHub](https://github.com/tonyantony300/alt-sendme/releases).

> 💡 **Astuce** : chaque release GitHub fournit un fichier `.sig` à côté du binaire. Si tu es en environnement sensible, vérifie la signature avant d'installer plutôt que de faire confiance aveuglément à un exécutable téléchargé.

### Windows

Télécharge l'installeur `.exe` (ou `.msi`) depuis les releases, lance-le, suis l'assistant. Une version Scoop existe aussi :

```bash
scoop bucket add extras
scoop install extras/altsendme
```

### macOS

Télécharge le `.dmg` universel, glisse Alt-SendMe dans `/Applications`. macOS bloque souvent l'app à la première ouverture (Gatekeeper, app non notarisée) :

```bash
cd /Applications
xattr -dr com.apple.quarantine AltSendme.app
```

### Linux

Le paquet `.deb` est fourni officiellement, une AppImage universelle existe aussi :

```bash
# Debian/Ubuntu
wget https://github.com/tonyantony300/alt-sendme/releases/download/v0.4.2/AltSendme_0.4.2_amd64.deb
sudo dpkg -i AltSendme_0.4.2_amd64.deb

# AppImage (n'importe quelle distro)
wget https://github.com/tonyantony300/alt-sendme/releases/download/v0.4.2/AltSendme_0.4.2_amd64.AppImage
chmod +x AltSendme_0.4.2_amd64.AppImage
./AltSendme_0.4.2_amd64.AppImage
```

### Android

Un APK universel est disponible directement dans les releases GitHub, hors Play Store.

## Envoyer et recevoir un fichier

**Envoyer, en GUI :**

1. Lance Alt-SendMe
2. Glisse-dépose ton fichier ou dossier
3. Clique sur le bouton de partage
4. Copie le ticket généré
5. Envoie ce ticket à ton destinataire par le canal de ton choix
6. Garde l'app ouverte tant que le transfert n'est pas terminé

**Recevoir :** ton destinataire colle simplement le ticket dans son Alt-SendMe, le transfert démarre automatiquement.

**En ligne de commande, avec Sendme CLI** (interopérable) :

```bash
# Installer Sendme CLI (développé par Iroh)
curl -fsSL https://iroh.computer/sendme.sh | bash

# Envoyer
sendme send mon-fichier.zip
# → Génère un ticket, à coller dans Alt-SendMe GUI ou à passer à sendme receive
```

## Performances réelles

Le projet publie ses propres statistiques d'usage agrégées, à prendre comme ordre de grandeur plutôt que promesse contractuelle : plus gros transfert enregistré 452 Go, transfert rapide le plus volumineux 54 Go à 123 Mo/s (environ 1 Gbps), transfert massif 328 Go à 93 Mo/s, pic de vitesse mesuré 125 Mo/s. Le débit réel dépend toujours de ta machine, ton réseau et le chemin de connexion entre les deux appareils.

## Sécurité et confidentialité

**Chiffré :** contenu des fichiers, noms de fichiers, métadonnées de transfert (TLS 1.3 de bout en bout).

**Visible pour un tiers réseau :** les adresses IP des deux machines et le volume de données transférées, comme pour n'importe quelle connexion internet classique.

**Jamais stocké :** pas de compte donc pas de logs utilisateur, pas de serveur cloud donc pas de copie de tes fichiers. Le relay, quand il sert de secours, ne conserve rien.

## Alt-SendMe face au reste

| Critère | Alt-SendMe | WeTransfer | Google Drive | LocalSend | SCP/SFTP |
|---|---|---|---|---|---|
| **Limite de taille** | Aucune | 2 Go (gratuit) | Selon forfait | Aucune | Aucune |
| **Compte requis** | Non | Non (envoi) | Oui | Non | Compte serveur |
| **Stockage cloud intermédiaire** | Non | Oui (7 jours) | Oui (permanent) | Non | Non |
| **Chiffrement bout en bout** | Oui (TLS 1.3) | En transit | En transit | Non (LAN) | Oui (SSH) |
| **Marche sur internet (pas juste LAN)** | Oui | Oui | Oui | Non | Oui |
| **Interface** | GUI + CLI (via Sendme) | Web | Web | GUI | CLI |
| **Open source** | Oui (AGPL-3.0) | Non | Non | Oui (MIT) | Oui |

## Cas d'usage réels

**Freelance vers client :** un dossier de rushes vidéo de plusieurs dizaines de Go part directement, sans upload préalable vers un cloud. Le client reçoit le ticket par email, colle-le dans son Alt-SendMe.

**Sysadmin, backup vers un VPS distant :** [sécurise ton VPS](https://brandonvisca.com/securite-de-votre-serveur-linux/) et utilise-le comme relais temporaire. Une session `screen` sur le VPS avec Sendme CLI, un transfert lancé, tu peux fermer ta session SSH sans interrompre le transfert.

**Partage de médiathèque entre deux homelabs** (par exemple deux installs [Jellyfin](https://brandonvisca.com/jellyfin-docker-alternative-netflix-gratuite/)) : plus simple que de monter un accès distant, le fichier part directement d'une machine à l'autre.

**Artefacts Docker entre collègues** : `docker save mon-image:latest | gzip | sendme send -`, le ticket circule sur Slack, l'autre récupère avec `sendme receive` puis `docker load`. Complémentaire à un vrai registre pour du ponctuel, pas un remplacement pour de la prod (regarde plutôt du côté d'un [guide Docker pour homelab](https://brandonvisca.com/docker-debutant-services-auto-heberger/) si tu montes une infra plus permanente comme [Nextcloud](https://brandonvisca.com/nextcloud-docker-installation-complete-2025/)).

## Limitations

**La machine émettrice doit rester allumée** pendant tout le transfert. C'est du P2P, pas un stockage cloud intermédiaire : tant que le fichier n'est pas intégralement reçu, ta machine doit être disponible. Le contournement classique : un VPS avec Sendme CLI dans une session `screen` ou un `cron`, qui reste allumé à ta place.

> ⚠️ **Attention** : si tu fermes l'application avant la fin du transfert, la connexion coupe net et ton destinataire doit attendre que tu relances un partage avec un nouveau ticket.

**Interface volontairement minimaliste** : pas d'historique de transferts avancé ni de gestion de file d'attente. Le projet mise sur la simplicité plutôt que sur les fonctionnalités superflues.

## Dépannage

**« Connection refused » ou connexion qui échoue**

Vérifie que ton pare-feu autorise le trafic UDP sortant et entrant (QUIC). Sur un firewall Linux restrictif, ouvre le port utilisé par ton installation plutôt que de tout désactiver en aveugle.

**Vitesse anormalement lente malgré une bonne connexion**

Dans les logs de l'application, vérifie si le transfert passe en connexion directe ou par le relay de secours. Un relay implique un chemin réseau plus long, donc plus lent, mais reste chiffré de bout en bout.

**Ticket invalide ou expiré**

L'expéditeur a probablement fermé Alt-SendMe avant que le destinataire ne récupère le fichier. Relance le partage, ça génère un nouveau ticket.

## Conclusion

Alt-SendMe comble un vrai vide : une interface graphique simple posée sur une techno P2P sérieuse, sans les compromis habituels du cloud grand public. Pas de compte, pas de limite de taille imposée, chiffrement de bout en bout par défaut.

Si tu gères un homelab et que tu échanges régulièrement de gros fichiers avec d'autres machines ou d'autres personnes, installe-le en parallèle de ton stockage permanent habituel. Pour de l'automatisation ou de l'intégration script, bascule sur Sendme CLI en ligne de commande, les tickets restent compatibles dans les deux sens.

## Pour aller plus loin

- [Sendme CLI : transfert P2P en ligne de commande](https://brandonvisca.com/sendme-cli-transfert-fichiers-p2p-terminal/)
- [Sécuriser son serveur Linux](https://brandonvisca.com/securite-de-votre-serveur-linux/)
- [Docker pour débutants : les services à auto-héberger absolument](https://brandonvisca.com/docker-debutant-services-auto-heberger/)
- [Documentation Iroh](https://iroh.computer/docs)
- [GitHub Alt-SendMe](https://github.com/tonyantony300/alt-sendme)
