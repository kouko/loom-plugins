# Dogfood verdict, round 2

An independent count of five sentence shapes in the eight original samples and
in the three rewrite sets P, Q and R, plus a fact check of each rewrite against
its original. The counter read only `dogfood-samples.md`, `rewrite-P.md`,
`rewrite-Q.md` and `rewrite-R.md`, and was not told which writing guide
produced which set.

Shape letters: (a) a thing does what only a person does; (b) subject far from
its verb; (c) three or more nouns in a row as one name; (d) noun used as a
verb; (e) dropped connecting word.

## 1. Shape counts per sample

| Sample | Original | P | Q | R |
|---|---|---|---|---|
| EN1 | 5 | 2 | 2 | 2 |
| EN2 | 3 | 2 | 0 | 0 |
| EN3 | 5 | 1 | 0 | 0 |
| EN4 | 3 | 0 | 0 | 0 |
| ZH1 | 5 | 1 | 1 | 1 |
| ZH2 | 3 | 0 | 0 | 0 |
| ZH3 | 4 | 0 | 0 | 0 |
| ZH4 | 4 | 0 | 0 | 0 |

## 2. Totals and subtotals

| Scope | Original | P | Q | R |
|---|---|---|---|---|
| English subtotal (EN1..EN4) | 16 | 5 | 2 | 2 |
| Chinese subtotal (ZH1..ZH4) | 16 | 1 | 1 | 1 |
| **Total** | **32** | **6** | **3** | **3** |

## 3. Per-shape totals

| Shape | Original | P | Q | R |
|---|---|---|---|---|
| (a) thing does a person's act | 8 | 0 | 0 | 0 |
| (b) subject far from verb | 6 | 1 | 1 | 1 |
| (c) noun stack | 8 | 3 | 2 | 2 |
| (d) noun as verb | 2 | 0 | 0 | 0 |
| (e) dropped connecting word | 8 | 2 | 0 | 0 |
| Total | 32 | 6 | 3 | 3 |

## 4. Fact verdicts

| Sample | P facts | Q facts | R facts |
|---|---|---|---|
| EN1 | kept | kept | kept |
| EN2 | kept | kept | kept |
| EN3 | kept | kept | kept |
| EN4 | kept | kept | kept |
| ZH1 | kept | kept | kept |
| ZH2 | kept | kept | kept |
| ZH3 | changed | kept | kept |
| ZH4 | kept | kept | kept |

`changed` totals: P 1, Q 0, R 0.

- P ZH3, added: 「其中 3 個檔案上」. The Chinese original lists the 3 files and
  the 12 files without saying the 3 are among the 12; 「其中」 asserts that
  they are.

Convention: a guessed cause, result or contrast is counted only in section 5
and does not by itself turn a facts verdict to `changed`. If guessed relations
were also treated as new assertions, Q's ZH1, ZH2, ZH3 and ZH4 and P's ZH1
would be `changed` as well.

## 5. Guessed relations

| Set | Count |
|---|---|
| P | 1 |
| Q | 5 |
| R | 0 |

Each sample is compared with its own original. EN1's original already says
"so", so "because" in the EN1 rewrites is a restatement and is not counted.
The ZH1 original joins the same two clauses with a bare comma, so a stated
cause there is counted.

P:
- ZH1: 「那個夜間工作還是顯示通過，原因是上一個 PR 加進來的重試程式接住了逾時錯誤」

Q:
- ZH1: 「那個夜間工作還是顯示通過，因為逾時發生時，上一個 PR 加進來的重試程式不回報錯誤」
- ZH1: 「部署延後，因為遷移沒跑完」
- ZH2: 「警示變少，因為門檻調高了」
- ZH3: 「報告列出 5 個警告，所以規則暫停」
- ZH4: 「產生發布說明的腳本輸出格式錯了，所以 PR 148 沒合併」

R: none.

## 6. Residual shape occurrences in P, Q and R

| Set | Sample | Shape | Quoted words |
|---|---|---|---|
| P | EN1 | (c) | "cache key collisions" |
| P | EN1 | (e) | "the one the infra team moved to the new runner" |
| P | EN2 | (b) | "the config loader, which is the first thing the CLI calls, does the rejecting" (8 words between "loader" and "does") |
| P | EN2 | (e) | "the first thing the CLI calls" |
| P | EN3 | (c) | "import order rule" |
| P | ZH1 | (c) | 「快取鍵衝突偵測」 |
| Q | EN1 | (b) | "Test coverage of the code that detects cache key collisions is at 62%" (8 words between "coverage" and "is") |
| Q | EN1 | (c) | "cache key collisions" |
| Q | ZH1 | (c) | 「快取鍵衝突」 |
| R | EN1 | (b) | "Test coverage of the code that detects cache key collisions is at 62%" (8 words between "coverage" and "is") |
| R | EN1 | (c) | "cache key collisions" |
| R | ZH1 | (c) | 「快取鍵衝突」 |

## Occurrences counted in the originals

| Sample | Shape | Quoted words |
|---|---|---|
| EN1 | (a) | "eats the timeout" |
| EN1 | (b) | "the nightly job that the infra team who took over the queue in March moved to the new runner after two outages still reports green" |
| EN1 | (c) | "Cache key collision detection test coverage" |
| EN1 | (d) | "ticket the fix" |
| EN1 | (e) | "The retry wrapper the last PR added" |
| EN2 | (b) | "The migration that the three services which share the orders table depend on before the 14:00 deploy finished" |
| EN2 | (c) | "Token refresh failure alert noise" |
| EN2 | (e) | "The config loader the CLI calls first" |
| EN3 | (a) | "The linter complains" |
| EN3 | (a) | "the formatter fights it" |
| EN3 | (c) | "import order rule" |
| EN3 | (c) | "parser version pin update" |
| EN3 | (e) | "The report the script generated" |
| EN4 | (a) | "The hook thinks" |
| EN4 | (b) | "The check that the maintainer who wrote the original guard added for tags created before version 3.0 after the September incident never runs" |
| EN4 | (d) | "I greenlit PR 148" |
| ZH1 | (a) | 「重試包裝吃掉了逾時錯誤」 |
| ZH1 | (b) | 「三月接手佇列的基礎設施團隊在兩次當機後搬到新執行機的那個夜間工作還是顯示通過」 |
| ZH1 | (c) | 「快取鍵衝突偵測測試覆蓋率」 |
| ZH1 | (e) | 「…吃掉了逾時錯誤，…那個夜間工作還是顯示通過」 |
| ZH1 | (e) | 「部署延後，遷移沒跑完」 |
| ZH2 | (b) | 「共用訂單資料表的三個服務在 14:00 部署前都依賴的那個遷移花了 41 秒完成」 |
| ZH2 | (c) | 「權杖更新失敗警示雜訊」 |
| ZH2 | (e) | 「警示變少，門檻調高了」 |
| ZH3 | (a) | 「格式化工具和檢查工具…打架」 |
| ZH3 | (a) | 「檢查工具抱怨了 12 個檔案」 |
| ZH3 | (c) | 「解析器版本鎖定更新合併流程」 |
| ZH3 | (e) | 「報告列出 5 個警告，規則暫停」 |
| ZH4 | (a) | 「這個掛鉤以為每個提交都是發布」 |
| ZH4 | (b) | 「九月事故後寫原始防護的維護者為 3.0 版之前建立的標籤加上的那個檢查在分支副本上從來不會執行」 |
| ZH4 | (c) | 「發布說明產生腳本輸出格式」 |
| ZH4 | (e) | 「發布說明產生腳本輸出格式錯了，PR 148 沒合併」 |

## Counting rules applied to all four sets

Borderline cases were left uncounted, and the same choice was applied
everywhere.

- (a) Not counted: "refuses" / 「拒絕」 (too close to "rejects"), "catches" /
  「接住」, "treats ... as", "accept", "conflict", "lands".
- (b) English: words strictly between the head noun of the subject and its
  verb; eight or more counts. "the infra team who took over the queue in March
  moved" (7) and Q EN3 "the update to the pinned version of the parser is
  merged" (7) are not counted. Chinese: only a pre-modifier clause of about
  twenty characters or more. Not counted: P ZH4 「針對 3.0 版之前建立的標籤的
  那個檢查」 (about 14 characters) and R ZH4 「維護者在九月事故後，為 3.0 版
  之前建立的標籤加上的」 (about 18 characters of adverbial phrases between
  subject and verb, not a pre-modifier clause).
- (c) Three bare nouns in a row count even when short, so "cache key
  collisions" and 「快取鍵衝突」 count in every set that has them, just as
  "import order rule" counts in the original. Not counted: two-noun pairs
  ("config loader", "orders table", 「雜訊警示」), adjective or participle plus
  two nouns ("pinned parser version", "failed token refreshes",
  「解析器鎖定版本」), 「基礎設施團隊」, 「訂單資料表」, 「權杖更新失敗的」, and
  Q ZH4 「腳本輸出格式」 (read as subject plus its attribute).
- (d) "shelve" is an ordinary verb and is not counted.
- (e) English: only a full clause with "that/which" left out. Participle
  phrases ("tags created before version 3.0", "the retry code added in the
  last PR") are not counted. Chinese: only comma-joined clauses whose unstated
  relation is cause, result or contrast. Plain listing is not counted (original
  ZH3 「…打架，檢查工具抱怨了 12 個檔案」; P ZH3 「…回報了問題，其中…」).
- Facts: a term paraphrased with the same referent ("retry wrapper" to "retry
  code", "green" to "success" or "a pass", "greenlit" to "approved") is treated
  as kept. P EN2 "The CLI rejects any config file over 2 MB" (original: the
  config loader refuses "any file") was judged a paraphrase and left as kept.
