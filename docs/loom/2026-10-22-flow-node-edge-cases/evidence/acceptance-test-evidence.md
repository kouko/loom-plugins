# Fix the flow diagram's flush body line and string-body splitting — acceptance test evidence

Tried on 2026-10-22, in a clean copy of the project at efa90a66.

## Setup
- Clean copies: `git archive efa90a66` and `git archive fc6e9bfc` (trunk named in the intent), each extracted into its own empty scratch directory; the session worktree was never used to run anything.
- Trunk reference check: `git merge-base efa90a66 3f98214c` = 3f98214c (origin/main); `git diff fc6e9bfc 3f98214c -- loom-workflow/skills/loom-visualization/ | wc -l` = 0, so fc6e9bfc and origin/main carry identical generator scripts.
- The skill's own setup (SKILL.md: "The scripts need only the Python standard library"; run `printf '%s' '<json>' | python3 <skill-dir>/scripts/generate.py <shape>`) worked unchanged in the clean copy with Python 3.12.11. Every Acceptance 1-2 case below was run through that CLI, as an agent following the skill would.

## 1. A flow node whose description line is wider than the width budget keeps one space between the text and the right border, as it does with no width given.
- How I tried it: `generate.py flow` on trunk and HEAD with
  - `{"steps":["Build\nxxxxxxxxxxx","Ship"],"width":10}` (the intent's reproduction)
  - `{"steps":[{"title":"Build","body":["xxxxxxxxxxx"]},"Ship"],"width":10}` (dict form)
  - `{"steps":[{"title":"","body":["ab"]}],"width":1}` (narrowest width)
  - `{"steps":[{"title":"Build","body":["x"*50]}]}` (no width, line over the default 40-cell budget)
  - controls: CJK body `處理所有請求並回傳結果` at width 8; word body `handles all incoming requests quickly` at width 12.
- What came back:
  - Intent reproduction — trunk `│ xxxxxxxxxxx│` (flush); HEAD `│ xxxxxxxxxx │` + `│ x          │`; no-width drawing `│ xxxxxxxxxxx │` identical on both.
  - Dict form: same as above.
  - Width 1: trunk `│ ab│`; HEAD `│ a │` / `│ b │`.
  - No width, 50 x's: trunk `│ xxx…x(41)│`; HEAD `│ xxx…x(40) │` / `│ xxxxxxxxxx  …│`.
  - CJK and word controls: byte-identical on trunk and HEAD (both already padded).
  - Fuzz residual check (seed 20261022, 20,000 flow inputs): 0 HEAD flow drawings with a box line whose last cell before the right border is not a space (lines with embedded control characters excluded).
  - Adversary nit observed: `{"steps":[{"title":"","body":["　"]}],"width":1}` (body is one U+3000) — trunk `│ 　│` (5-cell box), HEAD `│ 　 │` (6-cell box). HEAD keeps the pad; it is one cell wider than trunk, consistent with this line.
- Evidence: captured CLI output above; scripts `fuzz_a3.py` (scratch, see 3).

## 2. A flow or architecture node whose description is a single string draws that string as its description lines, one line per line of the string, instead of one character per line.
- How I tried it: `generate.py flow|arch` on trunk and HEAD with
  - `{"steps":[{"title":"Build","body":"handles requests"},"Ship"]}`
  - `{"layers":[{"name":{"title":"Web","body":"handles requests"},"components":[]}]}`
  - flow `body:"line one\nline two"` next to `body:["line one","line two"]`
  - arch `body:"處理請求\n回傳結果"` with components `API`,`DB`, next to the list form
  - boundaries: `body:""` (flow, arch), `body:"\n"`, `body:"a\tb"` vs `["a\tb"]`.
- What came back:
  - Flow: trunk 16 one-character lines; HEAD one line `│ handles requests │`.
  - Arch: trunk 16 one-character lines and `│ Web│`; HEAD `│ Web             │` / `│ handles requests│` (the body line touching the right border is the arch flush accepted at PR #104's decision point ③, out of scope in the intent).
  - Multi-line string vs list, flow and arch: HEAD draws the string and the list byte-identically (two lines); trunk split the string per character.
  - `""`: both trunk and HEAD print `generate.py flow: Body cannot be empty for structured node` (arch: `generate.py arch: …`).
  - `"\n"`: HEAD draws one empty body line, same as list `[""]`; `"a\tb"`: HEAD draws `│ a\tb    │`, same as list `["a\tb"]` and trunk's list form.
- Evidence: captured CLI output above.

## 3. For every one of the six generators, inputs that hit neither defect draw byte-identically to trunk fc6e9bfc, including error messages.
- How I tried it: differential fuzz, scratch scripts `render_batch.py` (loads one tree's `generate.render`, records `["ok", text]` or `["err", type, message]`) and `fuzz_a3.py <at-dir> 20000 <seed>`; 20,000 random inputs per generator (table, flow, tree, bar, arch, seq) mixing ASCII, spaces, CJK, half-width kana, emoji, combining marks, U+3000, tab, newline, BEL, empty strings, widths None/-1/0-60. A case "hits a defect" when it has a non-empty string description (defect 2) or its trunk flow drawing has a right border preceded by a non-space character, including an embedded newline (defect 1). Every other case must match trunk exactly, output and error type and message.
- What came back (seed 20261022; seed 7 also 0 unexplained):

| generator | total | hit neither | identical | of which errors | defect inputs |
|---|---|---|---|---|---|
| flow | 20000 | 15697 | 15697 | — | d1 1562, d2 3015 |
| arch | 20000 | 16909 | 16909 | 6741 | d2 3091 |
| table | 20000 | 20000 | 20000 | 11310 | 0 |
| tree | 20000 | 20000 | 20000 | 4396 | 0 |
| bar | 20000 | 20000 | 20000 | 5322 | 0 |
| seq | 20000 | 20000 | 20000 | 10753 | 0 |

  `unexplained differences: 0`. A first run with a narrower flush detector (split on `\n`) reported 26 differences, all flow cases whose list item embedded a newline so that the logical body line was flush on trunk; the detector was widened to count those as defect-1 inputs and the rerun reported 0.
- Also: the branch's own trunk-pin tests pass (see 5).
- Evidence: fuzz output above; `cases.json`, `out-trunk.json`, `out-head.json` in the scratch directory.

## 4. The test guarding that all six generators are pinned fails when a generator's drawn output changes.
- How I tried it: copied the clean HEAD export; for each generator appended to `gen_<g>.py` a wrapper making `render_<g>` return its output plus one trailing space; ran only `loom-workflow/tests/loom-visualization/test_ascii_generators.py::test_trunk_pins_draw_expected_output_for_all_six_generators` (`env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest -q -p no:cacheprovider …`); restored the file after each run (`diff -r` afterwards showed only `__pycache__` differences).
- What came back: unmodified — `1 passed`. Mutated table → `1 failed` (`AssertionError: table-ascii-multiline`); flow → failed (`flow-plain`); tree → failed (`tree-cjk`); bar → failed (`bar-all-zero`); arch → failed (`arch-cjk-components`); seq → failed (`seq-messages`).
- Evidence: scratch script `mutate_a4.sh`, output above. The test also asserts the drawn set equals the six generator names (`test_ascii_generators.py:1423-1428`).

## 5. The full package suite passes.
- How I tried it: ran only the tests covering this change, not the full suite: `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest -q -p no:cacheprovider loom-workflow/tests/loom-visualization/ loom-workflow/tests/scripts/test_release_metadata.py`.
- What came back: `255 passed, 5 skipped in 1.95s`; the 5 skips are `test_adversarial_probes.py:194: node or tests/mermaid/node_modules absent` (Mermaid probes, unrelated to this change). Release files read back: all four loom-workflow version fields `5.12.4`, CHANGELOG `## [5.12.4] — 2026-10-22 — flow node edge-case fixes`; origin/main (3f98214c) is still at 5.12.3, so the version is free.
- Full suite: `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q` — not run here; it is executed by finalize-review, which refuses the attestation when it fails.
- Evidence: pytest output above.
