# Unified lightweight roadmap — plan
intent: 2026-11-16-roadmap-simplification@6c3b1663
spec: docs/loom/2026-11-16-roadmap-simplification/spec.md@ebd634a4
charter: 1.1

## Task DAG

### Wave 1 — Replace planning ownership

**W1-01 Create the lightweight roadmap skill and evaluation cases** after: none acceptance: 1,2,5
- Files: loom-workflow/skills/roadmap/, loom-workflow/tests/roadmap/, docs/loom/2026-11-16-roadmap-simplification/evidence/
- Test: A1 positive: ordinary-document; boundary: existing-document. A2 positive: update-verified-result; negative: conflicting-evidence. A5 positive: authorized-handoff; negative: plan-as-execution-authority.
- Risk: REQ-1/REQ-2/REQ-5; agent-decided one instruction owner without runtime; matched baseline and skill cases must distinguish behavior from exact prose.

**W1-02 Connect existing entry points and replace map discovery** after: W1-01 acceptance: 2,3
- Files: loom-design/skills/capture-intent/, loom-workflow/skills/whats-next/, loom-workflow/skills/handoff/, loom-workflow/skills/using-loom-workflow/, loom-workflow/tests/whats-next/, loom-workflow/tests/handoff/, loom-design/tests/
- Test: A2 positive: routed-planning; boundary: viable-work-continues. A3 positive: roadmap-discoverable; negative: map-discovery-removed.
- Risk: REQ-2/REQ-3; agent-decided short ownership pointers; preserve existing handoff/whats-next tests and behavior, extend planning routing without introducing mandatory document creation.

### Wave 2 — Retire obsolete contracts

**W2-01 Remove map runtime and its intent contract** after: W1-02 acceptance: 3,4
- Files: loom-workflow/skills/decision-map/, loom-workflow/tests/decision-map/, loom-code/scripts/loom_checker/rule_checks/intent.py, loom-code/tests/test_loom_checker_intent.py, loom-code/contract/, loom-design/skills/capture-intent/templates/intent.md, loom-code/tests/test_contract_manifest.py, loom-workflow/tests/scripts/test_skill_count.py
- Test: A3 positive: replacement-inventory; negative: dangling-map-consumers. A4 positive: historical-files-retained; boundary: foreign-checkout-unchanged.
- Risk: REQ-3/REQ-4; existing map and intent tests define removed coverage; narrow map-only validation intentionally, preserve unrelated schema checks and historical records.

**W2-02 Retire repository-purpose drafting and preserve session goals** after: W2-01 acceptance: 3,4
- Files: loom-workflow/skills/goal-create/, loom-workflow/tests/goal-create/, loom-code/contract/templates/PURPOSE.md, loom-code/contract/README.md, loom-code/scripts/check_contract_citations.py, loom-code/tests/test_check_contract_citations.py, loom-code/tests/test_probes_language_policy.py, loom-design/tests/interface/test_north_star_purpose_retarget.py
- Test: A3 positive: session-goals-preserved; negative: arc-offers-absent. A4 positive: existing-purpose-readable; boundary: no-project-rewrite.
- Risk: REQ-3/REQ-4; test_skill_md.py and test_readmes.py lose ARC-only coverage; preserve goal shape/lint/input-floor and host activation tests; historical references remain history.

### Wave 3 — Release and verify

**W3-01 Synchronize guides, inventories and release packet** after: W2-02 acceptance: 1,3
- Files: README.md, loom-code/, loom-design/, loom-workflow/, .claude-plugin/marketplace.json, tests/, docs/loom/memory/, docs/loom/README.md
- Test: A1 positive: guide-ordinary-roadmap; negative: mandatory-roadmap-claim. A3 positive: thirty-skills; negative: stale-release-metadata.
- Risk: REQ-1/REQ-3; agent-decided minor bump packet includes CHANGELOG entries, README versions and release-pin rewrites; sync generates derived manifests; no installed-cache or user-project update.

**W3-02 Run behavioral boundary and integration verification** after: W3-01 acceptance: 1,2,3,4,5
- Files: loom-workflow/tests/roadmap/, docs/loom/2026-11-16-roadmap-simplification/evidence/
- Test: A1 positive: fresh-plan; boundary: absent-plan. A2 positive: resume; negative: failed-progress. A3 positive: session-retained; negative: map-runtime-absent. A4 positive: preserved-data; boundary: conflicting-edits. A5 positive: evidence-linked; negative: unauthorized-execution.
- Risk: REQ-1–REQ-5; agent-decided independent adversary and semantic trials complement structural checks; full package suite required; no installed-host success inferred from source evaluation.

## Simplicity check
- Reuse the existing manifest generator without editing it — taken

## Questions asked

① — what — 這個目標與驗收範圍符合你的意思嗎？
Clarification — what — 你說的「排程控制」主要指什麼？這會決定 roadmap skill 是協助規劃，還是要負責實際執行。

## Risks

1. Shared intent and goal tests must preserve unrelated coverage; retirement deliberately removes map-only and ARC-only capabilities rather than disguising coverage loss.
2. Existing family-relocation records remain untouched; source retirement removes their operational support, not their history. No automatic converter or cross-checkout edits.
3. No timed/background execution is authorized. Skill evaluations must challenge accidental execution, invented dates, forced scaffolding, ambiguous documents and unverified completion.
4. Behavioral trials use existing host-native agents and controlled fixture documents; retain matched no-skill baselines, input prompts, observed outputs, failures and limits. No external-vendor dispatch without opt-in.
5. Version targets are agent-decided at the last functional fix; include each changed plugin's minor bump, synchronized changelog/README pins and derived manifests before finalization.
6. Engineering exemption applies to decision point ②; user selected unified ownership explicitly. Rewritten spec reviewed independently at ebd634a4; original review does not cover it.
7. Publication remains authorized after checks; merge separate. Preserve GitHub connectivity failures; unavailable remote evidence is unconfirmed, not a delivery pass.

8. user-decided — On 2026-11-16 the user explicitly waived only the skill-authoring 15-percentage-point improvement threshold; retain semantic evaluation, all tests, independent reviews and acceptance. No comparative improvement is claimed.
