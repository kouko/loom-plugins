# Complex planning and process diagrams — acceptance test evidence

Tried on 2026-10-19 in a clean local clone at `1a4417c7` (`git status --short --branch` printed `## HEAD (no branch)`). Source: `/Users/kouko/GitHub/loom-plugins`; clone: `/private/tmp/loom-acceptance-complex-20261019`. No product files were edited in the clone.

## Setup and presentation boundary

- Project README setup: `loom-workflow/README.md:183-221` describes plugin installation and local validation. Ran `agy plugin validate ./loom-workflow` from the clean clone. Output: `[ok] ./loom-workflow`, `skills: 13 processed`, `hooks: 1 processed`. This verifies the local plugin package; it does not install the package in the user's host or prove a live agent's selection.
- Ran `python3 loom-workflow/skills/loom-visualization/scripts/detect_client.py`. Output: `{"client": "codex", "mermaid": false, "remote_viewer": false, "obsidian_vault": null, "reason": "Codex marker set; Codex Mermaid rendering is unverified"}`. For a file target outside Obsidian, `--target /private/tmp/loom-acceptance-complex-20261019/example.md` reported `obsidian_vault: false` and `mermaid: false`.
- Public guidance: `loom-workflow/skills/loom-visualization/SKILL.md:62-80` routes parallel joins and owned work to the two new templates, and `SKILL.md:82-117` prefers a Markdown table in this host. The spec has no UI flows.

## 1. 工程規劃者能從範例辨認多項任務的前置條件、可並行部分與匯合點，並依範例畫出自己的任務相依關係。

- How I tried it: Selected the task-dependencies row in `SKILL.md`, then read only `templates/12-task-dependencies.md`. Replaced its API/client example with this task plan: A defines data format; B builds an importer; C builds a report; D runs end-to-end verification. B and C both require A; D requires both B and C.
- Adapted table: `A → B`, `A → C`, `B → D`, `C → D`. The two middle tasks have no edge between them, so they may run in parallel. The template says all incoming prerequisites are required, not a conditional choice (`templates/12-task-dependencies.md:5-9,54-61`).
- Adapted ASCII input to `align.py -`:

  ```text
  A: 資料格式
  |
  +--> B: 匯入器 ----+
  |                   |
  +--> C: 報表 ------+--> D: 端對端驗證
  ```

- Captured result: `✓ no drift` (line widths `11, 1, 20, 21, 37`; exit 0). The same four edges can be transcribed to Mermaid as `A --> B`, `A --> C`, `B --> D`, `C --> D`; the supplied example uses exactly this edge structure (`templates/12-task-dependencies.md:44-49`).
- Named checks run directly from the clean clone, without the package suite: `test_task_dependencies_route_and_show_parallel_join` PASS; `test_task_dependencies_do_not_confuse_join_with_choice` PASS.

## 2. 流程設計者能從範例辨認不同角色負責的步驟與交接，並依範例畫出自己的跨角色流程。

- How I tried it: Selected the cross-role-workflow row in `SKILL.md`, then read only `templates/13-cross-role-workflow.md`. Adapted it to customer support collecting an issue, engineering fixing it, and quality assurance checking the fix. The handed-off outputs are an issue record and a repaired version.
- Adapted table:

  | Step | Owner | Work | Next handoff |
  |---|---|---|---|
  | A | 客服 | 收集問題 | 問題紀錄 to 工程 |
  | B | 工程 | 修復問題 | 修復版本 to 品保 |
  | C | 品保 | 驗證修復 | Completed work |

- Adapted ASCII input to `align.py -`:

  ```text
  [客服] A: 收集問題
         |
         | handoff: 問題紀錄
         v
  [工程] B: 修復問題
         |
         | handoff: 修復版本
         v
  [品保] C: 驗證修復
  ```

- Captured result: `✓ no drift` (line widths `18, 8, 26, 8, 18, 8, 26, 8, 18`; exit 0). The template's Mermaid form places each owned step in its owner's subgraph and labels both handoff arrows (`templates/13-cross-role-workflow.md:42-54`). This adapts to three distinct owner lanes with the same two outputs; it was not rendered in a Mermaid host.
- Named checks run directly from the clean clone: `test_cross_role_workflow_routes_owned_steps_and_handoffs` PASS; `test_cross_role_workflow_is_not_message_only_sequence` PASS.

## 3. 新範例在支援的呈現方式中可讀、關係沒有遺漏或誤導，既有圖型範例仍可使用。

- How I tried it: Read the table, ASCII, and Mermaid sections of both new templates and checked their edges and owner changes against the two adapted examples above. Ran the ASCII alignment checker against the supplied task-dependency diagram: `✓ no drift` (line widths `15, 1, 22, 22, 41`; exit 0). The new titles name actions on their own; no bodies repeat them. `references/node-structure.md:26-42` covers the two new shapes.
- Ran these named checks directly through Python's import machinery because this clean clone has no `pytest` installed: `test_shapes_each_have_table_ascii_mermaid`, `test_ascii_blocks_pass_ported_checks`, `test_generator_examples_reproduce_their_output`, and `test_mermaid_flowcharts_use_long_arrows_only`. All printed `PASS`; exit 0. These scan all 13 templates, verify ASCII checks, and reproduce existing generator examples, giving bounded compatibility evidence. The exact invocation was `python3 -c 'import importlib.util; p="loom-workflow/tests/loom-visualization/test_templates.py"; s=importlib.util.spec_from_file_location("template_checks",p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); names=("test_shapes_each_have_table_ascii_mermaid","test_ascii_blocks_pass_ported_checks","test_generator_examples_reproduce_their_output","test_mermaid_flowcharts_use_long_arrows_only","test_task_dependencies_route_and_show_parallel_join","test_task_dependencies_do_not_confuse_join_with_choice","test_cross_role_workflow_routes_owned_steps_and_handoffs","test_cross_role_workflow_is_not_message_only_sequence"); [(getattr(m,n)(), print("PASS",n)) for n in names]'`.
- Mermaid parser check unavailable here: `loom-workflow/tests/mermaid/node_modules` is absent, and no `mmdc` executable was found. `python3 -m pytest --version` returned `No module named pytest`. Attempting only the targeted template test through `UV_CACHE_DIR=/private/tmp/loom-acceptance-uv-cache uv run --offline --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-workflow/tests/loom-visualization/test_templates.py -q` stopped before testing because `execnet==2.1.2` was absent from the offline cache. This is an environment limit, not a test failure. A supported Mermaid host was not available to render the examples.
- The full automated package suite, which runs before acceptance and blocks it on failure, was not run by this tester. Its README command is `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`; the closing-review station will run it during finalization.
