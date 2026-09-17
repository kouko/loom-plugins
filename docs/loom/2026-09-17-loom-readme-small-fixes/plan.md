# Loom README small fixes — plan
intent: 2026-09-17-loom-readme-small-fixes@1272fd29
charter: 1.0

## Current State Evidence
- Forward: `docs/loom/README.md:30` "survive only in git history. They stay in" — "They" can bind to the removed stores.
- Reverse: no test reads these lines; probes of 2026-09-16-clean-stale-references scan the frozen-store section and codex-tools mentions only.
- Error: `docs/loom/README.md:16` links `maps/`; `docs/loom/maps/` is absent (all other README links resolve, checked).
- Data: `loom-workflow/skills/decision-map/SKILL.md:47` creates `docs/loom/maps/<map-id>/` on first use.
- Boundary: only `docs/loom/README.md`; the maps row and its description stay.

## Task DAG

**W1-01 README wording and maps link**  after: none  acceptance: 1, 2, 3
- Files: docs/loom/README.md
- Test: A1 positive: plans-named-as-subject; negative: bare-they-absent. A2 positive: all-links-resolve; negative: maps-link-absent. A3 positive: maps-path-still-named; boundary: maps-row-kept.
- Risk: Unlink maps/ rather than delete the row — it is a create-on-first-use store path. agent-decided.

## Questions asked
① — what — 你要的是修好 README 剩下的兩個小問題……這樣對嗎？

## Risks
1. Previous change broke live entries by trusting a scan; every target was re-checked on disk before editing.
