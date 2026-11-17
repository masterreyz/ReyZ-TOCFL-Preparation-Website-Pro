"""Build "original question book layout" images for every reading question.

Each image shows the passage and the question exactly as printed in the booklet,
with the answer choices removed (choices are offered separately as answer buttons).

Usage: python build_layouts.py <SOURCE_ROOT> <OUT_DIR>
Writes OUT_DIR/media/ex/<testId>/L<n>.webp (question), P<n>.webp (passage of a group lead)
and adds `layout: [image, ...]` to every reading question in OUT_DIR/content/exercise/<testId>.json.
"""
import json
import re
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw

import parse_mock as pm
from mock_catalog import CATALOG
from pdfutil import render_page

OPT_LINE_RE = re.compile(r'^\s*[(（]\s*[A-F]\s*[)）]')
NUM_ONLY_RE = re.compile(r'^\s*\d{1,2}\s*[.．]?\s*$')
DPI = 150

_last_opts = []
_calls = []


def _parse_options(rows):
    global _last_opts
    _last_opts = list(rows)
    return _orig_parse_options(rows)


def _save_crop(pdf, pages, rendered, media_dir, pi, top, bottom, name):
    _calls.append(dict(pi=pi, top=top, bottom=bottom, name=name, opts=_last_opts))
    return _orig_save_crop(pdf, pages, rendered, media_dir, pi, top, bottom, name)


_orig_parse_options, _orig_save_crop = pm.parse_options, pm.save_crop
pm.parse_options, pm.save_crop = _parse_options, _save_crop


def squeeze(im, max_gap=34, min_run=46):
    """Collapse tall blank bands (left by removed choices) and trim margins."""
    g = im.convert("L")
    w, h = g.size
    px = g.load()
    blank = [all(px[x, y] > 235 for x in range(0, w, 3)) for y in range(h)]
    keep, y = [], 0
    while y < h:
        if blank[y]:
            s = y
            while y < h and blank[y]:
                y += 1
            run = y - s
            keep.extend(range(s, s + (min(run, max_gap) if run >= min_run else run)))
        else:
            keep.append(y)
            y += 1
    while keep and blank[keep[-1]]:
        keep.pop()
    while keep and blank[keep[0]]:
        keep.pop(0)
    out = Image.new("RGB", (w, len(keep) + 24), "white")
    for i, yy in enumerate(keep):
        out.paste(im.crop((0, yy, w, yy + 1)), (0, i + 12))
    return out


def region_image(page_img, page, top, bottom, mask_rects, cut_at=None):
    sc = page_img.width / page["w"]
    bot = min(bottom, page["h"]) if cut_at is None else min(bottom, cut_at)
    box = (int(30 * sc), int(max(0, top) * sc), int((page["w"] - 30) * sc), int(bot * sc))
    if box[3] - box[1] < 12:
        return None
    im = page_img.crop(box).copy()
    d = ImageDraw.Draw(im)
    for x0, y0, x1, y1 in mask_rects:
        d.rectangle((int((x0 - 30) * sc) - 3, int((y0 - top) * sc) - 3, int((x1 - 30) * sc) + 3, int((y1 - top) * sc) + 3), fill="white")
    return squeeze(im)


def option_lines(page, top, bottom, recorded, bare_numbers=True, annotated=False):
    """All printed lines in [top,bottom] that belong to answer choices."""
    lines = [l for l in page["lines"] if l["y0"] >= top - 1 and l["y1"] <= bottom + 1]
    lines.sort(key=lambda l: (l["y0"], l["x0"]))
    rec_y = {round(it["y0"]) for r in recorded for it in r.get("items", [])}
    opt = []
    for l in lines:
        if OPT_LINE_RE.match(l["text"]) or pm.OPT_SPLIT_RE.search(l["text"]) or round(l["y0"]) in rec_y and opt:
            opt.append(l)
    # wrapped continuation lines of a choice
    for l in lines:
        if l in opt:
            continue
        for o in opt:
            if 0 <= l["y0"] - o["y1"] < 10 and l["x0"] >= o["x0"] + 8 and l["x0"] < o["x1"] + 40:
                opt.append(l)
                break
    # printed pinyin / zhuyin annotations belonging to a choice (Novice booklets)
    for l in lines:
        if l in opt or (re.search(r'[\u4e00-\u9fff]', l["text"]) and not annotated):
            continue
        if any(-6 <= o["y0"] - l["y1"] < 14 and l["x0"] < o["x1"] and l["x1"] > o["x0"] for o in opt):
            opt.append(l)
    # bare question numbers sitting right above choices ("1.   2." rows in fill-in-the-blank groups)
    for l in (lines if bare_numbers else []):
        if NUM_ONLY_RE.match(l["text"]) and any(0 <= o["y0"] - l["y1"] < 26 for o in opt):
            opt.append(l)
    return opt


def build(src_root, out_root):
    src_root, out_root = Path(src_root), Path(out_root)
    for t in CATALOG:
        if t["skill"] != "reading":
            continue
        base = src_root / "TOCFL Exercise" / t["folder"]
        pdf = base / t["booklet"]
        jf = out_root / "content" / "exercise" / f"{t['id']}.json"
        data = json.loads(jf.read_text(encoding="utf-8"))
        media = out_root / "media" / "ex" / t["id"]
        _calls.clear()
        with tempfile.TemporaryDirectory() as tmp:
            pm.parse_booklet(pdf, t["questions"], Path(tmp) / "m", t["id"], [])
            pages = pm.pages_lines(pdf)
            imgs = {}

            def page_img(pi):
                if pi not in imgs:
                    png = Path(tmp) / f"p{pi + 1}.png"
                    render_page(pdf, pi + 1, png, dpi=DPI)
                    imgs[pi] = Image.open(png).convert("RGB")
                return imgs[pi]

            calls = {c["name"]: c for c in _calls if not c["name"].endswith("o.webp")}
            # a question's region ends where the next question's region (often its own passage) begins
            for c in calls.values():
                nxt = [d["top"] for d in calls.values() if d["pi"] == c["pi"] and d["top"] > c["top"] + 10]
                if nxt:
                    c["bottom"] = min(c["bottom"], min(nxt) + 6)
            qs = {q["n"]: q for q in data["questions"]}
            made = {}
            for q in data["questions"]:
                c = calls.get(q.get("crop") or "")
                if not c:
                    continue
                page = pages[c["pi"]]
                opts = option_lines(page, c["top"], c["bottom"], c["opts"], bare_numbers=not q.get("stem"), annotated=t["band"] == "novice")
                pictures = q["options"] and not all(o.get("text") for o in q["options"])
                if pictures and opts:
                    # picture choices: keep only what is printed above the first choice label
                    first = min(l["y0"] for l in opts if OPT_LINE_RE.match(l["text"]) or pm.OPT_SPLIT_RE.search(l["text"]))
                    im = region_image(page_img(c["pi"]), page, c["top"], c["bottom"], [], cut_at=first - 2)
                else:
                    im = region_image(page_img(c["pi"]), page, c["top"], c["bottom"], [(l["x0"], l["y0"], l["x1"], l["y1"]) for l in opts])
                if im is None or im.height <= 30:  # nothing left once the choices are removed
                    continue
                name = f"L{q['n']}.webp"
                im.save(media / name, "WEBP", quality=74)
                made[q["n"]] = name
                # passage-only image of a group lead (shown before the questions that follow it)
                if q.get("context") and q.get("group"):
                    anchor = next((l for l in page["lines"] if c["top"] <= l["y0"] <= c["bottom"]
                                   and re.match(rf'^{q["n"]}\s*[.．、]', l["text"])), None)
                    if anchor:
                        pim = region_image(page_img(c["pi"]), page, c["top"], c["bottom"], [], cut_at=anchor["y0"] - 3)
                        if pim is not None:
                            pim.save(media / f"P{q['n']}.webp", "WEBP", quality=74)
                            q["_passage"] = f"P{q['n']}.webp"
            for q in data["questions"]:
                lead_n = q.get("groupLead") if q.get("cloze") else (int(q["group"][1:]) if q.get("group") else None)
                lead = qs.get(lead_n) if lead_n and lead_n != q["n"] else None
                own = made.get(q["n"])
                if lead and own and q.get("cloze"):
                    lay = [own]
                elif lead and own:
                    lay = [lead.get("_passage") or made.get(lead["n"]), own]
                elif lead:
                    lay = [made.get(lead["n"])]
                else:
                    lay = [own]
                q["layout"] = [x for x in lay if x]
            for q in data["questions"]:
                q.pop("_passage", None)
            missing = [q["n"] for q in data["questions"] if not q["layout"]]
            print(t["id"], "layout images:", len(made), "missing:", missing)
        jf.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2])
