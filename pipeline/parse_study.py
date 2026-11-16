"""Build the study library structure (levels -> books -> lessons) from the textbook/workbook PDFs.

Usage: python parse_study.py <SOURCE_ROOT> <OUT_ROOT>

Per book:
  * lesson boundaries from three signals in the embedded OCR layer: running header "LESSON • N",
    the lesson opener "第N課", and the first audio-track marker "NN-1"/"NN-01" printed in the book.
  * lesson titles re-OCR'd (tesseract chi_tra, 300 dpi) from the header line, flagged as OCR.
  * audio tracks linked to the page where their track marker is printed (by filename = marker).
Writes content/study/index.json and content/study/<bookId>.json. Hand-migrated lesson text lives in
content/study/lessons/<lessonId>.json and is never overwritten by this script.
"""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from study_catalog import LEVELS, BOOKS
from verified_titles import TITLES

# Manually reviewed lesson start pages that the heuristics got wrong (book -> {lesson: first PDF page}).
BOUNDARY_OVERRIDES = {
    "c1-te": {10: 237},  # L9 ends with a NOTE page (236); L10 dialogue + track 10-02 start at 237-239
    # workbooks: from each workbook's own table of contents (printed page + PDF offset measured on detected lessons)
    "b1-wo": {1: 3},                                   # offset +2
    "c1-wo": {1: 3, 2: 7, 3: 11, 4: 15, 5: 19, 6: 23, 7: 27, 8: 31, 9: 35, 10: 39},  # offset +2
    "c2-wo": {1: 5, 2: 9, 3: 13, 4: 17, 5: 21, 6: 25, 7: 29, 8: 33, 9: 37, 10: 41},  # offset +4
}

CN_NUM = {c: i for i, c in enumerate("零一二三四五六七八九十", 0)}
OCR_DIGIT = str.maketrans({"f": "1", "l": "1", "I": "1", "i": "1", "J": "1", "|": "1", "O": "0", "o": "0", "S": "5", "Z": "2"})


def cn_to_int(s):
    s = s.strip()
    if s.isdigit():
        return int(s)
    if s == "十":
        return 10
    if s.startswith("十"):
        return 10 + CN_NUM.get(s[1], 0)
    if "十" in s:
        a, b = s.split("十")
        return CN_NUM.get(a, 0) * 10 + (CN_NUM.get(b, 0) if b else 0)
    return CN_NUM.get(s, -1)


def page_texts(pdf):
    out = subprocess.run(["pdftotext", str(pdf), "-"], capture_output=True, text=True).stdout
    return out.split("\f")


def ocr_header(pdf, page):
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(["pdftoppm", "-r", "300", "-f", str(page), "-l", str(page), "-x", "0", "-y", "0", "-W", "2500", "-H", "330",
                        "-png", "-singlefile", str(pdf), f"{td}/h"], check=True)
        txt = subprocess.run(["tesseract", f"{td}/h.png", "-", "-l", "chi_tra+eng", "--psm", "6"], capture_output=True, text=True).stdout
    return txt


def clean_title(txt, n):
    for line in txt.splitlines():
        if "LESSON" in line.upper() or "課" in line:
            t = re.sub(r'^.*?(LESSON|Lesson)\s*[•·.\-]*\s*[\dflIJ| ]{1,3}\s*[•·.\-]*\s*', '', line)
            t = re.sub(r'^.*?第\s*\S{1,3}\s*課', '', t)
            t = re.sub(r'[\s•·]+', '', t)
            t = re.sub(r'[A-Za-z]{1,2}$', '', t)
            if len(t) >= 2:
                return t
    return None


def detect_lessons(texts, book, expected_n=None):
    n_pages = len(texts)
    header, opener, marker = {}, {}, {}
    for i, t in enumerate(texts, start=1):
        for m in re.finditer(r'LESSON\s*[•·.]?\s*([\dflIJ|](?:\s?[\dflIJ|O])?)\s*[•·.]', t):
            k = m.group(1).replace(" ", "").translate(OCR_DIGIT)
            if k.isdigit() and 1 <= int(k) <= 15:
                header.setdefault(int(k), i)
        for m in re.finditer(r'第\s*([一二三四五六七八九十]{1,3}|\d{1,2})\s*課', t):
            k = cn_to_int(m.group(1))
            if 1 <= k <= 15 and i > 8:
                opener.setdefault(k, i)
        for m in re.finditer(r'(?<![\d-])(\d{2})\s*-\s*0?1(?![\d])', t):
            k = int(m.group(1))
            if 1 <= k <= 15 and i > 8:
                marker.setdefault(k, i)
    # plausible lesson count: largest k seen in headers that also has a neighbour
    ks = sorted(set(header) | set(opener))
    max_k = expected_n or max([k for k in ks if (k - 1 in ks or k + 1 in ks)] or [0])
    starts = {}
    for k in range(1, max_k + 1):
        cands = [p for p in (opener.get(k), header.get(k), marker.get(k)) if p]
        if cands:
            starts[k] = min(cands)
    # enforce monotonic order; drop outliers
    lessons, last = [], 0
    for k in range(1, max_k + 1):
        p = starts.get(k)
        if p and p > last:
            lessons.append([k, p]); last = p
    # the opener page usually sits 1–4 pages before the header; if only a header was found, back up to the
    # previous page that has no text belonging to the earlier lesson (simple heuristic: keep header page)
    appendix = None
    for i in range(last + 1, n_pages + 1):
        t = texts[i - 1]
        if re.search(r'(Appendix|附錄|Index|索引|Vocabulary Index|生詞索引|Pinyin Index)', t):
            appendix = i; break
    out = []
    for j, (k, p) in enumerate(lessons):
        end = lessons[j + 1][1] - 1 if j + 1 < len(lessons) else (appendix - 1 if appendix else n_pages)
        out.append(dict(n=k, start=p, end=end, headerPage=header.get(k), detection={
            "header": header.get(k), "opener": opener.get(k), "audioMarker": marker.get(k)}))
    missing = [k for k in range(1, max_k + 1) if k not in [l["n"] for l in out]]
    return out, appendix, missing


def link_audio(texts, lessons, files):
    """Assign each audio file to a lesson (by its number prefix) and to the page where its marker is printed."""
    tracks = []
    for f in files:
        name = f["name"]
        m = re.match(r'^(\d{2})(?:-(\d{1,2}))?', name)
        if not m:
            tracks.append(dict(file=name, lesson=None)); continue
        a = int(m.group(1)); b = m.group(2)
        if b is None:
            # C1 workbook style "01.mp3" = lesson 1; "00.mp3" = introduction
            tracks.append(dict(file=name, lesson=a or None, label=name.rsplit(".", 1)[0])); continue
        lesson = next((l for l in lessons if l["n"] == a), None)
        page = None
        if lesson:
            pat = re.compile(rf'(?<![\d-]){a:02d}\s*-\s*0?{int(b)}(?!\d)')
            for p in range(lesson["start"], lesson["end"] + 1):
                if pat.search(texts[p - 1]):
                    page = p; break
        tracks.append(dict(file=name, lesson=a, label=f"{a:02d}-{int(b):02d}" + (" (alt)" if "(" in name else ""), page=page))
    return tracks


def main(src, out):
    src, out = Path(src), Path(out)
    listing = json.loads((Path(__file__).parent / "study_audio_listing.json").read_text(encoding="utf-8"))
    sdir = out / "public" / "content" / "study"
    (sdir / "lessons").mkdir(parents=True, exist_ok=True)
    index = dict(levels=[])
    report = []
    for lv in LEVELS:
        lvl = dict(id=lv["id"], label=lv["label"], vol=lv["vol"], books=[])
        for b in [b for b in BOOKS if b["level"] == lv["id"]]:
            pdf = src / "TOCFL Study" / b["folder"] / b["file"]
            texts = page_texts(pdf)
            if texts and not texts[-1].strip():
                texts = texts[:-1]
            tb_audio = listing.get(next(x for x in BOOKS if x["level"] == lv["id"] and x["kind"] == "textbook")["audioDir"], [])
            expected_n = max((int(f["name"][:2]) for f in tb_audio if f["name"][:2].isdigit()), default=None)
            lessons, appendix, missing = detect_lessons(texts, b, expected_n)
            ovs = BOUNDARY_OVERRIDES.get(b["id"], {})
            have = {l["n"]: l for l in lessons}
            for n, ov in ovs.items():
                if n not in have:
                    have[n] = dict(n=n, start=ov, end=None, headerPage=None, detection={})
                have[n]["start"] = ov; have[n]["detection"]["override"] = ov
            last_end = lessons[-1]["end"] if lessons else len(texts)
            lessons = sorted(have.values(), key=lambda l: l["n"])
            lessons[-1]["end"] = max(last_end, lessons[-1]["start"])
            missing = [k for k in missing if k not in ovs]
            for j in range(len(lessons) - 1):
                lessons[j]["end"] = lessons[j + 1]["start"] - 1
            for l in lessons:
                vt = TITLES.get(lv["id"], [])
                if l["n"] <= len(vt):
                    l["titleOcr"] = vt[l["n"] - 1]; l["titleVerified"] = True
                else:
                    hp = l.get("headerPage") or l["start"]
                    l["titleOcr"] = clean_title(ocr_header(pdf, hp), l["n"]); l["titleVerified"] = False
                l["id"] = f"{b['id']}-l{l['n']:02d}"
                mig = sdir / "lessons" / f"{l['id']}.json"
                l["migrated"] = mig.exists()
            files = listing.get(b["audioDir"], []) if b["audioDir"] else []
            tracks = link_audio(texts, lessons, files)
            for l in lessons:
                l["tracks"] = [t for t in tracks if t.get("lesson") == l["n"]]
            extra = [t for t in tracks if not t.get("lesson") or t["lesson"] not in [l["n"] for l in lessons]]
            book = dict(id=b["id"], level=lv["id"], kind=b["kind"], label=b["label"], pages=len(texts),
                        source=dict(folder=b["folder"], file=b["file"], audioDir=b["audioDir"]),
                        frontMatter=dict(start=1, end=(lessons[0]["start"] - 1) if lessons else len(texts)),
                        backMatter=dict(start=appendix or (lessons[-1]["end"] + 1 if lessons else None), end=len(texts)) if lessons and (lessons[-1]["end"] < len(texts)) else None,
                        lessons=lessons, otherTracks=extra, audioFiles=len(files))
            (sdir / f"{b['id']}.json").write_text(json.dumps(book, ensure_ascii=False, indent=1), encoding="utf-8")
            lvl["books"].append(dict(id=b["id"], kind=b["kind"], label=b["label"], pages=len(texts),
                                     lessons=[dict(id=l["id"], n=l["n"], title=l["titleOcr"], migrated=l["migrated"]) for l in lessons]))
            report.append(dict(book=b["id"], pages=len(texts), lessons=len(lessons), missingLessons=missing,
                               tracks=len(files), tracksOnPage=sum(1 for t in tracks if t.get("page")),
                               tracksUnassigned=len(extra)))
            print(b["id"], "pages", len(texts), "lessons", [(l["n"], l["start"], l["end"], l["titleOcr"]) for l in lessons], "missing", missing)
        index["levels"].append(lvl)
    (sdir / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8")
    (out / "reports").mkdir(exist_ok=True)
    (out / "reports" / "study_structure.json").write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
