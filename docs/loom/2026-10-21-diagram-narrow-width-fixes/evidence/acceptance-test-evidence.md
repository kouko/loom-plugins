# Fix the layered-architecture diagram's narrow-width hang and title overflow — acceptance test evidence

Tried on 2026-10-21, in a clean copy of the project at 155f92bc (detached
`git worktree add`), compared with a second clean copy of trunk at 114ad1ce
(origin/main, unchanged at test time).

## Setup

- The skill's documented entry point (SKILL.md Step 4) is
  `printf '%s' '<json>' | python3 <skill-dir>/scripts/generate.py <shape>`,
  verified with `python3 <skill-dir>/scripts/align.py -`. The scripts need only
  the Python standard library; nothing to install. Both commands ran in the
  clean copy without any setup step. Setup check: passed.
- Every diagram below went through `generate.py` and `align.py` exactly as a
  user or agent following SKILL.md would; `<G>` = `loom-workflow/skills/loom-visualization/scripts`.
- Trunk runs were wrapped in `timeout 5`; exit 124 means the timeout killed it.

## 1. Drawing a layered-architecture diagram whose body holds a two-cell character, at the narrowest width budgets, finishes within a few seconds and produces a box whose borders line up.

- How I tried it: `generate.py arch` with
  `{"layers":[{"name":{"title":"A","body":["中"]},"components":[""]}],"width":W}`
  for W = 0, 1, 2, 3, 4; then the multi-line string name `"A\n中"` at width 1;
  `{"title":"A","body":["中"]}` with component `x` at width 1; a two-layer
  diagram (`{"title":"A","body":["中文字"]}`, `"Web\n中"`) at width 1;
  `"API\n中"` at width 1; `{"title":"服務","body":["中","日本語"]}` at width 2.
- What came back (HEAD): every run exit 0 in 0 s (whole seconds). All box lines are 5 cells wide:
  ```
  ┌───┐
  │ A │
  ├───┤
  │ 中│
  ├───┤
  │   │
  └───┘
  ```
  align.py reports every line width 5 (no seam drift). For the inputs with
  an empty component `""` it adds one structural note,
  `line 5: col 0: separator row with no content line after it before box's bottom border`;
  trunk prints the same note for the same structure with an ASCII body at a
  wide budget (`{"title":"A","body":["b"]},"components":[""]`, width 20), so it
  comes from the empty component, not from this change. Every input with
  a non-empty component: `✓ no drift`.
- Trunk: the dict-name and `"A\n中"` inputs with an empty component exit 124 (hang) at every
  W tried; the inputs with wider components finish on trunk too.
- The flow generator was also tried at the adversary's case:
  `{"steps":[{"title":"","body":["中"]}],"width":0}` and `{"steps":["\n中文"],"width":-1}`
  — HEAD finishes, every line 5 cells (align.py only notes the empty title
  row, as expected for an empty title); trunk exits 124. Flow with a non-empty
  title at width 0, 1, -3 is byte-identical to trunk.
- Evidence: the outputs above; named tests
  `test_arch_cjk_body_at_narrowest_width_is_aligned`,
  `test_arch_multiline_string_name_cjk_body_at_width_1_is_aligned`,
  `test_flow_cjk_body_width_0_aligned`,
  `test_flow_multiline_string_cjk_body_width_0_aligned` passed.

## 2. Wrapping text containing two-cell characters at a one-cell width finishes instead of looping.

- How I tried it: imported the wrap helper from each clean copy and called
  `wrap_label(text, 1)` under `timeout 5`.
- What came back:

  | Call | HEAD | trunk |
  |---|---|---|
  | `wrap_label('中文', 1)` | `['中', '文']` | exit 124 after 5 s |
  | `wrap_label('a中b文', 1)` | `['a', '中', 'b', '文']` | exit 124 after 5 s |
  | `wrap_label('日本語テキスト', 1)` | one char per line, 7 lines | (hangs, same path) |
  | `wrap_label('abc', 1)` | `['a', 'b', 'c']` | `['a', 'b', 'c']` |
  | `wrap_label('中', 0)` | `ValueError: max_width must be positive` | same |

- Evidence: the table above; named tests `test_wrap_label_cjk_at_width_1_returns`,
  `test_wrap_label_ascii_at_width_1_unchanged` passed. Fix at
  `loom-workflow/skills/loom-visualization/scripts/width.py:101-104` (take one
  character when none fits).

## 3. A layered-architecture diagram whose layer title is wider than everything else in the layer shows the whole title inside a box whose borders line up.

- How I tried it: `generate.py arch` on HEAD and trunk with
  (a) `{"title":"Presentation Layer","body":["ui"]}`, components `web`,`cli`;
  (b) string name `"使用者介面層\nui"`, component `a`;
  (c) `{"title":"資料存取層 Data","body":["db"]}` + a second layer `API`;
  (d) case (a) with `"width":8`.
- What came back: HEAD, all four `✓ no drift`, e.g.
  ```
  ┌───────────────────┐
  │ Presentation Layer│
  ├───────────────────┤
  │ ui                │
  ├─────────┬─────────┤
  │ web     │ cli     │
  └─────────┴─────────┘
  ```
  Trunk, all four drift by one cell, e.g. `line 2: col 20: table line display width 21 differs from block width 20`
  and `line 2: col 14: table line display width 15 differs from block width 14`.
  On HEAD the title's last character touches the right border (no trailing
  space). In (c) the other layer's box grows by one cell with it, as it must
  to keep the shared width.
- Evidence: outputs above; named tests `test_arch_dict_name_long_title_is_aligned`,
  `test_arch_multiline_string_name_long_title_is_aligned` passed.

## 4. For inputs that hit neither defect, every diagram generator's output and error messages are byte-identical to trunk before this change.

- How I tried it: a comparison script (scratchpad, not committed) ran
  `generate.py <shape>` on both clean copies for 30 hand-picked inputs across
  all six shapes (table, flow, tree, bar, arch, seq) — including every error
  path I could reach (empty body for flow/tree/arch, `max_width must be
  positive`, mismatched table row, unknown seq participant, missing arch
  `components`) and the three known pre-existing behaviours — plus 300 seeded
  random arch/flow inputs (seed 20261021; ASCII and CJK labels, dict /
  multi-line / single-line names, width None or 1–20). It compared exit code,
  stdout and stderr (stderr with the copy's directory name normalised). An input
  counted as a defect input when trunk hung or drew arch lines of unequal width.
- What came back:
  `{'identical': 319, 'defect_hang': 0, 'defect_misaligned': 10, 'DIFF': 1}`.
  All 10 defect inputs are aligned on HEAD (the script printed no "still
  misaligned"). The one DIFF is the unhandled Python traceback for an arch
  layer missing its `components` key: the exception and message
  (`KeyError: 'components'`) are identical; only two `gen_arch.py` line numbers
  in the traceback moved (107→123, 108→124) because code was inserted above.
  This is an uncaught crash dump on malformed input, not one of the
  generator's error messages.
- Known pre-existing behaviours, byte-identical to trunk in this run:
  `{"title":"T","body":["abcdefghij"]}` at width 10 (wraps one cell early);
  empty single-line name `""`; empty-title one-cell body with no components at
  width 1 → `generate.py arch: max_width must be positive`.
- Evidence: script output above; named tests
  `test_arch_single_line_string_name_long_title_unchanged`,
  `test_arch_empty_title_one_cell_body_keeps_trunk_error` passed.

## 5. The complete package suite passes.

- How I tried it: per the acceptance-tester contract I did not run the full
  suite. I ran the change's own test modules in the clean copy:
  `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest -q -p no:cacheprovider loom-workflow/tests/loom-visualization loom-workflow/tests/scripts/test_release_metadata.py`
- What came back: `237 passed, 5 skipped in 0.84s`. The 10 new tests
  (filtered run): `12 passed, 216 deselected`.
- Version check: HEAD carries 5.12.2 in all four loom-workflow manifests;
  origin/main is still 114ad1ce at 5.12.1, so no collision.
- Full-suite command, run by finalize-review, which refuses the attestation
  on failure:
  `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`
  (run with `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID`).
