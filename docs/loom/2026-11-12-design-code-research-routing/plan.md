# Separate research ownership with small stage handoffs — plan
intent: 2026-11-12-design-code-research-routing@ed10de55
spec: docs/loom/2026-11-12-design-code-research-routing/spec.md@9ce68eef
charter: 1.1

## Task DAG

**W1-01 Implement separate research ownership and bounded stage handoffs** after: none acceptance: 1, 2, 3, 4, 5, 6
- Files: loom-design/skills/, loom-code/skills/, loom-design/tests/, loom-code/tests/, loom-code/contract/manifest.yaml, loom-code/scripts/check_mechanisms.py, docs/loom/evidence/mechanisms.yaml, tests/
- Test: A1 positive: D1; negative: D3. A2 positive: C1-C5; negative: N1-N5. A3 positive: D1; boundary: D2. A4 positive: F1; negative: unsupported-superiority. A5 positive: F1; boundary: F2. A6 positive: actual-trajectories; negative: static-only.
- Risk: agent-decided — REQ-1–6 keep methods inside owned skills and stage edits short. Preserve existing ownership, evidence and verification boundaries; extend package invariants only as needed, with independent behavioral cases at acceptance.

**W2-01 Synchronize release metadata and declared capability budget** after: W1-01 acceptance: 1
- Files: loom-code/.claude-plugin/plugin.json, loom-design/.claude-plugin/plugin.json, loom-code/CHANGELOG.md, loom-design/CHANGELOG.md, README.md, loom-code/README*.md, loom-design/README*.md, .claude-plugin/marketplace.json
- Test: A1 positive: synchronized-release; boundary: discoverable-design-research. Run existing metadata and manifest checks; update derived manifests and current-release pin through the established release packet.
- Risk: agent-decided — REQ-1 adds one capability with explicit budget accounting; bump code/design minor versions before review attestation. Preserve existing generated-manifest conventions and update the release pin in loom-code/tests/test_write_plan_station_text.py.

**W3-01 Preserve meaningful timeout verification under observed fixture startup** after: W2-01 acceptance: 6
- Files: loom-code/tests/test_external_review.py, loom-code/tests/test_external_review_adversarial.py, loom-code/CHANGELOG.md
- Test: A6 positive: complete-suite; negative: process-group-kill-disabled. Reproduce the five baseline failures, retain live-path evidence, then verify meaningful deadlines, descendant cleanup and blocked-input behavior.
- Risk: agent-decided — Newly measured fake-CLI startup exceeds existing test deadlines in both installed interpreters. Repair only test fixtures and timing preconditions; preserve production defaults and prove the tests still reject broken termination. This supports, not replaces, research behavior trials.

**W4-01 Resolve unsupported-context ambiguity before the first recommendation** after: W3-01 acceptance: 4, 5, 6
- Files: loom-code/skills/engineering-research/SKILL.md, loom-design/skills/design-research/SKILL.md
- Test: A4 positive: cold-initial-choice; negative: assumed-caller. A5 positive: followup-consistency; boundary: changed-conditions. A6 positive: prechallenge-operations; negative: source-only-proof.
- Risk: agent-decided — Replace ambiguous tentative-choice permission with disclosed decisive conditions and conditional alternatives. This corrects the first observed premise-selection defect, not prior catalog/word-budget repairs; retain failed evidence and existing Review episode.

**W4-02 Drive admitted-skill boundaries through the existing CLI entry** after: W4-01 acceptance: 1
- Files: loom-code/tests/test_check_mechanisms.py (entry exercised: check_mechanisms.main)
- Test: A1 positive: CLI-admit26; boundary: CLI-reject27. Preserve fixtures and externally observable count, exit status and rejection evidence; add no new test.
- Risk: agent-decided — Move both edited cases from internal measurement helpers to the actual --measure entry, preserving budget semantics and unchanged legacy cases.

**W5-01 Integrate the newly published trunk release without losing research routing** after: W4-02 acceptance: 1, 2, 3, 4, 5, 6
- Files: README.md, loom-code/CHANGELOG.md, loom-code/.claude-plugin/plugin.json, loom-code/README*.md, loom-code/tests/test_write_plan_station_text.py, derived manifests, upstream merge paths, docs/loom/2026-11-12-design-code-research-routing/research/002-upstream-design-compatibility.md
- Test: A1 positive: synchronized-release; boundary: preserve-upstream367. Run the existing release pin before the bump to observe rejection, then synchronize 3.68.0 and run focused checks; repeat complete integration and retained adversarial commands.
- Risk: agent-decided — Upstream ab40f0e6 published 3.67.0 after review. Preserve upstream progress and research routing while resolving conflicts. This new integration obligation preserves W4 requirements and retries; continue the same episode at terminal Round 3.

## Simplicity check

- none found

## Questions asked

① — what — 這是否就是你要的範圍？

## Risks

1. agent-decided — Research invocation alone does not establish good judgment. Behavioral verification must inspect actual supported choices, follow-up responses and saved records against REQ-4–6.
2. agent-decided — Add no global router, new artifact type, trigger ledger or mandatory evaluation checklist; existing stage and research records carry the handoff.
3. agent-decided — Existing engineering research ownership and portable plugin boundaries remain protected; design research is separately discoverable without reading code-plugin internal resources.
4. user-decided — Research owns detailed methods, comparison and conclusion maintenance; original stages stay as simple as possible.
5. agent-decided — Full package suite follows kickoff defaults; installed plugin behavior and model-wide activation rates remain outside claims unless actually measured.
6. agent-decided — W2 includes new CHANGELOG entries, README versions, derived manifest synchronization and CURRENT_VERSION pin rewrite; do not claim a release before review and publication evidence.
7. agent-decided — Build integration found incomplete new-skill installation/catalog/navigation accounting and a review paragraph caught by the existing verdict-reuse guard. Preserve frozen baselines and protection semantics while covering every affected catalog and localized link.
8. agent-decided — Keep capture-intent within its existing word cap by shortening only the added handoff; synchronize design release pins in loom-design/tests/spec/test_capture_intent_contract.py and marketplace metadata, preserving historical changelog entries.
9. agent-decided — W3 addresses a newly observed verification precondition: baseline 70a05fd7 reproduces all five timeout failures, and fresh CLI startup measured about 2.8s in both installed interpreters. W1/W2 remain completed; no research requirement or production behavior changes.
10. agent-decided — Batch the actual unsupported initial-context finding from acceptance and both reviewers with the CLI-entry test finding. W4 preserves confirmed requirements and fixes distinct newly observed obligations without resetting prior task retries or the bounded Review episode.
