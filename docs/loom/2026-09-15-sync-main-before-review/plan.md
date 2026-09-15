# Bring the change branch up to date with main before closing review — plan
intent: 2026-09-15-sync-main-before-review@f82a327b
charter: 1.0

## Current State Evidence
- Forward: `loom-code/skills/closing-review/SKILL.md:61-68` checks only Build's hand-off before dispatching reviewers; no step fetches or merges the trunk.
- Reverse: `loom-code/skills/build/SKILL.md:85-96` runs the package suite and adversarial programs before hand-off; `:110-112` calls closing-review with branch base and HEAD.
- Error: `loom-code/scripts/loom_checker/command_handlers/land.py:58` refuses `BEHIND`; `loom-code/scripts/loom_checker/digest.py:30` hashes the whole tree, so a later merge invalidates the attestation.
- Data: `loom-code/scripts/loom_checker/helpers.py:176` lists trunk candidates `origin/main`, `main`, `origin/master`, `master` resolved without network; `land.py:299-323` is the only trunk fetch or merge.
- Boundary: `loom-code/scripts/loom_checker.py:65` registers checker subcommands; `loom_checker/rules.py:6` and `test_loom_checker_cli.py:18` register rule ids; `test_land_merge.py:35-46` builds real temporary repositories.

## Task DAG
<!-- When a spec requirement changes after this commit, the un-landed
     tasks it touches are replaced and the reason is named in the commit
     message. Landed tasks stay as they are. -->

### Wave 1 — sync command

**W1-01 checker sync-trunk command**  after: none  acceptance: 2, 3, 4
- Files: `loom-code/scripts/loom_checker/command_handlers/sync.py`, `loom-code/scripts/loom_checker.py`, `loom-code/scripts/loom_checker/rules.py`, `loom-code/scripts/test_sync_trunk.py`, `loom-code/scripts/test_loom_checker_cli.py`, `docs/loom/evidence/mechanisms.yaml`
- Test: A2 positive: current-branch-adds-no-commit; boundary: branch-ahead-of-trunk-adds-no-commit. A3 positive: conflict-names-every-file-and-restores-head; negative: dirty-worktree-or-trunk-checkout-refused-untouched. A4 positive: unreachable-remote-warns-exit-zero; negative: unreachable-remote-creates-no-commit.
- Risk: merge, not rebase, so pushed history is never rewritten; trunk name resolved from `refs/remotes/origin/HEAD` then helpers candidates, needing no network. One rule id `review.sync`. agent-decided.

### Wave 2 — stations and release

**W2-01 build and closing-review run the sync before reviewers**  after: W1-01  acceptance: 1, 5
- Files: `loom-code/skills/build/SKILL.md`, `loom-code/skills/closing-review/SKILL.md`, `loom-code/scripts/test_sync_before_review_text.py`, `loom-code/CHANGELOG.md`, `loom-code/plugin.json`, `loom-code/.claude-plugin/plugin.json`, `loom-code/.codex-plugin/plugin.json`
- Test: A1 positive: behind-branch-synced-then-attestation-validates-at-head; negative: sync-after-finalize-invalidates-attestation. A5 positive: merged-sync-returns-to-build-checks-before-dispatch; boundary: no-op-sync-dispatches-without-rerun.
- Risk: Build §3 syncs before its suite so the common case runs checks once; closing-review re-syncs before dispatch and returns to Build when content arrived. Minor release 3.6.0. agent-decided.

## Questions asked
① — consequence — restated intent, including automatic push and Ready PR after review with merge asked separately; kouko: "OK"
① — what — 連不上 GitHub 時停下不審，還是警告後照審？ kouko: "Ｂ"

## Risks
1. user-decided — an unreachable remote warns and review continues unsynced; land may later still refuse `BEHIND`, costing a second review round.
2. Main can move again during review; re-syncing then is out of scope, so land's existing `BEHIND` refusal remains the backstop.
3. Branch `feat/2026-09-15-readable-flow-details` also plans loom-code 3.6.0; whichever lands second renumbers its release. agent-decided.
