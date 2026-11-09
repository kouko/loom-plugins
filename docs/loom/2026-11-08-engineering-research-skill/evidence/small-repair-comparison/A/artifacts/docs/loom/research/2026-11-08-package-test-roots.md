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

## Continuation check: does ordinary `--loom-family` run `tests/local/` Python and shell tests?

Same question and same source snapshot (provenance `HEAD` `d5a7f0da…`). "Ordinary preset" here means `--loom-family` with no `--only`, which runs the `code`, `design`, `workflow-python`, `workflow-shell` and `workflow-mermaid` groups (runner `main`, lines 153–167; `loom_family_commands`, lines 116–150). The earlier evidence was reused; the runner and test file were re-read in this pass (static inspection, nothing executed) to confirm applicability.

- **Python: not run.** The `code` group builds its session from `tests` and `loom-code/tests` via `_tests_session` (lines 124–128). For each root it sets `local = folder / "local"`, checks `_holds_tests(folder, (local,))` so that `local/` files do not count, and appends `--ignore=<abs tests/local>` when the directory exists (lines 76–85). The command is `pytest <targets> <ignores> -q -n auto` (line 128), so `tests/local/` Python files are not collected. The module docstring states the same intent (lines 7–10).
- **Shell: not run.** `_shell_tests` globs `test-*.sh` under each root and drops any path whose parents include `<root>/local` (lines 88–95; the exclusion is line 94). The `workflow-shell` command list is built only from that function (lines 134–138).
- **Test definitions agree** ([tests](../../../src/tests/test_run_package_tests.py), lines 222–235 for Python and 285–298 for shell). They plant `tests/local/` files and assert they are absent from collection or commands. They were read, not run.
- **Boundary found on re-read:** exclusion is only for a root's *direct* `local/` folder. A folder named `local` nested deeper (e.g. `tests/hooks/local/`) matches neither `folder / LOCAL` check, so by this source it would still be collected or run. This was not exercised by the cited tests and was not executed.
- **Harness observations** ([fixture-observations.json](../../../fixture-observations.json)): the recorded SHA256 values for the runner, test file and `repo_files.py`/`git_exec.py` match [provenance](../../../provenance.json); the runner and test hashes equal those cited above. In the temporary git fixture, `research-fixture` (`00fa764`) is an ancestor of `main` (`4959e62`). These are preparation-stage observations supplied by the harness, not commands I ran, and no post-write hash of the actor's copy is supplied.

**Answer:** No. In the ordinary `--loom-family` preset, neither Python nor shell tests under `tests/local/` (or `loom-code/tests/local/`, or the design/workflow root `local/` folders) are run, per source at this snapshot. Existing evidence was sufficient; no new experiment was made.

## Decision impact

Do not place tests intended for ordinary package coverage in `tests/local/`. A new standalone plugin test root is not automatically discovered: it must be added to `TEST_ROOTS`; otherwise use an existing listed root outside its excluded `local/` subtree, subject to the runner's normal discovery rules.

## Limitations and open questions

This is a source-supported conclusion, without runtime validation. CI configuration and deployed or installed versions are outside the supplied evidence; no claim is made about them. No material uncertainty remains for the inspected runner's root list and preset exclusion. The continuation check likewise rests on source reading only: no runner or pytest invocation was possible or made, so actual collected sets are unobserved, and deeper nested `local/` folders are untested (see above). `local/` Python files that import or are imported by non-local tests are not analyzed.
