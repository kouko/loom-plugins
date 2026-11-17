# W3-01 reproduction investigation

No production correction or task commit has been made. The proposed
regression did not establish a product failure, so RED/GREEN is incomplete.

## Actual validation boundary

Command:

```text
uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_selection_finalize.py -k prerequisite_glob -q
```

A temporary regression reused `test_probe_attribution.prerequisite_repo`
and replaced its first graduated filename with `test_[x].py` in memory.
The unmodified historical validator rejected the fixture before attribution:

```text
command = 'python3 -m pytest loom-code/tests/test_[x].py'
ValueError: it contains shell metacharacters; declare a plain argv command
(a program and its arguments) instead
1 failed, 62 deselected
```

This is a fixture-precondition failure, not the required behavioral RED.
`probes.py::argv_for` rejects brackets before splitting argv, including
quoted brackets. Its pattern also rejects `*`, `?`, and parentheses.

## Additional isolated observation

An exploratory version bypassed historical validation in memory solely to
inspect the suggested history failure. That temporary test first asserted
the unchanged bracket path was excluded, then modified and restored that
file and asserted it was retained. On the original production helper it
passed: `1 passed, 62 deselected`. This mock-based observation is not a
product acceptance result or valid RED.

The fixture's direct Git query also returned both alteration commits:

```text
git log --full-history --ancestry-path --format=%H 94aa9a8..HEAD -- loom-code/tests/test_[x].py
04916230886fbcf3376b1406a68dd0d95f7c10c2
220d7c7f9ddc4f3d5ec0cddaa964190c14eb1fa1
```

The temporary regression was removed. Existing tests and production code
were restored unchanged. A valid, reachable failing case is still needed.

## Defect-class inspection

Read the complete `probe_attribution.py`, its immediate graduated-discovery
caller, `git_exec.py::run_git`, historical attestation validation, and command
artifact parsing. Searched the helper and `probes.py` for `git_maybe`, `log`,
`ls-tree`, `full-history`, `ancestry-path`, and prerequisite calls.

The helper has three exact-name history queries: current intent introduction,
canonical attestation revisions, and artifact alterations. Canonical-record
enumeration deliberately uses `docs/loom/*/attestation.json`. No source
change was made to any query. No evidence from this investigation establishes
that a validated reachable artifact bypasses uninterrupted identity checks.

## Backslash follow-up with real validation

The reviewer replaced the bracket example with the Python string
`r"loom-code/tests/test_\x.py"`. A second temporary test used the existing
`make_repo`, `graduate`, `PASSING`, `commit_all`, and `git` helpers. Its local
attestation record followed the existing prerequisite fixture's schema and
used `shlex.quote(artifact)` to construct the adversarial command, with its
real SHA-256 command digest and functional content digest. No validator or
production function was mocked.

Command:

```text
uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_selection_finalize.py -k prerequisite_backslash -q
```

First run on the unchanged production helper: **1 passed, 62 deselected**.
The assertions established all of the following:

- The historical record passed the real `validate_attestation` with `[]`.
- The unchanged artifact was returned as a proven prerequisite.
- After modifying and restoring that same literal artifact, it was not
  returned as a proven prerequisite.

Direct Git history confirmed that both alterations were found:

```text
git log --full-history --ancestry-path --format=%H 6236ddf..HEAD -- 'loom-code/tests/test_\x.py'
cf1b4408cd3ec239437f7c39605f52985bce20df
92cd6b9107f54d1763b2101feb46770887964a9c
```

The fixture's ordinary `git diff --name-status main HEAD` printed the added
artifact as `"loom-code/tests/test_\\x.py"`, a quoted path. That observation
does not establish that the automatic graduated-discovery caller reaches
the attribution helper with this filename; it is a separate existing path
parsing boundary. The direct helper test above passed the actual literal
candidate, so the original helper itself did not falsely exclude it.

The temporary test was removed because it did not reproduce a new defect.
No production correction was made, and a valid behavioral RED remains
unestablished. A full focused suite was not run for a source correction
because no source or permanent test correction exists.
