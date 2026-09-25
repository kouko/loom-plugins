# Check every plan for a simpler way to reach the same outcome before Build — plan
intent: 2026-09-25-plan-simplicity-check@1a7f320b
charter: 1.1

## Current State Evidence
- Forward: `loom-code/skills/write-plan/SKILL.md:73` says write-plan has no formal plan review; nothing asks for a simpler shape before Build.
- Reverse: `loom-code/skills/build/SKILL.md:18-34` Build §1 runs only `selection show`; no plan checker runs at Build entry.
- Error: `loom-code/scripts/loom_checker/reviewers.py:85-118` judges narrow from the committed diff, which holds only intent and plan at plan time.
- Data: `loom-code/scripts/loom_checker/command_handlers/plan.py:11-32` and `command_handlers/intake.py:50-52` run the plan rules; `rules.py` lists 26 ids.
- Boundary: `loom-code/skills/closing-review/references/adversarial.md:78-81` says a reused test is left as it is, pinned by `loom-code/tests/test_adversary_protocol.py:107-114`.

## Task DAG

### Wave 0 — the check and its record

**W0-01 plan.field-caps requires a Simplicity check section on charter 1.1 plans**  after: —  acceptance: 2, 4
- Files: `loom-code/scripts/loom_checker/rule_checks/intake.py`, `loom-code/scripts/loom_checker/rules.py`, `loom-code/contract/templates/plan.md`, `loom-code/contract/manifest.yaml`, `loom-code/tests/test_plan_field_caps.py`
- Test: A2 positive: charter-1.1-plan-with-record-passes; negative: charter-1.1-plan-without-record-blocked. A4 positive: narrow-files-skip-accepted; negative: non-narrow-skip-refused.
- Risk: widens `test_plan_field_caps.py` coverage; charter 1.0 plans stay unchecked, so in-flight plans elsewhere keep working; narrow judged from Files entries with the existing classifier; agent-decided.

**W0-02 Plan lens, write-plan dispatch step, Build entry check, station tables**  after: W0-01  acceptance: 1, 3, 5
- Files: `loom-code/skills/closing-review/references/lenses.md`, `loom-code/agents/reviewer.md`, `loom-code/skills/write-plan/SKILL.md`, `loom-code/skills/build/SKILL.md`, `loom-design/skills/capture-intent/SKILL.md`, `loom-design/skills/write-spec/SKILL.md`, `loom-code/tests/test_plan_simplicity_text.py`
- Test: A1 positive: write-plan-dispatches-fresh-plan-lens-reviewer; negative: no-copy-says-no-formal-plan-review. A3 positive: lens-is-loom-code-reviewer; negative: no-loom-workflow-dependency. A5 positive: adoption-recorded-agent-decided; negative: no-user-question.
- Risk: the plan lens scores only deletion-first; Build §1 runs the existing `plan` command; three byte-identical table copies change together; agent-decided.

**W0-03 Adversary marks a reused test with its concern line**  after: —  acceptance: 6
- Files: `loom-code/skills/closing-review/references/adversarial.md`, `loom-code/tests/test_adversary_protocol.py`
- Test: A6 positive: reused-program-gets-concern-line-at-dispatch; negative: reused-test-body-still-unchanged.
- Risk: narrows the pinned "left as it is" sentence to "unchanged except its concern line"; agent-decided.

### Wave 1 — release

**W1-01 loom-code minor release 3.18.0**  after: W0-02, W0-03  acceptance: 2
- Files: `loom-code/plugin.json`, `loom-code/.claude-plugin/plugin.json`, `loom-code/.codex-plugin/plugin.json`, `loom-code/CHANGELOG.md`, `loom-code/README.md`, `loom-code/README.ja.md`, `loom-code/README.zh-TW.md`, `loom-code/tests/test_write_plan_station_text.py`
- Test: A2 positive: versions-synchronized-3.18.0; negative: check-mechanisms-net-unchanged.
- Risk: minor for station and rule-text changes; no new mechanism, so no budget exception; agent-decided.

**W1-02 loom-design patch release 2.4.1**  after: W1-01  acceptance: 1
- Files: `loom-design/plugin.json`, `loom-design/.claude-plugin/plugin.json`, `loom-design/.codex-plugin/plugin.json`, `loom-design/CHANGELOG.md`, `loom-design/README.md`, `loom-design/README.ja.md`, `loom-design/README.zh-TW.md`, `README.md`
- Test: A1 positive: loom-design-versions-synchronized-2.4.1; negative: stale-2.4.0-pin-detected.
- Risk: patch because only the mirrored station table changes in loom-design; agent-decided.

### Wave 2 — suite fixes

**W2-01 Station prose back within the station files' structural limits**  after: W1-02  acceptance: 1, 5
- Files: `loom-code/skills/write-plan/SKILL.md`, `loom-code/skills/write-plan/references/plan-simplicity.md`, `loom-code/skills/build/SKILL.md`, `loom-design/skills/capture-intent/SKILL.md`, `loom-design/skills/write-spec/SKILL.md`, `loom-code/tests/test_plan_simplicity_text.py`
- Test: A1 positive: pointer-and-reference-state-the-dispatch; negative: write-plan-body-under-word-cap. A5 positive: reference-records-agent-decided; negative: build-entry-names-no-other-station.
- Risk: class "W0-02 prose breaks station structural limits" searched across the three station files W0-02 edited; detail moves to a write-plan reference; agent-decided.

### Wave 3 — adversary fixes

**W3-01 Skip line with a missing Files field blocks instead of crashing; graduate the probe**  after: W2-01  acceptance: 2, 4
- Files: `loom-code/scripts/loom_checker/rule_checks/intake.py`, `loom-code/skills/build/SKILL.md`, `docs/loom/2026-09-25-plan-simplicity-check/evidence/probes/test_plan_skip_missing_files.py`, `loom-code/tests/test_plan_skip_missing_files.py`
- Test: A2 positive: missing-files-with-record-blocks-cleanly; negative: missing-files-never-internal-error. A4 positive: narrow-skip-still-accepted; negative: skip-with-missing-files-blocks.
- Risk: class "the plan check can fail without a BLOCK" searched in intake.py and Build entry; Build stops on any non-zero exit; probe moves unchanged; agent-decided.

### Wave 4 — closing review round 1 fixes

**W4-01 The simplicity step can be followed as written**  after: W3-01  acceptance: 1, 5
- Files: `loom-code/skills/write-plan/references/plan-simplicity.md`, `loom-code/skills/write-plan/SKILL.md`, `loom-code/skills/closing-review/references/lenses.md`, `loom-code/agents/reviewer.md`, `loom-code/CHANGELOG.md`, `loom-code/tests/test_plan_simplicity_text.py`
- Test: A1 positive: check-runs-before-the-checker-commands; negative: no-both-checks-pass-precondition. A5 positive: lens-maps-shapes-to-deletion-first-findings; negative: plan-lens-has-no-fix-round.
- Risk: class "the plan-simplicity step cannot be followed as written" searched in the reference, SKILL pointer, plan lens and reviewer input; write-plan stays under its word cap; agent-decided.

## Simplicity check
- Fold the record into plan.field-caps instead of a new rule id — taken
- Run the existing plan command at Build entry instead of new handler wiring — taken
- Base the plan lens on deletion-first instead of a new dimension — taken
- Merge the station-table task into the lens task — taken
- Grandfather via charter 1.0 alone — declined: in-flight charter 1.0 plans elsewhere would fail; bump the template to charter 1.1

## Questions asked
① — done — 對，checker 擋
① — consequence — 「沒有簡化檢查紀錄就不能進 Build」由 checker 擋（vs 只寫成文字）
① — what — adversary 沿用既有測試時第一次派出就標好 concern: 也一起做

## Risks
1. user-decided — the checker blocks Build on a plan without the simplicity record (2026-09-25).
2. Each non-narrow change gains one reviewer dispatch before Build, a standing cost the user accepted.
3. Keep tests within the new test budget: one pair per Acceptance line, reuse existing test helpers.
4. Known limitation: a charter value without a dot (e.g. `2`) skips the simplicity check; every plan in the repo uses X.Y.
