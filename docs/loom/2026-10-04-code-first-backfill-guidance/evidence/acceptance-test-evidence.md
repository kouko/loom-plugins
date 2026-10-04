# Code-first backfill guidance — acceptance test evidence

Tried on 2026-10-04, in a clean copy of the project at 88b1b83f
(`git worktree add --detach .git/loom-scratch/at-backfill 88b1b83f`; branch
base 620572db checked out the same way at `.git/loom-scratch/at-base` for
comparison). Both worktrees were removed afterwards.

## Setup — the change loads in the clean copy
- How I tried it: the README's install path is
  `claude plugin marketplace add … && claude plugin install loom-code@loom`.
  Installing would rewrite the user's own installed-plugin configuration, so I
  validated the package from the clean copy instead:
  `claude plugin validate ./loom-code` and `claude plugin validate .`.
- What came back: `✔ Validation passed` for loom-code; the marketplace passed
  with two pre-existing warnings (no marketplace description; unknown field
  `requires-contract` on plugins[2]), neither touched by this change.
- Evidence: the edited file `loom-code/references/engineering-baseline.md` is
  read by `loom-code/agents/implementer.md:24` ("Read ... engineering-baseline.md
  before writing any code ... where they differ, the baseline wins").

## 1. engineering-baseline 說明：使用者以一般語言指示跳過 tdd、程式在流程開始前就寫好時，補回流程要先寫測試釘住既有行為（bug 一起釘）再修改，並在 plan 記下先寫好的程式碼範圍。
- How I tried it: read §2 of `loom-code/references/engineering-baseline.md`
  in the clean copy as an implementer would, lines 43-70, checking each
  element of the line against the new paragraph at lines 63-70.
- What came back:
  - plain-words `tdd` skip, code before the flow: "When the user instructs a
    `tdd` skip in plain words for code written before the flow began
    (`skipped-by-instruction: tdd <date>`)" (63-64).
  - characterise first, bugs included, then change: "the backfill
    characterises that code first — pin its current behaviour, bugs included
    — before changing it" (65-66).
  - plan records the scope: "and the plan records which code predates the
    flow" (66-67). It does not say which plan section; see open question.
  - The paragraph sits directly after "Legacy backfill is not a violation"
    (56-61), which is unchanged.
- Focused tests (pass):
  `loom-code/tests/test_prose_pin_rule_text.py::test_engineeringbaselinemd_codefirstbackfill_present`,
  `loom-code/tests/test_adversarial_backfill_pin_a1.py` — part of the 27-pass
  run below.
- Evidence: `loom-code/references/engineering-baseline.md:63-70`.

## 2. 同一份說明寫明三個界線：沒有使用者指示而跳過先寫測試仍算違規；流程開始後新寫的程式碼照常先寫測試；編譯失敗不能當成測試抓得到問題的證據。
- How I tried it: same reading; then a break-the-text check — removed the
  sentence "An uninstructed skip remains a violation. " from the clean copy,
  reran the pins, restored the file from a backup copy (`git status --short`
  empty afterwards).
- What came back:
  - "An uninstructed skip remains a violation." (67)
  - "Code written after the flow began follows the iron law." (67-68)
  - "A compile or import failure proves only that an interface is missing;
    break the covered behaviour and watch the test fail (false-green
    diagnostic) to show it catches a defect." (68-70)
  - Break check: `FAILED ...test_prose_pin_rule_text.py::test_engineeringbaselinemd_codefirstbackfill_present`
    — `1 failed, 7 passed`. The pin does catch a missing boundary.
- Finding (tension with the build station, not with this line's wording):
  `loom-code/skills/build/SKILL.md:58-63` says "Unless `tdd` is skipped by
  the user's plain-words instruction, for every behavior change: 1. Write the
  smallest failing test ..." — i.e. once `tdd` is skipped the station text
  drops test-first for every behaviour change, including code written after
  the flow began. The implementer agent resolves this in the baseline's
  favour (`implementer.md:24-28`, "where they differ, the baseline wins"),
  but when `implementer` is also skipped the main agent implements itself and
  `build/SKILL.md` does not point to `engineering-baseline.md` (grep found no
  reference), so the post-flow boundary is not in front of it.
- Focused tests (pass): `loom-code/tests/test_adversarial_backfill_pin_a2.py`.
- Evidence: `loom-code/references/engineering-baseline.md:67-70`;
  `loom-code/skills/build/SKILL.md:58-63`.

## 3. 不新增 intent 欄位、checker 規則或流程步驟；紀錄由現有的跳過紀錄與 PR 揭露承載；沒有這種指示的變更，行為完全不變。
- How I tried it:
  - `python3 loom-code/scripts/loom_checker.py --list-rules` at 620572db and
    at 88b1b83f, `diff` of the two outputs.
  - `git diff --stat 620572db 88b1b83f -- loom-code/contract/ loom-code/scripts/ loom-code/skills/ loom-code/agents/ loom-code/hooks/ loom-design/ loom-workflow/`
  - `grep version loom-code/contract/manifest.yaml` at both commits.
  - Read the existing skip record and disclosure: `build/SKILL.md:18-30`,
    `ship/SKILL.md:80`.
- What came back:
  - both rule lists 26 lines, `diff` empty (RULES_IDENTICAL).
  - diffstat empty: no skill, agent, script, hook, contract, loom-design or
    loom-workflow file changed. Changed files are the baseline paragraph,
    tests, release metadata and this change's intent/plan only.
  - contract manifest `version: 2.3.1` at both commits.
  - `tdd` is already a skippable step (`build/SKILL.md:19`); honouring it
    appends `skipped-by-instruction: <step> <YYYY-MM-DD>` to the plan's
    `## Risks` (`build/SKILL.md:28`); ship writes `Skipped by instruction:
    <steps>` into the PR (`ship/SKILL.md:80`).
  - The new paragraph is conditional on the user's instruction; with no
    instruction nothing a station or the checker does is different.
- Focused tests (pass):
  `test_loom_checker_cli.py::test_list_rules_covers_exactly_the_planned_population`,
  `test_loom_checker_cli.py::test_the_rule_population_is_twenty_six`,
  `test_adversarial_version_metadata_sync.py` (includes
  `test_contract_manifest_version_is_untouched_as_the_changelog_claims`).

## 4. 完整 package suite 全部通過，版號一致。
- How I tried it:
  - version strings: `grep '"version"'` in `loom-code/plugin.json`,
    `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`, `package.json`;
    `grep 3.30.0` in `README.md`, `loom-code/README*.md`; head of
    `loom-code/CHANGELOG.md`.
  - `python3 scripts/sync_codex_manifests.py --check --all`
  - focused pytest run (below).
- What came back: all four manifests `3.30.0`; root README (lines 17, 132)
  and the three loom-code READMEs (en/ja/zh-TW) say 3.30.0; CHANGELOG top
  entry `## [3.30.0] — 2026-10-04 — engineering baseline states the
  code-first backfill path`; sync check `rc=0`.
- Full package suite: not run here (acceptance testing leaves it to
  finalize-review, which runs it and refuses the attestation on failure).
  Suite command:
  `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`
- Focused tests (pass):
  `test_write_plan_station_text.py::test_current_release_metadata_is_synchronized`.

## Focused test run (all lines)
```
env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --no-project --python /opt/homebrew/bin/python3 --with pytest --with pyyaml python -m pytest -p no:cacheprovider -q \
 loom-code/tests/test_prose_pin_rule_text.py \
 loom-code/tests/test_adversarial_backfill_pin_a1.py loom-code/tests/test_adversarial_backfill_pin_a2.py \
 loom-code/tests/test_write_plan_station_text.py::test_current_release_metadata_is_synchronized \
 loom-code/tests/test_loom_checker_cli.py::test_list_rules_covers_exactly_the_planned_population \
 loom-code/tests/test_loom_checker_cli.py::test_the_rule_population_is_twenty_six \
 loom-code/tests/test_adversarial_version_metadata_sync.py
...........................                                              [100%]
27 passed in 0.35s
```
