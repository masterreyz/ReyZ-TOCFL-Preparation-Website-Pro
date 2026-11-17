# Progress — ReyZ TOCFL Preparation Website

_Last updated: 2026-11-17_

## Done
- Inventory of `TOCFL Study` and `TOCFL Exercise` (see `reports/COMPLETENESS.md` §1).
- App: home/dashboard, study library (level → book → lesson, page reader), exercise library, test runner (practice + exam simulation), grading, results/review with transcripts and audio, mistake review, bookmarks, history, search, settings (theme, export/import/reset), about/credits, branding. Responsive, light/dark.
- **All 30 mock tests migrated** (1,450 questions, official keys, transcripts, crops, audio mapping).
- Study structure: 148 lessons located with verified titles; all 2,755 pages rendered; 937 audio files linked to lessons (≈half pinned to their page).
- A1 Textbook L1: dialogues + vocabulary migrated to structured text (validation milestone).
- Pipeline, validation, grading tests, e2e test, completeness report, README, manual GitHub Pages workflow.

## Next steps (in order)
1. On your PC: `npm install`, `npm run sync-media -- "<folder>"`, `npm run dev`, then check `reports/media-sync-report.json` shows 0 missing.
2. Per-part bank: `python pipeline/build_partbank.py "<folder>" . [--only-complete]`, then `python pipeline/finalize.py .`; review `reports/partbank_validation.json` (see table below).
3. Continue lesson text migration: the rest of A1 L1 (grammar, exercises, culture), then A1 L2… The page images in `public/media/study/<book>/` are the source; follow the `a1-te-l01.json` format. Estimated 25–30 pages per lesson, 148 lessons.
4. Verify per-question audio mapping for Novice L, Band B L3–5 and Band C L3–4 (tracks are only numbered); once confirmed, set `kind: "by-filename"`-style mapping in `pipeline/mock_catalog.py`.
5. Resolve redistribution permission, then deploy (README §6): host audio on object storage and set `audioBase`.

## Known limitations
- Most lessons are page images, not text, until migrated. Search covers lesson titles, migrated lessons and all test questions.
- The textbooks' embedded OCR layer is unusable for text (corrupted pinyin/characters), so it is not used.
- Lesson boundaries are heuristic except for the overrides listed in `pipeline/parse_study.py`.
- Exam-simulation timing and audio rules are configurable approximations, not the official exam procedure.
- Progress is per browser/device (localStorage); no cross-device sync.


## Study text migration (option a: accurate, lesson by lesson, in book order)
Chosen 2026-11-16. Order: A1 Textbook L1→L15, A1 Workbook L1→L15, then A2, B1, B2, C1, C2 (textbook, then workbook).

| Lesson | Pages (PDF) | Status |
|---|---|---|
| A1 Textbook L1 歡迎你來臺灣！ | 28–49 | ✅ complete, checked page by page (zhuyin column not copied; pinyin given) |
| A1 Textbook L2 我的家人 | 50–69 | ✅ complete, checked page by page (zhuyin column not copied; photos of real people not copied) |
| A1 Textbook L3 週末做什麼？ | 70–91 | ✅ complete, checked page by page (zhuyin column not copied; culture photos not copied) |
| A1 Textbook L4 請問一共多少錢？ | 92–111 | ✅ complete, checked page by page (zhuyin column not copied; culture photos not copied) |
| A1 Textbook L5 牛肉麵真好吃 | 112–129 | ✅ complete, checked page by page (zhuyin column not copied; photos of real people not copied) |
| A1 Textbook L6 他們學校在山上 | 130–157 | ✅ complete — **original mode** (own explanations, examples, practice dialogues, exercises, culture notes; book word list + audio tracks linked) |
| A1 Textbook L7 早上九點去KTV | 158–185 | ✅ complete — original mode (adds telling-time table, punctuation table) |
| A1 Textbook L8 坐火車去臺南 | 186–207 | ✅ complete — original mode (5 grammar points: 跟, 怎麼, 比較, 又…又…, 比; adds -iang/-ying pinyin note) |
| A1 Textbook L9 放假去哪裡玩？ | 208–227 | ✅ complete — original mode (5 grammar points: time-when vs. time-duration, verb+duration, 的時候, 有時候…有時候…, 要是…就…) |
| A1 Textbook L10 | 228– | ⏭ next (original mode) |
| all other lessons | — | page images until migrated |

### Original mode (from A1 L6 onward, chosen 2026-11-17)
The book's dialogues, exercises, explanations and illustrations are **not** copied or lightly reworded. Each lesson is written fresh:
- Vocabulary: the book's word list (word, pinyin, part of speech) with glosses in our own words; vocab tracks stay linked.
- Dialogues: new practice dialogues on the lesson topic using that vocabulary. A text block with the book's track (`track`) points to the original recording/page.
- Grammar: same grammar points, explained in our own words with our own example sentences (pinyin + English), plus our own exercises.
- Activities / culture / characters / checklist: own wording; facts checked; no book photos, charts or drawings.
- Lesson JSON carries `"mode": "original"` (the lesson page shows a matching banner). Builder: see the commit for A1 L6.
- Pinyin cross-check: `pip install pypinyin`; compare each zh/py pair (expected differences: 一/不 sandhi, neutral tones, heteronyms like 得 děi, 行 háng, 和 hàn).
- Check: every Chinese sentence, tone-marked pinyin and translation re-read; pattern use matches the book's grammar point; then build/test/e2e (add lesson checks to `scripts/e2e_pages.py`).

### Procedure per lesson (transcription mode, used for A1 L1–L5)
1. Render pages at 120 dpi: `pdftoppm -r 120 -f <start> -l <end> -png "<book>.pdf" /tmp/p`.
2. Transcribe each page into blocks (page-group files, then assemble into `content/study/lessons/<lessonId>.json`; see a1-te-l01.json / a1-te-l02.json).
   Block types: heading, dialogue (+translation), vocab, text, examples, pairs, exchanges, exercise (+image), table, figure, checklist, note.
   Each block has a `source.pages` reference. Illustrations needed for exercises go to `media/study/lessons/<lessonId>/`.
   Photos of people are not copied (link to the original page instead).
3. Check every page against the image (characters, tone-marked pinyin, numbering, punctuation), then set `"status": "complete"`.
4. `python pipeline/parse_study.py "<SRC>" .` → `python pipeline/finalize.py .` → `npm run build` → `npm test` → `python scripts/e2e_pages.py` → commit + push.

## TOCFL Exercise explanations (pinyin + English)

Pinyin is generated for every Chinese text. English is written per test in `pipeline/explain_src/<testId>.json` (see README §4). Order of work: Novice → A → B Reading → C Reading → B Listening → C Listening.

| Test | Segments | English |
|---|---|---|
| a-l1 | 201 | ✅ complete |
| a-l2 | 197 | ✅ complete |
| a-l3 | 240 | ✅ complete |
| a-l4 | 235 | ✅ complete |
| a-l5 | 226 | ✅ complete |
| a-r1 | 162 | ✅ complete |
| a-r2 | 160 | ✅ complete |
| a-r3 | 150 | ✅ complete |
| a-r4 | 156 | ✅ complete |
| a-r5 | 153 | ✅ complete |
| b-l1 | 370 | ⏭ pinyin only — English to do |
| b-l2 | 359 | ⏭ pinyin only — English to do |
| b-l3 | 407 | ⏭ pinyin only — English to do |
| b-l4 | 425 | ⏭ pinyin only — English to do |
| b-l5 | 446 | ⏭ pinyin only — English to do |
| b-r1 | 319 | ✅ complete |
| b-r2 | 325 | ✅ complete |
| b-r3 | 321 | ✅ complete |
| b-r4 | 319 | ⏭ pinyin only — English to do |
| b-r5 | 326 | ⏭ pinyin only — English to do |
| c-l1 | 438 | ⏭ pinyin only — English to do |
| c-l2 | 463 | ⏭ pinyin only — English to do |
| c-l3 | 404 | ⏭ pinyin only — English to do |
| c-l4 | 456 | ⏭ pinyin only — English to do |
| c-r1 | 347 | ⏭ pinyin only — English to do |
| c-r2 | 310 | ⏭ pinyin only — English to do |
| c-r3 | 316 | ⏭ pinyin only — English to do |
| c-r4 | 345 | ⏭ pinyin only — English to do |
| novice-l1 | 75 | ✅ complete |
| novice-r1 | 45 | ✅ complete |

## Per-part question bank (TOCFL Exercise → "Bank soal per bagian")
Built by `pipeline/build_partbank.py` from each part folder's `*_Answer.xlsx` + item PDFs (original item image, official key, script for listening).

| Section | Folder | Items | Questions | Sets |
|---|---|---|---|---|
| n-l1 | 1. TOCFL Band Novice Per Part/Part 1. Listening | 31 | 31 | 2 |
| n-l2 | 1. TOCFL Band Novice Per Part/Part 2. Listening | 30 | 30 | 2 |
| n-l3 | 1. TOCFL Band Novice Per Part/Part 3. Listening | 9 | 9 | 1 |
| n-r1 | 1. TOCFL Band Novice Per Part/Part 4. Reading | 26 | 26 | 2 |
| n-r2 | 1. TOCFL Band Novice Per Part/Part 5. Reading | 18 | 18 | 1 |
| a-r-sentence | 2. TOCFL Band A Per Part/Reading TOCFL A  Single sentence comprehension | 112 | 112 | 6 |
| a-r-paragraph | 2. TOCFL Band A Per Part/Reading TOCFL A Complete Paragraph | 28 | 140 | 7 |
| a-r-gap | 2. TOCFL Band A Per Part/Reading TOCFL A Fill in the blanks | 23 | 115 | 6 |
| a-r-pic | 2. TOCFL Band A Per Part/Reading TOCFL A Interpretation of the image | 110 | 110 | 6 |
| a-r-comp | 2. TOCFL Band A Per Part/Reading TOCFL A Reading Comprehension | 61 | 61 | 4 |
| b-r-gap | 3. TOCFL Band B Per Part/Fill in the blanks with the correct words | 27 | 151 | 9 |
| b-r-comp | 3. TOCFL Band B Per Part/Reading comprehension | 98 | 232 | 13 |
| c-r-comp | 4. TOCFL Band C Per Part/Reading Comprehension Band C | 34 | 133 | 8 |
| c-r-gap | 4. TOCFL Band C Per Part/Reading Fill in the blanks Band C | 17 | 95 | 6 |

- Band A Reading “Interpretation of the image”: the answer key lists 162 items but only 110 item PDFs exist in the source folder (Q01163500–Q01168600 are absent); the 110 available are included, the 52 others are listed in `reports/partbank_validation.json`.
- Listening parts of Band A, B and C: pending — their item and script PDFs are still being copied from the source folder.
