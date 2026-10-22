# Accept Go package adversarial probes — plan
intent: 2026-10-23-go-package-adversarial-probes@70001000
charter: 1.1

## Current State Evidence
- Forward: `probe_results.py:_go_accepts` requires one positional `_test.go` artifact and rejects `-run`; `closing-review/references/adversarial.md` prescribes the same command.
- Reverse: `attestation.py:adversarial_route` sends claimed Go commands to that row; `finalize.py:_runner_evidence` counts its parsed passing events before attesting.
- Error: Go compiles only explicitly named files for `go test file.go`; a probe needing sibling source and test helpers fails before any result can be read.
- Data: `probe_results.py:_go_passed` reads Go JSON test names without source files; `go list -json` reports selected `TestGoFiles` and `XTestGoFiles`.
- Boundary: `test_probe_language_commands.py` pins single-file Go forms, filtered-command rejection, zero-pass rejection, and other runner forms.

## Task DAG

**W1-01 Accept a Go package run bound to an artifact test**  after: none  acceptance: 1,2,3
- Files: `loom-code/scripts/loom_checker/probe_results.py`, `loom-code/tests/test_probe_language_commands.py`, `loom-code/tests/test_probe_confirmation_finalize.py`, `loom-code/skills/closing-review/references/adversarial.md`
- Test: A1 positive: sibling-dependent-package-probe-finalizes-and-validates; negative: missing-sibling-go-test-fails. A2 positive: exact-artifact-test-passes; negative: filtered-out-or-other-file-test-refused. A3 positive: existing-single-file-go-probe-passes; boundary: skipped-or-cached-result-refused.
- Risk: agent-decided — package mode requires `-json -count=1 -run '^TestName$'`, one package, selected artifact, and its declared test; Go JSON must show that test passing. Preserve existing single-file cases.

**W2-01 Release the corrected Go runner contract**  after: W1-01  acceptance: 3
- Files: `loom-code/plugin.json`, `loom-code/.claude-plugin/plugin.json`, `loom-code/.codex-plugin/plugin.json`, `loom-code/package.json`, `loom-code/CHANGELOG.md`, `loom-code/tests/test_write_plan_station_text.py`, `loom-code/README.md`, `README.md`
- Test: A3 positive: release-metadata-synchronized; negative: stale-version-pin-refused.
- Risk: agent-decided — bump loom-code to 3.48.0 because station guidance changes; update CHANGELOG entry, version pin, and README strings before final attestation.

## Simplicity check
- none found

## Questions asked
① — what — 這是你要的範圍嗎？

## Risks
1. Go JSON events carry test names but no defining file; package acceptance must bind an exact test name to a declaration in the selected, committed artifact before a pass counts.
2. Go may exclude a file through build constraints or reuse a cached package result; check selected test files and require `-count=1` for fresh execution.
