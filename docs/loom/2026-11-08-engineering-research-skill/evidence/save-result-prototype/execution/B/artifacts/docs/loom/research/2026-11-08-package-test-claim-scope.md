---
title: "Claim scope for the package test runner snapshot: receipt, record, hashes and links"
type: loom-research
status: concluded
created: 2026-11-08
updated: 2026-11-08
tags:
  - loom/research
---

# Claim scope for the package test runner snapshot

## Question and scope

The user wants to claim that the whole package tests/CI pass for this snapshot and that the source is traceable. The pending decision is how far that claim can go, given `sample-receipt.json` (`exit_code=0`), the existing record [package-test-roots](2026-11-08-package-test-roots.md), the source hashes and the links. Scope: the temporary local fixture only. No tests, remote checks, publishing or acceptance were done. The user did not ask for these.

This is a different question from the earlier record, which asked which test roots the runner lists. That record is linked and left unchanged.

## Method and rationale

Reused and inspected existing local evidence: the receipt, the earlier record, `provenance.json`, `fixture-observations.json` (a harness observation, not something I ran), the runner source and the test definitions. This is enough, because the question is about what these artifacts can support. No new experiment was needed or permitted.

## Findings

1. **The receipt is not a test result.** `exit_code: 0` in [sample-receipt.json](../../../sample-receipt.json) is the exit status of an executor process with id `B02`. The process was a `codex exec` invocation that ran with `web_search` disabled and `server_confirmed_model: null`. The receipt has no pytest, runner or CI command, no test counts and no output. Its `added_project_files` entry shows that process wrote the research record. So it shows that an executor finished, and says nothing about the package suite.
2. **The runner source gives no support for a "tests passed" claim.** In [the runner](../../../src/scripts/run_package_tests.py) `main` returns 0 only if every spawned command returns 0 (lines 163–167). That is the meaning of a runner exit code, but no runner exit code exists in this evidence. Running `--loom-family` would also need `npm ci` and `node` for the `workflow-mermaid` group (lines 139–145). Those parts of the tree are not in the snapshot (see 3).
3. **The snapshot is a minimal slice.** The files present are `src/scripts/run_package_tests.py`, `src/tests/test_run_package_tests.py` and `src/loom-code/scripts/{git_exec,repo_files}.py`. The runner's `TEST_ROOTS` (line 53) names `tests`, `loom-code/tests`, `loom-design/tests` and `loom-workflow/tests`. Most of those roots, the mermaid validator and the CI configuration are not in the fixture. The earlier record also says CI and deployed versions are outside its evidence.
4. **The existing record supports only a static claim.** [package-test-roots](2026-11-08-package-test-roots.md) concludes from source reading which roots the runner lists and that the `--loom-family` preset skips `local/`. It states that nothing was executed. I spot-checked its citations against the source. The runner line anchors are approximate: `_tests_session` is at lines 76–85, `loom_family_commands` code group at 124–128, and the explicit-argument mode at 168–175. The conclusions match the code. The test-definition ranges (lines 222–235 and 285–310) match the real test names and assertions. The record says the test definitions were "read, not run", which is accurate.
5. **Hashes match as recorded, within what I could check.** The runner and test-file SHA256 values in `provenance.json` equal the values in `fixture-observations.json` and the values quoted in the earlier record. The harness observation is the only hash source I have. I could not compute hashes myself, so I did not independently verify them. The observation file also lists a hash of the earlier record (`c54f2872…1283`) and of `provenance.json` (`8d9a1ad6…1364`). I did not check either, and the observation file is a preparation-stage observation, so no post-write hash exists for any later file.
6. **Traceability is partial.** `provenance.json` attributes the files to commit `d5a7f0da247214bdb9c61fe90c550256432e5f76` in an original repository, with `remote_freshness: "not checked"`. That repository is outside this fixture and I did not read it. The fixture's own git history (`3236024`, `00fa764`, `4959e62`) is from a temporary harness repository with no remote and no tags, so it does not show the original history. The provenance paths omit the `src/` prefix used in the fixture. This is a plausible mapping, not an established fact. The earlier record's statement that the hashes were "measured with `shasum -a 256`" is its own claim. I cannot confirm it, and the receipt does not record that command.
7. **Links resolve.** From this record's directory, `../../../sample-receipt.json`, `../../../src/scripts/run_package_tests.py` and `2026-11-08-package-test-roots.md` all point to existing fixture files. This was checked from the file listing and by reading them.

## Evidence

| Claim | Source | Kind | Status |
|---|---|---|---|
| `exit_code: 0` belongs to executor `B02` and records no test command | [sample-receipt.json](../../../sample-receipt.json) | existing execution record, read | observed in the file |
| Runner returns 0 only if all spawned commands pass | [runner](../../../src/scripts/run_package_tests.py) lines 153–176 | source inspection | not executed |
| Roots, preset and `local/` exclusion | [package-test-roots](2026-11-08-package-test-roots.md) and the runner | prior record plus source | source-supported, no runtime check |
| Source hashes agree across files | `provenance.json`, `fixture-observations.json` | harness observation | not recomputed by me |
| No remote, no tags, `main` contains `research-fixture` | `fixture-observations.json` git entries | harness observation | I ran no git commands |

## Decision impact

**Can be claimed:**
- The snapshot's runner source defines `TEST_ROOTS` as stated and the `--loom-family` preset skips `local/`. This is source-supported.
- The earlier record is internally consistent with the runner source and the test definitions it cites, with minor line-number drift.
- The source files' hashes match the values in `provenance.json`, as reported by the harness observation.
- The snapshot is attributed to commit `d5a7f0da…` in an original repository that was not examined and whose freshness was not checked.

**Cannot be claimed:**
- That the whole package tests pass. No test run output exists in this evidence.
- That CI passes. No CI configuration, run or result exists in this evidence.
- That the receipt's `exit_code=0` shows either of the above. It is an executor process status.
- That the provenance is fully traceable or current. The original repository and the remote were not examined, so this is a recorded attribution only.

A claim of passing tests would need an actual run of the suite, or a CI result for the exact commit, with the command, environment and output kept. That is outside this task's permissions and was not requested.

## Limitations and open questions

- I ran no commands, hash tools or tests, and the tools available were read-only apart from saving this record.
- The hash agreement is taken from harness-supplied observations. The skill-file hashes in `provenance.json` were not compared.
- The mapping between the `src/` paths and the original repository paths is inferred.
- Whether the original repository's CI passed for `d5a7f0da…` is unknown.
- Revalidate if the snapshot, the commit or the receipt changes.
