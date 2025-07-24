import { svelte } from '@sveltejs/vite-plugin-svelte';
import path from 'path';
import { defineConfig } from 'vite';

// https://vite.dev/config/
export default defineConfig({
  plugins: [svelte()],
  resolve: {
    alias: {
      lib: path.resolve(__dirname, 'src/lib'),
      client: path.resolve(__dirname, 'src/client'),
    },
  },
});
