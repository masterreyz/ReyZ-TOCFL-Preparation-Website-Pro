# Content completeness report — ReyZ TOCFL Preparation Website

Generated from the content data by `python scripts/report.py`. Source inventory taken 2026-11-16 from `D:\Material For TOCFL Website Claude`.

## 1. Source inventory

| Area | Items found | Size |
|---|---|---|
| TOCFL Study — textbooks (A1–C2) | 6 PDFs, 2,215 pages | ≈515 MB |
| TOCFL Study — workbooks (A1–C2) | 6 PDFs, 540 pages | ≈74 MB |
| TOCFL Study — audio | 937 MP3 in 11 folders (no C2 workbook audio folder exists) | ≈1.69 GB |
| TOCFL Exercise — full mock tests | 30 tests (Novice L/R, A L1–5/R1–5, B L1–5/R1–5, C L1–4/R1–4): booklet + answer key + listening script PDFs | ≈75 PDFs |
| TOCFL Exercise — mock-test audio | 916 MP3 | not measured exactly (≈1 GB) |
| TOCFL Exercise — per-question bank ("Per Part" folders) | 22 answer sheets (.xlsx); ≈1,100 item PDFs, ≈1,100 script PDFs, ≈533 MP3 (listing was capped, counts approximate) | ≈1.1 GB |
| Test instructions (ID/EN) | 10 PDFs | small |

## 2. TOCFL Exercise — mock tests

| Test | Questions | Gradable | Parsed issues |
|---|---|---|---|
| Novice Listening · Series 1 | 25 | 25 | 0 |
| Novice Reading · Series 1 | 25 | 25 | 0 |
| Band A Listening · Series 1 | 50 | 50 | 1 |
| Band A Listening · Series 2 | 50 | 50 | 1 |
| Band A Listening · Series 3 | 50 | 50 | 1 |
| Band A Listening · Series 4 | 50 | 50 | 1 |
| Band A Listening · Series 5 | 50 | 50 | 0 |
| Band A Reading · Series 1 | 50 | 50 | 0 |
| Band A Reading · Series 2 | 50 | 50 | 0 |
| Band A Reading · Series 3 | 50 | 50 | 0 |
| Band A Reading · Series 4 | 50 | 50 | 0 |
| Band A Reading · Series 5 | 50 | 50 | 0 |
| Band B Listening · Series 1 | 50 | 50 | 0 |
| Band B Listening · Series 2 | 50 | 50 | 0 |
| Band B Listening · Series 3 | 50 | 50 | 0 |
| Band B Listening · Series 4 | 50 | 50 | 0 |
| Band B Listening · Series 5 | 50 | 50 | 1 |
| Band B Reading · Series 1 | 50 | 50 | 0 |
| Band B Reading · Series 2 | 50 | 50 | 0 |
| Band B Reading · Series 3 | 50 | 50 | 0 |
| Band B Reading · Series 4 | 50 | 50 | 0 |
| Band B Reading · Series 5 | 50 | 50 | 0 |
| Band C Listening · Series 1 | 50 | 50 | 0 |
| Band C Listening · Series 2 | 50 | 50 | 0 |
| Band C Listening · Series 3 | 50 | 50 | 0 |
| Band C Listening · Series 4 | 50 | 50 | 0 |
| Band C Reading · Series 1 | 50 | 50 | 0 |
| Band C Reading · Series 2 | 50 | 50 | 0 |
| Band C Reading · Series 3 | 50 | 50 | 0 |
| Band C Reading · Series 4 | 50 | 50 | 0 |

**Total: 30 tests, 1450 questions, 1450 gradable against the official keys.** Every question has text (stem/options/passage) and/or a crop of the original booklet region; picture questions show the crop.

Validation findings:

- `a-l1` — answer_key_label_mismatch: answer key prints question number 44 at the position of question 34; used position (answer B)
- `a-l2` — answer_key_label_mismatch: answer key prints question number 44 at the position of question 34; used position (answer A)
- `a-l3` — answer_key_label_mismatch: answer key prints question number 44 at the position of question 34; used position (answer B)
- `a-l4` — answer_key_label_mismatch: answer key prints question number 4 at the position of question 34; used position (answer B)
- `b-l5` — parts_from_script: booklet part headers not detected; parts taken from listening script headings

Audio mapping: Band A L1–5, Band B L1–2 and Band C L1–2 map tracks to questions by the official file naming (e.g. `1-07.mp3` = Q7, `2-35-0/1` = dialogue + Q35). Novice L, Band B L3–5 and Band C L3–4 ship tracks numbered only `001…`; their per-question mapping is **not verified**, so the app plays the full ordered recording instead.

Transcripts: aligned automatically from the official listening scripts; the complete official script is also shown on every result page.

## 3. TOCFL Exercise — per-question bank

**Not yet imported into the website.** The importer (`pipeline/parse_partbank.py`) is written and was tested on a sample item (options, official answer and transcript extracted correctly), but the ≈2,700 files could not be transferred into the build environment in this session. Run it locally (README §4) to add these items; missing PDFs/answers are reported in `reports/partbank_validation.json` and never guessed.

## 4. TOCFL Study

| Book | Pages | Lessons located | Audio files | Tracks pinned to a page | Lessons migrated to text |
|---|---|---|---|---|---|
| a1-te | 399 | 15 | 141 | 56 | 1 |
| a1-wo | 130 | 15 | 90 | 68 | 0 |
| a2-te | 456 | 15 | 150 | 86 | 0 |
| a2-wo | 128 | 15 | 61 | 54 | 0 |
| b1-te | 360 | 12 | 127 | 69 | 0 |
| b1-wo | 98 | 12 | 25 | 17 | 0 |
| b2-te | 375 | 12 | 145 | 67 | 0 |
| b2-wo | 87 | 12 | 25 | 20 | 0 |
| c1-te | 299 | 10 | 86 | 18 | 0 |
| c1-wo | 55 | 10 | 11 | 0 | 0 |
| c2-te | 326 | 10 | 76 | 13 | 0 |
| c2-wo | 42 | 10 | 0 | 0 | 0 |

All 148 lessons are reachable with verified titles, page ranges and their audio. Every page of every book is available in the page reader (2,755 pages rendered to WebP).

**Text migration status:** A1 Textbook Lesson 1 is migrated as structured web text (Dialogue I & II with pinyin and the book's English translation, Vocabulary I & II — 43 entries — with audio placed beside each section), transcribed manually from the page images and checked against them. All other lessons — and the grammar/exercise/culture sections of A1 L1 — are shown as original page images with linked audio. The books' embedded text layer is a low-quality OCR (tone marks and characters corrupted, e.g. `K面wen` for Kāiwén), so it is not used as lesson text.

## 5. Uncertain or unresolved

- Lesson boundaries come from running headers, lesson openers and audio-track markers; 4 boundaries were corrected manually (C1 textbook L10; B1, C1, C2 workbooks from their contents pages). Other boundaries were not individually checked page by page.
- About half of the textbook audio tracks were pinned to the exact page where their number is printed; the rest are listed under their lesson.
- Four Band A listening answer keys print a wrong question number at position 34 ("44" or "4"); the answer at that position is used and the note is displayed in the review.
- Redistribution permission for the textbooks (NTNU MTC / Linking Publishing) and SC-TOP mock tests has not been established; see README §6 before publishing publicly.