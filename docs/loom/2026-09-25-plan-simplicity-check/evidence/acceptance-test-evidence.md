# Check every plan for a simpler way to reach the same outcome before Build — acceptance test evidence

Tried on 2026-09-25, in a clean copy of the project at 611c2182
(`git worktree add /tmp/at-psc 611c2182`), base main 67540c16.

## Setup
- How I tried it: the README install path (`claude plugin marketplace add https://github.com/kouko/loom-plugins.git`) fetches the published main branch and would change the machine's installed plugins, so it was not used. Instead the clean copy was used directly: `python3 loom-code/scripts/loom_checker.py --list-rules` (Python 3.12.11), and the three loom-code manifests were parsed with `json.load`.
- What came back: the checker loads and lists `plan.field-caps` with the new Simplicity check wording; `loom-code/plugin.json`, `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json` all parse and read `3.18.0`.

## 1. Before Build starts on a change, a fresh-context reviewer that did not write the plan checks it for a simpler way to reach the same Acceptance lines, and returns either no simpler shape or a concrete smaller shape.
- How I tried it: read `loom-code/skills/write-plan/SKILL.md:396-398` (pointer), `loom-code/skills/write-plan/references/plan-simplicity.md:3-13`, `loom-code/skills/closing-review/references/lenses.md:116-122` (Plan lens), `loom-code/agents/reviewer.md` (lens `plan` added to input and table). Then one cold run: a fresh `sonnet` general-purpose agent given only `plan-simplicity.md` and the Plan lens / `deletion-first` text of `lenses.md`, plus a toy intent (`greet NAME` prints `Hello, NAME`) and a toy four-task plan with a plugin registry, a YAML config loader and an abstract base class.
- What came back: the reference says write-plan dispatches one fresh-context `loom-code:reviewer` with lens `plan` before the plan commit and "the plan's author never reviews its own plan". The cold reviewer returned a concrete smaller shape: drop W0-01 (registry) and W0-02 (config loader), collapse the base class into one `greet(name)` function; "Net shape: two tasks (greet function + CLI) ... 3 fewer files/mechanisms". It asked no question.
- Evidence: the files above; cold-run output quoted above. Limit: the checker verifies the record's shape (see 2), not that the dispatch happened — a hand-written `- none found` passes.

## 2. The plan records the outcome of that check — the simpler shapes considered and whether each was taken or why not — and a plan without that record cannot enter Build.
- How I tried it: in `/tmp/at-psc-plans` wrote toy charter 1.1 plans from `loom-code/contract/templates/plan.md` and ran `python3 /tmp/at-psc/loom-code/scripts/loom_checker.py plan <file>` on each. Also ran it on this change's own plan. Read `loom-code/skills/build/SKILL.md:36-37`.
- What came back:
  - `a_record.md` (one `— taken`, one `— declined: <reason>`): exit 0
  - `b_none_found.md` (`- none found`): exit 0
  - `c_missing.md` (no section): `BLOCK plan.field-caps: Simplicity check section missing or empty (charter 1.1)`, exit 1
  - `d_empty.md` (section with only the template comment): same BLOCK, exit 1
  - `h_bad_line.md` (`- we thought about it`): `BLOCK plan.field-caps: Simplicity check#1 not '<shape> — taken' or '<shape> — declined: <reason>'`, exit 1
  - `g_charter10_missing.md` (charter 1.0, no section): exit 0 (grandfathered)
  - `docs/loom/2026-09-25-plan-simplicity-check/plan.md`: exit 0
  - Build §1: "Also at entry, run `loom_checker.py plan docs/loom/<change-id>/plan.md`; a BLOCK or any other non-zero exit stops Build until the plan passes."
- Evidence: commands and output above; tests in the targeted run below.

## 3. The check needs only loom-code installed.
- How I tried it: `grep -rn "loom-workflow\|loom_workflow"` over `plan-simplicity.md`, `lenses.md`, `agents/reviewer.md`, `loom-code/references/dispatch-profile.md`; `ls loom-code/agents`; the checker runs from `loom-code/scripts` alone.
- What came back: grep exit 1 (no match); `reviewer.md` lives in `loom-code/agents/`; the dispatched reviewer is `loom-code:reviewer`.
- Evidence: as above.

## 4. A change the checker judges narrow skips the check, and says so.
- How I tried it: same throwaway plans as 2.
- What came back:
  - `e_skip_docs.md` (`- skipped — narrow change`, Files `docs/guide.md`): exit 0
  - `f_skip_code.md` (same skip line, Files `src/toy.py`, `tests/test_toy.py`): `BLOCK plan.field-caps: Simplicity check skipped but the plan's Files are not narrow; the check is required`, exit 1
  - The skip line itself is the "says so" record in the plan; `plan-simplicity.md:4` skips the dispatch only when the section holds only that line.
- Evidence: as above; narrowness reuses `is_narrow_delta` (`loom-code/scripts/loom_checker/reviewers.py:85`).

## 5. The check never asks the user a question; adopting or declining a simpler shape is recorded as agent-decided.
- How I tried it: read `plan-simplicity.md:11-13`; watched the cold run in 1.
- What came back: "Each adoption or decline is agent-decided. This step never asks the user a question, and there is no second round." The cold reviewer returned shapes without asking anything. This change's own plan records five simplicity lines, none of them posed to the user.
- Evidence: as above.

## 6. When the adversary names an existing test as this change's adversarial program, it marks that test with its `concern:` line in the same dispatch, so finalize-review does not refuse the change for a missing line.
- How I tried it: read `loom-code/skills/closing-review/references/adversarial.md:79-83`. Demonstration in a throwaway repo `/tmp/at-psc-adv2`: committed `tests/test_existing.py` without a concern line, called `loom_checker.probes.check_adversarial_proportionate(repo, sha, 'toy', ['tests/test_existing.py'])`; then committed the same file with a first line `# concern: arithmetic regression in the reused path` and called it again.
- What came back:
  - before: `[('adversarial.proportionate', 'tests/test_existing.py carries no non-empty `concern:` line in its first 20 lines')]`
  - after: `[]`
  - The sentence now says the adversary "adds that test's line-start `concern:` comment naming the defect kind it defends against in the same dispatch and commits it"; `adversarial.md:139` says the line goes "among its first lines", matching the 20-line window (`probes.py:45`).
- Evidence: as above.

## Targeted tests
- Command: `env -u FORCE_COLOR python3 -m pytest -q loom-code/tests/test_plan_field_caps.py loom-code/tests/test_plan_simplicity_text.py loom-code/tests/test_plan_skip_missing_files.py loom-code/tests/test_adversary_protocol.py loom-code/tests/test_write_plan_station_text.py loom-design/tests/spec/test_capture_intent_contract.py`
- Result: `238 passed in 0.53s`.
- Full package suite (not run here; finalize-review runs it): `python3 scripts/run_package_tests.py --loom-family`.
