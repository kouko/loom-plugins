# CI environment extension — implementation evidence

## Scope and evidence continuity

Confirmation `ecddb23b175a133fc0d904aa8b557c844ba36d0a` adds AC5/6 to the
previously completed historical-test maintenance. Earlier acceptance and review
results prove their recorded AC1–4 revisions, not this new CI environment.
This work adds setup/readiness and setup-failure obligations rather than
retrying an earlier failed task. Independent integration and closing review
remain pending after the focused implementation observations below.

## Implementation observations

- Code, design and workflow Python jobs install the committed hash-verified
  requirements lock. Both events watch requirements source and lock changes.
- Code setup installs zsh and uv 0.13.1 and verifies the existing setup-python
  Python 3.11. [PyPI's publisher metadata](https://pypi.org/pypi/uv/0.13.1/json),
  read 2026-11-13, declares version 0.13.1 and Python 3.11 support; the local
  reference `uv --version` also reports 0.13.1. No conda environment is modified.
- The official agy artifact and SHA512 are retained in the installation
  research. The actual official installer extracts the member `antigravity`
  and copies it to `agy`; CI follows that layout, verifies the expected
  version and runs each plugin validator without opening a model session.
- Workflow Python setup installs Node 22 and its own Mermaid dependencies
  before its suites. The existing Mermaid validation job retains its runner
  installation and parser tests. Installation never relies on another job's
  filesystem. All three pytest selectors request `-rs` diagnostics.

## Focused execution

Commands use `uv run --isolated --with-requirements
requirements-package-tests.lock python -m pytest <paths> -q -rs` from this
worktree; each plugin configuration runs separately.

| Observation | Result | Raw output |
| --- | --- | --- |
| New environment regression module before workflow changes | 5 failed | `/private/tmp/loom-ci-environment-red.txt` |
| Environment module, unified design CI guard and manifest sync/real local agy validators after changes | 45 passed, 0 skipped | `/private/tmp/loom-ci-environment-green-root.txt` |
| Code dependency-source and replay modules | 16 passed, 0 skipped | `/private/tmp/loom-ci-environment-green-code.txt` |
| Design CI workflow module | 2 passed, 0 skipped | `/private/tmp/loom-ci-environment-green-design.txt` |

Two interim corrupt-download runs failed before exercising checksum rejection:
macOS's sha512sum rejected the GNU long option and then required an explicit
stdin operand. The shared `sha512sum -c -` invocation then exercised actual
checksum failure and passed the regression case. These were portability
corrections in the setup command, not skipped or successful checksum tests.

## Build integration observed at daf2adf33

The configured complete command `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q` exited zero: 4,273 pytest cases passed across 15 sessions, zero skipped; all shell and Mermaid commands passed. Raw output: `/private/tmp/loom-ci-environment-package-tests.txt`.

The retained adversarial declaration `uv run --with-requirements requirements-package-tests.lock python -m pytest loom-workflow/tests/loom-memory/test_migrate_legacy_store.py` exited zero with 17 passed. Raw output: `/private/tmp/loom-ci-environment-adversarial-rerun.txt`. New CI failure injections are recorded separately in `ci-adversarial-report.md`; they earned no new program because none exposed a defect.

Both Build and pre-acceptance `sync-trunk` observations reported up to date against origin/main fbdc29af358413bc9d55b599231b2a6cbcb4524d. These local executions do not establish Linux runtime readiness.

## Remaining remote boundary

No Linux container or VM was started. Local tests establish parsed preparation
order and failure propagation inside the actual installation shell; they do not
establish GitHub runner installation, Linux binary execution, or credential-free
Linux plugin validation. Actual GitHub execution, skip counts, complete package
execution and independent verification belong to the subsequent Build/Ship
observations. The macOS `/var` alias and case-insensitive-filesystem checks can
remain platform skips on Ubuntu; they must be reported separately from passes.

## Round 2 correction — propagate pytest skip diagnostics

This is a Round 2 repair in the same CI-extension review episode, under the
existing W3 AC6 obligation. It changes neither confirmed scope nor the episode
or same-task retry budget; no new confirmation or review episode is claimed.

The first remote run at `e98b17f0aea026899e7980a9cfbbae58665cd3ed` supersedes the preceding pending-Linux
boundary for that revision: all CI checks succeeded. Code run `43444813208`
reported 2,842 passed and zero skipped; design run `43444813139` reported 211
passed and zero skipped; workflow run `43444812907` reported 1,218 passed and
two skipped across its sessions. Combined pytest results were 4,271 passed and
two skipped. The real Linux setup printed agy 1.5.8 and successfully validated
all three plugins (8, 7 and 14 skills). Raw logs are
`/private/tmp/loom-ci-code-remote.txt`, `/private/tmp/loom-ci-design-remote.txt`
and `/private/tmp/loom-ci-workflow-remote.txt`. This confirms real installation
and local validation without model credentials at that revision. It does not
prove this diagnostic fix or establish printed skip reasons; that fix requires
a new remote observation.

Remote provenance: [code run](https://github.com/kouko/loom-plugins/actions/runs/43444813208),
[design run](https://github.com/kouko/loom-plugins/actions/runs/43444813139),
and [workflow run](https://github.com/kouko/loom-plugins/actions/runs/43444812907),
all at the first published revision identified above.

The first published CI execution exposed a diagnostic propagation defect.
Although the three workflow runner commands included `-rs`, the runner's
`--loom-family` path forwards only its supported verbosity selection, not
arbitrary pytest arguments. The earlier statement that the selectors requested
diagnostics described their command text; it did not establish that pytest
received the option. Existing passing environment checks asserted that same
text and therefore missed this defect. Preserve those observations as historical
results, not proof of skip-reason output.

Defect class: pytest diagnostic options not propagated. The search covered
all cumulative changed paths plus AC6 diagnostic surfaces. The actual instances
were the three Python suite commands in the code, design and workflow workflows,
the command-text assertion in the environment regression test, and this
evidence's diagnostics claim. Other recorded `-rs` commands invoke pytest
directly and remain valid. The disposition and release prose describe the
intended diagnostic outcome and are clarified with the actual environment path.

The three suite steps now set `PYTEST_ADDOPTS: '-rs'`, which pytest reads from
its inherited environment, and omit the ignored runner argument. The existing
parameterized environment case checks the actual step environment and executes
a tiny real pytest test using that environment, verifying the printed skip
reason. No runner API or inventory changes are made.

The strengthened regression was run before changing the workflows: 3 failed
and 2 passed because each suite environment lacked the option. Raw output:
`/private/tmp/loom-ci-diagnostics-red.txt`. The corrected environment and
unified-design focused run reported 10 passed, zero skipped, retained at
`/private/tmp/loom-ci-diagnostics-green.txt`; later integration and remote
observations must establish the cumulative result.
