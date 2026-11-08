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

Continuation (same question, same snapshot, 2026-11-08): confirm whether the ordinary `--loom-family` preset runs the Python **and** shell tests under `tests/local/`.

## Method and rationale

Static source inspection of the runner's entry point and discovery helpers, with relevant test definitions as corroboration. This directly answers the single-source question; no tests or runner commands were executed.

Continuation: the earlier evidence was reused after re-reading the runner (`src/scripts/run_package_tests.py`) in full and the relevant test definitions in the snapshot. The question and source snapshot are unchanged, so the earlier answer still applies. Only line anchors and one boundary detail were refined.

## Findings

- Answer to the continuation: no. In the `--loom-family` preset, neither Python tests nor `test-*.sh` shell tests under `tests/local/` are run. This is source-supported, not runtime-observed.
- `TEST_ROOTS` contains exactly `tests`, `loom-code/tests`, `loom-design/tests` and `loom-workflow/tests`.
- Python: the `code` group covers `tests` and `loom-code/tests` through `_tests_session`. It passes `--ignore=<absolute local path>` for each root's `local/` folder that exists. `_holds_tests` also excludes that folder when deciding whether a root has tests.
- Shell: `_shell_tests` globs `test-*.sh` under each root and drops any path that has `<root>/local` among its parents. The `workflow-shell` group runs only these.
- Design and workflow Python sessions exclude their root-level `local/` the same way.
- Refinement (inference from the code, not tested): every exclusion is keyed to the direct `<root>/local` folder. A directory named `local` deeper in a root, such as `tests/hooks/local/`, does not match these checks. I did not verify how it behaves, and no test in the snapshot covers it.
- The exclusion is preset-specific. The explicit-argument mode (no `--loom-family`) forwards each group straight to pytest without these ignores. This does not establish exclusion for bare pytest or for explicitly targeted local tests.

## Evidence

All line numbers refer to the [runner](../../../src/scripts/run_package_tests.py) as inspected (source inspection, snapshot only).

- Module docstring, lines 4–11: a root's `local/` folder is "skipped"; tests outside the roots do not run.
- `TEST_ROOTS`, lines 51–53.
- `_holds_tests` and `_tests_session`, lines 68–85: `local` is skipped when looking for tests, and `--ignore=<local>` is added at lines 83–84.
- `_shell_tests`, lines 88–95: the exclusion is `folder / LOCAL not in path.parents` at line 94.
- `_workflow_sessions`, lines 98–113, and the `design` and `workflow-python` branches, lines 129–132.
- `code` group, lines 124–128: its roots are `tests` and `loom-code/tests`.
- `workflow-shell` branch, lines 134–138.
- `--loom-family` dispatch, lines 153–167. Explicit-argument mode, lines 168–175.
- [Test definitions](../../../src/tests/test_run_package_tests.py), read but not run:
  - lines 222–235 seed `tests/local` and `loom-code/tests/local` Python tests and assert they are not collected.
  - lines 285–298 plant `tests/local/test-z.sh` and assert it is absent from the shell commands.
  - lines 301–311 assert the root list.
- The inspected runner and test file SHA256 values match their [provenance](../../../provenance.json) entries: `6730a53e11d862d5d3d93eadcdafb2011b81f2595332e4a57ae49a504f660d54` and `b7ed3d4e19fd4d03c68df5d8ca796d03442a859874745564c20ddaeb7780da28`.
  - These came from the harness's pre-run observation in `fixture-observations.json`. I did not recompute them, and the file reports no post-write hash.
  - That file also records the local git history of the temporary fixture. It is a harness observation, not deployment evidence.

## Decision impact

Do not place tests intended for ordinary package coverage in `tests/local/`, whether Python or shell. A new standalone plugin test root is not automatically discovered: it must be added to `TEST_ROOTS`. Otherwise use an existing listed root outside its excluded `local/` folder, subject to the runner's normal discovery rules. The earlier decision stands.

## Limitations and open questions

- This is a source-supported conclusion. No runner, pytest, shell test or CI run was performed, in this pass or the earlier one.
- Only the minimal snapshot was inspected. `repo_files.py` and its nested-repository handling were not re-read for this question. CI configuration and deployed or installed versions are outside the evidence.
- Behavior for nested `local` directories below a root is unverified (see Findings).
- Revalidate if the snapshot commit or runner hash changes.
