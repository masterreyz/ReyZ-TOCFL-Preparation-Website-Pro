"""Shared PDF helpers for the ReyZ TOCFL content pipeline.

Requires poppler-utils (pdftotext, pdftoppm) on PATH and Pillow.
"""
import re
import subprocess
from html import unescape
from pathlib import Path

LINE_RE = re.compile(r'<line xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</line>', re.S)
WORD_RE = re.compile(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</word>', re.S)
PAGE_RE = re.compile(r'<page width="([\d.]+)" height="([\d.]+)">(.*?)</page>', re.S)


def pages_lines(pdf):
    """Return list of pages: {w,h,lines:[{x0,y0,x1,y1,text,words}]} using pdftotext -bbox-layout."""
    out = subprocess.run(["pdftotext", "-bbox-layout", str(pdf), "-"], capture_output=True, text=True, check=True).stdout
    pages = []
    for pm in PAGE_RE.finditer(out):
        w, h, body = float(pm.group(1)), float(pm.group(2)), pm.group(3)
        lines = []
        for lm in LINE_RE.finditer(body):
            words = [(float(a), float(b), float(c), float(d), unescape(t)) for a, b, c, d, t in WORD_RE.findall(lm.group(5))]
            if not words:
                continue
            text = join_words(words)
            lines.append(dict(x0=float(lm.group(1)), y0=float(lm.group(2)), x1=float(lm.group(3)), y1=float(lm.group(4)), text=text, words=words))
        # merge lines that share a baseline (pdftotext splits columns into separate blocks)
        lines.sort(key=lambda l: (round(l["y0"] / 3), l["x0"]))
        pages.append(dict(w=w, h=h, lines=lines))
    return pages


def join_words(words):
    """Join words; no space between CJK characters, keep spaces for Latin text."""
    s = ""
    prev = None
    for x0, y0, x1, y1, t in words:
        if prev is not None:
            gap = x0 - prev[2]
            a, b = s[-1:] if s else "", t[:1]
            if is_cjk(a) and is_cjk(b) and gap < 6:
                pass
            elif gap > 0.5 or not (is_cjk(a) or is_cjk(b)):
                s += " "
        s += t
        prev = (x0, y0, x1, y1)
    return normalize(s)


def is_cjk(ch):
    return bool(ch) and ('　' <= ch <= '鿿' or '＀' <= ch <= '￯' or '豈' <= ch <= '﫿')


def normalize(s):
    s = s.replace('', '').replace('　', ' ')
    s = re.sub(r'[-]', '', s)  # private-use glyphs (answer-sheet bubbles)
    s = re.sub(r'\s+', ' ', s).strip()
    # unify option labels （A） -> (A)
    s = re.sub(r'[（(]\s*([A-F])\s*[）)]', r'(\1)', s)
    return s


def plain_text(pdf, layout=True):
    args = ["pdftotext"] + (["-layout"] if layout else []) + [str(pdf), "-"]
    return subprocess.run(args, capture_output=True, text=True, check=True).stdout


def render_page(pdf, page_no, out_png, dpi=150):
    """Render 1-based page to PNG."""
    out_png = Path(out_png)
    stem = out_png.with_suffix("")
    subprocess.run(["pdftoppm", "-r", str(dpi), "-f", str(page_no), "-l", str(page_no), "-png", "-singlefile", str(pdf), str(stem)], check=True)
    return out_png


def page_has_images(pdf):
    """Map page -> list of image sizes, via pdfimages -list."""
    out = subprocess.run(["pdfimages", "-list", str(pdf)], capture_output=True, text=True).stdout
    res = {}
    for ln in out.splitlines()[2:]:
        parts = ln.split()
        if len(parts) > 4 and parts[0].isdigit():
            res.setdefault(int(parts[0]), []).append((int(parts[3]), int(parts[4])))
    return res
