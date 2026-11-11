# Hook reproduction — 2026-11-11

Observed on `origin/main` at `31b98646` (loom-code 3.65.0), macOS, with a
temporary pytest probe that was deleted after the run.

## Setup

The `delivery` fixture repository (`loom-code/tests/test_delivery.py`) plus:

- `src.py`, `docs/loom/KICKOFF-DEFAULTS.md` (`package-tests: python3 -m pytest -q`)
  and `tests/test_added.py` (an ordinary test, no `concern:` line) committed;
- a content-valid attestation whose only adversarial execution is
  `{"kind": "adversarial", "no_program": "nothing earned a program"}`;
- local HEAD absent from the remote.

`subprocess.run` and `tempfile.TemporaryDirectory` were wrapped to record
every call and then delegate to the real implementation.

## Result

| Call | Non-git subprocesses | Temporary directories | Outcome |
|---|---|---|---|
| `publish.verification_status(repo, "change")` | 3 × `python3 -m pytest -q --collect-only -p _loom_pytest_collection`, each exit 0 | 3 × `loom-pytest-collect-` | `valid` |
| `publish.cmd_delivery(["--hook", "--host", "claude"])` | the same 3 commands, each exit 1 | 3 × `loom-pytest-collect-` | exit 0, the `unpublished` reminder, 1.96 s |

Three is the number of program-suffix paths the branch added (`delta.py`,
`src.py`, `tests/test_added.py`). Inside the hook `PATH` was `/usr/bin:/bin`.

## Not measured

- Why the collection exits 1 inside the hook (the restricted `PATH` is the
  suspected cause).
- A repository that carries `scripts/run_package_tests.py`, where collection
  first launches the runner inventory through `uv`.
- A branch adding enough program files to approach the 20-second deadline.
