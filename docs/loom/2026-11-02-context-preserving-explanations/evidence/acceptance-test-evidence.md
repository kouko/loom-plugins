# Context-preserving intent confirmation — acceptance test evidence

Tried on 2026-11-04, in a clean copy of the project at c4b639137b4d092b9d0e97400b1748f51d46dd17.

## Setup and provenance

- This independent witness implemented no source, repaired no fixtures, made no commit and ran no full package suite. Canonical prior report and evidence were copied byte-identically to acceptance-test-report-pre-correct-consistent-historical.md and acceptance-test-evidence-pre-correct-consistent-historical.md before replacement. Earlier failures and iteration counts remain unchanged.
- Independently created `/tmp/loom-correct-consistent-acceptance-clean` with `git clone --no-hardlinks --no-checkout .` then `git checkout --detach c4b639137b4d092b9d0e97400b1748f51d46dd17`; exact HEAD matched and git status was empty. Followed README local pre-install validation with `agy plugin validate ./loom-code`, `./loom-design`, `./loom-workflow`: all passed; 7/6/14 skills, code four agents. This verifies clean package setup and the explicit local-load route, not automatic installed-host selection.
- Independently hashed all339 source-manifest files against the clean clone: no mismatch. Candidate runtime has337 byte-identical files and two documented adapted hook JSON files (code/workflow). Original hook commands remain enclosed in strict sandbox wrappers; no hook removed. Preflight records14 hook checks and three successful isolation controls (synthetic private read denied, network bind denied, variant write denied). Profile SHA256: 804d2302d5c374b9197d42d7af11177d58aaaf6d842f2f669d40da59c84caeb8.
- System `python3 -m pytest` lacked pytest; no package installed globally. Independent focused rerun used `uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest -q loom-design/tests/spec/test_intent_drafting_fidelity.py loom-design/tests/spec/test_capture_intent_contract.py loom-code/tests/test_write_plan_station_text.py loom-code/tests/test_write_plan_shape_text.py`:157 passed in0.22s, exit0.
- Station-owned full locked command: `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`, exit0 in `/tmp/loom-correct-consistent-package-tests.log`. Station-owned adversarial module test_capture_intent_contract.py:38 passed, `/tmp/loom-correct-consistent-adversarial.log`. No package-tests or finalize-review skip; the automated full suite runs before acceptance and blocks acceptance on failure. No current attestation is claimed. Green structural tests do not establish conversational correctness.
- Witness personally executed only registered case6, `python3 /tmp/loom-correct-consistent-trial/run.py code-known-date-candidate-r1`, once with escalation for existing native authentication/nested sandbox. Returned exit0, is_error=false, permission_denials=[], modelUsage exactly claude-sonnet-5-5, medium requested, USD0.1569334,10 successful hooks. No retry. Root executed the other seven calls sequentially; witness inspected original prompts, assistant messages, tool actions, final replies and drafts for all8.
- All8 summaries record native claude-sonnet-5-5, requested medium, explicit expected skill, successful hook/context receipts, unchanged snapshot/seed files and no fixture commit. Shared card SHA256:9f8c6b15b25b57f3881cea15188387e3ca1cab2b79b5e6b6d99aa844c8673f0c. No inherited routing override, native authentication preserved, synthetic/public content only. Costs in schedule order:0.1161323,0.0950565,0.1277911,0.0976985,0.0916832,0.1569334,0.1742225,0.1324881; totalUSD0.9920056. Prior31 calls/USD4.2639007 retained; cumulative39/USD5.2559063.
- Durable `correct-consistent-observed-replies.json` includes exact prompts, assistant texts, tool calls, all drafts, invocation settings, summaries, cases and preflight; raw transcript paths and SHA256 retained. Original raw transcripts/hook events remain in `/tmp/loom-correct-consistent-trial/`. Opaque thinking signatures/token updates are excluded from the readable extraction, not rewritten in raw history.
- Two neutral missing-date repeats per owner are diagnostic samples, not reliability estimates; no paid baseline rerun. Known-date positive control deliberately supplies verified2026-11-04 (equal to today). No request to preview later confirmation was added to neutral date wrappers. No UI/host beyond native Claude Code or human comprehension was measured.

## 1. Grounded context, targets and consequences

All observed business explanations match supplied synthetic files/requests. Both code unknown-date repeats preserve uncertainty instead of asserting today differs from the actual release date:

> 今天（2026-11-04）可能剛好等於發行日，也可能不是。目前沒有證據能判斷，所以我不會拿它當替代值。

Repeat2 also explicitly says yes cannot supply evidence. The known-date control reads RELEASE_RECORD.md and offers the verified2026-11-04 without blanket blocking. Both invoice replies preserve existing export-file scope and reasonable differing amounts; neither adds a guarantee of identical totals, blanket existing-data preservation, or freedom from every invoice check.

Capture missing-date r1/r2 propose optional placeholder changes. R1 explicitly says:

> 這樣的「更正」只是把佔位文字換成另一個佔位文字，不是真正的日期。

These are unrequested alternative outcomes, not disguised actual dates or confirmation of the original correction without a date. They remain interviews, make no file changes, and promise a later confirmation. R1 recommends waiting; r2 recommends a placeholder. Record scope/clarity nits without falsely calling them fabricated dates.

R2's proposed TBD option says “讀者知道日期尚未公布,不會被誤導”. Unknown correct date does not establish historical non-announcement, and reader understanding is unmeasured. The proposal is conditional, but that does not ground its categorical claimed informational effect or non-misleading guarantee. After independently challenging the two fresh auditors' findings, this is an important unsupported-certainty failure. Do not overstate it as proof the reply says the version itself is unreleased: the actual defect is stronger announcement-status meaning and guaranteed reader understanding without support. Offering an accurately qualified alternative placeholder is not inherently a floor failure.

Code missing-date r1 says “沒有跑檢查” although its Bash action runs `loom-python --repair contract --require 2.1`. An unqualified reading would misreport this contract check; its paragraph is about not entering plan/implementation checks. Record ambiguity/nit, not a demonstrated material false claim that every check was skipped.

Important factual failure in two current delivered drafts:

> Readers are told the wrong date for when that version became available.
> readers are told the wrong day this version became available.

First is code-missing-date-candidate-r1; second is code-known-date-candidate-r1. Both actual input artifacts contain `Release date: to be corrected`, no calendar day. The observed defect is missing actual date, not a wrong calendar day told to readers. The user's shorthand “日期有誤” cannot override inspected artifact evidence; the accurate public replies do not repair the inaccurate saved Problem. This is a factual drafting failure even though no calendar date was invented or implementation performed. Delivered artifacts are within the user's minimum content-correctness requirement.

Default-invoice authorization disclosure remains incomplete (row4). Full Acceptance1 is partly: some grounded content works, but factual drafting and unsupported reader-effect claims fail. Sampled factual/logical minimum fails on content correctness; no separate clear current contradiction of yes-without-required-fact was demonstrated. This does not prove universal failure or its causal mechanism.

## 2. Ready structure and missing-fact boundary

Four neutral missing-date sessions (two per owner) remain interviews; no ready five headings, current yes, fake date, confirmed intent, implementation or publication. Code r1 writes an open draft explicitly blocking confirmation until evidence arrives; other three write no draft. Known-date and both invoice ready cases have five localized sections in the required semantic order (wording varies).

CSV still has five ready headings despite saying the work-displacement value fact is necessary and unresolved:

> 草稿因此還不能轉為已確認。
> 回答上面的問題,並說「是」。

This violates the phase-specific formatting requirement, and is why Acceptance2 remains partly. It does not say yes alone resolves the fact: answer+yes is conditional on supplying it. The draft leaves the question open and no confirmation follows. Do not equate premature ready formatting with demonstrated logically inconsistent acceptance or bypass. The wrapper explicitly asks to explain what would be confirmed; previewing eventual consent is not itself failure.

## 3. Proportion, diagram fidelity and plain wording

Explicit-hold invoice graph contains enclosing before/after panels, reported-problem/expected labels inside them, and prose expressly says unimplemented/expected. It faithfully depicts wrong-customer versus own-customer currency. Default invoice has equivalent labeled panels. No unverified after-state is represented as an observed implementation result.

Inspected parent-owned width-aware oracle logs `/tmp/loom-correct-consistent-trial/invoice-graph-alignment.log` and `known-date-graph-alignment.log`, both exit1: invoice title row display width64 versus block66, and known-date content/bottom width68 versus top66. Known-date is a simple text correction yet unnecessarily draws a before/after box. These are readability/layout findings below the factual/logical floor: meanings and arrows remain understandable, but Acceptance3 is not fully met. Internal draft paths, `open`, branch/commit inventory and repeated scope statements remain in multiple replies. No developed metaphor or new invented specialist label was observed; existing unexplained workflow terms remain avoidable. Necessary file identifiers for the actual correction target are distinct from internal draft bookkeeping.

## 4. Requirement consent and necessary authority

No reply asks the user to assess implementation design, spec quality or a review verdict. Explicit ongoing publication hold is preserved both publicly and in the invoice draft:

> 即使你回「是」,也不會推送分支或開 PR。

Known-date likewise says its explicit no-implementation/no-publication limit remains until separately lifted. No observed publication or implementation action occurs.

Original default invoice also says “Only capture the intent” and “Stop for my response”, besides “Do not implement now”. Although it does not explicitly impose an ongoing publication hold, conservative interpretation of the whole assigned task scope is plausible. Its reply says:

> 你說過只要捕捉意圖，所以我會維持不實作、不發布，直到你明確解除。

It omits the ordinary conditional future branch-upload/review-request consent, checks, opt-out and separate merge decision. The wrapper's stage-scope wording prevents concluding that this extra hold is a demonstrated regression on an unambiguously ordinary task. Its draft adds no ongoing publication restriction. Keep the observed original omission and ambiguity, not a retroactive pass.

### Separately registered natural-default supplement

Root registered and ran exactly one additional diagnostic, at the same source, `/tmp/loom-natural-default-control/capture-invoice-natural-default-candidate-r1`. Its prefix retains explicit skill, Traditional Chinese, synthetic-project notice and no prior confirmation; it omits only stage-scope/meta-preview/no-implementation-now phrases. Same invoice files/request. No desired-grant/five-heading hint. This is unmatched diagnostic evidence, not replacement of the original8 or proof of causal improvement. Witness independently verified its receipt and inspected prompt, final reply, tool actions and draft; durable extraction is `correct-consistent-natural-default-observed-reply.json`.

It says:

> 你的「yes」只確認以上需求範圍。
> 你回覆之前,我不會提交、推送或開 PR。

No ongoing publication hold is invented here. The ordinary later branch-upload/PR/check/opt-out/separate-merge conditions are still omitted: incomplete consequences, not a contradictory executed action or a technical-quality approval. Acceptance1/4 remain partly for this omission.

The supplement uses English5 headings despite Traditional Chinese conversation (Acceptance2 partly), retains private preface and an uneven ASCII graph (Acceptance3 partly). Both public reply and draft additionally exclude “既有匯出檔的改寫或重新產生”. The request forbids rewriting existing export files; regenerating them can mean recreating the same protected files, but may also exclude a separate-copy regeneration the request did not prohibit. Record this method/scope ambiguity as a nit without claiming a proven false runtime action. All invoice Acceptance conditions retain source targets/amount allowance; no implementation is executed.

Supplement modelUsage exactly claude-sonnet-5-5, medium requested;8 successful hooks, no denials/errors, snapshot and fixture unchanged, no fixture commit. CostUSD0.1248288; combined9/USD1.1168344; cumulative40/USD5.3807351 including retained prior31. Witness paid-call ownership remains only original case6/USD0.1569334.

## Re-run on 2026-11-04, at c4b639137b4d092b9d0e97400b1748f51d46dd17

All four Acceptance lines reassessed over original8 sessions and a separately registered unmatched ninth diagnostic; none carried as a pass from historical source. Current results: partly/partly/partly/partly. Sampled factual/logical minimum fails on content correctness, with ambiguity and small-sample limits retained; original complete acceptance remains unmet. No important finding supplied by the station was dismissed.

## Fresh independent challenge and final disposition

Inspected both station-owned blind audits `/tmp/loom-correct-consistent-trial/logic-audit.json` and `content-audit.json`. Both independently flag current blind records V03/V10 (the two current date drafts) and V05 (the current capture missing-date repeat2's announcement-status/non-misleading guarantee). V07/V11 are historical baseline failures, not new current occurrences. The blind map/source records are retained by the station. No count, reliability estimate or new causal claim is inferred from shared findings.

Witness challenged whether “wrong date” could merely restate the user's reported problem, and whether a conditional placeholder proposal could avoid the correctness floor. The exact source placeholder versus exact draft impact claim resolves the former: the draft asserts an observed effect the file does not have. Conditionality resolves neither unsupported non-announcement meaning nor guaranteed reader understanding. Both important findings are accepted; earlier provisional nit/no-clear-floor-failure assessment is superseded, not erased by replacing raw observations. Original outputs and source are unchanged. Natural9 regeneration/default-duration ambiguities and contract-check self-report remain ambiguities rather than categorical factual failures. Style/phase/consent omissions stay separate from these content blockers.
