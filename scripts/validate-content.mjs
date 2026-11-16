// Validates structural integrity of all content JSON. Exits non-zero on hard errors.
import { readFileSync, existsSync } from 'node:fs';

const C = 'content';
const read = (p) => JSON.parse(readFileSync(`${C}/${p}`, 'utf8'));
const errors = [], warnings = [];
let questions = 0, gradable = 0, crops = 0;

for (const t of read('exercise/index.json')) {
  const d = read(`exercise/${t.id}.json`);
  const ns = d.questions.map((q) => q.n);
  if (ns.join() !== Array.from({ length: ns.length }, (_, i) => i + 1).join()) errors.push(`${t.id}: question numbering not 1..N`);
  for (const q of d.questions) {
    questions++;
    if (q.gradable) gradable++;
    if (q.gradable && !/^[A-F]$/.test(q.answer)) errors.push(`${t.id} Q${q.n}: invalid answer ${q.answer}`);
    const labels = q.options.map((o) => o.label);
    if (q.gradable && labels.length && !labels.includes(q.answer)) errors.push(`${t.id} Q${q.n}: answer ${q.answer} not among options ${labels}`);
    if (!q.options.length && !q.showCrop) warnings.push(`${t.id} Q${q.n}: no options parsed and no picture crop`);
    if (q.crop) { crops++; if (!existsSync(`media/ex/${t.id}/${q.crop}`)) errors.push(`${t.id} Q${q.n}: crop missing ${q.crop}`); }
    if (q.part == null) warnings.push(`${t.id} Q${q.n}: not assigned to a part`);
    if (d.skill === 'listening' && !q.transcript && !q.transcriptIntro) warnings.push(`${t.id} Q${q.n}: no transcript segment`);
    if (q.answerNote) warnings.push(`${t.id} Q${q.n}: ${q.answerNote}`);
  }
  if (d.skill === 'listening' && !d.audio?.trackList?.length) errors.push(`${t.id}: listening test without audio`);
}
const idx = read('study/index.json');
let lessons = 0, migrated = 0;
for (const lv of idx.levels) for (const b of lv.books) {
  const book = read(`study/${b.id}.json`);
  for (const l of book.lessons) {
    lessons++;
    if (l.start > l.end) errors.push(`${b.id} L${l.n}: invalid page range`);
    if (l.migrated) {
      migrated++;
      const m = read(`study/lessons/${l.id}.json`);
      for (const blk of m.blocks) if (blk.track && !l.tracks.find((x) => x.label === blk.track)) errors.push(`${l.id}: block ${blk.id} references unknown track ${blk.track}`);
    }
  }
}
console.log(`exercise questions: ${questions} (gradable ${gradable}), crops: ${crops}`);
console.log(`study lessons: ${lessons} (migrated to text: ${migrated})`);
console.log(`warnings: ${warnings.length}`);
for (const w of warnings.slice(0, 15)) console.log('  WARN', w);
if (errors.length) { for (const e of errors) console.error('  ERROR', e); process.exit(1); }
console.log('content validation: OK');
