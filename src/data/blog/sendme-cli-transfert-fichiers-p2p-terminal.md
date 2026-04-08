---
title: "Sendme CLI : Transfert Fichiers P2P en 2 Commandes (Alternative scp Moderne)"
description: "Sendme CLI : l'outil qui transforme le transfert de fichiers en ligne de commande. P2P sécurisé, NAT traversal automatique, aucun serveur. Guide complet 2025."
pubDatetime: "2025-12-09T21:14:00+01:00"
author: Brandon Visca
tags:
  - homelab
  - iroh
  - ligne de commande
  - linux
  - macos
  - p2p
  - transfert fichiers
featured: true
draft: false
focusKeyword: sendme cli
---
## TL:DR;

Tu galères avec `scp` qui te demande des IP que tu ne connais pas ? Tu es obligé de passer par WeTransfer même pour un fichier de 10 Mo ? **Sendme CLI** va devenir ton meilleur ami.

Cet outil développé par l'équipe **Iroh** (n0-computer) transforme le transfert de fichiers en ligne de commande en quelque chose d'aussi simple qu'un copier-coller. Pas de config réseau, pas d'IP à retenir, pas de serveur à monter. Juste deux commandes, et hop, tes fichiers passent de machine à machine.

Spoiler : ça marche même derrière un NAT strict ou un firewall d'entreprise.

## Table of content

---

## 🎯 C'est Quoi Sendme CLI ?

**Sendme CLI** est un outil en ligne de commande qui permet d'envoyer et recevoir des fichiers directement entre deux machines, sans intermédiaire. Il utilise la technologie **Iroh** (QUIC + TLS 1.3 + Blake3) pour créer des connexions peer-to-peer sécurisées avec traversée NAT automatique.

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

```
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

```
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

- Compresser le dossier automatiquement
- Générer un ticket unique
- Le recevoir décompressera tout proprement

### 2. Envoyer plusieurs fichiers

```bash
sendme send fichier1.zip fichier2.pdf dossier/
```

### 3. Automation avec Scripts

**Exemple : Backup automatique vers une machine distante**

```bash
#!/bin/bash
# backup-to-server.sh

TICKET_FILE="/tmp/sendme-ticket.txt"

# Machine A : Créer backup et générer ticket
sendme send ~/backups/db-$(date +%Y%m%d).tar.gz > "$TICKET_FILE"

# Envoyer ticket à machine B (via SSH, webhook, etc.)
cat "$TICKET_FILE" | ssh user@machine-b "sendme receive \$(cat)"
```

### 4. Intégration CI/CD

**Exemple : Transférer artifacts de build**

```yaml
# .gitlab-ci.yml
deploy:
  script:
    - sendme send dist/ > ticket.txt
    - curl -X POST https://webhook.example.com/deploy \
           -d "ticket=$(cat ticket.txt)"
```

### 5. Streaming de données en temps réel

Sendme peut streamer des données :

```bash
# Machine A : Stream
tar czf - ~/gros-dossier/ | sendme send -

# Machine B : Recevoir et décompresser à la volée
sendme receive blobQmXYZ... | tar xzf -
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

# Lancer le relay
iroh-relay --bind-addr 0.0.0.0:3478
```

Puis configurer Sendme pour l'utiliser :

```bash
sendme send fichier.zip --relay https://mon-relay.example.com
```

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

```
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

1. Vérifier que le relay Iroh est accessible :
    
    ```bash
    curl https://relay.iroh.network/health
    ```
    
2. Forcer l'utilisation du relay :
    
    ```bash
    sendme send fichier.zip --force-relay
    ```
    

### Erreur : "Permission denied"

**Cause :** Sendme stocke temporairement les données dans `~/.cache/sendme/`

**Solution :**

```bash
mkdir -p ~/.cache/sendme
chmod 700 ~/.cache/sendme
```

### Ticket expiré ou invalide

**Cause :** Le serveur source s'est arrêté avant que le destinataire ne récupère le fichier.

**Solution :** L'expéditeur doit relancer `sendme send` et générer un nouveau ticket.

---

## 🎨 Sendme CLI vs Alt-SendMe GUI : Lequel Choisir ?

**Tu préfères le terminal ?** → **Sendme CLI** (cet article)

**Tu préfères les interfaces graphiques ?** → [**Alt-SendMe**](https://brandonvisca.com/alt-sendme-transfert-fichiers-p2p-open-source/) (interface desktop)

**Bonne nouvelle :** Les deux sont **interopérables** ! Un ticket généré par Sendme CLI fonctionne dans Alt-SendMe GUI et vice-versa.

### Cas d'usage recommandés

|Situation|Outil recommandé|
|---|---|
|Automation, scripts, CI/CD|**Sendme CLI**|
|Envoyer à un non-technicien|**Alt-SendMe GUI**|
|Serveur sans interface graphique|**Sendme CLI**|
|Usage ponctuel sur laptop|**Alt-SendMe GUI**|
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
docker save mon-image:latest | gzip | sendme send -
# Copie le ticket, envoie-le sur Slack

# Destinataire :
sendme receive blobQmXYZ... | gunzip | docker load
```

### Exemple : Backup homelab

Tu veux sauvegarder tes configs Docker Compose vers une machine externe ? Sendme CLI s'intègre parfaitement dans tes scripts d'automatisation.

```bash
#!/bin/bash
# backup-homelab.sh

tar czf - /opt/docker-configs/ | sendme send - > /tmp/ticket.txt
curl -X POST https://ntfy.sh/homelab-backup \
     -d "Backup ready: $(cat /tmp/ticket.txt)"
```

📌 **Ressource utile :** [Guide Docker Compose production sécurisé](https://brandonvisca.com/docker-debutant-services-auto-heberger/) pour structurer ton homelab proprement.

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

## 📚 Pour Aller Plus Loin

### Articles liés sur brandonvisca.com

1. **[Alt-SendMe : Interface graphique pour Iroh](https://brandonvisca.com/alt-sendme-transfert-fichiers-p2p-open-source/)**  
    Si tu préfères une GUI desktop, Alt-SendMe utilise la même technologie Iroh.
    
2. **[Auto-hébergement : Guide complet 2025](https://brandonvisca.com/auto-hebergement-guide-complet-2025/)**  
    Sendme CLI s'intègre parfaitement dans un setup homelab pour les backups.
    
3. **[Indépendance numérique : Le guide ultime](https://brandonvisca.com/independance-numerique-2025-guide-complet/)**  
    Sendme CLI fait partie des outils pour se passer de WeTransfer et Google Drive.
    
4. **[Docker pour les nuls : 10 services essentiels](https://brandonvisca.com/docker-debutant-services-auto-heberger/)**  
    Utilise Sendme CLI pour transférer des images Docker entre machines.
    

### Ressources officielles

- **Documentation Iroh** : [iroh.computer/docs](https://iroh.computer/docs)
- **GitHub Sendme** : [github.com/n0-computer/sendme](https://github.com/n0-computer/sendme)
- **Discord Iroh** : Communauté active pour support technique

---

## 🎯 Conclusion : Sendme CLI, Le scp du Futur

**Sendme CLI** résout un vrai problème : transférer des fichiers rapidement en ligne de commande sans se prendre la tête avec des configs réseau ou des serveurs intermédiaires.

**Ce qu'on retient :**

- ✅ Installation en une commande
- ✅ Transfert P2P automatique (même derrière NAT)
- ✅ Chiffrement TLS 1.3 et vérification Blake3
- ✅ Reprise automatique et streaming
- ✅ Compatible avec Alt-SendMe GUI

**Mon avis perso :**  
Sendme CLI devrait être installé par défaut sur toutes les machines Linux/macOS. C'est tellement plus simple que `scp` pour les transferts ponctuels, et tellement plus rapide que passer par WeTransfer ou un serveur FTP.

**Prochaine étape :**  
Si tu gères un homelab, intègre Sendme CLI dans tes scripts de backup. Si tu bosses en équipe, remplace vos pratiques "on s'envoie ça sur Google Drive" par un simple ticket Sendme.

Et si le terminal te fait peur, essaye [Alt-SendMe](https://brandonvisca.com/alt-sendme-transfert-fichiers-p2p-open-source/) pour avoir la même puissance avec une interface graphique.
