---
name: folding-a-pre-existing-hole-into-a-change-multiplies-its-probe-surface
description: A pre-existing defect folded into a change because the change "makes it reachable" is not a small addition — the fix enters the adversarial pass as part of the change, every finding it produces earns a permanent probe, and the probe surface grows with the fix rather than with the requirement; decide the fold before Build, and when the budget is not there take the whole change without it rather than half of it
type: decision
sources:
  - resource: branch 2026-09-18-blocked-publish-names-the-legal-routes — a 42-line requirement (a refusal naming routes that work) shipped as 4,815 insertions and 45 deletions across 15 files; of thirteen adversarial findings, six came from the folded fix rather than from the requirement, and the adversarial module reached 1,961 lines against roughly 30 lines of message logic
---

The change's requirement was one sentence of checker output: when publication
is refused, name what the agent can do next instead of leaving it nothing but
handing the command to the user. Verifying that the named routes actually work
surfaced a separate, pre-existing defect — a user-typed skip could reach a
pull request undisclosed on one of the two routes that open one.

Folding that fix in looked like a small addition, and was argued for on solid
grounds: the corrected refusal steers an agent toward binding a skip at the
moment it opens a pull request, so the change pointed materially more traffic
at the hole, and the intent's own Constraints required every skip to be
disclosed. The reasoning held. The cost estimate did not.

**Why:** a folded fix does not arrive alone. It enters the adversarial pass as
part of the change, so it is attacked as hard as the requirement is, and each
finding it produces earns a permanent regression probe by this repository's own
rules. Here the fix produced five further findings of its own, each closed and
each leaving probes behind, and two of those fixes produced findings in turn.
The probe surface tracked the fix, not the requirement. Review cost followed:
the closing review returned NEEDS_REVISION twice, and both rounds' heaviest
findings were against the folded work rather than against the sentence.

The fold is also the point where the estimate is cheapest to make and the
decision cheapest to reverse. Once the branch carries commits that test both
halves through shared fixtures, splitting costs more than it saves, and the
code ships either way — only the pull request gets smaller.

**How to apply:** when verification of a requirement surfaces a pre-existing
defect, decide the fold before Build and state the cost in the plan's Risks,
not after the adversary has already attacked it. Ask what the fix's own
adversarial surface is, not only what the fix is: a fix that reads a new input,
parses a new command shape, or adds a state-dependent branch will be attacked
on each of those, and each attack that lands becomes a probe this repository
keeps forever. When the budget for that is not available, file the defect as
its own intent carrying the evidence that this change is what makes it worth
fixing — and take the whole change without the fold rather than a partial one,
because a half-closed hole earns trust it has not got.

**Decided by the user on 2026-09-18**, against the alternative of splitting the
branch so that only the requirement shipped here: ship with the follow-up
recorded. The split was offered with its cost — by then the branch's commits
tested both halves through shared fixtures, so splitting cost more than it
saved and the code would ship either way — and declined on that basis. The debt
below is therefore someone's call, not an oversight.

**Follow-up this branch owes:** the probe count grew to roughly ten cases per
finding, and nobody pruned it. A later change should measure which probes are
redundant — several findings carry a reproduction, a control, and a
strengthened variant that assert overlapping facts — and remove what does not
earn its line, without removing the probes that record a real defect. That is a
measurement task, not a judgement call, and it belongs in its own intent rather
than in the branch that created the surplus.
