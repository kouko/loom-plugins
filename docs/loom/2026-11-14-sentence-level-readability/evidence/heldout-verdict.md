# Held-out verdict

Independent count of five sentence shapes in the held-out originals and in
rewrite sets P and R, plus two fact checks per rewrite. The counter read only
the three evidence files (samples, rewrite P, rewrite R) and was not told which
writing guide produced which set.

## Counting rules as applied

The same rules were applied to the originals, P and R.

- (a) Counted only verbs that literally need a living being (hate, trust,
  choke, forget, starve, believe). "handle", "read", "rely on", "use",
  "treat as", "get", "fail" were not counted.
- (b) English: counted every subject and verb pair, in a main or an embedded
  clause, with eight or more words between the head noun and its verb.
  Chinese: counted a pre-modifier of twenty or more characters before the
  head noun.
- (c) Counted a run of three or more bare nouns. A leading adjective or
  frequency word ("weekly", "daily", "legacy", 每週, 每日) is not a noun in
  the run.
- (d) English only.
- (e) English: a relative clause with "that/which" left out. Chinese: two
  clauses about different things, joined by a comma in one sentence, with no
  connecting word. A second clause that only says more about the same thing
  (它是…, 那份匯出…, 用於…) was not counted, and neither was a comma after a
  topic or a time phrase.
- Facts: judged on numbers, names and outcomes. A relation the rewrite added
  is reported under guessed relations, not as a `changed` fact.

## 1. Shape counts per sample

| Sample | Original | P | R |
|---|---|---|---|
| EN1 | 6 | 2 | 1 |
| EN2 | 5 | 1 | 1 |
| EN3 | 5 | 1 | 1 |
| EN4 | 3 | 0 | 0 |
| ZH1 | 5 | 0 | 0 |
| ZH2 | 5 | 0 | 0 |
| ZH3 | 5 | 1 | 1 |
| ZH4 | 4 | 0 | 0 |

## 2. Totals and subtotals

| Scope | Original | P | R |
|---|---|---|---|
| English subtotal (EN1..EN4) | 19 | 4 | 3 |
| Chinese subtotal (ZH1..ZH4) | 19 | 1 | 1 |
| Total | 38 | 5 | 4 |

## 3. Per-shape totals

| Shape | Original | P | R |
|---|---|---|---|
| (a) thing does what only a person does | 12 | 0 | 0 |
| (b) subject far from its verb | 7 | 3 | 3 |
| (c) three or more nouns in a row | 7 | 2 | 1 |
| (d) noun used as a verb | 3 | 0 | 0 |
| (e) dropped connecting word | 9 | 0 | 0 |
| Total | 38 | 5 | 4 |

Original occurrences, for reference:

| Sample | Shape | Quoted words |
|---|---|---|
| EN1 | a | "The orders model ... hates null store ids" |
| EN1 | b | "the join that the analyst ... to use the new calendar table drops" |
| EN1 | b | "the analyst who rebuilt the weekly revenue report in October rewrote" (8 words between) |
| EN1 | c | "Daily revenue snapshot freshness check latency" |
| EN1 | d | "I'll backlog the null handling" |
| EN1 | e | "The orders model the dashboard reads" |
| EN2 | a | "the importer trusts" |
| EN2 | a | "The date parser ... chokes on two-digit years" |
| EN2 | b | "The export that the finance team ... on the 28th ran" |
| EN2 | c | "Vendor invoice duplicate match rate" |
| EN2 | e | "The date parser the importer trusts" |
| EN3 | a | "The scheduler forgets jobs" |
| EN3 | a | "the queue starves the 4 slow workers" |
| EN3 | c | "worker pool size limit change" |
| EN3 | d | "I'll sunset the legacy cron bridge" |
| EN3 | e | "The log the agent attached" |
| EN4 | a | "The cache believes stale prices" |
| EN4 | b | "The alert that the on-call engineer ... after the August outage never fires" |
| EN4 | d | "I rubber-stamped ticket 3172" |
| ZH1 | a | 「訂單模型討厭空的門市編號」 |
| ZH1 | b | 「十月重做每週營收報表的分析師在稽核後為了改用新日曆表而重寫的那個關聯查詢」 |
| ZH1 | c | 「每日營收快照新鮮度檢查延遲」 |
| ZH1 | e | 「…討厭空的門市編號，…那個關聯查詢少了 214 筆資料」 |
| ZH1 | e | 「報表晚出，排程重跑了」 |
| ZH2 | a | 「匯入程式信任的日期解析器」 |
| ZH2 | a | 「日期解析器被兩位數年份噎住了」 |
| ZH2 | b | 「負責稅務帳本的財務團隊在 28 日季結前要求的那份匯出」 |
| ZH2 | c | 「廠商發票重複比對比率」 |
| ZH2 | e | 「比對變快，索引重建了」 |
| ZH3 | a | 「排程器重啟後忘記了工作」 |
| ZH3 | a | 「佇列餓著 4 個慢速工作程序」 |
| ZH3 | c | 「工作程序池大小上限變更上線流程」 |
| ZH3 | e | 「排程器重啟後忘記了工作，佇列餓著 4 個慢速工作程序」 |
| ZH3 | e | 「記錄檔顯示 17 次逾時，舊橋接停用」 |
| ZH4 | a | 「快取相信過期的價格」 |
| ZH4 | b | 「八月當機後接手定價服務的值班工程師為超過 500 元的退款設定的那個警示」 |
| ZH4 | c | 「退款通知寄送範本欄位對應」 |
| ZH4 | e | 「退款通知寄送範本欄位對應錯了，工單 3172 沒關閉」 |

## 4. Fact verdicts

| Sample | P facts | R facts |
|---|---|---|
| EN1 | kept | kept |
| EN2 | kept | kept |
| EN3 | kept | kept |
| EN4 | kept | kept |
| ZH1 | kept | kept |
| ZH2 | kept | kept |
| ZH3 | kept | kept |
| ZH4 | kept | kept |

Totals of `changed`: P 0, R 0.

Every number (214, 9, 3, 28th, 7%, 2%, 4, 17, 15, 500, 3172), every name and
every outcome in the originals is present in both rewrites. The one added
relation in P ZH1 is reported in section 5 and is not counted here.

## 5. Guessed relations

| Set | Count |
|---|---|
| P | 1 |
| R | 0 |

Instances:

- P ZH1: 「有一個關聯查詢少了 214 筆資料，原因是儀表板讀取的訂單模型無法處理門市編號是空的訂單。」
  The ZH1 original places the two clauses side by side with only a comma
  (「…討厭空的門市編號，…那個關聯查詢少了 214 筆資料」) and states no cause.
- R: none. R ZH1 keeps the two statements as separate sentences.

Not guesses: "because" in P EN1 and R EN1 (the EN1 original says "so");
「目的是」 in P ZH1 and 「重寫是為了」 in R ZH1 (the original says 「為了」);
"so that it uses" in P EN1 and R EN1 (the original says "to use").

## 6. Residual shape occurrences in P and R

| Set | Sample | Shape | Quoted words |
|---|---|---|---|
| P | EN1 | b | "The analyst who rebuilt the weekly revenue report in October rewrote" (8 words between) |
| P | EN1 | b | "The check on whether the daily revenue snapshot is up to date has" (10 words between) |
| P | EN2 | b | "The rate at which vendor invoices are matched as duplicates fell" (8 words between) |
| P | EN3 | c | "worker pool size limit" |
| P | ZH3 | c | 「工作程序池大小上限」 |
| R | EN1 | b | "The analyst who rebuilt the weekly revenue report in October rewrote" (8 words between) |
| R | EN2 | b | "The rate at which vendor invoices are matched as duplicates fell" (8 words between) |
| R | EN3 | b | "the change to the size limit of the worker pool ships" (8 words between) |
| R | ZH3 | c | 「工作程序池大小上限」 |

## 7. Borderline items left uncounted

Each choice below was applied the same way to the originals, P and R.

- (a) "relies on" (P EN2), 「依賴」 (P ZH2), "treats stale prices as current"
  (R EN4), 「把過期的價格當成有效的價格」 (R ZH4), "cannot handle" / "does not
  handle" (P EN1, R EN1), "cannot read" (P EN2), "get no work" (R EN3),
  「拿不到工作」 (R ZH3): a tool can plausibly do these, so not counted.
- (b) "The alert for refunds larger than 500 dollars never fires" (P EN4,
  R EN4): 7 words between, one short of the threshold.
- (b) Chinese pre-modifiers under twenty characters:
  「檢查「每日營收快照是不是最新」的那項檢查」 (P ZH1, 14),
  「檢查每日營收快照是否夠新的那項檢查」 (R ZH1, 12),
  「調整工作程序池大小上限的那項變更」 (P ZH3, 11),
  「變更工作程序池大小上限的那項修改」 (R ZH3, 11),
  「八月當機後接手定價服務的值班工程師」 (P ZH4, R ZH4, 11),
  「十月重做每週營收報表的(那位)分析師」 (original, P and R ZH1, 10).
- (c) "weekly revenue report", "daily revenue snapshot", "legacy cron bridge",
  "null store ids", 「每週營收報表」, 「每日營收快照」: the first word was read
  as an adjective or frequency word, leaving two nouns. Present in the
  originals, P and R alike.
- (c) "null handling" (original EN1, R EN1), "size limit" and "worker pool"
  as separate pairs (R EN3), 「退款通知的寄送範本」 (P ZH4): two nouns each.
- (d) "ships" (original EN3, R EN3) and "fires": established verbs, not
  counted.
- (e) Second clause only says more about the same thing, so no relation is
  left to guess:
  P ZH2 「…要求了一份匯出，那份匯出執行了 3 分鐘」,
  R ZH2 「那份匯出跑了 3 分鐘，它是…要求的」,
  R ZH4 「它是…值班工程師設定的，用於超過 500 元的退款」.
- (e) Topic or time phrase followed by a comma, not two clauses:
  「…的那項檢查，延遲是 9 分鐘」 (P ZH1, R ZH1),
  「…的那項變更，上線流程還沒完成」 (P ZH3) and the R ZH3 equivalent,
  「退款通知的寄送範本裡，欄位對應錯了」 (P ZH4),
  「寄送退款通知用的範本，欄位對應錯了」 (R ZH4),
  「…的價格，長達 15 分鐘」 (P ZH4, R ZH4).
- Guessed relations: 「而且」 in P ZH3 and R ZH3 joins two clauses the ZH3
  original joined with a comma. It adds "and", not a cause, result or
  contrast, so it was not counted for either set.
- Facts: "I will not fix the handling of empty store ids now" (P EN1) spells
  out what "backlog" implies; "orders with no store id" / 「門市編號是空的訂單」
  (P EN1, P ZH1) names the rows that have the null ids. Neither was treated
  as a new assertion.
