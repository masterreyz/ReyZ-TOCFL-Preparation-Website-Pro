"""Import every question of the official per-part question bank ("TOCFL Exercise/<band> Per Part").

Usage: python build_partbank.py <SOURCE_ROOT> <OUT_ROOT> [questions_per_set]

Each part folder holds one PDF per item (<id>.pdf, in "<..>_T" or directly in the folder), an optional
listening script (<..>_Listening Script/<id>.pdf) and an answer key "<..>_Answer.xlsx" with columns
題型 | 檔案名稱 | 答案. An item with several questions lists its answers on the rows below it
(file name empty). Every item page is shown as the printed image (several items are scanned, so the
image is the only faithful form), cropped to its content; answer buttons follow the key. Printed text
is kept where the PDF has a text layer (choices, listening scripts for speech synthesis, search).

Output: content/exercise/pb-<section>-<k>.json (sets of whole items) and media/ex/pb-<section>-<k>/,
plus content/exercise/partbank.json (section -> sets) and reports/partbank_validation.json.
Items whose PDF or answer cannot be found are reported, never guessed.
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import openpyxl
from PIL import Image, ImageOps

from parse_mock import OPT_SPLIT_RE, parse_options

# part folder -> (section id in sections.json, default number of choices)
PARTS = {
    ("1", "Part 1. Listening"): ("n-l1", 3), ("1", "Part 2. Listening"): ("n-l2", 3), ("1", "Part 3. Listening"): ("n-l3", 3),
    ("1", "Part 4. Reading"): ("n-r1", 3), ("1", "Part 5. Reading"): ("n-r2", 3),
    ("2", "Band A Listening Picture Description"): ("a-l-pic", 3),
    ("2", "Band A Listening AnA Understanding"): ("a-l-single", 3),
    ("2", "Band A Listening Dialogue Comprehension"): ("a-l-multi", 3),
    ("2", "Band A Listening Dialogue"): ("a-l-dialogue", 4),
    ("2", "Reading TOCFL A  Single sentence comprehension"): ("a-r-sentence", 3),
    ("2", "Reading TOCFL A Interpretation of the image"): ("a-r-pic", 3),
    ("2", "Reading TOCFL A Fill in the blanks"): ("a-r-gap", 3),
    ("2", "Reading TOCFL A Complete Paragraph"): ("a-r-paragraph", 6),
    ("2", "Reading TOCFL A Reading Comprehension"): ("a-r-comp", 4),
    ("3", "Listening Dialogue Band B"): ("b-l-dialogue", 4), ("3", "Listening Paragraph Band B"): ("b-l-monologue", 4),
    ("3", "Fill in the blanks with the correct words"): ("b-r-gap", 4), ("3", "Reading comprehension"): ("b-r-comp", 4),
    ("4", "Listening Dialogue Band C"): ("c-l-dialogue", 4), ("4", "Listening Paragraph Band C"): ("c-l-monologue", 4),
    ("4", "Reading Fill in the blanks Band C"): ("c-r-gap", 4), ("4", "Reading Comprehension Band C"): ("c-r-comp", 4),
}
BAND = {"1": "novice", "2": "a", "3": "b", "4": "c"}
# MP3 file names (relative to "TOCFL Exercise"); the audio is not needed to build, only to link per-item tracks
MP3S = json.loads((Path(__file__).parent / "partbank_mp3_listing.json").read_text(encoding="utf-8"))


def read_key(xlsx):
    """[(item_id, [answers...])] in file order; answers of multi-question items are on the following rows."""
    items = []
    for row in openpyxl.load_workbook(xlsx, read_only=True).active.iter_rows(min_row=2, values_only=True):
        if not row or len(row) < 3:
            continue
        name, ans = (str(row[1]).strip() if row[1] else ""), (str(row[2]).strip().upper() if row[2] else "")
        if name:
            items.append([name, []])
        if ans and items:
            items[-1][1] += re.findall(r'[A-F]', ans)
    return items


def pdf_text(pdf):
    return subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True, text=True).stdout


def render_item(pdf, out_png_dir):
    """Render all pages, crop each to its printed content, stack them; return a PIL image."""
    subprocess.run(["pdftoppm", "-r", "110", "-png", str(pdf), str(out_png_dir / "p")], check=True)
    pages = []
    for png in sorted(out_png_dir.glob("p*.png")):
        im = Image.open(png).convert("RGB")
        g = ImageOps.grayscale(im).point(lambda v: 255 if v > 200 else 0)  # drop pale watermarks
        box = ImageOps.invert(g).getbbox()
        if box:
            pad = 14
            box = (max(0, box[0] - pad), max(0, box[1] - pad), min(im.width, box[2] + pad), min(im.height, box[3] + pad))
            pages.append(im.crop(box))
        png.unlink()
    if not pages:
        return None
    w = max(p.width for p in pages)
    out = Image.new("RGB", (w, sum(p.height for p in pages) + 16 * (len(pages) - 1)), "white")
    y = 0
    for p in pages:
        out.paste(p, (0, y))
        y += p.height + 16
    return out


SPEAKER = re.compile(r'^(男|女|提問|問題)\s+')


def script_text(pdf):
    """Listening script as plain lines (speaker labels kept as 男：/女：/提問：)."""
    lines = []
    for raw in pdf_text(pdf).splitlines():
        t = raw.strip()
        if not t:
            continue
        t = re.sub(r'^\d{1,2}\s*[.．、]?\s*', '', t) if re.match(r'^\d{1,2}\s*[.．、]?\s*\S', t) and len(lines) == 0 else t
        if re.fullmatch(r'\d{1,2}\s*[.．、]?', t):
            continue
        t = SPEAKER.sub(lambda m: m.group(1) + '：', t)
        t = re.sub(r'\s{2,}', ' ', t)
        lines.append(t)
    return "\n".join(lines)


def item_choices(text):
    """Choices printed with text: {label: text}, only when every label has text."""
    rows = [dict(text=l.strip()) for l in text.splitlines() if l.strip()]
    rows = [r for r in rows if OPT_SPLIT_RE.search(r["text"].replace('（', '(').replace('）', ')'))]
    for r in rows:
        r["text"] = r["text"].replace('（', '(').replace('）', ')')
    opts = parse_options(rows)
    return {o["label"]: o["text"] for o in opts if o["text"]}


def build(src, out, per_set=20):
    src, out = Path(src), Path(out)
    cdir, mroot = out / "content" / "exercise", out / "media" / "ex"
    for old in cdir.glob("pb-*.json"):
        old.unlink()
    for old in mroot.glob("pb-*"):
        shutil.rmtree(old)
    index = [x for x in json.loads((cdir / "index.json").read_text(encoding="utf-8")) if not x["id"].startswith("pb-")]
    issues, bank = [], {}
    for xlsx in sorted((src / "TOCFL Exercise").glob("* Per Part/*/*_Answer.xlsx")):
        part = xlsx.parent
        key = (part.parent.name[0], part.name)
        if key not in PARTS:
            issues.append(dict(part=part.name, kind="unknown_part_folder"))
            continue
        sec, default_n = PARTS[key]
        band = BAND[key[0]]
        skill = "listening" if "Listening" in part.name else "reading"
        pdfs = {p.stem: p for p in part.rglob("*.pdf") if "Script" not in p.parent.name}
        scripts = {p.stem: p for p in part.rglob("*.pdf") if "Script" in p.parent.name}
        prefix = str(part.relative_to(src / "TOCFL Exercise")).replace("\\", "/") + "/"
        mp3s = {Path(m).stem: m for m in MP3S if m.startswith(prefix)}
        mp3s.update({p.stem: str(p.relative_to(src / "TOCFL Exercise")).replace("\\", "/") for p in part.rglob("*.mp3")})
        items = read_key(xlsx)
        built = []  # (item_id, [question dicts])
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            for item, answers in items:
                pdf = pdfs.get(item)
                if not pdf:
                    issues.append(dict(part=part.name, item=item, kind="item_pdf_missing"))
                    continue
                if not answers:
                    issues.append(dict(part=part.name, item=item, kind="answer_missing"))
                img = render_item(pdf, tmp)
                if img is None:
                    issues.append(dict(part=part.name, item=item, kind="empty_pdf"))
                    continue
                txt = pdf_text(pdf)
                choices = item_choices(txt) if len(answers) <= 1 else {}
                n_opts = max([default_n, len(choices)] + ["ABCDEF".index(a) + 1 for a in answers])
                transcript = script_text(scripts[item]) if item in scripts else ""
                if skill == "listening" and not transcript:
                    issues.append(dict(part=part.name, item=item, kind="listening_script_missing"))
                qs = []
                for j, ans in enumerate(answers or [None]):
                    q = dict(item=item, sub=j + 1, subCount=max(1, len(answers)), answer=ans, gradable=ans is not None,
                             stem="", context="", part=0, showCrop=True,
                             options=[dict(label=L, text=choices.get(L, "")) for L in "ABCDEF"[:n_opts]])
                    if j == 0:
                        q["_img"] = img
                        if transcript:
                            q["transcript"] = transcript
                        if txt.strip():
                            q["printedText"] = re.sub(r'[ \t]{2,}', ' ', txt.strip())
                    if skill == "listening" and transcript and j == 0:
                        q["spokenOptions"] = not choices
                    qs.append(q)
                built.append((item, qs))
        # sets of whole items, about per_set questions each
        sets, cur = [], []
        for item, qs in built:
            if cur and sum(len(x[1]) for x in cur) + len(qs) > per_set:
                sets.append(cur)
                cur = []
            cur.append((item, qs))
        if cur:
            sets.append(cur)
        bank[sec] = dict(section=sec, band=band, skill=skill, folder=str(part.relative_to(src / "TOCFL Exercise")),
                         items=len(built), questions=sum(len(q) for _, q in built), sets=[])
        for k, chunk in enumerate(sets, 1):
            tid = f"pb-{sec}-{k}"
            media = mroot / tid
            media.mkdir(parents=True, exist_ok=True)
            questions, tracks = [], []
            for item, qs in chunk:
                lead_n = len(questions) + 1
                for q in qs:
                    q = dict(q)
                    q["n"] = len(questions) + 1
                    img = q.pop("_img", None)
                    if img is not None:
                        img.save(media / f"{item}.webp", "WEBP", quality=72)
                        q["crop"] = f"{item}.webp"
                    else:
                        q["crop"] = None
                    if q["subCount"] > 1:
                        q["group"] = f"g{lead_n}"
                    if skill == "listening" and item in mp3s:
                        if q["sub"] == 1:
                            tracks.append(mp3s[item])
                        q["_track"] = len(tracks) - 1
                    questions.append(q)
            title = f"Bank Soal {BAND[key[0]].upper() if band != 'novice' else 'Novice'} · {part.name} · Set {k}"
            data = dict(id=tid, band=band, skill=skill, series=f"Set {k}", title=title, kind="partbank", section=sec,
                        source=dict(folder=bank[sec]["folder"], booklet="(per item)", answer=xlsx.name),
                        parts=[dict(title=part.name, subtitle="", instructions="", instructionsEn="", **{"from": 1, "to": len(questions)})],
                        questions=questions, audio=dict(dir="", kind="by-filename", tracks=tracks) if tracks else None, optionCount=max(len(q["options"]) for q in questions))
            (cdir / f"{tid}.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
            first_item, last_item = chunk[0][0], chunk[-1][0]
            bank[sec]["sets"].append(dict(test=tid, set=k, questions=len(questions), items=len(chunk), first=first_item, last=last_item))
            index.append(dict(id=tid, band=band, skill=skill, series=data["series"], title=title, kind="partbank", section=sec,
                              questions=len(questions), gradable=sum(1 for x in questions if x["gradable"])))
        print(f"{sec:14s} {part.name[:45]:45s} items {len(built):4d}/{len(items):4d}  questions {bank[sec]['questions']:4d}  sets {len(sets)}")
    (cdir / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8")
    (cdir / "partbank.json").write_text(json.dumps(bank, ensure_ascii=False, indent=1), encoding="utf-8")
    (out / "reports").mkdir(exist_ok=True)
    (out / "reports" / "partbank_validation.json").write_text(json.dumps(issues, ensure_ascii=False, indent=1), encoding="utf-8")
    print("issues:", len(issues))


if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 20)
