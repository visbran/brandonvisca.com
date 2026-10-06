import { SITE } from "@/config";

/**
 * Socle commun des cartes OG, aligné sur le thème sombre du site (palette
 * Cobalt, 2026-10). Les valeurs sont littérales : Satori ne résout ni les
 * tokens CSS ni color-mix(). Le halo d'accent en haut à droite reprend celui
 * de la carte « Dernier article » de la home.
 */
export const C = {
  background: "#10131a",
  surfaceLine: "#2a3342",
  foreground: "#e6e9ee",
  soft: "#98a1af",
  accent: "#4a9fe8",
};

const hostname = new URL(SITE.website).hostname;

/** Petit utilitaire : nœud Satori. */
export const h = (type, style, children) => ({
  type,
  props: { style, children },
});

/** Ligne du haut : invite du hero à gauche, domaine à droite. */
const topRow = () =>
  h(
    "div",
    {
      display: "flex",
      justifyContent: "space-between",
      alignItems: "center",
      width: "100%",
      fontFamily: "Geist Mono",
      fontSize: 24,
      color: C.soft,
    },
    [
      h("div", { display: "flex" }, [
        h("span", { color: C.accent }, SITE.heroTerminalPrompt.prefix),
        h("span", {}, ` ${SITE.heroTerminalPrompt.suffix}`),
      ]),
      h("span", {}, hostname),
    ]
  );

/** Ligne du bas sous un filet : contenu libre à gauche et à droite. */
export const bottomRow = (left, right) =>
  h(
    "div",
    {
      display: "flex",
      justifyContent: "space-between",
      alignItems: "center",
      width: "100%",
      paddingTop: 28,
      borderTop: `1px solid ${C.surfaceLine}`,
    },
    [left, right]
  );

/** Cadre 1200×630 : en-tête, contenu central, pied. */
export const frame = (middle, bottom) =>
  h(
    "div",
    {
      height: "100%",
      width: "100%",
      display: "flex",
      flexDirection: "column",
      justifyContent: "space-between",
      padding: "64px 72px",
      backgroundColor: C.background,
      backgroundImage: `radial-gradient(circle at 100% 0%, rgba(74, 159, 232, 0.2) 0%, rgba(16, 19, 26, 0) 55%)`,
      color: C.foreground,
      fontFamily: "Geist",
    },
    [topRow(), middle, bottom]
  );
