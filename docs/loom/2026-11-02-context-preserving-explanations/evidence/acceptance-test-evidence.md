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
