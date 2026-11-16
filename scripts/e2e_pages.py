"""E2E test of the GitHub Pages configuration: no original audio, Mandarin TTS fallback.
Usage: python scripts/e2e_pages.py <base_url>   (e.g. http://localhost:4173/ or the live Pages URL)
speechSynthesis is replaced by a recorder so the test can assert exactly what would be spoken.
"""
import json
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:4173/"
MOCK = """
window.__spoken = [];
const voices = [{name:'Google 國語（臺灣）',lang:'zh-TW',voiceURI:'g-tw'},{name:'Google US English',lang:'en-US',voiceURI:'en'}];
Object.defineProperty(window, 'speechSynthesis', { configurable: true, value: {
  getVoices: () => voices, cancel(){}, addEventListener(){},
  speak(u){ window.__spoken.push({text:u.text, lang:u.lang, voice:u.voice && u.voice.name}); setTimeout(() => u.onend && u.onend(), 2); } } });
window.SpeechSynthesisUtterance = function(t){ this.text = t; };
"""
res = []


def check(name, cond, detail=""):
    res.append(dict(test=name, ok=bool(cond), detail=detail))
    print(("PASS " if cond else "FAIL ") + name + (f" — {detail}" if detail else ""))


q1 = json.load(open("public/content/exercise/a-l1.json"))["questions"][0]
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome")
    ctx = b.new_context(viewport={"width": 1280, "height": 900})
    ctx.add_init_script(MOCK)
    page = ctx.new_page()
    errors, bad = [], []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.on("dialog", lambda d: d.accept())
    page.on("response", lambda r: bad.append(f"{r.status} {r.url}") if r.status >= 400 and "/media/audio/" not in r.url else None)

    page.goto(BASE + "#/")
    page.wait_for_selector("h1")
    check("home loads", page.inner_text("h1") == "ReyZ TOCFL Preparation Website")

    page.goto(BASE + "#/test/a-l1")
    page.wait_for_selector("h1")
    check("intro explains TTS", "suara sintetis" in page.inner_text("main"))

    page.goto(BASE + "#/test/a-l1/run?mode=practice")
    page.wait_for_selector(".q-pane .audio-player.tts")
    check("no original-audio player shown", page.locator(".q-pane .audio-player:not(.tts)").count() == 0)
    page.click(".q-pane .audio-player.tts .ap-btn")
    page.wait_for_timeout(800)
    spoken = page.evaluate("window.__spoken")
    text = "".join(s["text"] for s in spoken)
    check("Q1 spoken from official script", q1["transcript"].split("\n")[0][:6] in text, text[:60])
    check("uses zh-TW voice", all(s["voice"] == "Google 國語（臺灣）" for s in spoken))
    check("script text hidden during test", page.inner_text(".q-pane .tts-now") == "" if page.locator(".q-pane .tts-now").count() else True)
    page.check(".q-pane input[value='B']")
    page.click(".test-status .btn.primary")
    page.wait_for_selector(".big-score")
    page.evaluate("window.__spoken.length = 0")
    page.click("article.review .audio-player.tts .ap-btn")
    page.wait_for_timeout(500)
    check("review replays question via TTS", len(page.evaluate("window.__spoken")) > 0)

    page.goto(BASE + "#/test/b-l4/run?mode=exam&min=0")  # a test whose recordings are only numbered
    page.wait_for_selector(".audio-box .ap-btn")
    page.evaluate("window.__spoken.length = 0")
    page.click(".audio-box .ap-btn")
    page.wait_for_timeout(1500)
    sp = page.evaluate("window.__spoken.map(s => s.text)")
    check("exam mode reads whole test in order", sp[:1] and ("第1題" in sp or "第1題" in "".join(sp[:3])), str(sp[:3]))

    page.goto(BASE + "#/test/a-r1/run?mode=practice")
    page.wait_for_selector(".q-pane .crop img")
    page.wait_for_timeout(800)
    check("question crop image loads", page.evaluate("document.querySelector('.q-pane .crop img').naturalWidth") > 0)

    page.goto(BASE + "#/lesson/a1-te-l01")
    page.wait_for_selector(".dlg")
    page.evaluate("window.__spoken.length = 0")
    page.click(".dlg .tts-mini >> nth=0")
    page.wait_for_timeout(300)
    check("dialogue line speak button", page.evaluate("window.__spoken.map(s=>s.text).join('')").startswith("請問你是陳月美小姐嗎"))
    page.evaluate("window.__spoken.length = 0")
    page.click("table.vocab .tts-mini >> nth=3")
    page.wait_for_timeout(300)
    check("vocab speak button", page.evaluate("window.__spoken[0] && window.__spoken[0].text") == "你")

    page.goto(BASE + "#/lesson/a2-te-l03")
    page.wait_for_selector("figure.page img")
    page.locator("figure.page img").first.scroll_into_view_if_needed()
    page.wait_for_timeout(1200)
    check("book page image loads", page.evaluate("document.querySelector('figure.page img').naturalWidth") > 0)
    check("page lesson explains missing audio", "tidak tersedia di versi online" in page.inner_text("main"))

    page.goto(BASE + "#/settings")
    page.wait_for_selector("#voice")
    check("voice picker lists zh voices only", page.locator("#voice option").count() == 2)

    for route in ["#/study", "#/study/c2", "#/book/b1-wo", "#/exercise", "#/exercise/c", "#/search?q=茶", "#/about", "#/history", "#/mistakes", "#/bookmarks", "#/page/c1-te/40"]:
        page.goto(BASE + route)
        page.wait_for_selector("h1")
        check(f"route {route}", "Konten tidak dapat dimuat" not in page.inner_text("main"))
    page.goto(BASE + "#/test/c-l2")  # refresh-safe deep link
    page.reload()
    page.wait_for_selector("h1")
    check("deep link survives reload", "Band C Listening" in page.inner_text("h1"))
    check("no failed requests (except audio probe)", not bad, "; ".join(bad[:3]))
    check("no JS errors", not errors, "; ".join(errors[:3]))
    b.close()
Path("reports/e2e-pages-results.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))
print(f"{sum(r['ok'] for r in res)}/{len(res)} checks passed")
