import satori from "satori";
import { SITE } from "@/config";
import loadGoogleFonts from "../loadGoogleFont";

/**
 * Carte OG du site — même monde que la carte d'article : rack-night, accent
 * cyan, grille fantôme en signature. Aucun halo, aucune ombre portée.
 * `#a6a7aa` = `--text-soft` sombre aplati (f6f7f8 à 65 % sur 10131a).
 */
export default async () => {
  // Get the clean hostname (e.g. mydomain.com)
  const hostname = new URL(SITE.website).hostname;

  return satori(
    {
      type: "div",
      props: {
        style: {
          height: "100%",
          width: "100%",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          backgroundColor: "#10131a",
          // Grille fantôme : la signature du site, pas un halo décoratif.
          backgroundImage:
            "linear-gradient(rgba(34, 100, 227, 0.12) 1px, transparent 1px), linear-gradient(90deg, rgba(34, 100, 227, 0.12) 1px, transparent 1px)",
          backgroundSize: "48px 48px",
          color: "#f6f7f8",
        },
        children: [
          // 1. Conteneur central
          {
            type: "div",
            props: {
              style: {
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",
                textAlign: "center",
                padding: "40px",
                width: "90%",
              },
              children: [
                {
                  type: "h1",
                  props: {
                    style: {
                      fontSize: 96,
                      fontWeight: 900,
                      letterSpacing: "-2px",
                      color: "#f6f7f8",
                      margin: "0 0 24px 0",
                      lineHeight: 1,
                    },
                    children: SITE.title,
                  },
                },

                // Filet accent
                {
                  type: "div",
                  props: {
                    style: {
                      width: "64px",
                      height: "5px",
                      borderRadius: "3px",
                      backgroundColor: "#008fec",
                      marginBottom: "32px",
                    },
                  },
                },

                // Description
                {
                  type: "p",
                  props: {
                    style: {
                      fontSize: 34,
                      color: "#a6a7aa",
                      maxWidth: "78%",
                      margin: 0,
                      lineHeight: 1.4,
                      fontWeight: 400,
                    },
                    children: SITE.desc,
                  },
                },
              ],
            },
          },

          // 2. Pied : domaine, en pastille
          {
            type: "div",
            props: {
              style: {
                position: "absolute",
                bottom: "50px",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                backgroundColor: "rgba(0, 143, 236, 0.10)",
                border: "1px solid rgba(0, 143, 236, 0.35)",
                padding: "12px 30px",
                borderRadius: "100px",
              },
              children: {
                type: "span",
                props: {
                  style: {
                    fontSize: 24,
                    color: "#a6a7aa",
                    fontWeight: 600,
                    letterSpacing: "1px",
                  },
                  children: hostname,
                },
              },
            },
          },
        ],
      },
    },
    {
      width: 1200,
      height: 630,
      embedFont: true,
      fonts: await loadGoogleFonts(SITE.title + SITE.desc + hostname),
    }
  );
};
