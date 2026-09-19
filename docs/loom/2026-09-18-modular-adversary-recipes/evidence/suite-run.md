# Suite and adversarial run — 2026-09-19

Commit under test: `0b1ada15`, branch `worktree-modular-adversary-check`, after
`sync-trunk` merged `origin/main` (`fc5b1a02`) at `96203311`.

## Complete package suite

Command, the `package-tests:` value in `docs/loom/KICKOFF-DEFAULTS.md`:

```
uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q
```

Result: exit 0. The runner is the single inventory for every Loom pytest and
shell-test surface; the isolated invocation keeps each directory's own pytest
configuration and avoids host-Python drift, and the hash-verified lock pins what
it installs.

## Adversarial programs

| Command | Artifact | Result |
|---|---|---|
| `python3 -m pytest -q docs/loom/2026-09-18-modular-adversary-recipes/evidence/probes/test_modular_recipes_abuse.py` | `docs/loom/2026-09-18-modular-adversary-recipes/evidence/probes/test_modular_recipes_abuse.py` | 6 passed |
| `python3 -m pytest -q docs/loom/2026-09-15-adversary-probe-maintenance/evidence/probes/test_probe_maintenance_abuse.py` | `docs/loom/2026-09-15-adversary-probe-maintenance/evidence/probes/test_probe_maintenance_abuse.py` | 24 passed |

The second program is an earlier change's, updated by this change's adversary
because its hand-written copy list could not see the recipe files this change
adds. It stood at 7 of 22 cases failing at the branch base, 18 of 22 after the
split, and 24 of 24 passing here — the update also added two cases the list had
never covered.

## Second run, after the closing-review trunk sync

`sync-trunk` at the start of closing review merged `origin/main` (`5a309716`)
at `44ee3284`, bringing in ship-station content, and reported `content
changed`. Under the station's own rule that dispatches no reviewer until
Build's checks are repeated on the merged tree, both were re-run there:

| Check | Result |
|---|---|
| The same complete package suite command | exit 0 |
| Both adversarial programs in one invocation | 30 passed |

## Third run, at the content the closing-review fix round delivers

The two runs above were made at `0b1ada15` and at the post-sync `44ee3284`.
Ten commits later the content has moved: the recipes and the protocol gained
pins on every rule sentence, and this commit repoints the module criteria
map, adds a clause to the protocol's removal sentence and to the `remove`
criterion, and deletes two debt lists. Both checks were therefore run on the
working tree carrying every edit of the fix-round commit. That tree stood on
`28514022` when the runs were made; the commit lands on `a2ff04c7`, which the
blind runner added in parallel and which touches only
`docs/loom/2026-09-18-modular-adversary-recipes/blind-run-report.md`, so no
file either check reads moved between them.

| Check | Command | Result |
|---|---|---|
| Complete package suite | the `package-tests:` value above | exit 0 |
| Both adversarial programs, one invocation | `python3 -m pytest -q docs/loom/2026-09-18-modular-adversary-recipes/evidence/probes/test_modular_recipes_abuse.py docs/loom/2026-09-15-adversary-probe-maintenance/evidence/probes/test_probe_maintenance_abuse.py` | exit 0, 44 passed in 815s |

The 44 supersede the 30 of the second run: the second program grew cases after
that run, and the first was rewritten to attack the claim without deselecting
a case or picking an easy kind.

The ten modules that read the protocol, the recipes and the conventions ran
`317 passed` in one invocation, where the second run recorded
`260 passed, 1 skipped`. The skip is gone: it belonged to a parametrized case
over an empty debt list, and the list and the case were deleted in this round.

## Documents under check

Each recipe and the shared protocol are read by their own test module, and the
checks that recompute the four module criteria are named in
`loom-code/scripts/test_module_criteria_text.py`. The ten modules that read
these documents ran 260 passed, 1 skipped at the second run above, and
317 passed at the third.
