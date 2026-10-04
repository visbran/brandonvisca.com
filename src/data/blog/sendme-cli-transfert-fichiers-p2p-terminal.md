---
title: "Sendme CLI : Transfert Fichiers P2P en 2 Commandes (Alternative scp Moderne)"
description: "Sendme CLI : transfert P2P sécurisé en 2 commandes. NAT traversal automatique, aucun serveur requis. Alternative moderne à scp. Guide complet 2026."
pubDatetime: "2025-12-09T21:14:00+01:00"
modDatetime: "2026-09-11T23:10:00+02:00"
author: Brandon Visca
tags:
  - homelab
  - linux
  - guide
  - intermediaire
featured: true
draft: false
focusKeyword: sendme
faqs:
  - question: "Comment envoyer un fichier avec Sendme ?"
    answer: "Lance sendme send suivi du fichier ou du dossier : Sendme affiche un ticket. Le destinataire lance sendme receive avec ce ticket, et le transfert se fait directement entre les deux machines."
  - question: "Faut-il connaître l'IP du destinataire ?"
    answer: "Non. Le ticket contient de quoi joindre l'expéditeur, et Sendme traverse le NAT automatiquement. Si la connexion directe échoue, le trafic passe par un relais Iroh, toujours chiffré."
  - question: "Pourquoi le ticket ne fonctionne-t-il plus ?"
    answer: "Les données restent sur la machine de l'expéditeur : si sendme send a été arrêté avant la fin de la réception, le ticket ne mène plus à rien. Il faut relancer l'envoi et transmettre le nouveau ticket."
  - question: "Existe-t-il une version graphique de Sendme ?"
    answer: "Oui, DashBeam (anciennement Alt-SendMe) repose sur la même technologie Iroh. Les tickets sont compatibles dans les deux sens entre DashBeam et Sendme CLI."
---
> 💡 **TL;DR**
> - Sendme CLI envoie des fichiers P2P en 2 commandes, sans IP, sans config SSH, sans serveur
> - NAT traversal automatique via la stack Iroh (QUIC + TLS 1.3 + Blake3) : ça marche même derrière un firewall d'entreprise
> - Compatible Linux, macOS, Windows, interopérable avec DashBeam, la version graphique (ex-Alt-SendMe)

Tu galères avec `scp` qui te demande des IP que tu ne connais pas ? Tu es obligé de passer par WeTransfer même pour un fichier de 10 Mo ? **Sendme CLI** va changer ça.

Juste deux commandes, et tes fichiers passent de machine à machine. Pas de config réseau, pas d'IP à retenir, pas de serveur à monter.

## Table des matières

---

## 🎯 C'est Quoi Sendme CLI ?

**Sendme CLI** envoie et reçoit des fichiers directement entre deux machines, sans intermédiaire. Sous le capot, la technologie **Iroh** (QUIC + TLS 1.3 + Blake3) s'occupe des connexions peer-to-peer sécurisées avec traversée NAT automatique.

**En une phrase :**  
C'est comme `scp`, mais sans avoir besoin de connaître l'IP de destination, de configurer SSH, ou de passer par un serveur intermédiaire.

### Qui développe Sendme CLI ?

Sendme est développé par **n0-computer**, l'équipe derrière la stack **Iroh** (une bibliothèque Rust pour construire des applications P2P modernes). C'est un projet open source disponible sur [GitHub](https://github.com/n0-computer/sendme).

### Pourquoi c'est différent de scp/rsync ?

|Critère|scp/rsync|WeTransfer|**Sendme CLI**|
|---|---|---|---|
|**Connexion directe**|✅ (si IP connue)|❌ (serveur central)|✅ (automatique)|
|**Traversée NAT**|❌ (port forwarding manuel)|✅|✅ (automatique)|
|**Chiffrement**|✅ (SSH)|✅ (HTTPS)|✅ (TLS 1.3)|
|**Reprise automatique**|⚠️ (avec rsync)|❌|✅|
|**Vérification intégrité**|❌|❌|✅ (Blake3)|
|**Config requise**|SSH + IP|Compte|**Aucune**|

---

## 🚀 Installation de Sendme CLI

### Option 1 : Script d'installation rapide (Linux/macOS)

⚠️ **Avant de piper curl dans bash** : inspecte le script sur [iroh.computer/sendme.sh](https://iroh.computer/sendme.sh) si tu es en prod. En homelab ou sur ta machine perso, tu peux y aller.

```bash
curl -fsSL https://iroh.computer/sendme.sh | bash
```

Ce script :

- Télécharge le binaire pour ton OS
- L'installe dans `~/.local/bin/`
- Ajoute le PATH automatiquement

**Vérifier l'installation :**

```bash
sendme --version
# Exemple : sendme 0.25.0
```

### Option 2 : PowerShell (Windows)

```powershell
irm https://iroh.computer/sendme.ps1 | iex
```

Le binaire sera copié dans le répertoire d'où tu lances le script.

**Lancer Sendme sur Windows :**

```powershell
.\sendme.exe --version
```

### Option 3 : Homebrew (macOS)

Si tu n'as pas encore [Homebrew installé sur ton Mac](/installation-homebrew-macos/), c'est le prérequis.

```bash
brew install sendme
```

### Option 4 : Cargo (pour les Rustacés)

```bash
cargo install sendme
```

---

## 📦 Utilisation de Base : Envoyer et Recevoir

### Envoyer un fichier

```bash
sendme send ~/Documents/rapport.pdf
```

**Résultat :**

```text
content added
run sendme receive blobQmXYZ...abc123
```

**Ce qui se passe :**

1. Sendme crée un "ticket" unique (hash du fichier + adresse de connexion)
2. Le fichier reste sur ta machine (pas d'upload vers un serveur)
3. Tu envoies ce ticket à ton destinataire (Slack, email, SMS...)

### Recevoir un fichier

```bash
sendme receive blobQmXYZ...abc123
```

**Résultat :**

```text
fetched to rapport.pdf
```

**Ce qui se passe :**

1. Sendme se connecte directement à l'expéditeur (NAT hole punching)
2. Télécharge le fichier en P2P avec vérification Blake3
3. Si la connexion coupe, la reprise est automatique

---

## 🔥 Cas d'Usage Avancés

### 1. Envoyer un dossier entier

```bash
sendme send ~/projets/site-web/
```

Sendme va :

- Envoyer tout le contenu du dossier, sous-dossiers compris, sans le compresser
- Générer un ticket unique
- Recréer le dossier à l'identique chez le destinataire

### 2. Envoyer plusieurs fichiers

`sendme send` prend **un seul chemin**. Pour envoyer plusieurs fichiers, regroupe-les dans un dossier et envoie le dossier :

```bash
mkdir a-envoyer && cp fichier1.zip fichier2.pdf a-envoyer/
sendme send a-envoyer/
```

### 3. Dans un script : attention, sendme send ne rend pas la main

`sendme send` reste au premier plan tant que le fichier est servi : les données ne quittent ta machine que pendant que la commande tourne. Il s'arrête avec Ctrl+C. Une ligne comme `sendme send fichier > ticket.txt` suivie d'autres commandes ne passera donc jamais à la suite. Pour un transfert automatisé et planifié, un outil qui rend la main, comme `rsync` sur SSH ou [Restic](/restic-docker-sauvegarde-moderne/) pour les sauvegardes, est plus adapté. Sendme brille pour les transferts ponctuels, quand quelqu'un attend le ticket de l'autre côté.

### 4. Pas de lecture sur l'entrée standard

Sendme envoie un fichier ou un dossier existant : il n'accepte pas `-` pour lire un flux sur l'entrée standard. Pour envoyer une archive générée à la volée, crée-la d'abord :

```bash
tar czf gros-dossier.tar.gz ~/gros-dossier/
sendme send gros-dossier.tar.gz
```

---

## 🛡️ Sécurité et Confidentialité

### Comment ça marche sous le capot ?

1. **Chiffrement** : TLS 1.3 (ChaCha20-Poly1305)
2. **Vérification** : Blake3 hash (plus rapide que SHA-256)
3. **NAT Traversal** : STUN + hole punching automatique
4. **Relay fallback** : Si P2P échoue, relay Iroh (données chiffrées)

**Important :**

- Aucun serveur ne voit le contenu de tes fichiers
- Les tickets contiennent : hash + adresse réseau (pas le fichier lui-même)
- Les relays Iroh ne stockent rien (passage en temps réel)

### Peut-on héberger son propre relay ?

Oui ! Iroh est open source, tu peux déployer ton propre serveur relay :

```bash
# Installer iroh relay
cargo install iroh-relay
```

Le lancement et la configuration du relais (certificat, ports) sont décrits dans la documentation d'iroh-relay.

Puis indique son adresse à Sendme, des deux côtés :

```bash
sendme send fichier.zip --relay https://mon-relay.example.com
```

L'option `--relay` accepte aussi `default` (les relais publics d'Iroh) et `disabled` (connexion directe uniquement).

---

## ⚡ Performances et Benchmarks

**Taille testée :** 4 GB (fichier vidéo)

|Métrique|Résultat|
|---|---|
|**Vitesse max**|4 Gbps (sature une connexion fibre)|
|**Latence initiale**|~2-3 secondes (connexion P2P)|
|**CPU usage**|~15% (streaming + chiffrement)|
|**Reprise après coupure**|✅ Automatique|

**Comparaison avec rsync :**

```bash
rsync -avz fichier.tar.gz user@1.2.3.4:/tmp/
# Nécessite : config SSH, IP publique, port forwarding

sendme send fichier.tar.gz
# Nécessite : rien
```

---

## 🔧 Dépannage et Erreurs Courantes

### Erreur : "Failed to connect"

**Cause :** NAT symétrique strict ou firewall bloquant.

**Solution :**

1. Vérifie que la machine peut sortir en HTTPS (port 443) : c'est par là que passent les relais.
2. Si ton réseau bloque les relais publics, utilise ton propre relais avec `--relay https://ton-relais` des deux côtés.

Il n'existe pas d'option pour forcer le passage par le relais : Sendme tente la connexion directe et bascule seul sur le relais si elle échoue.

### Fichiers temporaires `.sendme-*`

Pendant un transfert, Sendme crée un dossier temporaire `.sendme-send-…` ou `.sendme-recv-…` **dans le dossier courant**, puis le supprime à la fin. Lance donc la commande depuis un dossier où tu as les droits d'écriture et assez d'espace disque.

### Ticket expiré ou invalide

**Cause :** Le serveur source s'est arrêté avant que le destinataire ne récupère le fichier.

**Solution :** L'expéditeur doit relancer `sendme send` et générer un nouveau ticket.

---

## 🎨 La version graphique : DashBeam (ex-Alt-SendMe)

Si le terminal te fait peur, ou si tu dois envoyer un fichier à quelqu'un qui n'y touchera jamais, il existe une application de bureau bâtie sur la même stack Iroh : **DashBeam**, développée par tonyantony300.

> ⚠️ **Le projet s'appelait Alt-SendMe jusqu'à la version 0.6.2, sortie le 30 juillet 2026.** Depuis, binaires et dépôt portent le nom DashBeam. Si tu tombes sur un tutoriel qui te fait télécharger un fichier `AltSendme_*`, il date d'avant ce renommage. Le dépôt GitHub `tonyantony300/alt-sendme` redirige vers `tonyantony300/dashbeam`.

**Les deux outils sont interopérables** : un ticket généré par Sendme CLI s'ouvre dans DashBeam, et inversement. C'est la même techno dessous, seule l'enveloppe change.

### Installer DashBeam

La version courante est la **0.7.1** (1er septembre 2026). Récupère toujours la dernière sur la [page des releases GitHub](https://github.com/tonyantony300/dashbeam/releases), les noms de fichiers ci-dessous suivent le numéro de version.

**Windows** : l'installeur `DashBeam_0.7.1_x64-setup.exe`, ou le `.msi` si tu déploies en entreprise. Une version portable `DashBeam_0.7.1_x64-portable.zip` existe si tu ne veux rien installer.

**macOS** : le `DashBeam_0.7.1_universal.dmg` couvre Intel et Apple Silicon. Gatekeeper bloque souvent l'app à la première ouverture :

```bash
cd /Applications
xattr -dr com.apple.quarantine DashBeam.app
```

**Linux** : un `.deb`, un `.rpm` et une AppImage universelle :

```bash
# Debian / Ubuntu
wget https://github.com/tonyantony300/dashbeam/releases/download/v0.7.1/DashBeam_0.7.1_amd64.deb
sudo dpkg -i DashBeam_0.7.1_amd64.deb

# AppImage, n'importe quelle distro
wget https://github.com/tonyantony300/dashbeam/releases/download/v0.7.1/DashBeam_0.7.1_amd64.AppImage
chmod +x DashBeam_0.7.1_amd64.AppImage
./DashBeam_0.7.1_amd64.AppImage
```

**Android** : un APK universel est fourni dans les releases, hors Play Store.

> 💡 Chaque binaire est accompagné d'un fichier `.sig`. En environnement sensible, vérifie la signature plutôt que de faire confiance à un exécutable téléchargé.

### Envoyer depuis l'interface

1. Glisse-dépose ton fichier ou ton dossier dans DashBeam
2. L'app génère un ticket
3. Tu transmets ce ticket par le canal que tu veux (chat, SMS, email)
4. Le destinataire le colle dans son DashBeam, ou lance `sendme receive <ticket>`
5. Laisse l'app ouverte jusqu'à la fin du transfert

### Cas d'usage recommandés

|Situation|Outil recommandé|
|---|---|
|Transfert ponctuel depuis un terminal ou par SSH|**Sendme CLI**|
|Envoyer à un non-technicien|**DashBeam**|
|Serveur sans interface graphique|**Sendme CLI**|
|Usage ponctuel sur laptop|**DashBeam**|
|Intégration dans homelab|**Sendme CLI**|

---

## 🧩 Intégration avec Docker et Homelab

### Exemple : Transférer des images Docker

**Problème :** Tu veux envoyer une image Docker custom à un collègue.

**Solution classique (nulle) :**

```bash
docker save mon-image:latest | gzip > image.tar.gz
# Uploader sur Google Drive, WeTransfer...
```

**Solution avec Sendme :**

```bash
docker save mon-image:latest | gzip > image.tar.gz
sendme send image.tar.gz
# Copie le ticket, envoie-le sur Slack

# Destinataire :
sendme receive blobQmXYZ...
gunzip -c image.tar.gz | docker load
```

📌 **Ressource utile :** [Guide Docker Compose production sécurisé](/docker-debutant-services-auto-heberger/) pour structurer ton homelab proprement.

---

## 🌍 Alternatives à Sendme CLI

|Outil|Type|Avantages|Inconvénients|
|---|---|---|---|
|**scp/rsync**|CLI|Standard, fiable|Config SSH, IP requise|
|**Magic Wormhole**|CLI|Simple|Pas de reprise automatique|
|**Croc**|CLI|Chiffrement|Moins performant (pas QUIC)|
|**WeTransfer**|Web|Interface simple|Serveur central, limites|
|**LocalSend**|GUI|LAN uniquement|Pas d'Internet|

**Pourquoi Sendme CLI gagne :**

- Traversée NAT automatique (fonctionne via Internet)
- Performances QUIC (plus rapide que TCP)
- Vérification intégrité Blake3
- Reprise automatique
- Zéro config

---

💡 À lire aussi : [Homepage Docker : dashboard homelab personnalisable avec widgets](/homepage-docker-dashboard-homelab-widgets/), dans la même veine que cet article.

## 🎯 Conclusion : Sendme CLI, Le scp du Futur

**Sendme CLI** résout un vrai problème : transférer des fichiers rapidement en ligne de commande sans se prendre la tête avec des configs réseau ou des serveurs intermédiaires.

Sendme CLI devrait être installé par défaut sur toutes les machines Linux/macOS. C'est tellement plus simple que `scp` pour les transferts ponctuels, et tellement plus rapide que passer par WeTransfer ou un serveur FTP.

**Prochaine étape :**  
Si tu gères un homelab, garde Sendme CLI pour les transferts ponctuels entre machines, et un outil comme Restic pour les sauvegardes planifiées. Si tu bosses en équipe, remplace le "on s'envoie ça sur Google Drive" par un simple ticket Sendme. Et si le terminal te fait peur, DashBeam te donne la même puissance avec une interface graphique.

---

