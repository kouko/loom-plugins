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

## Final Build result

At committed `c7fd9d5f606aa20cdf87d87587d0b4c23c537c65`, ran the original declared
complete command with the default interpreter and auto worker selection: no
worker override, interpreter override, deselection or skip was added.

```sh
uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q
```

Exit 0. The 15 pytest summaries total **4225 passed, 11 skipped**; all remaining
shell/check surfaces also completed successfully. The original root/code group
reported 2799 passed, 2 skipped in 200.05s. Raw local output:
`/private/tmp/loom-research-build-suite-verified.log`. Counts were recomputed
from actual pytest summary lines, not inferred from a zero exit alone.

The retained adversarial program was rerun after all fixes:

```sh
uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-design/tests/test_design_research_package.py
```

Result: 2 passed in 0.03s. No adversary re-dispatch was needed because the
retained program remained applicable and passing; its recorded initial attack
scope remains explicit. The timeout mutation evidence supplements
the repaired test behavior without claiming to be research acceptance evidence.

`sync-trunk` reported up to date at `c7fd9d5f`, containing origin/main `70a05fd7`.
The computed reviewer floor is 2. Build's required mechanical checks are complete;
independent research-behavior acceptance and closing review remain separate.


## Round 2 fix verification

At committed `1adb52d239d0a05677b05150e45e9eceff41d065`, the original declared
complete command passed again, with default interpreter and auto worker selection.
No worker override, interpreter override, deselection or skip was added.
The 15 actual pytest summaries total **4225 passed, 11 skipped**; every remaining
shell/check surface completed successfully, exit 0. Root/code reported 2799 passed,
2 skipped in 205.26s. Raw local output: `/private/tmp/loom-research-build-round2.log`.

The retained adversarial program was rerun with the same declared command:
`uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-design/tests/test_design_research_package.py`.
Result: 2 passed in 0.03s. An initial sandbox attempt could not acquire the existing
uv cache lock; the host-approved invocation executed successfully. No assertion
or program changed. `sync-trunk` reported up to date at `1adb52d2`, containing
origin/main `70a05fd7`, with no commit added.

The fixes disclose decision-critical unverified context before recommending in
both research skills and exercise the two edited budget boundaries through the
actual CLI entry. Independent behavioral acceptance and the same reviewers'
Round 2 fix verification remain separate from these mechanical results.


## Upstream integration / terminal-round Build result

Upstream `ab40f0e634db492c9b250da8e95b53579aeb23c2` independently published code
3.67.0 after Round 2. Initial sync reported README/changelog conflicts and did
not mutate the branch. W5 names the new integration obligation without resetting
requirements, retries or the Review episode. The [compatibility assessment](../research/002-upstream-design-compatibility.md)
records the actual source inspection. Integration preserves upstream progress,
collection filtering and our research handoffs; this code release becomes 3.68.0,
while design stays 2.24.0.

At `cdc5da8a193d7c1862e97af01e9ec6a97472dfdc`, the original declared complete
command passed with default auto workers and interpreter, without deselection or
additional skips. The 15 actual pytest summaries total **4251 passed, 11 skipped**;
all remaining shell/check surfaces passed, exit 0. Root/code reported 2825 passed,
2 skipped in 203.20s. Raw local output: `/private/tmp/loom-research-build-round3.log`.

The retained adversarial command passed: 2 passed in 0.02s. The upstream ordering
change did not make the program inapplicable or unable to run, so no adversary
re-dispatch or program rewrite was needed. Sync-trunk before the independent
acceptance re-dispatch reported up to date at `cdc5da8a`, containing `ab40f0e6`.
The previous attestation does not establish readiness for this new content;
affected acceptance and original-reviewer terminal verification remain required.
