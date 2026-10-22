# Claude Code review diagnostics — acceptance test evidence

Tried on 2026-10-22 in a clean local clone at `7c7c2542ffdccc7c8c225f32e42e87ca86726e3f`. The clone was made with `git clone --no-hardlinks --local --no-checkout /private/tmp/loom-claude-review-diagnostics-20261022 /private/tmp/loom-claude-review-acceptance-20261022` and detached at that SHA. `git status --short` was empty. `git worktree add` could not write the source repository's shared `.git/worktrees` directory, so the local clone supplied the clean copy.

Setup followed the root README's isolated `uv` environment. The default `uv` cache was not writable in the sandbox; an empty temporary cache could not fetch `pytest-xdist` because DNS/network access was unavailable. Reusing the existing local cache with `uv run --offline --isolated --with-requirements requirements-package-tests.lock` succeeded. No package was installed into the conda base environment. No actual Claude Code or other outside review service was called; no review-specific consent exists for this trial.

Focused command, run from the clean clone:

```sh
uv run --offline --isolated --with-requirements requirements-package-tests.lock python -m pytest -q loom-code/tests/test_external_review.py loom-code/tests/test_adversarial_claude_error_result.py
```

Output: `133 passed in 17.63s`. This is the focused set, not the complete package suite. The Build station had already run the complete suite; `finalize-review` is scheduled to run it again before attestation.

A second command selected the cases below with `python -m pytest -v` and `-k` over the same two files. Output: `40 passed, 93 deselected in 1.85s`. The selected names were `consent_blocks_all_subprocesses`, `owner_selected_direct_request_remains_valid`, `claude_zero_exit_error_result_never_completes_or_leaks`, `claude_alias_uses_explicit_flags_and_reports_accepted_level`, `claude_structured_api_error_reports_bounded_reason_without_review_material`, `nonzero_untrusted_stdout_does_not_become_failure_reason`, `claude_empty_stdout_classifies_only_known_stderr`, `nonzero_empty_diagnostic_is_explicitly_unknown`, `failed_selection_or_execution_never_falls_back`, `review_step_prints_progress_each_interval`, `json_result_unchanged_with_progress`, `execute_section_relay_safe_claude_failure_and_recovery`, and `execute_section_preserves_failed_review_boundary`.

## 1. 在已授權且 Claude Code 可正常執行的環境中，正式審查能在預檢後完成，並交回可歸屬的審查內容。

- How I tried it: Ran `test_claude_alias_uses_explicit_flags_and_reports_accepted_level` and `test_json_result_unchanged_with_progress` in the focused set. The latter invokes the command-line entry point with a synthetic executable and a public placeholder packet.
- What came back: Both passed. They require two executions, a completed result, the full review text, and observed model `claude-sonnet-4-5`; progress remains on stderr while stdout holds one JSON result. The tests do not contact the real Claude service.
- Evidence: `loom-code/tests/test_external_review.py:491`, `:1119`; selected run output above. Real-service behavior is unverified because this trial has no review-specific consent.

## 2. 正式審查失敗時，使用者或維護者能取得足以區分可辨識故障與未知故障的安全診斷及下一步；原始審查材料不會出現在對外結果中。

- How I tried it: Ran the selected synthetic structured API, stderr, unknown-output, zero-exit structured-error, and documentation relay cases. The tests place a public `SYNTHETIC_PRIVATE_MARKER` or placeholder prompt in fake process output and check that it is absent from the failed result.
- What came back: All selected cases passed. Examples include `probe-exit-1: Claude session limit (HTTP 429)` with a reset action, `review-exit-1: unknown error` with a local `claude doctor` action and five bounded diagnostic fields, and `execution-error: claude result reports error` without review output. Raw stdout/stderr text was not relayed in these cases.
- Evidence: `loom-code/tests/test_external_review.py:301`, `:516`, `:547`, `:574`, `:591`, `:1179`; selected run output above. This does not establish that every future Claude CLI error format will be recognized.

## 3. 沒有完成的 Claude Code 審查不會被記成成功的審查或審查結論；既有授權範圍與其他執行器的行為仍有效。

- How I tried it: Ran the selected authorization, failed-selection, and zero-exit-error cases, plus the graduated adversarial `test_claude_error_rejected` in the 133-case command.
- What came back: All passed. Failed Claude results have `status: failed` and `review_output: null`; a zero-exit structured error stops after the failing stage. Missing consent starts no subprocess. Explicit user choices for Codex, Claude, and Agy remain valid, and failed selections do not fall back to another executor.
- Evidence: `loom-code/tests/test_external_review.py:37`, `:149`, `:301`, `:831`, `:1192`; `loom-code/tests/test_adversarial_claude_error_result.py:18`.

## 4. No authorized request

- How I tried it: Ran `test_consent_blocks_all_subprocesses` across its five records and the owner selection cases.
- What came back: All passed. Missing or stale consent returned `consent-missing-or-stale`, and the fake runner was never called. This tests the execution boundary; the user's subsequent choice is documented rather than exercised in a live conversation.
- Evidence: `loom-code/tests/test_external_review.py:34`, `:149`; selected run output above.

## 5. In progress

- How I tried it: Ran `test_review_step_prints_progress_each_interval`, `test_json_result_unchanged_with_progress`, and related progress cases in the 133-case command.
- What came back: All passed. The synthetic process produced `external-review: review still running · <n>s elapsed` lines and closing lines on stderr. The JSON result stayed on stdout, without packet or review text in progress lines.
- Evidence: `loom-code/tests/test_external_review.py:1068`, `:1119`; selected run output above.

## 6. Success

- How I tried it: Ran the synthetic CLI entry-point case and the Claude alias/profile case.
- What came back: Both passed; the completed result contained `SECRET-REVIEW-TEXT` and observed model `claude-sonnet-4-5` after separate probe and review calls. This is a synthetic fixture, not a real Claude response.
- Evidence: `loom-code/tests/test_external_review.py:491`, `:1119`; selected run output above.

## 7. Recognized failure

- How I tried it: Ran structured API 429/503, known stderr, and zero-exit structured-error cases.
- What came back: All passed. Results exposed fixed categories and next actions, while `review_output` was null and the public private-marker fixture did not appear in the result.
- Evidence: `loom-code/tests/test_external_review.py:301`, `:516`, `:574`; selected run output above.

## 8. Unrecognized failure

- How I tried it: Ran the nonzero untrusted stdout and empty-diagnostic cases, including a fake review-stage failure after a successful probe.
- What came back: Both passed. The review-stage failure reported `review-exit-1: unknown error` with only `stage: review`, numeric exit code, and the three allowed booleans; the action directs local private diagnostics. The empty probe case reported the same bounded shape for `stage: probe`.
- Evidence: `loom-code/tests/test_external_review.py:547`, `:591`; selected run output above.
