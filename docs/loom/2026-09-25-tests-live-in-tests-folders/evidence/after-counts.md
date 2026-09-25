# Package-suite counts after the move

Measured 2026-09-25 on the branch `refactor/2026-09-25-tests-live-in-tests-folders`
(W1-01 working tree on top of f6a6e017) with the same method as
`baseline-counts.md`: `uv run --isolated --with-requirements
requirements-package-tests.lock` and one subprocess per command from
`scripts/run_package_tests.py::loom_family_commands`. Every command exited 0.

| Group | Command target | Result |
|---|---|---|
| code | `tests loom-code/tests` (xdist) | 2308 passed, 2 skipped |
| design | `loom-design/tests` | 247 passed, 1 skipped |
| workflow-python | `loom-workflow/tests` (top level) | 55 passed |
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
| workflow-shell | 17 `loom-workflow/tests/test-*.sh` scripts | 145 PASS / 0 FAIL in total |
| workflow-mermaid | `npm ci` + `validate_mermaid.mjs` + negative check | pass |

Totals: pytest 3610 passed, 6 skipped (code 2308/2, design 247/1,
workflow-python 1055/3); shell 145 PASS.

## Before and after

| Group | Before | After | Difference |
|---|---|---|---|
| code | 2271 passed, 2 skipped | 2308 passed, 2 skipped | +37 passed |
| design | 245 passed, 1 skipped | 247 passed, 1 skipped | +2 passed |
| workflow-python | 1052 passed, 3 skipped | 1055 passed, 3 skipped | +3 passed |
| pytest total | 3568 passed, 6 skipped | 3610 passed, 6 skipped | +42 passed |
| workflow-shell | 145 PASS | 145 PASS | 0 |
| workflow-mermaid | pass | pass | — |

## Where every difference comes from

The difference was computed, not estimated: every pytest command was run with
`--collect-only` at the baseline commit 23dad634 and on this tree, and each
collected test was keyed by its file basename plus test name (a move changes
the folder, not the key). No baseline test is missing after the move; 42 tests
are new, and each one is listed here.

| Group | File | Tests | Why it is new |
|---|---|---|---|
| code | `loom-code/tests/test_build_recovery_rules.py` | +8 | was `loom-code/skills/build/probes/`, never collected before |
| code | `loom-code/tests/test_closing_review_recovery_rules.py` | +13 | was `loom-code/skills/closing-review/probes/`, never collected before |
| code | `loom-code/tests/test_ship_guidance_presence.py` | +2 | was `loom-code/skills/ship/probes/`, never collected before |
| code | `tests/test_run_package_tests.py` | +5 | W0-01 inventory guards: discovery per group, `tests/local/` skipped, stray root test detected |
| code | `loom-code/tests/test_loom_code_tests_folder.py` | +2 | W0-02 guard: no test left in `loom-code/scripts/` or `loom-code/skills/`, and its negative case |
| code | `loom-code/tests/test_probes_coldread_abuse_coldread_branch_end.py` | +1 | W0-02: `test_byte_identity_tolerates_only_the_graduated_dir_line`, pinning the one line the move let differ from the evidence original |
| code | `tests/test_tests_folder_convention.py` | +6 | W1-01 guard: AGENTS.md states the convention, CI path filters cover the test folders (and a negative case), CI runs the inventory's groups, no old test path in AGENTS.md or the workflows (and a negative case) |
| design | `loom-design/tests/test_loom_design_tests_folder.py` | +2 | W0-03 guard: no test left in `loom-design/scripts/`, and its negative case |
| workflow-python | `loom-workflow/tests/test_plugin_manifest.py` | +1 | was `loom-workflow/.claude-plugin/`, never collected before |
| workflow-python | `loom-workflow/tests/test_loom_workflow_tests_folder.py` | +2 | W0-04 guard: no test left in `loom-workflow/skills/`, `scripts/` or `.claude-plugin/`, and its negative case |

Reconciliation: code 23 probes + 5 + 2 + 1 + 6 = 37; design 2; workflow 1 + 2 = 3;
37 + 2 + 3 = 42 = 3610 − 3568. The 24 tests the baseline recorded as never
collected (23 skill probes and the loom-workflow manifest test) are all among
them. The skipped counts are the same tests as before (2, 1, 3).

Workflow-python ran 11 sessions before and 11 after; the per-skill session
counts are identical, and the top-level session grew from 52 to 55 by the
manifest test and the two guard tests.

Not collected by the suite, by design: `loom-code/tests/local/` (the four
local-only integration scripts, moved from `loom-code/tests/integration/`);
they were not run for this record.
