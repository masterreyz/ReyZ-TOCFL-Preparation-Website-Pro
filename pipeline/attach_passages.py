"""Attach reading passages printed on a page of their own to the questions that follow them.

parse_mock.py reads a passage as the text above a question number on the same page. In the
Band B and C booklets a long passage often fills a page by itself and its questions start on the
next page; those passages were lost and the questions were grouped with the previous passage.
This step finds such passage-only pages, stores the passage as the `context` of the first
question on the next page, regroups the questions that belong to it, and saves the printed
passage as P<n>.webp for the "original question book layout" view.

Run after parse_mock.py and fix_text.py, before build_layouts.py:
    python attach_passages.py <SOURCE_ROOT> <OUT_DIR>
"""
import json
import re
import sys
import tempfile
from pathlib import Path

from PIL import Image

import parse_mock as pm
from mock_catalog import CATALOG
from pdfutil import pages_lines, render_page
from build_layouts import squeeze

PASSAGE_HEAD = re.compile(r'^[（(][一二三四五六七八九十]+[）)]')


def passage_pages(pages, data):
    qpages = {q["page"] for q in data["questions"]} | {q.get("optionsPage") for q in data["questions"]}
    first = min(q["page"] for q in data["questions"])
    out = []
    for pi, p in enumerate(pages):
        if pi + 1 < first or pi + 1 in qpages:
            continue
        rows = [r for r in pm.rows_of(p) if not pm.is_header(r["text"]) and not re.fullmatch(r'[\d\-– ]+', r["text"])]
        txt = "".join(r["text"] for r in rows)
        if not rows or not PASSAGE_HEAD.match(rows[0]["text"]) or "說明：" in txt or "說明:" in txt:
            continue
        # a passage printed as a picture (notice, table, ad): only its number is in the text layer
        out.append((pi, rows, len(txt) < 40))
    return out


def build(src_root, out_root):
    src_root, out_root = Path(src_root), Path(out_root)
    for t in CATALOG:
        if t["skill"] != "reading":
            continue
        pdf = src_root / "TOCFL Exercise" / t["folder"] / t["booklet"]
        jf = out_root / "content" / "exercise" / f"{t['id']}.json"
        data = json.loads(jf.read_text(encoding="utf-8"))
        pages = pages_lines(pdf)
        found = passage_pages(pages, data)
        if not found:
            continue
        qs = data["questions"]
        starts = {}
        with tempfile.TemporaryDirectory() as tmp:
            for pi, rows, pictured in found:
                nxt = sorted((q for q in qs if q["page"] > pi + 1), key=lambda q: q["n"])
                if not nxt:
                    continue
                lead = nxt[0]
                lead["context"] = pm.join_rows(rows)
                png = Path(tmp) / f"p{pi + 1}.png"
                render_page(pdf, pi + 1, png, dpi=150)
                im = Image.open(png).convert("RGB")
                sc = im.width / pages[pi]["w"]
                top, bottom = rows[0]["y0"] - 8, (pages[pi]["h"] - 50) if pictured else rows[-1]["y1"] + 8
                crop = im.crop((int(30 * sc), int(top * sc), int((pages[pi]["w"] - 30) * sc), int(bottom * sc)))
                name = f"P{lead['n']}.webp"
                squeeze(crop).save(out_root / "media" / "ex" / t["id"] / name, "WEBP", quality=74)
                lead["passageImage"] = name
                lead["passagePage"] = pi + 1
                starts[lead["n"]] = lead
        # regroup: questions after an attached passage (same part, up to the next passage) belong to it
        lead = None
        for q in qs:
            if q.get("context"):
                lead = q if q["n"] in starts else None
            if q["n"] in starts:
                q["group"] = f"g{q['n']}"
            elif lead is not None and q.get("part") == lead.get("part"):
                q["group"] = f"g{lead['n']}"
        jf.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
        print(t["id"], "passages attached to questions", sorted(starts))


if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2])
