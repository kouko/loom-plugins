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

### Wave 3 — integration fixes from the complete-suite RED
**W3-01 Restore skill guide navigation** after: W2-01 acceptance: 5
- Files: `loom-workflow/skills/whats-next/README*`
- Test: A5 positive: root-readme-backlink; negative: missing-localized-backlink. Reuse `tests/test_readme_navigation.py` and its adversarial module; all three new guides must preserve required destinations.
- Risk: agent-decided — REQ-5; missing navigation class searched across every changed guide and catalog; preserve all existing link checks.

**W3-02 Account for the admitted skill in measured budgets** after: W3-01 acceptance: 5
- Files: `docs/loom/evidence/mechanisms.yaml`, `loom-code/scripts/check_mechanisms.py`, `tests/test_loom_skill_description_catalog.py`, `loom-workflow/CHANGELOG.md`, `loom-code/.claude-plugin/plugin.json` and derived release mirrors, `loom-code/CHANGELOG.md`, root and plugin README version pins
- Test: A5 positive: registered-skill; negative: undeclared-admission. Reuse `loom-code/tests/test_check_mechanisms.py` and catalog tests; preserve the frozen baseline and unrelated skill accounting.
- Risk: agent-decided — REQ-5; incomplete new-skill admission affects registry, count ceiling and catalog. Explicit exception admits one skill; patch-bump code measurement metadata, no new checker rule or hook.

**W3-03 Align OpenCode invocation inventory** after: W3-02 acceptance: 1,5
- Files: `loom-code/tests/test_opencode_loader.py`, `loom-workflow/README*`, `docs/loom/2026-11-15-whats-next/evidence/`
- Test: A1 positive: loader-generates-invocation; negative: extra-command. A5 positive: measured-command-inventory; negative: unsupported-host-claim. Reuse the existing actual-loader inventory test; retain exact command comparison.
- Risk: agent-decided — REQ-1, REQ-5; user-invocable metadata intentionally exposes the skill through the loader; no separate wrapper is required.

## Simplicity check
- none found

## Questions asked
① — what — 以上是否就是你要的範圍？

## Risks
1. Agent-decided — selection eligibility is probabilistic and host-dependent; native synthetic tests cannot prove installed-host triggering. Publish measured scope only.
2. Agent-decided — no new hook, checker rule, queue or execution API; one counted skill mechanism is added with an explicit budget exception. Earlier unchanged-count estimate was incorrect. Estimated maintained addition 250–400 lines excludes evidence and remains unmeasured.
3. User-decided — first choice plus necessary alternatives, independent whats-next name, and bounded proactive use confirmed with intent. Engineering change skips behavior-confirmation stop.
4. Agent-decided — use invented visible-message fixtures; no new disclosure of private histories. Existing research links are sanitized before publication.
5. Agent-decided — merge requires separate authorization; preserve original worktree. No installed plugin update.
