# Context-preserving intent confirmation — acceptance test evidence

Tried on 2026-11-04, in a clean copy of the project at fad3ca007378f9f3b2d56a32e3136b5da4819e0d.

This independent witness implemented no source, repaired no harness, ran no full suite, and produced no commit, attestation or publication. Prior canonical report/evidence were copied verbatim to acceptance-test-report-pre-six-checks-historical.md and acceptance-test-evidence-pre-six-checks-historical.md before replacement. Earlier history is unchanged. The durable six-checks-observed-replies.json retains every actual prompt, final reply, draft, invocation summary, transcript hash and experiment record.

## Setup, source identity and execution ownership

- Confirmed current four-line intent, no retained spec (needs-design: no), W3-03 approved six-question edit and one real round. No package-tests/finalize-review skip or dismissed important finding was supplied.
- Independently created exact-HEAD clean clone using `git clone --no-hardlinks --no-checkout . /tmp/loom-six-checks-acceptance-clean` and `git checkout --detach fad3ca007378f9f3b2d56a32e3136b5da4819e0d`. HEAD matched, status empty.
- Followed README's local pre-install validation route: `agy plugin validate ./loom-code`, `./loom-design`, `./loom-workflow`: all [ok], 7/6/14 skills; code four agents. `python3 scripts/sync_codex_manifests.py --check --all` exit0. No host installation replaced. This verifies clean package loading, not installed automatic selection.
- Independently hashed all339 candidate-manifest source files against exact clean HEAD: zero mismatches. Runtime frozen source b536d274b1c7a6b067194562edc910a67145e565 differs from tested HEAD only in plan notes. All339 runtime hashes matched exported snapshot.337 source/runtime hashes identical; only loom-code/hooks/hooks.json and loom-workflow/hooks/hooks.json differ. Read both actual adaptations: original commands remain inside sandbox-exec/bash wrappers; no hook is removed. Manifest lists original commands and both adapted hashes.
- Own focused command in clean clone: `uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-design/tests/spec/test_capture_intent_contract.py loom-design/tests/spec/test_intent_drafting_fidelity.py loom-code/tests/test_write_plan_shape_text.py loom-code/tests/test_write_plan_station_text.py -q` ->152 passed in0.23s, exit0. Used escalation for existing locked uv cache; no source changes.
- Station-owned full-suite command, not rerun by witness: `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`; handoff exit0 at /tmp/loom-six-checks-package-tests.log. Station-owned adversarial38 pass /tmp/loom-six-checks-adversarial.log. Automated full suite runs before acceptance and blocks acceptance on failure; finalize-review is not skipped, but no new attestation is claimed and conversational failures remain.
- Five sessions were run by root; this witness personally ran exactly the sixth registered call: `python3 /tmp/loom-six-checks-trial/run.py capture-invoice-default-candidate-r1`, once with escalation for native authentication/nested strict sandbox. No retry or extra model call. Own call exit0/is_error=false/permission_denials=[]; exact returned model claude-sonnet-5-5; medium requested; costUSD0.1434542,10 successful hook responses.
- Independently inspected all6 original prompts, final replies, generated drafts, verified summaries and snapshot hashes, then reran verify.py on all6. Each exact requested skill observed; all hooks successful with no stderr; session context and exact shared style card present (SHA2569f8c6b15b25b57f3881cea15188387e3ca1cab2b79b5e6b6d99aa844c8673f0c); snapshot unchanged; seed files unchanged; fixture has no commit. Successful hook counts: explicit invoice15, capture date6, code date12, setup8, CSV10, default invoice10.
- All6 native first-party modelUsage match claude-sonnet-5-5, medium requested. CostsUSD0.1769912/0.0984345/0.1345450/0.1593217/0.1524643/0.1434542 respectively; totalUSD0.8652109. Prior25 calls/USD3.3986898 retained; cumulative31 calls/USD4.2639007.
- Preflight retains14 hook checks and three true isolation controls: synthetic private read denied, network bind denied, variant write denied. Endpoint/model/provider overrides absent; existing native auth preserved without printing secrets. Public runtime and synthetic fixtures only. Explicit skill invocation is not automatic-trigger evidence.
- Matched pre-fix observations exist for requested graph and two neutral missing-date wrappers. Other cases expand coverage; do not claim controlled A/B superiority or reliability from one sample per case. Two neutral date prompts omit any request to preview future confirmation.

## 1. Grounded context, source boundaries and consequences

All6 replies/drafts compared with original synthetic README, other fixture files and Chinese request. Ready invoice, setup and CSV backgrounds connect actual purpose/current direction/problem/outcome without invented roadmap. Date is never guessed or written. Consent is clearer (row4).

Nit, capture date unsupported certainty:
> 今天的日期(2026-11-04)是我知道的日期,但它不等於發行日期。用它代替,只會把一個不正確的日期換成另一個。

Actual date is unknown, so today's date could coincide by chance. The supported claim is no evidence establishes it as the release date, not proof that it differs. This is claim-strength drift, not observed file corruption. Its opening “已確認” is locally about the missing-fact situation; no confirmed intent/file/action was observed.

Default invoice:
> 不必再為了幣別錯誤逐張檢查

This is explicitly an expected-after table and narrower than historical unqualified “不需逐張檢查”. The fixture supplies the prior-customer currency error and resulting checks, so reduced checks for that bug are a plausible expected benefit. It does not establish all inspections unnecessary. Still, “幣別錯誤” is wider than this particular wrong-customer defect; do not promote the sentence to proof of a blanket runtime guarantee or automatic important failure.

Separate default wording:
> 這次沒有刪除或改寫你既有資料的動作，所以沒有需要額外同意的不可逆操作。

The source protects existing export files, not every existing datum. The live session indeed made no existing-data changes, so the present-action reading is true. In a future-scope/irreversible-consent paragraph it can imply broader preservation than supplied. Record as a scope ambiguity/nit, without claiming actual deletion, implementation or unauthorized action. The draft itself keeps export-file boundaries. Result partly (date certainty demonstrated; broader implications qualified).

## 2. Five ready sections and interview boundary

Ready explicit/default invoice and setup produce five localized sections in required order and meanings. Capture missing date remains an interview with no ready layout, draft or current yes. It correctly waits for evidence.

Important observed failure: code-only missing date uses all5 ready sections and offers:
> B. 現在先確認需求，日期留待之後補
> 你回覆日期，或選 B 並說「是，這就是我要的」後，我才會繼續。

It admits actual release date unknown, writes an open draft with the same unresolved question, yet permits confirmation before that required fact arrives. This neutral wrapper does not request any future-confirmation preview. The confirmed Acceptance2 explicitly requires continued interview and no forced ready layout or early confirmation when necessary facts are missing. No actual confirmation/implementation occurs; the finding concerns the offered user path.

CSV similarly says:
> 還差兩個價值面的事實,所以現在還不能請你確認。

Yet prints the complete five ready headings including “請確認”. It ultimately asks the two questions and explicitly waits, so this is premature formatting, not proof of current confirmation/unauthorized progress. The wrapper asks what a later yes means; that conditional future preview alone is not counted as failure. The model itself treats the two facts as necessary; this assessment does not adjudicate whether the workflow should require them. Result partly.

## 3. Proportion, diagram appropriateness and literal plain language

Requested explicit invoice graph has two enclosing panels, in-diagram before/expected-after headings and explicit unimplemented/unverified wording. Inspect /tmp/loom-six-checks-trial/invoice-graph.txt and invoice-graph-alignment.log:17 rows, each display width62, verifier “no drift”. No claim every font/host renders identically.

Setup one-line documentation correction includes a full before/expected-after diagram though no graph was requested. It explains command consequences, but the confirmed Acceptance explicitly says not to force charts on text corrections without a process; this is avoidable size, not an invented implementation. Invoice/default/CSV use suitable comparisons or ordinary prose.

Private inventory persists across cases:
> 狀態是 `open`
> status: open
> 我沒有確認它,沒有建立分支或 commit,也沒有實作或發布。

Every ready reply exposes its draft path/status, often alongside repeated boundaries. Necessary consent/hold disclosures should remain; machine status/path/commit inventory is not needed to decide the requirement.

Literal wording check: business descriptions identify actors, action and result; no sustained metaphor or newly coined specialist label observed. Everyday “卡住” is not treated as a new analogy. Existing unexplained “open”, “commit”, “pull request”, “write-spec”, and date “標籤時間” remain avoidable jargon. Source filenames used to identify the actual correction target are necessary referents, unlike internal draft paths. Result partly.

## 4. Requirements and necessary authorization only

No output asks the user to judge implementation architecture, specification quality or review verdicts.

Explicit hold invoice now says:
> 你的「是」只確認上面這些需求。
> 你的「是」不會解除發佈暫停：我不會推送分支，也不會建立 pull request，也不會實作。要發佈，你之後必須另外明確授權。

This removes the earlier contradictory “實作以外” sentence. Draft retains publication hold. No publication/implementation performed.

Default invoice correctly discloses both future non-force branch upload and review-request creation only after review/publication checks, opt-out before publication, separate merge decision. Setup preserves these conditions too. CSV waits for facts and previews later visible-behavior confirmation without asking the user to assess design quality. The code-date early yes issue is row2, not technical-quality approval. Result works over sampled surfaces; not proof of later execution enforcement.

## Re-run on 2026-11-04, at fad3ca007378f9f3b2d56a32e3136b5da4819e0d

All4 current Acceptance rows independently reassessed in full over the6 supplied live surfaces. None carried over as a pass. Own exact-HEAD clean load/focused tests and sixth paid call distinguished from five reused root calls and station-owned suite. Source identity distinguishes339 source files,337 identical runtime files and2 sandbox wrapper files. Findings remain despite green152 tests. Prior report/evidence preserved verbatim as historical pre-six-checks copies, not current results.
