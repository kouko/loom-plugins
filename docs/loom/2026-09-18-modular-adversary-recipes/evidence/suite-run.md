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

## Documents under check

Each recipe and the shared protocol are read by their own test module, and the
checks that recompute the four module criteria are named in
`loom-code/scripts/test_module_criteria_text.py`. The ten modules that read
these documents run 260 passed, 1 skipped.
