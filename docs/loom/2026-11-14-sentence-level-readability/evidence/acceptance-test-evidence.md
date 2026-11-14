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
