// Small DOM + data helpers. All imported text is inserted via textContent / escaped, never raw HTML.
export const $ = (sel, root = document) => root.querySelector(sel);

export function esc(s) {
  return String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

// Preserve line breaks of escaped text.
export const escBr = (s) => esc(s).replace(/\n/g, '<br>');

export function h(tag, attrs = {}, ...children) {
  const el = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs || {})) {
    if (v == null || v === false) continue;
    if (k === 'class') el.className = v;
    else if (k === 'html') el.innerHTML = v;
    else if (k.startsWith('on')) el.addEventListener(k.slice(2), v);
    else el.setAttribute(k, v === true ? '' : v);
  }
  for (const c of children.flat()) {
    if (c == null || c === false) continue;
    el.append(c instanceof Node ? c : document.createTextNode(String(c)));
  }
  return el;
}

const cache = new Map();
export async function getJson(path) {
  if (cache.has(path)) return cache.get(path);
  const p = fetch(new URL(path, document.baseURI)).then((r) => {
    if (!r.ok) throw new Error(`${r.status} ${path}`);
    return r.json();
  });
  cache.set(path, p);
  p.catch(() => cache.delete(path));
  return p;
}

export const mediaUrl = (p) => (window.REYZ_CONFIG?.mediaBase || './media/') + p.split('/').map(encodeURIComponent).join('/');
export const audioUrl = (p) => (window.REYZ_CONFIG?.audioBase || './media/audio/') + p.split('/').map(encodeURIComponent).join('/');

export function fmtTime(sec) {
  if (!isFinite(sec)) return '--:--';
  sec = Math.max(0, Math.round(sec));
  const m = Math.floor(sec / 60), s = sec % 60;
  return `${m}:${String(s).padStart(2, '0')}`;
}

export const fmtDate = (ts) => new Date(ts).toLocaleString('id-ID', { dateStyle: 'medium', timeStyle: 'short' });
export const pct = (a, b) => (b ? Math.round((a / b) * 1000) / 10 : 0);
export const uid = () => Date.now().toString(36) + Math.random().toString(36).slice(2, 7);

export function parseHash() {
  const raw = location.hash.replace(/^#\/?/, '');
  const [path, qs] = raw.split('?');
  return { parts: path.split('/').filter(Boolean).map(decodeURIComponent), query: new URLSearchParams(qs || '') };
}
