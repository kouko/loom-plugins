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
