LESSON_ID = "a1-wo-l01"
TITLE = "歡迎你來臺灣！ Welcome to Taiwan!"
STATUS = "complete"
DETAIL = ("Materi ini ditulis ulang secara orisinal untuk situs ini berdasarkan topik dan kosakata Pelajaran 1 "
          "buku ajar (hlm. buku 1–8): soal latihan, kalimat contoh, dan kunci memakai kata-kata sendiri. "
          "Soal bergambar asli ada di buku; audio trek asli tetap ditautkan.")

H("h-obj", "Learning Objectives", "學習目標", pages=[1])
T("obj",
  "Topic: 歡迎與自我介紹 Greetings and Self-Introduction",
  "• Practicing tone recognition for Lesson 1 vocabulary.",
  "• Practicing listening comprehension about greetings, nationality and likes/dislikes.",
  "• Practicing the A-not-A question pattern, word order, and writing characters from pinyin.",
  "• Practicing a short self-introduction.")

# ---- I. Differentiating Tones ----
H("h1", "I. Differentiating Tones", "一、辨別聲調", level=3, pages=[1])
T("h1-t",
  "Practice exercise written for this site using Lesson 1 vocabulary. The book's own tone-marking exercise is on book p. 1; its recording is track 01-01.",
  track="01-01")
add({"type": "table", "id": "h1-tab", "head": ["中文", "Pinyin (fill in the tone marks)"], "rows": [
  ["你好", "nihao"],
  ["謝謝", "xiexie"],
  ["喜歡", "xihuan"],
  ["臺灣", "Taiwan"],
  ["美國", "Meiguo"],
  ["日本", "Riben"],
  ["咖啡", "kafei"],
  ["先生", "xiansheng"],
  ["小姐", "xiaojie"],
  ["請問", "qingwen"],
]}, pages=[1])

# ---- II. Listen and Respond ----
H("h2", "II. Listen and Respond: Nice to Meet You", "二、請聽並回答：很高興認識你", level=3, pages=[1, 2])
T("h2-t",
  "Practice exercise written for this site using Lesson 1 vocabulary. The book's own listening exercises are on book pp. 1–2; their recordings are tracks 01-02, 01-03 and 01-04.")

T("h2a-t", "A. Listen to what is said about Miss Chen and choose the correct answer to each question below. (track 01-02)", track="01-02")
X("h2a-x", "Choose the correct answer for each question.", [
  "陳小姐喜歡喝什麼？ a. 茶　b. 咖啡",
  "陳小姐是不是日本人？ a. 是　b. 不是",
  "陳小姐喜不喜歡喝烏龍茶？ a. 喜歡　b. 不喜歡",
], title="A. 陳小姐")

T("h2b-t", "B. I would like to know more about Mr. Wu and Miss Lin. Write the appropriate letters in the parentheses below. (a. 吳先生　b. 林小姐　c. 臺灣人　d. 美國人 — track 01-03)", track="01-03")
X("h2b-x", "Write the appropriate letter in each blank.", [
  "（　）喜歡喝咖啡。",
  "（　）喜歡喝茶。",
  "吳先生是（　）。",
  "林小姐是（　）。",
], title="B. 吳先生、林小姐")

T("h2c-t", "C. Listen to the dialogue. Write ○ if the statement is true, × if it is false. (track 01-04)", track="01-04")
X("h2c-x", "Mark each statement ○ (true) or × (false).", [
  "（　）林小姐是臺灣人。",
  "（　）林小姐叫美美。",
  "（　）吳先生叫開文。",
  "（　）林小姐歡迎吳先生。",
], title="C. 對不對")

# ---- III. Create Dialogue Pairs ----
H("h3", "III. Create Dialogue Pairs", "三、對話配對", level=3, pages=[2, 3])

X("h3a-x", "Match the sentence on the left with the appropriate reply on the right; write the matching letter in each blank.", [
  "（　）你是不是美國人？　　　(A) 謝謝你。",
  "（　）歡迎你來臺灣。　　　　(B) 我姓林。",
  "（　）你喜歡喝茶嗎？　　　　(C) 謝謝。",
  "（　）你貴姓？　　　　　　(D) 不喜歡，謝謝。",
], title="A. 句子配對")

T("h3b-t", "B. Complete the greetings and replies based on the information provided: a. 你好！　b. 謝謝你。　c. 不客氣。　d. 我是臺灣人。")
X("h3b-x", "Fill in the blank with the matching reply.", [
  "A：你好！　B：＿＿＿＿＿＿",
  "A：你是哪國人？　B：＿＿＿＿＿＿",
  "A：請喝茶。　B：＿＿＿＿＿＿",
  "A：謝謝你歡迎我。　B：＿＿＿＿＿＿",
], title="B. 完成對話")

# ---- IV. Reading Comprehension ----
H("h4", "IV. Reading Comprehension", "四、閱讀理解", level=3, pages=[4])

T("h4a-t",
  "A. Introduce yourself and your friends. Read the paragraph and answer the questions below.",
  "我姓林，叫開文。我是臺灣人。我很喜歡喝烏龍茶。臺灣烏龍茶很好喝。他姓王，叫大同。他是美國人，他很喜歡喝咖啡。美國咖啡很好喝。我們喜歡臺灣。")
add({"type": "table", "id": "h4a-tab", "head": ["", "叫什麼", "哪國人", "喜歡喝什麼", "什麼好喝"], "rows": [
  ["林先生", "＿＿＿＿", "＿＿＿＿", "＿＿＿＿", "＿＿＿＿"],
  ["王先生", "＿＿＿＿", "＿＿＿＿", "＿＿＿＿", "＿＿＿＿"],
]}, pages=[4])

T("h4b-t",
  "B. Look at the name card below and complete the dialogue.",
  "國立臺灣師範大學國語教學中心　王開文　主編　10610臺北市和平東路一段129號",
  "a. 王　b. 主編　c. 開文　d. 王開文")
X("h4b-x", "Complete each answer using the name card above.", [
  "他姓什麼？　他姓＿＿＿＿＿＿。",
  "他叫什麼？　他叫＿＿＿＿＿＿。",
], title="B. 名片問答")

# ---- V. Practicing the "A-not-A" Pattern ----
H("h5", "V. Practicing the \"A-not-A\" Pattern", "五、練習「A不A」句型", level=3, pages=[5])
T("h5-t", "Write out each question using the \"A-not-A\" pattern and give a negative answer.")
add({"type": "table", "id": "h5-tab", "head": ["", "A-not-A", "Answer"], "rows": [
  ["Example：我姓林。", "你姓不姓林？", "我不姓林。"],
  ["1. 他是日本人。", "＿＿＿＿＿＿？", "＿＿＿＿＿＿。"],
  ["2. 臺灣人喜歡喝咖啡。", "＿＿＿＿＿＿？", "＿＿＿＿＿＿。"],
  ["3. 這是普洱茶。", "＿＿＿＿＿＿？", "＿＿＿＿＿＿。"],
  ["4. 她要喝烏龍茶。", "＿＿＿＿＿＿？", "＿＿＿＿＿＿。"],
]}, pages=[5])

# ---- VI. Rearrange the Characters ----
H("h6", "VI. Rearrange the Characters Below to Make Good Sentences", "六、重組句子", level=3, pages=[5, 6])
X("h6-x", "Rearrange the given characters into a correct sentence.", [
  "美國人　不是　你　是　請問　→ ＿＿＿＿＿＿？",
  "很　好喝　普洱茶　→ ＿＿＿＿＿＿。",
  "喝　喜歡　很　咖啡　我　→ ＿＿＿＿＿＿。",
  "是　林小姐　嗎　臺灣人　不　→ ＿＿＿＿＿＿？",
  "你　臺灣　來　歡迎　→ ＿＿＿＿＿＿。",
])

# ---- VII. Write Out in Chinese Characters ----
H("h7", "VII. Write Out in Chinese Characters", "七、聽寫漢字", level=3, pages=[6])
T("h7-t",
  "Practice exercise written for this site using Lesson 1 vocabulary. The book's own dictation exercise is on book p. 6; its recording is track 01-05.",
  track="01-05")
X("h7-x", "Listen to the recording and write out the sentences below in Chinese characters.", [
  "Qǐngwèn nǐ shì Lín Xiǎojiě ma?　→ ＿＿＿＿＿＿？",
  "Xièxie nǐ lái huānyíng wǒmen.　→ ＿＿＿＿＿＿。",
  "Zhè shì Wú Xiānshēng.　→ ＿＿＿＿＿＿。",
  "Wǒ xǐhuān hē wūlóngchá, nǐ ne?　→ ＿＿＿＿＿＿？",
  "Huānyíng nǐmen lái Táiwān.　→ ＿＿＿＿＿＿。",
])

# ---- VIII. Sentence Completion ----
H("h8", "VIII. Sentence Completion", "八、句子完成", level=3, pages=[7])
T("h8-t", "Complete the sentences below to introduce yourself.")
X("h8-x", "Fill in each blank to write your own self-introduction.", [
  "你們好。我姓＿＿＿＿＿＿，叫＿＿＿＿＿＿。",
  "我是＿＿＿＿＿＿人。我喜歡喝＿＿＿＿＿＿，不喜歡喝＿＿＿＿＿＿。我很高興認識你們。",
])
