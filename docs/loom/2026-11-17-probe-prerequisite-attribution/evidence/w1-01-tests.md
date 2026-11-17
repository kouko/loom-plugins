# W1-01 test evidence

## Command

```sh
uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_probe_attribution.py loom-code/tests/test_selection_finalize.py loom-code/tests/test_adversarial_probe_cap_coverage.py -q
```

## RED

The inherited-five assertion ran before the production change and failed:

```text
FAILED test_probe_attribution.py::test_inherited_five_are_excluded_without_changing_scope_or_evidence
assert graduated_probe_programs(repo, head, CHANGE) == [current]
AssertionError: Left contains 5 more items, first extra item: 'loom-code/tests/test_prior_0.py'
1 failed, 82 passed in 110.56s
```

The historical seven-key v2 fixture independently passed the existing
`validate_attestation` at its committed historical tree. RED was a behavior
failure, not a missing import or invalid fixture. The full RED command
continued running existing regression cases while implementation began.

## Intermediate verification

- Attribution and unchanged-identity cases: 5 passed in 10.38s.
- Invalid digest, malformed JSON, late evidence, change, copy, revert and mode
  boundaries: 8 passed in 15.79s.
- First complete focused GREEN: 83 passed in 79.41s.
- The added real finalization integration initially refused bare Python
  execution of pytest functions. The fixture now supplies `python3 -m pytest`
  for both historical and current execution records, preserving that guard.

## Coverage and boundaries

The positive case excludes five proven unchanged prerequisites, retains the
current program, deduplicates explicit inputs, and refuses explicit reuse of
all six paths. It resolves an earlier valid canonical revision despite later
malformed metadata. Real finalization explicitly reuses one prerequisite,
records it as a current execution, and writes a distinct current attestation.
Historical evidence bytes remain unchanged.

The same case verifies that all five prerequisite paths remain in the shared
branch delta, two reviewers remain required, and no automatic step is skipped.
Existing focused regression cases retain the ordinary-test distinction,
six-current-program refusal, package collection, and move/copy behavior.
No finance test, finance finalizer, historical attestation rewrite, remote
operation, or installed-cache change was performed.

## Final GREEN

```text
........................................................................ [ 86%]
...........                                                              [100%]
83 passed in 79.85s (0:01:19)
```

The final command includes the real finalization integration and all changed
historical fixture cases. `git diff --check` also passed.
