/**
 * Recadre le `sizes` des images de corps d'article sur la largeur réelle du
 * texte.
 *
 * `image.layout: "constrained"` calcule `sizes` en supposant que l'image
 * occupe presque toute la largeur de l'écran : une image de 2880 px reçoit
 * `(min-width: 2880px) 2880px, 100vw`. Or le corps d'article plafonne ses
 * images à 760 px (typography.css), donc le navigateur téléchargeait des
 * variantes jusqu'à quatre fois trop larges — jusqu'à plusieurs centaines de
 * kilo-octets inutiles par image.
 *
 * Intégration de build et non plugin de markdown : les plugins rehype
 * s'exécutent **avant** celui qui produit `srcset`/`sizes`, et les plugins
 * remark ne connaissent pas encore la largeur résolue de l'image. On corrige
 * donc l'attribut une fois le HTML écrit, quand la valeur est connue.
 *
 * Les images dont la largeur déclarée tient déjà dans le corps de texte
 * gardent leur `sizes` d'origine.
 */

import { readdir, readFile, writeFile } from "node:fs/promises";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

const PROSE_MAX_WIDTH = 760;
// 760 + la gouttière de `app-layout` (px-4 = 16px de chaque côté).
const PROSE_BREAKPOINT = PROSE_MAX_WIDTH + 32;

const OVERSIZED = /sizes="\(min-width: (\d+)px\) \d+px, 100vw"/g;

export default function proseImageSizes() {
  return {
    name: "prose-image-sizes",
    hooks: {
      "astro:build:done": async ({ dir, logger }) => {
        const pages = [];
        const collect = async path => {
          for (const entry of await readdir(path, { withFileTypes: true })) {
            const full = join(path, entry.name);
            if (entry.isDirectory()) await collect(full);
            else if (entry.name.endsWith(".html")) pages.push(full);
          }
        };
        await collect(fileURLToPath(dir));

        let rewritten = 0;
        await Promise.all(
          pages.map(async page => {
            const html = await readFile(page, "utf8");
            const fixed = html.replace(OVERSIZED, (match, width) =>
              Number(width) > PROSE_BREAKPOINT
                ? `sizes="(min-width: ${PROSE_BREAKPOINT}px) ${PROSE_MAX_WIDTH}px, 100vw"`
                : match
            );
            if (fixed !== html) {
              rewritten += 1;
              await writeFile(page, fixed, "utf8");
            }
          })
        );

        logger.info(
          `sizes recadré sur ${PROSE_MAX_WIDTH}px dans ${rewritten} page(s)`
        );
      },
    },
  };
}
