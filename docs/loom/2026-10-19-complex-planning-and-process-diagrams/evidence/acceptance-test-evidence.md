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
- Ran these named checks directly through Python's import machinery because this clean clone has no `pytest` installed: `test_shapes_each_have_table_ascii_mermaid`, `test_ascii_blocks_pass_ported_checks`, `test_generator_examples_reproduce_their_output`, and `test_mermaid_flowcharts_use_long_arrows_only`. All printed `PASS`; exit 0. The template inventory covered all 13 templates, but this version of `test_ascii_blocks_pass_ported_checks` skipped the two new unboxed diagrams because it filtered for box-drawing glyphs. The generator test reproduced examples only for shapes that have a generator. This was narrower evidence than the first report implied. The exact invocation was `python3 -c 'import importlib.util; p="loom-workflow/tests/loom-visualization/test_templates.py"; s=importlib.util.spec_from_file_location("template_checks",p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); names=("test_shapes_each_have_table_ascii_mermaid","test_ascii_blocks_pass_ported_checks","test_generator_examples_reproduce_their_output","test_mermaid_flowcharts_use_long_arrows_only","test_task_dependencies_route_and_show_parallel_join","test_task_dependencies_do_not_confuse_join_with_choice","test_cross_role_workflow_routes_owned_steps_and_handoffs","test_cross_role_workflow_is_not_message_only_sequence"); [(getattr(m,n)(), print("PASS",n)) for n in names]'`.
- Mermaid parser check unavailable here: `loom-workflow/tests/mermaid/node_modules` is absent, and no `mmdc` executable was found. `python3 -m pytest --version` returned `No module named pytest`. Attempting only the targeted template test through `UV_CACHE_DIR=/private/tmp/loom-acceptance-uv-cache uv run --offline --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-workflow/tests/loom-visualization/test_templates.py -q` stopped before testing because `execnet==2.1.2` was absent from the offline cache. This is an environment limit, not a test failure. A supported Mermaid host was not available to render the examples.
- The full automated package suite, which runs before acceptance and blocks it on failure, was not run by this tester. Its README command is `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`; the closing-review station will run it during finalization.

## Re-run on 2026-10-19, at `6e38b533`

- Clean-copy setup: Cloned the repository anew to `/private/tmp/loom-acceptance-complex-rerun-20261019`, checked out `6e38b5334cde651eecbb76f56ef8997b33765a7f`, and confirmed `git status --short --branch` printed `## HEAD (no branch)`. `agy plugin validate ./loom-workflow` again returned `[ok]`, `skills: 13 processed`, and `hooks: 1 processed`. `detect_client.py` again reported `client: codex`, `mermaid: false`.
- Fix scope checked against `git diff 00811eb9..6e38b533`: only `loom-workflow/tests/loom-visualization/test_templates.py` changed. It now includes the two unboxed ASCII blocks in its structural test, asserts their supplied connectors occupy equal display columns, and checks the Mermaid owner subgraphs and handoff labels explicitly. Since the shared test covers all three criteria, rows 1, 2 and 3 were re-tested in full; none was carried over.
- 1: Selected the task-dependencies route and reread only its template. The template's table still has `A→B`, `A→C`, `B→D`, `C→D`; its Mermaid block has the same four edges; its text says both B and C are needed at the join. Adapted the same data-format/importer/report/verification task plan. The first attempted ASCII diagram was:

  ```text
  A: 資料格式
  |
  +--> B: 匯入器 ----+
  |                   |
  +--> C: 報表 ------+--> D: 端對端驗證
  ```

  `printf '%s\n' 'A: 資料格式' '|' '+--> B: 匯入器 ----+' '|                   |' '+--> C: 報表 ------+--> D: 端對端驗證' | python3 loom-workflow/skills/loom-visualization/scripts/align.py -` printed line widths `11, 1, 20, 21, 37` and `✓ no drift` (exit 0). Yet `display_width()` measured the B endpoint, vertical segment, and C endpoint at columns `[19, 20, 19]` (zero-based). Thus the join is visibly broken although the user-facing verifier passes. This is an important finding at `loom-workflow/skills/loom-visualization/scripts/align.py` and the template's instruction to use it. Correcting my attempted diagram to B `-----+` and C `-------+` yielded widths `11, 1, 21, 21, 38`, `✓ no drift`, and independently measured join columns `[20, 20, 20]`. The criterion is partly met: an accurate diagram can be made, but the instructed check did not reject the first inaccurate one.
- 2: Selected the cross-role route and reread only its template. Its table names the Product, Design and Engineering owners and the two outputs; its ASCII brackets name each owner; its Mermaid subgraphs and arrows carry the same work and handoffs. Re-adapted the customer-support/engineering/quality-assurance example from the first run, including the issue record and repaired version. `align.py -` again printed widths `18, 8, 26, 8, 18, 8, 26, 8, 18` and `✓ no drift` (exit 0); the handoff marks are all in display column 7. The workflow is readable across the three forms, though this host cannot render Mermaid.
- 3: Reran `align.py -` on both supplied new ASCII examples. The task-dependency example returned widths `15, 1, 22, 22, 41` and `✓ no drift`; the cross-role example returned `18, 8, 26, 8, 18, 8, 24, 8, 18` and `✓ no drift`. Reran eight focused Python checks with the exact `python3 -c` invocation above; all eight again printed `PASS`. In the fixed test source, the template inventory still checks all 13 template files; the ASCII check now passes all fenced ASCII examples except the sequence generator's specially exempt output, and adds display-column assertions specifically for the two new unboxed examples. Existing generator examples still reproduce their output. These checks do not validate arbitrary user adaptations; the failed input in row 1 demonstrates that boundary. A Mermaid parser package and a supported Mermaid-rendering host remained unavailable, so visual rendering is still unverified. The tester did not run the full package suite; finalization will run the README command recorded above and block acceptance if it fails.

## Re-run on 2026-10-19, at `5642b658`

- Clean-copy setup: Cloned the repository anew to `/private/tmp/loom-acceptance-complex-rerun2-20261019`, checked out `5642b658facbf1c2565b54fe12293c7bca48e7dd`, and confirmed `git status --short --branch` printed `## HEAD (no branch)`. `agy plugin validate ./loom-workflow` returned `[ok]`, `skills: 13 processed`, and `hooks: 1 processed`. `detect_client.py` reported `client: codex`, `mermaid: false`.
- Fix scope checked against `git diff 43cbb95c..5642b658`: only `scripts/checks_kink.py` and `tests/loom-visualization/test_ascii_cli.py` changed. The shared alignment verifier affects both new shapes, so rows 1, 2 and 3 were re-tested in full; none was carried over.
- 1: Reselected task dependencies using the public shape table and reread its table, ASCII, Mermaid and mistakes sections. Its table and Mermaid still contain the four required edges `A→B`, `A→C`, `B→D`, `C→D`; the text says D needs both B and C, not one selected branch. Reused the exact failed input from the prior run:

  ```text
  A: 資料格式
  |
  +--> B: 匯入器 ----+
  |                   |
  +--> C: 報表 ------+--> D: 端對端驗證
  ```

  With the same `printf '%s\n' ... | python3 loom-workflow/skills/loom-visualization/scripts/align.py -` invocation recorded above, the command now exits 1 and prints `line 4: col 20: seam kink: unboxed join drifts across cols (19, 20, 19)`. The full width report is `11, 1, 20, 21, 37`. For the corrected adaptation, B ends `-----+` and C ends `-------+--> D`; its join columns are `[20, 20, 20]`, width report `11, 1, 21, 21, 38`, `✓ no drift`, exit 0. The user can distinguish parallel tasks and obtain a correctly joined diagram through the instructed verifier.
- 2: Reselected cross-role workflow and reread its table, ASCII, Mermaid and mistakes sections. Its owned steps and handoff outputs still agree across forms. Re-adapted the customer-support/engineering/quality-assurance process from the first run. The correct nine-line ASCII input recorded above returned widths `18, 8, 26, 8, 18, 8, 26, 8, 18`, `✓ no drift`, exit 0. Deliberately shifted the first handoff arrow one display column to the right (`        v` instead of `       v`); the same verifier exited 1 and printed `line 4: col 8: seam kink: unboxed handoff drifts across cols (7, 7, 8)`. The rest of the workflow remained unchanged. This checks owner changes and the output passed between roles without substituting a message-only sequence.
- 3: Reran the verifier on both supplied new ASCII examples. The task-dependency example returned widths `15, 1, 22, 22, 41`, `✓ no drift`, exit 0. The cross-role example returned `18, 8, 26, 8, 18, 8, 24, 8, 18`, `✓ no drift`, exit 0. Ran the same eight focused template checks using the exact `python3 -c` command above; all eight printed `PASS`. Ran two new focused CLI checks directly through Python import (`test_subprocess_stdin_unboxed_join_alignment` and `test_subprocess_stdin_unboxed_handoff_alignment`); both printed `PASS`. These verify the captured wrong and corrected inputs. The all-template inventory and generator reproduction checks passed again, which is bounded compatibility evidence for existing shapes. A supported Mermaid-rendering host was unavailable; source and structure checks do not prove visual rendering. The tester did not run the full package suite. The README command recorded above remains the finalization check that blocks acceptance if it fails.
- Exact focused CLI check invocation: `python3 -c 'import importlib.util; p="loom-workflow/tests/loom-visualization/test_ascii_cli.py"; s=importlib.util.spec_from_file_location("ascii_cli_checks",p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); names=("test_subprocess_stdin_unboxed_join_alignment","test_subprocess_stdin_unboxed_handoff_alignment"); [(getattr(m,n)(), print("PASS",n)) for n in names]'`. Output: `PASS test_subprocess_stdin_unboxed_join_alignment` and `PASS test_subprocess_stdin_unboxed_handoff_alignment`; exit 0.
