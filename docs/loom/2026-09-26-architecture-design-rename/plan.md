# Complete the architecture-design rename — plan
intent: 2026-09-26-architecture-design-rename@3a2e8fa9
charter: 1.1

## Current State Evidence
- Forward: loom-design/skills/architecture-design/SKILL.md frontmatter exposes the renamed tool and validator command.
- Reverse: loom-code/contract/manifest.yaml tools and standing_docs link ARCHITECTURE.md to architecture-design.
- Error: loom-design/README.md tool table still links the removed skill directory; test_architecture_skill.py accepts the old prefix.
- Data: docs/loom/2026-09-25-standing-architecture-doc/attestation.json contains a rewritten command with its original digest.
- Boundary: docs/loom/memory/big-rename-operative-frozen-sweep.md preserves historical evidence while updating operative references.

## Task DAG
### Wave 1 — complete and guard the rename
**W1-01 Repair stale operative references and preserve historical evidence** after: none acceptance: 1, 2, 3, 4, 5, 6
- Files: loom-design/, loom-code/skills/write-plan/SKILL.md, loom-code/contract/manifest.yaml, tests/, README.md, .claude-plugin/marketplace.json, docs/loom/2026-09-25-standing-architecture-doc/, docs/loom/evidence/mechanisms.yaml
- Test: A1 positive: exact-name; negative: old-alias. A2 positive: producer; negative: stale-tool. A3 positive: registration; negative: stale-description. A4 positive: routes; negative: dead-link. A5 positive: validator-import; negative: stale-path. A6 positive: documentation-links; boundary: frozen-evidence.
- Risk: Agent-decided: retain the completed directory rename and restore historical records from the branch base. Preserve existing validator coverage; strengthen test_architecture_skill.py's prefix assertion to exact identity. Existing adversarial programs remain adversary-owned.

**W1-02 Synchronize releases and validate the cumulative change** after: W1-01 acceptance: 6, 7
- Files: loom-code/, loom-design/, README.md, tests/, docs/loom/2026-09-26-architecture-design-rename/
- Test: A6 positive: synchronized-minor-releases; negative: stale-version-pin. A7 positive: complete-suite-and-checks; boundary: independent-review-and-adversarial-cases.
- Risk: Agent-decided: release loom-code 3.19.0 and loom-design 2.5.0 for contract and routing changes; include matching changelog entries and existing version-pin rewrites. Preserve prior changelog sections verbatim.

## Simplicity check
- none found

## Questions asked
- none — existing confirmed intent; the user authorized completing the rename and making the existing PR mergeable.

## Risks
1. User-decided: no backward-compatible alias; ARCHITECTURE.md and architecture-conformance remain unchanged.
2. Agent-decided: update the existing PR after verification; actual merge is outside this request.
3. Historical commands describe historical commits and must not be rewritten to match current paths.
