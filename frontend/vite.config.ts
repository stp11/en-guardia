import { svelte } from "@sveltejs/vite-plugin-svelte";
import tailwindcss from "@tailwindcss/vite";
import path from "path";
import { defineConfig } from "vite";

// https://vite.dev/config/
export default defineConfig({
  plugins: [svelte(), tailwindcss()],
  build: {
    outDir: "dist",
  },
  resolve: {
    alias: {
      lib: path.resolve(__dirname, "src/lib"),
      client: path.resolve(__dirname, "src/client"),
    },
  },
});
