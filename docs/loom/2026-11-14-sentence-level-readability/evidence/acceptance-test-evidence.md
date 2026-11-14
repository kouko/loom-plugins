# 白話指引補上句子層級的可讀性規則 — acceptance test evidence

Tried on 2026-11-14, in a clean copy of the project at f35f7430.

Setup, done once before the lines:

- Clean copy: `git worktree add --detach <scratch>/at-clean f35f74302c2fcc71242ba582327032135d476ed7`.
  A second clean copy at the branch base, `git worktree add --detach <scratch>/at-base adcd4cbfa468b374b5f8e0b9363adf0304b53e33`,
  supplied the guide as it was before the change.
- Install check, from the `## Install` section of `loom-workflow/README.md`: the
  marketplace install pulls from GitHub and would not test this commit, so the
  local equivalent was run: `claude plugin validate <scratch>/at-clean/loom-workflow`.
  Result: `Validation passed with warnings`. The two warnings (an unquoted
  `${CLAUDE_PLUGIN_ROOT}` in `hooks.PostToolUse`, and `ICON_MISSING`) are in
  files this change did not touch.
- Version strings in the clean copy: `5.23.0` in `loom-workflow/.claude-plugin/plugin.json`,
  `loom-workflow/.codex-plugin/plugin.json`, `loom-workflow/plugin.json`,
  `loom-workflow/package.json` and `loom-workflow/README.md:11`.
- Focused tests, run in the clean copy (never the complete suite, which is
  skipped by instruction):
  `uv run --isolated --with-requirements requirements-package-tests.lock --directory <scratch>/at-clean python -m pytest loom-workflow/tests/loom-visualization/test_references.py loom-workflow/tests/scripts/test_release_metadata.py docs/loom/2026-11-14-sentence-level-readability/evidence -q -p no:cacheprovider`
  Result: `44 passed in 1.87s`.
- Files the change touched under the plugin trees
  (`git diff --stat adcd4cbf f35f7430 -- loom-code loom-design loom-workflow/hooks loom-workflow/skills`):
  only `loom-workflow/skills/loom-visualization/references/plain-language.md`
  (38 insertions, 1 deletion).

The guide file is `loom-workflow/skills/loom-visualization/references/plain-language.md`;
line numbers below are from the clean copy.

## 1. 白話指引對五種句型（無生命主語配有生命動詞、主語與動詞距離過遠、三個以上名詞堆疊、名詞當動詞、省略連接子句的字詞）各有至少一組「難讀／白話」英文對照；在中文有對應寫法的句型，另有繁體中文對照。
- How I tried it: opened the guide in the clean copy and read the table under
  rule 3; ran the focused tests above.
- What came back: the table at lines 65-75 has nine rows. English pairs: all
  five shapes (lines 67, 69, 71, 73, 74). Traditional Chinese pairs: four
  shapes (lines 68, 70, 72, 75). "A noun used as a verb" (line 73) has an
  English pair only. Every Plain cell differs from its Hard cell and keeps the
  same facts.
- Evidence: `plain-language.md:65-75`;
  `test_references.py::test_sentence_shape_guidance_present` and
  `::test_broken_sentence_shape_guidance_rejected` passed.

## 2. 白話指引寫明：簡潔是刪掉使用者不需要的內容，不是刪掉把句子連起來的字詞。
- How I tried it: read rule 7 in the clean copy; ran the focused tests.
- What came back: lines 159-162: "Being concise means leaving out content that
  the user does not need. It never means dropping the words that connect a
  sentence: keep "that", "because", "so", 「因為」 and 「所以」 where the
  original has them or the relation is known."
- Evidence: `plain-language.md:159-162`; the "rule 7 keeps connecting words"
  pin in `test_sentence_shape_guidance_present` passed.

## 3. 使用者要求「說得更白話」時，指引的改寫步驟包含檢查這些句型。
- How I tried it: read the "Rewrite steps" section in the clean copy; ran the
  focused tests; and, in the fresh trial of line 4, gave a fresh agent only the
  guide and the samples and asked it to follow the rewrite steps.
- What came back: step 5 at line 192 reads "Check for metaphor words ... and
  for the five sentence shapes of rule 3 before sending, and replace each with
  the literal statement." The section still has exactly five steps. The fresh
  agent's rewrites (set X below) removed the shapes.
- Evidence: `plain-language.md:192`; the "last rewrite step checks the sentence
  shapes" pin and `test_guide_has_seven_rules_and_rewrite_steps` passed.

## 4. 實際試用（dogfood）：取一組含有這些句型的中文與英文回覆，交給沒有本次對話背景的 agent 分別依修改前與修改後的指引改寫。修改後的改寫結果殘留的這些句型比修改前少，而且原回覆的事實、數字、名稱與結果沒有減少也沒有增加。
- How I tried it, part one (the recorded trial): read
  `heldout-samples.md`, `heldout-rewrite-P.md` (old guide),
  `heldout-rewrite-S.md` (final guide) and `heldout-verdict-final.md` in the
  same evidence folder, and recounted P and S myself against the samples.
- What came back, part one: my recount agrees with the recorded counts.
  Originals 38 occurrences; P 5; S 4. P residue: EN1 two long subject-verb
  gaps, EN2 "The rate at which vendor invoices are matched as duplicates
  fell", EN3 "worker pool size limit", ZH3 「工作程序池大小上限」. S residue:
  the same two in EN1, EN3 "the change to the size limit of the worker pool is
  released" (exactly at the eight-word threshold), ZH3 「工作程序池大小上限」.
  Every number and name (214, 9, 3, 28th, 7%, 2%, 4, 17, 15, 500, 3172,
  October, August) is in both sets. P ZH1 adds 「原因是」 where the Chinese
  original states no cause; S adds none. One thing the recorded verdict
  waived that I note: S ZH3 writes 「舊的橋接停用了」 where the original says
  「舊橋接停用」, which commits to "already done" where the original is
  ambiguous.
- How I tried it, part two (my own fresh trial): the recorded margin is one
  occurrence from one rewriter per guide, so I ran the comparison once more.
  Two fresh agents with no context each read one guide and
  `heldout-samples.md`, and were asked to rewrite each sample as if the user
  had said "explain it more plainly", following the guide's rewrite steps.
  Agent X read the guide at f35f7430; agent Y read the guide at adcd4cbf.
  Neither was told there was another version. I counted both sets with the
  counting rules written in `heldout-verdict-final.md`. I knew which set was
  which, so this count is not blind.
- What came back, part two:

  | Set | Guide | Residual shapes | Changed facts | Guessed causes |
  |---|---|---|---|---|
  | Y | before the change | 4 (3 if the borderline item is dropped) | 0 | 0 |
  | X | after the change | 2 | 0 | 0 |

  Y residue: EN1 "The check that tests whether the daily revenue snapshot is
  up to date has" (12 words between subject and verb); EN2 "The rate at which
  vendor invoices are matched as duplicates fell" (8 words); EN3 "worker pool
  size limit"; ZH3 「工作程序池大小上限」; borderline, counted: ZH4
  「退款通知寄送範本的欄位對應」.
  X residue: EN1 "The analyst who rebuilt the weekly revenue report in October
  rewrote" (8 words); EN3 "the change to the size limit of the worker pool is
  released" (8 words).
  Left uncounted in both, as the recorded rules do: "relies on" / 「依賴」,
  "does not accept", "legacy cron bridge". Left uncounted in X: "The cache
  treats out-of-date prices as current" and 「把過期的價格當成有效的價格」.
  Y adds two glosses that are not in the originals, "(the step that combines
  tables)" / 「（把幾張表合併起來的查詢）」 and "for good"; they explain a
  term and are not counted as changed facts. All numbers and names are present
  in both sets.
- Reading of both trials together: each guide removes about nine in ten of
  the 38 occurrences. The final guide leaves one fewer (recorded trial) or one
  to two fewer (my trial). The direction is the same in both trials; the size
  is small, and with one rewriter per guide per trial it is within what chance
  could produce. The recorded trial's "1 guessed cause against 0" did not
  repeat in my trial (0 against 0).
- Evidence: the four recorded files named above; the two rewrite sets below.

### Set X — rewrites under the guide at f35f7430 (after the change)

#### EN1
The join drops 214 rows, because the orders model that the dashboard reads does not accept empty store ids [null]. The analyst who rebuilt the weekly revenue report in October rewrote that join after the audit so that it uses the new calendar table. I will put the null handling on the backlog. The freshness check for the daily revenue snapshot has a latency of 9 minutes.

#### EN2
The date parser that the importer relies on fails on two-digit years. The export ran in 3 minutes. The finance team, which owns the tax ledger, asked for it before the quarter close on the 28th. The rate of duplicate matches on vendor invoices fell from 7% to 2%.

#### EN3
After a restart, the scheduler no longer has its jobs, and the 4 slow workers get no jobs from the queue. I will shut down the legacy cron bridge once the change to the size limit of the worker pool is released. The log that the agent attached shows 17 timeouts.

#### EN4
The cache treats out-of-date prices as current for 15 minutes. The alert for refunds larger than 500 dollars never fires at night. The on-call engineer who inherited the pricing service set that alert up after the August outage. I approved ticket 3172 without checking it.

#### ZH1
那個關聯查詢少了 214 筆資料。儀表板讀取的訂單模型不接受空的門市編號。這個關聯查詢是十月重做每週營收報表的分析師在稽核後重寫的，重寫是為了改用新日曆表。檢查每日營收快照夠不夠新的那項檢查，延遲是 9 分鐘。報表晚出了。排程重跑了。

#### ZH2
匯入程式依賴的日期解析器遇到兩位數年份就會失敗。那份匯出跑了 3 分鐘。它是負責稅務帳本的財務團隊在 28 日季結前要求的。廠商發票的重複比對比率從 7% 降到 2%。比對變快了。索引重建了。

#### ZH3
排程器重啟後，不再保有原本的工作，而且 4 個慢速工作程序從佇列拿不到工作。有一項變更要調整工作程序池的大小上限，它的上線流程還沒走完。記錄檔顯示 17 次逾時。舊橋接停用。

#### ZH4
快取會把過期的價格當成有效的價格，長達 15 分鐘。那個警示在夜間從來不會觸發。它是八月當機後接手定價服務的值班工程師為超過 500 元的退款設定的。寄送退款通知用的範本，欄位對應錯了。工單 3172 沒有關閉。

### Set Y — rewrites under the guide at adcd4cbf (before the change)

#### EN1
The orders model that the dashboard reads cannot handle rows with an empty store id [null], so one join (the step that combines tables) drops 214 rows. That join was rewritten after the audit to use the new calendar table. The analyst who rewrote it is the one who rebuilt the weekly revenue report in October.

I will not fix the handling of empty store ids now; I will add it to the list of work to do later.

The check that tests whether the daily revenue snapshot is up to date has a delay of 9 minutes.

#### EN2
The importer relies on a date parser that fails on years written with two digits.

The finance team, which owns the tax ledger, asked for an export before the quarter close on the 28th. That export ran in 3 minutes.

The rate at which vendor invoices are matched as duplicates fell from 7% to 2%.

#### EN3
After a restart, the scheduler no longer has its jobs, and the queue gives no work to the 4 slow workers.

I will turn off the old cron bridge for good once the change to the worker pool size limit is released.

The log that the agent attached shows 17 timeouts.

#### EN4
For 15 minutes, the cache keeps using prices that are out of date.

After the August outage, the on-call engineer who inherited the pricing service set up an alert for refunds larger than 500 dollars. That alert never fires at night.

I approved ticket 3172 without checking it.

#### ZH1
儀表板讀取的訂單模型無法處理門市編號是空的資料。

有一個關聯查詢（把幾張表合併起來的查詢）少了 214 筆資料。這個查詢是稽核之後為了改用新的日曆表而重寫的，重寫的人是十月重做每週營收報表的那位分析師。

檢查「每日營收快照是不是最新」的那項檢查，延遲是 9 分鐘。

報表晚了才產出。排程重新跑了一次。

#### ZH2
匯入程式依賴的日期解析器，遇到只寫兩位數的年份就無法處理。

負責稅務帳本的財務團隊在 28 日季結前要求了一份匯出，那份匯出跑了 3 分鐘。

廠商發票被比對為重複的比率，從 7% 降到 2%。

比對變快了。索引重建了。

#### ZH3
排程器重啟後，原本的工作就不在了；佇列也沒有把工作分給那 4 個慢速工作程序。

調整工作程序池大小上限的那項變更，上線流程還沒走完。

記錄檔顯示有 17 次逾時。舊的橋接停用。

#### ZH4
快取會繼續使用過期的價格，長達 15 分鐘。

有一位值班工程師在八月當機後接手了定價服務，這位工程師為超過 500 元的退款設定了一個警示。這個警示在夜間從來不會觸發。

退款通知寄送範本的欄位對應錯了。工單 3172 沒有關閉。

## 5. 指引的適用範圍不變：只規範寫給使用者的對話文字，不規範寫給 AI 讀的文件。
- How I tried it: read the "Scope" section in the clean copy, checked the
  branch diff of the guide for any change to it, and ran the focused tests
  including the two probe tests in the evidence folder.
- What came back: lines 11-14 still read "This guide covers chat text written
  for the user ... It never covers files you write: intents, specs, plans,
  commit messages, code comments." The diff of the guide has no hunk in the
  Scope section. No other skill file, hook or card changed on the branch.
- Evidence: `plain-language.md:11-14`; the "scope excludes files you write"
  pin, `test_guide_scope_widened_to_agent_files.py` and
  `test_sentence_shape_check_negated_guidance.py` passed (part of the 44).

## 6. 指引標明這條規則的研究出處，以及該研究的限制：沒有做真人閱讀實驗、只測英文、沒有測試「要求模型寫清楚」是否有效。
- How I tried it: read the "Why" paragraph under rule 3 and the Sources list
  in the clean copy; ran the focused tests.
- What came back: lines 81-90 name Clark, Martin and Mahowald (2026) with the
  link https://arxiv.org/abs/2610.29162 and state: "The study has three
  limits: it ran no human reading experiment, it measured English only, and it
  did not test whether instructing a model reduces these shapes. The
  Traditional Chinese pairs are this guide's own extension, not a finding of
  the study." The same link is the last entry of the Sources list. I did not
  open the paper, so whether the guide's summary of its findings is accurate
  is not checked here.
- Evidence: `plain-language.md:81-90` and the last Sources line; the "rule 3
  study limits" pin and the study-cited-twice check passed.

## Re-run on 2026-11-14, at 95a6e265

Fix range checked: `git diff 323ececb 95a6e265` (one commit). It changes the
guide's rule 3 lead sentence ("make" became "can make"), the rule 3 "Why"
paragraph, and rewrite step 5; adds one sentence and rewords one in
`loom-workflow/CHANGELOG.md`; and adds three negative substitutions and two
comments to `loom-workflow/tests/loom-visualization/test_references.py`.

Setup, repeated on this run:

- Clean copy: `git worktree add --detach <scratch>/at-rerun 95a6e2650671f9b3e3d588cdf48ae0b37b3ad0bc`;
  the old guide again from a clean copy at `adcd4cbf` (`<scratch>/at-base2`).
- `claude plugin validate <scratch>/at-rerun/loom-workflow`: `Validation passed
  with warnings`, the same two warnings as the first run, in files this change
  did not touch.
- Focused tests in the clean copy, same command as the first run with
  `--directory <scratch>/at-rerun`: `44 passed in 1.96s`. The complete suite
  was not run (skipped by instruction).

Line numbers below are from the clean copy at 95a6e265.

- 1: re-tested — read the rule 3 table again (`plain-language.md:65-75`). The
  fix changed no table row: English pairs for all five shapes, Traditional
  Chinese pairs for four, "A noun used as a verb" English only. The lead
  sentence above the table now reads "Five sentence shapes can make the user
  read the sentence twice". `test_sentence_shape_guidance_present` passed, and
  `test_broken_sentence_shape_guidance_rejected` now also rejects a guide whose
  Chinese pair for the noun-stack shape is removed.
- 2: re-tested — rule 7 (`plain-language.md:162-165`) is word for word as in
  the first run. The fix added a negative case for it: a guide that says
  "Being brief" in place of "Being concise" is now rejected ("rule 7 does not
  name concise"). Both tests passed.
- 3: re-tested — step 5 (`plain-language.md:195`) now reads "Check for
  metaphor words ("like", "imagine", "think of it as", analogies) and for the
  five sentence shapes of rule 3 before sending; replace each metaphor with
  the literal statement and rewrite each shape as rule 3 shows." The section
  still has five steps. The "last rewrite step checks the sentence shapes" pin
  and `test_guide_has_seven_rules_and_rewrite_steps` passed. A fresh agent
  given only this guide and the samples, asked to follow the rewrite steps,
  took the 38 occurrences down to 5 (set X2 below).
- 4: re-tested — in full, because step 5 is the instruction the rewriters
  follow. Two fresh agents with no context, same prompt as the first run:
  agent X2 read the guide at 95a6e265, agent Y2 read the guide at adcd4cbf.
  Counted by me with the rules in `heldout-verdict-final.md`; not blind.

  | Set | Guide | Residual shapes | Changed facts | Guessed causes |
  |---|---|---|---|---|
  | Y2 | before the change | 6 | 0 | 1 (one more borderline) |
  | X2 | after the change, with the fix | 5 | 0 | 0 |

  Y2 residue: EN1 "the orders model the dashboard reads" (connecting word
  dropped); EN1 "The analyst who rebuilt the weekly revenue report in October
  rewrote" (8 words); EN1 "the check on whether the daily revenue snapshot is
  up to date has" (10 words); EN3 "The log the agent attached" (connecting
  word dropped); EN3 "worker pool size"; ZH3 「工作程序池大小上限」.
  X2 residue: EN1 "The analyst who rebuilt the weekly revenue report in
  October rewrote" (8 words); EN1 "The check of how fresh the daily revenue
  snapshot is has" (8 words); EN2 "The rate at which vendor invoices are
  matched as duplicates fell" (8 words); EN3 "the change to the size limit of
  the worker pool is released" (8 words); ZH3 「工作程序池大小上限」.
  Guessed causes: Y2 ZH1 writes 「原因是」 where the Chinese original states
  no relation (the same guess the recorded old-guide set made). Borderline,
  not counted: Y2 ZH2 「因為它依賴的日期解析器處理不了這種年份」 adds a
  「因為」 between two restatements of one original clause. X2 adds none.
  Facts: every number and name (214, 9, 3, 28th, 7%, 2%, 4, 17, 15, 500,
  3172, October, August) is in both sets. Noted, not counted as changed: Y2
  ZH4 writes 「最長 15 分鐘」 for 「長達 15 分鐘」; Y2 adds glosses for
  "join", "is not done yet", and the framings 「目前有兩個問題」 and
  「另外三件事」.

  All three paired trials so far:

  | Trial | Before the change | After the change |
  |---|---|---|
  | Recorded, guide at f35f7430, blind judge | 5 | 4 |
  | My first run, guide at f35f7430 | 4 | 2 |
  | This re-run, guide at 95a6e265 | 6 | 5 |

  Reading: in each pair the changed guide leaves fewer, by one or two out of
  38, and no fact changed in any set. The spread between runs of the same
  guide (2 to 5 after the change, 4 to 6 before) is as large as the gap
  between the guides, so the gap is not distinguishable from chance on this
  evidence. The steadier difference is the guessed cause: the old guide's
  rewriter added one in two of three trials, the changed guide's in none.
- 5: carried over — the fix diff has no hunk in the guide's Scope section
  (`plain-language.md:11-14` is unchanged) and touches no other skill file,
  hook or card; nothing in the fix can widen or narrow what the guide covers.
- 6: re-tested — the "Why" paragraph (`plain-language.md:81-93`) still names
  Clark, Martin and Mahowald (2026) with https://arxiv.org/abs/2610.29162, and
  the same link is the Sources entry at line 446. The fix reworded the
  findings: "longer distances between words that depend on each other, such
  as a subject and its verb"; a new sentence "Against paraphrases with the
  same meaning, almost all of the models also used more nouns as verbs"; and
  the limits are now introduced as "Three limits of the study matter for this
  guide" in place of "The study has three limits". All three limits the
  Acceptance line names are still stated. The "rule 3 study limits" pin
  passed, and the negative test now rejects a guide with the rule 3 citation
  removed ("study not cited in both rule 3 and Sources").
  Checked against the paper by the independent reviewer of this change, not
  by me: the reviewer read the abstract and the HTML page of arXiv 2610.29162
  (the first 100,000 of 114,759 characters) and reported that the citation,
  the nine-model count, the all-nine finding on things as subjects of
  person-only verbs, and the English-only limit match the paper, and that the
  guide wording that was narrower or stronger than the paper is what this fix
  corrected. The last 14,759 characters of the page were not read. I did not
  open the paper myself.

### Set X2 — rewrites under the guide at 95a6e265 (after the change, with the fix)

#### EN1
The join leaves out 214 rows, because the orders model that the dashboard reads does not accept null store ids. The analyst who rebuilt the weekly revenue report in October rewrote that join after the audit, so that it uses the new calendar table. I will put the null handling on the backlog. The check of how fresh the daily revenue snapshot is has a latency of 9 minutes.

#### EN2
The date parser that the importer relies on cannot handle two-digit years. The export ran in 3 minutes. The finance team, which owns the tax ledger, asked for that export before the quarter close on the 28th. The rate at which vendor invoices are matched as duplicates fell from 7% to 2%.

#### EN3
After a restart, the scheduler no longer has its jobs, and the 4 slow workers get no jobs from the queue. I will shut down the legacy cron bridge once the change to the size limit of the worker pool is released. The log that the agent attached shows 17 timeouts.

#### EN4
For 15 minutes, the cache treats out-of-date prices as current. The alert for refunds larger than 500 dollars never fires at night. The on-call engineer who inherited the pricing service set up that alert after the August outage. I approved ticket 3172 without checking it.

#### ZH1
那個關聯查詢少了 214 筆資料。這個查詢是十月重做每週營收報表的分析師在稽核後重寫的，重寫是為了改用新日曆表。儀表板讀取的訂單模型不接受空的門市編號。檢查每日營收快照是否夠新的那項檢查，延遲是 9 分鐘。報表晚出。排程重跑了。

#### ZH2
匯入程式依賴的日期解析器無法處理兩位數年份。那份匯出跑了 3 分鐘。它是負責稅務帳本的財務團隊在 28 日季結前要求的。廠商發票被比對為重複的比率從 7% 降到 2%。比對變快。索引重建了。

#### ZH3
排程器重啟後，不再保有原本的工作。4 個慢速工作程序從佇列拿不到工作。變更工作程序池大小上限的那項修改，上線流程還沒走完。記錄檔顯示 17 次逾時。舊橋接停用。

#### ZH4
快取把過期的價格當成有效的價格，長達 15 分鐘。針對超過 500 元退款的那個警示，在夜間從來不會觸發。它是八月當機後接手定價服務的值班工程師設定的。寄送退款通知用的範本裡，欄位對應錯了。工單 3172 沒關閉。

### Set Y2 — rewrites under the guide at adcd4cbf (before the change)

#### EN1
A join (the query step that matches rows between tables) drops 214 rows, because the orders model the dashboard reads cannot handle rows whose store id is empty. This is the join that was rewritten after the audit to use the new calendar table. The analyst who rebuilt the weekly revenue report in October rewrote it.

I will handle the empty store ids later; that work is now on the to-do list and is not done yet.

Separately, the check on whether the daily revenue snapshot is up to date has a delay of 9 minutes.

#### EN2
The importer cannot read dates whose year is written with two digits. It relies on a date parser, and the parser fails on those years.

The export ran in 3 minutes. This is the export requested by the finance team that owns the tax ledger, which they asked for before the quarter close on the 28th.

The share of vendor invoices matched as duplicates fell from 7% to 2%.

#### EN3
There are two problems: after a restart the scheduler no longer has the jobs it had before, and the queue gives no work to the 4 slow workers.

The log the agent attached shows 17 timeouts.

I will stop using the old cron bridge once the change to the limit on worker pool size is released.

#### EN4
The cache keeps using out-of-date prices for 15 minutes.

The alert for refunds larger than 500 dollars never fires at night. The on-call engineer who inherited the pricing service set it up after the August outage.

I approved ticket 3172 without checking it.

#### ZH1
有一個關聯查詢（把不同資料表的資料對起來的那一步）少了 214 筆資料，原因是儀表板讀取的訂單模型處理不了門市編號是空的資料。這個查詢是稽核後為了改用新日曆表而重寫的，重寫的人是十月重做每週營收報表的那位分析師。

另外三件事：

- 檢查「每日營收快照是不是最新」的那項檢查，延遲是 9 分鐘。
- 報表比較晚才出來。
- 排程重新跑過了。

#### ZH2
匯入程式讀不了年份只寫兩位數的日期，因為它依賴的日期解析器處理不了這種年份。

那份匯出跑了 3 分鐘。它是負責稅務帳本的財務團隊在 28 日季結前要求的。

廠商發票被比對為重複的比率從 7% 降到 2%。比對變快了，索引也重建了。

#### ZH3
目前有兩個問題：排程器重啟後，重啟前的工作沒有留下來；佇列沒有把工作分給 4 個慢速工作程序。

- 記錄檔顯示 17 次逾時。
- 「調整工作程序池大小上限」這項變更，上線流程還沒走完。
- 舊橋接停用。

#### ZH4
快取會繼續使用過期的價格，最長 15 分鐘。

針對超過 500 元退款的那個警示，在夜間從來不會觸發。這個警示是八月當機後接手定價服務的值班工程師設定的。

另外兩件事：

- 寄送退款通知用的範本，欄位對應錯了。
- 工單 3172 沒有關閉。
