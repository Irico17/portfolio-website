import { defineConfig } from "astro/config";

export default defineConfig({
  site: "https://irico17.github.io",
  base: "/portfolio-website/",
  output: "static",
  compressHTML: true,
  build: {
    inlineStylesheets: "auto",
  },
});
