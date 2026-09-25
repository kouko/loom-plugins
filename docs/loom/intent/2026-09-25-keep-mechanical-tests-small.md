# Keep the tests a change adds small, and make over-built tests a review finding
originator: kouko
kind: engineering
needs-design: no — implementer, adversary and review-lens contract text in loom-code plus a text-pin test; skill/agent artifacts, not interface surfaces under the manifest globs
status: confirmed 2026-09-25
publication: automatic — authorized 2026-09-25 by kouko

## Problem
The automated tests that loom changes add keep coming out more complex than
the behaviour needs: helper sets built for a single case, duplicated cases,
tests that pin other tests, and a new pin test for every review finding.
Nothing in loom limits this. The only limit today is the maintainer repeating
"keep the tests simple" in each session, which lives in one machine's memory
and reaches no other session or project. Over-built tests cost review rounds
and maintenance, and on 2026-09-25 the maintainer had to stop one change
whose tests had grown for a case nobody would hit in practice.

## Proposed outcome
loom itself states a test budget to whoever writes tests in a change, and
closing review treats tests beyond that budget as a finding, so every session
and project using loom gets the same limit without the maintainer asking.

## Acceptance
1. The implementer contract states a test budget: at most one positive and one negative or boundary case per Acceptance line or finding, reuse of the existing test helpers, no new test harness, no tests of tests, and the net test lines added in its report.
2. The adversary contract states that each probe program stays small and reuses existing test helpers.
3. Closing review's tests dimension makes over-built tests a finding with the smaller shape named, and says the fix for a finding adds at most one test, extending an existing test first.
4. No checker rule, flow step or agent dispatch is added.

## Constraints
- Changes stay inside loom-code; loom-code keeps working without loom-design or loom-workflow.
- No numeric line-count threshold enforced by a checker.

## Out of scope
- A complexity check of the plan or implementation design before Build (the next change).
- Rewriting or shrinking existing tests.
- The adversary's five-program cap, which stays as it is.

## Open questions
- none
