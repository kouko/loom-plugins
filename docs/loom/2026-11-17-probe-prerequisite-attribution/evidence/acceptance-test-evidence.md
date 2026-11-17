# Prerequisite probe attribution — acceptance test evidence

Tried on 2026-11-17, in a clean copy of the project at 8d3fa86fab76013f23da5572102a8beec108318f.

## Setup and scope

Independent witness; no implementation work. Fresh clone command:
`git clone --no-hardlinks . /private/tmp/loom-acceptance-probe-attribution`.
In that clone, `git rev-parse HEAD` returned the exact target above, and
`git status --porcelain` returned no output before and after acceptance.
No dependencies were installed into conda base. README lines 332–337 prescribe
the isolated locked requirements environment; used that environment with focused
tests rather than the full suite, as required by the acceptance-tester role.

Executed from the clean clone:
```sh
uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_probe_attribution.py loom-code/tests/test_adversarial_probe_cap_coverage.py loom-code/tests/test_selection_finalize.py -q
```
Actual result: exit 0; `84 passed in 92.09s (0:01:32)`.
Native escalation was used to access the existing uv dependency cache.

Full suite command (NOT run by this witness):
`uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`.
The orchestrator states package-tests is not skipped and finalize-review will run.
The report cites that mandatory blocking check without claiming a future result.
No UI flows exist in this engineering spec.

## 1. Proven unchanged prerequisites

Executed `test_inherited_five_are_excluded_without_changing_scope_or_evidence`.
Observed assertions: five prior paths excluded; automatic count contains only
the new current path; cap check returns no errors. Fixture uses real Git commits,
historical attestation validation and current finalization.

Also invoked the historical helper and graduated discovery against the pinned original finance Git tree; the two calls have different runtime boundaries:
```python
from pathlib import Path
from loom_checker.probes import graduated_probe_programs
from loom_checker.probe_attribution import prerequisite_probe_programs
from loom_checker.helpers import git_maybe
r = Path("/private/tmp/finance-research-continuation")
h = "9de82a7ec22ee0eff69787f26c1f0c72bd7ab3f7"
c = "2026-11-16-finance-research-continuation"
paths = set((git_maybe(r, "ls-tree", "-r", "--name-only", h, "--",
                      "obsidian-finance/tests") or "").splitlines())
print(sorted(prerequisite_probe_programs(r, h, c, paths)))
print(graduated_probe_programs(r, h, c))
```
Executed using `PYTHONPATH=loom-code/scripts uv run --isolated --with-requirements requirements-package-tests.lock python -c '<code above>'`.
Actual exit 0, proven paths:
- obsidian-finance/tests/test_fiscal_provenance.py
- obsidian-finance/tests/test_projection_type.py
- obsidian-finance/tests/test_quarter_publication.py
- obsidian-finance/tests/test_sec_filing_identifier.py
- obsidian-finance/tests/test_sec_source_identity.py

Actual graduated-discovery output: only `obsidian-finance/tests/test_research_continuation.py`. This is NOT an exact historical full-counter result: although its Git revision argument is pinned, graduated discovery calls suite collection against the current working tree. Only the helper's five proven paths above establish purely pinned historical provenance. The clean committed fixture independently establishes the five-prior/one-current full-counter behavior.

Initial standalone system-python helper attempt failed before accessing the source
with `ModuleNotFoundError: No module named 'yaml'`; reran using the documented
isolated environment and succeeded. This is an environment mismatch, not a product
pass or product failure.

Limitation: the finance checkout's current HEAD was observed as
`9c9ff1622088045b8ab70f0053655c5130c35913`, different from the handoff pin.
Every call explicitly used the historical full SHA argument above, but that pins Git reads only. `prerequisite_probe_programs` performs Git/JSON provenance reads; `graduated_probe_programs` can invoke `suite_collection` / `_pytest_collects`, whose subprocess uses `--collect-only` against the moving working tree. Collection may load finance code and use temporary cache. No finance test CASE execution, finalizer, reset, checkout, evidence write, installation or installed-cache update was performed. The full-counter query therefore crossed the intended pure-history boundary and is not offered as historical full-counter proof. It was not repeated. A subsequent `git status --porcelain` in finance exited 0 with no output, matching the initially clean status; no cleanup or reversal was performed. This verifies tracked/untracked worktree status, not absence of temporary-cache effects. None of this proves live finance delivery.

## 2. Explicit reuse and deduplication

Executed the same inherited-five test. Its duplicate supplied current path check
returns no error. Explicitly supplying all five prior paths plus the current path
returns a cap error. Finalizing a supplied prior path plus current path exits 0,
and the new attestation records exactly those two adversarial artifact paths.
Relevant additional passing tests: `test_a_graduated_program_spends_against_the_cap`,
`test_an_executed_artifact_outside_the_store_spends_against_the_cap`.
No old execution was substituted for the current supplied execution.

## 3. Fail-closed evidence and identity

Executed all eight parameterizations of
`test_unproven_or_changed_prerequisites_stay_counted`:
invalid digest, malformed JSON, evidence later than intent, changed bytes,
copy to a new path, changed-then-restored bytes, side-branch restoration merged
back, executable mode change. All passed; the current program remains counted
and the original prerequisite remains counted for every identity/evidence
corruption case other than the copy case, which specifically asserts the new copy.
New current programs are also asserted in every parameterization.
The original fixture's unchanged case is independently exercised in row 1.

## 4. Ceiling and ordinary-test boundary

Executed `test_cap_probe_programs_pass_and_one_more_is_refused`,
`test_an_ordinary_new_test_does_not_spend_against_the_cap`,
`test_a_shell_probe_program_counts_against_the_cap`, and all existing
`test_adversarial_probe_cap_coverage.py` tests.
Observed successful assertions: cap-sized input accepted, cap+1 rejected;
ordinary tests do not spend against the cap; hidden paths, shell programs,
extensionless programs, copied/rewritten and graduated explicit programs cannot
bypass counting. Aggregate actual result is the 84 passing tests above.

## 5. Preserve scope, reviewer floor, skips and collection

The inherited-five test asserts every prior path remains in
`committed_branch_delta`, reviewer count remains 2, and auto-skipped steps
remain empty. It also executes current finalization with a prior and current path.
Executed existing collection cases including
`test_finalize_accepts_a_graduated_program_the_suite_already_runs`,
`test_runner_honors_configured_pytest_file_names_and_ignores`,
`test_runner_collection_uses_declared_package_environment`,
and `test_a_file_the_suite_never_collects_is_still_refused`; all passed.
These exercise collection independently of cap exclusion.

Executed:
`git diff --exit-code d3faa624d436f22aaa083b8f2b163bb924c2e7ba 8d3fa86fab76013f23da5572102a8beec108318f -- scripts/run_package_tests.py loom-code/scripts/loom_checker/reviewers.py loom-code/scripts/loom_checker/helpers.py loom-code/scripts/loom_checker/command_handlers/finalize.py`.
Actual exit 0, no output: these shared policies and inventory runner are unchanged.
The full suite will run through the mandatory blocking finalize-review check;
this witness does not claim a completed full-suite result.

## 6. Preserve historical evidence and fresh acceptance

The inherited-five test snapshots the prior evidence bytes, performs new current
finalization, then asserts identical prior bytes and the current change id on the
new attestation. This passed, including older valid evidence revisions followed
by later malformed metadata. The late-evidence parameterization also passed,
rejecting a manufactured later prerequisite boundary.
The finance helper performed pinned Git/JSON reads, while the accompanying graduated query could collect current-tree tests as disclosed in row 1; no test CASE execution or finalization occurred. Main repo changes by this witness are only
this evidence document and its acceptance report. No installed cache was touched.

## Findings

None. All six criteria have executed focused evidence. Historical finance
attribution is pinned, with moving-HEAD and installation limits disclosed.

## Re-run on 2026-11-17, at 5fd9870b7d6f6dd17c9924cbd01bcd757ada93e9

Scope: publication-metadata correction only. No product test or finance collection was repeated. The original 84 passing focused tests remain the executed behavioral evidence; the following checks independently justify carrying their results forward.

Clean setup: `git clone --no-hardlinks . /private/tmp/loom-acceptance-probe-attribution-refresh` succeeded. In that fresh clone, the documented isolated locked-requirements environment successfully imported `loom_checker.digest`, `loom_checker.probe_attribution`, `loom_checker.probes` and `loom_checker.helpers`, and loaded the contract manifest. `git status --porcelain` returned no output afterward.

Executed via `PYTHONPATH=loom-code/scripts uv run --isolated --with-requirements requirements-package-tests.lock python -c '<imports and comparison>'`, with this comparison body:

```python
r = Path.cwd()
c = "2026-11-17-probe-prerequisite-attribution"
revisions = ["8d3fa86fab76013f23da5572102a8beec108318f",
             "5fd9870b7d6f6dd17c9924cbd01bcd757ada93e9"]
values = [functional_content_digest(r, h, c) for h in revisions]
assert values[0] is not None and values[0] == values[1]
```

Actual output: `imports loaded; manifest loaded: True`; both revisions returned `25ba9a1f76c5bde8c8df4efe926cff70c909ff6d`; `functional identity equal`; exit 0. Only the contract's declared publication-only metadata was excluded by the existing digest function, with no ad hoc exclusions. Production code, permanent tests and retained spec/plan therefore have identical functional content. The current clean-load commit is the report's canonical Tried-on revision; original behavioral results remain explicitly attributed to the earlier revision.

- 1: carried over — identical functional digest preserves the tested inherited-five/current-one fixture and pinned historical-helper result; extra live collection is not historical full-counter proof.
- 2: carried over — identical functional digest preserves explicit reuse, current execution and set-union assertions.
- 3: carried over — identical functional digest preserves all eight evidence/identity refusal parameterizations.
- 4: carried over — identical functional digest preserves five/six ceiling and ordinary-test assertions.
- 5: carried over — identical functional digest preserves scope, reviewer, skip and collection behavior; required full suite remains for finalize-review and is not claimed complete here.
- 6: carried over — identical functional digest preserves evidence immutability and fresh-attestation assertions; historical finance was not queried again.

## Dismissed severe findings and retained review episode

Read `evidence/review-rebuttal.md` and `evidence/w3-01-tests.md`. These document the same original code reviewer `/root/closing_code`, same Round 1, original review target `6ec90d1c8678ca4d2551372a52118114e3748ecb`, returning PASS after complete counterevidence. The witness did not rerun those investigator experiments or treat them as its own test execution.

1. Fatal correctness finding: Git path patterns could conceal modification/restoration of a prerequisite. Dismissed by the original reviewer after the real validator rejected the bracket-name fixture before attribution, and a valid backslash-name fixture passed real historical validation, excluded unchanged content and retained changed-then-restored content. Direct Git history returned both alteration commits. An unmatched hypothetical literal path did not prove omission of an existing file's history. No product fix resulted.
2. Fatal external-surface-grounding finding: insufficient support for Git command semantics. Dismissed by the original reviewer after the complete fixture and official Git global-options/history-traversal documentation were examined. The review criterion did not require source links adjacent to code; missing adjacent links alone did not establish the claimed fatal defect. Primary references are recorded in `review-rebuttal.md`: https://git-scm.com/docs/git and https://git-scm.com/docs/git-log .

The provisional design/plan repair was withdrawn after the hypothesis was disproven. No review episode was reset. Outstanding findings: none. The docs review's nonblocking isolation-wording nit is corrected in the report by separating pinned helper provenance from the extra live-working-tree collection query. Package-tests is not skipped; finalize-review will run its mandatory checks.

