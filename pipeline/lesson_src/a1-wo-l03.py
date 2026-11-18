LESSON_ID = "a1-wo-l03"
TITLE = "週末做什麼？ What Are You Doing Over the Weekend?"
STATUS = "complete"
DETAIL = ("Materi ini ditulis ulang secara orisinal untuk situs ini berdasarkan topik dan kosakata Pelajaran 3 "
          "buku kerja (hlm. buku 17–24): soal latihan, kalimat contoh, bacaan, dan kunci memakai kata-kata sendiri. "
          "Soal bergambar asli ada di buku; audio trek asli tetap ditautkan.")

H("h-obj", "Learning Objectives", "學習目標", pages=[17])
T("obj",
  "Topic: 週末活動 Weekend Activities",
  "• Practicing tone recognition for Lesson 3 vocabulary.",
  "• Practicing listening/reading comprehension about hobbies and weekend routines.",
  "• Practicing 也/都/常 and writing a short paragraph about one's own weekend.")

# ---- I. Differentiating Tones ----
H("h1", "I. Differentiating Tones", "一、辨別聲調", level=3, pages=[17])
T("h1-t",
  "Practice exercise written for this site using Lesson 3 vocabulary. The book's own tone-marking exercise is on book p. 17; its recording is track 03-01.",
  track="03-01")
add({"type": "table", "id": "h1-tab", "head": ["中文", "Pinyin (fill in the tone marks)"], "rows": [
  ["週末", "zhoumo"],
  ["網球", "wangqiu"],
  ["游泳", "youyong"],
  ["喜歡", "xihuan"],
  ["好玩", "haowan"],
  ["電影", "dianying"],
  ["籃球", "lanqiu"],
  ["晚飯", "wanfan"],
  ["一起", "yiqi"],
  ["覺得", "juede"],
]}, pages=[17])

# ---- II. Listen and Respond ----
H("h2", "II. Listen and Respond: What Are They Doing?", "二、請聽並回答：他們在做什麼", level=3, pages=[17, 18])
T("h2-t",
  "Practice exercise written for this site using Lesson 3 vocabulary. The book's own listening exercises are on book pp. 17–18; their recordings are tracks 03-02, 03-03 and 03-04.")

T("h2a-t", "A. Read about each person and choose what they like to do. (track 03-02)",
  track="03-02")
X("h2a-x", "Choose the correct answer for each question.", [
  "林先生喜歡做什麼？ a. 聽音樂　b. 彈鋼琴",
  "王小姐喜歡做什麼？ a. 上網　b. 打網球",
  "李先生喜歡做什麼？ a. 看電影　b. 看電視",
], title="A. 他們喜歡做什麼")

T("h2b-t", "B. Read about Miss Chen's weekend and number the activities below in the order she mentions them (1–4). (track 03-03)",
  "我週末常常先去游泳，游泳以後跟家人吃飯，吃飯以後和哥哥打籃球，最後看足球比賽。",
  track="03-03")
X("h2b-x", "Write the correct order (1–4) in front of each activity.", [
  "（　）打籃球",
  "（　）游泳",
  "（　）看足球比賽",
  "（　）吃飯",
], title="B. 陳小姐的週末")

T("h2c-t", "C. Listen to the questions below and choose an appropriate answer for each. (track 03-04)", track="03-04")
X("h2c-x", "Choose the most appropriate answer for each question.", [
  "你週末想做什麼？ a. 我想去游泳。　b. 我常打網球。　c. 我不喜歡看電影。",
  "你覺得打籃球好玩嗎？ a. 我想學中文。　b. 好玩！　c. 好啊！",
  "我們去吃晚飯，好不好？ a. 我也要去。　b. 歡迎你來。　c. 我也喜歡。",
  "你喜不喜歡看電影？ a. 我不想看電影。　b. 我想看電影。　c. 電影，我覺得很好看。",
  "我們去打網球，怎麼樣？ a. 我們打網球吧！　b. 我們打網球呢！　c. 我們打網球嗎？",
], title="C. 問答")

# ---- III. Create Dialogue Pairs ----
H("h3", "III. Create Dialogue Pairs", "三、對話配對", level=3, pages=[18, 19])
X("h3-x", "Match the sentence on the left with the appropriate reply on the right; write the matching letter in each blank.", [
  "（　）他週末常做什麼？　　　(C) 我也喜歡。",
  "（　）你是臺灣人，他呢？　　(F) 他也是臺灣人。",
  "（　）你喜歡聽音樂嗎？　　　(A) 他常去游泳。",
  "（　）今天晚上你想看書還是上網？　(E) 看書。",
  "（　）你喜歡做什麼？　　　　(B) 我想學中文。",
  "（　）我想吃臺灣菜。　　　　(H) 我們吃日本菜吧！",
  "（　）我們看臺灣電影吧！　　(D) 好啊！",
  "（　）你覺得打籃球好玩嗎？　(G) 打網球，我覺得很好玩。",
], title="句子配對")

# ---- IV. Reading Comprehension ----
H("h4", "IV. Reading Comprehension", "四、閱讀理解", level=3, pages=[19])
T("h4a-t",
  "Read the paragraph and complete the table below.",
  "我家有五個人，爸爸、媽媽、姐姐、弟弟和我。爸爸喜歡上網和照相，他週末常去照相。媽媽很喜歡看電視。我家有很多CD，都是姐姐的CD，她很喜歡聽音樂。弟弟喜歡看電影，也喜歡打籃球。我呢？我喜歡游泳和打網球，我和姐姐週末常常一起去打網球。")
add({"type": "table", "id": "h4a-tab", "head": ["我的家", "喜歡做的事"], "rows": [
  ["1. 爸爸", "＿＿＿＿＿＿＿＿＿＿"],
  ["2. 媽媽", "＿＿＿＿＿＿＿＿＿＿"],
  ["3. 姐姐", "＿＿＿＿＿＿＿＿＿＿"],
  ["4. 我", "＿＿＿＿＿＿＿＿＿＿"],
  ["5. 弟弟", "＿＿＿＿＿＿＿＿＿＿"],
]}, pages=[19])

# ---- V. Fill in the Blanks ----
H("h5", "V. Fill in the Blanks", "五、填空", level=3, pages=[20])
T("h5a-t", "A. Fill in the blanks with the appropriate character: 都, 吧, 也, 也都, or 去 to complete the dialogue.")
X("h5a-x", "Fill in each blank to complete the dialogue.", [
  "A：你是臺灣人，她呢？　B：她＿＿＿＿＿＿是臺灣人。",
  "A：你們喜歡游泳嗎？　B：我們＿＿＿＿＿＿很喜歡游泳。",
  "A：明天我們去看電影，好不好？　B：我們＿＿＿＿＿＿看電視＿＿＿＿＿＿。",
  "A：我喜歡聽音樂和看電影。　B：音樂、電影，我＿＿＿＿＿＿喜歡。",
  "A：週末你常做什麼？　B：我常＿＿＿＿＿＿打籃球。",
], title="A. 完成對話")

# ---- VI. Rearrange the Characters ----
H("h6", "VI. Rearrange the Characters Below to Make Good Sentences", "六、重組句子", level=3, pages=[20])
X("h6-x", "Rearrange the given characters into a correct sentence.", [
  "弟弟　也　很　聰明　→ ＿＿＿＿＿＿。",
  "也　聽　音樂　常　我　→ ＿＿＿＿＿＿。",
  "我們　都　常　上網　很　→ ＿＿＿＿＿＿。",
  "他們　臺灣菜　去　要　吃　週末　→ ＿＿＿＿＿＿。",
  "我　下午　明天　不　想　去　游泳　→ ＿＿＿＿＿＿。",
])

# ---- VII. Write Out in Chinese Characters ----
H("h7", "VII. Write Out in Chinese Characters", "七、聽寫漢字", level=3, pages=[20, 21])
T("h7-t",
  "Practice exercise written for this site using Lesson 3 vocabulary. The book's own dictation exercise is on book p. 20; its recording is track 03-05.",
  track="03-05")
X("h7-x", "Listen to the recording and write out the sentences below in Chinese characters.", [
  "Wǒ cháng kàn diànyǐng yě cháng shàngwǎng.　→ ＿＿＿＿＿＿。",
  "Tā bù xǐhuān dǎ bàngqiú.　→ ＿＿＿＿＿＿。",
  "Tāmen dōu xiǎng xué Zhōngwén.　→ ＿＿＿＿＿＿。",
  "Tā cháng dǎ lánqiú hàn yóuyǒng.　→ ＿＿＿＿＿＿。",
  "Wǎnshàng yìqǐ chī wǎnfàn, hǎo ma?　→ ＿＿＿＿＿＿？",
])

# ---- VIII. Complete the Dialogue ----
H("h8", "VIII. Complete the Dialogue", "八、完成對話", level=3, pages=[21])
X("h8-x", "Fill in the missing line of each short dialogue.", [
  "A：＿＿＿＿＿＿＿＿＿＿＿＿？　B：週末我想去打網球。",
  "A：你覺得游泳好玩嗎？　B：＿＿＿＿＿＿＿＿＿＿＿＿。",
  "A：你想今天還是明天去看電影？　B：＿＿＿＿＿＿＿＿＿＿＿＿。",
  "A：＿＿＿＿＿＿＿＿＿＿＿＿？　B：籃球、網球，我都想打。",
  "A：我們明天去游泳，怎麼樣？　B：＿＿＿＿＿＿＿＿＿＿＿＿。",
])

# ---- IX. Writing Exercises ----
H("h9", "IX. Writing Exercises", "九、寫作練習", level=3, pages=[22, 23])
T("h9a-t",
  "A. Read the information about each family member below and complete the paragraph.",
  "家人與他們喜歡做的事：爸爸——游泳；媽媽——看電影；姐姐——打網球；妹妹——聽音樂；我——打籃球；哥哥——覺得打棒球很好玩。")
X("h9a-x", "Complete the paragraph below using the information above.", [
  "這是我的家人。週末我爸爸常＿＿＿＿＿＿＿＿＿＿，媽媽喜歡＿＿＿＿＿＿＿＿＿＿，姐姐喜歡＿＿＿＿＿＿＿＿＿＿，妹妹喜歡＿＿＿＿＿＿＿＿＿＿，我常去＿＿＿＿＿＿＿＿＿＿，哥哥覺得＿＿＿＿＿＿＿＿＿＿很好玩。我家人都喜歡＿＿＿＿＿＿＿＿＿＿。",
], title="A. 完成短文")

T("h9b-t", "B. Composition (about 50 characters).",
  "寫一篇短文，介紹你自己，也要說有空的時候你常做什麼？週末你常做什麼？ (Write a short paragraph about yourself. Talk about what you usually do in your free time and on weekends.)")
X("h9b-x", "Write your own short composition using the prompt above.", [
  "你有空的時候常做什麼？",
  "你週末常做什麼？",
], title="B. 短文寫作")
