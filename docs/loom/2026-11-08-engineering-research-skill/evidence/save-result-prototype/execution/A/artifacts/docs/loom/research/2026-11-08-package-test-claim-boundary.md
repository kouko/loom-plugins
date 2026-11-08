---
title: "What may be claimed from sample-receipt.json exit_code=0 and the existing test-roots record"
type: loom-research
status: concluded
created: 2026-11-08
updated: 2026-11-08
tags:
  - loom/research
---

# What may be claimed from sample-receipt.json exit_code=0 and the existing test-roots record

## Question and scope

The user intends to claim that the whole package tests/CI pass for this snapshot and that the source is traceable, based on `exit_code=0` in [sample-receipt.json](../../../sample-receipt.json) and the existing record [package test roots](2026-11-08-package-test-roots.md). Question: how far do the receipt, the record, the source hashes and the links actually support that claim? Scope: the temporary local fixture only. No tests, runner, network or remote checks were run; none were requested.

This is a different question from the earlier record (which asks what `TEST_ROOTS` contains). That record is left unchanged.

## Method and rationale

Inspection of existing artifacts: the receipt, the earlier record, `provenance.json`, `fixture-observations.json` (harness observations), the runner source and test definitions. This fits because the gap is about what each artifact attests, not about new behavior. Nothing was executed by me.

## Findings

1. **The receipt does not attest to package tests or CI.** It describes a `codex exec --ephemeral ... --sandbox workspace-write` invocation (id `B02`, requested model `gpt-6.1-sol`, `timed_out: false`, `exit_code: 0`, 42.6 s). The `exit_code` is the exit status of that external model-executor process. It contains no pytest command, no `run_package_tests.py` invocation, no test counts and no CI job reference. It also records `source_unchanged: true` and `added_project_files: [docs/loom/research/2026-11-08-package-test-roots.md]`, so the one file it says that run added is the research record itself. The receipt is a record of authoring that Markdown file, not of any suite run.
2. **The existing record is a static-inspection result and says so.** Its Method section states that no tests or runner commands were executed, and its Limitations section says CI configuration and deployed versions are outside the evidence. Its conclusion is limited to the `TEST_ROOTS` list and the `tests/local/` exclusion in the `--loom-family` preset.
3. **The runner source itself shows what a passing suite would mean.** The runner returns the first non-zero subprocess code or 0 ([runner](../../../src/scripts/run_package_tests.py), `main`, lines 153–176). The `workflow-mermaid` group would run `npm ci` and node scripts, and CI selects groups with `--only` (docstring lines 10–24, 139–145). This snapshot contains only 4 source files, with no `loom-design/`, `loom-workflow/` or Mermaid tests, so the full suite cannot be reconstructed from it. A "whole package" pass is not even runnable from the snapshot.
4. **Source hashes: consistent, but only for the 4 snapshot files and only as a local comparison.** `fixture-observations.json` (harness observation, not my command) lists SHA256 values for the runner, the test file, `repo_files.py` and `git_exec.py` that equal the `provenance.json` entries by direct reading (runner `6730a53e…0d54`, test file `b7ed3d4e…0da28`, `repo_files.py` `62333168…6399`, `git_exec.py` `9c721b8e…e7c7`). I did not compute any hash myself. The observations file lists a hash for the research record (`c54f2872…1283`) taken before the actor run; there is no post-write hash, and I could not recompute it. Provenance paths lack the `src/` prefix used in this fixture (for example `scripts/run_package_tests.py` versus `src/scripts/run_package_tests.py`); the mapping is an assumption consistent with the matching hashes.
5. **Traceability is partial.** `provenance.json` names the original commit `d5a7f0da…` in a repository path outside this fixture, with `remote_freshness: "not checked"`. That commit is not present in this fixture's git history (commits `3236024`, `00fa764`, `4959e62`; no tags, no remotes, per the observations). The fixture git history shows only the harness's own commits and is not the original project. So the commit claim is an unverified attribution; matching hashes support that the files are the same bytes as those recorded, not that they came from that commit.
6. **Links.** From `docs/loom/research/`, `../../../provenance.json`, `../../../src/scripts/run_package_tests.py` and `../../../src/tests/test_run_package_tests.py` in the earlier record resolve to existing files (all present in the file listing). I read those targets and they are the intended evidence. Citations in the earlier record are slightly offset from the file I read: `TEST_ROOTS` is on line 53 (block 51–54, not 51–55); the `code` group is lines 124–128; shell discovery is 88–95; the explicit-argument path is 168–176. These do not change its conclusion, but the line anchors should not be quoted as exact.
7. **Test definitions** (`test_run_package_tests.py` lines 222–235, 285–298, 301–311) match what the earlier record says they assert. They were read, not run.

## Evidence

| Claim | Source kind | Support type |
|---|---|---|
| exit_code=0 belongs to a codex executor run, not tests | [sample-receipt.json](../../../sample-receipt.json) (`command`, `added_project_files`) | Read artifact |
| Earlier record is static only | [earlier record](2026-11-08-package-test-roots.md), Method and Limitations | Read artifact |
| Hash equality with provenance | [fixture-observations.json](../../../fixture-observations.json), [provenance.json](../../../provenance.json) | Harness observation compared by reading |
| Original commit is not in fixture history | observations `git log --all`, `tag --list`, `remote -v` | Harness observation |
| Runner exit semantics | [runner](../../../src/scripts/run_package_tests.py) lines 153–176 | Source inspection (not execution) |

## Decision impact

Supportable claims:
- The receipt shows an external executor process exited 0 and added the research record.
- The record is a static source-inspection result about `TEST_ROOTS` and the `tests/local/` exclusion in the runner preset in this 4-file snapshot.
- The four snapshot source files match the SHA256 values in `provenance.json` (per harness observation), and the record's local links resolve.

Not supportable:
- "Whole package tests/CI pass." No test execution record exists, the receipt is unrelated to tests, and the snapshot lacks most of the suite and any CI configuration.
- "Source traceable to commit `d5a7f0da`" as verified. It is a recorded attribution, with no original repository, remote or tag available here.
- Deployment or installation claims.

To claim a pass, a real execution record is needed (command, revision, environment, output, exit code) from the full checkout, plus CI run evidence.

## Limitations and open questions

- I ran no commands and computed no hashes; hash equality comes from the harness's pre-run observations and my reading of the values.
- I could not verify the post-write hash of the earlier record, or that `provenance.json` itself matches `source_provenance_sha256`.
- The receipt's content is taken at face value; I cannot confirm it is a faithful log of the executor run.
- The original repository, remote state and CI configuration were not inspected (out of bounds).
