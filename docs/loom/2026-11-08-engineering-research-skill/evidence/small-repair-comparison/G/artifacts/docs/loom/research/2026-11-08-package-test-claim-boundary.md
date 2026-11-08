---
title: "Claim boundary for sample receipt exit_code=0 and the package-test-roots record"
type: loom-research
status: concluded
created: 2026-11-08
updated: 2026-11-08
tags:
  - loom/research
---

# Claim boundary for sample receipt exit_code=0 and the package-test-roots record

## Question and scope

Can the existing [sample receipt](../../../sample-receipt.json) (`exit_code: 0`) and the existing record [package test roots](2026-11-08-package-test-roots.md) support the claim "the whole package tests/CI pass for this snapshot and the source is traceable"? Scope: the temporary local fixture only (minimal source snapshot in `src/`, [provenance](../../../provenance.json)). No tests, remote queries, publishing or acceptance were performed or are implied. The existing record was not edited; this is a separate question from its test-root/`local/` question.

## Method and rationale

Source and artifact inspection (receipt, existing record, provenance, runner source, test definitions) plus the harness-supplied [fixture observations](../../../fixture-observations.json) (git queries and SHA-256 values taken during fixture preparation, not by me). Sufficient to bound a claim; no execution needed or permitted. I had only file read/write tools, so I recomputed no hash and ran no git command.

## Findings

Observed / source-supported:

- The receipt describes an authoring run of a `codex exec` agent (id `B02`, requested model, `elapsed_seconds` 42.6). Its `exit_code: 0` is that agent process's exit status. Its only recorded project change is `added_project_files: [docs/loom/research/2026-11-08-package-test-roots.md]`, with `source_unchanged: true`. It contains no pytest/runner command, test counts, or CI job. It says nothing about any test passing.
- The existing record states "no tests or runner commands were executed" and "source-supported conclusion, without runtime validation", and that CI and deployed versions are outside its evidence. It answers only: which roots are in `TEST_ROOTS` and that the `--loom-family` preset skips `local/`.
- The runner's `--loom-family` mode would run several groups (code, design, workflow-python/shell/mermaid, including `npm ci` and `node`). The snapshot holds 4 files only: no `loom-design/`, `loom-workflow/`, `tests/` other than one test file, no CI config, no `pytest.ini`/conftest. The package suite cannot be represented by this snapshot ([runner](../../../src/scripts/run_package_tests.py), lines 116–150).
- Test definitions in [the test file](../../../src/tests/test_run_package_tests.py) were read, not run; they depend on helpers outside what I verified (e.g. `_seed_repo`, `REPO`).

Hash and provenance (harness observation, not my measurement):

- fixture-observations.json SHA-256 for the four source files equals the `provenance.json` entries (runner `6730a53e…0d54`, test `b7ed3d4e…0da28`, `repo_files.py` `62333168…6399`, `git_exec.py` `9c721b8e…e7c7`). Observed paths carry a `src/` prefix versus provenance paths (e.g. `scripts/run_package_tests.py`); this is a snapshot-layout mapping I infer, not stated in provenance.
- Provenance ties the files to original-repo HEAD `d5a7f0da…` and a locally recorded `origin/main` of the same value; `remote_freshness` is "not checked". The original repository path is outside this fixture and was not read.
- The record's SHA-256 (`c54f2872…1283`) was observed, but provenance has no entry for the record, so there is no independent expected hash for it. [snapshots/original-research.md](../../../snapshots/original-research.md) reads identically to the record by my inspection; I did not hash it.
- Git (observation file): `main` = `4959e62`, `research-fixture` = `00fa764` is an ancestor of `main`; no tags, no remotes; the record is in the temporary fixture's history, not the original project's.
- Links in the existing record (`../../../provenance.json`, `../../../src/scripts/run_package_tests.py`, `../../../src/tests/test_run_package_tests.py`) resolve from `docs/loom/research/` to existing files. Cited line anchors broadly match, with small offsets (e.g. `TEST_ROOTS` is at line 53, the `code` group begins at 124, `_shell_tests` at 88–95); these do not change the conclusions. The record lacks the template's H1 heading (cosmetic).

## Evidence

| Claim | Source kind | Status |
|---|---|---|
| exit_code 0 is an authoring-agent exit status | [receipt](../../../sample-receipt.json) command and fields | source inspection |
| No test or CI result exists | receipt, record, fixture-observations (no test command) | absence in inspected artifacts; not proof tests were never run elsewhere |
| Source files match provenance hashes | [observations](../../../fixture-observations.json) vs [provenance](../../../provenance.json) | harness observation, pre-actor; no post-write hash supplied |
| Runner/test content supports the root/`local/` claim | runner and test file | source inspection; tests not run |

## Decision impact

Can claim (within the fixture, with attribution):

- Four snapshot source files match provenance hashes (per harness observation), and provenance names an original commit, with remote freshness unchecked.
- The record is a retained, source-inspection-based answer on `TEST_ROOTS` and `local/` exclusion in that snapshot, with working relative links.
- The receipt shows one authoring run exited 0 and added that one record.

Cannot claim:

- That the package tests or CI pass: no test was run, no result recorded, and the snapshot is too small for the suite. `exit_code: 0` is not a test result.
- That traceability is complete or verified against the original repository: the original repo, commit `d5a7f0da…`, and remote were not inspected; the fixture git history is temporary; the record has no independent hash.
- Deployment, installation, or release status.

To support the stronger claim you would need an actual recorded run of the intended test command on the full checkout at the named commit (with command, environment, result), plus CI evidence, which I did not obtain.

## Limitations and open questions

- I recomputed no hash and ran no git command; hash and git facts come from the harness observation file, taken before my execution, with no post-write hash for the record.
- Whether the original tests pass at `d5a7f0da…` is unknown.
- The `src/` path mapping and the equivalence of the snapshot copy of the record are inferred from reading.
- Revalidate if the snapshot, provenance, or receipt changes.
