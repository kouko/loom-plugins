---
name: docs-review-dogfood-must-probe-the-evidence-class-trap
description: A reviewer-contract rule for how findings aggregate into a verdict fails only in behaviour, so probe it with a cold reviewer on a case where the incentive points against it; the original case (2026-07-30) was the retired docs-review evidence-class trap, where an evidence-class survivor had to still pass — no grep pin can catch a misread
type: practice
sources:
  - resource: PR feat-requesting-docs-review-skill (loom-code 0.42.0, 2026-07-30) — dogfood record docs/loom/dogfood/2026-07-30-requesting-docs-review-dogfood.md §D3
---

Grep pins verify the aggregation words exist; only a behavioral probe verifies a
cold reviewer APPLIES them when the incentive points the other way. The designed
trap: hand a round-2 reviewer a remediation where an evidence-class finding was
"fixed" by rephrasing in place (defect survives in new words). The correct
output is simultaneously (a) `not-fixed` on that finding, (b) no re-litigation
as a new differently-worded finding, and (c) a PASSING verdict — because
evidence-class findings never feed the gate, even when the surviving defect is
the round's headline. A reviewer that returns NEEDS_REVISION here has silently
reverted to severity-counting, which is the exact 9-round-loop failure mode the
instruction/evidence split shipped to end.

**Why:** The class-filter semantics are the one part of the docs-review design
that is both load-bearing and invisible to string tests — every other duty
(dimensions, scope, cap wording) pins mechanically; this one only fails in
behavior, and its failure mode looks like diligence.

**Historical procedure (2026-07-30, no longer current):** the retired
requesting-docs-review skill and docs-reviewer agent split findings into
instruction and evidence classes, and the dogfood record's D3 recipe (that
record is no longer in the repo) re-ran this trap before each ship, expecting
not-fixed + no re-litigation + a passing verdict. The `loom-code:reviewer`
docs lens that replaced them has no evidence class, so that expected verdict
is not a rule today.

**How to apply (still applies):** when a reviewer contract changes a rule
for how findings aggregate into a verdict, string pins prove only that the
words exist. Probe it once with a cold reviewer on a case where the
incentive points against the rule, and treat a wrong verdict as a wording
defect — fix the wording, not the reviewer.
