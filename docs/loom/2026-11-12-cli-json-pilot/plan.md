# Optional JSON results for preparation checks — plan
intent: 2026-11-12-cli-json-pilot@d19fc147
spec: docs/loom/2026-11-12-cli-json-pilot/spec.md@c5d46756
charter: 1.1

## Task DAG

### Wave 0 — Freeze comparison obligations

**W0-01 Preregister the matched-task comparison packet** after: none acceptance: 3
- Files: docs/loom/2026-11-12-cli-json-pilot/evidence/comparison-protocol.md, docs/loom/2026-11-12-cli-json-pilot/evidence/comparison-oracle.json
- Test: A3 positive: genuine-task-identities-and-four-metrics; boundary: no-posthoc-success-threshold.
- Risk: agent-decided — REQ-3 design requires preregistration before comparison; keep operator instructions separate from expected answers and commit the packet before execution.

### Wave 1 — Implement the optional representation

**W1-01 Add direct-data JSON results through the public CLI** after: W0-01 acceptance: 1, 2
- Files: loom-code/scripts/loom_checker.py (public entry: main), loom-code/scripts/loom_checker/command_handlers/plan.py, loom-code/scripts/loom_checker/command_handlers/intake.py, loom-code/scripts/loom_checker/preparation_output.py, loom-code/scripts/loom_checker/rule_checks/intent.py, loom-code/tests/test_preparation_json.py, loom-code/tests/test_loom_checker_cli.py, loom-code/tests/test_loom_checker_modules.py
- Test: A1 positive: json-passed-blocked-usage-internal; boundary: selector-help-notice-integrity. A2 positive: legacy-stream-and-rule-parity; boundary: hooks-other-commands-and-single-execution.
- Risk: agent-decided — REQ-1/2 direct-data and compatibility decisions; preserve and widen existing test_loom_checker_cli.py and test_loom_checker_modules.py coverage, never weaken dispatcher ownership. New helper remains bounded to preparation results; tests use public main/subprocess entry.

### Wave 2 — Synchronize the release candidate

**W2-01 Complete the 3.71.0 release packet and Build evidence** after: W1-01 acceptance: 1, 2
- Files: loom-code/.claude-plugin/plugin.json (SSOT), loom-code/.codex-plugin/plugin.json and loom-code/plugin.json and loom-code/package.json (generated), loom-code/CHANGELOG.md (new 3.71.0 entry), README.md, loom-code/README.md, loom-code/README.zh-TW.md and loom-code/README.ja.md, loom-code/tests/test_write_plan_station_text.py (CURRENT_VERSION), docs/loom/2026-11-12-cli-json-pilot/evidence/build-handoff.md
- Test: A1 positive: current-release-json-guidance; boundary: text-default-disclosure. A2 positive: synchronized-release-metadata; boundary: generated-manifest-check.
- Risk: agent-decided — REQ-1/2 representation-only scope requires accurate release guidance; use sync_codex_manifests.py --all, retain existing pin-test coverage, and declare the version before final review. Record genuine RED/GREEN and complete-suite evidence separately.

### Wave 3 — Run the preregistered comparison

**W3-01 Execute independent matched tasks and retain all observations** after: W2-01 acceptance: 3
- Files: docs/loom/2026-11-12-cli-json-pilot/evidence/comparison-protocol.md, docs/loom/2026-11-12-cli-json-pilot/evidence/comparison-oracle.json, docs/loom/2026-11-12-cli-json-pilot/evidence/comparison-results.md, docs/loom/2026-11-12-cli-json-pilot/evidence/comparison-raw.json
- Test: A3 positive: two-operator-matched-results; boundary: carryover-and-non-improvement-disclosure.
- Risk: agent-decided — REQ-3 comparison design; dispatch fresh non-implementing operators sequentially with opposite mode order, keep the oracle private until scoring, retain failures and recomputable counts. Independent acceptance judges the results; the implementer produces artifacts, never a verdict.

## Simplicity check

- none found

## Questions asked

① — what — 是否按此範圍進行？

## Risks

1. The public schema is an external contract; its six fields and status/error meanings must agree across both commands. The spec declares a single bounded mechanism-budget exception; no global output framework or new validation policy is authorized.
2. Legacy consumers include tests and station commands. Preserve normal text streams byte-for-byte, BLOCK ordering, advisory timing, exit codes and exact help; compare against main at 391fd01723efedfada3447673b1b99c3894af859, not another newly refactored implementation.
3. W0 freezes six tasks: plan success, field-cap rejection and missing operand; intake success, early confirmation rejection and advisory-before-late-BLOCK. Use authentic prior committed artifacts; label deliberate mutations and retain their source identities. Corrections touch only disposable copies.
4. Before operators start, pin the candidate SHA, artifact hashes, exact task instructions, expected result classifications and correction targets. Do not change these after viewing outcomes; unexpected cases remain failures or limitations, not substituted tasks.
5. Two informed operators each complete both modes on fresh identical snapshots, in opposite mode order. They receive task goals and discoverable help, not commands, prepared answers or implementation explanations. This is counterbalanced exploration, not a blind benchmark or population estimate.
6. Count interpretation errors against the frozen oracle; corrections are failed-attempt-to-next-attempt changes; operation steps are all tool invocations, with CLI invocations separately counted; output volume is stdout/stderr UTF-8 bytes separately. Preserve exact commands, exits, timestamps and operator answers.
7. Report per-task/per-operator values and raw totals for both modes, including zero differences and regressions. Exclude setup-only failures from task metrics but retain them separately. No posthoc threshold, assumed time/token benefit, or efficiency gate determines whether REQ-3 worked.
8. If an operator cannot complete a task, retain the incomplete result and actual resource boundary; do not manufacture interpretation counts or silently replace the operator. An alternative run needs a separately identified record and disclosed rationale.
9. No tests, adversarial work, independent acceptance or package suite are skipped. Build uses the locked complete runner, synchronizes trunk first, and reruns committed adversarial programs; finalization repeats checks on the reviewed candidate. No new paid external review is selected.
10. Required spec+adversarial review passed before planning. Engineering is exempt from decision point ②; decision point ① is already confirmed with automatic publication authorization. Merge remains a separate acceptance; retain every existing worktree.
