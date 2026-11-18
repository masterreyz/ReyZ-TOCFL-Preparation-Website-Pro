LESSON_ID = "a1-wo-l04"
TITLE = "請問一共多少錢？ Excuse Me. How Much Does That Cost in Total?"
STATUS = "complete"
DETAIL = ("Materi ini ditulis ulang secara orisinal untuk situs ini berdasarkan topik dan kosakata Pelajaran 4 "
          "buku kerja (hlm. buku 25–30): soal latihan, kalimat contoh, dan kunci memakai kata-kata sendiri. "
          "Soal bergambar asli ada di buku; audio trek asli tetap ditautkan.")

H("h-obj", "Learning Objectives", "學習目標", pages=[25])
T("obj",
  "Topic: 買東西、問價錢 Shopping and Asking Prices",
  "• Practicing tone recognition for Lesson 4 vocabulary.",
  "• Practicing listening/reading comprehension about prices, ordering food and drinks, and describing cell phone features.",
  "• Practicing asking for a total price and writing a short paragraph about what one can buy with a given amount of money.")

# ---- I. Differentiating Tones ----
H("h1", "I. Differentiating Tones", "一、辨別聲調", level=3, pages=[25])
T("h1-t",
  "Practice exercise written for this site using Lesson 4 vocabulary. The book's own tone-marking exercise is on book p. 25; its recording is track 04-01.",
  track="04-01")
add({"type": "table", "id": "h1-tab", "head": ["中文", "Pinyin (fill in the tone marks)"], "rows": [
  ["一杯", "yibei"],
  ["一共", "yigong"],
  ["多少", "duoshao"],
  ["上網", "shangwang"],
  ["外帶", "waidai"],
  ["照相", "zhaoxiang"],
  ["兩塊", "liangkuai"],
  ["內用", "neiyong"],
  ["微波", "weibo"],
  ["二十塊", "ershikuai"],
]}, pages=[25])

# ---- II. Listen and Respond ----
H("h2", "II. Listen and Respond", "二、請聽並回答", level=3, pages=[25, 26])
T("h2-t",
  "Practice exercise written for this site using Lesson 4 vocabulary. The book's own listening exercises are on book pp. 25–26; their recordings are tracks 04-02, 04-03 and 04-04.")

T("h2a-t", "A. Read the short situation below and choose the correct answer for each. (track 04-02)", track="04-02")
X("h2a-x", "Choose the correct answer for each question.", [
  "林先生要買大的包子，請問他要哪一個？ a. 小的　b. 大的",
  "陳小姐要在這裡吃，請問她要內用還是外帶？ a. 內用　b. 外帶",
  "王先生覺得這支手機很貴，請問是貴的還是便宜的？ a. 貴的　b. 便宜的",
  "妹妹不要熱咖啡，請問她要熱的還是不熱的？ a. 熱的　b. 不熱的",
  "姐姐的新手機能上網，不能照相，請問哪個對？ a. 能照相　b. 能上網",
], title="A. 問答")

T("h2b-t", "B. 大衛 placed an order. Read what he said and fill in the table below. (track 04-03)",
  "大衛說：「我要三個包子，一杯烏龍茶，不要咖啡。包子一個20塊，烏龍茶一杯35塊，請問一共多少錢？」",
  track="04-03")
add({"type": "table", "id": "h2b-tab", "head": ["我要買", "包子（個）", "烏龍茶（杯）", "咖啡（杯）", "一共多少錢"], "rows": [
  ["回答 answer", "＿＿＿＿", "＿＿＿＿", "＿＿＿＿", "＿＿＿＿"],
]}, pages=[25])

T("h2c-t", "C. Listen to the dialogue. Write ○ if the statement is true, × if it is false. (track 04-04)",
  "老闆：歡迎光臨，請問要什麼？",
  "安同：請問一杯烏龍茶多少錢？",
  "老闆：一杯35塊，兩杯65塊。",
  "安同：好，我要兩杯烏龍茶，一杯要冰的，一杯要熱的。",
  "老闆：好的，一共65塊。",
  track="04-04")
X("h2c-x", "Mark each statement ○ (true) or × (false).", [
  "（　）安同要買兩杯烏龍茶。",
  "（　）一杯烏龍茶35塊。",
  "（　）安同的兩杯烏龍茶都要熱的。",
  "（　）安同一共要付65塊。",
], title="C. 對不對")

# ---- III. Create Dialogue Pairs ----
H("h3", "III. Create Dialogue Pairs", "三、對話配對", level=3, pages=[26, 27])
X("h3-x", "Match the sentence on the left with the appropriate reply on the right; write the matching letter in each blank.", [
  "（　）你喝幾杯茶？　　　(D) 新的。",
  "（　）這支手機能不能照相？　　　(A) 一杯多。",
  "（　）這杯咖啡不熱。　　　(F) 我幫你微波。",
  "（　）請幫我加一點冰。　　　(C) 好的。",
  "（　）你喜歡新手機還是舊手機？　　　(E) 不能。",
  "（　）你要內用還是外帶？　　　(G) 外帶。",
  "（　）一個包子多少錢？　　　(B) 二十塊。",
  "（　）那支舊手機怎麼樣？　　　(H) 不好看，也太舊了。",
], title="句子配對")

# ---- IV. Fill in the Blanks ----
H("h4", "IV. Fill in the Blanks", "四、填空", level=3, pages=[27])
T("h4a-t", "A. Fill in the blanks using the words provided: a. 塊　b. 杯　c. 喝　d. 吃　e. 個　f. 支")
X("h4a-x", "Fill in each blank with the appropriate word.", [
  "我和哥哥都很喜歡＿＿＿＿＿＿臺灣的包子。",
  "我喜歡＿＿＿＿＿＿烏龍茶，可是哥哥喜歡喝咖啡。",
  "明天早上我想買五＿＿＿＿＿＿包子，也要買一＿＿＿＿＿＿熱咖啡。",
  "這＿＿＿＿＿＿手機不便宜，一共要三千＿＿＿＿＿＿錢。",
], title="A. 填空")

T("h4b-t", "B. What do you think about these two cell phones below?",
  "手機一：舊手機，能上網，不能照相，980元。",
  "手機二：新手機，能上網，也能照相，12800元。")
X("h4b-x", "Complete the sentences about each phone and the short dialogue below.", [
  "手機一能＿＿＿＿＿＿，不能＿＿＿＿＿＿。",
  "手機二能＿＿＿＿＿＿，也能＿＿＿＿＿＿。",
  "A：你覺得手機一好不好？　B：我覺得手機一＿＿＿＿＿＿。",
  "A：你覺得手機二貴不貴？　B：我覺得手機二＿＿＿＿＿＿。",
], title="B. 兩支手機")

# ---- V. Rearrange the Characters ----
H("h5", "V. Rearrange the Characters Below to Make Good Sentences", "五、重組句子", level=3, pages=[27, 28])
X("h5-x", "Rearrange the given characters into a correct sentence.", [
  "這支　太貴了　手機　我覺得　→ ＿＿＿＿＿＿。",
  "能上網　這種　能照相　手機　也　→ ＿＿＿＿＿＿。",
  "幫　微波　請　我　→ ＿＿＿＿＿＿。",
  "想　姐姐　買　一支　新手機　→ ＿＿＿＿＿＿。",
  "那支　能　不　舊手機　上網　→ ＿＿＿＿＿＿。",
])

# ---- VI. Write Out in Chinese Characters ----
H("h6", "VI. Write Out in Chinese Characters", "六、聽寫漢字", level=3, pages=[28])
T("h6-t",
  "Practice exercise written for this site using Lesson 4 vocabulary. The book's own dictation exercise is on book p. 28; its recording is track 04-05.",
  track="04-05")
X("h6-x", "Listen to the recording and write out the sentences below in Chinese characters.", [
  "Kāfēi yě qǐng bāng wǒ wēibō.　→ ＿＿＿＿＿＿。",
  "Qǐngwèn zhè liǎng ge bāozi yào wàidài háishì nèiyòng?　→ ＿＿＿＿＿＿？",
  "Yì bēi kāfēi, sān ge bāozi, yígòng duōshǎo qián?　→ ＿＿＿＿＿＿？",
  "Wǒ gēge xiǎng mǎi yì zhī xīn shǒujī.　→ ＿＿＿＿＿＿。",
  "Tā nà zhī shǒujī tài jiù le.　→ ＿＿＿＿＿＿。",
])

# ---- VII. Complete the Dialogue ----
H("h7", "VII. Complete the Dialogue", "七、完成對話", level=3, pages=[28, 29])
T("h7a-t", "A. Complete the questions below based on the responses provided.")
X("h7a-x", "Write a question that fits the given answer.", [
  "A：請問＿＿＿＿＿＿＿＿＿＿＿＿？　B：我要兩杯熱烏龍茶。",
  "A：請問你要＿＿＿＿＿＿＿＿＿＿＿＿還是＿＿＿＿＿＿＿＿＿＿＿＿？　B：我要外帶。",
  "A：請問＿＿＿＿＿＿＿＿＿＿＿＿？　B：一共一千兩百五十塊錢。",
  "A：請問＿＿＿＿＿＿＿＿＿＿＿＿？　B：我的手機能上網也能照相。",
  "A：請問＿＿＿＿＿＿＿＿＿＿＿＿？　B：一個包子賣25塊。",
], title="A. 完成問句")

T("h7b-t", "B. The following is a conversation between customer 小林 and a shopkeeper. Complete the dialogue based on the information given.",
  "籃球 720元；排球 480元；羽球拍 560元；桌球拍 350元")
X("h7b-x", "Fill in the blanks using the price list above.", [
  "小林：我想買一個排球，請問一個多少錢？",
  "老闆：＿＿＿＿＿＿＿＿＿＿＿＿。",
  "小林：太貴了。",
  "老闆：好，＿＿＿＿＿＿＿＿＿＿＿＿。（400）",
], title="B. 買東西")

# ---- VIII. Composition ----
H("h8", "VIII. Composition", "八、短文寫作", level=3, pages=[29])
T("h8-t",
  "Write a paragraph explaining what you can order with NT$100 based on the prices below.",
  "我有一百塊錢可以買……",
  "奶茶 45元；三明治 55元；蛋餅 一個20塊錢")
X("h8-x", "Write 2–3 sentences about what you would order with NT$100 using the price list above.", [
  "你想買什麼？",
  "一共多少錢？",
], title="短文")
