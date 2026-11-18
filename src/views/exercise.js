import { h, getJson, mediaUrl, escBr, fmtDate, fmtTime, pct, uid } from '../util.js';
import { t, BAND_LABEL, BAND_DESC } from '../i18n.js';
import { store } from '../store.js';
import { grade } from '../grading.js';
import { AudioPlayer, stopAll, originalAudio } from '../audio.js';
import { TtsPlayer, SpeakButton } from '../tts.js';
import { progressBar, scoreClass } from './home.js';

const loadTest = (id) => getJson(`content/exercise/${id}.json`);
const SKILL = { listening: 'Listening', reading: 'Reading' };
const loadExplain = (id) => getJson(`content/exercise/explain/${id}.json`).catch(() => null);

// One Chinese line with audio, pinyin, and its English and Indonesian translations.
function explainLine(seg, mark = '') {
  return h('div', { class: 'ex-line' },
    h('div', { class: 'ex-zh' }, mark ? h('span', { class: 'ex-mark' }, mark) : null, h('span', { lang: 'zh-Hant' }, seg.zh), SpeakButton(seg.zh, 'Dengarkan')),
    h('div', { class: 'ex-py', lang: 'zh-Latn-pinyin' }, seg.py),
    seg.en || seg.idn ? h('dl', { class: 'ex-tr' },
      seg.en ? [h('dt', { title: 'English' }, 'EN'), h('dd', { lang: 'en' }, seg.en)] : null,
      seg.idn ? [h('dt', { title: 'Bahasa Indonesia' }, 'ID'), h('dd', { lang: 'id' }, seg.idn)] : null) : null);
}
const explainGroup = (title, segs) => segs?.length ? h('section', { class: 'ex-group' }, h('h4', {}, title), ...segs) : null;

// Explanation shown after submitting: every Chinese text of the question with pinyin and English.
function explainPanel(test, q, ex, given) {
  if (!ex) return null;
  const all = ex.questions;
  const e = all[q.n] || {};
  const leadN = q.cloze ? q.groupLead : (q.group ? Number(q.group.slice(1)) : null);
  const lead = leadN && leadN !== q.n ? all[leadN] || {} : null;
  const passage = e.passage || lead?.passage;
  const image = e.image || lead?.image;
  const introN = q.transcriptLead && q.transcriptLead !== q.n ? q.transcriptLead : null;
  const intro = e.intro || (introN ? all[introN]?.intro : null);
  const opts = e.options ? Object.keys(e.options).sort().map((L) => explainLine(e.options[L], `(${L})${L === q.answer ? ' ✓' : (L === given ? ' ✗' : '')}`)) : [];
  return h('details', { class: 'explain', open: true },
    h('summary', {}, 'Pembahasan: pinyin, audio, terjemahan Inggris & Indonesia'),
    explainGroup(passage && lead && !e.passage ? `Teks bacaan (bersama soal ${leadN})` : 'Teks bacaan', passage?.map((x) => explainLine(x))),
    explainGroup('Teks di dalam gambar', image?.map((x) => explainLine(x))),
    explainGroup('Pengantar audio', intro?.map((x) => explainLine(x))),
    explainGroup('Transkrip audio', e.transcript?.map((x) => explainLine(x))),
    explainGroup('Soal', e.stem ? [explainLine(e.stem)] : null),
    explainGroup('Pilihan jawaban', opts),
    ex.indonesianComplete ? null : h('p', { class: 'small ex-pending' }, ex.englishComplete ? 'Terjemahan bahasa Indonesia untuk tes ini sedang ditambahkan bertahap.' : 'Terjemahan untuk tes ini sedang ditambahkan bertahap; pinyin sudah lengkap untuk semua teks.'),
    h('p', { class: 'small muted ex-note' }, 'Pinyin memakai Hanyu Pinyin dengan tanda nada; tombol 🔊 membacakan setiap baris dengan suara Mandarin. Terjemahan Inggris dan Indonesia disusun untuk situs ini dan bukan terjemahan resmi TOCFL.'));
}

// Speech-synthesis segments for one question, built from the official listening script.
function ttsSegments(test, q, { withIntro = true, number = false } = {}) {
  const segs = [];
  if (withIntro && q.transcriptIntro) segs.push({ label: 'Teks', text: q.transcriptIntro, pause: 900 });
  if (number) segs.push({ label: `Soal ${q.n}`, text: `第${q.n}題`, pause: 400 });
  if (q.transcript) segs.push({ label: `Soal ${q.n}`, text: q.transcript, pause: 1500 });
  return segs;
}
function fullTestSegments(test) {
  let lastIntro = null;
  return test.questions.flatMap((q) => {
    const withIntro = !!q.transcriptIntro && q.transcriptIntro !== lastIntro;
    lastIntro = q.transcriptIntro || lastIntro;
    return ttsSegments(test, q, { withIntro, number: true });
  });
}
const TTS_NOTE = 'Rekaman audio asli tidak tersedia di versi online ini. Soal listening dibacakan dengan suara sintetis Mandarin (TTS) dari naskah dengar resmi; pengucapan, kecepatan, dan intonasinya dapat berbeda dari rekaman ujian asli.';

export async function exerciseHome() {
  const tests = await getJson('content/exercise/index.json');
  return h('div', { class: 'wrap' },
    h('nav', { class: 'crumbs', 'aria-label': 'Breadcrumb' }, h('a', { href: '#/' }, 'Beranda'), ' / TOCFL Exercise'),
    h('h1', {}, 'TOCFL Exercise'),
    h('div', { class: 'tiles' }, ...['novice', 'a', 'b', 'c'].map((b) => {
      const list = tests.filter((x) => x.band === b);
      return h('a', { class: 'tile', href: `#/exercise/${b}` }, h('span', { class: 'tile-big' }, BAND_LABEL[b]), h('span', { class: 'tile-sub' }, BAND_DESC[b]),
        h('span', { class: 'tile-meta' }, `${list.filter((x) => x.skill === 'listening').length} listening · ${list.filter((x) => x.skill === 'reading').length} reading`));
    })));
}

const sectionAttempts = (testId, set) => store.get().attempts.filter((a) => a.testId === testId && a.range && a.range.from === set.from && a.range.to === set.to);
const bestPct = (atts) => atts.reduce((m, a) => Math.max(m, a.score.percent ?? pct(a.score.correct, a.score.gradable)), -1);

const loadBank = () => getJson('content/exercise/partbank.json').catch(() => ({}));
const bankAttempts = (testId) => store.attemptsFor(testId).filter((a) => !a.range);

export async function bandView({ band }) {
  const [tests, sections, bank] = await Promise.all([getJson('content/exercise/index.json'), getJson('content/exercise/sections.json'), loadBank()]);
  const fullTests = tests.filter((x) => x.band === band && !x.id.startsWith('pb-'));
  const sectionMenu = (skill) => h('div', { class: 'section-menu' }, ...sections.filter((x) => x.band === band && x.skill === skill).map((sec) => {
    const done = sec.sets.filter((st) => sectionAttempts(st.test, st).length).length;
    const pb = bank[sec.id];
    const total = sec.questions + (pb?.questions || 0);
    return h('a', { class: 'section-card', href: `#/section/${band}/${sec.id}` },
      h('span', { class: 'sec-zh', lang: 'zh-Hant' }, sec.zh),
      h('span', { class: 'sec-name' }, sec.name),
      h('span', { class: 'sec-desc' }, sec.desc),
      h('span', { class: 'sec-meta' }, pb ? `${total} soal · ${pb.questions} bank soal + ${sec.questions} dari tes lengkap` : `${sec.questions} soal · ${sec.sets.length} set`,
        done ? h('span', { class: 'pill good' }, `${done}/${sec.sets.length} dicoba`) : null));
  }));
  const fullList = (skill) => h('ul', { class: 'test-list' }, ...fullTests.filter((x) => x.skill === skill).map((x) => {
    const atts = store.attemptsFor(x.id).filter((a) => !a.range);
    const prog = store.getProgress(x.id);
    return h('li', {}, h('a', { href: `#/test/${x.id}` }, h('strong', {}, `Series ${x.series}`), h('span', { class: 'muted' }, ` · ${x.questions} soal`)),
      h('span', { class: 'test-meta' }, prog ? h('span', { class: 'pill warn' }, 'Sedang dikerjakan') : null,
        atts.length ? h('span', { class: 'pill' }, `${atts.length}× · terbaik ${bestPct(atts)}%`) : h('span', { class: 'pill ghost' }, 'Belum dicoba')));
  }));
  const col = (skill) => h('section', { class: 'skill-col' },
    h('h2', {}, t(skill)),
    h('h3', { class: 'sub-h' }, 'Latihan per bagian'),
    h('p', { class: 'small muted' }, 'Pilih satu jenis soal untuk berlatih fokus. Setiap bagian berisi seluruh bank soal resmi per bagian, ditambah soal bagian itu dari semua tes lengkap.'),
    sectionMenu(skill),
    h('details', { class: 'card full-tests' }, h('summary', {}, `Tes lengkap (${fullTests.filter((x) => x.skill === skill).length} seri, semua bagian sekaligus)`), fullList(skill)));
  return h('div', { class: 'wrap' },
    h('nav', { class: 'crumbs' }, h('a', { href: '#/' }, 'Beranda'), ' / ', h('a', { href: '#/exercise' }, 'TOCFL Exercise'), ` / ${BAND_LABEL[band]}`),
    h('h1', {}, `${BAND_LABEL[band]} — ${BAND_DESC[band]}`),
    h('div', { class: 'grid-2 skills' }, col('listening'), col('reading')));
}

export async function sectionView({ band, sec: secId }) {
  const sections = await getJson('content/exercise/sections.json');
  const sec = sections.find((x) => x.id === secId && x.band === band);
  if (!sec) throw new Error('Bagian latihan tidak ditemukan');
  const first = sec.sets[0];
  const pb = (await loadBank())[sec.id];
  const useOrig = sec.skill === 'listening' && await originalAudio();
  const timer = h('input', { type: 'number', min: 0, max: 120, step: 5, value: 0, id: 'sec-timer', class: 'num' });
  const rows = sec.sets.map((st) => {
    const atts = sectionAttempts(st.test, st);
    const prog = store.getProgress(`${st.test}@${st.from}-${st.to}`);
    const base = `#/test/${st.test}/run?sec=${sec.id}&from=${st.from}&to=${st.to}`;
    return h('li', { class: 'set-row' },
      h('div', {}, h('strong', {}, `Series ${st.series}`), h('span', { class: 'muted' }, ` · soal ${st.from}–${st.to} · ${st.questions} soal`),
        prog ? h('span', { class: 'pill warn' }, 'Sedang dikerjakan') : null,
        atts.length ? h('span', { class: 'pill' }, `${atts.length}× · terbaik ${bestPct(atts)}%`) : null),
      h('div', { class: 'set-actions' },
        h('a', { class: 'btn primary small', href: `${base}&mode=practice` }, prog?.mode === 'practice' ? 'Lanjutkan' : 'Latihan'),
        h('button', { class: 'btn small', type: 'button', onclick: () => { location.hash = `${base}&mode=exam&min=${Number(timer.value) || 0}`; } }, 'Simulasi')));
  });
  const bankRows = (pb?.sets || []).map((st) => {
    const atts = bankAttempts(st.test);
    const prog = store.getProgress(st.test);
    const base = `#/test/${st.test}/run?bank=${sec.id}`;
    return h('li', { class: 'set-row' },
      h('div', {}, h('strong', {}, `Set ${st.set}`), h('span', { class: 'muted' }, ` · ${st.questions} soal`),
        prog ? h('span', { class: 'pill warn' }, 'Sedang dikerjakan') : null,
        atts.length ? h('span', { class: 'pill' }, `${atts.length}× · terbaik ${bestPct(atts)}%`) : null),
      h('div', { class: 'set-actions' },
        h('a', { class: 'btn primary small', href: `${base}&mode=practice` }, prog?.mode === 'practice' ? 'Lanjutkan' : 'Latihan'),
        h('button', { class: 'btn small', type: 'button', onclick: () => { location.hash = `${base}&mode=exam&min=${Number(timer.value) || 0}`; } }, 'Simulasi')));
  });
  return h('div', { class: 'wrap narrow' },
    h('nav', { class: 'crumbs' }, h('a', { href: '#/exercise' }, 'TOCFL Exercise'), ' / ', h('a', { href: `#/exercise/${band}` }, BAND_LABEL[band]), ` / ${t(sec.skill)}`),
    h('h1', {}, h('span', { lang: 'zh-Hant' }, sec.zh), ' ', sec.name),
    h('p', { class: 'lead' }, sec.desc),
    pb ? h('p', {}, `${pb.questions + sec.questions} soal: ${pb.questions} soal dari bank soal resmi bagian ini (${pb.items} item, ${pb.sets.length} set) dan ${sec.questions} soal dari ${sec.sets.length} seri tes lengkap. Kunci jawaban mengikuti file kunci resmi.`)
      : h('p', {}, `${sec.questions} soal dari ${sec.sets.length} seri tes resmi ${BAND_LABEL[band]}. Kunci jawaban, gambar, dan naskah dengar mengikuti tes aslinya.`),
    sec.skill === 'listening' && !useOrig ? h('p', { class: 'note small' }, TTS_NOTE) : null,
    first?.instructions ? h('details', { class: 'card' }, h('summary', {}, 'Petunjuk resmi bagian ini'),
      h('p', { class: 'zh', lang: 'zh-Hant', html: escBr(first.instructions) }), first.instructionsEn ? h('p', { class: 'muted small', lang: 'en' }, first.instructionsEn) : null) : null,
    pb ? h('section', { class: 'card' }, h('h2', { class: 'h3' }, `Bank soal per bagian (${pb.questions} soal)`),
      h('p', { class: 'small muted' }, 'Soal resmi per bagian dari folder "Per Part", dikelompokkan per set. Soal ditampilkan persis seperti lembar soal aslinya.'),
      h('ul', { class: 'set-list' }, ...bankRows)) : null,
    h('section', { class: 'card' }, h('h2', { class: 'h3' }, pb ? `Dari tes lengkap (${sec.questions} soal)` : 'Pilih set soal'),
      h('ul', { class: 'set-list' }, ...rows),
      h('p', { class: 'small muted' }, h('label', { for: 'sec-timer' }, 'Batas waktu untuk mode Simulasi (menit, 0 = tanpa batas): '), timer)));
}

export async function testIntro({ test: id }) {
  const test = await loadTest(id);
  const prog = store.getProgress(id);
  const atts = store.attemptsFor(id).sort((a, b) => b.submittedAt - a.submittedAt);
  const timer = h('input', { type: 'number', min: 0, max: 180, step: 5, value: 0, id: 'timer', class: 'num' });
  const useOrig = await originalAudio();
  const audioNote = test.skill !== 'listening' ? null : !useOrig ? TTS_NOTE : (test.audio?.kind === 'by-filename'
    ? 'Audio per soal tersedia: pemetaan trek ↔ soal mengikuti penamaan file resmi (mis. "1-07.mp3" = soal 7).'
    : 'File audio tes ini hanya bernomor urut (001, 002, …), sehingga pemetaan per soal belum diverifikasi. Gunakan pemutar audio tes lengkap (putar berurutan).');
  return h('div', { class: 'wrap narrow' },
    h('nav', { class: 'crumbs' }, h('a', { href: '#/exercise' }, 'TOCFL Exercise'), ' / ', h('a', { href: `#/exercise/${test.band}` }, BAND_LABEL[test.band]), ` / ${test.title}`),
    h('h1', {}, test.title),
    h('p', {}, `${test.questions.length} soal · ${SKILL[test.skill]} · ${test.parts.length} bagian`),
    audioNote ? h('p', { class: 'note' }, audioNote) : null,
    h('section', { class: 'card' }, h('h2', {}, 'Bagian tes & petunjuk'),
      ...test.parts.map((p) => h('details', { class: 'part' },
        h('summary', {}, `${p.title} ${p.subtitle ? '· ' + p.subtitle : ''} — soal ${p.from}–${p.to}`),
        h('p', { class: 'zh', lang: 'zh-Hant', html: escBr(p.instructions) }), p.instructionsEn ? h('p', { class: 'muted small', lang: 'en' }, p.instructionsEn) : null))),
    h('section', { class: 'card' }, h('h2', {}, 'Pilih mode'),
      h('div', { class: 'grid-2' },
        h('div', {}, h('h3', {}, t('practice')), h('ul', { class: 'small' }, h('li', {}, 'Navigasi bebas antar soal'), h('li', {}, 'Audio dapat diulang dan diatur kecepatannya'), h('li', {}, 'Ulasan lengkap setelah dikumpulkan')),
          h('a', { class: 'btn primary', href: `#/test/${id}/run?mode=practice` }, prog?.mode === 'practice' ? 'Lanjutkan latihan' : 'Mulai latihan')),
        h('div', {}, h('h3', {}, t('exam')), h('ul', { class: 'small' }, h('li', {}, 'Jawaban & transkrip tersembunyi sampai dikumpulkan'),
          h('li', {}, test.skill === 'listening' ? 'Audio diputar berurutan tanpa geser/ubah kecepatan' : 'Fokus satu soal per layar'),
          h('li', {}, 'Konfirmasi sebelum mengumpulkan')),
          h('label', { class: 'small', for: 'timer' }, 'Batas waktu (menit, 0 = tanpa batas): '), timer,
          h('p', { class: 'muted small' }, 'Aturan simulasi ini bersifat perkiraan dan dapat diatur sendiri; tidak identik dengan ujian resmi.'),
          h('button', { class: 'btn', type: 'button', onclick: () => { location.hash = `#/test/${id}/run?mode=exam&min=${Number(timer.value) || 0}`; } }, prog?.mode === 'exam' ? 'Lanjutkan simulasi' : 'Mulai simulasi')))),
    atts.length ? h('section', { class: 'card' }, h('h2', {}, 'Percobaan sebelumnya'),
      h('ul', { class: 'plain results' }, ...atts.map((a) => h('li', {}, h('a', { href: `#/result/${a.id}` }, fmtDate(a.submittedAt)), ` · ${a.mode === 'exam' ? 'Simulasi' : 'Latihan'} `,
        h('span', { class: `score ${scoreClass(a)}` }, `${a.score.correct}/${a.score.gradable} · ${a.score.percent}%`))))) : null,
    h('p', { class: 'muted small' }, `Sumber: ${test.source.folder}/${test.source.booklet}`));
}

function trackObjs(test, idxs) {
  return idxs.map((i) => test.audio.trackList[i]);
}

export function questionBody(test, q, { selected, onSelect, review, result } = {}) {
  const lang = { lang: 'zh-Hant' };
  const lead = q.group && q.group !== `g${q.n}` ? test.questions.find((x) => `g${x.n}` === q.group) : null;
  const ctxText = q.context || lead?.context || '';
  const crop = q.crop || (q.cloze ? test.questions.find((x) => x.n === q.groupLead)?.crop : null);
  const leadCrop = !q.crop && lead?.crop ? lead.crop : null;
  const isPicture = q.showCrop;
  const optsHaveText = q.options.length && q.options.every((o) => o.text);
  const letters = q.options.length ? q.options.map((o) => o.label) : 'ABCDEF'.slice(0, test.optionCount || 3).split('');
  const name = `q${q.n}`;
  const optionEls = letters.map((L) => {
    const o = q.options.find((x) => x.label === L);
    // bank items always show the original item image; their option text (when parsed) is shown too
    const showText = optsHaveText && (!isPicture || test.kind === 'partbank');
    let cls = 'opt';
    if (review) {
      if (L === q.answer) cls += ' is-correct';
      if (L === result?.given && result.given !== q.answer) cls += ' is-wrong';
    }
    const mark = review ? (L === q.answer ? ' ✓' : (L === result?.given ? ' ✗' : '')) : '';
    return h('label', { class: cls },
      h('input', { type: 'radio', name, value: L, checked: (review ? result?.given : selected) === L || null, disabled: review || null,
        onchange: () => onSelect?.(L) }),
      h('span', { class: 'opt-label' }, `(${L})`), showText ? h('span', { class: 'opt-text', ...lang }, o.text) : null,
      mark ? h('span', { class: 'opt-mark', 'aria-hidden': 'true' }, mark) : null,
      review && L === q.answer ? h('span', { class: 'sr-only' }, ' — jawaban benar') : null,
      review && L === result?.given && L !== q.answer ? h('span', { class: 'sr-only' }, ' — jawaban Anda') : null);
  });
  const cropImg = (src, alt) => h('figure', { class: 'crop' }, h('img', { src: mediaUrl(`ex/${test.id}/${src}`), alt, loading: 'lazy' }));
  // A passage printed as a picture (notice, table, advertisement) has only its number "（八）" as text: show the picture.
  const headerOnly = ctxText && ctxText.trim().length < 8;
  const passagePic = headerOnly ? (q.passageImage || (lead && q.layout?.length > 1 ? q.layout[0] : null)) : null;
  const passage = passagePic ? cropImg(passagePic, `Teks bacaan ${ctxText.trim()} (gambar dari buku soal)`)
    : ctxText && !isPicture ? h('div', { class: 'passage zh', ...lang, html: escBr(ctxText) }) : null;
  const showCropNow = isPicture || q.spokenOptions || (!optsHaveText && !ctxText);
  // Reading: every question offers the booklet layout (passage + question only; choices are the buttons below).
  const layout = test.skill === 'reading' ? (q.layout || []) : [];
  const origView = layout.length
    ? h('details', { class: 'orig' }, h('summary', {}, 'Lihat tampilan asli dari buku soal'),
      h('p', { class: 'small muted orig-note' }, 'Teks bacaan dan soal persis seperti di buku soal. Pilihan jawaban tidak ditampilkan di sini; gunakan tombol pilihan di bawah.'),
      ...layout.map((src, i) => cropImg(src, layout.length > 1 && i === 0 ? `Teks bacaan untuk soal ${q.n} — tampilan asli` : `Soal ${q.n} — tampilan asli (tanpa pilihan jawaban)`)))
    : (!showCropNow && crop ? h('details', { class: 'orig' }, h('summary', {}, 'Lihat tampilan asli dari buku soal'), cropImg(crop, `Soal ${q.n} — tampilan asli`)) : null);
  const spokenNote = q.spokenOptions ? h('p', { class: 'small muted' }, 'Pilihan jawaban dibacakan di audio (tidak tercetak di buku soal).') : null;
  const subNote = q.subCount > 1 ? h('p', { class: 'note small sub-note' }, `Item ini berisi ${q.subCount} soal. Soal ini = nomor (${q.sub}) pada teks di bawah.`) : null;
  return h('div', { class: 'q-body' },
    subNote,
    leadCrop && !ctxText ? cropImg(leadCrop, `Teks soal ${lead.n} (tampilan asli)`) : null,
    passage,
    q.stem && !isPicture ? h('p', { class: 'stem zh', ...lang }, q.stem) : null,
    showCropNow && crop ? cropImg(crop, `Soal ${q.n} — gambar/tampilan asli dari buku soal`) : null,
    origView,
    spokenNote,
    h('fieldset', { class: 'opts' }, h('legend', { class: 'sr-only' }, `Pilihan jawaban soal ${q.n}`), ...optionEls));
}

export async function testRun({ test: id }, query) {
  const full = await loadTest(id);
  // Section practice: ?sec=<sectionId>&from=&to= limits the run to that part of the test.
  const range = query.get('from') ? { from: Number(query.get('from')), to: Number(query.get('to')), sec: query.get('sec') } : null;
  const section = range?.sec ? (await getJson('content/exercise/sections.json')).find((x) => x.id === range.sec) : null;
  const test = range ? { ...full, questions: full.questions.filter((q) => q.n >= range.from && q.n <= range.to),
    title: `${full.title} — ${section ? `${section.zh} ${section.name}` : `soal ${range.from}–${range.to}`}` } : full;
  const progKey = range ? `${id}@${range.from}-${range.to}` : id;
  const backSec = range?.sec || full.section || query.get('bank');
  const qs = range ? `&sec=${range.sec || ''}&from=${range.from}&to=${range.to}` : (full.section ? `&bank=${full.section}` : '');
  const mode = query.get('mode') === 'exam' ? 'exam' : 'practice';
  let prog = store.getProgress(progKey);
  if (!prog || prog.mode !== mode) prog = { mode, answers: {}, startedAt: Date.now(), elapsed: 0, limitMin: Number(query.get('min')) || 0, cur: 0 };
  prog.href = `#/test/${id}/run?mode=${mode}${qs}`; prog.title = test.title;
  const save = () => store.saveProgress(progKey, prog);
  save();
  let cur = Math.min(prog.cur || 0, test.questions.length - 1);
  const listening = test.skill === 'listening';
  const byFile = test.audio?.kind === 'by-filename';

  const navGrid = h('div', { class: 'qnav', role: 'list', 'aria-label': 'Navigasi soal' });
  const qPane = h('section', { class: 'q-pane', 'aria-live': 'polite' });
  const counter = h('span', { class: 'counter' });
  const markedList = h('p', { class: 'small marked-list' });
  const timerEl = h('span', { class: 'timer', role: 'timer' });

  // whole-test audio (exam mode, or tests whose tracks are only numbered sequentially)
  const useOrig = listening && await originalAudio();
  let fullAudio = null;
  if (listening && useOrig && test.audio) {
    const tracks = range && byFile ? [...new Set(test.questions.flatMap((q) => q.audio || []))].sort((x, y) => x - y).map((i) => test.audio.trackList[i]) : test.audio.trackList;
    fullAudio = AudioPlayer(tracks, { title: range ? 'Audio bagian ini' : 'Audio tes lengkap', exam: mode === 'exam', playAll: true });
  } else if (listening) {
    fullAudio = TtsPlayer(fullTestSegments(test), { title: 'Seluruh tes', exam: mode === 'exam', hideText: true });
  }

  function renderNav() {
    navGrid.replaceChildren(...test.questions.map((q, i) => h('button', {
      type: 'button', role: 'listitem', class: 'qn' + (prog.answers[q.n] ? ' done' : '') + (i === cur ? ' cur' : '') + (prog.marked?.[q.n] ? ' marked' : ''),
      'aria-label': `Soal ${q.n}${prog.answers[q.n] ? ', sudah dijawab' : ', belum dijawab'}${prog.marked?.[q.n] ? ', ditandai' : ''}`, 'aria-current': i === cur ? 'step' : null,
      onclick: () => go(i),
    }, String(q.n))));
    const n = Object.keys(prog.answers).length;
    const m = Object.keys(prog.marked || {}).length;
    counter.textContent = `${n}/${test.questions.length} terjawab` + (m ? ` · 🚩 ${m} ditandai` : '');
    const marked = test.questions.filter((q) => prog.marked?.[q.n]);
    markedList.replaceChildren(...(marked.length ? [h('strong', {}, `🚩 Ditandai (${marked.length}): `), ...marked.flatMap((q) => [h('button', { type: 'button', class: 'linkish', onclick: () => go(test.questions.indexOf(q)) }, String(q.n)), ' '])] : []));
  }
  function go(i) {
    cur = Math.max(0, Math.min(test.questions.length - 1, i));
    prog.cur = cur; save();
    renderQ(); renderNav();
  }
  function renderQ() {
    const q = test.questions[cur];
    const part = test.parts[q.part];
    const perQ = !listening || mode !== 'practice' ? null
      : useOrig ? (byFile && q.audio?.length ? AudioPlayer(trackObjs(test, q.audio), { title: `Audio soal ${q.n}`, playAll: true, compact: true }) : null)
        : TtsPlayer(ttsSegments(test, q), { title: `Soal ${q.n}`, compact: true, hideText: true });
    qPane.replaceChildren(...[

      h('div', { class: 'q-head' }, h('h2', {}, `Soal ${q.n}`), prog.marked?.[q.n] ? h('span', { class: 'flag-pill' }, '🚩 Ditandai') : null, part ? h('span', { class: 'muted' }, `${part.title} ${part.subtitle ? '· ' + part.subtitle : ''}`) : null),
      perQ,
      questionBody(test, q, { selected: prog.answers[q.n], onSelect: (L) => { prog.answers[q.n] = L; save(); renderNav(); } }),
      h('div', { class: 'q-actions' },
        h('button', { class: 'btn', type: 'button', disabled: cur === 0 || null, onclick: () => go(cur - 1) }, '← ' + t('prev')),
        h('button', { class: 'btn ' + (prog.marked?.[q.n] ? 'warn-on' : 'ghost'), type: 'button', 'aria-pressed': prog.marked?.[q.n] ? 'true' : 'false',
          onclick: () => { prog.marked = prog.marked || {}; if (prog.marked[q.n]) delete prog.marked[q.n]; else prog.marked[q.n] = true; save(); renderQ(); renderNav(); } },
          prog.marked?.[q.n] ? '🚩 Hapus tanda' : '⚑ Tandai soal'),
        prog.answers[q.n] ? h('button', { class: 'btn ghost', type: 'button', onclick: () => { delete prog.answers[q.n]; save(); renderQ(); renderNav(); } }, 'Hapus jawaban') : null,
        cur < test.questions.length - 1 ? h('button', { class: 'btn primary', type: 'button', onclick: () => go(cur + 1) }, t('next') + ' →')
          : h('button', { class: 'btn primary', type: 'button', onclick: submit }, t('submit')))].filter(Boolean));
  }
  function submit(force) {
    const unanswered = test.questions.filter((q) => !prog.answers[q.n]).map((q) => q.n);
    const markedNs = test.questions.filter((q) => prog.marked?.[q.n]).map((q) => q.n);
    if (force !== true) {
      const mk = markedNs.length ? `\n🚩 ${markedNs.length} soal ditandai untuk ditinjau (${markedNs.slice(0, 12).join(', ')}${markedNs.length > 12 ? ', …' : ''}).` : '';
      const msg = mk && !unanswered.length ? `Kumpulkan semua jawaban sekarang?${mk}\nSoal ditandai akan tersimpan di Ulas Kesalahan.` : unanswered.length ? `Masih ada ${unanswered.length} soal yang belum dijawab (${unanswered.slice(0, 12).join(', ')}${unanswered.length > 12 ? ', …' : ''}).${mk}\nKumpulkan sekarang?` : 'Kumpulkan semua jawaban sekarang?';
      if (!confirm(msg)) return;
    }
    stopAll();
    clearInterval(tick);
    const g = grade(test, prog.answers);
    const a = store.addAttempt({ id: uid(), testId: id, range, retry: `#/test/${id}/run?mode=${mode}${qs}`, title: test.title, band: test.band, skill: test.skill, mode,
      answers: { ...prog.answers }, marked: markedNs, score: g.score, byPart: g.byPart, results: g.results, submittedAt: Date.now(),
      durationSec: Math.round(prog.elapsed + (Date.now() - resumeAt) / 1000) });
    store.clearProgress(progKey);
    location.hash = `#/result/${a.id}`;
  }
  // timer (counts up; counts down when a limit is set in exam mode)
  const resumeAt = Date.now();
  const tick = setInterval(() => {
    if (!document.body.contains(timerEl)) { clearInterval(tick); prog.elapsed += (Date.now() - resumeAt) / 1000; save(); return; }
    const el = prog.elapsed + (Date.now() - resumeAt) / 1000;
    if (prog.limitMin) {
      const left = prog.limitMin * 60 - el;
      timerEl.textContent = `Sisa ${fmtTime(left)}`;
      timerEl.classList.toggle('warn', left < 120);
      if (left <= 0) { alert('Waktu habis. Jawaban dikumpulkan otomatis.'); submit(true); }
    } else timerEl.textContent = `Waktu ${fmtTime(el)}`;
  }, 1000);
  window.addEventListener('beforeunload', () => { prog.elapsed += (Date.now() - resumeAt) / 1000; save(); }, { once: true });

  renderQ(); renderNav();
  const audioBox = fullAudio ? h('section', { class: 'card audio-box' },
    h('h2', { class: 'h3' }, mode === 'exam' ? 'Audio tes' : 'Audio tes lengkap'),
    !useOrig ? h('p', { class: 'small muted' }, TTS_NOTE + (mode === 'exam' ? ' Tekan putar untuk membacakan seluruh tes secara berurutan.' : ' Suara per soal ada di atas setiap soal.')) : null,
    useOrig && mode === 'exam' ? h('p', { class: 'small muted' }, 'Tekan putar untuk memulai. Audio berjalan berurutan seperti ujian; selesai diputar tidak otomatis mengumpulkan jawaban.') : null,
    useOrig && mode !== 'exam' ? h('p', { class: 'small muted' }, byFile ? 'Audio per soal ada di atas setiap soal. Pemutar ini memutar seluruh rekaman tes secara berurutan.' : 'Pemetaan audio per soal belum diverifikasi untuk tes ini; putar rekaman tes secara berurutan.') : null,
    fullAudio) : null;
  return h('div', { class: 'wrap test-layout' },
    h('div', { class: 'test-top' },
      h('div', {}, h('a', { href: backSec ? `#/section/${full.band}/${backSec}` : `#/test/${id}`, class: 'small' }, backSec ? '← Kembali ke bagian' : '← Petunjuk tes'), h('h1', { class: 'h2' }, test.title), h('span', { class: 'pill' }, mode === 'exam' ? t('exam') : t('practice'))),
      h('div', { class: 'test-status' }, timerEl, counter, h('button', { class: 'btn primary', type: 'button', onclick: submit }, t('submit')))),
    h('div', { class: 'test-grid' },
      h('div', {}, audioBox, qPane),
      h('aside', { class: 'card side' }, h('h2', { class: 'h3' }, 'Daftar soal'), navGrid, markedList,
        h('p', { class: 'small muted' }, 'Kotak berwarna = sudah dijawab. 🚩 = soal ditandai untuk ditinjau lagi. Jawaban dan tanda tersimpan otomatis di perangkat ini.'))));
}

export async function resultView({ attempt: aid }, query) {
  const a = store.attempt(aid);
  if (!a) return h('div', { class: 'wrap' }, h('h1', {}, 'Hasil tidak ditemukan'), h('p', {}, 'Percobaan ini tidak ada di browser ini.'));
  const test = await loadTest(a.testId);
  const ex = await loadExplain(test.id);
  const useOrig = test.skill === 'listening' && await originalAudio();
  const filter = query.get('f') || 'all';
  const markedSet = new Set(a.marked || []);
  const backHref = a.range?.sec ? `#/section/${test.band}/${a.range.sec}` : (test.section ? `#/section/${test.band}/${test.section}` : `#/exercise/${test.band}`);
  const backBtn = h('a', { class: 'btn', href: backHref }, '← Kembali ke pilihan latihan');
  const shown = a.results.filter((r) => filter === 'all' || (filter === 'marked' ? markedSet.has(r.n) : filter === 'wrong' ? r.status === 'incorrect' || r.status === 'unanswered' : r.status === filter));
  const s = a.score;
  const items = shown.map((r) => {
    const q = test.questions.find((x) => x.n === r.n);
    const statusTxt = { correct: '✓ ' + t('correct'), incorrect: '✗ ' + t('incorrect'), unanswered: '– ' + t('unanswered'), ungradable: '? ' + t('ungradable') }[r.status];
    const leadQ = q.transcriptLead && q.transcriptLead !== q.n ? test.questions.find((x) => x.n === q.transcriptLead) : null;
    const audio = test.skill !== 'listening' ? null
      : useOrig ? (test.audio?.kind === 'by-filename' && q.audio?.length ? AudioPlayer(trackObjs(test, q.audio), { title: `Audio soal ${q.n}`, playAll: true, compact: true }) : null)
        : TtsPlayer(ttsSegments(test, q), { title: `Soal ${q.n}`, compact: true });
    const bmKey = `q:${test.id}:${q.n}`;
    return h('article', { class: `card review ${r.status}`, id: `r${q.n}` },
      h('div', { class: 'q-head' }, h('h3', {}, `Soal ${q.n}`), h('span', { class: `status ${r.status}` }, statusTxt), markedSet.has(r.n) ? h('span', { class: 'flag-pill' }, '🚩 Ditandai') : null,
        h('button', { class: 'btn ghost small', type: 'button', onclick: (e) => { const on = store.toggleBookmark(bmKey, { type: 'question', title: `${test.title} — Soal ${q.n}`, href: `#/result/${a.id}` }); e.target.textContent = on ? '★ ' + t('bookmarked') : '☆ ' + t('bookmark'); } },
          store.isBookmarked(bmKey) ? '★ ' + t('bookmarked') : '☆ ' + t('bookmark'))),
      h('p', { class: 'answers' }, `${t('yourAnswer')}: `, h('strong', {}, r.given ? `(${r.given})` : '—'), ' · ', `${t('correctAnswer')}: `, h('strong', {}, q.answer ? `(${q.answer})` : '—')),
      q.answerNote ? h('p', { class: 'note small' }, `Catatan kunci jawaban: ${q.answerNote}. Jawaban diambil dari posisi pada lembar kunci resmi.`) : null,
      r.status === 'ungradable' ? h('p', { class: 'note small' }, 'Kunci jawaban untuk soal ini tidak dapat diverifikasi, sehingga tidak dihitung dalam skor.') : null,
      questionBody(test, q, { review: true, result: r }),
      audio,
      explainPanel(test, q, ex, r.given),
      test.skill === 'listening' ? h('details', { class: 'transcript', open: r.status !== 'correct' || null },
        h('summary', {}, t('transcript') + ' (dari naskah resmi)'),
        q.transcriptIntro ? h('div', { class: 'zh tr-intro', lang: 'zh-Hant', html: escBr(q.transcriptIntro) }) : (leadQ?.transcriptIntro ? h('div', { class: 'zh tr-intro', lang: 'zh-Hant', html: escBr(leadQ.transcriptIntro) }) : null),
        q.transcript ? h('div', { class: 'zh', lang: 'zh-Hant', html: escBr(q.transcript) }) : h('p', { class: 'muted' }, 'Transkrip soal ini tidak ditemukan di naskah; lihat transkrip lengkap di bawah.')) : null);
  });
  const tab = (k, label) => h('a', { class: 'tab' + (filter === k ? ' on' : ''), href: `#/result/${aid}?f=${k}` }, label);
  return h('div', { class: 'wrap' },
    h('nav', { class: 'crumbs' }, h('a', { href: '#/exercise' }, 'TOCFL Exercise'), ' / ', h('a', { href: `#/test/${test.id}` }, test.title), ' / Hasil'),
    h('h1', {}, `Hasil: ${a.title || test.title}`),
    h('p', { class: 'muted' }, `${a.mode === 'exam' ? 'Simulasi tes' : 'Latihan'} · ${fmtDate(a.submittedAt)} · durasi ${fmtTime(a.durationSec)}`),
    h('section', { class: 'score-cards' },
      h('div', { class: `big-score ${scoreClass(a)}` }, h('span', {}, `${s.percent}%`), h('small', {}, `${s.correct} dari ${s.gradable} soal yang dinilai`)),
      h('div', { class: 'stat good' }, h('strong', {}, s.correct), t('correct')),
      h('div', { class: 'stat low' }, h('strong', {}, s.incorrect), t('incorrect')),
      h('div', { class: 'stat' }, h('strong', {}, s.unanswered), t('unanswered')),
      s.ungradable ? h('div', { class: 'stat' }, h('strong', {}, s.ungradable), t('ungradable')) : null),
    h('p', { class: 'note small' }, 'Skor ini adalah skor mentah (jumlah benar) dan persentase. Situs ini tidak menghitung skor skala resmi TOCFL, ambang kelulusan, atau hasil sertifikasi.'),
    h('section', { class: 'card' }, h('h2', { class: 'h3' }, 'Per bagian'),
      h('table', { class: 'table' }, h('thead', {}, h('tr', {}, h('th', {}, 'Bagian'), h('th', {}, 'Benar'), h('th', {}, '%'))),
        h('tbody', {}, ...a.byPart.filter((p) => p.gradable > 0).map((p) => h('tr', {}, h('td', {}, `${p.title} ${p.subtitle || ''}`), h('td', {}, `${p.correct}/${p.gradable}`), h('td', {}, `${pct(p.correct, p.gradable)}%`)))))),
    h('div', { class: 'row-links' }, h('a', { class: 'btn primary', href: a.retry || `#/test/${test.id}/run?mode=${a.mode}` }, a.range ? 'Ulangi bagian ini' : 'Ulangi tes'), h('a', { class: 'btn', href: '#/mistakes' }, 'Ulas semua kesalahan'), backBtn),
    h('div', { class: 'tabs', role: 'tablist' }, tab('all', `Semua (${a.results.length})`), tab('wrong', `Salah/kosong (${s.incorrect + s.unanswered})`), tab('correct', `Benar (${s.correct})`), markedSet.size ? tab('marked', `🚩 Ditandai (${markedSet.size})`) : null),
    ...items,
    h('div', { class: 'row-links' }, h('a', { class: 'btn', href: backHref }, '← Kembali ke pilihan latihan')),
    test.fullScript ? h('details', { class: 'card' }, h('summary', {}, t('fullScript')), h('div', { class: 'zh script', lang: 'zh-Hant', html: escBr(test.fullScript) })) : null);
}
