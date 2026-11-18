"""Pinyin + English + Indonesian explanations for the per-part question bank (pb-* tests).

Data: pipeline/explain_bank/<section>.json
  {"items": {"<item>": {"passage": [zh, ...], "subs": {"1": {"stem": zh, "options": {"A": zh, ...}}}}},
   "tr": {"<zh>": [english, indonesian]}}
  "items" holds the Chinese of reading items, transcribed from the item picture (checked against the PDF
  text layer where one exists). Listening items use the official script already stored in the test JSON.
  Translations are looked up first in "tr", then in the full-test explanations (same sentence, same meaning).

  python bank_explain.py stats                 -> per-section coverage
  python bank_explain.py items <sec>           -> reading items still to transcribe (item, printed text, picture path)
  python bank_explain.py todo <sec> [n]        -> untranslated lines (id, Chinese); writes /tmp/bank/<sec>.todo.json
  python bank_explain.py apply <sec> <tsv>     -> tsv lines "id<TAB>English<TAB>Indonesian" from the last todo
  python bank_explain.py load <sec> <file>     -> store reading transcriptions (format in load_items)
  python bank_explain.py merge <sec>           -> writes content/exercise/explain/pb-<sec>-<k>.json
"""
import glob
import json
import re
import sys
from pathlib import Path

from explain_tool import has_zh, sentences, speaker, structure
from pinyin_util import to_pinyin

ROOT = Path(__file__).resolve().parent.parent
BANK = ROOT / "pipeline" / "explain_bank"
TMP = Path("/tmp/bank")
norm = lambda s: re.sub(r"\s+", "", s or "")


def tests(sec):
    out = []
    for f in sorted(glob.glob(str(ROOT / "content" / "exercise" / f"pb-{sec}-*.json")), key=lambda p: int(re.search(r"-(\d+)\.json$", p).group(1))):
        t = json.loads(Path(f).read_text(encoding="utf-8"))
        if t.get("section") == sec:
            out.append(t)
    return out


def load(sec):
    f = BANK / f"{sec}.json"
    return json.loads(f.read_text(encoding="utf-8")) if f.exists() else {"items": {}, "tr": {}}


def save(sec, d):
    BANK.mkdir(exist_ok=True)
    (BANK / f"{sec}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


_mem = None


def memory():
    """zh -> (en, idn) from the full-test explanations and every bank section."""
    global _mem
    if _mem is None:
        _mem = {}

        def walk(x):
            if isinstance(x, dict):
                if x.get("zh") and x.get("en") and x.get("idn"):
                    _mem.setdefault(norm(x["zh"]), (x["en"], x["idn"]))
                for v in x.values():
                    walk(v)
            elif isinstance(x, list):
                for v in x:
                    walk(v)
        for f in glob.glob(str(ROOT / "content" / "exercise" / "explain" / "*.json")):
            if "/pb-" not in f:
                walk(json.loads(Path(f).read_text(encoding="utf-8")))
        for f in glob.glob(str(BANK / "*.json")):
            for zh, v in json.loads(Path(f).read_text(encoding="utf-8")).get("tr", {}).items():
                if v and v[0] and v[1]:
                    _mem[norm(zh)] = tuple(v)
    return _mem


def lines(sec, t, d):
    """(question n, field, key, zh) for one bank test. Reading items come from the transcription store."""
    if t["skill"] == "listening":
        items = structure(t)
        # questions of one multi-question item share the script: give each its transcript
        have = {n for n, f, _, _ in items if f == "transcript"}
        first = {}
        for q in t["questions"]:
            first.setdefault(q["item"], q["n"])
        for q in t["questions"]:
            lead = first[q["item"]]
            if q["n"] not in have and lead != q["n"] and lead in have:
                items += [(q["n"], "transcript", None, z) for n, f, _, z in structure(t) if n == lead and f == "transcript"]
        return items
    items, done = [], set()
    for q in t["questions"]:
        it = d["items"].get(q["item"])
        if not it:
            continue
        if q["item"] not in done:
            done.add(q["item"])
            for s in it.get("image", []):
                items.append((q["n"], "image", None, s))
            for s in it.get("passage", []):
                items.append((q["n"], "passage", None, s))
        sub = it.get("subs", {}).get(str(q.get("sub", 1)), {})
        if sub.get("stem"):
            items.append((q["n"], "stem", None, sub["stem"]))
        opts = dict(it.get("subs", {}).get("*", {}).get("options", {}))
        opts.update(sub.get("options", {}))
        for L, z in sorted(opts.items()):
            items.append((q["n"], "option", L, z))
    return items


def all_lines(sec):
    d = load(sec)
    out = []
    for t in tests(sec):
        out += [(t["id"],) + x for x in lines(sec, t, d)]
    return d, out


def stats():
    secs = sorted({json.loads(Path(f).read_text(encoding="utf-8"))["section"] for f in glob.glob(str(ROOT / "content" / "exercise" / "pb-*.json"))})
    mem = memory()
    for sec in secs:
        d, ls = all_lines(sec)
        uniq = {norm(x[4]): x[4] for x in ls}
        miss = [z for k, z in uniq.items() if k not in mem]
        items = {q["item"] for t in tests(sec) for q in t["questions"]}
        reading = tests(sec)[0]["skill"] == "reading"
        print(f"{sec:14} lines {len(uniq):5} untranslated {len(miss):5}" + (f"  items transcribed {len(set(d['items']) & items)}/{len(items)}" if reading else ""))


def items_todo(sec):
    d = load(sec)
    seen = set()
    for t in tests(sec):
        for q in t["questions"]:
            if q["item"] in seen or q["item"] in d["items"]:
                continue
            seen.add(q["item"])
            subs = sum(1 for x in t["questions"] if x["item"] == q["item"])
            print(f"=== {q['item']}  subs {subs}  options {len(q.get('options', []))}  picture media/ex/{t['id']}/{q.get('crop')}")
            print(q.get("printedText") or "(no text layer)")


def todo(sec, limit=None):
    d, ls = all_lines(sec)
    mem = memory()
    seen, rows = set(), []
    for tid, n, field, key, zh in ls:
        k = norm(zh)
        if k in mem or k in seen:
            continue
        seen.add(k)
        rows.append(zh)
    if limit:
        rows = rows[:int(limit)]
    TMP.mkdir(exist_ok=True)
    (TMP / f"{sec}.todo.json").write_text(json.dumps({str(i + 1): z for i, z in enumerate(rows)}, ensure_ascii=False), encoding="utf-8")
    for i, z in enumerate(rows):
        print(f"{i + 1}\t{z}")
    print(f"# {len(rows)} lines", file=sys.stderr)


def apply(sec, tsv):
    ids = json.loads((TMP / f"{sec}.todo.json").read_text(encoding="utf-8"))
    d = load(sec)
    got, bad = 0, []
    for ln in Path(tsv).read_text(encoding="utf-8").splitlines():
        if not ln.strip():
            continue
        p = ln.split("\t")
        if len(p) != 3 or p[0] not in ids or not p[1].strip() or not p[2].strip():
            bad.append(ln[:60])
            continue
        d["tr"][ids[p[0]]] = [p[1].strip(), p[2].strip()]
        got += 1
    save(sec, d)
    missing = [i for i in ids if ids[i] not in d["tr"]]
    print(f"{sec}: applied {got}, bad {len(bad)} {bad[:3]}, missing ids {missing[:20]}{'…' if len(missing) > 20 else ''}")


def load_items(sec, path):
    """Transcription file: '@<item>' starts an item; 'P: zh' passage line; 'I: zh' text printed inside the picture; 'S<k>: zh' stem of sub-question k;
    '<A-F><k>: zh' option of sub-question k ('<A-F>*' = shared by every sub-question). Replaces earlier entries for the same item."""
    d = load(sec)
    cur = None
    for ln in Path(path).read_text(encoding="utf-8").splitlines():
        ln = ln.rstrip()
        if not ln.strip() or ln.startswith("#"):
            continue
        if ln.startswith("@"):
            cur = d["items"][ln[1:].strip()] = {"image": [], "passage": [], "subs": {}}
            continue
        m = re.match(r"^(P|I|S\d+|[A-F](?:\d+|\*)):\s?(.*)$", ln)
        if not m or cur is None:
            raise SystemExit(f"bad line: {ln}")
        tag, zh = m.groups()
        if tag == "P":
            cur["passage"].append(zh.strip())
        elif tag == "I":
            cur["image"].append(zh.strip())
        elif tag[0] == "S":
            cur["subs"].setdefault(tag[1:], {})["stem"] = zh.strip()
        else:
            cur["subs"].setdefault(tag[1:], {}).setdefault("options", {})[tag[0]] = zh.strip()
    save(sec, d)
    print(f"{sec}: items stored {len(d['items'])}")


def merge(sec):
    d, _ = all_lines(sec)
    mem = memory()
    total_missing, untrans = 0, 0
    for t in tests(sec):
        out = {}
        n_lines = 0
        reading = t["skill"] == "reading"
        missing_items = sorted({q["item"] for q in t["questions"]} - set(d["items"])) if reading else []
        prev = {}
        for n, field, key, zh in lines(sec, t, d):
            tr = mem.get(norm(zh))
            p = prev.get((n, field))
            cont = bool(field in ("passage", "transcript", "intro") and p and len(p.strip()) >= 15 and p.strip()[-1] not in "。？！?!…」』”：:）)＃#0123456789")
            seg = {"zh": zh, "py": to_pinyin(zh, cont)}
            if tr:
                seg["en"], seg["idn"] = tr
                if field == "option":  # options carry their label, as in the full tests
                    seg["en"], seg["idn"] = (f"({key}) " + re.sub(r"^\([A-D]\)\s*", "", x) for x in tr)
            else:
                untrans += 1
            n_lines += 1
            e = out.setdefault(str(n), {})
            if field == "stem":
                e["stem"] = seg
            elif field == "option":
                e.setdefault("options", {})[key] = seg
            else:
                e.setdefault(field, []).append(seg)
                prev[(n, field)] = zh
        complete = not missing_items and all("en" in s for e in out.values() for s in walk_segs(e))
        total_missing += len(missing_items)
        doc = {"testId": t["id"], "segments": n_lines, "englishComplete": complete, "indonesianComplete": complete, "questions": out}
        (ROOT / "content" / "exercise" / "explain" / f"{t['id']}.json").write_text(json.dumps(doc, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"{sec}: tests {len(tests(sec))} untranslated lines {untrans} items not transcribed {total_missing}")


def walk_segs(e):
    for k, v in e.items():
        if k == "stem":
            yield v
        elif k == "options":
            yield from v.values()
        else:
            yield from v


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "stats":
        stats()
    elif cmd == "items":
        items_todo(sys.argv[2])
    elif cmd == "todo":
        todo(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
    elif cmd == "apply":
        apply(sys.argv[2], sys.argv[3])
    elif cmd == "load":
        load_items(sys.argv[2], sys.argv[3])
    elif cmd == "merge":
        merge(sys.argv[2])
