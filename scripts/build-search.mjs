// Builds content/search.json from study structure, migrated lessons and exercise items.
import { readFileSync, writeFileSync, existsSync } from 'node:fs';

const C = 'content';
const read = (p) => JSON.parse(readFileSync(`${C}/${p}`, 'utf8'));
const items = [];
const idx = read('study/index.json');
for (const lv of idx.levels) {
  for (const b of lv.books) {
    for (const l of b.lessons) {
      const title = `${lv.label} ${b.kind === 'textbook' ? 'Textbook' : 'Workbook'} · Pelajaran ${l.n}${l.title ? ' · ' + l.title : ''}`;
      items.push({ type: 'lesson', level: lv.id, book: b.id, href: `#/lesson/${l.id}`, title, text: l.title || '' });
      const f = `${C}/study/lessons/${l.id}.json`;
      if (!existsSync(f)) continue;
      const m = JSON.parse(readFileSync(f, 'utf8'));
      for (const blk of m.blocks) {
        if (blk.type === 'vocab') for (const v of blk.items) items.push({ type: 'vocab', level: lv.id, book: b.id, href: `#/lesson/${l.id}`, title, text: v.zh, py: v.py, en: v.en });
        if (blk.type === 'dialogue') for (const ln of blk.lines) items.push({ type: 'line', level: lv.id, book: b.id, href: `#/lesson/${l.id}`, title, text: ln.zh, py: ln.py });
        if (blk.type === 'text') for (const p of blk.paras || []) items.push({ type: 'line', level: lv.id, book: b.id, href: `#/lesson/${l.id}`, title, text: p.text });
        if (blk.type === 'examples') for (const x of blk.items) items.push({ type: 'line', level: lv.id, book: b.id, href: `#/lesson/${l.id}`, title, text: x.zh, py: x.py, en: x.en });
        if (blk.type === 'exchanges') for (const x of blk.items) for (const y of [x.a, x.b]) items.push({ type: 'line', level: lv.id, book: b.id, href: `#/lesson/${l.id}`, title, text: y.zh, py: y.py, en: y.en });
        if (blk.type === 'pairs') for (const r of blk.rows) for (const y of r) items.push({ type: 'line', level: lv.id, book: b.id, href: `#/lesson/${l.id}`, title, text: y.zh, py: y.py, en: y.en });
      }
    }
  }
}
for (const t of read('exercise/index.json')) {
  const d = read(`exercise/${t.id}.json`);
  for (const q of d.questions) {
    const text = [q.context, q.stem, ...q.options.map((o) => o.text)].filter(Boolean).join(' ').replace(/\s+/g, ' ').slice(0, 400);
    if (text.length > 1) items.push({ type: 'question', level: t.band, href: `#/test/${t.id}`, title: `${t.title} · Soal ${q.n}`, text });
  }
}
writeFileSync(`${C}/search.json`, JSON.stringify({ builtAt: new Date().toISOString(), items }));
console.log('search index entries:', items.length);
