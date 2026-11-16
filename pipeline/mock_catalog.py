"""Catalog of the official mock tests found in "TOCFL Exercise" (inspected 2026-11-16).

Audio track names were taken from the directory listing of the source folders.
`scripts/sync-media.mjs` re-checks every file on the user's machine and reports anything missing.

Audio mapping kinds:
  "by-filename": track names encode the question number (e.g. "1-07.mp3" -> Q7, "1-21-0"+"1-21-1" -> Q21).
                 Mapping is inferred from the official file naming, not from listening to each file.
  "sequence":    tracks are only numbered 001, 002, ... ; per-question mapping is NOT verified,
                 so the app offers the full ordered playlist instead of per-question clips.
"""


def rng(a, b, fmt):
    return [fmt.format(i) for i in range(a, b + 1)]


def seq(n):
    return [f"{i:03d}.mp3" for i in range(1, n + 1)]


def a_tracks(parts, intro_name, has_zero=True, final=True):
    """Band A style: 0-1, P-00000<intro>, P-NN ... ; parts = [(prefix, from, to)]"""
    t = ["0-1.mp3"] if has_zero else []
    for p, a, b in parts:
        t.append(intro_name(p))
        t += rng(a, b, f"{p}-{{:02d}}.mp3")
    if final:
        t.append(intro_name(len(parts) + 1))
    return t


def split_tracks(prefix, a, b, pairs):
    """Band B/C style where multi-question dialogues have -0 (dialogue) and -1 (first question)."""
    out = []
    for i in range(a, b + 1):
        if i in pairs:
            out += [f"{prefix}-{i:02d}-0.mp3", f"{prefix}-{i:02d}-1.mp3"]
        else:
            out.append(f"{prefix}-{i:02d}.mp3")
    return out


MOJI = "¤¤­^"  # garbled "中英" in Series 2/3 file names (as stored on disk)

N_L = "1. TOCFL Band Novice/Listening/Listening Test Series 1"
CATALOG = [
    dict(id="novice-l1", band="novice", skill="listening", series=1, title="Novice Listening · Series 1",
         folder=N_L, booklet="ls_mock_test_Novice_en_201811_t.pdf", script="ls_mock_test_Novice_listen.pdf",
         answer="mock_test_Novice_answer.pdf", questions=25,
         audio=dict(dir=N_L + "/mock_Novice_mp3_en", kind="sequence", tracks=seq(29))),
    dict(id="novice-r1", band="novice", skill="reading", series=1, title="Novice Reading · Series 1",
         folder="1. TOCFL Band Novice/Reading", booklet="1. TOCFL Reading Band Novice.pdf",
         answer="1. TOCFL Reading Answer Band Novice.pdf", questions=25, keySkip=25),
]

# ---- Band A listening
A1 = lambda p: f"{p}-00000中英-P{'(NEW)' if p == 4 else ''}.mp3"
A2 = lambda p: f"{p}-00000{MOJI}-P{'(NEW)' if p == 4 else ''}.mp3"
A3 = lambda p: f"{p}-00000{MOJI}-P(NEW).mp3"
A4 = lambda p: f"{p}-00000-英文-p.mp3.mp3"
std_a = [(1, 1, 25), (2, 26, 40), (3, 41, 45), (4, 46, 50)]
new_a = [(1, 1, 10), (2, 11, 25), (3, 26, 40), (4, 41, 50)]
A_AUDIO = {
    1: ("mock_BandA_mp3_en", a_tracks(std_a, A1)),
    2: ("mock2_BandA_mp3_en/mock2_BandA_mp3_en", a_tracks(std_a, A2)),
    3: ("mock3_BandA_mp3_en/mock3_BandA_mp3_en", a_tracks(new_a, A3)),
    4: ("mock4_BandA_mp3_en", a_tracks(new_a, A4)),
    5: ("mock5_BandA_mp3_en", a_tracks([(1, 1, 10), (2, 11, 28), (3, 29, 40), (4, 41, 50)], A4)),
}
for s in range(1, 6):
    m = "" if s == 1 else str(s)
    folder = f"2. TOCFL Band A/Listening/Listening Test Series {s}"
    d, tr = A_AUDIO[s]
    CATALOG.append(dict(id=f"a-l{s}", band="a", skill="listening", series=s, title=f"Band A Listening · Series {s}",
                        folder=folder, booklet=f"ls_mock{m}_test_BandA_en_t.pdf", script=f"ls_mock{m}_test_BandA_listen.pdf",
                        answer=f"ls_mock{m}_test_BandA_answer.pdf", questions=50,
                        audio=dict(dir=folder + "/" + d, kind="by-filename", tracks=tr)))
for s in range(1, 6):
    CATALOG.append(dict(id=f"a-r{s}", band="a", skill="reading", series=s, title=f"Band A Reading · Series {s}",
                        folder="2. TOCFL Band A/Reading", booklet=f"{s}. TOCFL Reading Band A.pdf",
                        answer=f"{s}. TOCFL Reading Answer Band A.pdf", questions=50))

# ---- Band B listening
b_pairs1 = {21, 23, 25, 28, 35, 37, 39, 41, 43, 45, 48}
b_pairs2 = {21, 23, 25, 28, 31, 33, 35, 37, 39, 41, 43, 45, 48}
B_AUDIO = {
    1: ("mock_BandB_mp3", "by-filename", ["1-00-1.mp3", "1-00-2.mp3"] + split_tracks(1, 1, 30, b_pairs1) + ["2-00.mp3"] + split_tracks(2, 31, 50, b_pairs1) + ["3-00.mp3"]),
    2: ("mock2_BandB_mp3", "by-filename", ["0-1.mp3", "1-00000.mp3"] + split_tracks(1, 1, 30, b_pairs2) + ["2-00000.mp3"] + split_tracks(2, 31, 50, b_pairs2) + ["3-00000.mp3"]),
    3: ("mock3_BandB_mp3", "sequence", ["0-1.mp3", "1-00000.mp3"] + rng(1, 35, "1-{:02d}.mp3") + ["2-00000.mp3"] + rng(36, 63, "2-{:02d}.mp3") + ["3-00000.mp3"]),
    4: ("mock4_BandB_mp3", "sequence", seq(67)),
    5: ("mock5_BandB", "sequence", seq(71)),
}
for s in range(1, 6):
    m = "" if s == 1 else str(s)
    folder = f"3. TOCFL Band B/Listening/Listening Test Series {s}"
    d, kind, tr = B_AUDIO[s]
    CATALOG.append(dict(id=f"b-l{s}", band="b", skill="listening", series=s, title=f"Band B Listening · Series {s}",
                        folder=folder, booklet=f"ls_mock{m}_test_BandB_t.pdf", script=f"ls_mock{m}_test_BandB_listen.pdf",
                        answer=f"ls_mock{m}_test_BandB_answer.pdf", questions=50,
                        audio=dict(dir=folder + "/" + d, kind=kind, tracks=tr)))
for s in range(1, 6):
    CATALOG.append(dict(id=f"b-r{s}", band="b", skill="reading", series=s, title=f"Band B Reading · Series {s}",
                        folder="3. TOCFL Band B/Reading", booklet=f"{s}. TOCFL Reading Band B.pdf",
                        answer=f"{s}. TOCFL Reading Answer Band B.pdf", questions=50))

# ---- Band C listening
c_pairs = {1, 3, 5, 8, 11, 14, 18, 22, 26, 28, 31, 34, 38, 42, 46}
C_AUDIO = {
    1: ("mock_BandC_mp3", "by-filename", ["0-1.mp3", "1-00000.mp3"] + split_tracks(1, 1, 25, c_pairs) + ["2-00000.mp3"] + split_tracks(2, 26, 50, c_pairs) + ["3-00000.mp3"]),
    2: ("mock2_BandC_mp3", "by-filename", ["0-1.mp3", "1-00000.mp3"] + split_tracks(1, 1, 25, c_pairs) + ["2-00000.mp3"] + split_tracks(2, 26, 50, c_pairs) + ["3-00000.mp3"]),
    3: ("mock3_BandC_mp3", "sequence", ["0-1.mp3", "1-00000.mp3"] + rng(1, 32, "1-{:02d}.mp3") + ["2-00000.mp3"] + rng(33, 64, "2-{:02d}.mp3") + ["3-00000.mp3"]),
    4: ("mock4_BandC_mp3", "sequence", seq(64)),
}
C_FILES = {1: ("ls_mock_test_BandC_t.pdf", "ls_mock_test_BandC_listen.pdf", "ls_mock_test_BandC_answer.pdf"),
           2: ("ls_mock2_test_BandC_t_2022.pdf", "ls_mock2_test_BandC_listen_2022.pdf", "ls_mock2_test_BandC_answer.pdf"),
           3: ("ls_mock3_test_BandC_t.pdf", "ls_mock3_test_BandC_listen.pdf", "ls_mock3_test_BandC_answer_fix.pdf"),
           4: ("ls_mock4_test_BandC_t.pdf", "ls_mock4_test_BandC_listen.pdf", "ls_mock4_test_BandC_answer.pdf")}
for s in range(1, 5):
    folder = f"4. TOCFL Band C/Listening/Listening Test Series {s}"
    d, kind, tr = C_AUDIO[s]
    b, sc, a = C_FILES[s]
    CATALOG.append(dict(id=f"c-l{s}", band="c", skill="listening", series=s, title=f"Band C Listening · Series {s}",
                        folder=folder, booklet=b, script=sc, answer=a, questions=50,
                        audio=dict(dir=folder + "/" + d, kind=kind, tracks=tr)))
for s in range(1, 5):
    CATALOG.append(dict(id=f"c-r{s}", band="c", skill="reading", series=s, title=f"Band C Reading · Series {s}",
                        folder="4. TOCFL Band C/Reading", booklet=f"{s}. TOCFL Reading Band C.pdf",
                        answer=f"{s}. TOCFL Reading Answer Band C.pdf", questions=50))
