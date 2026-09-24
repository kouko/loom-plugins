---
name: parallel-acceptance-testing-and-review-costs-more-than-it-saves
description: Starting the acceptance tester and the Round 1 reviewers together, then resuming the same reviewers with the report before their verdict, saves about one minute per round and costs about 30% more, because the saving and the cost come from the same resumed context; reviewers must keep reading the acceptance test report, so a variant earns a trial only with a saving well above a minute or a cost-neutral resume
type: practice
sources:
  - resource: PR #50 (feat/2026-09-24-parallel-acceptance-testing-and-review), closed unmerged 2026-09-24
  - resource: a scratch trial, 2026-09-24 — three real-size pairs on #49's Build hand-off, new closing review against the old one
---

PR #50 changed closing review so the acceptance tester and the Round 1
reviewers start together. Each reviewer read the change first; once the
report was committed, the same reviewers were resumed with the report
delta and only then gave their verdict. It was measured and closed
unmerged.

Evidence:

- **History, 17 real closing-review episodes.** Reviewers waited a median
  of ~12 min for acceptance testing; 2 of 17 episodes paid an extra round
  because testing and review ran as separate batches.
- **Reviewers catch report errors.** Across that history reviewers found
  8 important errors inside acceptance test reports; 7 were invisible to a
  reader of the report alone.
- **Real-size paired trial, n=3.** Skill load to last verdict: 5m05 new
  against 5m31 old, inside the run-to-run noise (the tester alone varied
  2m36-5m07). Tester return to last verdict: 54 s against 116 s — the
  real effect, about one minute. Cost: USD 3.05 against 2.35 (+30%);
  tokens +47%. About two thirds of the extra came from each reviewer's
  resumed leg re-reading its whole first leg, about one third from extra
  orchestrator turns.

**Why:** the minute saved and the extra cost are one mechanism — a resume
that carries the full first-leg context. The saving cannot be kept without
the cost, and for a user who prioritises cost one minute does not buy
+30%. Dropping the reviewers' read of the report instead would remove the
check that caught 7 errors no report reader could see.

**How to apply:** do not re-propose parallel acceptance testing and review
in this shape. Reviewers keep reading the committed acceptance test report
before their verdict. A future variant must show, on a real-size change, a
saving well above ~1 min per round or a resume that is cost-neutral.
Related: [[same-reviewer-delta-confirmation-dies-at-a-context-compaction]].
