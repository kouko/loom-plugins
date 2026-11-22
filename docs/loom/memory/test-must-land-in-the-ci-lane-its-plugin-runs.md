---
name: test-must-land-in-the-ci-lane-its-plugin-runs
description: A new test only gates if it lands in a lane CI actually runs — loom-family CI runs `python3 scripts/run_package_tests.py --loom-family --only <group>` over the TEST_ROOTS it names (skipping each root's local/ folder), the group is chosen by test TYPE (every shell test runs in loom-workflow CI's workflow-shell group), and a guarded path triggers the test only if it is in that workflow's paths:; a test dropped outside those lanes is a dark test that passes locally and never gates
type: gotcha
sources:
  - resource: PR closeout-privacy-gate (2026-07-19) — caught twice at plan + execution time
---

CI does not glob every test file in the repo. The loom-family workflows
run `python3 scripts/run_package_tests.py --loom-family --only <group>`,
which collects only the test roots in its `TEST_ROOTS` constant and skips
each root's `local/` folder.
A test placed next to the code it tests (in `scripts/` or a skill folder)
runs locally and is a real dev-time check, but it **never gates in CI**.

Dated example (2026-07-19), the lanes as they stood then, kept verbatim:

Two different plugins in this repo run their CI test suites two
different ways, and neither globs everything:

- **dev-workflow** (`.github/workflows/dev-workflow-ci.yml`) runs ONLY
  `for t in dev-workflow/tests/test-*.sh; do bash "$t"; done`. There is
  **no pytest job anywhere in CI** that covers `dev-workflow/skills/**`.
  A `test_*.py` co-located next to a skill script (mirroring
  distill-sessions) runs locally and is a real dev-time suite, but it
  **never gates in CI**. To gate a `dev-workflow/skills/` behavior, add
  a bash CLI test under `dev-workflow/tests/test-*.sh` that exercises the
  real script (exit codes / output), not only a pytest.
- **loom-code** (`.github/workflows/loom-code-ci.yml`) runs
  `pytest loom-code/tests/ tests/`; the gating lane for a SKILL.md
  prose pin is a `loom-code/tests/test_*.py` pytest (precedent:
  `test_finishing_merge_path_guidance.py`).

Caught twice in one arc: a plan first routed finishing-SKILL pins to
`loom-code/tests/*.sh` (dark) → moved to `loom-code/scripts/test_*.py`;
and a `privacy-scan.py` pytest had no CI gate → added a paired bash CLI
test under `dev-workflow/tests/`.

(Note 2026-11-21: that arc, 2026-07-19, ran under the CI lanes of that
time; dev-workflow and those per-plugin lanes are no longer in this repo.)

**Why:** "the test passes locally" and "the test gates in CI" are
different claims. A dark test gives false regression confidence — the
behavior it guards can break on main with a green check. Test *type*
(pytest vs bash) is not a free choice; it is dictated by which lane
CI actually executes for that type.

**How to apply:** before choosing a new test's type + location, check two
things:

1. **Find the workflow that actually runs the test's TYPE**, not just the
   target plugin's own workflow: `grep -n -- '--only' .github/workflows/*.yml`.
   As of 2026-11-21: `code` in loom-code-ci.yml, `design` in
   loom-design-ci.yml, and `workflow-python`, `workflow-shell` and the
   separate `workflow-mermaid` validator group in loom-workflow-ci.yml.
   `workflow-shell` runs every `test-*.sh` under every `TEST_ROOTS` root
   (`scripts/run_package_tests.py`), so a shell test for ANY plugin —
   loom-code included — gates only in loom-workflow CI; verify that group
   name in `.github/workflows/loom-workflow-ci.yml` before relying on it.
2. **Check that workflow's `pull_request:` and `push:` `paths:` filters.**
   A workflow starts when any changed file matches them, so the test
   guards a path only when that path is listed in the `paths:` of the
   workflow whose group runs the test. When an edit to the guarded path
   alone must trigger the test, list that path there (for example,
   loom-workflow-ci.yml lists `loom-code/tests/**` but not
   `loom-code/scripts/**`, so a loom-code shell test does not run on a
   change to `loom-code/scripts/` alone).

Place the test where both hold (for example a loom-code SKILL.md prose
pin as a pytest under `loom-code/tests/`). Dated examples, 2026-07-19:
the arc above used the per-plugin commands of that time — pytest under
`loom-code/scripts/test_*.py` for loom-code and a bash CLI test under
`dev-workflow/tests/` for dev-workflow. (Extends
[[gha-paths-filter-gates-at-workflow-level]]: that entry is about which
*pushes* trigger a workflow; this is about which *tests* a triggered
workflow actually executes.)
