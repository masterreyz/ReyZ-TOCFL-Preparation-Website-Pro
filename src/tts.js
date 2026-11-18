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
  const now = synth.getVoices();
  if (now.length) return Promise.resolve(now); // re-read each time: Edge adds its online voices late
  if (voicesReady) return voicesReady;
  voicesReady = new Promise((resolve) => {
    const done = () => { voicesReady = null; resolve(synth.getVoices()); };
    synth.addEventListener?.('voiceschanged', done, { once: true });
    setTimeout(done, 1500); // some browsers never fire voiceschanged
  });
  return voicesReady;
}

// TOCFL recordings are read by Taiwanese Mandarin speakers (one male, one female voice), calmly and clearly.
// We therefore prefer zh-TW voices, the high-quality "Natural"/neural ones first, and give 男/女 their own voice.
const isZh = (v) => /^zh|^cmn/i.test(v.lang) || /Chinese|中文|國語|普通话|Mandarin/i.test(v.name);
const isTw = (v) => /^zh[-_]tw|^cmn[-_]hant[-_]tw/i.test(v.lang) || /台灣|臺灣|Taiwan/i.test(v.name);
const MALE = /YunJhe|Zhiwei|Yunxi|Yunyang|Yunjian|Yunxia|Kangkang|Li-?mu|Danny|\bmale\b|男/i;
const FEMALE = /HsiaoChen|HsiaoYu|Hanhan|Yating|Mei-?Jia|Xiaoxiao|Xiaoyi|Huihui|Yaoyao|Ting-?Ting|Sin-?ji|Google|female|女/i;
export const voiceGender = (v) => (MALE.test(v.name) && !/female/i.test(v.name) ? 'm' : FEMALE.test(v.name) ? 'f' : '?');
const rank = (v) => {
  const lang = v.lang.replace('_', '-').toLowerCase();
  let s = 0;
  if (isTw(v)) s += 100;
  else if (lang.startsWith('zh-cn') || lang === 'cmn-hans-cn') s += 50;
  else if (lang.startsWith('zh-hk')) s += 10; // Cantonese voices are a last resort
  if (/Natural|Neural/i.test(v.name)) s += 40;
  else if (/Online|Enhanced|Premium|Siri/i.test(v.name)) s += 30;
  else if (/Google/i.test(v.name)) s += 25;
  if (/compact/i.test(v.voiceURI || '')) s -= 15;
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
/** Voices per speaker: default (narrator), m (男), f (女). The other gender only gets its own voice
 *  when one with the same accent exists; otherwise the main voice is used with a light pitch change. */
export async function pickCast() {
  const list = await chineseVoices();
  const main = await pickVoice();
  if (!main) return null;
  const same = (v) => isTw(v) === isTw(main);
  const g = voiceGender(main);
  const best = (gender) => list.find((v) => v !== main && voiceGender(v) === gender && same(v));
  const m = g === 'm' ? main : best('m');
  const f = g === 'f' || g === '?' ? main : best('f');
  return { default: main, m: m || main, f: f || main, mShift: !m, fShift: !f };
}

export const DEFAULT_RATE = 0.85; // calm, exam-like pace

// Normalise text so the voice reads it as a TOCFL recording would.
function normalise(line) {
  return line
    .replace(/^\s*\d{1,2}\s*[.．、]\s*/, '')                       // list numbers ("1.") are not read aloud
    .replace(/[（(]\s*([A-F])\s*[）)]/g, '$1，')                   // (A) → A，
    .replace(/_{2,}|＿{2,}|[─—―]{1,2}|～/g, '，')                  // blanks and dashes → short pause
    .replace(/[「」『』《》〈〉【】]/g, '')
    .replace(/\s+/g, ' ')
    .replace(/[，,、\s]*([，,])[，,\s]*/g, '$1')
    .replace(/[，,]+$/, '')
    .trim();
}

// Split a script into speakable chunks: one per sentence, with the speaker and natural pauses.
export function toChunks(text) {
  const out = [];
  for (let line of String(text || '').split(/\n+/)) {
    line = line.trim();
    if (!line) continue;
    let who = null;
    const m = line.match(/^(男|女|甲|乙)\s*[:：]\s*|^(男|女)\s+/);
    if (m) { who = /男|甲/.test(m[0]) ? 'm' : 'f'; line = line.slice(m[0].length); }
    line = normalise(line);
    const sents = line.match(/[^。！？!?；;]+[。！？!?；;]*/g) || [line];
    sents.forEach((s, i) => {
      let t = s.trim();
      if (!t) return;
      // very long sentences are split at a comma: some voices stop after ~15 s
      const parts = t.length > 90 ? t.match(/[^，,]+(?:[，,]|$)/g).reduce((a, p) => {
        if (a.length && (a[a.length - 1] + p).length <= 60) a[a.length - 1] += p; else a.push(p); return a; }, []) : [t];
      parts.forEach((p, j) => out.push({ text: p.trim(), who, pause: j < parts.length - 1 ? 60 : i < sents.length - 1 ? 280 : 550 }));
    });
  }
  return out.filter((c) => c.text);
}

let session = 0;
export function stopTts() { session++; synth?.cancel(); }
window.addEventListener?.('hashchange', stopTts);

/** Speak a list of {text, who, pause} chunks. Resolves when done or stopped. */
export async function speakChunks(chunks, { rate, onChunk } = {}) {
  stopTts();
  const my = ++session;
  const cast = await pickCast();
  if (!cast) throw new Error('no-voice');
  const r = rate ?? store.get().prefs.speechRate ?? DEFAULT_RATE;
  for (let i = 0; i < chunks.length; i++) {
    if (my !== session) return false;
    onChunk?.(i);
    const c = chunks[i];
    const voice = c.who ? cast[c.who] : cast.default;
    await new Promise((resolve) => {
      const u = new SpeechSynthesisUtterance(c.text);
      u.voice = voice; u.lang = voice.lang; u.rate = r; u.volume = 1;
      u.pitch = c.who === 'm' && cast.mShift ? 0.9 : c.who === 'f' && cast.fShift ? 1.08 : 1;
      u.onend = u.onerror = () => resolve();
      synth.speak(u);
    });
    if (c.pause && my === session && i < chunks.length - 1) await new Promise((res) => setTimeout(res, c.pause));
  }
  return my === session;
}

/** Small "listen" button for a single word/line. */
export function SpeakButton(text, label = 'Dengarkan') {
  return h('button', { type: 'button', class: 'tts-mini', 'aria-label': `${label}: ${text}`, title: label,
    onclick: () => speakChunks(toChunks(text)).catch(() => alert(NO_VOICE)) }, '🔊');
}

export const NO_VOICE = 'Browser/perangkat ini belum memiliki suara Mandarin. Cara termudah: buka situs ini di Google Chrome atau Microsoft Edge (suara Mandarin online sudah tersedia). Atau pasang suara di sistem — Windows: Settings → Time & language → Speech → Add voices → "Chinese (Traditional, Taiwan)"; Android: Pengaturan → Text-to-speech → Google → bahasa Mandarin; iPhone/Mac: sudah tersedia. Lalu muat ulang halaman.';

/**
 * Player for synthesized speech. segments: [{ label, text, pause }] — each segment becomes one or more chunks.
 */
export function TtsPlayer(segments, opts = {}) {
  const status = h('div', { class: 'ap-status', role: 'status' });
  const now = h('div', { class: 'tts-now zh', lang: 'zh-Hant', 'aria-live': 'off' });
  const btn = h('button', { class: 'ap-btn', type: 'button', 'aria-label': 'Putar suara' }, '▶');
  const rate = h('select', { class: 'ap-speed', 'aria-label': 'Kecepatan suara', disabled: opts.exam || null },
    ...[0.7, 0.8, 0.85, 0.9, 1].map((r) => h('option', { value: r, selected: r === (opts.exam ? DEFAULT_RATE : (store.get().prefs.speechRate ?? DEFAULT_RATE)) || null }, r === DEFAULT_RATE ? `${r}× (standar)` : `${r}×`)));
  rate.addEventListener('change', () => store.setPref('speechRate', Number(rate.value)));
  let playing = false;
  const chunks = [];
  for (const seg of segments) {
    const cs = toChunks(seg.text);
    if (cs.length) { cs[cs.length - 1].pause = seg.pause ?? 900; cs.forEach((c) => (c.label = seg.label)); }
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
