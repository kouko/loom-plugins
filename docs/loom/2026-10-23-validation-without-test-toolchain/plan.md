# Validate attestations without the test toolchain — plan
intent: 2026-10-23-validation-without-test-toolchain@7ff16b7e
charter: 1.1

## Current State Evidence
- Forward: `loom-code/scripts/loom_checker/probe_results.py:_go_package_test_name` runs `go list -json <package>` and `git show HEAD:<artifact>`; any failure returns None, so `_go_accepts` returns False.
- Reverse: `attestation.py:validate_attestation(repo, head_sha, ...)` calls `adversarial_route(command, artifact, repo)` with no revision; `finalize.py:303` calls the same route at HEAD; the route's docstring promises validation "without executing the recorded programs".
- Error: with `GOCACHE` unwritable or `go` off PATH, a finalize-accepted package-form command becomes `not-accepted`; publish prints `stale` (reading-list-summarize-scraper #19, #20; reproduced 2026-10-23).
- Data: `probes.py:cargo_test_targets(repo)` reads the working-tree `Cargo.toml` and globs `tests/` on disk; `probe_results.py:_cargo_test_path` uses it for `cargo test`/`nextest` acceptance during validation.
- Boundary: `tests/test_probe_language_commands.py:568-707` pins the Go package form, including route refusal of a `//go:build never` artifact (line 615) and a duplicate name (line 627).

## Task DAG

**W1-01 Decide Go and Cargo acceptance from the validated commit only**  after: none  acceptance: 1,2,3,4
- Files: `loom-code/scripts/loom_checker/probe_results.py`, `loom-code/scripts/loom_checker/attestation.py`, `loom-code/scripts/loom_checker/probes.py`, `loom-code/tests/test_probe_language_commands.py`, `loom-code/tests/test_probe_cargo_declared_dir_main.py`
- Test: A1 positive: go-package-probe-validates-without-go-on-path-or-writable-gocache; negative: undeclared-test-refused-without-go. A2 positive: go-artifact-and-cargo-manifest-read-at-validated-sha-not-worktree; negative: declaration-or-target-only-in-worktree-refused. A3 positive: sibling-file-duplicate-name-refused; boundary: duplicate-in-build-excluded-file-refused. A4 positive: single-file-go-cargo-nextest-still-accepted; negative: build-excluded-artifact-run-records-zero-passes-refused.
- Risk: agent-decided — `revision="HEAD"` keyword on route, Row.accepts, go/cargo only; validate passes head_sha; package name computed once; no `go` subprocess; narrows line-615 route refusal into passed>=1.

**W2-01 Release loom-code 3.48.1**  after: W1-01  acceptance: 4
- Files: `loom-code/.claude-plugin/plugin.json`, `loom-code/.codex-plugin/plugin.json`, `loom-code/plugin.json`, `loom-code/package.json`, `loom-code/CHANGELOG.md`, `loom-code/README*.md`, `README.md`, `loom-code/tests/test_write_plan_station_text.py`
- Test: A4 positive: release-metadata-synchronized; negative: stale-version-pin-refused.
- Risk: agent-decided — patch bump (bug fix, no field or rule id); edit SSOT then `scripts/sync_codex_manifests.py --all`; CHANGELOG entry and CURRENT_VERSION pin are deliverables.

## Simplicity check
- pass the revision only from validation, leaving finalize untouched — taken
- fold the Cargo task into W1-01 — taken
- compute the Go package test name once in the route — taken

## Questions asked
① — what — 你要的是發布或合併時重新檢查審查證明，結果只看被檢查那個版本裡已 commit 的檔案和證明本身……這樣對嗎？（答：對）

## Risks
1. user-decided — accept stricter Go duplicate check: a same-name test in a build-excluded file of the same directory now makes the package form stale; workaround is the single-file form.
2. Build-tag selection is no longer checked at route level; an excluded artifact is refused because its fresh `-count=1` run records zero passes of the named test, which finalize already rejects.
3. Validation must read the validated revision, not HEAD; finalize keeps the HEAD default on a committed tree. The keyword touches the Row.accepts type, `_env_accepts` and `_row`, shared by all 13 rows; only go and cargo read it.
