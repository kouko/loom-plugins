# Design research method selection — acceptance test evidence

Tried on 2026-11-12, in a clean copy of the project at 79789ae2230d8d0e8f163509c5275f119a5938f4.

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

## Supplemental restoration witness on 2026-11-12, at 79789ae2230d8d0e8f163509c5275f119a5938f4

This new independent witness (`method_restoration_acceptance`) tested only the added W5 exact-restoration obligation and clean setup. The original witness was `method_acceptance`; its twelve actual baseline/candidate executions at 029cce3a and later setup receipt at 3bf869d1 remain attributed to it. This supplement neither reran nor renamed that completed design-trial task, and resets no task or review continuity. Intent, spec, plan, report, earlier evidence, withdrawal record and retained trial outputs were inspected before deciding carryover.

### Newly executed commands and results

- `git clone --no-hardlinks /private/tmp/loom-design-research-method-selection /private/tmp/method-restoration-acceptance-79789ae2`: exit 0. `git rev-parse HEAD` returned `79789ae2230d8d0e8f163509c5275f119a5938f4`; `git status --porcelain` was empty before and after checks.
- Read root README local installation/validation instructions and loom-design README Install section; loaded the clean candidate skill and research template for inspection. `agy plugin validate ./loom-design`: exit 0, seven skills, `Validation passed`; generic-logo advisory only. Local package validation is established; no global install or remote-marketplace claim is made.
- `python3 -m pytest loom-design/tests/test_design_research_package.py -q`: exit 0, `2 passed in 0.02s`.
- Complete-file byte oracle used `pathlib.Path(path).read_bytes() == subprocess.check_output(["git", "show", "391fd01723efedfada3447673b1b99c3894af859:" + path])` and asserted equality for both files. Both returned `exact_bytes=True`. SHA256: `test_external_review.py` = `82a62069791fd92d002c9b426ef82c1fdafecfeaecb9fea8c51ad11e3909a937`; `test_external_review_adversarial.py` = `da875e872dd67a53312f06fa99bea1e9ef52a77eadfdcfcfc63daa1da6518c25`.
- `git diff --exit-code 391fd01723efedfada3447673b1b99c3894af859 -- loom-code/tests/test_external_review.py loom-code/tests/test_external_review_adversarial.py`: exit 0, empty output. All original assertions, coverage and deadlines are preserved by complete-byte equality, rather than inferred from selected passing tests.
- `python3 -m pytest -q loom-code/tests/test_external_review.py loom-code/tests/test_external_review_adversarial.py -k 'keeps_stdin_open or never_answers or holds_stdout or lingering_descendant or exit_before_answer or unreadPromptOverPipeBuffer'`: exit 0, `10 passed, 134 deselected in 47.86s`. This covers model-list stdin/EOF, no answer, exited parent/lingering descendant, review-stage descendant timeout, exit-before-answer and unread pipe-buffer prompt behavior using restored fixtures. No test code was edited.
- `git diff --exit-code 029cce3a..HEAD -- loom-design/skills/design-research loom-design/.claude-plugin/plugin.json loom-design/.codex-plugin/plugin.json loom-design/plugin.json loom-design/package.json`: exit 0, empty output. Production external-review resources likewise have no changes over the original-trial interval. `git diff --name-only 391fd017..HEAD` confirms final non-development changes are design-research guidance, design release metadata/README strings and its version-pin test; neither incidental test file remains changed.
- `git diff --exit-code 3bf869d1..HEAD -- docs/loom/2026-11-12-design-research-method-selection/evidence/baseline-trials.md docs/loom/2026-11-12-design-research-method-selection/evidence/candidate-trials.md docs/loom/2026-11-12-design-research-method-selection/evidence/behavioral-cases.md`: exit 0, empty output. These retained outputs were added after their original execution target; their absence from the original commit is not an output change. The immediately prior canonical evidence already contains them and they remain unchanged.

### Per-row carryover checked against the complete interval

- 1: carried over — research acquisition text and C2/C3/C5 inputs/outputs remain unchanged; withdrawing incidental test rewrites cannot change permitted research activities.
- 2: carried over — reuse/selection guidance, callers and C1–C4 observations are unchanged; original decisions remain the witnessed result.
- 3: carried over — evidence-category rules, inspected-source account and C2–C6 retained records are unchanged; restoration provides no new participant or technical proof.
- 4: carried over — design/engineering boundary, production runner and C4 handoff are unchanged; restored test fixtures cannot alter the handoff.
- 5: carried over — template, continuation/readback contract and C1/C2/C6 record snapshots are unchanged; original same-record readbacks remain attributed to their executor.
- 6: carried over — six matched baseline/candidate outputs and their snapshots remain inspectable and byte-unchanged from prior canonical evidence. Only new mechanical restoration/setup results above were executed by this supplemental witness.

Supplemental outcome: exact withdrawal/restoration works; clean local package validation and focused protocol checks work. No findings or dismissed important findings were supplied. Native fixture rewrites are withdrawn, not a shipped reliability fix. Original preflight timing uncertainty remains unresolved; this passing focused run does not guarantee stability. The station reports the locked full suite at this target passed (4264 passed, six skipped, 17 shell groups, zero failures), followed by two reused adversarial packaging checks; this is supplied provenance, not a full-suite execution by this witness. Package tests are not skipped. Finalize-review will run `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q` and block acceptance on failure. The failed prior Claude proposal review still supplied no verdict and is not counted as passed.

## Re-run on 2026-11-13, at ed20a0452e5b2d22b89168686eb07de8bee9f7b1

Independent witness: simplification_acceptance; not a runtime author. This is the new bounded review episode for added Acceptance 7 and expanded Acceptance 6, confirmed at intent commit 6869846f. Original baseline/candidate executions retain their original executor, date, commit and non-blind limitations; none is presented as newly executed here. The confirmed intent now has seven lines; UI flows remain N/A. No important-or-worse dismissed findings were supplied. Resolver inherited count is zero and no repair was attempted.

### Clean setup, actual commands and limits

- `git clone --no-hardlinks /private/tmp/loom-design-research-method-selection /private/tmp/loom-simplification-acceptance-ed20`: exit 0, `Cloning ... done.`. Clean HEAD was `ed20a0452e5b2d22b89168686eb07de8bee9f7b1`. `git status --porcelain` after focused checks returned no lines. Scratch records were created outside that clone.
- Read clean root AGENTS/README, both plugin README Install sections, actual candidate skills/templates and relevant engineering references. Native load/use succeeded in the five actual trials below; no global plugin install or marketplace installation was tested. README-local `agy plugin validate ./loom-code` and `agy plugin validate ./loom-design` both exited 0. Code reported eight skills/four agents and `Validation passed with 2 warnings`; design reported seven skills and `Validation passed`. Generic-logo advisory was also printed. Existing code validator warnings: `hooks/hooks.json: never loaded: plugin hooks are read only from hooks.json at the plugin root`; `skills/closing-review/SKILL.md: the body is 29757 bytes; only the first 24000 are loaded`. These package-validator messages do not prove host hook delivery or full closing-review loading. Those unrelated installed-host surfaces were not repaired or certified by these research trials. No external coding-agent CLI or model/API harness was used; agy was used only for README package validation.
- Initial focused-test invocation guessed nonexistent `loom-code/tests/test_engineering_research_package.py`; pytest exited 4 (`file or directory not found`, no tests ran). After locating the actual module with `rg --files`, the actual successful command was `python3 -m pytest -q loom-design/tests/test_design_research_package.py loom-code/tests/engineering-research/test_package.py loom-code/tests/test_write_plan_station_text.py::test_current_release_metadata_is_synchronized`: exit 0, `8 passed in 0.06s`. This verifies research packaging/metadata and release synchronization, not semantic behavior. Initial guessed `templates/research-record.md` paths were also absent; both actual linked `templates/research.md` files were read before executing.
- `git diff --exit-code 79789ae2..HEAD -- loom-design/skills/design-research/templates/research.md loom-code/skills/engineering-research/templates/research.md docs/loom/2026-11-12-design-research-method-selection/evidence/candidate-trials.md docs/loom/2026-11-12-design-research-method-selection/evidence/baseline-trials.md docs/loom/2026-11-12-design-research-method-selection/evidence/behavioral-cases.md`: exit 0, no output. Earlier template, fixture, actual response and readback bytes are preserved. Read the full skill diffs over this interval: only the active-simplification/comparison paragraphs changed; acquisition scope, source distinction, boundary ownership and same-question continuation sections stayed unchanged. The preceding provenance chain already checks the original-trial-to-79789ae2 interval. Thus earlier executions are retained only for these unchanged surfaces, not for the new simplification requirement.
- Five new native self-executions used exact D1/D2, E1/E2 and C1 fixture inputs in separate scratch directories. The witness read guidance/inputs, wrote actual records with apply_patch, returned the full substantive records through `cat`, inspected question/conditions/evidence/findings/decision/limits, then wrote the retained responses. Full exact inputs, actual responses, original scratch paths and complete actual record snapshots: [simplification-acceptance-trials.md](simplification-acceptance-trials.md). No keywords-as-behavior checks were substituted. No further questions, external source access or runtime experiments occurred. Supplied existing system correctness/control facts remain fixture facts; no production behavior was invented. The witness saw observable criteria: controlled and non-blind, not independently blinded cases.
- The station supplied Build's exact locked-suite command: `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`; actual log `/private/tmp/loom-simplification-build-suite.log`, supplied result 4264 passed, six skipped, 17 shell groups/zero failures at ed20a045. Supplied reused adversarial command: `python3 -m pytest loom-design/tests/test_design_research_package.py`, two passed. These are station-provided Build results, not independent full-suite execution by this witness. Package tests are not skipped. Finalize-review will run the full suite and blocks acceptance on failure; this report does not claim a pending finalization result. Original unchanged external-review timeout intermittence remains unresolved; no fixture repair/retry was performed.

### 1. Design Research 的研究執行限於網路研究及與當前使用者對談；不執行招募、團體訪談、工作坊、現場觀察、產品操作檢查、原型測試或實驗。

- Newly tried: D1/D2 and C1 use only supplied context; D2 refuses to transform missing package proof into product operation/prototype/experiment. No excluded action occurred.
- Unchanged-surface carryover: original C2/C3/C5 cover actual current-user dialogue, W3C source access and rejection of authorized recruitment/workshop/prototype testing. Exact inputs, source access and outputs in candidate-trials.md remain unchanged; acquisition rules and callers are unchanged across the complete provenance interval. These are original observations, not new source visits or participant activity.
- Result: works for the exercised scope. The changed comparison obligation does not expand acquisition; no universal refusal claim.

### 2. 方法選用符合待解問題與證據缺口；既有證據足夠時，不額外啟動研究或重問已回答的問題。

- Newly tried: C1 returns Friday directly without inquiry or simplification exercise. D1 compares current list and proposed queues from adequate context, D2 checks mandatory conditions and stops at the unsupported engineering premise. E1/E2 likewise perform bounded comparisons without research quotas.
- Unchanged-surface carryover: original C2's one concrete-episode question and exact supplied answer, C3's actual source comparison and C4's described connectivity scenario establish question-appropriate inquiry in the unchanged selection/acquisition text. No new framework efficacy claim follows.
- Result: works; neither simplification nor a method label caused settled facts to be reopened.

### 3. 研究結論可區分來源主張、使用者陳述與偏好、推論及未知；不把文獻、對談或方法名稱當成已完成的使用者研究或技術驗證。

- Newly tried: D1 labels current functionality as user account and removed burden as inference; D2 leaves package enforcement and actual keyboard implementation unverified. E1/E2 explicitly distinguish supplied correctness/controls from independent tests and leave X capability unknown. C1 treats personal preference as reported preference, not engagement or population evidence.
- Unchanged-surface carryover: original C3 distinguishes teammate claim, inspected W3C guidance and unseen-app conformance; original C5 rejects invented population evidence; original C6 distinguishes challenge from new factual evidence. Source/evidence-category rules and those actual records are unchanged.
- Result: works; no paper, dialogue, method name or saved record is counted as performed product research or technical proof.

### 4. 混合設計與技術問題能維持責任分界，將實作能力、相容性、可行性及安全控制實證的未解問題明確交回工程研究。

- Newly tried: D2 separates necessary design responsibilities from X 0.0.0 enforcement, names a bounded engineering-research handoff for exact-version reviewer separation/authorization evidence, retains the unknown and makes shared-screen consolidation conditional. No automatic delegation or private cross-plugin import occurred during that execution.
- Unchanged-surface carryover: original C4 explicitly covers conflict-free encrypted offline-sync compatibility/feasibility and key-leakage/security unknowns. Ownership and handoff guidance remains unchanged, and its original response/record is preserved. Newly loading the engineering skill for separately authorized E1/E2 witness cases is not delegation from D2.
- Result: works across the retained mixed-question and new constrained-simplification surfaces.

### 5. 延續或修正同一問題時，保留的研究紀錄與交付結論一致，並保留改變理由及限制。

- Newly tried: all five actual records were saved and their complete substantive contents returned by cat before delivery. D1/E1 retain reasons for simplifying; D2/E2 retain reasons controls/roles remain necessary and unresolved package premises. Delivery matches the saved conclusions, conditions and limits.
- Unchanged-surface carryover: original C2 same-question follow-up and C6 contradictory reminder record exercise actual continuation/correction, explicit withdrawal, preserved created date, updated date, reasoning-change explanation and substantive repeated readback. Continuation/template/readback sections and original transcripts are unchanged across the checked interval. These are retained actual update tests; new five cases are not falsely called same-record updates.
- Result: works for the affected retention content plus unchanged continuation/correction behavior.

### 6. 有可檢視的實際案例執行結果，能判定本次驗收要求的研究行為是否成立。

- Newly tried: five complete exact inputs, actual native responses, actual file writes and full record readbacks are retained in simplification-acceptance-trials.md. They cover positive simplification, preserved mandatory complexity, unsupported capability and adequate-evidence stopping in both owners. Clean packaging/release checks passed as recorded above. The automated test suite, which runs before the change is accepted and blocks it on failure, remains the final mechanical check.
- Unchanged-surface carryover: original six baseline/candidate trials remain preserved with original date/author/commit and exact source/turn/readback evidence; only the behavior they actually exercised is reused. No fresh baseline or broad improvement claim is made.
- Result: works within this controlled, non-blind sample. The added cases plus applicable retained observations support all seven rows; they establish neither general reliability nor actual participant evidence.

### 7. 對新增或重整的重要設計或工程方案，所屬研究技能能主動檢查是否有滿足同一需求與限制的更小方案，並清楚說明採用簡化或保留必要複雜度的理由。

- Newly tried in full: D1 recommends the already sufficient single list/checkbox over four queues/three self-performed roles and explains removed transitions/role burden. D2 rejects self-approval, retains distinct authorized review and keyboard access, considers shared presentation conditionally, and stops at missing X evidence. E1 retains the correct single process and rejects unneeded broker/services/loader/scheduler under identical formats and correctness. E2 rejects deleting tenant authorization/audit, considers shared handling only with controls/formats preserved, and leaves undocumented replacement capability unknown because further inquiry is unauthorized.
- All four retain the smaller shape or concrete necessity, reasoning status, decision impact and limits in actual records read back before response. C1 independently checks that adequate-evidence reuse remains direct; no simplification rounds, matrix or alternative count is imposed. No fixture explicitly requested simplification. No implementation or production experiment was used to fabricate support.
- Result: works in these four bounded proposal contexts. There is no carried-over evidence for this new obligation; these are the new actual candidate executions.

No new acceptance findings. The existing local-validator warnings are disclosed setup limitations, not newly certified host behavior or dismissed findings. No user-instructed skipped steps appear in the current intent constraints or plan risks. No source/participant or general-improvement claims are inferred beyond the captured executions.

