// Mandarin speech synthesis via the browser's Web Speech API (no API key, no server, no audio files).
// Used when the original recordings are not hosted (e.g. on GitHub Pages). Voices come from the
// user's browser/OS: Chrome "Google 國語（臺灣）", Edge "Microsoft … (Taiwan)", iOS/macOS "Mei-Jia", Android Google TTS.
import { h } from './util.js';
import { store } from './store.js';

const synth = typeof window !== 'undefined' ? window.speechSynthesis : null;
export const ttsSupported = () => !!synth && typeof window.SpeechSynthesisUtterance === 'function';

let voicesReady = null;
export function getVoices() {
  if (!ttsSupported()) return Promise.resolve([]);
  if (voicesReady) return voicesReady;
  voicesReady = new Promise((resolve) => {
    const done = () => resolve(synth.getVoices());
    const v = synth.getVoices();
    if (v.length) return resolve(v);
    synth.addEventListener?.('voiceschanged', done, { once: true });
    setTimeout(done, 1500); // some browsers never fire voiceschanged
  });
  return voicesReady;
}

const isZh = (v) => /^zh|^cmn/i.test(v.lang) || /Chinese|中文|國語|普通话|Mandarin/i.test(v.name);
const rank = (v) => {
  const lang = v.lang.replace('_', '-').toLowerCase();
  let s = 0;
  if (lang === 'zh-tw' || /台灣|臺灣|Taiwan/i.test(v.name)) s += 100;
  else if (lang.startsWith('zh-cn') || lang === 'cmn-hans-cn') s += 50;
  else if (lang.startsWith('zh-hk')) s += 10; // Cantonese voices are a last resort
  if (/Natural|Online|Neural|Google/i.test(v.name)) s += 20;
  return s;
};
export async function chineseVoices() {
  return (await getVoices()).filter(isZh).sort((a, b) => rank(b) - rank(a));
}
export async function pickVoice() {
  const list = await chineseVoices();
  const want = store.get().prefs.ttsVoice;
  return list.find((v) => v.voiceURI === want) || list[0] || null;
}

// Split a script into speakable chunks: one per line/sentence, with speaker hints for pitch.
export function toChunks(text) {
  const out = [];
  for (let line of String(text || '').split(/\n+/)) {
    line = line.trim();
    if (!line) continue;
    let pitch = 1;
    const m = line.match(/^(男|女|甲|乙)\s*[:：]\s*|^(男|女)\s+/);
    if (m) { pitch = /男|甲/.test(m[0]) ? 0.8 : 1.2; line = line.slice(m[0].length); }
    line = line.replace(/[（(]\s*([A-F])\s*[）)]/g, '$1，').replace(/_{2,}|＿{2,}/g, '，');
    for (const s of line.match(/[^。！？!?；;]+[。！？!?；;]*/g) || [line]) {
      const t = s.trim();
      if (t) out.push({ text: t, pitch });
    }
  }
  return out;
}

let session = 0;
export function stopTts() { session++; synth?.cancel(); }
window.addEventListener?.('hashchange', stopTts);

/** Speak a list of {text,pitch} chunks. Resolves when done or stopped. */
export async function speakChunks(chunks, { rate, onChunk } = {}) {
  stopTts();
  const my = ++session;
  const voice = await pickVoice();
  if (!voice) throw new Error('no-voice');
  for (let i = 0; i < chunks.length; i++) {
    if (my !== session) return false;
    onChunk?.(i);
    await new Promise((resolve) => {
      const u = new SpeechSynthesisUtterance(chunks[i].text);
      u.voice = voice; u.lang = voice.lang; u.pitch = chunks[i].pitch ?? 1;
      u.rate = rate ?? store.get().prefs.ttsRate ?? 0.9;
      u.onend = u.onerror = () => resolve();
      synth.speak(u);
    });
    if (chunks[i].pause && my === session) await new Promise((r) => setTimeout(r, chunks[i].pause));
  }
  return my === session;
}

/** Small "listen" button for a single word/line. */
export function SpeakButton(text, label = 'Dengarkan') {
  return h('button', { type: 'button', class: 'tts-mini', 'aria-label': `${label}: ${text}`, title: label,
    onclick: () => speakChunks(toChunks(text)).catch(() => alert(NO_VOICE)) }, '🔊');
}

export const NO_VOICE = 'Browser ini tidak memiliki suara Mandarin. Gunakan Chrome atau Edge terbaru, atau pasang paket bahasa "Chinese (Taiwan)" di pengaturan sistem, lalu muat ulang halaman.';

/**
 * Player for synthesized speech. segments: [{ label, text, pause }] — each segment becomes one or more chunks.
 */
export function TtsPlayer(segments, opts = {}) {
  const status = h('div', { class: 'ap-status', role: 'status' });
  const now = h('div', { class: 'tts-now zh', lang: 'zh-Hant', 'aria-live': 'off' });
  const btn = h('button', { class: 'ap-btn', type: 'button', 'aria-label': 'Putar suara' }, '▶');
  const rate = h('select', { class: 'ap-speed', 'aria-label': 'Kecepatan suara', disabled: opts.exam || null },
    ...[0.6, 0.75, 0.9, 1, 1.15].map((r) => h('option', { value: r, selected: r === (store.get().prefs.ttsRate ?? 0.9) || null }, `${r}×`)));
  rate.addEventListener('change', () => store.setPref('ttsRate', Number(rate.value)));
  let playing = false;
  const chunks = [];
  for (const seg of segments) {
    const cs = toChunks(seg.text);
    if (cs.length) { cs[cs.length - 1].pause = seg.pause ?? 600; cs.forEach((c) => (c.label = seg.label)); }
    chunks.push(...cs);
  }
  const setPlaying = (p) => { playing = p; btn.textContent = p ? '■' : '▶'; btn.setAttribute('aria-label', p ? 'Hentikan suara' : 'Putar suara'); if (!p) now.textContent = ''; };
  btn.addEventListener('click', async () => {
    if (playing) { stopTts(); setPlaying(false); return; }
    if (!ttsSupported()) { status.textContent = NO_VOICE; return; }
    if (!chunks.length) { status.textContent = 'Tidak ada teks untuk dibacakan.'; return; }
    setPlaying(true); status.textContent = '';
    try {
      await speakChunks(chunks, { rate: Number(rate.value), onChunk: (i) => { if (!opts.hideText) now.textContent = chunks[i].text; } });
    } catch { status.textContent = NO_VOICE; }
    setPlaying(false);
  });
  return h('div', { class: 'audio-player tts' + (opts.compact ? ' compact' : ''), role: 'group', 'aria-label': opts.title || 'Suara sintetis' },
    h('div', { class: 'ap-title' }, (opts.title ? opts.title + ' — ' : '') + 'suara sintetis (TTS)'),
    h('div', { class: 'ap-row' }, btn, h('span', { class: 'ap-time' }, `${chunks.length} kalimat`), rate),
    now, status);
}
