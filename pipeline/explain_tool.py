"""Pinyin + English explanations for TOCFL Exercise questions.

  python explain_tool.py sheet <testId>    -> prints numbered Chinese segments to translate
  python explain_tool.py merge <testId>    -> reads pipeline/explain_src/<testId>.json (id -> English,
                                              plus "img:<n>": [[zh, en], ...] for text printed inside pictures)
                                              and pipeline/explain_src_id/<testId>.json (id -> Indonesian,
                                              "img:<n>:<k>" -> Indonesian for the k-th picture line),
                                              and writes content/exercise/explain/<testId>.json
  python explain_tool.py idsheet <testId>  -> prints id, Chinese and English for every segment (for the Indonesian pass)
Every segment must be translated; merge fails if any is missing.
"""
import json
import re
import sys
from pathlib import Path

from pinyin_util import to_pinyin

ROOT = Path(__file__).resolve().parent.parent
SENT_RE = re.compile(r'.+?(?:[。！？；](?:[」』”）)])*|$)', re.S)


def sentences(text):
    out = []
    for line in (text or "").split("\n"):
        line = line.strip()
        if not line:
            continue
        if len(line) <= 40:
            out.append(line)
            continue
        out += [m.group(0).strip() for m in SENT_RE.finditer(line) if m.group(0).strip()]
    return out


SPEAKER_RE = re.compile(r'^(男|女)(?![兒生人孩士朋：:])')


def speaker(line):
    """Script lines are printed as 男/女 + speech; show the speaker label as 男：…"""
    line = re.sub(r'^提問(?![：:])\s*', '提問：', line)
    line = SPEAKER_RE.sub(r'\1：', line)
    return re.sub(r'^(男|女)：\s*(\d)\s+', r'\1\2：', line)  # 女：1 … → 女1：…


def has_zh(s):
    return bool(re.search(r'[㐀-鿿]', s or ""))


def structure(test):
    """Ordered list of (question n, field, key, chinese) — field in passage/stem/option/intro/transcript."""
    items = []
    for q in test["questions"]:
        n = q["n"]
        for s in sentences(q.get("context")):
            items.append((n, "passage", None, s))
        if has_zh(q.get("stem")) and not re.fullmatch(r'[（(]\d+[）)]', q["stem"].strip()):
            items.append((n, "stem", None, q["stem"].strip()))
        for o in q.get("options", []):
            if has_zh(o.get("text")):
                items.append((n, "option", o["label"], o["text"].strip()))
        for s in sentences(q.get("transcriptIntro")) if q.get("transcriptLead") == n else []:
            items.append((n, "intro", None, speaker(s)))
        for s in sentences(q.get("transcript")):
            items.append((n, "transcript", None, speaker(s)))
    return items


def segments(test):
    ids, order = {}, []
    for it in structure(test):
        if it[3] not in ids:
            ids[it[3]] = str(len(order) + 1)
            order.append(it[3])
    return ids, order


def load(tid):
    return json.loads((ROOT / "content" / "exercise" / f"{tid}.json").read_text(encoding="utf-8"))


def sheet(tid):
    test = load(tid)
    ids, _ = segments(test)
    seen = set()
    for n, field, key, zh in structure(test):
        tag = f"{n}{field[0].upper()}{key or ''}"
        sid = ids[zh]
        if sid in seen:
            print(f"{sid}\t[{tag}] (repeat)")
            continue
        seen.add(sid)
        print(f"{sid}\t[{tag}] {zh}")
    pics = [q["n"] for q in test["questions"] if q.get("showCrop") or (q.get("layout") and not q.get("context") and not has_zh(q.get("stem")))]
    print("PICTURES:", pics)


def merge(tid):
    test = load(tid)
    sf = ROOT / "pipeline" / "explain_src" / f"{tid}.json"
    src = json.loads(sf.read_text(encoding="utf-8")) if sf.exists() else {}
    ids, order = segments(test)
    missing = [i for i in map(str, range(1, len(order) + 1)) if not src.get(i, "").strip()]
    complete = not missing and src.get("_images_done") is True
    idf = ROOT / "pipeline" / "explain_src_id" / f"{tid}.json"
    ind = json.loads(idf.read_text(encoding="utf-8")) if idf.exists() else {}
    img_keys = [f"{k}:{j}" for k, v in src.items() if k.startswith("img:") for j in range(len(v or []))]
    id_missing = [i for i in list(map(str, range(1, len(order) + 1))) + img_keys if not ind.get(i, "").strip()]

    def seg(zh, prev=None):
        cont = bool(prev and len(prev.strip()) >= 15 and prev.strip()[-1] not in "。？！?!…」』”：:）)＃#0123456789")
        d = dict(zh=zh, py=to_pinyin(zh, cont))
        if src.get(ids[zh], "").strip():
            d["en"] = src[ids[zh]].strip()
        if ind.get(ids[zh], "").strip():
            d["idn"] = ind[ids[zh]].strip()
        return d
    out = {}
    for n, field, key, zh in structure(test):
        e = out.setdefault(str(n), {})
        if field == "stem":
            e["stem"] = seg(zh)
        elif field == "option":
            e.setdefault("options", {})[key] = seg(zh)
        else:
            lst = e.setdefault(field, [])
            lst.append(seg(zh, lst[-1]["zh"] if lst else None))
    for k, v in src.items():
        if k.startswith("img:") and v:
            out.setdefault(k[4:], {})["image"] = [dict(zh=zh, py=to_pinyin(zh), en=en, **({"idn": ind[f"{k}:{j}"].strip()} if ind.get(f"{k}:{j}", "").strip() else {}))
                                                  for j, (zh, en) in enumerate(v)]
    d = ROOT / "content" / "exercise" / "explain"
    d.mkdir(exist_ok=True)
    (d / f"{tid}.json").write_text(json.dumps(dict(testId=tid, segments=len(order), englishComplete=complete, indonesianComplete=complete and not id_missing, questions=out), ensure_ascii=False, indent=1), encoding="utf-8")
    print(tid, "segments", len(order), "untranslated", len(missing), "complete", complete, "indonesian missing", len(id_missing), "questions", len(out), "image texts", sum(1 for k in src if k.startswith("img:")))


def idsheet(tid):
    test = load(tid)
    ids, order = segments(test)
    src = json.loads((ROOT / "pipeline" / "explain_src" / f"{tid}.json").read_text(encoding="utf-8"))
    for i, zh in enumerate(order, 1):
        print(f"{i}\t{zh}\t{src.get(str(i), '')}")
    for k, v in src.items():
        if k.startswith("img:"):
            for j, (zh, en) in enumerate(v):
                print(f"{k}:{j}\t{zh}\t{en}")


if __name__ == "__main__":
    {"sheet": sheet, "merge": merge, "idsheet": idsheet}[sys.argv[1]](sys.argv[2])
