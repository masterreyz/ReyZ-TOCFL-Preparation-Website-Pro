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

## 6. Deploy the website (GitHub Pages)

Live site: **https://masterreyz.github.io/ReyZ-TOCFL-Preparation-Website-Pro/**

- `.github/workflows/deploy.yml` runs `npm ci`, `npm test` and `npm run build`, then publishes `dist/` on every push to `main`. In *Settings → Pages*, **Source** must be **GitHub Actions**; if it is set to "Deploy from a branch", GitHub serves the raw source and the site will not load.
- The site uses hash routing (`#/…`) and relative asset paths (`base: './'`), so it works under the `/ReyZ-TOCFL-Preparation-Website-Pro/` subpath and deep links survive a refresh. The published size is ≈171 MB, below the 1 GB Pages limit.

**Audio on the online site.** The original recordings (~3 GB) exceed the GitHub Pages size limit and are not deployed. `public/config.js` (`originalAudio: 'auto'`) checks whether they are reachable:
- **Found** (local use after `npm run sync-media`, or recordings hosted elsewhere with `audioBase` pointing to them): the original recordings play.
- **Not found** (GitHub Pages): **Mandarin speech synthesis** through the browser's Web Speech API. It reads the official listening scripts (per question in practice mode, the whole test in order in exam mode, and in the review) and the text of migrated lessons (whole dialogue or vocabulary list, plus a 🔊 button per line and per word). It prefers Taiwan Mandarin voices. Voice quality depends on the device: Edge ("Microsoft … Natural, Taiwan") and Chrome ("Google 國語（臺灣）") are best, and iOS, macOS and Android include built-in voices. Users can choose a voice in *Pengaturan*.
- No API key or server is involved. A cloud TTS API such as Google Cloud TTS would require a secret key in public client code and is billed per character, so it was not used.
- Limitation: synthesized speech is not the official recording. Lessons that are still page images have no text to synthesize, so they have no audio online until migrated.

**Permissions.** The textbooks (NTNU MTC / Linking Publishing) and mock tests (SC-TOP) are copyrighted third-party materials; the repository and site are public by the owner's decision.

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
