import { defineConfig } from 'vite';
import { resolve } from 'node:path';

// Layout: the repository root IS the deployable static site
//   index.html + assets/   <- built by `npm run build` from app/index.html + src/
//   config.js, content/, media/  <- static files, served as-is
// so GitHub Pages works both from the Actions workflow and from "Deploy from a branch (main, /)".
// base './' keeps every path relative (works under https://<user>.github.io/<repo>/).
export default defineConfig(({ command }) => ({
  root: resolve(__dirname, 'app'),
  base: './',
  // dev: serve the repo root so /content, /media and /config.js resolve; build: copy nothing
  publicDir: command === 'serve' ? resolve(__dirname) : false,
  build: {
    outDir: resolve(__dirname),
    emptyOutDir: false,
    assetsDir: 'assets',
    chunkSizeWarningLimit: 900,
  },
  server: { port: 5173, fs: { allow: [resolve(__dirname)] } },
  preview: { port: 4173 },
}));
