# Goal-create prompt and native activation boundary — acceptance test evidence

Tested on 2026-09-27 in a fresh local clone at `eef456ba` (`/private/tmp/loom-goal-acceptance-20260927`). The clone had a clean status before testing. The tester did not call `create_goal`, `ProposeGoal`, or `/goal` and did not install the plugin into either active host. These are focused tests and structural checks, not real host activation.

## Setup and test record

- Clean copy: `git clone --local --no-hardlinks --no-checkout . /private/tmp/loom-goal-acceptance-20260927`, then `git -C /private/tmp/loom-goal-acceptance-20260927 checkout --detach eef456bade16b93891eea94428738e6829c6625c`; output ended with `HEAD is now at eef456ba` and `git status --short` was empty.
- README setup check: `agy plugin validate ./loom-workflow` in the clone returned exit 0, `[ok] ./loom-workflow`, `skills: 12 processed`, and `hooks: 1 processed`. This validates the local plugin package without installing it into the user's host.
- README's isolated test environment was attempted with `uv run --isolated --with-requirements requirements-package-tests.lock ...`; it could not initialize the default cache due to filesystem permissions. With `UV_CACHE_DIR=/private/tmp/loom-goal-uv-cache` and `--offline`, resolution stopped because `execnet==2.1.2` was unavailable in the new offline cache. No package was installed.
- Focused fallback command: `/Users/kouko/.conda/envs/dbt-redshift/bin/python -m pytest -q loom-workflow/tests/goal-create/test_skill_md.py loom-workflow/tests/goal-create/test_input_floor.py loom-workflow/tests/goal-create/test_goal_shape.py loom-workflow/tests/goal-create/test_goal_lint.py loom-workflow/tests/goal-create/test_readmes.py loom-workflow/tests/scripts/test_release_metadata.py`; output: `54 passed in 0.28s`.
- Additional focused command: `/Users/kouko/.conda/envs/dbt-redshift/bin/python -m pytest -q loom-workflow/tests/goal-create/test_goal_lint_languages.py loom-workflow/tests/test_plugin_manifest.py`; output: `2 passed in 0.11s`.
- The full package suite was not run here. `finalize-review` is scheduled to execute the automated test suite before acceptance and block on failure; no suite result is claimed in this report.

## 1. SESSION sources, full prompt, constraints, and execution boundary

- How I tried it: Read the confirmed intent and spec in the clone; ran the focused tests above and a sample four-field condition through `python3 loom-workflow/skills/goal-create/scripts/goal_lint.py` on stdin. The sample named `Outcome`, `Constraints`, `Verification` with a backticked `test -f report.md`, and `Stop-when`.
- What came back: The sample exited 0 and reported only `UNCHECKED [condition-currently-false]`; the checker explicitly cannot determine the actual current state. `test_artifact_input_is_optional_and_preserves_intent_constraints` and `test_session_stops_after_prompt_and_host_activation` passed. No SESSION agent was invoked to produce an actual prompt from the intent or conversation.
- Evidence: `loom-workflow/skills/goal-create/references/input-floor.md:14-25`, `loom-workflow/skills/goal-create/SKILL.md:46-57`, `loom-workflow/tests/goal-create/test_skill_md.py:326-343`.

## 2. Codex activation and refusal

- How I tried it: Ran the focused contract tests. Inspected the Codex branch in the cloned skill. Did not call the exposed real `create_goal` tool because that could create or replace a Goal in the user's session.
- What came back: `test_session_activates_codex_only_after_lint_and_reports_host_evidence` and `test_codex_activation_requires_an_exposed_tool` passed. The contract says to submit the full four-field condition, report active only from host success, and preserve/report a refused unfinished Goal. No real success or refusal output was captured.
- Evidence: `loom-workflow/skills/goal-create/SKILL.md:59-71`, `loom-workflow/tests/goal-create/test_skill_md.py:249-257`, `loom-workflow/tests/goal-create/test_skill_md.py:332-336`.

## 3. Claude Code exposed proposal and manual fallback

- How I tried it: Ran the focused contract tests and inspected the Claude Code branch. Did not start a host session or alter host feature settings.
- What came back: `test_session_uses_a_faithful_bounded_claude_proposal`, `test_session_confirmation_and_replacement_follow_user_intent`, and `test_session_falls_back_without_starting_another_process` passed. The instructions distinguish pending confirmation from activation and require a full manual command after absence or non-success. No real `ProposeGoal` result or rendered command was observed.
- Evidence: `loom-workflow/skills/goal-create/SKILL.md:73-109`, `loom-workflow/tests/goal-create/test_skill_md.py:273-313`.

## 4. ARC, four-field lint, refusal, and release metadata

- How I tried it: Ran the focused tests and `agy plugin validate`; passed a valid sample and then `Outcome: [proposed] Improve this.` alone to the checker on stdin.
- What came back: The valid sample exited 0. The incomplete sample exited 1 with three `ERROR [missing-field]` lines for `Constraints`, `Verification`, and `Stop-when`. `test_declares_two_modes_and_conditional_arc`, `test_refusal_rule_states_empty_slot_and_no_goal`, lint tests, and release tests passed. All three plugin manifests state `5.4.0`; the changelog begins with `5.4.0`, and the English, Japanese, Traditional Chinese, and root README versions agree. ARC was not invoked interactively.
- Evidence: `loom-workflow/skills/goal-create/SKILL.md:112-122`, `loom-workflow/tests/goal-create/test_input_floor.py:368`, `loom-workflow/tests/scripts/test_release_metadata.py:17-56`, focused test output above.

## 5. UI flow: insufficient information

- How I tried it: Ran `test_refusal_rule_states_empty_slot_and_no_goal` and inspected the input floor. Did not invoke a live agent with incomplete conversation context.
- What came back: The test passed; the rule names the missing slot and emits no goal. There is no captured user-facing response.
- Evidence: `loom-workflow/skills/goal-create/references/input-floor.md:49-51`, `loom-workflow/tests/goal-create/test_input_floor.py:368-393`.

## 6. UI flow: usable draft

- How I tried it: Fed a complete sample directly to the checker and ran `test_artifact_input_is_optional_and_preserves_intent_constraints` and `test_session_activates_codex_only_after_lint_and_reports_host_evidence`.
- What came back: The checker exited 0; the tests passed. This confirms the checker accepts a complete shape and the instruction to show it, not that a host displayed a generated draft.
- Evidence: `loom-workflow/skills/goal-create/SKILL.md:19-44`, `loom-workflow/skills/goal-create/SKILL.md:51-53`, focused test output above.

## 7. UI flow: Codex tool available

- How I tried it: No real host call; tested the textual contract only because a real call could change the user's Goal.
- What came back: No activation or rejection result exists for this test. The focused tests in section 2 passed but cannot prove host behavior.
- Evidence: `loom-workflow/skills/goal-create/SKILL.md:59-71`.

## 8. UI flow: Claude proposal tool available

- How I tried it: No real Claude Code session with `ProposeGoal` was opened. Tested the textual contract only.
- What came back: No proposal, pending confirmation, or activation result exists for this test.
- Evidence: `loom-workflow/skills/goal-create/SKILL.md:81-98`.

## 9. UI flow: Claude proposal tool unavailable

- How I tried it: Ran `test_session_falls_back_without_starting_another_process`; inspected the fallback text.
- What came back: The test passed. The contract requires one full copyable `/goal <condition>` command, replacement disclosure, and no internal-setting instructions. No actual rendered fallback was captured.
- Evidence: `loom-workflow/skills/goal-create/SKILL.md:75-79`, `loom-workflow/skills/goal-create/SKILL.md:100-105`, `loom-workflow/tests/goal-create/test_skill_md.py:302-313`.

## 10. UI flow: Claude proposal not successful

- How I tried it: Inspected the same non-success fallback and ran its focused test; did not force a real `ProposeGoal` failure.
- What came back: The test passed, but there is no host failure reason or displayed command to inspect.
- Evidence: `loom-workflow/skills/goal-create/SKILL.md:100-109`, `loom-workflow/tests/goal-create/test_skill_md.py:302-313`.

## 11. UI flow: goal work remains unperformed

- How I tried it: Ran `test_session_stops_after_prompt_and_host_activation`; inspected the exit boundary. No generated goal was executed in this acceptance run.
- What came back: The test passed, and this run did no goal work. No real SESSION output was displayed, so the copyable prompt portion is unverified.
- Evidence: `loom-workflow/skills/goal-create/SKILL.md:46-49`, `loom-workflow/tests/goal-create/test_skill_md.py:326-329`.

## Re-run on 2026-09-27, at `5523b3c0`

- Fresh setup: `git clone --local --no-hardlinks --no-checkout . /private/tmp/loom-goal-acceptance-rerun-20260927`, then `git -C /private/tmp/loom-goal-acceptance-rerun-20260927 checkout --detach 5523b3c05ecb5b96df97f5351a443e4f58281ef2`; status was clean. `agy plugin validate ./loom-workflow` again returned exit 0, `skills: 12 processed`, and `hooks: 1 processed`.
- Fix inspected: `git diff 1ae51680..5523b3c0` changed only the Invocation section of the English, Japanese, and Traditional Chinese skill-local READMEs plus `test_readmes.py`. There were no runtime skill, reference, checker, host-activation, ARC, or release-metadata changes. Thus none of the 11 Acceptance/UI-flow rows is affected.
- Focused recheck: `/Users/kouko/.conda/envs/dbt-redshift/bin/python -m pytest -q loom-workflow/tests/goal-create/test_readmes.py loom-workflow/tests/goal-create/test_skill_md.py` returned `18 passed in 0.24s`. A search of the three skill-local READMEs found no old two-site or `purpose-link` claim; each now names only `loom-workflow:handoff` and direct user invocation. The prior nit is closed.
- The full package suite remains delegated to `finalize-review`; no new suite result is claimed. No real Goal tool was called on this re-run.
- 1: carried over — the fix changes invocation documentation only; source selection, prompt construction, constraint retention, and stop boundary are untouched.
- 2: carried over — the Codex tool branch and its tests are untouched.
- 3: carried over — the Claude proposal and manual fallback branches are untouched.
- 4: carried over — ARC, goal shape, lint/refusal, plugin version, changelog, and release metadata are untouched; the README invocation fix does not change those surfaces.
- 5: carried over — the missing-input refusal rule and its test are untouched.
- 6: carried over — the drafting, validation, and prompt-display rules are untouched.
- 7: carried over — the Codex success/refusal branch is untouched, and no real Goal call was made.
- 8: carried over — the Claude proposal and pending-confirmation branch is untouched, and no live proposal was made.
- 9: carried over — the Claude unavailable-tool fallback is untouched.
- 10: carried over — the Claude non-success fallback is untouched.
- 11: carried over — the skill's stop boundary and execution scope are untouched.
