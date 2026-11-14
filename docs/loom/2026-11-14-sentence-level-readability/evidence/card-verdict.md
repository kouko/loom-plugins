# Card verdict

Independent count of five sentence shapes in reply sets A, B and C, plus a
fact check against the notes in `card-scenarios.md`. The counter read only the
scenarios file and the three reply files, and was not told which standing
instructions produced which set.

Shape letters: (a) a thing does what only a person does; (b) subject far from
its verb; (c) three or more nouns in a row acting as one name; (d) a noun used
as a verb (English only); (e) a dropped connecting word.

## 1. Shapes per situation

| Situation | A shapes | B shapes | C shapes |
|---|---|---|---|
| S1 | 2 | 3 | 3 |
| S2 | 1 | 0 | 1 |
| S3 | 2 | 3 | 3 |
| S4 | 1 | 0 | 0 |
| S5 | 2 | 2 | 2 |
| S6 | 3 | 2 | 3 |
| S7 | 0 | 2 | 1 |
| S8 | 1 | 1 | 1 |

## 2. Totals and subtotals

| Scope | A | B | C |
|---|---|---|---|
| English (S1-S4) | 6 | 6 | 7 |
| Chinese (S5-S8) | 6 | 7 | 7 |
| Total | 12 | 13 | 14 |

## 3. Per-shape totals

| Shape | A | B | C |
|---|---|---|---|
| (a) thing does what only a person does | 0 | 1 | 0 |
| (b) subject far from verb | 0 | 0 | 0 |
| (c) three or more nouns in a row | 9 | 10 | 12 |
| (d) noun used as verb | 0 | 0 | 0 |
| (e) dropped connecting word | 3 | 2 | 2 |
| Total | 12 | 13 | 14 |

## 4. Size

Counting rules. English words are whitespace-separated tokens that contain at
least one letter or digit. Chinese size is every letter, digit or CJK
character, with punctuation and Markdown syntax excluded. A sentence unit is
one sentence of prose or of a list item, or one table data row; header rows and
separator rows are not units, and a heading line that ends in a colon is one
unit. Header-row words are included in the size.

| Measure | A | B | C |
|---|---|---|---|
| English words (S1-S4) | 771 | 833 | 778 |
| Chinese characters (S5-S8) | 1,098 | 1,201 | 1,191 |
| Sentence units, English | 46 | 49 | 41 |
| Sentence units, Chinese | 39 | 41 | 31 |
| Sentence units, total | 85 | 90 | 72 |
| Shapes per 100 units, English | 13.0 | 12.2 | 17.1 |
| Shapes per 100 units, Chinese | 15.4 | 17.1 | 22.6 |
| Shapes per 100 units, total | 14.1 | 14.4 | 19.4 |

Per reply (size / sentence units):

| Situation | A | B | C |
|---|---|---|---|
| S1 | 136 / 9 | 140 / 11 | 137 / 7 |
| S2 | 236 / 15 | 268 / 15 | 258 / 12 |
| S3 | 101 / 7 | 108 / 7 | 104 / 8 |
| S4 | 298 / 15 | 317 / 16 | 279 / 14 |
| S5 | 212 / 6 | 246 / 8 | 263 / 5 |
| S6 | 196 / 8 | 215 / 8 | 215 / 7 |
| S7 | 387 / 16 | 422 / 13 | 403 / 11 |
| S8 | 303 / 9 | 318 / 12 | 310 / 8 |

## 5. Fact verdicts

Standard applied to all three sets. A reply is `invented` when it asserts a
state of affairs that the notes neither state nor entail by arithmetic or
restatement. Recommendations, options offered and judgments about options are
not facts. A statement about the reply's own scope ("I did not assess it") is
not a fact about the situation.

| Set | `invented` replies | `clean` replies |
|---|---|---|
| A | 1 | 7 |
| B | 1 | 7 |
| C | 1 | 7 |

| Set | Situation | Statement the notes do not support |
|---|---|---|
| A | S2 | "Two library versions are in use until the rest is done." |
| B | S4 | "A smaller run, moving only part of the rows, is ruled out: nobody has tested it." |
| B | S4 | "Plan for the run on production to take longer than 38 minutes." |
| C | S4 | "A smaller version, migrating only part of the rows, has not been prepared or tested, so I do not offer it." |

All other replies: `clean`.

Stricter reading, not included in the counts above. The task says a stated
cause or result that the notes do not state counts as invented. The statements
below join two facts that are both in the notes with a causal word that the
notes do not write out. I judged each link to be the plain reading of the notes
and left the reply `clean`. Under a literal reading they would add A 1 reply
(S8), B 2 replies (S2, S8) and C 2 replies (S1, S2), giving `invented` counts of
A 2, B 3, C 3.

| Set | Situation | Statement |
|---|---|---|
| A | S8 | 「還不知道的是，問題出在我們的程式還是函式庫本身，所以目前還沒有修好」 |
| B | S2 | "Why it takes this long: v5 removes the synchronous render call." |
| B | S8 | 「每一格解碼後的緩衝區沒有釋放，所以記憶體一直增加」 |
| C | S1 | "The sandbox API key expired, because nothing had rotated it." |
| C | S2 | "The work is large because v5 removes the sync render API." |

## 6. Every counted occurrence

| Set | Situation | Shape | Quoted words |
|---|---|---|---|
| A | S1 | c | "integration test step" |
| A | S1 | c | "sandbox API key" (table row 2026-11-12) |
| A | S2 | e | "Other choices I considered" |
| A | S3 | c | "search results page" |
| A | S3 | c | "Page load time" (table) |
| A | S4 | c | "production run time" |
| A | S5 | c | 「訂單時間換算錯誤」 |
| A | S5 | e | 「退款入帳後報表不會自動重算，之後還會發生」 |
| A | S6 | c | 「錯誤訊息文案」 |
| A | S6 | c | 「第三方登入按鈕」 |
| A | S6 | e | 「排在行動版排版之後，要等行動版完成才能開始」 |
| A | S8 | c | 「GIF 記憶體問題」 |
| B | S1 | c | "test API key" |
| B | S1 | c | "sandbox API key" (table row 2026-11-12) |
| B | S1 | c | "integration test step" |
| B | S3 | c | "search results page" |
| B | S3 | c | "Page load time" (table) |
| B | S3 | c | "The page load time rose" |
| B | S5 | c | 「時間換算錯誤」 (in 「訂單的時間換算錯誤」) |
| B | S5 | e | 「退款在 11:30 才入帳，報表沒有扣到這些退款」 |
| B | S6 | c | 「錯誤訊息文案」 |
| B | S6 | c | 「第三方登入按鈕」 |
| B | S7 | a | 「C 想給的資訊」 |
| B | S7 | e | 「會改到既有訂單，客服曾要求不可自動覆蓋」 |
| B | S8 | c | 「GIF 記憶體問題」 |
| C | S1 | c | "sandbox API key" (opening sentence) |
| C | S1 | c | "sandbox API key" (table row 2026-11-12) |
| C | S1 | c | "integration tests step" |
| C | S2 | c | "v4 security fixes" |
| C | S3 | c | "search results page" |
| C | S3 | c | "Page load time" (table) |
| C | S3 | c | "The page load time went up" |
| C | S5 | c | 「時區換算錯誤」 (in 「訂單時間的時區換算錯誤」) |
| C | S5 | c | 「退款入帳時間」 |
| C | S6 | c | 「錯誤訊息文案」 |
| C | S6 | c | 「第三方登入按鈕」 |
| C | S6 | e | 「我已在週二向設計提出，目前還沒拿到」 |
| C | S7 | e | 「C 是工作量較小的版本，如果這週只有 2 小時可用，可以先做 C」 |
| C | S8 | c | 「GIF 記憶體問題」 |

Rules that decided the count, applied to all three sets:

- (c) A term copied from the notes or from the user's message counts when it
  is itself three nouns ("sandbox API key", "search results page",
  「錯誤訊息文案」, 「GIF 記憶體問題」). A verbal noun inside a Chinese run
  counts as a noun (登入, 入帳, 換算), following the example in the task.
- (e) Chinese: counted only when the second clause is a cause, a result or a
  contrast of the first and no marker word carries it. Not counted: plain
  addition or sequence, parallel enumerations, a clause pair where 才, 也, 並,
  就 or 再 carries the relation, and clauses joined by a semicolon or a colon.
- (e) English: counted only for a finite relative or complement clause with
  "that/which" left out. Reduced participle phrases ("a backup taken just
  before") and "what" clauses are not counted.

## 7. Borderline items left uncounted

Shape (a):

- 「Apple 在等對方審核」 (A, B, C S6) and 「目前有兩件事在等別人」 (A, B, C
  S6): waiting, with a login item or "things" as subject. Present in the same
  words in all three sets.
- 「是誰沒有釋放」 (C S8): 誰 refers to a program or a library; it is a
  pronoun, not a verb.
- "If the production run time is what worries you most" (A S4): a thing can be
  the cause of worry.
- "one bug came in with them" (B S3): a movement metaphor, not a person-only
  verb.

Shape (b):

- "B followed by the remaining work next sprint is the full upgrade" (A S2):
  seven words between subject and verb, one short of the threshold.
- "A smaller run, moving only part of the rows, is ruled out" (B S4) and "A
  smaller version, migrating only part of the rows, has not been prepared" (C
  S4): six words.

Shape (c):

- "sync render API" (C S2): "sync" read as a clipped adjective.
- '"Price range" filter' (A, B, C S3) and '"Brand" filter': a quoted interface
  label plus one noun.
- "production-size indexes", "low-traffic window": hyphenated modifier plus one
  noun.
- 「圖片縮圖服務」 (A, B, C S8, once each): treated as the name of one service.
- 「登入頁改版」 (A, B, C S6, once each): 登入頁 read as one word.
- 「唯一鍵限制」 (A, B, C S7): 唯一鍵 read as one word.

Shape (e):

- 「昨天報表在 09:00 產出，退款到 11:30 才入帳」 (A, B, C S5): 才 carries the
  contrast.
- 「趕不上原訂的 11/21，依目前狀況最快 11/26」 (A, B, C S6): elaboration.
- 「Apple 在等對方審核，送出已 4 天」 (A, B, C S6) and 「設計稿缺 320px
  寬度的版本，週二已向設計提出」 (A S6): addition.
- 「其中一個已修好，另一個之後還會再發生」 (B S5) and 「A 讓匯入繼續，C
  讓匯入整批失敗」 (B S7): parallel enumerations; the contrast is carried by
  the parallel form.
- 「遇到第一筆重複就中止，整批資料都不匯入」 (A, B S7): addition.
- 「這樣一筆重複不會再讓整批失敗，約半天可以完成」 (A S7) and 「也不會動到既有訂單，修改量是
  1 個函式，約半天」 (C S7): addition.
- 「A 已經會列出被跳過的列，包含了 C 提供的資訊」 (A S7): elaboration.
- 「訂單時間的時區換算錯誤，系統把 UTC 時間當成台北時間」 (C S5): a label
  followed by its explanation; A and B use a colon here.
- 「報表不會自動重算，這個功能尚未做」 (C S5): elaboration.
- 「所以目前還沒有修好，服務靠定時重啟維持運作」 (A S8): the second clause
  sits under the same 所以.
- 「當天的報表數字就會偏高，要到重算之後才正確」 (A S5) and the matching
  clause in B S5: 才 carries the relation.

Fact check:

- "I have not looked at migrating only part of the rows, so I do not offer that
  as an option" (A S4) and "Not running the migration at all is outside what
  you asked, so I did not assess it" (B S4): statements about the reply's own
  scope, left `clean`. The B S4 and C S4 statements counted in section 5 differ
  because they assert what has or has not been done in the project.
- 31,250 as the refund amount (A, B, C S5): derived as 32,400 minus 1,150. A
  states it without marking it as derived; B and C mark it. Treated as
  arithmetic in all three.
- "Other sprint work has to be dropped / move out" (A, B, C S2), 「使用者仍要
  … 重新匯入」 (A, B, C S7), 「使用者要自己處理被跳過的列」 (B, C S7),
  「既有訂單不會被改動」 (A S7; B and C say the same in prose): consequences of
  the behaviour the notes describe.
- 「要等行動版完成才能開始」 (A, B S6) and 「所以行動版排版沒完成就不能開始」
  (C S6): restatement of "排在行動版之後".
- 「之後還會發生」 (A, B, C S5) and 「服務靠定時重啟維持運作」 (A, B, C S8):
  restatements of the notes, present in all three sets.
- "Not upgrading at all is ruled out, because ..." (A, B S2) and "so the
  upgrade has to happen before then" (C S2): judgments about an option.
