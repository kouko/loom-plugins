# Close the two station-text gaps the Build and closing-review dogfood found
originator: kouko
kind: engineering
needs-design: no — this rewords existing Build and closing-review station prose; it touches no configured interface surface, and the review-round states it relies on are already defined by the closing-review contract
status: confirmed 2026-09-15
publication: automatic — authorized 2026-09-15 by kouko

## Problem
A blind dogfood of the loom-code 3.5.0 Build and closing-review stations —
fresh agents reading only the installed station text, graded by two blind
auditors — found two paths where the text leads an orchestrating agent wrong
or leaves it right only by guessing:

- After a fix made inside Build (a failing end-of-Build check or an adversary
  finding), the text never says to run the complete package suite and the
  adversarial programs again; its re-run rule fires only when closing review or
  a failed `finalize-review` returns the change. The agents re-ran by inference;
  a hurried agent can hand reviewers content the checks never saw.
- When `finalize-review` fails after a clean review round and the next round is
  Round 3, the agent inserted Round 3's technical design re-look — an unneeded,
  behaviour-changing step for a mechanical failure. Both auditors flagged it.

Build also never says which command is the complete package suite; a narrower
guessed command can pass at the end of Build and then fail in
`finalize-review`, spending a review round.

Every Loom change run in this repository pays these costs: extra rounds and
time, or reviewers reading untested content.

## Proposed outcome
A fresh agent reading the station text re-runs every mechanical check after
any fix, treats the round after a failed `finalize-review` as fix verification,
and runs the repository's declared suite command — without the station text
getting longer overall.

## Acceptance
1. The Build station text requires that after every fix made during Build — whether prompted by a failing end-of-Build check, an adversary finding, or a change returned by closing review or `finalize-review` — the complete package suite runs and the existing adversarial programs run again before hand-off, without dispatching the adversary again.
2. The closing-review station text makes the review round after a failed `finalize-review` a fix-verification round, and requires a technical design re-look only when its stuck rule applies (which still includes Round 2 ending with blockers), not merely because that round is Round 3.
3. The Build station text names the command the repository declares as `package-tests` as the complete package suite command.
4. Fresh agents given only the updated station text and the dogfood scenarios S2 and S3 (Build) and S7-a (closing review) re-run both checks after the fix without listing that as a guess and insert no technical design re-look after a finalize failure; a blind auditor grades all three scenarios CONFORMS.
5. The combined word count of the Build and closing-review station files does not increase.
6. The repository's package test suite passes, the mechanism check against the trunk reports no net increase, and no checker code changes.

## Constraints
- No change to checker code, attestation validation, or push validation.
- No new counted mechanisms; existing gate ids stay.
- When Round 2 ends with blockers, a technical design re-look still precedes Round 3.

## Out of scope
- The other dogfood findings (001–004, 007–009, 011–013), including defining "blocker".
- The missing attack-catalogue reference.
- A checker-run, content-bound mechanical result reused by `finalize-review`.

## Open questions
- none
