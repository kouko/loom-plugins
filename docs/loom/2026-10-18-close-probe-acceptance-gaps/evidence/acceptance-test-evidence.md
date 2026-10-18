# Close the remaining probe-acceptance gaps — acceptance test evidence

Tried on 2026-10-18, in a clean copy of the project at c1cb34a4
(`git worktree add --detach <scratch>/clean c1cb34a4`).

## Setup

- The checker ships as plain Python inside the plugin; no install step.
  `python3 loom-code/scripts/loom_checker.py --list-rules` in the clean copy
  printed the rule list (exit 0).
- Tools: python 3 with pytest 9.1.1, go 1.27.2, bun 1.4.3, cargo 1.99.1,
  node v26.11.1, pnpm 12.11.2, npx (jest 30.5.2 fetched / installed per repo).
- Method: a scratch driver (outside the repo) builds one fresh git example
  repo per scenario: `main` with `src.py` and
  `docs/loom/KICKOFF-DEFAULTS.md` declaring `package-tests`, then a `feature`
  branch adding `feature.py` (production code, so the adversarial step is
  required) plus the probe files. It writes a review input with two passing
  example verdicts (`r1`, `r2`) and the adversarial item under test, runs the
  clean copy's real `loom_checker.py finalize-review 2026-10-18-example
  --input <json>` with `FORCE_COLOR` and `CLAUDE_CODE_SESSION_ID` unset, and
  when an attestation is written, re-checks it with
  `loom_checker.attestation.validate_attestation` (the validator). Probe store
  = `docs/loom/2026-10-18-example/evidence/probes/` (`<S>` below).
- Every scenario's outcome matched the expected accept/refuse; one
  out-of-scope mismatch with cargo is recorded under 4/5.

## 1. pytest probe: only its own file; deselected or zero passed is refused; suite filters stay allowed

How I tried it: probe `<S>/test_attack.py` with two passing tests
(`test_attack`, `test_kept`), each scenario in its own example repo.

| Scenario | Command recorded | Result |
|---|---|---|
| no filter, sole file | `python3 -m pytest <S>/test_attack.py` | exit 0, attested, validator: valid |
| `-k` in command | `... <S>/test_attack.py -k test_kept` | exit 1, refused; pytest summary `1 passed, 1 deselected` |
| `-m` in command | `... <S>/test_attack.py -m slow` | exit 1, refused; `2 deselected` |
| `--deselect` in command | `... --deselect <S>/test_attack.py::test_attack` | exit 1, refused; `1 passed, 1 deselected` |
| second file listed | `... <S>/test_attack.py test_other.py` | `BLOCK finalize.adversarial: command must execute the artifact directly` |
| config file filter | `pytest.ini` `addopts = -k test_kept`, plain command | exit 1, refused; `1 passed, 1 deselected` |
| plugin filter | `conftest.py` hook `pytest_collection_modifyitems` calling `pytest_deselected` on `test_attack` | exit 1, refused; `1 passed, 1 deselected` |
| zero passed | probe whose only test is `@pytest.mark.skip` | exit 1, refused; `1 skipped` |
| suite command with its own filter | package-tests `python3 -m pytest -m "not slow" tests`, graduated `tests/test_graduated_probe.py`, probe command `python3 -m pytest tests/test_graduated_probe.py` | exit 0, attested, validator: valid |

Widened scope (bare `python3` run):

| Scenario | Command | Result |
|---|---|---|
| file with top-level test functions | `python3 <S>/test_attack.py` | `BLOCK finalize.adversarial: ... defines pytest tests that a bare python run never calls; record python -m pytest ...` |
| file with a `Test` class | `python3 <S>/test_attack.py` (class `TestThing`) | same refusal |
| plain script, no tests | `python3 <S>/probe_script.py` | exit 0, attested, validator: valid |

Criterion tests also run (subset, not the suite):
`loom-code/tests/test_probe_pytest_summary.py`,
`test_probe_pytest_config_added_file.py`,
`test_probe_direct_python_pytest_file.py` — included in the 160-passed
subset run listed under 6.

## 2. Artifact path that escapes the store is refused by finalize-review and the validator

| Scenario | Artifact | Result |
|---|---|---|
| in store | `<S>/probe_in.py` | exit 0, attested, validator: valid |
| `..` escape | `<S>/../../../../../outside_probe.py` | `BLOCK finalize.adversarial: adversarial artifact must be a plain repository path (no ./, .. or //)` |
| `./` + `..` | `./<S>/../../../../../outside_probe.py` | same refusal |
| `//` form | `<S>//probe_in.py` | same refusal |
| plain path outside store, not in suite | `outside_probe.py` | `BLOCK finalize.adversarial: adversarial artifact must be committed under <S> or be a program the package suite already runs` |
| validator, attestation edited to `..` path (digest recomputed) | — | `('push.attestation', 'adversarial artifact must be a plain repository path (no ./, .. or //)')` |
| validator, attestation edited to `./`+`..` path | — | same |
| symlink in store pointing outside (committed as mode 120000), target name carrying `concern:` | `<S>/link_probe.py` | refused: `BLOCK adversarial.proportionate: ... carries no non-empty concern: line` |

Note: the symlink case is refused, but by the concern-line rule, not by a
path rule naming the escape.

## 3. `env go test -json`, `npx --yes jest`, `pnpm jest` read without reviewer confirmation; zero passed refused

Real tools, example repos with no confirmation in the review input.

| Command | Result |
|---|---|
| `go test -json <S>/add_test.go` (baseline) | attested, `evidence: parsed, passed: 1`, valid |
| `env go test -json <S>/add_test.go` | attested, `evidence: parsed, passed: 1`, valid |
| `env GOTRACEBACK=all CGO_ENABLED=0 go test -json <S>/add_test.go` | attested, `evidence: parsed, passed: 1`, valid |
| `env go test -json ...` on a `t.Skip` probe | refused: `... its go output shows no passing, non-skipped test ...` |
| `env GOFLAGS=-count=1 go test -json ...` | refused: not in accepted form |
| `env -i HOME=... PATH=... go test -json ...` | exited 0, refused pending reviewer confirmation (`no listed runner claims it`) |
| `npx --yes jest --json --runTestsByPath <S>/attack.test.js` | attested, `evidence: parsed, passed: 1`, valid |
| `pnpm jest --json --runTestsByPath ...` | attested, `evidence: parsed, passed: 1`, valid |
| `npx jest ...`, `pnpm exec jest ...` (baseline forms) | attested, parsed, valid |
| each jest form above on a `test.skip` probe | refused: `... its jest output shows no passing, non-skipped test ...` |
| `pnpm test <S>/attack.test.js` (script name) | refused pending reviewer confirmation |

Setup note: `pnpm install` (jest 30.5.2) exited 1 because it ignored the
build scripts of `@parcel/watcher` and `unrs-resolver`; jest itself ran.
`pnpm-lock.yaml` was committed so the tree was clean.

## 4. Rust: default-feature targets and `tests/<dir>/main.rs` count as collected; targets cargo does not run stay refused

Example crate, package-tests `cargo test`, `.gitignore` = `target/`,
`Cargo.lock`. `[features] default = ["x"]`, `x`, `y`, `z = ["y"]`.

Real `cargo test` ran: `src/lib.rs`, `tests/declared/main.rs`,
`tests/deffeat.rs`, `tests/dirtest/main.rs`, `tests/plain.rs`.

| Target | cargo runs it | Probe command | finalize-review |
|---|---|---|---|
| `tests/plain.rs` | yes | `cargo test --test plain` | attested, parsed, valid |
| `deffeat`, `required-features = ["x"]` (in default) | yes | `cargo test --test deffeat` | attested, parsed, valid |
| `tests/dirtest/main.rs` (auto-discovered) | yes | `cargo test --test dirtest` | attested, parsed, valid |
| `[[test]] name = "declared"`, no path → `tests/declared/main.rs` | yes | `cargo test --test declared` | attested, parsed, valid |
| `required-features = ["y"]`, y not enabled | no | `cargo test --test transitive` | refused: not a program the package suite runs |
| `test = false` | no | `cargo test --test off` | refused |

Second crate: `default = ["x", "z"]`, `z = ["y"]`. Real `cargo test` ran
`deffeat` and `transitive`.

| Target | cargo runs it | finalize-review |
|---|---|---|
| `required-features = ["x", "z"]` (both in default) | yes | attested, valid |
| `required-features = ["x", "w"]` (w off) | no | refused |
| `required-features = ["y"]`, y on only through `z` | yes | refused — intent Out of scope (indirect enabling); safe direction |

## 5. Real-tool re-run: Bun `./` form attested, other forms refused; Rust matches cargo

Bun 1.4.3, probe `<S>/p.test.ts` plus a second `<S>/other.test.ts`.

| Command | Result |
|---|---|
| `bun test ./<S>/p.test.ts` | attested, `evidence: parsed, passed: 1`, validator: valid |
| `env bun test ./<S>/p.test.ts` | attested, parsed, valid |
| `bun test <S>/p.test.ts` (no `./`) | refused: bun command not in accepted form |
| `bun test /abs/.../p.test.ts` | refused: not in accepted form |
| `bun test ./<S>/p.test.ts ./<S>/other.test.ts` | refused |
| `bun ./<S>/p.test.ts` | refused |

Rust: see 4 — every accept/refuse matched what real `cargo test` ran,
except the out-of-scope indirect-feature target (refused, cargo runs it).

## 6. Full package suite passes

- Command, in the clean copy at c1cb34a4:
  `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`
- Exit 0, 2m42s; 14 pytest summaries totalling 3501 passed, none failed;
  shell checks all PASS.
- Criterion subset: `python -m pytest -q` over the seven
  `loom-code/tests/test_probe_*` files this change touched → 160 passed.
- `finalize-review` runs the same suite again before attesting and refuses
  on failure.
