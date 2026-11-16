# ReyZ TOCFL Preparation Website

*Created by Reynard Agahari* — Threads [@reynard_agahari](https://www.threads.com/@reynard_agahari) · Instagram [@reynard_agahari](https://www.instagram.com/reynard_agahari/) · TikTok [@reynardagahari](https://www.tiktok.com/@reynardagahari)

A static learning website for TOCFL preparation:

- **TOCFL Study**: 當代中文課程 (*A Course in Contemporary Chinese*) vols. 1–6 (A1–C2), textbook + workbook. It is organised Level → Book → Lesson, with lesson audio placed beside the page or section it belongs to.
- **TOCFL Exercise**: 30 official mock tests (Band Novice, A, B, C; listening + reading; 1,450 questions). They run as interactive tests with practice and exam-simulation modes, grading against the official answer keys, transcripts, audio replay, and mistake review.
- **Learning tools**: Continue Learning, progress per level, attempt history (retries never overwrite), bookmarks, mistake review, search (hanzi, pinyin with or without tones, English), light/dark mode, adjustable text size, progress export/import/reset.

The UI is in Indonesian (strings live in `src/i18n.js`). Progress is stored in the browser's `localStorage`, so it belongs to one browser on one device. Use **Pengaturan → Ekspor/Impor** to move it.

See `reports/COMPLETENESS.md` for what has been migrated and `reports/TEST_REPORT.md` for what was tested.

---

## 1. Requirements

- **Node.js 20+** (for the website)
- *Only to re-run the content pipeline:* **Python 3.10+** with `pip install pillow openpyxl`, plus **poppler-utils** (`pdftotext`, `pdftoppm`, `pdfimages`). On Windows, poppler is available from <https://github.com/oschwartz10612/poppler-windows/releases>; add its `bin` folder to PATH. Tesseract (`chi_tra`) is only needed for lesson titles that are not in `pipeline/verified_titles.py`.

## 2. Run locally

```bash
npm install
# copy the 1,853 audio files from your material folder into public/media/audio (ASCII-safe names)
npm run sync-media -- "D:\Material For TOCFL Website Claude"
npm run dev          # http://localhost:5173
```

`sync-media` reads `public/content/media-manifest.json`, copies only missing or changed files, and writes `reports/media-sync-report.json` listing any file it could not find. Without it the site still works, but audio players show a "file not available" message.

## 3. Build and check

```bash
npm test             # content validation + grading tests against the real answer keys
npm run build        # -> dist/  (includes page images and question crops, ~170 MB, excluding audio)
npm run preview      # http://localhost:4173
python scripts/e2e.py   # optional browser test (needs: pip install playwright && playwright install chromium)
```

## 4. Content pipeline (re-run or extend)

Everything in `public/content` and `public/media/{ex,study}` is generated from your PDFs. Run these from the project root, passing the folder that contains `TOCFL Study` and `TOCFL Exercise`:

```bash
SRC="D:\Material For TOCFL Website Claude"
python pipeline/parse_mock.py   "$SRC" .     # 30 mock tests -> public/content/exercise + question crops
python pipeline/parse_study.py  "$SRC" .     # books/lessons/audio links -> public/content/study
python pipeline/render_pages.py "$SRC" . 100 # every book page -> public/media/study/<book>/pNNN.webp
python pipeline/parse_partbank.py "$SRC" . 25   # per-question bank ("Per Part" folders) -> practice sets
python pipeline/finalize.py .                # audio targets + media manifest (always run last)
python scripts/report.py                     # regenerate reports/COMPLETENESS.md
npm run sync-media -- "$SRC"
```

- **Adding a mock test:** add an entry to `pipeline/mock_catalog.py` (folder, file names, audio track list), then re-run `parse_mock.py` and `finalize.py`.
- **Migrating a lesson to web text:** create `public/content/study/lessons/<lessonId>.json`. Use `a1-te-l01.json` as the template; block types are `heading`, `dialogue`, `vocab`, `text`, `note`, and `"track": "01-03"` puts that track's player on the block. Then re-run `parse_study.py` (it sets `migrated`) and `npm run build-index`. Hand-written lesson files are never overwritten.
- **Wrong lesson boundary:** add it to `BOUNDARY_OVERRIDES` in `pipeline/parse_study.py`.

Stable IDs: tests `a-l1`, `b-r3`; questions are numbered within their test; lessons are `a1-te-l01` (level-book-lesson). Saved progress refers to these IDs, so re-running the pipeline keeps progress.

## 5. Publish to GitHub

```bash
git init
git add .
git commit -m "ReyZ TOCFL Preparation Website"
git branch -M main
git remote add origin https://github.com/<your-user>/reyz-tocfl.git
git push -u origin main
```

`.gitignore` excludes `node_modules/`, `dist/` and `public/media/audio/` (≈3 GB). The repository holds the app, content JSON, page images and question crops (≈170 MB), which is under GitHub's 1 GB recommended repository size.

**Uploading the repository does not publish a website.** Publishing is a separate step (§6).

## 6. Deploy the website (read first)

**Permissions.** The textbooks and audio (NTNU Mandarin Training Center / Linking Publishing) and the mock tests (SC-TOP) are copyrighted third-party materials. Branding identifies the site's creator only. Before making a public site that contains them, confirm you have permission to redistribute them. Without permission, keep the site local (`npm run dev` / `npm run preview`) or restrict access.

**Hosting constraints (checked 2026-11-16).** GitHub Pages: published site ≤ 1 GB, deployment timeout 10 minutes, soft bandwidth limit 100 GB/month. The audio (~3 GB) therefore cannot be served from GitHub Pages. Git LFS does not solve this: LFS only changes how the repository stores large files, and the published site would still exceed the 1 GB limit. Recommended setup:

1. **App, content, page images and crops** go on GitHub Pages: in the repo go to *Settings → Pages → Source: GitHub Actions*, then run the **Deploy to GitHub Pages** workflow manually (*Actions* tab). It is manual on purpose, so nothing goes public until you decide.
2. **Audio** goes on object storage with public read access and CORS allowing your Pages origin (e.g. Cloudflare R2, Backblaze B2, or any S3-compatible bucket). Upload `public/media/audio/` keeping the same folder structure.
3. In the deployed `config.js`, set `audioBase: 'https://<your-bucket-url>/audio/'` (no rebuild needed; it is a plain file in `dist/`).

The site uses hash routing (`#/…`) and relative asset paths (`base: './'`), so it works under `https://<user>.github.io/<repo>/` and survives page refreshes on any route.

## 7. Project layout

```
index.html, src/          app (vanilla JS modules, Vite)
  views/                  home, study, exercise (runner/review), personal tools, search, about
  grading.js              pure grading logic (unit-tested)
  store.js                localStorage progress (versioned, export/import)
  audio.js                accessible audio player (one plays at a time, no autoplay)
public/config.js          runtime config: mediaBase / audioBase
public/content/           generated JSON (exercise/, study/, search.json, media-manifest.json)
public/media/             ex/ (question crops), study/ (page images), audio/ (copied by sync-media, not committed)
pipeline/                 Python import scripts (see §4)
scripts/                  sync-media, search index, validation, grading tests, e2e test, report
reports/                  completeness, validation and test reports
PROGRESS.md               status and next steps for continuing the migration
```
