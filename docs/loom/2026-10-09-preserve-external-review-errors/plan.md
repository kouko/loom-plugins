# Preserve external review failure reasons — plan
intent: 2026-10-09-preserve-external-review-errors@c8a7c240214e46712a74877626e365686dd2b823
charter: 1.1

## Current State Evidence
- Forward: `loom-code/scripts/external_review.py:284` runs the probe and review with one explicit profile.
- Reverse: `loom-code/tests/test_external_review.py:179` checks Claude success output and observed model.
- Error: `loom-code/scripts/external_review.py:295` uses only stderr on nonzero exit, hiding Claude JSON errors on stdout.
- Data: `loom-code/scripts/external_review.py:198` already parses Claude JSON for successful execution.
- Boundary: `loom-code/scripts/external_review.py:254` initializes failed status and empty review output before execution.

## Task DAG

**W0-01 Preserve bounded execution failure reasons**  acceptance: 1, 2, 3
- Files: `loom-code/scripts/external_review.py` (entry: `execute`), `loom-code/tests/test_external_review.py`
- Test: A1 positive: claude-structured-429; negative: untrusted-stdout. A2 positive: empty-diagnostic; boundary: failed-review-no-verdict. A3 positive: unchanged-success; negative: no-prompt-echo.
- Risk: agent-decided — use CLI-owned JSON error fields and a bounded message; arbitrary stdout can contain review material, so never echo it wholesale.

**W0-02 Retain defect-catching probes in the package suite**  acceptance: 1, 3
- Files: `loom-code/tests/test_external_review.py`, `docs/loom/2026-10-09-preserve-external-review-errors/evidence/probes/test_external_failure_probe_output_privacy.py`, `docs/loom/2026-10-09-preserve-external-review-errors/evidence/probes/test_external_failure_terminal_envelope.py`
- Test: both adversarial cases remain green in the package suite after relocation; the original probe paths are removed.
- Risk: agent-decided — relocate only the two cases that caught actual defects; preserve their assertions and synthetic data.

**W0-03 Classify every external CLI failure without exposing its text**  acceptance: 1, 2, 3
- Files: `loom-code/scripts/external_review.py`, `loom-code/tests/test_external_review.py`, `docs/loom/2026-10-09-preserve-external-review-errors/evidence/claude-failure-envelope.json`
- Test: Claude readable stderr with empty stdout identifies a bounded category; Codex and Agy echoed secrets remain absent from result; the observed Claude API error envelope is documented and covered; unknown diagnostics stay unknown.
- Risk: agent-decided — CLI stderr and JSON result text are untrusted and may echo review material; map only verified diagnostic shapes to fixed categories.

## Simplicity check
- none found

## Questions asked
1 — what — 修正目標是否正確：外部審查失敗時顯示可判讀原因；原因缺失時明確標示未知且不算審查完成；成功結果照常？修好並驗證後，再於額度恢復時用 Claude Opus + high 審查原分支。Loom 的 capture-intent 規則要求先確認這份目標。這次修正是否先只留在本機？

## Risks
1. The original failed review stdout was discarded, so its exact error cannot be reconstructed from the retained result.
2. The user authorized local work only; no push or PR is part of this change.
