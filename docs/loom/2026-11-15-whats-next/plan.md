# Evidence-grounded next action — plan
intent: 2026-11-15-whats-next@2a4c4321
spec: docs/loom/2026-11-15-whats-next/spec.md@71621f97
charter: 1.1

## Task DAG
### Wave 0 — freeze evidence and baseline
**W0-01 Freeze synthetic cases and ordinary-answer baseline** after: none acceptance: 5
- Files: `loom-workflow/tests/whats-next/behavior_cases.json`, `loom-workflow/tests/whats-next/trigger_queries.json`, `docs/loom/2026-11-15-whats-next/evidence/`
- Test: A5 positive: matched-baseline; negative: unmeasured-host-claim. Freeze cases before draft; record isolated native-agent outputs and scoring criteria without private histories.
- Risk: agent-decided — REQ-5; baseline may already pass, so preserve negative comparative evidence and report insufficient incremental benefit rather than manipulate cases.

### Wave 1 — advice contract
**W1-01 Implement the bounded advice contract and discoverability** after: W0-01 acceptance: 1,2,3,4,5
- Files: `loom-workflow/skills/whats-next/`, `loom-workflow/tests/whats-next/`, `loom-workflow/skills/using-loom-workflow/SKILL.md`
- Test: A1 positive: grounded-gap; negative: stale-premise. A2 positive: material-alternative; boundary: completed-goal. A3 positive: blocked-direction; negative: viable-plan. A4 positive: authorized-continuation; negative: ungranted-merge. A5 positive: matched-comparison; negative: host-overclaim.
- Risk: agent-decided — REQ-1–REQ-5; require RED discovery before adding the skill, separate description-only selection from loaded behavior, retain adjacent recap routing and actions' original owners.

### Wave 2 — delivery surfaces
**W2-01 Document and version the validated contract** after: W1-01 acceptance: 1,2,3,4,5
- Files: `loom-workflow/README*` and root `README.md`, `loom-workflow/.claude-plugin/plugin.json`, `loom-workflow/CHANGELOG.md`, `loom-workflow/tests/scripts/test_release_metadata.py`, `docs/loom/2026-11-15-whats-next/`, `docs/loom/research/2026-11-14-whats-next-skill-discovery.md`
- Test: A1 positive: readme-advice; negative: recap-confusion. A2 positive: readme-alternatives; boundary: no-quota. A3 positive: readme-proactive; negative: ambient-hook. A4 positive: readme-authority; negative: advice-permission. A5 positive: release-parity; negative: private-locators.
- Risk: agent-decided — REQ-5; minor version 5.25.0 before closing review; generated manifests handled separately; preserve original research and worktree.

## Simplicity check
- none found

## Questions asked
① — what — 以上是否就是你要的範圍？

## Risks
1. Agent-decided — selection eligibility is probabilistic and host-dependent; native synthetic tests cannot prove installed-host triggering. Publish measured scope only.
2. Agent-decided — no new hook, checker rule, queue or execution API; mechanism count unchanged. Estimated maintained addition 250–400 lines excluding review evidence, not a measured result.
3. User-decided — first choice plus necessary alternatives, independent whats-next name, and bounded proactive use confirmed with intent. Engineering change skips behavior-confirmation stop.
4. Agent-decided — use invented visible-message fixtures; no new disclosure of private histories. Existing research links are sanitized before publication.
5. Agent-decided — merge requires separate authorization; preserve original worktree. No installed plugin update.
