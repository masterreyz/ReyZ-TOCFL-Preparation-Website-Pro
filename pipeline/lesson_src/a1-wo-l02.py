LESSON_ID = "a1-wo-l02"
TITLE = "我的家人 My Family"
STATUS = "complete"
DETAIL = ("Materi ini ditulis ulang secara orisinal untuk situs ini berdasarkan topik dan kosakata Pelajaran 2 "
          "buku kerja (hlm. buku 9–15): soal latihan, kalimat contoh, bacaan, dan kunci memakai kata-kata sendiri. "
          "Soal bergambar asli ada di buku; audio trek asli tetap ditautkan.")

H("h-obj", "Learning Objectives", "學習目標", pages=[9])
T("obj",
  "Topic: 我的家人 Family Members",
  "• Practicing tone recognition for Lesson 2 vocabulary.",
  "• Practicing listening/reading comprehension about family size, members and what they like to do.",
  "• Practicing the measure words 個 and 張, and introducing one's own family in writing.")

# ---- I. Differentiating Tones ----
H("h1", "I. Differentiating Tones", "一、辨別聲調", level=3, pages=[9])
T("h1-t",
  "Practice exercise written for this site using Lesson 2 vocabulary. The book's own tone-marking exercise is on book p. 9; its recording is track 02-01.",
  track="02-01")
add({"type": "table", "id": "h1-tab", "head": ["中文", "Pinyin (fill in the tone marks)"], "rows": [
  ["看書", "kanshu"],
  ["漂亮", "piaoliang"],
  ["伯母", "bomu"],
  ["家人", "jiaren"],
  ["您好", "ninhao"],
  ["照片", "zhaopian"],
  ["房子", "fangzi"],
  ["老師", "laoshi"],
  ["兩個", "liangge"],
  ["姐姐", "jiejie"],
]}, pages=[9])

# ---- II. Listen and Respond ----
H("h2", "II. Listen and Respond: Family Introductions", "二、請聽並回答：我的家人", level=3, pages=[9, 10])
T("h2-t",
  "Practice exercise written for this site using Lesson 2 vocabulary. The book's own listening exercises are on book pp. 9–10; their recordings are tracks 02-02, 02-03 and 02-04.")

T("h2a-t", "A. Read about Mr. Zhang's family and choose what each person likes to do. (track 02-02)",
  "張先生的家人：張先生喜歡看書，張太太喜歡喝咖啡。張先生的女兒喜歡照相，兒子喜歡打籃球。",
  track="02-02")
X("h2a-x", "Choose the correct answer for each question.", [
  "張先生喜歡做什麼？ a. 看書　b. 喝咖啡　c. 打籃球",
  "張太太喜歡做什麼？ a. 看書　b. 喝咖啡　c. 照相",
  "張先生的女兒喜歡做什麼？ a. 看書　b. 打籃球　c. 照相",
  "張先生的兒子喜歡做什麼？ a. 看書　b. 打籃球　c. 照相",
], title="A. 張先生的家人")

T("h2b-t", "B. Read about Mr. Lin and Miss Chen. Write the appropriate letter in each blank. (a. 林先生　b. 陳小姐　c. 老師　d. 臺灣人 — track 02-03)",
  "林先生的爸爸是老師，他喜歡看書。陳小姐是臺灣人，她的伯母喜歡照相。",
  track="02-03")
X("h2b-x", "Write the appropriate letter in each blank.", [
  "（　）的爸爸是老師。",
  "（　）是臺灣人。",
  "林先生的爸爸是（　）。",
  "陳小姐的伯母喜歡（　）照相。",
], title="B. 林先生、陳小姐")

T("h2c-t", "C. Listen to the dialogue. Write ○ if the statement is true, × if it is false. (track 02-04)",
  "大衛：陳小姐，妳家有幾個人？",
  "陳小姐：我家有四個人，爸爸、媽媽、我和妹妹。",
  "大衛：你們家人都喜歡做什麼？",
  "陳小姐：我爸爸是老師，他喜歡看書。我媽媽喜歡喝茶，我喜歡照相，妹妹喜歡看電視。",
  track="02-04")
X("h2c-x", "Mark each statement ○ (true) or × (false).", [
  "（　）陳小姐家有四個人。",
  "（　）陳小姐的爸爸是老師。",
  "（　）陳小姐的媽媽喜歡照相。",
  "（　）陳小姐喜歡看電視。",
], title="C. 對不對")

# ---- III. Create Dialogue Pairs ----
H("h3", "III. Create Dialogue Pairs", "三、對話配對", level=3, pages=[10, 11])
X("h3-x", "Match the sentence on the left with the appropriate reply on the right; write the matching letter in each blank.", [
  "（　）這是誰？　　　(D) 不是，我爸爸是日本人。",
  "（　）王先生的家有幾個人？　　　(A) 不客氣。",
  "（　）你要不要喝咖啡？　　　(E) 是的，她是。",
  "（　）你爸爸媽媽都是臺灣人嗎？　　　(C) 不要，謝謝。",
  "（　）李小姐的媽媽是老師嗎？　　　(B) 五個。",
  "（　）你有沒有你家人的照片？　　　(H) 是的，他們都喜歡。",
  "（　）林先生的兄弟姐妹都喜歡看書嗎？　　　(F) 我哥哥。",
  "（　）謝謝你們來接我。　　　(G) 有，我有很多照片。",
], title="句子配對")

# ---- IV. Reading Comprehension ----
H("h4", "IV. Reading Comprehension", "四、閱讀理解", level=3, pages=[11])
T("h4a-t",
  "林大為 introduces his family. Read the paragraph and answer the questions below.",
  "你們好，我叫林大為，我家有五個人：爸爸、媽媽、哥哥、妹妹和我。我爸爸是老師，媽媽喜歡喝茶、看書。我哥哥喜歡打籃球，妹妹喜歡照相。我家有很多照片，也有很多書。")
X("h4-x", "Mark each statement ○ (true) or × (false).", [
  "（　）林大為的家有五個人。",
  "（　）林大為的爸爸是老師。",
  "（　）林大為的哥哥喜歡看書。",
  "（　）林大為家有很多照片。",
], title="對不對")

# ---- V. Fill in the Blanks ----
H("h5", "V. Fill in the Blanks", "五、填空", level=3, pages=[12, 13])
T("h5a-t", "A. Fill in the blanks using the words provided: a. 個　b. 的　c. 張")
X("h5a-x", "Fill in each blank with 個, 的, or 張.", [
  "林太太＿＿＿＿＿＿照片很漂亮。",
  "我有很多好看＿＿＿＿＿＿照片。",
  "陳小姐的家有六＿＿＿＿＿＿人。",
  "王先生有五＿＿＿＿＿＿照片。",
  "他有三＿＿＿＿＿＿妹妹。",
], title="A. 填空")

T("h5b-t", "B. 安同 Antong overhears two people talking about photos, but he misses some words. Can you help him?",
  "a. 哪　b. 誰　c. 幾　d. 兩　e. 坐　f. 都　g. 進　h. 照片　i. 照相　j. 好看")
X("h5b-x", "Fill in each blank using a word from the box above.", [
  "A：你家有＿＿＿＿＿＿個人？",
  "B：我家有＿＿＿＿＿＿個人，爸爸和我。",
  "A：你有沒有家人的＿＿＿＿＿＿？",
  "B：有，我家人都很＿＿＿＿＿＿。",
  "A：這張照片裡的人是＿＿＿＿＿＿？",
  "B：那是我哥哥，他喜歡＿＿＿＿＿＿。",
  "A：歡迎你＿＿＿＿＿＿來我家坐坐！",
], title="B. 完成對話")

# ---- VI. Rearrange the Characters ----
H("h6", "VI. Rearrange the Characters Below to Make Good Sentences", "六、重組句子", level=3, pages=[13])
X("h6-x", "Rearrange the given characters into a correct sentence.", [
  "很好看　你的　照片　→ ＿＿＿＿＿＿。",
  "都　我家人　喜歡　看電影　→ ＿＿＿＿＿＿。",
  "老師　都　我們　是　姓林的　→ ＿＿＿＿＿＿。",
  "兩個　陳小姐　哥哥　有　→ ＿＿＿＿＿＿。",
])

# ---- VII. Write Out in Chinese Characters ----
H("h7", "VII. Write Out in Chinese Characters", "七、聽寫漢字", level=3, pages=[13, 14])
T("h7-t",
  "Practice exercise written for this site using Lesson 2 vocabulary. The book's own dictation exercise is on book p. 13; its recording is track 02-05.",
  track="02-05")
X("h7-x", "Listen to the recording and write out the sentences below in Chinese characters.", [
  "Wǒ jiā yǒu wǔ ge rén.　→ ＿＿＿＿＿＿。",
  "Nǐ jiārén dōu xǐhuān kàn zhàopiàn ma?　→ ＿＿＿＿＿＿？",
  "Wǒ bàba shì lǎoshī.　→ ＿＿＿＿＿＿。",
  "Zhè zhāng zhàopiàn hěn piàoliang.　→ ＿＿＿＿＿＿。",
  "Nǐ yǒu jǐ ge jiějie?　→ ＿＿＿＿＿＿？",
])

# ---- VIII. Complete the Dialogue ----
H("h8", "VIII. Complete the Dialogue", "八、完成對話", level=3, pages=[14, 15])
X("h8-x", "Fill in the missing line of each short dialogue.", [
  "A：你家有幾個人？　B：＿＿＿＿＿＿＿＿＿＿＿＿。",
  "A：你爸爸是不是老師？　B：＿＿＿＿＿＿＿＿＿＿＿＿。",
  "A：＿＿＿＿＿＿＿＿＿＿＿＿？　B：這是我姐姐的照片。",
  "A：你哥哥喜歡做什麼？　B：＿＿＿＿＿＿＿＿＿＿＿＿。",
  "A：＿＿＿＿＿＿＿＿＿＿＿＿？　B：不是，是我妹妹。",
  "A：你有沒有家人的照片？　B：＿＿＿＿＿＿＿＿＿＿＿＿。",
])

# ---- IX. Picture Story ----
H("h9", "IX. Picture Story", "九、看圖寫作", level=3, pages=[15])
T("h9-t",
  "Use the new words below to introduce 李小姐's family in writing.",
  "李小姐的家：李小姐、李小姐的爸爸、李小姐的媽媽和李小姐的弟弟，一共四個人。他們坐在家門口，爸爸拿著一本書，媽媽拿著一杯茶，弟弟拿著一個照相機。",
  "都、喜歡、漂亮、看書、喝茶、照相")
X("h9-x", "Write 4–5 sentences introducing 李小姐's family using the word bank above.", [
  "李小姐的家有幾個人？他們是誰？",
  "他們喜歡做什麼？",
])
