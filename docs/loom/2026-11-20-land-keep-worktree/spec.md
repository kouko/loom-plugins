# Keep the worktree when landing an accepted change — spec
intent: 2026-11-20-land-keep-worktree@96e37196
pre-build-review: not-required — adds an opt-in that removes less than today; no security, privacy, irreversible-data or cross-system effect, and the default path is unchanged

## Requirements
REQ-1 — Keep the change's worktree and branches
  WHEN the maintainer accepts a change and asks to keep its worktree, and the agent runs `land --accepted-by <name> --keep-worktree`, the land command shall merge the PR and leave the change worktree (its files and checked-out branch), the local branch and the remote branch in place; this carries the maintainer's acceptance words 「接受 保留 worktree」 → Acceptance #1
REQ-2 — Same gates when keeping
  WHEN `--keep-worktree` is given, the land command shall run the same merge preconditions, checks wait, acceptance line, merge verification and trunk sync as the form without it, and shall refuse the merge on any failure exactly as that form does → Acceptance #2
REQ-3 — Default unchanged
  The land command shall, when `--accepted-by` is given without `--keep-worktree`, remove the change worktree and the local and remote branch after a verified merge, as it does today → Acceptance #3
REQ-4 — Later cleanup works on a kept change
  WHEN a change was landed with `--keep-worktree`, `land --cleanup <branch>` shall remove that change's worktree and local and remote branch, and the keep output shall name that command → Acceptance #4
REQ-5 — A compliant keep path in ship and help
  The ship station text shall tell the agent to add `--keep-worktree` to land when the maintainer asks to keep the worktree, and the `land --help` text shall describe that option instead of asking for preservation the accepted form cannot honour → Acceptance #5

## Design decision
- Add one flag, `--keep-worktree`, accepted only together with `--accepted-by`; `_land_args` returns a usage error (exit 2) when it appears with `--cleanup` or `--sweep`, or twice. agent-decided — one opt-out on the existing form is the smallest shape that keeps every pre-merge gate (critique complexity verdict PROCEED-WITH-CAVEAT, about 20-30 lines plus tests).
- With the flag, `_land_accepted` still calls `sync_trunk` and then skips `cleanup_change`; it prints one line naming the kept worktree path and branch and the `land --cleanup <branch>` command, and prints no `next: cd` line, so the agent stays in the kept worktree. agent-decided — trunk sync is part of today's merged state and is independent of the worktree.
- Keep the remote branch too; nothing is partially cleaned. user-decided — the maintainer chose option A at decision point ① (2026-11-20).
- The ship station's "Land after acceptance" section gains one sentence for the keep case; the closing line about land removing the worktree is qualified. The help line "Do not run cleanup when worktree preservation was requested." is rewritten to point at `--keep-worktree` for the accepted form. agent-decided — these are the two places an agent reads before running land.
- No new state is recorded: a kept change is an ordinary merged change, so the existing `--cleanup` and `--sweep` handle it unchanged. agent-decided.

## Alternatives considered
- Let ship allow `gh pr merge` when keeping — rejected: skips the live PR-body validation, the `Accepted-by:` line and the verification disclosure that land adds.
- Make the accepted form never clean and always run `--cleanup` separately — rejected: changes every user's default and makes forgotten cleanup the common case.
- Keep the worktree but delete the remote branch — rejected by the maintainer (option B at decision point ①).
- An environment variable or KICKOFF-DEFAULTS key instead of a flag — rejected: keeping is a per-acceptance choice, not a repository default.

## Current state evidence
- Forward: loom-code/scripts/loom_checker/command_handlers/land.py:140 `cmd_land` dispatches `--accepted-by` to `_land_accepted` (:182), which merges, verifies and calls `_sync_and_clean` (:202).
- Reverse: loom-code/skills/ship/SKILL.md:323-331 tells the agent to run `land --accepted-by <name>` from the worktree root and states land removes that worktree.
- Error: loom-code/scripts/loom_checker/command_handlers/land.py:110-137 `_land_args` returns usage errors such as "use exactly one of --accepted-by, --cleanup, or --sweep" and "unexpected argument"; any other token is rejected today.
- Data: loom-code/scripts/loom_checker/command_handlers/land.py:226 `CleanupPlan` (worktree, local, remote) is what `cleanup_change` (:529) removes; no record marks a change as kept.
- Boundary: loom-code/scripts/loom_checker.py:200-225 land help text; `--cleanup` (:173) and `--sweep` behaviour is not changed.

## UI flows
| case | what the agent runs | what it sees |
|---|---|---|
| keep requested | `land --accepted-by <name> --keep-worktree` | `Merged PR #<n> as <sha7>`, the trunk result, then a line naming the kept worktree path and branch and `land --cleanup <branch>`; no `next: cd` line |
| keep requested, a check fails | same | the same BLOCK message and exit 1 as without the flag; nothing merged |
| no keep | `land --accepted-by <name>` | unchanged from today |
| flag misused | `land --cleanup <b> --keep-worktree` | usage error naming that `--keep-worktree` applies only to `--accepted-by`, exit 2 |
| later cleanup | `land --cleanup <branch>` | unchanged; removes the kept worktree and branches |
