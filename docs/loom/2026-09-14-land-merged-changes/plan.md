# Land a reviewed Loom change: wait for CI, merge, sync, and clean up — plan
intent: 2026-09-14-land-merged-changes@3869e1a8
spec: docs/loom/2026-09-14-land-merged-changes/spec.md@b510bcb4
charter: 1.0

## Task DAG
<!-- When a spec requirement changes after this commit, the un-landed
     tasks it touches are replaced and the reason is named in the commit
     message. Landed tasks stay as they are. -->

Wave 1 — hook and rule registry

**W1-01 Hook refuses every hand-typed merge**  after: none  acceptance: 11
- Files: loom-code/scripts/loom_checker/command_handlers/push.py, loom-code/scripts/loom_checker/rules.py, loom-code/scripts/test_loom_checker_cli.py, loom-code/scripts/test_loom_publish.py, loom-code/scripts/test_ship_worktree_merge.py, loom-code/scripts/test_publish_command_detection.py, loom-code/scripts/test_codex_stale_hook.py, loom-code/scripts/test_hooks_json.py
- Test: A11 positive: hook-blocks-absolute-cd-merge-with-push-merge; negative: hook-still-allows-canonical-git-push.
- Risk: REQ-11; block runs before repository selection so nested eval/bash -c forms get push.merge; agent-decided.

Wave 2 — land merge path

**W2-01 land merge preconditions and acceptance**  after: W1-01  acceptance: 2, 3
- Files: loom-code/scripts/loom_checker/command_handlers/land.py, loom-code/scripts/loom_checker.py, loom-code/scripts/loom_checker/rules.py, loom-code/scripts/test_loom_checker_cli.py, loom-code/scripts/test_land_merge.py
- Test: A2 positive: failing-nonrequired-check-blocks; negative: unstable-state-blocks. A3 positive: originator-name-passes; negative: missing-or-foreign-name-blocks.
- Risk: REQ-2, REQ-3; all checks, not required-only; fakes via run_land_external seam; agent-decided.

**W2-02 land squash merge and verification**  after: W2-01  acceptance: 1, 4
- Files: loom-code/scripts/loom_checker/command_handlers/land.py, loom-code/scripts/test_land_merge.py
- Test: A1 positive: accepted-green-pr-merges-with-match-head; negative: merge-timeout-still-open-blocks. A4 positive: body-file-carries-body-and-accepted-by; negative: title-only-commit-verify-blocks.
- Risk: REQ-1, REQ-4; after timeout re-read PR state up to 60s before "merge not performed" (review nit); agent-decided.

Wave 3 — trunk sync and cleanup

**W3-01 trunk fast-forward and change cleanup**  after: W2-02  acceptance: 5, 6, 7, 8
- Files: loom-code/scripts/loom_checker/command_handlers/land.py, loom-code/scripts/test_land_cleanup.py
- Test: A5 positive: clean-trunk-fast-forwards; negative: dirty-trunk-skipped. A6 positive: merged-change-refs-worktree-removed; boundary: cwd-inside-worktree-prints-next-cd. A7 positive: untracked-file-refuses; negative: ignored-env-refuses. A8 positive: similar-named-dirty-worktree-untouched; negative: moved-tip-update-ref-refuses.
- Risk: REQ-5..REQ-8; real temp git repos for worktree/ref ops, faked gh; never --force; agent-decided.

**W3-02 named cleanup and sweep**  after: W3-01  acceptance: 9, 10
- Files: loom-code/scripts/loom_checker/command_handlers/land.py, loom-code/scripts/test_land_sweep.py
- Test: A9 positive: cleanup-named-merged-branch; negative: reused-branch-name-refuses. A10 positive: sweep-lists-then-confirm-removes; negative: changed-list-token-removes-nothing.
- Risk: REQ-9, REQ-10; token over sorted remove lines with sha7; agent-decided.

Wave 4 — station text, registry, release

**W4-01 Ship text, mechanism registry, release notes**  after: W3-02  acceptance: 1, 11
- Files: loom-code/skills/ship/SKILL.md, loom-code/scripts/test_ship_station_text.py, docs/loom/evidence/mechanisms.yaml, loom-code/CHANGELOG.md, loom-code/plugin.json, loom-code/.claude-plugin/plugin.json, loom-code/.codex-plugin/plugin.json
- Test: A1 positive: ship-text-runs-land-after-acceptance; negative: ship-text-has-no-direct-gh-pr-merge. A11 positive: check-mechanisms-green-with-budget-exceptions; negative: ship-text-keeps-no-worktree-instruction.
- Risk: spec Ship station text and Release; four budget-exception lines naming evals; agent-decided.

## Questions asked
① — consequence — 以後的變更，merge 的同意要怎麼給？（答：接受報告＝同意 merge）
① — what — 單獨清理的範圍？（答：我覺得兩個功能都需要）
① — what — 上面的覆述（含本次變更自動 push＋開 PR 的授權）正確嗎？（答：對，照這樣）
① — consequence — 掃描清理「先列清單、你確認才刪」這樣可以嗎？確認後 intent 就定案。（答：可以，先列清單再刪）

## Risks
1. Branch renamed from auto-git to feat/2026-09-14-land-merged-changes before the plan so publish title type matches; herdr workspace metadata may still show the old name.
2. The maintainer's global guard outside this repo still denies hand-typed merges; land uses subprocesses, so it is unaffected; dotfiles regex fixes are a separate diff.
3. Blind run cannot merge a real PR safely here; merge and cleanup Acceptance lines are proven against faked gh plus real temporary git repositories.
