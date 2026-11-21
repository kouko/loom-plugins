---
name: test-must-land-in-the-ci-lane-its-plugin-runs
description: A new test only gates if it lands in the exact lane its plugin's CI actually runs — loom-family CI runs scripts/run_package_tests.py over the TEST_ROOTS it names (skipping tests/local/); a test dropped outside those roots is a dark test that passes locally and never gates
type: gotcha
sources:
  - resource: PR closeout-privacy-gate (2026-07-19) — caught twice at plan + execution time
---

CI does not glob every test file in the repo. The loom-family workflows
run `python3 scripts/run_package_tests.py --loom-family`, which collects
only the test roots in its `TEST_ROOTS` constant and skips `tests/local/`.
A test placed next to the code it tests (in `scripts/` or a skill folder)
runs locally and is a real dev-time check, but it **never gates in CI**.

Caught twice in one arc: a plan first routed finishing-SKILL pins to
`loom-code/tests/*.sh` (dark) → moved to `loom-code/scripts/test_*.py`;
and a `privacy-scan.py` pytest had no CI gate → added a paired bash CLI
test under `dev-workflow/tests/`.

(Note 2026-11-21: that arc, 2026-07-19, ran under the CI lanes of that
time; dev-workflow and those per-plugin lanes are no longer in this repo.)

**Why:** "the test passes locally" and "the test gates in CI" are
different claims. A dark test gives false regression confidence — the
behavior it guards can break on main with a green check. Test *type*
(pytest vs bash) is not a free choice; it is dictated by which lane the
target plugin's CI actually executes.

**How to apply:** before choosing a new test's type + location, open the
target plugin's `.github/workflows/*-ci.yml` and check two things:

1. the `--only <group>` its `run_package_tests.py --loom-family` step
   selects (as of 2026-11-21: `code` in loom-code-ci.yml, `design` in
   loom-design-ci.yml, `workflow-shell` and `workflow-python` in
   loom-workflow-ci.yml) — the group decides which `TEST_ROOTS` and which
   test type run (`workflow-shell` runs `test-*.sh`, the others pytest);
2. the workflow's `pull_request:` and `push:` `paths:` filters — the new
   test's path, and the code it guards, must match them, or the job never
   starts for that change.

Place the test where both hold (for example a loom-code SKILL.md prose
pin as a pytest under `loom-code/tests/`). Dated examples, 2026-07-19:
the arc above used the per-plugin commands of that time — pytest under
`loom-code/scripts/test_*.py` for loom-code and a bash CLI test under
`dev-workflow/tests/` for dev-workflow. (Extends
[[gha-paths-filter-gates-at-workflow-level]]: that entry is about which
*pushes* trigger a workflow; this is about which *tests* a triggered
workflow actually executes.)
