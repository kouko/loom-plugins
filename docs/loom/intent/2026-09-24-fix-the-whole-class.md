# Fix rounds fix the whole class of a finding, not only the flagged instance
originator: kouko
kind: engineering
needs-design: no — closing-review and build station prose that tells the orchestrator how to scope a fix; skill/gate artifacts, not interface surfaces under the manifest globs
status: confirmed 2026-09-24
publication: automatic — authorized 2026-09-24 by kouko

## Problem
After closing review or independent acceptance testing flags a defect, the
fix that follows usually repairs exactly the place the finding names. When
the same defect also sits in other places the change touched, those siblings
survive, a later review round finds them, and the change pays for one more
fix round, one more acceptance re-run and one more pair of reviewers. A
survey of 71 recorded loom changes across 6 repositories (2026-09-24) found
this visible in 18 of them (25%); it is the largest avoidable cause of extra
rounds the survey could attribute, ahead of acceptance testing and reviewers
reporting in separate batches (12 changes). On the rename change of
2026-09-23 it cost one extra round: the first fix renamed one of four
pull-request lines the same Acceptance line named, and the other three were
found and fixed one round later. Each extra
round costs roughly 300–400k tokens and 15 minutes.

## Proposed outcome
When a finding is fixed, the fix covers every place in the change where the
same defect occurs, so a later round does not find the flagged defect's
siblings.

## Acceptance
1. Before a fix is handed to an implementer, the orchestrator names the defect's class and searches the whole change for other instances of it — including every surface named by the Acceptance line the finding maps to — and the fix hand-off lists every instance found, the flagged one included.
2. The fix's record (its hand-off and commit message) states the class and the places searched, so a reader can see siblings were looked for even when none were found.
3. Given a finding that names one instance while siblings of the same defect exist elsewhere in the change, an agent following the station text produces a fix hand-off that covers the siblings, shown by a trial run on such a case.
4. The rule is carried by station prose; the checker's rule list does not grow and no new step, reviewer or dispatch is added.

## Constraints
- No new checker rule, no new flow step, no extra agent dispatch; the gate budget stays as it is.
- The writer ≠ judge split is unchanged: the orchestrator scopes the fix, an implementer makes it, fresh reviewers judge it.

## Out of scope
- Refusing to defer nits that map to an Acceptance line (evidence too thin: 2 recorded cases).
- Running acceptance testing and reviewers in parallel on the same version.
- Why reviewers find new problems in later rounds (a separate survey).

## Open questions
- none
