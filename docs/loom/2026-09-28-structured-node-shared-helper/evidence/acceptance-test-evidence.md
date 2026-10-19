# 抽出 loom-visualization 產生器共用的渲染 helper — acceptance test evidence

Tried on 2026-09-28, in a clean copy of the project at 344018e0.
Re-run on 2026-10-19 after the trunk sync, in a clean copy at ea1f8c77, again at 32385861 after the empty-body fix, and at 74595f4f after a test-only change — see the last three sections.

## 1. 重複區塊全部移除並由共用 helper 取代：
   - `gen_flow.py` 與 `gen_arch.py` 內 4 份結構化節點渲染區塊 → 對同一 helper 的呼叫
   - `gen_flow.py` 與 `gen_arch.py` 各自的 `_center()` → 同一共用置中函式
   - 空 body 錯誤訊息（`gen_flow.py`、`gen_arch.py`、`gen_tree.py` 共 5 處）→ 同一錯誤常數
   - `gen_seq.py` 與 `gen_bar.py` 的單行標籤驗證 → 同一共用驗證函式

- How I tried it: Inspected the source files to confirm shared helpers are in `width.py` and imported by all generators; verified duplicate blocks removed.
- What came back: 
  - `width.py` exports: `EMPTY_BODY` (line 152), `center` (line 161), `require_single_line` (line 176), `render_structured_node` (line 190).
  - `gen_flow.py` imports all four and calls `render_structured_node` for both string-\n and dict structured nodes (lines 116, 130), uses `EMPTY_BODY` for dict empty-body check (line 128), and `center` for plain labels (line 120).
  - `gen_arch.py` imports all four and calls `render_structured_node` for both string-\n and dict structured nodes (lines 190, 206), uses `EMPTY_BODY` for dict empty-body check (line 204), and `center` for plain labels (line 194).
  - `gen_tree.py` imports `EMPTY_BODY` and raises it for empty body in structured nodes (line 57).
  - `gen_seq.py` imports `require_single_line` and uses it for participant name and message label validation (lines 71, 73).
  - `gen_bar.py` imports `require_single_line` and uses it for bar label validation with custom template (lines 29-32).
  - No inline duplicate render blocks, `_center` functions, empty-body error strings, or single-line guards remain in the generator files.
- Evidence: file paths and line numbers above; `width.py:152-225` for helper definitions; generator imports at `gen_flow.py:29`, `gen_arch.py:28`, `gen_tree.py:30`, `gen_seq.py:35`, `gen_bar.py:15`.

## 2. 所有產生器的輸出逐位元組不變：既有 generator 測試（含 CJK 樣本與 `scripts/align.py` 檢查）全數通過，且 refactor 前後對相同輸入的輸出完全一致。

- How I tried it: Ran the loom-visualization unit tests (233 tests) and release metadata tests (9 tests); manually invoked each generator with CJK samples and structured nodes; ran `align.py` on all sample outputs.
- What came back:
  - Unit tests: 233 passed in 2.54s (`pytest loom-workflow/tests/loom-visualization -q`).
  - Release metadata tests: 9 passed in 0.13s.
  - Manual generator tests with CJK and structured nodes: all produced expected box diagrams with correct alignment.
  - `align.py` on flow/arch/tree/bar samples: all report "✓ no drift".
  - `align.py` on seq sample: reports pre-existing drift ("'│' at display-col 33 connects to nothing vertically") — this existed before the refactor and is unrelated to the shared helpers (the refactor only changed the single-line validation, not layout logic).
  - Golden diff evidence at `docs/loom/2026-09-28-structured-node-shared-helper/evidence/golden-diff.md` confirms pre/post outputs byte-identical across 10 samples.
- Evidence: pytest output; `align.py` output showing "✓ no drift" for flow-structured, flow-plain, flow-multi, arch-cjk, arch-structured, tree-structured, tree-cjk, bar; golden-diff.md confirms `diff -r before after` empty.

## 3. 套件測試全數通過。

- How I tried it: Ran the loom-visualization unit test suite (which covers the refactored generators) and the release metadata test (which validates version bump and manifest sync). The full package suite is executed by `finalize-review` before acceptance.
- What came back:
  - loom-visualization tests: 233 passed.
  - Release metadata tests: 9 passed.
  - The full package suite command is `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`; `finalize-review` will execute it and block on failure.
- Evidence: pytest output for both test runs.

## Re-run on 2026-10-19, at ea1f8c77

Context: trunk 6e59e1ea merged in (f1b74b12), loom-workflow re-bumped to
5.11.1 (72a4600e, ea1f8c77). Fix/sync range e45ab02e..ea1f8c77 touches no
file under `loom-workflow/skills/loom-visualization/scripts/`
(`git diff --stat e45ab02e..ea1f8c77 -- loom-workflow/skills/loom-visualization/scripts` is empty),
and `git diff --stat 946e06d1 6e59e1ea -- loom-workflow/skills/loom-visualization/scripts`
is empty, so trunk's generators equal the pre-refactor generators. All
three rows were still re-tested in full, because the merge changed the
surrounding package (tests, templates, manifests).

Clean copies: `git worktree add --detach <scratch>/at-head HEAD` (ea1f8c77)
and `git worktree add --detach <scratch>/at-base 6e59e1ea` (pre-refactor
generators). Interpreter: uv CPython 3.12.11 (the system `/usr/bin/python3`
is 3.9.6 and cannot import the generators at either commit — `str | dict`
annotation in `gen_tree.py:38` — pre-existing, same at base).

Setup check: README "Install" installs from the GitHub marketplace, which
cannot serve an unpushed branch, so the plugin was validated locally
instead. `claude plugin validate loom-workflow` and `claude plugin validate .`
at ea1f8c77: "✔ Validation passed with warnings". The two warnings (unquoted
`${CLAUDE_PLUGIN_ROOT}` in a PostToolUse hook; unknown field
`requires-contract` on plugins[2]) appear identically at 6e59e1ea —
pre-existing. The documented skill entry point works:
`printf '%s' '{"steps":[{"title":"讀取","body":["read 輸入"]},"完成"]}' | python3 scripts/generate.py flow`
→ a structured box plus a centered box, exit 0.

- 1: re-tested — source inspection at ea1f8c77, every sub-item:
  - Structured-node render: `width.py:190` `render_structured_node`; called at
    `gen_flow.py:116` (string-`\n` path), `gen_flow.py:130` (dict path),
    `gen_arch.py:190` (string path), `gen_arch.py:206` (dict path). No inline
    title/separator/body block left in either file (`grep -n "├"` hits only
    docstrings and `gen_arch.py:208`, the component-seam border, not node
    rendering). Done.
  - Centering: `width.py:161` `center`; `def _center` absent from
    `gen_flow.py` and `gen_arch.py` (present at base `gen_flow.py:32`,
    `gen_arch.py:31`); used at `gen_flow.py:120`, `gen_arch.py:194`. Done.
  - Empty-body message — **only 3 of the 5 sites use the constant**.
    `grep -n "Body cannot be empty\|EMPTY_BODY" gen_*.py`:
    - base 6e59e1ea, 5 literals: `gen_arch.py:199` and `gen_flow.py:126`
      ("…for structured node from string with \\n"); `gen_arch.py:227`,
      `gen_flow.py:152`, `gen_tree.py:57` ("…for structured node").
    - head ea1f8c77: `raise ValueError(EMPTY_BODY)` at `gen_flow.py:128`,
      `gen_arch.py:204`, `gen_tree.py:57`; but
      `gen_flow.py:114` and `gen_arch.py:189` still hold the inline literal
      `raise ValueError("Body cannot be empty for structured node from string with \\n")`.
    - `width.py:152-158` docstring records the choice: "The longer variant
      … is specific to string-input paths and remains at those call sites."
      The plan (`plan.md` W1-04) names no such exception. The two literals
      are still a duplicate pair across two generators. Using `EMPTY_BODY`
      there would change the error text (breaking row 2 / the "error
      messages unchanged" constraint); a second shared constant would satisfy
      both. The 2026-09-28 run's statement "No … empty-body error strings …
      remain" was wrong; this gap predates the sync.
  - Single-line guard: `width.py:176` `require_single_line`; used at
    `gen_seq.py:71`, `gen_seq.py:73`, `gen_bar.py:29-32` (bar keeps its own
    message template). Done.
  - Result: partly.
- 2: re-tested — golden comparison, base generators (6e59e1ea) vs head
  generators (ea1f8c77), 26 cases across all six shapes: plain, CJK,
  string-`\n` structured, dict structured, narrow width forcing CJK/mixed
  wrapping, an over-wide title, and every error path (empty body dict and
  string-`\n` for flow/arch, empty body for tree, line breaks `\n` / `\r\n`
  / `\r` for seq participant, seq label and bar label). Error cases record
  `ERROR <type>: <message>` so message text is compared too.
  - Command: `python3.12 -I render_cases.py <at-base>/…/scripts before`,
    same for `<at-head>` → `after`, then `diff -r before after` → empty
    ("DIFF EMPTY"), 26 files each.
  - `align.py` on all 18 non-error outputs, each with its own commit's
    checker: 17 "✓ no drift" at both commits; `seq-basic` reports
    "line 8: col 29: '│' at display-col 29 connects to nothing vertically"
    identically at base and head — pre-existing, outside this change.
  - Generator tests at ea1f8c77:
    `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-workflow/tests/loom-visualization -q`
    → "211 passed, 5 skipped". The 5 skips are
    `test_adversarial_probes.py:194` "node or tests/mermaid/node_modules
    absent" (Mermaid rendering, not the ASCII generators). The count is lower
    than 2026-09-28's 233 because trunk PR #97 shrank `test_references.py`,
    `test_templates.py`, `test_skill_script_paths.py`; no generator test file
    changed in the sync.
  - Case list (script kept in the tester's scratch space, cases verbatim):
    flow-plain, flow-cjk, flow-str-structured, flow-dict-structured,
    flow-dict-narrow (width 16), flow-mixed-wide (width 12),
    flow-err-dict-empty, flow-err-str-empty, arch-plain, arch-cjk,
    arch-str-structured, arch-dict-structured, arch-dict-narrow (width 18),
    arch-err-dict-empty, arch-err-str-empty, tree-plain, tree-cjk,
    tree-structured, tree-err-empty, seq-basic, seq-err-participant,
    seq-err-label, bar-basic, bar-err-label, table-basic, table-ascii.
  - Result: works.
- 3: re-tested — this criterion's own tests at ea1f8c77: the helper tests
  `pytest loom-workflow/tests/loom-visualization/test_ascii_width.py -q` →
  "41 passed" (includes `test_EMPTY_BODY_constant`, `test_center_*`,
  `test_require_single_line_*`, `test_render_structured_node_*`); the
  loom-visualization folder → "211 passed, 5 skipped" (above); release
  metadata `pytest loom-code/tests/test_write_plan_station_text.py -k "release_metadata or synchronized"`
  → "1 passed" (manifests agree on 5.11.1). The full package suite was not
  run here; it is
  `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`,
  executed by `finalize-review`, which refuses the attestation on failure.
  Result: works.

## Re-run on 2026-10-19, at 32385861

Fix range 1dc85bd1..32385861 (`fix(loom-workflow): route string-input
empty-body errors through width.py`): `width.py` adds
`EMPTY_BODY_FROM_STRING = EMPTY_BODY + " from string with \\n"`;
`gen_flow.py:114` and `gen_arch.py:189` raise it; `test_ascii_width.py`
gains two tests; `plan.md` gains Risk 4 (agent-decided, line 63). The fix
touches the shared helper module and two generators, so rows 1, 2 and 3 can
all be affected; all three re-tested in full.

Clean copies again: `git worktree add --detach <scratch>/h2 32385861`,
`git worktree add --detach <scratch>/b2 6e59e1ea`. Interpreter uv CPython
3.12.11. Setup: the documented entry point
`printf '%s' '<json>' | python3 scripts/generate.py <shape>` still runs.

- 1: re-tested — every sub-item, at 32385861:
  - Structured-node render: `render_structured_node` called at
    `gen_flow.py:116`, `gen_flow.py:130`, `gen_arch.py:190`,
    `gen_arch.py:206`. Done.
  - Centering: no `def _center` in any generator; `center` used at
    `gen_flow.py:120`, `gen_arch.py:194`. Done.
  - Empty-body message: `grep -n "Body cannot be empty\|EMPTY_BODY" gen_*.py width.py`
    → the literal appears once, at `width.py:152` (`EMPTY_BODY`);
    `width.py:158` derives `EMPTY_BODY_FROM_STRING` from it. Raises:
    `gen_flow.py:114` and `gen_arch.py:189` (`EMPTY_BODY_FROM_STRING`),
    `gen_flow.py:128`, `gen_arch.py:204`, `gen_tree.py:57` (`EMPTY_BODY`).
    All 5 sites now come from the one shared constant; no inline message
    is left in any generator. The two-name design (rather than one
    literal for all 5, which would change error text) is recorded as plan
    Risk 4. Done.
  - Single-line guard: `require_single_line` at `gen_seq.py:71`,
    `gen_seq.py:73`, `gen_bar.py:29`. Done.
  - Result: works.
- 2: re-tested — the same 26-case battery, base generators (6e59e1ea)
  vs 32385861 generators: `diff -r r2/before r2/after` → empty
  ("DIFF EMPTY"). Both string-input error paths give the identical message
  at both commits:
  `flow-err-str-empty` and `arch-err-str-empty` →
  `ERROR ValueError: Body cannot be empty for structured node from string with \n`.
  Through the CLI: `printf '%s' '{"steps":["Title\n"]}' | python3 generate.py flow`
  and `printf '%s' '{"layers":[{"name":"T\n","components":["c"]}]}' | python3 generate.py arch`
  → `generate.py <shape>: Body cannot be empty for structured node from string with \n`,
  exit 1, the same at base and head. `align.py` on the 18 non-error
  outputs: 17 "✓ no drift" at both commits; `seq-basic` reports the same
  pre-existing "line 8: col 29 … connects to nothing vertically" at both.
  Generator tests: `pytest loom-workflow/tests/loom-visualization -q` →
  "213 passed, 5 skipped" (same Mermaid/node skips). Result: works.
- 3: re-tested — this criterion's own tests at 32385861:
  `test_ascii_width.py` → "43 passed" (incl. the new
  `test_EMPTY_BODY_FROM_STRING_constant` and
  `test_empty_body_messages_live_only_in_width`); loom-visualization →
  "213 passed, 5 skipped"; release metadata (`-k "release_metadata or synchronized"`)
  → "1 passed". The full package suite was not run here (the coordinator
  is running it separately); `finalize-review` executes
  `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`
  and refuses the attestation on failure. Result: works.

## Re-run on 2026-10-19, at 74595f4f

Fix range bd3e5ee5..74595f4f (`test(loom-visualization): check string-input
empty-body errors at the generator entries`): `git diff --stat` shows only
`loom-workflow/tests/loom-visualization/test_ascii_generators.py` (+15) and
`test_ascii_width.py` (−14). The two tests added in 32385861
(`test_EMPTY_BODY_FROM_STRING_constant`,
`test_empty_body_messages_live_only_in_width`) were removed and replaced by
`test_string_node_with_empty_body_keeps_its_error_text`, which drives
`render_flow(["Title\n"])` and `render_arch([{"name": "Title\n", ...}])`
and asserts the exact error text. No production code changed.

- 1: carried over — no file under `scripts/` changed in bd3e5ee5..74595f4f;
  the 32385861 source inspection still describes the code.
- 2: carried over — generators unchanged, so the 26-case golden diff run at
  32385861 still applies; the new entry-level test independently pins both
  string-input error texts (see row 3).
- 3: re-tested — clean copy at 74595f4f:
  `pytest loom-workflow/tests/loom-visualization -q` → "212 passed,
  5 skipped" (same Mermaid/node skips); `test_ascii_width.py` → "41 passed";
  `test_ascii_generators.py::test_string_node_with_empty_body_keeps_its_error_text`
  → "1 passed"; release metadata → "1 passed". Full package suite not run
  here (running separately; `finalize-review` executes it and refuses the
  attestation on failure). Result: works.