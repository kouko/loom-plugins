# Context-preserving intent confirmation — acceptance test evidence

Tried on 2026-11-04, in a clean copy of the project at 8c6a3f2628efc4dafadfab00f048dac7364c253f.

## Setup and provenance

- Independent witness implemented no source, repaired no fixture, made no commit and ran no full package suite. Before replacement, canonical report/evidence were copied using apply_patch into evidence/acceptance-test-report-pre-value-state-historical.md and evidence/acceptance-test-evidence-pre-value-state-historical.md; independently verified byte equality with both originals. Prior failures/counts remain retained.
- Clean clone: `git clone --no-hardlinks --no-checkout . /tmp/loom-value-state-acceptance-clean`, then `git checkout --detach 8c6a3f2628efc4dafadfab00f048dac7364c253f`. Exact HEAD matched; status empty before and after validation. README185–205 local validation: `agy plugin validate ./loom-code`, `./loom-design`, `./loom-workflow`, each exit0; 7/6/14 skills, code four agents. This tests clean setup/local load, not automatic installed-host selection.
- All339 candidate-manifest source hashes independently matched the clean clone. Runtime337 files are byte-identical; the only two adapted files are code/workflow hooks/hooks.json. Parsed both originals and adapted JSON, unwrapped commands with shlex, and asserted every original command/noncommand field equal; no hook removed. Preflight records both variants passing, 14 hook checks total, synthetic-private-read/network-bind/variant-write denials. Profile SHA256:2abaddb20849c4fcaf9009018db637980a0bdb84d7a314ac44d9670c6b977fae.
- Independent focused command: `uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest -q loom-design/tests/spec/test_intent_drafting_fidelity.py loom-design/tests/spec/test_capture_intent_contract.py loom-code/tests/test_write_plan_station_text.py loom-code/tests/test_write_plan_shape_text.py`. Initial sandbox invocation could not lock the existing uv cache; identical command with escalation passed157 tests in0.23s, exit0. No global package installed.
- Station-owned full locked command `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q` reported exit0, log /tmp/loom-value-state-package-tests.log. Station supplied38 adversarial passes in /tmp/loom-value-state-adversarial.log. Package-tests/finalize-review are not skipped; the automated full suite runs before acceptance and blocks it on failure. No current attestation claimed. Structural passes do not establish conversational correctness.
- Witness personally ran exactly registered case7 once: `python3 /tmp/loom-value-state-trial/run.py code-known-wrong-date-candidate-r1`, with escalation for existing native authentication/nested sandbox. Exit0, is_error=false, modelUsage exactly claude-sonnet-5-5, requested medium, costUSD0.1578241,12 successful hooks, zero permission denials. Snapshot/fixture unchanged, no fixture HEAD. No retry. Root ran the other eight sequentially.
- Independently checked all9 summaries, actual assistant messages, final replies, saved drafts and selected tool actions. All9: exact requested model, expected skill, successful verified context, no denials/errors, unchanged snapshot and input files, no fixture commit. Successful-hook counts in schedule order:8,10,8,6,8,14,12,13,9. Shared-card SHA256:9f8c6b15b25b57f3881cea15188387e3ca1cab2b79b5e6b6d99aa844c8673f0c.
- Costs in schedule order:0.0936074,0.1511467,0.1220019,0.0927817,0.1059412,0.1460148,0.1578241,0.1804784,0.1375136. Recomputed totalUSD1.1873098. Prior40/USD5.3807351 retained: cumulative49/USD6.5680449. Public tracked runtime and synthetic fixtures only; native Anthropic authentication, no inherited routing overrides, no private-data export.
- Durable evidence/value-state-observed-replies.json and value-state-test-context.json retain prompts, replies, drafts, source fixtures, settings, invocations, controls and raw transcript references/hashes. Original raw transcripts remain /tmp/loom-value-state-trial/*.jsonl. Root preserves blind packet/map, audits and graph checks. No old failure is overwritten or relabeled a current result.
- Fixed source: fix range c4b63913..8c6a3f26. All four original Acceptance lines re-tested in full over both owners and ready/interview branches. No verdict carried from old source. Two repeats per missing-date owner are diagnostic, not reliability estimates; no paid baseline rerun. Known-placeholder and actual-wrong-date controls are unmatched. No human understanding or non-Claude native host measured.

## 1. Grounded context, targets and consequences

Previous-source wrong-calendar Problems and announcement/nonmisleading guarantees were specifically re-tested in both chat and saved drafts. Current capture-missing-date-r1 draft accurately records the inspected non-date field and unknown actual date. Current known-placeholder-date draft says:

> The latest release notes show the release date as "to be corrected" instead of a calendar date

It does not claim a wrong calendar day was shown. Verified2026-11-04 (equal to fixture today) remains a usable correction; neither reply nor draft infers that unknown means false or that today must differ. Actual-wrong-date control correctly reports observed2026-10-31 versus verified2026-11-04 in both reply and Problem. Refusing all wrong-date wording would incorrectly fail this positive control.

Current code-missing-date-r1 overstates the reason for refusing substitutes:

> 我不能用今天的日期、「TBD」或其他暫代文字來填，因為那等於編造一個沒有依據的事實

Guessing a calendar date invents a fact. Clearly labeling missing knowledge does not necessarily invent a calendar fact; it may instead be an unrequested outcome change. TBD may suggest undetermined status, so caution is appropriate, but a blanket assertion about every temporary label is too strong. Both independent auditors flag this rationale. No substitute was actually written.

CSV public background says:

> 要用的資料目前只能在列表上看。

Seed README says only that the list has no CSV download action; request says manual list-to-spreadsheet copying. Neither excludes every other access/viewing route. List-workflow shorthand is a plausible intended reading, but the unqualified exclusivity exceeds supplied evidence. Record unsupported certainty, not proof that another route exists or a measured runtime defect. Both auditors independently flag it.

Known-wrong-date public opening only describes two files, omitting supplied shared-notes purpose and direction. Known-placeholder-date and invoice replies do connect grounded context. Thus complete Acceptance1 is partly even apart from the content floor.

## 2. Ready structure and missing-fact boundary

All four neutral missing-date cells stay interviews: no ready five headings, current yes, guessed date, confirmed intent, implementation or publication. Capture-r1 writes an open draft; the other three write none. Capture-r1 explicitly treats a placeholder alternative as a different outcome requiring changed acceptance, not evidence for the actual release date.

Current capture-missing-date-r2 instead says:

> 之後要繼續，需要其中一項：
> 實際的發行日期，或能查出該日期的紀錄；
> 你確認這個欄位在日期查明之前就維持現狀。
> 拿到其中一項後，我會用你的原話重述這項更正，包括只改顯示的發行日期、其他文字不動，再請你確認。

Agreeing to retain the unresolved field does not supply the actual date. Deferring/no-change is a coherent different outcome, but the reply fails to distinguish it and promises the same correction-confirmation path after either alternative. Both auditors independently identify this sufficiency conflict. This is a conflict in the offered next-step explanation; no bare-yes acceptance or unauthorized execution was observed.

Code-missing-date-r1 status table says a plan requires a confirmed intent, then closes:

> 意圖和計畫會在那時一起建立，並請你確認「這就是我要的」。

Literal together-create-and-confirm wording conflicts with its prior prerequisite. A compressed description of draft-then-confirm-then-plan could reconcile it, but that order is unstated. Treat as an unresolved sequence ambiguity, not proved plan creation before confirmation. Code-r2 explicitly says confirm first, resolving its future replacement wording.

Ready controls and all three invoice/CSV cells have five localized semantic sections in order. CSV nonetheless says a required work-displacement answer remains missing while presenting the ready skeleton. It requires answer AND confirmation, so it does not demonstrate that yes alone supplies the fact. Its formatting still violates the original missing-required-fact interview requirement. GO recommendation plus an open question is not inherently a contradiction. Acceptance2 remains partly.

## 3. Proportion, diagrams, plain wording and scope

Both invoice diagrams retain enclosing before/after panels and in-diagram expected labels; explicit-hold reply also expressly says the right side is unverified. CSV has now/expected labels and bounded fields/access/data constraints. Date-only controls do not force a flow diagram: placeholder control uses a small table; actual-wrong-date control uses prose. No forecast is described as a measured implemented result.

Internal open/commit/decision-point/draft-path bookkeeping and repeated scope remain in multiple replies, making simple explanations longer than necessary. The unsupported CSV exclusivity and blanket substitute rationale also breach no-added-facts. Inspected evidence/value-state-graph-verification.json and raw /tmp/loom-value-state-trial/graph-{1,2,3}-alignment.log: CSV graph1 exits1 (line8 width73 versus block74, right seam drift); explicit-hold invoice graph2 and natural-default invoice graph3 both exit0/no drift. Raw graphs are unchanged. The CSV defect is a readability issue below the factual/logical floor; passing invoice geometry does not reverse semantic findings.

Content auditor raises medium-confidence concern that invoice "不需逐張檢查幣別" and natural-default draft "可免去逐張檢查與重新匯出" could promise elimination of every inspection. Logic auditor and witness read the adjacent Problem/request as defining the particular currency-fault workaround, hence a bounded anticipated benefit. No universal release from all invoice checking is forced by that context. Retain the scope-sensitive ambiguity and recommendation to qualify isolated reuse; do not manufacture a categorical factual failure. Expected labeling alone would not rescue a genuinely overbroad promise.

Source qualifiers remain: own customer's currency, unchanged format, no rewriting old export files, differing amounts permitted. No old-file regeneration ban, same-amount guarantee, blanket existing-data guarantee or added visibility qualifier was observed. Complete Acceptance3 remains partly for unsupported claims/repetition/internal language, independently of geometry.

## 4. Requirement consent and necessary authority

No current reply asks the user to judge implementation design, spec quality or review verdict. Explicit ongoing hold publicly remains until separately lifted; intent confirmation does not silently reactivate publication. Known-date controls preserve their no-implementation/no-publication limits.

Natural-default invoice has no capture-only/no-implementation-now wrapper. Its public confirmation now explicitly describes after-review/checks nonforce push, a pending pull request, opt-out before publication and separate merge:

> 等你確認後，審查與發布檢查都通過，才會以非強制方式推送分支並開一個待審的 pull request。你可以在發布前隨時選擇不發布。合併是另一個獨立的決定。

This repairs the prior sampled disclosure omission. "是只確認需求" alongside future conditional actions can be made clearer, but disclosed later conditions do not prove immediate permission or actual publication. No action was executed. Some delivered drafts omit publicly stated ongoing holds; this is standalone-draft consent coverage weakness, not literal authorization or an observed bypass. Under the exact original Acceptance4 (requirements/necessary authority rather than technical judging), current result is works. This does not waive missing facts, grounded context or other original criteria.

## Re-run on 2026-11-04, at 8c6a3f2628efc4dafadfab00f048dac7364c253f

All four rows re-tested: partly/partly/partly/works. Sampled minimum is not met: unsupported current-state exclusivity and overbroad factual rationale remain, plus a non-equivalent missing-date alternative is offered as enabling the same correction path. The plan-order ambiguity is not escalated to an executed bypass. No single numerical pass rate or causal reliability claim is inferred. No important finding supplied by the station was dismissed.

Two fresh blind audits independently read the actual requests, fixtures, replies and drafts without source/variant mapping or each other's findings. Durable copies are evidence/value-state-logic-audit.json and evidence/value-state-content-audit.json; mapping is evidence/value-state-blind-map.json. Current issues appear as blind Z04/Z06/Z07; old wrong-date/TBD-status failures appear as Z01/Z09/Z11. Mapping was inspected only after independent per-record grading. Those historical failures are controls, not new current occurrences. The witness challenged the broader invoice-benefit reading and retained its context-dependent uncertainty rather than forcing agreement. Correct old-error controls do not establish a floor pass in the presence of current counterexamples.

Both blind auditors correctly mark case7's operational no-warning claim unverified from their restricted packet, which omitted tool results. The full raw transcript supplies the standing-check Bash result with empty stdout; root verified this scoped no-warning claim. It is not a statement that all project/package checks passed. No current source repair, paid retry, finalization or attestation follows this failed floor; W3-03's initial attempt plus two ordinary continuations and all older history remain consumed and retained.
