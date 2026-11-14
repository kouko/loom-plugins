# Held-out verdict (final count)

Counted by an independent reader who saw only `heldout-samples.md`,
`heldout-rewrite-P.md` and `heldout-rewrite-S.md`. The reader was not told
which writing guide produced which set and did not look.

Shapes: (a) a thing does what only a person does; (b) subject far from its
verb; (c) three or more nouns in a row as one name; (d) noun used directly as
a verb (English only); (e) dropped connecting word.

## Counting rules applied to all three sets

- (b) English: count the words strictly between the head noun of a subject and
  its verb; eight or more counts. This is applied to every subject-verb pair,
  including one inside a subordinate clause. An adverb next to the verb
  ("never") is counted as an intervening word.
- (b) Chinese: count the characters of the pre-modifier that ends in 的 before
  the subject; about twenty or more counts. A subject followed directly by
  是 in a 是…的 sentence does not count.
- (c) A word that can be read as an adjective (weekly, daily, null, new,
  legacy, duplicate, 每日, 每週, 新, 重複, 慢速) is not counted as a noun.
  Three or more of the remaining nouns in a row count as one occurrence.
- (d) A word that is primarily a noun, used as a verb: "backlog", "sunset",
  "rubber-stamped".
- (e) Chinese: two full clauses with different subjects, joined by a comma
  with no connecting word, where a cause, result or contrast reading is
  plausible. A clause that only continues the same topic with a pointer word
  (那份, 這個) is not counted. A topic followed by a comma and its comment is
  one clause, not two.
- When unsure, the item was left uncounted in all three sets (section 7).

## 1. Counts per sample

| Sample | Original | P | S |
|---|---|---|---|
| EN1 | 6 | 2 | 2 |
| EN2 | 5 | 1 | 0 |
| EN3 | 5 | 1 | 1 |
| EN4 | 3 | 0 | 0 |
| ZH1 | 5 | 0 | 0 |
| ZH2 | 5 | 0 | 0 |
| ZH3 | 5 | 1 | 1 |
| ZH4 | 4 | 0 | 0 |

## 2. Totals and subtotals

| Scope | Original | P | S |
|---|---|---|---|
| English (EN1..EN4) | 19 | 4 | 3 |
| Chinese (ZH1..ZH4) | 19 | 1 | 1 |
| Total | 38 | 5 | 4 |

## 3. Totals per shape

| Shape | Original | P | S |
|---|---|---|---|
| (a) thing does a person's act | 12 | 0 | 0 |
| (b) subject far from verb | 7 | 3 | 3 |
| (c) noun stack | 7 | 2 | 1 |
| (d) noun as verb | 3 | 0 | 0 |
| (e) dropped connecting word | 9 | 0 | 0 |
| Total | 38 | 5 | 4 |

Occurrences counted in the originals:

- EN1: (a) "model ... hates"; (b) "the join that ... drops"; (b) "the analyst
  who rebuilt the weekly revenue report in October rewrote" (8 words);
  (c) "Daily revenue snapshot freshness check latency"; (d) "backlog";
  (e) "The orders model the dashboard reads".
- EN2: (a) "the importer trusts"; (a) "parser ... chokes"; (b) "The export
  that ... ran"; (c) "Vendor invoice duplicate match rate"; (e) "The date
  parser the importer trusts".
- EN3: (a) "scheduler forgets"; (a) "queue starves"; (c) "worker pool size
  limit change"; (d) "sunset"; (e) "The log the agent attached".
- EN4: (a) "cache believes"; (b) "The alert that ... never fires";
  (d) "rubber-stamped".
- ZH1: (a) 「訂單模型討厭」; (b) 「十月重做…而重寫的那個關聯查詢少了」;
  (c) 「每日營收快照新鮮度檢查延遲」; (e) 「…討厭空的門市編號，…少了 214
  筆資料」; (e) 「報表晚出，排程重跑了」.
- ZH2: (a) 「匯入程式信任」; (a) 「解析器被…噎住了」; (b) 「負責稅務帳本的
  財務團隊在 28 日季結前要求的那份匯出跑了」; (c) 「廠商發票重複比對比率」;
  (e) 「比對變快，索引重建了」.
- ZH3: (a) 「排程器…忘記了」; (a) 「佇列餓著」; (c) 「工作程序池大小上限變更
  上線流程」; (e) 「排程器重啟後忘記了工作，佇列餓著…」; (e) 「記錄檔顯示 17
  次逾時，舊橋接停用」.
- ZH4: (a) 「快取相信」; (b) 「八月當機後…設定的那個警示…不會觸發」;
  (c) 「退款通知寄送範本欄位對應」; (e) 「退款通知寄送範本欄位對應錯了，工單
  3172 沒關閉」.

## 4. Fact verdicts

| Sample | P | S |
|---|---|---|
| EN1 | kept | kept |
| EN2 | kept | kept |
| EN3 | kept | kept |
| EN4 | kept | kept |
| ZH1 | kept | kept |
| ZH2 | kept | kept |
| ZH3 | kept | kept |
| ZH4 | kept | kept |
| `changed` total | 0 | 0 |

Every number (214, 9, 3, 28th, 7%, 2%, 4, 17, 15, 500, 3172), name and
outcome of each original is present in both rewrites. The one added causal
link in P ZH1 is reported in section 5 only and is not also counted as a
changed fact.

## 5. Guessed relations

| Set | Count |
|---|---|
| P | 1 |
| S | 0 |

- P ZH1: 「有一個關聯查詢少了 214 筆資料，原因是儀表板讀取的訂單模型無法處理
  門市編號是空的訂單。」 The Chinese original joins these two clauses with a
  comma and states no relation.

Not counted as guesses, because the original states the relation:

- P EN1 and S EN1 "because" (original: "so").
- P EN1 and S EN1 "so that it uses" (original: "to use").
- P ZH1 「目的是」 and S ZH1 「重寫是為了」 (original: 「為了」).
- P ZH3 「而且」 is an addition, not a cause, result or contrast.

## 6. Residual occurrences in P and S

P (5):

- EN1 (b): "The analyst who rebuilt the weekly revenue report in October
  rewrote" (8 words between "analyst" and "rewrote").
- EN1 (b): "The check on whether the daily revenue snapshot is up to date
  has" (10 words between "check" and "has").
- EN2 (b): "The rate at which vendor invoices are matched as duplicates fell"
  (8 words between "rate" and "fell").
- EN3 (c): "worker pool size limit".
- ZH3 (c): 「工作程序池大小上限」.

S (4):

- EN1 (b): "The analyst who rebuilt the weekly revenue report in October
  rewrote" (8 words between "analyst" and "rewrote").
- EN1 (b): "The check on how fresh the daily revenue snapshot is has"
  (9 words between "check" and "has").
- EN3 (b): "the change to the size limit of the worker pool is released"
  (8 words between "change" and "is released").
- ZH3 (c): 「工作程序池大小上限」.

## 7. Borderline items left uncounted

- (e) P ZH2: 「負責稅務帳本的財務團隊在 28 日季結前要求了一份匯出，那份匯出
  執行了 3 分鐘。」 Two clauses joined by a comma with no connecting word.
  Left uncounted because the second clause only continues the topic with
  「那份」 and no cause, result or contrast reading is plausible. Counting it
  would make P ZH2 = 1, P Chinese = 2, P total = 6.
- (e) P ZH4: 「…在夜間從來不會觸發；這個警示是…設定的。」 Joined by a
  semicolon, same topic-continuation pattern; uncounted.
- (a) P EN2 "The importer relies on" and P ZH2 「匯入程式依賴的」: "rely on"
  is ordinary wording for a software dependency; uncounted.
- (a) P EN1 "cannot handle", S EN1 "does not accept", S ZH1 「不接受」,
  S ZH2 「處理不了」, P EN3 and S EN3 "no longer has its jobs", S ZH3
  「不再保有」: ordinary technical verbs; uncounted.
- (c) "legacy cron bridge" (original EN3, S EN3): "legacy" read as an
  adjective; uncounted in both.
- (c) "weekly revenue report", "daily revenue snapshot", "null store ids",
  "new calendar table" (original, P, S) and 「每週營收報表」, 「每日營收快照」
  (original, P, S): first word read as an adjective, leaving two nouns;
  uncounted everywhere.
- (c) S ZH2 「重複比對比率」: 「重複」 read as an adjective, leaving two nouns;
  uncounted.
- (b) P EN4 "The alert for refunds larger than 500 dollars never fires":
  7 words between "alert" and "fires"; below the threshold.
- (b) P EN3 "the change to the worker pool size limit is released": 6 words;
  below the threshold.
- (b) Chinese pre-modifiers of 10 to 14 characters, all below the threshold:
  P ZH1 「檢查「每日營收快照是不是最新」的那項檢查」, S ZH1 「檢查每日營收
  快照夠不夠新的那項檢查」, P ZH3 and S ZH3 「調整工作程序池大小上限的那項
  變更」, P ZH4 「針對超過 500 元退款的那個警示」.
- (d) "rubber-stamped" (original EN4) is counted, on the same footing as
  "backlog" and "sunset"; all three appear in dictionaries as verbs but are
  primarily nouns.
- Facts, P EN1: "I will not fix the handling of empty store ids now" spells
  out what "backlog" implies; not treated as a new assertion.
- Facts, S ZH3: 「舊的橋接停用了」 adds 「了」 to the original 「舊橋接停用」;
  the original is itself ambiguous about whether this has happened, so it is
  not treated as a changed outcome.
