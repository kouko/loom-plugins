# Review lens compares rule direction against the base — plan
intent: 2026-09-29-review-lens-polarity-check@3bbeec3e
spec: docs/loom/2026-09-29-review-lens-polarity-check/spec.md
charter: 1.1

## Current State Evidence
- Forward: `loom-code/skills/closing-review/references/lenses.md` "## Docs — five dimensions"; `inconsistency` covers changed-against-unchanged only.
- Reverse: `loom-code/agents/reviewer.md:52` lists docs dimensions; `loom-code/tests/test_lenses_deletion_first.py` pins each row's last token.
- Error: batch-4 compaction rows cite a lens `omission` check, but no lens tells a reviewer to diff a rule against its base version.
- Data: batch 4 hands 65 of 73 removed checks to review lenses (batch-4 census-report.md).
- Boundary: versions 3.22.3 / 2.6.2 / 5.5.3 across manifests, CHANGELOGs, READMEs and pin tests.

## Task DAG

### Wave 1

**W1-01 Lens paragraph: compare polarity sentences with the base**  after: —  acceptance: 1, 2, 3
- Files: loom-code/skills/closing-review/references/lenses.md
- Test: A1 positive: docs-section-states-base-comparison; negative: reviewer-rows-unchanged. A2 positive: cold-reviewer-flags-buried-flip; negative: pure-reword-not-flagged. A3 positive: no-rule-list-named; boundary: chinese-polarity-word-covered.
- Risk: agent-decided — per spec Design decision: sharpen `inconsistency` under the Docs table, no new dimension, no gate marker, no new test; test_lenses_deletion_first.py coverage preserved.

**W1-02 Patch release bump**  after: —  acceptance: 4
- Files: loom-*/plugin.json, loom-*/.claude-plugin/plugin.json, loom-*/.codex-plugin/plugin.json, loom-*/CHANGELOG.md, README.md and loom-*/README*.md, loom-code/tests/test_write_plan_station_text.py, loom-design/tests/spec/test_capture_intent_contract.py, loom-workflow/tests/scripts/test_release_metadata.py
- Test: A4 positive: current-release-metadata-synchronized; negative: stale-pin-fails-before-rewrite.
- Risk: agent-decided — loom-code 3.22.4, loom-design 2.6.3, loom-workflow 5.5.4; committed in Build so the attestation covers it.

## Simplicity check
- none found

## Questions asked
① — what — 覆述：LLM reviewer 在 skill 與 docs 審查時，diff 刪改帶方向字眼的句子就對照舊版逐句比對，方向反轉或刪掉即提出；通用、不靠清單；升三個 plugin 版號；含自動發布授權 → 對

## Risks
1. Acceptance 2 is probabilistic: a cold reviewer may miss a buried flip; acceptance testing runs the trial and reports the observed result, not a guarantee.
2. The paragraph lengthens every docs and skill review slightly; kept to one paragraph with no per-rule list.
