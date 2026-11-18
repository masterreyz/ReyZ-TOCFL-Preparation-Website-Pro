LESSON_ID = "a1-te-l15"
TITLE = "我很不舒服 I Don't Feel Well"
STATUS = "complete"
DETAIL = ("Materi ini ditulis ulang secara orisinal untuk situs ini berdasarkan topik, daftar kosakata, dan pola tata bahasa "
          "buku (hlm. buku 324–350): penjelasan, contoh kalimat, dialog latihan, soal, dan catatan budaya memakai kata-kata sendiri. "
          "Dialog, latihan bergambar, dan foto asli ada di buku; audio trek asli tetap ditautkan.")

# ---- objectives ----
H("h-obj", "Learning Objectives", "學習目標", pages=[324])
T("obj",
  "Topic: 健康 Health",
  "• Learning to ask someone how they are feeling.",
  "• Learning to describe symptoms in simple terms.",
  "• Learning to make suggestions to somebody who is sick.",
  "• Learning to politely accept or reject suggestions.")

# ---- Dialogue I ----
H("h-d1", "Dialogue I", "對話一", pages=[324])
T("d1-audio",
  "Practice dialogue written for this site with the vocabulary of Dialogue I. "
  "The book’s own Dialogue I is on book p. 324; its recording is track 15-01.",
  track="15-01")
D("d1", None, [
  ("醫生", "王小姐，妳怎麼了？", "Wáng Xiǎojiě, nǐ zěnme le?"),
  ("王小姐", "我這兩天一直流鼻水，頭很痛，胃口也很差，什麼都不想吃。", "Wǒ zhè liǎng tiān yìzhí liú bíshuǐ, tóu hěn tòng, wèikǒu yě hěn chā, shénme dōu bù xiǎng chī."),
  ("醫生", "我看看妳的喉嚨。喉嚨有一點發炎，妳也有一點發燒，應該是感冒了。", "Wǒ kànkàn nǐ de hóulóng. Hóulóng yǒu yìdiǎn fāyán, nǐ yě yǒu yìdiǎn fāshāo, yīnggāi shì gǎnmào le."),
  ("王小姐", "請問我生病了，需要吃藥嗎？", "Qǐngwèn wǒ shēngbìng le, xūyào chī yào ma?"),
  ("醫生", "需要，妳先去藥局拿藥。", "Xūyào, nǐ xiān qù yàojú ná yào."),
  ("王小姐", "好的。請問我的病什麼時候會好？", "Hǎode. Qǐngwèn wǒ de bìng shénme shíhòu huì hǎo?"),
  ("醫生", "把藥吃了，多喝水，多休息，早一點睡覺，很快就會好。", "Bǎ yào chīle, duō hē shuǐ, duō xiūxí, zǎo yìdiǎn shuìjiào, hěn kuài jiù huì hǎo."),
  ("王小姐", "謝謝您。", "Xièxie nín."),
], [
  ("Doctor", "Miss Wang, what's wrong?"),
  ("Miss Wang", "I've had a runny nose nonstop for the past two days, my head really hurts, and my appetite is poor too — I don't feel like eating anything."),
  ("Doctor", "Let me look at your throat. Your throat is a bit inflamed, and you have a slight fever too — you've probably caught a cold."),
  ("Miss Wang", "Excuse me, since I'm sick, do I need to take medicine?"),
  ("Doctor", "Yes, go to the pharmacy first to get your medicine."),
  ("Miss Wang", "Okay. Excuse me, when will I get better?"),
  ("Doctor", "Take your medicine, drink plenty of water, get plenty of rest, go to bed a bit earlier, and you'll be better soon."),
  ("Miss Wang", "Thank you."),
])

H("h-v1", "Vocabulary I", "生詞一", pages=[326])
V("v1-vocab", "Vocabulary", [
  ("醫生", "yīshēng", "N", "doctor"),
  ("一直", "yìzhí", "Adv", "continuously, all the way"),
  ("流", "liú", "V", "to flow"),
  ("鼻水", "bíshuǐ", "N", "snot, nasal mucus, a running nose"),
  ("頭", "tóu", "N", "head"),
  ("痛", "tòng", "Vs", "painful"),
  ("胃口", "wèikǒu", "N", "appetite"),
  ("差", "chā", "Vs", "poor, bad"),
  ("喉嚨", "hóulóng", "N", "throat"),
  ("發炎", "fāyán", "Vp-sep", "to be inflamed"),
  ("生病", "shēngbìng", "Vp-sep", "to fall ill"),
  ("發燒", "fāshāo", "Vp-sep", "to have a fever"),
  ("感冒", "gǎnmào", "Vp", "to catch/have a cold"),
  ("藥", "yào", "N", "medicine"),
  ("藥局", "yàojú", "N", "pharmacy, drug store"),
  ("拿", "ná", "V", "to get"),
  ("把", "bǎ", "Ptc", "disposal marker"),
  ("水", "shuǐ", "N", "water"),
  ("休息", "xiūxí", "Vi", "to take a rest"),
  ("睡覺", "shuìjiào", "V-sep", "to sleep"),
], track="15-02", pages=[326, 327])
V("v1-phrases", "Phrases", [
  ("早一點", "zǎo yìdiǎn", "", "a bit earlier"),
], start=21, pages=[327])

# ---- Dialogue II ----
H("h-d2", "Dialogue II", "對話二", pages=[327])
T("d2-audio",
  "Practice dialogue written for this site with the vocabulary of Dialogue II. "
  "The book’s own Dialogue II is on book p. 327; its recording is track 15-03.",
  track="15-03")
D("d2", None, [
  ("如玉", "大衛，你怎麼了？臉色這麼難看。", "Dàwèi, nǐ zěnme le? Liǎnsè zhème nánkàn."),
  ("大衛", "我昨天晚上肚子很不舒服，吐了好幾次。", "Wǒ zuótiān wǎnshàng dùzi hěn bù shūfú, tùle hǎo jǐ cì."),
  ("如玉", "你這麼不舒服，要不要我跟你一起去看病？", "Nǐ zhème bù shūfú, yào bú yào wǒ gēn nǐ yìqǐ qù kànbìng?"),
  ("大衛", "不用了，我在臺灣沒有健康保險，我想自己去藥局買藥就好。", "Búyòng le, wǒ zài Táiwān méiyǒu jiànkāng bǎoxiǎn, wǒ xiǎng zìjǐ qù yàojú mǎi yào jiù hǎo."),
  ("如玉", "你真的不去看病嗎？學校的健康中心很方便，而且不用付很多錢。", "Nǐ zhēnde bú qù kànbìng ma? Xuéxiào de jiànkāng zhōngxīn hěn fāngbiàn, érqiě búyòng fù hěn duō qián."),
  ("大衛", "好吧，那麻煩妳陪我去健康中心。", "Hǎo ba, nà máfán nǐ péi wǒ qù jiànkāng zhōngxīn."),
  ("如玉", "好。你要多小心，冰的、油的東西最好都別吃。", "Hǎo. Nǐ yào duō xiǎoxīn, bīng de, yóu de dōngxi zuìhǎo dōu bié chī."),
  ("大衛", "謝謝妳的關心。", "Xièxie nǐ de guānxīn."),
  ("大衛", "醫生說我吃一包藥，睡一個小時以後就會好一點。", "Yīshēng shuō wǒ chī yì bāo yào, shuì yí ge xiǎoshí yǐhòu jiù huì hǎo yìdiǎn."),
  ("如玉", "太好了，你趕快回家休息吧。", "Tài hǎo le, nǐ gǎnkuài huíjiā xiūxí ba."),
], [
  ("Ruyu", "David, what's wrong? You don't look good at all."),
  ("David", "My stomach was really upset last night — I threw up several times."),
  ("Ruyu", "You're feeling that bad — do you want me to go with you to see a doctor?"),
  ("David", "No need. I don't have health insurance in Taiwan — I think I'll just go buy some medicine at the pharmacy myself."),
  ("Ruyu", "Are you really not going to see a doctor? The school's health center is convenient, and it doesn't cost much."),
  ("David", "All right, then please go with me to the health center."),
  ("Ruyu", "Okay. Be careful — you'd best not eat anything icy or oily."),
  ("David", "Thanks for your concern."),
  ("David", "(After seeing the doctor) The doctor said I should take a packet of medicine, and I'll feel a bit better after sleeping for an hour."),
  ("Ruyu", "Great, go home and rest right away."),
])

H("h-v2", "Vocabulary II", "生詞二", pages=[330])
V("v2-vocab", "Vocabulary", [
  ("臉色", "liǎnsè", "N", "a person's \"color\" (said of the face when healthy or sick, pleased or angry etc.)"),
  ("難看", "nánkàn", "Vs", "not to look good"),
  ("肚子", "dùzi", "N", "stomach, abdomen"),
  ("吐", "tù", "V", "to throw up, to vomit"),
  ("幾", "jǐ", "N", "(a) few"),
  ("次", "cì", "M", "measure word for times, occurrences"),
  ("陪", "péi", "V", "to go/stay with somebody, to accompany"),
  ("看病", "kànbìng", "V-sep", "to see a doctor"),
  ("健康", "jiànkāng", "N", "health"),
  ("保險", "bǎoxiǎn", "N", "insurance"),
  ("跟", "gēn", "Prep", "to, with"),
  ("油", "yóu", "Vs", "oily, greasy"),
  ("冰", "bīng", "Vs", "icy"),
  ("別", "bié", "Adv", "don't (used in imperatives)"),
  ("關心", "guānxīn", "Vst", "to be concerned about"),
  ("包", "bāo", "M", "measure word for bags, packages etc."),
  ("睡", "shuì", "Vi", "to sleep"),
  ("小時", "xiǎoshí", "N", "hour"),
], track="15-04", pages=[330])
V("v2-phrases", "Phrases", [
  ("怎麼了", "zěnme le", "", "What's wrong?"),
  ("不用了", "búyòng le", "", "It's not necessary."),
  ("健康中心", "jiànkāng zhōngxīn", "", "health center"),
  ("回家", "huí jiā", "", "go home"),
  ("最好", "zuìhǎo", "", "It would be best.../ (You) should..."),
], start=19, pages=[330, 331])

# ---- Grammar ----
H("h-gr", "Grammar", "文法", pages=[331])

# I. Non-committal Stance with Question Words
H("g1", "I. Non-committal Stance with Question Words", level=3, pages=[331])
T("g1-f",
  "Use: When a question word (什麼, 多少, 幾, 哪裡, 什麼地方, 誰, 什麼時候, etc.) occurs in a statement rather than in a question, it shows the speaker is giving a vague, non-committal answer instead of a clear one. A non-committal statement like this is always negative.")
EX("g1-ex", [
  ("我感冒了，什麼東西都不想吃。", "Wǒ gǎnmào le, shénme dōngxi dōu bù xiǎng chī.", "I've caught a cold — I don't feel like eating anything at all."),
  ("她生病了，哪裡都不想去。", "Tā shēngbìng le, nǎlǐ dōu bù xiǎng qù.", "She's sick — she doesn't want to go anywhere."),
  ("我這幾天沒有胃口，吃不下多少東西。", "Wǒ zhè jǐ tiān méiyǒu wèikǒu, chī bú xià duōshǎo dōngxi.", "I haven't had any appetite these past few days — I can't manage to eat much of anything."),
])
X("g1-x", "Complete each sentence with a question word showing a non-committal, negative stance.", [
  "他今天胃口不好，不想吃＿＿＿＿＿＿（什麼）。",
  "她感冒以後，一直待在家裡，不想去＿＿＿＿＿＿（哪裡）。",
  "我沒有力氣，不想花＿＿＿＿＿＿（多少）時間打掃房間。",
])

# II. To Dispose of Something with 把
H("g2", "II. To Dispose of Something with 把 bǎ", level=3, pages=[332, 333])
T("g2-f",
  "Use: 把 bǎ, the “disposal construction,” describes how the subject disposes of or handles a definite object. Structure: 把 + definite object + (bare, one-syllable, outward-transitive) verb + 了. The object must be definite (a bare noun, or one modified by 這個, 那個, 他的, etc.). Negation uses 沒 or 別 before 把.")
EX("g2-ex", [
  ("我把藥吃了。", "Wǒ bǎ yào chīle.", "I took the medicine."),
  ("她把感冒藥放在包包裡了。", "Tā bǎ gǎnmào yào fàng zài bāobāo lǐ le.", "She put the cold medicine in her bag."),
  ("護士把我的藥拿來了。", "Hùshì bǎ wǒ de yào ná lái le.", "The nurse brought my medicine over."),
])
X("g2-x", "Complete each sentence using the 把 disposal construction.", [
  "請你＿＿＿＿＿＿（把／藥）喝了。",
  "妳＿＿＿＿＿＿（把／窗戶）打開了嗎？",
  "我已經＿＿＿＿＿＿（把／咳嗽藥水）喝完了。",
])

# III. V了…就…
H("g3", "III. V 了 le…就 jiù… — do...right after doing...", level=3, pages=[333, 334])
T("g3-f",
  "Use: The pattern “V 了…就…” shows that the second event happens right after the first one is completed. It differs from the 一…就… pattern (Lesson 13) in that the verbal phrase after V了 is not restricted to being short, and 以後 can be added after V了 (but not after 一).")
EX("g3-ex", [
  ("他看了醫生就回家了。", "Tā kànle yīshēng jiù huíjiā le.", "He went home right after seeing the doctor."),
  ("我吃了藥就覺得舒服多了。", "Wǒ chīle yào jiù juéde shūfú duō le.", "I felt a lot better right after taking the medicine."),
  ("她下了課就去藥局拿藥。", "Tā xiàle kè jiù qù yàojú ná yào.", "She went to the pharmacy to get medicine right after class."),
])
X("g3-x", "Answer each question using the V了…就… pattern.", [
  "你什麼時候要去看醫生？（下班）→ ＿＿＿＿＿＿。",
  "你什麼時候要吃藥？（吃飯）→ ＿＿＿＿＿＿。",
  "他什麼時候會覺得好一點？（睡覺）→ ＿＿＿＿＿＿。",
])

# IV. 一點 a bit
H("g4", "IV. 一點 yìdiǎn — a bit", level=3, pages=[335])
T("g4-f",
  "Use: 一點 yìdiǎn indicates a minimal quantity or degree. It can go before a noun as its modifier (一點 + NP), after a state verb to show comparison (Vs + 一點, “a little more/less…”), or after 有 before a state verb without implying comparison (有(一)點 + Vs).")
EX("g4-ex", [
  ("她喝了一點熱湯，覺得舒服多了。", "Tā hēle yìdiǎn rè tāng, juéde shūfú duō le.", "She drank a bit of hot soup and felt a lot more comfortable."),
  ("這個藥有一點苦，可是很有效。", "Zhè ge yào yǒu yìdiǎn kǔ, kěshì hěn yǒuxiào.", "This medicine is a bit bitter, but it's very effective."),
  ("請你早一點回家休息。", "Qǐng nǐ zǎo yìdiǎn huíjiā xiūxí.", "Please go home a bit earlier to rest."),
])
X("g4-x", "Complete the sentences below using 一點, 有一點, or 多/少 V 一點 as appropriate.", [
  "你不舒服，要＿＿＿＿＿＿（休息）。",
  "他感冒了，臉色看起來＿＿＿＿＿＿（難看）。",
  "醫生說我的病＿＿＿＿＿＿（嚴重），要多注意。",
])

# V. Comparing Actions with a 得 Complement
H("g5", "V. Comparing Actions with a 得 de Complement", level=3, pages=[336, 337])
T("g5-f",
  "Use: This pattern compares how an action is performed. Most commonly: Action + 得 + Comparative + State, with the verb repeated when it takes an object (e.g., 看病看得比…快). Negation places 不 before 比.")
EX("g5-ex", [
  ("這位醫生看病看得比較仔細。", "Zhè wèi yīshēng kànbìng kàn de bǐjiào zǐxì.", "This doctor examines patients more carefully."),
  ("弟弟睡覺睡得比我晚。", "Dìdi shuìjiào shuì de bǐ wǒ wǎn.", "My younger brother goes to sleep later than I do."),
  ("她吃藥吃得不比我快。", "Tā chī yào chī de bù bǐ wǒ kuài.", "She doesn't take her medicine faster than I do."),
])
X("g5-x", "Compare the two actions using 得 de and complete the sentences.", [
  "王小姐看病看了半個小時，田中看病看了二十分鐘。→ 王小姐看病＿＿＿＿＿＿。",
  "哥哥昨天晚上睡了五個鐘頭，妹妹睡了八個鐘頭。→ 哥哥昨天晚上＿＿＿＿＿＿。",
  "如玉吃藥吃得很快，大衛吃藥吃得很慢。→ 如玉＿＿＿＿＿＿。",
])

# VI. Complements of Degree in Comparison Structures
H("g6", "VI. Complements of Degree in Comparison Structures", level=3, pages=[338])
T("g6-f",
  "Use: A degree of difference can be added after a comparison with 比 using …一點 (a little), …得多 (a lot), or …多了 (a lot more). All three go after the state verb.")
EX("g6-ex", [
  ("這次的感冒比上次嚴重一點。", "Zhè cì de gǎnmào bǐ shàng cì yánzhòng yìdiǎn.", "This cold is a little more serious than the last one."),
  ("喝熱湯比喝冷水舒服得多。", "Hē rè tāng bǐ hē lěng shuǐ shūfú de duō.", "Drinking hot soup is a lot more pleasant than drinking cold water."),
  ("我現在覺得比早上好多了。", "Wǒ xiànzài juéde bǐ zǎoshàng hǎo duō le.", "I feel a lot better now than I did this morning."),
])
X("g6-x", "Answer the questions below using 一點, 得多, or 多了 in the complement.", [
  "這種藥比那種藥貴嗎？→ ＿＿＿＿＿＿。",
  "你今天的胃口是不是比昨天好？→ ＿＿＿＿＿＿。",
  "田中的燒是不是比如玉的高得多？→ ＿＿＿＿＿＿。",
])

# VII. Separable Verbs
H("g7", "VII. Separable Verbs", level=3, pages=[339])
T("g7-f",
  "Use: Separable verbs have the inherent structure [V+N]; an element — 了, an object, or a time-duration — can be inserted between the V and the N, after which the two behave like a verb and its object. Examples among the words of this lesson: 看病, 生病, 睡覺.")
EX("g7-ex", [
  ("他這個月看了三次病。", "Tā zhège yuè kànle sān cì bìng.", "He's seen a doctor three times this month."),
  ("我想睡一個下午的覺。", "Wǒ xiǎng shuì yí ge xiàwǔ de jiào.", "I'd like to sleep the whole afternoon."),
  ("她照顧了我好幾天。", "Tā zhàogùle wǒ hǎo jǐ tiān.", "She took care of me for several days."),
])
X("g7-x", "Separate the elements V and N below, then insert something between them to form a good sentence.", [
  "看病 → ＿＿＿＿＿＿",
  "生病 → ＿＿＿＿＿＿",
  "睡覺 → ＿＿＿＿＿＿",
])

# ---- Classroom activities ----
H("h-act", "Classroom Activities", "課室活動", pages=[345])
H("act1", "I. Let's Compare", level=3)
T("act1-t",
  "Goal: Learning to make comparisons of varying degrees using a 得 complement.",
  "Task: The chart below shows how long four classmates slept last night and how many times each saw a doctor this semester. Using the questions as a guide, compare the four people with a classmate.",
  "睡覺時間：田中 6 小時 / 如玉 7 個半小時 / 安同 5 個小時 / 月美 8 個小時",
  "看病次數（這學期）：田中 1 次 / 如玉 3 次 / 安同 0 次 / 月美 2 次",
  "1. 誰睡得比較久？誰睡得比較少？", "2. 誰看病看得比較多次？誰一次都沒看過？")
H("act2", "II. Who Is Taking Care of Me?", level=3, pages=[346])
T("act2-t",
  "Goal: Learning to ask how someone is feeling and to give suggestions to somebody who is sick.",
  "Task 1: Act out the roles A and B with a classmate and write down your conversation. A asks B what's wrong; B describes a symptom; A suggests something B should do (應該/最好); B accepts or politely declines the suggestion.",
  "Task 2: Role-play being a patient who has a headache and a slight fever. Your partner plays the doctor. Describe your symptoms, and have the doctor give you some advice.")
H("act3", "III. Taking Medication", level=3, pages=[347])
T("act3-t",
  "Goal: Learning to read the instructions on a prescription label.",
  "Task: Look at the prescription label below and ask a classmate the three questions that follow.",
  "健康藥局：一天 3 次，4 日份，飯後 30 分鐘",
  "1. 這種藥一天吃幾次？", "2. 這些藥夠吃幾天？", "3. 應該在飯前還是飯後吃？")
H("act4", "IV. Use 把 Construction", level=3, pages=[348])
T("act4-t",
  "Goal: Learning to use the disposal construction 把.",
  "Task: With a partner, complete the dialogues below based on the situations given.",
  "1. A：醫生說我的藥一天要吃三次，可是我常常忘記。B：那你要記得按時＿＿＿＿＿＿（把／藥）吃了。",
  "2. A：你怎麼還沒去藥局？B：我等一下就去，我想先＿＿＿＿＿＿（把／這碗湯）喝完。",
  "3. A：你的感冒好一點了嗎？B：好多了，昨天晚上我＿＿＿＿＿＿（把／醫生開的藥）吃了，今天就不發燒了。")
H("act5", "V. How Are You Feeling?", level=3, pages=[348])
T("act5-t",
  "Goal: Learning to talk about having a cold.",
  "Task: Your friend 田中 is sick at home. Call him and ask how he is feeling, then ask four more questions about his condition.",
  "1. ＿＿＿＿＿＿？", "2. ＿＿＿＿＿＿？", "3. ＿＿＿＿＿＿？", "4. ＿＿＿＿＿＿？")

# ---- Culture ----
H("h-cult", "Bits of Chinese Culture", "文化", pages=[349])
H("cult1", "Wearing Surgical Masks", level=3)
T("cult1-t",
  "Seeing someone wearing a surgical mask on the street in Taiwan doesn't necessarily mean that person is ill.",
  "Because colds spread easily through the respiratory system, especially when the seasons are changing, many people wear a mask on crowded buses or the MRT simply to lower the chance of catching or spreading one.",
  "People wear masks for other everyday reasons too: scooter riders wear them in winter to stay warm and to filter out exhaust and dust; restaurant staff wear them so that they don't unintentionally let anything land in the food they're preparing; and in hospitals, both staff and patients wear them to help prevent infections from spreading. In short, a mask in Taiwan is usually a simple precaution, not a sign that something is wrong.")

# ---- Self-assessment ----
H("h-self", "Self-Assessment Checklist", pages=[350])
add({"type": "checklist", "id": "self", "items": [
  "I can ask someone how they are feeling.",
  "I can describe symptoms in simple terms.",
  "I can make suggestions to somebody who is sick.",
  "I can politely accept or reject suggestions.",
]})
