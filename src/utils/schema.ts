import { SITE } from "@/config";

// Entités Schema.org partagées. Chaque page les référence par `@id` plutôt que
// de les redéfinir : Google et les crawlers IA fusionnent alors les nœuds en
// une seule personne et une seule organisation au lieu de N copies divergentes.

const origin = SITE.website.replace(/\/$/, "");

export const SCHEMA_IDS = {
  person: `${origin}/about/#person`,
  organization: `${origin}/#organization`,
  website: `${origin}/#website`,
} as const;

const SAME_AS = ["https://github.com/visbran"];

export const personSchema = {
  "@type": "Person",
  "@id": SCHEMA_IDS.person,
  name: SITE.author,
  url: `${origin}/about/`,
  sameAs: SAME_AS,
  jobTitle: "Administrateur systèmes et réseaux",
  knowsAbout: [
    "Homelab",
    "Auto-hébergement",
    "Linux",
    "Proxmox VE",
    "Docker",
    "Réseaux",
    "Sécurité informatique",
    "macOS",
  ],
};

export const organizationSchema = {
  "@type": "Organization",
  "@id": SCHEMA_IDS.organization,
  name: SITE.title,
  url: `${origin}/`,
  logo: {
    "@type": "ImageObject",
    url: `${origin}/apple-touch-icon.png`,
    width: 180,
    height: 180,
  },
  image: `${origin}/${SITE.ogImage}`,
  description: SITE.desc,
  sameAs: SAME_AS,
  founder: { "@id": SCHEMA_IDS.person },
};
