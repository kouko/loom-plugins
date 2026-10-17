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
