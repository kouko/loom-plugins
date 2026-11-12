# Design research method selection — acceptance test evidence

Tried on 2026-11-12, in a clean copy of the project at 3bf869d138a8a743b20b01ddab0dbe95e7fbbd20.

Original behavioral trials ran at 029cce3a6328e86e8d66b1c6b23b2db0947f7cbb; the setup/provenance and numbered observations below retain that original execution, not a claim that the twelve cases were rerun. The dated re-run section records the clean setup recheck and per-row carryover at the current target.

## Setup and execution provenance

- Independent native acceptance witness; did not implement the change. No product/code changes or repairs made.
- Stage A loaded only `/private/tmp/design-research-trial-inputs.md` and saved baseline skill/template. Six scratch project directories were used. Raw responses, records and readbacks were retained immediately, then archived before candidate/expected checks were read. Archive SHA256: `c6983ddf01e54d4924d20cba54670a456d03155a01df9237369c721b9ce03fd6`.
- Stage B read acceptance-tester contract/report template, confirmed intent/spec/plan, expected checks, and candidate skill/template. `git clone --no-hardlinks /private/tmp/loom-design-research-method-selection /private/tmp/design-research-execution/clean-candidate` returned `Cloning ... done.`; `git rev-parse HEAD` returned original behavioral target `029cce3a6328e86e8d66b1c6b23b2db0947f7cbb`; `git status --porcelain` was empty before trial setup and after focused checks. No uncommitted implementation was copied.
- README Install section was inspected. `agy plugin validate ./loom-design` in the clean clone exited 0: `skills 7 · agents 0 · rules 0 · hooks 0 · mcpServers 0 · sidecars 0`, `Validation passed`. Advisory: missing logo means a generic icon. Direct native load of clean skill/template succeeded and was used for actual candidate runs. This verifies local load/usability and package validation; marketplace installation and existing installed copies were not changed or tested.
- `cmp loom-design/skills/design-research/templates/research.md docs/loom/2026-11-12-design-research-method-selection/evidence/baseline/templates/research.md` exited 0, confirming unchanged template.
- Focused command in clean clone: `python3 -m pytest loom-design/tests/test_design_research_package.py -q`; exit 0, `2 passed in 0.02s`. It covers portable discovery, relative bundled targets and flat template metadata, not behavior. The automated test suite, which runs before the change is accepted and blocks it on failure, remains the final mechanical check. Full-suite command reserved for finalize-review: `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`; this witness did not rerun it.
- Same native executor, separate scratch projects, sequential baseline then candidate, no API/model harness or independent model contexts per case. Baseline guidance was loaded from the saved artifact; candidate from the clean clone. Neither version was installed globally or copied into every scratch directory. The actual responses are the witness following that version's guidance, not a separately dispatched hidden agent. This is an explicitly non-blind controlled sample; no causal improvement, superiority, population validity or future reliability claim follows.
- Exact inputs and scripted turns: [behavioral-cases.md](behavioral-cases.md). Actual baseline outputs: [baseline-trials.md](baseline-trials.md). Actual candidate outputs: [candidate-trials.md](candidate-trials.md). Source accesses occurred through the web tool: baseline open returned W3C content before Stage B; candidate reused that inspected source then opened the same official page again before completion. No recruitment, participant contact, product operation, workshop, prototype check or experiment occurred.

## 1. Design Research 的研究執行限於網路研究及與當前使用者對談；不執行招募、團體訪談、工作坊、現場觀察、產品操作檢查、原型測試或實驗。

- How I tried it: C2/C3/C5 native skill execution with identical controlled inputs and permitted scripted follow-ups.
- What came back: Native execution used a neutral current-user question and an actual W3C web read; C5 refused recruitment, workshop and prototype testing despite authorization. No prohibited activity was performed. Baseline C5 proposed such future activity but did not perform it; do not confuse proposed with performed scope.
- Evidence: candidate-trials.md#c2, #c3, #c5 (links above), including actual saved-record snapshots and retained responses.
- Verdict: works for this bounded execution; no universal behavior claim.

## 2. 方法選用符合待解問題與證據缺口；既有證據足夠時，不額外啟動研究或重問已回答的問題。

- How I tried it: C1/C2/C3/C4 native skill execution with identical controlled inputs and permitted scripted follow-ups.
- What came back: C1 returned the settled Friday preference without search or repeated question. C2 asked one past-episode question, consumed the exact scripted turn and compared current copying, tags and inbox by effort and morning visibility. C3 used source comparison; C4 used a concrete train-connectivity scenario. No formal method quota or new engineering investigation was applied to C1/C2.
- Evidence: candidate-trials.md#c1 through #c4 (links above), including actual saved-record snapshots and retained responses.
- Verdict: works for this bounded execution; no universal behavior claim.

## 3. 研究結論可區分來源主張、使用者陳述與偏好、推論及未知；不把文獻、對談或方法名稱當成已完成的使用者研究或技術驗證。

- How I tried it: C2/C3/C4/C5/C6 native skill execution with identical controlled inputs and permitted scripted follow-ups.
- What came back: Records label user accounts/preferences, source claims, inference and unknowns. C3 actually inspected original W3C material and kept app conformance unknown. C4 retained package/security unknowns. C5 did not invent nurse answers or infer population adoption. C6 treated challenge as reasoning review, not a changed preference.
- Evidence: candidate-trials.md (links above), including actual saved-record snapshots and retained responses.
- Verdict: works for this bounded execution; no universal behavior claim.

## 4. 混合設計與技術問題能維持責任分界，將實作能力、相容性、可行性及安全控制實證的未解問題明確交回工程研究。

- How I tried it: C4 native skill execution with identical controlled inputs and permitted scripted follow-ups.
- What came back: Response and record separated availability/freshness tradeoffs from X 0.0.0 capability and encryption/key-leakage proof; the bounded unresolved handoff names engineering-research and specifies identity/version, conflict behavior, encryption and key lifecycle controls. No delegation or private cross-plugin reads occurred.
- Evidence: candidate-trials.md#c4 (links above), including actual saved-record snapshots and retained responses.
- Verdict: works for this bounded execution; no universal behavior claim.

## 5. 延續或修正同一問題時，保留的研究紀錄與交付結論一致，並保留改變理由及限制。

- How I tried it: C1/C2/C6 native skill execution with identical controlled inputs and permitted scripted follow-ups.
- What came back: Actual saved records were created/read back; C2 continued the same record after the exact supplied turn. C6 seed was created and read, then the matching record explicitly withdrew daily-default reasoning; created stayed 2026-11-10 and updated became 2026-11-12. After the challenge clarification the record was updated/read back again and agreed with response-2.
- Evidence: candidate-trials.md#c1, #c2, #c6 (links above), including actual saved-record snapshots and retained responses.
- Verdict: works for this bounded execution; no universal behavior claim.

## 6. 有可檢視的實際案例執行結果，能逐條判定以上研究行為是否成立。

- How I tried it: All six matched cases native skill execution with identical controlled inputs and permitted scripted follow-ups.
- What came back: Baseline outputs were authored and written/read back before loading candidate/intent/spec/expected checks, then frozen in an archive. Candidate outputs were generated natively after loading the clean package. Direct retained Markdown contains actual responses and substantive record snapshots. These are controlled fixture trials, not simulated product-user evidence or an API benchmark.
- Evidence: baseline-trials.md and candidate-trials.md (links above), including actual saved-record snapshots and retained responses.
- Verdict: works for this bounded execution; no universal behavior claim.

## Comparison and limitations

Baseline already reused sufficient evidence, asked about the missing episode, rejected the W3C conformance inference, separated technical unknowns and corrected the contradictory record. Therefore those candidate outcomes do not demonstrate newly acquired abilities. Baseline C5 proposed future workshop/prototype activity under supplied authorization, whereas candidate C5 excluded it as outside the skill; neither performed those activities. The observed scope response is the useful contrast. Small sample, identical executor, visible expected checks during candidate, sequential learning and source reuse limit inference. No statistical or general efficacy result is claimed.

No important-or-worse dismissed findings were supplied. Requested Claude Code proposal review previously failed preflight and supplied no verdict; not counted as passed or as a requirement of native acceptance. No user-instructed skipped steps were found in intent constraints or plan risks.

## Re-run on 2026-11-12, at 3bf869d138a8a743b20b01ddab0dbe95e7fbbd20

This is the same acceptance witness and review episode after the integration-only repair, not a new behavioral trial round. Previous integrated target: 71aa3cf2. Original behavioral-trial target: 029cce3a. No new requirements, altered acceptance lines or product flows were introduced; spec UI flows remain N/A.

### Actual clean setup and focused results

- Command: `git clone --no-hardlinks /private/tmp/loom-design-research-method-selection /private/tmp/design-research-execution/clean-rerun-3bf869d1`. Result: exit 0, `Cloning ... done.`.
- In that clone, `git rev-parse HEAD` returned `3bf869d138a8a743b20b01ddab0dbe95e7fbbd20`; `git status --porcelain` returned no lines before checks and after the focused timeout test.
- Re-read README Install instructions and the candidate skill/template in that clean clone. `agy plugin validate ./loom-design`: exit 0, `Validation passed`, seven skills; unchanged generic-logo advisory only. This is local load/package revalidation, not a marketplace installation claim.
- `python3 -m pytest loom-design/tests/test_design_research_package.py -q`: exit 0, `2 passed in 0.03s`.
- `python3 -m pytest loom-code/tests/test_external_review_adversarial.py::test_unreadPromptOverPipeBuffer_timesOutAtLimit -q`: exit 0, `1 passed in 6.98s`. This actually exercises the modified test double through the unchanged runner: 1 MiB prompt, 5-second preflight deadline, 6-second review deadline, review-start marker and process-cleanup/elapsed assertions.
- `git diff --stat 71aa3cf2..3bf869d1`: four files, 74 insertions and eight deletions; only plan/spec development additions, integration-repair evidence and the one test file.
- Read the full test repair via `git diff 71aa3cf2..3bf869d1 -- loom-code/tests/test_external_review_adversarial.py`: Python fake replaced by a shell fake reading one bounded prefix, returning preflight JSON or entering `exec sleep 60`. Actual runner, prompt size, distinct deadlines and assertions are unchanged.
- `git diff 029cce3a..3bf869d1 -- loom-design/skills/design-research loom-design/.claude-plugin/plugin.json loom-design/.codex-plugin/plugin.json loom-design/plugin.json loom-design/package.json` produced no output. `git diff --name-only 029cce3a..3bf869d1` listed only retained reports/evidence, plan/spec and the test repair; original research behavior, template, caller code and installed code are unchanged. This comparison covers the whole interval from actual trials, not only the latest repair.
- Original twelve controlled executions were not rerun. Their retained responses, source accesses and snapshots remain the observations; setup/focused mechanical checks above are the only newly executed checks.
- The station reports Build's locked suite passed at this target: 4264 passed, six skipped and 17 shell groups with zero failures, followed by two passing reused packaging adversarial checks. This witness did not independently rerun the full suite. Finalize-review will execute `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q` and block acceptance on failure. Package tests and finalization are not skipped.

### Per-row carryover, checked against the complete diff

- 1: carried over — acquisition-scope guidance and all trial inputs are unchanged; the test-only CLI replacement cannot enable participant, product-operation or experimental activities. C2/C3/C5 actual observations still apply.
- 2: carried over — evidence-reuse and question-led selection text, supplied episodes and callers are unchanged. No change reaches C1–C4 decision behavior.
- 3: carried over — evidence-honesty rules and actual C2–C6 records/source observations are unchanged; repair supplies no new product-user or technical evidence.
- 4: carried over — design/engineering ownership text and production runner are unchanged; replacing a test double does not alter the C4 bounded engineering handoff.
- 5: carried over — research template, metadata, continuation and readback rules are unchanged. Original same-record updates and retained readbacks remain the result.
- 6: carried over — original actual transcripts and record snapshots remain intact; added development evidence does not replace them with invented outputs. Setup was rechecked separately above.

No findings arose from these checks. No important-or-worse dismissed findings were supplied. Original sample, sequence, source-reuse and non-blind limitations remain unchanged.

