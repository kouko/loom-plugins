# A standing ARCHITECTURE.md that agents are held to — acceptance test evidence

Evidence stays in English per the acceptance-tester contract; the report is in Traditional Chinese.

Tried on 2026-09-25, in a clean copy of the project at 8b80c9ce
(`git worktree add $TMPDIR/at-arch/clean HEAD`; all loom scripts below were
run from that clean copy, never from the working tree).

Setup check: `python3 loom-code/scripts/loom_checker.py contract --require 2.1`
in the clean copy → `contract 2.3.1 satisfies requires-contract >=2.1`, exit 0
(Step 0 of the new skill). The `architecture` skill is listed in both plugin
manifests (`loom-design/.claude-plugin/plugin.json:19`,
`loom-design/.codex-plugin/plugin.json:18`), the zh-TW/en/ja READMEs and the
`using-loom-design` router table (`loom-design/skills/using-loom-design/SKILL.md:20`).

Throwaway project (`$TMPDIR/at-arch/proj`, git init): a tiny Python CLI
`notes` with `src/notes/{__init__,__main__,cli,store}.py`, `tests/test_store.py`,
`pyproject.toml` (pytest `testpaths = ["tests"]`), a README, one intent
`docs/loom/intent/2026-09-25-add-tags.md`, and
`docs/loom/KICKOFF-DEFAULTS.md` declaring
`- package-tests: python3 -m pytest -q — ...`. Before the tool ran: 1 passed.

I played the agent following `loom-design/skills/architecture/SKILL.md` and
its two references, and played the user; as user I picked the recommended
option every time and said "yes" to the restatement.

## 1. In a repository without ARCHITECTURE.md, a loom-design tool reads the project's requirements and existing code and proposes an architecture covering module split and dependency direction, main technology choices, folder structure and required CI stages, giving at least two options with their trade-offs for each open choice, and the user picks.
- How I tried it: followed SKILL.md Step 1 (no ARCHITECTURE.md → design mode) and Step 2 "Read first" (README, the intent, `src/`, `tests/`, `pyproject.toml`; no CI present), then "Propose" with options drawn from `references/design-know-how.md`.
- What came back (the proposal as produced):
  - Module split — drivers: one small CLI, one storage backend. Option A two layers `cli → store` (good: minimal, matches code; bad: a second backend means a refactor). Option B ports and adapters (good: swappable backend; bad: structure for a presumptive feature, YAGNI). Recommended A; wrong if a second backend is planned. Picked A.
  - Technology — Python stdlib + sqlite3 + pytest are settled by the existing code: stated, not re-opened (SKILL.md Step 2 allows this).
  - Folder structure — src layout + `tests/` settled by the code (stated). File-size ceiling open: 300 lines (ESLint default) vs 1000 (Pylint default), trade-offs from the know-how table. Recommended 300. Picked 300.
  - CI stages — tests only vs lint then tests (know-how "baseline order"). Recommended lint then tests. Picked it.
- Evidence: every open choice had two options with good/bad trade-offs and a recommendation; SKILL.md Step 2 requires "at least two options" and "Never present a single answer". Limitation: the proposal was produced by me following the text, so this shows the text can be followed as written, not that every agent will.

## 2. The chosen design is written as a user-ratified ARCHITECTURE.md at the repository root holding the design decisions with their reasons and the structural rules, with no project overview and no data models or API interfaces.
- How I tried it: wrote `ARCHITECTURE.md` at the project root per `references/architecture-md-schema.md` (D-1..D-5 decisions; MB-1, FP-1, FS-1 with guards; CI-1 `check: review`), then:
  - `python3 <clean>/loom-design/scripts/architecture-design/validate_architecture_output.py ARCHITECTURE.md --draft` → `OK`, exit 0
  - same without `--draft`, before ratifying → `INVALID ... no 'ratified-by:' line`, exit 1
  - added `ratified-by: tester 2026-09-25`, re-ran without `--draft` → `OK`, exit 0; committed (`1fed7aa docs(loom): ARCHITECTURE.md ratified` in the throwaway repo)
  - negative copies: appended `## Overview` → `section '## Overview' is not allowed`, exit 1; appended `## Data models` → `section '## Data models' is not allowed`, exit 1; appended `### API interfaces` + `- GET /notes` under CI stages → both lines rejected as breaking the rule grammar, exit 1
  - a malformed ratify line `ratified-by: tester 2026-09-25 (re-ratified after re-design)` → `'ratified-by:' line is malformed`, exit 1
- Evidence: captured validator output above.

## 3. Every rule in that file that can be checked mechanically comes with a guard test that the repository's package suite runs.
- How I tried it: wrote `tests/arch/test_boundaries.py` (MB-1), `tests/arch/test_placement.py` (FP-1), `tests/arch/test_file_size.py` (FS-1); CI-1 is `check: review`. Ran the declared package-tests command `python3 -m pytest -q`.
- What came back: `4 passed` (1 original + 3 guards). Validator with a rule pointing at a non-existent guard (`check: tests/arch/missing.py`) → `rule FS-1 names guard 'tests/arch/missing.py', which does not exist ...`, exit 1.
- Evidence: captured output. Observation: the validator checks that each guard file exists, not that the package-tests command actually collects it; that part rests on the agent following SKILL.md Step 3.

## 4. When a change breaks a checkable rule, the package suite fails with a message that names the rule, the offending file, and the two ways out: conform to the rule, or change the rule and its guard together.
- How I tried it: added `helpers.py` at the project root (breaks FP-1) and `from notes.cli import main` to `src/notes/store.py` (breaks MB-1), ran `python3 -m pytest -q`.
- What came back: `2 failed, 2 passed`, with
  - `AssertionError: MB-1 (src/notes/store.py never imports notes.cli) broken by src/notes/store.py importing notes.cli. Conform to the rule, or change the rule and its guard together in ARCHITECTURE.md and re-ratify.`
  - `AssertionError: FP-1 (every Python source file lives under src/notes/ and every test under tests/) broken by helpers.py. Conform to the rule, or change the rule and its guard together in ARCHITECTURE.md and re-ratify.`
  Reverted → `4 passed`.
- Evidence: captured output. The message wording is what SKILL.md Step 3 and the schema's "Guard failure message" section tell the agent to write.

## 5. When ARCHITECTURE.md exists, the plan for a change that adds or moves files places them by its rules and names the rule it followed.
- How I tried it: read `loom-code/skills/write-plan/SKILL.md` Step 5 "Architecture." paragraph (lines 319–324) as a planner for the throwaway intent "Add tags to notes", with the plan template's `- Risk:` task line (`loom-code/contract/templates/plan.md:19`).
- What came back: the text directs the planner to read root `ARCHITECTURE.md` before the Task DAG, place added/moved files by its rules and name the rule id on the Risk line. The planner would place `src/notes/tags.py` and `tests/test_tags.py` and write `Risk: FP-1 (source under src/notes/, test under tests/); MB-1 (store must not import cli)`. A rule-breaking task changes rule + guard via the re-design mode.
- Evidence: the paragraph above; tests `loom-code/tests/test_architecture_doc_consumers.py` passed (see suite section). No full write-plan run was performed.

## 6. When ARCHITECTURE.md exists, closing review reports whether the change conforms to it, and a violation is a finding that sends the change back; this uses the existing reviewers, with no reviewer added.
- How I tried it: read `loom-code/skills/closing-review/references/lenses.md` and `loom-code/agents/reviewer.md`; `git diff --quiet 499f127b..HEAD -- loom-code/scripts/loom_checker/reviewers.py loom-code/scripts/loom_checker/command_handlers/reviewer_count.py` → unchanged.
- What came back:
  - `lenses.md:59` adds the `architecture-conformance` row to the code lens ("Code — twelve dimensions"); `reviewer.md:49` lists it in the code lens. N/A rule extended at `lenses.md:43`.
  - Reviewer-count code is untouched; the only change under `loom-code/agents/` is the one dimension-list line.
  - Send-back: `lenses.md` "Severity and verdict" sends a change back only for a fatal finding or two importants (Round 2 batches fatal and important). The new row says "A violation is a finding whose fix is concrete" but sets no severity floor, so a reviewer may rate a rule violation `nit`, which yields `PASS` and does not send the change back.
- Evidence: `lenses.md:17-29`, `lenses.md:59`. No live closing review with a violating diff was run.

## 7. When ARCHITECTURE.md is absent, every change shows a warning line alongside the existing standing-document warnings, never blocks, and the existing waiver silences it; review scores that conformance check as not applicable.
- How I tried it: throwaway repo `$TMPDIR/at-arch/bare` with an `kind: engineering` intent; `python3 <clean>/loom-code/scripts/loom_checker.py standing docs/loom/intent/2026-09-25-add-tags.md`.
- What came back:
  - no standing docs → `WARN: this repo has no PRINCIPLES.md or DESIGN.md or ARCHITECTURE.md yet.` + the two fixed WARN lines, exit 0
  - `- standing-docs: waived — throwaway test repo (2026-09-25)` in KICKOFF-DEFAULTS → no output, exit 0. (A first attempt with an un-bulleted `standing-docs: waived` line still warned; the parser only reads `- key: value` lines, which is the documented format — my setup error, not the change's.)
  - `ARCHITECTURE.md` at root, other two missing → `WARN: this repo has no PRINCIPLES.md or DESIGN.md yet.`, exit 0
  - `ARCHITECTURE.md` only under `docs/` → still named as missing, exit 0 (root-only, as the spec says)
  - only ARCHITECTURE.md missing → `WARN: this repo has no ARCHITECTURE.md yet.` followed by the fixed line "…cannot check any change for consistency against what this product is supposed to be." (generic wording, reads a little off for an architecture file)
  - all three present → silent, exit 0
  - N/A: `lenses.md:43` "no `ARCHITECTURE.md` — scores `N/A` with the reason", and the row's "Scored only when that file exists, else `N/A`".
- Evidence: captured output above.

## 8. When a change alters the structure, the same tool re-designs the affected part and updates its design decisions, rules and guards together.
- How I tried it: in `proj` (with ARCHITECTURE.md present → SKILL.md Step 1 re-design mode) simulated adding a `tags` module: added decision D-6 (options: separate tags module vs fold into store), rule MB-2 (store never imports notes.tags), extended `tests/arch/test_boundaries.py` to a parametrized MB-1/MB-2 guard, added `src/notes/tags.py`; ran the validator, the suite, and a violating import.
- What came back: validator `OK`, exit 0; suite `5 passed`; `from notes.tags import tagged` in store → `AssertionError: MB-2 (src/notes/store.py never imports notes.tags) broken by src/notes/store.py importing notes.tags. Conform to the rule, or change the rule and its guard together in ARCHITECTURE.md and re-ratify.`; reverted. One commit carried all three: `ARCHITECTURE.md | 2 ++`, `src/notes/tags.py | 3 +++`, `tests/arch/test_boundaries.py | 14 +++++++++-----`.
- Evidence: captured output. Observation: nothing mechanical detects a re-design that skips re-ratification (same-day `ratified-by:` line stays valid); it rests on SKILL.md Step 1/4.

## Suite
- Criterion tests (clean copy): `env -u FORCE_COLOR uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest -q -p no:cacheprovider --color=no loom-design/tests/architecture loom-code/tests/test_architecture_doc_consumers.py loom-code/tests/test_loom_checker_standing.py` → `56 passed in 3.63s`.
- Package suite, run once at the station's request: `env -u FORCE_COLOR uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q` → exit 0; pytest roots `2351 passed, 2 skipped`, `267 passed, 1 skipped`, `261 passed`, `196 passed`, … all passing, no failures. `finalize-review` runs it again and blocks on failure.

# Re-run after fixes (87f50da3..21289e5d, plan tasks W3-01, W3-02)

Tried on 2026-09-25 in a new clean copy at 21289e5d
(`git worktree add --detach $TMPDIR/at-arch/clean2 21289e5d`); every loom
script below ran from that copy. Reused throwaway repos `proj` and `bare`;
built `proj3` (same notes CLI, no `docs/loom/KICKOFF-DEFAULTS.md`).

Setup check: `python3 loom-code/scripts/loom_checker.py contract --require 2.1`
→ `contract 2.3.1 satisfies requires-contract >=2.1`, exit 0; `architecture`
still listed in `loom-design/.claude-plugin/plugin.json:19` and
`loom-design/.codex-plugin/plugin.json:18`.

Scope, checked against `git diff 87f50da3..21289e5d`:
- Re-tested A2 (validator), A3 (`SKILL.md` Step 3/5), A5 (`write-plan/SKILL.md:319-325`), A6 (`lenses.md:59`), A7 (`standing.py` STANDING_WARN), A8 (`SKILL.md` Step 4 re-ratify; schema "Updating" section removed).
- Carried over A1: diff to `design-know-how.md` only re-sources the Pylint 1000-line default and rewords security-scanning cost; the A1 proposal's options (300 vs 1000 lines, lint-then-tests) are unchanged.
- Carried over A4: `SKILL.md` Step 3 now points to the schema's "Guard failure message" section, which the diff does not touch; the same message was observed again under A3.

## A2 re-run
`V = python3 $TMPDIR/at-arch/clean2/loom-design/scripts/architecture-design/validate_architecture_output.py`, in `proj`:
- `V ARCHITECTURE.md` → `OK`, exit 0
- two `ratified-by:` lines → `more than one 'ratified-by:' line; keep exactly one, replacing the old line when re-ratifying`, exit 1 (also with `--draft`, exit 1)
- `This project is a small notes CLI.` under the title → `line above the first '## ' section is not allowed; ...`, exit 1
- `## Decisions` emptied → `section '## Decisions' is empty; ...`, exit 1
- no `ratified-by:` → `--draft` OK exit 0; without `--draft` `no 'ratified-by:' line; ...`, exit 1
- `## Overview` / `## Data models` → `section ... is not allowed`, exit 1 each; `### API interfaces` + `- GET /notes` → both lines break the rule grammar, exit 1
- `## File size` emptied → `OK`, exit 0 (empty rule sections accepted — the dismissed Codex finding; behaves as the dismissal says)

## A3 re-run
In `proj3` (no `docs/loom/KICKOFF-DEFAULTS.md`), following `SKILL.md` Step 3: as agent proposed `python3 -m pytest -q` (pyproject `testpaths = ["tests"]`), as user accepted, recorded
`- package-tests: python3 -m pytest -q — runs tests/ incl. tests/arch guards, pytest testpaths in pyproject.toml (2026-09-25)`.
Wrote `ARCHITECTURE.md` (D-1, FP-1 → `tests/arch/test_placement.py`, other rule sections empty); `V --draft` OK exit 0; added ratified line; `V` OK exit 0.
Step 5: `git add ARCHITECTURE.md tests/arch/test_placement.py docs/loom/KICKOFF-DEFAULTS.md` → commit `2b7e668` shows `ARCHITECTURE.md`, `docs/loom/KICKOFF-DEFAULTS.md` (the guard file was already in my setup commit).
Ran the recorded command → `2 passed`; with `helpers.py` at root → `1 failed, 1 passed`, `AssertionError: FP-1 (every Python source file lives under src/notes/ and every test under tests/) broken by helpers.py. Conform to the rule, or change the rule and its guard together in ARCHITECTURE.md and re-ratify.`; removed `helpers.py`.
Limitation: the validator checks the guard file exists, not that the recorded command collects it.

## A5 re-run
`loom-code/skills/write-plan/SKILL.md:319-325` now: place files by the rules, name the rule id on the Risk line; when a task must break a rule the planner runs the `architecture` re-design mode with the user before Build and lists `ARCHITECTURE.md` and the guard in the task's Files (template `loom-code/contract/templates/plan.md` `- Files:` line); "an implementer never changes a rule on its own". No full write-plan run.

## A6 re-run
`lenses.md:59` adds "A violation of an `ARCHITECTURE.md` rule is at least `important`, so the round sends it back to Build." `closing-review/SKILL.md:266` Round 2 "Batch fatal and important findings, return to Build", and `:295` collects every fatal or important finding before fixes — so a single important is sent back even when the verdict is `PASS_WITH_NOTES`. `git diff --quiet 499f127b..HEAD -- loom-code/scripts/loom_checker/reviewers.py loom-code/scripts/loom_checker/command_handlers/reviewer_count.py` → exit 0 (unchanged); `reviewer.md:49` still one dimension-list line. No live closing review with a violating diff was run.

## A7 re-run
`bare`, `python3 $TMPDIR/at-arch/clean2/loom-code/scripts/loom_checker.py standing docs/loom/intent/2026-09-25-add-tags.md`:
- none present → `WARN: this repo has no PRINCIPLES.md or DESIGN.md or ARCHITECTURE.md yet.` / `WARN: without it, the closing-review station cannot check any change against it.` / waiver hint, exit 0
- `- standing-docs: waived — throwaway test repo (2026-09-25)` → silent, exit 0
- only ARCHITECTURE.md missing → `WARN: this repo has no ARCHITECTURE.md yet.` + the same neutral line 2, exit 0
- all three present → silent, exit 0
- N/A: `lenses.md:43` and `:59` unchanged in meaning.

## A8 re-run
In `proj`: replacing `ratified-by: tester 2026-09-25` with `... 2026-09-26` → `OK`, exit 0; a second line is rejected (A2). `SKILL.md` Step 1 keeps "update the affected decisions, rules and guards in the same commit"; Step 4 "replace the existing `ratified-by:` line; never add a second". Suite `python3 -m pytest -q` → `5 passed`. Still nothing mechanical detects a re-design that keeps the old date.

## Suite (re-run)
- Criterion tests in the clean copy: `env -u FORCE_COLOR uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest -q -p no:cacheprovider --color=no loom-design/tests/architecture loom-code/tests/test_architecture_doc_consumers.py loom-code/tests/test_loom_checker_standing.py` → `58 passed in 3.60s`.
- Full package suite not run by me this round; `finalize-review` runs `env -u FORCE_COLOR uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q` and blocks on failure.
