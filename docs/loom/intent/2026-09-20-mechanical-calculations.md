# 2026-09-20-mechanical-calculations
originator: kouko
kind: engineering
needs-design: no — the change is inside the checker and Loom station contracts, neither of which is a configured interface surface
status: confirmed 2026-09-20
publication: automatic — authorized 2026-09-20 by kouko

## Problem

Every Loom change currently pays for a full specification, plan, and blind run even when its complete branch diff contains only a low-risk intent, documentation, and tests. The maintainer must also type a step-selection confirmation before those stations can be omitted. That makes a small documentation or test-only change slower than its risk requires.

## Proposed outcome

The checker computes the ritual scale from the complete branch delta. A narrow, mechanically low-risk delta automatically omits specification, plan, and blind-run work without a typed confirmation; broader or uncertain deltas retain the full ritual. An explicit user selection still overrides the automatic result.

## Acceptance

1. The checker classifies a complete branch delta as narrow only when every changed path is this change's intent, its Loom evidence, a test file, or a low-risk document outside `docs/loom/`; production code, protected surfaces, interface surfaces, unsafe paths, and unknown file types keep the full ritual.
2. With no bound user selection, `selection show <change-id>` reports `spec`, `plan`, and `blind-run` as skipped for a narrow delta, and the write-spec, write-plan, and blind-run stations omit only those steps.
3. With no bound user selection, an empty, unknown, broad, mixed, or unreadable delta reports no automatic skips and retains the full ritual.
4. A bound user selection determines the effective steps; automatic classification cannot add to or remove from the steps the user selected.
5. Narrow classification does not skip `adversarial`, `package-tests`, reviewer evidence, publication checks, or any other mechanical gate.
6. The write-plan contract no longer requires a plan artifact when `selection show` lists `plan` as skipped, while it still requires one for all other changes.
7. A fresh-context blind run of a narrow documentation-or-test change confirms that no specification, plan, or blind-run station was needed and that all remaining gates passed.
8. The repository package test suite passes, and the mechanism check against the trunk reports no net increase in counted mechanisms.

## Constraints

- The complete branch delta includes committed, staged, unstaged, and untracked functional paths; host plumbing remains excluded exactly as `changed_paths` defines today.
- The reviewer floor, fresh-context reviewer independence, writer-not-judge separation, and checker-executed evidence remain unchanged.
- No change to `finalize-review`, attestation validation, push validation, reviewer models, reviewer effort, or the three-content-version closing-review limit.
- No change to `PRINCIPLES.md`; this changes mechanical routing, not the evidence threshold for publication.

## Out of scope

- Changing which files count as tests or low-risk documentation beyond the existing reviewer-floor allowlist.
- Skipping `adversarial`, package tests, reviewers, or publication safety for narrow changes.
- Reusing mechanical evidence between separate content versions.
- P1's consolidation of PR #30 adversarial tests.
- The pending branch-fate decisions and the dotfiles permission-list change.

## Open questions

- none
