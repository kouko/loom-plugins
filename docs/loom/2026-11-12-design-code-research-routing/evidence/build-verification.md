# Build integration verification

## Initial complete-inventory attempt

At `03e0bee9`, ran the declared command:

```sh
uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q
```

The runner stopped at its first failed pytest group: 10 failed, 2789 passed,
2 skipped, 1 warning in 214.89 seconds. Later groups were not reached.
Raw local output: `/private/tmp/loom-research-build-suite.log`.

Eight failures exposed two integration defect classes:

- Incomplete new-skill admission: install inventory (two failures), frozen-leaf
  and rendered-description accounting (three), and README navigation (two).
  Preserve the historical baseline/hash and 60% unchanged-catalog limit while
  explicitly admitting the new leaf and its 222-character description. The
  design router's own description was shortened by six characters instead of
  adding another exception. Add the required skill usage page and navigation.
- Review wording collision (one): the existing no-old-verdict-reuse guard
  matched the new paragraph's reuse-of-evidence sentence. Restate adequate
  evidence handling without changing the existing verdict protection or test.

The whole-content sweep covered every path changed from `70a05fd7...HEAD` and
the affected installation, description and navigation tests. It found 52 reuse
and 30 design-research matches; the review paragraph was the sole new collision,
and the pre-existing verdict prohibition remains intact. Root tests were added
to W1's explicit Files scope. Requirements and task identity did not change.

The implementer reproduced seven admission/navigation failures and the review
guard failure before fixing them. After the fixes, focused install/catalog/
navigation/design-package checks passed 49 tests; review convergence checks
passed 16. Existing tests supplied RED; no duplicate regression harness was added.

## Unchanged timeout tests and local execution conditions

The other two failures were in existing external-review fake-CLI tests:
`test_agy_discovery_times_out_when_descendant_holds_stdout` (pid absent before
the one-second kill) and `test_review_stage_times_out_when_descendant_holds_stdout`
(one-second probe timeout rather than the expected two-second review timeout).
Both source and tests are unchanged from `70a05fd7`. Running those exact two
tests alone with the same isolated locked environment passed: 2 passed in 3.90s.

An existing separately confirmed change in the original worktree already records
the fake-CLI interpreter-startup race under load. That record supports treating
load as a plausible cause, not proof of every failure's internal timing. This
change does not modify those tests, their timeouts, assertions or production code.

Inspected the installed locked xdist 3.8.0 implementation of
`pytest_xdist_auto_num_workers`: `PYTEST_XDIST_AUTO_NUM_WORKERS` is an explicitly
supported override for auto worker count. Subsequent complete runs use value 4
to bound local contention while retaining the declared command's `-n auto`,
all discovered groups, every test and every assertion. This is a temporary local
execution setting, not a repository-default change or a skip. Results do not
establish load-insensitivity on other machines.

## Second attempt and design-group completion

At `76d65d24`, the same complete-inventory command with the supported four-worker
setting passed the entire root/code group: 2799 passed, 2 skipped in 256.05s.
The runner then reached design and stopped: 3 failed, 208 passed, 1 skipped.
Raw local output: `/private/tmp/loom-research-build-suite-fixed.log`.

The design failures exposed two further integration surfaces. Capture-intent's
new paragraph made its body 3542 words against the unchanged 3500-word cap;
the baseline was already 3498 words. The handoff is now one sentence and the
adjacent orientation paragraph is equivalently compressed, preserving required
fields, sufficient-evidence drafting, no question quota, outcome-first capture
and unchanged decision points. The body is now 3499 words; the cap was not raised.

Design's current-release assertion and root marketplace description were also
stale. The whole changed-content and design release-surface search located the
pin in one test; historical changelog entries remain unchanged. The release
implementer reproduced the failing version test, then updated only the current
pins and marketplace entry. The complete design group subsequently passed:
211 passed, 1 skipped. Manifest synchronization and diff checks passed.

These fixes retain the same six Acceptance obligations and task identities.
Final Build and finalization results are recorded by their actual commands and
generated attestation; this record does not claim a future run passed.

## Further timeout diagnosis and supporting repair

The next four-worker run failed five unchanged timeout cases (2794 passed,
2 skipped); one-worker execution reproduced those five (1010.76s). All five
also failed on untouched base `70a05fd7`, and no-worker execution did not solve
them. Minimal fresh CLI launches measured approximately 2.8s in both installed
interpreters. Thus the earlier worker-count hypothesis was insufficient.

The [bounded research record](../research/001-timeout-fixture-startup.md)
retains conditions and limitations. W3 repairs only fake-CLI test preconditions;
[fixture evidence](timeout-fixture-evidence.md) records 144 focused passes and
three descendant-check failures under a parent-only-kill mutation. The production
external-review script/defaults remain unchanged. Complete verification is still
reported separately; these focused results do not substitute for it.
