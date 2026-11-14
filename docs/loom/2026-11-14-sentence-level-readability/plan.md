# Sentence-level readability rules in the plain-language guide — plan
intent: 2026-11-14-sentence-level-readability@ef57d5d99
charter: 1.1

## Current State Evidence
- Forward: `loom-workflow/skills/loom-visualization/references/plain-language.md` "3. Say it literally" bans metaphors only; no rule names verbs, subject distance, noun stacks or dropped connectives.
- Reverse: `loom-workflow/skills/loom-visualization/SKILL.md` routing row "A plainer explanation" and the per-message card both send agents to this guide.
- Error: `plain-language.md` "7. Give only what the user needs" rewards short replies without saying which words must stay.
- Data: `loom-workflow/tests/loom-visualization/test_references.py` `guide_errors` pins rules 1-7 and exactly five rewrite steps.
- Boundary: `plain-language.md` "Scope" limits the guide to chat text for the user; `loom-workflow/skills/handoff/references/handoff-schema.md` keeps agent-read documents precise.

## Task DAG
### Wave 1 — Guide text
**W1-01 Add sentence-shape rules and rewrite pairs to the guide** acceptance: 1, 2, 3, 5, 6
- Files: loom-workflow/skills/loom-visualization/references/plain-language.md, loom-workflow/tests/loom-visualization/test_references.py
- Test: A1 positive: pattern-pairs; negative: pair-missing. A2 positive: concise-rule; negative: concise-absent. A3 positive: step-checks-shape; boundary: five-steps. A5 positive: scope-kept; boundary: agent-docs-excluded. A6 positive: source-limits; negative: limits-absent.
- Risk: agent-decided — extend rule 3, rule 7 and rewrite step 5 in place. One new `sentence_shape_errors` helper carries the new cases; existing `test_guide_has_seven_rules_and_rewrite_steps` already holds five-steps, scope-kept and agent-docs-excluded. Coverage preserved and widened.

### Wave 2 — Dogfood and release
**W2-01 Probe test: fresh agents rewrite samples with the old and new guide** after: W1-01 acceptance: 4
- Files: docs/loom/2026-11-14-sentence-level-readability/evidence/
- Test: A4 positive: fewer-patterns-after; negative: facts-changed.
- Risk: agent-decided — fixed Chinese and English samples, one fresh rewriter per guide version, a separate fresh judge blind to version; a tie or a fact change fails Acceptance 4 and blocks merge.

**W2-02 Synchronize loom-workflow release metadata** after: W1-01 acceptance: 1
- Files: loom-workflow/.claude-plugin/plugin.json, loom-workflow/CHANGELOG.md, loom-workflow/README.md, loom-workflow/README.ja.md, loom-workflow/README.zh-TW.md, README.md, loom-workflow/tests/scripts/test_release_metadata.py, derived manifests via the sync script
- Test: A1 positive: release-metadata-synchronized; negative: old-version-left-behind. Both are existing cases in `loom-workflow/tests/scripts/test_release_metadata.py`; no new test.
- Risk: agent-decided — minor bump because skill guidance changes; derived manifests come from the sync script, never hand edits.

## Simplicity check
- One test helper with one positive and one broken-text negative instead of ten prose-pin tests — taken
- Drop the release task's test pair — declined: the intake check requires an Acceptance owner and pair; the pair now names existing release-metadata cases and adds no test
- Merge the release wave into the dogfood wave; the bump does not depend on the dogfood result — taken

## Questions asked
① — what — 上面的範圍與成功條件符合你要的嗎？回「是」代表：範圍與成功條件符合；審查與檢查通過後推送分支並開 PR；實際試用驗證成功後直接合併（若想先看過再合併，現在告訴我）。
① — what — 你選 1 還是 2？（選項 1：這次只改 loom-workflow 的指引與提醒卡；選項 2：三個外掛一起改）
① — what — 範圍縮回白話指引並合併，回「是」代表：提醒卡與另外兩個外掛的成功條件移除，接著跑完整測試、獨立審查、開 PR，通過後直接合併。
build — consequence — 本機完整測試在這台機器的環境下通不過（主線同樣失敗 37 個），要略過本機完整測試、以 GitHub 上的 CI 為準嗎？選 1 的話請直接說「略過本機完整測試」。

## Risks
1. The cited study ran no human reading experiment and never tested instructions; the dogfood comparison is the only evidence the rule changes agent output.
2. Risk: one rewriter per guide version is a small sample; probe test W2-01 records every sample and the judge's counts under `docs/loom/2026-11-14-sentence-level-readability/evidence/`.
3. user-decided — 2026-11-14: merge is authorized only after the dogfood comparison succeeds; a failed comparison stops before merge and is reported.
4. agent-decided — intake complexity check: fold into existing rules, no eighth rule; the study's rare-word-combination feature is excluded as not instructable.
5. agent-decided — guide iteration stopped after round two; held-out final comparison: old guide 5 residual shapes, new guide 4, no fact changed, guessed causes 1 against 0. The margin is one occurrence.
6. user-decided — 2026-11-14 scope widened to cards and three plugins, then narrowed back. Wave 3 withdrawn before any file changed: card probe (12, 13, 14 shapes) and report probe (4 against 3, one guessed cause) showed no gain.
7. The withdrawn probes' records stay in the evidence folder as the reason for the narrowing; they prove nothing about Acceptance 1-6.
8. Local complete suite: 2806 passed, 37 failed; the same 37 loom-code runtime tests fail on untouched origin/main at 7c137958 because no local Python carries PyYAML in its base. GitHub CI is the deciding run.
skipped-by-instruction: package-tests 2026-11-14
