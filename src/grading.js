// Pure grading logic (no DOM) — unit-tested by scripts/test-grading.mjs.
// The supplied answer keys are the only grading source. Questions without a verified key are "ungradable"
// and are excluded from the graded denominator.
export function grade(test, answers) {
  const results = test.questions.map((q) => {
    const given = answers[q.n] ?? null;
    let status;
    if (!q.gradable || !q.answer) status = 'ungradable';
    else if (!given) status = 'unanswered';
    else status = given === q.answer ? 'correct' : 'incorrect';
    return { n: q.n, part: q.part, given, answer: q.gradable ? q.answer : null, status };
  });
  const count = (s) => results.filter((r) => r.status === s).length;
  const score = {
    total: results.length,
    correct: count('correct'), incorrect: count('incorrect'), unanswered: count('unanswered'), ungradable: count('ungradable'),
  };
  score.gradable = score.total - score.ungradable;
  score.percent = score.gradable ? Math.round((score.correct / score.gradable) * 1000) / 10 : 0;
  const byPart = (test.parts || []).map((p, i) => {
    const rs = results.filter((r) => r.part === i && r.status !== 'ungradable');
    return { title: p.title, subtitle: p.subtitle, correct: rs.filter((r) => r.status === 'correct').length, gradable: rs.length };
  });
  return { results, score, byPart };
}
