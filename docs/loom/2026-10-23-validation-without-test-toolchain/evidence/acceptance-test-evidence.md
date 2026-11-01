# Validate attestations without the test toolchain — acceptance test evidence

Tried on 2026-10-23, in a clean copy of the project at 9b5304f2 (`git worktree add --detach <scratch>/clean-head 9b5304f2`), compared against the base 91e89a52 (`<scratch>/clean-base`, same method). `<scratch>` is `/private/tmp/claude-501/-Users-kouko--herdr-worktrees-loom-plugins-prove-tool/7893f49e-4950-410f-b99f-10ace61b1682/scratchpad/at`.

## Setup (every run)

- The README's setup is "install the plugin"; the checker needs only `python3` (3.12.11 here, conda env `dbt-redshift`). `python3 <scratch>/clean-head/loom-code/scripts/loom_checker.py --list-rules` printed the rule list from the clean copy — it loads.
- Toolchains on the host: go 1.27.2, cargo 1.99.1, cargo-nextest 0.9.148.
- Two user repositories were built from scratch with shell scripts kept outside them:
  - `<scratch>/go-head` (`mk_go.sh`): module `example.test/godemo`, package `internal/pipeline`; branch `fix/2026-10-23-go-demo` adds a committed intent and `internal/pipeline/adversarial_test.go` (`// concern:` line, `TestAdversarialEmpty`), which calls `stubExtractor` defined in the sibling `extraction_test.go`. `KICKOFF-DEFAULTS.md`: `package-tests: go test ./...`.
  - `<scratch>/rust-head` (`mk_rust.sh`): crate `rdemo`, committed `Cargo.lock`; branch `fix/2026-10-23-rust-demo` adds the intent and `tests/attack.rs`. `package-tests: cargo test`.
- Attestations were produced by the real station command, run in each repo: `python3 <scratch>/clean-head/loom-code/scripts/loom_checker.py finalize-review <change-id> --input <review-input.json>` (two PASS verdicts plus one adversarial item), then committed.
- "Validation" below is `loom_checker.verification.verification_status(repo, change_id, base="main", head=...)`, the status that publish, land, the push hook and CI print (`status.py` wrapper). Publish itself was not run, since it pushes to a remote.
- Fixture slip, mine: the first Rust finalize stopped with `BLOCK finalize.stable-tree: working tree or index changed during functional verification` because the fixture had no committed `Cargo.lock`; after committing one (as a real crate does) finalize passed. Not a defect of the change.
- Refusal cases need an attestation that matches the commit's content but claims something the commit does not support. finalize-review itself refuses to write those, so `forge.py` recomputes `content_digest` (via `loom_checker.digest.functional_content_digest`) and, where named, swaps the adversarial command and its digest. A forge with nothing changed (control, `g0`) stayed `valid`.

## 1. 在找不到 `go`、或 Go 快取資料夾不能寫入的環境，驗證一份以 Go 套件寫法產生的有效審查證明，結果是有效，不是過期。

- How I tried it:
  - `go-head`: `GOCACHE=<scratch>/gocache python3 .../clean-head/loom-code/scripts/loom_checker.py finalize-review 2026-10-23-go-demo --input go-review-input.json` with adversarial command `go test -json -count=1 -run '^TestAdversarialEmpty$' ./internal/pipeline`.
  - Contrast: `go test internal/pipeline/adversarial_test.go` (single-file form) does not build.
  - Validated three ways with each checker: normal; `env PATH=<scratch>/nogo-bin:/usr/bin:/bin` (only `git` linked in; `shutil.which("go")` printed `None`); `GOCACHE=<scratch>/ro-cache/sub` under a `chmod 555` directory (`touch` there: `Permission denied`).
  - Also validated an attestation the base checker's finalize wrote (`b1`).
- What came back:
  ```
  wrote docs/loom/2026-10-23-go-demo/attestation.json for d8cf9c175ade37465330b7dc8d327d15272a9e8e
  adversarial execution: "evidence": "parsed", "passed": 1
  single-file contrast: internal/pipeline/adversarial_test.go:7:5: undefined: stubExtractor

  == checker clean-head (9b5304f2)
  normal:            valid
  go off PATH:       valid
  GOCACHE read-only: valid
  == checker clean-base (91e89a52)
  normal:            valid
  go off PATH:       stale (adversarial command is a go command but not in its accepted form for its artifact)
  GOCACHE read-only: stale (adversarial command is a go command but not in its accepted form for its artifact)

  b1 (attestation written by the base finalize): clean-head no go -> valid; clean-base no go -> stale (...)
  ```
- Evidence: the outputs above. The base reproduces the reported #19/#20 false `stale`; HEAD reports `valid`. Targeted tests (`test_probe_language_commands.py`, among the 173 below) passed.

## 2. 驗證時，Go 測試檔與同資料夾其他測試檔、以及 Rust 的 `Cargo.toml`，讀的都是被驗證那個版本裡的內容；工作目錄當下的內容和該版本不同時，結果不受影響。

- How I tried it (every case run with clean-head and clean-base; Go cases with and without `go`):
  - A2-i `w1`: uncommitted edits — artifact's test renamed to `TestRenamed`, untracked sibling `dup_test.go` declaring `TestAdversarialEmpty`, `KICKOFF-DEFAULTS.md` changed to `go test -race ./...`.
  - A2-i' `w1b`: only the untracked sibling duplicate.
  - A2-ii `w2` (negative): forged attestation names `TestOnlyInWorktree`, which exists only in an uncommitted edit of the artifact.
  - A2-iii `w3`: a later commit renames the test; validate the attested commit (`head=0ea68397`) while the working tree holds the later commit.
  - Rust `rust-head`: uncommitted (a) `autotests = false` plus `tests/attack.rs` deleted; (b) `Cargo.toml` maps target `attack` to `tests/elsewhere.rs`; (c) `Cargo.toml` deleted. Same (b) with the `cargo nextest run --test attack` attestation (`n1`).
  - Rust negative `r2`: committed `Cargo.toml` maps `attack` to `tests/elsewhere.rs`, forged attestation, working-tree `Cargo.toml` restored to the original mapping.
- What came back:
  ```
  A2-i   clean-head (no go / go): valid / valid
         clean-base (no go / go): stale (package-tests execution does not match the declared package command)
  A2-i'  clean-head (go): valid      clean-base (go): stale (adversarial command is a go command but not in its accepted form ...)
  A2-ii  clean-head (no go / go): stale (... not in its accepted form ...)   clean-base: stale (same)
  A2-iii clean-head (no go / go): valid / valid
         clean-base (no go / go): stale (... not in its accepted form ...)
  Rust (a) clean-head: valid   clean-base: valid
  Rust (b) clean-head: valid   clean-base: stale (adversarial command is a cargo test command but not in its accepted form ...)
  Rust (c) clean-head: valid   clean-base: stale (same)
  nextest (b) clean-head: valid   clean-base: stale (adversarial command is a nextest command but not in its accepted form ...)
  Rust r2 (target only in worktree) clean-head: stale (cargo test ... not in its accepted form ...)   clean-base: valid
  ```
- Evidence: the outputs above; `test_adversarial_validate_worktree_declared_command.py` and `test_probe_cargo_declared_dir_main.py` passed in the targeted run. Rust (a) also passed on the base, because a missing target falls back to `tests/<name>.rs`; (b), (c) and r2 show the difference.

## 3. Go 套件寫法下，指定測試不在指定檔案裡、或同資料夾另有測試檔宣告同名測試時，驗證仍不接受。

- How I tried it:
  - Validation (forged attestations, clean-head and clean-base, with and without `go`): `g1` command `-run '^TestExtract$'` (declared in sibling `extraction_test.go`, not the artifact); `g2` committed sibling `duplicate_test.go` in `package pipeline_test` declaring `TestAdversarialEmpty`; `g3` duplicate only in a `//go:build never` sibling.
  - finalize-review (go available, clean-head): `f1` sibling duplicate; `f2` artifact itself `//go:build never`; `f3` command names `TestExtract`.
- What came back:
  ```
  g1 clean-head no go / go: stale (adversarial command is a go command but not in its accepted form for its artifact)  [base: same]
  g2 clean-head no go / go: stale (same)  [base: same]
  g3 clean-head no go / go: stale (same)  [base: no go stale, go valid]
  f1 BLOCK finalize.adversarial: `go test -json -count=1 -run '^TestAdversarialEmpty$' ./internal/pipeline` is a go command but not in its accepted form for internal/pipeline/adversarial_test.go ...
  f2 BLOCK finalize.adversarial: adversarial artifact must be committed under docs/loom/2026-10-23-go-demo/evidence/probes/ or be a program the package suite already runs
  f3 BLOCK finalize.adversarial: `go test -json -count=1 -run '^TestExtract$' ./internal/pipeline` is a go command but not in its accepted form ...
  ```
- Evidence: outputs above; `test_adversarial_go_symlinked_sibling_duplicate.py` (symlinked sibling duplicate) passed in the targeted run. g3 is the stricter rule the plan records as user-decided (Risk 1).

## 4. 現有可被接受的 Go 單檔寫法與 Rust 寫法仍產生有效的審查證明；repo 的完整 package suite 通過。

- How I tried it:
  - Go single-file `s1`: probe `docs/loom/2026-10-23-go-demo/evidence/probes/single_test.go`, finalize with `go test -json -count=1 docs/loom/2026-10-23-go-demo/evidence/probes/single_test.go`.
  - Rust `rust-head` with `cargo test --test attack`; `n1` with `cargo nextest run --test attack`.
  - Targeted tests: `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest -q loom-code/tests/test_probe_language_commands.py loom-code/tests/test_probe_cargo_declared_dir_main.py loom-code/tests/test_adversarial_go_symlinked_sibling_duplicate.py loom-code/tests/test_adversarial_validate_worktree_declared_command.py loom-code/tests/test_loom_attestation.py`.
  - Package suite, once, in the clean copy: `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`.
- What came back:
  ```
  s1: wrote docs/loom/2026-10-23-go-demo/attestation.json for e464b3093eae...; clean-head no go / go: valid / valid; clean-base: valid / valid
  cargo test: wrote .../attestation.json for 13a03f2e...; "evidence": "parsed", "passed": 1; clean-head valid; clean-base valid
  nextest:    wrote .../attestation.json for 13a03f2e...; "evidence": "parsed", "passed": 1; clean-head valid; clean-base valid
  targeted: 173 passed in 33.94s
  package suite: exit=0 in 2:09.52 wall; largest pytest root "2373 passed, 2 skipped in 81.58s", every other section passed (no "failed" line in the log)
  ```
- Evidence: outputs above; full suite log at `<scratch>/suite.log`.

## Data and format

- The attestation the base finalize wrote for `go-head`'s commit and the one the HEAD finalize wrote are byte-identical (`cmp`), and the HEAD checker validates both.
