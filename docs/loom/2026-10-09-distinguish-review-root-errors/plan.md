# Distinguish review-root errors — plan
intent: 2026-10-09-distinguish-review-root-errors@6a672ac
charter: 1.1

## Current State Evidence
- Forward: `loom-code/scripts/external_review.py:332` starts the selected CLI with the review root as its working directory.
- Reverse: `loom-code/tests/test_external_review.py:182` checks missing CLI errors at discovery and execution entry points.
- Error: `loom-code/scripts/external_review.py:186` and `:368` classify every `FileNotFoundError` as a missing executor.
- Data: `loom-code/scripts/external_review.py:168` and `:306` verify that the review root is absolute, not that it exists.
- Boundary: `loom-code/scripts/external_review.py:297` strips probe output before reporting failed execution.

## Task DAG

**W0-01 Distinguish missing working directory from missing executable**  acceptance: 1, 2, 3
- Files: `loom-code/scripts/external_review.py` (entry: `discover`, `execute`), `loom-code/tests/test_external_review.py`
- Test: A1 positive: missing-root-error; negative: failed-no-verdict. A2 positive: missing-executor-error; boundary: valid-root-missing-executable. A3 positive: no-raw-path-or-exception; boundary: existing-success.
- Risk: agent-decided — compare exception filename with the selected root without returning it; retain existing error categories for other failures and existing test coverage.

## Simplicity check
- none found

## Questions asked
1 — what — Loom 的 closing-review 限制同一修正最多三輪；最後一輪確認「目錄不存在」仍被誤報為「CLI 未安裝」，因此需用新的已確認意圖繼續。新意圖只修正這兩種原因的區分、保留隱私與失敗狀態，且只留本機。這是你要的嗎？（使用者回答：「請繼續」）

## Risks
1. A selected root can disappear while the CLI starts; the exception must remain distinguishable from a missing executable without exposing either path.
2. User authorized local work only; no push or PR is part of this change.
