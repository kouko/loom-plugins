# Close the open follow-ups left by the last four loom changes
originator: kouko
kind: engineering
needs-design: no — closing-review station prose, the implementer agent contract, loom-code tests and a repo memory entry; skill/gate/test artifacts, not interface surfaces under the manifest globs
status: confirmed 2026-09-24
publication: automatic — authorized 2026-09-24 by kouko

## Problem
The last four loom changes (2026-09-23 to 2026-09-24) each left follow-ups
that reviewers flagged but that were out of their scope. They are small, but
each one either lets an agent misread the flow or keeps the test suite
misleading:

| Follow-up | What goes wrong today |
|---|---|
| The fix-round paragraph scopes findings to "the current functional-content digest" | A literal reader can leave out acceptance-testing findings, because committing the report changes that digest |
| The acceptance tester's contract says closing review hands it every dismissed important finding | Closing review never lists that input, so the tester's "decided for you" section can silently miss dismissals |
| The implementer contract says more than one distinct assertion returns `BLOCKED` | A fix hand-off that lists several instances of one defect class can be read as more than one assertion and be refused |
| Two tests pin the checker's rule count at a literal 26 | Any later change that adds a checker rule breaks tests unrelated to it; the checker's own tests already pin the count |
| One recovery-rule probe has been red on main | A known-red test teaches everyone to ignore red, and the probe suite is not run by the package suite |
| The lesson from the rejected parallel acceptance-testing change (PR #50) lives only in machine-local memory | The next session on another machine can re-propose the same design without the evidence |

## Proposed outcome
Each follow-up above is closed, so the flow reads without these gaps, the
suite has no unrelated rule-count pins and no known-red probe, and the PR #50
lesson is in the repository's memory store.

## Acceptance
1. The fix-round paragraph in closing review names the acceptance-testing findings on the content the reviewers just read, including the committed acceptance test report, so no reading of it leaves them out.
2. Closing review lists, among what it hands the acceptance tester, every important-or-worse finding it decided not to act on.
3. The implementer contract states that a fix hand-off listing several instances of one defect class is one task, not a reason to return `BLOCKED`.
4. No test outside the checker's own tests pins the checker's rule count as a literal.
5. The recovery-rule probe that is red on main passes, with the cause recorded as either wrong station prose or a wrong probe expectation.
6. The repository memory store holds the PR #50 lesson — the measured time saving, the cost increase and why reviewers must keep reading the report — with its index entry.
7. The checker's rule list does not grow and no new step, reviewer or dispatch is added.

## Constraints
- No new checker rule, no new flow step, no extra agent dispatch.
- Merged history (earlier plans, CHANGELOG entries, reports) is not edited.

## Out of scope
- GitHub branch rules for main.
- Further trials of the fix-scoping change from 2026-09-24.
- Parallel acceptance testing and review in any form.

## Open questions
- none
