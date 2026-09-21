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

The ten modules that read the protocol, the recipes and the conventions are the
ones this invocation names, and it is what their count is recomputed from:

```
python3 -m pytest -q \
  loom-code/scripts/test_adversary_layout.py \
  loom-code/scripts/test_adversary_protocol.py \
  loom-code/scripts/test_adversary_recipe_code.py \
  loom-code/scripts/test_adversary_recipe_shape.py \
  loom-code/scripts/test_adversary_recipe_skill_gate.py \
  loom-code/scripts/test_adversary_recipe_spec.py \
  loom-code/scripts/test_adversary_routing.py \
  loom-code/scripts/test_module_criteria_text.py \
  loom-code/scripts/test_build_mechanical_checks.py \
  loom-code/scripts/test_prose_pin_rule_text.py
```

It runs `292 passed`, where the second run recorded `260 passed, 1 skipped`.
The skip is gone: it belonged to a parametrized case over an empty debt list,
and the list and the case were deleted in this round. The `317 passed` this
paragraph carried before named no module and no command; the figure above
replaces it because this command is the one that produces it.

## Fourth run, after the pre-merge trunk sync

`land` refused the pull request as `BEHIND`: the trunk had gained
`a1891ed1` (loom-code 3.7.1 to 3.7.2) after the attestation was generated, and
this repository requires a branch to be current before it merges. `sync-trunk`
merged that commit at `1499dea6`, which changes the functional-content digest,
because the digest covers the whole tree rather than this change's own paths.

kouko chose, on 2026-09-19, to regenerate the attestation for the merged
content while carrying the two reviewer verdicts forward, rather than open a
fourth review round over content the reviewers had not read. The reasoning,
recorded here because a decision that lives only in a conversation is not
evidence: the verdicts judge this change's own delta, and the trunk commit
arrived through the same stations with its own attestation at
`docs/loom/2026-09-19-bump-loom-code-3-7-2/attestation.json`. The cost is that
this attestation's digest names content one commit newer than the tree the
reviewers read, and that difference is exactly `a1891ed1`.

Build's mechanical checks were repeated on the merged tree before the
attestation was regenerated:

| Check | Result |
|---|---|
| Complete package suite, the `package-tests:` command above | exit 0 |
| Both adversarial programs, one invocation | 44 passed in 982 s |

## Documents under check

Each recipe and the shared protocol are read by their own test module, and the
checks that recompute the four module criteria are named in
`loom-code/scripts/test_module_criteria_text.py`. The ten modules that read
these documents are the ones the invocation above names; they ran 260 passed,
1 skipped at the second run above, and 292 passed at the third.
