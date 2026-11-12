# Integration repair — blocked-input regression

## Observed RED and bounded diagnosis

The first finalization package run failed the unchanged
`loom-code/tests/test_external_review_adversarial.py::test_unreadPromptOverPipeBuffer_timesOutAtLimit`:
expected `execution-timeout: 6s`, observed `execution-timeout: 5s`, with
`probe timed out after 5s`. The retained local log is
`/private/tmp/design-research-finalize.log`; its package summary is
1 failed, 2832 passed, 2 skipped in 214.14s. The orchestrator also observed
an earlier complete-suite pass and a standalone pass of the original test.
This is an intermittent wrong-phase timeout, not a deterministic old-test
failure or proof of a particular CPU scheduling mechanism. The original
stub's own comment documented cold Python startup as a timing dependency.

Defect class: a short-deadline fake CLI can spend its deadline starting
Python before reaching the blocked-input review branch. The orchestrator's
whole-content search covered every changed file plus the failing test and
found one applicable stub. Unrelated changelog references to cold installs
were excluded. This repair inspected the full failing test file, the actual
production preflight prompt, and the runner's pipe/deadline/cleanup code.

## Test-only repair

The fake CLI now uses POSIX shell and reads one bounded prefix with
`dd bs=4096 count=1`. It recognizes the actual preflight prompt and returns
the same model-usage JSON. The review branch records its PID and replaces
itself with `sleep 60` without consuming the remaining prompt. The public
`external_review.main` entry, real subprocesses and pipes, 1 MiB input,
distinct 5/6-second deadlines, start marker, process cleanup assertion and
15-second elapsed bound are retained unchanged. Production code and all
other pre-existing tests are untouched. No code-plugin release bump applies
to this test-only repair; the design release remains 2.25.0.

## Observed GREEN and limits

- `python3 -m pytest loom-code/tests/test_external_review_adversarial.py -q`:
  9 passed in 8.75s.
- Three concurrent executions of
  `python3 -m pytest loom-code/tests/test_external_review_adversarial.py::test_unreadPromptOverPipeBuffer_timesOutAtLimit -q`:
  each passed, in 8.10s, 7.00s and 7.53s. These provide bounded concurrent
  repetition, not proof against every possible suite load.
- The isolated locked-environment command could not start because the
  sandbox denied creating a temporary lock file under the default uv cache.
  The focused results above use the existing local Python environment;
  complete locked-suite verification remains with the orchestrator.
- No mutation experiment was run. The unchanged production runner and the
  existing test's unchanged assertions bound this evidence; no claim is made
  that an old implementation mutant was killed by these runs.

Existing design-research behavioral cases and retained trials remain
applicable: this repair changes only their integration test environment,
not design guidance or runtime external-review behavior. The orchestrator
will run complete-suite verification and renew the checkpoint using the same
reviewer identities in the existing bounded review episode.

## Additional orchestrator mutation checks

After the implementer's checks above, the orchestrator copied the script tree
and the committed target test at `3bf869d1` into two temporary trees under
`/private/tmp/design-repair-mutations-v2`. The test bytes were compared with
`git show 3bf869d1:loom-code/tests/test_external_review_adversarial.py` and were
identical in both copies. Only the copied production runner was mutated;
the actual repository's production runner and test were left untouched.

Each copy executed this unchanged committed test through pytest:

```
python3 -m pytest loom-code/tests/test_external_review_adversarial.py::test_unreadPromptOverPipeBuffer_timesOutAtLimit -q --basetemp <copy>/pytest-tmp
```

- `synchronous-input`: replaced exactly one `writer.start()` with `write_in()`
  in the copied launcher, restoring synchronous large-input writing outside
  the deadline. The review-start PID marker proved the blocked-input branch
  was reached. The test did not return within the external 25-second guard;
  the guard terminated it (return code -9) and explicitly reaped the marked
  CLI process group. This is bounded nontermination evidence, not a normal
  pytest assertion result. Output was empty before the guard.
- `generic-probe-word`: changed exactly one occurrence of the real probe's
  `single word ok` to `single word okay` in the copied runner. The exact shell
  selector did not accept the near miss; pytest returned 1 with
  `expected execution-timeout: 6s`, `observed execution-timeout: 5s`, and
  `1 failed in 5.10s`. The target test and its assertions were unchanged.

Both marked child PIDs were checked absent afterward. The initial copy-setup
attempt failed before tests because it assumed a nonexistent pytest.ini;
the corrected copies required no project config. No production mutation was
applied to the source worktree, no new executable harness was committed, and
these two checks do not establish sensitivity to every possible mutant.
Local result receipts and output are retained under the temporary directory
above. They supplement, rather than change, the implementer's reported scope.
