# Acceptance testing and the first reviewers run on the same version at the same time
originator: kouko
kind: engineering
needs-design: no — closing-review station prose and the reviewer and acceptance-tester agent contracts; skill/gate artifacts, not interface surfaces under the manifest globs
status: confirmed 2026-09-24
publication: automatic — authorized 2026-09-24 by kouko

## Problem
Closing review today runs independent acceptance testing first, commits its
report, and only then lets the reviewers start, because the report is part of
what the reviewers must read. Every change waits for acceptance testing
before any reviewer begins, and when acceptance testing finds a problem, it
is fixed and re-tested before the reviewers ever see the change, so the
reviewers' own findings arrive a round later. Session history (2026-09-24,
17 real closing-review episodes) shows a median wait of about 12 minutes
between the acceptance test result and the first reviewer starting, and 2
episodes where the two reported in separate batches and paid an extra fix
round. The reviewers' reading of the report cannot simply be dropped: in the
same history reviewers caught 8 important errors inside acceptance test
reports, 7 of which a user reading only the report could not have noticed.

## Proposed outcome
Acceptance testing and the first-round reviewers start on the same version at
the same time; the same reviewers still read the acceptance test report
before they give their verdict, inside the same round; and the findings from
both reach one fix round together.

## Acceptance
1. In closing review, the acceptance tester and the first-round reviewers start on the same version, and the reviewers begin reading the change without waiting for the acceptance test report.
2. The same reviewers read the committed acceptance test report and its evidence file before giving their verdict, in the same round, so the report is still reviewed and committing it causes no extra review round.
3. Findings from acceptance testing and from the reviewers on that version reach the fix round as one list.
4. The acceptance test report the user reads at acceptance still states, one row per Acceptance line, what was tried and the result.
5. Given a trial change run through closing review with both steps, the time from the start of closing review to the reviewers' verdicts is shorter than running acceptance testing and then the reviewers one after the other, shown by a trial run.
6. The checker's rule list does not grow and no new step, reviewer or dispatch is added.

## Constraints
- No new checker rule, no new flow step, no extra agent dispatch.
- The writer ≠ judge split is unchanged: the acceptance tester and the reviewers are fresh-context agents that did not implement the change.
- Findings from both reach Build through the grouped hand-off added on 2026-09-24.

## Out of scope
- Dropping the reviewers' reading of the acceptance test report.
- Changing when acceptance testing is skipped (narrow changes, user skips).
- Making acceptance testing itself lighter or heavier.
- Running later-round re-tests and fix-verification reviews in parallel.

## Open questions
- none
