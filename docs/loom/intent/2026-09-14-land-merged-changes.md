# Land a reviewed Loom change: wait for CI, merge, sync, and clean up
originator: kouko
kind: engineering
needs-design: yes — the landing sequence is multi-state (CI wait, merge, merge verification, trunk sync, branch and worktree cleanup, each with its own refusal) and no spec covers it
evidence: [loom-code/skills/ship/SKILL.md, loom-code/scripts/loom_checker/command_handlers/publish.py, loom-code/scripts/loom_checker/command_handlers/push.py, docs/loom/memory/a-worktree-cleanup-by-pattern-match-destroys-other-peoples-work.md, docs/loom/memory/squash-dialog-can-drop-entire-pr-body.md]
status: confirmed 2026-09-14
publication: automatic — authorized 2026-09-14 by kouko

## Problem
Loom automates a change up to an open PR, then stops. Everything after that is
done by hand, every time, by the maintainer or by an agent improvising commands:

- Waiting for CI: agents poll `gh pr checks` / `gh pr view` in `sleep` loops —
  251 calls across 42 sessions (session history 2026-07-25 to 2026-09-14).
- Merging: Ship says "do not merge without the user's separate explicit
  authorization", and the maintainer's global guard refuses an agent's
  `gh pr merge`, so the maintainer typed `gh pr merge` themselves 57 times in
  27 sessions.
- Cleaning up: nothing in Loom removes the merged change's branch or worktree
  (Ship says "keep the worktree until integration is verified"). A squash
  merge leaves the branch looking unmerged to git, so agents reach for
  `git branch -D`, which is denied — 30 denials in 20 sessions — and the
  maintainer cleaned up by hand 32 times in 15 sessions.
- Improvised cleanup is dangerous: on 2026-09-11 a pattern-matched
  `git worktree remove --force` loop destroyed uncommitted work in five
  unrelated worktrees.

The consequence is a stalled finish on every change, stale branches and
worktrees accumulating, and each agent re-inventing risky git choreography.

## Proposed outcome
After a change's blind-run report is accepted, Loom finishes the change by
itself: it waits for CI, merges the PR, confirms the merge landed, brings the
local trunk up to date, and removes that change's branch (local and remote) and
worktree — refusing, and saying why, whenever a safety condition is not met.
The same cleanup can be run on its own, either for one named already-merged
change or as a sweep over every change whose PR is merged.

## Acceptance
1. On a change whose blind-run report was accepted and whose merge is
   authorized, the PR ends up merged without the maintainer typing any git or
   GitHub command.
2. When a PR check fails or the PR cannot merge cleanly, nothing is merged and
   the report names the failing check or the blocking reason.
3. Accepting the blind-run report is the merge authorization (user-decided
   2026-09-14). Without that recorded acceptance, nothing is merged and the
   report says the authorization is missing.
4. The squash commit on the trunk carries the PR's title and body.
5. After a successful merge, the local trunk contains the merge commit, or the
   report states why the trunk was not updated (it is never force-updated or
   merged into).
6. After a successful merge, the change's local branch, remote branch, and
   worktree no longer exist.
7. Cleanup removes nothing, and names the reason, when the PR is not merged on
   GitHub, the worktree has uncommitted or untracked files, or the branch has
   commits that are not in the merged PR.
8. Other worktrees and branches — including ones with uncommitted files and
   names similar to the change's — are untouched after landing or cleanup.
9. Cleanup alone, run for one already-merged change, removes that change's
   branches and worktree under the same refusals as 6–8.
10. A sweep selects only changes whose PR is merged on GitHub; before removing
    anything it lists what it would remove and what it skips with each reason,
    and removes only after the maintainer confirms that list. Each selected
    change gets the same refusals as 7–8, and one refusal does not stop the
    others.
11. A hand-typed `gh pr merge` is still refused by Loom's publication hook;
    only the landing path merges.

## Constraints
- The landing entry point is a `loom_checker.py` sub-command beside `publish`
  (user-decided 2026-09-14).
- Worktrees are removed one at a time by exact known path, never selected by
  filtering a listing, and never with `--force`
  (docs/loom/memory/a-worktree-cleanup-by-pattern-match-destroys-other-peoples-work.md).
- Cleanup alone offers both a single named change and a sweep over merged
  changes (user-decided 2026-09-14).
- Must work on the hosts Ship already supports: Claude Code, Codex CLI,
  Antigravity CLI.
- The maintainer's global guard (`~/dotfiles/claude/.claude/hooks/executable_bash-guard.sh`,
  `~/.claude/settings.json` deny list) lives outside this repository and is not
  edited by this change.

## Out of scope
- Editing the maintainer's global dotfiles guard or permission settings.
- Creating worktrees, stash handling, PR comments or approvals.
- Changing push or PR-creation behavior.

## Later changes
- PR #43 replaced Acceptance 11: a hand-typed `gh pr merge` is no longer refused; the publication hook prints a reminder and allows it (`loom-code/scripts/loom_checker/command_handlers/push.py`). The merge floor is now GitHub's ruleset plus the `loom-pr-floor` CI check.
- `land` still refuses a malformed PR body and a missing acceptance, and discloses a non-valid verification status as "merged anyway" (`loom-code/scripts/loom_checker/command_handlers/land.py`).
- Decision recorded in #43's PR body Decisions table and intent 2026-09-22-publication-floor-moves-to-github.

## Open questions
- none
