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
2. Run `python pipeline/parse_partbank.py "<folder>" . 25` and `python pipeline/finalize.py .` to add the per-question bank, then review `reports/partbank_validation.json`.
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
| A1 Textbook L7 早上九點去KTV | 158–185 | ⏭ next (original mode) |
| all other lessons | — | page images until migrated |

### Original mode (from A1 L6 onward, chosen 2026-11-17)
The book's dialogues, exercises, explanations and illustrations are **not** copied or lightly reworded. Each lesson is written fresh:
- Vocabulary: the book's word list (word, pinyin, part of speech) with glosses in our own words; vocab tracks stay linked.
- Dialogues: new practice dialogues on the lesson topic using that vocabulary. A text block with the book's track (`track`) points to the original recording/page.
- Grammar: same grammar points, explained in our own words with our own example sentences (pinyin + English), plus our own exercises.
- Activities / culture / characters / checklist: own wording; facts checked; no book photos, charts or drawings.
- Lesson JSON carries `"mode": "original"` (the lesson page shows a matching banner). Builder: see the commit for A1 L6.
- Check: every Chinese sentence, tone-marked pinyin and translation re-read; pattern use matches the book's grammar point; then build/test/e2e (add lesson checks to `scripts/e2e_pages.py`).

### Procedure per lesson (transcription mode, used for A1 L1–L5)
1. Render pages at 120 dpi: `pdftoppm -r 120 -f <start> -l <end> -png "<book>.pdf" /tmp/p`.
2. Transcribe each page into blocks (page-group files, then assemble into `content/study/lessons/<lessonId>.json`; see a1-te-l01.json / a1-te-l02.json).
   Block types: heading, dialogue (+translation), vocab, text, examples, pairs, exchanges, exercise (+image), table, figure, checklist, note.
   Each block has a `source.pages` reference. Illustrations needed for exercises go to `media/study/lessons/<lessonId>/`.
   Photos of people are not copied (link to the original page instead).
3. Check every page against the image (characters, tone-marked pinyin, numbering, punctuation), then set `"status": "complete"`.
4. `python pipeline/parse_study.py "<SRC>" .` → `python pipeline/finalize.py .` → `npm run build` → `npm test` → `python scripts/e2e_pages.py` → commit + push.
