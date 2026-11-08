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
- The package preset is selected by `--loom-family` (lines 153–167). Its `code` group includes the first two roots and calls `_tests_session` (lines 124–128). That helper excludes the root's `local/` while checking for tests and adds `--ignore=<absolute local path>` when present (lines 76–85). Consequently, `tests/local/` is excluded from this preset's Python collection. Shell discovery likewise excludes each root's direct `local/` subtree (lines 88–95). Design and workflow Python paths also exclude their root-level `local/` directories (lines 99–114, 129–132).
- [Test definitions](../../../src/tests/test_run_package_tests.py), lines 222–235, 285–310, assert the root list and exclusion of Python and shell files under `tests/local/`. These definitions were read, not run.
- The exclusion is preset-specific: the alternate explicit-argument mode forwards each group directly to pytest without adding these ignores (runner lines 168–176). This finding does not establish exclusion for bare pytest or explicitly targeted local tests.

The inspected runner and test file SHA256 values, measured with `shasum -a 256`, match their entries in provenance: `6730a53e11d862d5d3d93eadcdafb2011b81f2595332e4a57ae49a504f660d54` and `b7ed3d4e19fd4d03c68df5d8ca796d03442a859874745564c20ddaeb7780da28`, respectively.

## Continuation (2026-11-08): does ordinary `--loom-family` run `tests/local/` Python and shell tests?

Same question and same source snapshot (commit `d5a7f0da…` per provenance); no new experiment. Earlier evidence was reused after re-reading the runner (`src/scripts/run_package_tests.py`) and the relevant test definitions, which also corrected a few off-by-one line anchors above.

- **Answer: no, for the ordinary preset (no `--only`, or `--only code`/`workflow-shell`).**
  - Python: the `code` group builds its targets with `_tests_session` for `tests` and `loom-code/tests` (lines 124–128). A root is a target only if tests exist outside `<root>/local`, and `--ignore=<abs root>/local` is added whenever that folder exists (lines 76–85). The `design` and `workflow-python` groups apply the same pattern to their `local/` folders (lines 129–132, 98–113).
  - Shell: `_shell_tests` takes `test-*.sh` under each `TEST_ROOTS` entry and drops any whose parents include `<root>/local` (lines 88–95); `loom_family_commands` uses it for the `workflow-shell` group (lines 134–138).
  - Test definitions (`src/tests/test_run_package_tests.py` lines 222–235, 286–298) assert that a Python test and a `test-z.sh` under `tests/local/` are not collected or commanded. Read only, not run.
- **Narrow boundaries (source-read):** only a `local/` directly under a root is excluded. A `local` folder nested deeper (for example `tests/foo/local/`) is not excluded by these checks. Explicit-argument mode (without `--loom-family`) and direct pytest or `bash` invocations are not covered by the exclusion.
- **Harness observations:** [fixture-observations.json](../../../fixture-observations.json) records prior local `git` queries and SHA256 values (runner `6730a53e…0d54`, test file `b7ed3d4e…da28`, the earlier record `c54f2872…1283`) taken before this turn, plus a clean ancestry of `research-fixture` in `main`. I did not run these commands or re-hash any file this turn; the runner and test hashes agree with [provenance](../../../provenance.json) as recorded, and the observations are not treated as a runtime test.
- **Not verified:** no runner, pytest, or shell command was executed, so actual collection on a real checkout is untested. The earlier record's hash was taken before this edit, so it no longer describes this updated file.

## Decision impact

Do not place tests intended for ordinary package coverage in `tests/local/`. A new standalone plugin test root is not automatically discovered: it must be added to `TEST_ROOTS`; otherwise use an existing listed root outside its excluded `local/` subtree, subject to the runner's normal discovery rules.

## Limitations and open questions

This is a source-supported conclusion, without runtime validation. CI configuration and deployed or installed versions are outside the supplied evidence; no claim is made about them. No material uncertainty remains for the inspected runner's root list and preset exclusion, beyond the runtime and nested-`local/` caveats noted in the continuation.
