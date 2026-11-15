# Sandbox network recovery — plan
intent: 2026-11-16-codex-sandbox-network-recovery@b78044f02f152f0d38179d597330b78150b066fe
charter: 1.1

## Current State Evidence
- Forward: `loom-code/skills/ship/SKILL.md` §3 invokes the canonical publisher; the agent controls its enclosing execution context.
- Reverse: `loom-code/scripts/loom_checker/command_handlers/publish.py` `run_publish_external` inherits process restrictions; Python cannot grant host-tool permissions.
- Error: `loom-code/skills/ship/SKILL.md` §3 stops on missing remedies without identifying sandbox connectivity as a recoverable execution condition.
- Data: `docs/loom/research/2026-11-15-codex-sandbox-gh-connectivity.md` Findings records identical read-only API queries failing inside restrictions and succeeding with host execution.
- Boundary: `loom-code/skills/ship/SKILL.md` §5 keeps merge through land; host-context recovery must preserve authorization and denial boundaries.

## Task DAG
### Wave 1
**W1-01 Repair host-aware network recovery guidance** acceptance: 1, 2, 3, 4
- Files: loom-code/skills/ship/SKILL.md, loom-code/tests/test_ship_station_text.py, docs/loom/2026-11-16-codex-sandbox-network-recovery/
- Test: A1 positive: connectivity-evidence; negative: auth-not-network. A2 positive: same-command-retry; negative: unauthorized-retry. A3 positive: denied-stops; boundary: failed-retry. A4 positive: scenario-evidence; negative: unsupported-success. Existing station tests retained; blind scenario probes validate agent decisions.
- Risk: agent-decided — repair guidance without a privilege-granting subsystem. Preserve all existing test_ship_station_text.py coverage; add only distinct missing recovery boundaries. Search complete Ship guidance and publication diagnostics for the premature-stop class before editing.

### Wave 2
**W2-01 Release metadata and retained evidence** after: W1-01 acceptance: 4
- Files: loom-code/.claude-plugin/plugin.json, loom-code/CHANGELOG.md, README.md, loom-code/README.md, loom-code/README.ja.md, loom-code/README.zh-TW.md, loom-code/tests/test_write_plan_station_text.py, generated manifests
- Test: A4 positive: synchronized-release; negative: stale-version. Run existing release synchronization checks and full package inventory.
- Risk: agent-decided — minor bump for station guidance; use authoritative manifest and generator. Only existing README version strings are changed; no new documentation surfaces.

## Simplicity check
- Narrow release edits to existing plugin READMEs and invoke the existing manifest generator without modifying it — taken

## Questions asked
① — what — 以上是否就是你要的修正範圍？

## Risks
1. agent-decided — This is engineering guidance repair, not a new CLI, network service or host configuration change. No spec or new generic recovery framework is needed.
2. user-decided — kouko confirmed the restatement with「是」and explicitly requested「完成本機修正與驗證 之後 幫我合併」; publication and merge authorization persist, acceptance remains pending.
3. agent-decided — Host-network retry requires the host's permitted mechanism; platform denial is terminal for that attempt. A transport error alone does not prove DNS or authentication state.
4. agent-decided — Record decisions and sources here; retain all experimental failures. The existing research note supplies the durable evidence, so no duplicate memory carrier is required.
