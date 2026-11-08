---
title: "Package runner test roots and local-test exclusion"
type: loom-research
status: concluded
created: 2026-11-08
updated: 2026-11-08
tags:
  - loom/research
---

## Question and scope

Which directories does this runner list in `TEST_ROOTS`, and does its ordinary package suite include `tests/local/`? This informs placement of a new plugin's tests. Scope is the supplied minimal source snapshot, attributed by [provenance](../../../provenance.json) to commit `d5a7f0da247214bdb9c61fe90c550256432e5f76`; it is neither a complete checkout nor evidence of deployment.

## Method and rationale

Static source inspection of the runner's entry point and discovery helpers, with relevant test definitions as corroboration. This directly answers the single-source question; no tests or runner commands were executed.

## Findings and evidence

- `TEST_ROOTS` contains exactly `tests`, `loom-code/tests`, `loom-design/tests`, and `loom-workflow/tests` ([runner](../../../src/scripts/run_package_tests.py), lines 51–55).
- The package preset is selected by `--loom-family` (lines 153–167). Its `code` group includes the first two roots and calls `_tests_session` (lines 122–128). That helper excludes the root's `local/` while checking for tests and adds `--ignore=<absolute local path>` when present (lines 76–86). Consequently, `tests/local/` is excluded from this preset's Python collection. Shell discovery likewise excludes each root's direct `local/` subtree (lines 89–96). Design and workflow Python paths also exclude their root-level `local/` directories (lines 99–114, 129–132).
- [Test definitions](../../../src/tests/test_run_package_tests.py), lines 222–235, 285–310, assert the root list and exclusion of Python and shell files under `tests/local/`. These definitions were read, not run.
- The exclusion is preset-specific: the alternate explicit-argument mode forwards each group directly to pytest without adding these ignores (runner lines 168–175). This finding does not establish exclusion for bare pytest or explicitly targeted local tests.

The inspected runner and test file SHA256 values, measured with `shasum -a 256`, match their entries in provenance: `6730a53e11d862d5d3d93eadcdafb2011b81f2595332e4a57ae49a504f660d54` and `b7ed3d4e19fd4d03c68df5d8ca796d03442a859874745564c20ddaeb7780da28`, respectively.

## Decision impact

Do not place tests intended for ordinary package coverage in `tests/local/`. A new standalone plugin test root is not automatically discovered: it must be added to `TEST_ROOTS`; otherwise use an existing listed root outside its excluded `local/` subtree, subject to the runner's normal discovery rules.

## Continuation check — 2026-11-08

The follow-up asks whether the ordinary `--loom-family` preset runs Python or shell tests under `tests/local/`, under the same source-snapshot conditions. The existing evidence is sufficient and remains applicable: **neither is included by the preset's discovery path**. This continues the same question; no new change or experiment was created.

Reused evidence was checked against the actual runner and test definitions. In `main`, ordinary `--loom-family` selects `only=None` and calls `loom_family_commands` (runner lines 153–164). This includes the `code` path through `_tests_session` (lines 124–128), which excludes `tests/local/` from its test-presence check and adds its absolute pytest ignore when present (lines 76–85). The shell group calls `_shell_tests` (lines 134–138), whose discovery explicitly excludes descendants of the root's `local/` (lines 88–95). If only local Python tests exist, the root does not become a target. The previously cited Python and shell test assertions corroborate these exclusions; they were inspected, not executed. Fresh `shasum -a 256 src/scripts/run_package_tests.py src/tests/test_run_package_tests.py` output exactly matched both hashes recorded above and in provenance, confirming the same supplied source files.

This was an evidence-reuse and static applicability check, with no test, runner, sample command, or external model execution. The [existing executor receipt](../../../sample-receipt.json) records an earlier executor invocation; its exit code is not evidence that these package tests ran or passed. The [fixture cleanup record](../../../fixture-cleanup.json) reports an empty `git status --porcelain` result at temporary post-merge main revision `4959e620a78e15678a3cc2a8a0c18f79de58dc73`, cleanup destination `.`, no linked worktree or generated temporary build artifact, and retention of the topic branch. That is fixture lifecycle evidence only, not the original source revision, deployment validation, or a claim that this research edit leaves the current tree clean. No additional cleanup was needed or performed for this check.

The decision and runtime limitations below remain unchanged. Revalidation is needed if the source snapshot or invocation mode changes; explicit-argument mode and bare pytest are outside this conclusion.

## Limitations and open questions

This is a source-supported conclusion, without runtime validation. CI configuration and deployed or installed versions are outside the supplied evidence; no claim is made about them. No material uncertainty remains for the inspected runner's root list and preset exclusion.
