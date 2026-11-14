# Post-merge delivery guidance — acceptance test evidence

Tried on 2026-11-14, in a clean copy of the project at 7de6f54ef6eb7a983d564403c49a151e1ebcd78a.

## Environment and provenance

Independent acceptance executor; did not implement the change. Fresh source was extracted with these exact commands, before any execution:

```sh
git archive 7de6f54ef6eb7a983d564403c49a151e1ebcd78a -o /private/tmp/acceptance-post-merge.tar
mkdir -p /private/tmp/acceptance-post-merge-clean
tar -xf /private/tmp/acceptance-post-merge.tar -C /private/tmp/acceptance-post-merge-clean
```

The archive command ran in `/private/tmp/loom-post-merge-delivery-guidance`; subsequent commands ran in `/private/tmp/acceptance-post-merge-clean`. Read the clean README setup/discovery instructions. Host marketplace installation was deliberately not attempted: installed plugin changes are outside the intent. The clean source's actual startup hook and launcher were exercised instead. An archive is not a Git repository; the first delivery invocation returned exit 1, `is not inside a git work tree`. Initialized an empty main fixture with `git init -b main /private/tmp/acceptance-post-merge-clean`, preserving all extracted source, and repeated the diagnostic. This fixture is intentionally unidentified, not a simulated real merged PR.

## 1. 完成前的通用指示與 Ship 規約一致，本次變更已確認合併並完成清理時，可依同一次 land 執行的完整結果回報，不被要求再次執行依賴已清理分支的交付檢查。

Executed `bash loom-code/hooks/session-start </dev/null > /private/tmp/acceptance-post-merge-startup.json` (exit 0); decoded `hookSpecificOutput.additionalContext` with Python. Actual emitted text says `After land has confirmed merge and completed cleanup for the same change being reported, use that execution's full result, including exit status, verification and cleanup outcomes, without rerunning a branch-dependent delivery check.` Read clean Ship Handoff as the companion action instructions.

Cold exercise `test_completion_same_change_success_uses_full_result`: input to this independent executor was the emitted context plus Ship, current change A, synthetic land result exit 0 / merge A confirmed / verification valid / worktree and branch cleanup successful / next surviving directory. Executed decision output: **report A merged and cleanup complete using the full result; follow the surviving directory before any further filesystem command; do not run delivery on the deleted branch**. No GitHub action was issued. This is an actor's bounded instruction-following exercise, not live merger or host enforcement.

## 2. 無法辨認變更時，交付診斷說明其適用範圍與合併後可使用的證據，不將重新命名分支或提交意圖當作所有情況的必要處置。

Actual command `loom-code/scripts/loom-python --repair delivery --json`, against the clean source and initialized main fixture, returned exit 1:

```json
{"state":"unconfirmed","reason":"cannot identify a committed change","next":"For an active change, use its <type>/<change-id> feature branch and committed confirmed intent. After land removes that identity, report the same change's full land execution result, including exit status, verification and cleanup outcomes. Preserve failures and pending work; a merge line or next-directory hint alone cannot establish completion. If cleanup is partial, use the existing land --cleanup recovery from a surviving repository. Without that evidence, delivery remains unconfirmed.","evidence":{},"complete":false}
```

The actual response additionally duplicates `next` as `suggested_next` and prints a help hint. No installed 3.79 command was called: the executable path resolves inside the clean source. Its interpreter cache is shared, not a new host installation. Conditional active-change advice is retained, with a separate post-land route rather than mandatory branch renaming.

## 3. 缺少交付證據仍回報未確認；既有修改分支的交付檢查、自動結束檢查、發布與合併授權行為維持不變。

Actual absent-identity diagnostic above remains unconfirmed / complete false / exit 1. Focused tests command:

```sh
uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest -q -p no:cacheprovider loom-code/tests/test_delivery.py loom-code/tests/test_delivery_stop.py
```

The first sandbox attempt failed before tests because uv could not acquire its cache lock (`Operation not permitted`). Retried the exact command with approved cache access. Exit 0; captured final output: `44 passed in 107.97s (0:01:47)`. Named coverage includes matching remote PR, newer local HEAD, local-only without network, missing authorization, missing PR without grant, required-check failure, unavailable remote, premature/repeated Stop, pause metadata, human boundaries, unready verification, and changed HEAD. These exercise fixture-backed current-source behavior, not live external host termination. The full automated suite is left to finalization, which runs before acceptance and blocks it on failure.

Cold exercise `test_completion_research_only_no_delivery_required`: input current task is research-only, no software change, no land output. Chosen action: deliver research findings directly; no software completion command, publication or merge. The emitted entry exclusions explicitly support this boundary.

Cold exercise `test_completion_absent_land_evidence_stays_unconfirmed`: input current software change A, lost branch, no land execution evidence. Chosen action: report delivery unconfirmed, explain absent full result; do not invent merge success or initiate publication/merge. Actual CLI output independently demonstrates the matching absent-evidence state.

## 4. 合併後驗證失敗或僅完成部分清理時，回報保留其失敗與待處理事項，不以單行合併訊息或目錄指示宣稱全部完成；已失去原工作目錄或分支時，仍提供適用的既有恢復指引。

Cold exercise `test_completion_merge_then_verify_failure_preserves_block`: input current A, synthetic `Merged PR #41`, then verification BLOCK, exit 1, cleanup not established. Chosen output/action: report merged but verification failed and cleanup unconfirmed; resolve the named verification failure and then recover using `land --cleanup fix/A`; do not rerun accepted-by or report all done.

Cold exercise `test_completion_partial_cleanup_branch_failure_recovers_surviving_repo`: input current A, synthetic merge confirmed / verification valid / original worktree removed / local branch deletion failure / `next: cd /surviving/repo` / exit 1. Chosen output/action: retain branch deletion failure and pending cleanup; go to the surviving repository and use existing `land --cleanup fix/A`; do not treat next-directory hint as completion and do not depend on the removed worktree. No recovery mutation was run. Both exercises used the actual emitted completion paragraph and clean Ship's Land/Handoff recovery instructions; synthetic results are not represented as actual CLI output.

## 5. 收尾例外僅適用於本次回報的同一變更，先前變更的成功結果不能代替新工作的交付證據。

Cold exercise `test_completion_prior_success_current_work_unconfirmed`: input prior A has exit-0 full land success, current B has unfinished edits and no delivery observation. Chosen action: do not reuse A's result; B remains unfinished/unconfirmed; continue B's applicable workflow and observe its delivery while identifiable before claiming completion. No publication or merge authorization inferred. Captured instruction says `Earlier success for another change supplies no evidence for current work; absent evidence remains unconfirmed.` This independently selected action rejects the adversarial success substitution.

## Scope limits

Six synthetic scenario decisions were performed by this fresh acceptance executor after loading the actual emitted context and Ship. They are behavioral evidence of this executor applying instructions, not a repeated source inspection assertion and not a benchmark across other models. No live GitHub writes, merge, cleanup, installation, installed hook reload, full package suite, or live OpenCode/Antigravity enforcement was performed. The change itself retains that enforcement limitation.
