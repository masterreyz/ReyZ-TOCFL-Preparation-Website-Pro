# Test report — ReyZ TOCFL Preparation Website (2026-11-16)

## Automated checks (all passing)

| Check | Command | Result |
|---|---|---|
| Content validation (numbering 1..N, answer letters present among options, crops exist, every listening test has audio, lesson block tracks exist) | `npm run validate` | OK — 1,450 questions, 1,450 gradable; 0 errors; 4 warnings (the answer-key label typos listed in COMPLETENESS.md) |
| Grading against the real answer keys (all-correct = 100 %, all-empty, all-wrong, per-part sums, ungradable excluded from the denominator, spot checks vs printed keys incl. the shared Novice key) | `node scripts/test-grading.mjs` | Passed for all 30 tests |
| Production build | `npm run build` | OK (JS 50 kB, CSS 15 kB gzip-small; dist ≈171 MB incl. page images/crops) |
| Browser end-to-end (headless Chrome, production build) | `python scripts/e2e.py` | **23/23 passed** |

### End-to-end checks performed
1. Home renders the exact title, the "Created by Reynard Agahari" signature, and the three social links (correct URLs).
2. **Full listening flow (Band A Listening S1, practice):** the picture crop for Q1 is shown, the per-question audio plays (0:02 / 0:30, no error), two answers are chosen, the page is **refreshed and both answers persist**, then the test is submitted. The result shows 2/50 as expected from the key, and transcripts appear only after submission.
3. **Full reading flow (Band A Reading S1, exam mode):** all 50 questions are answered with the official key and the result is **100 %**. A retry in practice mode creates a **second attempt and the first is kept**. Mistake review lists the test.
4. A1 Textbook Lesson 1 (migrated): the dialogue text and the 43-row vocabulary table render, the lesson audio (01-01) plays, and *Tandai selesai* works. A2 L3 (not yet migrated) renders its original pages.
5. Search: `烏龍茶` (hanzi) and `wulong` (toneless pinyin) both find the lesson vocabulary.
6. Mobile 375 px: no horizontal overflow on home, reading test, lesson, or result routes.
7. No uncaught JavaScript errors during the run.

Audio playback was tested with 6 real MP3s copied by `sync-media`. The other 1,847 files are copied on your machine by the same script, which reports any file it cannot find.

## Manual / visual checks
- Crops of picture questions (Band A reading/listening, Novice) compared against the booklet pages: correct regions, readable.
- Contact sheets of all 76 textbook lesson headers were read to verify lesson titles.
- A1 L1 transcription (pinyin with tone marks, translations, vocabulary, parts of speech) was checked against the page images.

## Not tested here
- Audio for the 1,847 files not copied into the build environment (paths are generated from the folder listings; `sync-media` verifies them on your machine).
- The per-question bank importer on the full folder (tested on one sample item).
- A live deployed URL (no deployment was made; see README §6).
- Screen-reader walkthrough (semantic structure, labels and focus states were implemented but not tested with assistive technology).

## Live deployment check — https://masterreyz.github.io/ReyZ-TOCFL-Preparation-Website-Pro/ (2026-11-16)

Run in a real browser (Claude desktop browser pane, Windows) against the public URL after the GitHub Pages deployment of commit 4ecbe27:
- All 21 sampled routes render (home, study levels/books/lessons/page reader, all 4 bands, test intro, search, about, settings, history, mistakes, bookmarks). Deep links survive reload because of hash routing.
- Content served: 30 tests / 1,450 questions; 90 sampled question crops → HTTP 200; page images for all 12 books → 200; search index 1,426 entries.
- Full Band B Reading S2 attempt in exam mode, answered with the official key → **100 % (50/50)**. Listening attempt → graded 1/50 as expected, review shows 50 transcripts + 50 speech players. In-progress answers saved to localStorage.
- Original audio correctly detected as absent (probe 404) → speech-synthesis players shown, no broken audio players.
- This test machine's browser exposes only English system voices (Microsoft David/Mark/Zira), so speech could not be heard here; the player and Settings correctly show the "no Mandarin voice" guidance. Speech output itself was verified with a recording mock (scripts/e2e_pages.py, 28/28) — real playback requires a Mandarin voice (Chrome/Edge online voices, or an OS voice pack).
