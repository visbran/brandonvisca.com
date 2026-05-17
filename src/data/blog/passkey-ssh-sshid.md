---
title: "Passkey SSH : remplace tes clés avec SSH ID (2026)"
description: "Passe au passkey SSH biométrique avec SSH ID de Termius : Face ID, Touch ID, Windows Hello. La clé privée reste sur ton appareil, inextractible."
pubDatetime: 2026-05-06 00:00:00+01:00
author: Brandon Visca
tags:
  - securite
  - linux
  - ssh
  - hardening
  - intermediaire
  - guide
featured: false
draft: false
focusKeyword: passkey ssh
faqs:
  - question: "SSH ID fonctionne-t-il sans Termius côté serveur ?"
    answer: "Oui. Les clés publiques SSH ID sont standards et s'ajoutent dans ~/.ssh/authorized_keys comme n'importe quelle clé. Seule la création et gestion des clés côté client nécessite Termius."
  - question: "Mes clés privées sont-elles stockées dans le cloud ?"
    answer: "Non. SSH ID garantit que la clé privée reste dans le Secure Enclave de ton appareil — inextractible et non synchronisable. Même Termius n'y a pas accès."
  - question: "SSH ID est-il gratuit ?"
    answer: "La création de clés SSH ID est accessible via Termius. L'offre de base de Termius est gratuite. Vérifie les plans actuels sur termius.com pour les fonctionnalités avancées."
---
> 💡 **TL;DR** — Ce qu'il faut retenir :
> - SSH ID de Termius te permet d'utiliser un passkey biométrique (Face ID, Touch ID, Windows Hello) à la place de tes clés SSH classiques
> - La clé privée reste dans le Secure Enclave de ton appareil — inextractible, non exportable, non synchronisable
> - Provisionner un nouveau serveur se résume à une seule commande `curl`

## Table des matières

T'as déjà perdu ta clé privée SSH ? Ou pire, tu l'as uploadée par erreur dans un dépôt public ? Bienvenue dans le club. La gestion des clés SSH, c'est un enfer discret : fichiers `.pem` éparpillés sur trois machines, passphrases oubliées, accès à un client passé par mail "provisoirement", et qui tourne encore deux ans après.

SSH ID ([sshid.io](https://sshid.io/)), l'outil de Termius, attaque ce problème différemment. Le principe : un passkey SSH biométrique à la place de tes fichiers `.pem`. Tu relies ton authentification SSH à ton biométrique, la clé privée ne quitte jamais ton appareil. Et provisionner un nouveau serveur prend 30 secondes chrono.

J'ai testé SSH ID pendant plusieurs semaines sur mon homelab (Proxmox, 6 VMs Debian). Voici ce que ça donne vraiment.

## Le problème avec les clés SSH classiques

La méthode classique : `ssh-keygen`, tu copies ta clé publique sur le serveur, tu gardes la privée quelque part sur ton disque. Simple en théorie.

En pratique, c'est le bazar. Tu as 3 machines → 3 fichiers `.pem` différents (ou le même copié-collé partout, ce qui est encore pire). Tu passes un accès à un client → tu lui envoies une clé par mail ou Signal. Tu changes de laptop → migration à la main et inévitablement un accès qu'on oublie de révoquer. Tu perds la clé privée → accès perdu, ou backup stocké dans un endroit douteux.

Et les mots de passe SSH sur un serveur exposé, n'en parlons pas. C'est du brute force en attente.

> ⚠️ **Attention** : Si tu utilises encore l'authentification par mot de passe SSH sur un serveur exposé, commence par [durcir ton serveur Linux](/securite-de-votre-serveur-linux/) avant de continuer ici. C'est urgent.

## Comment fonctionne un passkey SSH

Un passkey SSH, c'est une paire de clés cryptographiques dont la clé privée est générée et stockée dans le **Secure Enclave** de ton appareil (la puce hardware dédiée à la cryptographie, présente dans tous les Mac récents, iPhones, et les PC Windows avec TPM 2.0).

Ce qui change par rapport à une clé classique :

- La clé privée **ne peut jamais quitter la puce**. Pas d'export, pas de copie, pas de backup, pas de sync cloud.
- Pour signer une authentification SSH, ton OS déclenche une vérification biométrique (Face ID, Touch ID ou Windows Hello).
- La clé publique, elle, est entièrement diffusable. C'est son rôle.

SSH ID utilise le standard **FIDO2** pour implémenter ce passkey SSH. Algorithmes supportés : `ECDSA-SK` et `ED25519-SK` (les variantes FIDO, les plus sécurisées), plus `ECDSA` et `RSA` classiques pour les systèmes legacy.

> 💡 **Astuce** : Les algorithmes `-SK` font signer l'authentification directement dans le hardware, pas dans le process SSH. Préfère-les si ton serveur tourne OpenSSH ≥ 8.2 (Debian 11+, Ubuntu 20.04+, etc.).

Côté serveur, rien à installer. Les clés publiques SSH ID sont compatibles `~/.ssh/authorized_keys` standards. Zéro plugin, zéro daemon, zéro dépendance.

## Créer ton handle SSH ID et générer tes clés

Tu as besoin de [Termius](https://termius.com/) (gratuit, disponible Windows, macOS, Linux, iOS, Android). Si tu veux remplacer PuTTY en même temps, j'ai fait [un guide complet Termius pour Windows](/termius-client-ssh-windows-guide-complet/).

**Étape 1 : ton handle**

Sur [sshid.io](https://sshid.io/), crée ton compte et choisis un handle public (quelque chose comme `@ton-pseudo`). C'est l'identifiant que tu vas partager avec tes serveurs.

**Étape 2 : générer la clé**

Dans Termius, cherche la section SSH Keys dans les paramètres, puis génère une nouvelle clé SSH ID. Termius déclenche une vérification biométrique. La paire est générée à la volée : la privée va dans le Secure Enclave, la publique s'associe à ton handle.

**Étape 3 : vérifier tes clés publiques**

Depuis n'importe quel terminal :

```bash
curl https://sshid.io/@ton-handle.keys
```

Tu vois toutes tes clés publiques actives. C'est exactement ce que tes serveurs vont utiliser.

## Provisionner un serveur en 30 secondes

C'est là que le passkey SSH change vraiment la donne. Au lieu de copier-coller une clé manuellement, tu fais ça sur le serveur :

```bash
curl https://sshid.io/@ton-handle.keys >> ~/.ssh/authorized_keys
```

Toutes tes clés publiques sont désormais autorisées. Une seule ligne, aucune erreur de copier-coller possible.

Pour automatiser avec **Ansible** :

```yaml
- name: Autoriser les clés SSH ID
  authorized_key:
    user: "{{ ansible_user }}"
    key: "{{ lookup('url', 'https://sshid.io/@ton-handle.keys') }}"
    state: present
```

Ça marche pareil avec Puppet, JumpCloud ou n'importe quel outil de provisioning qui accepte une URL comme source de clé autorisée.

> ✅ **Bonne pratique** : Crée un handle différent par contexte (perso, pro, clients). Si tu révokes ou perds un handle, tu n'impactes que les serveurs liés à ce contexte précis.

## Partager un accès sans envoyer une clé privée

Le cas classique : un client te demande un accès temporaire, ou tu dois déléguer à un prestataire. Avec la méthode classique, tu te retrouves à envoyer une clé privée quelque part. Ou pire, un mot de passe par messagerie.

Avec SSH ID, c'est propre :

1. La personne crée son SSH ID handle
2. Tu ajoutes ses clés sur le serveur : `curl https://sshid.io/@son-handle.keys >> ~/.ssh/authorized_keys`
3. Quand c'est terminé → tu supprimes sa ligne dans `authorized_keys` ou tu utilises un outil de gestion d'accès

Pas de clé privée qui traîne, pas de [mot de passe à partager de façon sécurisée](/partager-mot-de-passe-securise-comparatif/), juste un handle public auditable.

## Les limites à connaître avant de foncer

SSH ID, c'est du vrai progrès. Mais y a des trucs à savoir avant de migrer.

**Dépendance à Termius**. La création et gestion des clés passe obligatoirement par l'app Termius. Si Termius change de modèle ou ferme, tu dois migrer. Côté serveur : aucun lock-in, tes clés publiques restent dans `authorized_keys` comme d'habitude.

**Clé liée à l'appareil**. Un passkey SSH est lié au hardware qui l'a créé. Si tu perds ou changes de laptop sans préparation, la clé privée est perdue (par design). Il faut générer une nouvelle paire et re-provisionner tes serveurs. Pas de récupération possible, c'est le prix de l'inextractabilité.

**Systèmes anciens**. OpenSSH < 8.2 ne supporte pas les algorithmes FIDO (`-SK`). SSH ID génère du ECDSA/RSA classique pour ces cas, mais sans le bénéfice hardware. Ça reste meilleur que de gérer des fichiers `.pem` manuellement.

**CI/CD avec clés partagées**. Si ton pipeline déploie avec une clé SSH partagée stockée dans les secrets GitHub/GitLab, SSH ID ne convient pas : le Secure Enclave ne partage pas, c'est sa définition même. Pour ce cas d'usage, garde une clé de service classique.

## Conclusion

SSH ID ne réinvente pas SSH. Il réinvente la façon de gérer les clés. Et c'est exactement ce dont on avait besoin.

Si t'en as assez de jongler avec des fichiers `.pem`, de gérer des accès temporaires à la main ou de provisionner tes serveurs un par un, le passkey SSH est une solution concrète et sans friction. La biométrie en entrée, `authorized_keys` standard en sortie. Rien à installer côté serveur, rien à apprendre côté protocole.

Mon setup actuel : Termius + SSH ID sur Mac, provisioning `curl` sur mes 6 VMs Proxmox. Ça tourne depuis plusieurs semaines sans accroc.

## Pour aller plus loin

- [Termius 2026 : remplace PuTTY et économise 30 min/jour sur Windows](/termius-client-ssh-windows-guide-complet/)
- [Sécurité de ton serveur Linux : durcir avec les bonnes pratiques](/securite-de-votre-serveur-linux/)
- [Partager un mot de passe en toute sécurité : comparatif des outils](/partager-mot-de-passe-securise-comparatif/)

## Articles connexes

- [Sécurité de votre serveur linux : Comment durcir un serveur sous linux ?](/securite-de-votre-serveur-linux/)
- [Sendme CLI : Transfert Fichiers P2P en 2 Commandes (Alternative scp Moderne)](/sendme-cli-transfert-fichiers-p2p-terminal/)
- [Content-Security-Policy : Protéger votre site sans bloquer vos utilisateurs](/content-security-policy-nginx-sans-casser-site/)
- [Exchange Online : bloquer les transferts email automatiques avec PowerShell (2026)](/exchange-online-bloquer-transferts-automatiques-emails/)
