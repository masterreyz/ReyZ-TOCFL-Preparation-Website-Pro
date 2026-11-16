# Progress — ReyZ TOCFL Preparation Website

_Last updated: 2026-11-16 (session 1)_

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
