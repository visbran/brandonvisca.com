#!/usr/bin/env python3
"""Injects faqs frontmatter into blog articles."""

import re
import os

BLOG_DIR = "src/data/blog"

FAQS = {
    "warp-terminal-2025-iterm2-killer-ou-simple-hype-test-complet-ia.md": [
        {"question": "Warp remplace-t-il iTerm2 ?", "answer": "Warp est une excellente alternative à iTerm2 avec des features IA avancées, mais tu peux garder iTerm2 pour SSH prod et scripts automatisés."},
        {"question": "Est-ce que mes données sont envoyées à OpenAI/Anthropic ?", "answer": "Warp utilise un mix de modèles (OpenAI, Anthropic Claude, Google Gemini), mais tu contrôles ce qui est envoyé via les paramètres de confidentialité."},
        {"question": "Ça fonctionne offline ?", "answer": "L'Agent Mode requiert internet, mais le terminal fonctionne normalement sans connexion."},
        {"question": "Compatibilité avec Oh My Zsh ?", "answer": "Warp détecte automatiquement ta config Oh My Zsh et l'importe, aucune reconfiguration nécessaire."},
    ],
    "wailbrew-interface-graphique-homebrew.md": [
        {"question": "WailBrew est-il gratuit ?", "answer": "Oui, 100% gratuit sans version premium."},
        {"question": "WailBrew fonctionne-t-il sans Homebrew ?", "answer": "Non, WailBrew est juste une interface graphique pour Homebrew, qui doit déjà être installé."},
        {"question": "Puis-je utiliser WailBrew ET Homebrew CLI ?", "answer": "Oui, ils fonctionnent parfaitement ensemble. WailBrew pour l'usage quotidien, Terminal pour les cas avancés."},
        {"question": "WailBrew fonctionne-t-il sur Apple Silicon (M1/M2/M3) ?", "answer": "Oui, WailBrew est optimisé nativement pour Apple Silicon."},
    ],
    "shutter-encoder-mac-alternative-handbrake.md": [
        {"question": "Shutter Encoder est-il vraiment gratuit ?", "answer": "Oui, 100% gratuit et open-source. Le développeur accepte les donations mais l'app reste entièrement fonctionnelle sans payer."},
        {"question": "Shutter Encoder fonctionne-t-il sur M1/M2/M3 ?", "answer": "Oui, optimisé pour Apple Silicon avec hardware acceleration (VideoToolbox) et excellentes performances."},
        {"question": "Puis-je encoder en AV1 avec Shutter Encoder ?", "answer": "Oui, Shutter Encoder supporte AV1 via FFmpeg. Attention : très lent à encoder, mais compression maximale, idéal pour l'archivage."},
        {"question": "Quelle différence avec FFmpeg en ligne de commande ?", "answer": "Shutter Encoder est une interface graphique pour FFmpeg. Si tu maîtrises FFmpeg CLI, tu as plus de contrôle. Sinon, Shutter rend FFmpeg accessible."},
    ],
    "securite-de-votre-serveur-linux.md": [
        {"question": "Qu'est-ce que le durcissement d'un serveur sous Linux ?", "answer": "C'est l'ensemble des mesures de sécurité appliquées à un serveur pour minimiser les vulnérabilités : SSH durci, firewall, fail2ban, sysctl renforcés."},
        {"question": "Comment désactiver la connexion SSH en tant que root et modifier le port ?", "answer": "Édite /etc/ssh/sshd_config : définis PermitRootLogin no et change le port 22 par un numéro personnalisé."},
        {"question": "Comment limiter l'accès à su uniquement au groupe admin ?", "answer": "Crée un groupe admin et utilise dpkg-statoverride pour restreindre l'accès à /bin/su uniquement à ce groupe."},
        {"question": "Qu'est-ce que DenyHosts et Fail2Ban ?", "answer": "DenyHosts et Fail2Ban sont des outils qui analysent les logs et bannissent automatiquement les IPs des attaques SSH et autres tentatives malveillantes."},
    ],
    "quitter-google-auto-hebergement.md": [
        {"question": "C'est compliqué de quitter Google ?", "answer": "Non, si tu sais ce qu'est un fichier ZIP, tu peux le faire. Les commandes Linux sont des copier-coller, aucun code à écrire."},
        {"question": "C'est sécurisé d'auto-héberger ses données ?", "answer": "Plus que Google en fait. Tes données sont chez toi, pas dans un cloud scanné par des algos. Faut juste suivre les bonnes pratiques : firewall, backups, HTTPS."},
        {"question": "Et si ça tombe en panne ?", "answer": "Tu restaures un backup. Ça prend 30 minutes. Avec une bonne configuration, c'est rare."},
        {"question": "C'est légal d'auto-héberger ?", "answer": "100% légal. Héberger tes propres données est parfaitement légal. Streamer tes achats DVD sur Jellyfin est légal. Le piratage est illégal."},
    ],
    "notion-sites-creation-de-sites-web.md": [
        {"question": "Quelle est la différence principale entre Notion Sites et WordPress ?", "answer": "Notion Sites se distingue par sa simplicité sans compétences techniques avancées, tandis que WordPress demande une courbe d'apprentissage plus longue."},
        {"question": "Comment intégrer un domaine personnalisé à mon site Notion ?", "answer": "Tu peux associer ton domaine existant à ton site Notion depuis les paramètres Notion pour une présence web professionnelle."},
        {"question": "Notion Sites est-il adapté pour la création de blogs professionnels ?", "answer": "Oui, Notion Sites offre des fonctionnalités CMS robustes pour créer et gérer des blogs professionnels avec aisance."},
    ],
    "mise-a-jour-pfsense-2-8-nouveautes-installation.md": [
        {"question": "Quelles sont les nouveautés de pfSense 2.8 ?", "answer": "Mise à jour FreeBSD 14.0 avec meilleur support matériel, amélioration des performances réseau, nouvelles versions OpenVPN/IPsec/WireGuard, interface Web plus rapide."},
        {"question": "Comment mettre à jour pfSense vers la version 2.8 ?", "answer": "Sauvegarder la config, aller dans System > Update, vérifier la branche pfSense CE, cliquer sur Update et laisser redémarrer."},
        {"question": "La mise à jour vers pfSense 2.8 est-elle stable ?", "answer": "Oui, la 2.8 est stable pour usage en production. Largement testée et corrige des bugs des versions précédentes. Tester en labo avant production."},
        {"question": "Quels matériels sont compatibles avec pfSense 2.8 ?", "answer": "Support natif du matériel moderne (Intel, AMD 64 bits) grâce à FreeBSD 14. Compatible avec la plupart des cartes Intel NIC (i210, i350). Éviter les vieux chipsets Realtek/Broadcom."},
    ],
    "migration-wordpress-all-in-one-guide-2025.md": [
        {"question": "Combien de temps prend une migration WordPress ?", "answer": "Selon la taille du site, entre 30 minutes (petit site) et 2 heures (gros site avec base de données massive)."},
        {"question": "All-in-One WP Migration est-il gratuit ?", "answer": "La version 6.77 importe gratuitement. Les versions récentes ont retiré cette fonction et demandent une extension payante."},
        {"question": "Que faire si la migration échoue ?", "answer": "Vérifie les logs d'erreur, augmente les limites PHP (upload_max_filesize, memory_limit), ou utilise la migration manuelle par FTP."},
        {"question": "Faut-il sauvegarder avant migration ?", "answer": "Toujours. Crée une sauvegarde via phpMyAdmin ou le Dashboard WordPress avant de migrer. C'est ton filet de sécurité."},
    ],
    "masquer-utilisateurs-gal-office365-active-directory.md": [
        {"question": "Ma règle de synchronisation ne fonctionne pas !", "answer": "Vérifie que l'attribut msDS-cloudExtensionAttribute1 est bien configuré dans SSSD et que la formule IIF est correcte."},
        {"question": "L'utilisateur apparaît toujours dans la GAL", "answer": "Attends que la synchro Delta soit complète (peut prendre plusieurs minutes). Teste aussi avec un autre utilisateur pour vérifier."},
        {"question": "Je peux utiliser un autre attribut que msDS-cloudExtensionAttribute1 ?", "answer": "Oui, utilise msDS-cloudExtensionAttribute2 à 15, mais reste cohérent dans ta formule de synchronisation."},
        {"question": "Ça marche avec les groupes aussi ?", "answer": "Oui, la même logique s'applique aux groupes Distribution avec l'attribut msExchHideFromAddressLists."},
    ],
    "ldap-filtrage-utilisateurs-snipeit.md": [
        {"question": "Erreur ldap_search(): Search: Bad search filter", "answer": "La syntaxe du filtre LDAP est invalide. Vérifie les parenthèses, opérateurs (&, |, !), et attributs comme objectCategory, objectClass."},
        {"question": "Aucun utilisateur retourné après la synchronisation LDAP", "answer": "Le filtre est correct mais trop restrictif. Teste avec un filtre plus large d'abord : (&(objectCategory=person)(objectClass=user))"},
        {"question": "Certains utilisateurs sont exclus alors qu'ils ne devraient pas l'être", "answer": "Révise le filtre sur userAccountControl ou userPrincipalName. L'opérateur ! exclut, pas de demi-mesures."},
    ],
    "installer-localwp-wordpress-local.md": [
        {"question": "LocalWP est-il gratuit ?", "answer": "Oui, 100% gratuit sans version premium obligatoire ni limitations. Monétisé via intégrations avec hébergeurs."},
        {"question": "LocalWP fonctionne-t-il sur Windows/Mac/Linux ?", "answer": "Oui, compatible Windows 10/11 (64-bit), macOS 10.15+ (Intel/Apple Silicon), et Linux (Debian/Ubuntu)."},
        {"question": "Puis-je avoir plusieurs sites en parallèle ?", "answer": "Oui, autant que tu veux. Consommation ~200-300 Mo par site. La limite est la RAM de ton PC."},
        {"question": "Comment migrer de LocalWP vers un hébergeur ?", "answer": "Utilise All-in-One WP Migration : export depuis LocalWP → fichier .wpress → import sur l'hébergement."},
    ],
    "independance-numerique-2025-guide-complet.md": [
        {"question": "Faut-il des compétences en Linux pour l'indépendance numérique ?", "answer": "Non, ça aide mais ce n'est pas obligatoire. Chaque guide est pensé pour débutants. Tu apprendras au fur et à mesure."},
        {"question": "Ça coûte combien par mois ?", "answer": "Homelab physique : 0-30€/mois (électricité). VPS : 5-20€/mois. Combo : 15-25€/mois plus investissement initial matériel."},
        {"question": "C'est légal d'héberger ses propres services ?", "answer": "100% légal. Héberger ses données et streamer ses achats DVD légaux est parfaitement légal. Le piratage reste illégal."},
        {"question": "Mes données sont-elles vraiment plus en sécurité chez moi ?", "answer": "Plus qu'avec Google, oui. Tes données ne sortent pas de chez toi, à condition de suivre les bonnes pratiques : firewall, backups, HTTPS, mots de passe forts."},
    ],
    "docker-debutant-services-auto-heberger.md": [
        {"question": "Docker vs LXC vs VM, quelle différence ?", "answer": "Docker : conteneurs applicatifs ultra-légers. LXC : conteneurs système (mini-VMs). VM : machine virtuelle complète avec OS, très lourd."},
        {"question": "Mes conteneurs Docker utilisent beaucoup de RAM, c'est normal ?", "answer": "Docker alloue la RAM par conteneur. Solution : limiter la RAM par conteneur (mem_limit), utiliser des images alpine, ou fermer les services inutilisés."},
        {"question": "Puis-je faire tourner Docker sur un Raspberry Pi ?", "answer": "Oui. Beaucoup d'images disponibles en architecture ARM. Services lourds (Jellyfin avec transcodage) limités, mais Nextcloud/Vaultwarden tournent parfaitement."},
        {"question": "Comment migrer mes conteneurs Docker vers un autre serveur ?", "answer": "Arrêter les conteneurs (docker compose down), copier le dossier docker vers le nouveau serveur, relancer (docker compose up -d)."},
    ],
    "connecter-les-systemes-ubuntu-a-active-directory-en-utilisant-sssd.md": [
        {"question": "Comment dépanner les problèmes de SSSD ?", "answer": "Vérifie systemctl status sssd et journalctl -u sssd pour les erreurs. Les problèmes courants : DNS mal configuré, certificats Kerberos, ou permissions."},
        {"question": "Puis-je utiliser SSSD avec d'autres distributions Linux ?", "answer": "Oui, SSSD est compatible avec Debian, RedHat, CentOS. Les commandes d'installation diffèrent légèrement."},
        {"question": "Comment assurer la création des répertoires personnels pour les utilisateurs AD ?", "answer": "Configure oddjob-mkhomedir avec pam-auth-update --enable mkhomedir pour créer automatiquement les home dirs à la première connexion."},
    ],
    "comment-modifier-heure-du-serveur-sous-linux.md": [
        {"question": "Comment vérifier mon fuseau horaire actuel sous Linux ?", "answer": "Utilise timedatectl pour voir le fuseau horaire et l'état de la synchronisation NTP."},
        {"question": "Comment lister tous les fuseaux horaires disponibles ?", "answer": "Tape timedatectl list-timezones ou explore le répertoire /usr/share/zoneinfo/"},
        {"question": "Comment changer le fuseau horaire sous Ubuntu en utilisant le terminal ?", "answer": "Utilise timedatectl set-timezone Europe/Paris (remplace par ton fuseau horaire)."},
    ],
    "calendrier-et-gestion-des-taches-unifies-morgen.md": [
        {"question": "Quelles sont les principales fonctionnalités de Morgen Calendar ?", "answer": "Intégration de calendriers, gestion de tâches, scheduling intelligent, gestion d'équipes, thèmes personnalisables."},
        {"question": "Comment Morgen assure-t-il la sécurité des données ?", "answer": "Morgen applique une politique stricte de confidentialité et une protection avancée des données utilisateur."},
        {"question": "Comment intégrer Morgen avec d'autres applications de gestion de tâches ?", "answer": "Morgen s'intègre avec Notion, Todoist, Google Calendar, Outlook, et Apple Calendar pour une synchronisation complète."},
    ],
    "auto-hebergement-guide-complet-2025.md": [
        {"question": "Faut-il des compétences en Linux pour l'auto-hébergement ?", "answer": "Non. Chaque article est pensé pour débutants. Tu apprendras au fur et à mesure."},
        {"question": "Ça coûte combien par mois ?", "answer": "Homelab : 0-30€/mois (électricité). VPS : 5-20€/mois. Combo : 15-25€/mois plus investissement matériel (~200-500€)."},
        {"question": "C'est légal d'héberger ses propres services ?", "answer": "100% légal. Héberger tes données et streamer tes achats DVD légaux est parfaitement légal. Le piratage reste illégal."},
        {"question": "Mes données sont-elles vraiment plus en sécurité chez moi ?", "answer": "Oui, plus qu'avec Google. Tes données ne sortent pas de chez toi, à condition de suivre les bonnes pratiques : firewall, backups, HTTPS."},
    ],
    "appcleaner-mac-alternative-gratuite-cleanmymac.md": [
        {"question": "AppCleaner est-il vraiment gratuit ?", "answer": "Oui, 100% gratuit sans version premium. Le développeur accepte les donations mais l'app reste entièrement fonctionnelle."},
        {"question": "AppCleaner supprime-t-il les malwares ?", "answer": "Non, AppCleaner est uniquement pour désinstaller les apps proprement. Utilise Malwarebytes pour les malwares."},
        {"question": "AppCleaner fonctionne-t-il sur macOS Sequoia ?", "answer": "Oui, AppCleaner est compatible avec toutes les versions macOS récentes y compris Sequoia."},
        {"question": "Quelle différence avec la suppression manuelle vers la corbeille ?", "answer": "La suppression manuelle laisse des traces dans Library. AppCleaner supprime tous les fichiers associés : préférences, caches, logs."},
    ],
    "alttab-macos-gestion-fenetres-windows.md": [
        {"question": "AltTab est-il vraiment gratuit ?", "answer": "Oui, open-source, gratuit, sans version premium. Disponible sur GitHub releases ou via Homebrew."},
        {"question": "AltTab fonctionne-t-il sur macOS Sequoia ?", "answer": "Oui, compatible avec toutes les versions macOS récentes. Test recommandé sur ta version spécifique."},
        {"question": "La permission Screen Recording est-elle sûre à accorder ?", "answer": "Oui. AltTab est open-source (auditable sur GitHub), ne transmet rien en dehors de ton Mac."},
        {"question": "AltTab ralentit-il mon Mac ?", "answer": "Non, très léger. Utilise peu de CPU/RAM sauf en mode grid avec beaucoup de fenêtres ouvertes."},
    ],
    "ajouter-un-programme-au-path-windows.md": [
        {"question": "Comment ajouter un programme au PATH Windows ?", "answer": "Trois méthodes : interface graphique (sysdm.cpl), PowerShell (SetEnvironmentVariable), ou CMD (setx). Le plus simple : interface graphique."},
        {"question": "Quelle est la différence entre PATH utilisateur et PATH système ?", "answer": "Utilisateur : personnel, modifiable sans droits admin. Système : pour tous les utilisateurs, nécessite les droits admin. Préfère utilisateur si possible."},
        {"question": "Pourquoi ma commande n'est toujours pas reconnue après ajout au PATH ?", "answer": "Ferme et rouvre ton terminal (pas besoin de redémarrer Windows). Vérifie que le chemin est correct et que le fichier .exe existe."},
    ],
}

def build_faqs_yaml(faqs):
    lines = ["faqs:"]
    for faq in faqs:
        q = faq["question"].replace('"', "'")
        a = faq["answer"].replace('"', "'")
        lines.append(f'  - question: "{q}"')
        lines.append(f'    answer: "{a}"')
    return "\n".join(lines)

def inject_faqs(filepath, faqs):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Already has faqs? skip
    if "faqs:" in content[:2000]:
        print(f"SKIP (already has faqs): {os.path.basename(filepath)}")
        return

    # Find end of frontmatter (second ---)
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        print(f"ERROR (no frontmatter): {os.path.basename(filepath)}")
        return

    frontmatter_end = match.end()
    faqs_yaml = build_faqs_yaml(faqs)

    # Insert faqs before closing ---
    closing_pos = content.rfind("\n---", 0, frontmatter_end)
    new_content = content[:closing_pos] + "\n" + faqs_yaml + content[closing_pos:]

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"OK: {os.path.basename(filepath)} ({len(faqs)} FAQs)")

if __name__ == "__main__":
    for filename, faqs in FAQS.items():
        filepath = os.path.join(BLOG_DIR, filename)
        if os.path.exists(filepath):
            inject_faqs(filepath, faqs)
        else:
            print(f"NOT FOUND: {filename}")
