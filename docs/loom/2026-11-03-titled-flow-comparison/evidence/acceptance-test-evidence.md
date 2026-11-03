# Titled before/after flow illustration — acceptance test evidence

Tried on 2026-11-03, in a clean copy of the project at 8d6c1e471cb83dc4958261fd1ad5ccc9bbe39c1a.

The initial execution below tested c5b9abc9d02b9af8bb62bceaa0edfe09265d7ecf. The retained re-run section records the new committed clean snapshot, full Acceptance 4 recheck and explicit carry-over reasons for 1–3.

## Environment and execution

- Independent tester: `/root/release_flow_acceptance`; no implementation or functional source edits.
- Source repository: `/tmp/loom-titled-flow-release`, clean before testing, exact HEAD verified with `git rev-parse HEAD` and `git status --porcelain=v1` (empty).
- Clean copy: `/var/folders/m5/4cb4p8h938qc4qcpdykwz2480000gn/T/loom-flow-acceptance-clean-2avodwg8`, extracted directly from `git archive c5b9abc9d02b9af8bb62bceaa0edfe09265d7ecf`. No pre-existing working files or generated artifacts were included. Python extraction used the standard-library `tarfile` data filter.
- Setup: read the root README, visualization README, SKILL.md and template. The documented local scripts require only Python's standard library. Loaded those scripts from the clean snapshot and executed the documented recipe; no package installation, network, model calls or host plugin installation was required for this documentation artifact.
- Harness: `/tmp/loom-flow-acceptance-check.py`. Command: `python3 /tmp/loom-flow-acceptance-check.py > /tmp/loom-flow-acceptance-output.txt 2>&1`, exit 0.
- The harness extracted the Python body literally between the shell recipe's `<<'PY'` and `PY` delimiters into the clean snapshot's `recipe.py`; no recipe code was changed. It replaced only the documented skill-directory and available-width arguments by invoking Python directly, avoiding a shell heredoc launcher.
- Recipe argv, once for each width: `python3 <clean-copy>/recipe.py <clean-copy>/loom-workflow/skills/loom-visualization 72` and the same with `40`. Both exit 0. Output was saved as `flow-comparison-72.txt` and `flow-comparison-40.txt` in that snapshot.
- Verification argv: `python3 <clean-copy>/loom-workflow/skills/loom-visualization/scripts/align.py <clean-copy>/flow-comparison-72.txt` and the same with `40`. Both exit 0 and print `✓ no drift`; the entire composition, including outer frames, was checked.
- Harness-only corrections: the first trial had an over-broad fence extraction pattern and an incorrect expectation of 18 rather than 17 rows; a subsequent comparison also needed to normalize the Markdown code block's trailing newline. These tester errors were corrected only in the temporary harness. The delivered recipe and all functional files remained unchanged. The final independent run passed all four checks.

Captured final result:

```text
test_labels_proposed_change_is_distinct_from_reported_and_observed ... ok
test_panels_committed_layout_preserves_titles_steps_and_alignment ... ok
test_recipe_parallel_and_stacked_complete_frames_pass_align ... ok
test_release_scoped_diff_retains_tools_contracts_and_other_versions ... ok
Ran 4 tests in 0.048s
OK
```

## 1. 樣板範例以各自的外框包住流程，標題位於圖內，單獨引用時仍能辨識兩側；有對應關係的步驟盡量對齊，不捏造步驟或刪除分支。

- How I tried it: executed the literal saved recipe at width 72; compared its complete output to the committed titled diagram, ignoring only the final newline. Checked both outer frame corners, the title row and the row position of every step pair. Read the instructions concerning unequal topology and branching.
- What came back: exact diagram match; two closed outer frames; both titles inside row 2; corresponding step pairs on rows 5, 10 and 15. Each row is 62 display cells wide. No branches are represented by this linear example; the text explicitly prohibits inventing steps, removing branches or forcing equal topology and directs branching interiors to the branching template.
- Evidence: `test_panels_committed_layout_preserves_titles_steps_and_alignment`; committed template section `Before/after flows in titled panels`; captured output above and below.

```text
A1: two complete titled frames; all three corresponding step pairs share rows; no fabricated branch example.
```

## 2. 文件區分使用者回報、已觀察行為及尚未完成的預期結果，示例以「預期修改後」標示未驗證的改變。

- How I tried it: inspected the rendered title row and the paragraph immediately introducing the saved example; checked that the example was not claimed as an implemented or verified result.
- What came back: the reproduced titles are `修改前（使用者回報）` and `預期修改後`. The guidance reserves Before/After states for supporting evidence, distinguishes a user's report from observed behavior, and calls the illustrated correction requested rather than implemented or verified.
- Evidence: `test_labels_proposed_change_is_distinct_from_reported_and_observed`; the executed diagram and template introductory paragraph.

```text
A2: reported-before and expected-after labels reproduced; prose reserves observed states for supporting evidence.
```

## 3. 文件的重現方式可產生並排與上下排列的完整外框圖；並排輸出與範例一致，兩種排列均通過既有對齊檢查。

- How I tried it: executed the unchanged Python recipe from the committed Markdown in a clean snapshot, at widths 72 and 40. Ran the existing alignment CLI on both complete output files. Checked the wide output against the saved example and split the narrow output at its blank separator to inspect both complete panels.
- What came back: width 72 produced the exact saved side-by-side illustration, 17 rows by 62 cells. Width 40 produced two complete 17-row by 30-cell panels separated by one blank line, retaining their titles. Both alignment commands returned 0 and `✓ no drift`.
- Evidence: `test_recipe_parallel_and_stacked_complete_frames_pass_align`; captured generator and alignment results:

```text
RECIPE width=72 exit=0
ALIGN width=72 exit=0
all 17 lines: width 62
✓ no drift
RECIPE width=40 exit=0
ALIGN width=40 exit=0
lines 1-17 and 19-35: width 30; line 18: width 0
✓ no drift
A3: width 72 -> 17 lines x 62 cells; width 40 -> two 17-line x 30-cell panels; both complete compositions align exit 0.
```

## 4. 釋出只包含共用圖表樣板、選用提示及必要版本資訊，不修改需求確認契約、其他插件版本、產圖工具或其依賴。

- How I tried it: executed `git diff --name-only ae4f92e4629bf19b16784ee0f798047b99626499 c5b9abc9d02b9af8bb62bceaa0edfe09265d7ecf`; checked the exact set against the authorized visualization documents, release metadata and intent/plan records. Parsed all four workflow manifests from the clean copy; byte-compared the design/code source manifests to baseline. Compared the full visualization SKILL.md against baseline with only the one expected routing phrase changed; checked changelog and all affected README versions.
- What came back: exactly 13 paths below; all four workflow manifests read `5.19.2`; affected READMEs and changelog agree. Other plugin manifests are byte-identical to baseline. No confirmation contract, renderer, generator script or dependency file is in the diff.
- Evidence: `test_release_scoped_diff_retains_tools_contracts_and_other_versions` and captured changed-path list:

```text
README.md
docs/loom/2026-11-03-titled-flow-comparison/plan.md
docs/loom/intent/2026-11-03-titled-flow-comparison.md
loom-workflow/.claude-plugin/plugin.json
loom-workflow/.codex-plugin/plugin.json
loom-workflow/CHANGELOG.md
loom-workflow/README.ja.md
loom-workflow/README.md
loom-workflow/README.zh-TW.md
loom-workflow/package.json
loom-workflow/plugin.json
loom-workflow/skills/loom-visualization/SKILL.md
loom-workflow/skills/loom-visualization/templates/02-linear-steps.md
A4: 13 authorized paths only; all four workflow manifests 5.19.2; other plugin manifests byte-identical; no renderer/dependency/confirmation-contract changes.
```

## Initial structured probe results (superseded for Acceptance 4 by the re-run below)

```json
{
  "tested_commit": "c5b9abc9d02b9af8bb62bceaa0edfe09265d7ecf",
  "baseline": "ae4f92e4629bf19b16784ee0f798047b99626499",
  "command": "python3 /tmp/loom-flow-acceptance-check.py",
  "exit_code": 0,
  "probes": [
    {"acceptance": 1, "name": "test_panels_committed_layout_preserves_titles_steps_and_alignment", "result": "works"},
    {"acceptance": 2, "name": "test_labels_proposed_change_is_distinct_from_reported_and_observed", "result": "works"},
    {"acceptance": 3, "name": "test_recipe_parallel_and_stacked_complete_frames_pass_align", "result": "works"},
    {"acceptance": 4, "name": "test_release_scoped_diff_retains_tools_contracts_and_other_versions", "result": "works"}
  ]
}
```

## Limits and remaining release verification

- These are local clean-snapshot checks of the saved recipe, document semantics and committed change scope. They do not prove improved human understanding, automatic selection by a future coding agent, typography in every host, or installed-plugin behavior.
- No specification UI flows apply (`kind: engineering`, `needs-design: no`). The initial run carried over no lines; the retained re-run below carries over 1–3. No important-or-worse dismissed findings were supplied. No instructed skips occur in the committed intent or plan.
- The independent tester did not run or claim the full package suite. The project-declared command is `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`; the station runs the complete Build suite and `finalize-review` runs it again before acceptance, blocking on failure. Those results are separate from this report.
- The scope check covers the tested committed HEAD; this report and its evidence are subsequently added as review records. No source repair was made during acceptance testing.

## Re-run on 2026-11-03, at 8d6c1e471cb83dc4958261fd1ad5ccc9bbe39c1a

- Fix range inspected: `git diff c5b9abc9d02b9af8bb62bceaa0edfe09265d7ecf 8d6c1e471cb83dc4958261fd1ad5ccc9bbe39c1a`. Exactly two paths changed: the plan names the existing release test and records the prior red/green result; `loom-workflow/tests/scripts/test_release_metadata.py` changes only `CURRENT = "5.19.1"` to `CURRENT = "5.19.2"`. No assertion, test function, dependency or runtime code was added, removed or weakened.
- New clean snapshot: `/var/folders/m5/4cb4p8h938qc4qcpdykwz2480000gn/T/loom-flow-acceptance-recheck-5bhvuv8d`, freshly extracted from `git archive 8d6c1e471cb83dc4958261fd1ad5ccc9bbe39c1a`.
- 1: carried over — the complete fix diff changes only the plan and existing version-test expectation; the diagram, three step pairs, outer frames and preservation guidance are byte-unchanged.
- 2: carried over — the complete fix diff leaves the reported/observed/expected guidance, title labels and example unchanged.
- 3: carried over — the complete fix diff leaves the recipe, saved output, renderer, width helper and alignment checker unchanged; both previously tested layouts remain the same content.
- 4: re-tested — ran the full Acceptance 4 scope/version probe against the new clean snapshot, including every previously checked surface, the newly included existing release-test file and the exact repair diff; then ran that existing test module using the project's locked dependencies.

### Complete current scope inventory

The baseline-to-new-HEAD inventory is now **14 paths**, comprising all 13 initially listed paths plus `loom-workflow/tests/scripts/test_release_metadata.py`. The initial 13-path result above remains historical evidence for the original SHA only. The current authorized set is:

```text
README.md
docs/loom/2026-11-03-titled-flow-comparison/plan.md
docs/loom/intent/2026-11-03-titled-flow-comparison.md
loom-workflow/.claude-plugin/plugin.json
loom-workflow/.codex-plugin/plugin.json
loom-workflow/CHANGELOG.md
loom-workflow/README.ja.md
loom-workflow/README.md
loom-workflow/README.zh-TW.md
loom-workflow/package.json
loom-workflow/plugin.json
loom-workflow/skills/loom-visualization/SKILL.md
loom-workflow/skills/loom-visualization/templates/02-linear-steps.md
loom-workflow/tests/scripts/test_release_metadata.py
```

Commands and captured results:

```text
python3 /tmp/loom-flow-acceptance-recheck.py
test_release_scoped_diff_retains_tools_contracts_and_other_versions ... ok
Ran 1 test in 0.179s
OK
A4: all 14 authorized paths checked; four manifests, four READMEs and changelog agree; other plugins/tools/contracts unchanged; existing release-test update is precisely CURRENT 5.19.1 -> 5.19.2 with no check weakening.

# From the fresh snapshot:
uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-workflow/tests/scripts/test_release_metadata.py -q
..............                                                           [100%]
14 passed in 0.02s
```

Both commands exited 0. The locked test invocation initially could not create a temporary lock file in the host uv cache under the sandbox; the same command was then approved through the host permission tool and completed successfully. This is the existing release module alone, not the full package suite. No claim is made about the separately scheduled full suite or finalization results.

```json
{
  "tested_commit": "8d6c1e471cb83dc4958261fd1ad5ccc9bbe39c1a",
  "baseline": "ae4f92e4629bf19b16784ee0f798047b99626499",
  "probes": [
    {"acceptance": 1, "name": "test_panels_committed_layout_preserves_titles_steps_and_alignment", "result": "works", "execution": "carried over", "tested_commit": "c5b9abc9d02b9af8bb62bceaa0edfe09265d7ecf", "reason": "Diagram and preservation guidance unchanged in inspected fix diff"},
    {"acceptance": 2, "name": "test_labels_proposed_change_is_distinct_from_reported_and_observed", "result": "works", "execution": "carried over", "tested_commit": "c5b9abc9d02b9af8bb62bceaa0edfe09265d7ecf", "reason": "Status guidance and titles unchanged in inspected fix diff"},
    {"acceptance": 3, "name": "test_recipe_parallel_and_stacked_complete_frames_pass_align", "result": "works", "execution": "carried over", "tested_commit": "c5b9abc9d02b9af8bb62bceaa0edfe09265d7ecf", "reason": "Recipe, output and toolchain unchanged in inspected fix diff"},
    {"acceptance": 4, "name": "test_release_scoped_diff_retains_tools_contracts_and_other_versions", "result": "works", "execution": "re-tested", "command": "python3 /tmp/loom-flow-acceptance-recheck.py", "exit_code": 0, "existing_release_tests_passed": 14}
  ]
}
```
