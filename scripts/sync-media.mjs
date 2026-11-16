// Copies audio from your original material folder into public/media/audio using ASCII-safe names.
// Usage:  npm run sync-media -- "D:\Material For TOCFL Website Claude"
//   (or set TOCFL_SOURCE). Re-running only copies missing/changed files. Reports anything missing.
import { readFileSync, existsSync, mkdirSync, copyFileSync, statSync, writeFileSync } from 'node:fs';
import { join, dirname } from 'node:path';

const src = process.argv[2] || process.env.TOCFL_SOURCE;
if (!src) {
  console.error('Berikan path folder materi, mis.: npm run sync-media -- "D:\\Material For TOCFL Website Claude"');
  process.exit(1);
}
const manifest = JSON.parse(readFileSync('public/content/media-manifest.json', 'utf8'));
let copied = 0, skipped = 0;
const missing = [];
for (const { source, target } of manifest) {
  // Series 2/3 Band A file names are stored with legacy (Big5) bytes; try the literal name and a "中英" variant.
  const candidates = [source, source.replace('\u00a4\u00a4\u00ad^', '中英')];
  const from = candidates.map((c) => join(src, ...c.split('/'))).find((p) => existsSync(p));
  const to = join('public', 'media', 'audio', ...target.split('/'));
  if (!from) { missing.push(source); continue; }
  if (existsSync(to) && statSync(to).size === statSync(from).size) { skipped++; continue; }
  mkdirSync(dirname(to), { recursive: true });
  copyFileSync(from, to);
  copied++;
}
writeFileSync('reports/media-sync-report.json', JSON.stringify({ at: new Date().toISOString(), total: manifest.length, copied, skipped, missing }, null, 1));
console.log(`audio: ${copied} copied, ${skipped} already present, ${missing.length} missing (of ${manifest.length})`);
if (missing.length) console.log('Missing files listed in reports/media-sync-report.json (first 10):\n  ' + missing.slice(0, 10).join('\n  '));
