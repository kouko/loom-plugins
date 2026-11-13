# CI environment adversarial report

Attack points tried: **5**. Attacks that succeeded: **0**. Programs committed: **0**.

## Scope

Independently attacked the AC5/6 extension at
`d2ad25c4b3a3f8a43f4048dba46c202e3805e37b`, relative to
`fbdc29af358413bc9d55b599231b2a6cbcb4524d`. Read the cumulative diff,
intent, plan, preparation regression tests and prior CI implementation evidence.
The code artifact recipe applies; release documentation and evidence have no
separate adversarial recipe. No production files were modified. Existing AC1–4
migration adversarial evidence and its executable declaration remain unchanged.

## Executed attacks

Executed the exact committed `Install Antigravity CLI` shell body using
`bash --noprofile --norc -eo pipefail -c <body>`. Each run used a separate
temporary directory, a temporary `PATH` prefix containing controlled `curl`,
`sha512sum` and `tar` executables, and isolated `RUNNER_TEMP` and `GITHUB_PATH`.
The wrappers logged their invocation order. Later stages returned success until
the selected failing boundary; extraction supplied a minimal executable only
for the version and validator boundary attacks. These fixtures do not claim
that the official Linux executable ran.

| Attack | Observed execution | Result |
| --- | --- | --- |
| Download command exits 22 | `curl`; shell exits 22 | Extraction and PATH publication never run. |
| Checksum command exits 1 | `curl`, checksum; shell exits 1 | Extraction and PATH publication never run. |
| Extraction command exits 2 | `curl`, checksum, extraction; shell exits 2 | PATH publication never runs. |
| Extracted executable reports 9.9.9 | `curl`, checksum, extraction; shell exits 1 | No plugin validation or PATH publication runs. |
| First plugin validator exits 7 | `curl`, checksum, extraction, one validation; shell exits 7 | Subsequent validations and PATH publication never run. |

Every trial asserted a nonzero shell status and absence of `GITHUB_PATH`.
The first two additionally asserted no extraction; the wrong-version trial
asserted no validation; the failed-validator trial asserted exactly one
validation. All assertions passed. The disposable trial command was
`python3 /private/tmp/ci-adversary-trial.py`; it is an exploratory harness,
not a committed clean-tree program or finalization declaration.

## Findings and program disposition

No fatal, important or nit finding was demonstrated by these attacks.
No new CI program: all five dependency-failure attacks were stopped by the
committed setup script, so no defect earned a new adversarial program.
`probes: []` for this extension. Keep the existing migration program as the
cumulative change's declaration; do not combine a `no_program` declaration
with that existing executable declaration.

The existing `tests/test_ci_environment_preparation.py` provides the permanent
corrupt-download regression and parsed per-job setup checks; this dispatch did
not modify that implementation-owned test or name it as a new adversarial
program.

## Limits and execution interruptions

This tests shell failure propagation in the real committed setup body using
controlled dependencies, not the Actions scheduler, downloads, Linux binary
compatibility, actual validator behavior, or successful dependency installation.
It opens no model/account session and makes no network request. Full-suite and
actual GitHub-runner results belong to independent integration and acceptance.

An initial attempt to use `uv run --isolated --with-requirements
requirements-package-tests.lock` stopped at an unwritable external cache before
running the trial. System Python lacked PyYAML. The trial then used Python's
standard library to extract the committed indented shell body and executed all
five cases successfully; no dependency installation or guard retry was needed.

Git-memory classification: routine evidence commit; no new durable decision,
surprising product constraint, or reusable gotcha was demonstrated. No memory
trailer is warranted. The carrier contains no private-party identifiers.
