# 把儀式規模改成機械計算 — plan
intent: 2026-09-20-mechanical-calculations@9f60b7b0
charter: 1.0

## Current State Evidence
- Forward: `required_reviewer_count()` counts reviewers from committed diff; floor 1 → 1 reviewer.
- Reverse: a protected path, unsafe path, or non-test file in the delta → floor 2 (default).
- Error: a git plumbing failure failing closed counts as a broad delta (floor 2).
- Data: intent file at `docs/loom/intent/2026-09-20-mechanical-calculations.md`, confirmed 2026-09-20.
- Boundary: `selection show` on a narrow delta with no bound selection reports `spec`, `plan`, and `blind-run` as skipped.

## Task DAG

**W1-01 提取 shared committed-branch path source**  acceptance: 3, 8
- Files: loom-code/scripts/loom_checker/reviewers.py, loom-code/scripts/loom_checker/selection.py
- Test: A3 positive: shared committed paths exclude working edits; negative: unreadable diff yields empty set. A8 positive: package suite passes; negative: mechanism count increases.
- Risk: mechanical refactor, low — two call sites now read from one helper, eliminating the dirty-tree disagreement. agent-decided.

**W1-02 啟用 narrow delta 自動跳站**  after: W1-01  acceptance: 1, 2, 3, 5
- Files: loom-code/scripts/loom_checker/selection.py
- Test: A1 positive: narrow intent auto-skips spec/plan/blind-run; negative: broad keeps all. A2 positive: mixed → no auto-skip; negative: pure narrow skips. A3 positive: one frozenset; negative: change needs edit. A5 positive: adversarial retained; negative: never auto-skipped.
- Risk: auto-skip list growing stale if vocabulary changes; `_NARROW_AUTO_SKIP_STEPS` is a single frozenset to update. agent-decided — not authorised to expand scope.

**W1-03 驗證 acceptance 6、7 的實作狀態**  after: W1-02  acceptance: 6, 7
- Files: loom-code/skills/plan/SKILL.md (plan artifact contract), closing-review 盲跑報告
- Test: A6 positive: `selection show` lists `plan` as skipped → write-plan not required; negative: full ritual requires plan artifact. A7 positive: blind-run confirms spec/plan/blind-run omitted; boundary: blind-run runs only at closing review.
- Risk: A7 verified by Build's adversary and package tests; A6 by intent A6 specification. agent-decided.

**W1-04 綁定 acceptance 4 的用戶選擇優先權**  acceptance: 4
- Files: loom-code/scripts/loom_checker/selection.py
- Test: A4 positive: 綁定用戶選擇決定有效步驟; negative: 自動分類不增加也不移除用戶選擇的步驟.
- Risk: acceptance 4 是既有合約，此任務僅確認無迴歸。agent-decided.

## Questions asked
None — intent was already confirmed; no open questions.

## Risks
1. Auto-skip list drifts from vocabulary changes — `_NARROW_AUTO_SKIP_STEPS` is a single frozenset; adding or removing a step requires one edit.
2. A future change to `reviewer_floor_for_paths()` allowlist could silently widen or narrow the auto-skip window — both the floor and auto-skip delegate to it so this is self-anchored.
3. The acceptance A7 (blind-run) cannot be verified until the diff is committed and a blind-run is actually run; it is tracked here but executed at closing review.