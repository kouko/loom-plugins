# Build verification

## W1 core behavior

Commit: b642d749257a94b49aaa031a98bb0c695e1e69c8.

The focused command was `uv run --offline --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_delivery_stop.py loom-code/tests/test_delivery.py loom-code/tests/test_hooks_json.py loom-code/tests/test_hook_recovery_literal_path.py -q`.

- RED: 15 failed and 79 passed before implementation.
- GREEN: 94 passed after implementation.
- Restoring the old Claude block response made the response assertion fail; restoring the fix passed. This checks the actual response rather than host argument parsing alone.
- Existing explicit delivery and literal-dollar-path recovery tests passed. Both packaged hook recovery tests execute the recovered command after removing the hook-only host argument.
- Tests grew by 50 net lines across existing modules; no new test file or production abstraction was introduced.

Agent-decided metadata validation: each entry in a nonempty Claude background array must be an object with a nonempty string ID after trimming. No status or natural-language inference is performed. Codex does not use those arrays for pause decisions.

Native host evidence remains separate in `host-framing.md`: these tests validate source behavior, not an installed repair or interactive host UI. No installed configuration or persisted hook trust was modified.

## W2 release and revised design evidence

Release commit: 74c797435. Existing release pin RED: expected 3.65.0, observed 3.64.0, one failed test. After source version, CHANGELOG, README and derived manifest synchronization, the entire station-text module passed (43 tests). Manifest synchronization check and diff whitespace check passed. No new tests; net test lines zero.

Prose-only correction 5d47d2a6f removed temporary account quota/native-probe history from reusable Ship instructions; host-framing evidence retains the actual limitations.

Before W3, `uv run --offline --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_verification_status.py loom-code/tests/test_delivery_stop.py -q` passed 39 tests in 42.95 seconds. This validates the existing classifier and W1 behavior; it does not establish the not-yet-implemented W3 boundary. The revised spec independently passed at f295840f; the revised plan independently passed at 80f30cd8. Both reviewers inspected the skip/publication distinction and human-wait uncertainty.

## Build and closing verification

- Branch base: a8ec84e02740b58820055249e40e186d63233fbd. Build and Closing Review sync-trunk both reported up to date, with no new commit or warning.
- W3 final focused result: 205 passed; earlier failed and corrected cases are retained in w3-verification.md.
- Full package command: `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`. Build exit 0: 4,197 pytest passes, 11 skips, and successful shell suites. Log: /private/tmp/stop-build-suite.log.
- Reused adversarial command: `uv run --offline --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_delivery_stop.py`. Build exit 0: 32 passed in 74.40 seconds. No adversarial finding remained open, and no adversary redispatch occurred.
- Independent acceptance tested 0c65e553637bf7924cb16b24a28017ab85a14a67 in a clean clone. Native repaired-host validation remains incomplete; this is not dismissed or converted to a pass.
- Closing Review Round 1 target: a4ef9e3d06a1dc7d93d2882f0d50d90dc03ceba1. Two fresh reviewers returned PASS_WITH_NOTES, independently executing 142 and 144 tests, no skips. One important native-host validation gap remains explicitly open in the verdict and acceptance report; no finding was dismissed.
- finalize-review reran the entire package suite and reused adversarial program successfully, generating content digest 5814df535b87d02d8e708078c183d0bd1941589b. Acceptance statuses remain partly, works, partly. No human acceptance, merge or installed-host update occurred.
