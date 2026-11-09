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
- The package preset is selected by `--loom-family` (lines 153–167). Its `code` group includes the first two roots and calls `_tests_session` (lines 122–128). That helper excludes the root's `local/` while checking for tests and adds `--ignore=<absolute local path>` when present (lines 76–85). Consequently, `tests/local/` is excluded from this preset's Python collection. Shell discovery likewise excludes each root's direct `local/` subtree (lines 89–96). Design and workflow Python paths also exclude their root-level `local/` directories (lines 99–114, 129–132).
- [Test definitions](../../../src/tests/test_run_package_tests.py), lines 222–235, 285–310, assert the root list and exclusion of Python and shell files under `tests/local/`. These definitions were read, not run.
- The exclusion is preset-specific: the alternate explicit-argument mode forwards each group directly to pytest without adding these ignores (runner lines 168–175). This finding does not establish exclusion for bare pytest or explicitly targeted local tests.

The inspected runner and test file SHA256 values, measured with `shasum -a 256`, match their entries in provenance: `6730a53e11d862d5d3d93eadcdafb2011b81f2595332e4a57ae49a504f660d54` and `b7ed3d4e19fd4d03c68df5d8ca796d03442a859874745564c20ddaeb7780da28`, respectively.

## Continuation: does ordinary `--loom-family` run `tests/local/` Python and shell tests?

Same question and conditions (same snapshot at `d5a7f0da…`, same runner and test file; SHA256 of both re-measured with `shasum -a 256` and still equal to the values above and to provenance). Existing evidence was reused after re-reading the runner in full; no tests or runner were run, and nothing else was changed. Method: static source inspection of the connected path from `main` to the command builders.

- **Path:** `main` takes `--loom-family` (runner lines 154–163) and calls `loom_family_commands` with `only=None` for the ordinary preset, so both the `code` group and the `workflow-shell` group are built (lines 124, 134).
- **Python:** the `code` group builds from `tests` and `loom-code/tests` (lines 125–126). `_tests_session` (lines 76–85) selects a root only if it holds tests outside `<root>/local`, and adds `--ignore=<root>/local` when that folder exists. For `tests/local/`, pytest therefore receives an ignore, so its Python tests are not collected. A root containing only `local/` tests is not targeted at all.
- **Shell:** `_shell_tests` (lines 88–95) rglobs `test-*.sh` under every root and drops files whose parents include `<root>/local`. `tests/local/test-*.sh` is therefore not emitted as a `bash` command.
- **Corroboration (read, not run):** [`test_code_group_discovers_tests_folders_and_skips_local`](../../../src/tests/test_run_package_tests.py) (line 222) and [`test_shell_group_discovers_test_scripts_under_every_root`](../../../src/tests/test_run_package_tests.py) (line 285) define these expectations.
- **Answer:** no. In the ordinary preset, neither Python nor shell tests under root-level `tests/local/` are run.
- **Line-anchor corrections to the findings above:** the `code` group is lines 124–128, `_tests_session` is 76–85 and `_shell_tests` is 88–95; the substance is unchanged.

Boundaries: only a `local/` directly under a root is excluded (`root/local`); a nested `local/` deeper in a subfolder (for example `tests/hooks/local/`) is not excluded by this code, and I did not examine whether such a case occurs. A user-supplied explicit path, bare pytest, or the non-preset mode still can run `tests/local/`. Behavior in CI or any installed version remains unverified.

## Decision impact

Do not place tests intended for ordinary package coverage in `tests/local/`. A new standalone plugin test root is not automatically discovered: it must be added to `TEST_ROOTS`; otherwise use an existing listed root outside its excluded `local/` subtree, subject to the runner's normal discovery rules.

## Limitations and open questions

This is a source-supported conclusion, without runtime validation. CI configuration and deployed or installed versions are outside the supplied evidence; no claim is made about them. No material uncertainty remains for the inspected runner's root list and preset exclusion.
