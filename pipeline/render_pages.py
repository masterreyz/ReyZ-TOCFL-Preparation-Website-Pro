"""Render every page of the study books to WebP (fallback reader for lessons not yet migrated to text).

Usage: python render_pages.py <SOURCE_ROOT> <OUT_ROOT> [dpi]
"""
import subprocess
import sys
import tempfile
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from PIL import Image

from study_catalog import BOOKS


def render_chunk(args):
    pdf, out_dir, first, last, dpi = args
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(["pdftoppm", "-r", str(dpi), "-f", str(first), "-l", str(last), "-jpeg", "-jpegopt", "quality=90",
                        str(pdf), f"{td}/p"], check=True)
        for f in sorted(Path(td).glob("p-*.jpg")):
            n = int(f.stem.split("-")[-1])
            im = Image.open(f).convert("RGB")
            im.save(Path(out_dir) / f"p{n:03d}.webp", "WEBP", quality=58, method=4)
    return last - first + 1


def main(src, out, dpi=100):
    jobs = []
    for b in BOOKS:
        pdf = Path(src) / "TOCFL Study" / b["folder"] / b["file"]
        out_dir = Path(out) / "media" / "study" / b["id"]
        out_dir.mkdir(parents=True, exist_ok=True)
        n = int(next(l for l in subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout.splitlines() if l.startswith("Pages")).split()[1])
        for a in range(1, n + 1, 20):
            jobs.append((pdf, out_dir, a, min(n, a + 19), dpi))
    done = 0
    with ProcessPoolExecutor() as ex:
        for k in ex.map(render_chunk, jobs):
            done += k
    print("rendered pages:", done)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 100)
