import satori from "satori";
import loadGoogleFonts from "../loadGoogleFont";
import { C, h, frame, bottomRow } from "./frame";

/**
 * Carte OG du site (home, tags, pages annexes) : reprend le hero de la home,
 * promesse en grand et sous-titre, avec les thèmes principaux en pied.
 */
const THEMES = ["Homelab", "Auto-hébergement", "Linux", "Docker", "macOS"];

export default async () => {
  const middle = h("div", { display: "flex", flexDirection: "column" }, [
    h(
      "div",
      {
        fontSize: 80,
        fontWeight: 600,
        lineHeight: 1.05,
        letterSpacing: "-0.035em",
        color: C.foreground,
      },
      "Reprendre le contrôle de tes données."
    ),
    h(
      "div",
      {
        marginTop: 28,
        maxWidth: 860,
        fontSize: 34,
        lineHeight: 1.4,
        color: C.soft,
      },
      "Guides concrets sur le homelab, l'auto-hébergement et Linux."
    ),
  ]);

  const bottom = bottomRow(
    h(
      "div",
      { display: "flex", fontSize: 24, fontWeight: 500, color: C.foreground },
      THEMES.map((t, i) => h("span", { marginLeft: i === 0 ? 0 : 28 }, t))
    ),
    h("span", {}, "")
  );

  return satori(frame(middle, bottom), {
    width: 1200,
    height: 630,
    embedFont: true,
    fonts: await loadGoogleFonts(),
  });
};
