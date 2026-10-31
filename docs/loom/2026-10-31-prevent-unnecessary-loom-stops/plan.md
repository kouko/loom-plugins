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

**W1-06 Retarget the write-spec no-repeat mutation probe**  after: W1-02  acceptance: 4, 5
- Files: loom-design/tests/spec/test_adversarial_write_spec_no_reask_unpinned_sentences.py
- Test: A4 negative: removing the new merge qualifier makes the real write-spec contract test fail; positive: the unchanged qualifier passes. A5 boundary: the other consent and no-repeat mutation cases remain active.
- Risk: The old probe's exact string no longer exists after narrowing the question rule. Change only its mutation target and keep its RED-on-bad-prose behavior.

**W1-07 Align late write-spec choices with the shared question boundary**  after: W1-02  acceptance: 4, 5
- Files: loom-design/skills/write-spec/SKILL.md, loom-design/tests/spec/test_write_spec_contract.py
- Test: A4 positive: late evidence-based technical choice proceeds; negative: missing outcome or authorization is asked while independent work continues. A5 boundary: no committing action proceeds without authorization.
- Risk: Two reviewers found the same stale late-choice paragraph and its broad question wording. Search all changed skill prose and A4/A5 surfaces; retain the conservative option when it meets the outcome.

**W1-08 Reject a reversed three-trade-offs rule in its contract test**  after: W1-01, W1-04  acceptance: 3
- Files: loom-code/tests/test_one_way_door_question_rule.py
- Test: A3 positive: the affirmative rule passes; negative: reversing that rule to an automatic question fails the test.
- Risk: A whole-file regex crosses sentences and hides the reversal. Search all changed tests and A3 surfaces for the same false-positive class; preserve the existing consent checks.

**W1-09 Align release READMEs with the narrowed question rule**  after: W1-01  acceptance: 3, 4, 5
- Files: loom-code/README.md, loom-code/README.ja.md, loom-code/README.zh-TW.md
- Test: A3 positive: consequential choices disclose effects; negative: hard-to-reverse alone does not force a question. A5 boundary: missing authorization still asks.
- Risk: Three translated READMEs retain the former automatic-question wording. Keep their decision-point numbers and release version unchanged.

**W1-10 Keep the reversed-rule test valid across pytest import layouts**  after: W1-08  acceptance: 3
- Files: loom-code/tests/test_one_way_door_question_rule.py
- Test: A3 negative: the reversed-rule mutation is rejected both alone and in one pytest process collecting code and design tests; positive: the unmodified rule passes.
- Risk: Acceptance testing found `__import__(__name__)` resolves the wrong module when pytest gives the test a dotted name. Use the already-loaded module object without changing the mutation itself.

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

Wave 3 — integrate the newly fetched trunk release and give this guidance distinct minor versions.

**W3-01 Resolve the trunk release conflicts without losing either change**  after: W2-03  acceptance: 3
- Files: README.md, loom-code/CHANGELOG.md, loom-design/CHANGELOG.md
- Test: A3 positive: both the shared-diagram release and this guidance remain documented; boundary: the merge contains trunk content and no conflict markers.
- Risk: Trunk has already published loom-code 3.53.0 and loom-design 2.17.0. Preserve its release entries and this change's entries; W3-02 through W3-04 assign distinct versions.

**W3-02 Assign loom-code guidance version 3.54.0**  after: W3-01  acceptance: 3
- Files: loom-code/.claude-plugin/plugin.json, loom-code/.codex-plugin/plugin.json, loom-code/plugin.json, loom-code/package.json, loom-code/CHANGELOG.md, loom-code/README.md, loom-code/README.ja.md, loom-code/README.zh-TW.md
- Test: A3 positive: source and generated manifests, changelog, and plugin READMEs agree on 3.54.0.
- Risk: Keep trunk's 3.53.0 shared-diagram entry and derive manifests with scripts/sync_codex_manifests.py.

**W3-03 Assign loom-design guidance version 2.18.0**  after: W3-01  acceptance: 3
- Files: loom-design/.claude-plugin/plugin.json, loom-design/.codex-plugin/plugin.json, loom-design/plugin.json, loom-design/package.json, loom-design/CHANGELOG.md, loom-design/README.md, loom-design/README.ja.md, loom-design/README.zh-TW.md
- Test: A3 positive: source and generated manifests, changelog, and plugin READMEs agree on 2.18.0.
- Risk: Keep trunk's 2.17.0 shared-diagram entry and derive manifests with scripts/sync_codex_manifests.py.

**W3-04 Refresh shared version listing and test pins**  after: W3-02, W3-03  acceptance: 3
- Files: README.md, loom-code/tests/test_write_plan_station_text.py, loom-design/tests/spec/test_capture_intent_contract.py
- Test: A3 positive: root listing and pinned tests match 3.54.0 and 2.18.0; negative: stale pins fail.
- Risk: The root README also contains trunk's shared-diagram documentation; preserve it while changing only the two version strings.

## Simplicity check
- none found

## Questions asked
① — what — 如果這正是你的意思，請回「對」。
① — consequence — 你是否同意把這三項從「預設要問」改為「預設由 agent 查證並決定；只在你的結果偏好或授權未定時問」？

## Risks
1. The 2026-10-22 Closing Review stop is observed; other station stops are only candidate risks, so this plan changes no other hand-off wording without a failing case.
2. Three policy copies can drift; preserve the existing cross-copy test and use behavior-focused cases that distinguish technical choice from consent.
3. No new reviewer, checker rule, user decision point, or automatic external execution is introduced.
