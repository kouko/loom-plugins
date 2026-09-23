# Make acceptance testing lighter without losing what only it catches
originator: kouko
kind: engineering
needs-design: no — acceptance-tester contract, report template and station prose are skill/gate artifacts, not interface surfaces under the manifest globs
status: confirmed 2026-09-23
publication: automatic — authorized 2026-09-23 by kouko

## Problem
Independent acceptance testing is now the second slowest step of a change:
median 7 to 10 minutes and about 127k tokens per run, 15 minutes on the
13-criterion change of 2026-09-23. Across 62 recorded changes it is worth
keeping — in 23 of them it caught a real problem no reviewer, adversary, CI
run or package test recorded, nearly always by actually using the change —
but three things around that core cost time without buying it. 51 of 66 runs
re-ran the full package suite, which Build and finalize-review had already
run and which the tester's own contract tells it not to report. 29 of 62
changes re-ran the whole test after a fix, although most fixes touch a few
criteria; the 2026-09-23 change ran it in full three times. Reports run to a
median of 100 lines, and about 60 per cent of that is evidence the user does
not need in order to accept. The user's words for the goal are 盲跑減重.
A partial re-run has its own trap: on the rename change of 2026-09-23 a
re-test scoped to the one line the fix touched reported its criterion as
working, while three other pull-request lines the same criterion names were
still wrong; it cost one more fix, re-test and review round.

## Proposed outcome
Acceptance testing spends its time using the change, the user can accept from
a report that reads in about a minute, and a re-run after a fix tests only
what the fix could have changed — while every kind of catch the step made in
the recorded history stays within reach.

## Acceptance
1. The acceptance tester does not run the full package suite; a criterion the suite settles cites the finalize-review result instead. A setup check from a fresh clone still runs every time.
2. The report the user reads holds one row per criterion (verdict and one plain sentence), the decisions made on the user's behalf, and the open questions; the evidence behind each row lives in a separate file under the change's evidence directory.
3. A re-run after a fix tests only the criteria the fix could affect, marks every other verdict as carried over from the earlier run, and gives a one-line reason for each carried-over verdict. A criterion that is re-tested is re-tested in full — every surface the Acceptance line names — never only the part the fix touched.
4. These rules are carried by the acceptance tester's contract and the report template's own structure, and the checker's rule list does not grow.

## Constraints
- The step still starts from a clean checkout, is run by an agent that wrote none of the change, and fixes nothing.
- A criterion the tester could not actually try is still reported as not verified, never as working on the strength of reading.
- The user's plain-words skip stays as it is.

## Out of scope
- Reusable standing fixtures such as a permanent test repository.
- Changing when the step runs or which changes skip it.
- Renaming the step (a separate change, done first).

## Open questions
- none
