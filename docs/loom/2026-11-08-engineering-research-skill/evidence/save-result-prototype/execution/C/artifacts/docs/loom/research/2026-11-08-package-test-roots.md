---
title: "Package runner test roots and local-test exclusion"
type: loom-research
status: concluded
created: 2026-11-08
updated: 2026-11-08
tags:
  - loom/research
---

# Package runner test roots and local-test exclusion

## Question and scope

Which directories does this runner list in `TEST_ROOTS`, and does its ordinary package suite include `tests/local/`? This informs placement of a new plugin's tests. Scope is the supplied minimal source snapshot, attributed by [provenance](../../../provenance.json) to commit `d5a7f0da247214bdb9c61fe90c550256432e5f76`; it is neither a complete checkout nor evidence of deployment.

**Continuation (2026-11-08):** the same question under the same snapshot was re-asked in narrower form: does the ordinary `--loom-family` preset run the Python and the shell tests under `tests/local/`? No new question or changed conditions, so this record is reopened rather than split.

## Method and rationale

Static source inspection of the runner's entry point and discovery helpers, with relevant test definitions as corroboration. This directly answers the single-source question; no tests or runner commands were executed.

Continuation: the earlier evidence was reused. Applicability was rechecked by re-reading the runner (`src/scripts/run_package_tests.py`) and the cited test definitions in full for the relevant paths, and by comparing the file hashes in [harness observations](../../../fixture-observations.json) with [provenance](../../../provenance.json). No new experiment was needed or run; this agent had no command tool.

## Findings and evidence

- `TEST_ROOTS` contains exactly `tests`, `loom-code/tests`, `loom-design/tests`, and `loom-workflow/tests` ([runner](../../../src/scripts/run_package_tests.py), lines 52–53).
- The package preset is selected by `--loom-family` (`main`, lines 153–167). **Python, `code` group:** it takes every root except design and workflow, i.e. `tests` and `loom-code/tests` (lines 124–128), and builds the session with `_tests_session`. That helper tests for test files while skipping `<root>/local` and, when that folder exists, appends `--ignore=<absolute local path>` (lines 76–85). So `tests/local/` Python tests are excluded from the pytest command. If a root held only `local/` tests, it would not be targeted at all.
- **Shell, `workflow-shell` group:** `_shell_tests` globs `test-*.sh` under each root and drops any path whose parents include `<root>/local` (lines 88–95), used at lines 134–138. So `tests/local/test-*.sh` is not run by the preset.
- Design and workflow Python sessions likewise exclude their root-level `local/` (lines 98–113, 129–132). The module docstring states the same intent (lines 4–11).
- [Test definitions](../../../src/tests/test_run_package_tests.py) assert this: lines 222–235 (Python files under `tests/local` and `loom-code/tests/local` are not collected in the `code` group) and 285–298 (a `tests/local/test-z.sh` is absent from the shell commands). These were read, not run.
- Boundaries: (a) the exclusion applies only to the direct `<root>/local` folder; by this code a deeper folder such as `tests/sub/local/` is not special-cased and would be discovered (inference from lines 76–95, not tested). (b) The alternate explicit-argument mode forwards each group straight to pytest with no ignores (lines 168–175), so it does not establish exclusion for bare pytest or explicitly targeted local tests. (c) Exclusion applies equally with `--only code`/`workflow-shell` and with no `--only`, since the same helpers are used.
- Mechanical observations: the runner and test file SHA256 values, `6730a53e…0d54` and `b7ed3d4e…0da28`, match [provenance](../../../provenance.json). The same values appear in the harness-prepared [observations file](../../../fixture-observations.json), which also records a clean-ancestry git check of the temporary fixture. These are harness observations; I did not run these commands. Earlier measurement of the hashes with `shasum -a 256` is retained from the first pass.
- Correction: some line anchors in the first version were off by one to two lines (e.g. the code group begins at line 124, `_shell_tests` at 88). They are corrected above; conclusions are unchanged.

## Decision impact

Yes to the re-check question: by source, the ordinary `--loom-family` preset does **not** run Python or shell tests in `tests/local/`. Do not place tests intended for ordinary package coverage there. A new standalone plugin test root is not automatically discovered: it must be added to `TEST_ROOTS`; otherwise use an existing listed root outside its excluded `local/` subtree, subject to the runner's normal discovery rules.

## Limitations and open questions

This is a source-supported conclusion, without runtime validation: neither the runner nor its tests were executed. CI configuration and deployed or installed versions are outside the supplied evidence, and remote freshness of the source commit was not checked. The nested-`local/` behavior is inferred from code only. No material uncertainty remains for the inspected runner's root list and the direct `<root>/local` exclusion.
