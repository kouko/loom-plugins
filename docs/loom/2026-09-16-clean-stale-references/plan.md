# Plan: Clean stale references — plan
intent: 2026-09-16-clean-stale-references@a388bc09
charter: 1.0

## Current State Evidence
- Forward: `docs/loom/README.md:35-40` lists obsolete paths like `plans/` and `specs/`.
- Reverse: `loom-design/skills/write-spec/SKILL.md:173` references "ten completeness questions".
- Error: `loom-workflow/skills/distill-sessions/references/codex-tools.md:8` points to `codex-tools.md`, which does not exist.
- Data: N/A.
- Boundary: Changes are limited to documentation and skill-instruction prose; no logic changed.

## Task DAG

**W1-01 Update distill-sessions reference**  after: none  acceptance: 1
- Files: `loom-workflow/skills/distill-sessions/references/codex-tools.md`
- Test: A1 positive: internal-dispatch-found; negative: codex-tools-missing
- Risk: None. agent-decided.

**W1-02 Update docs/loom/README.md frozen store list**  after: none  acceptance: 2
- Files: `docs/loom/README.md`
- Test: A2 positive: frozen-paths-removed; negative: obsolete-paths-missing
- Risk: None. agent-decided.

**W1-03 Update write-spec completeness questions reference**  after: none  acceptance: 3
- Files: `loom-design/skills/write-spec/SKILL.md`
- Test: A3 positive: ten-questions-removed; negative: completeness-rule-present
- Risk: None. agent-decided.

## Questions asked
- none

## Risks
- None.
