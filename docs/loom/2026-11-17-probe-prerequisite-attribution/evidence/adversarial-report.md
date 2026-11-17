# Adversarial report

Attack points tried: 17. Attacks that succeeded: 0. New programs committed: 0.
One existing repository program reused with its concern marker added.

Target: `2f122b3bcb3fa43e117eccb7f66a53238334eb25`, against
`d3faa624d436f22aaa083b8f2b163bb924c2e7ba`.
Dispatch profile: resolver inherited; overrides null. Fresh-context attacker;
no implementation changes, old finance execution, installed-cache changes,
remote operations, full package run or finalization.

## Attacks and observed outcomes

1. Valid five-prerequisite evidence plus one current program: automatic
   discovery excludes the five, while explicit reuse still spends the cap.
2. Invalid historical digest: prerequisite remains counted.
3. Malformed historical JSON: prerequisite remains counted.
4. Evidence introduced after intent: prerequisite remains counted.
5. Changed prerequisite bytes: prerequisite remains counted.
6. Copied prerequisite bytes at a new path: copy remains counted.
7. Changed then restored bytes: prerequisite remains counted.
8. Side-branch change and restoration merged back: prerequisite remains counted.
9. Executable mode changed: prerequisite remains counted.
10. Missing canonical historical evidence: no exclusion.
11. A no-program execution mixed into historical evidence: no exclusion.
12. An object in place of the execution list: no exclusion.
13. One-character result change from `pass` to `pasS`: no exclusion.
14. Delete then restore the exact prerequisite bytes: no exclusion.
15. Delete and reintroduce the current intent: ambiguous introduction grants
    no exclusion.
16. Six real current programs, hidden-store paths, ordinary tests and rename
    boundaries: exercised existing cap attack coverage; no bypass.
17. Malformed and mixed no-program declarations, filtered execution and explicit
    prerequisite union: exercised existing finalizer coverage; no bypass.

Points 1–9 execute in `loom-code/tests/test_probe_attribution.py`; points
16–17 execute in `test_adversarial_probe_cap_coverage.py` and
`test_selection_finalize.py`. Points 10–15 were additional disposable trials
using `prerequisite_repo`, `commit_all`, `git` and the public
`prerequisite_probe_programs` function. The trial parameter values were
`missing`, `no-program`, `object`, `false-pass`, `delete-restore` and
`intent-reintroduced`. Each asserts the first prerequisite is absent from
the returned exclusion set. For evidence corruption trials, checkout the
fixture's pre-intent `HEAD~2`, corrupt its evidence, create an orphan snapshot
with that tree, commit, then introduce the current intent. For identity trials,
commit each deletion/restoration separately. This keeps the trial isolated
from earlier valid evidence while reusing the repository fixtures.

## Executions

Disposable trial command:

```sh
PYTHONPATH=loom-code/scripts:loom-code/tests uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest /tmp/test_prerequisite_attacks.py -q
```

Observed: `6 passed in 7.37s`. The first trial execution yielded `4 failed,
2 passed in 6.71s`: four fixture setup failures were `FileNotFoundError`
while creating the current intent's missing parent directory in the orphan
snapshot. Adding `intent.parent.mkdir(parents=True, exist_ok=True)` repaired
the trial; these were not product REDs and earned no committed program.
The disposable GREEN trial is intentionally not committed.

Initial sandbox invocation could not acquire `/Users/kouko/.cache/uv` lock;
a temporary-cache retry could not resolve PyPI. Authorized local elevated
execution then used the existing dependency environment successfully.

Re-runnable existing coverage command:

```sh
uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_probe_attribution.py loom-code/tests/test_adversarial_probe_cap_coverage.py loom-code/tests/test_selection_finalize.py -q
```

Observed: `84 passed in 93.79s (0:01:33)`.

Reused program declaration (single artifact):

```sh
uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_probe_attribution.py -q
```

Observed: `9 passed in 27.53s`.

## Skill and gate temptations

Read under the literal temptation, "the diff is one line, proceed?" The
changed protocol grants no shortcut: historical validation, pre-intent timing,
uninterrupted path/blob/mode identity and explicit-union counting still apply.
The executable attacks above test these refusal boundaries, including the
one-character result mutation. Release/docs artifacts have no dedicated
adversarial recipe; no separate runtime behavior was invented for metadata.
No declared mutation/fuzz runner was found in the inspected package manifests.

## Handoff

Findings: none. No product defect earned a new probe. Reused program:
`loom-code/tests/test_probe_attribution.py`; status `reused`; reason:
its historical fixture attacks already cover identity, timing, explicit reuse
and preserved review/evidence scope. Only its line-start concern marker was
added; assertions and implementation remain unchanged.

Git-memory classification: routine evidence capture, no new decision,
learning or gotcha requiring trailers. Local commit authorization inherited
from the orchestrator. Exact commit text receives the deterministic privacy
scan; no ambiguous private-party identity appears, so no semantic judge is
required.
