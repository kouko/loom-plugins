# Consolidate loom rule text without changing what the flow does — plan
intent: 2026-09-16-loom-rule-text-consolidation@b9bc36a0
charter: 1.0

## Current State Evidence
- Forward: `loom-code/skills/build/SKILL.md:86-98` — Build dispatches the adversary after all tasks land; `loom-code/skills/closing-review/SKILL.md:177` dispatches no adversary.
- Reverse: `docs/loom/README.md:48-161` — the sequence still has review dispatching the adversary (steps 4a, 8) and lanes; `loom-code/agents/adversary.md:59` and `loom-code/skills/closing-review/references/adversarial.md:83` link a missing `attack-catalogue.md`.
- Error: `loom-design/skills/write-spec/SKILL.md:320-326` and `loom-code/skills/write-plan/SKILL.md:356-360` hand a pre-build spec to closing-review "with scope spec", which has no spec mode and reads a plan that does not exist yet.
- Data: dec4e927 baseline — 31 `.md` files under loom-code/{skills,agents,references} and loom-design/skills, minus README/CHANGELOG: 37,665 words (`str.split`); write-plan body 4,182.
- Boundary: `loom-code/scripts/check-skill-crossrefs.py:77-79` scans only `*/SKILL.md` and `agents/*.md` `](path)` links; `loom-design/scripts/spec/test_capture_intent_contract.py:199` and `loom-design/scripts/interface/test_design_system_skill.py:71` require byte-identical station tables; `loom-code/scripts/test_expert_mode_skill.py:269-278` requires the selection paragraph once per station.

## Task DAG

### Wave 1

**W1-01 Rewrite the docs/loom README sequence to the current flow**  after: none  acceptance: 1
- Files: docs/loom/README.md, loom-code/scripts/test_readme_review_order.py
- Test: A1 positive: readme-adversary-at-build-end-no-lanes-no-review-json; negative: readme-review-dispatches-adversary-rejected.
- Risk: agent-decided — covers audit C1-C4; keeps the pinned adversary-at-Build-end unit, role-trigger heading and 三方 paragraph.

**W1-02 Remove dead adversary pointers and retired trailer wording**  after: none  acceptance: 1
- Files: loom-code/agents/adversary.md, loom-code/skills/closing-review/references/adversarial.md, loom-code/agents/implementer.md, loom-code/skills/build/SKILL.md, loom-code/scripts/test_build_mechanical_checks.py
- Test: A1 positive: no-attack-catalogue-or-task-trailer-reference; negative: catalogue-link-reintroduced-fails.
- Risk: agent-decided — C5, C10, C18; catalogue stays deleted, recipe kept as the classes already inline; Build links adversarial.md in place so 71 pinned paths do not move.

**W1-03 Align station hand-offs with enforced behaviour**  after: none  acceptance: 1
- Files: loom-design/skills/write-spec/SKILL.md, loom-code/skills/write-plan/SKILL.md, loom-design/skills/capture-intent/SKILL.md, loom-code/agents/blind-runner.md, loom-code/scripts/test_simplified_station_text.py, loom-design/scripts/spec/test_capture_intent_contract.py
- Test: A1 positive: spec-review-dispatches-reviewer-directly; negative: closing-review-scope-spec-rejected. A1 boundary: implementer-mandatory-unless-selection-skips.
- Risk: agent-decided — C6-C9, C13-C15; a required spec review dispatches loom-code:reviewer with lens spec+adversarial from the spec author, matching the only runnable path; copies stay.

**W1-04 Fix reviewer, lens, backlog, and loom-workflow stale names**  after: none  acceptance: 1
- Files: loom-code/agents/reviewer.md, loom-code/skills/closing-review/references/lenses.md, loom-code/skills/closing-review/SKILL.md, loom-workflow/skills/loom-memory/SKILL.md, loom-workflow/skills/git-memory/protocols/recall.md, loom-workflow/skills/git-memory/protocols/compose-commit.md, loom-workflow/skills/distill-sessions/agents/prompt-failure-analysis.md, loom-workflow/skills/distill-sessions/agents/prompt-success-analysis.md
- Test: A1 positive: no-retired-loom-code-skill-names; negative: ship-folds-nits-sentence-rejected.
- Risk: agent-decided — C11, C12 (blind-runner handled in W1-03), C16, C17, C19; provenance comment in fidelity-check.md is exempt and untouched.

**W1-05 Extend the cross-reference checker to references and backtick paths**  after: none  acceptance: 4
- Files: loom-code/scripts/check-skill-crossrefs.py, loom-code/scripts/test_check_skill_crossrefs.py
- Test: A4 positive: missing-link-in-references-reported; negative: existing-backtick-path-passes. A4 boundary: plugin-root-relative-path-resolves.
- Risk: agent-decided — scan widened only; backtick paths are checked when they name a skill-relative or loom-code-rooted `.md` file, to avoid flagging placeholders like `<change-id>`.

### Wave 2

**W2-01 Keep severity rules only in lenses.md**  after: W1-04  acceptance: 2
- Files: loom-code/agents/reviewer.md, loom-code/skills/closing-review/references/lenses.md, loom-code/scripts/test_reviewer_mechanical_evidence.py
- Test: A2 positive: severity-verdict-rules-once-in-lenses; negative: reviewer-md-restates-severity-table.
- Risk: agent-decided — audit D9; reviewer.md already defers to lenses.md for severity.

**W2-02 Keep the dispatch-profile invocation only in dispatch-profile.md**  after: W1-02  acceptance: 2
- Files: loom-code/skills/build/SKILL.md, loom-code/skills/closing-review/SKILL.md, loom-code/references/dispatch-profile.md, loom-code/scripts/test_dispatch_profile_contract.py
- Test: A2 positive: stations-point-to-dispatch-profile-reference; negative: station-restates-resolver-invocation.
- Risk: agent-decided — audit D4; the gate marker in dispatch-profile.md stays put.

**W2-03 Keep the selection paragraph only in expert-mode**  after: W2-02  acceptance: 2
- Files: loom-code/skills/expert-mode/SKILL.md, loom-code/skills/build/SKILL.md, loom-code/skills/closing-review/SKILL.md, loom-code/skills/ship/SKILL.md, loom-code/skills/write-plan/SKILL.md, loom-code/scripts/test_expert_mode_skill.py, loom-code/scripts/test_selection_capture.py
- Test: A2 positive: each-station-one-sentence-points-to-expert-mode; negative: station-missing-selection-show-step.
- Risk: agent-decided — audit D3; each station keeps the `selection show` call so the step list is unchanged; after W2-02 because both edit build and closing-review.

**W2-04 Keep the adversary procedure only in adversarial.md**  after: W1-02  acceptance: 2
- Files: loom-code/agents/adversary.md, loom-code/skills/closing-review/references/adversarial.md, loom-code/scripts/test_build_mechanical_checks.py
- Test: A2 positive: adversary-md-keeps-role-inputs-return-format; negative: procedure-sentence-in-both-files.
- Risk: agent-decided — audit D5; pins move to adversarial.md unweakened; the committed probes of 2026-09-15-adversary-probe-maintenance will fail on moved anchors and are recorded, not edited.

**W2-05 Drop the station table from loom-design tools and share Step 0**  after: W1-03  acceptance: 2
- Files: loom-design/skills/design-system/SKILL.md, loom-design/skills/product-principles/SKILL.md, loom-design/skills/write-spec/SKILL.md, loom-design/skills/capture-intent/SKILL.md, loom-design/skills/capture-intent/references/locate-loom-code.md, loom-design/scripts/interface/test_design_system_skill.py, loom-design/scripts/spec/test_capture_intent_contract.py
- Test: A2 positive: four-skills-link-one-locate-loom-code-reference; negative: tool-skill-carries-station-table.
- Risk: agent-decided — audit D1 (tools only) and D2; station copies in capture-intent, write-spec and write-plan stay because cross-plugin dedup is out of scope.

**W2-06 Move write-plan's loom-design-absent confirmation into a reference**  after: W2-03, W1-03  acceptance: 3
- Files: loom-code/skills/write-plan/SKILL.md, loom-code/skills/write-plan/references/confirm-intent.md, loom-design/scripts/spec/test_capture_intent_contract.py, loom-code/scripts/test_write_plan_shape_text.py
- Test: A3 positive: write-plan-body-under-3750-words; boundary: confirmed-intent-skips-reference-load.
- Risk: agent-decided — Step 3 runs only for an unconfirmed intent, so loading it on demand keeps behaviour; no gate marker sits inside Step 3.

### Wave 3

**W3-01 Measure the word reduction against the baseline**  after: W1-01, W1-02, W1-03, W1-04, W1-05, W2-01, W2-04, W2-05, W2-06  acceptance: 3
- Files: docs/loom/2026-09-16-loom-rule-text-consolidation/evidence/word-count.md
- Test: A3 positive: total-at-most-35665-words; boundary: write-plan-body-below-3750.
- Risk: agent-decided — same file set and `str.split` method as the baseline; if under 2,000 words, Build tightens restated prose inside already-touched files rather than widening scope.

**W3-02 Compare cold-read behaviour on main and the branch**  after: W3-01  acceptance: 5, 6
- Files: docs/loom/2026-09-16-loom-rule-text-consolidation/evidence/cold-read-parity.md
- Test: A5 positive: same-steps-questions-checker-results-per-station; negative: branch-reader-skips-a-step. A6 positive: package-suite-mechanisms-citations-green; negative: prose-gate-count-not-17.
- Risk: agent-decided — fresh-context readers get the installed-path-free branch and main copies and one real task each for capture-intent, write-spec, write-plan, build, closing-review and ship.

## Questions asked
① — what — 這次整理要做到哪裡？（A 修矛盾＋同外掛內去重 / B 加跨外掛 / C 加 loom-workflow 語氣）答：A 修矛盾＋同外掛內去重
① — what — 需求覆述（範圍 A）…不加新規則、不加問題；硬性禁令維持強度但附理由；被刪掉的攻擊清單不復原；跨外掛去重留到下次。對嗎？（含審查與發布檢查通過後自動 push 開 PR 的授權）答：對，授權自動發布

## Risks
1. user-decided — scope A: contradictions plus duplication within one plugin; cross-plugin copies and loom-workflow emphasis are a later change (2026-09-16).
2. The first confirmation question was sent before the restatement was visible; it was asked again with the full restatement and answered the same way.
3. Anchored probe programs under docs/loom/2026-09-*/evidence/probes/ are change-scoped and will go red where their literals move; Build records them, and graduated copies in loom-code/scripts stay in the package suite.
4. Firm prohibitions keep their force; a prose-pin test rejects negation inside a pinned sentence, so pins on reworded prohibitions use exact-once matching.
