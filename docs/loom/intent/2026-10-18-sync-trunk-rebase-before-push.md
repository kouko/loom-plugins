# sync-trunk rebases a change branch that has never been pushed
originator: kouko
kind: engineering
needs-design: no — internal behaviour of the existing `sync-trunk` checker command; its result lines and the stations that read them keep their current vocabulary
status: confirmed 2026-10-18
publication: automatic — authorized 2026-10-18 by kouko

## Problem
When a change branch falls behind trunk, `loom_checker.py sync-trunk` always merges trunk into it. Every such sync leaves a "Merge origin/main into …" commit in the branch, so the pull request's commit list is interleaved with merge commits that carry no change of their own. The maintainer prefers a linear branch history and reads that commit list during review.

## Proposed outcome
While the change branch has never been pushed, `sync-trunk` replays the branch's own commits on the trunk tip, so the branch stays a straight line with no merge commit. Once any of the branch has been pushed, `sync-trunk` keeps merging as today, so pushed history is never rewritten and a later non-forced publish still succeeds.

## Acceptance
1. On a never-pushed change branch that is behind trunk with no conflict, `sync-trunk` leaves the branch's own commits sitting directly on the trunk tip with no merge commit, and reports that content changed.
2. On a change branch that has already been pushed and is behind trunk, `sync-trunk` merges as today: the pushed commits are still in the branch unchanged, and the next non-forced publish of the branch is accepted by the remote.
3. When replaying a never-pushed branch would conflict, `sync-trunk` names the conflicting paths and leaves the branch, its commits and the working tree exactly as they were before the command.
4. Every other `sync-trunk` outcome (already up to date, warnings, refusals) is unchanged, and the complete package suite passes.

## Constraints
- Never force-push and never rewrite a commit that exists on the remote.
- A conflict is named, never resolved by the command (existing `review.sync` rule).

## Out of scope
- Changing how pull requests are merged into trunk (squash merge stays).
- Rebasing in any other station or command (`land`, `publish`, CI repair).
- Force-pushing a pull-request branch after it has been pushed (revisit only if merge commits after publication become a real nuisance).
- The user's shell hooks outside this repository.

## Open questions
- none
