---
change-id: 2026-10-21-ship-memory-write-timing
status: confirmed 2026-10-21
kind: engineering
needs-design: no — internal skill prose timing rule; no user-visible surface
originator: kouko
publication: automatic — authorized 2026-10-21 by kouko
---

# Ship memory write timing rule

## Problem

Ship's loom-memory routing paragraph (added by PR #101) tells the agent to route
durable lessons to `docs/loom/memory/` while Ship runs, i.e. after
`finalize-review` has already generated the attestation. A memory file committed
there is functional content: it changes the functional content digest, so the
attestation goes stale, forcing either another review round (complete package
suite + 2 reviewers) or publication with `Verification status: stale`. The
maintainer verified this risk with an independent Codex audit and industry
research (SLSA sign-software-not-docs, postmortem/ADR timing conventions) and
selected Direction D: Ship only confirms or defers; it never writes memory
entries after finalization.

## Proposed outcome

`loom-code/skills/ship/SKILL.md` carries an explicit memory-write-timing rule:
memory entries land before `closing-review`'s `finalize-review` generates the
attestation, never after; qualifying lessons discovered at or after Ship are
deferred to the next change's branch, citing the existing git-memory deadline
and loom-memory's ride-the-next-branch rule.

## Acceptance

1. `loom-code/skills/ship/SKILL.md` contains the memory-write-timing rule and
   cites the git-memory finalization deadline and loom-memory's
   ride-the-next-change rule.
2. Closing review completes with a `valid` attestation over the branch
   including the new rule; the rule is functional content the reviewers read.
3. All ship station tests pass (`test_ship_station_text.py`,
   `test_ship_worktree_merge.py`, `test_ship_risk_section_agent_decided_door.py`).

## Constraints

- Direction D only: a prose timing rule in Ship; no Build/closing-review
  routing change, no `publication_only_paths` change.
- The branch already carries the functional edit (a152dfef) on
  `feat/2026-10-21-ship-memory-write-timing`.

## Out of scope

- Moving the routing point into Build or closing-review (option A).
- Excluding `docs/loom/memory/**` from the digest (option B).
- `claude_reviewer.py` silent-hang fix (separate change).

## Open questions

- none
