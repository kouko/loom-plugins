# Frozen probes that stand red on this branch

Two frozen adversarial artifacts from earlier changes are red on
`docs/2026-09-16-loom-rule-text-consolidation`. Neither red is a
regression: both pin literal sentences by the file they used to live in,
and this change moved those sentences to their new single home. The rules
themselves are still pinned — see "Where the moved rules are pinned now".

Frozen probes under `docs/loom/2026-09-1[45]*/` are read-only history, so
they were not updated to the new locations.

## `docs/loom/2026-09-15-adversary-probe-maintenance/evidence/probes/test_probe_maintenance_abuse.py`

- **7 of 22 red** on this branch (`7 failed, 15 passed`); **0 of 22 red**
  at the branch base `dec4e927`.
- Red: `test_pins_scratch_copy_unmutated_passes`,
  `test_pins_guard_mutation_killed[drop-red-then-reverted]`,
  `test_pins_guard_mutation_killed[added-discard-literal]`,
  `test_adversary_update_defect_relabelled_stale_kept_red`,
  `test_adversary_update_old_case_preserved_required`,
  `test_adversary_reuse_implementer_tests_excluded_from_floor`,
  `test_cross_docs_roles_consistent_holds`.
- Cause: the literals it mutates moved from `loom-code/agents/adversary.md`
  to `loom-code/skills/closing-review/references/adversarial.md`. The probe
  looks for them in `adversary.md`, finds none, and fails on its own
  "mutation anchor not unique" assertion before it can mutate anything.

## `docs/loom/2026-09-15-mechanical-checks-before-review/evidence/probes/test_text_pins_mutation.py`

- **5 of 10 red** on this branch (`5 failed, 5 passed`); **3 of those 5
  were already red** at the branch base `dec4e927` (`3 failed, 29 passed`
  for both files together there).
- Already red at base: `test_harness_unmutated_green`,
  `test_guards_weakenedprose_killed[build-escape-sentence-hands-off-before-suite-finishes]`,
  `test_guards_weakenedprose_killed[build-fix-loop-suite-made-optional]`
  — anchors in `loom-code/skills/build/SKILL.md` that a change before this
  branch reworded.
- New on this branch (2):
  `test_guards_weakenedprose_killed[reviewer-suite-ban-scoped-to-round-1]`
  and
  `test_guards_weakenedprose_killed[reviewer-skipped-changed-test-no-longer-a-finding]`
  — their anchors moved from `loom-code/agents/reviewer.md` to
  `loom-code/skills/closing-review/references/lenses.md`.

## Where the moved rules are pinned now

Moving a sentence did not unpin its rule. Every rule named above is still
enforced by live tests that this branch runs:

- The complete package suite (`- package-tests:` in
  `docs/loom/KICKOFF-DEFAULTS.md`), which covers
  `loom-code/scripts/test_reviewer_mechanical_evidence.py` (the reviewer /
  lenses rules) and the adversary-contract tests.
- This change's own adversarial probe
  `docs/loom/2026-09-16-loom-rule-text-consolidation/evidence/probes/moved_pin_mutation.py`,
  which re-runs the moved-literal mutations against the files the rules
  now live in.

## No CI gate reads these files

`scripts/run_package_tests.py` — the single inventory the repo's test
groups are selected from — collects `loom-code/scripts/`, `scripts/`,
`.claude/hooks/`, `loom-design/scripts/` and the `loom-workflow` test
directories. It never collects anything under `docs/`, so neither frozen
probe is run by the package suite or by CI. They are read by hand, by a
reader asking what an earlier change proved.
