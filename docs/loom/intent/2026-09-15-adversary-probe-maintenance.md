# Let the adversary keep its probes current and reuse existing tests first
originator: kouko
kind: engineering
needs-design: no — this changes build-station and adversary agent instructions and their tests; no command, output format, or interface surface a user types into changes
status: confirmed 2026-09-16
publication: automatic — authorized 2026-09-16 by kouko

## Problem
When the adversary's findings make Build widen a change's scope, a probe the
adversary already committed can stop fitting the change. Build requires every
adversarial program to pass before hand-off, the adversary may not fix what it
breaks, and Build may not dispatch the adversary again, so no one is allowed to
bring the probe up to date. In PR #19 this stopped the change twice: the
implementer had to edit the adversary's probe, the host's safety check refused
to let that agent run or commit the edited probe, and the maintainer had to run
and commit it by hand. The edit was then declared "not weakened" on one
mutation, and review later found it had in fact been loosened.

Separately, the adversary always writes new probes: nothing tells it to look at
the probes this change already has, or at the repository's existing tests,
before adding more. Every change therefore adds another batch of probe files,
and the practice has no guard against duplicating coverage that already exists.

## Proposed outcome
When Build widens scope after the adversary ran, the adversary itself updates
its own probes for the new scope and shows, on the committed probe, that the
update did not loosen any check, so the change reaches review without the
maintainer running or committing probe files by hand. Before writing any probe,
the adversary checks what this change's probes and the related existing tests
already cover, and reuses or extends them instead of adding duplicates.

## Acceptance
1. The build station's instructions say what happens when a committed adversarial program no longer fits the widened scope: the adversary is dispatched again to update its own probes, and no other role edits them.
2. The adversary's instructions require every probe update to come with mutation evidence run against the committed probe itself, with at least one mutation per kind of change the update touches, including one that an over-broad update would wrongly accept.
3. In a trial change whose scope is widened after the adversary ran, the stale probe is updated and passes, and the change reaches closing review without the maintainer running or committing any probe file by hand.
4. Before writing probes, the adversary checks this change's existing probes and the repository's related tests, and its report marks each probe as reused, modified, or new, with a reason for every new one.
5. The repository's existing package test suite passes.

## Constraints
- The adversary still never fixes the product it attacks, and an implementer still never edits an adversarial program.
- Build still does not hand off to review until every adversarial program passes or the user has chosen to skip adversarial checks.

## Out of scope
- Restoring the deleted attack catalogue that the adversary instructions still point to.
- Changing the host's safety check or the user's permission settings.

## Open questions
- none
