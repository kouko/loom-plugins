# Resolve five confirmed skill/checker consistency defects — acceptance test evidence

Tried on 2026-10-27, in a clean copy of the project at 02c51607 (a fresh
`git clone` of the branch, checked out at `02c51607`, in a scratch directory
outside the repository). The driver scripts (`tools/at_finalize.py`,
`tools/at_a2.py`, `tools/at_a4.py`), their logs and the throwaway repos lived
in that session scratch directory and are not committed; the outputs that
back each verdict are reproduced inline below. Every throwaway repository below was created fresh
by a driver script in the scratch directory; nothing in the working tree was
modified apart from committing this file and the report.

Sections Setup and 1-5 record the first run at 02c51607. Section 6 (an
Acceptance line added when the intent was re-confirmed at 0aa7ec08) and the
re-run at 0a27f371 are recorded below; the former line 6 is now line 7. Where
the re-run's output differs from a first-run section (the refusal wording in
section 1), the re-run section is the current one. A second re-run at
a0966dd7 re-tested line 6 only; its section at the end supersedes section 6's
Follow-ups row and refusal wording.

## Setup

- How I tried it: followed the README's Install section as far as it applies
  without touching the user's global host configuration — the plugins are
  run from the clean clone rather than installed with
  `claude plugin install` (installing would rewrite the user's real plugin
  set). Ran the plugin's own launcher from the clone:
  `loom-code/scripts/loom-python --repair --list-rules`.
- What came back: exit 0; the rule list printed, starting with
  `adversarial.proportionate ... at most 5 adversarial probe programs`.
- Evidence: the launcher resolves its cached interpreter and runs the checker
  from a clean clone. The marketplace install itself was not exercised.

## 1. A change that survives every adversarial attack and has no covering repository test can complete finalize-review without the user skipping the adversarial step, and the recorded adversarial evidence names the no-program outcome and its reason.
- How I tried it: a driver (`tools/at_finalize.py <clean> <work> a1`) built
  one throwaway git repo per case (`main` with `src.py` and a
  `KICKOFF-DEFAULTS.md` whose package-tests is `python3 -c pass`, then a
  `feature` branch adding `feature.py`, no probe store, no skip). Each case
  wrote a review input with two passing verdicts and the given `adversarial`
  list, and ran the real launcher:
  `loom-code/scripts/loom-python --repair finalize-review 2026-10-27-at-fixture --input <json>`
  with `FORCE_COLOR` and `CLAUDE_CODE_SESSION_*` unset. When an attestation
  was written it was committed and re-read through
  `loom_checker.verification.verification_status(repo, change, base="main")`,
  the same validator Ship, land and CI call.
- What came back:

  | case | adversarial input | finalize-review | attestation status |
  |---|---|---|---|
  | positive | `[{"no_program": "every attack failed and no repository test covers the change"}]` | exit 0, `wrote docs/loom/2026-10-27-at-fixture/attestation.json` | `valid` |
  | positive, reason then blanked in the committed attestation | (tampered after the fact) | — | `stale (a no-program record needs a non-blank reason)` |
  | no record at all (the old deadlock) | `[]` | exit 1, `BLOCK finalize.adversarial: at least one adversarial execution is required` | none written |
  | blank reason | `[{"no_program": "   "}]` | exit 1, `a no-program record needs a non-blank reason` | none written |
  | two records | two `no_program` rows | exit 1, `a no-program record must be the only adversarial record` | none written |
  | beside a supplied program | `no_program` + `python3 …/probe_0.py` | exit 1, same message | none written |
  | beside a RED program committed in the store | `no_program` only, store holds `test_red.py` | exit 1, same message | none written |
  | extra field on the record | `{"no_program": …, "command": "python3 -c pass"}` | exit 1, `a no-program record carries only its reason` | none written |

  The positive attestation's executions are exactly
  `[{"kind":"package-tests","command":"python3 -c pass",…,"result":"pass"}, {"kind":"adversarial","no_program":"every attack failed and no repository test covers the change"}]`;
  `selection` is `null` and nothing records the adversarial step as skipped.
  `intent_state._delivery_witness_valid` on that attestation returned `True`
  (delivery recognition accepts the row).
- Prose read against the code: `loom-code/agents/adversary.md:47-49` now has
  the adversary record the no-program outcome instead of asking the user to
  skip; `loom-code/skills/build/SKILL.md:114-115,185` carries it in the
  hand-off; `loom-code/skills/closing-review/SKILL.md:407-417` shows the
  `{"no_program": …}` input and says blank reasons and mixing are refused,
  matching `probes.py:592-597`. No remaining wording in the adversary, Build
  or adversarial reference asks the user to skip when no program exists
  (`grep -i "whether to skip"` → no match).
- Evidence: driver output saved as `scratchpad/a1.log`; the checks live at
  `loom-code/scripts/loom_checker/probes.py:573-600`,
  `command_handlers/finalize.py:284-292,401`, `attestation.py:160-205`,
  `intent_state.py:145-151`.

## 2. The adversarial ceiling stated in the skill prose and the ceiling enforced by finalize-review count the same set of programs, so reusing an existing program never overflows the five-program ceiling and never produces a refusal the prose says cannot happen.
- How I tried it: read `loom-code/skills/closing-review/references/adversarial.md:63-82`
  against `probes.py:518-561` (`check_adversarial_proportionate`) and
  `finalize.py:343`; then ran the real launcher on three throwaway repos
  (`tools/at_a2.py`).
- What came back:
  - Prose (line 79-82): "The ceiling counts distinct program paths across this
    change's store, the programs it graduated and the programs supplied to
    `finalize-review`, so re-running a path already counted adds none, while a
    repository test named as this change's program is a path like any other."
    Code: `counted = dict.fromkeys(stored)` plus graduated paths plus supplied
    artifacts, refused when `len > MAX_PROBE_PROGRAMS (5)`. Same three sets,
    same de-duplication by path. The old sentence "spends nothing against the
    ceiling" is gone; `grep -i "ceiling\|spends"` over the skills and agents
    finds no other statement of the count.
  - Five programs committed, all five supplied again → exit 0, status `valid`.
  - Five committed, `probe_0` supplied twice → exit 0, status `valid`.
  - A sixth distinct path committed and supplied → exit 1,
    `BLOCK adversarial.proportionate: 6 probe programs for this change (committed under its store, executed by finalize-review, or graduated into the package suite); at most 5 are allowed`
    — the case the prose says counts.
- Evidence: `scratchpad/a2.log`; `adversarial.md:79-82`; `probes.py:542-554`.

## 3. Recording a lesson that an existing memory entry already states produces exactly one defined outcome and never a second entry for the same subject, and the skill and its operations reference name that outcome identically.
- How I tried it: read `loom-workflow/skills/loom-memory/SKILL.md:130-157` and
  `references/operations.md:76-108`; then walked the procedure on a throwaway
  store with the shipped tool: `loom_memory.py init`, wrote one concept
  (`run-suites-without-force-color`, one source), `regenerate-index` +
  `validate`; then applied the equivalent-lesson outcome (added a second
  `sources[].resource` to the same file), `regenerate-index` + `validate`.
- What came back:
  - Record step 3 routes "an equivalent or contradictory live entry" to
    Reconcile (`SKILL.md:130-131`, `operations.md:76-78`); Reconcile's trigger
    now reads "contradicts, narrows, or is equivalent to a current entry (same
    subject, same rule)" in both files (`SKILL.md:145-146`,
    `operations.md:92-94`), so the routed case is covered.
  - Outcome sentence, both files word for word: "An equivalent lesson keeps the
    existing entry unchanged and only adds its new source to that entry's
    `sources`." (`SKILL.md:151-152`, `operations.md:99-101`). Both forbid "a
    second entry for the same subject" (`SKILL.md:154`, `operations.md:103-104`).
  - Store walk: both validations `OK — OKF v0.2-compatible Loom memory profile
    holds.`; the store holds one concept file with two sources and the index
    lists one entry.
- Evidence: `scratchpad/work/a3-store/`; file:line above. The walk shows the
  defined outcome is executable with the shipped tool; it does not show an
  agent choosing it (that would need a skill-behaviour trial).

## 4. Every loom-visualization chat template that draws a node-label separator uses exactly six U+2501 characters, and the page verifier accepts a page built from each changed template.
- How I tried it: `grep -o "━+"` over all 13 templates; a driver
  (`tools/at_a4.py`) extracted every `<div style='text-align:left'>` label
  from the Mermaid block of 02, 04 and 08 and ran the shipped
  `verify_cot_html.check_node_label` on it, plus a seven-character mutation;
  then wrapped each template's Mermaid block into a minimal HTML page and ran
  `python3 verify_cot_html.py <page>`; and once more with the first line
  rewritten to `graph TB` to see what lies behind the first refusal.
- What came back:
  - Only 02, 04 and 08 contain U+2501; every run is length 6 (02:62 ×1,
    04:70 ×2, 04:74 ×2, 08:63 ×1).
  - Per label: 02/C, 04/A-D, 08/P each `fails=none`; each seven-character
    mutation fails.
  - Whole page, as written: all three exit 1 with one FAIL,
    `diagram 1: must start with graph TB … or graph LR` (the templates use
    `flowchart`).
  - Whole page with the header rewritten: still exit 1, for reasons that are
    not the separator — 02: no subgraph rows, nodes A/B/D are plain quoted
    labels with no separator, unlabelled edges, no style lines; 04: subgraph
    rows contain no node definitions, malformed-arrow count, style for
    undefined nodes; 08: subgraph ids `P`/`APP`/`DATA` off-spec, no
    `direction LR`, node W has no separator, unlabelled edge. None of these
    FAIL lines is about a six-character separator in a changed label.
- Evidence: `scratchpad/a4.log`, `scratchpad/a4b.log`,
  `scratchpad/work/a4-pages/`. The plan's W1-04 Risk and Simplicity check
  record this as agent-decided: a per-label check instead of a full page,
  because a full page would require widening the templates, which the intent's
  Out of scope excludes. The second half of this Acceptance line is therefore
  met only per label, not for a page.

## 5. A pytest-style adversarial probe recorded with any supported Python invocation (for example `python3 -m pytest`) is accepted by finalize-review, and one recorded as a direct `python3 <artifact>` run is still refused; the adversarial protocol states that acceptance instead of one literal spelling.
- How I tried it: `tools/at_finalize.py <clean> <work> a5` committed one
  pytest-style probe (`# concern:` line, `def test_holds(): assert True`)
  under the change's probe store in five throwaway repos and ran the real
  launcher with each command form; read `adversarial.md:146-153` against
  `probes.py:678-740` (`runs_pytest`, `_python_argv`, `direct_pytest_style_failure`).
- What came back:

  | command recorded | finalize-review | status |
  |---|---|---|
  | `python3 -m pytest <a>` | exit 0 | `valid` |
  | `python3.12 -m pytest <a>` | exit 0 | `valid` |
  | `/Users/kouko/.conda/envs/dbt-redshift/bin/python3 -m pytest <a>` | exit 0 | `valid` |
  | `uv run --with pytest python3 -m pytest <a>` | exit 0 | `valid` |
  | `python3 <a>` | exit 1, `BLOCK finalize.adversarial: … defines pytest tests that a bare python run never calls; record python -m pytest …` | none |

  Prose now reads "any supported Python invocation followed by
  `-m pytest <artifact>`, such as a versioned interpreter (`python3.12`), an
  interpreter named by its full path, or one wrapped in `uv run` or
  `conda run -n <env>`", and keeps the bare-run refusal — the same set
  `runs_pytest` accepts (any argv0 whose basename starts with `python`, after
  unwrapping `uv run` and `conda run -n ENV`). `conda run -n` was read, not
  run.
- Evidence: `scratchpad/a5.log`; `adversarial.md:150-153`; `probes.py:711-714`.

## 6. When the recorded adversarial evidence is a no-program outcome, the pull request's Verification section states that no adversarial program ran and gives the recorded reason, and publication refuses a body that leaves it out.
- How I tried it: tried 2026-10-27 in a fresh `git clone` checked out at
  `0a27f371`. A driver (`tools/at_a6.py <clean> <work>`) built throwaway git
  repos on branch `feat/2026-10-27-at-fixture` with a committed intent and an
  origin of `git@github.com:example/at-fixture.git`, ran the real launcher
  `loom-code/scripts/loom-python --repair finalize-review 2026-10-27-at-fixture --input <json>`,
  committed the attestation, read its status with the real
  `verification_status`, and then called the real
  `loom_checker.command_handlers.publish.cmd_publish(["--confirm-authorized", "--title", …, "--body-file", <body>])`.
  Change identification, status computation and body validation were not
  stubbed. Only the network seam `run_publish_external` was replaced, with a
  recorder that answers every outward call with a failure. On top of that, a
  guard on `subprocess.run` refused any `gh`, `push`, `ls-remote` or `fetch`
  argv. Nothing was pushed and GitHub was never called. Bodies carried the
  nine contextual headings, with `Verification status: valid` under
  Verification.
- What came back (`scratchpad/a6.log`):

  | case | body | publish result | outward calls attempted |
  |---|---|---|---|
  | no-program attestation, status `valid` | `Adversarial outcome: no program — <recorded reason>` under Verification | validation passed: printed `Verification valid for <head>`, then stopped at the stubbed `gh repo view` | `repo view` (stubbed, not made) |
  | same | line missing | exit 1, `BLOCK push.contextual-body: the attestation records that the adversarial step left no program; the body must carry exactly this bare line:` followed by the full line with the recorded reason | none |
  | same | line with a different reason | exit 1, same refusal printing the recorded line | none |
  | same | `Adversarial outcome: no program` with no reason | exit 1, same refusal | none |
  | same | line inside an HTML comment | exit 1, same refusal | none |
  | same | line inside a code fence | exit 1, same refusal | none |
  | same | line as a bullet (`- Adversarial outcome: …`) | exit 1, same refusal | none |
  | same | line under `## Follow-ups`, not under Verification | **accepted**: printed `Verification valid for <head>`, then stopped at the stubbed `gh repo view` | `repo view` (stubbed, not made) |
  | programs attestation (`python3 -m pytest <probe>`), status `valid` | no outcome line | accepted (boundary: no line is needed) | `repo view` (stubbed, not made) |

- Why the Follow-ups case passes: `validate_disclosed_outcome`
  (`loom-code/scripts/loom_checker/rule_checks/publish.py:55-64`) collects
  `visible` from `_body_sections(body, strip_comments=True)[1]` (line 58),
  which holds every non-fenced line of the whole body, not the lines of the
  Verification section. So the refusal enforces that the line is somewhere
  in the body, not that it is in the Verification section the Acceptance line
  names. Ship's prose (`loom-code/skills/ship/SKILL.md:86-92`) tells the agent
  to write the line under the Verification heading, so an agent following
  Ship puts it in the right place. The section is unenforced only for a body
  written another way.
- Scope of the check: it runs only when the computed status is `valid`
  (`command_handlers/publish.py:414-420`). Reasons are read from the
  attestation committed at `HEAD` (`_no_program_reasons`, line 349). The plan
  (W4-01 Risk) records this as agent-decided.
- Criterion tests, run in the clean clone:
  `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest -q loom-code/tests/test_loom_publish.py loom-code/tests/test_selection_finalize.py loom-code/tests/test_loom_attestation.py loom-code/tests/test_adversarial_no_program_beside_stored.py`
  → `163 passed in 64.84s` (`scratchpad/a1a6-tests.log`). This includes
  `test_no_program_outcome_line_lets_valid_publication_proceed`, which checks
  the line reaches the published body. That test stubs the status rather than
  computing it.
- Evidence: `scratchpad/a6.log`, `scratchpad/tools/at_a6.py`,
  `scratchpad/a1a6-tests.log`.

## 7. The complete package suite passes, and both affected plugins land synchronized minor version bumps with CHANGELOG entries.
- (First run, recorded when this was line 6.)
- How I tried it: in the clean clone,
  `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`
  (run on the station's explicit instruction; my standing contract otherwise
  leaves the full suite to finalize-review). Read every manifest's `version`,
  the README version strings and both CHANGELOG heads.
- What came back:
  - Suite: exit 0 in 1:57 wall time; no `FAILED`/`ERROR` line and no
    `N failed` summary anywhere in the log; largest pytest root reported
    `2424 passed, 2 skipped in 70.15s`, and every other root and shell test
    reported passing (e.g. `198 passed, 1 skipped`, `248 passed, 5 skipped`,
    `13/13 mermaid blocks parsed`). The graduated probe
    `loom-code/tests/test_adversarial_no_program_beside_stored.py` is under
    `loom-code/tests/`, one of the suite's four roots.
  - Versions: loom-code 3.49.0 → 3.50.0 in `.claude-plugin/plugin.json`,
    `.codex-plugin/plugin.json`, `plugin.json`, `package.json`; loom-workflow
    5.15.0 → 5.16.0 in the same four files. Root `README.md:17-18,133,150`,
    `loom-code/README{,.ja,.zh-TW}.md` read 3.50.0,
    `loom-workflow/README{,.ja,.zh-TW}.md` read 5.16.0.
  - CHANGELOG: `loom-code/CHANGELOG.md` `## [3.50.0] — 2026-10-27 — feat(closing-review): accept a recorded no-program adversarial outcome`;
    `loom-workflow/CHANGELOG.md` `## [5.16.0] — 2026-10-27 — loom-memory equivalence outcome and six-character label separators`.
  - Constraint spot checks: `check_contract_citations.py` →
    `OK: 1 known-violating files unchanged, no new contract citations`;
    contract manifest version stays 2.3.1 with the `executions` grammar gaining
    the `{kind: adversarial, no_program}` row.
- Evidence: `scratchpad/suite.log`.

## Re-run on 2026-10-27, at 0a27f371

Fix range `7d28c2f1..0a27f371`: intent re-confirm, plan Wave 4, 894a679a
(publish disclosure), 495ebae0 (refusal wording), 0a27f371 (count-free
prose). It touches only `loom-code/` and the change's intent and plan:
`git diff --stat 7d28c2f1..0a27f371 -- loom-workflow README.md` is empty.

- Setup: re-tested. Fresh `git clone` of the branch, checked out at
  `0a27f371`, outside the repository. Then
  `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID loom-code/scripts/loom-python --repair --list-rules`
  → exit 0, rule list printed (first line `adversarial.proportionate …`).
- 1: re-tested in full, every case of section 1, with
  `tools/at_finalize.py <clean> <work> a1` against the 0a27f371 clone
  (`scratchpad/a1-rerun.log`):
  - The no-program outcome alone → exit 0, attestation row
    `{'kind': 'adversarial', 'no_program': '<reason>'}`, status `valid`,
    selection not used. With the reason blanked in the committed attestation
    → `stale (a no-program outcome needs a non-blank reason)`.
  - No record → exit 1,
    `BLOCK finalize.adversarial: the adversarial step left no outcome: record its programs, or a no-program outcome with its reason`.
  - Blank reason → exit 1, `a no-program outcome needs a non-blank reason`.
  - Two records, beside a supplied program, or beside a RED program
    committed in the store → exit 1,
    `a no-program outcome contradicts another adversarial record or a program stored for this change`.
  - Extra field → exit 1, `a no-program record carries only its reason`.
  - In every refusal case, no attestation was written. Every decision is
    the same as in the first run; only the wording changed
    (`probes.py:593-603`).
  - Count-free wording: `grep -rniE "at least one adversarial|one no-program|only adversarial record|must be the only|exactly one no.program|minimum …"`
    over `loom-code/skills`, `agents`, `scripts` and `contract` → no match.
  - Prose: `adversary.md:47`, `build/SKILL.md:114` and
    `adversarial.md:77` now say "a no-program outcome"; closing-review
    `SKILL.md:408` says "the no-program outcome and its reason, with no
    program beside it".
  - Criterion tests: included in the `163 passed` run in section 6.
- 2: carried over. The fix's `probes.py` hunk is confined to
  `missing_adversarial_execution` (lines 573-603). `check_adversarial_proportionate`
  (518-561) and `MAX_PROBE_PROGRAMS` are untouched. The only
  `adversarial.md` edit is "one" → "a" at line 77, outside the ceiling
  sentence at 79-82.
- 3: carried over. The fix range touches no `loom-workflow/` file.
- 4: carried over. The fix range touches no `loom-workflow/` file (the
  templates and `verify_cot_html.py`).
- 5: carried over. `runs_pytest`, `_python_argv` and
  `direct_pytest_style_failure` (`probes.py:678-740`) are outside the fix
  hunk. The command-form paragraph `adversarial.md:146-153` is unchanged.
- 6: re-tested (line new at this re-run). See section 6.
- 7: re-tested.
  - Versions read in the 0a27f371 clone: loom-code 3.50.0 in all four
    manifests; loom-workflow 5.16.0 in all four.
  - README counts of `3.50.0`: root `README.md` 2,
    `loom-code/README{,.ja,.zh-TW}.md` 1 each.
  - CHANGELOG heads: `## [3.50.0] — 2026-10-27 — feat(closing-review): …`,
    which now carries the bullet "`publish` requires the PR body line
    `Adversarial outcome: no program — <reason>` …" under the same heading
    (no new version heading); `## [5.16.0] — 2026-10-27 — …`.
  - Release pins:
    `python -m pytest -q loom-code/tests/test_write_plan_station_text.py -k release_metadata loom-workflow/tests/scripts/test_release_metadata.py`
    → `15 passed, 35 deselected` (`scratchpad/a7-tests.log`).
  - Full package suite: not run by me in this re-run; finalize-review
    executes it and refuses the attestation when it fails. Suite command:
    `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`.

## Re-run on 2026-10-27, at a0966dd7

Fix range `23a7ff2e..a0966dd7`: one commit, a0966dd7, touching exactly
`loom-code/scripts/loom_checker/rule_checks/publish.py` (`validate_disclosed_outcome`
now collects visible lines only from sections whose heading is `Verification`,
from `_body_sections(...)[0]`, and the refusal says "under the Verification
heading") and `loom-code/tests/test_loom_publish.py` (one new test).
`git diff --stat 23a7ff2e..a0966dd7 -- loom-workflow README.md '*/CHANGELOG.md' '*plugin.json' '*/package.json' '*/README*' loom-code/scripts/loom_checker/probes.py loom-code/skills`
is empty.

- Setup: re-tested. Fresh `git clone` of the worktree, checked out at
  `a0966dd7`, in the session scratch directory. Then
  `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID loom-code/scripts/loom-python --repair --list-rules`
  → exit 0, first line `adversarial.proportionate …` (`scratchpad/setup-a0966dd7.log`).
- 6: re-tested in full with `tools/at_a6_rerun.py <clean> <work>` (the
  section-6 driver plus four placement cases), same real code path and same
  network stub and `subprocess.run` guard as section 6. Nothing was pushed
  and GitHub was never called (`scratchpad/a6-rerun.log`):

  | case | body | publish result | outward calls attempted |
  |---|---|---|---|
  | no-program attestation (real finalize-review exit 0, row `{"kind":"adversarial","no_program":"<reason>"}`), status `valid` | line under Verification | validation passed: `Verification valid for <head>`, then stopped at the stubbed `gh repo view` | `repo view` (stubbed, not made) |
  | same | line missing | exit 1, `BLOCK push.contextual-body: the attestation records that the adversarial step left no program; the body must carry exactly this bare line under the Verification heading:` + the full recorded line | none |
  | same | different reason | exit 1, same refusal | none |
  | same | no reason | exit 1, same refusal | none |
  | same | inside an HTML comment | exit 1, same refusal | none |
  | same | inside a code fence | exit 1, same refusal | none |
  | same | as a bullet | exit 1, same refusal | none |
  | same | under `## Follow-ups` only | **exit 1, same refusal** (accepted at 0a27f371) | none |
  | same | under `## Context` only | exit 1, same refusal | none |
  | same | before the first heading | exit 1, same refusal | none |
  | same | under Verification and also under Follow-ups | validation passed, stopped at stubbed `gh repo view` | `repo view` (stubbed, not made) |
  | same | under a `### Adversarial step` sub-heading inside Verification | validation passed, stopped at stubbed `gh repo view` | `repo view` (stubbed, not made) |
  | programs attestation (`python3 -m pytest <probe>`), status `valid` | no outcome line | validation passed (boundary: no line is needed) | `repo view` (stubbed, not made) |

  The `###` case passes because `_body_sections` opens a section only on a
  `## ` heading (`publish.py:116`, `## ([^#\n].*)`), so a deeper heading stays
  inside Verification. Ship's prose (`loom-code/skills/ship/SKILL.md:84-91`)
  puts the line in the paragraph that begins "Under the Verification heading",
  which matches the check.
- Criterion tests in the clean clone:
  `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest -q loom-code/tests/test_loom_publish.py`
  → `70 passed in 21.56s` (`scratchpad/a6-rerun-tests.log`), including the new
  `test_no_program_outcome_line_outside_verification_refused`.
- 1, 2, 3, 4, 5, 7: carried over. The fix touches neither `probes.py`, the
  finalize command, any skill or agent prose, `loom-workflow/`, the
  manifests, CHANGELOGs nor READMEs (the empty `--stat` above).
  `validate_disclosed_outcome` is called only from publish, so finalize-review
  (lines 1, 2, 5) cannot see the change. Full package suite: not run by me;
  finalize-review executes it and refuses the attestation when it fails.

## Re-run on 2026-10-27, at 7df38898

Fix range `db53bc59..7df38898`: one commit, 7df38898, touching
`loom-code/scripts/loom_checker/probes.py` (`missing_adversarial_execution`:
the reason must equal its `strip()`, contain no `\n`/`\r` and no `<!--`),
`rule_checks/publish.py` (`validate_disclosed_outcome`: inside a
`Verification` section, a line matching `^ {0,3}#{1,2}(?:[ \t]|$)` ends it),
`command_handlers/publish.py` (the disclosure check no longer sits under
`if status == "valid"`), `skills/ship/SKILL.md`, the 3.50.0 entry of
`loom-code/CHANGELOG.md`, and two test files.
`git diff --stat db53bc59..7df38898 -- loom-workflow README.md '*/README*' '*plugin.json' '*/package.json' loom-code/skills/closing-review loom-code/agents`
is empty. This section supersedes the a0966dd7 section for lines 1, 6 and 7.
Section 1's and section 6's notes that the disclosure runs only for status
`valid` no longer hold.

- Setup: re-tested. Fresh `git clone` of the worktree, checked out at
  `7df38898`, in the session scratch directory. Then
  `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID loom-code/scripts/loom-python --repair --list-rules`
  → exit 0, first line `adversarial.proportionate …` (`scratchpad/setup-7df38898.log`).
- 1: re-tested in full. `tools/at_finalize.py <clean> <work> a1` (every case
  of section 1) plus `tools/at_a1_reasons.py <clean> <work>` (new reason
  shapes), real launcher `finalize-review`, status read with the real
  `verification_status` (`scratchpad/a1-r3.log`, `scratchpad/a1-reasons-r3.log`):

  | case | adversarial input | finalize-review | status |
  |---|---|---|---|
  | positive | `[{"no_program": "<reason>"}]` | exit 0, row `{'kind': 'adversarial', 'no_program': '<reason>'}` | `valid` |
  | reason blanked in the committed attestation | (tampered) | — | `stale (a no-program outcome needs a reason on one line, with no surrounding whitespace or HTML comment)` |
  | no record | `[]` | exit 1, `the adversarial step left no outcome: record its programs, or a no-program outcome with its reason` | none |
  | blank `"   "` / empty `""` | | exit 1, `a no-program outcome needs a reason on one line, with no surrounding whitespace or HTML comment` | none |
  | two records / beside a supplied program / beside a stored RED program | | exit 1, `a no-program outcome contradicts another adversarial record or a program stored for this change` | none |
  | extra field | | exit 1, `a no-program record carries only its reason` | none |
  | reason with an em dash inside | `"every attack failed — no repository test covers it"` | exit 0 | `valid` |
  | trailing space / leading space | | exit 1, the one-line refusal | none |
  | `\n` inside / `\r` inside | | exit 1, the one-line refusal | none |
  | `<!-- x -->` inside / lone `<!--` inside | | exit 1, the one-line refusal | none |
  | U+2028 / form feed `\x0c` / NEL `\x85` inside | (case 6 of `at_a6_r3.py`) | **exit 0**, attestation written | `valid` |

  Prose: `loom-code/skills/closing-review/SKILL.md:416` still says only
  "`finalize-review` refuses a blank reason"; it does not state the
  one-line / no-comment rule the code now enforces (the refusal message
  does).
- 6: re-tested in full with `tools/at_a6_r3.py <clean> <work>` (all
  a0966dd7 cases plus cases 3-6 below), same real code path, same network
  stub and `subprocess.run` guard. Nothing was pushed and GitHub was never
  called (`scratchpad/a6-r3.log`). "passed" = printed
  `Verification <status> for <head>`, then stopped at the stubbed
  `gh repo view`; "refused" = exit 1,
  `BLOCK push.contextual-body: … the body must carry exactly this bare line under the Verification heading:`
  + the recorded line, no outward call.

  | case | body | result |
  |---|---|---|
  | valid no-program | line under Verification | passed |
  | same | missing / wrong reason / no reason / in HTML comment / in code fence / as bullet | refused (each) |
  | same | only under `## Follow-ups` / only under `## Context` / before first heading | refused (each) |
  | same | under Verification and Follow-ups | passed |
  | same | under `### Adversarial step` / `#### Deeper` inside Verification | passed |
  | same | after `# Aside` inside Verification | refused |
  | same | after `   ## Notes` (3-space indent) / `  # Aside` (2-space) / bare `##` | refused (each) |
  | same | after `    ## Notes` (4-space indent, not a heading) / `##Notes` (no space, not a heading) | passed |
  | same | line, then `# Aside` later in Verification | passed |
  | programs attestation, valid | no outcome line | passed (boundary) |
  | no-program attestation, then a later commit: `stale (attestation functional content digest does not match the selected tree)` | line under Verification + matching status line | passed, printed `publishing anyway` |
  | same stale | line missing | refused |
  | same stale | line only under Follow-ups | refused |
  | no attestation: `absent` | no outcome line | passed (boundary: nothing records no-program) |
  | valid, reason containing U+2028 / `\x0c` / `\x85` | the exact recorded line under Verification | **refused**; the printed "line to carry" itself breaks across two lines |

  The last row: `missing_adversarial_execution` rejects only `\n`/`\r`, but
  `_body_sections` splits the body with `str.splitlines()`
  (`rule_checks/publish.py:103`), which also breaks at `\x0b \x0c \x1c-\x1e
  \x85    `. A reason with one of those is accepted at
  finalize-review and can never be disclosed, so publish refuses every body
  until the change is finalized again — the class of defect this fix set out
  to close, not covered for these characters.
- Criterion tests in the clean clone:
  `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest -q loom-code/tests/test_loom_publish.py loom-code/tests/test_selection_finalize.py loom-code/tests/test_loom_attestation.py loom-code/tests/test_adversarial_no_program_beside_stored.py`
  → `168 passed in 63.93s` (`scratchpad/a1a6-tests-r3.log`).
- 7: re-tested. Versions and README strings untouched by the fix (empty
  `--stat` above); root `README.md` still carries `3.50.0` twice. The
  CHANGELOG edit stays under `## [3.50.0] — 2026-10-27 — feat(closing-review): …`
  (one bullet reworded, one added; no new heading). Release pins:
  `python -m pytest -q loom-code/tests/test_write_plan_station_text.py -k release_metadata loom-workflow/tests/scripts/test_release_metadata.py`
  → `15 passed, 35 deselected` (`scratchpad/a7-tests-r3.log`). Full package
  suite: not run by me; finalize-review executes it and refuses the
  attestation when it fails. Suite command:
  `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`.
- 2: carried over. The `probes.py` hunk is confined to
  `missing_adversarial_execution` (lines 582-603);
  `check_adversarial_proportionate` and `MAX_PROBE_PROGRAMS` are untouched,
  and no `references/adversarial.md` line changed.
- 3, 4: carried over. The fix touches no `loom-workflow/` file.
- 5: carried over. `runs_pytest`, `_python_argv` and
  `direct_pytest_style_failure` are outside the hunk; `adversarial.md` is
  unchanged.
