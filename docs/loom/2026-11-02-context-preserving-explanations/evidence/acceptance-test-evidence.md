# Context-preserving intent confirmation — acceptance test evidence

Historical evidence below is retained verbatim. Its all-works conclusion is superseded by the dated renewed assessment at the end of this file.

Tried on 2026-11-03, in a clean copy of the project at 242ba265a2a7b648356fd6aa082fc5e5ffe9e93c.

## Setup and execution boundary

An independent acceptance tester used a clean tracked-file archive, not the implementation worktree:

```text
mkdir -p /tmp/loom-context-acceptance-242ba265
git archive 242ba265a2a7b648356fd6aa082fc5e5ffe9e93c | tar -x -C /tmp/loom-context-acceptance-242ba265
python3 /tmp/loom-context-acceptance-242ba265/scripts/sync_codex_manifests.py --check --all
exit 0, no output
```

The README's Codex setup uses a marketplace and plugin installation. To avoid changing the user's installed plugins or testing the remote main version instead of this commit, this exercise loaded the exact clean-copy station sources into fresh native responder agents. The clean-copy Codex manifests point to `./skills/`; their versions were loom-code 3.57.0 and loom-design 2.20.0, and the manifest synchronization check passed. This verifies source loading and manifest consistency, not a fresh marketplace installation or host discovery. Each responder read its station resources successfully and returned actual replies below.

Two fresh-context native responders ran sequentially: `capture_responder` loaded capture-intent; `code_responder` loaded code-only write-plan and confirm-intent without loading capture-intent. Both received only clean-copy resource paths, fixture IDs 4/5/6, and bounded execution context: separate scenarios, already-ratified standing documents if relevant, second-vendor suggest, stop at confirmation, no edits or publication. The captured responses are the actual returned messages, not tester-authored examples. Each owner used one fresh responder for its three scenarios; these are six sampled replies in two isolated contexts, not six fully independent agent sessions. The fixtures are from `loom-design/skills/capture-intent/test-prompts.json`.

Before each of the two spawns, the packaged dispatch resolver was actually run:

```text
echo '{"event":"initial","main_profile":{"model":null,"effort":null},"task_evidence":{},"capabilities":{},"inheritance_guaranteed":true,"completed_redispatches":0}' | /tmp/loom-context-acceptance-242ba265/loom-code/scripts/loom-python --repair --script dispatch_profile.py
{"completed_redispatches":0,"effective_profile":"inherited","outcome":"dispatch","overrides":null,"reason":"unobservable-main-profile","requested_profile":null,"task_class":"ordinary","uncertainty":null}
```

Both invocations exited 0. Both spawns omitted model and effort overrides. Main profile components were unavailable; no model tier was inferred.

## Captured capture-intent responses

### Fixture 4 — simple familiar request

> 發行說明仍顯示上個月的日期，讓客戶誤以為最新版本已經過時。這次只把日期改為最新版本的正確發行日期，其餘內容不變。
>
> 回答「是」也會授權我在審查與發布檢查通過後，推送變更並建立可供審查的 PR；合併另行決定，你也可以在發布前取消這項授權。是否確認這個範圍？

### Fixture 5 — unfamiliar concepts and multiple problems

> 這次要修正兩個會影響背景工作的問題：每個工作應依自己的規則選擇執行者；失敗後重做的次數，也應受到各自設定的上限約束。
>
> 「執行者選擇設定」決定由誰處理工作。目前工作誤用了別人的設定，完成後應各自使用自己的設定。「失敗重試規則」決定工作失敗後如何重做；目前失敗的工作會無限重試、堵住佇列，完成後應在達到設定上限時停止。
>
> 驗收範圍是：
>
> 1. 每個工作使用自己的執行者選擇設定。
> 2. 失敗工作的重試次數遵守各自設定的上限。
> 3. 原本能成功完成的工作維持既有行為。
>
> 這次只修正內部行為，不新增介面。
>
> 回答「是」也會授權我在審查與發布檢查通過後，推送變更並建立可供審查的 PR；合併另行決定，你也可以在發布前取消這項授權。是否確認上述需求與範圍？

### Fixture 6 — detailed correction round

> 這次要讓每個工作依自己的規則選擇執行者，修正誤用其他工作設定、造成結果不一致的問題。我先前只說「修正 profile」，省略了這層關係，沒有把需求說清楚。
>
> 這裡的「profile」指的是你提到的「選擇由誰執行工作的設定」。它的作用是決定每個工作交給誰執行。需求的重點有三個：
>
> - **目前的問題**：工作使用了另一個工作的選擇設定。
> - **造成的影響**：使用錯誤的設定後，工作產生不一致的結果。
> - **想要的結果**：每個工作都使用屬於自己的選擇設定，依自己的規則決定執行者。
>
> 因此，驗收要能確認每個工作確實使用自己的設定，沒有再誤用另一個工作的設定。這裡尚未判定誤用是怎麼發生的；修正方法由後續查證決定。
>
> 這是同一輪需求的修正確認。回答「是」也會授權我在審查與發布檢查通過後，推送變更並建立可供審查的 PR；合併另行決定，你也可以在發布前取消這項授權。以上是否正確表達你的需求？

## Captured code-only write-plan responses

### Fixture 4 — simple familiar request

> 發行說明仍顯示上個月的日期，讓客戶誤以為最新版本已經過時；這次只把日期更正為最新版本的正確發行日期，其餘內容不變。
>
> 回答「是」也代表授權我在完成審查及發布檢查後，以不覆寫遠端歷史的方式推送變更，並建立可供審查的 PR（合併請求）；合併另外決定，發布前你可以明確退出這項授權。這樣理解正確嗎？

### Fixture 5 — unfamiliar concepts and multiple problems

> 這次要修正背景工作的執行與重試行為，讓每項工作依自己的設定執行，失敗時也不會無限重跑而堵住佇列。
>
> 「工作分派設定」決定由哪個執行者處理工作；目前有工作誤用另一項工作的設定，修正後每項工作都應使用自己的選擇。「重試規則」決定工作失敗後如何再次執行；目前失敗工作會一直重跑，修正後應在各自設定的重試上限停止。既有成功工作的行為維持不變，也不新增操作介面。
>
> 回答「是」也代表授權我在完成審查及發布檢查後，以不覆寫遠端歷史的方式推送變更，並建立可供審查的 PR（合併請求）；合併另外決定，發布前你可以明確退出這項授權。以上需求是否正確？

### Fixture 6 — detailed correction round

> 你要修正的是「每項工作由誰執行」的選擇：每項工作應使用自己的選擇，避免誤用另一項工作的選擇而產生不一致的結果。
>
> 我先前說的「profile」，指的是你提到的工作執行者選擇設定，也就是決定由誰處理該項工作的規則。只說「修正 profile」漏掉了它的用途、現在的錯誤，以及完成後應有的結果。
>
> 需求應完整表達為：
>
> - 現在的問題：工作會用到另一項工作的執行者選擇，造成結果不一致。
> - 想要的結果：每項工作都依照屬於自己的選擇執行。
> - 驗收重點：確認工作實際使用的是自己的選擇，不會誤用別項工作的選擇。這不代表要求不同工作產生相同結果。
>
> 這裡尚未判定錯誤原因，也沒有預先指定修法。
>
> 這是同一輪需求修正後的再次確認。回答「是」也代表授權我在完成審查及發布檢查後，以不覆寫遠端歷史的方式推送變更，並建立可供審查的 PR（合併請求）；合併另外決定，發布前你可以明確退出這項授權。這次的說明是否準確表達你的需求？

## 1. 使用者閱讀需求確認說明後，能辨識討論對象、目前問題與影響、預期結果，以及此次確認的範圍與後果。

- How I tried it: read each actual reply above against its fixture, separately for both entry owners.
- What came back: fixture 4 identifies release notes, old date, customer confusion, date-only correction and unchanged other content. Fixture 5 connects job ownership and retries to correct worker selection and bounded failures, queue blockage, successful-job compatibility and no new interface. Fixture 6 restores the supplied definition, cross-job mix-up, inconsistent results and own-selection outcome. Every reply discloses conditional publication, opt-out and separate merge authorization.
- Evidence: all six captured replies. No claim of a human comprehension study is made. The supplied unfamiliar-concept fixture provides no separate impact for the wrong profile; replies do not invent one, and preserve its supplied queue-blockage impact for endless retries.
- Result: works in the sampled source-loaded conversations.

## 2. 需求確認說明允許依情境選擇措辭、篇幅與呈現方式，不必套用固定填空句型或逐項顯示固定章節。

- How I tried it: compared actual reply structures across both owners and all three scenarios; ran the focused contract check below covering both owners and reversed obligations.
- What came back: short prose for fixture 4; capture-intent uses numbered acceptance for fixture 5 while code-only uses connected prose; fixture 6 uses a longer corrective explanation and bullets. No reply repeats a compulsory section list or fill-in script. The guidance was read directly and treats examples/headings as optional.
- Evidence: six captured replies; `test_first_confirmation_preserves_context_with_flexible_expression` and its selected mutation cases: six tests passed.
- Result: works; observed variation supports flexibility, without claiming all possible formats have been exercised.

## 3. 簡單需求的說明保持簡短，涉及陌生概念或多項問題的說明仍保留理解必需的背景；使用者不必追問核心名詞才能理解正在確認的事情。

- How I tried it: both owners received fixture 4 (familiar), 5 (two unfamiliar concepts) and 6 (explicit request for detail after an unexplained label).
- What came back: both familiar replies contain two short paragraphs; both unfamiliar replies explain what worker selection and retry rules do, link failure behavior to queue blockage, preserve limits and compatibility; both correction replies define profile before expanding the wrong-selection problem and intended result. Neither requires a further question to discover the supplied core term's role.
- Evidence: each owner's fixture 4/5/6 sections, not text assertions alone.
- Result: works for these samples; later ordinary conversations may differ.

## 4. 需求確認仍只要求使用者確認需求與必要授權，不要求使用者評斷實作方案、規格品質或審查結論。

- How I tried it: inspected every actual question and its preceding authorization disclosure in all six replies.
- What came back: all questions ask whether the scope or restatement is correct. None asks the user to choose an implementation, assess specification quality, approve a review verdict or accept a guessed cause. Both fixture-6 replies keep renewed confirmation within the correction round. Publication remains conditional on review/checks and separate from merge.
- Evidence: closing paragraphs in all six responses and explicit method deferral in both fixture-6 replies.
- Result: works in the sampled conversations. No publication or merge was performed.

## Focused contract check

The system Python attempt failed before collection: `No module named pytest`. The isolated locked uv attempt failed before execution because the sandbox denied creating a uv cache lock temporary file. Neither is counted as a test result. The available project-compatible interpreter then ran the targeted contract checks in the clean archive:

```text
/Users/kouko/.conda/envs/dbt-redshift/bin/python3 -m pytest loom-design/tests/spec/test_capture_intent_contract.py -q -k first_confirmation
...... [100%]
6 passed, 27 deselected in 0.11s
```

These text checks cover both owners and polarity mutations, supplementing rather than replacing the actual conversations. The full locked package suite is left to the automated test suite, which runs before the change is accepted and blocks it on failure:

```text
uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q
```

No full package suite was run by the acceptance tester. The station reported its earlier full-suite pass; that report is not substituted for this acceptance run.

## Limits and findings

- No acceptance-blocking finding observed in the four requested criteria.
- Six bounded fixture replies from two fresh source-loaded contexts establish sampled behavior. They do not prove every host's runtime loading, marketplace installation, human comprehension, future response consistency, or causal superiority over an unchanged baseline.
- No installation, publication, remote write or change to the user's real data was performed. The archive and report/evidence are the only test artifacts created.
- The station supplied no dismissed finding of severity important or worse. No acceptance step was skipped by user instruction.

## Re-run on 2026-11-03, at 1d481a176e624657bfe2b2aa7bcb36305378c502

### Clean setup and provenance

This independent tester did not implement the change and made no source/test edits. The fix range `b6f666d7..1d481a17` changes both first-confirmation owners, including drafting fidelity, brevity and publication wording; therefore all four rows were re-tested, none carried over. The confirmed intent has `needs-design: no`; no omitted spec flows exist. No user-directed skip or dismissed important finding was supplied. The retained Build report explicitly leaves semantic failures open.

Commands independently executed:

```text
git clone --no-hardlinks --no-checkout . /tmp/loom-context-renewed-acceptance-1d481a17
git -C /tmp/loom-context-renewed-acceptance-1d481a17 checkout --detach 1d481a176e624657bfe2b2aa7bcb36305378c502
HEAD is now at 1d481a17 docs(loom): record drafting-boundary verification and remaining risk
```

The following commands ran inside that clean clone:

```text
python3 scripts/sync_codex_manifests.py --check --all
exit 0, no output
/Users/kouko/.conda/envs/dbt-redshift/bin/python3 loom-code/scripts/loom_checker.py contract --require 2.1
contract 2.3.1 satisfies requires-contract >=2.1
/Users/kouko/.conda/envs/dbt-redshift/bin/python3 -m pytest loom-design/tests/spec/test_capture_intent_contract.py loom-design/tests/spec/test_intent_drafting_fidelity.py -q
42 passed in 0.13s
```

The system `python3` checker attempt failed importing `yaml`; rerunning with the available project-compatible interpreter succeeded. No package installation or full package suite was run. README setup points to marketplace installation; that would install remote content and change the user's installed plugins. Instead this run checked candidate manifest consistency and checker loading locally, and verified the already-executed candidate CLI loading evidence described next. This does not establish normal marketplace discovery, a fresh installed-plugin launch, or loading on other hosts.

Behavioral inputs: `/tmp/loom-context-claude-dogfood-retest/blind-packet-r2.json`, all eight `{case}-r2.jsonl` raw transcripts, their summaries, `export-manifest-r2.json`, and `settings-run.json`. These are actual prior first-party Claude Code executions, not tester-authored sample replies. This tester did not call an external model or execute a new native responder. Each packet reply was independently compared to its raw JSONL `type: result` text: eight exact matches; all eight raw initializations say `claude-sonnet-5-5`, all eight result records have `is_error: false` and zero permission denials. Those are execution results, not eight behavioral passes. The raw init reports inline code 3.58.0/design 2.21.0; code-only tool output loads the candidate confirmation resource. Settings disable hooks and memory, restrict network and deny candidate-bundle writes. This is the candidate inline-plugin boundary, not ordinary installed-plugin behavior.

The export manifest identifies source `4d4d12cdf56073482d8091306b022ddc747d4f05`. Independently computed SHA256 of each owner in the clean tested HEAD and the candidate bundle matches both each other and the manifest:

| Owner | SHA256 |
|---|---|
| `loom-design/skills/capture-intent/SKILL.md` | `e77d6c46aa7ae5cb4551cd9135533ac8ac165ef6690b24badf168646b639460d` |
| `loom-code/skills/write-plan/references/confirm-intent.md` | `2b0bd9c175994dc211b81f656b584e7e45c90df514b5868a0aac1346a8a757cd` |

The two owners now explicitly say: `Keep own-rule isolation separate from same-worker or same-result guarantees.` Passing source checks and this strengthened instruction do not erase a contrary actual reply.

### 1. Context, intended outcome, scope and consequences — partly

- How tried: compared both owners' simple (4), multiissue (5), and detailed correction (6) replies and saved drafts against the original user requests; also assessed capture random-choice (7) and code unknown-date (8). Inspected raw replies, not audit votes.
- Simple: both identify release notes, incorrect displayed date, customer confusion and date-only correction. Asking the true date is legitimate missing-fact intake, not a failure.
- Multiissue: both preserve own-rule selection, configured retry limit, blocked queue, successful-job compatibility and no new interface. Capture's `各自由自己指定的 worker 處理` is stronger wording than selecting by a rule; it should not be treated as proof of deterministic selection without more evidence. Code's `每個工作仍由自己的派工設定選出 worker` preserves rule ownership.
- Correction: code-6 explicitly changes the outcome to `同一個工作在相同條件下,會由同一個執行者執行,結果一致。` User said the rule chooses who runs each job and the bug uses another job's rule; they did not promise deterministic worker/output across runs. This is a material unsupported guarantee, even though the reply later says the selection rule itself will not change. It also substitutes `選擇結果` for the supplied selection rule.
- Capture-6 is more qualified: `重複執行同一組工作,每個工作的執行者與結果一致,不因其他工作而改變。` Its limit says `隔離的是規則本身。我不承諾不同工作會得到相同的執行者或相同的結果。` The causal tail plausibly intends only cross-job isolation. Accordingly this is recorded as ambiguity, not the same explicit deterministic guarantee as code-6. However the limitation addresses different jobs, not one job's legitimate variation across runs; the repeated-execution acceptance remains ambiguous. Code-6 alone establishes the material failure; no need to overstate capture-6.
- Random-choice counterexample capture-7 preserves own-list random choice and expressly disallows fixing one worker; it does not rescue code-6's unstated determinism. Unknown-date code-8 leaves the date unverified and does not substitute today.
- Consequences: code-4, capture-4, capture-5 and code-5 disclose automatic publication/opt-out and separate merge. Capture-6 says `我預設不記錄這項授權`; capture-7 requires explicit extra authorization; code-8 promises a later authorization question. These differ from the unchanged default informed-yes publication contract, even though no unauthorized publication occurred.
- Exact contract comparison: capture-intent Step 4 says `Disclose automatic publication and offer opt-out before answering.` and `after informed yes only; otherwise omit.` Code-only confirmation says `Publication defaults to automatic; explicitly offer opt-out before publication. Disclose before the answer.` By contrast capture-7 says `你也可以選擇授權**自動發佈**` and `沒有明說的話,我就不記錄這項授權。`; code-8 says `確認前我會問你，之後是否允許` while already asking `請確認、修正`. The defect is altered/deferred disclosure and an added choice, not absence of authorization metadata in an unconfirmed draft. Severity important because the task explicitly preserves existing confirmation/authorization conditions. Capture-6's `我預設不記錄這項授權` likewise changes the stated default; no actual unauthorized write is alleged.
- Result: partly. Core context often survives, but scope strength and confirmation consequences are not consistently faithful.

### 2. Flexible expression — works

- How tried: read both tested owners and all eight actual replies; independently ran the two narrowly related test modules (42 passed), including flexible first-confirmation and fidelity guards.
- What came back: owners permit optional examples/headings and free wording. Actual replies vary between prose, numbered/bulleted lists and a comparison table (capture-6); no fixed fill-in wording is required. The many headings in actual replies are a brevity problem, not evidence that the contract mandates a fixed format.
- Result: works for the permitted flexibility and observed sample formats. Text checks supplement actual behavior; they do not establish semantic reliability. The full suite command is `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`. The station reports a previous Build pass at functional `765c50d6`; this tester did not run that suite. Final verification is not skipped but is held while material semantic failures remain; no successful future attestation is promised.

### 3. Proportional length and explained concepts — fails

- How tried: assessed both owners across all three core scenarios and the two counterexamples, including first sentence, necessary background, and amount of workflow bookkeeping.
- Simple code-4 is 846 characters and capture-4 747 characters (Python Unicode `len` of packet result), with multiple headings, artifact status/path, classification, next-station steps and branch/commit details for a date-only request. The true-date question and publication disclosure are necessary; the surrounding workflow inventory is not. This independently contradicts the requirement to keep familiar requests short.
- Multiissue replies explain dispatch/profile and queue blockage, but capture-5 leaves `worker` in English without defining it and mostly demonstrates what it does rather than its name. This alone is not the decisive failure.
- Correction capture-6 opens `那個詞不是你說的,我也無法告訴你它指什麼。` and sends `profile` back as an unresolved equivalence question even though the user supplies the role of worker selection and asks to repair the assistant's earlier shorthand. Code-6 likewise declines to connect its own label to the supplied meaning. Both do explain the user-supplied rule afterward, so this is not total absence of context; it is incomplete repair with unnecessary uncertainty about the assistant's word.
- Random and date counterexamples keep key supplied qualifications. None makes the simple replies short or removes the correction guarantee.
- Result: fails. Pending interviews and incomplete factual values are not counted as failures; excessive workflow narration and the unresolved repair are the relevant observations.

### 4. Confirm requirements and necessary authority only — partly

- How tried: inspected every requested decision in all eight replies, with particular attention to added user choices and implementation restrictions.
- Most questions concern requirement accuracy, missing facts and publication; no reply asks the user to judge a spec or reviewer verdict.
- Code-6 adds `一個工作自己沒有設定選擇時,該用預設值,還是報錯?` and an acceptance line for missing selection, although the request concerns using another job's existing rule. This creates a new outcome/scope decision before establishing that the case belongs to the requested fix. Merely asking a question is not the violation; elevating the unsupported case into Acceptance is.
- This missing-setting question concerns visible outcomes, not implementation approval; it supports the row-1 scope-fidelity concern rather than independently proving a row-4 failure. The row-4 partial verdict rests on the unqualified no-function restriction below.
- Capture-7 asks confirmation of `不新增任何介面(函式、選項、設定、指令都不加)` while the request only says no new interface. Its written draft says `no new public function`, a narrower and defensible interface restriction. The spoken unqualified `函式` can prohibit internal helper functions and therefore asks the user to endorse an unnecessary implementation restriction. This mismatch must be repaired; it is not proof that every no-interface interpretation is wrong.
- Result: partly. No implementation proposal review is requested, but capture-7's spoken confirmation includes an unsupported restriction on implementation. A missing-fact interview alone would not fail this row.

### Current findings and boundary

- Important: code-6 adds deterministic same-worker/same-result guarantees. Close by preserving rule ownership and supplied qualifiers without adding temporal consistency, then observe actual corrected intake behavior.
- Important: both simple replies are dominated by workflow bookkeeping; correction replies fail to cleanly repair the assistant's unexplained label. Close with actual concise simple confirmations and contextual correction samples.
- Important: added missing-selection Acceptance and unqualified no-function restriction expand confirmation scope; remove unsupported obligations and retest the affected surfaces.
- Important: some replies replace the existing informed-yes publication default or defer its disclosure. Preserve the existing confirmation consequence without extra decision points.
- Capture-6's repeated-run sentence is ambiguous after its causal qualifier; it is not independently classified as a material deterministic guarantee. No important finding is dismissed merely because tests pass.
- No source repair, external message, new model run, commit, publication, or modification of user-owned data occurred in this independent run. Existing evidence above and original CLI failure samples are retained as history; current verdicts supersede the earlier all-works report.

## Re-run on 2026-11-03, at aa9c8d1e58dba50a999f7e0e47f4e369002addb2 — authorized iteration 4

### Clean setup and provenance

This independent witness did not implement source or tests. All four rows were re-tested because fix range `1d481a17..aa9c8d1e` changes both intake owners, example loading and composition. No spec exists by the confirmed `needs-design: no` decision. This is candidate 4 of the user's additional five-iteration allowance; failed history above is retained, not reset. No user-directed skip or dismissed important finding was supplied.

Commands run:

```text
git clone --no-hardlinks --quiet . /tmp/loom-context-acceptance-i4-clean
git -C /tmp/loom-context-acceptance-i4-clean rev-parse HEAD
aa9c8d1e58dba50a999f7e0e47f4e369002addb2
```

The following ran in that clean clone, all exiting zero:

```text
python3 scripts/sync_codex_manifests.py --check --all
(no output)
/Users/kouko/.conda/envs/dbt-redshift/bin/python3 loom-code/scripts/loom_checker.py contract --require 2.1
contract 2.3.1 satisfies requires-contract >=2.1
/Users/kouko/.conda/envs/dbt-redshift/bin/python3 -m pytest loom-design/tests/spec/test_capture_intent_contract.py loom-design/tests/spec/test_intent_drafting_fidelity.py -q
57 passed in 0.13s
/Users/kouko/.local/bin/claude plugin validate /tmp/loom-context-acceptance-i4-clean/loom-code
Validation passed
/Users/kouko/.local/bin/claude plugin validate /tmp/loom-context-acceptance-i4-clean/loom-design
Validation passed with warnings
```

Validator warnings: both plugin directories lack a listing icon; Claude ignores design's `requires-contract` field. The separate checker above accepts the contract. README's Claude setup installs from the marketplace; doing that would install remote content and mutate installed state, not test this candidate. Local validation plus the actual inline-plugin initialization below establishes candidate loading only. Normal marketplace installation, automatic triggering, live hooks and other hosts remain unverified.

Independent SHA256 recomputation found **376/376** export-manifest entries identical in both clean HEAD and `/tmp/loom-context-claude-dogfood-retest/candidate-bundle`. Manifest `export-manifest-i4.json` names the exact tested HEAD. Thus the already executed behavioral payload matches this clean source across all exported files, not merely two owner files.

Read `blind-packet-i4.json`, all ten original `{case}-i4.jsonl` result records, their initialization/tool traces and summaries, `run_authorized_i4.py`, both detailed-repair prompts and `settings-run.json`. All ten packet replies exactly equal raw `type: result` text; all ten have exit 0, `is_error: false`, no permission denials and model `claude-sonnet-5-5`. Init lists inline code 3.58.0/workflow 5.19.0, and design 2.21.0 for capture cases. The runner explicitly selects medium effort. Tools request the examples in all ten cases; Bash `cat`/`sed` also counts as reading. Code-h2 initially looks in a nonexistent `loom-code/references` directory, receives a tool error, then successfully reads the correct `skills/write-plan/references` files; this recovered navigation error is not a permission denial or behavioral pass. No fixture commit was produced. Settings disable hooks/memory, restrict network, and deny bundle writes. These are ten actual executions made before this witness, not ten new calls or ten semantic passes. No model was called by this witness.

### 1. Context, outcome, scope and consequences — partly

- Tested both owners on unknown-date intake (code-4/capture-4), multiple background-job issues (code-5/capture-5), detailed shorthand repair (code-6/capture-6), plus capture-7 randomness, code-8 explicitly unknown date, capture-h1 currency and code-h2 known command correction.
- All preserve the central subject, reported issue and target. Multiissue cases retain own-rule selection, configured retry limit, blocked queue, successful-job preservation and no new interface. Both detailed repairs now connect `profile` to the already supplied rule and explicitly avoid a same-worker/same-result guarantee. The earlier deterministic guarantee and label-returning failures were not reproduced.
- However code-6 says `如果原本的選擇有隨機性,隨機性會保留,改的只是從哪份清單挑。` The conditional randomness clause itself is legitimate preservation, but `從哪份清單挑` concretizes an unverified mechanism: this request says a rule chooses who executes a job; unlike capture-7, it never supplies eligible lists. The repair introduces another mechanism the user would have to accept or correct. Both case-6 replies also add unchanged-interface constraints not stated in those requests. Preserving unrelated behavior is a defensible narrow default, so this witness does not independently elevate that alone to a material scope failure. Code-6 additionally discusses internal helpers; that is unnecessary implementation exposition, not a demonstrated request to approve a design.
- Capture-h1 preserves the currency owner, legitimate amount variation, unchanged export format and no rewriting existing exports. Code-h2 preserves the verified replacement command and other guide content.
- All seven ready confirmations bind yes to scope plus non-forced upload/PR, offer opt-out and separate merge. Code-5, capture-5, code-6, capture-7 and code-h2 explicitly put checks before both upload and PR. Capture-6 and capture-h1 place the checks grammatically before PR after mentioning upload; this leaves timing less clear, but does not explicitly promise unchecked upload. Capture-h1 says `如果你不想自動發佈，在回答前告訴我就好`; it offers an early opt-out without explicitly removing later opt-out, so this is not independently classified as a reversal of authorization policy. There was no actual publication. The three pending date interviews legitimately defer full confirmation disclosure; code-8's eventual authorization wording is not counted as an added confirmation stop.
- Important finding: the detailed code repair substitutes an unsupported list mechanism for the supplied selection rule. Close by preserving the supplied abstraction and checking actual replies, without borrowing case-7 facts. Verdict partly, not the previous deterministic failure.

### 2. Flexible expression — works

- Both owners and their references explicitly permit optional headings, wording, grouping and length. All ten actual replies were read: unknown facts use prose plus short source choices; detailed repairs use explanations and lists; capture-7 uses connected paragraphs; other replies use headings and numbered lists. No fixed fill-in script is imposed.
- Fifty-seven narrowly related tests passed in the clean copy, covering optional composition, drafting fidelity, example boundaries and polarity guards. These source checks supplement actual output; they do not prove brevity or comprehension.
- The full suite belongs to the automated test suite, which runs before the change is accepted and blocks it on failure: `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`. The witness did not run it. The station reports a prior Build pass in `/tmp/context-outline-i4-suite.log`; this is not substituted for independent behavioral acceptance. Final verification is not skipped, but unresolved semantic findings preclude promising its future success.

### 3. Proportionate explanation and concept repair — partly

- Both date-only interviews now explain the missing actual date, ask for it or a record, and do not invent today's date. These are valid pending interviews, not ready confirmations. They still include private status narration, but are materially shorter and more focused than the earlier samples. Code-8 likewise preserves unknown facts.
- Both detailed repairs now define the assistant's own shorthand from the user's supplied meaning, acknowledging the omission rather than making the user define it. Capture-7 explains own eligible-list selection while preserving randomness. Both multiissue replies connect worker selection, failed retries and queue blockage; the currency variation uses the supplied domain terms accurately.
- Important remaining brevity issue: capture-h1 repeats the unchanged-format/no-existing-file-write and amount-variation scope under acceptance, scope and out-of-scope headings. It then adds `這是內部修正（engineering），不需要另外寫設計規格，確認後會直接進入規劃。我不會問你任何實作做法的問題。`, `另外兩點`, assertions about no irreversible design choice and not guessing workaround/frequency, plus open/confirmed status, branch and commit inventory. These are exactly the internal inventory and repeated field labels the candidate's final-message check says to remove, not needed explanations of currency ownership. Its request asks what is confirmed, not for a station report.
- The known simple correction code-h2 repeats the same one-line command change through Problem, Goal, Acceptance and Scope, quotes an unrelated unchanged troubleshooting paragraph, then appends the draft path, open status, commit/branch/plan inventory. Necessary authorization disclosure is not counted as excess. A simple correction is correctly understood but still fails to remain concise in content. Capture-5 similarly repeats outcome bullets as acceptance bullets and opens with status/path bookkeeping; capture-6 appends status/path/branch inventory after an otherwise useful detailed repair.
- No arbitrary word/character cap was applied, and use of headings alone is not a failure. The finding concerns repeated information and pure internal work exposition after the necessary scope and consent are already available. Close by observing actual concise known-fact confirmations across both owners, retaining required disclosures and detailed explanations where requested. Verdict partly: concept repair improves, proportional brevity is not yet consistent.

### 4. Requirements and necessary authority only — works

- Across all ten results, requested decisions are missing factual dates/records, correctness of the intended outcome, and upload/PR authorization with separate merge. No request asks the user to rate implementation, specification quality or reviewer verdicts.
- Capture-7 no longer expands no-interface into a ban on every function. Code-6 explicitly says private helper functions may be added; that exposition is unnecessary, but it is not a requirement that the user choose or approve a helper design. Its unsupported list description is recorded under row 1 rather than misclassified as a user-judgment demand.
- No extra implementation-choice acceptance line or missing-setting policy request appears in this batch. This is a sampled behavioral result, not proof that every future intake will respect the boundary.

### Current boundary and return to the station

- Acceptance: 1 partly; 2 works; 3 partly; 4 works. All rows re-tested; no carried-over verdict.
- Important findings remain: code-6's unverified list mechanism; repeated scope and internal bookkeeping especially capture-h1/code-h2. No finding is waived because tests or execution exits pass. Do not declare a global dogfood pass or unconditional readiness for finalization.
- No new source/test edit, model run, external message, commit, remote write or publication. Only report/evidence changed. Prior failures remain above. Human understanding, ordinary installed-plugin loading/triggering, other hosts, future reliability and causal superiority over an unchanged baseline remain unproven.

## Re-run on 2026-11-03, at 010d79e7afad64f2494b0201090a8dc1e272b089 — authorized iteration 5

### Clean setup and provenance

Independent witness, no source/test implementation. Fix range `aa9c8d1e..010d79e7` splits the primary adaptable template from the optional example gallery and clarifies that both publication actions require prior checks; both intake owners change. All four Acceptance lines were re-tested in full, none carried over. The confirmed intent and retained plan remain the requirements; `needs-design: no` means no missing spec flows. This is the fifth and final additional authorized iteration, not a reset of earlier failed history. No user-directed skip or dismissed important finding was supplied.

```text
git clone --no-hardlinks --quiet . /tmp/loom-context-acceptance-i5-clean
git -C /tmp/loom-context-acceptance-i5-clean rev-parse HEAD
010d79e7afad64f2494b0201090a8dc1e272b089
```

Inside the fresh clone, these checks exited zero:

```text
python3 scripts/sync_codex_manifests.py --check --all
(no output)
/Users/kouko/.conda/envs/dbt-redshift/bin/python3 loom-code/scripts/loom_checker.py contract --require 2.1
contract 2.3.1 satisfies requires-contract >=2.1
/Users/kouko/.conda/envs/dbt-redshift/bin/python3 -m pytest loom-design/tests/spec/test_capture_intent_contract.py loom-design/tests/spec/test_intent_drafting_fidelity.py -q
65 passed in 0.14s
/Users/kouko/.local/bin/claude plugin validate /tmp/loom-context-acceptance-i5-clean/loom-code
Validation passed
/Users/kouko/.local/bin/claude plugin validate /tmp/loom-context-acceptance-i5-clean/loom-design
Validation passed with warnings
```

Warnings are the existing missing listing icons and Claude's ignored design `requires-contract` field; the independent contract checker accepts compatibility. README marketplace setup would mutate installed state and fetch remote content rather than this candidate. Local validation and actual inline-plugin initialization establish the bounded candidate-loading setup; ordinary marketplace installation and automatic discovery/triggering remain unverified.

Independently recomputed SHA256 for all **378/378** `export-manifest-i5.json` entries: clean source and current candidate bundle both match every manifest hash, whose source commit equals the tested HEAD. Read `blind-packet-i5.json`, all ten original `{case}-i5.jsonl` result/init/tool records and summaries, settings and changed owners/template. All ten packet replies equal original result text exactly; all exit 0, `is_error: false`, zero permission denials, model `claude-sonnet-5-5`. Init lists inline code 3.58.0 and workflow 5.19.0; capture cases also load design 2.21.0. Primary-template reads were requested ten times; optional gallery reads zero times. The gallery is optional, so zero is not a failure and does not support claiming gallery usage. Settings retain medium effort, disabled hooks/memory, restricted network and read-only candidate bundle. Code-8 contains one shell tool error during directory/absence inspection (its output also reports the contract accepted); the run recovered and completed. Zero permission denials is not a claim that every shell command succeeded. No fixture commits occurred. These are already executed first-party calls, not new witness model calls and not ten semantic passes.

### 1. Subject, problem, intended scope and consequences — partly

- Re-tested code-4/capture-4 simple unknown dates, code-5/capture-5 multiple issues, code-6/capture-6 detailed shorthand repair, capture-7 random eligible lists, code-8 explicitly unknown date, capture-h1 currency and code-h2 verified command correction, including any saved drafts.
- Every case identifies its central subject, issue and intended outcome. Date interviews leave missing dates unknown. Multiple-issue cases retain selection ownership, configured retry limits, blocked-queue impact and successful-job preservation. Currency keeps legitimate amount variation, format and existing-file preservation; known command correction uses the supplied verified command. Both detailed repairs now distinguish the role of a selection rule from an unverified list/file/cache representation; the previous code-6 list-mechanism finding is not reproduced.
- **Important current scope contradiction, capture-6:** its desired-outcome table says `每個工作都用它自己的選擇規則來決定由誰執行,不再借用別的工作的規則。` Later it says `範圍只含目前受影響的工作。我不會自行擴大到「所有工作」。` The latter is explicitly a future correction boundary, not merely a description of which jobs are presently observed to fail. The user describes worker selection as choosing who runs **each job** and reports borrowed selection; no restriction to a presently enumerated failing subset is supplied. The table preserves the universal target, so the output is contradictory rather than consistently narrowed. No draft was written; this evidence establishes an inconsistent explanation, not an implemented subset-only fix. Close by retaining the each-job target while leaving the unknown observed failing population as an unknown fact, then verifying actual replies.
- Code-6 also says it will write only `受影響的工作`, but its stated outcome remains every job. That is less explicit than capture-6's scope exclusion and is not independently counted as a second definite narrowing. Likewise `同樣類型`/`同一類` in both corrections adds an unstated result comparison; it does not introduce a deterministic target and is not needed to establish the finding.
- Code-5 translates profile as `派送設定檔`, although the request defines a selector role and does not establish file representation. This is avoidably specific terminology, but may be ordinary translation rather than a concrete file design promise; it is not independently elevated to an important mechanism finding. The explicit representation disclaimers in both detailed repairs are correctly credited.
- All ready confirmations (capture-5, code-5, code-6, capture-7, capture-h1, code-h2, plus provisional code-8) now explicitly put **both** non-forced branch upload and review-ready PR after review and publication checks, with opt-out until publication and separate merge. Capture-4/code-4 are missing-date interviews, and capture-6 remains an interview asking missing facts; lack of a full grant there is not a failure. Capture-6's future `是否上傳` wording does not by itself establish a changed automatic default in an actual ready confirmation.
- Verdict partly: earlier mechanism and authorization issues improve, but the scope contradiction remains material to understanding what is being requested.

### 2. Flexible expression — works

- Read both owners and the new primary template. The outline explicitly permits merging, reordering, expanding, optional headings and free length. Actual outputs vary between prose, bullet lists, numbered items and capture-6's table. No mandatory fill-in sentence or required set of displayed headings appears.
- Clean-copy focused tests: 65 passed, including both owners' fidelity and flexible-composition checks. They supplement actual examples, not replace semantic assessment.
- The full suite belongs to the automated test suite, which runs before the change is accepted and blocks it on failure: `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`. This witness did not run it. The station reports Build exit 0 at `/tmp/context-outline-i5-suite.log`; no claim of witness-run full tests is made. Finalization is not user-skipped, but is ineligible with the important findings below; the old attestation remains stale and no successful renewal is promised.

### 3. Proportionate length and sufficient concept explanation — partly

- Both detailed repairs now explain the assistant's `profile` shorthand using the supplied selection-rule role, without pretending to have verified an application object. Asking for a concrete observed example or missing impact does not itself fail acceptance; capture-6 is a pending interview, not an ignored confirmation. Dates remain unknown instead of being invented. The supplied retry and currency concepts are understandable in context.
- **Important continuing brevity defect:** capture-5 repeats outcome information in Problem, desired result, four acceptance lines and out-of-scope. It additionally lists `engineering`, `needs-design: no`, next station, absence of irreversible choices, counts of acceptance/constraint fields and `none` open questions. These add internal schema/work inventory rather than decision context. Capture-7 likewise includes type/design routing and `這是單純的錯誤修正,沒有增加機制,所以沒有跑複雜度檢查。`
- Capture-h1 repeats unchanged format and untouched old files under acceptance, fixed constraints and exclusions, then adds `這是修 bug，所以我沒有跑複雜度檢查。`, `跨模型審查：預設是 suggest，這裡不問你。`, and a list of frequencies/workarounds/customer counts it did not infer. The concrete consequence that old incorrect exports remain incorrect is useful and is **not** counted as excess; skipped-check/default-setting narration is not useful for choosing currency-setting ownership.
- The simple known command correction code-h2 adds `未決問題：無`, a branch/commit announcement, `接著我會寫出實作計畫,再交給 build 階段。計畫只有一項任務,就是改那一行。`, then appends draft path and uncommitted/no-branch inventory **after the confirmation question**. Its facts and consent paragraph are correct, but these additions do not help decide the one-line correction. The new template expressly requires removing private progress/status/paths/check logs/commits/handoff inventory and ending at the question; the actual known-fact sample has not achieved that result.
- Code-4 also narrates future draft fields and private no-file/no-commit state around a legitimate missing-date question. Not every long response or heading is a failure, and the detailed request is allowed more space. No arbitrary word limit is used; necessary authorization disclosure and relevant consequences are retained. The issue is unnecessary repetition and internal work inventory across both owners.
- Verdict partly: concept repair and unknown-fact handling work in these samples, but simple-case brevity and whole-message relevance remain inconsistent. Close with observed concise known-fact confirmations and relevant detailed explanations, rather than further source assertions alone.

### 4. Requirements and necessary authority only — works

- All ten actual requested answers concern facts needed to understand the issue, whether the intended result/scope is right, or necessary publication authority. None asks the user to judge implementation design, specification quality or a review verdict.
- Capture-6 asks examples/affected people/workarounds/preservation boundaries while staying unconfirmed; these may be more questions than useful, but are outcome/fact questions, not implementation approval. The scope contradiction is recorded under row 1, not converted into a false reviewer-quality demand.
- No unqualified ban on private functions or request to choose a new default worker policy recurs. Code-h2's implementation-stage narration is a row-3 relevance defect, not an implementation decision placed on the user. Verdict works for this sampled criterion.

### Final iteration disposition

- Acceptance: **1 partly, 2 works, 3 partly, 4 works**. All re-tested; no carried-over row.
- Important unresolved findings: capture-6's conflict between each-job coverage and currently-affected-only scope; repeated scope/internal workflow inventory across capture-5/capture-7/capture-h1/code-h2. No important finding is dismissed because tests pass, execution exits zero, or the iteration allowance is exhausted.
- Five additional iterations are used. This witness performs no sixth repair, model call, commit or publication. The station must stop with honest incomplete acceptance; current old attestation is stale and will not be renewed as passing on this evidence.
- No global dogfood pass, ordinary installation/automatic-trigger proof, live-hook proof, human comprehension result, causal superiority, or future-reliability claim. Only the report/evidence changed; prior failed history is preserved.

### Metadata clarification — omitted shared prompt context, no new iteration

Independently read `loom-workflow/hooks/hooks.json`, `loom-workflow/hooks/visualization-card`, `loom-workflow/skills/loom-visualization/assets/trigger-card.md`, and `/tmp/loom-context-claude-dogfood-retest/settings-run.json`. The manifest registers `UserPromptSubmit` to call `hooks/visualization-card`; that script normally reads a static card and injects it as additional prompt context. The full card supplies shared plain-language and visualization guidance: conclusion and user impact first, explain function before internal names, literal actors/actions, and context-sensitive tables/diagrams. The script can select a coexistence card when the ASCII toolkit is active; normal integrated behavior depends on the runtime installation and settings.

The test settings explicitly have `disableAllHooks: true`, with global instruction exclusion via `claudeMdExcludes: ["/Users/kouko/**"]`; runners use `--setting-sources ''` and this settings file. All five additional-iteration batches, 50 samples, therefore lacked the normal UserPromptSubmit shared card. This specific omission was overlooked when interpreting verbosity. These are isolated candidate-skill tests without that shared prompt context, not a measurement of normal integrated hook behavior. This limits transfer of the observed prose/style findings to the complete installed environment; it does not erase actual isolated scope/style failures or show that enabling the card would repair them. No hook-enabled comparison was run, and the user limit precludes another probe or sixth source iteration. Verdicts remain 1 partly, 2 works, 3 partly, 4 works.

Report row 2 now cites only this witness's 65 passing focused checks and observed formatting flexibility. Build's complete locked package-suite pass is station-provided evidence at `/tmp/context-outline-i5-suite.log`, not a witness full-suite run. Finalization is held and was not run for this candidate; no fresh attestation, future successful final review or future package result is claimed. This clarification changes report provenance only, without source/test edits, new model calls, commits or publication.
