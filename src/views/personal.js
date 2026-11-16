import { h, getJson, fmtDate, fmtTime } from '../util.js';
import { t } from '../i18n.js';
import { store } from '../store.js';
import { questionBody } from './exercise.js';
import { scoreClass } from './home.js';
import { chineseVoices, speakChunks, toChunks, ttsSupported, NO_VOICE } from '../tts.js';

export async function mistakesView(_, query) {
  const s = store.get();
  const latest = new Map();
  for (const a of s.attempts) if (!latest.has(a.testId) || latest.get(a.testId).submittedAt < a.submittedAt) latest.set(a.testId, a);
  const groups = [...latest.values()].map((a) => ({ a, wrong: a.results.filter((r) => r.status === 'incorrect' || r.status === 'unanswered') })).filter((g) => g.wrong.length);
  const only = query.get('test');
  const shown = only ? groups.filter((g) => g.a.testId === only) : groups;
  const sections = [];
  for (const g of shown.slice(0, only ? 1 : 50)) {
    const test = await getJson(`content/exercise/${g.a.testId}.json`);
    sections.push(h('section', { class: 'card' },
      h('h2', { class: 'h3' }, h('a', { href: `#/result/${g.a.id}` }, g.a.title), h('span', { class: 'muted small' }, ` · percobaan terakhir ${fmtDate(g.a.submittedAt)} · ${g.wrong.length} soal salah/kosong`)),
      only ? h('div', {}, ...g.wrong.map((r) => {
        const q = test.questions.find((x) => x.n === r.n);
        return h('div', { class: 'review-mini' }, h('h3', {}, `Soal ${q.n} — jawaban Anda ${r.given ? '(' + r.given + ')' : '—'}, benar (${q.answer})`), questionBody(test, q, { review: true, result: r }));
      })) : h('p', {}, h('a', { href: `#/mistakes?test=${g.a.testId}` }, 'Ulas soal-soal ini →'), ' · ', h('a', { href: `#/test/${g.a.testId}/run?mode=practice` }, 'Kerjakan ulang tes'))));
  }
  return h('div', { class: 'wrap' },
    h('h1', {}, 'Ulas Kesalahan'),
    h('p', { class: 'muted' }, 'Menampilkan soal yang salah atau tidak dijawab pada percobaan terakhir setiap tes. Percobaan lama tetap tersimpan di Riwayat.'),
    only ? h('p', {}, h('a', { href: '#/mistakes' }, '← Semua tes')) : null,
    sections.length ? sections : h('p', { class: 'card' }, 'Belum ada kesalahan untuk diulas. Kerjakan tes di TOCFL Exercise terlebih dulu.'));
}

export async function bookmarksView() {
  const b = Object.entries(store.get().bookmarks).sort((x, y) => y[1].ts - x[1].ts);
  return h('div', { class: 'wrap narrow' }, h('h1', {}, 'Penanda'),
    b.length ? h('ul', { class: 'card plain bm' }, ...b.map(([k, v]) => h('li', {},
      h('span', { class: 'pill ghost' }, v.type === 'lesson' ? 'Pelajaran' : 'Soal'), ' ', h('a', { href: v.href }, v.title),
      h('button', { class: 'btn ghost small', type: 'button', onclick: (e) => { store.toggleBookmark(k); e.currentTarget.closest('li').remove(); } }, 'Hapus'))))
      : h('p', { class: 'card' }, 'Belum ada penanda. Gunakan tombol ☆ Tandai di halaman pelajaran atau ulasan soal.'));
}

export async function historyView() {
  const atts = [...store.get().attempts].sort((a, b) => b.submittedAt - a.submittedAt);
  return h('div', { class: 'wrap' }, h('h1', {}, 'Riwayat Percobaan'),
    atts.length ? h('div', { class: 'table-wrap card' }, h('table', { class: 'table' },
      h('thead', {}, h('tr', {}, ...['Tanggal', 'Tes', 'Mode', 'Skor', 'Durasi', ''].map((x) => h('th', { scope: 'col' }, x)))),
      h('tbody', {}, ...atts.map((a) => h('tr', {}, h('td', {}, fmtDate(a.submittedAt)), h('td', {}, a.title), h('td', {}, a.mode === 'exam' ? 'Simulasi' : 'Latihan'),
        h('td', {}, h('span', { class: `score ${scoreClass(a)}` }, `${a.score.correct}/${a.score.gradable} · ${a.score.percent}%`)), h('td', {}, fmtTime(a.durationSec)),
        h('td', {}, h('a', { href: `#/result/${a.id}` }, 'Lihat'), ' · ', h('a', { href: `#/test/${a.testId}/run?mode=${a.mode}` }, 'Ulangi')))))))
      : h('p', { class: 'card' }, 'Belum ada tes yang dikumpulkan.'));
}

export async function settingsView() {
  const s = store.get();
  const file = h('input', { type: 'file', accept: 'application/json', id: 'imp' });
  const msg = h('p', { role: 'status', class: 'small' });
  file.addEventListener('change', async () => {
    try { store.importJson(await file.files[0].text()); msg.textContent = 'Progres berhasil diimpor.'; }
    catch (e) { msg.textContent = 'Gagal mengimpor: ' + e.message; }
  });
  const exp = () => {
    const blob = new Blob([store.exportJson()], { type: 'application/json' });
    const a = h('a', { href: URL.createObjectURL(blob), download: `reyz-tocfl-progress-${new Date().toISOString().slice(0, 10)}.json` });
    document.body.append(a); a.click(); a.remove();
  };
  const theme = h('select', { id: 'theme', onchange: (e) => { store.setPref('theme', e.target.value); location.reload(); } },
    ...[['auto', 'Ikuti sistem'], ['light', 'Terang'], ['dark', 'Gelap']].map(([v, l]) => h('option', { value: v, selected: s.prefs.theme === v || null }, l)));
  return h('div', { class: 'wrap narrow' }, h('h1', {}, 'Pengaturan & Progres'),
    h('p', { class: 'note' }, t('localOnly')),
    !store.ok() ? h('p', { class: 'note error' }, 'Penyimpanan browser tidak tersedia (mode privat atau penuh). Progres tidak akan tersimpan.') : null,
    h('section', { class: 'card' }, h('h2', { class: 'h3' }, 'Tampilan'), h('label', { for: 'theme' }, 'Tema: '), theme),
    await voiceSection(),
    h('section', { class: 'card' }, h('h2', { class: 'h3' }, 'Ekspor / impor progres'),
      h('p', { class: 'small' }, `${s.attempts.length} percobaan tes · ${Object.values(s.lessons).filter((x) => x.completed).length} pelajaran selesai · ${Object.keys(s.bookmarks).length} penanda`),
      h('button', { class: 'btn', type: 'button', onclick: exp }, 'Ekspor progres (.json)'), ' ',
      h('label', { class: 'btn ghost', for: 'imp' }, 'Impor progres…'), file, msg),
    h('section', { class: 'card' }, h('h2', { class: 'h3' }, 'Reset'),
      h('p', { class: 'small' }, 'Menghapus seluruh progres, riwayat, dan penanda di browser ini.'),
      h('button', { class: 'btn danger', type: 'button', onclick: () => { if (confirm('Hapus SEMUA progres di browser ini? Tindakan ini tidak dapat dibatalkan.')) { store.reset(); location.hash = '#/'; } } }, 'Reset progres')));
}

async function voiceSection() {
  const msg = h('p', { class: 'small', role: 'status' });
  const voices = ttsSupported() ? await chineseVoices() : [];
  const cur = store.get().prefs.ttsVoice;
  const sel = h('select', { id: 'voice', onchange: (e) => store.setPref('ttsVoice', e.target.value || null) },
    h('option', { value: '' }, 'Otomatis (utamakan Mandarin Taiwan)'),
    ...voices.map((v) => h('option', { value: v.voiceURI, selected: v.voiceURI === cur || null }, `${v.name} (${v.lang})`)));
  const test = h('button', { class: 'btn', type: 'button', onclick: () => speakChunks(toChunks('你好！歡迎你來臺灣。我們一起學中文吧。')).catch(() => { msg.textContent = NO_VOICE; }) }, '🔊 Tes suara');
  return h('section', { class: 'card' }, h('h2', { class: 'h3' }, 'Suara Mandarin (TTS)'),
    h('p', { class: 'small muted' }, 'Suara sintetis memakai mesin suara bawaan browser/perangkat Anda (Web Speech API) — gratis, tanpa unduhan tambahan. Kualitas terbaik: Microsoft Edge (suara “Natural” Taiwan) atau Google Chrome (“Google 國語（臺灣）”).'),
    voices.length ? h('div', {}, h('label', { for: 'voice' }, 'Suara: '), sel, ' ', test) : h('p', { class: 'note' }, NO_VOICE), msg);
}
