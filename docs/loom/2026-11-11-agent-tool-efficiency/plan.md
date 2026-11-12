# Gradual CLI conventions and tool efficiency — plan
intent: 2026-11-11-agent-tool-efficiency@3499c468
spec: docs/loom/2026-11-11-agent-tool-efficiency/spec.md@05014d31
charter: 1.1

## Task DAG

### Wave 1 — First CLI rollout

**W1-01 Publish progress boundary tests and implementation** after: none acceptance: 1, 4
- Files: `loom-code/scripts/loom_checker/command_handlers/publish.py` (entry: cmd_publish), `loom-code/tests/test_loom_publish.py`
- Test: A1 positive: publish_progress_before_wait; boundary: publish_progress_cadence. A4 positive: publish_stdout_unchanged; negative: publish_progress_failure_preserves_authority.
- Risk: agent-decided — REQ-1/4; preserve every existing test_loom_publish.py case, especially registration, timeout and mutation authorization; extend coverage through injected streams and clocks without changing polling decisions.

**W1-02 Finalization progress boundary tests and implementation** after: W1-01 acceptance: 1, 4
- Files: `loom-code/scripts/loom_checker/command_handlers/finalize.py` (entry: cmd_finalize_review), `loom-code/tests/test_selection_finalize.py`
- Test: A1 positive: finalize_progress_before_child_exit; negative: finalize_exit_zero_invalid_evidence. A4 positive: finalize_stdout_unchanged; boundary: finalize_progress_stream_failure.
- Risk: agent-decided — REQ-1/4; preserve test_selection_finalize.py evidence and refusal coverage; pass stage only after evidence validators. Keep captured child logs and existing terminal errors. Prefer local stream writes over a new shared module.

### Wave 2 — Avoid irrelevant collection

**W2-01 Concern-first discovery boundary tests and implementation** after: W1-02 acceptance: 2, 4
- Files: `loom-code/scripts/loom_checker/probes.py` (entry: graduated_probe_programs), `loom-code/tests/test_selection_finalize.py`
- Test: A2 positive: ordinary_files_skip_collection; boundary: marked_moved_unknown_collection. A4 positive: graduated_probe_cap_preserved; negative: executed_unmarked_probe_refused.
- Risk: agent-decided — REQ-2/4; preserve test_selection_finalize.py and test_probe_language_suite_collection.py coverage. Reorder existing predicates only; retain is-not-False semantics and moved-path handling.

### Wave 3 — Measure before adding a converter

**W3-01 Compare review conversion alternatives** after: W2-01 acceptance: 3
- Files: `docs/loom/2026-11-11-agent-tool-efficiency/evidence/conversion-comparison.md`, `docs/loom/2026-11-11-agent-tool-efficiency/evidence/conversion-fixtures.json`, `docs/loom/2026-11-11-agent-tool-efficiency/evidence/conversion-results.json`
- Test: A3 positive: valid_review_conversion_comparison; negative: malformed_duplicate_missing_identity_rejected. Replay exact retained baseline and candidate commands on identical fixtures.
- Risk: agent-decided — REQ-3; preserve raw outputs and differing failures; record caller operations and candidate footprint. Retain replay snippets in the comparison document, no production adapter or token/time extrapolation.

### Wave 4 — Document applicability and prepare release

**W4-01 Document the first rollout and synchronize release metadata** after: W3-01 acceptance: 1, 2, 3, 4
- Files: `README.md`, `loom-code/README*.md`, `loom-code/.claude-plugin/plugin.json`, `loom-code/.codex-plugin/plugin.json`, `loom-code/plugin.json`, `loom-code/package.json`, `loom-code/CHANGELOG.md`, `loom-code/tests/test_write_plan_station_text.py`
- Test: A1 positive: release_progress_documented; boundary: unsupported_modes_not_claimed. A2 positive: discovery_change_recorded; boundary: policy_unchanged. A3 positive: comparison_link_resolves; negative: unmeasured_benefit_absent. A4 positive: release_metadata_synchronized; boundary: hook_contract_unchanged.
- Risk: agent-decided — REQ-1/4; existing README Development section carries a short convention/applicability summary. Minor 3.67.0 documents the CLI contract; sync generated manifests, CHANGELOG entry, README versions and CURRENT_VERSION pin before final review.

**W4-02 Synchronize publication waiting guidance** after: W4-01 acceptance: 1, 4
- Files: `loom-code/skills/ship/SKILL.md`
- Test: A1 positive: documented_elapsed_notice; boundary: unchanged_polling_not_repeated. A4 positive: existing_ship_station_tests; negative: authorization_guidance_unchanged.
- Risk: agent-decided — REQ-1/4; fix outdated no-repeat wording found across cumulative changed files and Ship guidance; retain polling limits, authorization and termination policy. Existing test_ship_station_text.py coverage is preserved.

## Simplicity check
- none found

## Questions asked
① — what — 確認按這個範圍進行，並在驗證通過後自動建立 Ready PR 嗎？合併仍另行確認，發佈前也可撤回授權。

## Risks
1. Progress messages must never become verification inputs. The first rollout preserves existing outputs and authorization; additional help, typed errors and JSON modes are deferred rather than promised as implemented.
2. No ratified ARCHITECTURE.md exists. Keep command handlers and tests in their existing locations; no module split or new dependency is planned.
3. A converter is an experiment only. Record a negative recommendation when benefits do not outweigh caller complexity, identity/provenance risks or maintenance cost.
4. Build uses sequential implementers, failing regression tests before each code fix, a fresh adversary, and the complete locked package suite. Closing Review independently checks acceptance and code; finalization replays required verification.
5. Full suite: `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`. No validation step is skipped; only focused checks run during task development.
6. Publication is authorized after required review and checks; merge remains separate. This planning checkpoint does not claim code, acceptance, or host installation completion.
