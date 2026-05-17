import { SITE } from "@/config";

export interface TagMeta {
  title: string;
  description: string;
  intro?: string;
}

/**
 * Dictionnaire de meta-données SEO pour chaque tag du site.
 * Les titles et descriptions sont optimisés pour le référencement
 * et reflètent le contenu réel du blog.
 */
export const TAG_META: Record<string, TagMeta> = {
  // Tags primaires
  homelab: {
    title: `Homelab — Guides et tutoriels | ${SITE.title}`,
    description:
      "Tous les articles sur l'homelab : serveurs personnels, Proxmox, virtualisation, infrastructure et hardware auto-hébergé.",
    intro:
      "Construire et gérer son propre datacenter à la maison — de la virtualisation Proxmox au hardware dédié.",
  },
  "auto-hebergement": {
    title: `Auto-hébergement — Guides et tutoriels | ${SITE.title}`,
    description:
      "Tous les articles sur l'auto-hébergement : Docker, Nextcloud, Jellyfin, services auto-hébergés et indépendance numérique.",
    intro:
      "Reprendre le contrôle de ses données et services en les hébergeant soi-même.",
  },
  linux: {
    title: `Linux — Administration et tutoriels | ${SITE.title}`,
    description:
      "Tous les articles sur Linux : administration système, CLI, serveurs, distributions et optimisation.",
    intro:
      "Guides et tutoriels pour administrer Linux au quotidien, du serveur au poste de travail.",
  },
  macos: {
    title: `macOS — Guides et tutoriels | ${SITE.title}`,
    description:
      "Tous les articles sur macOS : productivité Mac, apps, Homebrew, scripts et automatisation.",
    intro:
      "Optimiser macOS avec des outils et workflows pensés pour la productivité.",
  },
  windows: {
    title: `Windows — Guides et tutoriels | ${SITE.title}`,
    description:
      "Tous les articles sur Windows : administration, Active Directory, PowerShell, outils et astuces.",
    intro:
      "Guides pratiques pour Windows et l'administration système en environnement professionnel.",
  },
  docker: {
    title: `Docker — Guides et tutoriels | ${SITE.title}`,
    description:
      "Tous les articles sur Docker : conteneurs, Docker Compose, Watchtower, déploiement et bonnes pratiques.",
    intro:
      "Maîtriser Docker et la conteneurisation pour déployer des services en toute simplicité.",
  },
  securite: {
    title: `Sécurité — Guides et tutoriels | ${SITE.title}`,
    description:
      "Tous les articles sur la sécurité informatique : durcissement serveur, Nginx, chiffrement, bonnes pratiques.",
    intro:
      "Sécuriser ses serveurs et services avec des méthodes concrètes et éprouvées.",
  },
  reseau: {
    title: `Réseau — Guides et tutoriels | ${SITE.title}`,
    description:
      "Tous les articles sur le réseau : pfSense, DNS, Pi-hole, configuration et administration.",
    intro:
      "Administrer son réseau local et ses services DNS avec des outils open source.",
  },
  productivite: {
    title: `Productivité — Guides et tutoriels | ${SITE.title}`,
    description:
      "Tous les articles sur la productivité : workflows, outils, automatisation et gestion du temps.",
    intro:
      "Améliorer son efficacité au quotidien avec des outils et méthodes testés.",
  },
  sysadmin: {
    title: `Sysadmin — Guides et tutoriels | ${SITE.title}`,
    description:
      "Tous les articles sur l'administration système : PowerShell, Active Directory, ITSM, scripts.",
    intro:
      "Ressources pour les administrateurs système et les professionnels de l'infrastructure IT.",
  },
  developpement: {
    title: `Développement — Guides et tutoriels | ${SITE.title}`,
    description:
      "Tous les articles sur le développement : dev tools, éditeurs, terminal, scripting et bonnes pratiques.",
    intro:
      "Outils et méthodes pour développer efficacement et maintenir du code propre.",
  },
  "microsoft-365": {
    title: `Microsoft 365 — Guides et tutoriels | ${SITE.title}`,
    description:
      "Tous les articles sur Microsoft 365 : Office 365, Exchange, Teams, Outlook et administration cloud.",
    intro:
      "Guides pratiques pour administrer et optimiser Microsoft 365 en entreprise.",
  },

  // Tags méta (masqués dans l'index, mais descriptifs quand même)
  guide: {
    title: `Guides complets — Tous les tutoriels | ${SITE.title}`,
    description:
      "Tous les guides complets du blog : tutoriels étape par étape pour apprendre et mettre en pratique.",
  },
  debutant: {
    title: `Articles pour débutants — Bases et fondamentaux | ${SITE.title}`,
    description:
      "Tous les articles accessibles aux débutants : concepts de base, premiers pas et introductions.",
  },
  intermediaire: {
    title: `Articles intermédiaires — Aller plus loin | ${SITE.title}`,
    description:
      "Tous les articles de niveau intermédiaire : approfondissements et configurations avancées.",
  },
  avance: {
    title: `Articles avancés — Expertise et optimisation | ${SITE.title}`,
    description:
      "Tous les articles avancés : configurations complexes, optimisation et techniques expertes.",
  },

  // Tags secondaires
  snipeit: {
    title: `Snipe-IT — Guides et tutoriels | ${SITE.title}`,
    description:
      "Tous les articles sur Snipe-IT : gestion d'inventaire IT, ITSM et déploiement.",
  },
  nginx: {
    title: `Nginx — Guides et tutoriels | ${SITE.title}`,
    description:
      "Tous les articles sur Nginx : configuration, reverse proxy, sécurité et optimisation.",
  },
  "active-directory": {
    title: `Active Directory — Guides et tutoriels | ${SITE.title}`,
    description:
      "Tous les articles sur Active Directory : administration, GPO, rôles FSMO et bonnes pratiques.",
  },
  powershell: {
    title: `PowerShell — Scripts et tutoriels | ${SITE.title}`,
    description:
      "Tous les articles sur PowerShell : scripts, automatisation et administration Windows.",
  },
  terminal: {
    title: `Terminal — Guides et tutoriels | ${SITE.title}`,
    description:
      "Tous les articles sur le terminal : Zsh, Oh My Zsh, iTerm2, prompts et configuration.",
  },
  "windows-server": {
    title: `Windows Server — Guides et tutoriels | ${SITE.title}`,
    description:
      "Tous les articles sur Windows Server : installation, rôles, Hyper-V et administration.",
  },
  dns: {
    title: `DNS — Guides et tutoriels | ${SITE.title}`,
    description:
      "Tous les articles sur le DNS : configuration, Pi-hole, résolution de noms et sécurité.",
  },
  homebrew: {
    title: `Homebrew — Guides et tutoriels | ${SITE.title}`,
    description:
      "Tous les articles sur Homebrew : gestion de paquets macOS, taps et automatisation.",
  },
  hardening: {
    title: `Hardening — Durcissement et sécurité | ${SITE.title}`,
    description:
      "Tous les articles sur le durcissement serveur : headers HTTP, chiffrement et bonnes pratiques.",
  },
  multimedia: {
    title: `Multimédia — Guides et tutoriels | ${SITE.title}`,
    description:
      "Tous les articles sur le multimédia : FFmpeg, conversion, streaming et gestion de médias.",
  },
  raycast: {
    title: `Raycast — Guides et tutoriels | ${SITE.title}`,
    description:
      "Tous les articles sur Raycast : productivité macOS, extensions et workflows.",
  },
  monitoring: {
    title: `Monitoring — Guides et tutoriels | ${SITE.title}`,
    description:
      "Tous les articles sur le monitoring : Uptime Kuma, UptimeRobot, supervision et alertes.",
  },
  backup: {
    title: `Sauvegarde — Guides et tutoriels | ${SITE.title}`,
    description:
      "Tous les articles sur la sauvegarde : stratégies, outils et restauration de données.",
  },
  nextcloud: {
    title: `Nextcloud — Guides et tutoriels | ${SITE.title}`,
    description:
      "Tous les articles sur Nextcloud : déploiement, configuration et auto-hébergement.",
  },
  wordpress: {
    title: `WordPress — Guides et tutoriels | ${SITE.title}`,
    description:
      "Tous les articles sur WordPress : administration, sécurité et optimisation.",
  },
  ldap: {
    title: `LDAP — Guides et tutoriels | ${SITE.title}`,
    description:
      "Tous les articles sur LDAP : annuaire, authentification et intégration Active Directory.",
  },
  ssh: {
    title: `SSH — Guides et tutoriels | ${SITE.title}`,
    description:
      "Tous les articles sur SSH : clés, configuration sécurisée et tunneling.",
  },
  vim: {
    title: `Vim — Guides et tutoriels | ${SITE.title}`,
    description:
      "Tous les articles sur Vim : configuration, plugins et productivité dans l'éditeur.",
  },
  "hyper-v": {
    title: `Hyper-V — Guides et tutoriels | ${SITE.title}`,
    description:
      "Tous les articles sur Hyper-V : virtualisation Windows, VHDX et machines virtuelles.",
  },
};

/**
 * Retourne les meta-données SEO pour un tag donné.
 * Si le tag n'est pas dans le dictionnaire, retourne un fallback générique.
 */
export function getTagMeta(tag: string, count: number): TagMeta {
  const meta = TAG_META[tag];
  if (meta) return meta;

  const tagLabel = tag.charAt(0).toUpperCase() + tag.slice(1).replace(/-/g, " ");
  return {
    title: `${tagLabel} — Articles et guides | ${SITE.title}`,
    description: `Tous les articles avec le tag "${tagLabel}" sur ${SITE.title}.`,
  };
}
