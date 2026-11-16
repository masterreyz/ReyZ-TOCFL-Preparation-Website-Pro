import { h, getJson, mediaUrl } from '../util.js';
import { t } from '../i18n.js';
import { store } from '../store.js';
import { AudioPlayer } from '../audio.js';
import { progressBar } from './home.js';

const bookIdOf = (lessonId) => lessonId.split('-l')[0];
const lessonTitle = (l) => `Pelajaran ${l.n}${l.title ? ' · ' + l.title : ''}`;
const KIND = { textbook: 'Textbook 課本', workbook: 'Workbook 作業本' };

export async function studyHome() {
  const idx = await getJson('content/study/index.json');
  return h('div', { class: 'wrap' },
    h('nav', { class: 'crumbs' }, h('a', { href: '#/' }, 'Beranda'), ' / TOCFL Study'),
    h('h1', {}, 'TOCFL Study'),
    h('p', { class: 'lead' }, 'Materi 當代中文課程 (A Course in Contemporary Chinese) jilid 1–6, disusun per level → buku → pelajaran, dengan audio pelajaran di samping halaman yang sesuai.'),
    migrationNote(idx),
    h('div', { class: 'tiles' }, ...idx.levels.map((lv) => {
      const ids = lv.books.flatMap((b) => b.lessons.map((l) => l.id));
      const done = ids.filter((id) => store.isCompleted(id)).length;
      return h('a', { class: 'tile', href: `#/study/${lv.id}` }, h('span', { class: 'tile-big' }, lv.label), h('span', { class: 'tile-sub' }, `當代中文課程 第${'一二三四五六'[lv.vol - 1]}冊`),
        progressBar(done, ids.length), h('span', { class: 'tile-meta' }, `${lv.books.length} buku · ${done}/${ids.length} selesai`));
    })));
}

function migrationNote(idx) {
  const all = idx.levels.flatMap((lv) => lv.books.flatMap((b) => b.lessons));
  const mig = all.filter((l) => l.migrated).length;
  return h('p', { class: 'note' }, `Status migrasi: ${mig} dari ${all.length} pelajaran sudah tersedia sebagai teks web terstruktur. Pelajaran lain sementara ditampilkan sebagai halaman asli buku (gambar) dengan audio yang terhubung, sampai migrasi teksnya selesai.`);
}

export async function levelView({ level }) {
  const idx = await getJson('content/study/index.json');
  const lv = idx.levels.find((x) => x.id === level);
  if (!lv) throw new Error('Level tidak ditemukan');
  return h('div', { class: 'wrap' },
    h('nav', { class: 'crumbs' }, h('a', { href: '#/study' }, 'TOCFL Study'), ` / ${lv.label}`),
    h('h1', {}, `Level ${lv.label} — 當代中文課程 ${lv.vol}`),
    h('div', { class: 'grid-2' }, ...lv.books.map((b) => h('section', { class: 'card' },
      h('h2', {}, KIND[b.kind]), h('p', { class: 'muted small' }, `${b.pages} halaman · ${b.lessons.length} pelajaran`),
      h('ol', { class: 'lesson-list' }, ...b.lessons.map((l) => h('li', {},
        h('a', { href: `#/lesson/${l.id}` }, lessonTitle(l)),
        l.migrated ? h('span', { class: 'pill good' }, 'Teks') : h('span', { class: 'pill ghost' }, 'Halaman asli'),
        store.isCompleted(l.id) ? h('span', { class: 'pill' }, '✓ ' + t('completed')) : null))),
      h('a', { class: 'small', href: `#/book/${b.id}` }, 'Daftar isi lengkap & semua halaman →')))));
}

export async function bookView({ book }) {
  const b = await getJson(`content/study/${book}.json`);
  const lvId = b.level;
  const range = (r, label) => r ? h('li', {}, h('a', { href: `#/page/${b.id}/${r.start}` }, label), h('span', { class: 'muted' }, ` · hlm. PDF ${r.start}–${r.end}`)) : null;
  return h('div', { class: 'wrap narrow' },
    h('nav', { class: 'crumbs' }, h('a', { href: '#/study' }, 'TOCFL Study'), ' / ', h('a', { href: `#/study/${lvId}` }, lvId.toUpperCase()), ` / ${b.label}`),
    h('h1', {}, `${lvId.toUpperCase()} ${b.label}`),
    h('p', { class: 'muted' }, `${b.pages} halaman · ${b.audioFiles} file audio`),
    h('section', { class: 'card' }, h('h2', {}, 'Daftar isi'),
      h('ul', { class: 'toc' }, range(b.frontMatter, 'Bagian depan (kata pengantar, pendahuluan, daftar isi)'),
        ...b.lessons.map((l) => h('li', {}, h('a', { href: `#/lesson/${l.id}` }, `Pelajaran ${l.n}${l.titleOcr ? ' · ' + l.titleOcr : ''}`), h('span', { class: 'muted' }, ` · hlm. ${l.start}–${l.end} · ${l.tracks.length} audio`))),
        range(b.backMatter, 'Bagian belakang (lampiran, indeks)'))),
    b.otherTracks?.length ? h('section', { class: 'card' }, h('h2', { class: 'h3' }, 'Audio lain'), AudioPlayer(b.otherTracks.map((x) => ({ src: x.src, label: x.label || x.file })), { title: 'Audio umum' })) : null);
}

export async function lessonView({ lesson }) {
  const book = await getJson(`content/study/${bookIdOf(lesson)}.json`);
  const i = book.lessons.findIndex((l) => l.id === lesson);
  const l = book.lessons[i];
  if (!l) throw new Error('Pelajaran tidak ditemukan');
  const title = `${book.level.toUpperCase()} ${book.kind === 'textbook' ? 'Textbook' : 'Workbook'} · ${lessonTitle({ n: l.n, title: l.titleOcr })}`;
  store.visitLesson(lesson, title, `#/lesson/${lesson}`);
  let migrated = null;
  if (l.migrated) migrated = await getJson(`content/study/lessons/${lesson}.json`).catch(() => null);
  const prev = book.lessons[i - 1], next = book.lessons[i + 1];
  const done = h('button', { class: 'btn' + (store.isCompleted(lesson) ? ' on' : ''), type: 'button', 'aria-pressed': String(store.isCompleted(lesson)),
    onclick: (e) => { const v = !store.isCompleted(lesson); store.setCompleted(lesson, v); e.currentTarget.classList.toggle('on', v); e.currentTarget.setAttribute('aria-pressed', String(v)); e.currentTarget.textContent = v ? '✓ ' + t('completed') : t('markComplete'); } },
    store.isCompleted(lesson) ? '✓ ' + t('completed') : t('markComplete'));
  const bmKey = `lesson:${lesson}`;
  const bm = h('button', { class: 'btn ghost', type: 'button', onclick: (e) => { const on = store.toggleBookmark(bmKey, { type: 'lesson', title, href: `#/lesson/${lesson}` }); e.currentTarget.textContent = on ? '★ ' + t('bookmarked') : '☆ ' + t('bookmark'); } },
    store.isBookmarked(bmKey) ? '★ ' + t('bookmarked') : '☆ ' + t('bookmark'));
  const size = (d) => () => { const v = Math.min(1.6, Math.max(0.8, Math.round((store.get().prefs.fontScale + d) * 10) / 10)); store.setPref('fontScale', v); document.documentElement.style.setProperty('--reading-scale', v); };
  const toolbar = h('div', { class: 'lesson-tools' }, done, bm,
    h('span', { class: 'font-ctl', role: 'group', 'aria-label': 'Ukuran teks' }, h('button', { class: 'btn ghost', type: 'button', onclick: size(-0.1), 'aria-label': 'Perkecil teks' }, 'A−'), h('button', { class: 'btn ghost', type: 'button', onclick: size(0.1), 'aria-label': 'Perbesar teks' }, 'A+')));
  const navLinks = h('nav', { class: 'lesson-nav', 'aria-label': 'Navigasi pelajaran' },
    prev ? h('a', { class: 'btn', href: `#/lesson/${prev.id}` }, `← Pelajaran ${prev.n}`) : h('span', {}),
    h('a', { class: 'btn ghost', href: `#/book/${book.id}` }, 'Daftar isi'),
    next ? h('a', { class: 'btn', href: `#/lesson/${next.id}` }, `Pelajaran ${next.n} →`) : h('span', {}));
  const allAudio = l.tracks.length ? h('details', { class: 'card' }, h('summary', {}, `Semua audio pelajaran ini (${l.tracks.length})`),
    AudioPlayer(l.tracks.map((x) => ({ src: x.src, label: x.label })), { title: `Audio Pelajaran ${l.n}` })) : null;
  const body = migrated ? renderMigrated(migrated, l, book) : renderPages(book, l);
  return h('div', { class: 'wrap reading' },
    h('nav', { class: 'crumbs' }, h('a', { href: '#/study' }, 'TOCFL Study'), ' / ', h('a', { href: `#/study/${book.level}` }, book.level.toUpperCase()), ' / ', h('a', { href: `#/book/${book.id}` }, book.label), ` / Pelajaran ${l.n}`),
    h('h1', {}, title), toolbar, allAudio, body, navLinks);
}

function trackFor(l, label) {
  return l.tracks.find((x) => x.label === label);
}

function renderPages(book, l) {
  const pages = [];
  for (let p = l.start; p <= l.end; p++) pages.push(p);
  return h('div', {},
    h('p', { class: 'note' }, l.titleOcr ? '' : 'Judul pelajaran ini belum terverifikasi. ',
      'Pelajaran ini belum dimigrasi menjadi teks web; sementara ditampilkan sebagai halaman asli buku. Audio ditempatkan di halaman tempat nomor treknya tercetak.'),
    ...pages.map((p) => {
      const tr = l.tracks.filter((x) => x.page === p);
      return h('figure', { class: 'page', id: `p${p}` },
        tr.length ? h('div', { class: 'page-audio' }, ...tr.map((x) => AudioPlayer([{ src: x.src, label: `Trek ${x.label}` }], { compact: true }))) : null,
        h('img', { src: mediaUrl(`study/${book.id}/p${String(p).padStart(3, '0')}.webp`), alt: `${book.level.toUpperCase()} ${book.label}, halaman PDF ${p}`, loading: 'lazy', width: 1100, height: 1480 }),
        h('figcaption', { class: 'muted small' }, `Halaman PDF ${p}`));
    }));
}

// ---- structured (migrated) lesson rendering
function renderMigrated(m, l, book) {
  const showPy = store.get().prefs.showPinyin;
  const pyToggle = h('label', { class: 'small' }, h('input', { type: 'checkbox', checked: showPy || null, onchange: (e) => { store.setPref('showPinyin', e.target.checked); document.querySelectorAll('.py').forEach((x) => (x.hidden = !e.target.checked)); } }), ' Tampilkan pinyin');
  const blocks = m.blocks.map((b) => {
    const tr = b.track ? trackFor(l, b.track) : null;
    const player = tr ? AudioPlayer([{ src: tr.src, label: `Trek ${tr.label}` }], { compact: true }) : null;
    const src = b.source ? h('p', { class: 'src muted small' }, `Sumber: ${book.label}, hlm. PDF ${b.source.pages.join(', ')}`) : null;
    switch (b.type) {
      case 'heading': return h(b.level === 3 ? 'h3' : 'h2', { class: 'block-h', id: b.id }, b.zh ? h('span', { lang: 'zh-Hant' }, b.zh + ' ') : null, b.en || '');
      case 'dialogue': return h('section', { class: 'block dialogue', id: b.id },
        b.title ? h('h3', {}, b.title) : null, player,
        h('div', { class: 'dlg' }, ...b.lines.map((ln) => h('div', { class: 'dlg-line' },
          h('span', { class: 'spk', lang: 'zh-Hant' }, ln.spk ? ln.spk : ''),
          h('div', {}, h('p', { class: 'zh', lang: 'zh-Hant' }, ln.zh), h('p', { class: 'py', lang: 'zh-Latn-pinyin', hidden: !showPy || null }, ln.py))))),
        b.translation ? h('details', { class: 'trans' }, h('summary', {}, 'Terjemahan bahasa Inggris (dari buku)'),
          h('dl', {}, ...b.translation.flatMap((x) => [h('dt', {}, x.spk), h('dd', { lang: 'en' }, x.en)]))) : null, src);
      case 'vocab': return h('section', { class: 'block', id: b.id }, b.title ? h('h3', {}, b.title) : null, player,
        h('div', { class: 'table-wrap' }, h('table', { class: 'table vocab' },
          h('thead', {}, h('tr', {}, h('th', { scope: 'col' }, 'No.'), h('th', { scope: 'col' }, '詞'), h('th', { scope: 'col', class: 'py-col' }, 'Pinyin'), h('th', { scope: 'col' }, 'Kelas kata'), h('th', { scope: 'col' }, 'Arti (Inggris)'))),
          h('tbody', {}, ...b.items.map((v) => h('tr', {}, h('td', {}, v.n ?? ''), h('td', { class: 'zh', lang: 'zh-Hant' }, v.zh), h('td', { class: 'py-col', lang: 'zh-Latn-pinyin' }, v.py), h('td', {}, v.pos || ''), h('td', { lang: 'en' }, v.en))))) ), src);
      case 'text': return h('section', { class: 'block', id: b.id }, b.title ? h('h3', {}, b.title) : null, player,
        ...(b.paras || []).map((p) => h('p', { class: p.lang === 'en' ? '' : 'zh', lang: p.lang === 'en' ? 'en' : 'zh-Hant' }, p.text)), src);
      case 'note': return h('aside', { class: 'note', id: b.id }, b.text);
      default: return null;
    }
  });
  return h('div', { class: 'migrated' },
    h('p', { class: 'note good-note' }, m.status === 'complete' ? 'Seluruh isi pelajaran ini sudah dimigrasi menjadi teks web.' : `Sebagian pelajaran ini sudah dimigrasi menjadi teks web (${m.statusDetail}). Bagian lain dapat dibuka sebagai halaman asli di bawah.`),
    pyToggle, ...blocks,
    m.status !== 'complete' ? h('details', { class: 'card' }, h('summary', {}, 'Halaman asli pelajaran ini (bagian yang belum dimigrasi)'), renderPages(book, l)) : null);
}

export async function pageView({ book, page }) {
  const b = await getJson(`content/study/${book}.json`);
  const p = Math.max(1, Math.min(b.pages, Number(page) || 1));
  store.update((s) => { s.pagesSeen[book] = p; });
  const l = b.lessons.find((x) => p >= x.start && p <= x.end);
  const tr = l ? l.tracks.filter((x) => x.page === p) : [];
  const go = (n) => h('a', { class: 'btn', href: `#/page/${book}/${n}` }, n < p ? '← Halaman sebelumnya' : 'Halaman berikutnya →');
  return h('div', { class: 'wrap reading' },
    h('nav', { class: 'crumbs' }, h('a', { href: '#/study' }, 'TOCFL Study'), ' / ', h('a', { href: `#/book/${book}` }, `${b.level.toUpperCase()} ${b.label}`), ` / hlm. ${p}`),
    h('h1', { class: 'h2' }, `${b.level.toUpperCase()} ${b.label} — halaman PDF ${p} dari ${b.pages}`),
    l ? h('p', {}, h('a', { href: `#/lesson/${l.id}` }, `Bagian dari Pelajaran ${l.n}`)) : null,
    h('div', { class: 'lesson-nav' }, p > 1 ? go(p - 1) : h('span', {}), p < b.pages ? go(p + 1) : h('span', {})),
    tr.length ? h('div', { class: 'page-audio' }, ...tr.map((x) => AudioPlayer([{ src: x.src, label: `Trek ${x.label}` }], { compact: true }))) : null,
    h('figure', { class: 'page' }, h('img', { src: mediaUrl(`study/${book}/p${String(p).padStart(3, '0')}.webp`), alt: `Halaman PDF ${p}` })),
    h('div', { class: 'lesson-nav' }, p > 1 ? go(p - 1) : h('span', {}), p < b.pages ? go(p + 1) : h('span', {})));
}
