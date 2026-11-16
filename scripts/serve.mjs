// Serves the repository root exactly like GitHub Pages does, under /<repo-name>/ (default port 4173).
// Usage: npm run preview  ->  http://localhost:4173/ReyZ-TOCFL-Preparation-Website-Pro/
import { createServer } from 'node:http';
import { readFile, stat } from 'node:fs/promises';
import { extname, join, normalize } from 'node:path';

const PREFIX = '/ReyZ-TOCFL-Preparation-Website-Pro/';
const TYPES = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.css': 'text/css', '.json': 'application/json', '.webp': 'image/webp', '.mp3': 'audio/mpeg', '.svg': 'image/svg+xml' };
const port = Number(process.env.PORT) || 4173;
createServer(async (req, res) => {
  let path = decodeURIComponent(new URL(req.url, 'http://x').pathname);
  if (path === '/') { res.writeHead(302, { location: PREFIX }); return res.end(); }
  if (!path.startsWith(PREFIX)) { res.writeHead(404); return res.end('not found'); }
  let file = normalize(join(process.cwd(), path.slice(PREFIX.length)));
  if (!file.startsWith(process.cwd())) { res.writeHead(403); return res.end(); }
  try {
    if ((await stat(file)).isDirectory()) file = join(file, 'index.html');
    const body = await readFile(file);
    res.writeHead(200, { 'content-type': TYPES[extname(file)] || 'application/octet-stream' });
    res.end(req.method === 'HEAD' ? undefined : body);
  } catch { res.writeHead(404, { 'content-type': 'text/html' }); res.end('<h1>404</h1>'); }
}).listen(port, () => console.log(`http://localhost:${port}${PREFIX}`));
