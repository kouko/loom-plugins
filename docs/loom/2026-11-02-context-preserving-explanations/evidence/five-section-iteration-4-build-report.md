# W3-01 continuation 3 author report

Baseline: `ddc7e46822791e4c44277c439e78870413ab4a58`. This is the same task, with the initial execution and two completed continuations retained. The user's additional iteration authorization is recorded by the orchestrator in the plan. No commit, paid CLI call, full suite, agent dispatch, publication or merge was performed by this implementer.

The orchestrator subsequently committed this source as `60fa5cdb169dc0ac73056e5bb66e1dc08775eeef` and started the separately owned checks and source-4 trials. No further functional source edit was made by this implementer after that snapshot.

## Diagnosis from actual consumption

- `/tmp/loom-five-section-trial-i3/capture-missing-date-candidate-r1.jsonl`: events/lines 17 and 19 Read interview and grounding; line 21 Read the ready format despite the unavailable required date. The actual reply then serializes an artifact table and future confirmation/publication steps. It also puts `查證或推測真正的日期` outside scope, conflating legitimate verification with guessing.
- `capture-invoice-explicit-hold-graph-candidate-r1.jsonl`: line 18 Bash cats interview, grounding and ready format together. Line 37 invokes `loom-workflow:loom-visualization`; there is no subsequent Read or Bash consumption of `templates/02-linear-steps.md`. The invocation returns the skill's instructions, not its selected template. The emitted comparison lacks titled outer frames. Its `不需逐張檢查` also drops the currency-specific reason, and `不改寫、不刪除任何既有資料` expands the named existing-export-file preservation boundary.
- Invoice default and ordinary invoice runs also consume grounding/format via Bash cat (line 18), not Read. CSV consumes ready format before grounding (lines 17, 19). Code missing-date reads grounding and the no-intent interview (29, 31); code setup reads those plus ready format (21, 22, 36). None of the seven traces contains a Read or Bash load of the optional example gallery. Absence of a Read event alone was never treated as proof of non-consumption.
- Competing directions are visible in the sources: the public main write-plan entry advertises the ready-format filename while intake remains open; owners repeat a content outline, private consequence/question inventories, intent-file diagram rules and the ready layout. The visualization skill provides a generic table default and requires a subsequent selected-template read; invoking it alone never supplies the titled-panel reproduction example. The explicit user request for ASCII makes the flow form applicable; no workflow default needs changing.
- These are observed reading/output facts. It is an implementation hypothesis that placing phase examples in the already required readers and making preparation inputs subordinate to the one ready layout will improve the next replies. This report does not claim that source reading alone proves behavior, or that earlier wording establishes an actual runtime/publication action.

## Minimal design and rejected alternative

Reorganize existing examples rather than adding another optional warning:

1. Move the unavailable-date Good/Bad case from the optional gallery into the mandatory grounding/interview reader, with a distinct Grounded drafting section. Make explicit that absent supplied records do not ban verification. State literal who/does what/user sees/changes, with no analogy and no unnecessary new terminology, in the same mandatory reader.
2. Move the invoice and filtered-CSV Good/Bad cases into the mandatory ready-format reader. Keep the other illustrative cases optional; all facts remain explicitly case-specific. Extend the invoice negative example to catch the unqualified promise of removing all inspection.
3. At the two intake owners, stop the missing-required-fact branch before confirmation preparation. Remove the redundant ready-format advertisement from the main code-only route, leaving that link solely at its confirmation composer. Clarify that intent-file diagrams belong to the artifact, and private preparation supplies inputs rather than a competing reply outline.
4. Make the ready-format diagram step name the already released `templates/02-linear-steps.md` and its existing reproduction procedure after invoking the optional skill. No cross-plugin filesystem link, new renderer, checker, schema, glossary, or workflow-source edit is introduced.

Rejected: make the entire large optional gallery mandatory before every intake reply, or append more reminders to owners. That would load completed five-section/publication examples during unavailable-fact interviews, increase reading, and preserve the very phase competition observed. Moving the three relevant cases to their phase readers changes consumption rather than merely restating existing prohibitions. The evaluator-pinned owner content obligations remain in place.

## Plain-language evaluation of actual iteration-3 replies

The core descriptions generally do say concretely who does what. For example, `會計同事現在必須逐張檢查發票，遇到錯誤再重新匯出` and `每位客戶都有自己的幣別設定` name the actor and the work. No metaphor/analogy was identified in the seven actual replies; that is a bounded inspection finding, not a general reliability claim.

The avoidable terminology is mostly leaked internal vocabulary rather than newly coined application names:

- `status: open`/`open` adds a machine field to ready openings; the ordinary fact, when needed, is simply that the user has not confirmed the request.
- The default invoice's `工程修正 (engineering)` explains private classification rather than what the user receives.
- The setup reply's `agent-decided`, `spec`, and `背景文件檢查 (standing)` are unnecessary for deciding whether one command line should change. There is no need for a new label or glossary; omit the internal inventory.
- CSV is the user's requested file format. The exact `orbit launch`/`orbit start` command strings are essential to the requested correction. Pull request/PR is an established publication action whose role must be explained when publication consent applies; these are not automatically invented-term violations.
- The explicit-hold reply's no-publication explanation is understandable and retains the hold. Its broad data-preservation and inspection claims are semantic fidelity defects even though their words are simple. Plain wording must preserve the exact source target/reason, not turn an unsupported assertion into an easier sentence.

The existing visualization plain-language reference already says to be literal, avoid metaphors, explain names by what they do, remove process detail, and avoid temporary coined names. It also gives an unheaded conclusion-first rewrite procedure only for a request to rewrite the last reply more plainly. That conditional rewrite procedure does not replace the confirmed five headings here. No released shared reference was changed.

## Changed files

- `loom-design/skills/capture-intent/SKILL.md`
- `loom-code/skills/write-plan/SKILL.md`
- `loom-code/skills/write-plan/references/confirm-intent.md`
- Both plugin-local `references/confirmation-template.md` copies
- Both plugin-local `references/confirmation-format.md` copies
- Both plugin-local `references/confirmation-examples.md` copies
- `loom-design/tests/spec/test_intent_drafting_fidelity.py`
- Existing unreleased entries in `loom-code/CHANGELOG.md` and `loom-design/CHANGELOG.md`

The orchestrator's concurrent plan edit is preserved and was not authored here. Versions remain code 3.58.0/design 2.21.0. Historical raw evidence, old attestations, the evaluator-owned `loom-design/tests/spec/test_capture_intent_contract.py`, and released workflow files are unchanged.

## Test-first and verification evidence

- RED: `/tmp/loom-five-section-i4-red.log`: three failing tests for required phase examples, stop-before-preparation routing, and literal/no-new-terminology guidance. These fail on the baseline's absent routing/content.
- GREEN: `/tmp/loom-five-section-i4-green.log`: `python3 -m pytest -q loom-design/tests/spec/test_intent_drafting_fidelity.py loom-design/tests/spec/test_capture_intent_contract.py loom-code/tests/test_write_plan_station_text.py` — **128 passed**.
- Existing gallery tests were relocated to read the same cases in their new phase readers, preserving Good/Bad checks, unavailable-fact protection, default/held consent, heading order, portability and byte parity. The new routing test checks file consumption/phase placement rather than creating an output evaluator or mirroring every sentence.
- All three paired references are byte-identical. Capture-intent's body is **3500 words**, satisfying the unchanged strict maximum. Existing numerical consent-policy anchors 2..6 remain untouched and their focused contract checks pass.
- The moved existing invoice diagram is `/tmp/loom-five-section-i4-example-graph.txt`; `/tmp/loom-five-section-i4-example-graph-check.log` reports **no drift**, every line **66 cells**, below 72. It is not new live-host output evidence.
- `git diff --check` passes. Diff checks show no modification to evaluator-owned contract tests or the released visualization owner/template.
- One combined shell heredoc was blocked by the local command guard's parser. No allowlist or permission bypass was used; the actual edit was put in a reviewable Python file through apply_patch and executed directly. The blocked command was not repeated. A first supplementary search hit an untracked binary; the bounded scan was corrected to tracked acceptance surfaces, without modifying those files.

## Whole-class search

Defect class: **reference-loading gaps and competing composition guidance; unsupported scope/exclusion claims**, including avoidable private terminology. `/tmp/loom-five-section-i4-author-class-scan.json` reads whole contents of **102 files**, containing all **88** original changed paths plus tracked files under both affected skill trees and visualization owner/plain-language/titled-flow sources. The original input `/tmp/loom-five-section-i4-class-scan.json` is unchanged. Matches include historical evidence, which is observation to retain rather than a runtime target.

All affected runtime match groups were inspected:

- Both owners, no-intent and main code routing: distinguish interview, private preparation and ready composer; direct premature-ready advertisement removed, unavailable-fact stop made early.
- Both grounding/format/gallery sets: case-specific preservation/absence/exclusion examples are now consumed in the applicable phase; optional gallery still covers shorthand/interface/determinism cases without making its facts defaults.
- Intent field templates/interview: existing source-abstraction constraints and explicitly excluded capability/data language remain valid; no additional inferred internal method ban was introduced. Other interview/standing/reviewer/one-way-door references retain their existing conditional disclosures and consent policies.
- Visualization owner/template: existing selected-template read and titled-frame reproduction already implement the requested diagram; the consumer now names the required read. Plain-language source supports literal explanations; its conditional rewrite and general table guidance do not override this ready confirmation's fixed sections or explicit ASCII request.
- Existing tests, release notes and historical development/evidence records: current focused checks were updated only for moved reader locations; historical failures, counts and attestations remain unchanged. No further runtime instance requiring a new source surface was found within this bounded scan.

No live-host behavior or overall acceptance pass is claimed. The orchestrator owns the three planned source-4 exercises and independent evaluation. No hidden additional source iteration is authorized by these static checks.

## Integration addendum — stale moved-rule pin

The orchestrator's complete suite on `60fa5cdb` found one failure in `loom-code/tests/test_write_plan_shape_text.py::test_intakeReferences_holdMovedRules_bodyDoesNot`. I read that test, its originating `dc1c3f3e` (#120) change, and the original change's commit contract. The test was introduced to prove that conditional intake rules still reside in their references and do not drift back into the main body after the extraction. Its sampled sentence was `Any intent section may use a Markdown table or a Mermaid flowchart`; the source clarification to `Any intent-file section...` preserved that artifact capability while separating it from user-facing chat. The old spelling was not a permanent behavioral obligation.

The legitimate smallest integration fix changes only the expected sampled sentence to the current exact artifact wording and adds the existing exact chat restriction to the same list: `and chat shows text tables or text diagrams, not Mermaid.` Both remain subject to the existing reference-present/main-body-absent assertions. No test is deleted, no containment check is relaxed, and the additional pin explicitly protects the intent-file versus chat distinction. Runtime wording is not reverted to appease an obsolete spelling.

- Integration RED: `/tmp/loom-five-section-i4-integration-red.log` — the single stale-pin test fails before this edit.
- Integration GREEN: `/tmp/loom-five-section-i4-integration-green.log` — `python3 -m pytest -q loom-code/tests/test_write_plan_shape_text.py loom-design/tests/spec/test_intent_drafting_fidelity.py loom-design/tests/spec/test_capture_intent_contract.py loom-code/tests/test_write_plan_station_text.py` — **152 passed**.
- `git diff --check` passes. The only repository edit in this addendum is two additions/one deletion in the existing shape test. `git diff --exit-code 60fa5cdb -- loom-design/skills/capture-intent loom-code/skills/write-plan` is clean: the exported public runtime remains byte-identical to source-4's snapshot.
- This completes integration of the same user-authorized continuation 3; it is not another behavioral source iteration, and it changes neither earlier attempts nor their counts. No commit, full suite, paid call, agent dispatch or additional runtime edit was performed by this implementer.
