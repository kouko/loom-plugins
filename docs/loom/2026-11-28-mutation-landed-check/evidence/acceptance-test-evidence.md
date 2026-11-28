# Confirm a mutation landed before its RED counts — acceptance test evidence

Tried on 2026-11-28, in a clean copy of the project at 1e203cdd3 (full sha 1e203cdd380da47581f407043dbb9d9ea83859ad).

## Setup

- Clean copy: `git worktree add --detach <scratchpad>/at-clean 1e203cdd380da47581f407043dbb9d9ea83859ad`; `git rev-parse HEAD` printed `1e203cdd380da47581f407043dbb9d9ea83859ad`; `git status --short` was empty.
- The README's install path is `claude plugin marketplace add … && claude plugin install loom-code@loom`, which installs from the published GitHub marketplace, not from this commit. The equivalent local check: `claude plugin validate ./loom-code` printed `✔ Validation passed` and listed all eight skills (build, closing-review, engineering-research, external-review, maintain, ship, using-loom-code, write-plan) and the agents (correction from the re-run below: four agents — acceptance-tester, adversary, implementer, reviewer; the first run read a truncated listing and said "both").
- Every mutation below ran in its own fresh `cp -R` of the clean copy (`m-<name>`), applied by a helper that asserts the edit anchor matched exactly once, and was shown landed by `diff` against the clean copy. The unmutated copy passed the same tests first (see 1).
- Test runs used `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID python3 -m pytest …`. The full package suite was not run; `finalize-review` runs it.

## 1. 共用的測試標準檔中有一條規則：用故意改壞讓測試失敗來證明測試有效時，必須先確認改動確實生效（與原始版本比對有差異，或要改的那段文字剛好比對到一次），也確認沒改的版本會通過；沒確認的失敗不能當作證據。
- How I tried it: read `loom-code/references/tests-standard.md` §1 in the clean copy; `grep -rn "mutation landed\|unmutated version\|pristine copy" loom-code loom-design loom-workflow` (excluding CHANGELOG and tests).
- What came back: `loom-code/references/tests-standard.md:16-23`, inside "## 1. A test can fail for the behaviour it names":
  "Whoever forces a RED by deliberately mutating code, a fixture or text must confirm, before counting it as evidence, that the mutation landed — a non-empty diff against the pristine copy, or the edit anchor matched exactly once — and that the unmutated version passes. An unconfirmed RED is not evidence. / The diff or the matched anchor must lie in the code, fixture or text the test covers."
  The grep found these phrases only in that file (lines 17-19).
- Evidence: the two alternatives (diff vs. anchor once), the unmutated-pass check and "not evidence" are all present. Baseline run: `pytest loom-code/tests/test_tests_standard_text.py loom-code/tests/test_write_plan_station_text.py::test_current_release_metadata_is_synchronized -q` → `6 passed in 0.19s`.

## 2. implementer 讀的 engineering baseline 中，False-green diagnostic 與 Code-first backfill 這兩處「改壞看失敗」的指示都指向這條規則，不另外重述。
- How I tried it: read `loom-code/references/engineering-baseline.md` around both paragraphs.
- What came back:
  - `engineering-baseline.md:44-49` (False-green diagnostic): "… re-run — it must fail. That failure is evidence once it meets the mutation rule in [`tests-standard.md`](tests-standard.md) §1. If it still passes, …"
  - `engineering-baseline.md:67-77` (Code-first backfill, heading at line 67): "… break the covered behaviour and watch the test fail (false-green diagnostic) to show it catches a defect. The mutation rule in [`tests-standard.md`](tests-standard.md) §1 decides when that failure counts."
  - Neither paragraph restates diff / anchor / unmutated-pass; the grep in 1 found no copy in the baseline.
- Evidence: mutation `m-restate` appended "You must confirm, before counting it as evidence, that the mutation landed." to the False-green paragraph (anchor matches: 1; diff showed line 49 changed) → `1 failed, 4 passed`, `AssertionError: restated in baseline: must confirm, before counting it as evidence, that the mutation landed`. Mutation `m-drop-baseline-ptr1` removed the False-green pointer (anchor matches: 1; diff lines 45-47) → `1 failed, 4 passed`, `AssertionError: That failure is evidence once it meets the mutation rule in [`tests-standard.md`](tests-standard.md) §1.` The Code-first backfill pointer is pinned by the same loop (`BASELINE_MUTATION_POINTERS` in `loom-code/tests/test_tests_standard_text.py`); I did not mutate it separately.

## 3. adversary 更新對抗程式時要附的改壞證據規則指向同一條，並要求報告寫出確認改動生效的方式。
- How I tried it: read `loom-code/skills/closing-review/references/adversarial.md:118-130` (the probe-update mutation-evidence paragraph); checked the relative link resolves (`ls loom-code/skills/closing-review/references/../../../references/tests-standard.md` succeeded).
- What came back: "Each mutation must turn the probe RED and is then reverted, and the report gives each one's command, observed result and how the mutation was confirmed landed, as `../../../references/tests-standard.md` §1 requires."
- Evidence: mutation `m-drop-adv-ptr` cut the sentence back to "… command, observed result." (anchor matches: 1; diff lines 126-127) → `1 failed, 4 passed`.

## 4. 把這條規則刪掉、或把「必須確認」改成「可以略過」時，package suite 會有測試失敗。
- How I tried it: on separate copies of the clean tree, applied each mutation, confirmed it landed (anchor matched once + `diff` against the clean copy), ran `pytest loom-code/tests/test_tests_standard_text.py -q`.
- What came back:
  | Copy | Mutation in `tests-standard.md` | Result |
  |---|---|---|
  | m-delete-rule | removed the whole rule paragraph (diff 16,21d15) | 1 failed, 4 passed — `AssertionError: must confirm, before counting it as evidence, that the mutation landed` |
  | m-must-to-may | "must confirm" → "may skip confirming" (diff 16,17c16) | 1 failed, 4 passed — same assertion |
  | m-notevidence | "is not evidence" → "is still evidence" (diff 19c19) | 1 failed, 4 passed — `AssertionError: An unconfirmed RED is not evidence.` |
  | m-drop-target | "must lie in the code, fixture or text the test covers" → "may lie anywhere" (diff 22,23c22) | 1 failed, 4 passed — `AssertionError: The diff or the matched anchor must lie in the code, fixture or text the test covers.` |
  The unmutated clean copy passed the same file (see 1).
- Evidence: the file is under `loom-code/tests/`, which `scripts/run_package_tests.py` `TEST_ROOTS` includes (its `code` group), so the package suite picks it up. Suite command (run later by finalize-review): `python3 scripts/run_package_tests.py --loom-family`.

## 5. loom-code 發布新版號，CHANGELOG 寫明這條規則。
- How I tried it: read the four loom-code manifests' `version`, `loom-code/CHANGELOG.md` top entry, the three loom-code READMEs and the root README; ran the release pin test; mutated the SSOT version back.
- What came back: `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`, `plugin.json`, `package.json` all `3.92.0`. CHANGELOG: `## [3.92.0] — 2026-11-28 — Confirm a mutation landed before its RED counts`, first bullet states the rule (diff or anchor once, in what the test covers, unmutated passes, unconfirmed RED is not evidence), then the baseline and adversarial pointer bullets. READMEs: `loom-code/README.md:15`, `README.ja.md:15`, `README.zh-TW.md:13`, root `README.md:17` and `:105` all say 3.92.0.
- Evidence: `test_current_release_metadata_is_synchronized` passed on the clean copy; mutation `m-stale` set `.claude-plugin/plugin.json` back to `3.91.0` (anchor matches: 1; diff 3c3) → failed with `AssertionError: assert '3.91.0' == '3.92.0'`.

## Re-run on 2026-11-28, at 77cf89993 (full sha 77cf8999365deb0a50776798c3b62c67ba71c861)

Fix range f8e5c229ad19dad2f34813042aa67fa4569f0bf9..77cf8999365deb0a50776798c3b62c67ba71c861 (one commit, 77cf89993): `loom-code/references/tests-standard.md` §1 second paragraph now reads "The diff or the matched anchor must lie in the code, fixture or text the test covers, and a matched anchor counts only once the edit was applied there and the text changed. A mutation tool that applies and checks its own mutants already meets this rule."; `loom-code/tests/test_tests_standard_text.py` adds two `MOVED_RULES` literals ("must lie in the code, fixture or text the test covers", "and that the unmutated version passes") and repins the §1 sentences. Rows 1 and 4 read the rule text directly; rows 2 and 3 rest on `test_moved_rules_stated_once_in_standard_only`, whose restatement loop over baseline and adversarial gained the two literals; row 5 asks the CHANGELOG to state the rule, which changed. Every row was therefore re-tested in full.

Setup: `git worktree add --detach <scratchpad>/at2 77cf8999365deb0a50776798c3b62c67ba71c861`; HEAD printed the full sha; `git status --short` empty. `claude plugin validate ./loom-code` → `✔ Validation passed`, 8 skills, 4 agents (acceptance-tester, adversary, implementer, reviewer). All four manifests `3.92.0`. Unmutated: `pytest loom-code/tests/test_tests_standard_text.py loom-code/tests/test_write_plan_station_text.py::test_current_release_metadata_is_synchronized -q` → `6 passed in 0.18s`. Each mutation below ran in its own `cp -R` copy (`r2-<name>`), helper asserted `anchor matches: 1`, `diff` against the clean copy shown; command `pytest loom-code/tests/test_tests_standard_text.py -q`.

- 1: re-tested — `tests-standard.md:16-25` holds both paragraphs (quoted above and in section 1). `grep -rn "mutation landed\|unmutated version\|pristine copy\|own mutants\|edit was applied" loom-code loom-design loom-workflow` (excluding CHANGELOG and tests) → only `tests-standard.md:17,18,19,23,24`.
- 2: re-tested — False-green pointer at `engineering-baseline.md:45-47`, Code-first backfill pointer at `:76-77`. `r2-restate-baseline` (diff 49c49) → `AssertionError: restated in baseline: must confirm, before counting it as evidence, that the mutation landed`; `r2-drop-baseline-ptr1` (diff 45,47c45) → `AssertionError: That failure is evidence once it meets the mutation rule in [`tests-standard.md`](tests-standard.md) §1.`; `r2-drop-baseline-ptr2` (diff 76,77c76) → `AssertionError: The mutation rule in [`tests-standard.md`](tests-standard.md) §1 decides when that failure counts.` Each 1 failed, 4 passed.
- 3: re-tested — `adversarial.md:124-127` unchanged sentence; `ls loom-code/skills/closing-review/references/../../../references/tests-standard.md` resolves. `r2-drop-adv-ptr` (diff 126,127c126) → 1 failed, 4 passed; `r2-restate-adv-new` appended "The anchor must lie in the code, fixture or text the test covers." (diff 127c127) → `AssertionError: restated in adversarial: must lie in the code, fixture or text the test covers`.
- 4: re-tested — mutations of `tests-standard.md`, each 1 failed, 4 passed:
  | Copy | Mutation | diff | Assertion |
  |---|---|---|---|
  | r2-delete-rule | first paragraph removed | 16,21d15 | `must confirm, before counting it as evidence, that the mutation landed` |
  | r2-delete-both | both paragraphs removed | 16,20d15 22,26d16 | same |
  | r2-must-to-may | "must confirm" → "may skip confirming" | 16,17c16 | same |
  | r2-notevidence | "is not evidence" → "is still evidence" | 19c19 | `An unconfirmed RED is not evidence.` |
  | r2-drop-unmutated | " — and that the unmutated version passes." → " —." | 19c19 | `and that the unmutated version passes` |
  | r2-drop-target | "must lie in the code, fixture or text the test covers," → "may lie anywhere," | 22,23c22 | `must lie in the code, fixture or text the test covers` |
  | r2-drop-applied | removed ", and a matched anchor counts only once the edit was applied there and the text changed" | 23,24c23 | full second-paragraph sentence |
  | r2-widen-exempt | exemption → "Any mutation tool already meets this rule." | 24,25c24 | `A mutation tool that applies and checks its own mutants already meets this rule.` |
  The test file is under `loom-code/tests/`, inside `TEST_ROOTS` of `scripts/run_package_tests.py`. Suite command (finalize-review): `python3 scripts/run_package_tests.py --loom-family`.
- 5: re-tested — manifests and READMEs (`loom-code/README.md:15`, `README.ja.md:15`, `README.zh-TW.md:13`, root `README.md:17`, `:105`) all 3.92.0; CHANGELOG top entry `## [3.92.0] — 2026-11-28 — Confirm a mutation landed before its RED counts` unchanged by the fix. `r2-stale` (`.claude-plugin/plugin.json` 3.92.0 → 3.91.0, diff 3c3) → `AssertionError: assert '3.91.0' == '3.92.0'`. Observation: the CHANGELOG bullet does not mention the fix's two additions (anchor counts only once the edit was applied; self-checking mutation tools already meet the rule).
