// Grading tests against the real answer keys.
import { readFileSync } from 'node:fs';
import assert from 'node:assert/strict';
import { grade } from '../src/grading.js';

const read = (p) => JSON.parse(readFileSync(`content/${p}`, 'utf8'));
let n = 0;
for (const t of read('exercise/index.json')) {
  const d = read(`exercise/${t.id}.json`);
  const key = Object.fromEntries(d.questions.filter((q) => q.gradable).map((q) => [q.n, q.answer]));
  // all correct
  let g = grade(d, key);
  assert.equal(g.score.correct, g.score.gradable, `${t.id} all-correct`);
  assert.equal(g.score.percent, 100);
  // all empty
  g = grade(d, {});
  assert.equal(g.score.unanswered, g.score.gradable, `${t.id} empty`);
  assert.equal(g.score.correct, 0);
  // all wrong (shift letter)
  const wrong = Object.fromEntries(Object.entries(key).map(([k, v]) => [k, v === 'A' ? 'B' : 'A']));
  g = grade(d, wrong);
  assert.equal(g.score.incorrect, g.score.gradable, `${t.id} all-wrong`);
  // per-part sums
  assert.equal(g.byPart.reduce((s, p) => s + p.gradable, 0), g.score.gradable, `${t.id} part totals`);
  n++;
}
// ungradable handling
const fake = { parts: [{ title: 'P' }], questions: [{ n: 1, part: 0, gradable: true, answer: 'A' }, { n: 2, part: 0, gradable: false, answer: null }] };
const g = grade(fake, { 1: 'A', 2: 'C' });
assert.deepEqual([g.score.correct, g.score.gradable, g.score.ungradable, g.score.percent], [1, 1, 1, 100]);
// spot checks against the printed keys
assert.equal(read('exercise/a-l1.json').questions[0].answer, 'B');   // Band A L S1 Q1 = B
assert.equal(read('exercise/a-r1.json').questions[41].answer, 'E');  // Band A R S1 Q42 = E
assert.equal(read('exercise/b-l1.json').questions[0].answer, 'C');   // Band B L S1 Q1 = C
assert.equal(read('exercise/novice-r1.json').questions[0].answer, 'A'); // Novice R Q1 = A (second half of shared key)
console.log(`grading tests passed for ${n} tests + edge cases`);
