# Return the entry-definition pin to sentence-level judging — acceptance test evidence

Tried on 2026-10-06, in a clean copy of the project at 9f6ae237
(`git worktree add --detach <scratchpad>/at-wt HEAD`, outside the repo tree so
no nested worktree is seen by tree-walking tests). Every pytest command below
ran as
`env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest -p no:cacheprovider -q <files>`
(the README's isolated environment; the two variables are unset per known
nested-pytest leaks).

## Setup — the change installs and loads in a clean copy
- How I tried it: the README Development checks, then plugin manifest validation.
  - `python3 scripts/sync_codex_manifests.py --check --all` -> exit 0
  - `python3 scripts/check_plugin_boundaries.py loom-code` -> `OK: loom-code is filesystem-boundary clean.` exit 0
  - `python3 scripts/check_plugin_boundaries.py loom-design` -> `OK: loom-design is filesystem-boundary clean.` exit 0
  - `python3 loom-code/scripts/check-skill-crossrefs.py` -> `OK: all relative skill cross-references resolve.` exit 0
  - `claude plugin validate loom-code` -> `✔ Validation passed`
- What came back: all green; the README setup works as written.

## 1. 在入口定義那一句裡，用分號接上一段否定把它推翻，測試會失敗。
- How I tried it: edited the clean copy's `loom-code/skills/write-plan/SKILL.md`
  the way a careless editor would, ran the pin, then restored the file from a
  scratch backup by copy (no git discard).
  - Variant A: `Files marks the entry other modules call;` ->
    `Files marks the entry other modules call; that is not the function its tests call;`
  - Variant B: `name behaviour seen there;` ->
    `name behaviour seen there; never mark a function other modules call;`
  - Control: the pre-change pin (`git show acf23cec:loom-code/tests/test_write_plan_entry_definition.py`,
    copied in as a temporary test file and deleted after) run against Variant A.
- What came back:
  - Variant A, new pin: `FAILED ...test_write_plan_entry_definition.py::test_taskentry_skilltext_definedbyoutsidecallers` — `1 failed, 4 passed`
  - Variant A, pre-change pin: `4 passed` (the gap the intent describes, reproduced)
  - Variant B, new pin: same test FAILED — `1 failed, 4 passed`
  - After restore: `git status --short` empty; pin `5 passed`
- Also: `test_write_plan_entry_definition.py`, `test_write_plan_entry_definition_curly.py`,
  `test_write_plan_entry_definition_split.py` (the graduated adversary probe) as delivered -> `10 passed`.
  Direct calls of `_pins_outside_callers`:
  `"...other modules call; it is not that function."` -> False;
  `"...other modules call, i.e. not that one."` -> False.
- Evidence: captured output above; named test
  `test_entrypin_siblingclausenegation_rejected` (loom-code/tests/test_write_plan_entry_definition.py:68).

## 2. write-plan 目前的入口定義文字經改寫後仍讓測試通過，意思與原本相同，字數不增加。
- How I tried it: read the one-line diff of SKILL.md (acf23cec..HEAD), ran the
  pin and the write-plan size test, counted words at both commits.
- What came back:
  - Diff: `logic that entry cannot reach is its own module,` -> `logic beyond that entry's reach is its own module,` (loom-code/skills/write-plan/SKILL.md:328)
  - Phrase words: 5 -> 5. Whole file (`str.split`): 3786 -> 3786. Body words via the
    test's own `_body_words`: 3749 -> 3749, cap `< 3750` (loom-code/tests/test_write_plan_shape_text.py:41).
  - `test_write_plan_entry_definition.py` -> `5 passed`; `test_write_plan_shape_text.py` -> `5 passed`.
  - Meaning: both say logic the entry cannot reach is its own module, tested at its
    entry; read as equivalent.
- Evidence: diff and counts above.

## 3. 測試本身說明它只是固定檢查，抓不到所有反義寫法。
- How I tried it: read the pin's module docstring (loom-code/tests/test_write_plan_entry_definition.py:1-17)
  and checked its stated limits are real by calling `_pins_outside_callers`.
- What came back:
  - Docstring: "It is a cheap fixed check (a tripwire), not a semantic guarantee:
    inversions phrased with "rather than", "instead of" or "neither ... nor" pass it
    and are left to closing-review reviewers." It also states "i.e. Never" splits.
  - `"Files marks what its tests call rather than the entry other modules call."` -> True (passes, as documented)
  - `"Files marks the entry other modules call, i.e. Never mind."` -> True (passes, as documented)
- Evidence: docstring text and probe calls above.

## 4. 完整 package suite 全部通過；三份 manifest、README 的版號字串與 CHANGELOG 新區段一致。
- How I tried it: read every version string; ran only the version-sync tests and the manifest sync check.
- What came back:
  - `"version": "3.36.0"` in loom-code/.claude-plugin/plugin.json:3, loom-code/.codex-plugin/plugin.json:3,
    loom-code/plugin.json:3, loom-code/package.json:3.
  - README: loom-code/README.md:11, README.ja.md:11, README.zh-TW.md:9, root README.md:17 and :132 all 3.36.0.
  - CHANGELOG top section `## [3.36.0] — 2026-10-06 — the write-plan entry-definition pin judges whole sentences`.
  - `git grep 3.35.0` outside CHANGELOG/docs: no hits.
  - `test_adversarial_version_metadata_sync.py` + `test_write_plan_station_text.py` -> `46 passed`.
  - `sync_codex_manifests.py --check --all` -> exit 0.
  - Full package suite NOT run here (left to finalize-review, which runs it and blocks on failure):
    `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`.
    The graduated probe lives in loom-code/tests/, which that runner discovers automatically.
- Note (nit): CHANGELOG 3.36.0 first bullet says the pin splits "on `.` only"; after
  ebd3443c it ends a sentence at `.`, `!` or `?` followed by a capitalised word
  (loom-code/tests/test_write_plan_entry_definition.py:40). The CHANGELOG was not updated with that fix.
- Evidence: file:line references and outputs above.
