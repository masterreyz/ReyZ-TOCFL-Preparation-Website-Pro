LESSON_ID = "a1-te-l10"
TITLE = "臺灣的水果很好吃 The Fruit in Taiwan Tastes Really Good"
STATUS = "complete"
DETAIL = ("Materi ini ditulis ulang secara orisinal untuk situs ini berdasarkan topik, daftar kosakata, dan pola tata bahasa "
          "buku (hlm. PDF 228–248): penjelasan, contoh kalimat, dialog latihan, soal, dan catatan budaya memakai kata-kata sendiri. "
          "Dialog, latihan bergambar, dan foto asli ada di buku; audio trek asli tetap ditautkan.")

# ---- objectives ----
H("h-obj", "Learning Objectives", "學習目標", pages=[228])
T("obj",
  "Topic: 人或物件外貌 The Appearance of People and Things",
  "• Learning to give simple descriptions of someone’s appearance.",
  "• Learning to describe the color, smell, and taste of food.",
  "• Learning to briefly explain and give reasons.",
  "• Learning to describe tentative activities and changeable states.")

# ---- Dialogue I ----
H("h-d1", "Dialogue I", "對話一", pages=[229])
T("d1-audio",
  "Practice dialogue written for this site with the vocabulary of Dialogue I. "
  "The book’s own Dialogue I is on book p. 202 (PDF p. 229); its recording is track 10-01.",
  track="10-01")
D("d1", None, [
  ("哥哥", "這種黃色的水果，你吃吃看，是臺灣的芒果。", "Zhè zhǒng huángsè de shuǐguǒ, nǐ chīchīkàn, shì Táiwān de mángguǒ."),
  ("妹妹", "好，給我一塊。[taking a bite] 嗯，香香的、甜甜的，真好吃！", "Hǎo, gěi wǒ yí kuài. Ń, xiāngxiāng de, tiántián de, zhēn hǎochī!"),
  ("哥哥", "那這個紅色的呢？妳說的是不是西瓜？", "Nà zhè ge hóngsè de ne? Nǐ shuō de shì bú shì xīguā?"),
  ("妹妹", "對對對！以前我不太喜歡吃西瓜，現在很喜歡了。", "Duì duì duì! Yǐqián wǒ bú tài xǐhuān chī xīguā, xiànzài hěn xǐhuān le."),
  ("哥哥", "臺灣有很多好吃的水果，妳可以每一種都吃吃看。", "Táiwān yǒu hěn duō hǎochī de shuǐguǒ, nǐ kěyǐ měi yì zhǒng dōu chīchīkàn."),
  ("妹妹", "聽說泰國的水果也很好吃，要是有機會，我也想吃吃看。", "Tīngshuō Tàiguó de shuǐguǒ yě hěn hǎochī, yàoshì yǒu jīhuì, wǒ yě xiǎng chīchīkàn."),
  ("哥哥", "沒問題，妳來泰國找我，我一定請妳吃。", "Méi wèntí, nǐ lái Tàiguó zhǎo wǒ, wǒ yídìng qǐng nǐ chī."),
], [
  ("Older brother", "Try this yellow fruit — it’s a Taiwanese mango."),
  ("Younger sister", "OK, give me a piece. [taking a bite] Mmm, it’s fragrant and sweet, really good!"),
  ("Older brother", "And that red one? Is it the watermelon you meant?"),
  ("Younger sister", "Yes, yes! I didn’t used to like watermelon much, but now I like it a lot."),
  ("Older brother", "Taiwan has so much good fruit — you could try a bit of every kind."),
  ("Younger sister", "I’ve heard Thai fruit is good too. If I get the chance, I’d like to try it."),
  ("Older brother", "No problem — come find me in Thailand, and I’ll treat you for sure."),
])

H("h-v1", "Vocabulary I", "生詞一", pages=[231])
V("v1-vocab", "Vocabulary", [
  ("水果", "shuǐguǒ", "N", "fruit"),
  ("黃色", "huángsè", "N", "yellow"),
  ("芒果", "mángguǒ", "N", "mango"),
  ("給", "gěi", "V", "to give"),
  ("塊", "kuài", "M", "measure word for pieces of food (e.g., meat, cake)"),
  ("香", "xiāng", "Vs", "fragrant"),
  ("甜", "tián", "Vs", "sweet (taste)"),
  ("紅色", "hóngsè", "N", "red"),
  ("西瓜", "xīguā", "N", "watermelon"),
  ("吧", "ba", "Ptc", "sentence-final particle for guessing"),
  ("對", "duì", "Vs", "correct, right"),
  ("以前", "yǐqián", "N", "before"),
  ("機會", "jīhuì", "N", "opportunity"),
  ("請", "qǐng", "V", "to treat sb to sth"),
], track="10-02", pages=[231])
V("v1-phrases", "Phrases", [("吃吃看", "chīchīkàn", "", "to have a taste, try it, taste it")], start=15, pages=[231])

# ---- Dialogue II ----
H("h-d2", "Dialogue II", "對話二", pages=[232])
T("d2-audio",
  "Practice dialogue written for this site with the vocabulary of Dialogue II. "
  "The book’s own Dialogue II is on book p. 205 (PDF p. 232); its recording is track 10-03.",
  track="10-03")
D("d2", None, [
  ("老師", "你上個星期去臺南玩，拍了很多照片吧？", "Nǐ shàng ge xīngqí qù Táinán wán, pāi le hěn duō zhàopiàn ba?"),
  ("學生", "對啊，你看，這些都是我拍的。我們笑得很開心！", "Duì a, nǐ kàn, zhèxiē dōu shì wǒ pāi de. Wǒmen xiào de hěn kāixīn!"),
  ("老師", "穿藍色衣服的這個是誰？", "Chuān lánsè yīfú de zhè ge shì shéi?"),
  ("學生", "是我同學。穿黑色衣服的是民宿老闆。", "Shì wǒ tóngxué. Chuān hēisè yīfú de shì mínsù lǎobǎn."),
  ("老師", "矮的跟高的呢？", "Ǎi de gēn gāo de ne?"),
  ("學生", "矮的是老闆的太太，高的是他們的女兒。", "Ǎi de shì lǎobǎn de tàitai, gāo de shì tāmen de nǚ’ér."),
  ("老師", "你們住的民宿怎麼樣？", "Nǐmen zhù de mínsù zěnmeyàng?"),
  ("學生", "很乾淨，從窗戶往外看，是綠色的山。", "Hěn gānjìng, cóng chuānghù wǎng wài kàn, shì lǜsè de shān."),
  ("老師", "貴不貴？", "Guì bú guì?"),
  ("學生", "因為現在去的人比較少，所以不太貴，下次我還想去住。", "Yīnwèi xiànzài qù de rén bǐjiào shǎo, suǒyǐ bú tài guì, xià cì wǒ hái xiǎng qù zhù."),
], [
  ("Teacher", "You went to Tainan last week — took a lot of pictures, I bet?"),
  ("Student", "Yes! Look, these are all ones I took. We were all smiling so happily!"),
  ("Teacher", "Who’s this one wearing blue?"),
  ("Student", "That’s my classmate. The one in black is the B&B owner."),
  ("Teacher", "What about the short one and the tall one?"),
  ("Student", "The short one is the owner’s wife, the tall one is their daughter."),
  ("Teacher", "How was the place you stayed?"),
  ("Student", "Very clean — looking out the window, you’d see green mountains."),
  ("Teacher", "Was it expensive?"),
  ("Student", "Because fewer people go there now, it wasn’t too expensive. I’d like to stay there again next time."),
])

H("h-v2", "Vocabulary II", "生詞二", pages=[234])
V("v2-vocab", "Vocabulary", [
  ("拍", "pāi", "V", "to take (pictures)"),
  ("笑", "xiào", "V", "to laugh, to smile"),
  ("開心", "kāixīn", "Vs", "happy"),
  ("穿", "chuān", "V", "to wear, to put on"),
  ("衣服", "yīfú", "N", "clothes"),
  ("旅館", "lǚguǎn", "N", "hotel"),
  ("太太", "tàitai", "N", "wife"),
  ("男 + noun", "nán", "N", "boy-, male-"),
  ("矮", "ǎi", "Vs", "short (height)"),
  ("高", "gāo", "Vs", "tall"),
  ("弟弟", "dìdi", "N", "younger brother"),
  ("乾淨", "gānjìng", "Vs", "clean"),
  ("窗戶", "chuānghù", "N", "window"),
  ("往", "wǎng", "Prep", "toward, to"),
  ("藍色", "lánsè", "N", "blue"),
  ("因為", "yīnwèi", "Conj", "because"),
  ("住", "zhù", "V", "to stay"),
], track="10-04", pages=[234])
V("v2-phrases", "Phrases", [
  ("上個月", "shàng ge yuè", "", "last month"),
  ("這些", "zhèxiē", "", "these"),
], start=18, pages=[234])

# ---- Grammar ----
H("h-gr", "Grammar", "文法", pages=[235])

# I. VV看
H("g1", "I. VV看 kàn: to try and see", level=3, pages=[235])
T("g1-f",
  "Use: This pattern reduplicates a mono-syllabic action verb and ends with the cognitive verb 看. It suggests “try (verb) and see”, and because of 看, the sentence carries a highly tentative tone. Basic mono-syllabic action verbs work in this pattern, e.g. 吃, 喝, 打, 寫, 穿, 學, 做, 聽, 唱, 逛, 住.",
  "This pattern is closely related to the plain reduplication introduced in Lesson 6 (這杯咖啡很香，你喝喝看 ≈ 你喝喝). They are usually interchangeable, except when the sentence is not a request to try something (我週末常看看書、喝喝咖啡 — 看 cannot be added), and VV看 generally cannot take an object (you cannot say ＊喝喝看咖啡, though plain VV can: 喝喝咖啡).")
EX("g1-ex", [
  ("這塊芒果很香，你吃吃看。", "Zhè kuài mángguǒ hěn xiāng, nǐ chīchīkàn.", "This piece of mango is fragrant — try it."),
  ("聽說這家店的西瓜很甜，我想買買看。", "Tīngshuō zhè jiā diàn de xīguā hěn tián, wǒ xiǎng mǎimǎikàn.", "I’ve heard the watermelon at this shop is sweet — I’d like to buy some and try it."),
  ("這件藍色的衣服不錯，你穿穿看。", "Zhè jiàn lánsè de yīfú búcuò, nǐ chuānchuānkàn.", "This blue shirt looks nice — try it on."),
  ("那家旅館聽說很乾淨，我們去住住看。", "Nà jiā lǚguǎn tīngshuō hěn gānjìng, wǒmen qù zhùzhùkàn.", "I’ve heard that hotel is clean — let’s stay there and see."),
])
X("g1-x", "Fill in each blank with a VV看 form of a suitable verb.", [
  "這杯咖啡很香，你＿＿＿＿＿＿。",
  "這種水果我沒吃過，我想＿＿＿＿＿＿。",
  "這首歌很好聽，你＿＿＿＿＿＿。",
  "這條路我不認識，我們＿＿＿＿＿＿，應該可以找到。",
])

# II. Intensification with Reduplicated State Verbs
H("g2", "II. Intensification with Reduplicated State Verbs", level=3, pages=[236, 237])
T("g2-f",
  "Use: Reduplicating a state verb intensifies the statement, somewhat like 很 + state verb, but it expresses the speaker’s subjective feeling rather than an objective, factual observation.",
  "No degree adverb can appear with reduplication (not ＊這杯茶很香香的). A 的 follows the reduplicated state verb — 這杯茶香香的, not ＊這杯茶香香. When two state verbs appear in sequence, the first 的 can be dropped: 那種水果香香甜甜的.",
  "Not every state verb can be reduplicated. 香、甜、高、熱、大、美、遠、辣、矮 can; 多、貴、近、忙、新、少 cannot.",
  "Because reduplication is subjective, it tends to appear when describing or praising something, not in a plain factual statement — when ordering, say 買一杯熱咖啡, not ＊買一杯熱熱的咖啡.")
EX("g2-ex", [
  ("這塊芒果香香甜甜的，真好吃。", "Zhè kuài mángguǒ xiāngxiāng tiántián de, zhēn hǎochī.", "This piece of mango is really fragrant and sweet — so good."),
  ("熱熱的茶，喝起來很舒服。", "Rèrè de chá, hē qǐlái hěn shūfú.", "Hot tea feels really nice to drink."),
  ("她們笑得開心開心的，看起來很幸福。", "Tāmen xiào de kāixīn kāixīn de, kàn qǐlái hěn xìngfú.", "They were smiling so happily — they looked really content."),
])
X("g2-x", "Describe each item using a reduplicated state verb.", [
  "那位先生…（高）→ ＿＿＿＿＿＿。",
  "這杯茶…（甜）→ ＿＿＿＿＿＿。",
  "那碗湯…（熱）→ ＿＿＿＿＿＿。",
  "他們家…（大）→ ＿＿＿＿＿＿。",
])

# III. Clause as Modifiers of Nouns
H("g3", "III. Clause as Modifiers of Nouns", level=3, pages=[238, 239])
T("g3-f",
  "Use: Clauses, like all modifiers in Chinese, precede the noun they modify, with 的 directly in front of that noun. A relative clause can be affirmative or negative, and may modify a noun that is the subject, object, or any other role in the clause.")
EX("g3-ex", [
  ("你說的水果是西瓜。", "Nǐ shuō de shuǐguǒ shì xīguā.", "The fruit you’re talking about is watermelon."),
  ("這些是我拍的照片。", "Zhèxiē shì wǒ pāi de zhàopiàn.", "These are photos that I took."),
  ("穿藍色衣服的這個人是我同學。", "Chuān lánsè yīfú de zhè ge rén shì wǒ tóngxué.", "The person wearing blue is my classmate."),
  ("現在去那家旅館的人比較少。", "Xiànzài qù nà jiā lǚguǎn de rén bǐjiào shǎo.", "Fewer people go to that hotel now."),
])
EX("g3-neg", [
  ("不喜歡吃水果的人可以試試看這種芒果。", "Bù xǐhuān chī shuǐguǒ de rén kěyǐ shìshìkàn zhè zhǒng mángguǒ.", "People who don’t usually like fruit could try this kind of mango."),
  ("不住旅館的旅客可以去住民宿。", "Bú zhù lǚguǎn de lǚkè kěyǐ qù zhù mínsù.", "Travelers who don’t stay at hotels can stay at a B&B instead."),
], title="Negation")
X("g3-x", "Combine each pair of sentences into one with a relative clause.", [
  "哥哥給我一塊芒果，那塊芒果很甜。→ ＿＿＿＿＿＿。",
  "這件衣服很漂亮。妹妹穿這件衣服。→ ＿＿＿＿＿＿。",
  "他在喝茶。我也喜歡喝那種茶。→ ＿＿＿＿＿＿。",
])

# IV. Change in Situation with Sentential 了
H("g4", "IV. Change in Situation with Sentential 了 le", level=3, pages=[240])
T("g4-f",
  "Use: The sentential 了 at the end of a sentence marks a change in situation — something has changed, resulting in a new state of affairs. It can be affirmative, negative, or a question.")
EX("g4-ex", [
  ("這種芒果貴了。", "Zhè zhǒng mángguǒ guì le.", "This kind of mango has gotten expensive."),
  ("我現在喜歡吃西瓜了。", "Wǒ xiànzài xǐhuān chī xīguā le.", "I like watermelon now. (I didn’t before.)"),
  ("去那家旅館住的人多了。", "Qù nà jiā lǚguǎn zhù de rén duō le.", "More people are staying at that hotel now."),
])
EX("g4-neg", [
  ("我不喜歡吃芒果了。", "Wǒ bù xǐhuān chī mángguǒ le.", "I don’t like mango any more."),
  ("他不想住那家旅館了。", "Tā bù xiǎng zhù nà jiā lǚguǎn le.", "He doesn’t want to stay at that hotel any more."),
], title="Negation")
EX("g4-q", [
  ("你現在喜歡吃臺灣水果了嗎？", "Nǐ xiànzài xǐhuān chī Táiwān shuǐguǒ le ma?", "Do you like Taiwanese fruit now?"),
  ("去花蓮玩的人少了嗎？", "Qù Huālián wán de rén shǎo le ma?", "Have fewer people been going to Hualien?"),
], title="Questions")
X("g4-x", "Describe each change using sentential 了.", [
  "我家現在很乾淨了。",
  "車票…（貴）→ ＿＿＿＿＿＿。",
  "這個學生…（想學中文）→ ＿＿＿＿＿＿。",
])

# V. Cause and Effect with 因為…所以…
H("g5", "V. Cause and Effect with 因為 yīnwèi …，所以 suǒyǐ …", level=3, pages=[241])
T("g5-f",
  "Use: 因為…所以… links a cause clause to its effect. The two conjunctions almost always appear as a pair, reinforcing each other, and in Chinese the cause clause always comes first, unlike English where the order is more flexible.")
EX("g5-ex", [
  ("因為現在去玩的人比較少，所以旅館不太貴。", "Yīnwèi xiànzài qù wán de rén bǐjiào shǎo, suǒyǐ lǚguǎn bú tài guì.", "Because fewer people are visiting now, the hotels aren’t too expensive."),
  ("因為這種水果很香很甜，所以很多人喜歡吃。", "Yīnwèi zhè zhǒng shuǐguǒ hěn xiāng hěn tián, suǒyǐ hěn duō rén xǐhuān chī.", "Because this fruit is fragrant and sweet, a lot of people like to eat it."),
  ("因為我以前沒吃過芒果，所以想吃吃看。", "Yīnwèi wǒ yǐqián méi chī guò mángguǒ, suǒyǐ xiǎng chīchīkàn.", "Because I’d never had mango before, I wanted to try it."),
])
X("g5-x", "Connect each pair of sentences with 因為…所以….", [
  "我喜歡吃甜的東西。我常買水果吃。→ ＿＿＿＿＿＿。",
  "那家民宿很乾淨。很多人想去住。→ ＿＿＿＿＿＿。",
  "我剛開始學中文。我的中文說得不好。→ ＿＿＿＿＿＿。",
])

# ---- Classroom activities ----
H("h-act", "Classroom Activities", "課室活動", pages=[216])
H("act1", "I. Which One Do You Prefer?", level=3)
T("act1-t",
  "Goal: Learning to give simple descriptions of someone’s appearance, and to describe the color, smell, and taste of food.",
  "Task: Pair up with a partner. For each pair of pictures below, say which one you prefer and briefly give a reason (you can use VV看, reduplicated state verbs, or 因為…所以…).",
  "1. 哪一個人比較好看？ 2. 哪一張照片比較漂亮？ 3. 你想看哪一個電影？",
  "4. 你比較想去哪一個海邊玩？ 5. 你比較想去哪一家餐廳吃飯？ 6. 你比較喜歡吃哪一種西瓜？",
  "7. 你比較喜歡喝哪一種咖啡？ 8. 你比較喜歡穿什麼衣服？ 9. 你比較想住哪一個地方？")
H("act2", "II. Then and Now", level=3, pages=[218])
T("act2-t",
  "Goal: Learning to describe changes in situation with sentential 了.",
  "Task: Ask classmates whether anything has changed for them since arriving in Taiwan, or in their home country compared to the past. Write down a classmate’s name if the answer is yes.",
  "你會做中國菜了嗎？ 你會唱中文歌了嗎？ 你會寫書法了嗎？ 你現在喜歡吃臭豆腐了嗎？",
  "在你的國家，吃的東西比以前貴了嗎？ 在你的國家，房子比以前貴了嗎？")
H("act3", "III. Your Observations on Taiwanese Society", level=3, pages=[219])
T("act3-t",
  "Goal: Learning to briefly explain and give reasons, using 因為…所以….",
  "Task: Pair up and discuss the following questions, then share your conclusions with the class.",
  "1. 為什麼很多人到臺灣來學中文？ 2. 為什麼現在學中文的人比以前多？",
  "3. 在臺灣，為什麼很多人不常在家吃飯？ 4. 在臺灣，為什麼很多人喜歡去夜市？ 5. 在臺灣，為什麼很多人騎機車？")

# ---- Culture ----
H("h-cult", "Bits of Chinese Culture", "文化", pages=[220])
H("cult1", "The Meanings of Different Colors", level=3)
T("cult1-t",
  "In Chinese culture, three colors carry especially strong meanings: red, white, and yellow.",
  "Red is an auspicious color used for happy events. At traditional Chinese weddings, the garments and decorations are red, and wedding guests give red envelopes containing money for good luck. At Chinese New Year, people hang up red scrolls and couplets, and often write the character 福 fú (blessing) on red paper; adults give children money in red envelopes.",
  "White is the opposite: where red is for joy and birth, white is traditionally for mourning. At funerals, the family’s clothing and the items used are white, and visitors paying respects may offer a white envelope to the family. With Western influence, however, brides in Taiwan now also wear white wedding gowns, and — as in the West and in Japan — white has also come to carry a sense of purity.",
  "Yellow was historically reserved for the emperor and the royal family; the emperor’s own robe was called 黃袍 huángpáo, literally “yellow gown”, and yellow was the color of the highest class. Since the end of imperial China, the meaning of yellow has shifted a great deal — today the word is also used in the term 黃色書刊 huángsè shūkān, “pornographic publications”, a meaning with no connection to its old royal associations.")

# ---- Self-assessment ----
H("h-self", "Self-Assessment Checklist", pages=[249])
add({"type": "checklist", "id": "self", "items": [
  "I can give simple descriptions of someone’s appearance.",
  "I can describe the color, smell, and taste of food.",
  "I can briefly explain and give reasons.",
  "I can describe tentative activities and changeable states.",
]})
