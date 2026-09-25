# Check every plan for a simpler way to reach the same outcome before Build
originator: kouko
kind: engineering
needs-design: no — write-plan station text, a reviewer lens and plan grammar in loom-code; skill/gate artifacts, not interface surfaces under the manifest globs
status: confirmed 2026-09-25
publication: automatic — authorized 2026-09-25 by kouko

## Problem
Agents often propose an implementation that is more complex than the outcome
needs. When the maintainer asks for a complexity check after a proposal, the
agent usually finds a way that reaches the same outcome more simply. loom
never asks this question itself: planning has no review, and closing review
only sees the complexity after it is built, when simplifying means rewriting.
The check therefore happens only when the maintainer remembers to ask, in
sessions where they are present, and never in other projects using loom.

## Proposed outcome
Before Build starts, every plan gets a check from a fresh reviewer whose only
question is whether the same outcome can be reached more simply. The plan
records what simpler shapes were considered and which was taken, so the check
cannot be silently skipped, and it works with loom-code installed alone.

## Acceptance
1. Before Build starts on a change, a fresh-context reviewer that did not write the plan checks it for a simpler way to reach the same Acceptance lines, and returns either no simpler shape or a concrete smaller shape.
2. The plan records the outcome of that check — the simpler shapes considered and whether each was taken or why not — and a plan without that record cannot enter Build.
3. The check needs only loom-code installed.
4. A change the checker judges narrow skips the check, and says so.
5. The check never asks the user a question; adopting or declining a simpler shape is recorded as agent-decided.
6. When the adversary names an existing test as this change's adversarial program, it marks that test with its `concern:` line in the same dispatch, so finalize-review does not refuse the change for a missing line.

## Constraints
- loom-code keeps working without loom-design or loom-workflow.
- At most one extra reviewer dispatch per change.
- The checker blocks Build on a plan without the simplicity record (user-decided 2026-09-25).

## Out of scope
- Checking test complexity (done in the test-budget change).
- A complexity check after Build beyond the existing closing-review dimensions.
- Changing the number of closing-review reviewers.

## Open questions
- none
