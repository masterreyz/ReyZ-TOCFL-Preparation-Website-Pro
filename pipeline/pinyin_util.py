"""Hanyu Pinyin (tone marks, word-spaced) for Traditional Chinese text.

Words are segmented on a Simplified copy (jieba's dictionary is Simplified); the
conversion is character-for-character, so word boundaries map back exactly.
"""
import re
import warnings

warnings.filterwarnings("ignore")
import jieba  # noqa: E402
import jieba.posseg as pseg  # noqa: E402
from opencc import OpenCC  # noqa: E402
from pypinyin import Style, lazy_pinyin, load_phrases_dict  # noqa: E402

jieba.setLogLevel(60)
_t2s = OpenCC("t2s")
PUNCT = {"，": ",", "。": ".", "？": "?", "！": "!", "：": ":", "；": ";", "、": ",", "「": "“", "」": "”", "『": "‘", "』": "’",
         "（": "(", "）": ")", "《": "«", "》": "»", "…": "…", "—": "—", "～": "~", "．": ".", "　": " "}
# common readings pypinyin gets wrong for these texts (neutral tones / Taiwan-standard choices kept to Hanyu Pinyin)
load_phrases_dict({"这个": [["zhè"], ["ge"]], "那个": [["nà"], ["ge"]], "哪个": [["nǎ"], ["ge"]], "一个": [["yí"], ["ge"]],
                   "几个": [["jǐ"], ["ge"]], "两个": [["liǎng"], ["ge"]], "什么": [["shén"], ["me"]], "怎么": [["zěn"], ["me"]],
                   "东西": [["dōng"], ["xi"]], "朋友": [["péng"], ["yǒu"]], "觉得": [["jué"], ["de"]], "知道": [["zhī"], ["dào"]],
                   "地方": [["dì"], ["fāng"]], "时候": [["shí"], ["hòu"]], "关系": [["guān"], ["xì"]], "休息": [["xiū"], ["xí"]],
                   "先生": [["xiān"], ["sheng"]], "太太": [["tài"], ["tai"]], "名字": [["míng"], ["zi"]], "妹妹": [["mèi"], ["mei"]],
                   "爸爸": [["bà"], ["ba"]], "妈妈": [["mā"], ["ma"]], "哥哥": [["gē"], ["ge"]], "姐姐": [["jiě"], ["jie"]],
                   "弟弟": [["dì"], ["di"]], "儿子": [["ér"], ["zi"]], "孩子": [["hái"], ["zi"]], "房子": [["fáng"], ["zi"]],
                   "鞋子": [["xié"], ["zi"]], "桌子": [["zhuō"], ["zi"]], "包子": [["bāo"], ["zi"]], "喜欢": [["xǐ"], ["huān"]],
                   "漂亮": [["piào"], ["liang"]], "便宜": [["pián"], ["yi"]], "认识": [["rèn"], ["shi"]], "事情": [["shì"], ["qing"]]})


def _sandhi(syls, chars):
    """一 / 不 tone changes as printed in teaching materials."""
    out = list(syls)
    for i, ch in enumerate(chars):
        if i + 1 >= len(chars) or ch not in "一不":
            continue
        nxt = out[i + 1]
        fourth = any(c in nxt for c in "àèìòùǜ")
        if ch == "不" and out[i] == "bù" and fourth:
            out[i] = "bú"
        elif ch == "一" and out[i] == "yī" and chars[i + 1] not in "一二三四五六七八九十百千萬零":
            out[i] = "yí" if fourth else "yì"
    return out


def to_pinyin(text):
    if not text:
        return ""
    simp = _t2s.convert(text)
    if len(simp) != len(text):
        simp = text
    out, pos = [], 0
    for w, flag in ((x.word, x.flag) for x in pseg.cut(simp)):
        orig = text[pos:pos + len(w)]
        pos += len(w)
        if not w.strip():
            out.append(" ")
            continue
        if all(c in PUNCT for c in orig):
            out.append("".join(PUNCT[c] for c in orig))
            continue
        if re.fullmatch(r"[A-Za-z0-9.%+\-/:@ ]+", orig):
            out.append(" " + orig)
            continue
        syls = lazy_pinyin(w, style=Style.TONE, neutral_tone_with_five=False, errors=lambda s: list(s))
        syls = _sandhi(syls, w) if len(syls) == len(w) else syls
        # numeral + measure word / 個 written apart: yí ge, sān ge
        if len(w) >= 2 and w[-1] in "个" and syls[-1] in ("gè", "ge"):
            syls[-1] = " ge"
        word = "".join(syls)
        if flag in ("nr", "ns", "nt", "nz", "nrt", "nrfg") and word:
            word = word[0].upper() + word[1:]
        out.append(" " + word)
    s = "".join(out)
    s = re.sub(r"\s+([,.?!:;”’)»~])", r"\1", s)
    s = re.sub(r"([“‘(«])\s+", r"\1", s)
    s = re.sub(r"(?<=[^\s“‘(«])([“‘(«])", r" \1", s)
    s = re.sub(r"\s{2,}", " ", s).strip()
    # capitalise the first letter of each sentence, as in pinyin teaching texts
    s = re.sub(r"(^|[.?!:]\s+|[“‘(«])([a-zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜü])", lambda m: m.group(1) + m.group(2).upper(), s)
    return s


if __name__ == "__main__":
    import sys
    print(to_pinyin(sys.argv[1]))
