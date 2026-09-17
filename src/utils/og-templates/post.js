import satori from "satori";
import { SITE } from "@/config";
import loadGoogleFonts from "../loadGoogleFont";

/**
 * Carte OG d'article — palette du site, pas de décor flottant.
 *
 * rack-night (#10131a) en fond, accent cyan (#008fec), grille fantôme en
 * signature (celle du site, pas un halo), texte plat sans ombre. Les valeurs
 * sont littérales : Satori ne résout ni les tokens CSS ni color-mix().
 * `#a6a7aa` est le `--text-soft` sombre aplati (f6f7f8 à 65 % sur 10131a).
 */
export default async post => {
  return satori(
    {
      type: "div",
      props: {
        style: {
          height: "100%",
          width: "100%",
          display: "flex",
          flexDirection: "column",
          alignItems: "flex-start",
          justifyContent: "space-between",
          backgroundColor: "#10131a",
          color: "#f6f7f8",
          padding: "72px",
          // Grille fantôme : la signature du site, pas un halo décoratif.
          backgroundImage:
            "linear-gradient(rgba(34, 100, 227, 0.12) 1px, transparent 1px), linear-gradient(90deg, rgba(34, 100, 227, 0.12) 1px, transparent 1px)",
          backgroundSize: "48px 48px",
        },
        children: [
          // 1. En-tête : marqueur accent + nom de domaine
          {
            type: "div",
            props: {
              style: {
                display: "flex",
                alignItems: "center",
              },
              children: [
                {
                  type: "div",
                  props: {
                    style: {
                      width: "12px",
                      height: "12px",
                      borderRadius: "3px",
                      backgroundColor: "#008fec",
                      marginRight: "14px",
                    },
                  },
                },
                {
                  type: "span",
                  props: {
                    style: {
                      fontSize: 24,
                      fontWeight: 600,
                      color: "#a6a7aa",
                      letterSpacing: "1px",
                    },
                    children: SITE.title + ".com",
                  },
                },
              ],
            },
          },

          // 2. Titre de l'article
          {
            type: "div",
            props: {
              style: {
                display: "flex",
                flexDirection: "column",
                width: "100%",
              },
              children: {
                type: "h1",
                props: {
                  style: {
                    fontSize: 76,
                    fontWeight: 900,
                    lineHeight: 1.12,
                    margin: 0,
                    color: "#f6f7f8",
                    overflow: "hidden",
                    display: "-webkit-box",
                    lineClamp: 3,
                    boxOrient: "vertical",
                  },
                  children: post.data.title,
                },
              },
            },
          },

          // 3. Signature : filet accent + auteur
          {
            type: "div",
            props: {
              style: {
                display: "flex",
                alignItems: "center",
                width: "100%",
              },
              children: [
                {
                  type: "div",
                  props: {
                    style: {
                      width: "56px",
                      height: "5px",
                      borderRadius: "3px",
                      backgroundColor: "#008fec",
                      marginRight: "24px",
                    },
                  },
                },
                {
                  type: "span",
                  props: {
                    style: {
                      fontSize: 30,
                      color: "#a6a7aa",
                    },
                    children: [
                      "Par ",
                      {
                        type: "span",
                        props: {
                          style: {
                            fontWeight: 700,
                            color: "#f6f7f8",
                          },
                          children: post.data.author,
                        },
                      },
                    ],
                  },
                },
              ],
            },
          },
        ],
      },
    },
    {
      width: 1200,
      height: 630,
      embedFont: true,
      fonts: await loadGoogleFonts(
        post.data.title + post.data.author + SITE.title + "Par" + ".com"
      ),
    }
  );
};
