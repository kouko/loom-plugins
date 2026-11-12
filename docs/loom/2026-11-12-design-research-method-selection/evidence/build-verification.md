# End-of-Build verification

Tested commit: `029cce3a6328e86e8d66b1c6b23b2db0947f7cbb`.
Branch base: `391fd01723efedfada3447673b1b99c3894af859`.

## Integration

The installed checker's `sync-trunk` reported up to date against `origin/main`
at the branch base; no sync commit was added. A second observation before
independent acceptance returned the same result. The computed reviewer floor
is two. No workflow step is skipped by instruction.

Command:

```
uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q
```

Observed exit code: 0. The fifteen pytest invocations reported an aggregate
4,259 passed and 11 skipped. All seventeen shell-test summary groups reported
zero failures. The final npm deprecation notice did not fail the command.
This is the complete declared inventory, not a bare root pytest invocation.
Full terminal output is retained locally at
`/private/tmp/design-research-build-suite.log`; its relevant pytest summaries:

```
2833 passed, 2 skipped in 217.74s (0:03:37)
211 passed, 1 skipped in 11.52s
53 passed in 2.35s
264 passed in 7.36s
64 passed in 14.08s
22 passed in 0.06s
13 passed in 0.03s
12 passed in 0.02s
58 passed in 3.02s
125 passed, 3 skipped in 2.57s
248 passed, 5 skipped in 1.54s
12 passed in 0.02s
19 passed in 0.04s
163 passed in 1.73s
162 passed in 1.43s
```

## Adversarial handoff

Independent attacker: native agent `method_adversary`, inherited profile,
not an implementation author. Seven attack points, no earned new program,
no product changes and no unresolved findings. Two executable attempts:
relocated archive packaging (2 passed), release-pin consistency (1 passed).
Five additional prose temptation inspections were not model executions and
do not establish behavioral resistance.

Reused concern-tagged program:

```
python3 -m pytest loom-design/tests/test_design_research_package.py
loom-design/tests/test_design_research_package.py ..                     [100%]
============================== 2 passed in 0.03s ===============================
```

The orchestrator reran this exact command after the complete suite; exit 0.
This program establishes packaging invariants, not method-selection behavior.
Actual baseline/candidate trials and their limits belong to independent
acceptance evidence. Finalization must execute the full suite and this program
again on the committed reviewed content.

## Earlier independent checks and outside-review limitation

Native `method_spec_review` returned PASS on the spec at `3404c009` with base
`bd14580d`; native `method_plan_review` returned PASS and no simpler shape.
Neither edited the target. These checks do not validate runtime behavior.

The explicitly requested Claude Code proposal review produced no usable review:
the Opus/high preflight exited 1 with an unknown error. Its result had no
observed model or effort, evidence level `none`, and no review output. Local
doctor reported inaccessible credentials/keychain in that execution context;
that does not establish the exact preflight cause. No retry or outside-vendor
closing-review verdict is claimed.

## Integration repair and repeated Build verification

The first `finalize-review` attempt stopped before generating an attestation:
the package suite failed an existing blocked-input regression during the
five-second preflight instead of reaching its six-second review deadline.
See [integration-repair.md](integration-repair.md) for the actual failure,
bounded diagnosis, test-only repair and additional mutation checks.
The research requirements and twelve retained design-trial executions did not
change. This remains the same bounded review episode, with the original two
closing reviewers; it is not a new episode or a retry-budget reset.

Repeated Build target: `3bf869d138a8a743b20b01ddab0dbe95e7fbbd20`.
`sync-trunk` again reported up to date against `391fd017`. The exact locked
package command above exited 0; fifteen pytest invocations totaled 4,264 passed
and 6 skipped, and all seventeen shell summary groups had zero failures.
Both inventories total 4,270 pytest cases; five previously skipped cases ran
in this later invocation. These are observed run counts, not five new tests
attributed to the repair. Detailed local output:
`/private/tmp/design-research-build-suite-r2.log`.

After that complete suite, the same committed adversarial program was rerun:

```
python3 -m pytest loom-design/tests/test_design_research_package.py
loom-design/tests/test_design_research_package.py ..                     [100%]
============================== 2 passed in 0.03s ===============================
```

No adversary was redispatched: the existing program remains applicable and
passes. The test-only repair has not changed its covered packaging invariant.
Renewed acceptance setup and same-reviewer fix verification precede the next
finalization. No formal outside-review verdict or skipped step is added.
