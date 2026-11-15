# Independent blinded quality audit — two

All six outputs are acceptable. No material or critical issue was established. Pairwise judgments: C1 tie; C2 tie; C3 Y, by a modest useful-evidence advantage rather than a guardrail failure in X. These judgments concern the bounded questions, not production adoption of either hidden condition.

## Scope and verification

I read the audit rubric, three case files, six research outputs and six trajectories, then inspected the cited actual project sources. I did not inspect variants, manifest, protocol, metrics, other audits or session/project memories. No network, test execution, installation, model replay or commit was performed. Only this audit file was written.

Output anchors below use `runs/<case-condition>/research.md:<line>`, relative to this pilot directory. Project-source anchors use repository-relative paths. All 64 output Markdown links resolve to existing local files; numeric line anchors were checked against file lengths. Relevant target text was inspected directly. Heading-target rendering and immutable historical file identity were not independently verified. This is a source-backed audit of retained records, not a reconstruction or certification of past executions.

Trajectories are self-reported lists, not independently captured complete tool transcripts. Their declared source reads and lack of experiments are consistent with the reports, but neither completeness nor all negative execution claims can be independently certified. No exact model snapshot, token/cost telemetry, or comparable full-task timing is available. Different start boundaries, grouping of nested calls and counting conventions prevent treating listed elapsed times/tool counts as causal efficiency evidence. No consequential prerequisite-read omission is established; absence from a self-reported inventory alone would not prove a missing read.

## C1 — suite coverage

### C1-X: acceptable

- `runs/C1-X/research.md:23–28` correctly identifies the four configured roots, Python filename eligibility, shell discovery, root-relative local exclusions, foreign-tree exclusions and selected-group behavior. Actual source is `scripts/run_package_tests.py:53,68–113,123–149,153–176`; foreign discovery limitations are supported by `loom-code/scripts/repo_files.py:73–94,97–120,123–145`.
- The important nuance at output line 26 is correct: dotted/underscored workflow folders are not separate sessions, but may remain in a top-level pytest directory. The source only ignores selected sibling sessions there (`run_package_tests.py:101–112`). It does not justify universal exclusion of every similarly named descendant.
- Output lines 28,33,37 distinguish generated-command success from individual test-body execution and source inspection from passing tests. The focused exclusion tests cited at `tests/test_run_package_tests.py:222–298` are definitions, as the output explicitly states. `requirements-package-tests.lock:35–43` supports declared dependency versions, not installation.
- The concrete local script exists and defines hook coexistence checks (`loom-code/tests/local/test-superpowers-mode-on.sh:1–43`); its exclusion follows from the runner, without executing it. No consequential omission found.

### C1-Y: acceptable

- Output lines 25–30 reach the same supported scope and exclusion conclusions against the same runner/helper source. Lines 34,38,42 explicitly withhold current/historical test success, installed versions and skip totals.
- Its defensible success wording at line 38 requires an actual unrestricted family run from the intended root and says all generated commands completed, avoiding the false every-repository-test claim. It preserves pytest skip limitations and selected-group qualification.
- Minor precision point, not material: line 25's compressed statement that discovery filters `node_modules` should be read alongside its Python eligibility explanation. The implementation filters Python *presence detection* (`:68–72`) and shell enumeration (`:88–95`); whole Python directories are handed to pytest. The report does not claim universal test-body execution, and line 42 preserves collection/configuration limits.

**Pair: tie.** Both answer the core question correctly and retain decisive exclusions and execution limits. X's additional focused-test read does not itself establish better correctness or execution coverage.

## C2 — dispatch trust

### C2-X: acceptable

- Output lines 23–25 correctly separate boolean/name/schema validation from truth assessment. `dispatch_profile.py:71–84,263–299` validates caller packets; it does not inspect task artifacts. `loom-code/references/dispatch-profile.md:22–26` assigns evidence-based classification to the station.
- The contradictory-input predictions at lines 27–33 follow directly from `dispatch_profile.py:80–84,147–160`: all three mechanical predicates return before any complex predicate, even trust-boundary/inconsistency flags. Missing/null versus empty evidence uncertainty is correctly distinguished. The documented precedence is indeed explicit (`dispatch-profile.md:139–147`), so the output appropriately avoids calling this a contract violation or demonstrated vulnerability.
- Lines 35,39–41 distinguish supplied capabilities and tested fixture assertions from actual host dispatch, real risk or semantic acceptance. The tests construct booleans (`test_dispatch_profile_resolver.py:27–45`) and assert route outputs (`:176–204`); feedback success depends on supplied booleans (`dispatch_profile.py:166–188`). No test pass is claimed.

### C2-Y: acceptable

- Output lines 23–29 correctly trace the same validation, uncertainty, precedence and route arithmetic. Its concrete standard/medium example and frontier qualification match `dispatch_profile.py:147–156`.
- Lines 33–35 add a useful precise distinction: the CLI fixture compares output with the resolver itself (`test_dispatch_profile_resolver.py:559–580`), establishing agreement for that packet rather than an independent risk oracle. Source reading is explicitly distinguished from test success and real host application.
- Lines 39,43 preserve the separate policy question and source/runtime boundary. No material omission or unsupported decision found.

**Pair: tie.** Y provides a useful CLI self-agreement caveat; both already fully retain the consequential caller-trust, contradiction and test-meaning distinctions.

## C3 — existing comparison

### C3-X: acceptable

- Output lines 23–24 correctly attribute the six-case, single ordered consumer comparison to historical records, preserve the injected crash distinction and reject token/cost/latency extrapolation. `comparison.md:7,20,28–34,170–186` and `acceptance-test-evidence.md:28–38,77,89–93` support these claims. The byte subtraction is correct: 2,681 − 2,236 = 445.
- Output lines 25–26 correctly correct the historical text-only inventory using current implementation: `loom_checker.py:576–579,607–614`, `command_handlers/intake.py:28–48,104`, `preparation_output.py:20–26`. These are static capability observations, not runtime passes.
- Lines 36–42 bound the recommendation to the original use case and explicitly avoid removing current optional JSON without assessing callers/compatibility. Historical handler/test costs are treated as sunk costs. Not reading the entire raw scoring inventory is disclosed; the directly inspected comparison and acceptance records suffice for this bounded conclusion.

### C3-Y: acceptable

- Output lines 25–29 corroborate the same historical choice and limitations, additionally checking `consumer-scoring.json` directly. Its five-versus-three completeness counts, justified unknowns and shared crash overstatement match that source's `summary` and `per_case` entries. Historical acceptance is correctly distinguished from the later informed final-guidance rerun (`acceptance-test-evidence.md:52–60,66–77,87–101`).
- Line 28 additionally identifies the current schema difference: `preparation_output.py:10–16` creates schema_version/command/status/diagnostics/notices/error/suggested_next; the historical recipe consumes state/checks_complete/failures (`comparison.md:114–124`). This usefully demonstrates why the old trial is not a direct benchmark of today's implementation.
- Lines 39–45 reject unsupported overhead savings and unassessed removal while retaining conditions for a concrete future evaluation. No material or critical issue found.

**Pair: Y.** Both are safe and sufficient. Y's direct scoring corroboration and explicit old/current schema comparison provide a modest evidence-quality advantage relevant to applicability. This is not an efficiency judgment or proof X omitted required evidence.

## What the evidence permits

These six outputs support bounded source-inspection answers and careful reuse of historical observations. They do not establish that either hidden guidance condition improves general research quality, reduces cost, or should be adopted in production. No authorization breach is visible in the inspected artifacts; self-reported trajectories cannot independently prove complete action history.
