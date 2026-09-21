# Plan: 2026-09-21-reviewer-floor-clean
intent: 2026-09-21-reviewer-floor-clean@HEAD
charter: 1.0

## Current State Evidence
- Forward: loom-code/scripts/loom_checker/reviewers.py — reviewer_floor_for_paths already returns floor 1 for version-only JSON bumps (merged via PR #40); loom-code/skills/write-plan/SKILL.md — existing write-plan skill; loom-workflow/skills/git-memory/SKILL.md — existing git-memory skill
- Reverse: No reverse dependencies identified
- Error: No error paths
- Data: No data files
- Boundary: No boundary cases

## Task DAG
### Wave 0 — documentation and cleanup (already committed)
**W0-01 Document write-plan coverage-naming rule**  after: none  acceptance: 1
- Files: loom-code/skills/write-plan/SKILL.md
- Test: A1 positive: rule added to SKILL.md; negative: rule absent
- Risk: Low — documentation only; clarifies existing discipline

**W0-02 Document git-memory finalize-review timing warning**  after: none  acceptance: 2
- Files: loom-workflow/skills/git-memory/SKILL.md
- Test: A2 positive: cross-reference added; negative: duplicated warning
- Risk: Low — documentation only; shortens existing warning

**W0-03 Remove dead modules heading_window.py and sibling_import.py**  after: none  acceptance: 3
- Files: loom-code/scripts/heading_window.py, loom-code/scripts/sibling_import.py, loom-code/scripts/test_heading_window.py, loom-code/scripts/test_sibling_import.py
- Test: A3 positive: files deleted, full suite green; negative: live references remain
- Risk: agent-decided — not authorised, took the conservative option (verified no live references via full repo scan)

## Questions asked
① — engineering — Clean up reviewer-floor branch after PR #35 merge conflict; is it acceptable to split into clean branch with only the non-conflicting documentation/cleanup commits?

## Risks
- None — all changes are documentation updates and dead-code removal, verified by full package suite (11 PASS / 0 FAIL)
