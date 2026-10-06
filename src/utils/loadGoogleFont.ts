import fs from "fs";
import path from "path";

type SatoriFont = {
  name: string;
  data: ArrayBuffer;
  weight: 400 | 500 | 600;
  style: "normal";
};

// Satori ne lit ni le woff2 ni les polices variables : une WOFF statique par
// graisse (sous-ensemble latin, accents français compris), comme sur le site.
// Les tables GSUB/GPOS/GDEF/kern sont retirées (pyftsubset --layout-features=''
// --drop-tables+=GSUB,GPOS,GDEF,kern) : avec elles, Satori 0.19 mesure les mots
// sans crénage mais les dessine crénés, d'où des espaces irréguliers entre mots.
const FONTS: Array<[name: string, file: string, weight: SatoriFont["weight"]]> = [
  ["Geist", "geist-latin-400-normal.woff", 400],
  ["Geist", "geist-latin-500-normal.woff", 500],
  ["Geist", "geist-latin-600-normal.woff", 600],
  ["Geist Mono", "geist-mono-latin-400-normal.woff", 400],
];

async function loadGoogleFonts(): Promise<SatoriFont[]> {
  return FONTS.map(([name, file, weight]) => {
    const buf = fs.readFileSync(path.resolve(`./src/assets/fonts/og/${file}`));
    const data = buf.buffer.slice(
      buf.byteOffset,
      buf.byteOffset + buf.byteLength
    ) as ArrayBuffer;
    return { name, data, weight, style: "normal" };
  });
}

export default loadGoogleFonts;
