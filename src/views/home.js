import { h, getJson, fmtDate, pct } from '../util.js';
import { t, BAND_LABEL, BAND_DESC } from '../i18n.js';
import { store } from '../store.js';

export async function homeView() {
  const [study, tests] = await Promise.all([getJson('content/study/index.json'), getJson('content/exercise/index.json')]);
  const s = store.get();
  const last = s.lastLesson;
  const attempts = [...s.attempts].sort((a, b) => b.submittedAt - a.submittedAt).slice(0, 5);
  const inProg = Object.entries(s.inProgress);
  const bookmarks = Object.keys(s.bookmarks).length;
  const mistakes = countMistakes(s.attempts);

  const levelCards = study.levels.map((lv) => {
    const ids = lv.books.flatMap((b) => b.lessons.map((l) => l.id));
    const done = ids.filter((id) => store.isCompleted(id)).length;
    return h('a', { class: 'tile', href: `#/study/${lv.id}` },
      h('span', { class: 'tile-big' }, lv.label), h('span', { class: 'tile-sub' }, `當代中文課程 ${lv.vol}`),
      progressBar(done, ids.length), h('span', { class: 'tile-meta' }, `${done}/${ids.length} pelajaran selesai`));
  });
  const bandCards = ['novice', 'a', 'b', 'c'].map((b) => {
    const list = tests.filter((x) => x.band === b);
    const doneIds = new Set(s.attempts.map((a) => a.testId));
    return h('a', { class: 'tile', href: `#/exercise/${b}` },
      h('span', { class: 'tile-big' }, BAND_LABEL[b]), h('span', { class: 'tile-sub' }, BAND_DESC[b]),
      progressBar(list.filter((x) => doneIds.has(x.id)).length, list.length),
      h('span', { class: 'tile-meta' }, `${list.length} tes (${list.filter((x) => x.skill === 'listening').length} listening, ${list.filter((x) => x.skill === 'reading').length} reading)`));
  });

  return h('div', { class: 'wrap' },
    h('section', { class: 'hero' },
      h('div', {},
        h('p', { class: 'eyebrow' }, 'Belajar Mandarin Tradisional untuk TOCFL'),
        h('h1', {}, t('siteTitle')),
        h('p', { class: 'lead' }, 'Satu tempat untuk mempelajari materi A1–C2, mendengarkan audio pelajaran, dan berlatih soal listening & reading TOCFL dari Band Novice sampai Band C — lengkap dengan penilaian, transkrip, dan ulasan kesalahan.'),
        h('div', { class: 'cta' },
          h('a', { class: 'btn primary', href: '#/study' }, 'Buka TOCFL Study'),
          h('a', { class: 'btn', href: '#/exercise' }, 'Buka TOCFL Exercise')),
        h('p', { class: 'sig hero-sig' }, t('createdBy'))),
      h('div', { class: 'hero-side', 'aria-hidden': 'true' }, h('span', {}, '學'), h('span', {}, '中'), h('span', {}, '文'))),

    h('section', { class: 'grid-2' },
      h('div', { class: 'card' },
        h('h2', {}, t('continue')),
        last ? h('a', { class: 'continue', href: last.href }, h('strong', {}, last.title), h('span', { class: 'muted' }, fmtDate(last.ts)))
          : h('p', { class: 'muted' }, 'Belum ada pelajaran yang dibuka. Mulai dari A1 Pelajaran 1.'),
        inProg.length ? h('div', {}, h('h3', {}, 'Tes yang belum selesai'),
          h('ul', { class: 'plain' }, ...inProg.map(([id, p]) => {
            const meta = tests.find((x) => x.id === id);
            return h('li', {}, h('a', { href: p.href || `#/test/${id}/run?mode=${p.mode}` }, p.title || meta?.title || id), h('span', { class: 'muted' }, ` — ${Object.keys(p.answers || {}).length} jawaban tersimpan`));
          }))) : null),
      h('div', { class: 'card' },
        h('h2', {}, 'Hasil latihan terbaru'),
        attempts.length ? h('ul', { class: 'plain results' }, ...attempts.map((a) => h('li', {},
          h('a', { href: `#/result/${a.id}` }, a.title), h('span', { class: `score ${scoreClass(a)}` }, `${a.score.correct}/${a.score.gradable} · ${pct(a.score.correct, a.score.gradable)}%`))))
          : h('p', { class: 'muted' }, 'Belum ada tes yang dikumpulkan.'),
        h('div', { class: 'row-links' },
          h('a', { href: '#/mistakes' }, `Ulas kesalahan (${mistakes})`), h('a', { href: '#/bookmarks' }, `Penanda (${bookmarks})`), h('a', { href: '#/history' }, 'Riwayat lengkap')))),

    h('section', {}, h('h2', {}, 'TOCFL Study — pilih level'), h('div', { class: 'tiles' }, ...levelCards)),
    h('section', {}, h('h2', {}, 'TOCFL Exercise — pilih band'), h('div', { class: 'tiles' }, ...bandCards)),
    h('p', { class: 'note' }, t('localOnly')));
}

export function progressBar(a, b) {
  const p = b ? Math.round((a / b) * 100) : 0;
  return h('span', { class: 'bar', role: 'progressbar', 'aria-valuenow': p, 'aria-valuemin': 0, 'aria-valuemax': 100, 'aria-label': `${p}%` }, h('span', { style: `width:${p}%` }));
}
export const scoreClass = (a) => { const p = pct(a.score.correct, a.score.gradable); return p >= 80 ? 'good' : p >= 50 ? 'mid' : 'low'; };

export function countMistakes(attempts) {
  const latest = new Map();
  for (const a of attempts) { const k = (a.testId + (a.range ? `@${a.range.from}-${a.range.to}` : '')); if (!latest.has(k) || latest.get(k).submittedAt < a.submittedAt) latest.set(k, a); }
  let n = 0;
  for (const a of latest.values()) n += a.results.filter((r) => r.status === 'incorrect' || r.status === 'unanswered').length;
  return n;
}
