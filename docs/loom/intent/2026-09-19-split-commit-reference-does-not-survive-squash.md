---
originator: maintenance-loop
kind: engineering
needs-design: no — internal test fixture reference, not an interface surface under the manifest globs
status: confirmed 2026-09-19
publication: automatic — authorized 2026-09-20 by kouko
---

## Problem
`main` fails its own required CI for anyone who clones it fresh. Discovered
while shipping an unrelated change: `loom-code/scripts/test_adversary_recipe_shape.py`
(via `test_adversary_layout.py`'s `_at_split`/`_original` helpers) reads two
commit SHAs recorded in `docs/loom/2026-09-18-modular-adversary-recipes/evidence/rule-correspondence.md`
("at commit `5b8dfdce...`" and "at split commit `50cf9f8b...`") to compare the
pre-split and post-split state of the adversary recipe files. Both SHAs were
intermediate commits on PR #33's own development branch; squash-merging that
PR into `main` as commit `9bf87029` discarded both, so neither exists on the
shared remote. A fresh clone of `main` at `9bf87029` fails 31 of 35 tests in
that one file. A checkout that happens to share a machine with that PR's own
now-superseded local branch can still resolve the SHAs from stray local
objects and passes, masking the break for exactly that machine.

## Proposed outcome
The two recorded commit references name commits that exist on the shared
remote and carry the same pre-split and post-split tree content the tests
already rely on, so the affected tests pass on a genuinely fresh clone of
`main`.

## Acceptance
1. `python3 -m pytest loom-code/scripts/test_adversary_recipe_shape.py -q`
   passes in full on a clone of `main` made independently of any machine that
   worked on PR #33 (no shared git object database).
2. The two commit references recorded in the correspondence document each
   resolve on that same independent clone and still yield the pre-split and
   post-split tree content their respective helper function expects.

## Constraints
- Fix only the stale references; do not change the recipe-split design, the
  routing table, or any recipe file's content.
- No change to the 2026-09-19-loom-flow-recovery-loop branch or worktree.

## Out of scope
- Any change to how future migrations record their commit references (a
  process note, not a mechanism, is enough per this incident's own scale).

## Open questions
- none
