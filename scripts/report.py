"""Generate reports/COMPLETENESS.md from the content data (run after the pipeline)."""
import json
from collections import Counter
from pathlib import Path

C = Path("content")
idx = json.loads((C / "exercise/index.json").read_text(encoding="utf-8"))
mock = [t for t in idx if not t["id"].startswith("pb-")]
pb = [t for t in idx if t["id"].startswith("pb-")]
val = json.loads(Path("reports/exercise_validation.json").read_text(encoding="utf-8"))
study = json.loads((C / "study/index.json").read_text(encoding="utf-8"))
struct = json.loads(Path("reports/study_structure.json").read_text(encoding="utf-8"))
L = []
w = L.append
w("# Content completeness report — ReyZ TOCFL Preparation Website\n")
w("Generated from the content data by `python scripts/report.py`. Source inventory taken 2026-11-16 from `D:\\Material For TOCFL Website Claude`.\n")
w("## 1. Source inventory\n")
w("| Area | Items found | Size |\n|---|---|---|")
w("| TOCFL Study — textbooks (A1–C2) | 6 PDFs, 2,215 pages | ≈515 MB |")
w("| TOCFL Study — workbooks (A1–C2) | 6 PDFs, 540 pages | ≈74 MB |")
w("| TOCFL Study — audio | 937 MP3 in 11 folders (no C2 workbook audio folder exists) | ≈1.69 GB |")
w("| TOCFL Exercise — full mock tests | 30 tests (Novice L/R, A L1–5/R1–5, B L1–5/R1–5, C L1–4/R1–4): booklet + answer key + listening script PDFs | ≈75 PDFs |")
w("| TOCFL Exercise — mock-test audio | 916 MP3 | not measured exactly (≈1 GB) |")
w("| TOCFL Exercise — per-question bank (\"Per Part\" folders) | 22 answer sheets (.xlsx); ≈1,100 item PDFs, ≈1,100 script PDFs, ≈533 MP3 (listing was capped, counts approximate) | ≈1.1 GB |")
w("| Test instructions (ID/EN) | 10 PDFs | small |\n")
w("## 2. TOCFL Exercise — mock tests\n")
w("| Test | Questions | Gradable | Parsed issues |\n|---|---|---|---|")
for t in mock:
    w(f"| {t['title']} | {t['questions']} | {t['gradable']} | {t['issues']} |")
tq = sum(t['questions'] for t in mock)
w(f"\n**Total: {len(mock)} tests, {tq} questions, {sum(t['gradable'] for t in mock)} gradable against the official keys.** Every question has text (stem/options/passage) and/or a crop of the original booklet region; picture questions show the crop.\n")
w("Validation findings:\n")
for v in val:
    w(f"- `{v['test']}` — {v['kind']}: {v.get('detail', '')}")
w("\nAudio mapping: Band A L1–5, Band B L1–2 and Band C L1–2 map tracks to questions by the official file naming (e.g. `1-07.mp3` = Q7, `2-35-0/1` = dialogue + Q35). Novice L, Band B L3–5 and Band C L3–4 ship tracks numbered only `001…`; their per-question mapping is **not verified**, so the app plays the full ordered recording instead.\n")
w("Transcripts: aligned automatically from the official listening scripts; the complete official script is also shown on every result page.\n")
w("## 3. TOCFL Exercise — per-question bank\n")
if pb:
    w(f"Imported: {len(pb)} practice sets, {sum(t['questions'] for t in pb)} questions.\n")
else:
    w("**Not yet imported into the website.** The importer (`pipeline/parse_partbank.py`) is written and was tested on a sample item (options, official answer and transcript extracted correctly), but the ≈2,700 files could not be transferred into the build environment in this session. Run it locally (README §4) to add these items; missing PDFs/answers are reported in `reports/partbank_validation.json` and never guessed.\n")
w("## 4. TOCFL Study\n")
w("| Book | Pages | Lessons located | Audio files | Tracks pinned to a page | Lessons migrated to text |\n|---|---|---|---|---|---|")
mig = Counter()
for lv in study["levels"]:
    for b in lv["books"]:
        mig[b["id"]] = sum(1 for l in b["lessons"] if l["migrated"])
for s in struct:
    w(f"| {s['book']} | {s['pages']} | {s['lessons']} | {s['tracks']} | {s['tracksOnPage']} | {mig[s['book']]} |")
total_l = sum(s['lessons'] for s in struct)
w(f"\nAll {total_l} lessons are reachable with verified titles, page ranges and their audio. Every page of every book is available in the page reader (2,755 pages rendered to WebP).\n")
w("**Text migration status:** A1 Textbook Lesson 1 is migrated as structured web text (Dialogue I & II with pinyin and the book's English translation, Vocabulary I & II — 43 entries — with audio placed beside each section), transcribed manually from the page images and checked against them. All other lessons — and the grammar/exercise/culture sections of A1 L1 — are shown as original page images with linked audio. The books' embedded text layer is a low-quality OCR (tone marks and characters corrupted, e.g. `K面wen` for Kāiwén), so it is not used as lesson text.\n")
w("## 5. Uncertain or unresolved\n")
w("- Lesson boundaries come from running headers, lesson openers and audio-track markers; 4 boundaries were corrected manually (C1 textbook L10; B1, C1, C2 workbooks from their contents pages). Other boundaries were not individually checked page by page.")
w("- About half of the textbook audio tracks were pinned to the exact page where their number is printed; the rest are listed under their lesson.")
w("- Four Band A listening answer keys print a wrong question number at position 34 (\"44\" or \"4\"); the answer at that position is used and the note is displayed in the review.")
w("- Redistribution permission for the textbooks (NTNU MTC / Linking Publishing) and SC-TOP mock tests has not been established; see README §6 before publishing publicly.")
Path("reports/COMPLETENESS.md").write_text("\n".join(L), encoding="utf-8")
print("written reports/COMPLETENESS.md")
