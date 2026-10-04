# Capture-intent complexity check — plan
intent: 2026-10-04-capture-intent-complexity-check@07fedbe6
charter: 1.1

## Current State Evidence
- Forward: `loom-design/skills/capture-intent/SKILL.md` Step 4 composes decision point ① in one message; no step weighs whether a proposed scope earns its cost.
- Reverse: `loom-design/tests/spec/test_capture_intent_contract.py` pins the station text (word cap 3500, body now 2899 words; gate markers; version 2.11.0).
- Error: simplification checks run only later — write-plan Simplicity check, closing-review deletion-first.
- Data: `loom-code/skills/ship/SKILL.md` already names `loom-workflow:git-memory` by public skill name, the form `scripts/check_plugin_boundaries.py` allows.
- Boundary: no new gate marker, checker rule, intent field, decision point or skill; loom-code and loom-workflow untouched.

## Task DAG
Wave 1 writes the guidance; wave 2 releases it.

**W1-01 Capture-intent runs a complexity check before decision point ①**  after: none  acceptance: 1, 2, 3, 4
- Files: loom-design/skills/capture-intent/SKILL.md, loom-design/tests/spec/test_capture_intent_contract.py
- Test: A1 positive: skill-names-critique-complexity-when-scope-adds-mechanism; negative: critique-not-named-outside-step-4. A2 positive: verdict-and-smaller-alternative-in-the-one-message; boundary: no-second-stop-sentence-preserved. A3 positive: no-added-cost-request-skips-check; negative: bug-fix-wording-not-a-trigger. A4 positive: absent-loom-workflow-means-unchanged-behaviour; boundary: plugin-boundary-check-exits-0.
- Risk: agent-decided — one Step 4 item: run critique first, carry only verdict and smaller alternative in plain words, never paste its response; public skill name; unmarked prose; pins widened only.

**W2-01 Release metadata for loom-design 2.12.0**  after: W1-01  acceptance: 5
- Files: loom-design/CHANGELOG.md, loom-design/plugin.json, loom-design/.claude-plugin/plugin.json, loom-design/.codex-plugin/plugin.json, loom-design/package.json, README.md, loom-design/README*.md, loom-design/tests/spec/test_capture_intent_contract.py
- Test: A5 positive: loom-design-version-test-passes-at-2.12.0; negative: version-test-fails-while-package-json-stays-2.11.0.
- Risk: agent-decided — minor bump because station guidance changes; loom-code and loom-workflow untouched.

## Simplicity check
- One Step 4 item reusing critique instead of a new skill, gate or checker rule — taken

## Questions asked
① — what — 覆述 intent（含自動發布授權） → 「對」
① — what — 是否排除 loom-design 未安裝時 write-plan 代跑的路徑 → 「對」（排除）

## Risks
1. Guidance only: whether a scope "adds cost" is the agent's judgment; nothing mechanically forces the check, so acceptance testing needs one live run that fires and one that stays quiet.
2. Each triggered run reads a critique mindset reference; untriggered requests pay nothing extra.
