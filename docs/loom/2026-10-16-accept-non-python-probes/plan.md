# Accept adversarial probes from any language and test framework — plan
intent: 2026-10-16-accept-non-python-probes@f6cc849d
charter: 1.1

## Current State Evidence
- Forward: `probes.py:command_executes_artifact` accepts Python/pytest/uv/conda and bash/sh argv; this branch's earlier commits add `_go_test_runs`, `_node_test_runs`, `_cargo_test_target`, which check only the argv, never what ran.
- Reverse: `command_handlers/finalize.py:_finalize` (lines 118-136) and `attestation.py:validate_attestation` (lines 86-89) both refuse on `command_names_artifact`/`command_executes_artifact`; finalize discards stdout/stderr of a passing run and records only `{kind, command, artifact, result, command_digest}`.
- Error: reproduced `node --test /dev/null` reporting `tests 1 / pass 1` and `pytest a.py b.py -k other` passing both predicates; command shape alone cannot show a file's tests ran.
- Data: `contract/manifest.yaml` grammar is `[{kind, command, artifact, result, command_digest}]`; `go test -json`, node and deno junit output carry per-test pass and skip status locally.
- Boundary: `closing-review/SKILL.md` returns any `finalize-review` failure to Build for a new round, so a reviewer confirmation must be gathered inside the round, before finalization.

## Task DAG

**W1-01 Runner table with result parsers for Go, Node, Deno, Bun and unittest**  after: none  acceptance: 1,2,3
- Files: `loom-code/scripts/loom_checker/probe_results.py`, `loom-code/scripts/loom_checker/probes.py`, `loom-code/tests/test_probe_runner_results.py`, `loom-code/tests/test_probe_language_commands.py`
- Test: A1 positive: go-json-passing-test-accepted; negative: go-all-skipped-refused. A2 positive: node-deno-bun-unittest-passing-accepted; negative: node-empty-file-level-case-refused. A3 positive: listed-runner-without-output-flag-or-extra-file-refused; boundary: unreadable-output-needs-confirmation.
- Risk: agent-decided — row table per spec Design decision; fixtures are real captured outputs. Folding `_go_test_runs`/`_node_test_runs` narrows `test_probe_language_commands.py`; preserves pytest/shell cases in `test_adversarial_pytest_option_order.py`, `test_loom_attestation.py`.

**W1-02 Rows for jest, vitest, mocha, rspec, minitest, phpunit, cargo test and nextest**  after: W1-01  acceptance: 2,3
- Files: `loom-code/scripts/loom_checker/probe_results.py`, `loom-code/scripts/loom_checker/probes.py`, `loom-code/tests/test_probe_runner_results.py`, `loom-code/tests/test_probe_language_suite_collection.py`
- Test: A2 positive: js-ruby-php-rust-passing-accepted; negative: results-from-another-file-refused. A3 positive: nextest-no-tests-not-fail-refused; boundary: bun-multi-file-summary-refused.
- Risk: agent-decided — npm/gem installs only in temporary directories; cargo target path via Cargo.toml `[[test]]` narrows the fixed mapping; preserves `test_probe_language_suite_collection.py`. An `.rspec` dry-run that real JSON cannot distinguish stays a residual risk.

**W2-01 Finalize and validate by parsed result or bound reviewer confirmation**  after: W1-02  acceptance: 3,4,5
- Files: `loom-code/scripts/loom_checker/command_handlers/finalize.py`, `loom-code/scripts/loom_checker/attestation.py`, `loom-code/scripts/loom_checker/reviewers.py`, `loom-code/contract/manifest.yaml`, `loom-code/tests/test_probe_confirmation_finalize.py`
- Test: A3 positive: listed-zero-passed-refused-even-with-confirmation; negative: claimed-but-untargeted-refused. A4 positive: unlisted-maven-with-confirmation-attested; negative: other-content-or-partial-line-quote-refused. A5 positive: pytest-shell-attestation-unchanged; negative: python-noop-still-refused.
- Risk: agent-decided — confirmation binding and the `evidence` execution field follow spec Design decision; the contract manifest grammar changes with them. Widens; preserves `test_loom_attestation.py` and `test_selection_finalize.py` coverage.

**W2-02 Document runner commands and the confirmation hand-off**  after: W2-01  acceptance: 2,4
- Files: `loom-code/skills/closing-review/references/adversarial.md`, `loom-code/skills/closing-review/SKILL.md`, `loom-code/agents/reviewer.md`, `loom-code/agents/adversary.md`
- Test: A2 positive: per-runner-command-forms-documented; negative: none-docs-only. A4 positive: reviewer-confirmation-handoff-documented; negative: none-docs-only.
- Risk: agent-decided — closing-review runs each non-pytest/shell probe once, hands its output path to the round's reviewers, and copies each reviewer's `{artifact, quote}` into the finalize input, so no extra round is needed; replaces the earlier per-language Recording examples.

**W3-01 Release 3.41.0**  after: W2-02  acceptance: 5
- Files: `loom-code/plugin.json`, `loom-code/.claude-plugin/plugin.json`, `loom-code/.codex-plugin/plugin.json`, `loom-code/package.json`, `loom-code/CHANGELOG.md`, `loom-code/tests/test_write_plan_station_text.py`, `README.md`, `loom-code/README*.md`
- Test: A5 positive: release-metadata-synchronized; negative: stale-version-refused.
- Risk: agent-decided — minor bump because an attestation field and station guidance change; CHANGELOG entry, pin rewrite and README version strings are deliverables.

## Simplicity check
- Reviewer-only for all new runners — declined: user chose industry-style parsing with reviewer fallback after seeing both
- Parse console summaries where a runner has no native per-test output, instead of requiring report plugins — taken
- Bind confirmation by quoted line in this run's output instead of an output digest (timings vary) — taken
- Graduated artifacts with undeterminable suite membership reuse reviewer confirmation — declined: confirming a run does not show suite membership

## Questions asked
① — what — 這次修好後，你希望審查證明工具能接受哪些語言寫的找漏洞測試？（答：Go 跟其他常見語言 (Recommended)）
① — what — 要多加哪些常用的語言 × 測試框架組合？（答：JS/TS：mocha、Bun、Deno；Python unittest、Rust nextest；Ruby（rspec、minitest）、PHP（phpunit））
① — what — 清單外的組合交給 LLM 判斷要這次一起加嗎？（答：這次一起加 (Recommended)）
① — what — 第一級被挑出漏洞後，新語言改用哪種接受方式？（答：A）
① — what — 依業界方式實作加上 LLM 備援，要做到多大、缺的執行器要裝嗎？（答：一次做完全部 13 個；用 Homebrew 裝 bun、php、rust、cargo-nextest、maven）
① — what — 覆述的需求對嗎？（答：對）

## Risks
1. Runner output formats drift across versions; an unreadable output falls back to reviewer confirmation instead of refusing, so drift costs a confirmation, not a block.
2. A test program can print fake results; parsers and reviewers alike cannot stop deliberate forgery (intent Out of scope).
3. Fixtures come from the locally installed versions (Go, Node 26, Deno, Bun 1.4.3, Python 3.12, PHP 8.5, cargo 1.99, nextest 0.9.148, Maven 3.10); older runner versions are untested.
4. jest/vitest/mocha/rspec/phpunit fixture capture needs package downloads into temporary directories.
