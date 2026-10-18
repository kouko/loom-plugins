# Independent node titles — acceptance test evidence

Tried on 2026-10-16 in a fresh local clone at `87fe724c` (`/private/tmp/loom-title-acceptance-87fe`). `git status --short` was empty before testing. The clone was created with `git clone --no-hardlinks --shared /Users/kouko/GitHub/loom-plugins /private/tmp/loom-title-acceptance-87fe`. No product source was edited in the clone.

## Setup

- Followed the README's local Antigravity validation route: `agy plugin validate ./loom-workflow`.
- Result: `[ok] ./loom-workflow`; `skills: 13 processed`; `hooks: 1 processed`. Validation confirms this checkout loads as a plugin. Installing over the user's existing plugin was unnecessary for these file and CLI criteria.

## 1. 使用者能在圖表指引中找到標題與內文各自應承載什麼資訊的明確判準，且單行節點仍可保留。

- How I tried it: Read `loom-workflow/skills/loom-visualization/references/node-structure.md:26-34` and submitted a plain string alongside a structured node to the documented flow CLI:

  `printf '%s\n' '{"steps":["git pull",{"title":"Run test suites","body":["* unit tests","* integration tests"]}]}' | python3 loom-workflow/skills/loom-visualization/scripts/generate.py flow`

- What came back: The rule says a short title names the action, role, state, or claim without relying on the body. Body detail must differ from title, edges, and adjacent cells; a title-only node has no separator. The CLI returned a `git pull` box with no separator and a `Run test suites` box with a separator and two bullet lines:

  ```text
  ┌─────────────────────┐
  │      git pull       │
  └─────────────────────┘
             │
             ▼
  ┌─────────────────────┐
  │ Run test suites     │
  ├─────────────────────┤
  │ * unit tests        │
  │ * integration tests │
  └─────────────────────┘
  ```

- Evidence: Captured CLI output above; rule at `references/node-structure.md:26-34`.

## 2. 工程規劃與流程設計的相關範例示範可獨立理解的標題；只有需要補充不同資訊的節點才加內文。

- How I tried it: Read the ASCII, Mermaid, and input examples in the six edited templates and checked each body against its title, edge labels, and adjacent cells. The template structure check was run with `pytest -q -p no:cacheprovider loom-workflow/tests/loom-visualization/test_templates.py`.
- What came back: `17 passed in 0.26s`. The linear example uses `Run test suites` with unit/integration types as detail, while the command-only steps stay title-only (`02-linear-steps.md:28-64`). The branching question's body names `inspect CI result`, not the already visible yes/no edges; the downstream actions have no filler (`03-branching-decision.md:28-59`). The reasoning chain removes restatements of the measured 2x latency and the single-query conclusion (`04-reasoning-chain.md:28-77`). The lifecycle keeps state titles and uses actor abilities as body details (`05-state-lifecycle.md:28-53`). The hierarchy describes `skills` as reusable workflows and puts the two skill names in child nodes (`07-hierarchy.md:28-55`). The architecture layer states its input-validation role while Web UI and CLI appear once as component cells (`08-system-architecture.md:29-73`).
- Evidence: Captured pytest result above and the six cited template locations. This is a semantic review of representative examples, not a claim that a parser can judge title quality.

## 3. 更新後的 ASCII 範例通過對齊檢查，Mermaid 範例通過解析檢查；既有節點輸入與輸出行為保持可用。

- How I tried it: Ran the targeted ASCII/example checks above, then targeted generator compatibility tests:

  `pytest -q -p no:cacheprovider loom-workflow/tests/loom-visualization/test_ascii_generators.py::test_all_box_borders_share_one_display_width loom-workflow/tests/loom-visualization/test_ascii_generators.py::test_gen_flow_structured_node_width_budget loom-workflow/tests/loom-visualization/test_ascii_generators.py::test_grandchild_under_last_sibling_uses_space_continuation loom-workflow/tests/loom-visualization/test_ascii_generators.py::test_two_layers_share_outer_width loom-workflow/tests/loom-visualization/test_ascii_cli.py::test_all_generator_shapes_render_aligned loom-workflow/tests/loom-visualization/test_ascii_cli.py::test_converged_flowchart_passes_oracle`

- What came back: `6 passed in 0.16s`. The template suite's `test_ascii_blocks_pass_ported_checks` and `test_generator_examples_reproduce_their_output` also passed as part of its 17 tests. The latter regenerates ASCII from each documented JSON input and compares it with the shown output.
- How I tried Mermaid: From the clean clone, installed the repository's pinned parser dependencies with `npm ci --offline --ignore-scripts --no-audit --no-fund` in `loom-workflow/tests/mermaid` (`added 150 packages`). Then ran `node loom-workflow/tests/mermaid/validate_mermaid.mjs` with the six edited template paths as arguments.
- What came back: The parser printed `OK` for each of `02-linear-steps.md`, `03-branching-decision.md`, `04-reasoning-chain.md`, `05-state-lifecycle.md`, `07-hierarchy.md`, and `08-system-architecture.md`, followed by `6/6 mermaid blocks parsed`.
- How I tried existing inputs: The flow CLI output in section 1 demonstrates a plain string and a structured node in one payload. I also ran:

  `printf '%s\n' '{"node":{"label":"root","children":[{"label":{"title":"skills","body":["* reusable workflows"]},"children":[{"label":"handoff"}]}]}}' | python3 loom-workflow/skills/loom-visualization/scripts/generate.py tree`

- What came back:

  ```text
  root
  └─ skills
     * reusable workflows
     └─ handoff
  ```

- Evidence: Captured outputs above. `git diff 70ebf14..87fe724c -- loom-workflow/skills/loom-visualization/scripts` was empty, confirming the generator scripts did not change in this implementation. The complete package command documented in `README.md` is `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`; it was deliberately left to `finalize-review` as required by the acceptance-tester contract.

## Re-run on 2026-10-16, at `fd93b231`

- Clean setup: Created a new clone with `git clone --no-hardlinks --shared /Users/kouko/GitHub/loom-plugins /private/tmp/loom-title-acceptance-fd93`. `git rev-parse --short HEAD` returned `fd93b231`; `git status --short` was empty. `agy plugin validate ./loom-workflow` again returned `[ok] ./loom-workflow`, `skills: 13 processed`, and `hooks: 1 processed`.
- Fix diff checked: `git diff a4f56ba4..fd93b231 --name-only` returned only `loom-workflow/skills/loom-visualization/references/node-structure.md`. The exact diff changes `Scope A` from “box-drawn nodes” to “box-drawn ASCII nodes” and adds branching decisions, reasoning chains, and state lifecycles; no template, script, test, or diagram text changed.
- 1: re-tested — Read the full title/body rule, width rule, ASCII scope, excluded text slots, and Mermaid counterpart at `references/node-structure.md:26-61`. The rule still requires an independently meaningful action, role, state, or claim as title; body detail must add information absent from title, edges, and adjacent cells; title-only nodes have no separator. Scope now explicitly includes all affected ASCII forms: flow, branching, reasoning, state, architecture, tree, and hierarchy, while excluding edge labels, table/bar cells, and sequence messages. Ran `printf '%s\n' '{"steps":["git pull",{"title":"Run test suites","body":["* unit tests","* integration tests"]}]}' | python3 loom-workflow/skills/loom-visualization/scripts/generate.py flow`. The output again showed `git pull` as a box with no separator, followed by a `Run test suites` box with a separator and two distinct bullet lines. This directly verifies the one-line and structured forms still work at the new HEAD.
- 2: re-tested — Read the complete ASCII, Mermaid, and input sections of `templates/02-linear-steps.md`, `03-branching-decision.md`, `04-reasoning-chain.md`, `05-state-lifecycle.md`, `07-hierarchy.md`, and `08-system-architecture.md` in the new clone. The examples still align with the expanded scope: linear steps use an action title plus test-type detail; branching questions and destination actions have standalone labels, and the one branch body adds the CI inspection source rather than repeating yes/no edges; reasoning nodes state symptoms, causes, or action, with quantitative/implementation detail in bodies; lifecycle states name states and bodies add actor ability, while Mermaid states stay title-only; hierarchy names the category and places members as children; architecture names a layer, adds its input-validation role, and shows its components in adjacent cells. Ran `pytest -q -p no:cacheprovider loom-workflow/tests/loom-visualization/test_templates.py`; result: `17 passed in 0.33s`.
- 3: carried over — The exact fix diff is limited to the scope list in the prose reference. Neither the six ASCII/Mermaid diagrams, their JSON payloads, nor any generator or parser code changed. Thus the previous run's ASCII alignment/example checks, `6/6` Mermaid parses, and plain-string/structured-node CLI outputs still apply. The full package suite remains reserved for `finalize-review`.

## Re-run on 2026-10-18, at `d3ac19a7`

- Clean setup: `git clone --no-hardlinks --shared /Users/kouko/GitHub/loom-plugins /private/tmp/loom-title-acceptance-rebase.JqxxGv/repo` created a new copy. `git rev-parse HEAD` returned `d3ac19a796a3774a279324725ffd677e743a0eac`; `git status --short` was empty. Following the README's local validation route, `agy plugin validate ./loom-workflow` returned `[ok] ./loom-workflow`, `skills: 13 processed`, and `hooks: 1 processed`. No product source was edited in the clone. `git rev-parse HEAD^{tree}` and `git rev-parse d9288a936768b7828e5060d4dbbb575452e8483f^{tree}` both returned `4f51f19d4c2d6998a512e67a9356477986a56217`; the rebase and release-version correction did not change the prior product tree. All three Acceptance lines were nevertheless tried again.
- 1: re-tested — Read the complete rule at `loom-workflow/skills/loom-visualization/references/node-structure.md:26-61`. It assigns an independently meaningful action, role, state, or claim to the short title; body information must be distinct from the title, edges, and adjacent cells. It explicitly keeps title-only nodes without a separator and names the ASCII forms to which the rule applies. Ran `printf '%s\n' '{"steps":["git pull",{"title":"Run test suites","body":["* unit tests","* integration tests"]}]}' | python3 loom-workflow/skills/loom-visualization/scripts/generate.py flow`. Captured output:

  ```text
  ┌─────────────────────┐
  │      git pull       │
  └─────────────────────┘
             │
             ▼
  ┌─────────────────────┐
  │ Run test suites     │
  ├─────────────────────┤
  │ * unit tests        │
  │ * integration tests │
  └─────────────────────┘
  ```

- 2: re-tested — Read the Table, ASCII, Mermaid, and Common mistakes sections of all six edited templates: `02-linear-steps.md`, `03-branching-decision.md`, `04-reasoning-chain.md`, `05-state-lifecycle.md`, `07-hierarchy.md`, and `08-system-architecture.md`. The linear steps have an action title with test types as distinct detail; branching uses standalone questions and actions, and CI source detail rather than duplicate edge answers; reasoning titles state symptoms, causes, or the fix, with measurements and implementation detail below; lifecycle titles name states while bodies give actor abilities; hierarchy's `skills` body states the category's role, while child nodes name its members; architecture's layer body states its input-validation role while component cells show Web UI and CLI. None of these bodies merely repeats its title or adjacent visible text. Ran `pytest -q -p no:cacheprovider loom-workflow/tests/loom-visualization/test_templates.py`; captured result: `17 passed in 0.27s`.
- 3: re-tested — The template suite above includes `test_ascii_blocks_pass_ported_checks` and `test_generator_examples_reproduce_their_output`, which check the documented ASCII blocks and regenerate documented JSON examples. Ran `pytest -q -p no:cacheprovider loom-workflow/tests/loom-visualization/test_ascii_generators.py::test_all_box_borders_share_one_display_width loom-workflow/tests/loom-visualization/test_ascii_generators.py::test_gen_flow_structured_node_width_budget loom-workflow/tests/loom-visualization/test_ascii_generators.py::test_grandchild_under_last_sibling_uses_space_continuation loom-workflow/tests/loom-visualization/test_ascii_generators.py::test_two_layers_share_outer_width loom-workflow/tests/loom-visualization/test_ascii_cli.py::test_all_generator_shapes_render_aligned loom-workflow/tests/loom-visualization/test_ascii_cli.py::test_converged_flowchart_passes_oracle`; captured result: `6 passed in 0.18s`. In `loom-workflow/tests/mermaid`, `npm ci --offline --ignore-scripts --no-audit --no-fund` installed 150 pinned packages. Then `node loom-workflow/tests/mermaid/validate_mermaid.mjs` with the six edited template paths returned `OK` for each template at lines 60, 52, 66, 47, 47, and 61 respectively, ending `6/6 mermaid blocks parsed`. The flow CLI output in row 1 demonstrates plain-string and structured-node input. Also ran `printf '%s\n' '{"node":{"label":"root","children":[{"label":{"title":"skills","body":["* reusable workflows"]},"children":[{"label":"handoff"}]}]}}' | python3 loom-workflow/skills/loom-visualization/scripts/generate.py tree`; captured output:

  ```text
  root
  └─ skills
     * reusable workflows
     └─ handoff
  ```

  The complete package command is `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`; it is reserved for `finalize-review` and was not run here.
