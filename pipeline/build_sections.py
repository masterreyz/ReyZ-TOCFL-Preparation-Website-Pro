"""Build content/exercise/sections.json: practice sections per band and skill.

Section names are the official part names printed in the answer keys and booklets
(第一部分 看圖回答 Part 1 Picture Description, ...). Novice keys print no part names, so their
labels describe each part's official instructions. Each section lists, for every mock test, the
question range of that part, as detected from the booklet (and confirmed by the listening scripts).

Usage: python build_sections.py <OUT_ROOT>
"""
import json
import sys
from pathlib import Path

SECTIONS = {
    ("novice", "listening"): [
        ("n-l1", "第一部分", "Part 1 — dengar kalimat, pilih gambar", "Listen to a sentence, choose the matching picture (A–C)."),
        ("n-l2", "第二部分", "Part 2 — lihat gambar, pilih kalimat yang didengar", "Look at a picture, choose the spoken sentence (A–C) that matches it."),
        ("n-l3", "第三部分", "Part 3 — dialog tanya-jawab singkat", "Listen to a short question-and-answer dialogue, then answer the question."),
    ],
    ("novice", "reading"): [
        ("n-r1", "第一部分", "Part 1 — baca teks, pilih gambar", "Read a short text, choose the matching picture (A–C)."),
        ("n-r2", "第二部分", "Part 2 — lihat gambar, pilih kalimat", "Look at a picture, choose the sentence (A–C) that matches it."),
    ],
    ("a", "listening"): [
        ("a-l-pic", "看圖回答", "Picture Description", "Lihat gambar, dengar pertanyaan dan tiga pilihan jawaban."),
        ("a-l-single", "問答理解", "Single-round Dialogue (Q&A Understanding)", "Dengar satu pertanyaan/pernyataan, pilih tanggapan yang tepat."),
        ("a-l-multi", "對話理解", "Multiple-round Dialogue (Dialogue Comprehension)", "Dengar percakapan beberapa giliran, jawab pertanyaannya."),
        ("a-l-dialogue", "對話", "Dialogue", "Dengar percakapan yang lebih panjang, jawab pertanyaannya."),
    ],
    ("a", "reading"): [
        ("a-r-sentence", "單句理解", "Sentence Comprehension (Single Sentence)", "Baca satu kalimat, pilih gambar yang sesuai."),
        ("a-r-pic", "看圖釋義", "Picture Description (Interpretation of the Image)", "Lihat gambar/teks visual, pilih pernyataan yang benar."),
        ("a-r-gap", "選詞填空", "Gap Filling (Fill in the Blanks)", "Pilih kata yang tepat untuk mengisi bagian kosong."),
        ("a-r-paragraph", "完成段落", "Paragraph Completion", "Lengkapi paragraf dengan pilihan kalimat (A–F)."),
        ("a-r-comp", "閱讀理解", "Reading Comprehension", "Baca teks pendek, jawab pertanyaannya."),
    ],
    ("b", "listening"): [
        ("b-l-dialogue", "對話", "Dialogue", "Dengar percakapan, jawab pertanyaan (A–D)."),
        ("b-l-monologue", "段落", "Monologue (Paragraph)", "Dengar pengumuman/teks monolog, jawab pertanyaan (A–D)."),
    ],
    ("b", "reading"): [
        ("b-r-gap", "選詞填空", "Gap Filling (Fill in the Blanks)", "Isi bagian kosong dalam teks dengan pilihan yang tepat."),
        ("b-r-comp", "閱讀理解", "Reading Comprehension", "Baca teks, jawab pertanyaannya."),
    ],
    ("c", "listening"): [
        ("c-l-dialogue", "對話", "Dialogue", "Dengar percakapan, jawab pertanyaan (A–D)."),
        ("c-l-monologue", "段落", "Monologue (Paragraph)", "Dengar teks monolog, jawab pertanyaan (A–D)."),
    ],
    ("c", "reading"): [
        ("c-r-gap", "選詞填空", "Gap Filling (Fill in the Blanks)", "Isi bagian kosong dalam teks dengan pilihan yang tepat."),
        ("c-r-comp", "閱讀理解", "Reading Comprehension", "Baca teks, jawab pertanyaannya."),
    ],
}


def main(out):
    cdir = Path(out) / "content" / "exercise"
    idx = [t for t in json.loads((cdir / "index.json").read_text(encoding="utf-8")) if not t["id"].startswith("pb-")]
    result = []
    for (band, skill), secs in SECTIONS.items():
        tests = [t for t in idx if t["band"] == band and t["skill"] == skill]
        for i, (key, zh, en, desc) in enumerate(secs):
            sets = []
            for t in sorted(tests, key=lambda x: x["series"]):
                d = json.loads((cdir / f"{t['id']}.json").read_text(encoding="utf-8"))
                if len(d["parts"]) != len(secs):
                    raise SystemExit(f"{t['id']}: {len(d['parts'])} parts, expected {len(secs)} — check the booklet")
                p = d["parts"][i]
                n = sum(1 for q in d["questions"] if p["from"] <= q["n"] <= p["to"])
                sets.append(dict(test=t["id"], series=t["series"], title=t["title"], part=i, partTitle=p["title"],
                                 instructions=p.get("instructions", ""), instructionsEn=p.get("instructionsEn", ""),
                                 **{"from": p["from"], "to": p["to"]}, questions=n))
            result.append(dict(id=key, band=band, skill=skill, order=i, zh=zh, name=en, desc=desc, sets=sets,
                               questions=sum(s["questions"] for s in sets)))
    (cdir / "sections.json").write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
    total = sum(s["questions"] for s in result)
    print(f"sections: {len(result)}, questions covered: {total}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
