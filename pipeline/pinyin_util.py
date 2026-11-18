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


# ---- context rules for characters with more than one reading (polyphones) ----
VERBISH = {"v", "vg", "vd", "vn", "a", "ad", "an", "ag", "z", "ug", "zg", "d"}
ZHE_KEEP = {"顯著": "xiǎn zhù", "著名": "zhù míng", "著作": "zhù zuò", "土著": "tǔ zhù", "昭著": "zhāo zhù", "卓著": "zhuó zhù",
            "著重": "zhuó zhòng", "著手": "zhuó shǒu", "著想": "zhuó xiǎng", "執著": "zhí zhuó", "著陸": "zhuó lù", "衣著": "yī zhuó",
            "著迷": "zháo mí", "著墨": "zhuó mò", "著眼": "zhuó yǎn", "穿著打扮": "chuān zhuó dǎ bàn", "著急": "zháo jí", "著涼": "zháo liáng", "著火": "zháo huǒ", "睡著": "shuì zháo", "不著": "bù zháo",
            "找著": "zhǎo zháo", "用不著": "yòng bù zháo", "睡不著": "shuì bù zháo", "犯不著": "fàn bù zháo", "沉著": "chén zhuó"}
DE_DEI = {"總得": ["zǒng", " děi"], "還得": ["hái", " děi"], "就得": ["jiù", " děi"], "也得": ["yě", " děi"], "都得": ["dōu", " děi"]}
DE_KEEP = {"獲得", "取得", "贏得", "難得", "心得", "不得", "募得", "幸得", "記不得", "捨不得", "得到", "得以", "所得", "值得", "覺得",
           "記得", "懂得", "免得", "使得", "捨得", "認得", "曉得", "顯得", "省得", "怪不得", "恨不得", "巴不得", "不見得", "得知",
           "得獎", "得分", "得病", "得意", "得罪", "得當", "非得", "只得", "求得", "習得", "博得", "奪得", "換得", "落得", "樂得",
           "失而復得", "來得及", "來不及", "得了", "不得了", "不得不", "了不得", "舍得", "自得", "取之不盡", "得天獨厚", "一舉兩得"}
DE_DE = {"獲得", "取得", "贏得", "難得", "心得", "不得", "募得", "幸得", "得到", "得以", "所得", "得知", "得獎", "得分", "得病",
         "得意", "得罪", "得當", "求得", "習得", "博得", "奪得", "換得", "得天獨厚", "一舉兩得", "失而復得", "自得"}
WEI2_NEXT = {"目的", "背景", "手段", "媒介", "代表", "藉口", "例", "限", "本人", "真實", "人", "人母", "人妻", "優品", "主", "首",
             "準", "宜", "佳", "止", "伍", "師", "榮", "難", "最", "數", "重", "準則", "基礎", "核心", "中心", "原則", "依據", "對象",
             "前提", "宗旨", "單位", "期", "限度", "標準", "大宗", "大", "多", "少", "上", "下", "零", "例子"}
ZHONG4_NEXT = {"了", "起來", "在", "下", "馬鈴薯", "菜", "花", "樹", "田", "稻", "水稻", "果樹", "蔬菜"}
PUNCT_SET = set(PUNCT) | set("()[],.?!:;\"'-")
DEGREE = re.compile(r"^(很|太|真|更|比|越|好|這麼|那麼|怎麼|非常|十分|特別|相當|有點|不錯|不好|不夠|快|慢|多|少|久|飽|早|晚|清楚|厲害|要命|不得了|一塌糊塗|滿頭大汗|像)")


def _isnum(tok):
    return bool(re.match(r"^[0-9０-９一二三四五六七八九十百千萬兩壹貳參肆伍陸柒捌玖拾半幾多]", tok or ""))


def _fix(toks):
    """toks: list of [orig, flag, syls]; adjusts readings in place using neighbouring words."""
    for i, t in enumerate(toks):
        w, flag, syls = t
        if not syls or len(syls) != len(w):
            continue
        j = i - 1
        while j >= 0 and not toks[j][0].strip():
            j -= 1
        prev = toks[j][0] if j >= 0 else ""
        pflag = toks[j][1] if j >= 0 else ""
        nxt = toks[i + 1][0] if i + 1 < len(toks) else ""
        nflag = toks[i + 1][1] if i + 1 < len(toks) else ""
        start = i == 0 or prev in PUNCT_SET or not prev.strip()
        if w in ZHE_KEEP:
            t[2] = ZHE_KEEP[w].split(); continue
        if w in DE_DEI:
            t[2] = list(DE_DEI[w]); continue
        keep = next((k for k in ZHE_KEEP if len(k) == 2 and w.endswith(k)), None)
        if keep and len(w) > 2:
            syls[-2:] = ZHE_KEEP[keep].split(); continue
        if w == "不得了" or w == "了不得":
            t[2] = ["bù", "dé", "liǎo"] if w == "不得了" else ["liǎo", "bù", "dé"]; continue
        # 著: aspect particle after a verb → zhe
        if w.endswith("著") and len(w) > 1:
            syls[-1] = "zhe"
        elif w == "著":
            if nxt.startswith("重"):
                syls[0] = "zhuó"
            elif start and nxt.startswith(("增", "減", "提", "改", "變", "成")):
                syls[0] = "zhù"  # second half of 顯著 split by a line break
            else:
                syls[0] = "zhe"
        # 得: complement marker de / must děi / obtain dé
        if w.endswith("得") and len(w) == 2 and flag.startswith("nr"):
            t[1] = flag = "n"   # 錢得 is not a name
        if w.endswith("得") and len(w) > 1 and w not in DE_KEEP and flag not in ("nr", "ns", "nt", "nz", "nrt", "nrfg"):
            head = list(pseg.cut(_t2s.convert(w[:-1])))
            if len(head) == 1 and head[0].flag.startswith(("n", "r", "t")) and nflag.startswith("v") and not DEGREE.match(nxt):
                syls[-1] = " děi"   # 錢得放在… = money must …
            else:
                syls[-1] = " de"
        elif w in DE_DE:
            pass
        elif w == "得":
            if re.match(r"^(此病|病|獎|分|到|知|以|不到|頭籌|一技|第|冠軍|名)", nxt):
                syls[0] = "dé"
            elif DEGREE.match(nxt) and not start:
                syls[0] = "de"
            elif pflag in VERBISH - {"d"} or prev.endswith(("長", "高", "緊張", "頭疼", "痛", "疼", "多", "環保", "貼心", "稀鬆", "知道", "表演", "歌唱", "實在")) and not prev.endswith("實在"):
                syls[0] = "de"
            elif start and nxt.startswith(("無法", "這", "很", "不得", "要死", "太")):
                syls[0] = "de"   # line starts with the second half of 覺得 / 變得
            else:
                syls[0] = "děi"
        # 了 after a potential complement (V得了 / V不了) → liǎo
        if w == "了" and prev.endswith("得") and prev not in DE_KEEP:
            if nxt == "" or nxt in PUNCT_SET or nflag in ("d", "v", "uj", "x", "y", "zg"):
                syls[0] = "liǎo"
        # 著 glued to the next word by the segmenter (拿/著書) → zhe + word
        if w.startswith("著") and len(w) > 1 and w not in ZHE_KEEP and pflag in VERBISH - {"d"}:
            syls[0] = "zhe "
        # 地: adverbial particle → de (but 地 as a noun at a line start / after a noun stays dì)
        if w == "地":
            syls[0] = "dì" if (flag == "n" or start or (not nxt or nxt in PUNCT_SET) and pflag.startswith("n")) and not prev.startswith(("相反", "相對")) else "de"
        # 長 cháng (long) / zhǎng (grow)
        if w == "長":
            syls[0] = "zhǎng" if nxt.startswith(("得", "大", "高", "到", "出", "成")) else "cháng"
        # 教 as a verb → jiāo
        if w == "教":
            syls[0] = "jiāo"
        # 當 dàng (treat as / that very)
        if w == "當":
            syls[0] = "dàng" if (nxt in ("水", "次", "天", "年", "時", "作", "成", "真") or "把" in "".join(x[0] for x in toks[max(0, i - 4):i])) and nxt != "時候" else "dāng"
        # 應 yìng (answer / respond)
        if w == "應":
            syls[0] = "yìng" if nxt in ("了", "勢", "聲", "的") or (start and nxt == "的") else "yīng"
        # 種 zhòng (to plant)
        if w == "種":
            if nxt in ZHONG4_NEXT or (not nxt or nxt in PUNCT_SET) and prev not in ("哪", "這", "那", "一", "各", "某", "每", "此", "幾", "多") and not _isnum(prev) and not re.search(r"\d$", prev):
                syls[0] = "zhòng"
            else:
                syls[0] = "zhǒng"
        # 量 liáng (to measure)
        if w == "量" and (nxt.startswith("一量") or nxt.startswith("量")):
            syls[0] = "liáng"
        if w == "一量" and prev == "量":
            syls[:] = ["yi", "liáng"]
        # 重 chóng (again)
        if w == "重":
            syls[0] = "chóng" if nxt.startswith(("找", "新", "複", "來", "做", "修", "建", "考", "播", "啟")) or (prev in ("能", "要") and (not nxt or nxt in PUNCT_SET)) else "zhòng"
        # 數 shǔ (to count)
        if w == "數":
            syls[0] = "shǔ" if nxt in ("現金", "錢", "好", "一數", "數", "到", "不清", "著") or prev in ("一張", "張", "一個", "在", "來") or (not nxt and start) else "shù"
        if w == "乾":
            syls[0] = "gān"
        if w == "調":
            syls[0] = "tiáo" if nxt.startswith(("高", "低", "到", "整", "回", "大", "小", "成")) else "diào"
        if w == "假":
            syls[0] = "jià" if prev.endswith(("的", "兒", "天", "點", "請", "放", "休", "幾天", "暑", "寒")) else "jiǎ"
        if w == "還" and nxt in ("錢", "書", "給", "款", "清", "債", "回", "她", "他", "我", "你", "車"):
            syls[0] = "huán" if nxt in ("錢", "書", "給", "款", "清", "債", "回", "車") or prev in ("先生",) else syls[0]
        if w == "好" and nxt in ("學", "客", "奇", "動", "勝", "吃懶做"):
            syls[0] = "hào"
        if w == "中" and prev in ("考", "打", "猜", "選", "射", "命", "看"):
            syls[0] = "zhòng"
        # 為 wéi (be / as) vs wèi (for)
        if w == "為":
            if _isnum(nxt) or nflag in ("m", "mq", "t", "q") or nxt in WEI2_NEXT or nxt in ("：", "，") or (nxt == "" and prev in ("不", "所", "作", "有", "可", "而")) \
                    or prev in ("轉化", "減少", "增加", "變", "成", "視", "稱", "改", "分", "作", "以", "此", "列", "選", "譽", "定", "升", "降", "化"):
                syls[0] = "wéi"
            else:
                syls[0] = "wèi"


NOT_ERHUA = ("女兒", "嬰兒", "幼兒", "孤兒", "健兒", "寵兒", "胎兒", "產兒", "生兒", "血兒", "育兒", "託兒", "乳兒", "棄兒", "患兒")


def _erhua(toks):
    """Rhotic suffix 兒: 哪兒 nǎr, 一點兒 yìdiǎnr, 一會兒 yíhuìr (but 女兒 nǚ'ér, 兒子 érzi)."""
    for i, t in enumerate(toks):
        w, flag, syls = t
        if not syls or len(syls) != len(w):
            continue
        if len(w) > 1 and w.endswith("兒") and not w.endswith(NOT_ERHUA) and syls[-1] in ("ér", "er"):
            syls[-2] = syls[-2].rstrip() + "r"
            t[2] = syls[:-1]
            t[0] = w  # keep text
        elif w == "兒" and i and toks[i - 1][2] and toks[i - 1][0][-1] not in "女嬰幼孤健寵胎" and syls[0] in ("ér", "er"):
            toks[i - 1][2][-1] = toks[i - 1][2][-1] + "r"
            t[2] = []


def to_pinyin(text):
    if not text:
        return ""
    simp = _t2s.convert(text)
    if len(simp) != len(text):
        simp = text
    toks, pos = [], 0
    for w, flag in ((x.word, x.flag) for x in pseg.cut(simp)):
        orig = text[pos:pos + len(w)]
        pos += len(w)
        if orig == "○":
            toks.append([orig, "m", ["líng"]])
            continue
        if not w.strip() or all(c in PUNCT for c in orig) or re.fullmatch(r"[A-Za-z0-9.%+\-/:@ ()\[\],?!;'\"*#&=<>○]+", orig):
            toks.append([orig, flag, None])
            continue
        syls = lazy_pinyin(w, style=Style.TONE, neutral_tone_with_five=False, errors=lambda s: list(s))
        syls = _sandhi(syls, w) if len(syls) == len(w) else syls
        toks.append([orig, flag, syls])
    _fix(toks)
    _erhua(toks)
    # 一 / 不 sandhi across word boundaries (一 + next word, 不 + next word)
    for i, t in enumerate(toks[:-1]):
        nx = toks[i + 1][2]
        if t[2] and nx and t[0][-1] in "一不" and len(t[2]) == len(t[0]):
            fourth = any(c in nx[0] for c in "àèìòùǜ")
            if t[0][-1] == "不" and t[2][-1] == "bù" and fourth:
                t[2][-1] = "bú"
            elif t[0][-1] == "一" and t[2][-1] == "yī" and len(t[0]) == 1 and toks[i + 1][0][0] not in "一二三四五六七八九十百千萬零○" \
                    and (i == 0 or not re.match(r"[0-9第○零一二三四五六七八九十百千萬]", toks[i - 1][0][-1:] or "")):
                t[2][-1] = "yí" if fourth else "yì"
    out = []
    for orig, flag, syls in toks:
        if syls is None:
            if not orig.strip():
                out.append(" ")
            elif all(c in PUNCT for c in orig):
                out.append("".join(PUNCT[c] for c in orig))
            else:
                out.append(" " + orig)
            continue
        # numeral + measure word / 個 written apart: yí ge, sān ge
        if len(orig) >= 2 and orig[-1] in "個个" and syls[-1] in ("gè", "ge"):
            syls[-1] = " ge"
        if not syls:
            continue
        word = syls[0] + "".join(("'" if re.match(r"[aoeāáǎàōóǒòēéěè]", x) else "") + x for x in syls[1:])
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
