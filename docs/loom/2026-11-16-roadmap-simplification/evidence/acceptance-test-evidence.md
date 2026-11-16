# Roadmap simplification — acceptance test evidence

Tried on 2026-11-16, in a clean copy of the project at de49933ac.

## Environment and setup

- Source: `/private/tmp/roadmap-acceptance-clean`; `git rev-parse HEAD` returned `de49933acbc129d1431fe910165a453780fb8043`. Initial `git status --short` returned empty. A final source status check also returned empty before writing these reports to the separate primary worktree.
- The main agent created this fresh worktree; this witness never implemented the change. The primary tree was at af2272ad, which was NOT substituted for the tested SHA.
- Read root README installation instructions, roadmap README and the clean source SKILL.md. README documents marketplace installation and invoking the skill through the host. This bounded run used the supplied authorization for source instruction loading instead: read the clean runtime instructions and performed their actions against separate scratch fixtures. No marketplace installation, installed-cache refresh, host discovery, automatic triggering or native goal activation was attempted or claimed.
- Scratch root: `/private/tmp/roadmap-trial.Wlhwsw`. Fixtures were created with apply_patch. Semantic actions below were performed by this independent witness following the source instructions, not by a synthetic parser that asserts expected phrases. This is one source-level agent trial, not evidence of universal agent compliance.
- Read the spec; UI flows are explicitly N/A. No additional GUI/CLI/API flow was omitted.

## 1. Ordinary optional root planning document

- Scenario `test_roadmap_new_staged_request_creates_plain_summary`: request staged CSV-export planning across two sessions, with no prior applicable planning file. Following the loaded instructions, created `new/ROADMAP.md` containing a goal, observable done condition, proposed status, next action, unknown date/effort and evidence status.
- Actual artifact content includes `Status: proposed; no implementation or acceptance yet.` and `Unknown: effort and delivery date remain unknown.` No map identifier, runtime, store or parser was used. The done condition retains both test success and user acceptance.
- Structural check, separate from the semantic trial: roadmap packaging/local-link tests passed in the focused invocation below. These checks establish packaging, not semantic quality.

## 2. Creation, chosen-document resumption and result maintenance

- Scenario `test_roadmap_selected_document_resume_avoids_duplicate`: created a pre-existing `existing/initiative.md` with authorized work and an unrelated user filename/language choice, then selected that file for resumption. Read it before editing; edited this selected file only. `test ! -e ROADMAP.md && echo 'no duplicate root roadmap'` returned `no duplicate root roadmap` in that directory.
- Continued the already authorized fixture check without a new planning interview: `python3 check.py` returned exit 0 and `Unicode fixture passed; scope: one fixture only`. Updated the summary to Unicode passed, empty-input and acceptance pending; linked `unicode-result.md` and preserved the exact unrelated user-choice line.
- Scenario `test_roadmap_failed_result_preserves_unfinished_status`: `python3 empty-check.py` returned exit 1 with `AssertionError: empty-input expectation not satisfied`. This is an intentionally negative acceptance fixture, not a product regression. Recorded the failure in `empty-result.md`, retained the success evidence, and bounded the next action to inspect the failing case. No CSV implementation was changed.
- Scenario `test_roadmap_advice_without_plan_keeps_absence`: advice/resume-only fixture `advice/intent.md` authorized inspection of the failing input, without requesting staged planning. Read the available intent and recommended that same next step. Created no planning document: `test ! -e ROADMAP.md && echo 'resume/advice kept absent roadmap absent'` returned `resume/advice kept absent roadmap absent`.
- Final selected summary:

```text
Status: Unicode fixture passed; empty-input check failed; user acceptance pending.
Next: inspect the failing empty-input case within approved scope; do not publish or merge.
Unrelated user choice: keep the existing filename and Japanese labels.
Evidence: [approved scope](intent.md).
Evidence: [Unicode result](unicode-result.md); one fixture only.
Evidence: [failed empty-input check](empty-result.md); retained, not completed.
```

## 3. Retired capabilities and retained session goal

- Actual clean-source commands: `test ! -e loom-workflow/skills/decision-map` succeeded; `test ! -e loom-code/contract/templates/PURPOSE.md` succeeded. Output labels: `decision-map skill absent`, `PURPOSE scaffold absent`.
- `rg -n 'ARC|SESSION' loom-workflow/skills/goal-create/SKILL.md` returned SESSION references only (including the `## SESSION mode` heading), no ARC match. Read the retained skill and both referenced goal-shape/input-floor instructions.
- Focused tests below exercised retained goal shape/lint/inputs, unrelated intent validation and purpose retargeting. All 89 passed. This is actual execution evidence for those checks, not a behavioral trial of every retained delivery, research or handoff capability. Therefore Acceptance 3 is partly verified. No native goal was activated, because this acceptance task did not authorize replacing the session goal.

## 4. Existing data preservation

- Scenario `test_roadmap_existing_history_and_input_preserved`: created historical MAP.md, PURPOSE.md, authorized intent and Unicode CSV input before roadmap resumption. `shasum -a 256 MAP.md PURPOSE.md intent.md export.csv` was run before and after all semantic edits, returning the same values:

```text
a328f989f809d98e49d764e90546db3cf8811168bbc2fdead29130ecb92b8071  MAP.md
f450d889d0069406431483ddfd66e76722bb0f505d47f3e4bb2a8c4966088172  PURPOSE.md
33f044d27044f2000cbebf8eeeaec2001b08a250025e3cf720a09ebbf8d9a09e  intent.md
9daceffd29a52c7470a4477d1bec37b7b236046567817bc7664e0de43e0538dd  export.csv
```

- These are scratch user-data stand-ins, not the user's private project data. Actual installed-plugin upgrade behavior was not exercised. Acceptance 4 is partly verified rather than asserting installer behavior from prose.

## 5. Authorization and unverified-result boundaries

- The successful Unicode check was scoped to one fixture, not all completion conditions. Failed evidence remained linked. Final status explicitly retains failed empty-input verification and pending acceptance.
- The summary did not authorize implementation, publication or merge; continuation ran only the already authorized bounded checks. No confirmation/verification/acceptance document was manufactured, no external service called, and no background execution scheduled.
- Scenario `test_roadmap_partial_success_does_not_claim_completion` is witnessed by the actual final summary and both executed checks in sections 2 and 4. These semantic observations are distinct from the packaging assertions.

## Focused automated checks and final-suite boundary

- Initial `python3 -m pytest ...` failed before collecting tests: system Python lacks pytest. The interpreter path supplied by the main agent was no longer present. Neither failure was a product finding or hidden.
- Offline locked setup first encountered the sandbox's uv-cache temporary-file restriction; the same offline command ran successfully after permitted sandbox escalation. No dependencies were added to the project or conda base.

```sh
uv run --offline --isolated --with-requirements requirements-package-tests.lock python -m pytest -q loom-workflow/tests/roadmap/test_skill_structure.py loom-workflow/tests/goal-create loom-code/tests/test_loom_checker_intent.py loom-design/tests/interface/test_north_star_purpose_retarget.py
```

Result: `89 passed in 20.33s` (exit 0).

The full package suite was NOT run by this witness. The closing-review finalizer will run the automated test suite before acceptance and block on failure; no successful future run is claimed here. Its documented command is:

```sh
uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q
```

No important findings were supplied as dismissed. Only the 15-percentage-point comparative improvement threshold was waived on 2026-11-16; semantic evaluation, independent review, acceptance and finalization remain required.

## Re-run on 2026-11-16, at de49933ac — additional A3 source trials

The first-pass Acceptance 3 verdict was partly: it had not exercised research or handoff. That original coverage limit is retained above, not retroactively called a pass. The following actual additional trials close the bounded source-capability gap; they do not claim installed-host activation. No source changed between trials.

- Research: loaded clean `engineering-research/SKILL.md`, research-methods, source-policy and research template. Question and sufficient condition were set before the new directory inspection: whether ordinary planning needs a dedicated runtime at this revision. Used local source inspection and the existing scoped trial; no web question existed. `ls /private/tmp/roadmap-acceptance-clean/loom-workflow/skills/roadmap` returned `README.md` and `SKILL.md`. Saved `/private/tmp/roadmap-trial.Wlhwsw/docs/loom/research/2026-11-16-roadmap-runtime.md`, read its full substantive content back with `cat`, and resolved all three relative evidence links with Python: each returned `True`. The record has required flat metadata, question/conditions, method, findings, evidence, decision impact and limitations. The source/runtime distinction and failed input evidence remain explicit.
- Handoff Prepare: loaded clean handoff skill and read the entire 714-line schema reference without truncation (the earlier combined read was truncated and was not treated as sufficient). State collection returned exact HEAD `de49933acbc129d1431fe910165a453780fb8043`, branch `HEAD`, empty status, five Git history lines and `2.1.325 (Claude Code)`. The version command only reports a CLI version; no model process was launched.
- Created scratch `.claude/handoffs/HANDOFF-2026-11-16-230000-source-trial.md` with all ten blocks and appended a thin Resume Launcher. The scenario's single synthetic user turn is clearly labeled and reproduced verbatim; it is not substituted for the actual session record. Critical files point to the existing selected initiative; no roadmap creation or rewrite occurred. Git checks explicitly refer to the clean source repository, distinct from the non-Git scratch fixture.
- Handoff Resume: `ls -t .claude/handoffs/ | head -1` selected `HANDOFF-2026-11-16-230000-source-trial.md`. Read the whole file, ran every saved verification command and compared expected to actual:

| Tier | Command | Expected | Actual |
|---|---|---|---|
| T1 | `git -C /private/tmp/roadmap-acceptance-clean rev-parse HEAD` | `de49933acbc129d1431fe910165a453780fb8043` | `de49933acbc129d1431fe910165a453780fb8043` |
| T1 | `git -C /private/tmp/roadmap-acceptance-clean rev-parse --abbrev-ref HEAD` | `HEAD` | `HEAD` |
| T1 | `claude --version` | `2.1.325 (Claude Code)` | `2.1.325 (Claude Code)` |
| T1 | `test -f /private/tmp/roadmap-trial.Wlhwsw/existing/initiative.md && echo selected-plan-present` | `selected-plan-present` | `selected-plan-present` |
| T2 | `git -C /private/tmp/roadmap-acceptance-clean status --short` | empty | empty |

- No drift. Source-invoked synthesis was: (1) selected plan preserves Unicode success and empty-input failure; (2) pending work is inspecting that failed case; (3) next step needs direction before action. Trial stops here; no pending implementation was performed and no actual user confirmation was invented. Launcher text is retained in the scratch artifact and below, identical:

```text
Read `/private/tmp/roadmap-trial.Wlhwsw/.claude/handoffs/HANDOFF-2026-11-16-230000-source-trial.md` fully. If handoff is installed use Resume mode; otherwise follow this procedure directly: run every T1/T2 command, compare actual output against the file, stop on T1 mismatch, and report/judge T2 drift. Give a three-to-five-bullet synthesis and wait for user direction before acting. Reply in the frontmatter conversation language, Traditional Chinese.

USER DIRECTIVE:
```

- SESSION retained source CLI: `python3 loom-workflow/skills/goal-create/scripts/goal_lint.py /private/tmp/roadmap-trial.Wlhwsw/valid-goal.md` exited 0; output was `UNCHECKED [condition-currently-false]: Whether the described condition is currently false cannot be checked from goal text alone — it needs the repository's current state, not just the text.` This is properly a structural pass, not semantic proof. The referenced empty-input check actually failed earlier, so this scenario's wanted difference is not already true.
- Invalid input CLI with `/private/tmp/roadmap-trial.Wlhwsw/invalid-goal.md` exited 1; missing-field errors named Constraints, Verification and Stop-when, with the same UNCHECKED notice. No real goal was activated or replaced.
- Acceptance 3 now works for the bounded source preservation criterion: retirement inventory, unrelated intent tests, 89 focused checks, actual research retention, verified handoff restart and valid/invalid SESSION CLI. Ordinary full delivery and every possible research path were not exhaustively exercised; finalization's full suite still remains required.
- Acceptance 1, 2 and 5 carried over: no source changes, only additional independent trials. Acceptance 4 remains partly pending separate installer evidence.

## Re-run on 2026-11-16, at de49933ac — independent inspection of local Codex update trial

The first-pass Acceptance 4 was partly because no installer update had been tried. This remains the accurate history. The main agent subsequently ran an isolated local Codex installation/update trial; this independent witness inspected its raw results and actual resulting files rather than accepting the summary alone.

- Trial root: `/private/tmp/roadmap-local-upgrade-check`. Read `old-marketplace-result.json`, `old-plugin-result.json`, `old-installed-inventory.json`, `new-plugin-result.json`, `new-plugin-list.json`, `before-upgrade-data.json` and `upgrade-observations.json` in full.
- Old marketplace add and old plugin add both exited 0. Old install result identifies version 5.25.0 and its isolated cache path. Old recorded inventory contains 15 skills, including decision-map; ARC present.
- New plugin add exited 0 and identifies version 5.26.0. Plugin list exited 0 and records installed/enabled true, local source `/private/tmp/roadmap-local-upgrade-check/marketplace/loom-workflow`, in the isolated `codex-profile`. This is installer/list evidence, not live-model activation.
- Independently recomputed SHA-256 from all actual project files and compared each against the pre-update baseline: `notes.txt`, `ROADMAP.md`, `docs/loom/PURPOSE.md`, and `docs/loom/maps/legacy/MAP.md` all returned `True`. Read all four actual contents; historic purpose/map and user plan/text remain readable and unchanged.
- Direct actual installed-cache inspection found 15 new skills, roadmap present and decision-map absent. New goal-create contains no ARC. New installed roadmap SKILL.md byte-for-byte equals the tested clean source. The retained old marketplace source backup actually contains decision-map and ARC.
- The initial independent inspection attempted the old installed 5.25.0 cache and got FileNotFoundError: that cache no longer exists after update. This does not disprove the captured old successful installation, but old-cache inspection is not claimed. Old installation is supported by its captured result/inventory plus old source backup, new installation by actual current files and captured results.
- The main agent reported an initial dynamic-argument command rejected by the local command guard before execution; only the subsequent static-argument invocation ran. No bypass, permission waiver, model invocation or network-source installation is inferred. The witness did not reconstruct an execution from a blocked attempt.
- Acceptance 4 now works within the observed isolated local Codex update scope. This does not establish other hosts, production-profile update, automatic session activation or universal data preservation. No actual user project data was read or changed.
- Acceptance 1, 2, 3 and 5 carry over: tested source unchanged, the additional trial only measures installation and scratch-data preservation.

Reproducibility details supplied with captured results: Codex version output independently read as `codex-cli 0.169.0`. Sequential literal child argv used `/Users/kouko/.local/bin/codex plugin marketplace add /private/tmp/roadmap-local-upgrade-check/marketplace --json`, then `/Users/kouko/.local/bin/codex plugin add loom-workflow@loom --json` for old install; after replacing the controlled source using the de49933a Git archive (old source retained as marketplace-v5.25), the identical literal plugin-add argv installed the new version, then `/Users/kouko/.local/bin/codex plugin list --json`. Every child cwd was the scratch `project` directory; child environment set `CODEX_HOME=/private/tmp/roadmap-local-upgrade-check/codex-profile` while retaining only PATH/TMPDIR/LANG/LC_ALL/HOME/USER/SHELL from its process. This intended isolation did not modify production configuration. Raw seven-record bundle retained by the main agent: [local Codex update results](local-codex-upgrade.json).

## Re-run on 2026-11-16, at 99404a2a4 — repair acceptance

### Clean setup and retained failures

`git rev-parse HEAD` in `/private/tmp/roadmap-repair-acceptance` returned `99404a2a47c5ac4e3289e2dd5820f86d067ae2e0`; initial and final `git status --short` returned empty. The main agent created this fresh clean tree. Later publication-evidence commit 641bfc08 was not substituted for the tested revision.

Setup repeated this run: read clean root README Codex installation section, roadmap README and full repaired SKILL.md with `cat`. Loaded the instruction-only source directly under the same bounded authorization as the earlier trial and used a new scratch root `/private/tmp/roadmap-repair-trial.rgql3a`. This produced real ordinary-file edits and real executed checks below. No installation/host activation claim follows from this load. No setup dependency was needed for this instruction-only path.

Compared `git diff --stat a09c4eeb..99404a2a`, `git diff --name-only` and the full roadmap diff. Production delta is two roadmap paragraphs plus their heading and changelog; other changes are spec clarification, plan and evidence. Read the added spec decision and public dogfood-repair-retest record. It retains the original genuine trial's unsupported component-pending generalization and unclear continuation terms; these failures are not relabeled as initial passes. No private finance input was read or copied into this report.

### Acceptance 1 — carried over

Checked against the fix diff: ordinary Markdown, optional root default, creation criteria and no-runtime format are unchanged. Prior actual creation result remains applicable. The current A2 re-test also creates a new ordinary document, but this carried-over row does not imply rerunning the full original packaging checks.

### Acceptance 2 — re-tested in full

- `test_roadmap_repaired_new_plan_creates_summary`: actual staged-planning source invocation created `new/ROADMAP.md` with goal, observable completion, proposed status, next step, unknown effort/date and evidence state. Read back its full text; it did not claim implementation or results.
- `test_roadmap_repaired_selected_plan_preserves_component_status`: actual selected `selected/plan.md` was read with `prior.md` before editing. Prior evidence says Unicode reported complete at fixture-v1, empty input explicitly pending, no formatting result. The encompassing stage is in progress. Kept Unicode attributed completion without a rerun, kept explicit empty-input pending until its own check ran, and left formatting unknown rather than labeling every component unfinished. No duplicate root summary was created: `test ! -e selected/ROADMAP.md && echo NO_DUPLICATE` returned `NO_DUPLICATE`.
- `test_roadmap_repaired_authorized_check_continues`: resumed the concrete already approved empty-input check with `python3 check.py`, no new intent interview. Actual output `PASS empty-input fixture only; review/acceptance not performed`, exit 0. This is actual continuation, not merely advice to continue.
- `test_roadmap_repaired_failed_evidence_stays_visible`: `python3 fail.py` exited 1 with `AssertionError: Unicode not established by empty-input fixture`. This deliberately negative fixture tests evidence separation; it is not a production bug. Retained the failure in `results.md`, explained its limited scope, and linked both earlier and current evidence rather than erasing either.
- Updated only the selected summary's empty-input result and next action. Verified result did not advance independent review or user acceptance. `Formatting: unknown; no supporting result.` and `Unicode: reported complete by earlier report at revision fixture-v1; not freshly verified.` remained intact.
- `test_roadmap_repaired_direction_change_keeps_evidence`: under the synthetic request to prioritize empty files first, actually updated the goal/order in the selected document. Read the final document; preserved its old completion conditions, prior reported status, unknown formatting, evidence links and unrelated user-selected Japanese-label choice. No invented deadline or migration.
- `test_roadmap_repaired_advice_resume_avoids_creation`: read `advice/intent.md`, whose existing authorization is inspection only and contains no staged-planning request. Wrote the actual bounded recommendation in `advice-response.md`; no implementation or planning file created. `test ! -e advice/ROADMAP.md && echo NO_ADVICE_ROADMAP` returned `NO_ADVICE_ROADMAP`.
- `test_roadmap_repaired_missing_entry_stays_planning`: in the declared synthetic host inventory with neither implementation entry available, authored `no-entry-response.md` explaining the unavailable entry and ending with planning only. Also covered capture-intent-present and write-plan-only inventories: chose the respective existing entry, without executing a station or inventing a fallback. These are actual instruction-following response trials against controlled inventories, not claims about installed host capability discovery.

### Acceptance 3 — carried over

Compared the fix range: no retirement inventory, goal-create code, research/handoff runtime guidance or test was changed. Prior retirement checks, actual research retention, complete verified handoff source trial and valid/invalid SESSION CLI remain applicable. Continued-work wording was re-tested under A2/A5. No full delivery or installed-host activation is newly claimed.

### Acceptance 4 — carried over

Compared the fix range: no installer/loader/migration implementation, manifest inventory or data-handling mechanism changed. The source instruction still forbids converting or rewriting existing history solely due to plugin update. Prior actual isolated local Codex upgrade and independently checked four-data-file hashes remain applicable; no new upgrade was run. Repairs affect how an authorized planning summary is explained and edited, covered by selected-file scope checks in A2.

### Acceptance 5 — re-tested in full

Actual trial outputs distinguish four states: historical reported completion at fixture-v1, current empty-input pass, deliberate current negative-check failure, and unsupported formatting unknown. Neither a broad stage label nor an unmet exit condition was used to downgrade every component. Failure was retained with its explanation; reported prior success was not falsely called fresh verification. Completion still requires review and user acceptance, neither claimed performed.

Already authorized checks actually ran; no intent reset occurred. Advice remained advice. A newly authorized change was directed only to the available entry in the controlled response trial; neither-entry case stopped at planning with the limitation disclosed. No new implementation, spend, disclosure, deletion, publication, merge or background dispatch was performed. The actual final selected summary was read back:

```text
Goal: prioritize empty-file reliability first; retain Unicode as the following stage.
Done when: both fixtures pass, independent review completes and user accepts.
Stage: in progress.
Unicode: reported complete by earlier report at revision fixture-v1; not freshly verified.
Empty input: observed check passed in this trial; earlier pending state superseded only for this fixture.
Formatting: unknown; no supporting result.
Next: inspect the failing Unicode check within approved scope; review and acceptance still pending.
Direction: user-authorized ordering change in this synthetic trial; no deadline added.
Unknowns: effort and date.
Keep: user-selected Japanese labels.
Evidence: [earlier report](prior.md).
Evidence: [current checks](results.md); empty-input success does not freshly verify Unicode.
```

No product repair or test modification was made by this witness. No package suite was run by this witness. The station reports 4,036 pytest cases plus shell inventory passing for this repair and retained 65 existing adversarial checks; these are station-reported results, not this witness's fresh suite execution. Earlier 4,031/89 counts remain historical under their tested revisions. Finalization still reruns the full automated suite and blocks on failure; neither package testing nor finalization is skipped. No dismissed important findings were supplied. Only the pre-existing 15pp numerical improvement waiver applies.
