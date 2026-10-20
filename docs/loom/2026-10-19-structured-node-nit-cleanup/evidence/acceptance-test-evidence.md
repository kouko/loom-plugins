# Clean up the eight structured-node reviewer nits — acceptance test evidence

Tried on 2026-10-20, in a clean copy of the project at a57a5769 (a fresh
`git worktree add --detach` of HEAD), compared against a second clean copy of
trunk base f055b428. All Python ran with `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID`.
Both scratch copies were removed afterwards.

Setup check: the skill's documented entry point
(`printf '%s' '<json>' | python3 <skill-dir>/scripts/generate.py <shape>`, SKILL.md:122)
ran from the clean copy with no extra install; every sample below went through it.

## 1. For the same inputs, including every error path, all five diagram generators produce output and error messages byte-identical to trunk before this change.
- How I tried it: a scratch harness ran 31 JSON payloads through
  `generate.py` in both clean copies (`python3 -I`, 10 s timeout each) and
  compared exit code, stdout and stderr byte for byte. Payloads: flow (plain,
  CJK, dict structured, string `"T\nbody"` structured, over-wide title with
  `width: 12`, CJK over-wide with `width: 14`, wrapping body, dict empty body,
  string empty body, empty step list); arch (plain, CJK, dict structured with
  CJK, string structured, over-wide title with `width: 10`, dict empty body,
  string empty body); tree (plain, CJK, dict structured, dict empty body);
  seq (plain, CJK, multi-line participant, multi-line label, unknown
  participant); bar (plain, CJK, multi-line label, negative value); unknown shape.
  A second harness imported `width.py` from both copies and called `center`
  and `render_structured_node` on 11 over-wide / CJK / negative-slack cases
  (`center("abc", -5)`, `render_structured_node("很寬的標題文字", ["內容"], 6)`, …).
  Criterion tests: `pytest loom-workflow/tests/loom-visualization/test_ascii_generators.py loom-workflow/tests/loom-visualization/test_ascii_width.py`.
- What came back: `samples=31 differing=1`. The one difference (seq with an
  unknown participant `Z`) is an uncaught `KeyError` traceback whose only
  difference is the checkout path in the `File "..."` lines; after replacing
  each tree root with `<ROOT>` the two outputs are identical. Every error text
  matched, e.g. `generate.py flow: Body cannot be empty for structured node`,
  `generate.py arch: Body cannot be empty for structured node from string with \n`,
  `generate.py tree: Body cannot be empty for structured node`,
  `generate.py seq: line break not supported in message label: 'two\nlines'`,
  `generate.py bar: bar label must be single-line, got line break in 'two\nlines'`.
  Helper harness: `cases=11 identical=11`; `EMPTY_BODY` and
  `EMPTY_BODY_FROM_STRING` equal across copies. Criterion tests: `72 passed`.
- Observation (pre-existing, identical on base): arch with an over-wide dict
  title and `width: 10` draws the title line one cell past the right border
  (`│ Extremely wide layer title│` under a 26-cell top border). Not caused by
  this change.
- Evidence: scratch harness output above; tests named above.
- Suite check: `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`.

## 2. The structured-node wrapping test fails when the width the body wraps at is changed.
- How I tried it: in the scratch HEAD copy only, edited
  `width.py:218` `wrap_label(body_line, interior - 1)` to `interior - 2`, ran
  `test_ascii_width.py::test_render_structured_node_wrapped_body`; then to
  `interior`, ran it plus both visualization test files; restored the line
  (scratch `git status` clean afterwards). Also replayed the base version's
  old assertions (title line, separator, border characters only) against the
  `interior - 2` mutant.
- What came back: `interior - 2` → `1 failed` (`AssertionError` at
  `test_ascii_width.py:382`, mutant wrapped to `this is a long` / `body line that` / `wraps`).
  `interior` → `1 failed`; `test_ascii_width.py` `1 failed, 40 passed`;
  `test_ascii_generators.py` `1 failed, 30 passed`. Old base assertions on the
  `interior - 2` mutant: `base-version assertions pass on mutant: True` — the
  old test would not have noticed; the new one does.
- Evidence: `loom-workflow/tests/loom-visualization/test_ascii_width.py:377-387`.

## 3. No test only restates a constant's literal text; the empty-body error text stays checked through the generator entry points.
- How I tried it: `grep -rn "EMPTY_BODY" loom-workflow/tests/` (no hits);
  `grep -rnE "assert +[A-Z][A-Z_]+ *==" loom-workflow/tests/loom-visualization/` (no hits);
  `grep -rn "Body cannot be empty" loom-workflow/tests/`; ran the two entry-point tests.
- What came back: the only literal checks are
  `test_ascii_generators.py:1037` (string path, flow + arch) and
  `test_ascii_generators.py:1053` (dict path through `render_flow`,
  `render_arch`, `render_tree`); both pass inside the 72-pass run above.
  `test_EMPTY_BODY_constant` is gone from `test_ascii_width.py`. The CLI
  harness in line 1 also confirmed the dict-path text for flow, arch and tree.
- Evidence: `loom-workflow/tests/loom-visualization/test_ascii_generators.py:1033-1063`.

## 4. The shared helper file carries no plan-only labels and no branch that cannot change its output, and `gen_arch.py` has no run of more than two blank lines.
- How I tried it: read `width.py:147-223`; `grep -nE "W[0-9]-[0-9]{2}|copies\)"` and
  `grep -nE "< 0"` on `width.py`; `grep -rnE "W[0-9]+-[0-9]+"` on the scripts
  folder; counted the longest blank-line run per file with a short Python regex.
- What came back: no plan labels, no "(4 copies)", no `< 0` clamps; the
  helper section has one conditional left (`require_single_line`'s raise),
  which changes the outcome. Longest blank run: `gen_arch.py` 2 (base: 4),
  `width.py` 2. Removing the clamps did not change any output (line 1 helper
  harness, negative-slack cases).
- Evidence: `loom-workflow/skills/loom-visualization/scripts/width.py:165-223`; `gen_arch.py:28-31`.

## 5. The 5.11.1 release note lists every helper that release added, and the structured-node change's golden-diff evidence and intent each carry a note pointing to what finally shipped (the 26-sample comparison; five sites derived from one error constant), with their original text kept.
- How I tried it: listed what PR #63 added to `width.py`
  (`git diff f055b428^..f055b428 -- .../width.py | grep -E '^\+(def |[A-Z_]+ =)'`)
  and compared with the 5.11.1 entry; `git diff --numstat f055b428..HEAD` on the
  two merged records; grepped the five raise sites; checked the note's target
  report for the 26-sample figure.
- What came back: PR #63 added `EMPTY_BODY`, `EMPTY_BODY_FROM_STRING`,
  `center`, `require_single_line`, `render_structured_node`; the 5.11.1 entry
  now names all five (`EMPTY_BODY_FROM_STRING` was the missing one).
  numstat: golden-diff `2 0`, old intent `1 0` (additions only, nothing
  removed). golden-diff note: "the final comparison after the trunk sync used
  26 samples, including every error path; see …/acceptance-test-report.md"
  — that report exists and its row 2 says 26 samples. Old intent note (in that
  intent's language): five sites all derive from `EMPTY_BODY`, string path via
  `EMPTY_BODY_FROM_STRING`. Raise sites found: `gen_flow.py:114,128`,
  `gen_arch.py:187,202`, `gen_tree.py:57` = five.
- Evidence: `loom-workflow/CHANGELOG.md:14-21`;
  `docs/loom/2026-09-28-structured-node-shared-helper/evidence/golden-diff.md:13`;
  `docs/loom/intent/2026-09-28-structured-node-shared-helper.md:19`.

## 6. The complete package suite passes.
- How I tried it: from the change worktree
  `/Users/kouko/GitHub/loom-plugins/.claude/worktrees/structured-node-nit-cleanup`
  at a57a5769 (clean tree): `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`.
- What came back: exit code 0; every shell-test summary `N PASS / 0 FAIL`;
  pytest blocks all `passed` (e.g. `161 passed`, `128 passed`), no `failed`.
- Evidence: command and exit code above. `finalize-review` re-runs this suite
  and refuses the attestation on failure.
