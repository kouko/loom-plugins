# 2026-10-23-memory-and-agents-md-fix — plan
intent: 2026-10-23-memory-and-agents-md-fix@1eca278a
charter: 1.1

## Current State Evidence
- Forward: docs/loom/memory/ — empty store (no entries for this change yet)
- Reverse: AGENTS.md:147-149 — stale "three manifests must sync" description
- Error: loom-code/tests/test_adversarial_version_metadata_sync.py — 8 tests that fail when derived manifests are hand-edited instead of SSOT+sync
- Data: docs/loom/memory/ — target store for git-memory trailers
- Boundary: loom-workflow/skills/git-memory/SKILL.md:102-111 — pre-finalize deadline rule

## Task DAG

**W0-01 Add git-memory trailers for Direction D and version-bump lessons**  after:  acceptance: 1
- Files: docs/loom/memory/ (via commit trailers)
- Test: A1 positive: two trailers present in git log; negative: missing Decision/Learning/Gotcha
- Risk: agent-decided — trailers must land before finalize-review per Direction D

**W0-02 Fix AGENTS.md manifest description**  after: W0-01  acceptance: 2
- Files: AGENTS.md
- Test: A2 positive: "three manifests" text removed, SSOT+derived structure described; negative: old text still present
- Risk: agent-decided — wording change only, no behaviour change

**W0-03 Run git-memory and version-sync tests**  after: W0-02  acceptance: 3
- Files: (no new files)
- Test: A3 positive: git-memory trailers verified, all version-sync tests pass; negative: any fail
- Risk: agent-decided — verification only

## Simplicity check
- none found

## Questions asked
1 — what — 是否繼續錄製兩條 lesson 與修正 AGENTS.md（用戶已確認 yes）
2 — behaviour — 實作細節：memory trailer 格式、version bump 流程（已於決策點 ① 記錄）
3 — done — 兩條 lesson 與 AGENTS.md 修正均已完成

## Risks
1. agent-decided — memory trailers must land before finalize-review per the rule this change records
2. agent-decided — AGENTS.md wording change only, no behaviour change