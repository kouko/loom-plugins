# Change records start on the change branch, and a diverged trunk is never discarded unasked
originator: kouko
kind: engineering
needs-design: no — skill prose for capture-intent, write-spec, write-plan and ship; no CLI, API or template surface changes
evidence: [/private/tmp/claude-501/-Users-kouko--herdr-worktrees-loom-plugins-consistence-review-2/5b11059c-24eb-4eec-9170-a767ecffcf0e/scratchpad/dogfood-report-2026-10-29.md]
status: confirmed 2026-10-29
publication: automatic — authorized 2026-10-29 by kouko

## Problem
In the 2026-10-28/29 sandbox dogfood (`kouko/loom-dogfood-sandbox`, PRs #1 and #2), both
rounds committed the confirmed intent — and in round 1 the spec — directly on the local
trunk. `capture-intent` permits an intent commit on the trunk, `write-spec` gives no
branch guidance before its spec commit, and `write-plan` branches only at its Step 6 (or
early at Step 3 for an already-confirmed intent), after its own intent-confirmation
commit in `references/confirm-intent.md`. After the squash merge the local trunk
diverged from `origin`; `land` printed `trunk not updated: not a fast-forward`, and both
times the agent ran `git reset --hard origin/main` on its own, without asking the
maintainer. Resetting the trunk that way can discard unrelated local work that only
exists in its history.

## Proposed outcome
Every change-owned commit — intent confirmation, corrective and skip-record commits,
spec, plan and later — lands on that change's branch, so the change itself never
diverges the local trunk. When `land` still reports that the trunk was not updated, the
agent tells the maintainer and does not discard local trunk commits without asking.
When the change has to move to another worktree, everything it produced and has not
yet committed moves with it, and nothing it produced is left behind.

## Acceptance
1. Running a change from a clean, synchronized trunk through `capture-intent` (and `write-spec` when it runs) adds no commit to the local trunk; the intent commit is on the change branch.
2. Starting from a trunk synchronized with `origin` and receiving no independent local commits, after that change is merged through `land` the local trunk fast-forwards to the merge with no manual reconciliation.
3. Given a local-only sentinel commit on the trunk and `land` reporting `trunk not updated`, an agent following the station instructions reports it to the maintainer and leaves the trunk's commit identifier unchanged; merge acceptance does not count as permission to discard it.
4. A change entered at `write-plan` (loom-design absent) branches before its first change-owned commit, including the intent-confirmation commit.
5. When HEAD is already on the branch belonging to this change, the station reuses it; on an unrelated branch or a detached HEAD it does not commit there before that is resolved, and existing work is preserved.
6. When the change moves to another worktree — a new one, or the one where its branch is already checked out — every uncommitted file the change produced so far (the intent draft, a spec, a `PRINCIPLES.md` edit) ends up committed on the change branch there, and the original checkout keeps exactly its own earlier work. A spec is never left in a checkout the change has left.

## Constraints
- Prose and existing-checker changes only; no new `land` reconciliation mechanism (critique complexity, confirmed by an outside Codex review: reconciling in `land` adds policy and code for a symptom the earlier branch removes, and cannot substitute for permission to discard history).

## Out of scope
- Automatic reconciliation of an already-diverged trunk by `land`.
- Committing an intent on the trunk for later work (the existing allowance is removed; an uncommitted draft needs no branch).
- The other dogfood findings (pytest interpreter, background adversary, set-head message, language after compaction).

## Open questions
- none
