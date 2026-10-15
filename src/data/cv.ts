/*
 * Contenu du CV (/cv/). La mise en page vit dans src/pages/cv.astro.
 * Dans les chaînes, **texte** passe en gras (chiffres et faits saillants).
 */

export const identity = {
  name: "Brandon Visca",
  role: "Responsable Infrastructure & Sécurité IT",
  subrole: "Référent technique",
  email: "brandonvisca@gmail.com",
  github: "visbran",
  location: "Chambéry (73)",
  profile:
    "Responsable Infrastructure & Sécurité IT, **7 ans** comme référent technique unique : école supérieure multi-sites (**1800 utilisateurs**) puis groupe BTP multi-entités. J'administre, sécurise, supervise et documente des SI on-premise et Microsoft 365 de bout en bout, en arbitrant seul les priorités.",
};

export const keyFigures = [
  { value: "7 ans", label: "d'expérience" },
  { value: "17+", label: "projets pilotés" },
  { value: "1800", label: "utilisateurs" },
  { value: "90 K€", label: "économisés" },
];

type Group = { label: string; items: string[] };

export type Job = {
  role: string;
  company: string;
  place: string;
  period: string;
  duration?: string;
  summary: string;
  groups: Group[];
};

export const jobs: Job[] = [
  {
    role: "Administrateur Systèmes & Réseaux - Référent IT unique",
    company: "Groupe BTP multi-entités (5 sociétés)",
    place: "Chambéry",
    period: "Déc. 2025 - aujourd'hui",
    summary:
      "Seul responsable du SI (**~80 utilisateurs**) : infrastructure, sécurité, M365, support et prestataires. Reprise d'un environnement non documenté, structuré et documenté progressivement.",
    groups: [
      {
        label: "Réalisations",
        items: [
          "**Infrastructure** : migration vers un nouveau plan d'adressage, transfert des rôles FSMO, restructuration AD (OU, conventions de nommage), PKI AD CS, déploiement MDT/WDS Windows 11",
          "**Sécurité** : FortiGate et segmentation VLAN, élévation de privilèges à la demande, audit et gouvernance du tenant SharePoint/Teams",
          "**Supervision** : déploiement Zabbix 7 + Grafana",
          "**Automatisation** : archivage SharePoint en PowerShell avec restauration, circuit de visa documentaire SharePoint + Power Automate",
          "**Projets** : passage à la téléphonie IP avec pilotage de l'intégrateur, accès fichiers web sous Docker",
        ],
      },
    ],
  },
  {
    role: "Responsable Informatique - Référent technique unique",
    company: "Groupe ECORIS",
    place: "Chambéry",
    period: "Août 2019 - Juil. 2025",
    duration: "6 ans",
    summary:
      "SI complet d'une école de commerce multi-sites (**1500 étudiants + 300 collaborateurs**). Évolution d'**Administrateur Système** (2019-2021) à **Responsable Informatique** (2021-2025).",
    groups: [
      {
        label: "Projets majeurs",
        items: [
          "**Refonte réseau multi-sites (2020-2022)** : 5 établissements, 10 routeurs pfSense + Unifi, 25 bornes WiFi. Bande passante **x4**, incidents **-80 %**, **30 K€** économisés",
          "**Plateforme d'hébergement pédagogique (2021-2024)** : 5 serveurs, **~880 sites/an**, provisioning automatisé en **30 s**, disponibilité **99,9 %**, **15 K€/an** économisés",
          "**Refonte ECORIS Notes (2021-2023)** : MOA complète, cahier des charges **100+ pages**, **300 utilisateurs** formés, gain de temps **60 %**",
          "**Refonte Ecoris Connect (2023-2024)** : étude de 8 solutions, POC, migration HumHub, adoption **95 % en 2 mois**",
        ],
      },
      {
        label: "Exploitation & sécurité",
        items: [
          "**110 postes**, **10 serveurs physiques**, **4 serveurs cloud** ; Windows Server, Linux, AD, Hyper-V, VMware",
          "**Microsoft 365** : 2 tenants gérés pendant 5 ans",
          "Sauvegardes **Veeam** + Synology (3-2-1), **zéro perte de données en 4 ans** ; phishing **-82 %**",
          "Déploiement **WDS/MDT** (gain **50 %**), ITSM : **2000+ tickets/an**",
        ],
      },
    ],
  },
];

export const skills: Group[] = [
  {
    label: "Systèmes & identités",
    items: [
      "Windows Server 2016 à 2022",
      "Linux (Debian, Ubuntu)",
      "Active Directory (OU, GPO, FSMO)",
      "DNS",
      "DHCP",
      "AD CS",
    ],
  },
  {
    label: "Cloud & Microsoft 365",
    items: [
      "Entra ID",
      "Exchange Online",
      "SharePoint",
      "Teams",
      "Licences",
      "Graph API (5 ans, 2 tenants)",
    ],
  },
  {
    label: "Virtualisation",
    items: ["Hyper-V", "VMware", "Proxmox", "Docker", "Docker Compose"],
  },
  {
    label: "Sécurité, sauvegarde & PRA",
    items: [
      "FortiGate",
      "pfSense",
      "VLAN",
      "Élévation JIT (EPM)",
      "Veeam",
      "Synology",
      "3-2-1",
      "Tests de restauration",
    ],
  },
  {
    label: "Réseau & supervision",
    items: [
      "Fortinet",
      "Unifi",
      "Cisco",
      "TCP/IP",
      "VPN site-à-site",
      "Zabbix 7",
      "Grafana",
      "PRTG",
      "Uptime Kuma",
    ],
  },
  {
    label: "Automatisation & pilotage",
    items: [
      "PowerShell (PnP)",
      "Bash",
      "Batch",
      "Git/GitHub",
      "GLPI",
      "MOA",
      "Cahiers des charges",
      "Prestataires",
    ],
  },
];

export const education = [
  {
    degree: "Bachelor Cybersécurité (Bac+3)",
    school: "ECORIS, Chambéry",
    year: "2022",
  },
  { degree: "BTS SIO option SISR", school: "ECORIS, Chambéry", year: "2021" },
  { degree: "Bac STG", school: "Lycée du Granier", year: "2013" },
];

export const softSkills = [
  "**Autonomie totale** (référent unique)",
  "**Arbitrage rapide** des priorités",
  "**Pilotage** de projets et de prestataires",
  "**Documentation** systématique",
  "**Résolution de problèmes** complexes",
];

export const sideProjects = [
  "Homelab Proxmox + Unifi, WireGuard, Caddy, CrowdSec",
  "Micro-SaaS en production (Astro, Vercel), code sous Git/GitHub",
  "Blog technique IT ([ce site](https://brandonvisca.com))",
  "Veille active : automatisation, sécurité, conteneurisation",
];

export const interests = ["Musculation", "Vélo en loisir"];
