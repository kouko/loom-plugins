# Post-merge delivery guidance — acceptance test evidence

Tried on 2026-11-14, in a clean copy of the project at d67ebb14defe50bc26734ba6297879c6926d67c0.

## Re-run on 2026-11-14, at d67ebb14defe50bc26734ba6297879c6926d67c0

Independently inspected `git diff 4d282d7ab801be9ba95b004afa7eb5873437500d..d67ebb14d`: only plan W4 acceptance linkage, test-pair wording, risk wording and build evidence changed. Combined with the preceding inspected fix range, no runtime source, instructions, tests, README or canonical intent content changed.

Exact clean-copy commands: `git archive d67ebb14d -o /private/tmp/acceptance-post-merge-final.tar`; `mkdir -p /private/tmp/acceptance-post-merge-final`; `tar -xf /private/tmp/acceptance-post-merge-final.tar -C /private/tmp/acceptance-post-merge-final`. Read README setup at lines 258–287. From that copy, executed `bash loom-code/hooks/session-start </dev/null > /private/tmp/acceptance-post-merge-final-startup.json`, exit 0, and decoded `hookSpecificOutput.additionalContext`. It again emitted full-result same-change completion, preservation of verification/cleanup failures, surviving-repository recovery and rejection of prior-change success. No installed plugin changes.

Repeated canonical byte comparison via `git show aa0f50acf:docs/loom/intent/2026-11-14-post-merge-delivery-guidance.md` and `git show d67ebb14d:docs/loom/intent/2026-11-14-post-merge-delivery-guidance.md`, removing entire status/pin lines as recorded in the preceding run. Output: `canonical bytes equal: True`; `git hash-object --stdin` gives `56acccd13debac07366685edc4ee850e40bbde61`, equal to the repaired pin. This verifies original requirements and publication authorization, not a new user confirmation.

- 1: carried over — emitted context and Ship unchanged across both fix ranges; earlier full-success scenario remains applicable. Setup emission repeated successfully.
- 2: re-tested — ran `git init -b main /private/tmp/acceptance-post-merge-final`, then clean-source `loom-code/scripts/loom-python --repair delivery --json`. Exit 1; `state: unconfirmed`, `reason: cannot identify a committed change`, `complete: false`. Actual next text: `For an active change, use its <type>/<change-id> feature branch and committed confirmed intent. After land removes that identity, report the same change's full land execution result, including exit status, verification and cleanup outcomes. Preserve failures and pending work; a merge line or next-directory hint alone cannot establish completion. If cleanup is partial, use the existing land --cleanup recovery from a surviving repository. Without that evidence, delivery remains unconfirmed.` Both requested scopes observed in full.
- 3: carried over — confirmed canonical content/authorization equal; delivery, Stop, publication and merge implementations/tests untouched. Prior `44 passed in 107.97s` is specifically the first run at 7de6f54, not a fresh test result. Mandatory full suite remains for finalization. The new actual diagnostic also preserves absent-evidence failure.
- 4: carried over — no failure/recovery runtime prose changed; original two synthetic failure exercises retain coverage of all named surfaces.
- 5: carried over — same-change restriction and Acceptance unchanged; prior independent rejection of unrelated success remains applicable.

No new tests were started, no full suite claimed, no live GitHub actions or installed-plugin edits. No findings; no important dismissed findings supplied. Historical 4d and first-run evidence follows unchanged.

## Re-run on 2026-11-14, at 4d282d7ab801be9ba95b004afa7eb5873437500d

Earlier sections below preserve the first run at 7de6f54ef6eb7a983d564403c49a151e1ebcd78a, including its test result and synthetic actor decisions; none is claimed as a new test execution. Independently inspected `git diff e51626a7d38fab2195c4021401989a08ccfaa3d4..4d282d7ab801be9ba95b004afa7eb5873437500d`: only the intent confirmation pin, plan reference/W4 bookkeeping and build evidence changed. No runtime instruction, CLI source, authorization logic, tests, README or Acceptance text changed.

Created another clean archive with `git archive 4d282d7ab801be9ba95b004afa7eb5873437500d -o /private/tmp/acceptance-post-merge-rerun.tar`, `mkdir -p /private/tmp/acceptance-post-merge-rerun`, `tar -xf /private/tmp/acceptance-post-merge-rerun.tar -C /private/tmp/acceptance-post-merge-rerun`. Re-read this copy's README setup and executed `bash loom-code/hooks/session-start </dev/null > /private/tmp/acceptance-post-merge-rerun-startup.json` (exit 0), then decoded its actual additionalContext: the full same-change completion, verification/cleanup failures, surviving-repository recovery and unrelated-success exclusions were emitted. As before, tested source loading without modifying installed plugins.

Independently read original `aa0f50acf` and new target intent bytes using `git show`, removed entire `status:` and `intent_confirmed_sha:` lines with `re.sub(rb"^(?:status|intent_confirmed_sha):.*\n?",b"",raw,flags=re.M)`, compared canonical bytes and computed `git hash-object --stdin`. Output: `canonical bytes equal: True`; blob `56acccd13debac07366685edc4ee850e40bbde61`; new pin `56acccd13debac07366685edc4ee850e40bbde61`. Requirements and publication authorization are byte-identical; no new confirmation is implied or requested.

- 1: carried over — no change to either emitted instruction or Ship; the prior independent full-success exercise remains applicable. Setup emission was repeated, not a new semantic exercise.
- 2: re-tested — after `git init -b main /private/tmp/acceptance-post-merge-rerun`, ran this new copy's `loom-code/scripts/loom-python --repair delivery --json`. Exit 1, state `unconfirmed`, reason `cannot identify a committed change`, complete false. Actual next text again conditions feature-branch/confirmed-intent advice on active work, then allows the same change's full land result after identity removal, rejects a merge line/directory hint alone, and offers surviving-repository cleanup recovery. Both scope and post-land evidence guidance were observed in full.
- 3: carried over — canonical confirmation bytes and authorization are independently verified unchanged; delivery/Stop/publication/merge implementation and focused tests are untouched. Prior 44-test result at 7de6f54 is retained, not rerun; actual missing-evidence diagnostic was additionally observed during setup. The full suite remains the finalizer's responsibility.
- 4: carried over — no runtime or recovery prose changed; both earlier verification-failure and partial-cleanup scenario decisions retain their full surface coverage.
- 5: carried over — no same-change exclusion or Acceptance text changed; prior unrelated-success exercise remains applicable.

No important dismissed findings were supplied. No new findings. No full suite, live GitHub action or installation performed.

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
