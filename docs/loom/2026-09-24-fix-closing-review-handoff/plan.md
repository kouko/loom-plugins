# A fix round starts from every blocking finding, grouped by defect class — plan
intent: 2026-09-24-fix-closing-review-handoff@cd7891e8
charter: 1.0

## Current State Evidence
- Forward: `loom-code/skills/closing-review/SKILL.md:263` says Round 2 batches fatal and important findings, but names neither acceptance-testing findings nor grouping by class.
- Reverse: `loom-code/skills/closing-review/SKILL.md:292-296` only records each non-passing reviewer verdict, then points at Build §2's per-fix sibling search.
- Error: Codex review 2026-09-24 found the recorded `--rule <verdict>` is the verdict name, so grouping by it merges unrelated defects.
- Data: `loom-code/scripts/test_simplified_station_text.py:406` pins the record-failure sentence verbatim; `test_fix_scope_text.py` allows exactly one closing-review sentence naming class and Build §2.
- Boundary: `loom_checker.py --list-rules` lists 26 rules; `check_mechanisms.py --baseline main` counts prose gates, so unmarked prose adds none.

## Task DAG

### Wave 0 — the hand-off rule

**W0-01 Collect and group blocking findings before a fix round**  after: —  acceptance: 1, 2, 3, 4, 5
- Files: `loom-code/skills/closing-review/SKILL.md`, `loom-code/scripts/test_fix_handoff_text.py`
- Test: A1 positive: list-covers-reviewers-and-acceptance-testing; negative: subset-fix-forbidden. A2 positive: shared-class-one-handoff; negative: verdict-label-not-class. A3 positive: record-is-disclosure-only; boundary: record-sentence-kept-verbatim. A4 positive: grouping-example-stated; negative: weakened-rule-fails-pins. A5 positive: rule-count-26; negative: no-dispatch-or-gate-wording.
- Risk: `test_simplified_station_text.py:406` and `test_fix_scope_text.py` pin neighbouring sentences; both kept, coverage preserved. New prose avoids "Build §2" so one pointer remains; agent-decided.

**W0-02 Bind hand-offs to one fix round; pin sentences exactly; graduate probe**  after: W0-01, W1-01  acceptance: 1, 2
- Files: `loom-code/skills/closing-review/SKILL.md`, `loom-code/scripts/test_fix_handoff_text.py`, `loom-code/CHANGELOG.md`, `docs/loom/2026-09-24-fix-closing-review-handoff/evidence/probes/test_handoff_pins_reject_inverting_insertions.py`
- Test: A1 positive: every-handoff-same-round-before-reviewers-resume; negative: class-per-round-rewrite-fails. A2 positive: exact-sentence-pins; negative: inverting-insertions-fail.
- Risk: adversary findings: ordered-word pins accepted meaning-reversing insertions; separate hand-offs were not bound to one round. Probe graduates into the test file and leaves the store; agent-decided.

### Wave 1 — release

**W1-01 Minor release metadata 3.13.0**  after: W0-01  acceptance: 5
- Files: `loom-code/plugin.json`, `loom-code/.claude-plugin/plugin.json`, `loom-code/.codex-plugin/plugin.json`, `loom-code/CHANGELOG.md`, `loom-code/scripts/test_write_plan_station_text.py`, `loom-code/README.md`, `loom-code/README.ja.md`, `loom-code/README.zh-TW.md`
- Test: A5 positive: versions-synchronized-3.13.0; negative: check-mechanisms-not-raised.
- Risk: `test_write_plan_station_text.py` pins 3.12.0; rewritten, coverage preserved. Root `README.md` version edited in the same commit; minor because station guidance changes; agent-decided.

## Questions asked
① — what — 開吧
① — done — 對 在實作後請做 dogfood testing 確保如預期動作

## Risks
1. Acceptance 4 is behavioural; independent acceptance testing proves it with seeded trials under `claude -p --plugin-dir`, per the user's dogfood request, not by reading prose.
2. The narrow-change auto-skip was computed on an intent-only delta; the skill and test edits make the delta non-narrow, so the full flow runs; agent-decided.
