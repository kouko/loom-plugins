# Split-commit reference does not survive squash — plan
intent: 2026-09-19-split-commit-reference-does-not-survive-squash@99e4ca95
charter: 1.0

## Current State Evidence
- Forward: docs/loom/2026-09-18-modular-adversary-recipes/evidence/rule-correspondence.md:11,19 — recorded two commit SHAs from PR #33's own pre-squash development branch.
- Reverse: test_adversary_layout.py's `_original`/`_at_split` read those SHAs via `git show <sha>:<path>`; both are absent from origin/main, confirmed only via a clone sharing no local machine's object database.
- Error: a fresh clone of origin/main at 9bf87029 fails 31 of 35 cases in loom-code/scripts/test_adversary_recipe_shape.py with `fatal: path '...' exists on disk, but not in '<sha>'`.
- Data: squash-merge commit 9bf87029 and its sole parent a1891ed1 are both remote-reachable and carry the exact pre/post-split tree content the stale SHAs were meant to name.
- Boundary: no other file in the repository references either stale SHA (repo-wide grep, zero hits beyond the one correspondence document).

## Task DAG

**W0-01 Replace both stale commit references with the squash-surviving commits**  after: —  acceptance: 1, 2
- Files: docs/loom/2026-09-18-modular-adversary-recipes/evidence/rule-correspondence.md
- Test: A1 positive: independent-fresh-clone-pytest-run; A2 positive: independent-fresh-clone-sha-resolution.
- Risk: A local worktree sharing this machine's git object database cannot verify this fix (it would false-pass even on the broken text) — verification requires a clone independent of any machine that worked on PR #33. agent-decided.

## Questions asked
1 — consequence — 使用者選擇：先另開一個小 PR 修 main，PR #34 先擱置，main 恢復正常後再回來確認 #34 的 CI

## Risks
1. This fix touches only a documentation reference; the underlying design (reading migration evidence from historical git state rather than the working tree) is intentional and unchanged, per test_adversary_layout.py's own docstring reasoning.
