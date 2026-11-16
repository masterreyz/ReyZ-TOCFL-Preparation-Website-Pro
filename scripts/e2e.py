"""End-to-end browser test (Playwright + Chrome) against `npm run preview` (http://localhost:4173).
Usage: python scripts/e2e.py [base_url]
Covers: home, listening attempt with audio + refresh persistence + submit, full reading attempt graded
against the official key, migrated lesson with audio, search (hanzi + toneless pinyin), mobile overflow.
"""
import json
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:4173/ReyZ-TOCFL-Preparation-Website-Pro/"
OUT = Path("reports/screens"); OUT.mkdir(parents=True, exist_ok=True)
results = []


def check(name, cond, detail=""):
    results.append(dict(test=name, ok=bool(cond), detail=detail))
    print(("PASS " if cond else "FAIL ") + name + (f" — {detail}" if detail else ""))


with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--autoplay-policy=no-user-gesture-required"])
    page = b.new_page(viewport={"width": 1280, "height": 900})
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.on("dialog", lambda d: d.accept())

    page.goto(BASE + "#/")
    page.wait_for_selector("h1")
    check("home title", page.inner_text("h1") == "ReyZ TOCFL Preparation Website")
    check("creator signature", "Created by Reynard Agahari" in page.inner_text("body"))
    links = page.eval_on_selector_all(".site-footer .social a", "els => els.map(e => e.href)")
    check("social links", links == ["https://www.threads.com/@reynard_agahari", "https://www.instagram.com/reynard_agahari/", "https://www.tiktok.com/@reynardagahari"], str(links))
    page.screenshot(path=str(OUT / "home.png"), full_page=False)

    # ---- listening attempt (practice) with per-question audio
    page.goto(BASE + "#/test/a-l1/run?mode=practice")
    page.wait_for_selector(".q-pane h2")
    check("listening Q1 picture crop visible", page.locator(".q-pane .crop img").count() >= 1)
    page.click(".q-pane .audio-player .ap-btn")
    page.wait_for_timeout(2500)
    t = page.evaluate("() => { const a=[...document.querySelectorAll('audio')]; return 0 }")
    cur = page.inner_text(".q-pane .ap-time")
    check("per-question audio plays", not cur.startswith("0:00 /") or "0:0" not in cur, cur)
    status = page.inner_text(".q-pane .ap-status") if page.locator(".q-pane .ap-status").count() else ""
    check("no audio error", "tidak dapat dimuat" not in status, status)
    page.screenshot(path=str(OUT / "listening-q1.png"))
    page.click(".q-pane .opt:nth-child(3)")  # choose B (legend is child 1)
    page.click("text=Berikutnya →")
    page.click(".q-pane .opt:nth-child(2)")  # A
    page.reload()
    page.wait_for_selector(".qnav .qn")
    done = page.locator(".qnav .qn.done").count()
    check("answers persist after refresh", done == 2, f"{done} answered")
    page.click(".test-status .btn.primary")  # submit (dialog auto-accepted)
    page.wait_for_selector(".big-score")
    txt = page.inner_text(".score-cards")
    key = json.load(open("content/exercise/a-l1.json"))
    exp = sum(1 for g, q in zip(["B", "A"], key["questions"][:2]) if q["answer"] == g)
    check("listening result score", f"{exp} dari 50" in txt, txt.replace("\n", " "))
    check("transcript shown after submit", page.locator(".transcript").count() > 0)
    page.screenshot(path=str(OUT / "listening-result.png"))

    # ---- full reading attempt answered with the official key -> 100%
    d = json.load(open("content/exercise/a-r1.json"))
    page.goto(BASE + "#/test/a-r1/run?mode=exam&min=0")
    page.wait_for_selector(".q-pane h2")
    for q in d["questions"]:
        page.click(f".qnav .qn:nth-child({q['n']})")
        page.check(f".q-pane input[value='{q['answer']}']")
    page.screenshot(path=str(OUT / "reading-q50.png"))
    page.click(".test-status .btn.primary")
    page.wait_for_selector(".big-score")
    check("reading full attempt = 100%", "100%" in page.inner_text(".big-score"), page.inner_text(".big-score").replace("\n", " "))
    page.goto(BASE + "#/test/a-r1/run?mode=practice")
    page.wait_for_selector(".q-pane h2")
    page.click(".test-status .btn.primary")
    page.wait_for_selector(".big-score")
    check("retry keeps previous attempt", page.evaluate("() => JSON.parse(localStorage.getItem('reyz-tocfl-v1')).attempts.filter(a=>a.testId==='a-r1').length") == 2)
    page.goto(BASE + "#/mistakes")
    page.wait_for_selector("h1")
    check("mistake review lists tests", page.locator("section.card").count() >= 1)

    # ---- migrated lesson + audio
    page.goto(BASE + "#/lesson/a1-te-l01")
    page.wait_for_selector(".dlg")
    check("lesson dialogue rendered", "請問你是陳月美小姐嗎？" in page.inner_text(".dlg"))
    check("vocab table rendered", page.locator("table.vocab tbody tr").count() >= 40)
    page.click(".block.dialogue .ap-btn")
    page.wait_for_timeout(2000)
    st = page.inner_text(".block.dialogue .ap-status")
    check("lesson audio plays", "tidak dapat dimuat" not in st, st)
    page.click("text=Tandai selesai")
    page.screenshot(path=str(OUT / "lesson.png"))
    page.goto(BASE + "#/lesson/a2-te-l03")
    page.wait_for_selector("figure.page img")
    check("page-image fallback lesson", page.locator("figure.page img").count() > 10)

    # ---- search
    page.goto(BASE + "#/search?q=" + "烏龍茶")
    page.wait_for_selector("h1")
    check("search hanzi", page.locator(".search-results li").count() >= 1)
    page.goto(BASE + "#/search?q=wulong")
    page.wait_for_selector("h1")
    check("search toneless pinyin", page.locator(".search-results li").count() >= 1)

    # ---- mobile layout
    m = b.new_page(viewport={"width": 375, "height": 800}, is_mobile=True)
    for route in ["#/", "#/test/b-r1/run?mode=practice", "#/lesson/a1-te-l01", "#/result/x"]:
        m.goto(BASE + route)
        m.wait_for_selector("h1")
        m.wait_for_timeout(400)
        ow = m.evaluate("() => document.documentElement.scrollWidth - window.innerWidth")
        check(f"mobile no horizontal overflow {route}", ow <= 1, f"{ow}px")
    m.goto(BASE + "#/test/b-r1/run?mode=practice")
    m.wait_for_selector(".q-pane")
    m.screenshot(path=str(OUT / "mobile-reading.png"))
    check("no JS errors", not errors, "; ".join(errors[:3]))
    b.close()

Path("reports/e2e-results.json").write_text(json.dumps(results, ensure_ascii=False, indent=1))
print(f"{sum(r['ok'] for r in results)}/{len(results)} checks passed")
