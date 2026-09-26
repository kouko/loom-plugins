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

## Extended scoped run on 2026-09-26, candidate b7aa3cb9

This extension supersedes the initial partly verdicts where actual agent execution is documented below. It does not require publication, installed-host hook firing, or a full architecture interview: none is part of the five requested outcomes. Fixture-user instructions are test data only and do not skip verification of the real change.

### 1–2. Actual native-dispatched implementation without spec or plan

Created a fresh toy Git repository with an empty existing `greeting(name)` implementation, README's standard-library unittest command, and a confirmed intent whose Acceptance requires `greeting("Ada") == "Hello, Ada!"`. No spec or plan was supplied. Fixture request: “規格和計畫都略過，直接修好 greeting；保留實作代理與先寫失敗測試。這個暫存案例略過對抗、完整套件、closing review 和發布。不要改外面的正式專案。”

Executed candidate `loom-code/scripts/dispatch_profile.py` with null model and effort, empty capabilities, inheritance true, ordinary evidence. Result: `outcome: dispatch`, `effective_profile: inherited`, `overrides: null`, `reason: unobservable-main-profile`. Dispatched a fresh-context native implementer with resource paths to candidate Build/implementer contracts and fixture request/intent; no expected solution was passed. The witness did not implement the solution.

Observed actual agent result and artifacts:

```text
selection show 2026-09-26-toy-greeting: exit 0; bound false, skip []
d8c4445 docs(fixture): record explicitly omitted workflow steps
python3 -m unittest discover -s tests -v [RED before implementation]: exit 1
AssertionError: '' != 'Hello, Ada!'; Ran 1 test; FAILED (failures=1)
python3 -m unittest discover -s tests -v [GREEN after implementation]: exit 0
Ran 1 test; OK
60dcb66 fix(greeting): return the requested named greeting
changed files: greeting.py, tests/test_greeting.py
git status --short: empty
Requested confirmation: none. Blocker: none.
```

The witness read the actual agent report `/tmp/loom-downstream-result.md`, inspected the commits and focused test file, and independently reran the focused unittest: 1 test, OK. Spec/plan were absent. Eight test lines were added. The agent preserved the one-argument public function interface. Its only concern was `sync-trunk` WARN because the toy repository has no remote; candidate policy explicitly permits continuing on this WARN. No publication or real-project skips occurred. Together with the earlier real intake negative cases, criteria 1 and 2 now work over the requested scope.

### 3 and 5. Previous evidence retained

The candidate implementation did not change. The new actual downstream run also used only the existing intent carrier and created only the scoped production/test files; no replacement planning document or selection confirmation was needed. Prior focused test results remain applicable. No full package suite was run by this witness.

### 4. Actual fresh-context architecture consumer artifacts

Created two toy snapshots with the same FP-1 rule, `Python implementation files live under src/`, and a proposed root-level `greeting.py` addition. Only the second snapshot carried `ratified-by: fixture-user 2026-09-26`. A fresh native reader received paths to both documents, candidate write-plan and code lenses, and the proposed change; no expected verdict was supplied.

The initial dispatch hit the host concurrency limit. The profile resolver's `host-rejection` event returned inherited/no overrides, `reason: host-rejection-replacement`. After the implementer finished, the fresh reader dispatch succeeded. This was a capacity limit, not a candidate behavior failure.

The reader wrote `/tmp/loom-architecture-reader/verdict.md`; the witness read the artifact. Actual output:

```text
Draft: N/A. No ratified-by line; rules advisory. Findings: none.
Planned task: add greeting.py at root.
Risk: draft FP-1 cannot require a move or block planning.

Ratified: PASS_WITH_NOTES, one important finding, returns to Build.
Finding: root greeting.py violates FP-1.
Anchor: ratified ARCHITECTURE.md:2 (ratification), :11 (FP-1).
Concrete fix and planned task: add src/greeting.py.
Risk: follow ratified FP-1, preserve MB-1 independence and FS-1 size bound.
```

The verdict label matches the supplied lens severity rubric (one important => PASS_WITH_NOTES); the reader explicitly required correction and did not treat it as a clean pass. Neither architecture document was modified. Combined with the existing executed live/draft/redesign guard isolation checks, criterion 4 works over the requested planning, review, and ordinary-test boundaries. Earlier first-run `partly` text is retained as historical evidence and superseded by this extension, not silently promoted from text assertions. A full design interview and installation/publication were not run and are outside these acceptance outcomes.

No product defect emerged from the extension. All five final report rows are works. Only scoped fixture code, tests, commits, and reader artifacts were created; the real candidate implementation was unchanged.
