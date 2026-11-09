---
title: "Claim scope: receipt exit_code 0 and existing research record versus full package tests/CI pass"
type: loom-research
status: concluded
created: 2026-11-08
updated: 2026-11-08
tags:
  - loom/research
---

# Claim scope: receipt exit_code 0 and existing research record versus full package tests/CI pass

## Question and scope

The user plans to claim that this snapshot's whole package test suite / CI passed and that its sources are traceable, based on `exit_code=0` in [sample-receipt.json](../../../sample-receipt.json) and the existing record [package test roots](2026-11-08-package-test-roots.md). Which parts of that claim do the receipt, record, source hashes and links actually support? Conditions: the minimal source snapshot in `src/` (provenance HEAD `d5a7f0da247214bdb9c61fe90c550256432e5f76`, remote freshness "not checked"), local git history of the temporary fixture, no test execution, no network. This is a different question from the earlier record (which asked about `TEST_ROOTS`), so it is a separate file linked to it.

## Method and rationale

Inspection of existing artifacts: receipt fields, record text, provenance, local git history, SHA256 of the four source files (`shasum -a 256`), link resolution, and re-reading the runner lines the earlier record cites. Existing evidence suffices; nothing was run. Per the source policy, an exit code, test definitions or an existing artifact alone do not prove the promised outcome.

## Findings

Observed:
- The receipt describes a `codex exec` run (`--sandbox workspace-write`, model request `gpt-6.1-sol`) that produced the research record. Its `exit_code: 0` is that process's exit status. It records `added_project_files: ["docs/loom/research/2026-11-08-package-test-roots.md"]` and `source_unchanged: true`. It contains no pytest/runner command, no test output, no CI identifier. `server_confirmed_model` is null.
- The research record states "no tests or runner commands were executed" and "source-supported conclusion, without runtime validation", and excludes CI configuration and deployments.
- Source hashes: all four files in `src/` match `provenance.json` (runner `6730a53e…0d54`, test file `b7ed3d4e…da28`, `repo_files.py` `62333168…6399`, `git_exec.py` `9c721b8e…e7c7`). The earlier record only mentions two of the four.
- Links: the record's relative links (`../../../provenance.json`, `../../../src/...`) resolve from its location. The receipt's `-C` and `-o` paths point to directories outside this fixture and were not read.
- Cited runner lines hold: `TEST_ROOTS` at line 53 (record says 51–55, a loose range), `--loom-family` preset at 153–167, `_tests_session` at 76–86, shell exclusion at 88–95.
- The snapshot contains only 4 files; the roots `tests/`, `loom-code/tests`, `loom-design/tests`, `loom-workflow/tests` and `.github`/CI configuration are absent, so a package suite cannot even be run here.
- The skill files read here differ in hash from `provenance.json`'s `skill_files` for `SKILL.md` and `templates/research.md` (current `5f2880b8…`, `62757b98…`); the other three listed references match. The record was thus produced under a possibly different skill version.

Inference: the receipt's `exit_code=0` means the agent process finished, not that any tests passed.

## Evidence

| Claim | Support | Kind |
|---|---|---|
| Source files match recorded hashes | `shasum -a 256` of [runner](../../../src/scripts/run_package_tests.py), [tests](../../../src/tests/test_run_package_tests.py), [repo_files](../../../src/loom-code/scripts/repo_files.py), [git_exec](../../../src/loom-code/scripts/git_exec.py) vs [provenance](../../../provenance.json) | measured locally |
| Receipt shows no test run | [sample-receipt.json](../../../sample-receipt.json) fields above | artifact inspection |
| Record is static analysis only | [record](2026-11-08-package-test-roots.md) Method and Limitations | artifact inspection |
| Prior record's line anchors | runner lines 53, 76–86, 88–95, 153–176 | source inspection |
| Provenance of the snapshot | local git: `3236024 fixture source snapshot`, `00fa764 retain genuine prior research slice`, `4959e62 merge temporary research fixture` | harness-built temporary repo, not original history |

## Decision impact

Supported claims:
- The snapshot's four source files are byte-identical to the hashes recorded in provenance, which attributes them to original commit `d5a7f0da…` (attribution is the provenance file's assertion; the original repository was not read and remote freshness was not checked).
- A source-reading record exists that answers the `TEST_ROOTS`/`tests/local/` question for this snapshot, with the caveats above.
- A receipt exists showing the producing agent process exited 0 and left source unchanged.

Not supported:
- "Whole package tests pass": no test was run in the evidence; test definitions were only read; the snapshot lacks the test roots.
- "CI passes": no CI configuration, run or log is in evidence.
- "Fully traceable": traceability is limited to four files by hash plus a provenance assertion; the git history is a temporary fixture; the receipt's paths are external and unverified; the record was made under a skill version whose two files differ from the provenance hashes.

Acceptable wording: "Static inspection of a 4-file snapshot (hashes match provenance for commit d5a7f0da, remote not checked) found `TEST_ROOTS` and the `tests/local/` exclusion in the `--loom-family` preset; no tests or CI were run." To claim a full pass, someone must run the package runner on the complete checkout, or cite a CI run with commit and log; that is outside this authorization.

## Limitations and open questions

Not checked: the original repository, any CI system, actual runner execution, the receipt's external paths, model identity (unconfirmed). The earlier record deviates slightly from the template (no H1, merged Findings/Evidence) and its test-file line citations (222–235, 285–310) were not re-verified here. Acceptance of the claim remains the user's decision.
