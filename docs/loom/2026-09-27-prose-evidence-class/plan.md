# Prose changes stop producing mandatory executable tests — plan
intent: 2026-09-27-prose-evidence-class@fdacfd51
charter: 1.1

## Current State Evidence
- Forward: `loom-code/skills/closing-review/references/lenses.md:54` tests dimension admits only RED→GREEN executable evidence; no prose evidence class exists.
- Reverse: `loom-code/scripts/loom_checker/rules.py:52-55` and `loom-code/skills/write-plan/SKILL.md:357-361` require a positive+negative pair per task, no docs/release exemption.
- Error: `loom-code/tests/test_write_plan_station_text.py:467-481` hardcodes 3.21.0 while `loom-workflow/tests/scripts/test_release_metadata.py:14` hardcodes 5.4.0 — two patterns, both edited per release.
- Data: 166 of 225 test files reference .md paths; all 25 SKILL.md files are pinned; docs/loom work documents carry none (schema rules instead).
- Boundary: `loom-code/scripts/loom_checker/reviewers.py:15-40` already classifies executable vs doc paths (`_REVIEW_PROTECTED_PARTS`, `_is_test_path`, `_LOW_RISK_DOC_EXTENSIONS`); reusable, no new classifier.

## Task DAG

### Wave 0 — mechanism text and single version check

**W0-01 intake.test-case-pair: docs/release exemption and change-level pair ownership**  after: —  acceptance: 1, 2
- Files: `loom-code/scripts/loom_checker/rules.py`, `loom-code/scripts/loom_checker/rule_checks/intake.py`, `loom-code/skills/write-plan/SKILL.md`, `loom-code/tests/test_loom_checker_intake.py`
- Test: A1 positive: prose-only-task-plan-passes-intake; negative: protected-task-without-pair-blocked. A2 positive: behaviour-task-pair-required; boundary: mixed-docs-code-task-keeps-pair.
- Risk: Rewrites the pair recompute in intake.py; existing test_loom_checker_intake.py cases preserved, coverage widened with exemption paths. Exemption reuses reviewers.py path sets. agent-decided.

**W0-02 tests lens names the prose evidence class**  after: —  acceptance: 3
- Files: `loom-code/skills/closing-review/references/lenses.md`, `loom-code/tests/test_reviewer_mechanical_evidence.py`, `loom-code/tests/test_test_budget_text.py`
- Test: A3 positive: tests-dimension-names-prose-evidence; negative: behaviour-changes-still-require-executable-evidence.
- Risk: Definition row plus one explicit sentence that lens definition rows are reviewer-executed and checker-unrecomputed. Two existing pin files narrowed then extended same commit. agent-decided.

**W0-03 one release-metadata test replaces hardcoded version pins**  after: —  acceptance: 4
- Files: `loom-code/tests/test_release_metadata.py`, `loom-code/tests/test_write_plan_station_text.py`
- Test: A4 positive: single-test-covers-manifests-changelog-readmes; negative: stale-or-split-version-fails.
- Risk: Removes two hardcoded-version tests (test_write_plan_station_text.py), coverage preserved and widened (readmes join). Keeps a hardcoded CURRENT constant — it is the no-bump enforcer. agent-decided.

### Wave 1 — release

**W1-01 loom-code minor release 3.22.0**  after: W0-01, W0-02, W0-03  acceptance: 4, 5
- Files: `loom-code/plugin.json`, `loom-code/.claude-plugin/plugin.json`, `loom-code/.codex-plugin/plugin.json`, `loom-code/CHANGELOG.md`, `loom-code/README.md`, `loom-code/README.ja.md`, `loom-code/README.zh-TW.md`, `loom-code/tests/test_release_metadata.py`
- Test: A4 positive: metadata-current-at-3.22.0; boundary: no-bump-detected. A5 positive: package-suite-green; boundary: rule-population-still-26.
- Risk: Minor: rule text and station guidance change, no new mechanism. Release edits only the metadata test's CURRENT line. agent-decided.

## Simplicity check
- Reuse reviewers.py path sets for the exemption instead of a new classifier — taken
- Mirror loom-workflow's release-metadata test shape instead of a consistency-only check — taken
- Drop change-level pair aggregation, keep per-task pairs — declined: the user confirmed change-level ownership; intake.py already parses every task, so aggregation is small
- Make the lens carve-out part of the existing tests row, not a new dimension — taken

## Questions asked
① — what — 要解決的是 loom 機制本身帶來的過度測試，不是 repo 存量？ — 對，要解決的是 loom 機制本身帶來的過度測試
① — what — 接受以 RESHAPE＋獨立審查修正後的方向開變更？ — 對
① — consequence — 品質天花板：執行型散文移除字面感應層，改以語意審查＋行為驗收把關；可逆，漏網即收回？ — 對，執行散文 改以語意審查＋行為驗收把關
① — what — 確認重點是「執行型散文換證據類別、說明型維持 0 測試」這個分型？ — 對 重點是「執行型散文換證據類別、說明型維持 0 測試」
① — what — 確認 LLM 成本不變（語意層本來就是既有 reviewer 在做）？ — 期待 LLM 成本不變或降低

## Risks
1. user-decided — evidence class (d) accepted: prose changes lose the literal-sensor layer; revert condition is in the intent's Constraints (2026-09-27).
2. In-flight plans elsewhere keep working: behaviour tasks still need pairs; only exempt-task plans change; no charter gate moves.
3. W0-02's own pins are the last literal pins this mechanism mandates — on itself; noted, not a defect.
