# Accept adversarial probes from any language and test framework — acceptance test evidence

Tried on 2026-10-17, in a clean copy of the project at 0e4fb975
(`git worktree add --detach <scratchpad>/clean 0e4fb975`).

## Setup

- The README installs loom from the GitHub marketplace, which serves the
  released 3.40.0, not this branch. Installing this branch as a plugin would
  have changed the user's own plugin configuration, so the checker was run
  the way the stations run it: `python3 loom-code/scripts/loom_checker.py`
  from the clean copy.
- `python3 loom-code/scripts/loom_checker.py --list-rules` exit 0; the clean
  copy's `loom-code/plugin.json` reads `3.41.0`.
- Toolchains: go 1.27.2, node 26.11.1, deno 2.9.7, bun 1.4.3, Python 3.12.11
  (unittest, pytest 9.1.1), ruby 2.6.10 (minitest 5.11.3), PHP 8.5.11,
  cargo 1.99.1, cargo-nextest 0.9.148, Apache Maven 3.10.0. Installed into
  temporary directories only: jest 30.5.2, vitest 5.0.5, mocha 12.0.3 (npm,
  inside each sample repo, `node_modules/` ignored), rspec 3.13.6 (gem, a
  temporary `GEM_HOME`), phpunit 13.4.3 (composer.phar downloaded to a
  temporary directory, `vendor/` ignored), Maven dependencies
  (`-Dmaven.repo.local=<temporary>/m2`).
- Every sample repo lives in the session scratchpad, outside the worktree.
  Each is built by a driver script (`scratchpad/at/driver.py`): `main` holds
  a README and `docs/loom/KICKOFF-DEFAULTS.md` with a `package-tests:` line;
  branch `feature` adds the code under test and the probe, with a
  `concern:` line. The driver writes the review input that closing-review
  hands to `finalize-review` (two PASS verdicts, reviewers `r1` and `r2`,
  plus the adversarial item), runs
  `python3 <clean>/loom-code/scripts/loom_checker.py finalize-review 2026-10-17-sample --input <file>`
  in the sample repo, commits the written attestation, and asks the
  checker's own `verification_status(repo, change, base="main")` — the
  status that ship's PR floor, publish and land use — whether it is
  `valid`.
- All commands ran with `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID`.
- Change id inside every sample: `2026-10-17-sample`; probe store
  `docs/loom/2026-10-17-sample/evidence/probes/` (written `<P>` below).

## 1. 在一個乾淨的 Go 範例 repo 裡，一支 Go 寫的找漏洞測試用 `go test` 執行並記錄後，不需要 reviewer 確認，`finalize-review` 就產生審查證明，而且該證明通過 checker 的驗證。

- How I tried it: Go module `example.com/sample` with `calc.Div`; probe
  `<P>attack_test.go` (package `probes`, imports `calc`, one test
  `TestDivByZeroRefused`); package-tests `go test ./...`. Adversarial item
  `{"command": "go test -json <P>attack_test.go", "artifact": "<P>attack_test.go"}`,
  no confirmation.
- What came back:
  ```
  finalize exit: 0
  wrote docs/loom/2026-10-17-sample/attestation.json for 254d2a8389b310d64c58ea5ae0963b948324580a
  adversarial execution: {"kind": "adversarial", "command": "go test -json docs/loom/2026-10-17-sample/evidence/probes/attack_test.go", ..., "result": "pass", "evidence": "parsed", "passed": 1}
  validator (verification_status at HEAD): valid
  ```
- Evidence: captured output above; the attestation records
  `evidence: parsed, passed: 1` and carries no confirmation.

## 2. 同樣的結果，對下列每個組合在對應的範例 repo 各成立一次：Python unittest；JavaScript／TypeScript 的 Node 內建測試、vitest、jest、mocha、Bun、Deno；Rust 的 cargo test 與 cargo nextest；Ruby 的 rspec 與 minitest；PHP 的 phpunit。

- How I tried it: one sample repo per combination, each probe a single
  passing test of a small `valid(name)` function, no confirmation supplied.
  Commands, in the accepted forms from the closing-review Recording table:

  | Combination | Command recorded | finalize | attestation | validator |
  |---|---|---|---|---|
  | unittest | `python3 -m unittest -v <P>test_attack.py` | exit 0 | parsed, passed 1 | valid |
  | node | `node --test --test-reporter=junit <P>attack.test.js` | exit 0 | parsed, passed 1 | valid |
  | deno | `deno test --reporter=junit <P>attack_test.ts` | exit 0 | parsed, passed 1 | valid |
  | bun | `bun test ./<P>attack.test.ts` | exit 0 | parsed, passed 1 | valid |
  | jest | `npx jest --json --runTestsByPath <P>attack.test.js` | exit 0 | parsed, passed 1 | valid |
  | vitest | `npx vitest run --reporter=json --outputFile=/dev/stdout <P>attack.test.js` | exit 0 | parsed, passed 1 | valid |
  | mocha | `npx mocha --reporter json <P>attack.test.js` | exit 0 | parsed, passed 1 | valid |
  | cargo test | `cargo test --test attack` (artifact `tests/attack.rs`, package-tests `cargo test`) | exit 0 | parsed, passed 1 | valid |
  | nextest | `cargo nextest run --test attack` (artifact `tests/attack.rs`, package-tests `cargo nextest run`) | exit 0 | parsed, passed 1 | valid |
  | rspec | `rspec --format json <P>attack_spec.rb` | exit 0 | parsed, passed 1 | valid |
  | minitest | `ruby -Ilib <P>attack_test.rb` | exit 0 | parsed, passed 1 | valid |
  | phpunit | `vendor/bin/phpunit <P>AttackTest.php` | exit 0 | parsed, passed 1 | valid |

- What came back: every row printed `wrote docs/loom/2026-10-17-sample/attestation.json`,
  an adversarial execution with `"evidence": "parsed", "passed": 1`, and
  `validator (verification_status at HEAD): valid`.
- Two first attempts failed for my fixture, not the change: mocha's
  package-tests `npx mocha` found no `test/` folder, and phpunit's
  `vendor/bin/phpunit` without a folder printed its help — both were
  `finalize.package-tests` blocks; after pointing package-tests at `docs`
  both passed as above.
- Evidence: captured driver output per row (table above).

## 3. 對清單上的組合，下列情況被拒收：指令雖然寫了測試檔路徑、但不會只執行它（例如把路徑當成其他選項的值、用不跑測試的子指令、同時跑其他測試檔）；執行成功但該測試檔沒有任何測試真的通過（零支，或全部被跳過）。

- How I tried it: each scenario is a copy of a passing sample from line 2
  with its attestation removed, the edit below committed, then
  `finalize-review` with no confirmation (`scratchpad/at/neg.py`).

  | Scenario | Command | Result |
  |---|---|---|
  | path as an option's value | `go test -json -run <P>attack_test.go ./calc` | refused: "is a go command but not in its accepted form" |
  | other test file too | `go test -json <P>attack_test.go <P>other_test.go` | refused: not in accepted form |
  | other test file too | `npx jest --json --runTestsByPath <P>attack.test.js <P>other.test.js` | refused: not in accepted form |
  | other test file too | `npx mocha --reporter json <P>attack.test.js <P>other.test.js` | refused: not in accepted form |
  | bun substring filter (no `./`, second file `attack2.test.ts` present) | `bun test <P>attack.test.ts` | refused: not in accepted form |
  | no machine-readable output | `node --test <P>attack.test.js` | refused: not in accepted form |
  | non-running subcommand of a claimed runner | `npx vitest list --reporter=json --outputFile=/dev/stdout <P>attack.test.js` | refused: not in accepted form |
  | `--no-tests` not `fail` | `cargo nextest run --no-tests=warn --test attack` | refused: not in accepted form |
  | all skipped | go `t.Skip` | refused: "exited 0, but its go output shows no passing, non-skipped test ... a reviewer confirmation cannot stand in for it" |
  | empty file (only the concern line) | node | refused: no passing, non-skipped test |
  | all skipped | node `test.skip` | refused: no passing, non-skipped test |
  | all skipped | jest `test.skip` | refused: no passing, non-skipped test |
  | all skipped | unittest `self.skipTest` | refused: no passing, non-skipped test |
  | all pending | rspec `xit` | refused: no passing, non-skipped test |
  | all skipped | minitest `skip` | refused: no passing, non-skipped test (first run exited 1 only because my temporary `GEM_PATH` hid minitest; re-run without it shows the parse refusal) |
  | all skipped | phpunit `markTestSkipped` | refused: no passing, non-skipped test |
  | all ignored | cargo `#[ignore]` | refused: no passing, non-skipped test |
  | non-running subcommand | `go vet <P>attack_test.go` | not refused outright: "no listed runner claims it ... needs a reviewer confirmation" |
  | non-running subcommand | `deno check <P>attack_test.ts` | not refused outright: needs a reviewer confirmation |
  | non-running subcommand | `cargo build --test attack` | not refused outright: needs a reviewer confirmation |

- Follow-up on the last three: a non-test subcommand of go, deno, cargo or
  bun is claimed by no row, so it goes to the reviewer-confirmation path
  instead of being refused. `go vet`, `deno check` (non-TTY) and
  `cargo build` printed no line naming the file, so no confirmation could
  quote one. `bun build` does print it:
  ```
  $ bun build --target=bun ./<P>attack.test.ts
  // @bun
  // docs/loom/2026-10-17-sample/evidence/probes/attack.test.ts
  import { test, expect } from "bun:test";
  ...
  ```
  Without a confirmation: `BLOCK finalize.adversarial: ... exited 0, but no listed runner claims it ... needs a reviewer confirmation`.
  With `confirmation: {reviewer: r1, reviewed_sha: <HEAD>, quote: "// docs/loom/2026-10-17-sample/evidence/probes/attack.test.ts"}`:
  ```
  finalize exit: 0
  adversarial execution: {..., "command": "bun build --target=bun ./docs/loom/2026-10-17-sample/evidence/probes/attack.test.ts", "result": "pass", "evidence": "reviewer", "confirmation": {"reviewer": "r1", ..., "quote": "// docs/loom/2026-10-17-sample/evidence/probes/attack.test.ts"}}
  validator (verification_status at HEAD): valid
  ```
  A bundler run that executed no test was attested on one reviewer's
  word. The reviewer contract (`loom-code/agents/reviewer.md:146-151`)
  tells reviewers to confirm only output that shows a test ran and passed,
  so this needs a reviewer mistake; the tool itself does not refuse it.
- Evidence: `scratchpad/at/neg-output.txt` captured above, trimmed to the
  BLOCK line per scenario.

## 4. 清單外的組合（例如 Java 的 Maven），以及清單上但結果讀不懂的執行，只有在 reviewer 確認後才產生審查證明，證明裡看得出是哪個 reviewer、依據哪一段輸出確認的；沒有確認，或確認不屬於這次執行（例如沿用別的執行或舊內容的確認）就被拒收。

- How I tried it (unlisted runner, real Maven): JUnit 5 project whose test
  source directory is the probe store, probe `<P>AttackTest.java`; command
  `mvn -B -Dmaven.repo.local=<temp>/m2 test -Dtest=AttackTest`.

  | Scenario | Confirmation | Result |
  |---|---|---|
  | none | — | refused: "no listed runner claims it ... needs a reviewer confirmation", with the output tail including `[INFO] Tests run: 1, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.014 s -- in AttackTest` |
  | pass line from the earlier run, same content | r1, HEAD, the `Tests run ... 0.014 s` line | first try: attested (this run also printed 0.014 s), validator `valid` |
  | pass line from another run | r1, HEAD, the `Tests run ... 0.016 s` line | refused: "the confirmation's quote is not one or more whole, non-blank lines of this run's output" (this run printed 0.015 s) |
  | reviewer who gave no verdict | r3 | refused: "the confirmation's reviewer 'r3' gave no verdict this round" |
  | part of a line | `Tests run: 1, Failures: 0` | refused: quote not whole lines |
  | old content (after a fix commit changed `Sample.java`) | r1, the pre-fix sha, `[INFO] Running AttackTest` | refused: "the confirmation's reviewed_sha 48c1e00… does not have HEAD's functional content, so it confirms another run" |
  | current content | r1, HEAD, `[INFO] Running AttackTest` | attested: `"evidence": "reviewer", "confirmation": {"reviewer": "r1", "reviewed_sha": "75e095de…", "content_digest": "7c85f92c…", "quote": "[INFO] Running AttackTest"}`; validator `valid` |
  | hand-edited attestation, confirming reviewer swapped to r9 | — | validator: `stale (adversarial confirmation reviewer is not one of the verdict reviewers)` |

- Timing in the quoted line: five back-to-back runs of the same Maven
  command printed `Time elapsed:` 0.014, 0.013, 0.014, 0.013, 0.016 s. The
  closing-review station runs each such probe once before reviewers and
  `finalize-review` runs it again, and the quote must match the second run
  exactly. A reviewer following its contract quotes the line that shows a
  test passed — the `Tests run: ... Time elapsed` line — which then matches
  only when the timing repeats. A mismatch is a refusal other than a
  missing confirmation, which the closing-review station sends back to
  Build as a new round (`loom-code/skills/closing-review/SKILL.md`, the
  paragraph beginning "When `finalize-review` refuses only for a missing
  confirmation"). Node's junit `<testcase ... time="0.000306" ...>` is
  the only node line naming the file, with the same property.
- How I tried it (listed runner, unreadable output): five real attempts
  to make a listed runner's accepted-form output unreadable all still
  parsed (`evidence: parsed, passed: 1`): mocha with a `console.log` line in
  the JSON stream; rspec with `.rspec` `--format documentation`; rspec with
  a helper adding the `progress` formatter (progress text before the
  JSON); phpunit with `phpunit.xml` `testdox="true"`; node with
  `NODE_OPTIONS` adding a TAP reporter to stdout (TAP interleaved with
  junit XML). So that half was settled by the change's own tests: in the
  clean copy,
  `uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest -q -p no:cacheprovider loom-code/tests/test_probe_language_commands.py loom-code/tests/test_probe_confirmation_finalize.py loom-code/tests/test_probe_language_suite_collection.py loom-code/tests/test_probe_bun_absolute_outside_repo.py loom-code/tests/test_probe_deno_ignored_steps.py loom-code/tests/test_loom_attestation.py loom-code/tests/test_adversarial_pytest_option_order.py loom-code/tests/test_selection_finalize.py`
  → `188 passed in 80.27s`. These include
  `test_unreadable_output_needs_confirmation` (13 runners, each output
  read as "cannot read") and
  `test_unlisted_maven_with_confirmation_attested` /
  `test_other_content_or_partial_line_quote_refused` (the same
  confirmation path the Maven runs used).
- Evidence: captured driver output per scenario above
  (`scratchpad/at/maven-*.txt`).

## 5. 現有用 Python（pytest）或 shell 寫的找漏洞測試照舊被接受，repo 的完整 package suite 通過。

- How I tried it: Python sample with `<P>test_attack_pytest.py` and
  `<P>attack.sh`; package-tests `python3 -m pytest -q docs`.
  - `python3 -c pass <P>test_attack_pytest.py` (does not run the file) →
    `BLOCK finalize.adversarial: command must execute the artifact directly`.
  - `python3 -m pytest <P>test_attack_pytest.py -q` and `bash <P>attack.sh` →
    finalize exit 0; both executions `{"kind", "command", "artifact", "result": "pass"}`
    with no `evidence` field; validator `valid`.
  - The same sample finalized by the installed 3.40.0 checker
    (`~/.claude/plugins/cache/loom/loom-code/3.40.0/scripts/loom_checker.py finalize-review ...`)
    and committed: this branch's validator reports `valid` for that older
    attestation.
- Package suite: not run here. `finalize-review` runs the suite command
  `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`
  before accepting the change and refuses the attestation when it fails.
  The criterion's own tests (the 188 listed under line 4, which include
  `test_pytest_shell_attestation_unchanged`, `test_python_noop_still_refused`,
  `test_loom_attestation.py`, `test_adversarial_pytest_option_order.py`)
  passed in the clean copy.
- Evidence: captured driver output above.
