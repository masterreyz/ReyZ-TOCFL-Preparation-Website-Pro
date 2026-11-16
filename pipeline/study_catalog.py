"""The study books found in "TOCFL Study" (inspected 2026-11-16).

Source series: 當代中文課程 / A Course in Contemporary Chinese, vols. 1–6
(National Taiwan Normal University Mandarin Training Center; Linking Publishing).
"""
LEVELS = [
    dict(id="a1", label="A1", folder="1. 第一本 (A1)", vol=1),
    dict(id="a2", label="A2", folder="2. 第二本 (A2)", vol=2),
    dict(id="b1", label="B1", folder="3. 第三本 (B1)", vol=3),
    dict(id="b2", label="B2", folder="4. 第四本 (B2)", vol=4),
    dict(id="c1", label="C1", folder="5. 第五本 (C1)", vol=5),
    dict(id="c2", label="C2", folder="6. 第六本 (C2)", vol=6),
]

BOOKS = []
for lv in LEVELS:
    for kind, label in (("textbook", "Textbook 課本"), ("workbook", "Workbook 作業本")):
        name = "Textbook" if kind == "textbook" else "Workbook"
        audio = f"TOCFL {lv['label']} {name} Audio"
        if lv["id"] == "c2" and kind == "workbook":
            audio = None  # no workbook audio folder exists for C2
        BOOKS.append(dict(id=f"{lv['id']}-{kind[0:2]}", level=lv["id"], kind=kind, label=label, vol=lv["vol"],
                          folder=lv["folder"], file=f"TOCFL {lv['label']} {name}.pdf",
                          audioDir=f"{lv['folder']}/{audio}" if audio else None))
