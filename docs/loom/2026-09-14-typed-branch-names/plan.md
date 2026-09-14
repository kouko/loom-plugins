# Typed branch names — plan
intent: 2026-09-14-typed-branch-names@db4b663e
charter: 1.0

## Current State Evidence
- Forward: `loom-code/skills/write-plan/SKILL.md` Step 6 — "Branch first" block runs `git switch -c <change-id>`.
- Reverse: `loom-design/skills/capture-intent/SKILL.md` Step 5 — Branch note says write-plan creates `<change-id>` from the trunk.
- Error: `loom-code/scripts/loom_checker/helpers.py` `ON_A_BRANCH` — trunk refusal hint prints `git switch -c <change-id>`.
- Data: `loom-code/scripts/command_handlers/publish.py` `_publication_change_id` — change-id comes from the attestation path, never the branch name.
- Boundary: `loom-code/scripts/test_loom_checker_intent.py` `test_working_on_the_trunk_fails_closed` — asserts only `git switch -c` in stderr.

## Task DAG

### Wave 1

**W1-01 Typed branch in checker trunk hint**  after: none  acceptance: 2, 5
- Files: loom-code/scripts/loom_checker/helpers.py, loom-code/scripts/test_loom_checker_intent.py
- Test: A2 positive: trunk-hint-names-typed-branch; negative: trunk-hint-bare-change-id-absent. A5 positive: typed-branch-base-resolves; boundary: typed-branch-with-nested-slash-resolves.
- Risk: agent-decided — change only the hint string; branch_base logic untouched so no name parsing is introduced (intent Constraint 1).

**W1-02 Typed branch in station prose**  after: W1-01  acceptance: 1, 3, 4, 6
- Files: loom-code/skills/write-plan/SKILL.md, loom-design/skills/capture-intent/SKILL.md
- Test: A1 positive: write-plan-names-typed-branch-and-types; negative: write-plan-bare-switch-absent. A3 positive: capture-intent-names-typed-branch; negative: capture-intent-bare-branch-absent. A4 positive: repo-grep-no-bare-branch; negative: changelog-history-excluded. A6 positive: package-suite-pass; negative: station-text-test-regression.
- Risk: agent-decided — allowed types are feat, fix, docs, refactor, test, chore, ci, matching implementer.md; the agent picks one and applies it to the branch prefix and PR title.

## Questions asked
① — consequence — 回答「對」就表示你同意：review 和發布前檢查都通過後，agent 會自動 push，並開一個 Ready 狀態的 PR。merge 還是會另外問你。
① — what — 以上都對嗎？

## Risks
1. agent-decided — the change branch was created as `feat/2026-09-14-typed-branch-names` per write-plan Step 6 (the worktree's placeholder branch `branch-name` was never a change branch); the worktree directory keeps its old name.
2. The installed plugin cache still carries the old wording until a release; out of scope per intent.
