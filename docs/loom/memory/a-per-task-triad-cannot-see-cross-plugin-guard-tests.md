---
name: a-per-task-triad-cannot-see-cross-plugin-guard-tests
description: A per-task check that runs only the task's own test file (2026-08 the SDD triad, since retired; today an implementer's focused test command) is blind to guard tests elsewhere, so a guard test that asserts an invariant about an EDITED file but lives in a DIFFERENT plugin's test directory is invisible to both the implementer and the per-task spec/code-quality reviewers — the complete package suite at the end of Build and closing-review's branch-end reviewers are the safety net; on multi-plugin branches, cross-plugin guard tests are the recurring shape that per-task review structurally cannot catch
type: practice
sources:
  - resource: 2026-08-15 plain-relay-contract arc — T10 (8bc0f516) dedup'd the brief-before-fork trigger in brainstorming/SKILL.md but over-stripped a distinct sibling rule; the guard test (loom-pipeline/scripts/test_family_relay.py::test_brainstorming_fork_table_default) lives in a different plugin's test dir and was never run by T10's triad, so both T10 reviewers returned PASS saying "no over-stripping" while the test was RED
---

SDD's per-task triad runs the task's own test file (the RED→GREEN
test the implementer wrote for that task). It does not run the rest
of the suite. A guard test that lives in a *different plugin's* test
directory — asserting an invariant about a file this task edits — is
therefore invisible to the implementer, the spec-reviewer, and the
code-quality-reviewer alike. All three can return PASS on a change
that is actively breaking a guard test in another plugin's dir.

On the plain-relay-contract branch, T10 replaced the
brief-before-fork paragraph in `loom-code/skills/brainstorming/SKILL.md`
with a dedup pointer. The paragraph held three distinct rules; T10
correctly dedup'd two (the trigger + the stakes-first framing) but
over-stripped the third (the "render ≥2 options as a markdown
comparison table" default, governed by family-relay.md §Family relay
discipline). The guard —
`loom-pipeline/scripts/test_family_relay.py::test_brainstorming_fork_table_default`
— lives in loom-pipeline's test dir, not loom-code's. T10's triad ran
only T10's own test file; both reviewers returned PASS explicitly
stating "no over-stripping." The test was RED the whole time.
Whole-branch review round 2 caught it.

This is structural, not a reviewer lapse: the triad's scope is the
task's test file by design. The safety net is the complete package suite
at the end of Build plus closing-review's branch-end reviewers — never rely on per-task
PASS alone for a change to a file that has guard tests in other
plugins. Before declaring a multi-plugin branch done, grep every
`TEST_ROOTS` entry in `scripts/run_package_tests.py` for assertions naming
the files you edited.

Note 2026-11-21: the SDD triad (implementer, spec-reviewer,
code-quality-reviewer) was retired. Today an implementer runs only its
task's focused test command, and the complete package suite
(`scripts/run_package_tests.py --loom-family`, all `TEST_ROOTS`) runs at
the end of Build and again in closing-review's finalize-review; run it
before closing-review on any branch that edits files guarded from another
plugin's tests.

Pairs with [[a-branch-suite-must-cover-every-touched-plugin-scripts-dir]]
(verify-command blindspot) and
[[dedup-of-one-rule-must-not-strip-a-sibling-rule-in-the-same-paragraph]]
(the over-strip shape this test caught).