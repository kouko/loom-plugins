# Package-suite counts after the move

Measured 2026-09-25 on the branch `refactor/2026-09-25-tests-live-in-tests-folders`
(the closing-review fix-round working tree on top of 78de9aec) with the same
method as `baseline-counts.md`: `uv run --isolated --with-requirements
requirements-package-tests.lock python scripts/run_package_tests.py
--loom-family -q`, which runs one subprocess per command from
`scripts/run_package_tests.py::loom_family_commands`. Every command exited 0.

| Group | Command target | Result |
|---|---|---|
| code | `tests loom-code/tests` (xdist) | 2334 passed, 2 skipped |
| design | `loom-design/tests` | 245 passed, 1 skipped |
| workflow-python | `loom-workflow/tests` (top level) | 53 passed |
| workflow-python | `loom-workflow/tests/decision-map` | 261 passed |
| workflow-python | `loom-workflow/tests/distill-sessions` | 121 passed |
| workflow-python | `loom-workflow/tests/git-memory` | 64 passed |
| workflow-python | `loom-workflow/tests/goal-create` | 43 passed |
| workflow-python | `loom-workflow/tests/handoff` | 13 passed |
| workflow-python | `loom-workflow/tests/independent-advisor` | 1 passed |
| workflow-python | `loom-workflow/tests/loom-memory` | 80 passed, 3 skipped |
| workflow-python | `loom-workflow/tests/loom-visualization` | 209 passed |
| workflow-python | `loom-workflow/tests/recap-state` | 12 passed |
| workflow-python | `loom-workflow/tests/scripts` | 196 passed |
| workflow-shell | 17 `test-*.sh` scripts found under the four test roots (all in `loom-workflow/tests/`) | 145 PASS / 0 FAIL in total |
| workflow-mermaid | `npm ci` + `validate_mermaid.mjs` + negative check | pass |

Totals: pytest 3632 passed, 6 skipped (code 2334/2, design 245/1,
workflow-python 1053/3); shell 145 PASS.

## Before and after

| Group | Before | After | Difference |
|---|---|---|---|
| code | 2271 passed, 2 skipped | 2334 passed, 2 skipped | +63 passed |
| design | 245 passed, 1 skipped | 245 passed, 1 skipped | 0 |
| workflow-python | 1052 passed, 3 skipped | 1053 passed, 3 skipped | +1 passed |
| pytest total | 3568 passed, 6 skipped | 3632 passed, 6 skipped | +64 passed |
| workflow-shell | 145 PASS | 145 PASS | 0 |
| workflow-mermaid | pass | pass | — |

## Where every difference comes from

The difference was computed, not estimated: every pytest command was run with
`--collect-only` at the baseline commit 23dad634 and on the W1-01 tree, and each
collected test was keyed by its file basename plus test name (a move changes
the folder, not the key). No baseline test is missing after the move. The
closing-review fix round then removed only tests this change had added (none
of the removed test names exists at 23dad634) and added the ones listed below.
64 tests are new, and each one is listed here.

| Group | File | Tests | Why it is new |
|---|---|---|---|
| code | `loom-code/tests/test_build_recovery_rules.py` | +8 | was `loom-code/skills/build/probes/`, never collected before |
| code | `loom-code/tests/test_closing_review_recovery_rules.py` | +13 | was `loom-code/skills/closing-review/probes/`, never collected before |
| code | `loom-code/tests/test_ship_guidance_presence.py` | +2 | was `loom-code/skills/ship/probes/`, never collected before |
| code | `tests/test_run_package_tests.py` | +5 | W0-01 discovery per group (code, design, workflow subfolders: 3); fix round: a `test-*.sh` under any test root runs and `tests/local/` does not (1), `TEST_ROOTS` are exactly the folders the pytest groups run (1) |
| code | `tests/test_tests_folder_convention.py` | +7 | W1-01 guard: AGENTS.md states the convention, CI path filters cover the test folders (and a negative case), CI runs the inventory's groups, no old test path in AGENTS.md or the workflows (and a negative case); fix round: the workflow that runs the shell group is triggered by every test root (1) |
| code | `tests/test_tests_folder_convention.py` | +28 | W1-03 and fix-round repo-wide guard: no test file outside the four test roots or `docs/loom/` (1); 19 planted strays refused (root `scripts/`, `.claude/hooks/`, a plugin `hooks/`, a new plugin's `contract/` and `scripts/`, a tests folder under root `scripts/`, `.claude/hooks/`, a plugin `hooks/` or a skill, a new plugin's `tests/` not in `TEST_ROOTS`, and the nine cases the deleted per-plugin and root-level guards covered); 7 planted tests allowed (root `tests/`, `tests/hooks/`, a loom-design station folder, a loom-workflow skill shell test, a loom-code subfolder shell test, a `tests/local/` shell test, `docs/loom/` evidence), each allowed shell test outside `local/` also shown to be run; a stray is refused without git (1) |
| workflow-python | `loom-workflow/tests/test_plugin_manifest.py` | +1 | was `loom-workflow/.claude-plugin/`, never collected before |

Reconciliation: code 23 probes + 5 + 7 + 28 = 63; design 0; workflow 1;
63 + 0 + 1 = 64 = 3632 − 3568. The 24 tests the baseline recorded as never
collected (23 skill probes and the loom-workflow manifest test) are all among
them. The skipped counts are the same tests as before (2, 1, 3).

Removed in the closing-review fix round, all added earlier in this change:
the three per-plugin guard modules (`loom-code/tests/test_loom_code_tests_folder.py`,
`loom-design/tests/test_loom_design_tests_folder.py`,
`loom-workflow/tests/test_loom_workflow_tests_folder.py`, 2 tests each) and
the two root-level stray tests in `tests/test_run_package_tests.py`, whose
cases the repository-wide guard now refuses; the planted "new plugin's
`tests/`" allowed case, now refused; and
`test_byte_identity_tolerates_only_the_graduated_dir_line`, with the
graduated-probe comparison restored to strict byte equality.

Workflow-python ran 11 sessions before and 11 after; the per-skill session
counts are identical, and the top-level session grew from 52 to 53 by the
manifest test.

Not collected by the suite, by design: `loom-code/tests/local/` (the four
local-only integration scripts, moved from `loom-code/tests/integration/`);
they were not run for this record.
