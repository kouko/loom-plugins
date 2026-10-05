# Close the three deep-module follow-ups — acceptance test evidence

Tried on 2026-10-05, in a clean copy of the project at e338a750
(`git worktree add --detach <scratchpad>/at-wt HEAD`; nobody had worked in it).

## Setup

- How I tried it: followed the root README's only setup step for working on
  this repository (README.md:274), from the clean copy:
  `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`
- What came back: the lock installed and the suite ran to the end, `EXIT=0`.
  The installable surface of the change is prose read by agents plus test
  files; no install step beyond the lock is needed.

## Expected answers, written before any reader ran (18:23:21)

```
A1-a version-bump-only task, Files line marks no entry -> NOT asked to mark an entry
A1-b config-only task, Files line marks no entry -> NOT asked to mark an entry
A1-c task changing a function's behaviour, no entry marked -> finding
A1-d task adding a new module with a callable function, no entry marked -> finding
Control (base 1a792fe1 text): A1-a and A1-b expected to be flagged under the old wording.
A3 example doc review note -> reason = the wrappers change for the same reason, not count alone.
```

## 1. closing review 不會要求只改設定檔、manifest、版號字串或文件的 task 標入口，改到可被呼叫的程式行為的 task 仍會被要求；用範例 task 試，只 bump 版號的 task 不被要求標入口，改函式行為卻沒標入口的 task 仍被抓。

- How I tried it: four example plan tasks (scratchpad `case-a.md` … `case-d.md`),
  each handed to its own fresh-context `sonnet` reader together with the clean
  copy's `loom-code/skills/closing-review/references/lenses.md`, told to read only
  those two files and apply the `tests` row. Question asked of each: "must this
  task's plan Files line mark the module entry (would you raise a finding because
  its Files line marks no entry)?"
  - a: version bump in pyproject.toml, `__version__` string, CHANGELOG
  - b: two YAML config values changed, no code
  - c: `round_total` body switched to half-up rounding; called by `Cart.total()`, which other packages import
  - d: new module `slack.py` with public `send_slack` (a later task's dispatcher calls it) and private `_build_payload`
- What came back:

| case | expected | reader answer | clause quoted |
|---|---|---|---|
| a version bump | no | `ENTRY FINDING: NO` | "a task adding or changing a function's behaviour whose plan Files line marks no entry is a finding" — "changes no function's behaviour" |
| b config only | no | `ENTRY FINDING: NO` | same clause — "only YAML config values … no function's behaviour is added or changed" |
| c function behaviour | finding | `ENTRY FINDING: YES` (first line said NO, then the reader corrected itself) | same clause |
| c re-run 1 | finding | `ENTRY FINDING: YES` | same clause plus the entry definition |
| c re-run 2 | finding | `ENTRY FINDING: YES` | same clause |
| d new module | finding | `ENTRY FINDING: YES` | entry definition + same clause |

- Control: the same cases a and b against the base text (`git show 1a792fe1:…/lenses.md`)
  also came back `ENTRY FINDING: NO` from two fresh readers ("there is no module
  entry for the Files line to mark"). So my pre-written control expectation was
  wrong: these readers did not mis-apply the old wording either. This does not
  change the Acceptance 1 result, which concerns the new text, but it means this
  trial does not show a reader who would have been wrong before.
- Note on case c: the first reader wrote NO on its answer line and then reversed
  to YES in its own reasoning. Two more independent readers, asked to reason
  first, both said YES. The three readers did not agree on which function is the
  entry (`round_total` or `Cart.total()`), but all three raised the
  missing-entry finding.
- Evidence: lenses.md:54 (`tests` row, clause "a task adding or changing a
  function's behaviour whose plan Files line marks no entry is a finding");
  the reader answers quoted above.

## 2. 釘住 write-plan 入口定義的測試，遇到用 `cannot`（及同類否定縮寫）把入口定義反過來的句子會失敗；對目前 write-plan 的正確文字仍然通過。

- How I tried it:
  1. Loaded the pin's own judging function from the clean copy and fed it
     (a) the current write-plan Task size paragraph, (b) a stand-alone inverted
     sentence `Files marks the entry, which <neg> be the function other modules call.`,
     and (c) the real write-plan paragraph with "the entry other modules call"
     rewritten to "the entry other modules <neg> call", for `<neg>` = `cannot`,
     ASCII `can't` and curly `can’t` (scratchpad `a2_check.py`).
  2. For each of the three inversions, copied the pin test next to an inverted
     copy of write-plan's SKILL.md and ran the real pin test with pytest.
  3. Ran the pin's two test files on the unmodified clean copy.
  4. Control: the base pin (`git show 1a792fe1:loom-code/tests/test_write_plan_entry_definition.py`)
     on the three stand-alone sentences.
- What came back:

```
current write-plan text accepted: True
'cannot'   sentence accepted: False  | inverted write-plan text accepted: False
"can't"    sentence accepted: False  | inverted write-plan text accepted: False
'can’t'    sentence accepted: False  | inverted write-plan text accepted: False

== inverted with cannot   -> FAILED test_taskentry_skilltext_definedbyoutsidecallers; 1 failed, 3 passed
== inverted with can't    -> FAILED test_taskentry_skilltext_definedbyoutsidecallers; 1 failed, 3 passed
== inverted with can’t    -> FAILED test_taskentry_skilltext_definedbyoutsidecallers; 1 failed, 3 passed

unmodified: pytest test_write_plan_entry_definition.py test_write_plan_entry_definition_curly.py -> 6 passed

base pin control: cannot accepted: True; can't accepted: False; can’t accepted: True
```

- Evidence: the outputs above; `loom-code/tests/test_write_plan_entry_definition.py:22`
  (NEGATION now includes `cannot` and `n['’]t`), `:32-38` (clause split on `.` and `;`);
  the current paragraph's legitimate "logic that entry cannot reach" sits in a
  separate `;` clause, which is why the correct text still passes.

## 3. 範例文件中要求抽出共用程式的審查意見，理由改為那幾處會因同一個理由一起改，不再只憑出現次數。

- How I tried it: one fresh-context `sonnet` reader given only
  `loom-code/docs/examples/swift-network-layer.md`, asked to find every place a
  review asks for (or the retrospective endorses) extraction and classify the
  stated reason as (A) same reason to change, (B) count alone, (C) both/unclear,
  then state the rule an agent would learn. Plus
  `grep -n -i -E "rule.of.three|three times|3 times|extract"` on the file.
- What came back:
  - Reader: line 266 → A ("the 4 wrappers change for the same reason, since any
    change to cancellation or resume handling must hit all of them together");
    line 282 → A; line 234 → C (bare "extract common continuation wrapper —
    omitted for brevity", gives no reason). Rule learned: "Extract shared code
    when the sites must change together for the same reason … Seeing the
    pattern repeat is not itself the trigger."
  - grep: no "Rule of Three" / "three times" left; matches only at 234, 266, 282.
- Evidence: swift-network-layer.md:266, :282.

## 4. 完整 package suite 全部通過；三份 manifest、README 的版號字串與 CHANGELOG 新區段一致。

- How I tried it: the full suite command from the Setup section, in the clean
  copy; then read every version string:
  `python3 -c "json.load(...)['version']"` on the four manifests,
  `grep -n "3\.34\.[01]"` on the READMEs and the version pin test,
  `grep -n -m2 "^## \["` on the CHANGELOG, `git grep -n "3\.34\.0" -- ':!docs' ':!**/CHANGELOG.md'`.
- What came back:
  - Suite: `EXIT=0`; pytest groups `1906 passed, 2 skipped`, `190 passed, 1 skipped`,
    `53 passed`, `260 passed`, `121 passed`, `64 passed`, `22 passed`, `13 passed`,
    `1 passed`, `71 passed, 3 skipped`, `201 passed, 5 skipped`, `12 passed`,
    `155 passed`; shell-test summaries all `0 FAIL`; no `failed` line anywhere in the log.
  - Versions: loom-code/plugin.json, .claude-plugin/plugin.json,
    .codex-plugin/plugin.json, package.json all `3.34.1`; README.md:17 and :132,
    loom-code/README.md:11, README.ja.md:11, README.zh-TW.md:9 all `3.34.1`;
    CHANGELOG top section `## [3.34.1] — 2026-10-05 — …`; version pin
    `CURRENT_VERSION = "3.34.1"`. The only leftover `3.34.0` outside docs and
    changelogs is an unrelated `cytoscape ^3.34.0` dependency in
    loom-workflow/tests/mermaid/package-lock.json. `.claude-plugin/marketplace.json`
    carries no version field.
- Evidence: the suite log and grep outputs above.
