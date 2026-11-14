# Document probe verdict — sentence shapes in acceptance test reports A and B

Counted blind: the counter read only `report-factsheets.md`, `report-A.md` and
`report-B.md`, and does not know which template produced which set. Text copied
from the Acceptance lines ("what you asked for" cells) and the fixed section
headings is excluded. The same rules were applied to both sets; when a case was
uncertain it was left uncounted in both and listed in section 6.

## 1. Shapes (a)–(e) per report

| Report | A shapes | B shapes |
|---|---|---|
| R1 (Traditional Chinese) | 3 | 2 |
| R2 (English) | 1 | 1 |
| Total | 4 | 3 |

## 2. Per-shape totals

| Shape | A | B |
|---|---|---|
| (a) thing does what only a person does | 0 | 0 |
| (b) subject far from its verb | 1 | 1 |
| (c) three or more nouns in a row | 0 | 0 |
| (d) noun used directly as a verb | 0 | 0 |
| (e) dropped connecting word | 3 | 2 |
| Total (a)–(e) | 4 | 3 |

Counted separately:

| | A | B |
|---|---|---|
| (f) no stated actor — R1 | 4 | 2 |
| (f) no stated actor — R2 | 3 | 2 |
| (f) total | 7 | 4 |

## 3. Sentence units and density

A unit is one sentence. A bullet's bold label is counted together with the
first sentence that follows it. Fixed headings and "what you asked for" cells
are not units.

| | A R1 | A R2 | A total | B R1 | B R2 | B total |
|---|---|---|---|---|---|---|
| Sentence units | 19 | 16 | 35 | 19 | 18 | 37 |
| Shapes (a)–(e) | 3 | 1 | 4 | 2 | 1 | 3 |
| Shapes per 100 units | 15.8 | 6.3 | 11.4 | 10.5 | 5.6 | 8.1 |
| (f) count | 4 | 3 | 7 | 2 | 2 | 4 |
| (f) per 100 units | 21.1 | 18.8 | 20.0 | 10.5 | 11.1 | 10.8 |

Unit breakdown — A R1: intro 2, table 4, existing-data paragraph 3, decision
bullets 6, skipped steps 1, open question 3. A R2: intro 2, table 3,
existing-data paragraph 3, decision bullets 4, "No finding…" 1, skipped steps 1,
open questions 2. B R1: intro 2, table 4, existing-data paragraph 2, decision
bullets 7, skipped steps 1, open question 3. B R2: intro 2, table 3,
existing-data paragraph 4, decision bullets 5, "No finding…" 1, skipped steps 1,
open questions 2.

## 4. Fact check

Standard used: a causal claim is `invented` unless the fact sheet states the
cause in causal words or the claim follows by logic alone from stated facts.
"I did not assess / my notes do not record" statements are not facts.

| Report | A | B |
|---|---|---|
| R1 | clean | invented (1) |
| R2 | clean | clean |

Invented statements:

- A: none.
- B R1, table row 4: 「但第二次花了 71 秒，因為第二次的檔案裡有 2,000 列重複」.
  The fact sheet gives the 2,000 duplicates only as a parenthetical beside the
  71 s figure ("71 s on second run (second run had 2,000 duplicates)") and does
  not say the duplicates caused the slower run; the open question likewise only
  says "when a file has many duplicates". This is an empirical cause that the
  stated facts do not entail.

Omitted fact-sheet items:

- A R2, table row 1: omits "recalculation job last run is 23:30" (the report
  says refunds after 23:30 are picked up the next day but not that the last
  run of the day is at 23:30).
- A R1: none.
- B R1: none.
- B R2: none. (Minor wording loss, not counted as an omission: the fact sheet
  says the 2026-11-02 difference "appears only when that report is opened";
  B R2 says "when you open it" without "only".)

Totals: A invented 0, omitted 1. B invented 1, omitted 0.

## 5. Every counted occurrence

### Shapes (a)–(e)

| Set | Report | Shape | Quoted words |
|---|---|---|---|
| A | R1 | (e) | 「比對了 4 筆既有訂單匯入前後的內容，所有欄位都一樣。」 — result relation between comparing and the finding left unstated |
| A | R1 | (e) | 「第二次的檔案有 2,000 列重複，花了 71 秒」 — relation between the duplicates and the time left unstated |
| A | R1 | (e) | 「畫面上看不到全部，只能靠下載。」 — result relation left unstated |
| A | R2 | (b) | "A report produced at 09:00 with a total of 1,284,300 was recalculated" — 8 words between "report" and "was recalculated" |
| B | R1 | (e) | 「我比對了 4 筆既有訂單在匯入前和匯入後的內容，所有欄位都一模一樣。」 — same construction as the A R1 row-3 item |
| B | R1 | (e) | 「匯入只會寫入新的列，你既有的資料沒有任何一筆被改動。」 — two clauses with different subjects, result relation left unstated |
| B | R2 | (b) | "A report produced at 09:00 with a total of 1,284,300 was recalculated" — same 8-word gap |

### (f) No stated actor

| Set | Report | Quoted words |
|---|---|---|
| A | R1 | 「2026-11-13 在專案的一份乾淨副本（4be21c7）上試的。」 |
| A | R1 | 「比對了 4 筆既有訂單匯入前後的內容」 |
| A | R1 | 「…這項意見沒有採納」 (bullet label) |
| A | R1 | 「沒有採納，是因為畫面已經限制在 500 筆」 |
| A | R2 | "Tried on 2026-11-13, in a clean copy of the project at 9d07a1e." |
| A | R2 | "Of 30 older reports compared before and after" |
| A | R2 | "The full test suite — skipped on your instruction, 2026-11-12." |
| B | R1 | 「…這個意見被駁回了」 (bullet label) |
| B | R1 | 「這個意見被駁回，因為畫面上最多只顯示 500 筆」 |
| B | R2 | "Tried on 2026-11-13, in a clean copy of the project at 9d07a1e." |
| B | R2 | "The full test suite — skipped on your instruction, 2026-11-12." |

Rule used for (f): counted when an act was actually performed and the context
identifies the tester/writer as the one who performed it (trying, comparing,
dismissing a finding, skipping a step), whether the form is a dropped Chinese
subject, a Chinese 被 passive without an agent, or an English passive or
passive participle without an agent.

## 6. Borderline items left uncounted

Shape (e):

- A R1 「那一列重複的是同一個檔案裡的另一列，不是既有的訂單」 — the 是／不是
  pair itself signals the contrast (B writes 而不是). Also the colon in A and
  the semicolon in B before this clause leave an explanation relation unstated,
  but the joiner is not a comma.
- A R1 「匯入只會新增列，不會改動原本就在的訂單。」 — same subject, 只會／不會
  pair signals the contrast.
- A R1 「我選了保留第一次出現的那一列、跳過後面的，另一個做法是全部跳過。」 and
  「我選了畫面上最多顯示 500 筆，完整清單可以下載成 CSV，另一個做法是全部顯示在畫面上。」
  — comma-joined independent clauses, but 另一個做法 names the relation
  (alternative) and the middle clause is additive. If these were counted, A
  would gain 2.
- A R1 「一個 50 列…的檔案，匯入了 46 列，跳過 4 列。」 and B R1
  「我在 2026-11-13 試的，用的是…」 — additive, not cause/result/contrast.
- A R1 and B R1 「…，嚴重程度是…」 after the reviewer clause — additive.
- English reduced relatives in both sets ("A report produced at 09:00",
  "refunds posted after 23:30"; A only: "30 older reports compared") — a
  standard participle construction, not an omitted "that/which" before a
  finite clause.

Shape (b):

- A R1 / B R1 「一個 50 列、其中 4 列訂單編號重複的檔案」 — a 16-character
  modifier, but it stands before the head noun, not between subject and verb.

Shape (a):

- 「畫面列出」, "the screen recomputes the total and shows", "My notes record",
  「我的紀錄裡沒有寫下」 — ordinary technical or documentary verbs.
- B R1 「我的紀錄裡沒有寫下選這個做法的理由，也沒有評估之後要改的代價」 — if
  紀錄 is read as the subject of 評估 this would be (a); read here as a dropped
  「我」, so not counted under (a) or (f).

Shape (c):

- "config value", "hand calculation", "timezone fix", "test suite",
  「訂單編號」 — two nouns each.

Shape (d):

- "is emailed again" (both sets, bullet label) and "email the recipients"
  (both sets, copied from the fact sheet) — "email" is an established verb.

Shape (f):

- Negative statements where no act took place, uncounted in both sets:
  A R1 「這次沒有做備份」 (B R1 states 「我沒有做備份」); A R2 "The stored
  totals of your old reports were not rewritten." (B R2 states "The change does
  not rewrite…"); both sets 「沒有任何步驟被跳過」 and "No finding of severity
  important or worse was dismissed." If negatives were counted, A (f) would be
  7 + 4 = 11 and B (f) would be 4 + 2 = 6.
- Passives whose actor is the system or is not named in the fact sheet,
  uncounted in both sets: "was recalculated", "were posted", "are picked up",
  "was never recalculated", "can still be read", 「被跳過的列」; A R2 only:
  "is opened and recomputed on screen"; A R1 「匯入了 46 列，跳過 4 列」 and
  B R1 「46 列匯入、4 列被跳過」.
- A R1 「每一條怎麼試、得到什麼：」 — a label fragment with no stated tester
  (B R1 has 「每一條我怎麼試」).
- Generic-actor clauses in both sets: 「之後要改的話，要改／需要修改一個 function」,
  A R1 「畫面上看不到全部，只能靠下載」.

Fact check:

- B R2 row 1 "picked up the next day, because the last recalculation of the
  day runs at 23:30" — the fact sheet gives the 23:30 last run as a
  parenthetical without a causal word, as in the R1 71-second case. Left as
  clean because the consequence follows by logic alone from the stated fact (no
  run after 23:30 means later refunds cannot be picked up that day). If any
  parenthetical turned into "because" were treated as invented, B would have 2.
- A R1 「問題會出現在被跳過的列超過 500 筆的時候：畫面上看不到全部，只能靠下載」
  — not in the fact sheet word for word, but follows by logic from the 500-row
  cap plus download. B R1 「問題就會出現在這份清單上」 is likewise not in the
  fact sheet and is vaguer. Both left as clean.
- A R2 and B R2 "so the old number can still be read" — follows from "original
  stored value still in the database". Left as clean in both.
- "I did not assess what changing it later would cost" (A R2),
  「之後要改的代價我沒有評估過」 (A R1), 「也沒有評估之後要改的代價」 (B R1) —
  treated as statements that the notes record nothing, not as invented facts.
  B R2 words the same point as "My notes record neither the reason nor the
  cost".
