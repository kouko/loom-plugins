# Prevent unnecessary Loom stops — acceptance test evidence

Tried on 2026-10-31, in a clean copy of the project at `a24ab73d`.

## Setup and boundary

- Clean copy: `git worktree add --detach /private/tmp/loom-acceptance.IAD8Ts/checkout a24ab73d7a99474f99dc0af2d78be3f3a39677b` returned `HEAD is now at a24ab73d`.
- The clean copy's `git status --short --branch` returned `## HEAD (no branch)` with no changed files.
- Followed README.md's local plugin validation route: `agy plugin validate ./loom-code` returned `[ok]`, `skills: 7 processed`, `agents: 4 processed`, `hooks: 1 processed`; `agy plugin validate ./loom-design` returned `[ok]`, `skills: 6 processed`.
- First test command `python3 -m pytest ...` failed before collection because the default Python has no pytest (`No module named pytest`). The available project-independent `pytest` executable was used instead; its focused run passed.
- Focused command from the clean copy: `pytest -q loom-code/tests/test_one_way_door_question_rule.py loom-code/tests/test_one_way_door_copies.py loom-code/tests/test_questionrule_negation_rejected.py loom-code/tests/test_review_convergence_contract.py loom-code/tests/test_adversarial_product_one_way_door_without_spec.py loom-code/tests/test_adversarial_no_reask_pin_flipped_polarity.py loom-code/tests/test_write_plan_shape_text.py loom-design/tests/spec/test_adversarial_write_spec_no_reask_unpinned_sentences.py loom-design/tests/spec/test_capture_intent_contract.py loom-design/tests/spec/test_write_spec_contract.py` returned `131 passed in 0.48s`.
- The full package suite was deliberately left to `finalize-review`, which runs the repository-declared suite and blocks attestation on failure. The repo's suite entry point is `python3 scripts/run_package_tests.py --loom-family`; it was not run here.
- A controlled Codex probe was attempted with `codex exec --ephemeral --ignore-user-config -s read-only -C /private/tmp/loom-acceptance.IAD8Ts/checkout` and a prompt to read the changed Closing Review guidance and state the next actions without executing them. In the sandbox, the CLI returned `failed to initialize in-process app-server client: Operation not permitted`. The request to run the same read-only probe with host escalation was rejected by automatic approval review: it could transmit private worktree skill content to an external model service without explicit user authorization. The rejection explicitly prohibited bypassing it. No Codex behavioral response was obtained. No real Claude Code station run was performed.

## 1. 在本站已取得必要結果、下一個動作已明定且沒有合法停止條件時，agent 不需使用者再說「請繼續」就會執行該動作；只回報進度不算完成。

- How I tried it: Read the updated Closing Review instructions and ran the focused test command above, including `test_ready_review_continues_through_finalize_and_ship`.
- What came back: The test passed. The instructions at `loom-code/skills/closing-review/SKILL.md:438-440` say to run `finalize-review` in the current turn once verdicts and probe evidence are ready, and explicitly reject a progress-only update as completion.
- Evidence: `loom-code/tests/test_review_convergence_contract.py:214-230` asserts both clauses. This is a text-contract check; the controlled Codex probe and real Claude Code execution were unavailable as described above.

## 2. 在本站已完成、下一站已有明定入口且沒有合法停止條件時，agent 不需使用者再說「請繼續」就會啟動下一站。

- How I tried it: Read Closing Review finalization and handoff instructions and ran the same focused test.
- What came back: The test passed. `loom-code/skills/closing-review/SKILL.md:440-441` says a committed valid attestation leads to Ship in the same turn unless a stated stop applies; `:470-475` retains the Ship handoff.
- Evidence: `loom-code/tests/test_review_convergence_contract.py:214-230`. No actual attestation was generated or Ship session entered in this acceptance run.

## 3. 對於可由既有決定、專案證據、實測或適用的外部資料判斷的選擇，agent 先查證並記錄理由；「以後難替換」、「影響品質上限」或「有三項以上取捨」本身不會使 agent 停下來要求使用者選方案。

- How I tried it: Read `loom-code/skills/write-plan/references/one-way-door.md`, the write-plan instructions, and both loom-design copies; ran focused question-rule, cross-copy, negation, and decision-point tests in the command above.
- What came back: All selected tests passed. The reference at `loom-code/skills/write-plan/references/one-way-door.md:4-9,15-31,41-51` makes the risk classes disclosure triggers and directs evidence-based technical decisions; three trade-offs alone do not trigger a question. The two design station copies repeat the narrower rule. The negation probe proves its positive instruction would fail the text test if changed to `do not decide`.
- Evidence: `loom-code/tests/test_one_way_door_question_rule.py:31-44`, `loom-code/tests/test_questionrule_negation_rejected.py:16-32`, `loom-code/tests/test_one_way_door_copies.py:43-75`, `loom-design/tests/spec/test_capture_intent_contract.py:83-96`, `loom-design/tests/spec/test_write_spec_contract.py:292-304`. No agent was observed making a real choice.

## 4. 當不同做法會實質改變使用者要的結果，且查證後仍無法從既有決定推得偏好，或行動需要尚未取得的明確授權時，agent 才請使用者決定；在等待時繼續不依賴答案的工作。

- How I tried it: Read the unresolved outcome, prior-choice, data-consent, and waiting instructions in all three policy copies; ran the focused tests above, including no-spec and no-repeat adversarial cases.
- What came back: All selected tests passed. `loom-code/skills/write-plan/references/one-way-door.md:41-54,78-87` narrows questions to unresolved user outcomes or missing authorization, preserves prior decisions, and directs independent work during the wait. `loom-code/skills/write-plan/references/confirm-intent.md:64-87` sends no-spec product questions to the first decision point and avoids asking again after authorization. Both design copies carry the same decision boundary.
- Evidence: `loom-code/tests/test_one_way_door_question_rule.py:46-64`, `loom-code/tests/test_adversarial_product_one_way_door_without_spec.py:1-110`, `loom-code/tests/test_adversarial_no_reask_pin_flipped_polarity.py`, `loom-design/tests/spec/test_adversarial_write_spec_no_reask_unpinned_sentences.py`. No agent wait-and-continue behavior was observed in a live station run.

## 5. 對於重大選擇，使用者能看見與自身相關的後果，即使 agent 不需請使用者選方案；需要使用者確認成果、取得授權或遇到其他正當停止條件時，agent 仍依現有規則處理。

- How I tried it: Read the consequence and consent examples, decision-point guidance, and Closing Review stop boundaries; ran the focused tests above.
- What came back: All selected tests passed. `loom-code/skills/write-plan/references/one-way-door.md:56-73` calls for user-facing consequences even without a question. `:26-36,83-87` keeps existing-data consent. `loom-code/skills/closing-review/SKILL.md:439-452` preserves stated stops and skipped-review behavior; `:242-246` retains fresh authorization for a repeated outside review.
- Evidence: `loom-code/tests/test_one_way_door_question_rule.py:56-64`, `loom-code/tests/test_review_convergence_contract.py:214-230`, `loom-code/tests/test_one_way_door_copies.py:43-75`. User-visible handling in a real Claude Code conversation remains untested.

## Re-run on 2026-10-31, at `4f1c7eec`

- Clean copy: `git worktree add --detach /private/tmp/loom-acceptance-r2.X1arLD/checkout 4f1c7eece8f9637e1e5cd8c47f5daafa6e33c1b3` returned `HEAD is now at 4f1c7eec`; `git status --short --branch` returned `## HEAD (no branch)` and no changed files.
- Setup repeated from the README: `agy plugin validate ./loom-code` returned `[ok]`, `skills: 7 processed`, `agents: 4 processed`, `hooks: 1 processed`; `agy plugin validate ./loom-design` returned `[ok]`, `skills: 6 processed`.
- Fix range checked: `git diff --name-status 0edaff6f..4f1c7eece8f9637e1e5cd8c47f5daafa6e33c1b3` changed the question-rule test, write-spec guidance/test, three loom-code READMEs and the plan. Neither Closing Review guidance nor its convergence test changed, so rows 1 and 2 are carried over.
- A single mixed-root focused command, `pytest -q loom-code/tests/test_one_way_door_question_rule.py loom-code/tests/test_one_way_door_copies.py loom-code/tests/test_questionrule_negation_rejected.py loom-code/tests/test_adversarial_product_one_way_door_without_spec.py loom-code/tests/test_adversarial_no_reask_pin_flipped_polarity.py loom-code/tests/test_write_plan_shape_text.py loom-design/tests/spec/test_adversarial_write_spec_no_reask_unpinned_sentences.py loom-design/tests/spec/test_capture_intent_contract.py loom-design/tests/spec/test_write_spec_contract.py`, returned `1 failed, 118 passed in 0.50s`. `test_three_tradeoffs_reversed_rule_is_rejected` raised `AttributeError: <module 'private' (namespace) from ['/private']> has no attribute 'DOOR'` at `loom-code/tests/test_one_way_door_question_rule.py:69`. The test also passed when its file ran alone (`7 passed in 0.16s`). This is a portability defect in the new test's module lookup across pytest root layouts; no product guidance was changed by this finding.
- The project's package runner executes code and design test roots in separate subprocesses (`scripts/run_package_tests.py:122-138`), so the affected focused checks were repeated in that separation: `pytest -q loom-code/tests/test_one_way_door_question_rule.py loom-code/tests/test_one_way_door_copies.py loom-code/tests/test_questionrule_negation_rejected.py loom-code/tests/test_adversarial_product_one_way_door_without_spec.py loom-code/tests/test_adversarial_no_reask_pin_flipped_polarity.py loom-code/tests/test_write_plan_shape_text.py` returned `64 passed in 0.20s`; `pytest -q loom-design/tests/spec/test_adversarial_write_spec_no_reask_unpinned_sentences.py loom-design/tests/spec/test_capture_intent_contract.py loom-design/tests/spec/test_write_spec_contract.py` returned `55 passed in 0.20s`. These 119 focused cases passed in the package runner's grouping. The full package suite was not run; `finalize-review` will run it and block attestation on failure.
- The earlier automatic approval review rejected an escalated Codex probe because private skill text might reach an external model service without explicit authorization. It was not retried or bypassed. There is still no controlled model response or real Claude Code station run.

### 1. Carried over

- The fix diff did not touch `loom-code/skills/closing-review/SKILL.md` or `loom-code/tests/test_review_convergence_contract.py`; the prior result and its live-behavior limit remain valid.

### 2. Carried over

- The fix diff did not touch Closing Review finalization or handoff, or the focused test for either; the prior result and its live-handoff limit remain valid.

### 3. Re-tested in full

- How I tried it: Re-read `loom-code/skills/write-plan/references/one-way-door.md`, the write-plan and capture-intent guidance, the changed write-spec guidance, all three changed README language copies, and the rule/cross-copy/negation tests. Ran both focused test groups above, covering evidence-based technical choice, hard-to-swap and output-quality risk, three-trade-off reversal, and prior decisions.
- What came back: The code group passed 64 cases; the design group passed 55. The updated `loom-code/tests/test_one_way_door_question_rule.py:42-75` now checks the three-trade-off rule by sentence and mutates it to an automatic-question form. `loom-design/skills/write-spec/SKILL.md:238-254` directs late technical choices from evidence. `loom-code/README.md:102-108` and corresponding Japanese/Traditional Chinese paragraphs say hard-to-reverse choices disclose consequences and only unresolved user outcomes or missing authorization prompt a question. The mixed-root invocation's import failure is recorded above and is not a behavioral observation.
- Evidence: The two focused test outputs and inspected files above. No model was observed making a real choice.

### 4. Re-tested in full

- How I tried it: Re-read the no-spec first-question route, write-plan late-choice rule, capture-intent and write-spec decision points including the changed late-choice paragraph, the no-repeat and consent tests, and all three README copies. Ran both focused test groups above.
- What came back: The 119 cases in the runner-aligned grouping passed. `loom-design/skills/write-spec/SKILL.md:246-254` now asks for an unresolved user outcome or missing authorization after the visible-behavior message, continues independent work while waiting, and uses a reversible no-obligation option only if it meets the user's outcome. `loom-design/tests/spec/test_write_spec_contract.py:307-323` checks this boundary. The same question boundary appears in `loom-code/skills/write-plan/references/one-way-door.md:41-54,78-87` and the README paragraphs. A live wait-and-continue sequence remains unobserved.
- Evidence: The two focused test outputs and inspected guidance above.

### 5. Re-tested in full

- How I tried it: Re-read the consequence and existing-data consent examples, all three README copies, changed write-spec late-choice guidance, and Closing Review's existing consent/stop language; ran both focused test groups above.
- What came back: The 119 cases in the runner-aligned grouping passed. The README copies disclose material effects and require explicit consent for existing-data change or transfer. `loom-design/skills/write-spec/SKILL.md:246-254` preserves consequence disclosure and prior authorization before a committing action. `loom-code/skills/write-plan/references/one-way-door.md:56-73,83-87` preserves consequence and consent wording. The fix did not modify Closing Review's legitimate stop conditions or fresh authorization for repeated outside review. Real user-visible presentation remains unobserved.
- Evidence: The two focused test outputs and inspected guidance above.

## Re-run on 2026-10-31, at `ce451484`

- Clean copy: `git worktree add --detach /private/tmp/loom-acceptance-r3.Z3N3UU/checkout ce451484c8343784d57e2ad13d0deae0d93378f1` returned `HEAD is now at ce451484`; `git status --short --branch` returned `## HEAD (no branch)` and no changed files.
- Setup repeated: `agy plugin validate ./loom-code` returned `[ok]`, `skills: 7 processed`, `agents: 4 processed`, `hooks: 1 processed`; `agy plugin validate ./loom-design` returned `[ok]`, `skills: 6 processed`.
- Fix range: `git diff --name-status 36170136..ce451484c8343784d57e2ad13d0deae0d93378f1` changed only `loom-code/tests/test_one_way_door_question_rule.py` and the plan. The test now uses `sys.modules[__name__]` instead of `__import__(__name__)` at line 70. No station guidance, README, or other test changed.
- Repeated the formerly failing mixed-root command: `pytest -q loom-code/tests/test_one_way_door_question_rule.py loom-code/tests/test_one_way_door_copies.py loom-code/tests/test_questionrule_negation_rejected.py loom-code/tests/test_adversarial_product_one_way_door_without_spec.py loom-code/tests/test_adversarial_no_reask_pin_flipped_polarity.py loom-code/tests/test_write_plan_shape_text.py loom-design/tests/spec/test_adversarial_write_spec_no_reask_unpinned_sentences.py loom-design/tests/spec/test_capture_intent_contract.py loom-design/tests/spec/test_write_spec_contract.py` returned `119 passed in 0.34s`. The previous module-lookup failure did not recur.
- The package-runner-aligned focused groups also passed separately: the six loom-code files in the command above returned `64 passed in 0.34s`; the three loom-design files returned `55 passed in 0.34s`. The full package suite was not run; `finalize-review` will run it and block attestation on failure.
- The auto-review-rejected external Codex probe was not retried or bypassed. No controlled model response or real Claude Code station run is available.

### 1. Carried over

- The fix touched only the A3 test's self-module lookup and plan record; Closing Review execution guidance and its prior evidence are unchanged.

### 2. Carried over

- The fix touched only the A3 test's self-module lookup and plan record; Closing Review handoff guidance and its prior evidence are unchanged.

### 3. Re-tested in full

- How I tried it: Re-read the evidence-based technical-choice and three-trade-off guidance in write-plan, capture-intent, write-spec, and the three loom-code README languages. Inspected the one-line self-module fix and repeated the full A3 focused surface: question rule, mutation, negation, cross-copy, no-spec and no-repeat cases, alongside the write-spec decision tests.
- What came back: The mixed-root invocation passed all 119 tests; the code and design groups separately passed 64 and 55. The reversed three-trade-off sentence was still rejected by the mutation test, now without an import-layout failure. The changed test is `loom-code/tests/test_one_way_door_question_rule.py:42-73`; the policy wording at `loom-code/skills/write-plan/references/one-way-door.md:4-9,15-31,41-51`, `loom-design/skills/capture-intent/SKILL.md:204-224`, `loom-design/skills/write-spec/SKILL.md:190-224`, and the three README paragraphs remains the same as Round 2. No agent was observed making a real decision.
- Evidence: The three focused test outputs, plugin validations, inspected files and diff above. The Round 2 portability finding is resolved; real-host behavior remains unverified.

### 4. Carried over

- The fix did not alter the unresolved-outcome, authorization or wait-and-continue guidance, or its tests, apart from the A3 test's own module lookup.

### 5. Carried over

- The fix did not alter consequence disclosure, existing-data consent, legitimate stop guidance, or its tests, apart from the A3 test's own module lookup.
