---
name: a-probe-outpaced-by-scope-growth-needs-a-maintainer
description: An adversarial program written for one scope becomes a wrong oracle once Build widens that scope, so someone must be allowed to update it with mutation evidence before hand-off.
type: gotcha
sources:
  - resource: change 2026-09-15-closing-review-station-name (PR #19)
---

Build requires every committed adversarial program to pass before hand-off,
forbids the adversary from fixing what it breaks, and forbids re-dispatching
the adversary at the end of Build. When the adversary's own findings widen the
change's scope, a probe written for the earlier scope can contradict the widened
change: in PR #19 one probe demanded a capitalised `Review` be renamed while
another demanded that undoing only the original phrase restore the base text,
so no honest wording passed both. No role was authorised to update the probe.

On Claude Code in auto mode, the host's safety classifier also refused to let an
agent run or commit a probe file another agent had edited ("Security Test
Removal", "CI Bypass" — labels as reported by the refused agents), so the maintainer had to run and commit it by hand.
A single mutation that turned RED was then taken as proof the edit did not
weaken the probe; review found a global substitution plus case-insensitive
comparison that still let a lowercase `review` become `closing-review`
unnoticed.

**Why:** a stale probe forces either a dodge (rewording the product to satisfy
the oracle instead of the intent) or an unreviewed test edit, and one passing
mutation says nothing about the mutation classes it did not try.

**How to apply:** when Build widens scope after the adversary ran, treat the
probe update as its own reviewed task: make every reversal exact and
case-sensitive, extend the probe to every newly changed file, and prove
tightness with one mutation per risk class (the widened-scope rename, an
unrelated word, a generic-word substitution) — not one mutation overall. Run
each mutation against the committed probe itself, not a copy of its logic: in
PR #19 the per-class proof ran on a standalone copy, which is the vacuity that
`a-mutation-test-must-run-the-production-assertion` warns about.
Until Loom assigns that maintenance to a role, expect the host classifier to
route the run and commit to the maintainer.

Note: the store charter still names `environment-gotchas.md` as the home for
harness friction, but that file no longer exists in this repository, so this
entry records the classifier half here.

Related: [[a-graduated-probe-that-pins-a-fact-of-the-moment-goes-red-at-the-next-change]]
(a different mechanism — a fact of the branch-moment going stale across
changes, not authorization to update after Build widens scope within one
branch; both are probe-staleness gotchas), [[a-probe-that-pins-a-manifest-block-as-a-literal-breaks-when-a-line-is-inserted-inside-it]]
(a different mechanism again — a literal-text match breaking on an unrelated
insertion, not a scope widening the probe cannot honestly satisfy; both are
"a probe that was correct once breaks for a reason the reviewer must
diagnose before touching the probe").
