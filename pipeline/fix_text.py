"""Text corrections for the mock tests.

1. Glyph errors from the booklet fonts (e.g. 頇 is extracted where 須 is printed); see GLYPHS.
2. Novice mock-test text that the booklet's printed pinyin/zhuyin garbles during extraction.

The Novice booklet prints pinyin and zhuyin around every character, so automatic extraction
duplicates or shifts text. These corrections were checked against the booklet pages and the
official listening script. Run after parse_mock.py:  python fix_text.py <OUT_DIR>
"""
import json
import sys
from pathlib import Path

# Big5 font glyphs extracted as the wrong character (checked against the printed pages)
GLYPHS = [("頇", "須"), ("帄", "平"), ("帅稚", "幼稚"), ("年付", "年代"), ("付替", "代替"), ("現付人", "現代人"),
          ("一付一付", "一代一代"), ("取付", "取代"), ("命仙", "命令"), ("下仙", "下令"), ("仙人驚", "令人驚")]

R_STEMS = {1: "妹妹的書", 2: "五百二十八元", 3: "他在開車", 4: "九點四十分", 5: "他們在看電影", 6: "這是他的名字",
           7: "她在練習寫字", 8: "我帶了衣服", 9: "漂亮的房子", 10: "她覺得很熱", 11: "他在餐廳吃東西",
           12: "這裡有一些蘋果", 13: "爸爸想買手機", 14: "她和朋友一起運動", 15: "我一個星期上兩次英文課"}
R_OPTS = {16: ["這個東西六百零五元。", "這個東西六百五十元。", "這個東西八百五十元。"],
          17: ["他在洗東西。", "他在找東西。", "他在買東西。"],
          18: ["她覺得考試很難。", "她覺得考試很有趣。", "她覺得考試很容易。"],
          19: ["這裡不可以看書。", "這裡不可以說話。", "這裡不可以喝東西。"],
          20: ["爸爸沒穿鞋子。", "媽媽沒穿鞋子。", "弟弟沒穿鞋子。"],
          21: ["這個人下午吃飯。", "這個人早上打電話。", "這個人中午在學習。"],
          22: ["學生給老師一張票。", "老師在聽學生唱歌。", "學生在問老師問題。"],
          23: ["醫院在餐廳和圖書館的中間。", "圖書館在餐廳和醫院的中間。", "餐廳在圖書館和醫院的中間。"],
          24: ["他們都一樣大。", "他們都是學生。", "他們都會英文。"],
          25: ["酒比茶便宜。", "咖啡比酒便宜。", "茶比咖啡便宜。"]}
L_PART3 = {
    21: ("美美今年要去哪裡玩？", "男：美美，你今年去日本玩嗎？\n女：不，我今年去台灣玩。\n提問：美美今年去哪裡玩？\n(A) 日本\n(B) 台灣\n(C) 美國"),
    22: ("明天他們要一起做什麼？", "男：小美，明天我們一起去運動吧？\n女：好啊，我很喜歡運動。\n提問：明天他們要一起做什麼？\n(A) 運動\n(B) 學習\n(C) 吃飯"),
    23: ("大明在做什麼？", "女：大明，你在做什麼？\n男：我在找我的書。\n提問：大明在做什麼？\n(A) 找書\n(B) 買書\n(C) 看書"),
    24: ("林太太的兒子今年幾歲？", "男：林太太，你兒子今年十四歲嗎？\n女：不，他今年十七歲了。\n提問：林太太的兒子今年幾歲？\n(A) 十一歲\n(B) 十四歲\n(C) 十七歲"),
    25: ("小張星期天要做什麼？", "女：小張，星期天跟我們去看電影吧？\n男：我不能去，我星期天要參加考試。\n提問：小張星期天要做什麼？\n(A) 唱歌\n(B) 看電影\n(C) 參加考試"),
}


def main(out):
    d = Path(out) / "content" / "exercise"
    f = d / "novice-r1.json"
    t = json.loads(f.read_text(encoding="utf-8"))
    for q in t["questions"]:
        if q["n"] in R_STEMS:
            q["stem"] = R_STEMS[q["n"]]
        if q["n"] in R_OPTS:
            q["stem"] = ""
            q["options"] = [dict(label=L, text=x) for L, x in zip("ABC", R_OPTS[q["n"]])]
    f.write_text(json.dumps(t, ensure_ascii=False, indent=1), encoding="utf-8")
    f = d / "novice-l1.json"
    t = json.loads(f.read_text(encoding="utf-8"))
    for q in t["questions"]:
        if q["n"] in L_PART3:
            q["stem"], q["transcript"] = L_PART3[q["n"]]
            q["context"] = ""
            for k in ("transcriptIntro", "transcriptLead"):
                q.pop(k, None)
    f.write_text(json.dumps(t, ensure_ascii=False, indent=1), encoding="utf-8")
    for f in d.glob("*-[rl][0-9].json"):
        txt = f.read_text(encoding="utf-8")
        new = txt
        for a, b in GLYPHS:
            new = new.replace(a, b)
        if new != txt:
            f.write_text(new, encoding="utf-8")
    print("text corrections applied")


if __name__ == "__main__":
    main(sys.argv[1])
