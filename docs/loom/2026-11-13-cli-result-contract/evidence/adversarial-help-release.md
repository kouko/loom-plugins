# Help and release adversarial exercise

Attack points tried: 8. Successful attacks: 0. New programs committed: 0.
One existing repository program is reused with an additional concern header.

Target: `9cedb9f9917640917d1b39d75ce384de59a0b63e` against
`fbdc29af358413bc9d55b599231b2a6cbcb4524d`.
The attacker read the adversary contract, common protocol, code/spec recipes,
current intent/spec/plan, artifact charter, dispatcher diff and related tests.
No declared mutation/fuzz runner was found in repository configuration files.
Docs, intent, plan and evidence have no specialized recipe; code and spec do.

## Attempts and observed outcomes

1. **REQ-1, inventory omission:** existing discovery tests enumerate all sixteen
   commands and require both exact spellings, discoverability and appropriate
   command-specific details outside a repository. Held.
2. **REQ-2, success mistaken for completion:** existing outcome/authority tests
   exercise help pages for publication, delivery, hooks, merge, advisory rules,
   standing policy and contract compatibility. They require the partial-effect,
   advisory-exit, missing-check and authorization caveats. Held. This is a
   bounded operational-caveat attack, not a replacement for source conformance
   review of every sentence.
3. **REQ-3, nonexact/hostile help bypass:** a temporary trial replaces every
   handler with a recording sentinel returning 7. For all sixteen commands,
   it tries ten single-token and one hundred two-token forms: `--help`, `-h`,
   `--HELP`, `--help=1`, Unicode em-dash `—help`, embedded NUL, empty token,
   `--`, `extra`, and newline-suffixed help. All 1,760 invocations preserve
   dispatch and exact arguments except the intended two exact forms. Held.
4. **REQ-3, existing consumer corruption:** CLI tests exercise preparation JSON,
   delivery JSON, malformed selectors, hook boundaries, usage errors and legacy
   diagnostics. Existing published shapes and result streams held.
5. **REQ-4, help executing work:** existing tests replace handlers, stdin,
   subprocess, socket and Path read/write/open operations with exceptions.
   All 32 exact command/help pairs return 0, text and empty stderr, outside
   a repository; the extra-argument form reaches the tripwire. Held.
6. **REQ-4, forgotten state/repeated calls:** after the 1,760 hostile trial
   invocations, all sixteen exact help pages still return 0 and clean stderr.
   No persistent dispatcher state was introduced. Held.
7. **REQ-4, interrupted/missing runtime:** launcher tests provision only through
   fake uv, then call all 32 ready-runtime help forms without another repair.
   Removing the isolated runtime cache yields exit 86 and does not recreate it.
   Held. No live provisioning, publication, install or cleanup was performed.
8. **Release drift:** release/station tests recompute the four manifest/package
   versions, changelog, root README locations and three language README versions.
   All agree with 3.73.0. Held. This attacks the release boundary rather than
   claiming installed-host or marketplace validation.

## Commands and results

Run from the repository root:

```sh
uv run --offline --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_loom_checker_cli.py loom-code/tests/test_loom_python_runtime.py
# 49 passed in 18.84s
uv run --offline --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_write_plan_station_text.py
# 43 passed in 0.18s
uv run --offline --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_loom_checker_cli.py
# 39 passed in 9.37s after adding the reused program's concern header
```

The first attempted uv invocation could not create a cache lock under the
sandbox. The identical offline command succeeded with approved access to the
existing cache; dependency versions remained pinned by the requirements lock.

The uncommitted trial was executed as:

```sh
uv run --offline --isolated --with-requirements requirements-package-tests.lock python /private/tmp/loom-help-adversarial-trial.py /private/tmp/loom-cli-result-contract
# hostile/nonexact/repeated dispatcher calls held: 1760
# post-hostile help recovery held: 16
```

The temporary trial is preserved at that path and can run against a clean
checkout by replacing its repository argument. Its green code is not copied
into the repository. The clean-tree, committed adversarial declaration below
uses the existing test artifact instead; it requires no temporary trial file.

## Recorded adversarial program

```yaml
attack_points: {found: 8, earned_a_program: 0, committed: 0}
adversarial:
  - command: uv run --offline --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_loom_checker_cli.py
    artifact: loom-code/tests/test_loom_checker_cli.py
probes:
  - artifact: loom-code/tests/test_loom_checker_cli.py
    status: reused
    reason: Existing public-entry tests cover safe exact help, ordinary rejection, result streams and authority caveats; only a concern comment was added.
findings: []
```

No new green probe was retained. No full package suite, live network writer,
paid CLI, host installation, branch cleanup or worktree deletion was executed.
The temporary trial remains outside the repository. These attempts do not
produce a review verdict or independent acceptance report.
