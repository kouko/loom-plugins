# External review authorization — acceptance test evidence

Tried on 2026-10-10 in a clean local clone at `d43a2bfd` (`/private/tmp/loom-external-review-acceptance-clean`). The clone was clean before testing. No real outside coding-agent CLI was invoked, and no repository code or review packet was sent out.

## Setup and method

- Source checkout: `git clone --local --no-hardlinks --no-checkout /private/tmp/loom-external-review-consent /private/tmp/loom-external-review-acceptance-clean`; then `git -C /private/tmp/loom-external-review-acceptance-clean checkout d43a2bfdbbb5bf34542f23774e4dbcd5ec1a81b6`.
- README setup offers network-backed host plugin installation. That was outside this local-only acceptance run. `python3 loom-code/scripts/external_review.py --help` succeeded in the clean clone and displayed the documented arguments, showing that the local entry point loads. Actual host plugin installation was not verified.
- Executed `python3 /private/tmp/acceptance_probe_external_review.py`. This standalone local probe imported the clean clone's `external_review.py` and supplied an in-process fake runner returning synthetic candidate, probe, and review outputs. The probe did not call `subprocess.run` for a CLI. `fake_calls` counts calls to the fake runner only; it is not an egress measurement.
- Focused tests: `uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest -q loom-code/tests/test_external_review.py loom-code/tests/test_excluded_executor_no_egress.py` returned `119 passed in 0.19s` from the clean clone. The managed sandbox denied write access to the normal uv cache, so this focused command used narrowly scoped host execution. Earlier direct Python and offline attempts failed before test collection because pytest and one locked package, respectively, were unavailable there. The complete package-suite command reserved for `finalize-review` is `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`; it was not run here.

Captured local probe output (each call is to an in-process fake runner):

```text
cancelled: discovery failed; execution failed; fake_calls 0
paused: discovery failed; execution failed; fake_calls 0
switched_from_codex: discovery failed; execution failed; fake_calls 0
reselected_codex: discovery completed; execution completed; fake_calls 4
direct_with_explanation: discovery completed; execution completed; fake_calls 4
accepted_selection: discovery completed; execution completed; fake_calls 4
ambiguous_choice_withheld: discovery failed; execution failed; fake_calls 0
missing_target: discovery failed; execution failed; fake_calls 0
missing_source: discovery failed; execution failed; fake_calls 0
mismatched_executor: discovery failed; execution failed; fake_calls 0
mismatched_scope: discovery failed; execution failed; fake_calls 0
missing_egress_disclosure: discovery failed; execution failed; fake_calls 0
unapproved_effort: discovery completed; execution failed; fake_calls 1
stale_owner_record_after_cancel: discovery completed; execution completed; fake_calls 4
```

## 1. 使用者取消、暫緩或改選外部 coding agent 後，被排除的 agent 不會執行模型查詢、探測或審查。

- How I tried it: Synthesized a direct Codex request followed by cancellation, pause, or selection of Claude. Recorded the final choice as `approved: false` or `selected_executor: claude`, then called both `discover` and `execute` with a fake runner that recorded calls.
- What came back: `cancelled`, `paused`, and `switched_from_codex` each returned `failed / consent-missing-or-stale` for discovery and execution, with `fake_calls: 0`. Therefore none reached the fake discovery, probe, or review stage.
- Counterexample: `stale_owner_record_after_cancel` quoted `Use Codex to review this change. Actually cancel all outside reviews.` while leaving `approved: true` and `selected_executor: codex`. Both discovery and execution returned `completed`, with `fake_calls: 4`. This is a synthetic stale-record failure, not evidence that a real owner model will make that mistake or that any network egress occurred.
- Evidence: local probe output, `loom-code/scripts/external_review.py:43-79`, and the owner/runner division stated at `loom-code/skills/external-review/SKILL.md:70-78`.

## 2. 使用者明確改回或選定某個 coding agent 時，指定 agent 能承接原本的審查任務，不因請求中的早期拒絕或附帶說明而要求重複確認。

- How I tried it: Supplied `Do not use Codex. Actually, please use Codex to review this change.` and `Use Codex to review this change; no need to ask again. Do not use Claude.` with final `selected_executor: codex`, then called discovery and execution through the fake runner.
- What came back: `reselected_codex`, `direct_with_explanation`, and `accepted_selection` each returned `completed` for discovery and execution, with four fake calls: one discovery call plus an execution-stage candidate lookup, probe, and review. No second confirmation hook appeared at this boundary.
- Evidence: local probe output and `loom-code/tests/test_external_review.py:147-193`. This tests the structural boundary with an already-correct owner record, not the accuracy of a live model interpreting the conversation or completing a real outside review.

## 3. 最後選擇或審查範圍不明確，以及授權紀錄缺漏或不一致時，外部動作不會開始；有效授權仍須保留資料傳送告知及模型與 effort 限制。

- How I tried it: Removed the authorization source; mismatched the selected executor; changed the requested review root; removed the vendor-egress disclosure; and requested `max` effort from a record authorizing only `high`. Called both entry points through the fake runner.
- What came back: `ambiguous_choice_withheld`, `missing_target`, `missing_source`, `mismatched_executor`, `mismatched_scope`, and `missing_egress_disclosure` each failed both entry points with zero fake calls. `unapproved_effort` allowed candidate discovery (one fake call) but blocked execution before its candidate lookup, probe, or review. This matches the intended distinction between model discovery and a specific model/effort run.
- Evidence: local probe output and `loom-code/scripts/external_review.py:65-105,169-178,315-326`. Ambiguous conversational choice and scope are assigned to the owning flow at `loom-code/skills/external-review/SKILL.md:64-78`; the fake runner cannot validate a live model's classification.

## Re-run on 2026-10-10, at `6fb29888`

- Clean copy: `git clone --local --no-hardlinks --no-checkout /private/tmp/loom-external-review-consent /private/tmp/loom-external-review-acceptance-rerun`; `git -C /private/tmp/loom-external-review-acceptance-rerun checkout 6fb298885f3fb96e42bdd31416f51b21d4566385`. `git status --short` was empty. `python3 loom-code/scripts/external_review.py --help` loaded the local entry point successfully. Host plugin installation and live-model behavior remained outside this local-only run.
- Fix diff: `git diff 006a5d12..6fb29888` adds a latest-choice recheck immediately before each owner call in the independent-advisor, closing-review, and external-review instructions. It does not change `external_review.py` or add a conversation parser. The plan records the remaining stale-record and in-call timing limits.
- Focused tests: `uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest -q loom-code/tests/test_external_review.py loom-code/tests/test_excluded_executor_no_egress.py loom-workflow/tests/independent-advisor/test_independent_advisor_readmes.py` returned `131 passed in 0.23s`. This used narrowly scoped host execution for the locked uv cache. The complete package suite was not run by the acceptance tester; `finalize-review` will run it.
- Local synthetic command: `python3 /private/tmp/acceptance_probe_external_review.py`, now pointing to the clean `6fb29888` clone. All calls used the in-process fake runner. No real outside coding-agent CLI was invoked and no review packet or repository content was sent out.
- 1: re-tested cancellation, pause, replacement, ambiguous choice, and the previous stale-record counterexample through both discovery and execution. Updated records blocked with zero fake calls; a stale approved record still completed both with four fake calls. Also tried a cancellation between separately invoked discovery and execution: discovery completed with one fake call, then refreshed `approved: false` made execution fail `consent-missing-or-stale` with no further fake calls. The new owner instructions are at `loom-code/skills/external-review/SKILL.md:80-88`, `loom-code/skills/closing-review/SKILL.md:195-202`, and `loom-workflow/skills/independent-advisor/SKILL.md:56-63`. An in-process fake cannot prove the live owner will always refresh the record.
- 2: re-tested explicit re-selection, direct request with side explanation, and accepted selection through discovery and execution. Each completed with four fake calls and no second confirmation boundary. The updated instruction explicitly preserves that path. Real model interpretation and outside review completion were not tried.
- 3: re-tested withheld ambiguous choice, missing target or source, mismatched executor or scope, missing vendor-egress disclosure, and unapproved effort. All except the effort case blocked before any fake call; the effort case allowed one candidate discovery call and blocked before probe or review. The focused tests passed. The owner must still classify live ambiguous language and recheck any later turn; a new turn during one synchronous execution call cannot interrupt that call, and already transmitted material cannot be recalled.

Captured re-run result summary:

```text
cancelled/paused/switched_from_codex/ambiguous_choice_withheld: discovery failed, execution failed, fake_calls 0
reselected_codex/direct_with_explanation/accepted_selection: discovery completed, execution completed, fake_calls 4
missing_target/missing_source/mismatched_executor/mismatched_scope/missing_egress_disclosure: discovery failed, execution failed, fake_calls 0
unapproved_effort: discovery completed, execution failed, fake_calls 1
stale_owner_record_after_cancel: discovery completed, execution completed, fake_calls 4
cancel_between_calls_with_refreshed_record: discovery completed, execution failed, fake_calls 1
```
