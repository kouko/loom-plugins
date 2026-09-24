# A fix round starts from every blocking finding, grouped by defect class
originator: kouko
kind: engineering
needs-design: no — closing-review station prose that tells the orchestrator what to hand Build before a fix round; skill/gate artifacts, not interface surfaces under the manifest globs
status: confirmed 2026-09-24
publication: automatic — authorized 2026-09-24 by kouko

## Problem
When closing review sends a change back for fixes, the station text says to
batch the fatal and important findings, but the only concrete instruction
next to it records each failing reviewer verdict one at a time, and it never
says that findings from independent acceptance testing on the same version
belong in that batch. An orchestrator reading it can start fixing from one
verdict or one finding while others from the same version wait, and two
findings of the same defect class can reach Build as separate hand-offs.
The sibling search added on 2026-09-24 then runs once per finding instead of
once per class, and whatever was left out of the first batch comes back in a
later round. A survey of 71 recorded loom changes (2026-09-24) counted 18
changes where a later round fixed a sibling of an earlier fix and 12 where
acceptance testing and reviewers reported in separate batches; each extra
round costs roughly 300–400k tokens and 15 minutes. An independent Codex
review of that survey (2026-09-24) confirmed the hand-off gap and warned that
grouping by the recorded failure label would merge unrelated defects, since
that label is only the verdict name.

## Proposed outcome
Before any fix starts, closing review hands Build one complete list of the
blocking findings on the version the reviewers and acceptance tester read,
grouped by defect class, so each class is fixed once and nothing from that
version is left for a later round.

## Acceptance
1. Before a fix round starts, every fatal or important finding from the reviewers and from independent acceptance testing on the current version is collected into one list, and no fix begins from a subset of it.
2. Findings in that list that share a defect class, named in words from the findings themselves and not from the recorded verdict label, reach Build as one hand-off that names all of their instances.
3. The station text states that the per-verdict failure record kept for the pull request is disclosure only and is not the input a fix is scoped from.
4. Given a seeded case with two reviewer findings and one acceptance-testing finding, two of which share a defect class, an agent following the station text produces one hand-off for the shared class and a separate one for the other, shown by a trial run.
5. The rule is carried by station prose; the checker's rule list does not grow and no new step, reviewer or dispatch is added.

## Constraints
- No new checker rule, no new flow step, no extra agent dispatch; the gate budget stays as it is.
- The failure-recording command and what it stores stay unchanged.
- Build §2's sibling search stays the single place that defines how a class is searched; closing review only decides what Build receives.

## Out of scope
- Running acceptance testing and reviewers at the same time on the same version.
- Findings a reviewer could only have raised after a fix changed the content.
- Storing finding content or defect classes in the checker's records.

## Open questions
- none
