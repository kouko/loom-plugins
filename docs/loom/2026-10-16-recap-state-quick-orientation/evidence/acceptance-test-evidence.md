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
