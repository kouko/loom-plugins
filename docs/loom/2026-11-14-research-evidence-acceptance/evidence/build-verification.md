# Build verification

- Branch base: `3bf50711f983e12ac25b219c6340f5b164f5201c`.
- Tested functional HEAD: `f3e9de10d4663a6235f9d62109627cd3aeec62fe`.
- Trunk sync before final Build checks: up to date; no commit added.
- Focused package invariants: 5 passed. Release-pin test file: 43 passed.
- Existing misplaced-program regression: initial full-suite RED; after the
  byte-preserving archive relocation, 1 passed on committed HEAD.
- Complete suite: `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`.
  Exit 0; [actual output](build-suite-passed.txt). Its first failed attempt is
  retained in [the original failure output](build-suite-initial-failure.txt).
- Adversarial program: `loom-code/tests/engineering-research/test_package.py`.
  Command: `uv run --offline --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/engineering-research/test_package.py`.
  Exit 0, 5 passed; [actual output](build-adversarial-passed.txt).
- Both commands inherited `UV_CACHE_DIR=/private/tmp/loom-uv-research`.
- No adversary redispatch, new adversarial program or unresolved adversarial
  finding. The unchanged existing program still passes after relocation.
- Independent behavioral assessments and actual trajectories are linked from
  [the archive pointer](behavioral-evidence.md); they establish bounded local
  observations, not general efficacy or automatic activation.

Closing Review's first sync attempt refused newly captured, uncommitted output
files. They are retained in this commit before the deliberate sync retry; no
trunk content or requirements changed.

## Integration verification after merge acceptance

The authorized merge first refused GitHub's DIRTY state. Main had advanced to
`cb737ec3ee13b7670857b65a7c874774a4d3340a`; the sole conflict was adjacent
release-version rows in README. Merge commit
`36622c801faed3d6ae2f7c5ba2cb17b2b629ff73` retains code 3.80.0 and workflow
5.24.0, with all eight engineering-research files byte-identical to the
previously published tree. Requirements and the accepted partial validation
limit are unchanged. This is the same bounded review episode's second digest.

- Sync: up to date with the fetched main; no further commit added.
- Focused release checks: code metadata 6 passed, workflow metadata 14 passed;
  generated-manifest check passed.
- Same complete suite command above: exit 0;
  [actual integration output](build-suite-r2-passed.txt).
- Same unchanged adversarial program and command above: exit 0, 5 passed;
  [actual output](build-adversarial-r2-passed.txt).
- No adversary redispatch: its existing program is unchanged and passes.
- No efficacy trials were repeated or new coverage inferred from this merge.
