# Planning intake observation pilot — plan
intent: 2026-11-11-intake-observation-pilot@241362a4
spec: docs/loom/2026-11-11-intake-observation-pilot/spec.md@a6af7bc1
charter: 1.1

## Task DAG

### Wave 1 — Existing intake entry
**W1-01 Structured intake observation and station consumption** after: none acceptance: 1, 2
- Files: `loom-code/scripts/loom_checker/command_handlers/intake.py` (entry: cmd_intake), `loom-code/scripts/loom_checker.py`, `loom-code/tests/test_loom_checker_intake.py`, `loom-code/skills/write-plan/SKILL.md`
- Test: A1 positive: intake_json_equivalent; boundary: intake_json_unavailable. A2 positive: intake_json_readonly; boundary: intake_json_earlyexit. Run the existing intake test module and write-plan station tests.
- Risk: agent-decided — REQ-1/2 Design decision; preserve all existing cases in `loom-code/tests/test_loom_checker_intake.py`, widen output coverage only. Scope completeness to applicable intake checks, never workflow readiness.

### Wave 2 — Reproducible comparison and research
**W2-01 Prepare matched observation cases and evidence** after: W1-01 acceptance: 3, 4
- Files: `docs/loom/2026-11-11-intake-observation-pilot/evidence/comparison.md`, `docs/loom/research/2026-11-11-mechanical-decision-input-evidence.md`, `docs/loom/research/2026-11-11-recursive-decision-models-for-loom.md`
- Test: A3 positive: comparison_matched_outputs; boundary: comparison_no_savings_claim. A4 positive: input_cases_reproduced; boundary: input_assertions_not_truth. Execute the retained comparison recipe and inspect source anchors.
- Risk: agent-decided — REQ-3/4 Design decision; keep ground truth separate from agent packets. Independent acceptance testing consumes the cases; synthetic input perturbations never establish task-classification accuracy.

### Wave 3 — Release packet
**W3-01 Synchronize minor release metadata** after: W2-01 acceptance: 1, 2, 3, 4
- Files: `loom-code/.claude-plugin/plugin.json`, `loom-code/.codex-plugin/plugin.json`, `loom-code/plugin.json`, `loom-code/package.json`, `loom-code/CHANGELOG.md`, `loom-code/README*.md`, `README*.md`, `loom-code/tests/test_write_plan_station_text.py`
- Test: A1 positive: release_sync; boundary: release_stale_pin. A2 positive: release_sync; boundary: release_stale_pin. A3 positive: release_sync; boundary: release_stale_pin. A4 positive: release_sync; boundary: release_stale_pin. Run release metadata checks and manifest sync verification.
- Risk: agent-decided — REQ-1 Design decision changes station guidance; bump 3.66.0, add CHANGELOG entry, rewrite version pin, derive mirrors with `scripts/sync_codex_manifests.py --all`; preserve station-text tests except assertions intentionally changed by W1-01.

### Wave 4 — Adversarial invocation repair
**W4-01 Reject repeated JSON options before positional interpretation** after: W3-01 acceptance: 1, 2
- Files: `loom-code/scripts/loom_checker/command_handlers/intake.py` (entry: cmd_intake), `loom-code/tests/test_loom_checker_intake.py`, `docs/loom/2026-11-11-intake-observation-pilot/evidence/probes/test_intake_repeated_json.py` → `loom-code/tests/test_intake_repeated_json.py` (unchanged probe graduation)
- Test: A1 positive: intake_json_equivalent; boundary: intake_json_unavailable and intake_repeatedflags_unconfirmed. A2 positive: intake_json_readonly; boundary: intake_json_earlyexit. Run intake, station-text and graduated probe modules; retain the existing adversarial RED before implementation.
- Risk: agent-decided — Duplicate options must remain invocation errors even without an id, across both stations and option positions. Preserve ordinary parsing, observation-only scope and version 3.66.0; move the adversarial probe byte-for-byte without duplication.

## Simplicity check
- Keep the reproducible collection recipe in evidence prose instead of committing an executable experiment harness — taken

## Questions asked
① — what — 確認以這個範圍進行嗎？

## Risks
1. agent-decided — Keep observation failure distinct from a valid blocker. Confirmation early-exit must not imply later checks ran; no new policy rules or mechanism count increase.
2. agent-decided — The experiment may demonstrate format reliability without speed or token savings. Retain guidance-only as a candidate and disclose unmeasured host behavior.
3. agent-decided — Prior input research is source-local. Recheck claims independently; no private sessions, hosted classifier, dispatch-policy change or assumed user consent.
4. user-decided — Automatic non-forced branch publication and Ready PR authorized at decision point ①; merge remains separate. No second-vendor review selected.
