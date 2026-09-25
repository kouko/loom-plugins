# Keep the tests a change adds small, and make over-built tests a review finding — plan
intent: 2026-09-25-keep-mechanical-tests-small@51c7baf4
charter: 1.0

## Current State Evidence
- Forward: `loom-code/agents/implementer.md:33-36` rule 2 demands a failing test first but sets no budget on how many or how large.
- Reverse: `loom-code/skills/closing-review/references/lenses.md:54` tests dimension checks that tests run and exercise behaviour, never that they are over-built.
- Error: `loom-code/skills/closing-review/references/adversarial.md:73-82` asks probes to reuse before writing new ones, but not to stay small or reuse helpers.
- Data: the only budget today is the 5-program adversarial cap recomputed by `adversarial.proportionate`; ordinary tests have none.
- Boundary: `lenses.md:61` deletion-first already covers implementation abstractions; this change adds the test side only.

## Task DAG

### Wave 0 — the budget

**W0-01 Test budget in implementer, adversary protocol and the tests dimension**  after: —  acceptance: 1, 2, 3, 4
- Files: `loom-code/agents/implementer.md`, `loom-code/skills/closing-review/references/adversarial.md`, `loom-code/skills/closing-review/references/lenses.md`, `loom-code/tests/test_test_budget_text.py`
- Test: A1 positive: implementer-states-budget-and-net-lines; negative: budget-not-a-number-threshold. A2 positive: adversarial-probe-small-reuses-helpers; negative: five-program-cap-unchanged. A3 positive: tests-dimension-overbuilt-is-finding; negative: fix-adds-at-most-one-test. A4 positive: rule-count-unchanged; negative: no-new-gate-marker.
- Risk: adversary reads adversarial.md as its protocol, so the probe sentence lives there, not in agents/adversary.md; one pin test file; agent-decided.

### Wave 1 — release

**W1-01 loom-code minor release 3.17.0**  after: W0-01  acceptance: 4
- Files: `loom-code/plugin.json`, `loom-code/.claude-plugin/plugin.json`, `loom-code/.codex-plugin/plugin.json`, `loom-code/CHANGELOG.md`, `loom-code/README.md`, `loom-code/README.ja.md`, `loom-code/README.zh-TW.md`, `README.md`
- Test: A4 positive: versions-synchronized-3.17.0; negative: check-mechanisms-net-unchanged.
- Risk: minor because agent and lens guidance changes; release pin in `loom-code/tests/test_write_plan_station_text.py` updated too; agent-decided.

### Wave 2 — adversary fixes

**W2-01 Budget wording agrees and covers added tests only; pins reject negation**  after: W1-01  acceptance: 1, 3
- Files: `loom-code/agents/implementer.md`, `loom-code/skills/closing-review/references/lenses.md`, `loom-code/tests/test_test_budget_text.py`
- Test: A1 positive: implementer-budget-sentence-not-negated; negative: negated-budget-sentence-fails-pin. A3 positive: overbuilt-clause-limited-to-added-tests; negative: negated-finding-sentence-fails-pin.
- Risk: classes "budget wording inconsistent or over-broad" and "pins miss a polarity flip" searched in the three prose files and the pin test; extends two existing tests, none added; agent-decided.

## Questions asked
① — done — 對

## Risks
1. The budget is prose read by agents plus a reviewer finding; there is no mechanical count, by the intent's constraint.
2. Keep this change's own tests small: one pin test file, one assertion per Acceptance case.
