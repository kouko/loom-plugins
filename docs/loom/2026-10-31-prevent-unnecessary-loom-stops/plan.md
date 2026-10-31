# Prevent unnecessary Loom stops with narrow station guidance — plan
intent: 2026-10-31-prevent-unnecessary-loom-stops@a78342d52248f0bfecfbfa7782324785527071cb
charter: 1.1

## Current State Evidence
- Forward: loom-code/skills/closing-review/SKILL.md §5 instructs the agent to run `finalize-review` after reviewer output is available.
- Reverse: loom-code/skills/closing-review/SKILL.md Handoff sends a PASS attestation to Ship, but §5 does not say progress reporting cannot end the turn.
- Error: loom-code/skills/closing-review/SKILL.md §4 separates technical repair from renewed external-review authorization and changed user requirements.
- Data: loom-code/skills/write-plan/references/one-way-door.md makes three trade-offs and five door classes reasons to ask; two loom-design skills repeat the rule.
- Boundary: PRINCIPLES.md non-negotiables 1 and 5 limit user questions and require consent before changing or sending existing data.

## Task DAG

Wave 1 — adjust the existing decision and hand-off guidance; keep each policy copy consistent.

**W1-01 Separate technical risk from a user-owned choice in loom-code**  after: none  acceptance: 3, 4, 5
- Files: loom-code/skills/write-plan/references/one-way-door.md, loom-code/skills/write-plan/references/confirm-intent.md, loom-code/skills/write-plan/SKILL.md, loom-code/skills/closing-review/references/lenses.md, loom-code/tests/test_one_way_door_question_rule.py
- Test: A3 positive: technical-choice-proceeds; boundary: three-trade-offs-do-not-ask. A4 positive: unresolved-outcome-asked; negative: pinned-choice-not-asked. A5 positive: consequence-disclosed; boundary: data-egress-needs-consent.
- Risk: Agent-decided: retain risk classes as consequence flags, but ask only for unresolved user outcomes or authorization; preserve PRINCIPLES.md non-negotiables 1 and 5.

**W1-02 Align the two loom-design decision points with the narrowed question rule**  after: W1-01  acceptance: 3, 4, 5
- Files: loom-design/skills/capture-intent/SKILL.md, loom-design/skills/write-spec/SKILL.md, loom-design/skills/write-spec/references/ui-flows.md, loom-design/skills/write-spec/references/spec-forms.md, loom-design/tests/spec/test_capture_intent_contract.py, loom-design/tests/spec/test_write_spec_contract.py, loom-code/tests/test_one_way_door_copies.py
- Test: A3 positive: measured-choice-is-agent-decided; boundary: hard-to-swap-alone-does-not-ask. A4 positive: unresolved-consequence-asked; negative: pinned-choice-not-asked. A5 positive: consequence-disclosed; boundary: existing-data-action-needs-consent.
- Risk: Existing tests pin the copied class titles and gates; preserve explicit consent while removing automatic option selection, including stale wording in the two write-spec references.

**W1-03 Execute the next Closing Review action after the required evidence arrives**  after: none  acceptance: 1, 2, 5
- Files: loom-code/skills/closing-review/SKILL.md, loom-code/tests/test_review_convergence_contract.py
- Test: A1 positive: two-PASS-reviewer-case-runs-finalize; negative: progress-only-end-turn-is-incomplete. A2 positive: completed-review-hands-to-ship; boundary: handoff-waits-for-attestation. A5 positive: authorized-path-continues; boundary: outside-review-retry-needs-authorization.
- Risk: A single §5 clarification should cover the observed premature stop; preserve bounded review, failed-check repair, and fresh authorization for a repeated outside review.

**W1-04 Reject negated technical-choice prose and graduate the adversarial probe**  after: W1-01, W1-03  acceptance: 3
- Files: loom-code/tests/test_one_way_door_question_rule.py, docs/loom/2026-10-31-prevent-unnecessary-loom-stops/evidence/probes/test_questionrule_negation_rejected.py, loom-code/tests/test_questionrule_negation_rejected.py
- Test: A3 positive: affirmative-evidence-based-decision-passes; negative: same-sentence-do-not-decide-fails. The committed adversarial probe is RED before the fix and GREEN after it moves unchanged into the permanent suite.
- Risk: A broad regex accepted a negated obligation. Search all changed files and A3 surfaces for the same prose-pin class; keep the fix bounded to the affected assertion and preserve the probe's original test logic during graduation.

**W1-05 Align legacy question-route probes with the narrowed rule**  after: W1-01, W1-02  acceptance: 3, 4, 5
- Files: loom-code/tests/test_adversarial_product_one_way_door_without_spec.py, loom-code/tests/test_adversarial_no_reask_pin_flipped_polarity.py, loom-code/tests/test_write_plan_shape_text.py
- Test: A4 positive: unresolved product outcome or missing authorization routes to ① without a spec; negative: answered question is not repeated at ②. A5 boundary: existing-data action still needs authorization. Keep affirmative/negated detector self-tests.
- Risk: These tests pin the old automatic one-way-door wording. Update the detector target and mutation text, retaining the missing-consent and no-repeat safeguards rather than reviving automatic technical-choice questions.

Wave 2 — release metadata after the guidance and its tests stabilize.

**W2-01 Bump loom-code minor version and release text**  after: W1-01, W1-03  acceptance: 3
- Files: loom-code/.claude-plugin/plugin.json, loom-code/.codex-plugin/plugin.json, loom-code/plugin.json, loom-code/package.json, loom-code/CHANGELOG.md, loom-code/README.md, loom-code/README.ja.md, loom-code/README.zh-TW.md
- Test: A3 positive: loom-code-release-metadata-is-synchronized; boundary: derived-manifests-match-3.53.0.
- Risk: Agent-decided: use minor bump 3.53.0 for changed station guidance; derive exported manifests through scripts/sync_codex_manifests.py, not manual edits.

**W2-02 Bump loom-design minor version and release text**  after: W1-02  acceptance: 3
- Files: loom-design/.claude-plugin/plugin.json, loom-design/.codex-plugin/plugin.json, loom-design/plugin.json, loom-design/package.json, loom-design/CHANGELOG.md, loom-design/README.md, loom-design/README.ja.md, loom-design/README.zh-TW.md
- Test: A3 positive: loom-design-release-metadata-is-synchronized; boundary: derived-manifests-match-2.17.0.
- Risk: Agent-decided: use minor bump 2.17.0 for changed station guidance; derive exported manifests through scripts/sync_codex_manifests.py, not manual edits.

**W2-03 Refresh root version listing and pinned version tests**  after: W2-01, W2-02  acceptance: 3
- Files: README.md, loom-code/tests/test_write_plan_station_text.py, loom-design/tests/spec/test_capture_intent_contract.py
- Test: A3 positive: readme-and-version-pins-match-both-manifests; negative: stale-current-version-pins-fail.
- Risk: Both plugins appear in README.md; update the shared listing only after both source manifests have their final versions.

## Simplicity check
- none found

## Questions asked
① — what — 如果這正是你的意思，請回「對」。
① — consequence — 你是否同意把這三項從「預設要問」改為「預設由 agent 查證並決定；只在你的結果偏好或授權未定時問」？

## Risks
1. The 2026-10-22 Closing Review stop is observed; other station stops are only candidate risks, so this plan changes no other hand-off wording without a failing case.
2. Three policy copies can drift; preserve the existing cross-copy test and use behavior-focused cases that distinguish technical choice from consent.
3. No new reviewer, checker rule, user decision point, or automatic external execution is introduced.
