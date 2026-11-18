# Original-mode lesson builder.
# Usage: python pipeline/build_lesson.py pipeline/lesson_src/<lessonId>.py
# The source file defines LESSON_ID, TITLE, STATUS, DETAIL and calls H/T/V/D/EX/X/add in page order.
import json, sys
B = []
def add(b, pages=None):
    if pages: b["source"] = {"pages": pages}
    B.append(b)
def H(id, en, zh=None, level=None, pages=None):
    b = {"type": "heading", "id": id, "en": en}
    if zh: b["zh"] = zh
    if level: b["level"] = level
    add(b, pages)
def T(id, *paras, pages=None, track=None):
    b = {"type": "text", "id": id, "paras": [{"lang": "en", "text": p} for p in paras]}
    if track: b["track"] = track
    add(b, pages)
def V(id, title, rows, start=1, track=None, pages=None):
    items = []
    for i, r in enumerate(rows):
        zh, py, pos, en = r
        items.append({"n": start + i, "zh": zh, "py": py, "pos": pos, "en": en})
    b = {"type": "vocab", "id": id, "title": title, "items": items}
    if track: b["track"] = track
    add(b, pages)
def D(id, track, lines, trans, pages=None):
    b = {"type": "dialogue", "id": id}
    if track: b["track"] = track
    add({**b,
         "lines": [{"spk": s, "zh": z, "py": p} for s, z, p in lines],
         "translation": [{"spk": s, "en": e} for s, e in trans]}, pages)
def EX(id, items, title=None, pages=None):
    b = {"type": "examples", "id": id, "items": [{"zh": z, "py": p, "en": e} for z, p, e in items]}
    if title: b["title"] = title
    add(b, pages)
def X(id, instruction, prompts, title="練習 Exercise", image=None, imageAlt=None, pages=None):
    b = {"type": "exercise", "id": id, "title": title, "instruction": instruction,
         "items": [{"prompt": p, "hint": ""} for p in prompts]}
    if image: b["image"] = image; b["imageAlt"] = imageAlt
    add(b, pages)

exec(open(sys.argv[1], encoding="utf-8").read())

out = {
    "id": LESSON_ID,
    "title": TITLE,
    "status": STATUS,
    "mode": "original",
    "statusDetail": DETAIL,
    "transcribedBy": "Ditulis ulang secara orisinal berdasarkan isi buku, diperiksa terhadap halaman asli, 2026-11-18",
    "blocks": B,
}
ids = [b["id"] for b in B]
assert len(ids) == len(set(ids)), [i for i in ids if ids.count(i) > 1]
json.dump(out, open(f"content/study/lessons/{LESSON_ID}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(B), "blocks")
