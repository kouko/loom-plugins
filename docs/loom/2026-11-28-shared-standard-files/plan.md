# Writer and judge read one standard — plan
intent: 2026-11-28-shared-standard-files@93f7ee80c
charter: 1.1

## Current State Evidence
- Forward: `loom-code/agents/implementer.md:30` sends the writer to `loom-code/references/engineering-baseline.md`; `loom-code/agents/reviewer.md:47` sends the judge to `closing-review/references/lenses.md`.
- Reverse: lenses `tests` row (`lenses.md:58`) already cites baseline §5 item 8 via `../../../references/engineering-baseline.md`, the path form new standards reuse.
- Error: baseline §5 item 2 forbids "abstraction for a single use"; lenses `deletion-first` (`lenses.md:65`) also accepts an explicit request or visible motivation.
- Data: judge-only test rules (cannot-fail tests, mock replacing the covered seam, internal-function tests) live in `lenses.md:58`; baseline §5 item 6 has only a one-line version.
- Boundary: 14 tests under `loom-code/tests/` read lenses or baseline text (e.g. `test_lenses_deletion_first.py`, `test_prose_pin_rule_text.py`, `test_test_budget_text.py`).

## Task DAG

### Wave 1

**W1-01 Tests standard**  after: none  acceptance: 1, 2, 4, 6, 9
- Files: loom-code/references/tests-standard.md, loom-code/references/engineering-baseline.md, loom-code/skills/closing-review/references/lenses.md, loom-code/tests/test_tests_standard_text.py, loom-code/tests/test_prose_pin_rule_text.py
- Test: A1 positive: tests-standard-exists; negative: lens-row-restates-rule. A2 positive: rule-once-in-standard; negative: rule-copied-in-baseline. A4 positive: tautology-ban-affirmative; negative: tautology-ban-negated. A6 positive: impl-coupled-ban-affirmative; negative: impl-coupled-ban-negated. A9 positive: moved-rules-present; boundary: red-green-refactor-unchanged.
- Risk: move writer-relevant rules out of lens `tests` row and baseline §5 items 6, 8; reviewer mechanics stay in lenses; repoint `test_prose_pin_rule_text.py`; agent-decided.

**W1-02 Code-design standard**  after: W1-01  acceptance: 1, 2, 3, 5, 7, 8, 9
- Files: loom-code/references/code-design-standard.md, loom-code/references/engineering-baseline.md, loom-code/skills/closing-review/references/lenses.md, loom-code/skills/write-plan/SKILL.md, loom-code/tests/test_code_design_standard_text.py, loom-code/tests/test_lenses_deletion_first.py
- Test: A3 positive: one-abstraction-threshold; negative: single-use-ban-remains. A5 positive: shallow-and-deletion-test-present; negative: shallow-negated. A7 positive: testability-present; negative: testability-negated. A8 positive: task-size-cites-standard; negative: task-size-no-pointer. A1 positive: file-exists; negative: missing. A2 positive: refactoring-rule-once; negative: duplicated. A9 positive: forward-only-finding-kept; boundary: barrel-exemption-kept.
- Risk: lenses `deletion-first` threshold wins (user-confirmed restatement); naming/refactoring/deletion-first/deliberate-simplification rules move; `architecture` keeps SOLID citation; agent-decided.

**W1-03 Docs and skill-text standard**  after: W1-02  acceptance: 1, 2, 9
- Files: loom-code/references/docs-standard.md, loom-code/references/engineering-baseline.md, loom-code/skills/closing-review/references/lenses.md, loom-code/tests/test_docs_standard_text.py, loom-code/tests/test_lenses_deletion_first.py
- Test: A1 positive: docs-standard-exists; negative: missing. A2 positive: polarity-rule-once; negative: polarity-rule-in-lenses. A9 positive: five-dimensions-and-polarity-kept; boundary: reviewer-dimension-names-unchanged.
- Risk: the `charter.plan-omission-narrow` gate block stays in lenses (registered gate location); docs dimension names unchanged in lenses so reviewer scoring keys hold; agent-decided.

### Wave 2

**W2-01 Release metadata for loom-code 3.91.0**  after: W1-03  acceptance: 10
- Files: loom-code/.claude-plugin/plugin.json, loom-code/CHANGELOG.md, loom-code/README.md, loom-code/README.ja.md, loom-code/README.zh-TW.md, README.md, loom-code/tests/test_write_plan_station_text.py
- Test: A10 positive: release_sync; boundary: release_stale_pin. Existing pin `test_current_release_metadata_is_synchronized` covers it.
- Risk: minor bump (station guidance and contract text change) via SSOT then `sync_codex_manifests.py --all`, derived manifests committed; agent-decided.

## Simplicity check
- Drop the reader-wiring task and its single-source guard test; baseline and lenses already reach the writer and judge, and each W1 task tests A2 — taken

## Questions asked
① — consequence — Shared standards: one file / two files (tests, code design) / three files (+ docs/skill text) / standalone skill? (user chose three files: 「但是我想改成 B 方案三份都抽出來」)
① — what — Add the two missed mattpocock rules (implementation-coupled tests, testability design)? (user: 「選 A，補上漏掉的兩項 但是把 C 加入之前的文件備註」)
① — consequence — Confirm the restated intent and authorize automatic non-forced push + Ready PR after closing-review; merge separate. (user: 「是」)

## Risks
1. Intent Problem says the judge asks only for RED→GREEN evidence; `lenses.md:58` already bans cannot-fail tests and internal-function tests. Acceptance is unaffected; the writer still lacks them.
2. Moving review-gate prose can flip polarity; the adversary runs polarity near-miss probes against every moved sentence before hand-off.
3. user-decided — automatic publication after closing-review; merge stays a separate decision.
