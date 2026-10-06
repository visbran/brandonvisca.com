import { defineConfig, envField, fontProviders } from "astro/config";
import mdx from "@astrojs/mdx";
import tailwindcss from "@tailwindcss/vite";
import sitemap from "@astrojs/sitemap";
import remarkToc from "remark-toc";
import remarkCollapse from "remark-collapse";
import {
  transformerNotationDiff,
  transformerNotationHighlight,
  transformerNotationWordHighlight,
} from "@shikijs/transformers";
import { transformerFileName } from "./src/utils/transformers/fileName";
import proseImageSizes from "./src/utils/prose-image-sizes.mjs";
import { SITE } from "./src/config";

// https://astro.build/config
export default defineConfig({
  site: SITE.website,
  integrations: [
    proseImageSizes(),
    mdx({
      extendMarkdownConfig: true,
      // Astro 6.4 laisse markdown.gfm/smartypants à undefined (options dépréciées) :
      // le pipeline Markdown applique quand même ses défauts, mais MDX en hérite
      // comme désactivés. Sans ces deux lignes, les tableaux des .mdx sortent en texte brut.
      gfm: true,
      smartypants: true,
    }),
    sitemap({
      // Les routes désactivées restent générées par le build : sans filtre
      // elles continuaient d'être soumises à Google et indexées.
      filter: page => {
        // `includes` et non `endsWith` : les URLs du sitemap portent un slash
        // final, donc le test d'origine ne matchait jamais.
        if (!SITE.showArchives && page.includes("/archives")) return false;
        if (!SITE.showGalleries && page.includes("/galleries")) return false;
        return true;
      },
    }),
  ],
  markdown: {
    remarkPlugins: [
      [remarkToc, { heading: "Table des matières", maxDepth: 3 }],
      [remarkCollapse, { test: "Table des matières", summary: (str: string) => str }],
    ],
    shikiConfig: {
      // For more themes, visit https://shiki.style/themes
      themes: { light: "min-light", dark: "github-dark-default" },
      defaultColor: false,
      wrap: false,
      transformers: [
        transformerFileName({ style: "v2", hideDot: false }),
        transformerNotationHighlight(),
        transformerNotationWordHighlight(),
        transformerNotationDiff({ matchAlgorithm: "v3" }),
      ],
    },
  },
  vite: {
    plugins: [tailwindcss()],
    optimizeDeps: {
      exclude: ["@resvg/resvg-js"],
    },
  },
  image: {
    responsiveStyles: true,
    layout: "constrained",
  },
  env: {
    schema: {
      PUBLIC_GOOGLE_SITE_VERIFICATION: envField.string({
        access: "public",
        context: "client",
        optional: true,
      }),
      PUBLIC_TIANJI_WEBSITE_ID: envField.string({
        access: "public",
        context: "client",
        optional: true,
      }),
    },
  },

  fonts: [
    {
      name: "Geist",
      cssVariable: "--font-geist",
      fallbacks: ["ui-sans-serif", "system-ui", "sans-serif"],
      provider: fontProviders.local(),
      options: {
        variants: [
          {
            weight: "100 900",
            style: "normal",
            src: ["./src/assets/fonts/geist-latin-wght-normal.woff2"],
            unicodeRange: ["U+0000-00FF", "U+0131", "U+0152-0153", "U+02BB-02BC", "U+02C6", "U+02DA", "U+02DC", "U+0304", "U+0308", "U+0329", "U+2000-206F", "U+20AC", "U+2122", "U+2191", "U+2193", "U+2212", "U+2215", "U+FEFF", "U+FFFD"],
          },
          {
            weight: "100 900",
            style: "normal",
            src: ["./src/assets/fonts/geist-latin-ext-wght-normal.woff2"],
            unicodeRange: ["U+0100-02BA", "U+02BD-02C5", "U+02C7-02CC", "U+02CE-02D7", "U+02DD-02FF", "U+0304", "U+0308", "U+0329", "U+1D00-1DBF", "U+1E00-1E9F", "U+1EF2-1EFF", "U+2020", "U+20A0-20AB", "U+20AD-20C0", "U+2113", "U+2C60-2C7F", "U+A720-A7FF"],
          },
          {
            weight: "100 900",
            style: "italic",
            src: ["./src/assets/fonts/geist-latin-wght-italic.woff2"],
            unicodeRange: ["U+0000-00FF", "U+0131", "U+0152-0153", "U+02BB-02BC", "U+02C6", "U+02DA", "U+02DC", "U+0304", "U+0308", "U+0329", "U+2000-206F", "U+20AC", "U+2122", "U+2191", "U+2193", "U+2212", "U+2215", "U+FEFF", "U+FFFD"],
          },
          {
            weight: "100 900",
            style: "italic",
            src: ["./src/assets/fonts/geist-latin-ext-wght-italic.woff2"],
            unicodeRange: ["U+0100-02BA", "U+02BD-02C5", "U+02C7-02CC", "U+02CE-02D7", "U+02DD-02FF", "U+0304", "U+0308", "U+0329", "U+1D00-1DBF", "U+1E00-1E9F", "U+1EF2-1EFF", "U+2020", "U+20A0-20AB", "U+20AD-20C0", "U+2113", "U+2C60-2C7F", "U+A720-A7FF"],
          },
        ],
      },
    },
    {
      name: "Geist Mono",
      cssVariable: "--font-geist-mono",
      fallbacks: ["ui-monospace", "SFMono-Regular", "monospace"],
      provider: fontProviders.local(),
      options: {
        variants: [
          {
            weight: "100 900",
            style: "normal",
            src: ["./src/assets/fonts/geist-mono-latin-wght-normal.woff2"],
            unicodeRange: ["U+0000-00FF", "U+0131", "U+0152-0153", "U+02BB-02BC", "U+02C6", "U+02DA", "U+02DC", "U+0304", "U+0308", "U+0329", "U+2000-206F", "U+20AC", "U+2122", "U+2191", "U+2193", "U+2212", "U+2215", "U+FEFF", "U+FFFD"],
          },
          {
            weight: "100 900",
            style: "normal",
            src: ["./src/assets/fonts/geist-mono-latin-ext-wght-normal.woff2"],
            unicodeRange: ["U+0100-02BA", "U+02BD-02C5", "U+02C7-02CC", "U+02CE-02D7", "U+02DD-02FF", "U+0304", "U+0308", "U+0329", "U+1D00-1DBF", "U+1E00-1E9F", "U+1EF2-1EFF", "U+2020", "U+20A0-20AB", "U+20AD-20C0", "U+2113", "U+2C60-2C7F", "U+A720-A7FF"],
          },
        ],
      },
    },
  ],
});
