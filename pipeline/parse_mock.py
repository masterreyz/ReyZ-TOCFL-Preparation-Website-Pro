"""Parse official TOCFL mock tests (booklet + answer key + listening script) into JSON.

Usage: python parse_mock.py <SOURCE_ROOT> <OUT_DIR>
SOURCE_ROOT = the folder that contains "TOCFL Exercise".
Outputs OUT_DIR/content/exercise/<testId>.json, OUT_DIR/public/media/ex/<testId>/q<N>.webp,
and OUT_DIR/reports/exercise_validation.json
"""
import json
import re
import sys
from pathlib import Path

from PIL import Image

from pdfutil import pages_lines, render_page, page_has_images, plain_text, is_cjk
from mock_catalog import CATALOG

PART_RE = re.compile(r'^(第[一二三四五六]部分|[一二三四五六]、\S{1,10})$')
SCRIPT_ANCHOR_RE = re.compile(r'^(\d{1,2})\s+(.+)$')
ANCHOR_RE = re.compile(r'^(\d{1,2})\s*[.．、]\s*(.*)$')
OPT_SPLIT_RE = re.compile(r'\(([A-F])\)')
SKIP_PAGE_MARKERS = ('說明：', 'Directions', '例題', '說明結束')
HEADER_RE = re.compile(r'^(第[一二三四五六七八九十]+部分|Part\s+\w+|[一二三四五六]、.{1,8}|\(第\s*\d+\s*[～~\-–]\s*\d+\s*題\)|（第\s*\d+\s*[～~\-–]\s*\d+\s*題）|\d{1,3}|- ?\d{1,3} ?-)$')


def rows_of(page):
    """Group lines into visual rows by vertical overlap; each row sorted by x."""
    rows = []
    for ln in sorted(page["lines"], key=lambda l: l["y0"]):
        cy = (ln["y0"] + ln["y1"]) / 2
        for r in rows:
            if abs(r["cy"] - cy) < 5:
                r["items"].append(ln)
                r["y0"] = min(r["y0"], ln["y0"]); r["y1"] = max(r["y1"], ln["y1"])
                break
        else:
            rows.append(dict(cy=cy, y0=ln["y0"], y1=ln["y1"], items=[ln]))
    for r in rows:
        r["items"].sort(key=lambda l: l["x0"])
        r["x0"] = r["items"][0]["x0"]
        r["text"] = join_items(r["items"])
    rows.sort(key=lambda r: r["y0"])
    return rows


def join_items(items):
    s = ""
    for it in items:
        t = it["text"]
        if s and not (is_cjk(s[-1]) and is_cjk(t[:1])):
            s += " "
        s += t
    return s.strip()


def join_rows(rows):
    """Join wrapped prose rows; CJK rows concatenate without spaces; new paragraph on indent."""
    if not rows:
        return ""
    left = min(r["x0"] for r in rows)
    out = []
    for r in rows:
        t = r["text"]
        if out and r["x0"] - left < 12 and not re.match(r'^[（(]?[一二三四五六七八九十\d]+[）)]', t):
            prev = out[-1]
            sep = "" if (is_cjk(prev[-1:]) or is_cjk(t[:1])) else " "
            out[-1] = prev + sep + t
        else:
            out.append(t)
    return "\n".join(out)


def parse_options(rows):
    """Return list of {label,text} from option rows (handles several options on one row and wrapped text)."""
    opts = []
    for r in rows:
        t = r["text"]
        parts = OPT_SPLIT_RE.split(t)
        if len(parts) > 1:
            if parts[0].strip() and opts:
                opts[-1]["text"] = (opts[-1]["text"] + parts[0].strip()).strip()
            for i in range(1, len(parts), 2):
                opts.append(dict(label=parts[i], text=parts[i + 1].strip()))
        elif opts:
            opts[-1]["text"] = (opts[-1]["text"] + t).strip()
    return opts


def is_header(t):
    return bool(HEADER_RE.match(t.strip())) or t.strip() in ('Part One', 'Part Two', 'Part Three', 'Part Four', 'Part Five')


def parse_booklet(pdf, n_questions, media_dir, test_id, issues):
    pages = pages_lines(pdf)
    imgs = page_has_images(pdf)
    page_rows = [rows_of(p) for p in pages]
    parts, groups = [], []  # groups: dict(page, ri, anchors=[(n, x0)])
    preview_ns = set()  # questions whose number line carried the stem (options may follow later)
    expected = 1
    for pi, rows in enumerate(page_rows):
        txt = " ".join(r["text"] for r in rows)
        hdr = next((r["text"] for r in rows if PART_RE.match(r["text"])), None)
        if hdr and any(m in txt for m in ('說明：', 'Directions')):
            ins, en, on = [], [], False
            for r in rows:
                t = r["text"]
                if t.startswith('說明'):
                    on = True
                if t.startswith(('例題', '請看下面', 'Example')) or '例題如下' in t:
                    break
                if on:
                    (en if re.match(r'^[A-Za-z]', t) else ins).append(r)
            sub = next((r["text"] for r in rows if r["text"].startswith('Part ')), "")
            parts.append(dict(title=hdr, subtitle=sub, instructions=join_rows(ins),
                              instructionsEn=" ".join(r["text"] for r in en), page=pi + 1))
        if any(m in txt for m in SKIP_PAGE_MARKERS):
            continue
        pw = pages[pi]["w"]
        for ri, r in enumerate(rows):
            anc = []
            for it in r["items"]:
                m = ANCHOR_RE.match(it["text"])
                if m and not m.group(2).strip() and int(m.group(1)) < expected and int(m.group(1)) in preview_ns and it["x0"] < pw * 0.6:
                    groups.append(dict(page=pi, ri=ri, anchors=[(int(m.group(1)), it["x0"], "")], reanchor=True))
                    preview_ns.discard(int(m.group(1)))
                    continue
                if m and int(m.group(1)) == expected and (anc or it["x0"] < pw * 0.32):
                    anc.append((expected, it["x0"], m.group(2).strip()))
                    if m.group(2).strip() and not OPT_SPLIT_RE.search(m.group(2)):
                        preview_ns.add(expected)
                    expected += 1
                    # same line may hold a second anchor e.g. "1. 2."
                    rest = m.group(2).strip()
                    m2 = re.match(r'^(\d{1,2})\s*[.．]\s*$', rest)
                    if m2 and int(m2.group(1)) == expected:
                        anc[-1] = (anc[-1][0], anc[-1][1], "")
                        anc.append((expected, it["x0"] + 120, ""))
                        expected += 1
            if anc:
                groups.append(dict(page=pi, ri=ri, anchors=anc))
                if parts:
                    parts[-1].setdefault("from", anc[0][0]); parts[-1]["to"] = anc[-1][0]
            else:
                # cloze blanks like （41） inside a passage
                for mm in re.finditer(r'[（(]\s*(\d{2})\s*[）)]', r["text"]):
                    if int(mm.group(1)) == expected:
                        groups.append(dict(page=pi, ri=ri, anchors=[(expected, None, "")], cloze=True))
                        if parts:
                            parts[-1].setdefault("from", expected); parts[-1]["to"] = expected
                        expected += 1
    media_dir.mkdir(parents=True, exist_ok=True)
    rendered = {}
    questions = {}
    prev_end = {}
    cloze_buf = []
    for gi, g in enumerate(groups):
        pi, ri = g["page"], g["ri"]
        rows = page_rows[pi]
        nxt = groups[gi + 1] if gi + 1 < len(groups) else None
        if g.get("cloze"):
            cloze_buf.append(g)
            if nxt and nxt.get("cloze") and nxt["page"] == pi:
                continue
            # passage = rows from first cloze row's paragraph start .. rows before options; options = (A)..(F) rows after
            first = cloze_buf[0]["ri"]
            start = prev_end.get(pi, 0)
            body = [r for r in rows[start:] if not is_header(r["text"])]
            ptxt_rows = [r for r in body if not OPT_SPLIT_RE.match(r["text"]) and rows.index(r) <= cloze_buf[-1]["ri"] + 3 and not OPT_SPLIT_RE.search(r["text"])]
            opt_rows = [r for r in body if OPT_SPLIT_RE.match(r["text"])]
            options = parse_options(opt_rows)
            passage = join_rows(ptxt_rows)
            top = (ptxt_rows[0]["y0"] if ptxt_rows else rows[first]["y0"]) - 8
            bottom = (opt_rows[-1]["y1"] + 8) if opt_rows else pages[pi]["h"] - 50
            crop = save_crop(pdf, pages, rendered, media_dir, pi, top, bottom, f"q{cloze_buf[0]['anchors'][0][0]}.webp")
            for k, cg in enumerate(cloze_buf):
                n = cg["anchors"][0][0]
                questions[n] = dict(n=n, page=pi + 1, stem=f"（{n}）", context=passage if k == 0 else "", options=options,
                                    crop=crop if k == 0 else None, showCrop=False, cloze=True, groupLead=cloze_buf[0]["anchors"][0][0])
            prev_end[pi] = rows.index(opt_rows[-1]) + 1 if opt_rows else len(rows)
            cloze_buf = []
            continue
        end_ri = nxt["ri"] if nxt and nxt["page"] == pi else len(rows)
        body = [r for r in rows[ri + 1:end_ri] if not (r["y0"] > pages[pi]["h"] - 60 and is_header(r["text"]))]
        anchors = g["anchors"]
        # column boundaries
        xs = [a[1] for a in anchors]
        bounds = [(xs[i] - 10 if i else -1, (xs[i + 1] - 10) if i + 1 < len(xs) else 1e9) for i in range(len(xs))]
        # context rows for the first anchor
        ctx_rows = []
        for r in ([] if g.get("reanchor") else rows[prev_end.get(pi, 0):ri]):
            if is_header(r["text"]) or (r["y0"] > pages[pi]["h"] - 60 and re.fullmatch(r'[\d\-– ]+', r["text"])):
                continue
            ctx_rows.append(r)
        # a stem printed on the same visual line just above the anchor
        lifted = None
        if ctx_rows and abs(ctx_rows[-1]["y1"] - rows[ri]["y0"]) < 6 and len(anchors) == 1 and not anchors[0][2]:
            lifted = ctx_rows.pop()
        last_used = ri
        for ai, (n, x0, rest) in enumerate(anchors):
            lo, hi = bounds[ai]
            col_rows = []
            for r in body:
                its = [it for it in r["items"] if lo <= it["x0"] < hi] if len(anchors) > 1 else r["items"]
                if its:
                    col_rows.append(dict(r, items=its, text=join_items(its), x0=its[0]["x0"]))
            stem = rest
            if len(anchors) == 1:
                row_items = rows[ri]["items"]
                idx = next((k for k, it in enumerate(row_items) if ANCHOR_RE.match(it["text"])), 0)
                tail = join_items(row_items[idx + 1:])
                stem = (stem + " " + tail).strip() if tail else stem
            if lifted is not None and not stem:
                stem = lifted["text"]
            opt_rows, stem_rows, seen_opt = [], [], False
            if OPT_SPLIT_RE.search(stem):
                opt_rows.append(dict(text=stem, x0=0, y0=0, y1=0))
                stem = OPT_SPLIT_RE.split(stem)[0].strip()
                seen_opt = True
            for r in col_rows:
                if OPT_SPLIT_RE.search(r["text"]):
                    seen_opt = True
                    opt_rows.append(r)
                elif seen_opt:
                    if opt_rows and r["x0"] >= opt_rows[-1]["x0"] + 8 and r["y0"] - opt_rows[-1]["y1"] < 12:
                        opt_rows.append(r)
                    else:
                        break
                else:
                    stem_rows.append(r)
            if stem_rows:
                stem = (stem + " " + join_rows(stem_rows)).strip()
            options = parse_options(opt_rows)
            for r in opt_rows:
                if r in rows:
                    last_used = max(last_used, rows.index(r))
                else:
                    for rr in rows:
                        if rr["y0"] == r.get("y0") and rr["y0"]:
                            last_used = max(last_used, rows.index(rr))
            context = join_rows(ctx_rows) if ai == 0 else ""
            top = min([rows[ri]["y0"]] + ([ctx_rows[0]["y0"]] if ai == 0 and ctx_rows else []) + ([lifted["y0"]] if lifted else [])) - 8
            if nxt and nxt["page"] == pi:
                bottom = rows[nxt["ri"]]["y0"] - 6
                nctx = [r for r in rows[ri + 1:nxt["ri"]] if r["y0"] > (opt_rows[-1]["y1"] if opt_rows and opt_rows[-1].get("y1") else 0) + 2]
            else:
                bottom = pages[pi]["h"] - 50
            region = [r for r in rows if r["y0"] >= top and r["y1"] <= bottom]
            ys = sorted([top + 8] + [y for r in region for y in (r["y0"], r["y1"])] + [bottom])
            max_gap = max((b - a) for a, b in zip(ys, ys[1:])) if len(ys) > 1 else 0
            empty_opts = (not options) or any(not o["text"] for o in options)
            has_pic = (pi + 1) in imgs and (max_gap > 45 or empty_opts)
            crop = save_crop(pdf, pages, rendered, media_dir, pi, top, bottom, f"q{n}{'o' if g.get('reanchor') else ''}.webp") if len(anchors) == 1 or ai == 0 else None
            if g.get("reanchor") and n in questions:
                if options:
                    questions[n]["options"] = options
                    questions[n]["optionsPage"] = pi + 1
                    questions[n]["cropOptions"] = crop
                continue
            questions[n] = dict(n=n, page=pi + 1, stem=stem, context=context, options=options, crop=crop,
                                showCrop=bool(has_pic), cropGap=round(max_gap))
        prev_end[pi] = last_used + 1
    for p in media_dir.glob("_p*.png"):
        p.unlink()
    found = sorted(questions)
    if found != list(range(1, n_questions + 1)):
        missing = sorted(set(range(1, n_questions + 1)) - set(found))
        issues.append(dict(test=test_id, kind="booklet_questions_missing", detail=f"missing {missing}"))
    parts = [p for p in parts if "from" in p]
    if not parts:
        issues.append(dict(test=test_id, kind="no_parts_detected"))
    return questions, parts


def save_crop(pdf, pages, rendered, media_dir, pi, top, bottom, name):
    if pi not in rendered:
        png = media_dir / f"_p{pi + 1}.png"
        render_page(pdf, pi + 1, png, dpi=150)
        rendered[pi] = Image.open(png).convert("RGB")
    im = rendered[pi]
    sc = im.width / pages[pi]["w"]
    box = (int(30 * sc), int(max(0, top) * sc), int((pages[pi]["w"] - 30) * sc), int(min(bottom, pages[pi]["h"]) * sc))
    if box[3] - box[1] < 20:
        return None
    im.crop(box).save(media_dir / name, "WEBP", quality=72)
    return name


def parse_answer_key(pdf, n_questions, test_id, issues, skip=0):
    txt = plain_text(pdf)
    pairs = re.findall(r'(?<!\d)(\d{1,2})\s+([A-F])(?![A-Za-z])', txt)
    ans = {}
    expected = 1
    pairs = pairs[skip:]
    for num, letter in pairs:
        num = int(num)
        if num == expected:
            ans[num] = letter
        else:
            issues.append(dict(test=test_id, kind="answer_key_label_mismatch",
                               detail=f"answer key prints question number {num} at the position of question {expected}; used position (answer {letter})"))
            ans[expected] = letter
        expected += 1
        if expected > n_questions:
            break
    if len(ans) != n_questions:
        issues.append(dict(test=test_id, kind="answer_key_incomplete", detail=f"{len(ans)}/{n_questions} answers parsed"))
    return ans


RANGE_RE = re.compile(r'第\s*(\d{1,2})\s*(?:[～~\-–至到]|題\s*[～~\-–至到])\s*(\d{1,2})\s*題')


def parse_script(pdf, n_questions, test_id, issues):
    pages = pages_lines(pdf)
    rows = [r for p in pages for r in rows_of(p)]
    script_parts = []
    blocks = {}
    current = None
    expected = 1
    pending = []  # rows before an anchor (group intro, e.g. passage text)
    group_ranges = []
    for r in rows:
        t = r["text"]
        m = ANCHOR_RE.match(t) or SCRIPT_ANCHOR_RE.match(t)
        if m and int(m.group(1)) == expected and r["x0"] < 150:
            current = expected
            inline = bool(m.group(2).strip()) and not re.match(r'^[男女甲乙]\s*[:：]', m.group(2).strip())
            blocks[current] = dict(pre=pending, lines=[m.group(2)] if m.group(2) else [], inline=inline)
            pending = []
            expected += 1
            continue
        if re.match(r'^(以下是|請聽|下面是|接下來)', t):
            current = None
            pending = [t]
            continue
        rm = RANGE_RE.search(t)
        if rm:
            group_ranges.append((int(rm.group(1)), int(rm.group(2)), len(group_ranges)))
        pm = re.match(r'^(第[一二三四五]部分)\s*(\S*)', t)
        if pm:
            script_parts.append(dict(title=pm.group(1), subtitle=pm.group(2), instructions="", instructionsEn="", page=None, startAt=expected))
        if re.match(r'^(第[一二三四五]部分|.*聽力文本|.*模擬試題)', t):
            pending = []
            current = None if 'block' else current
            continue
        if current is not None and blocks[current].get("inline") and not re.match(r'^[(（]', t):
            current = None
            pending = []
        if current is None:
            pending.append(t)
        else:
            blocks[current]["lines"].append(t)
    if len(blocks) != n_questions:
        issues.append(dict(test=test_id, kind="script_anchor_mismatch", detail=f"{len(blocks)}/{n_questions} script blocks"))
    out = {}
    group_intro, lead = "", None
    for n in sorted(blocks):
        b = blocks[n]
        lines = [l for l in b["lines"] if l]
        pre = "\n".join(l for l in b["pre"] if l)
        if pre:
            group_intro, lead = pre, n
        elif lines and len(lines) > 2:
            group_intro, lead = "", None  # a self-contained item: dialogue follows its own number
        out[n] = dict(transcript="\n".join(lines), intro=group_intro, lead=lead)
    for i, p in enumerate(script_parts):
        p["from"] = p.pop("startAt"); p["to"] = (script_parts[i + 1]["startAt"] - 1) if i + 1 < len(script_parts) else n_questions
    out["_parts"] = script_parts
    return out


def build(src_root, out_root):
    src_root, out_root = Path(src_root), Path(out_root)
    content_dir = out_root / "public" / "content" / "exercise"
    content_dir.mkdir(parents=True, exist_ok=True)
    all_issues = []
    index = []
    for t in CATALOG:
        issues = []
        base = src_root / "TOCFL Exercise" / t["folder"]
        nq = t["questions"]
        media = out_root / "public" / "media" / "ex" / t["id"]
        q, parts = parse_booklet(base / t["booklet"], nq, media, t["id"], issues)
        key = parse_answer_key(base / t["answer"], nq, t["id"], issues, skip=t.get("keySkip", 0))
        scr = parse_script(base / t["script"], nq, t["id"], issues) if t.get("script") else {}
        sparts = scr.pop("_parts", []) if scr else []
        if not parts and sparts:
            parts = sparts
            issues[:] = [i for i in issues if i["kind"] != "no_parts_detected"]
            issues.append(dict(test=t["id"], kind="parts_from_script", detail="booklet part headers not detected; parts taken from listening script headings"))
        for p in parts:
            p["grouped"] = any(k in p["title"] for k in ("閱讀", "段落", "短文", "選詞", "完成", "填空", "對話")) and t["skill"] == "reading" or "段落" in p["title"]
        qs = []
        for n in range(1, nq + 1):
            item = q.get(n, dict(n=n, stem="", context="", options=[], crop=None, showCrop=True, missing=True))
            item["answer"] = key.get(n)
            item["gradable"] = item["answer"] is not None
            if scr.get(n):
                item["transcript"] = scr[n]["transcript"]
                if scr[n]["intro"]:
                    item["transcriptIntro"] = scr[n]["intro"]
                    item["transcriptLead"] = scr[n]["lead"]
            item["part"] = next((i for i, p in enumerate(parts) if p["from"] <= n <= p["to"]), None)
            qs.append(item)
        counts = [len(x["options"]) for x in qs if x["options"]]
        opt_n = max(set(counts), key=counts.count) if counts else 3
        for x in qs:
            if not x["options"] and t["skill"] == "listening":
                x["spokenOptions"] = True
                x["showCrop"] = True
        # group consecutive questions sharing a context passage (context only printed once)
        gid = None
        for item in qs:
            if item.get("context"):
                gid = f"g{item['n']}"
            elif gid and item["part"] is not None and parts[item["part"]].get("grouped"):
                pass
            else:
                gid = None
            item["group"] = gid if (gid and item["part"] is not None and parts[item["part"]].get("grouped")) else None
        audio = t.get("audio")
        full_script = plain_text(base / t["script"], layout=False) if t.get("script") else None
        if full_script:
            full_script = re.sub(r'\n{3,}', '\n\n', full_script.replace('\f', '\n')).strip()
        for iss in issues:
            if iss["kind"] == "answer_key_label_mismatch":
                qn = int(re.search(r'position of question (\d+)', iss["detail"]).group(1))
                qs[qn - 1]["answerNote"] = iss["detail"]
        data = dict(id=t["id"], band=t["band"], skill=t["skill"], series=t["series"], title=t["title"],
                    source=dict(folder=t["folder"], booklet=t["booklet"], answer=t["answer"], script=t.get("script")),
                    timeMinutes=t.get("time"), parts=parts, questions=qs, audio=audio, fullScript=full_script, optionCount=opt_n)
        (content_dir / f"{t['id']}.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
        index.append(dict(id=t["id"], band=t["band"], skill=t["skill"], series=t["series"], title=t["title"],
                          questions=nq, gradable=sum(1 for x in qs if x["gradable"]), timeMinutes=t.get("time"),
                          issues=len(issues)))
        all_issues += issues
        print(t["id"], "q:", len(q), "key:", len(key), "script:", len(scr), "issues:", len(issues))
    (content_dir / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8")
    (out_root / "reports").mkdir(exist_ok=True)
    (out_root / "reports" / "exercise_validation.json").write_text(json.dumps(all_issues, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2])
