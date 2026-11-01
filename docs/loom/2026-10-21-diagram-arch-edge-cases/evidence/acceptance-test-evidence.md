# Fix the layered-architecture diagram's early wrap and empty-name edge cases — acceptance test evidence

Tried on 2026-10-21, in a clean copy of the project at 3f44b26f, compared against a clean copy of trunk at 5e850c70.

## Setup
- How I tried it: `git worktree add --detach <scratch>/at-head 3f44b26f` and `git worktree add --detach <scratch>/at-trunk 5e850c70`. The skill's SKILL.md says the scripts need only the Python standard library and are run as `python3 <skill-dir>/scripts/<name>.py`; the user path is `printf '%s' '<json>' | python3 <skill-dir>/scripts/generate.py arch` (SKILL.md line 122).
- What came back: both copies ran with no install step. Release metadata check: `loom-workflow/plugin.json` is 5.12.3 on HEAD; `origin/main` (fetched 2026-10-21) is still 5e850c70 at 5.12.2, so no concurrent bump (plan Risk 1).
- Driver scripts (scratch, not committed): `drive.py` runs each case through `generate.py arch` on both trees and reports the set of display widths of the output lines (one width = borders line up); `fuzz.py` compares trunk and HEAD through `generate.render` for 6,000 seeded random inputs (seed 20261021).

## 1. A layered-architecture layer whose description line is its widest line shows that line unbroken, in a box whose borders line up, whenever no width budget forces it narrower.
- How I tried it: `generate.py arch` with
  - `{"layers":[{"name":{"title":"API","body":["handles requests"]},"components":["auth","db"]}]}` (no width, and again with `"width":40`)
  - `{"layers":[{"name":"API\nhandles requests","components":["auth","db"]}]}`
  - `{"layers":[{"name":{"title":"API","body":["處理所有請求"]},"components":["a"]}]}`
  - boundary: the dict input with `"width":12` (budget narrower than the line)
- What came back (HEAD, dict input, both widths; the string-name input is byte-identical):
  ```
  ┌─────────────────┐
  │ API             │
  ├─────────────────┤
  │ handles requests│
  ├─────────┬───────┤
  │ auth    │ db    │
  └─────────┴───────┘
  ```
  line widths {19}. Trunk drew `handles` / `requests` on two lines (widths {18}). CJK: HEAD `│ 處理所有請求│` on one line, widths {15}; trunk split it `處理所有請` / `求`. Boundary `width:12`: HEAD and trunk identical, still wraps to `handles` / `requests`, widths {14}.
- Re-run 2026-10-21 at 0fd51596 (after spec-conformance review findings 1 and 3), fresh `git worktree add --detach <scratch>/rerun/at-head 0fd51596` and `.../at-trunk 5e850c70`, both ran with no install step:
  - all five cases above re-run: HEAD outputs and widths identical to the first run ({19}, {19}, {19}, CJK {15}, `width:12` {14} same as trunk).
  - Default budget: `render_arch` sets `budget = width if width is not None else 40` (`gen_arch.py:76`). `{"layers":[{"name":{"title":"API","body":["x"*40]},"components":[]}]}` with no width: HEAD and trunk byte-identical, body wraps to 39 `x` then a lone `x`, box 42 cells wide. Same with 39 `x`: HEAD one line, box 42 wide; trunk wraps to 38 + 1, box 41 wide. 40 `x` with `"width":60`: HEAD one line (box 43 wide); trunk wraps to 39 + 1. So with no width, a description line of 40+ cells still wraps, as on trunk.
  - Multi-layer: `{"layers":[{"name":"Web","components":["ui"]},{"name":{"title":"API","body":["handles requests"]},"components":["auth","db"]}]}` — all layers share one interior width, so the unaffected `Web` box widens from 18 cells (trunk `│      Web       │`) to 19 (HEAD `│       Web       │`); both trees aligned.
  - Covering tests at 0fd51596: `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID python3 -m pytest -q -p no:cacheprovider loom-workflow/tests/loom-visualization/test_ascii_generators.py loom-workflow/tests/scripts/test_release_metadata.py` → `79 passed in 1.72s`.
- Evidence: scratch `drive.out`, cases "A1 ...". Covering tests passed on HEAD: `test_ascii_generators.py` (incl. the A1 tests named in the plan) — `79 passed in 1.57s` together with `tests/scripts/test_release_metadata.py`.

## 2. A layer with an empty single-line name and no components draws a box whose borders line up.
- How I tried it: `{"layers":[{"name":"","components":[]}]}`; also as the second layer after `{"name":"Web","components":["ui"]}`; also name `"́"` (a zero-width mark only, plan Risk 5).
- What came back: HEAD
  ```
  ┌─┐
  │ │
  ├─┤
  │ │
  └─┘
  ```
  widths {3}. Trunk: `┌┐ ││ ├┤ │ │ └┘`, widths {2, 3} (last row one cell wider). Second-layer case: identical on both trees, aligned. Zero-width name: HEAD aligned 3-wide box; trunk `┌┐` box with a 3-wide row.
- Evidence: scratch `drive.out`, cases "A2 ..."; zero-width cases run as `printf '%s' '{"layers":[{"name":"́","components":[]}]}' | python3 -I <tree>/loom-workflow/skills/loom-visualization/scripts/generate.py arch` on both trees, outputs as quoted here.

## 3. A layer with an empty title and at least one description line draws a box whose borders line up instead of raising an error, at any width budget.
- How I tried it: `{"name":{"title":"","body":["x"]},"components":[]}` with no width, `width:1`, `width:0`; string `"\nx"`; `{"title":"","body":[""]}` (empty description line); `{"title":"","body":["some longer text"]}` + components at `width:5`; `{"title":"","body":["中文"]}` at `width:2`; `{"title":"","body":["abc def"]}` + two components at `width:3`; title `"́"` + body `x`.
- What came back: trunk exits 1 with `generate.py arch: max_width must be positive` for the first five; HEAD exits 0 for all, every output one width, e.g.
  ```
  ┌──┐
  │  │
  ├──┤
  │ x│
  ├──┤
  │  │
  └──┘
  ```
  The three wider cases (width 5 / 2 / 3) already rendered on trunk and are byte-identical on HEAD.
  Not in this line's scope but observed: `{"title":"","body":[]}` (no description line) exits 1 with `Body cannot be empty for structured node` on both trees.
- Evidence: scratch `drive.out`, cases "A3 ..."; covering tests `test_arch_empty_title_narrow_widths_aligned` and the plan's A3 tests passed in the run above.

## 4. For inputs that hit none of the three defects, every diagram generator's output and error messages are byte-identical to trunk before this change.
- How I tried it: `python3 -I fuzz.py <scratch> 3000` — 3,000 random arch inputs (dict and string names, CJK, combining marks, trailing spaces, empty strings, widths 0–40 or none) and 600 each for table, flow, tree, bar, seq; same inputs rendered by trunk and HEAD; every difference classified.
- What came back:
  ```
  identical / total per shape: {'arch': [2673, 3000], 'table': [600, 600], 'flow': [600, 600], 'tree': [600, 600], 'bar': [600, 600], 'seq': [600, 600]}
  difference classes: {'fewer-lines (unwrapped)': 320, 'trunk-error->rendered': 5, 'trunk-misaligned': 2}
  HEAD arch misaligned: 0
  ```
  No difference fell outside the three defect classes (`OTHER` 0, `error-changed` 0); every error HEAD raised is the same text trunk raised. `git diff --name-only 5e850c70...HEAD` touches only `gen_arch.py` among the generator scripts.
- Evidence: scratch `fuzz.out`; the suite's trunk pins (`test_generator_output_matches_trunk_pin`, `test_generator_error_matches_trunk_pin`) copied into the trunk tree and run there: `19 passed, 46 deselected` — the pins hold on trunk code, so they record trunk output.

## 5. The package suite pins the exact trunk output of unaffected inputs for every diagram generator, and the hang-guarded rendering in the generator tests goes through one shared helper.
- How I tried it: read `loom-workflow/tests/loom-visualization/test_ascii_generators.py` at HEAD; ran it.
- What came back: `_TRUNK_PINS` holds two cases each for table, flow, tree, bar, arch, seq (`test_ascii_generators.py:1207-1331`); `test_trunk_pins_cover_all_six_generators` asserts the six-shape set (`:1347`). One `subprocess.run` in the file, inside `_render_isolated` (`:1069`), used 12 times; trunk had two near-duplicate helpers `_render_arch_isolated` (`:1067`) and `_render_flow_isolated` (`:1134`). The pins pass on HEAD and on trunk code (see 4).
- Evidence: `grep -c "subprocess.run"` → 1; pytest run above.

## 6. The complete package suite passes.
- How I tried it: per the acceptance-tester contract I did not run the full suite; I ran the tests covering this change: `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID python3 -m pytest -q -p no:cacheprovider loom-workflow/tests/loom-visualization/test_ascii_generators.py loom-workflow/tests/scripts/test_release_metadata.py` → `79 passed in 1.57s`. Trunk's own copy of the generator tests: `39 passed`.
- Re-run at 0fd51596: same command → `79 passed in 1.72s`. The full suite passing at Build (3f44b26f) is as reported by the closing-review station; not witnessed by this tester.
- Rows 2–5 carried over: `git diff --stat 88defa02..0fd51596` → only `docs/loom/2026-10-21-diagram-arch-edge-cases/plan.md` (1 line, Risk 3 wording); no production or test file changed.
- Full suite command, executed by finalize-review, which refuses the attestation when it fails: `python3 scripts/run_package_tests.py --loom-family`.
- Evidence: pytest output above.
