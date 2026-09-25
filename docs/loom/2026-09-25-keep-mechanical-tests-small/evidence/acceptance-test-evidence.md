# Keep the tests a change adds small — acceptance test evidence

Tried on 2026-09-25, in a clean copy of the project at 1b056075
(`git worktree add /tmp/at-kmts HEAD --detach`; base main 19ce6e9a checked out
separately at `/tmp/at-kmts-base` for the before/after counts).

## 0. Setup
- How I tried it: loom-code is a plugin with no build step; its README says it
  installs independently and needs neither sibling plugin. Checked the three
  manifests parse and agree, and that the checker scripts run from the clean copy.
- What came back: `loom-code/plugin.json`, `.claude-plugin/plugin.json`,
  `.codex-plugin/plugin.json` all parse, all `3.17.0`; `loom_checker.py` and
  `check_mechanisms.py` run without error.

## 1. The implementer contract states a test budget: at most one positive and one negative or boundary case per Acceptance line or finding, reuse of the existing test helpers, no new test harness, no tests of tests, and the net test lines added in its report.
- How I tried it: read `loom-code/agents/implementer.md` as the implementer
  would; then gave a fresh-context sonnet agent only that file plus a toy task
  (one Acceptance line with a happy and an error case, one review finding, an
  existing test file with a helper) and asked what tests it would add.
- What came back: `loom-code/agents/implementer.md:36-41` — "The tests a task
  adds stay within a budget: at most one positive and one negative or boundary
  case per Acceptance line; a finding's fix adds at most one test, extending an
  existing test first; reuse the target test file's existing helpers and
  fixtures; no new test harness; no tests of tests. Report the net test lines
  added in `net_test_lines`." Report shape `implementer.md:112`
  `net_test_lines: <test lines added minus test lines removed>`.
  For a finding the budget is stricter than the intent wording (one test, not
  one positive plus one negative) — it matches Acceptance line 3's fix rule.
- Cold read (sonnet, file-only, 1 tool use): planned three test changes —
  extend the existing positive test with `'90s' -> 90`, one new negative test
  for `'5x'`, and fix the finding by extending the existing test that covers
  `'1m30s'` rather than adding one; "No — reuse `assert_parses`; no new
  helper/fixture/harness"; named `net_test_lines` as the size field; quoted
  the budget sentence verbatim. Within budget on every clause.
- Evidence: `loom-code/tests/test_test_budget_text.py::test_implementer_states_budget_and_net_lines`,
  `::test_budget_not_a_number_threshold` — passed (see command under 4).

## 2. The adversary contract states that each probe program stays small and reuses existing test helpers.
- How I tried it: read `loom-code/skills/closing-review/references/adversarial.md`
  as the adversary would, for the case "write a probe for a boundary input".
- What came back: `adversarial.md:84-85` — "Each probe program stays small and
  reuses the repository's existing test helpers; no harness built for one case."
  The five-program ceiling at `adversarial.md:60` is unchanged (out of scope
  per intent). An adversary writing a probe would import the repo's existing
  helper rather than build its own scaffolding.
- Evidence: `test_test_budget_text.py::test_adversarial_probe_small_reuses_helpers`,
  `::test_five_program_cap_unchanged` — passed.

## 3. Closing review's tests dimension makes over-built tests a finding with the smaller shape named, and says the fix for a finding adds at most one test, extending an existing test first.
- How I tried it: read the `tests` row of
  `loom-code/skills/closing-review/references/lenses.md:54` as a reviewer, for
  two cases: (a) the change adds a duplicated case plus a helper used once;
  (b) an old test file, untouched by the change, already has a duplicated case.
- What came back: row appends "tests the change adds beyond what the behaviour
  needs — duplicated cases, a helper set or harness for one case, tests of
  tests — are a finding that names the smaller shape, and the fix for any
  finding adds at most one test, extending an existing test first".
  Case (a): finding, naming e.g. "one parametrised test, inline the helper".
  Case (b): not a finding — the wording scopes it to tests "the change adds",
  which also honours the intent's out-of-scope "rewriting existing tests".
- Evidence: `test_test_budget_text.py::test_tests_dimension_overbuilt_is_finding`,
  `::test_fix_adds_at_most_one_test` — passed.

## 4. No checker rule, flow step or agent dispatch is added.
- How I tried it:
  - `python3 loom-code/scripts/loom_checker.py --list-rules | wc -l` at HEAD and at base
  - `python3 loom-code/scripts/check_mechanisms.py --baseline main`
  - `git diff 19ce6e9a..HEAD | grep -n '^+.*<!-- gate:'`
  - `git diff --name-only 19ce6e9a..HEAD | grep -E 'SKILL.md|hooks|agents/'`
- What came back:
  - rule count 26 at HEAD, 26 at base
  - `checker-rule 26/26`, `skill 23/23`, `contract 64/64`, `prose-gate 20/20`;
    "net mechanism count (excl. host-hygiene): 142 / baseline net count: 142 /
    all clear"
  - the only `<!-- gate:` hits are two string literals inside the new test
    file (lines counting markers), not markers in contract text
  - only `loom-code/agents/implementer.md` touched among skills/hooks/agents —
    a text edit to an existing agent, no new dispatch; no SKILL.md (station
    flow) changed
- Criterion tests run (not the full suite):
  `env -u FORCE_COLOR uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest -q loom-code/tests/test_test_budget_text.py loom-code/tests/test_loom_checker_cli.py`
  → `37 passed in 3.73s`.
- Full package suite is left to finalize-review:
  `env -u FORCE_COLOR uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`
