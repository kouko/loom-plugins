# Accept Go package adversarial probes — plan
intent: 2026-10-23-go-package-adversarial-probes@70001000
charter: 1.1

## Current State Evidence
- Forward: `probe_results.py:_go_accepts` requires one positional `_test.go` artifact and rejects `-run`; `closing-review/references/adversarial.md` prescribes the same command.
- Reverse: `attestation.py:adversarial_route` sends Go commands to that row; `finalize.py` first checks `probes.py:suite_collection` for an artifact outside the change store.
- Error: Go compiles only explicitly named files for `go test file.go`; a probe needing sibling source and test helpers fails before any result can be read.
- Data: `probe_results.py:_go_passed` reads Go JSON test names without source files; `go list -json` reports selected `TestGoFiles` and `XTestGoFiles`.
- Boundary: `probes.py:suite_collection` recognizes cargo and pytest, not a Go package suite; existing tests pin Go single-file forms and other runners.

## Task DAG

**W1-01 Accept a Go package run bound to an artifact test**  after: none  acceptance: 1,2,3
- Files: `loom-code/scripts/loom_checker/probe_results.py`, `loom-code/scripts/loom_checker/probes.py`, `loom-code/scripts/loom_checker/attestation.py`, `loom-code/scripts/loom_checker/command_handlers/finalize.py`, `loom-code/tests/test_probe_language_commands.py`, `loom-code/tests/test_probe_language_suite_collection.py`, `loom-code/tests/test_probe_confirmation_finalize.py`, `loom-code/skills/closing-review/references/adversarial.md`
- Test: A1 positive: sibling-dependent-package-probe-finalizes-and-validates; negative: suite-does-not-collect-artifact. A2 positive: exact-artifact-test-passes; negative: filtered-out-or-other-file-test-refused. A3 positive: existing-single-file-go-probe-passes; boundary: skipped-or-cached-result-refused.
- Risk: agent-decided — package mode requires `-json -count=1 -run '^TestName$'`, one package, selected artifact, and its declared test; permit literal `$` in argv without shell execution. Widen Go suite collection only; preserve other runners.

**W2-01 Release the corrected Go runner contract**  after: W1-01  acceptance: 3
- Files: `loom-code/plugin.json`, `loom-code/.claude-plugin/plugin.json`, `loom-code/.codex-plugin/plugin.json`, `loom-code/package.json`, `loom-code/CHANGELOG.md`, `loom-code/tests/test_write_plan_station_text.py`, `loom-code/README*.md`, `README.md`
- Test: A3 positive: release-metadata-synchronized; negative: stale-version-pin-refused.
- Risk: agent-decided — bump loom-code to 3.48.0 because station guidance changes; update CHANGELOG entry, version pin, and README strings before final attestation.

**W1-02 Graduate the adversarial Go attribution probe**  after: W1-01  acceptance: 2,3
- Files: `docs/loom/2026-10-23-go-package-adversarial-probes/evidence/probes/test_go_misattributed_comment.py`, `loom-code/tests/test_probe_language_commands.py`
- Test: A2 positive: commented declaration cannot claim sibling test pass; negative: the probe turned red before the Go source-scanner fix. A3 boundary: permanent package suite collects the graduated probe.
- Risk: agent-decided — the adversarial program exposed a real false attribution; move it into the standing suite before final review so later changes rerun it.

## Simplicity check
- none found

## Questions asked
① — what — 這是你要的範圍嗎？

## Risks
1. Go JSON events carry test names but no defining file; package acceptance must bind an exact test name to a declaration in the selected, committed artifact before a pass counts.
2. Go may exclude a file through build constraints or reuse a cached package result; check selected test files and require `-count=1` for fresh execution.
3. Go permits the same test name in the package and external test package, but JSON does not distinguish their events; reject ambiguous selected declarations.
