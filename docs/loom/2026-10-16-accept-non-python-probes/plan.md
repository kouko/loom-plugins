# Accept Go, JavaScript/TypeScript and Rust adversarial probes — plan
intent: 2026-10-16-accept-non-python-probes@8ccc9612
charter: 1.1

## Current State Evidence
- Forward: `probes.py:command_executes_artifact` accepts only Python/pytest/uv/conda and bash/sh argv; any other suffix requires argv[0] to be the artifact itself.
- Reverse: `command_handlers/finalize.py:_finalize` and `attestation.py` both call `command_names_artifact` then `command_executes_artifact`; one refusal blocks attestation generation and validation alike.
- Error: finalize returns `finalize.adversarial` "command must execute the artifact directly"; zero adversarial executions is refused by `missing_adversarial_execution`.
- Data: `probes.py:TEST_COMMAND_MARKERS` already maps `go.mod`, `Cargo.toml`, `package.json` to `go test ./...`, `cargo test`, `npm test`.
- Boundary: `probes.py:suite_collection` without `scripts/run_package_tests.py` only asks direct pytest, so a graduated Go or Rust test reads as not collected.

## Task DAG

**W1-01 Recognize Go, Node and Rust probe commands**  after: none  acceptance: 1,2,3,4
- Files: `loom-code/scripts/loom_checker/probes.py`, `loom-code/tests/test_probe_language_commands.py`
- Test: A1 positive: go-test-file-list-accepted; negative: go-vet-or-run-filter-refused. A2 positive: node-vitest-jest-cargo-accepted; negative: cargo-name-filter-refused. A3 positive: vitest-list-or-jest-config-refused; boundary: unlisted-flag-refused. A4 positive: python-shell-unchanged; negative: python-noop-refused.
- Risk: agent-decided — fail closed on any unlisted flag or positional; `cargo test --test <n>` names `tests/<n>.rs`, so `command_names_artifact` maps it. Widens; preserves `test_adversarial_pytest_option_order.py`, `test_loom_attestation.py` cases.

**W1-02 Count graduated Rust tests as suite-collected**  after: W1-01  acceptance: 2
- Files: `loom-code/scripts/loom_checker/probes.py`, `loom-code/tests/test_probe_language_suite_collection.py`
- Test: A2 positive: cargo-tests-dir-collected; negative: cargo-autotests-off-or-subdir-refused.
- Risk: agent-decided — Rust cannot run from the change store, so only the marker-default `cargo test` at repo root collects `tests/<n>.rs`; workspaces stay undeterminable. Preserves `test_selection_finalize.py` coverage.

**W2-01 Document per-language probe commands**  after: W1-02  acceptance: 1,2
- Files: `loom-code/skills/closing-review/references/adversarial.md`
- Test: A1 positive: go-store-example-documented; negative: none-docs-only. A2 positive: rust-graduation-documented; negative: none-docs-only.
- Risk: agent-decided — Go and JS/TS probes stay in the change store; Rust probes graduate to `tests/<n>.rs` through a plan task.

**W2-02 Release 3.41.0**  after: W2-01  acceptance: 4
- Files: `loom-code/plugin.json`, `loom-code/.claude-plugin/plugin.json`, `loom-code/.codex-plugin/plugin.json`, `loom-code/package.json`, `loom-code/CHANGELOG.md`, `loom-code/tests/test_write_plan_station_text.py`, `README.md`, `loom-code/README*.md`
- Test: A4 positive: release-metadata-synchronized; negative: stale-version-refused.
- Risk: agent-decided — minor bump because station guidance changes; CHANGELOG entry, pin rewrite and README version strings are deliverables of this task.

## Simplicity check
- Go probes stay in the change store instead of graduating, so W1-02 is Rust-only — taken
- Merge README version sync into the release task — taken

## Questions asked
① — what — 這次修好後，你希望審查證明工具能接受哪些語言寫的找漏洞測試？（答：Go 跟其他常見語言 (Recommended)）

## Risks
1. `cargo` is not installed on this machine; Acceptance #2's Rust line needs a Rust toolchain in the acceptance environment, else the report marks it untested.
2. A store-resident Go probe compiles as its own package, so it reaches only exported identifiers; verified `go test <store>/x_test.go` passes in a scratch module.
3. A `go test -run` or cargo test-name filter can select zero tests and still exit 0, so both stay refused rather than allowlisted.
