# Close the open follow-ups left by the last four loom changes — acceptance test evidence

Tried on 2026-09-24, in a clean copy of the project at 84f546dc (`git worktree add --detach <scratch>/head 84f546dc`).
Trunk control: a clean copy at 710814a9 (`git worktree add --detach <scratch>/trunk 710814a9`).

## Setup check
- How I tried it: the README installs from the published marketplace (`claude plugin install loom-code@loom`), which would give the released 3.13.0, not this branch. I loaded the branch the local way: `claude -p --plugin-dir <scratch>/head/loom-code` (Claude Code 2.1.281), asking a haiku session to invoke `loom-code:closing-review` and quote the fix-list sentence.
- What came back: init event `plugins: [{"name": "loom-code", "path": "<scratch>/head/loom-code", "source": "loom-code@inline", "version": "3.14.0"}]`; skill `Base directory for this skill: <scratch>/head/loom-code/skills/closing-review`; the quoted sentence is the new wording ("…returned on the content the reviewers just read, including the committed acceptance test report, into one list."). The installed user-scope 3.13.0 did not shadow it. Cost USD 0.061.
- Every trial below was checked the same way: A1/A2 runs' init events name the `head` or `trunk` path and version 3.14.0 / 3.13.0 and each invoked the Skill tool with the base directory of its own arm.

Covering tests (not the package suite), run in the clean copy:
`python3 -m pytest -q loom-code/scripts/test_fix_scope_text.py loom-code/scripts/test_fix_handoff_text.py loom-code/scripts/test_acceptance_test_report_shape.py loom-code/scripts/test_probes_language_policy.py loom-code/scripts/test_write_plan_station_text.py`
→ `100 passed in 0.34s`. The package suite is executed later by `finalize-review` (not skipped), which refuses the attestation on failure; command recorded per the plan: the repo's package-level pytest run.

Trials: `claude -p --plugin-dir <arm>/loom-code --model sonnet --no-session-persistence --output-format stream-json --verbose --max-budget-usd 2 --permission-mode bypassPermissions` (no `--disable-slash-commands`), one run per arm. Seeds are reproduced under each line.

## 1. The fix-round paragraph in closing review names the acceptance-testing findings on the content the reviewers just read, including the committed acceptance test report, so no reading of it leaves them out.
- Text: `loom-code/skills/closing-review/SKILL.md:293-296` now reads "…returned on the content the reviewers just read, including the committed acceptance test report, into one list." (was "…on the current functional-content digest…").
- Seed (both arms, same text): station for change `2026-09-20-csv-export`; Build handed off at a1 (digest D1); tester ran at a1 and returned an important finding "exporting an empty table writes no header row"; its report was committed as a2 (digest now D2); reviewers read D2, code reviewer NEEDS_REVISION with important "the CSV writer does not quote commas inside cell values (export.py:41)", docs reviewer PASS + nit. Question: which findings go on the fix list and how grouped. No other tool, no dispatch.
- HEAD (3.14.0, skill loaded from `<scratch>/head/...`, USD 0.172): fix list = both important findings, nit excluded, two separate hand-offs; says "Acceptance finding is included even though it came from a1" and quotes the new sentence.
- Trunk control (3.13.0, USD 0.184): also both findings, two hand-offs; reasons the report commit put the finding on D2, quoting the old sentence.
- Reading: HEAD behaves as the line requires. No before/after difference on this seed at n=1 — the trunk reader did not take the literal digest reading either.
- The station's suggested seed (report committed after the reviewers started) was replaced by the normal order (report committed, then reviewers read), because that is the order the intent's Problem row names and the skill requires.
- Covering tests: `test_fix_scope_text.py` / `test_fix_handoff_text.py` in the 100-pass run above.

## 2. Closing review lists, among what it hands the acceptance tester, every important-or-worse finding it decided not to act on.
- Text: `SKILL.md:218-220` adds "Also hand it every finding of severity `important` or worse that the main agent dismissed."
- Seed: change `2026-09-21-api-retry`; round 1 code reviewer important F1 "timeout error message omits the URL (client.py:52)" (fixed in b3..b4) and F2 "retry loop has no backoff (client.py:88)" dismissed by the main agent because the Constraints forbid sleeps; re-dispatch the tester, neither package-tests nor finalize-review skipped. Task: write the dispatch prompt verbatim.
- HEAD (USD 0.186): prompt carries a section "F2 (dismissed by the main agent): … Reason for dismissal: the intent's Constraints forbid adding sleeps to the client. Do not treat the missing backoff as a defect … If you think the dismissal contradicts an Acceptance line, say so in the report", plus skip status, earlier report/evidence paths and `b3..b4`.
- Trunk control (USD 0.185): prompt names F1, skip status, paths and range; F2 and its dismissal appear nowhere.
- Reading: clear before/after difference; the change closes the gap it targets.

## 3. The implementer contract states that a fix hand-off listing several instances of one defect class is one task, not a reason to return `BLOCKED`.
- Text: `loom-code/agents/implementer.md:30-32` adds "A fix hand-off that lists several instances of one defect class is one task, a single assertion about that class."
- Load check (`--agent loom-code:implementer`, asked to quote rule 1 from its own instructions, USD 0.125 each): HEAD quoted the new sentence; trunk quoted only "In a fix hand-off, the instances it lists and their files are the task's scope." So each arm ran its own contract.
- Seed: a two-file Python repo (`app/users.py` register()/login(), `app/invites.py` accept_invite()), hand-off class "email inputs are compared without trimming surrounding whitespace", three instances across the two files; `claude -p --agent loom-code:implementer` in that repo.
- HEAD (USD 0.241): `status: DONE`, one commit 34e8ceb touching `app/users.py`, `app/invites.py`, `tests/test_basic.py`; three failing tests written first ("3 failed, 2 passed"), then 5 passed; self-review: "This was one class, so I made one commit with one test per instance."
- Trunk control (USD 0.238): also `status: DONE`, one commit 89f7994, 6 passed.
- Reading: HEAD proceeds as required; the trunk text did not refuse this seed either (no difference at n=1).

## 4. No test outside the checker's own tests pins the checker's rule count as a literal.
- `grep -rnE "(==|!=|>=|<=)\s*26\b|\b26\s*==" --include='test_*.py' <head> | grep -v test_loom_checker_` → no output.
- Same grep on trunk → `test_probes_language_policy.py:351`, `test_fix_handoff_text.py:96`, `test_fix_scope_text.py:81` (the three pins removed).
- Remaining pins are in the checker's own tests: `test_loom_checker_cli.py:313`, `test_loom_checker_modules.py:45`.
- Guard: `test_fix_scope_text.py:123` `test_no_literal_rule_count_outside_checker_tests`, with negatives at :131 and :142 (their samples build the operator from `{eq}`, so they carry no literal pin); passed in the covering run. Its docstring says the recognition is partial (a count held in a variable passes unseen); my grep is the independent check.

## 5. The recovery-rule probe that is red on main passes, with the cause recorded as either wrong station prose or a wrong probe expectation.
- From repo root: `python3 -m pytest -q loom-code/skills/closing-review/probes/` → `13 passed in 0.10s`.
- From `loom-code/`: `python3 -m pytest -q skills/closing-review/probes/` → `13 passed in 0.10s`.
- Trunk control: `…/probes/test_recovery_rules.py` → `RL-06 FAIL: paragraph 'Stop and ask when producing an absent item needs' is missing ['expert-mode']`, `1 failed, 11 passed`.
- Cause recorded as a wrong probe expectation: commit c3f70a86 message ("PR #43 (b568ba1a) intentionally changed … The RL-06 probe still pinned the old expert-mode ending and went stale unnoticed because the package suite does not collect loom-code/skills/closing-review/probes/") and `loom-code/CHANGELOG.md:23-24`.
- The package suite still does not collect this probes directory (plan Risk 2, out of scope).

## 6. The repository memory store holds the PR #50 lesson — the measured time saving, the cost increase and why reviewers must keep reading the report — with its index entry.
- Entry: `docs/loom/memory/parallel-acceptance-testing-and-review-costs-more-than-it-saves.md` — time saving "54 s against 116 s — the real effect, about one minute"; cost "USD 3.05 against 2.35 (+30%); tokens +47%"; why reviewers keep reading: "reviewers found 8 important errors inside acceptance test reports; 7 were invisible to a reader of the report alone" and "Dropping the reviewers' read of the report instead would remove the check that caught 7 errors".
- Index: `docs/loom/memory/index.md` gains one line for the entry.
- `python3 loom-workflow/skills/loom-memory/scripts/loom_memory.py validate docs/loom/memory` → `loom_memory validate: OK — OKF v0.2-compatible Loom memory profile holds.`
- `regenerate-index` on a scratch copy of the store, then `diff` against the committed `index.md` → identical.

## 7. The checker's rule list does not grow and no new step, reviewer or dispatch is added.
- `python3 loom-code/scripts/loom_checker.py --list-rules | wc -l` → 26 on HEAD and on trunk; `diff` of the two lists → identical.
- `python3 loom-code/scripts/check_mechanisms.py` → `net mechanism count (excl. host-hygiene): 140`, `all clear`; output identical to trunk.
- `grep -c "gate:" loom-code/skills/closing-review/SKILL.md` → 4 on both.
- Diff of `SKILL.md`: one sentence added to the existing tester dispatch paragraph and one phrase replaced in the fix-list paragraph; `implementer.md`: one sentence. No new step, reviewer or dispatch.
- `test_write_plan_station_text.py` (release metadata sync, 3.14.0) passed in the covering run.

## Cost
Nine `claude -p` runs: load check 0.061, A1 0.172 + 0.184, A2 0.186 + 0.185, A3 0.241 + 0.238, A3 load checks 0.125 + 0.125 → USD 1.52 total.
