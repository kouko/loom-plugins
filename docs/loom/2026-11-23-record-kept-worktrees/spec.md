# Record kept worktrees so sweep never removes them — spec
intent: 2026-11-23-record-kept-worktrees@7bafdd12
pre-build-review: not-required — adds a local, uncommitted marker and makes sweep remove less than today; no security, privacy, irreversible-data or cross-system effect; default paths unchanged

## Requirements
REQ-1 — A later session can see that a change was kept
  WHEN a change was landed with `land --accepted-by <name> --keep-worktree`, a later `land --sweep` listing run from any worktree of the same repository, with no memory of the earlier session, shall show that change's branch on a line marked kept → Acceptance #1
REQ-2 — Sweep lists kept changes separately and never removes them
  WHEN `land --sweep` runs, the land command shall list each kept change on its own `kept` line naming its worktree and the `land --cleanup <branch>` command, exclude it from the confirmation token and from removal, and leave its worktree, local branch and remote branch in place after `land --sweep --confirm <token>`; this is the maintainer's choice to list kept changes separately and never delete them → Acceptance #2
REQ-3 — Explicit cleanup still removes a kept change and its record
  WHEN the maintainer asks to remove a kept change and `land --cleanup <branch>` runs for it, the land command shall remove its worktree, local branch and remote branch as for any merged change, and no keep record for that branch shall remain → Acceptance #3
REQ-4 — Unkept changes behave as today
  The land command shall, for a change landed without `--keep-worktree`, produce the same sweep listing lines, confirmation token and cleanup result as before this change → Acceptance #4
REQ-5 — Ship cleans only unrecorded changes, and asks when unsure
  The ship station text shall tell the agent to treat a change on a `kept` sweep line as kept and leave it, and to show the maintainer the sweep listing and obtain their yes before cleaning any merged change left from earlier work that still has a worktree, rather than cleaning it on its own judgement → Acceptance #5

## Design decision
- The keep record is one git config entry, `branch.<branch>.loomKept`, written with `git config` in the repository's common config when the keep land succeeds (after trunk sync, alongside today's "Kept worktree" line). agent-decided — it lives outside every working tree, is never committed or pushed (intent Constraint 1), is readable from any worktree of the repository, and git removes the `branch.<branch>` section when the local branch is deleted.
- Sweep reads `git config --get branch.<branch>.loomKept` for each candidate; a set value produces `kept <branch> — <where>; remove with: land --cleanup <branch>` instead of a `remove` line and the change is not added to the removable list. The token is computed only over `remove` lines (unchanged rule), so kept changes cannot enter a confirmed sweep. user-decided — the maintainer chose "list separately, mark kept, never delete" at decision point ① (2026-11-23).
- `land --cleanup <branch>` on a kept change behaves as for any merged change and then removes the `branch.<branch>` config section (which holds the record), even when no local branch exists (no error when already gone), so a record cannot outlive a cleanup that removed only the remote branch or found no local branch. agent-decided — explicit cleanup is the maintainer's request to remove (intent Proposed outcome).
- Ship §5: the earlier-work cleanup paragraph is rewritten so the agent runs `land --sweep` (listing only), leaves `kept` lines alone, and cleans other merged changes only after the maintainer answers yes to the listing; this also covers 3.88.0-era keeps that have no record (intent Out of scope: no backfill). The land help text documents the `kept` line and the record. agent-decided.
- No new flag, file, or schema. Release as a minor loom-code bump (station guidance and CLI output change). agent-decided.

## Alternatives considered
- Wording-only (ship: "when unsure, ask"; no record) — rejected: sweep would still list kept changes under `remove`, so a maintainer's yes deletes them (Acceptance #2).
- Sweep skips any merged branch whose worktree still exists (no record) — rejected: it also hides worktrees left by a failed cleanup, which sweep exists to remove, and gives a later session nothing to tell the two apart (Acceptance #1).
- Hide kept changes from the sweep listing entirely — rejected by the maintainer at decision point ①; kept worktrees would be forgotten.
- Marker file inside the kept worktree or under `docs/loom/` — rejected: dirties the worktree the maintainer asked to keep or gets committed and pushed (intent Constraint 1).
- Marker file under the common `.git/` directory — rejected: needs its own lifecycle and cleanup code, while the branch config section is removed by git with the branch.

## Current state evidence
- Forward: loom-code/scripts/loom_checker/command_handlers/land.py:211-218 — the keep path in `_sync_and_clean` syncs trunk and prints "Kept worktree … remove it later with: land --cleanup <branch>"; nothing is persisted.
- Reverse: loom-code/skills/ship/SKILL.md:349-353 — ship tells the agent to clean a merged change from earlier work "except a change landed with `--keep-worktree`" and to confirm sweep only after the maintainer's yes.
- Error: loom-code/scripts/loom_checker/command_handlers/land.py:701-721 — `_sweep_list` emits a `remove` line and appends to `removable` for every merged branch whose cleanup plan succeeds, kept or not; a confirmed token then removes it (:756).
- Data: loom-code/scripts/loom_checker/command_handlers/land.py:726-728 — `sweep_token` hashes only lines starting `remove `; `CleanupPlan` (:226) carries worktree/local/remote only.
- Boundary: loom-code/scripts/loom_checker/command_handlers/land.py:529 `cleanup_change` and the merge path before `_sync_and_clean` are unchanged apart from the explicit record unset; loom-code/scripts/loom_checker.py land help is the only other text surface.

## UI flows
| case | what the agent runs | what it sees |
|---|---|---|
| keep a change | `land --accepted-by <name> --keep-worktree` | the Kept worktree line ("Kept worktree … remove it later with: land --cleanup <branch>"); the record is written |
| keep record write fails | `land --accepted-by <name> --keep-worktree` | the Kept worktree line, then `BLOCK land.cleanup: keep record not written: <detail>; run: git config branch.<branch>.loomKept <date>`; exit 1 |
| later session lists sweep | `land --sweep` | a `kept <branch> — <where>; remove with: land --cleanup <branch>` line for each kept change, `remove …` lines for the rest; the confirm token covers only `remove` lines |
| only kept changes merged | `land --sweep` | the `kept` lines, then "No merged changes to clean up"; no token |
| confirm sweep | `land --sweep --confirm <token>` | removes only the `remove` lines; kept changes untouched |
| maintainer asks to remove a kept change | `land --cleanup <branch>` | the usual cleanup output; afterwards no `kept` line for that branch |
| no keep used | any form | unchanged from today |
