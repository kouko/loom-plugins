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

## Pending boundaries

No Linux container or VM was started. Local tests establish parsed preparation
order and failure propagation inside the actual installation shell; they do not
establish GitHub runner installation, Linux binary execution, or credential-free
Linux plugin validation. Actual GitHub execution, skip counts, complete package
execution and independent verification belong to the subsequent Build/Ship
observations. The macOS `/var` alias and case-insensitive-filesystem checks can
remain platform skips on Ubuntu; they must be reported separately from passes.
