# Context-preserving intent confirmation — acceptance test evidence

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
