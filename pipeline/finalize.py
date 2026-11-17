"""Attach audio targets to content JSON and write content/media-manifest.json.

Usage: python finalize.py <OUT_ROOT>
Every source audio file gets an ASCII-safe target path under media/audio/.
scripts/sync-media.mjs copies source -> target on the user's machine.
"""
import json
import re
import sys
from pathlib import Path


def safe(name):
    base, ext = name.rsplit(".", 1)
    base = re.sub(r'[^A-Za-z0-9\-]+', '_', base).strip('_') or 'track'
    return f"{base}.{ext.lower()}"


def main(out):
    out = Path(out)
    content = out / "content"
    manifest = []
    # ---- exercises
    for f in sorted((content / "exercise").glob("*.json")):
        if f.name in ("index.json", "sections.json", "partbank.json"):
            continue
        d = json.loads(f.read_text(encoding="utf-8"))
        for q in d["questions"]:
            q["stem"] = re.sub(r'\s*現在請聽(這|下面|以下).{0,8}[。．]?\s*$', '', q.get("stem", "")).strip()
        a = d.get("audio")
        if not a:
            f.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
            continue
        tracks = []
        for i, name in enumerate(a["tracks"]):
            src = f"ex/{d['id']}/t{i + 1:03d}-{safe(name.rsplit('/', 1)[-1])}"
            manifest.append(dict(source="/".join(x for x in ("TOCFL Exercise", a["dir"], name) if x), target=src))
            label = name.rsplit(".", 1)[0]
            m = re.match(r'^(\d)-(\d{2})(?:-(\d))?$', label)
            kind, q = "other", None
            if a["kind"] == "by-filename" and m:
                q = int(m.group(2))
                kind = "dialogue" if m.group(3) == "0" else "question"
                label = f"Soal {q}" + (" — percakapan/teks" if kind == "dialogue" else "")
            elif re.match(r'^\d-0+', label) or label.startswith("0-") or label.endswith("-00"):
                kind = "instructions"
                label = "Petunjuk / jeda" if label.startswith(("0-", "5-", "3-0")) else f"Petunjuk Bagian {label[0]}"
            else:
                label = f"Trek {i + 1} ({name})"
            tracks.append(dict(src=src, file=name, label=label, kind=kind, q=q))
        a["trackList"] = tracks
        if d.get("kind") == "partbank":
            for qd in d["questions"]:
                if "_track" in qd:
                    i = qd.pop("_track"); qd["audio"] = [i]
                    tracks[i].update(label=f"Soal {qd['n']} ({qd.get('item')})", kind="question", q=qd["n"])
            f.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
            continue
        # per-question mapping (only when naming encodes the question number)
        if a["kind"] == "by-filename":
            byq = {}
            for i, tr in enumerate(tracks):
                if tr["q"]:
                    byq.setdefault(tr["q"], []).append(i)
            for qd in d["questions"]:
                idxs = byq.get(qd["n"], [])
                lead = qd.get("transcriptLead")
                if lead and lead != qd["n"]:
                    lead_dialogue = [i for i in byq.get(lead, []) if tracks[i]["kind"] == "dialogue"]
                    idxs = lead_dialogue + idxs
                qd["audio"] = idxs
        f.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    # ---- study
    sdir = content / "study"
    for f in sorted(sdir.glob("*.json")):
        if f.name == "index.json":
            continue
        d = json.loads(f.read_text(encoding="utf-8"))
        ad = d["source"].get("audioDir")
        for l in d["lessons"] + [{"tracks": d.get("otherTracks", [])}]:
            for tr in l["tracks"]:
                tr["src"] = f"study/{d['id']}/{safe(tr['file'])}"
                manifest.append(dict(source=f"TOCFL Study/{ad}/{tr['file']}", target=tr["src"]))
        f.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    (content / "media-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=0), encoding="utf-8")
    print("manifest entries:", len(manifest))


if __name__ == "__main__":
    main(sys.argv[1])
