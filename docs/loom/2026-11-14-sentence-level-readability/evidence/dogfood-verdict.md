# Dogfood verdict

Independent count of five sentence shapes in the originals
(`dogfood-samples.md`) and in two rewrite sets (`rewrite-P.md`,
`rewrite-Q.md`), plus a fact check of each rewrite against its original.
Only those three files were read. The counter did not know which writing
guide produced which set.

## 1. Counts and fact verdicts per sample

| Sample | Original count | P count | Q count | P facts | Q facts |
|---|---|---|---|---|---|
| EN1 | 5 | 2 | 2 | kept | kept |
| EN2 | 4 | 2 | 0 | changed | kept |
| EN3 | 5 | 1 | 0 | kept | kept |
| EN4 | 3 | 0 | 0 | kept | kept |
| ZH1 | 5 | 1 | 1 | kept (1 causal note) | kept (2 causal notes) |
| ZH2 | 3 | 0 | 0 | kept | kept (1 causal note) |
| ZH3 | 4 | 0 | 0 | changed | kept (1 causal note) |
| ZH4 | 4 | 0 | 0 | kept | kept (1 causal note) |
| **Total** | **33** | **6** | **3** | 6 kept / 2 changed | 8 kept / 0 changed |

## 2. Subtotals by language

| Group | Original count | P count | Q count | P facts | Q facts |
|---|---|---|---|---|---|
| English (EN1-EN4) | 17 | 5 | 2 | 3 kept / 1 changed | 4 kept / 0 changed |
| Chinese (ZH1-ZH4) | 16 | 1 | 1 | 3 kept / 1 changed | 4 kept / 0 changed |
| All eight | 33 | 6 | 3 | 6 kept / 2 changed | 8 kept / 0 changed |

Causal-direction notes: P 1, Q 5 (all in the Chinese samples).

## 3. Totals per shape

| Shape | Original | P | Q |
|---|---|---|---|
| (a) thing does what only a person does | 9 | 0 | 0 |
| (b) subject far from its verb | 6 | 1 | 1 |
| (c) three or more nouns in a row | 8 | 3 | 2 |
| (d) noun used as a verb (English only) | 2 | 0 | 0 |
| (e) dropped connecting word | 8 | 2 | 0 |
| Total | 33 | 6 | 3 |

Per-sample breakdown (a/b/c/d/e):

| Sample | Original | P | Q |
|---|---|---|---|
| EN1 | 1/1/1/1/1 | 0/0/1/0/1 | 0/1/1/0/0 |
| EN2 | 1/1/1/0/1 | 0/1/0/0/1 | 0/0/0/0/0 |
| EN3 | 2/0/2/0/1 | 0/0/1/0/0 | 0/0/0/0/0 |
| EN4 | 1/1/0/1/0 | 0/0/0/0/0 | 0/0/0/0/0 |
| ZH1 | 1/1/1/0/2 | 0/0/1/0/0 | 0/0/1/0/0 |
| ZH2 | 0/1/1/0/1 | 0/0/0/0/0 | 0/0/0/0/0 |
| ZH3 | 2/0/1/0/1 | 0/0/0/0/0 | 0/0/0/0/0 |
| ZH4 | 1/1/1/0/1 | 0/0/0/0/0 | 0/0/0/0/0 |

## 4. Residual occurrences in the rewrites

### P (6)

| Sample | Shape | Quoted words |
|---|---|---|
| EN1 | c | "cache key collisions" |
| EN1 | e | "the one the infra team moved to the new runner" ("that" omitted) |
| EN2 | b | "the config loader, which is the first thing the CLI calls, does the rejecting" (8 words between "loader" and "does") |
| EN2 | e | "the first thing the CLI calls" ("that" omitted) |
| EN3 | c | "import order rule" |
| ZH1 | c | 「快取鍵衝突偵測」(in 「快取鍵衝突偵測這部分程式」) |

### Q (3)

| Sample | Shape | Quoted words |
|---|---|---|
| EN1 | b | "Test coverage of the code that detects cache key collisions is at 62%" (8 words between "coverage" and "is") |
| EN1 | c | "cache key collisions" |
| ZH1 | c | 「快取鍵衝突」(in 「偵測快取鍵衝突的那段程式」) |

### Occurrences counted in the originals (for reference)

| Sample | Shape | Quoted words |
|---|---|---|
| EN1 | a | "eats the timeout" |
| EN1 | b | "the nightly job that the infra team who took over the queue in March moved to the new runner after two outages still reports" |
| EN1 | c | "Cache key collision detection test coverage" |
| EN1 | d | "ticket the fix" |
| EN1 | e | "The retry wrapper the last PR added" |
| EN2 | a | "refuses any file" |
| EN2 | b | "The migration that the three services which share the orders table depend on before the 14:00 deploy finished" |
| EN2 | c | "Token refresh failure alert noise" |
| EN2 | e | "The config loader the CLI calls first" |
| EN3 | a | "The linter complains" |
| EN3 | a | "the formatter fights it" |
| EN3 | c | "import order rule" |
| EN3 | c | "parser version pin update" |
| EN3 | e | "The report the script generated" |
| EN4 | a | "The hook thinks" |
| EN4 | b | "The check that the maintainer who wrote the original guard added for tags created before version 3.0 after the September incident never runs" |
| EN4 | d | "greenlit" |
| ZH1 | a | 「重試包裝吃掉了逾時錯誤」 |
| ZH1 | b | 「三月接手佇列的基礎設施團隊在兩次當機後搬到新執行機的那個夜間工作」 |
| ZH1 | c | 「快取鍵衝突偵測測試覆蓋率」 |
| ZH1 | e | 「…吃掉了逾時錯誤，…那個夜間工作還是顯示通過」 |
| ZH1 | e | 「部署延後，遷移沒跑完」 |
| ZH2 | b | 「共用訂單資料表的三個服務在 14:00 部署前都依賴的那個遷移」 |
| ZH2 | c | 「權杖更新失敗警示雜訊」 |
| ZH2 | e | 「警示變少，門檻調高了」 |
| ZH3 | a | 「格式化工具和檢查工具…打架」 |
| ZH3 | a | 「檢查工具抱怨了 12 個檔案」 |
| ZH3 | c | 「解析器版本鎖定更新合併流程」 |
| ZH3 | e | 「報告列出 5 個警告，規則暫停」 |
| ZH4 | a | 「這個掛鉤以為」 |
| ZH4 | b | 「九月事故後寫原始防護的維護者為 3.0 版之前建立的標籤加上的那個檢查」 |
| ZH4 | c | 「發布說明產生腳本輸出格式」 |
| ZH4 | e | 「發布說明產生腳本輸出格式錯了，PR 148 沒合併」 |

## 5. Fact-check evidence

### `changed` verdicts

| Set | Sample | Evidence |
|---|---|---|
| P | EN2 | Added: "The CLI rejects any config file over 2 MB". The original says "The config loader the CLI calls first refuses any file over 2 MB": it does not make the CLI the one that rejects, and it says "any file", not "any config file". Nothing was dropped; the next clause restores the loader as the actor. |
| P | ZH3 | Added: 「其中 3 個檔案上」. The original says 「格式化工具和檢查工具在 3 個檔案上打架，檢查工具抱怨了 12 個檔案」 and does not state that the 3 files are among the 12. Nothing was dropped. |

Q has no `changed` verdict.

Both `changed` verdicts are small added specifics, not lost numbers, names or
outcomes. Every number (62%, 2 MB, 41 seconds, 14:00, 30, 4, 12, 3, 5, 3.0,
148, March, September, two outages, three services) is present in all sixteen
rewrites.

### Causal-direction notes (verdict stays `kept`)

The rewrite states a cause-and-effect direction that the original left open by
placing two clauses side by side.

| Set | Sample | Original | Rewrite |
|---|---|---|---|
| P | ZH1 | 「…重試包裝吃掉了逾時錯誤，…那個夜間工作還是顯示通過」 | 「那個夜間工作還是顯示通過，原因是…重試程式接住了逾時錯誤」 |
| Q | ZH1 | same sentence | 「那個夜間工作還是顯示通過，因為逾時發生時，…重試程式不回報錯誤」 |
| Q | ZH1 | 「部署延後，遷移沒跑完」 | 「部署延後，因為遷移沒跑完」 |
| Q | ZH2 | 「警示變少，門檻調高了」 | 「警示變少，因為門檻調高了」 |
| Q | ZH3 | 「報告列出 5 個警告，規則暫停」 | 「報告列出 5 個警告，所以規則暫停」 |
| Q | ZH4 | 「發布說明產生腳本輸出格式錯了，PR 148 沒合併」 | 「產生發布說明的腳本輸出格式錯了，所以 PR 148 沒合併」 |

For the last four pairs P kept the relation open by writing two separate
sentences (「部署延後了。遷移沒有跑完。」, 「警示變少了。門檻調高了。」,
「報告列出 5 個警告。規則暫停了。」, 「…輸出格式是錯的。PR 148 沒有合併。」).

### Wording substitutions that did not change a verdict

- "retry wrapper" / 「重試包裝」: P writes "retry code" / 「重試程式」 and drops
  the word "wrapper"; Q writes "retry code ... [retry wrapper]" /
  「重試程式…〔重試包裝〕」. Treated as a paraphrase of a common-noun term,
  because the component is still identified by "added in the last PR".
- Figurative verbs had to be decoded by both rewriters ("eats", "fights",
  「打架」). P reads the conflict as "conflicting results" / 「結果互相衝突」;
  Q reads it as "conflict" / 「要求互相衝突」. Neither reading is stated by the
  original; both were treated as paraphrase.

## Counting decisions (applied identically to originals, P and Q)

- (a) Counted: eats, refuses, complains, fights, thinks, 吃掉, 打架, 抱怨, 以為.
  Not counted: "rejects", "does not accept", "catches", "treats", "reports",
  接住, 不接受. Chinese 「拒絕」 is not counted, because it is also the plain
  technical word for "reject"; it appears in original ZH2 and in P ZH2. If it
  were counted, the original and P would each rise by 1.
- (b) English: words strictly between the head noun of the subject and its
  main verb, eight or more. Chinese: a pre-modifier of twenty or more
  characters. Near misses not counted: P EN4 "The check for tags created
  before version 3.0 never runs" (7 words); Q EN3 "the update to the pinned
  version of the parser is merged" (7 words); Q ZH3
  「格式化工具和檢查工具在 3 個檔案上的要求」(17 characters); P ZH4
  「針對 3.0 版之前建立的標籤的那個檢查」(about 14 characters).
- (c) Two-noun names are not counted ("config loader", "orders table",
  「測試覆蓋率」, 「合併流程」). 「基礎設施團隊」 is treated as two nouns.
  「權杖更新失敗的」 (P ZH2 and Q ZH2, identical words) is read as a clause and
  not counted. Q ZH4 「腳本輸出格式錯了」 is read as topic plus comment
  (P has the same words split by a comma) and not counted; if it were counted,
  Q would rise by 1.
- (d) "ticket" and "greenlit" counted. "shelve", "pause" and "pinned" are
  established verbs and are not counted.
- (e) English: only an omitted "that/which" counts; reduced participle phrases
  ("tags created before", "the retry code added in") do not. Chinese: only two
  clauses joined inside one sentence with a cause, result or contrast relation
  left unstated. Clauses that merely add a second fact (original ZH3 first
  sentence; semicolon pairs in P and Q) are not counted. Two separate full
  sentences are not counted; this covers the four P sentence pairs quoted
  above. If those four were counted, P would rise by 4.
