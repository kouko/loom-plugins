# Close the remaining probe-acceptance gaps — plan
intent: 2026-10-18-close-probe-acceptance-gaps@184b2f1e
charter: 1.1

## Current State Evidence
- Forward: `loom-code/scripts/loom_checker/probes.py:command_executes_artifact` (line 589) accepts `python -m pytest` when the first positional is the artifact, allowing more files and `-k`/`-m`/`--deselect`.
- Reverse: `finalize.py` line 212 tests the store by `startswith`; a `./` prefix lets `git cat-file` normalize `..` and escape it; `attestation.py` line 145 checks no path form.
- Error: `pytest a.py b.py -k other` exits 0 with none of `a.py`'s tests run and is attested; `env go test …`, `npx --yes jest` fall to reviewer confirmation.
- Data: `probe_results.py` `_named` (line 46) and `JS_LAUNCHERS` (line 290); `probes.py:cargo_test_targets` (line 216) reads Cargo.toml test targets.
- Boundary: `probes.py` line 178 parses the declared package-suite pytest command with the shared `pytest_positionals`; its filters must stay allowed.

## Task DAG

**W1-01 Refuse pytest probes that list other files or deselect tests**  after: none  acceptance: 1
- Files: `loom-code/scripts/loom_checker/probes.py`, `loom-code/scripts/loom_checker/command_handlers/finalize.py`, `loom-code/tests/test_probe_pytest_summary.py`
- Test: A1 positive: sole-artifact-pytest-passing-accepted; negative: config-addopts-deselect-refused. A1 boundary: second-positional-refused-suite-filter-still-collects.
- Risk: agent-decided — sole positional in `command_executes_artifact` (finalize and validator); finalize reads the pytest summary line, refusing deselected, zero passed or no summary. Narrows `test_adversarial_pytest_option_order.py`; preserves `test_loom_attestation.py`.

**W1-02 Refuse artifact paths that escape the store**  after: W1-01  acceptance: 2
- Files: `loom-code/scripts/loom_checker/command_handlers/finalize.py`, `loom-code/scripts/loom_checker/attestation.py`, `loom-code/tests/test_probe_artifact_path_escape.py`
- Test: A2 positive: store-artifact-accepted; negative: dotdot-escape-refused-by-finalize-and-validator.
- Risk: agent-decided — one path-form refusal (leading `./` or `../`, any `..` part, or any part `normpath` changes) in finalize before `cat-file` and in the validator; existing `startswith` then suffices.

**W1-03 Parse env and npx/pnpm launcher forms**  after: W1-02  acceptance: 3
- Files: `loom-code/scripts/loom_checker/probe_results.py`, `loom-code/tests/test_probe_language_commands.py`, `loom-code/skills/closing-review/references/adversarial.md`
- Test: A3 positive: env-go-npx-yes-pnpm-jest-parsed; negative: env-option-or-pnpm-script-name-refused-or-confirmed.
- Risk: agent-decided — `env` with only `NAME=value` prefixes is stripped before `_named`; `npx --yes` and bare `pnpm` join `JS_LAUNCHERS`; any `env` option falls to reviewer confirmation. Widens `test_probe_language_commands.py`.

**W1-04 Count cargo targets enabled by default features and tests/<dir>/main.rs**  after: W1-03  acceptance: 4,5
- Files: `loom-code/scripts/loom_checker/probes.py`, `loom-code/tests/test_probe_language_suite_collection.py`
- Test: A4 positive: default-feature-target-and-dir-main-collected; negative: transitive-feature-target-refused. A5 positive: dir-main-graduated-probe-collected; boundary: test-false-dir-main-refused.
- Risk: agent-decided — direct `[features] default` membership only (intent Out of scope); A5's real-tool Bun and Rust re-run belongs to acceptance testing, Bun code is untouched. Widens `test_probe_language_suite_collection.py`.

**W2-01 Release 3.42.0**  after: W1-04  acceptance: 6
- Files: `loom-code/plugin.json`, `loom-code/.claude-plugin/plugin.json`, `loom-code/.codex-plugin/plugin.json`, `loom-code/package.json`, `loom-code/CHANGELOG.md`, `loom-code/tests/test_write_plan_station_text.py`, `README.md`, `loom-code/README*.md`
- Test: A6 positive: full-package-suite-passes; negative: release-metadata-pin-catches-stale-version.
- Risk: agent-decided — minor bump because station guidance (`adversarial.md`) and acceptance rules change; CHANGELOG entry, pin rewrite and README version strings are deliverables.

## Simplicity check
- Remove `-k`/`-m`/`--deselect` from the shared pytest allowlist — declined: misses config, plugin and conftest filters, and breaks suite commands that filter
- Make pytest a parsed row with per-test output — declined: rewrites existing recorded pytest commands, breaking the unchanged-acceptance constraint
- Resolve transitive cargo features — declined: intent Out of scope; direct default membership is a few lines
- Parse wrapper forms through the existing launcher table rather than new rows — taken
- One path-form refusal instead of a containment helper plus refusal (plan reviewer) — taken
- Bun unit fixtures for A5 dropped; A5 is a real-tool acceptance re-run (plan reviewer) — taken
- W2-01 Test re-pointed to the full suite, A6's actual outcome (plan reviewer) — taken

## Questions asked
① — what — 要怎麼處理這些剩下的問題？（答：先合併，再開新變更 (Recommended)）
① — what — 覆述的需求對嗎？（答：對）
① — what — 要改用 B 嗎？（答：Ｂ）

## Risks
1. A conftest hook that drops items without reporting them as deselected stays invisible to the summary check; intent Out of scope covers deliberate forgery only, so this is a disclosed residual.
2. The validator checks path form only; a normalized out-of-store path the suite does not collect is refused by finalize's collection check but not re-checked at validation.
3. pytest summary wording may change across versions; an unreadable summary refuses rather than accepting, costing a Build round, never a false attestation.
