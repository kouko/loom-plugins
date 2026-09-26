# Step policy boundaries — acceptance test evidence

Tried on 2026-09-26 in a fresh local clone at b7aa3cb9fd5c83d275176587478352801720cca9. The witness did not implement the change. This is a first run, not a carry-over.

## Setup and limits

`git clone --local --no-hardlinks . /tmp/loom-acceptance-b7aa3cb9` succeeded; `git rev-parse HEAD` returned the target SHA. Read README installation and development instructions and loaded the cloned station files, not installed cached skills. `python3 loom-code/scripts/loom_checker.py contract --require 2.1` returned `contract 2.3.1 satisfies requires-contract >=2.1`. `python3 scripts/sync_codex_manifests.py --check --all` exited 0.

README's isolated environment was used for every focused pytest run: `uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest ...`. Initial sandbox cache access failed; an alternate temporary cache could not resolve PyPI. Narrow escalation using the existing cache succeeded. No global installation or base environment modification was made. Marketplace install commands were read but not executed: they would update the user's installed plugins and load marketplace HEAD rather than this clean target. Host plugin installation/hook firing remains unverified.

An initial mixed code/design pytest invocation returned 1 failed, 23 passed: `test_omitted_artifacts_keep_intent_requirements[bound]` could not import `test_selection_store`. This was an invalid combined invocation, not a product finding: `scripts/run_package_tests.py:15-18` explicitly requires separate sessions because design's importlib pytest configuration breaks code's sibling imports. Correct separate sessions passed below.

The witness read actual write-plan, build, architecture-design, and code-lens instructions and performed their relevant toy actions in a newly initialized temporary Git repository. This is independent fresh-context behavioral dry-run evidence plus actual CLI/filesystem/test results, not a full host-to-agent end-to-end run. No implementation worker, closing reviewer, publication, or real user ratification was invoked. No product repair was made.

## 1. Plain-language omissions preserve other requirements

Toy user input: “規格和計畫都略過，直接做；其他檢查照常。” The witness followed write-plan's instruction handling and build's scope handling, wrote the existing `skipped-by-instruction` lines into intent Constraints, and committed them before intake. No `selection propose`, confirmation code, or replacement artifact was requested.

Actual CLI transcript (checker path in the clean clone):

```text
selection show 2026-09-02-a => exit 0
bound: false; skip: []; code: null; narrow_change_line: null
run: spec, plan, implementer, tdd, reviewers, adversarial, acceptance-test, package-tests
intake write-plan 2026-09-02-a [before instruction] => exit 1
BLOCK intake.spec-ready: needs-design: yes but no spec
intake write-plan 2026-09-02-a [after committed instructions] => exit 0
intake write-plan 2026-09-02-a [status changed to open] => exit 1
BLOCK intake.confirmed: write-plan accepts only status: confirmed <date>; status is open.
```

The scoped test `test_omitted_artifacts_keep_intent_requirements` exercised intent, plan, bound selection, and spec-only carriers; `test_intake_quotedskip_keepsrequirements` checked fenced examples cannot waive requirements. Both passed in the supported code session. Verdict partly because actual full conversational orchestration remains unverified.

## 2. Missing spec and plan no longer block the dry-run handoff

After successful intake, both `docs/loom/2026-09-02-a/spec.md` and `plan.md` were absent. Following build §1, the witness omitted the plan command and produced this bounded handoff:

```text
Intent: confirmed toy intent
Task: add report cache
Files: report.py, tests/test_report.py
Acceptance: 1
Test command: python -m pytest tests/test_report.py
Risk: preserve report output
Omitted: spec, plan
Retained: implementer, TDD, adversary, package-tests, review, acceptance
```

No implementation was performed. This demonstrates intake and dry-run scope delivery without omitted artifacts, not full downstream completion. Plan validation itself remains strict when retained; the station omits its invocation when plan is skipped. Verdict partly.

## 3. Early and late scope decisions

The initial toy branch had only a committed intent delta; `selection show` retained all eight steps and emitted no narrow-change line. The focused regression `test_entry_keeps_steps_before_implementation_even_on_a_docs_delta` also tested absent, untracked, and staged production files. Late simplification was exercised by `test_narrow_delta_finalizes_with_no_adversarial_artifact`; explicit retained requirements by `test_bound_kept_adversarial_required_on_narrow_delta`. All passed. Verdict works for these executed command scenarios.

## 4. Architecture draft and ratification boundaries

Read `loom-code/skills/write-plan/SKILL.md:326-332`, `loom-code/skills/closing-review/references/lenses.md:59`, and architecture-design steps 1–4. Independent dry-run decisions: a draft's proposed placement is advisory and produces no mandatory planning change; the draft architecture-conformance dimension is N/A; the same rule in a ratified document constrains placement and a violation requires an important finding. These decisions were made by this fresh-context witness, not inferred from string assertions as full behavioral proof.

Actual suite isolation exercise used sibling temporary `live/` and `draft/` trees, each with its own `tests/`. A deliberately failing draft `test_rule` asserted `False, "MB-1 toy violation"`:

```text
python -m pytest -q tests [live, base test only] => exit 0; 1 passed
python -m pytest -q tests [draft, failing guard] => exit 1; 1 failed
copy guard to live [simulated ratification activation, not real user confirmation]
python -m pytest -q tests [live] => exit 1; 1 failed, 1 passed
replace draft guard with passing proposal [redesign]
python -m pytest -q tests [draft] => exit 0; 1 passed
python -m pytest -q tests [live, old active guard retained] => exit 1; 1 failed, 1 passed
```

The intentional failures prove isolation and retained guard execution; they are not shipped test failures. This activation test deliberately bypasses the normal requirement that the proposed guard pass before ratification to observe enforcement on a violating tree. Actual validator coverage (draft versus ratified document and guard path requirements) passed in the separate design session. Verdict partly: a complete architecture interview, user ratification, worker planning, and reviewer dispatch were not run.

## 5. Existing carriers and release checks

After the skip walkthrough, ordinary files were exactly `seed.txt` and the existing intent path. `.git/loom/selections` did not exist. No replacement plan, phase store, or confirmation record was created. Reviewed `git diff --stat origin/main...HEAD`: production changes extend existing policy/command/station files; new tracked files are the change's intent/spec/plan records, with existing manifests and changelogs updated. This structural observation complements the executed no-new-state scenario; it is not a universal proof over every workflow.

Successful focused commands:

```sh
uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest -q loom-code/tests/test_loom_checker_intake.py loom-code/tests/test_selection_store.py loom-code/tests/test_selection_finalize.py loom-code/tests/test_architecture_doc_consumers.py loom-code/tests/test_write_plan_station_text.py -k 'omitted_artifacts or quotedskip or entry_keeps or narrow_delta or bound_kept or architecture or current_release_metadata'
# 15 passed, 207 deselected in 12.28s
uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest -q loom-design/tests/architecture-design/test_validate_architecture_output.py loom-design/tests/architecture-design/test_architecture_skill.py
# 22 passed in 0.08s
```

The full package suite was intentionally not run by this witness. The coordinator states package-tests is retained and finalize-review will execute the suite and block attestation on failure. Required full command from README:

```sh
uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q
```

## Findings and decisions

No confirmed product defect was observed. No dismissed important/fatal findings were supplied. Partial verdicts identify missing full host workflow evidence, not a waiver or fabricated pass. The mixed-session import error was resolved by the repository's documented test grouping without changing product files.
