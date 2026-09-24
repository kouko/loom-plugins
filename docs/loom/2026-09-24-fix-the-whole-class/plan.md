# Fix rounds fix the whole class of a finding, not only the flagged instance — plan
intent: 2026-09-24-fix-the-whole-class@e394121a
charter: 1.0

## Current State Evidence
- Forward: `loom-code/skills/build/SKILL.md:98-101` makes every fix inside Build and fixes each fatal or important adversary finding, but says nothing about scoping a fix beyond the flagged place.
- Reverse: `loom-code/skills/closing-review/SKILL.md:292-294` opens every fix round by recording non-passing verdicts; no sentence tells the orchestrator to search for siblings first.
- Error: fix-round survey 2026-09-24, 18 of 71 changes show a later round fixing a sibling of an earlier fix; kouko/loom-plugins#46 c14 vs c17/c22 is one case.
- Data: `loom-code/scripts/test_simplified_station_text.py:406` pins the "Before any fix round" sentence verbatim.
- Boundary: `python3 loom-code/scripts/loom_checker.py --list-rules` lists 26 rules; `check_mechanisms.py --baseline main` counts prose gates, so an unmarked sentence adds none.

## Task DAG

### Wave 0 — the rule

**W0-01 Scope every fix to the defect's class before hand-off**  after: —  acceptance: 1, 2, 4
- Files: `loom-code/skills/build/SKILL.md`, `loom-code/skills/closing-review/SKILL.md`, `loom-code/scripts/test_fix_scope_text.py`
- Test: A1 positive: rule-names-class-search-and-acceptance-surfaces; negative: rule-absent-from-other-station. A2 positive: record-states-class-and-places-searched; boundary: none-found-still-recorded. A4 positive: no-gate-marker-and-rule-count-26; negative: no-new-dispatch-wording.
- Risk: `test_simplified_station_text.py:406` pins the fix-round sentence; kept verbatim, coverage preserved. One home for the rule, at most a one-sentence pointer elsewhere; agent-decided.

### Wave 1 — release

**W1-01 Minor release metadata 3.12.0**  after: W0-01  acceptance: 3, 4
- Files: `loom-code/plugin.json`, `loom-code/.claude-plugin/plugin.json`, `loom-code/.codex-plugin/plugin.json`, `loom-code/CHANGELOG.md`, `loom-code/scripts/test_write_plan_station_text.py`, `loom-code/README.md`, `loom-code/README.ja.md`, `loom-code/README.zh-TW.md`
- Test: A3 positive: changelog-names-class-scoped-fixes; negative: no-readme-names-3.11.0-as-current. A4 positive: versions-synchronized-and-rules-26; negative: check-mechanisms-not-raised.
- Risk: `test_write_plan_station_text.py` pins 3.11.0; rewritten, coverage preserved. Root `README.md` carries the version twice and is edited in the same commit; minor because station guidance changes; agent-decided.

## Questions asked
① — what — 先開 A 的 intent
① — done — 對

## Risks
1. Acceptance 3 is a behavioural claim about agents; the acceptance tester proves it with a trial on a seeded case, not by reading the prose.
2. A class search can overreach into unrelated code; the rule bounds it to the change's own delta and the surfaces the mapped Acceptance line names.
