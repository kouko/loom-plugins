# Context-preserving intent confirmation — plan
intent: 2026-11-02-context-preserving-explanations@2cfaae5e
charter: 1.1

## Current State Evidence
- Current continuation (2026-11-04): the user explicitly approved fixed five-section explanations with grounded project/function background and current direction first. This replaces optional headings, not sentence-level freedom or the missing-facts interview. W0/W1 below retain prior trial history; their superseded presentation obligations do not govern W3. W2 shipped independently in PR #130. Prior failures and counts remain retained.
- Forward: `loom-design/skills/capture-intent/SKILL.md` Step 4 requires a plain-language Problem and Acceptance restatement before confirmation.
- Reverse: `loom-code/skills/write-plan/references/confirm-intent.md` duplicates decision point 1 for code-only installations.
- Error: `loom-design/skills/capture-intent/SKILL.md` Step 4's short fill-in example does not explicitly connect unfamiliar terms, present pain and consequences.
- Data: `loom-design/skills/capture-intent/test-prompts.json` contains behavioral prompts; `loom-workflow/skills/loom-visualization/references/plain-language.md` already requires preserving facts when simplifying wording.
- Boundary: `loom-design/skills/write-spec/SKILL.md` Step 3 and `loom-code/skills/closing-review/references/acceptance-test-report.md` own other decision points, excluded here.

## Task DAG

**W0-01 Preserve context without prescribing sentences** after: none acceptance: 1,2,3,4
- Files: `loom-design/skills/capture-intent/`, `loom-code/skills/write-plan/references/confirm-intent.md`, `loom-design/tests/spec/`, `loom-code/tests/`
- Test: A1 positive: connected-background; negative: label-only. A2 positive: varied-expression; negative: mandatory-script. A3 positive: brief-familiar; boundary: unfamiliar-concepts. A4 positive: outcome-confirmation; negative: technical-approval.
- Risk: agent-decided — update both owners of decision point 1; use content checks and optional examples, preserving intent altitude, publication disclosure and the existing single confirmation stop.

**W0-02 Synchronize release metadata** after: W0-01 acceptance: 1,2,3,4
- Files: `loom-design/.claude-plugin/plugin.json`, `loom-code/.claude-plugin/plugin.json`, `loom-design/CHANGELOG.md`, `loom-code/CHANGELOG.md`, `loom-design/README.md`, `loom-code/README.md`, `loom-code/tests/test_write_plan_station_text.py`
- Test: A1 positive: synchronized-release; negative: stale-version. A2 positive: synchronized-release; negative: stale-version. A3 positive: synchronized-release; negative: stale-version. A4 positive: synchronized-release; negative: stale-version.
- Risk: agent-decided — minor bumps for changed station guidance: loom-design 2.20.0 and loom-code 3.57.0; preserve existing release checks and rewrite current-version pins where required.

**W1-01 Repair unsupported additions and excessive workflow language** after: W0-02 acceptance: 1,2,3,4
- Files: `loom-design/skills/capture-intent/`, `loom-code/skills/write-plan/references/confirm-intent.md`, `loom-design/tests/spec/test_capture_intent_contract.py`, `loom-code/tests/test_write_plan_station_text.py`, `loom-design/CHANGELOG.md`, `loom-code/CHANGELOG.md`
- Test: A1 positive: supplied-scope; negative: deterministic-addition. A2 positive: flexible-expression; negative: fixed-script. A3 positive: proportionate-context; negative: invented-date. A4 positive: concrete-authorization; negative: technical-approval.
- Risk: agent-decided — repair unsupported additions across both owners, preserving existing coverage and word caps. Replace redundant affected prose instead of adding structure. The existing unpublished minor bumps remain; independent review and host evidence need renewal.

**W1-02 Integrate current main and reconcile unpublished release numbers** after: W1-01 acceptance: 1,2,3,4
- Files: `loom-code/`, `loom-design/`, `README.md`
- Test: A1 positive: integrated-guidance; negative: lost-obligation. A2 positive: flexible-expression; negative: fixed-script. A3 positive: word-cap; boundary: merged-content. A4 positive: synchronized-release; negative: stale-pin.
- Risk: agent-decided — main 2a4c5a31 now owns code 3.57.0/design 2.20.0. Preserve its fallback repair and carried-detail prose; resolve changelogs without overwriting either change, then release this candidate as code 3.58.0/design 2.21.0.

**W1-01 continued — move fidelity to the drafting boundary** after: W1-02 acceptance: 1,2,3,4
- Files: `loom-design/skills/capture-intent/SKILL.md`, `loom-code/skills/write-plan/references/confirm-intent.md`, `loom-design/tests/spec/test_intent_drafting_fidelity.py`, `loom-code/CHANGELOG.md`, `loom-design/CHANGELOG.md`
- Test: A1 positive: supplied-strength-before-draft; negative: invented-guarantee. A2 positive: flexible-expression; negative: fixed-script. A3 positive: unknown-fact-retained; boundary: random-selection. A4 positive: outcome-only; negative: implementation-approval.
- Risk: agent-decided — live trials found D1 survives W1-01. Reconsider drafting, not another restatement reminder; move fidelity earlier, preserve uncertainty and limit whole-message bookkeeping. The failed obligation and retry/review continuity remain.

**W1-01 authorized iteration 1 — adaptable outline with contrastive examples** after: W1-02 acceptance: 1,2,3,4
- Files: `loom-design/skills/capture-intent/`, `loom-code/skills/write-plan/references/`, `loom-design/tests/spec/test_intent_drafting_fidelity.py`, `loom-code/tests/test_write_plan_station_text.py`, `loom-design/CHANGELOG.md`, `loom-code/CHANGELOG.md`
- Test: A1 positive: faithful-outline; negative: stronger-guarantee. A2 positive: adaptable-examples; negative: mandatory-headings. A3 positive: short-date-correction; boundary: detailed-repair. A4 positive: outcome-confirmation; negative: no-helper-constraint.
- Risk: agent-decided — replace accumulated reminders with an adaptable content outline and contrastive examples in portable sibling references. Preserve existing gates and authorization consequences, mirror the two copies with a parity check, and validate real outputs before claiming improvement.

**W1-01 authorized iteration 2 — separate preparation from the user message** after: W1-02 acceptance: 1,2,3,4
- Files: `loom-design/skills/capture-intent/`, `loom-code/skills/write-plan/references/`, `loom-design/tests/spec/test_intent_drafting_fidelity.py`, `loom-code/tests/test_write_plan_station_text.py`, `loom-design/CHANGELOG.md`, `loom-code/CHANGELOG.md`
- Test: A1 positive: faithful-scope; negative: new-guarantee. A2 positive: adaptable-outline; negative: copied-procedure-headings. A3 positive: brief-known-facts; boundary: missing-fact-interview. A4 positive: same-yes-consequences; negative: implementation-approval.
- Risk: agent-decided — iteration1 fixes content fidelity but still serializes bookkeeping. Separate private preparation/post-reply records from the user-message instructions; unresolved required facts stay in the existing interview. Preserve all conditional disclosures, one stop, prior coverage and the five-iteration allowance.

**W1-01 authorized iteration 3 — load examples at the producer and restore routing anchors** after: W1-02 acceptance: 1,2,3,4
- Files: `loom-code/skills/write-plan/`, `loom-design/skills/capture-intent/SKILL.md`, `loom-design/tests/spec/test_intent_drafting_fidelity.py`, `loom-code/tests/test_write_plan_station_text.py`, `loom-code/CHANGELOG.md`, `loom-design/CHANGELOG.md`
- Test: A1 positive: pre-draft-loaded-guidance; negative: stronger-outcome. A2 positive: local-direct-reference; negative: output-inventory. A3 positive: brief-known-facts; boundary: missing-fact-only. A4 positive: no-spec-consent-route; negative: lost-routing-anchor.
- Risk: agent-decided — directly load code-only examples before intake drafting and existing-intent confirmation; preserve the missing-fact phase boundary. Separately restore both owners' original policy numbering consumed by consent tests. No new rules, weakened tests, output schema or publication changes.

**W1-01 authorized iteration 4 — bound example facts and check final-message relevance** after: W1-02 acceptance: 1,2,3,4
- Files: `loom-design/skills/capture-intent/`, `loom-code/skills/write-plan/references/`, `loom-design/tests/spec/test_intent_drafting_fidelity.py`, `loom-code/tests/test_write_plan_station_text.py`, `loom-code/CHANGELOG.md`, `loom-design/CHANGELOG.md`
- Test: A1 positive: neutral-unknown-impact; negative: borrowed-example-fact. A2 positive: adaptable-wording; negative: mandatory-script. A3 positive: relevant-complete-confirmation; negative: appended-work-inventory. A4 positive: necessary-disclosure-retained; negative: extra-process-approval.
- Risk: agent-decided — iteration3 improves loading and brevity but imports example facts and retains internal inventory. Refine examples with explicit fact boundaries and an otherwise-correct verbose counterexample; invoke relevance checking at the existing composer, preserving required disclosures and free presentation.

**W1-01 authorized iteration 5 — separate primary template from optional examples** after: W1-02 acceptance: 1,2,3,4
- Files: `loom-design/skills/capture-intent/`, `loom-code/skills/write-plan/`, `loom-design/tests/spec/test_intent_drafting_fidelity.py`, `loom-code/tests/test_write_plan_station_text.py`, `loom-code/CHANGELOG.md`, `loom-design/CHANGELOG.md`
- Test: A1 positive: live-case-abstraction; negative: imported-list-or-population. A2 positive: adaptable-content-grouping; negative: required-script. A3 positive: primary-brief-output; negative: repeated-artifact-inventory. A4 positive: both-actions-after-checks; negative: early-upload-or-optout-cutoff.
- Risk: agent-decided — final authorized iteration: load a short primary content template, with examples optional and context-bound. Preserve evidence strength, scope and free expression; clarify both-action publication timing and opt-out. Keep prior failure history and all relevant test coverage.

**W2-01 Save the approved titled before/after flow illustration** after: W1-02 acceptance: 1,2,3,4
- Files: `loom-workflow/skills/loom-visualization/templates/02-linear-steps.md`, `loom-workflow/skills/loom-visualization/SKILL.md`, retained intent Constraints and this plan.
- Verification: run existing template tests; reproduce the illustration with the existing flow generator and width helper, and run `align.py` on side-by-side and stacked layouts.
- Risk: user-decided — save the specifically demonstrated outer-panel style as a shared documentation example. This newly requested reusable illustration is distinct from the exhausted confirmation-source iterations; it does not reset their counts or prove prior failures resolved. The proposed five-section confirmation redesign remains unimplemented. No production generator, confirmation-contract change, publication or release is included; earlier evidence does not verify this new example.

**W3-00 Integrate the released visualization example and current main** after: W1-02 acceptance: 1,2,3,4
- Files: current four uncommitted paths, upstream merge paths, release metadata and existing release pins.
- Test: A1 positive: preserved-intent-history. A2 positive: current-confirmed-scope. A3 positive: released-diagram-preserved. A4 negative: unrelated-feature-loss.
- Risk: agent-decided — preserve local approved work in a checkpoint before integration; merge main rather than replaying or deleting historical trials. The local visualization edits already equal the released files and must not appear as a new visualization release. Keep code/design unpublished minor releases, preserve main's patch history and workflow 5.19.2, and renew content-bound evidence after integration.

**W3-01 Implement the newly approved five-section confirmation contract** after: W3-00 acceptance: 1,2,3,4
- Files: both confirmation-template.md and confirmation-examples.md copies, capture-intent/SKILL.md, write-plan confirmation producers, affected existing contract tests and focused behavior fixtures.
- Test: A1 positive: grounded-project-context-and-current-direction; negative: invented-roadmap. A2 positive: five-localized-sections-in-order; boundary: missing-required-facts-interview. A3 positive: concise-known-correction-and-framed-process-comparison; negative: cross-section-duplication-or-unverified-after-state. A4 positive: same-yes-publication-after-checks; negative: technical-quality-choice.
- Risk: user-decided — fixed headings and source-grounded opening context are newly approved output obligations, distinct from the exhausted optional-outline task. Preserve prior evidence and counters, and do not claim they verify this contract. Remove competing optional-heading and overbroad public/private directions rather than stacking new reminders. Reuse the existing portable reference structure and optional visualization skill; do not require a cross-plugin filesystem path or new generator.

**W3-02 Exercise realistic requests and finish independent verification** after: W3-01 acceptance: 1,2,3,4
- Files: retained behavioral evidence and acceptance report; affected plugin release notes and version pins before finalization.
- Test: A1 positive: invoice-export-context. A2 positive: ordinary-new-feature; boundary: incomplete-request. A3 positive: simple-correction-and-before-after-flow; negative: repeated-scope-and-private-inventory. A4 positive: understandable-consent; negative: extra-user-quality-checkpoint.
- Risk: agent-decided — use identical, concrete requests and supplied project context for old/new samples under verified plugin hooks and explicit first-party model routing. Keep source selection and observed quality separate; run focused checks, adversarial checks, the complete locked suite and fresh independent review. No publication or merge is authorized for this continuation.

## Simplicity check
- none found

## Questions asked
1 — what — 確認這次要做到：各確認點的說明都保留理解所需的背景、名詞與結果，簡單事情仍簡短，且不增加確認次數嗎？

## Risks
1. user-decided — scope remains decision point 1. The earlier optional-heading design was superseded by the approved five-section structure on 2026-11-04; sentence wording stays free. Product behavior confirmation and final acceptance remain unchanged.
2. agent-decided — reuse existing references and tests, with no new skill, checker rule or schema field. W3 adds the explicitly approved conversation sections; no additional workflow decision point is introduced.
3. agent-decided — prose assertions cannot establish actual conversational behavior; fresh-context exercises must cover unfamiliar concepts, simple requests, and a user's detailed follow-up.
4. agent-decided — sources motivate the design, not a claim of proven effectiveness: GOV.UK check-answers, Google conversation design, NHS SBAR, Google Cloud ADR and Atlassian DACI guidance were consulted.
5. user-decided — repair dogfood findings D1–D3, fix the harness and rerun six original scenarios plus two counterexamples; publication remains held. This corrects observed failures under existing Acceptance, without changing requested outcomes or restarting review budgets.
6. agent-decided — defect class: unsupported additions during explanation, observed as deterministic-selection guarantees and an invented date fallback. Both first-confirmation owners and all cumulative changed files were searched; internal publication jargon is repaired in the same affected paragraphs.
7. agent-decided — sync-trunk detected conflicts in both plugin changelogs and left the tree untouched. Integration is a new bounded task, not a retry of completed W1-01; existing source edits remain applicable, while all pre-integration verification requires replacement.

8. agent-decided — eight-case retest had no permission denials. Both blind audits found unsupported deterministic/result guarantees in capture-6 and code-6; date/random counterexamples held. W1-01 remains incomplete; this continuation changes rule placement, preserving requirements and retry identity.

9. user-decided — explicitly override the previous local iteration ceiling: at most five additional iterations, stopping early on acceptance. Prior failures/counts remain retained; no requirement or publication authorization changes. Template-plus-examples reference structure approved.
