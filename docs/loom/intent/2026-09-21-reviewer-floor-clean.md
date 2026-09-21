change_id: 2026-09-21-reviewer-floor-clean
kind: engineering
status: confirmed 2026-09-21
needs-design: no
publication: automatic

## Problem
The reviewer-floor branch from PR #35 has merge conflicts with main (reviewers.py). This clean branch separates the non-conflicting documentation and cleanup commits for independent delivery.

## Proposed outcome
Deliver the documentation updates and dead-code removal from the original reviewer-floor branch without the conflicting JSON version-bump logic (which is already in main via PR #40).

## Acceptance
1. write-plan SKILL.md documents the coverage-naming rule for protected functions
2. git-memory SKILL.md adds cross-reference to closing-review for finalize-review timing
3. Dead modules heading_window.py and sibling_import.py (and their tests) are removed

## Constraints
- Only documentation updates and dead-code removal
- No changes to reviewer_floor_for_paths logic (already in main)
- No changes to JSON version-bump detection (already in main)

## Open questions
- none
