import fs from "fs";
import path from "path";

const WEIGHTS = [400, 600, 700, 900] as const;

async function loadGoogleFonts(): Promise<
  Array<{ name: string; data: ArrayBuffer; weight: number; style: string }>
> {
  // Satori cannot read woff2 or variable fonts: load one static WOFF per
  // weight so OG images render real Figtree weights instead of faux bold.
  return WEIGHTS.map(weight => {
    const fontPath = path.resolve(
      `./src/assets/fonts/og/figtree-latin-${weight}-normal.woff`
    );
    const file = fs.readFileSync(fontPath);
    const data = file.buffer.slice(
      file.byteOffset,
      file.byteOffset + file.byteLength
    ) as ArrayBuffer;
    return { name: "Figtree", data, weight, style: "normal" };
  });
}

export default loadGoogleFonts;
