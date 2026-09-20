# Record the lesson from an adversarial probe that could not see its own defect

originator: maintenance-loop
kind: engineering
needs-design: no — a documentation-only addition to the repository's own practice-memory store, no command, output format, or interface surface a user types into changes
status: confirmed 2026-09-20
publication: automatic — authorized 2026-09-20 by kouko

## Problem

`2026-09-18-modular-adversary-recipes` (merged as `9bf87029`, PR #33) split the adversary's attack recipes into one file per artifact kind. During that branch's own build, the adversarial probe written to prove the split's `add`/`change`/`locate` properties went through an earlier draft that reported green while it could not have caught the defects that actually existed:

- Its nested run went through the repository's own test runner, which deselects the cases that copy the repository — and those were exactly the cases that required a second file (the routing-table row) to exist. With them deselected, the probe could not see the very defect it was written to test for.
- Its population for "add a kind" was computed as the alphabetically-first unrouted artifact type, which happened to be the one whose name collides with nothing in the shared protocol's prose — the only candidate that could not trigger the name-collision defect that was actually present for other kinds.

Both weaknesses were fixed before the branch merged (the shipped probe now enumerates every unrouted type from the manifest and builds a git-visible copy so nothing needs deselecting). But the defects the flawed probe had missed were not found by reading the probe's code or the diff — they surfaced only when a blind-run reader performed the "add a kind" step for real per the documentation, and separately when the reader redid it choosing a different, independently-picked kind ("plan"), which turned 14 checks red. Nobody wrote down, in the durable practice-memory store, the general shape of this failure: a probe can pick its own population or its own exclusions so that neither one ever exercises the claim it is supposed to be testing.

## Proposed outcome

`docs/loom/memory/` gains one entry recording that a probe which computes its own population, or deselects cases inside its own nested execution, can choose exactly the member or exclusion that never exercises the defect it exists to catch — producing a pass that proves nothing — and that this class of blind spot is caught by executing the real recipe independently (a blind run with a population the writer did not pick), not by reading the probe's code.

## Acceptance

1. `docs/loom/memory/` contains one new entry, filename matching its frontmatter `name` slug, following the store's required frontmatter (`name`, `description`, `type`, `sources`) and body shape (fact, **Why:**, **How to apply:**) exactly as `docs/loom/memory/README.md` specifies.
2. The entry's `description` states the durable, tool-agnostic rule (a probe's self-chosen population/exclusion can dodge the claim it tests) and does not state which specific functions or files currently implement the fix.
3. The entry's body names the two concrete manifestations from `2026-09-18-modular-adversary-recipes` (the deselect-in-nested-run case and the alphabetically-first-population case) as evidence, and states that both were caught by real execution (blind run with an independently chosen instance), not by code or diff reading.
4. The entry's `sources` field points at the originating change (`9bf87029` / PR #33 / `2026-09-18-modular-adversary-recipes`).
5. `python3 loom-workflow/skills/loom-memory/scripts/loom_memory.py validate docs/loom/memory` exits 0 against the updated store, including the regenerated `index.md`.
6. The repository's full package-test command from `docs/loom/KICKOFF-DEFAULTS.md` passes in a clean environment.

## Constraints

- Documentation-only: no change to any adversary probe, recipe file, or checker script. The probes named in the intent are cited as evidence for the memory entry, not modified.
- The memory entry describes the general lesson, not a narration of the specific fixed functions (per the store's own rule that a description must not state which tools currently exist).

## Out of scope

- Re-litigating or re-verifying the `2026-09-18-modular-adversary-recipes` change itself; it already merged and its own attestation stands.
- Any new mechanism, check, or probe enforcing this lesson going forward — this intent only records the practice-memory fact, per the maintain station's guidance that a new mechanism is added only when a deterministic regression test earns its ongoing cost, which does not apply to a documentation fact.
- Any other memory-store entry or cleanup.

## Open questions

- none
