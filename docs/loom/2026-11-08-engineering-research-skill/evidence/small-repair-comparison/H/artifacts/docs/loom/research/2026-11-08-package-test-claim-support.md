---
title: "What can be claimed from the sample receipt and the package-test-roots record"
type: loom-research
status: concluded
created: 2026-11-08
updated: 2026-11-08
tags:
  - loom/research
---

# What can be claimed from the sample receipt and the package-test-roots record

## Question and scope

The user intends to claim that this snapshot's whole package tests/CI pass and that its sources are traceable, based on `exit_code=0` in [sample-receipt.json](../../../sample-receipt.json) and the existing record [package test roots](2026-11-08-package-test-roots.md). Which parts are supported? Scope: the temporary local fixture only. No tests, remote queries or publishing were performed. This is a separate question from the earlier record, which is left unchanged.

## Method and rationale

Inspection of existing artifacts (receipt, earlier record, provenance, harness observations, runner source), per the source policy: an exit code, an existing artifact or a test definition does not alone prove the promised outcome. No command could be run in this session; hash values below are harness observations, not my measurements.

## Findings

1. **Receipt does not show package tests ran.** The receipt (`id` B02) records a `codex exec ... -` invocation of a different executor (model `gpt-6.1-sol`), with `exit_code: 0`. That is the exit status of the executor process, not of `run_package_tests.py` or pytest. The command contains no runner invocation, and the receipt has no test output, counts or test command. Observed: the executor exited 0, `source_unchanged: true`, and it added one file, `docs/loom/research/2026-11-08-package-test-roots.md`. Its `-C` and `-o` paths point to a different directory than this fixture. No claim about any test result follows.
2. **The research record is static source inspection only.** It states that no tests or runner commands were executed and that no runtime validation exists. File existence is not a test outcome.
3. **The snapshot cannot support a whole-suite claim.** `src/` has 4 files: the runner, `repo_files.py`, `git_exec.py` and `test_run_package_tests.py`. The runner's `TEST_ROOTS` expects `tests`, `loom-code/tests`, `loom-design/tests` and `loom-workflow/tests`. Apart from this one test file, no listed test root is present, and the Mermaid group needs `loom-workflow/tests/mermaid`, which is absent. A full package run cannot be reproduced from this snapshot. The runner's `--loom-family` mode does not depend on a CI configuration, and CI config is not in the snapshot either. "CI passed" has no evidence.
4. **Source traceability is partial.** Harness observation: SHA256 of the four `src/` files equals the values in [provenance.json](../../../provenance.json) (runner `6730a53e…`, `repo_files` `62333168…`, `git_exec` `9c721b8e…`, test file `b7ed3d4e…`), and the earlier record's hash statement matches these. Provenance ties them to commit `d5a7f0da…` of an external original repository; that repository was not readable and `remote_freshness` is "not checked". The locally recorded `origin/main` equals HEAD only as a recorded string. So hashes show the files match provenance's declaration, not that the commit exists or contains those contents.
5. **Record accuracy.** I checked the earlier record's anchors against the runner and the test file: `TEST_ROOTS` at line 53 (record says 51–55, which includes adjacent lines), the `local/` ignore in `_tests_session` (76–86), shell exclusion (88–95), preset and explicit-argument modes (153–176). The test definitions at lines 222 and 285–311 assert root list and `local` exclusion. The record's narrow claim, that these roots are listed and the preset excludes `local/`, is supported by source. Line ranges are slightly loose (for example, the code group begins at 124, not 122).
6. **Git state.** Harness observation of the local git queries: `main` is `4959e62`, `research-fixture` is `00fa764` and is an ancestor of `main`; no tags and no remotes. This is a temporary harness repository, not the original project history. The record's own SHA256 is `c54f2872…` (harness observation, pre-actor; the file was not modified by me). Observations carry no post-write actor-copy hash.

## Evidence

| Claim | Source | Kind / status |
|---|---|---|
| Executor exit 0, different command, no test output | [sample-receipt.json](../../../sample-receipt.json) | Existing artifact, read |
| No tests run for the earlier record | [earlier record](2026-11-08-package-test-roots.md), Method and Limitations | Read |
| Roots, `local/` exclusion | [runner](../../../src/scripts/run_package_tests.py) lines 51–53, 76–86, 88–95, 124–128 | Source inspection |
| Test definitions only | [test file](../../../src/tests/test_run_package_tests.py) lines 222, 285–311 | Source grep; not run |
| File hashes equal provenance | [fixture-observations.json](../../../fixture-observations.json), [provenance.json](../../../provenance.json) | Harness observation, not my command |
| Only 4 source files present | Glob of `src/` | Observed listing |

## Decision impact

Supportable claim: "In this fixture, the supplied runner source, by static reading, lists four test roots and its `--loom-family` preset excludes `local/`. The four snapshot files match the SHA256 values declared in provenance for commit `d5a7f0da…`; the original repository and remote freshness were not verified."

Not supportable: that the whole package tests pass, that CI passed, that the receipt shows any test run, or that provenance has been verified against the original repository. To claim a test result, someone must run the runner in a complete checkout, retain the command, output and revision, and have CI evidence if CI is claimed. I did not accept or approve the result on the user's behalf.

## Limitations and open questions

- I ran no commands; hashes and git results are quoted from the harness file and not independently reproduced.
- The original repository, the `d5a7f0da…` commit and CI configuration were not inspected.
- Whether the receipt's prompt asked for tests is unknown, as the prompt is not in the receipt.
- Runtime behavior of the runner (including `nested_repositories`) was not examined or executed.
