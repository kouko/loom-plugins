# Accept adversarial probes from any language and test framework — spec
intent: 2026-10-16-accept-non-python-probes@f6cc849d
pre-build-review: required — changes the attestation contract field `executions` and what the review-evidence checker trusts

## Requirements
REQ-1 — Go probe attests by parsed result
  WHEN a recorded `go test -json <artifact>_test.go` probe exits 0 with at least one passing, non-skipped test in its JSON events, finalize-review shall attest it with no reviewer confirmation and the validator shall accept that attestation → Acceptance #1
REQ-2 — Listed runners attest by parsed result
  WHEN a recorded probe uses a listed runner row (table below) in its accepted argv form and its output shows at least one passing, non-skipped test from the artifact and from no other file, finalize-review shall attest it with no reviewer confirmation → Acceptance #2
REQ-3 — Listed runners refuse non-running or empty runs
  WHEN an argv is claimed by a listed row but is not in that row's accepted form (another test file, a filter, a non-running subcommand or option, a missing output flag, a bun positional without `./`), or finalize-review reads zero passing tests from the artifact, or tests from another file, or a summary covering more than one file, finalize-review shall refuse it whether or not a confirmation is supplied, and the validator shall refuse an attested execution whose argv a row claims but does not accept → Acceptance #3
REQ-4 — Reviewer confirmation fallback
  WHEN an argv is claimed by no row, or a listed run in accepted form produces output its row cannot read, finalize-review shall attest only with a confirmation whose `reviewer` is one of the verdict reviewers, whose `reviewed_sha` has the same functional content digest as HEAD, and whose `quote` is one or more complete, non-blank lines of this finalize run's output containing the artifact's file stem; a missing confirmation, a different-content `reviewed_sha`, or a quote failing those rules is refused → Acceptance #4
REQ-5 — pytest, shell and graduation unchanged
  WHEN a probe is a Python/pytest or bash/sh program or a directly executed artifact, the existing acceptance rules shall apply unchanged; a graduated artifact still needs suite membership as today, with a declared `cargo nextest run` treated like `cargo test`; the package suite shall pass → Acceptance #5

### Accepted argv per row
| Row | Claims (runner identity) | Accepted form (`<A>` = the artifact; `[w]` = allowed launcher) |
|---|---|---|
| go | `go test` | `go test -json [-v] [-race] [-count N] [-timeout D] [-tags T] <A>` with `<A>` ending `_test.go`, the only positional |
| unittest | `python -m unittest` (same python/uv/conda launchers as pytest) | `python -m unittest [-v] [-q] <A>` |
| node | `node --test` | `node --test --test-reporter=junit [--experimental-strip-types] <A>` |
| deno | `deno test` | `deno test --reporter=junit [-A] [--allow-*] <A>` |
| bun | `bun test` | `bun test ./<A>` (an absolute path is refused: the recorded command must validate from any checkout) |
| jest | `jest` via `[npx|pnpm exec|yarn]` | `[w] jest --json --runTestsByPath <A>` |
| vitest | `vitest` via `[npx|pnpm exec|yarn]` | `[w] vitest run --reporter=json --outputFile=/dev/stdout <A>` (vitest 5 writes JSON to a file unless `--outputFile` points at stdout) |
| mocha | `mocha` via `[npx|pnpm exec|yarn]` | `[w] mocha --reporter json <A>` |
| cargo test | `cargo test` | `cargo test [--release] [-q] --test <n>`, `<n>` resolving to `<A>` |
| nextest | `cargo nextest` | `cargo nextest run [--release] [--no-tests=fail] --test <n>`, `<n>` resolving to `<A>` |
| rspec | `rspec` via `[bundle exec]` | `[w] rspec --format json <A>` |
| minitest | `ruby` with `<A>` named `*_test.rb` or `test_*.rb`, via `[bundle exec]` | `[w] ruby [-I<dir>]... <A>` |
| phpunit | `phpunit` at any path (e.g. `vendor/bin/phpunit`) | `<phpunit> <A>` |

Runner and launcher names in the Claims column match the file name of the argv element, so a full path such as `/opt/homebrew/bin/go` is claimed as `go`. The go, deno, bun and cargo rows claim the runner whatever its subcommand, so a non-test subcommand (`go vet`, `deno check`, `bun build`, `cargo build`) is claimed and refused rather than routed to REQ-4. Any other argv (for example `node X.mjs` without `--test`, `java X.java`, `mvn ...`) is claimed by no row and goes to REQ-4; a directly executed artifact stays under REQ-5.

## Design decision
- agent-decided: a new module `loom_checker/probe_results.py` holds the row table; each row has `claims(argv)`, `accepts(argv, artifact)` and `passed(output, artifact) -> int | None`. Adding a runner is one row plus its fixtures; `probes.py` keeps the pytest/shell rules.
- agent-decided: the recorded command carries the machine-readable output flag where the runner has one built in; the checker never rewrites a user's command. Rows without a built-in per-test format read the console summary.
- agent-decided: one-file attribution — node, deno, jest, vitest, mocha, rspec refuse any test from another file; bun counts only when its summary says `across 1 file`; unittest, cargo test, nextest and phpunit are held to one file by their single module, test target or file positional; minitest and unittest run only what the file loads (residual: tests defined in a helper it requires, or a TestCase it imports, are counted). A node file-level case (name equals the base name, no subtests) is not a test; go and deno count only leaf tests, so a parent whose subtests or steps were all skipped is not a test.
- agent-decided: `passed` returns None for output it cannot read, routing to REQ-4 instead of refusing; a readable zero refuses.
- agent-decided: cargo — `<n>` resolves through Cargo.toml `[[test]]` `path`, defaulting to `tests/<n>.rs`; nextest is refused when `--no-tests` is anything other than `fail`. Suite membership of a graduated Rust probe uses the same resolution: a declared `[[test]]` path is collected even with `autotests = false`.
- agent-decided: confirmation is `confirmation: {reviewer, reviewed_sha, quote}` on the adversarial input item. `reviewed_sha` binds it to content (a fix round's new content invalidates it); the quote must match whole lines of this finalize run's output, which binds it to this execution. Quote and line match are checked in finalize-review only; duration values (a number with a time unit, a clock form, `time="..."`, `duration_ms`) are masked on both sides before comparing, because reviewers quote a run made before finalize-review re-runs the probe; counts stay exact. A quote that misses on unchanged content is re-confirmed, like a missing confirmation, not sent back to Build.
- agent-decided: attestation executions gain optional `evidence: "parsed"` with `passed: <n>`, or `evidence: "reviewer"` with `confirmation: {reviewer, reviewed_sha, content_digest, quote}` (finalize records the digest it verified, so validation compares digests and never resolves a sha a rebase may have dropped); pytest/shell executions carry no `evidence`. The manifest grammar becomes `[{kind, command, artifact, result, command_digest, evidence?, passed?, confirmation?}]`; the schema stays `loom-attestation/v2` because its key check is top-level.
- agent-decided: the validator does not re-run programs and stores no output. It recomputes: `claims`/`accepts` from the argv (a claimed-but-not-accepted argv is refused); for a claimed argv, `evidence` is `parsed` with `passed >= 1` or `reviewer`; for an unclaimed argv, `evidence` is `reviewer`; for `reviewer`, the confirmation's reviewer is among the attestation's verdict reviewers and the confirmation's recorded `content_digest` equals the attested content digest.
- agent-decided: closing-review runs each non-pytest/shell probe once at HEAD before dispatching the round's reviewers, writing outputs to a temporary directory outside the repository, and hands reviewers those paths; the reviewer Output schema in `agents/reviewer.md` gains `probe_confirmations: [{artifact, reviewed_sha, quote}]`, and the outside-reviewer YAML check accepts it. Reviewers judge the handed output and do not run probes.

## Alternatives considered
- Reviewer confirmation for every new runner — smaller, but the user chose industry-style result parsing after seeing both.
- Command-shape allowlist only — cannot show tests ran (`node --test /dev/null`, `pytest a b -k other`, nextest `--no-tests=warn`).
- Injecting reporter flags at finalize — rewrites the user's command and can conflict with their config.
- Requiring JUnit XML everywhere — jest, rspec and minitest need extra plugins and several dialects carry no file path.
- Reviewer confirmation for undeterminable suite membership — confirming tests ran does not show the probe is in the permanent suite; kept as today's refusal.

## Current state evidence
- Forward: `loom-code/scripts/loom_checker/probes.py:command_executes_artifact`; this branch already adds shape-only Go/Node/Rust rules (e989f12d, 3636cd3b, b1f2d388) that this spec replaces
- Reverse: `loom-code/scripts/loom_checker/command_handlers/finalize.py:_finalize`, `loom-code/scripts/loom_checker/attestation.py:validate_attestation`, `loom-code/scripts/loom_checker/reviewers.py:outside_verdict_failure`
- Error: `finalize.adversarial` "command must execute the artifact directly"; bun 1.4.3 runs `bun test a/p.test.ts` as a substring filter over two files
- Data: `loom-code/contract/manifest.yaml` attestation `executions` grammar; `loom-code/skills/closing-review/references/adversarial.md` Recording examples
- Boundary: `loom-code/skills/closing-review/SKILL.md` returns every finalize failure to Build for a new round

## UI flows
N/A
