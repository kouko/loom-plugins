# Bring the change branch up to date with main before closing review
originator: kouko
kind: engineering
needs-design: no — adds a step to the existing closing-review flow in station prose and checker internals; it touches no configured interface surface, and its outcomes (already current, synced, conflict, remote unreachable) are few enough to state in Acceptance without a spec
evidence: [loom-code/scripts/loom_checker/command_handlers/land.py, loom-code/scripts/loom_checker/digest.py]
status: confirmed 2026-09-15
publication: automatic — authorized 2026-09-15 by kouko

## Problem
The trunk's branch protection requires a pull request to contain the latest
main before it merges (`strict: true`), and `land` refuses a PR GitHub reports
as `BEHIND`. Nothing in Build, closing review, or Ship brings the change branch
up to date with main, so whenever another change lands first the maintainer or
agent has to type `git merge origin/main` by hand — twice since 2026-09-14
(`7e97f7a7`, `f9b67533`), the second followed by a plan commit renumbering
release versions after main moved to 3.5.0.

When that merge happens after closing review it is worse than a typed command:
the attestation's functional-content digest covers the whole tree, so any
content main brings in invalidates the review, and the change pays a second
review round for content nobody changed on purpose. When it happens before
review by hand, it is easy to forget the fetch and merge a stale main.

## Proposed outcome
Before closing review dispatches any reviewer, the change branch already
contains the current tip of main fetched from the remote, and the mechanical
checks that gate reviewer dispatch have passed on that synced content. The
review therefore reads, and the attestation binds, the content that will
actually merge. A conflicting sync stops the review with a plain report
instead of guessing; an unreachable remote is reported as a warning and the
review continues on the unsynced branch.

## Acceptance
1. When closing review starts on a change branch that lacks commits from the remote main and merges with it cleanly, the branch contains the freshly fetched remote main tip before the first reviewer is dispatched, and the generated attestation validates at the resulting HEAD.
2. When the change branch already contains the remote main tip, starting closing review adds no commit to the branch.
3. When bringing in the remote main conflicts, closing review dispatches no reviewer, the branch and working tree are left as they were before the attempt, and the report names every conflicting file.
4. When the remote cannot be reached, closing review reports a warning that the branch could not be checked against main and then continues without syncing.
5. When the sync brings in new content, the complete package suite and the adversarial programs run and pass on the synced content before any reviewer is dispatched.

## Constraints
- Conflicts are never resolved automatically; they are reported for a human or a new build round.
- The trunk checkout is never modified by this step.
- `land`'s existing merge preconditions, including its refusal of a `BEHIND` pull request, stay unchanged.

## Out of scope
- Re-syncing when main moves again during closing review or between review and `land`.
- Changing what `land` reports or does when a pull request is `BEHIND`.
- Syncing at any other station (write-plan, Build tasks, Ship).

## Open questions
- none
