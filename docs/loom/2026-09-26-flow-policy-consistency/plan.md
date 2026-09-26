# Repair flow policy consistency — plan
intent: 2026-09-26-flow-policy-consistency@3aa2e331
charter: 1.1

## Current State Evidence
- Forward: loom-code/scripts/loom_checker/selection.py::effective_selection preserves bound selections over automatic skips.
- Reverse: loom-code/scripts/loom_checker/command_handlers/finalize.py::cmd_finalize_review and attestation.py::validate_attestation unconditionally union automatic skips into bound selections.
- Error: loom-code/scripts/loom_checker/reviewers.py::_REVIEW_PROTECTED_NAMES omits architecture.md; architecture-only changes receive one reviewer and automatic waivers.
- Data: scripts/run_package_tests.py::_holds_tests discovers only test_*.py although AGENTS.md promises both pytest naming patterns.
- Boundary: Existing test_selection_finalize.py fixtures support real Git branches, bound confirmations, finalization and attestation validation without new harnesses.

## Task DAG

### Wave 0 — Restore existing contracts, sequentially

**W0-01 Protect architecture-rule changes**  after: --  acceptance: 1
- Files: loom-code/scripts/loom_checker/reviewers.py, loom-code/tests/test_loom_attestation.py
- Test: A1 positive: architecture-protected; boundary: ordinary-doc-control.
- Risk: agent-decided — extend existing policy cases; old architecture-only attestations may become stale; do not grandfather insufficient evidence or add a new classifier.

**W0-02 Discover both promised pytest filename patterns**  after: W0-01  acceptance: 2
- Files: scripts/run_package_tests.py, tests/test_run_package_tests.py
- Test: A2 positive: suffix-test-executes; boundary: suffix-local-excluded.
- Risk: agent-decided — preserve existing grouping and exclusions; extend existing runner cases, not pytest collection or a separate discovery framework.

**W0-03 Honor bound verification choices throughout finalization**  after: W0-02  acceptance: 3
- Files: loom-code/scripts/loom_checker/attestation.py, loom-code/scripts/loom_checker/command_handlers/finalize.py, loom-code/tests/test_selection_finalize.py, loom-code/skills/closing-review/SKILL.md, loom-code/skills/expert-mode/SKILL.md, loom-code/tests/test_expert_mode_skill.py, loom-code/tests/test_simplified_station_text.py
- Test: A3 positive: bound-kept-adversarial-required; boundary: unbound-auto-skip-and-explicit-skip.
- Risk: agent-decided — preserve claimed-selection CI validation and legacy evidence; prefer existing selection evidence over new state or schema; search every auto_skipped_steps consumer for the same precedence defect.

### Wave 1 — Release and independent verification

**W1-01 Synchronize the release and document compatibility**  after: W0-03  acceptance: 1, 2, 3
- Files: loom-code/plugin.json, loom-code/.claude-plugin/plugin.json, loom-code/.codex-plugin/plugin.json, loom-code/CHANGELOG.md, loom-code/README*.md, README.md, loom-code/tests/test_write_plan_station_text.py
- Test: A1 positive: release-policy-described; boundary: no-universal-publication-block. A2 positive: suite-inventory; boundary: excluded-folders. A3 positive: metadata-synchronized; boundary: no-new-contract-schema.
- Risk: agent-decided — bump loom-code to 3.20.0 because station guidance changes; include CHANGELOG entry and pin test rewrite; no sibling plugin runtime changes.

## Simplicity check
- Keep selection.py read-only; condition the two downstream consumers on existing evidence without a new helper or schema — taken

## Questions asked
- No new question: the user confirmed the previously restated first three fixes with「那就先修前三項吧 修改的時候注意複雜度問題 不過當前 loom 機制內應該已經有複雜度相關的控制機制了？」.

## Risks
1. agent-decided — no publication authorization is inferred; local commits and review only. Existing weak architecture attestations must be re-reviewed to regain valid status; stale status does not universally prohibit publication.
2. agent-decided — remaining audit findings about spec/plan omission, draft applicability and planned versus committed narrowness remain out of scope.
3. agent-decided — no new persisted field, rule id, dependency or test harness; independent plan review may further reduce the change.
