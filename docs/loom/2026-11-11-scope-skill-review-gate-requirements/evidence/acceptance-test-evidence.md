# Scoped skill review — acceptance test evidence

Tried on 2026-11-11, in a clean copy of the project at a689bd1547306d1788888169b06f0dc429782931.

## Setup and execution boundary

- Ran `git clone --no-hardlinks --quiet /Users/kouko/GitHub/loom-plugins /private/tmp/loom-scope-acceptance-20261111-a689`, then `git checkout --detach a689bd1547306d1788888169b06f0dc429782931` in that clone.
- `git rev-parse HEAD` returned exactly the target SHA above.
- Read README's Codex installation instructions and package-test setup.
  No marketplace installation was performed: that would resolve a published
  marketplace rather than prove this detached target. Host installation and
  automatic routing are unverified, not claimed passing.
- Loaded the clone's Codex manifest, closing-review skill, and Skill lens.
  A Python path-resolution check returned `Local manifest resolves closing-review skill and lens; version=3.64.0`.
- The independent acceptance agent actually applied that lens to the target
  prose. The first output was saved in `acceptance-fresh-reader.md` before
  reading the six-case fixture; all subsequent review outputs were saved
  before reading either baseline result. This is actual fresh-reader
  execution, not a CLI/runtime benchmark or a string-test semantic claim.
- Raw inputs, target anchors, findings, and concrete fixes for all eleven
  executions are retained in `acceptance-fresh-reader.md` beside this file.

## 1. Non-governed skills do not acquire Loom registration obligations

- How I tried it: applied the Skill lens first to `unprompted-case.md`, then
  `external-clean` and `workflow-only-adoption` in `skill-lens-cases.md`.
- What came back: all three PASS, no findings, no request for a gate marker
  or registration mechanism. The target contracts settled applicability.
- Evidence: raw first-execution and six-case sections in
  `acceptance-fresh-reader.md`.
- Baseline comparison, opened afterward: `unprompted-baseline.md` had PASS
  with a nit proposing unnecessary registration. This run removed that
  recommendation; it is not a rejection-to-pass comparison.
  `explicit-context-baseline.md` already passed the two explicit controls;
  those demonstrate preservation, not newly corrected failures.

## 2. Governed missing markers and registration remain findings

- How I tried it: reviewed `governed-missing-marker`, `governed-marked`, and
  independent extension `test_release_registry_missing_reports_omission`.
- What came back: the missing marker was an important omission with an
  exact marker fix; the complete control passed; a present marker with an
  empty registry and absent checker produced a fatal omission with a
  registration/recomputation fix.
- Evidence: corresponding raw case sections in `acceptance-fresh-reader.md`.
  These cases explicitly govern an external project, so artifact location
  does not determine applicability.

## 3. Usage errors and unmet acceptance remain findings in either contract

- How I tried it: reviewed `real-command-error`, `correct-command`, and
  extensions `test_governed_command_invalid_reports_usage_error`,
  `test_external_acceptance_unmet_reports_omission`, and
  `test_governed_acceptance_unmet_reports_omission`.
- What came back: both unsupported-command cases produced fatal
  incorrect-fact findings; both omitted-capability cases produced fatal
  omission findings. The correct-command control passed.
- Evidence: corresponding raw case sections in `acceptance-fresh-reader.md`;
  each failure names its actual target instruction and a concrete fix.
- No installed Quill or external manual was consulted; the synthetic
  reference manuals are the fixtures' ground truth. No finding from a
  synthetic target is a product regression in the changed lens.

## Supporting checks and limitations

- `python3 -m pytest -q loom-code/tests/test_test_budget_text.py loom-code/tests/test_write_plan_station_text.py` initially failed because the system Python lacks pytest.
- The README's isolated uv dependency setup initially failed to create a
  lock in the default cache; a writable temporary cache was then used.
- `UV_CACHE_DIR=/private/tmp/loom-scope-acceptance-uv uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest -q loom-code/tests/test_test_budget_text.py loom-code/tests/test_write_plan_station_text.py` failed fetching `mdurl` from PyPI because DNS was unavailable. This attempt did not execute tests.
- Retried using the existing cache with authorized sandbox escalation and
  no network: `uv run --offline --isolated --with-requirements requirements-package-tests.lock python -m pytest -q loom-code/tests/test_test_budget_text.py loom-code/tests/test_write_plan_station_text.py`.
  Result: `45 passed in 0.15s`, exit 0. These are supporting existing-rule
  and station/release checks; they are not the semantic acceptance oracle.
  The automated full suite runs before acceptance is finalized and blocks
  finalization on failure; no future full-suite result is claimed here.
- The complete package suite was not run by this tester. The orchestrator
  owns it and finalization; semantic verdicts above come from executed
  reviews, not from a suite pass or text assertions.
- No spec exists; no UI flow applies. No important dismissed finding or
  user-instructed skip was supplied. Existing baseline files were preserved.
- One reader and bounded synthetic cases do not establish repeated
  reliability, universal correctness, or cross-host behavior.
