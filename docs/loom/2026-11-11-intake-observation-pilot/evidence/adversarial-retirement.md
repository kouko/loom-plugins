# Candidate probe retirement

The initial adversarial run at `4c362237` exposed a repeated-JSON-option
invocation bug: `intake write-plan --json --json` returned a rule blocker
instead of an invocation error. Commit `fd65d1f1` retained the failing program
at `docs/loom/2026-11-11-intake-observation-pilot/evidence/probes/test_intake_repeated_json.py`.
It subsequently graduated unchanged to `loom-code/tests/test_intake_repeated_json.py`.
The candidate repair and successful historical acceptance remain recorded in
`acceptance-test-evidence.md` at candidate `7da5d59`.

The adoption decision withdrew the JSON interface, returning the checker to
its pre-pilot implementation at final-scope commit `113491d5`. The unchanged
probe then failed while decoding empty stdout as JSON (`JSONDecodeError`),
before reaching its assertions. It requires an interface the final spec no
longer provides. Its deletion retires that candidate-specific contract; no
assertion about retained text behavior is weakened, skipped or xfailed.
The historical probe remains retrievable from Git at `fd65d1f1` and `7da5d59`.

The adversary reuses `loom-code/tests/test_loom_checker_intake.py` for the
retained interface, adding only a concern comment. All existing test logic
remains unchanged. The rerunnable final adversarial command is:

```sh
uv run --offline --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_loom_checker_intake.py
```

Temporary final-scope abuse trials exercise malformed identifiers, absent,
empty and unreadable intents, repeated read-only observations and a missing
required spec. They remain uncommitted because none earned a new RED program.
This is a scope-change re-evaluation, not a retry of a failing product repair.
