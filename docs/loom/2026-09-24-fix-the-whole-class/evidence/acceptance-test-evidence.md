# Fix rounds fix the whole class of a finding — acceptance test evidence

Tried on 2026-09-24, in a clean copy of the project at 706ea36b.

Scratch root below: `/private/tmp/claude-501/-Users-kouko-GitHub-loom-plugins/3e0c28a5-8a45-4b2c-9db3-458c53cd9e9f/scratchpad` (written `$S`).

## Setup check
- How I tried it: `git worktree add --detach $S/wt-head 706ea36b` and, for the control, `git worktree add --detach $S/wt-main main` (main at e359c246). The README's install path (`claude plugin marketplace add https://github.com/kouko/loom-plugins.git`) installs what is published on main, not this branch, so the branch was loaded the way the Claude Code CLI loads an unpublished plugin: `claude -p ... --plugin-dir $S/wt-head/loom-code` (control: `--plugin-dir $S/wt-main/loom-code`). No `--disable-slash-commands`.
- What came back: every session's `init` event listed `loom-code` at `$S/wt-head/loom-code`, `source: loom-code@inline`, `version: 3.12.0` (control sessions: `$S/wt-main/loom-code`, `3.11.0`). Every session called `Skill {"skill": "loom-code:build"}` and the tool result began `Base directory for this skill: $S/wt-head/loom-code/skills/build` (control: `wt-main`). The sentence "Before any fix is handed to an implementer" is present in the loaded skill text in all 4 branch sessions and absent in all 4 control sessions.
- Evidence: transcripts `$S/fs-{rule1,rule2,ctl1,ctl2,h-rule1,h-rule2,h-ctl1,h-ctl2}.jsonl`; summarizer `$S/fs_summarize.py`. Claude Code 2.1.281, model `claude-opus-5-5[1m]`.

## 1. Before a fix is handed to an implementer, the orchestrator names the defect's class and searches the whole change for other instances of it — including every surface named by the Acceptance line the finding maps to — and the fix hand-off lists every instance found, the flagged one included.
- How I tried it: in `$S/wt-head/loom-code/scripts`, `python3 -m pytest -q test_fix_scope_text.py`; then the trials in section 3 (the behaviour this line describes is what those trials exercise).
- What came back: `5 passed in 0.19s` (`test_rule_names_class_search_and_acceptance_surfaces`, `test_record_states_class_and_places_searched_even_when_none_found`, `test_weakened_rule_fails_the_pins`, `test_pointers_reach_every_fix_path`, `test_no_gate_marker_rule_count_26_or_dispatch_wording`). In all 4 branch trials the hand-off has a "Defect class" heading, a "Places searched" list naming `git diff --name-only main...HEAD` and the Acceptance line's surfaces, and an instance table with the flagged instance marked and every sibling listed.
- Evidence: named tests above; rule text `loom-code/skills/build/SKILL.md:69-79`; transcripts `fs-rule1/2.jsonl`, `fs-h-rule1/2.jsonl`. Full suite (`python3 -m pytest` over `loom-code/scripts`, run by `finalize-review`) not run here, per the tester contract.

## 2. The fix's record (its hand-off and commit message) states the class and the places searched, so a reader can see siblings were looked for even when none were found.
- How I tried it: the same `test_fix_scope_text.py` run (the "even when the flagged instance is the only one found" clause is pinned by `test_record_states_class_and_places_searched_even_when_none_found`, and a negated variant is rejected by `test_weakened_rule_fails_the_pins`); read the commit-message requirement out of each trial hand-off.
- What came back: 5 passed. All 4 branch hand-offs state the class and the places searched, and all 4 require the implementer's commit message to state class, places searched and instances (rule1 and h-rule1 give a full example message with `Defect class:` / `Searched:` / `Places searched:` lines; rule2 and h-rule2 list them as "Commit message requirements"). Control hand-offs: ctl1, h-ctl1, h-ctl2 state no class heading and no places searched; ctl2 mentions "same defect class as the finding" in task titles but no places searched; no control asks the commit message to record either.
- Evidence: named tests above; transcripts. Limit: no actual commit was made (the trial asked for the hand-off only), and no trial had a finding with zero siblings, so the none-found case rests on the pinned text, not on a trial.

## 3. Given a finding that names one instance while siblings of the same defect exist elsewhere in the change, an agent following the station text produces a fix hand-off that covers the siblings, shown by a trial run on such a case.
- How I tried it: two seeded git repos, each a `main` commit plus one feature-branch commit, cloned once per session (`$S/trial-*`). Prompt: `$S/fixscope-prompt.txt` / `$S/fixscope-prompt2.txt` — "Use the loom-code:build skill. You are the main agent in the Build station … Closing review returned this finding … Prepare the fix hand-off you would give the implementer … Do not implement … Print the complete hand-off." Command per session (from `$S/fixscope-trials.sh`, `$S/fixscope-trials2.sh`): `claude -p "$P" --plugin-dir <loom-code> --output-format stream-json --verbose --allowedTools "Read,Grep,Glob,Bash(git *),Bash(grep *),Skill" --disallowedTools "Edit,Write,Agent,NotebookEdit"`. Each case run twice on the branch and twice on main as control.
  - Case A (easy): SQL built from caller input in `app/reports.py:6` (f-string, flagged), `app/reports.py:11` (`+`), `app/users.py:10` (`%`); the finding maps to Acceptance 1, which itself names all three lookups. Distractor outside the change: `app/legacy.py:5`.
  - Case B (hard): same defect in `app/reports.py:9` (flagged, Acceptance 1), `app/audit.py:6` (Acceptance 2), `app/search.py:5` (Acceptance 3); the finding's Acceptance line names only the order lookup. Same distractor.
- What came back:

  | Session | Plugin | Instances in the hand-off's scope | Class stated | Places searched stated |
  |---|---|---|---|---|
  | A rule1 | branch 3.12.0 | 3 of 3 | yes | yes |
  | A rule2 | branch 3.12.0 | 3 of 3 | yes | yes |
  | A ctl1 | main 3.11.0 | 3 of 3 | no | no |
  | A ctl2 | main 3.11.0 | 3 of 3 (as three separate hand-offs) | informal | no |
  | B rule1 | branch 3.12.0 | 3 of 3 | yes | yes |
  | B rule2 | branch 3.12.0 | 3 of 3 | yes | yes |
  | B ctl1 | main 3.11.0 | 1 of 3 — "Do not edit app/audit.py, app/search.py … tracked separately" | no | no |
  | B ctl2 | main 3.11.0 | 1 of 3 — "Leave app/audit.py, app/search.py … as they are" | no | no |

  All 8 sessions left `app/legacy.py` out (branch sessions: "outside the search bound"). `git status --short` empty and HEAD unchanged in every trial clone afterwards (nothing edited or committed).
- Evidence: transcripts `$S/fs-*.jsonl`; seeds `$S/seed`, `$S/seed2`; seed sources `$S/seed-src`, `$S/seed2-src`. Cost per session $0.41–0.52, 5–8 turns.

## 4. The rule is carried by station prose; the checker's rule list does not grow and no new step, reviewer or dispatch is added.
- How I tried it: `python3 loom_checker.py --list-rules | wc -l` in both worktrees; `python3 loom-code/scripts/check_mechanisms.py --baseline main` in `wt-head`; `git diff main...HEAD -- loom-code/skills loom-code/agents | grep '^+' | grep -iE "gate|dispatch|subagent|step"`; `test_fix_scope_text.py::test_no_gate_marker_rule_count_26_or_dispatch_wording`; `test_write_plan_station_text.py -k synchronized`; `test_simplified_station_text.py`.
- What came back: 26 rules on main and on the branch; `prose-gate 20 20`, `net mechanism count (excl. host-hygiene): 140`, `baseline net count: 140`, `all clear`; the grep found no added line (exit 1); `1 passed, 48 deselected`; `54 passed`. Added prose: one paragraph in Build §2, one sentence in closing-review, one sentence in Ship, one sentence in the implementer contract.
- Evidence: commands and outputs above.
