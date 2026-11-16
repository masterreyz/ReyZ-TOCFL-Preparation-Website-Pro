"""Import the per-question bank ("TOCFL Exercise/* Per Part") into practice sets.

Usage: python parse_partbank.py <SOURCE_ROOT> <OUT_ROOT> [set_size]
For every "*_Answer.xlsx" (columns: 題型 | 檔案名稱 | 答案) the matching item PDF (<id>.pdf, not in a
"Listening Script" folder), listening script (<...Listening Script>/<id>.pdf) and audio (<id>.mp3) are
looked up anywhere below that part folder. Items are grouped into sets of `set_size` questions and written
in the same format as the mock tests (content/exercise/pb-*.json) and appended to the index.
Items whose answer or PDF cannot be found are recorded in reports/partbank_validation.json and the
answer is marked ungradable instead of guessed. Run finalize.py afterwards.
"""
import json
import re
import sys
from pathlib import Path

import openpyxl

from parse_mock import parse_booklet, parse_script

BAND = {"1": "novice", "2": "a", "3": "b", "4": "c"}


def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')[:40]


def main(src, out, set_size=25):
    src, out = Path(src), Path(out)
    cdir = out / "content" / "exercise"
    index = [x for x in json.loads((cdir / "index.json").read_text(encoding="utf-8")) if not x["id"].startswith("pb-")]
    issues = []
    for xlsx in sorted((src / "TOCFL Exercise").glob("* Per Part/*/*_Answer.xlsx")):
        part_dir = xlsx.parent
        band = BAND[part_dir.parent.name[0]]
        skill = "listening" if "_L_" in xlsx.name or "Listening" in part_dir.name else "reading"
        rows = [r for r in openpyxl.load_workbook(xlsx, read_only=True).active.iter_rows(min_row=2, values_only=True) if r and r[1]]
        pdfs = {p.stem: p for p in part_dir.rglob("*.pdf") if "Script" not in str(p.parent) and "Instruction" not in str(p)}
        scripts = {p.stem: p for p in part_dir.rglob("*.pdf") if "Script" in str(p.parent)}
        mp3s = {p.stem: p for p in part_dir.rglob("*.mp3")}
        kind = slug(xlsx.stem.replace("_Answer", ""))
        for k in range(0, len(rows), set_size):
            chunk = rows[k:k + set_size]
            tid = f"pb-{band}-{kind}-{k // set_size + 1}"
            media = out / "media" / "ex" / tid
            qs, tracks = [], []
            for row in chunk:
                item, ans = str(row[1]).strip(), str(row[2] or "").strip().upper()
                answers = re.findall(r'[A-F]', ans)
                pdf = pdfs.get(item)
                if not pdf:
                    issues.append(dict(set=tid, item=item, kind="item_pdf_missing")); continue
                local = []
                try:
                    q, _ = parse_booklet(pdf, max(1, len(answers)), media / item, tid, local)
                except Exception as e:  # keep going; record
                    issues.append(dict(set=tid, item=item, kind="parse_error", detail=str(e))); continue
                scr = parse_script(scripts[item], max(1, len(q)), tid, local) if item in scripts else {}
                scr.pop("_parts", None)
                for j, n in enumerate(sorted(q)):
                    x = q[n]
                    x["n"] = len(qs) + 1
                    x["crop"] = f"{item}/{x['crop']}" if x.get("crop") else None
                    x["answer"] = answers[j] if j < len(answers) else None
                    x["gradable"] = x["answer"] is not None
                    x["item"] = item
                    x["part"] = 0
                    if scr.get(n):
                        x["transcript"] = scr[n]["transcript"]
                        if scr[n].get("intro"):
                            x["transcriptIntro"] = scr[n]["intro"]
                    if not x["options"] and skill == "listening":
                        x["spokenOptions"] = True; x["showCrop"] = True
                    if item in mp3s:
                        rel = mp3s[item].relative_to(src / "TOCFL Exercise")
                        tracks.append(str(rel).replace("\\", "/"))
                        x["_track"] = len(tracks) - 1
                    qs.append(x)
                if not answers:
                    issues.append(dict(set=tid, item=item, kind="answer_missing"))
                issues += [dict(set=tid, item=item, **i) for i in local if i["kind"] != "no_parts_detected"]
            if not qs:
                continue
            title = f"Bank Soal {BAND[part_dir.parent.name[0]].upper() if band != 'novice' else 'Novice'} · {part_dir.name} · Set {k // set_size + 1}"
            audio = None
            if tracks:
                audio = dict(dir="", kind="by-filename", tracks=tracks)
            data = dict(id=tid, band=band, skill=skill, series=f"P{k // set_size + 1}", title=title, kind="partbank",
                        source=dict(folder=str(part_dir.relative_to(src / "TOCFL Exercise")), booklet="(per item)", answer=xlsx.name),
                        parts=[dict(title=part_dir.name, subtitle="", instructions="", instructionsEn="", **{"from": 1, "to": len(qs)})],
                        questions=qs, audio=audio, optionCount=max([len(x["options"]) for x in qs] + [3]))
            (cdir / f"{tid}.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
            index.append(dict(id=tid, band=band, skill=skill, series=data["series"], title=title, kind="partbank",
                              questions=len(qs), gradable=sum(1 for x in qs if x["gradable"])))
            print(tid, len(qs), "questions")
    (cdir / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8")
    (out / "reports").mkdir(exist_ok=True)
    (out / "reports" / "partbank_validation.json").write_text(json.dumps(issues, ensure_ascii=False, indent=1), encoding="utf-8")
    print("issues:", len(issues))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 25)
