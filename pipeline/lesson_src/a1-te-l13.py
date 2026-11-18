LESSON_ID = "a1-te-l13"
TITLE = "生日快樂 Happy Birthday"
STATUS = "complete"
DETAIL = ("Materi ini ditulis ulang secara orisinal untuk situs ini berdasarkan topik, daftar kosakata, dan pola tata bahasa "
          "buku (hlm. buku 269–298): penjelasan, contoh kalimat, dialog latihan, soal, dan catatan budaya memakai kata-kata sendiri. "
          "Dialog, latihan bergambar, dan foto asli ada di buku; audio trek asli tetap ditautkan.")

# ---- objectives ----
H("h-obj", "Learning Objectives", "學習目標", pages=[269])
T("obj",
  "Topic: 社交生活 Social Life",
  "• Learning to make appointments on the phone.",
  "• Learning to ask friends about their dietary preferences.",
  "• Learning to compare cultures.",
  "• Learning to express wishes to others on special occasions and to respond appropriately.")

# ---- Dialogue I ----
H("h-d1", "Dialogue I", "對話一", pages=[270])
T("d1-audio",
  "Practice dialogue written for this site with the vocabulary of Dialogue I. "
  "The book’s own Dialogue I is on book p. 270; its recording is track 13-01.",
  track="13-01")
D("d1", None, [
  ("如玉", "喂，請問田中在不在？", "Wéi, qǐngwèn Tiánzhōng zài bú zài?"),
  ("田中", "我就是，如玉，好久不見！聽說妳去高雄玩了？", "Wǒ jiù shì, Rúyù, hǎojiǔ bújiàn! Tīngshuō nǐ qù Gāoxióng wán le?"),
  ("如玉", "沒有啊，我剛從花蓮回來。", "Méiyǒu a, wǒ gāng cóng Huālián huílái."),
  ("田中", "妳找我有事嗎？", "Nǐ zhǎo wǒ yǒu shì ma?"),
  ("如玉", "後天是你的生日，你不記得了嗎？", "Hòutiān shì nǐ de shēngrì, nǐ bù jìde le ma?"),
  ("田中", "啊！我怎麼忘了！最近太忙了，謝謝妳還記得。", "A! Wǒ zěnme wàng le! Zuìjìn tài máng le, xièxie nǐ hái jìde."),
  ("如玉", "我當然記得。上次語言交換，你那麼熱心地教我法文呢！", "Wǒ dāngrán jìde. Shàngcì yǔyán jiāohuàn, nǐ nàme rèxīn de jiāo wǒ Fǎwén ne!"),
  ("田中", "妳對我真好，妳也教了我不少中文。", "Nǐ duì wǒ zhēn hǎo, nǐ yě jiāole wǒ bùshǎo Zhōngwén."),
  ("如玉", "明天我想請你吃晚飯，幫你過生日，好不好？", "Míngtiān wǒ xiǎng qǐng nǐ chī wǎnfàn, bāng nǐ guò shēngrì, hǎo bù hǎo?"),
  ("田中", "太客氣了！那要約幾點，在哪裡見面？", "Tài kèqì le! Nà yào yuē jǐ diǎn, zài nǎlǐ jiànmiàn?"),
  ("如玉", "我一下課，就去圖書館門口等你，六點左右，好嗎？", "Wǒ yí xiàkè, jiù qù túshūguǎn ménkǒu děng nǐ, liù diǎn zuǒyòu, hǎo ma?"),
  ("田中", "好，明天見！", "Hǎo, míngtiān jiàn!"),
], [
  ("Ruyu", "Hello, is Tanaka there, please?"),
  ("Tanaka", "This is he. Ruyu, long time no see! I heard you went to Kaohsiung?"),
  ("Ruyu", "No, I just got back from Hualien."),
  ("Tanaka", "Did you call me for some reason?"),
  ("Ruyu", "The day after tomorrow is your birthday — don’t you remember?"),
  ("Tanaka", "Oh! How did I forget that? I’ve been so busy lately. Thanks for remembering."),
  ("Ruyu", "Of course I remember. During our language exchange, you were so enthusiastic about teaching me French!"),
  ("Tanaka", "You’re too kind to me. You taught me quite a bit of Chinese too."),
  ("Ruyu", "I’d like to treat you to dinner tomorrow to celebrate your birthday — is that all right?"),
  ("Tanaka", "That’s very kind of you! What time should we meet, and where?"),
  ("Ruyu", "As soon as I get out of class, I’ll go wait for you at the library entrance, around six — is that okay?"),
  ("Tanaka", "Sure, see you tomorrow!"),
])

H("h-v1", "Vocabulary I", "生詞一", pages=[272])
V("v1-vocab", "Vocabulary", [
  ("生日", "shēngrì", "N", "birthday"),
  ("快樂", "kuàilè", "Vs", "happy"),
  ("回來", "huílái", "Vi", "to come back"),
  ("啊", "a", "Ptc", "particle indicating a realization"),
  ("怎麼", "zěnme", "Adv", "how come?"),
  ("忘（了）", "wàngle", "Vpt", "to forget"),
  ("記得", "jìde", "Vst", "to remember"),
  ("當然", "dāngrán", "Adv", "certainly, of course"),
  ("語言", "yǔyán", "N", "language"),
  ("交換", "jiāohuàn", "V", "to exchange"),
  ("那麼", "nàme", "Adv", "so (very)"),
  ("熱心", "rèxīn", "Vs", "with enthusiasm"),
  ("西班牙文", "Xībānyá wén", "N", "the Spanish language"),
  ("一樣", "yíyàng", "Vs", "the same, alike"),
  ("過", "guò", "V", "to celebrate"),
  ("左右", "zuǒyòu", "N", "approximately"),
  ("門口", "ménkǒu", "N", "gate, entrance"),
], track="13-02", pages=[272])
V("v1-names", "Names", [("西班牙", "Xībānyá", "", "Spain")], start=18, pages=[272])
V("v1-phrases", "Phrases", [
  ("生日快樂", "shēngrì kuàilè", "", "Happy Birthday."),
  ("我就是", "wǒ jiù shì", "", "(said of self on the phone) This is s/he speaking."),
  ("好久不見", "hǎojiǔ bújiàn", "", "long time no see"),
  ("不必客氣", "búbì kèqì", "", "No need to stand on formalities, i.e., It’s my pleasure."),
  ("太客氣", "tài kèqì", "", "That’s very kind of you."),
], start=19, pages=[273])

# ---- Dialogue II ----
H("h-d2", "Dialogue II", "對話二", pages=[274])
T("d2-audio",
  "Practice dialogue written for this site with the vocabulary of Dialogue II. "
  "The book’s own Dialogue II is on book p. 274; its recording is track 13-03.",
  track="13-03")
D("d2", None, [
  ("田中", "如玉，謝謝妳請我到這家餐廳吃飯，這家的菜看起來都很好吃。", "Rúyù, xièxie nǐ qǐng wǒ dào zhè jiā cāntīng chīfàn, zhè jiā de cài kàn qǐlái dōu hěn hǎochī."),
  ("如玉", "不必客氣，這是我給你的生日禮物。", "Búbì kèqì, zhè shì wǒ gěi nǐ de shēngrì lǐwù."),
  ("田中", "謝謝！真開心，今年有臺灣朋友幫我過生日。", "Xièxie! Zhēn kāixīn, jīnnián yǒu Táiwān péngyǒu bāng wǒ guò shēngrì."),
  ("如玉", "你有沒有不吃的東西？", "Nǐ yǒu méiyǒu bù chī de dōngxi?"),
  ("田中", "我什麼都吃，不過海鮮吃得比較少。", "Wǒ shénme dōu chī, búguò hǎixiān chī de bǐjiào shǎo."),
  ("如玉", "那我多點一點蔬菜，少點一點海鮮。", "Nà wǒ duō diǎn yìdiǎn shūcài, shǎo diǎn yìdiǎn hǎixiān."),
  ("田中", "在你們國家，過生日是不是也都吃蛋糕？", "Zài nǐmen guójiā, guò shēngrì shìbúshì yě dōu chī dàngāo?"),
  ("如玉", "對啊，這是傳統，不過，現在大部分年輕人過生日還會跟朋友出去玩。", "Duì a, zhè shì chuántǒng, búguò, xiànzài dà bùfèn niánqīng rén guò shēngrì hái huì gēn péngyǒu chūqù wán."),
  ("田中", "那麼，你們過生日還會做什麼呢？", "Nàme, nǐmen guò shēngrì hái huì zuò shénme ne?"),
  ("如玉", "跟你一樣，也會吃蛋糕。我已經訂了一個生日蛋糕了。", "Gēn nǐ yíyàng, yě huì chī dàngāo. Wǒ yǐjīng dìngle yí ge shēngrì dàngāo le."),
  ("田中", "妳對我真好。", "Nǐ duì wǒ zhēn hǎo."),
  ("如玉", "田中，祝你生日快樂、萬事如意、心想事成。", "Tiánzhōng, zhù nǐ shēngrì kuàilè, wànshì rúyì, xīnxiǎng shìchéng."),
  ("田中", "謝謝！謝謝！", "Xièxie! Xièxie!"),
], [
  ("Tanaka", "Ruyu, thanks for treating me to this restaurant. Everything here looks delicious."),
  ("Ruyu", "No need to stand on formalities — this is my gift for you."),
  ("Tanaka", "Thank you! I’m really happy that a Taiwanese friend is celebrating my birthday with me this year."),
  ("Ruyu", "Is there anything you don’t eat?"),
  ("Tanaka", "I eat anything, but I eat relatively little seafood."),
  ("Ruyu", "Then I’ll order a bit more vegetables and a bit less seafood."),
  ("Tanaka", "In your country, do people also eat cake on their birthdays?"),
  ("Ruyu", "Yes. That’s a tradition, but most young people nowadays also go out with friends on their birthdays."),
  ("Tanaka", "Then what else do you do on your birthday?"),
  ("Ruyu", "Just like you, we eat cake too. I’ve already ordered a birthday cake."),
  ("Tanaka", "You’re really nice to me."),
  ("Ruyu", "Tanaka, Happy Birthday — I wish you the best in everything, and may all your wishes come true."),
  ("Tanaka", "Thank you! Thank you!"),
])

H("h-v2", "Vocabulary II", "生詞二", pages=[276])
V("v2-vocab", "Vocabulary", [
  ("禮物", "lǐwù", "N", "gift, present"),
  ("今年", "jīnnián", "N", "this year"),
  ("訂", "dìng", "V", "to order (something in advance)"),
  ("了", "le", "Ptc", "verbal particle indicating a completed action"),
  ("豬腳", "zhūjiǎo", "N", "pork knuckles"),
  ("麵線", "miànxiàn", "N", "extra fine noodles"),
  ("蛋", "dàn", "N", "egg"),
  ("一點", "yìdiǎn", "Vs", "a little, some"),
  ("傳統", "chuántǒng", "N", "tradition, customs"),
  ("年輕", "niánqīng", "Vs", "young"),
  ("蛋糕", "dàngāo", "N", "cake"),
  ("對", "duì", "Prep", "to"),
  ("祝", "zhù", "V", "to wish (somebody happiness, good luck, etc.)"),
], track="13-04", pages=[276])
V("v2-phrases", "Phrases", [
  ("哪裡，哪裡", "nǎlǐ, nǎlǐ", "", "Don’t mention it, it’s my pleasure."),
  ("大部分", "dà bùfèn", "", "most (of), mostly"),
  ("萬事如意", "wànshì rúyì", "", "May everything go your way."),
  ("心想事成", "xīnxiǎng shìchéng", "", "May all your wishes come true."),
], start=14, pages=[276])

# ---- Grammar ----
H("h-gr", "Grammar", "文法", pages=[277])

# I. 一…就…
H("g1", "I. 一 yī…就 jiù… as soon as…", level=3, pages=[277])
T("g1-f",
  "Use: The pattern 一 A 就 B describes a sequence of two events, with B happening right after A. Both events can be affirmative or negative. 一 and 就 are adverbs and come after the subject of their own clause; when the subject of both clauses is the same, the second subject is usually dropped.")
EX("g1-ex", [
  ("我一下課，就去圖書館門口等你。", "Wǒ yí xiàkè, jiù qù túshūguǎn ménkǒu děng nǐ.", "I’ll go wait for you at the library entrance as soon as I’m out of class."),
  ("他一記得你的生日，就馬上打電話給你。", "Tā yí jìde nǐ de shēngrì, jiù mǎshàng dǎ diànhuà gěi nǐ.", "As soon as he remembered your birthday, he called you right away."),
  ("我朋友一回來，就訂了一個蛋糕。", "Wǒ péngyǒu yì huílái, jiù dìngle yí ge dàngāo.", "As soon as my friend got back, she ordered a cake."),
])
X("g1-x", "Complete each sentence using 一…就….", [
  "我一聽說他的生日，＿＿＿＿＿＿。",
  "她一到餐廳，＿＿＿＿＿＿。",
  "我們一吃完蛋糕，＿＿＿＿＿＿。",
])

# II. Completed Action with Verbal 了
H("g2", "II. Completed Action with Verbal 了 le", level=3, pages=[277, 278])
T("g2-f",
  "Use: The verbal 了 is added right after the verb to show that an action has already happened or been completed, in contrast to a plan that has not yet taken place. 了 does not appear in negative sentences — 沒 replaces it instead — and questions add 沒有 at the end of the sentence.")
EX("g2-ex", [
  ("如玉已經訂了一個生日蛋糕。", "Rúyù yǐjīng dìngle yí ge shēngrì dàngāo.", "Ruyu has already ordered a birthday cake."),
  ("他昨天教了我一點西班牙文。", "Tā zuótiān jiāole wǒ yìdiǎn Xībānyá wén.", "He taught me a little Spanish yesterday."),
  ("我吃了豬腳麵線，也吃了蛋糕。", "Wǒ chīle zhūjiǎo miànxiàn, yě chīle dàngāo.", "I ate pork-knuckle noodles, and I also had cake."),
])
EX("g2-neg", [
  ("我今天沒訂蛋糕，明天再訂。", "Wǒ jīntiān méi dìng dàngāo, míngtiān zài dìng.", "I didn’t order the cake today — I’ll order it tomorrow instead."),
  ("他沒忘記你的生日，只是太忙了。", "Tā méi wàngjì nǐ de shēngrì, zhǐshì tài máng le.", "He didn’t forget your birthday — he was just too busy."),
], title="Negation")
X("g2-x", "Fill in the blank with 了 or 沒, based on the cue.", [
  "我已經（打電話給他）了嗎？→ 我＿＿＿＿＿＿。（是）",
  "她昨天（買禮物）＿＿＿＿＿＿嗎？（否，太晚了）",
  "我今天（吃早餐）＿＿＿＿＿＿。（否）",
])

# III. 不 Negation vs. 沒 Negation
H("g3", "III. 不 bù Negation vs. 沒 méi Negation", level=3, pages=[278, 279, 280])
T("g3-f",
  "Use: 不 and 沒 are both negation markers, but they attach to different kinds of verbs. Action verbs can take either 不 (habitual or an intention not to) or 沒 (something that didn’t happen in the past). State verbs — adjective-like verbs such as 忙, 熱心, 一樣 — can only be negated by 不. Process verbs — verbs describing a change, such as 忘, 決定, 結束 — can only be negated by 沒.")
EX("g3-ex", [
  ("我平常不喝咖啡，不過今天想喝一杯。", "Wǒ píngcháng bù hē kāfēi, búguò jīntiān xiǎng hē yì bēi.", "I usually don’t drink coffee, but today I feel like having a cup. (habitual)"),
  ("他不去夜市，想在家休息。", "Tā bú qù yèshì, xiǎng zài jiā xiūxí.", "He’s not going to the night market — he wants to rest at home. (intention)"),
  ("昨天太忙了，我沒打電話給她。", "Zuótiān tài máng le, wǒ méi dǎ diànhuà gěi tā.", "I was too busy yesterday, so I didn’t call her. (non-happening, action verb)"),
])
EX("g3-state", [
  ("這家餐廳的菜不貴，大家都喜歡來。", "Zhè jiā cāntīng de cài bú guì, dàjiā dōu xǐhuān lái.", "The food at this restaurant isn’t expensive — everyone likes to come."),
  ("我的生日跟他的不一樣。", "Wǒ de shēngrì gēn tā de bù yíyàng.", "My birthday isn’t the same as his."),
], title="Negation of state verbs (不 only)")
EX("g3-process", [
  ("我還沒決定要訂什麼蛋糕。", "Wǒ hái méi juédìng yào dìng shénme dàngāo.", "I still haven’t decided what cake to order."),
  ("語言交換還沒結束，我們再聊一下。", "Yǔyán jiāohuàn hái méi jiéshù, wǒmen zài liáo yíxià.", "The language exchange hasn’t ended yet — let’s chat a bit more."),
], title="Negation of process verbs (沒 only)")
X("g3-x", "Fill in 不 or 沒 and briefly explain why.", [
  "他常常（　）記得朋友的生日。",
  "這兩種蛋糕的味道（　）一樣。",
  "我（　）決定要不要去語言交換。",
])

# IV. All-inclusive with Question Words
H("g4", "IV. All-inclusive with Question Words", level=3, pages=[280, 281])
T("g4-f",
  "Use: Question words such as 誰, 哪裡, 什麼, 什麼時候, and 怎麼+V can appear in statements rather than questions. Paired with 都 dōu, they show total inclusion (“everyone”, “everywhere”, “no matter how”) in affirmative sentences; with 都 or 也 plus a negative, they show total exclusion (“no one”, “nowhere”, “not at all”).")
EX("g4-ex", [
  ("誰都想在生日的時候收到禮物。", "Shéi dōu xiǎng zài shēngrì de shíhòu shōudào lǐwù.", "Everyone wants to receive a gift on their birthday."),
  ("這家店的蛋糕什麼都好吃。", "Zhè jiā diàn de dàngāo shénme dōu hǎochī.", "Everything at this shop’s cake counter is delicious."),
  ("他怎麼過生日都很開心。", "Tā zěnme guò shēngrì dōu hěn kāixīn.", "No matter how he celebrates his birthday, he’s always happy."),
])
EX("g4-neg", [
  ("今天太忙了，我哪裡都沒去。", "Jīntiān tài máng le, wǒ nǎlǐ dōu méi qù.", "I was too busy today — I didn’t go anywhere."),
  ("他這個星期什麼時候都不在家，在準備考試。", "Tā zhè ge xīngqí shénme shíhòu dōu bú zài jiā, zài zhǔnbèi kǎoshì.", "He’s not home at all this week — he’s preparing for an exam."),
], title="Negation")
X("g4-x", "Rewrite each sentence into an all-inclusive or all-exclusive pattern.", [
  "大家都喜歡吃豬腳麵線。→ ＿＿＿＿＿＿。",
  "他早上、中午、晚上都在打電話。→ ＿＿＿＿＿＿。",
  "這個禮物，他看了也不喜歡，摸了也不喜歡。→ ＿＿＿＿＿＿。",
])

# V. More/Less...Than Planned with 多/少 + Verb
H("g5", "V. More/Less…Than Planned with 多 duō / 少 shǎo + Verb…", level=3, pages=[281, 282])
T("g5-f",
  "Use: Pre-verbal 多 (“more”) and 少 (“less/fewer”) describe doing more or less of an action than originally planned or than usual. 一點 often follows the object to soften the amount, and the pattern can describe either past or future actions.")
EX("g5-ex", [
  ("海鮮比較貴，我們少點一點。", "Hǎixiān bǐjiào guì, wǒmen shǎo diǎn yìdiǎn.", "Seafood is relatively pricey — let’s order a bit less."),
  ("他喜歡吃蔬菜，我多買了一點。", "Tā xǐhuān chī shūcài, wǒ duō mǎile yìdiǎn.", "He likes vegetables, so I bought a bit extra."),
  ("今年他的生日人比較多，我們應該多訂一個蛋糕。", "Jīnnián tā de shēngrì rén bǐjiào duō, wǒmen yīnggāi duō dìng yí ge dàngāo.", "More people are coming to his birthday this year, so we should order an extra cake."),
])
X("g5-x", "Give a suggestion for each situation using 多/少 + Verb + 一點.", [
  "朋友最近很忙，常常很晚才睡覺。→ 他應該＿＿＿＿＿＿。",
  "你的中文不太好，可是你很少說中文。→ 你應該＿＿＿＿＿＿。",
  "這個星期你花了不少錢。→ 下個星期你應該＿＿＿＿＿＿。",
])

# VI. 是不是 shìbúshì — is it true?
H("g6", "VI. 是不是 shìbúshì — is it true?", level=3, pages=[282, 283])
T("g6-f",
  "Use: 是不是 asks for confirmation of something the speaker already believes or finds obvious, rather than asking for brand-new information, as 嗎 or A-not-A questions do. Structure: Subject + 是不是 + VP？ This pattern must be used, instead of A-not-A, with sentences that already contain 比 (comparison) or a degree adverb such as 太/很.")
EX("g6-ex", [
  ("你是不是忘了他的生日？", "Nǐ shìbúshì wàngle tā de shēngrì?", "You forgot his birthday, didn’t you?"),
  ("這家餐廳是不是很有名？", "Zhè jiā cāntīng shìbúshì hěn yǒumíng?", "This restaurant is famous, isn’t it?"),
  ("你是不是比他忙？", "Nǐ shìbúshì bǐ tā máng?", "You’re busier than him, aren’t you? (comparison — A-not-A is not possible here)"),
])
X("g6-x", "Insert 是不是 into the right place in each sentence.", [
  "我們明天給他過生日。→ ＿＿＿＿＿＿？",
  "你比較喜歡吃甜點。→ ＿＿＿＿＿＿？",
  "他最近太忙了。→ ＿＿＿＿＿＿？",
])

# VII. Comparison with 跟…一樣
H("g7", "VII. Comparison with 跟 gēn…一樣 yíyàng", level=3, pages=[283])
T("g7-f",
  "Use: 跟…一樣 compares two people or things and states that they are the same or equal; the quality being compared, if given, follows 一樣. Structure: A 跟 B 一樣 (state verb). Negating with 不 before 一樣 says the two are different; negating with 不 before 跟 instead shifts the “different” object, so the sentence then says what A is the same as.")
EX("g7-ex", [
  ("我的生日跟田中的一樣，都是十二月。", "Wǒ de shēngrì gēn Tiánzhōng de yíyàng, dōu shì shí'èr yuè.", "My birthday is the same as Tanaka’s — both are in December."),
  ("這個蛋糕跟那個一樣甜。", "Zhè ge dàngāo gēn nàge yíyàng tián.", "This cake is just as sweet as that one."),
  ("他跟我一樣，都喜歡交外國朋友。", "Tā gēn wǒ yíyàng, dōu xǐhuān jiāo wàiguó péngyǒu.", "He’s like me — we both enjoy making foreign friends."),
])
EX("g7-neg", [
  ("海鮮跟蔬菜不一樣貴。", "Hǎixiān gēn shūcài bù yíyàng guì.", "Seafood and vegetables don’t cost the same."),
  ("他不跟我一樣高，跟如玉一樣高。", "Tā bù gēn wǒ yíyàng gāo, gēn Rúyù yíyàng gāo.", "He’s not the same height as me — he’s the same height as Ruyu."),
], title="Negation")
X("g7-x", "Ask a question about each pair using 跟…一樣, with either the A-not-A form or 是不是.", [
  "牛肉麵／牛肉湯 → ＿＿＿＿＿＿？",
  "今年的生日／去年的生日 → ＿＿＿＿＿＿？",
])

# ---- Classroom activities ----
H("h-act", "Classroom Activities", "課室活動", pages=[294])
H("act1", "I. Going to the Night Market", level=3)
T("act1-t",
  "Goal: Learning to ask people about their preferences.",
  "Task: You heard that a classmate went to the night market yesterday. Ask whether they tried each item below, using the verbal 了 pattern, e.g. 你昨天逛夜市，吃了珍珠奶茶沒有？ Possible answers: 喝了，很好喝 / 沒有，我點了別的飲料 / 我沒喝珍珠奶茶.",
  "Items to ask about: 牛肉麵、小籠包、甜點、珍珠奶茶、臭豆腐、熱咖啡、芒果、豬腳、越南菜、西瓜、熱烏龍茶、牛肉湯.")
H("act2", "II. How Do You Celebrate Your Birthday?", level=3, pages=[295])
T("act2-t",
  "Goal: Learning to compare cultures briefly.",
  "Task: Pair up with a classmate from a different country and ask each other how birthdays are celebrated back home. Check off which of the following apply, then report to the class the similarities and differences you found: family celebrates it for you / friends celebrate it for you / celebrated at home / eaten out at a restaurant / cake is eaten / friends give gifts / you buy your own cake to share with friends / pork-knuckle noodles are eaten / it’s different from how we do it here.")
H("act3", "III. Calling a Friend", level=3, pages=[296])
T("act3-t",
  "Goal: Learning to make appointments on the phone.",
  "Task: Your teacher’s birthday is tomorrow. Pair up with a classmate and call each other to plan taking the teacher out for a meal. In your call, be sure to cover: why you’re inviting him/her, what time to meet, where to meet, and how everyone will find each other there.")
H("act4", "IV. Congratulatory Words", level=3, pages=[296])
T("act4-t",
  "Goal: Learning to express wishes on happy occasions.",
  "Task: It’s your teacher’s birthday today. Write him or her a short card wishing them well, using at least one of the phrases 萬事如意 or 心想事成.")

# ---- Culture ----
H("h-cult", "Bits of Chinese Culture", "文化", pages=[297])
H("cult1", "Congratulatory Expressions in Chinese", level=3)
T("cult1-t",
  "Chinese culture places a lot of value on saying the right caring thing, at the right moment, for the right occasion — this is part of why congratulatory expressions are so common. Most of these set sayings are four-character phrases with a fixed, auspicious meaning, often used together, such as 萬事如意、心想事成 wànshì rúyì, xīnxiǎng shìchéng, “may everything go your way and all your wishes come true” — probably the most all-purpose good wish of all, suitable for almost any happy occasion, not only birthdays. These phrases turn up everywhere from spoken well-wishes to red envelopes and decorative scrolls hung at home.")
H("cult2", "Taiwanese Birthdays", level=3, pages=[297, 298])
T("cult2-t",
  "Traditionally, birthdays in Taiwan were tracked by the lunar calendar, though most people today mark theirs by the regular Gregorian calendar instead. Birthdays matter a good deal in Taiwanese culture, and some are celebrated more elaborately than others: a baby’s first month and first full year are both commonly marked with a gathering, and so are milestone decades later in life, such as turning 60, 70, or 80. One well-known custom tied to a baby’s first birthday is 抓週 zhuāzhōu (“grabbing at the first year”): a variety of small objects are placed in front of the child, and whichever one they reach for and grab is taken as a playful sign of the kind of personality or career they might have later in life.")

# ---- Self-assessment ----
H("h-self", "Self-Assessment Checklist", pages=[298])
add({"type": "checklist", "id": "self", "items": [
  "I can make appointments on the phone.",
  "I can ask friends about their dietary preferences.",
  "I can compare cultures.",
  "I can express wishes to others on special occasions and respond appropriately when others offer me wishes.",
]})
