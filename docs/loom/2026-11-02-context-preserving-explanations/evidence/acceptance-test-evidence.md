# Context-preserving intent confirmation — acceptance test evidence

Tried on 2026-11-04, in a clean copy of the project at f66da1d9434b1367b88c9cccdc3ef6f27690454d.
This independent witness did not implement source, repair tests/harnesses, run the full suite, commit, finalize an attestation, or publish.
The canonical prior documents were copied before replacement to `acceptance-test-report-pre-five-section-i4-historical.md` and `acceptance-test-evidence-pre-five-section-i4-historical.md` in this evidence directory. They remain historical, including superseded criteria and failures.

## Setup, exact source identity and execution ownership

- Read the current confirmed intent and retained plan. Current intent has four five-section Acceptance lines and no retained spec (`needs-design: no`). No instructed skips or dismissed important findings were supplied.
- Created a clean clone: `git clone --no-hardlinks --no-checkout . /tmp/loom-acceptance-f66da1d9-clean`, then `git checkout --detach f66da1d9434b1367b88c9cccdc3ef6f27690454d`. `git rev-parse HEAD` matched the full tested SHA and `git status --short` was empty.
- Followed the README local clone/validation route: `agy plugin validate ./loom-code`, `./loom-design`, `./loom-workflow` each returned [ok], with 7/6/14 skills respectively; code included four agents. These validate package loading, not installation into a user's host or automatic runtime selection. README marketplace install targets released main and changes real installed state; it was not used to replace the user's installation.
- `python3 scripts/sync_codex_manifests.py --check --all` exited 0 in the clean clone.
- `git diff --stat 60fa5cdb169dc0ac73056e5bb66e1dc08775eeef HEAD` showed only `loom-code/tests/test_write_plan_shape_text.py` (2 insertions, 1 deletion). Independently hashed all 339 candidate-manifest source entries against clean HEAD: all match `source_sha256`. The live snapshot has 337 identical files; two `hooks/hooks.json` files have documented sandbox-command wrappers. An initial assertion that all runtime hashes were identical failed on these two files; it was corrected, not hidden. The wrappers preserve the original command inside sandbox-exec; no other runtime hash mismatch was observed. Public source identity is distinct from isolation adaptations and fresh-clone validation.
- Independently ran only four focused modules in the clean clone:
  `uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-design/tests/spec/test_capture_intent_contract.py loom-design/tests/spec/test_intent_drafting_fidelity.py loom-code/tests/test_write_plan_shape_text.py loom-code/tests/test_write_plan_station_text.py -q`
  -> `152 passed in 0.25s`, exit 0. Initial restricted execution could not acquire the existing uv-cache lock; the authorized escalated run succeeded. No source was changed.
- Full-suite command (station-owned, not rerun by witness): `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`. The station reports exit 0 at `/tmp/loom-five-section-package-tests-i4-final.log`; this is handoff provenance, not my own execution. Finalization has not been skipped, but remains conditional on closing important findings. The full automated test suite runs before acceptance and blocks acceptance on failure; passing unit tests cannot resolve conversational wording defects.
- Primary reused observations: three current-source sessions under `/tmp/loom-five-section-trial-i4`, independently inspected through original prompts, summaries, candidate-manifest, graph outputs, and fixture README/draft. Retained record: `five-section-iteration-4-observed-replies.json`; blinded audit/map files distinguish iteration 4 P01/P02/P03 from historical iteration 3 P04/P05/P06. The latter are comparisons, not current passes.
- Supplemental diagnostic: `/tmp/loom-five-section-natural-interview-i4`; root ran capture-missing-date, this witness ran exactly the single preregistered `python3 /tmp/loom-five-section-natural-interview-i4/run.py code-missing-date-candidate-r1` (escalated execution for native authentication/nested strict sandbox). No retries. Prompts remove only the orchestration request to preview future confirmation; actual Chinese request/files remain identical. The pair is unmatched, not a new controlled A/B or hidden source iteration. Retained record: `five-section-iteration-4-neutral-wrapper-diagnostic.json`.
- Both supplemental results returned exactly `claude-sonnet-5-5` in modelUsage; medium explicitly requested. Code cost USD0.1173902; capture USD0.1003863; total USD0.2177765. Code exit0/is_error=false/permission_denials=[]; skill call `loom-code:write-plan`; design skill call `loom-design:capture-intent`. Code has 8 successful hook responses, capture 4; both verify session context and shared card SHA256 `9f8c6b15b25b57f3881cea15188387e3ca1cab2b79b5e6b6d99aa844c8673f0c`, unchanged plugin snapshot, no drafts and no fixture commit.
- Preflight: 14 hook checks and 3 isolation guards passed (private-sentinel read denied, network bind denied, variant write denied). No routing environment override, proxy alias, private-source copy or personal host modification was used. Existing native auth was consumed by the CLI without exposing values. Settings, tools, hooks, prompts and artifact hashes are retained in the diagnostic record. Native CLI explicit skill loading in synthetic fixtures does not establish automatic selection in installed Codex/Claude/Antigravity/OpenCode.

## 1. Grounded context, scope and confirmation consequences

How I tried it: read complete current invoice wrapper, synthetic README and actual output/draft; compare every substantive claim with supplied facts; inspect both original and neutral unknown-date replies.

What came back: the invoice starts with Cedar Accounts as an internal accounting app and the accounting team's invoice work, then the README-backed direction to preserve export format and prevent cross-customer setting leakage. It retains each customer's own currency, allows different amounts, and preserves existing export files. Missing dates stay unknown; no date, roadmap or project purpose was fabricated. The invoice draft remains open and no implementation/commit occurred.

Minor unsupported exclusivity in the new neutral code reply:
> 只有你知道這個日期是錯的，我沒有任何證據能判斷正確日期是哪天。

The second clause accurately preserves the unknown true date; the first claims only the user knows the displayed date is wrong, which the fixture never establishes. Absence of evidence available to the assistant does not show no other person knows. This is a nit grounded in actual wording, not an observed runtime failure or a new confirmation/authorization issue. “你指出目前日期有誤，但正確日期尚無依據” would avoid the unsupported exclusivity. No claim that the diagnostic is entirely fact-addition-free is made.

Boundary: no human comprehension study; current ready code-only branch and unrelated ready cases were not rerun. Confirmation consequences have the important ambiguity in row4. Result: partly.

## 2. Ready five sections and missing-fact interview

How I tried it: inspect ordered headings in invoice final output and all four unknown-date outputs (two original, two neutral); inspect code diagnostic tool/result controls.

What came back: current invoice headings are `背景與目前方向`, `目前的問題與影響`, `要改變什麼`, `範圍與驗收`, `請確認` in order. Natural equivalent headings retain the required five meanings. Unknown-date cases do not force the five-section ready layout, do not guess a date, do not write a draft, and do not request a current yes.

The original wrapper explicitly says “Only capture the intent and explain what I would be confirming.” Therefore “你之後回覆「是」時，確認的是這幾點” is a requested future preview, not itself premature confirmation. The neutral code final reply says:
> 目前無法更正，因為缺少真正的發行日期。我沒有建立計畫、沒有修改任何檔案，也沒有發布。

It waits for a reliable date/source, states other text is unchanged, and ends:
> 在那之前，這個變更維持未確認，也不排計畫。

The neutral capture reply similarly waits for a true date or evidence, with no draft or current confirmation. Both are shorter without the preview request. This supports a wrapper contribution, not a measured causal improvement/reliability claim. No paid retry was made.

Boundary: full current ready confirmation only observed through capture-intent; code-only ready behavior, known-date simple request, CSV/new-feature/default-consent branches are not established on source4 by these samples. Old source3 outputs are not carried forward as passes. Result: partly.

## 3. Proportionate, literal explanation and appropriate diagram

How I tried it: inspect actual invoice diagram and source facts, compare current and historical sampled replies without promoting historical results, inspect both alignment outputs and literal terminology.

What came back: invoice includes each outer frame, in-diagram before and expected-after titles, and explicit not-yet-verified wording. It no longer says the old unqualified “不需逐張檢查” or that all existing data is preserved. The current graph changes whose currency is used, without promising equal amounts. Unknown-date document correction has no unnecessary diagram.

The original 22-line graph alignment command exits1: lines18–21 retain trailing padding after the shorter right panel ends. The rstrip-only diagnostic exits0 (“no drift”). Both original and diagnostic artifacts remain preserved in `five-section-iteration-4-graph-verification.json`; this witness inspected the actual graph text. This is a raw verifier/whitespace discrepancy, not evidence of visibly displaced boxes. No original output was edited to manufacture a pass; font/rendering in every user host remains untested.

Plain-language assessment of current samples: the business description is literal and identifies actor/action/problem/outcome. No sustained analogy/metaphor or unnecessary invented specialized name was found. This is a bounded observation, not proof of all future outputs. The everyday words “卡住”/“卡關” do not introduce an analogy model. Exact avoidable process terms remain:
- “狀態是 `open`” and “你確認前,它不會變成 `confirmed`。” expose machine status names instead of simply saying the request awaits confirmation.
- “也不會推送分支或建立 pull request。” preserves the important publication restriction but leaves the review/upload term unexplained.
- Neutral code “例如 tag、發布公告或上線紀錄” uses an unexplained existing Git term; “可證明日期的發行紀錄” would suffice.
- Original capture “我沒有請你確認任何東西，也沒有提到發布。” mentions publication while claiming not to mention it; confusing wording, not an actual publication action.
These are existing technical/process terms, not proof that a new specialized name was coined. Current invoice repeats format/preservation boundaries across Acceptance and scope; some repetition clarifies tests versus boundaries, but the status inventory adds avoidable length.

Boundary: known-date simple ready confirmation and CSV were not freshly exercised. Result: partly.

## 4. Requirement/authorization confirmation only

How I tried it: compare full wrapper, actual invoice consent paragraph and subsequent held-publication paragraph; inspect available fixture draft/status and tool/result behavior.

What came back: no request asks the user to judge architecture, technical implementation, specification quality or reviewer conclusions. Explicit publication hold remains: “即使你回覆「是」,也不會推送分支或建立 pull request。” No actual implementation/publication was observed.

Important finding (wording ambiguity, not demonstrated unauthorized action):
> 你回覆「是」,只代表確認上面的需求範圍和驗收條件,不代表授權實作以外的任何動作。

The opening “只代表確認” limits consent, but “實作以外” can imply implementation itself is authorized. The wrapper says later yes confirms intent only. Therefore users cannot confidently tell whether yes also permits implementation, even though the ongoing publication hold is unambiguous. The independent blind semantic audit calls the same sentence material; this witness narrows it to contradictory/ambiguous wording and does not claim the model performed unauthorized work. Close by clearly stating yes confirms requirements only and does not authorize implementation or publication, then verify the actual resulting reply. Result: partly.

## Re-run on 2026-11-04, at f66da1d9434b1367b88c9cccdc3ef6f27690454d

All four current intent lines were reassessed; no old verdict was carried over. Current clean-load/focused checks were personally rerun. Three primary current-source calls and one neutral capture call were reused with explicit provenance; exactly one neutral code call was personally run. Runtime source identity was checked separately from test changes and sandbox wrappers. Two old canonical documents are historical snapshots, not current pass evidence. Report results remain partly because the material consent ambiguity is observed and coverage boundaries remain. No new attestation is claimed.
