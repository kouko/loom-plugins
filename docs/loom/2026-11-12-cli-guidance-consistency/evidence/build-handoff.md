# Preparatory-command guidance — task evidence

## W1-01

Implementation commit: `0f1e142ff3901e7141ef38b87ec375794168b0dc`.
The existing public-entry tests were extended before production changes.
The RED execution reported six failures and 33 passes; failures exercised
the absent help entries and failure hints. The preserved stdout
characterization already passed. Raw output: [w1-red.txt](w1-red.txt).

The implementation only extends the existing mapping and top-level discovery
text. It introduces no callable, handler change, parser or output envelope.
Existing test cases remain; reviewer-count stderr expectations now include
the intended appended hint. A new real-handler case compares intake stdout
with its direct handler for both successful and blocked checks, retaining the
conditional advisory output. The empty-file plan case remains a limited
check success, never plan approval.

Final focused command:

```text
uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_loom_checker_cli.py loom-code/tests/test_loom_checker_modules.py -q
```

Exit 0: **44 passed in 7.18s**. Raw output: [w1-green.txt](w1-green.txt).
During the green loop, the new help vocabulary assertion first differed in
the capitalization of “Exit”; only the new expected tokens were aligned with
the displayed text. Existing case-sensitive assertions were retained. No
test was removed or skipped to obtain green.

## W2-01

The code SSOT is 3.70.0; the three derived manifests were regenerated with
`python3 scripts/sync_codex_manifests.py --all`. The `--all --check` invocation
passed. Four README version surfaces, the existing CURRENT_VERSION test pin,
and the dated CHANGELOG section agree. Root README lists the newly covered
commands and distinguishes their successful checks from completed review.

Release-focused command:

```text
uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_loom_checker_cli.py loom-code/tests/test_loom_checker_modules.py loom-code/tests/test_write_plan_station_text.py -q
```

Exit 0: **87 passed in 7.34s**. Raw output: [w2-focused.txt](w2-focused.txt).
No new prose-pin tests were introduced. Historical CHANGELOG sections retain
their original versions. `git diff --check` passed for the task edits.

## Remaining Build work

These are implementer task results, not independent acceptance or review.
The parent Build orchestrator must still sync trunk, dispatch an independent
adversary, prepare npm dependencies, run the complete package suite and every
declared adversarial program, then hand off to Closing Review. Neither task
ran the complete suite, wrote an attestation, published or changed installed
plugins. No task outside the two planned file sets was edited.
