# Consistent planning-command guidance — plan
intent: 2026-11-12-cli-guidance-consistency@ecaac7d971c5e7ffc75996b4c78ac76517eaf908
spec: docs/loom/2026-11-12-cli-guidance-consistency/spec.md@d61475f09a2d6ecbd076df2a5784f5b3ceaac2b2
charter: 1.1

Current state evidence and behavior decisions: [spec.md](spec.md).

## Task DAG

### Wave 1 — Extend the existing public dispatcher

**W1-01 Add consistent guidance for the three preparatory checks** after: none acceptance: 1, 2, 3
- Files: `loom-code/scripts/loom_checker.py` (public entry: main), `loom-code/tests/test_loom_checker_cli.py`
- Test: A1 positive: planning-help-discovery; boundary: planning-help-outside-repo. A2 positive: planning-error-recovery; negative: malformed-help-shape. A3 positive: planning-output-compatible; boundary: conditional-intake-stdout.
- Risk: agent-decided — REQ-1/2/3 Design decisions retain dispatcher ownership. Extend existing `test_loom_checker_cli.py` coverage without removing cases; preserve the architecture guard and conditional intake stdout. Write failing subprocess/entry tests first; then extend the existing mapping only.

### Wave 2 — Release the completed batch

**W2-01 Synchronize the 3.70.0 release and retain Build evidence** after: W1-01 acceptance: 1, 2, 3
- Files: `loom-code/.claude-plugin/plugin.json`, generated code manifests, `loom-code/CHANGELOG.md`, `loom-code/README*.md`, `README.md`, `loom-code/tests/test_write_plan_station_text.py`, `docs/loom/2026-11-12-cli-guidance-consistency/evidence/`
- Test: A1 positive: release-guidance-present; boundary: deferred-commands-unchanged. A2 positive: release-help-consistent; negative: misleading-success-claim. A3 positive: release-metadata-synchronized; boundary: generated-manifest-drift.
- Risk: agent-decided — REQ-3 Design decisions preserve runtime contracts. Bump SSOT to 3.70.0; add dated CHANGELOG section, update README versions and CURRENT_VERSION pin, run sync_codex_manifests.py --all and --check; retain existing release-test coverage. Finalize only after all release edits.

## Simplicity check
- none found

## Questions asked

① — what — 確認後我會繼續規格與實作，驗證通過後更新 Ready PR；合併另行確認。這個範圍可以嗎？

## Risks

1. Public help can misstate partial check outcomes; preserve all three handlers and their result streams. Independent acceptance must exercise genuine committed artifacts, recovery and conditional intake output, rather than infer semantics from green unit tests.
2. The release packet includes CHANGELOG entry `## [3.70.0] — 2026-11-12 — extend planning-command help and recovery guidance`, generated manifests, four README surfaces and the existing release-pin test. Minor version reflects the extended public CLI guidance contract.
3. Build runs the complete locked package runner and independent adversarial programs before Closing Review; finalization repeats both. Prepare npm dependencies before the full suite so visualization coverage is executed instead of provisionally skipped.
4. No ARCHITECTURE.md exists. No new parser, formatter, output envelope, handler validation, hook behavior or remote mutation belongs to this change. Independent review checks the bounded mechanism budget against the completed diff.
5. Agent-decided — this reversible mapping extension adds no paid service or standing obligation. Existing-data and publication authority remain unchanged; automatic publication is authorized by the confirmed intent, while merge requires separate acceptance.
