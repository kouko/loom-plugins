# Accept adversarial probes from any language and test framework — spec
intent: 2026-10-16-accept-non-python-probes@f6cc849d
pre-build-review: required — changes the attestation contract field `executions` and what the review-evidence checker trusts

## Requirements
REQ-1 — Go probe attests by parsed result
  WHEN a recorded `go test -json <artifact>_test.go` probe exits 0 with at least one passing, non-skipped test in its JSON events, finalize-review shall attest it with no reviewer confirmation and the validator shall accept that attestation → Acceptance #1
REQ-2 — Listed runners attest by parsed result
  WHEN a recorded probe uses a listed runner row (unittest, node --test, vitest, jest, mocha, bun, deno, cargo test, cargo nextest, rspec, minitest, phpunit) in its documented form and its output shows at least one passing, non-skipped test from the artifact, finalize-review shall attest it with no reviewer confirmation → Acceptance #2
REQ-3 — Listed runners refuse non-running or empty runs
  WHEN an argv is claimed by a listed row but does not run only the artifact with the row's output form, or its output shows zero passing tests from the artifact, or shows tests from another file, finalize-review and the validator shall refuse it, whether or not a confirmation is supplied → Acceptance #3
REQ-4 — Reviewer confirmation fallback
  WHEN an argv is claimed by no row, or a listed run's output is unreadable, or a graduated artifact's suite membership is undeterminable, finalize-review shall attest only with a confirmation whose reviewer is one of the verdict reviewers and whose quote occurs in this finalize run's output, recording reviewer and quote in the execution; otherwise it shall refuse → Acceptance #4
REQ-5 — pytest and shell unchanged
  WHEN a probe is a Python/pytest or bash/sh program, the existing acceptance rules shall apply unchanged and the package suite shall pass → Acceptance #5

## Design decision
- agent-decided: a new module `loom_checker/probe_results.py` holds one table of rows; each row has `claims(argv)`, `targets(argv, artifact)` and `passed(output, artifact) -> int | None`. Adding a runner is one row plus its fixtures; `probes.py` keeps the pytest/shell rules.
- agent-decided: the recorded command itself carries the machine-readable output flag where the runner has one built in (`go test -json`, `node --test --test-reporter=junit`, `deno test --reporter=junit`, `jest --json --runTestsByPath`, `vitest run --reporter=json`, `mocha --reporter json`, `rspec --format json`); the checker never rewrites a user's command. Runners without a built-in per-test format are read from their console summary (unittest, bun, cargo test, nextest, minitest, phpunit).
- agent-decided: attribution — `targets` admits exactly one test-file positional, the artifact; where the output names files (node, deno, jest, vitest, mocha, rspec), any test from another file refuses the run. A node file-level case (name equals the file's base name, no subtests) is not a test.
- agent-decided: `passed` returns None for output it cannot read; None routes to the confirmation fallback instead of refusing, so format drift costs a confirmation, not a block. A readable zero refuses.
- agent-decided: cargo — `cargo test --test <n>` and `cargo nextest run --test <n>` resolve `<n>` through Cargo.toml `[[test]]` `path`, defaulting to `tests/<n>.rs`; nextest is refused when `--no-tests` is set to anything other than `fail`.
- agent-decided: confirmation binding — the input item carries `confirmation: {reviewer, quote}`; `reviewer` must equal one verdict's `reviewer`, `quote` must be a non-empty substring of this finalize run's combined stdout and stderr. A quote is used instead of an output digest because runner output carries timings that differ per run.
- agent-decided: attestation executions gain `evidence: "parsed"` with `passed: <n>`, or `evidence: "reviewer"` with `confirmation: {reviewer, quote}`; pytest/shell executions carry no `evidence` key, as today. The validator does not re-run programs; it recomputes `claims`/`targets`, refuses a `reviewer` execution whose argv a row claims and the run was readable, and checks the confirmation's reviewer against the attestation's verdicts.
- agent-decided: closing-review runs each non-pytest/shell probe once before dispatching the round's reviewers, hands them the output paths, and copies each reviewer's `{artifact, quote}` into the finalize input; a confirmation is gathered inside the round so no extra round is needed.

## Alternatives considered
- Reviewer confirmation for every new runner — smaller, but the user chose industry-style result parsing after seeing both.
- Command-shape allowlist only — cannot show tests ran (`node --test /dev/null`, `pytest a b -k other`, nextest `--no-tests=warn`).
- Injecting reporter flags at finalize — rewrites the user's command and can conflict with their config.
- Requiring JUnit XML everywhere — several runners need extra plugins (jest, rspec, minitest) and several JUnit dialects carry no file path.

## Current state evidence
- Forward: `loom-code/scripts/loom_checker/probes.py:command_executes_artifact`
- Reverse: `loom-code/scripts/loom_checker/command_handlers/finalize.py:_finalize`, `loom-code/scripts/loom_checker/attestation.py:validate_attestation`
- Error: `finalize.adversarial` "command must execute the artifact directly"
- Data: `loom-code/contract/manifest.yaml` attestation `executions` grammar
- Boundary: `loom-code/skills/closing-review/SKILL.md` returns every finalize failure to Build for a new round

## UI flows
N/A
