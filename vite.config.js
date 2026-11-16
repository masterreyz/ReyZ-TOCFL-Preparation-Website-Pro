import { defineConfig } from 'vite';

// base './' keeps every asset path relative, so the build works on a GitHub Pages
// project subpath (https://<user>.github.io/<repo>/) and from any static host.
export default defineConfig({
  base: './',
  build: { outDir: 'dist', assetsDir: 'assets', chunkSizeWarningLimit: 900 },
  server: { port: 5173 },
});
