# Implementation and live execution evidence

## W1-01 initial RED/GREEN

The implementer added the smallest cross-surface continuation regression before changing skill prose.

- RED: `python3 -m pytest -q loom-workflow/tests/independent-advisor/test_independent_advisor_readmes.py -k named_review_continues` — 1 failed, advisor lacked explicit same-turn continuation.
- GREEN: `python3 -m pytest -q loom-workflow/tests/independent-advisor/test_independent_advisor_readmes.py loom-code/tests/test_external_review.py` — 148 passed (33.42s final initial run).
- JSON prompt corpus parsing and `git diff --check` passed.
- These assertions verify the text contract and existing runner; they are not behavioral or platform acceptance evidence.

## W2-01 live outside execution

Ran installed external_review.py through its installed loom-python launcher in Codex, with narrowly scoped host escalation, accepted-selection authorization, the isolated eight-file packet, Sonnet/medium, 45-second probe and 600-second review limits. No user answer was requested after the already-confirmed intent. No retry or provider substitution occurred.

Observed progress: probe exited 0 after 2 seconds; review exited 0 after 28 seconds. The JSON execution result reported completed, observed Claude model claude-sonnet-5-5, accepted-explicit-settings; effective effort was not independently observable. Claude returned actual YAML review text, PASS_WITH_NOTES, with a substantive concern about distinguishing consent from host execution approval. The implementation is being clarified in response; that review is not a final-tree closing-review verdict.

The raw result is retained locally outside publication; live-execution.json records the bounded execution fields and review-text hash. The packet manifest lists the exact copied paths; no histories, credentials or unrelated documents were included. Startup/cache access outside the copied root remains possible.

This execution used explicit acceptance of the precise live-test scope and destination, so it cannot alone establish the original goal for future terse review requests. A successful subprocess or internal approved record does not establish a host-wide authorization policy change.

## W1-01 host-approval clarification

The live reviewer identified conflation between consent and host execution approval. The implementer searched all four caller surfaces and related README/prompt tests, added a RED-first boundary assertion, then clarified that consent does not grant host approval and a required second user answer fails uninterrupted acceptance. Focused suite: 148 passed in 33.78s. Existing retry authorization remains unchanged.

## Behavioral continuation gap

A fresh caller actor with a readable single-file target and a natural named review request stopped on unavailable rejected-options history before calling the controlled simulator. This revealed a separate instance of the interruption class: generic consultation packet prerequisites applied to explicit unowned artifact reviews. The implementation repair preserves the report shape and consultation completeness while allowing a factual unavailable-history marker for this artifact-only context. Cancellation control dispatched nothing. No second real vendor execution was attempted.

## First complete package-suite attempt

Command: `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`.

The first code group returned 1 failed, 2836 passed, 2 skipped in 115.95s. Failure: `test_review_convergence_contract.py::test_earlier_verdicts_not_reused` treated the affirmative reuse of existing request authorization as prohibited reuse of an earlier review verdict. The runner stopped before subsequent groups. This failure is retained; it is not a completed package pass. The repair must preserve whole-document detection of affirmative verdict reuse while excluding authorization reuse.

## Build integration after guard correction

The verdict-reuse guard was repaired with affirmative active/passive verdict self-tests and an authorization-reuse negative control. Focused convergence plus advisor checks: 30 passed. No runtime authorization semantics were relaxed.

The second complete locked package-suite invocation exited 0: 15 pytest groups summed to 4,265 passed and 11 skipped, plus the runner's shell checks. The first failed log remains separate. The reused adversarial artifact was then re-executed: 13 passed in 0.17s. Trunk sync reported up to date with origin/main fbdc29af3 at tested HEAD 862088abd.

Commands:
- `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`
- `python3 -m pytest loom-workflow/tests/independent-advisor/test_independent_advisor_readmes.py -q`

Full second-run log: /private/tmp/loom-uninterrupted-package-tests-r2.log. This integration result is not itself semantic acceptance of the user's uninterrupted-review goal.
