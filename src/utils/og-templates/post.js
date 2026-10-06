import satori from "satori";
import { SITE } from "@/config";
import loadGoogleFonts from "../loadGoogleFont";
import { C, h, frame, bottomRow } from "./frame";

/**
 * Carte OG d'article : même composition que l'en-tête d'article du site.
 * Titre Geist 600 serré, auteur en pied, tags thématiques en mono.
 */
const META_TAGS = new Set(["guide", "debutant", "intermediaire", "avance"]);

export default async post => {
  const { title, tags = [] } = post.data;
  // Certains articles portent « Brandon » seul : la carte affiche le nom complet.
  const author =
    !post.data.author || SITE.author.startsWith(post.data.author)
      ? SITE.author
      : post.data.author;
  const topicTags = tags.filter(t => !META_TAGS.has(t)).slice(0, 3);
  // Titres longs : on réduit le corps plutôt que de tronquer trop tôt.
  const fontSize = title.length > 70 ? 58 : title.length > 45 ? 66 : 76;

  const middle = h(
    "div",
    {
      display: "block",
      width: "100%",
      fontSize,
      fontWeight: 600,
      lineHeight: 1.08,
      letterSpacing: "-0.03em",
      color: C.foreground,
      overflow: "hidden",
      lineClamp: 3,
    },
    title
  );

  const bottom = bottomRow(
    h("span", { fontSize: 28, fontWeight: 500, color: C.foreground }, author),
    h(
      "div",
      { display: "flex", fontFamily: "Geist Mono", fontSize: 22, color: C.soft },
      topicTags.map((t, i) =>
        h("span", { marginLeft: i === 0 ? 0 : 20 }, `#${t}`)
      )
    )
  );

  return satori(frame(middle, bottom), {
    width: 1200,
    height: 630,
    embedFont: true,
    fonts: await loadGoogleFonts(),
  });
};
