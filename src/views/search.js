import { h, getJson } from '../util.js';

// Pinyin-insensitive matching: strip tone marks / tone numbers and spaces.
const fold = (s) => String(s || '').normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/ü/g, 'v').toLowerCase().replace(/[1-5\s'’·]/g, '');

export async function searchView(_, query) {
  const idx = await getJson('content/search.json');
  const q = query.get('q') || '';
  const level = query.get('level') || '';
  const type = query.get('type') || '';
  const input = h('input', { type: 'search', name: 'q', value: q, placeholder: 'Cari: 茶, chá, cha, "Oolong", 你好…', 'aria-label': 'Kata kunci pencarian', autofocus: true });
  const lv = h('select', { name: 'level', 'aria-label': 'Filter level' }, h('option', { value: '' }, 'Semua level / band'),
    ...['a1', 'a2', 'b1', 'b2', 'c1', 'c2', 'novice', 'a', 'b', 'c'].map((x) => h('option', { value: x, selected: x === level || null }, x.length === 2 && x[1].match(/\d/) ? x.toUpperCase() : 'Band ' + (x === 'novice' ? 'Novice' : x.toUpperCase()))));
  const ty = h('select', { name: 'type', 'aria-label': 'Filter jenis' }, ...[['', 'Semua jenis'], ['lesson', 'Pelajaran'], ['vocab', 'Kosakata'], ['line', 'Dialog/teks pelajaran'], ['question', 'Soal latihan']].map(([v, l]) => h('option', { value: v, selected: v === type || null }, l)));
  const form = h('form', { class: 'search-form', role: 'search', onsubmit: (e) => {
    e.preventDefault();
    const p = new URLSearchParams({ q: input.value.trim(), level: lv.value, type: ty.value });
    location.hash = `#/search?${p}`;
  } }, input, lv, ty, h('button', { class: 'btn primary', type: 'submit' }, 'Cari'));
  let results = [];
  if (q) {
    const fq = fold(q);
    results = idx.items.filter((it) => (!level || it.level === level) && (!type || it.type === type)
      && (it.text.includes(q) || (fq.length > 1 && fold(it.py).includes(fq)) || it.en?.toLowerCase().includes(q.toLowerCase()))).slice(0, 200);
  }
  const TYPE = { lesson: 'Pelajaran', vocab: 'Kosakata', line: 'Teks', question: 'Soal' };
  return h('div', { class: 'wrap narrow' }, h('h1', {}, 'Cari'),
    h('p', { class: 'muted small' }, `Mencari di ${idx.items.length.toLocaleString('id-ID')} entri: judul pelajaran, isi pelajaran yang sudah dimigrasi (aksara Mandarin, pinyin dengan/tanpa nada, arti), serta teks soal latihan.`),
    form,
    q ? h('p', { role: 'status' }, `${results.length}${results.length === 200 ? '+' : ''} hasil untuk “${q}”`) : null,
    h('ul', { class: 'search-results plain' }, ...results.map((r) => h('li', { class: 'card' },
      h('span', { class: 'pill ghost' }, TYPE[r.type]), ' ', h('a', { href: r.href }, r.title),
      h('p', { class: 'zh', lang: 'zh-Hant' }, r.text.slice(0, 160)), r.py ? h('p', { class: 'py' }, r.py) : null, r.en ? h('p', { class: 'small muted' }, r.en) : null))));
}
