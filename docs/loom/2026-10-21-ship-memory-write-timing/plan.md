# 2026-10-21-ship-memory-write-timing — plan
intent: 2026-10-21-ship-memory-write-timing@b83cf75d
charter: 1.1

## Current State Evidence
- Forward: loom-code/skills/ship/SKILL.md:130-140 — Memory write timing rule added
- Reverse: loom-code/skills/ship/SKILL.md:118-128 — existing git-memory + loom-memory routing
- Error: attestation.py:124-126 — digest invalidation check on functional content change
- Data: docs/loom/memory/ — store where git-memory routes qualifying lessons
- Boundary: git-memory/SKILL.md:102-111 — pre-finalization deadline rule

## Task DAG

**W0-01** verify memory timing rule is present  after:  acceptance: 1
- Files: loom-code/skills/ship/SKILL.md
- Test: A1 positive: rule-present; negative: rule-absent
- Risk: agent-decided — no functional code change, only prose timing rule

**W0-02** run ship station tests  after: W0-01  acceptance: 3
- Files: loom-code/tests/test_ship_station_text.py, loom-code/tests/test_ship_worktree_merge.py, loom-code/tests/test_ship_risk_section_agent_decided_door.py
- Test: A3 positive: all-pass; negative: any-fail
- Risk: agent-decided — existing tests validate rule presence

## Simplicity check
- none found

## Questions asked
① — consequence — yes, this is what I want to verify

## Risks
1. agent-decided — no functional code change, only prose timing rule; reversible by revert