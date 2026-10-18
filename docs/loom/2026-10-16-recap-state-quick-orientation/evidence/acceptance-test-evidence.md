# Recap state quick orientation — acceptance test evidence

Tested on 2026-10-17 in a fresh local clone at `ce8f7cd4e463297caab89753c03afe24347e7893`. The clone was made with `git clone --no-hardlinks --quiet . /private/tmp/recap-state-acceptance-ce8f7cd4`; `git status --short` returned no changes. No product files were edited. The current chat host did not offer a way to load the plugin from this clone and capture a live recap. Therefore tests and the checked example establish the shipped instruction contract, while live behavior and rendered chat remain unverified.

## Clean-copy setup and targeted checks

- README setup reviewed: `README.md:180-270` describes plugin installation for Claude Code, Codex, Antigravity CLI, and OpenCode. A global install from this clone would alter the user's plugin state; local validation was available and used instead.
- Command: `agy plugin validate ./loom-workflow`
- Output: `[ok] ./loom-workflow`, `skills: 13 processed`, `hooks: 1 processed`.
- Command: `pytest -q loom-workflow/tests/recap-state/test_skill_md.py loom-workflow/tests/recap-state/test_seven_block_schema.py loom-workflow/tests/recap-state/test_readmes.py loom-workflow/tests/scripts/test_recap_state_compaction.py`
- Output: `................ [100%]` and `16 passed in 0.16s`.
- The full package suite was deliberately left to `finalize-review`; the README command is `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`, the automated test suite that runs before acceptance and blocks a failing change. No result is claimed for that suite here.
- `python3 -m pytest` could not run because the default Python 3.15 lacks pytest. The existing `pytest` executable ran the targeted checks without installing a package.

## 1. 長時間對話的回顧先交代有對話依據的原始目的、目前位置和建議下一步；無法確認的資訊會明示未知。

- How I tried it: inspected the active skill and reference in the clean clone; ran `test_runtime_routes_to_orientation_schema_without_six_required_sections`, `test_l3_contract_defines_goal_grounded_natural_output`, and `test_entrypoint_routes_to_purpose_first_variable_length_recap` within the 16-test command above.
- What came back: all named tests passed. The reference starts with original purpose, current position and proposed next step; it says unknown facts must be labeled and purpose must not be inferred from silence. The fictional long-session example begins with the user's stated purpose and current gap.
- Evidence: `loom-workflow/skills/recap-state/SKILL.md:21-26`, `loom-workflow/skills/recap-state/references/seven-block-schema.md:14-21`, `:120-121`. No live long-session recap was captured.

## 2. 回顧呈現影響目前方向的關鍵決定、已完成事項與尚存差距，使使用者不需自行重建工作過程。

- How I tried it: inspected the example's decision, completed-work and pending-work sequence; ran `test_good_example_demonstrates_long_session_orientation`.
- What came back: the named test passed. The example identifies the order-date decision, completed imports and verification, the refund gap, and the next decision.
- Evidence: `loom-workflow/skills/recap-state/references/seven-block-schema.md:120-149`. No real conversation was summarized by a loaded skill.

## 3. 段落標題清楚醒目，段落之間有可辨識的留白；表格前有簡短狀況說明，可比較資訊和實際依賴關係以適合的形式呈現；簡單情況維持精簡，不加入裝飾性圖表。

- How I tried it: ran `test_good_example_demonstrates_long_session_orientation` and `test_l3_contract_defines_goal_grounded_natural_output`; independently computed the displayed widths of all four three-line heading frames with Python Unicode East Asian width; checked the example's separator and table preface.
- What came back: tests passed; each frame measured `[28, 28, 28]` cells across top, middle and bottom; three fullwidth-space-only separator lines appear between four sections; a situation sentence immediately precedes the table. The reference reserves diagrams for real dependency, branch or merge topology and omits padding in short sessions.
- Evidence: `loom-workflow/skills/recap-state/references/seven-block-schema.md:19-36`, `:114-155`. The actual chat renderer and diagram choice were not exercised.

## 4. 回顧區分已確認事實、假設與未知，並逐字保留會影響後續行為的使用者原文。

- How I tried it: inspected active wording and its worked example; ran `test_l3_contract_defines_goal_grounded_natural_output` and `test_good_example_demonstrates_long_session_orientation`.
- What came back: tests passed. The contract names facts, assumptions, unknowns and exact wording. The example quotes the fictional user's objective and labels its unknown refund rule.
- Evidence: `loom-workflow/skills/recap-state/SKILL.md:27-29`, `:37-43`; `loom-workflow/skills/recap-state/references/seven-block-schema.md:36-40`, `:120-121`, `:143-149`. Exact quotation by a live agent was not observed.

## 5. 回顧最後提出明確的方向確認問題，並在使用者回答前停止後續工作。

- How I tried it: inspected the final example line and the stop contract; ran `test_good_example_demonstrates_long_session_orientation` and `test_runtime_routes_to_orientation_schema_without_six_required_sections`.
- What came back: tests passed. The example ends by asking whether the proposed refund-rule-first sequence matches the user's direction. Both entrypoint and reference tell the agent to wait for an answer.
- Evidence: `loom-workflow/skills/recap-state/SKILL.md:31-33`, `:45-51`; `loom-workflow/skills/recap-state/references/seven-block-schema.md:27-29`, `:153-161`. No live post-question pause was observed.

## 6. 回顧只出現在目前對話，不寫入檔案，也不取代跨對話交接或內建的離開後摘要。

- How I tried it: checked the entrypoint, reference and three localized READMEs; ran `test_tri_lang_readmes_describe_flexible_recap_and_pause_without_six_section_claim` plus the routing tests.
- What came back: tests passed. All three READMEs describe no disk write; the entrypoint explicitly says chat only and separates the handoff and built-in away-summary features.
- Evidence: `loom-workflow/skills/recap-state/SKILL.md:11-13`, `:45-51`; `loom-workflow/skills/recap-state/references/seven-block-schema.md:39-40`. A loaded host invocation and its file effects were not observed.

## 7. Long-session recap flow

- How I tried it: inspected the fictional long-session example and ran `test_good_example_demonstrates_long_session_orientation`.
- What came back: the example covers purpose, position, prior decisions, completed work, gap, unknowns and a next-step question; the test passed.
- Evidence: `loom-workflow/skills/recap-state/references/seven-block-schema.md:114-161`. No host run was captured.

## 8. Short-session recap flow

- How I tried it: inspected the short-session condition and ran `test_l3_contract_defines_goal_grounded_natural_output` and `test_tri_lang_readmes_describe_flexible_recap_and_pause_without_six_section_claim`.
- What came back: tests passed. The contract says to omit sections with no useful content and avoid invented history.
- Evidence: `loom-workflow/skills/recap-state/references/seven-block-schema.md:19-21`, `:31-35`. No host run was captured.

## 9. Table recap flow

- How I tried it: inspected the example table and preceding sentence; ran `test_good_example_demonstrates_long_session_orientation`.
- What came back: the test passed; the example has a plain situation sentence before the table.
- Evidence: `loom-workflow/skills/recap-state/references/seven-block-schema.md:143-149`. Rendered chat was not captured.

## 10. Dependency or branch recap flow

- How I tried it: inspected diagram-selection instructions.
- What came back: the contract says to use a diagram only when it clarifies real dependency, branch or merge topology. There is no named output test or live rendered example for this flow; no behavior verdict is available.
- Evidence: `loom-workflow/skills/recap-state/references/seven-block-schema.md:31-36`, `:64-69`.

## Re-run on 2026-10-17, at d4f5a706

The re-run used a new clean local clone at `/private/tmp/recap-state-acceptance-d4f5a706`. `git rev-parse HEAD` returned `d4f5a7067b37733c80577d5c5a430e702868d4f1`; `git status --short` returned no changes. The fix range `d3fe984a..d4f5a706` changes only the skill entrypoint, its reference, and two focused test modules. It conditions next-step guidance on a grounded original purpose. The host still could not load this clone into an observed chat, so the live-renderer and live-pause limitations remain.

- Setup check: `agy plugin validate ./loom-workflow` returned `[ok]`, `skills: 13 processed`, `hooks: 1 processed`.
- Focused command: `pytest -q loom-workflow/tests/recap-state/test_seven_block_schema.py::test_l3_contract_defines_goal_grounded_natural_output loom-workflow/tests/recap-state/test_seven_block_schema.py::test_good_example_demonstrates_long_session_orientation loom-workflow/tests/scripts/test_recap_state_compaction.py::test_entrypoint_routes_to_purpose_first_variable_length_recap loom-workflow/tests/recap-state/test_readmes.py::test_tri_lang_readmes_describe_flexible_recap_and_pause_without_six_section_claim`.
- Output: `.... [100%]`, `4 passed in 0.13s`.
- Independent branch check: both active instruction files contain the unknown-purpose-only question, prohibition on an invented next step, grounded-purpose next-step branch, and wait condition. The known-purpose example still ends with a directed question. All six checks returned `True`.
- Full package suite: left to `finalize-review` as on the first run; no result claimed here.

### Acceptance 1 — re-tested

- Known-purpose branch: the reference leads with grounded original purpose and position, allows a next step only when grounded, and retains the fictional known-purpose example. The named reference and example tests passed.
- Unknown-purpose branch: the entrypoint says to ask only for original purpose and not invent a work step; the reference repeats both instructions and says to wait for clarification. The updated entrypoint test checks these in both files and passed.
- Anchors: `loom-workflow/skills/recap-state/SKILL.md:21-37`; `loom-workflow/skills/recap-state/references/seven-block-schema.md:14-24`, `:116-167`. Live conversation behavior remains unverified.

### Acceptance 2 — carried over

- Diff check: the fix changes purpose and final-question wording but does not change the reference's decisions, completed-work and remaining-gap guidance or its worked trajectory. The first-run partial verdict remains.

### Acceptance 3 — carried over

- Diff check: heading frame, fullwidth-space line, table preface and diagram-selection instructions are unchanged. The first-run width check and rendered-host limitation remain.

### Acceptance 4 — carried over

- Diff check: the fix reinforces unknown-purpose handling but does not change the requirements to distinguish facts, assumptions and unknowns or preserve consequential user wording. The first-run partial verdict remains.

### Acceptance 5 — re-tested

- Unknown-purpose branch: both active instructions direct the final question solely to the missing purpose, forbid proposing a work step, and require waiting for the user to state or clarify it. The updated entrypoint test passed.
- Known-purpose branch: the example still asks whether the proposed next sequence matches the user's direction; the reference requires a pause and the named example test passed.
- Anchors: `loom-workflow/skills/recap-state/SKILL.md:32-37`, `:46-55`; `loom-workflow/skills/recap-state/references/seven-block-schema.md:20-33`, `:99-106`, `:161-167`. Live post-question pause remains unverified.

### Acceptance 6 — carried over

- Diff check: the chat-only, no-file, handoff and built-in-recap boundaries did not change. The first-run partial verdict remains.

### UI flow 7, long conversation — re-tested

- Known-purpose trajectory: the existing example still covers original purpose, current position, decisions, completed work, remaining gap and an alignment question; its named test passed.
- Unknown-purpose trajectory: active entrypoint and reference require asking only for purpose, with no invented next work step; the updated entrypoint test passed. No host run was captured.

### UI flow 8, short conversation — re-tested

- The reference still says to omit sections with no useful content. Its unknown-purpose branch asks only for purpose, including in a short session. The reference and localized README tests passed. No host run was captured.

### UI flow 9, table — carried over

- Diff check: neither the table preface guidance nor the worked table changed. The first-run partial verdict remains.

### UI flow 10, dependency or branch — carried over

- Diff check: diagram-selection guidance did not change. No live diagram or output test became available, so the first-run `not verified` verdict remains.

## Re-run on 2026-10-17, at 46794ef6

The re-run used a new clean clone at `/private/tmp/recap-state-acceptance-46794ef6`. `git rev-parse HEAD` returned `46794ef699876c260a38a3a95916b0e225e624d0`; `git status --short` returned no changes. The fix range `c79b8c4e..46794ef6` adds diagram examples and their tests in the recap reference bundle; it does not change the skill entrypoint. No plugin from this clone was loaded into a live host chat, so rendering and model choice remain unobserved.

- Setup check: `agy plugin validate ./loom-workflow` returned `[ok]`, `skills: 13 processed`, `hooks: 1 processed`.
- Focused command: `pytest -q loom-workflow/tests/recap-state/test_seven_block_schema.py loom-workflow/tests/scripts/test_recap_state_compaction.py`.
- Output: `...... [100%]`, `6 passed in 0.14s`.
- Alignment check: each of the four diagrams was extracted from its fenced example and piped into `loom-workflow/skills/loom-visualization/scripts/align.py -`; all four returned exit 0 and `no drift`. The four heading frames also returned exit 0. The tool uses Unicode display-cell widths, including CJK characters.
- Structure check: the worked recap contains only the decision-context diagram; the argument map, decision tree and flowchart occur after it in `## 6 — Other diagram examples`. The worked recap retains three fullwidth-space-only separator lines, a situation sentence immediately before its table, and four framed headings. Both the active selection rule and the examples say to draw a diagram only when the relationship adds understanding.
- Full package suite: left to `finalize-review`; no result claimed here.

### Acceptance 1 — carried over

- Diff check: the new decision-context diagram is inserted inside the existing middle section. The grounded-purpose and unknown-purpose branches, first section and proposed-next-step guidance are unchanged. The prior partial verdict remains.

### Acceptance 2 — re-tested

- The worked recap still states the original goal, current position, completed imports and verification, and unresolved refund rule. Its new decision-context diagram connects the goal to an earlier order-total-only proposal, then explains why the proposal was dropped in favor of including refunds. This is a stated tradeoff, not a claim about hidden reasoning. The named worked-example test passed.
- Anchors: `loom-workflow/skills/recap-state/references/seven-block-schema.md:116-185`. No live long-session recap was captured.

### Acceptance 3 — re-tested

- Four distinct relationships were checked: the worked recap's decision-context diagram gives a rationale for an earlier choice; the argument map separates a confirmed fictional observation from an unresolved rule in support of asking the user; the decision tree branches on the user's future answer; the flowchart orders three steps after the rule is settled. The three mini examples are explicitly alternatives, not additional diagrams for the worked recap.
- All four diagrams and all four heading frames passed `align.py -`. The worked recap has three fullwidth-space-only section separators and a brief situation sentence before its table. The active rule reserves diagrams for useful dependency, branch or merge topology and keeps flat progress in prose or a table. The named reference tests passed.
- Anchors: `loom-workflow/skills/recap-state/references/seven-block-schema.md:20-44`, `:116-185`, `:200-250`. Actual host rendering and automatic diagram selection were not observed.

### Acceptance 4 — carried over

- Diff check: the new argument map explicitly says to suppose a fictional confirmed observation. It is an illustrative case, while the active fact, assumption, unknown and exact-wording requirements are unchanged. The prior partial verdict remains.

### Acceptance 5 — carried over

- Diff check: the worked recap still ends with the same directed question, and neither pause instruction changed. The prior partial verdict remains.

### Acceptance 6 — carried over

- Diff check: the new material is confined to the skill's reference examples. The chat-only, no-file, handoff and built-in-recap boundaries are unchanged. The prior partial verdict remains.

### UI flow 7, long conversation — re-tested

- The complete worked recap keeps purpose, position, decisions, completed work, unknown, pending action and its final alignment question. It now has one decision-context diagram in the decision section and no argument-map, decision-tree or flowchart insert. The named worked-example test passed. No host run was captured.

### UI flow 8, short conversation — carried over

- Diff check: the additions are to the long-session worked example and separate mini examples; the short-session omission rule is unchanged. The prior partial verdict remains.

### UI flow 9, table — carried over

- Diff check: the worked table and its situation sentence are unchanged. The same sentence was checked while testing Acceptance 3; the prior partial verdict remains.

### UI flow 10, dependency or branch — re-tested

- The new decision tree visibly forks between original payment week and actual refund week, each with a different calculation action. The flowchart shows ordered steps, and the argument and decision-context examples express other relationships. All four diagrams passed the width-aware alignment check. This gives partial evidence for the graph flow; no live agent selected or rendered a diagram, so full behavior remains unverified.
- Anchors: `loom-workflow/skills/recap-state/references/seven-block-schema.md:200-250`.

## Re-run on 2026-10-18, at fdf5738b

This re-run used a fresh local clone at `/private/tmp/recap-state-acceptance-fdf5738b`, made with `git clone --no-hardlinks --quiet . /private/tmp/recap-state-acceptance-fdf5738b`. Before probe setup, `git rev-parse HEAD` returned `fdf5738bdde7930babace10525e10fc46ac061ba` and `git status --short` was empty. The source range was `e4e8c626..fdf5738b`; the relevant edits change historical-decision provenance and diagram eligibility in the active skill/reference, plus the conditional final question in all three skill-local READMEs. A merge also brought unrelated loom-code work from main. The previous Codex CLI dogfood at `e4e8c626` is historical evidence only and is **not** used to verify this fixed source.

### Clean-copy setup and focused checks

- README setup: `README.md:174-230` documents installation and local plugin validation; `README.md:272-283` gives the package suite command. A global install would change the user's installed plugin, so the local validator was used for setup. Command: `agy plugin validate ./loom-workflow`. Output: `[ok] ./loom-workflow`; `skills: 13 processed`; `hooks: 1 processed`.
- Focused command: `pytest -q loom-workflow/tests/recap-state/test_skill_md.py loom-workflow/tests/recap-state/test_seven_block_schema.py loom-workflow/tests/recap-state/test_readmes.py loom-workflow/tests/scripts/test_recap_state_compaction.py`. Output: `20 passed in 0.17s`.
- Alignment check: a Python reader extracted all eight fenced text blocks from `loom-workflow/skills/recap-state/references/seven-block-schema.md` and passed each to `python3 loom-workflow/skills/loom-visualization/scripts/align.py -`; each exited 0 with `✓ no drift`. This includes four section-heading frames and four diagrams. The complete worked recap has three fullwidth-space-only separator lines and the situation sentence immediately before its table.
- The package suite was not run by this witness. Its README command is `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`. `finalize-review` will execute that suite as an automated check before acceptance and block the change if it fails; no suite result is claimed here.
- Codex-only behavior setup: copied the current `recap-state` and `loom-visualization` skill folders into the clone's `.agents/skills/`. SHA-256 showed the copied recap `SKILL.md` and reference matched the source (`f1468372...` and `72b99c97...`). The copy was untracked probe setup, made only after the clean-clone check.
- Attempted read-only natural-language probe: `command codex exec -C /private/tmp/recap-state-acceptance-fdf5738b --ephemeral --json -s read-only '我跟丟了，幫我回顧目前進度。'`. The sandbox returned `failed to initialize in-process app-server client: Operation not permitted (os error 1)` before any model output. A host escalation request for the same read-only command was rejected by automatic approval review because private repository content might be sent to an external model service without specific authorization; the rejection explicitly forbade a workaround. The explicit `$recap-state` probe was therefore not attempted. No current-HEAD model output, rendered client view, or post-question pause exists. The redirected natural-language JSONL file is empty.

### Acceptance 1 — re-tested

- Checked both branches of `SKILL.md:21-40` and `references/seven-block-schema.md:14-27`: grounded purpose leads to position and proposed next step; unknown purpose is labeled and leads only to a purpose question. The complete example at reference `:118-195` still covers the grounded branch. All three local READMEs now describe both branches (`README.md:17-43`, `README.ja.md:18-41`, `README.zh-TW.md:15-38`). The four-module focused command passed. No long-session output from the fixed version was obtained.

### Acceptance 2 — re-tested

- `SKILL.md:21-28` and reference `:14-22` now require an identifiable user turn or prior action before calling something a historical decision, and exclude this recap's formatting choices. The worked example at reference `:118-195` still shows the fictional order-total choice, rejected alternative, completed imports and reconciliation, refund gap and next action. `test_skill_requires_source_for_past_decisions`, `test_past_decisions_require_identifiable_conversation_evidence`, and the worked-example test passed in the focused command. Whether a live recap obeys the provenance rule remains unobserved.

### Acceptance 3 — re-tested

- Reference `:29-48` and `:73-81` now admit useful rationale, evidence and sequence diagrams as well as dependency, branch and merge relationships, while excluding flat status decoration. The worked recap has one decision-context diagram; the other three are separate alternatives (`:198-251`). All eight framed text blocks passed `align.py`; there are three separator lines and a brief table preface. The focused tests, including `test_diagram_rule_covers_meaningful_reasoning_without_status_decoration`, passed. Chat rendering and autonomous format choice remain unverified.

### Acceptance 4 — re-tested

- The new source-check rule at `SKILL.md:24-27` and reference `:18-22` addresses unsupported past decisions. The existing exact-quotation and fact/assumption/unknown rules remain at `SKILL.md:31-47` and reference `:44-47`, `:91-107`. The fictional example quotes the stated goal and labels the refund rule unknown. Focused tests passed; a live model's exact quoting and evidence classification were not observed.

### Acceptance 5 — re-tested

- `SKILL.md:35-40`, `:49-59` and reference `:23-36`, `:103-111` require the purpose-only question when purpose is unknown, otherwise a grounded next-step question, then a wait. Each updated local README now states these two branches in prose and in a two-wait-state flow (`README.md:17-43`, `:86-88`; `README.ja.md:18-41`, `:81-82`; `README.zh-TW.md:15-38`, `:77-78`). `test_tri_lang_readmes_keep_final_question_conditional` and routing tests passed. No live question or pause was observed.

### Acceptance 6 — carried over

- Diff check: `git diff e4e8c626..fdf5738b -- loom-workflow/skills/recap-state` changes only decision provenance, diagram permission and README question wording. `SKILL.md:53-59` and reference `:47-48` still set chat-only/no-file and handoff/built-in-recap boundaries; the README no-disk sentences are unchanged. Prior `partly` verdict remains because a live invocation's file effects were never observed.

### UI flow 7, long conversation — re-tested

- The complete example at reference `:118-195` still provides purpose, current position, a stated choice with tradeoff, completed work, remaining gap, unknown rule and one directed final question. The new provenance rule was checked against the whole flow. The worked-example and decision-source tests passed. No current-HEAD long-session model run was obtained.

### UI flow 8, short conversation — re-tested

- Reference `:23-27` still omits useless sections, while all three changed READMEs now give the unknown-purpose-only question and separate waiting branch. Focused README and schema tests passed. No current-HEAD short-session model run was obtained.

### UI flow 9, table — re-tested

- Reference `:38-43`, `:73-81` still prefers a table for comparison and a plain sentence before it, while excluding diagrams for flat status. The worked recap at `:166-180` has the preface directly before its table. Focused schema tests passed; live table selection and rendering remain unverified.

### UI flow 10, dependency or branch — re-tested

- Reference `:40-43`, `:73-81` includes genuine dependency and branch relationships, and `:219-251` shows a future decision branch and ordered process. All four diagram blocks passed `align.py`. No current-HEAD model selection or client rendering was observed.

## Re-run on 2026-10-18, at 0b120aa0

This re-run used a new clean clone at `/private/tmp/recap-state-acceptance-0b120aa0`, created with `git clone --no-hardlinks --quiet . /private/tmp/recap-state-acceptance-0b120aa0`. Before checks, `git rev-parse HEAD` returned `0b120aa0d55c86667adf17327652cb69e349ebad`; `git status --short` was empty. `git diff 937f885f..0b120aa0` changed only three lines in `docs/loom/2026-10-16-recap-state-quick-orientation/spec.md`: conditional next-step wording in REQ-1, conditional final-question wording in REQ-5, and diagram eligibility in one design decision. No runtime skill, schema, README, or test changed. This is a spec-conformance re-run, not a new live behavior trial.

### Clean-copy setup and focused checks

- Followed `README.md:174-230`'s local validation path: `agy plugin validate ./loom-workflow` returned `[ok] ./loom-workflow`, `skills: 13 processed`, and `hooks: 1 processed`.
- Ran the focused recap checks: `pytest -q loom-workflow/tests/recap-state/test_skill_md.py loom-workflow/tests/recap-state/test_seven_block_schema.py loom-workflow/tests/recap-state/test_readmes.py loom-workflow/tests/scripts/test_recap_state_compaction.py`. Output: `20 passed in 0.19s`.
- Re-extracted eight fenced text blocks from the unchanged runtime reference and ran each through `python3 loom-workflow/skills/loom-visualization/scripts/align.py -`: eight of eight returned exit 0 and `no drift`. The worked recap still has three fullwidth-space-only section separators and a situation sentence directly before its table.
- The full package suite was left to `finalize-review`. The README command is `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`; that automated suite runs before acceptance and blocks a failing change. No result for the full suite is claimed here.
- The previous attempt to run the current skill through Codex CLI was rejected by automatic approval review because it could transmit private repository content to an external model. The rejection explicitly forbade a workaround. No Codex CLI command was retried, no Claude Code was used, and no output or client rendering at `0b120aa0` was observed. The older `e4e8c626` dogfood does not verify this source.

### Acceptance 1 — re-tested

- Full scope checked: known purpose, unknown purpose, long-session output guidance, current position, and next-step condition. The changed `spec.md:7` now agrees with `SKILL.md:21-40` and reference `:14-27`: a proposed next step requires a grounded purpose; otherwise the recap labels it unknown and asks for purpose. The known-purpose worked example remains at reference `:118-195`, and all three unchanged local READMEs still describe both branches. Focused tests passed.
- Finding: `spec.md:38` still says the long-session UI flow shows a `proposed next step` without a purpose condition. In the unknown-purpose case, that line conflicts with REQ-1 and the runtime prohibition on inventing a work step. No live long-session output was obtained; result remains `partly`.

### Acceptance 2 — carried over

- Diff check: the only source change is `spec.md:7`, `:16`, `:22`. REQ-2 and the runtime decision-source, completed-work and remaining-gap rules did not change. The prior `partly` verdict and its no-live-output limit remain.

### Acceptance 3 — re-tested

- Full scope checked: heading frames, separator spacing, table preface, information-bearing diagrams, flat-status exclusion and short-session economy. The changed design decision at `spec.md:22` now names rationale, evidence, sequence, dependency, branch and merge, matching reference `:38-43`, `:73-81`. The eight alignment checks, three fullwidth separators, table-preface check and relevant focused tests passed. Actual client spacing and autonomous diagram choice remain unobserved; result is `partly`.

### Acceptance 4 — carried over

- Diff check: REQ-4, runtime fact/assumption/unknown and exact-quotation rules, and worked example were untouched. The prior `partly` verdict remains because no live output was observed.

### Acceptance 5 — re-tested

- Full scope checked: unknown-purpose question, grounded-purpose next-step question, and stop/wait. Changed `spec.md:16` now matches `SKILL.md:35-40`, `:49-59` and reference `:23-36`, `:103-111`; three local READMEs still show separate waiting states. Focused tests passed. The contradictory long-session UI flow at `spec.md:38` remains, and no live question or post-question pause was observed; result is `partly`.

### Acceptance 6 — carried over

- Diff check: REQ-6, runtime chat-only/no-file, handoff and built-in-recap boundaries were untouched. The prior `partly` verdict remains because live file effects were never observed.

### UI flow 7, long conversation — re-tested

- Checked both purpose branches and every named surface. The worked example still covers purpose, current position, history, completed and pending work, unknown refund rule, a grounded next step and final alignment question. `spec.md:38` remains unqualified about next step, conflicting with `spec.md:7`, `:16` for an unknown-purpose long session. Worked-example and routing tests passed; no host run was obtained.

### UI flow 8, short conversation — re-tested

- The changed REQ-5 applies to short sessions too: reference `:23-27` still omits useless sections and asks only for the original purpose when unknown. Three local READMEs retain this branch. Focused schema and README tests passed; no host output was obtained.

### UI flow 9, table — re-tested

- The changed diagram decision at `spec.md:22` excludes flat status diagrams, leaving the table rule in `spec.md:40` and reference `:38-43`, `:73-81` aligned. The worked table still has its situation sentence immediately before it. Focused tests passed; live selection and rendering remain unverified.

### UI flow 10, dependency or branch — re-tested

- `spec.md:22`, `:41` and reference `:40-43`, `:73-81` permit a diagram for real dependency/branch relationships when it helps. The decision-tree and process examples at reference `:219-251` remain, and all four diagram text blocks passed the alignment checker. A live agent's selection and client rendering remain unverified.

## Re-run on 2026-10-18, at 6b8cf5e2

This focused re-run used a new clean clone at `/private/tmp/recap-state-acceptance-6b8cf5e2`, created with `git clone --no-hardlinks --quiet . /private/tmp/recap-state-acceptance-6b8cf5e2`. Before checking it, `git rev-parse HEAD` returned `6b8cf5e2e4d4a0f48f1c652193574e71d607ce8c` and `git status --short` was empty. `git diff bfe412cc..6b8cf5e2` changes only the long-session UI-flow sentence at `docs/loom/2026-10-16-recap-state-quick-orientation/spec.md:38`. No runtime skill, schema, README, test, or other spec sentence changed.

### Clean-copy setup and focused checks

- `agy plugin validate ./loom-workflow` returned `[ok] ./loom-workflow`, `skills: 13 processed`, `hooks: 1 processed`.
- `pytest -q loom-workflow/tests/recap-state/test_skill_md.py loom-workflow/tests/recap-state/test_seven_block_schema.py loom-workflow/tests/recap-state/test_readmes.py loom-workflow/tests/scripts/test_recap_state_compaction.py` returned `20 passed in 0.19s`.
- The full package suite was left to `finalize-review`. Its README command remains `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`; that automated test suite runs before acceptance and blocks a failing change. No full-suite result is claimed here.
- The earlier Codex CLI escalation was rejected by automatic approval review due to possible transmission of private repository content to an external model, with an explicit no-workaround instruction. No Codex CLI command was retried and no Claude Code was used. Current-HEAD model output, rendered chat, and post-question pause remain unobserved.

### Acceptance 1 — re-tested

- Checked the entire long-conversation path in both purpose branches. `spec.md:7` requires original purpose and position, unknown labeling, and a next step only for a grounded purpose. The fixed UI flow at `spec.md:38` now says `grounded original purpose or an explicit unknown`, then asks only for the purpose and waits when unknown, while proposing a next step and asking for alignment when grounded. This matches `SKILL.md:21-40`, reference `:14-27`, and the three local README descriptions. The known-purpose worked example still covers original purpose, current position, work history, completed work, gap, unknown refund rule and proposed next action. Focused tests passed. No current-HEAD live recap was obtained, so result remains `partly`.

### Acceptance 2 — carried over

- Diff check: only `spec.md:38` changed, and its new purpose/final-question branches do not alter REQ-2, historical-decision source checking, completed work, or remaining-gap requirements. Prior `partly` verdict and live-output limit remain.

### Acceptance 3 — carried over

- Diff check: only the long-session purpose/final-question sentence changed. Section frames, spacing, table preface, diagram eligibility and short-session economy did not change. Prior alignment and focused-test evidence, plus the rendered-client limit, remain.

### Acceptance 4 — carried over

- Diff check: fact/assumption/unknown classification, exact consequential quotation and past-decision provenance rules were untouched. Prior `partly` verdict remains.

### Acceptance 5 — re-tested

- Checked both final-question paths and the wait condition in full. Fixed `spec.md:38` now requires the unknown-purpose question and wait, or the grounded next-step alignment question and wait; it agrees with `spec.md:15`, `SKILL.md:35-40`, `:49-59`, and reference `:23-36`, `:103-111`. Focused tests passed. The earlier important finding at `spec.md:38` is resolved in the source contract. A real model question and pause were not observed, so result remains `partly`.

### Acceptance 6 — carried over

- Diff check: only `spec.md:38` changed; chat-only/no-file, handoff and built-in-recap boundaries did not change. Prior `partly` verdict remains because live file effects were not observed.

### UI flow 7, long conversation — re-tested

- Checked every named part of the UI flow: grounded purpose or explicit unknown, current position, concise history, completed and pending work, and the two conditional final-question branches with a wait. The fixed `spec.md:38` now matches REQ-1 and REQ-5 and the unchanged runtime instructions. The worked example demonstrates the grounded branch; the unknown branch is specified in the runtime and three local READMEs. Focused tests passed. No current-HEAD host output was captured.

### UI flows 8–10 — carried over

- Diff check: `git diff bfe412cc..6b8cf5e2` has only the long-session UI-flow line. The short-session, table and dependency/branch UI-flow lines at `spec.md:39-41` are unchanged, as are their runtime guidance, examples and focused tests. Their prior `partly` verdicts and live-rendering limitations remain.

## Codex CLI behavioral verification — 2026-10-18

The user explicitly authorized a Codex-only live test. `command codex --version` returned `codex-cli 0.163.0`. Tests used a read-only `codex exec` session in `/private/tmp/recap-state-codex-current-20261018`; only the current branch's `SKILL.md` and `references/seven-block-schema.md` were copied to local `.agents/skills/recap-state/`. Final-copy SHA-256: `576d5bf0a35390c381356ed847cccb5670e175b5a051e7f4b2a447846866c578` for `SKILL.md`, `dd93ae657f755edfc2ccb2791e1964e09f86e57c54c7dbf9bc81d0138f457f2b` for the reference. Codex still loaded global user configuration and installed `loom-visualization` 5.9.0, so this was a local skill copy in a normal Codex environment rather than a fully isolated configuration.

The synthetic five-turn user conversation was:

1. 「這是一個虛構的測試專案：我要做每週淨銷售額報表，資料來源有訂單與退款。現在只要記下目標，回覆一句已收到；不要計算或修改檔案。」
2. 「我們已決定用訂單付款日期統計銷售。訂單與退款資料都已匯入，上週訂單總額也核對完成。請只確認收到，暫時不要開始新工作。」
3. 「跨週退款應歸哪一週還沒決定。我現在的限制是：「先不要算淨額，等規則確認。」請記住這個限制，只回覆已收到。」
4. 「補充進度：我們已排除測試訂單，並確認重複訂單以訂單編號去重。退款資料的交易編號欄位已核對，但有 12 筆跨週退款待分類。這些都是虛構測試資料。請只回覆已收到，不要計算或修改檔案。」
5. 「另有一個尚未採納的提議：有人建議把跨週退款算在原訂單週，但我們還沒決定，也沒有核對 12 筆退款的歸屬。等我確認規則後，才計算淨額並整理報表。請只回覆已收到。」

Each setup turn received an acknowledgment. The final tests forked from their shared session `01a14e22-8ef5-76c3-9048-cfe357b73af0`.

| Probe | Request | Trace | Observed result |
|---|---|---|---|
| Empty context, natural language | `我跟丟了。請回顧這段對話原本想做什麼、目前完成什麼、還缺什麼。` | `natural.jsonl` | Read the local `SKILL.md` and reference; said original task unknown, asked for it, and invented no project step. This ran before the final wording edits. |
| Empty context, explicit | `$recap-state` | `explicit.jsonl` | Read the local reference; said no concrete task existed and asked what the user wanted to resume. No `SKILL.md` read command was visible, so the trace alone proves reference use, not host injection of the main file. This ran before the final wording edits. |
| Five-turn context, natural language | `我跟丟了。請回顧原本要做什麼、哪些已決定或完成、哪些仍未知，以及接下來應該先確認什麼。` | `corrected-natural.jsonl`, thread `01a14e36-b294-7c71-babd-bac9863a57c2` | Read both local skill files; used four framed headings, fullwidth-space separators, a table with an immediate situation preface, grounded status, the exact constraint, and a directed final question. |
| Same context, explicit | `$recap-state` | `corrected-explicit.jsonl`, thread `01a14e36-abbe-78b1-9554-26fd80213b4f` | Read the local reference; used four framed headings, fullwidth-space separators, grounded bullets, the exact constraint, and a directed final question. No main-file read command was visible. |

Both final JSONL streams end with `agent_message` followed immediately by `turn.completed`, without a later tool call. The model made no visible file-write call; the CLI's `-o` option did save each final message as a test artifact. All eight final heading frames passed the `ascii-graph` `align.py -` oracle with `✓ no drift`. The CLI does not prove how the chat client renders frames or whitespace, and one observed completion does not guarantee every future completion will follow the layout. Neither final prompt contained a dependency that warranted a relationship diagram; diagram selection remains untested.

Two independent Codex blind auditors checked earlier long-output traces against the synthetic turns. Both found grounded content, the exact consequential quote, and no action after the final question. They found two format problems: one natural-language output omitted frames and one explicit output compressed a complex state into a paragraph. A later run exposed a missing situation sentence before a table. The instructions were clarified; the final two runs below retested the current files. An independent acceptance auditor verified the copied files' hashes and identified a heading-count error and an overclaim about file output in a previous evidence draft; both were corrected here. The focused recap suite returned `20 passed in 0.13s` after the last instruction change.
The complete `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q` command was rerun after that change and exited 0; its first group reported `2256 passed, 2 skipped`. `agy plugin validate ./loom-workflow` processed 13 skills and one hook, and the recap adversarial program reported `7 passed`.

### Final natural-language output (verbatim)

````markdown
每週淨銷售額報表的資料準備已有進展；目前先等你確認跨週退款歸屬哪一週，再處理退款與計算淨額。以下進度來自你在對話中提供的資訊，我尚未核對資料或修改檔案。

```text
┌──────────────────┐
│ ■ 目標與目前位置 │
└──────────────────┘
```

原本的目標是用虛構的訂單與退款資料，製作每週淨銷售額報表。目前停在退款歸屬規則，報表尚未整理。

　

```text
┌────────────────┐
│ ■ 已決定與完成 │
└────────────────┘
```

你回報的決定與進度如下。

| 項目 | 狀態 |
|---|---|
| 銷售統計 | 已決定按訂單付款日期歸週 |
| 訂單處理 | 已排除測試訂單；重複訂單按訂單編號去重 |
| 資料與核對 | 訂單、退款資料已匯入；上週訂單總額及退款交易編號欄位已核對 |

　

```text
┌──────────────┐
│ ■ 未知與限制 │
└──────────────┘
```

跨週退款應歸哪一週仍未決定；「歸在原訂單週」只是尚未採納的提議。另有 **12 筆跨週退款**尚未核對歸屬。你目前的限制是：「先不要算淨額，等規則確認。」

　

```text
┌──────────┐
│ ■ 下一步 │
└──────────┘
```

應先確認跨週退款的歸屬規則，再依規則核對那 12 筆；之後才計算淨額並整理報表。這符合你的方向嗎？
````

### Final explicit-call output (verbatim)

````markdown
```text
┌──────────────────┐
│ ■ 目的與目前位置 │
└──────────────────┘
```

這是虛構的每週淨銷售額報表專案。報表尚未計算；目前等你確認跨週退款歸屬規則。

　

```text
┌────────────────┐
│ ■ 已確認的進度 │
└────────────────┘
```

- 銷售按訂單付款日期統計。
- 訂單與退款資料已匯入；上週訂單總額已核對。
- 測試訂單已排除，重複訂單按訂單編號去重。
- 退款的交易編號欄位已核對；另有 12 筆跨週退款待分類。

　

```text
┌────────────┐
│ ■ 尚未決定 │
└────────────┘
```

「把跨週退款算在原訂單週」只是尚未採納的提議，12 筆退款的歸屬也尚未核對。你目前的限制是：「先不要算淨額，等規則確認。」

　

```text
┌──────────┐
│ ■ 下一步 │
└──────────┘
```

我會先維持等待，不計算或修改檔案；等你確認跨週退款規則後再接續。這符合你的方向嗎？
````
