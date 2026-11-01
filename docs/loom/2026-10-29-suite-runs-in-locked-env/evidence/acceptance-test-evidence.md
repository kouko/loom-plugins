# The detected package suite runs in a uv project's locked environment — acceptance test evidence

Tried on 2026-10-29, in a clean copy of the project at edc30a0b (`git worktree add --detach <scratch>/at1/loom-clean edc30a0b`).
Re-run on 2026-10-29 after fix c5038e3a..0ffd76e6, in a new clean worktree at 0ffd76e6 (`<scratch>/at2/loom-clean`), row 1 only (see "Re-run" under row 1).
For before/after comparison a second clean worktree was added at the base 3555782c (`<scratch>/at1/loom-base`).
`<scratch>` = `/private/tmp/claude-501/-Users-kouko--herdr-worktrees-loom-plugins-consistence-review-2/5b11059c-24eb-4eec-9170-a767ecffcf0e/scratchpad`.

Setup
- Sample uv project: `git clone /Users/kouko/GitHub/loom-dogfood-sandbox <scratch>/at1/sandbox` (the original checkout was never modified); work on a local branch from `origin/main` (66d763b), which commits `pyproject.toml` + `uv.lock`, dev group `pytest>=8`, src layout, `testpaths = ["tests"]`, and declares no `package-tests:` in KICKOFF-DEFAULTS.
- Interpreter on PATH for every run: `command -v python3` → `/Users/kouko/.conda/envs/dbt-redshift/bin/python3` (conda env without `tasknote`). PATH was never changed.
- Checker: `<scratch>/at1/loom-clean/loom-code/scripts/loom-python --repair ...`, run from inside the clone. Setup check: `loom-python --repair --list-rules` exit 0.
- The checker has no CLI that prints the detected suite command, so a small driver `<scratch>/at1/tools/detect.py` imports `loom_checker.probes` from a given checker tree and prints `declared_test_command(repo)`, `declared_test_command(repo, HEAD)` and optionally `suite_collection(repo, artifact)`; run as `loom-python --repair --script <scratch>/at1/tools/detect.py <checker-scripts-dir> HEAD [--collect <artifact>]`.
- All suite runs used `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID`.

## 1. In a uv-managed Python repository with no declared package-tests command, the end-of-Build suite and finalize-review's suite pass on a machine where the first `python3` on PATH is an interpreter without the project's dependencies, with no PATH change by the agent.
- How I tried it:
  - Detection, new vs base checker, in the clone at 66d763b.
  - Ran both commands in the clone (no `.venv` present beforehand): `python3 -m pytest -q` and `uv run --locked python -m pytest -q`.
  - Built a throwaway Loom change `2026-10-29-at-probe` on branch `feat/2026-10-29-at-probe` (intent a63b3c7, plan + graduated test 0ee28be) and ran `loom-python --repair finalize-review 2026-10-29-at-probe --input <scratch>/at1/finalize-input.json`. The input carries two stub reviewer verdicts (not a real review; only there to reach the package run) and one graduated adversarial program.
  - End-of-Build: read `loom-code/skills/build/SKILL.md:117-121` and searched `loom-code/skills`, `loom-code/agents`, `loom-code/contract` for any listing of the build markers or a checker command Build is told to call (`intake` covers only write-spec / write-plan).
- What came back:
  - new: `working-tree: ('uv run --locked python -m pytest -q', 'detected uv.lock')`, `revision HEAD: (same)`; base: `('python3 -m pytest -q', 'detected pyproject.toml')`.
  - `python3 -m pytest -q` → `ModuleNotFoundError: No module named 'tasknote'`, `3 errors during collection`, exit 2.
  - `uv run --locked python -m pytest -q` → `Creating virtual environment at: .venv` … `25 passed in 0.09s`, exit 0. `uv.lock` sha256 `0518640a…b74da2` before and after; `git status --short` empty.
  - finalize-review → `wrote docs/loom/2026-10-29-at-probe/attestation.json for 64f4a2eb…`, exit 0; executions: `{'kind': 'package-tests', 'command': 'uv run --locked python -m pytest -q', 'result': 'pass'}` and the adversarial program `result: pass`.
  - Build step 3 says only "the command detected from build markers"; no station text names the markers or the `uv.lock` row, and no checker command prints the detected command for Build. The end-of-Build choice of command is left to the Build agent.
- Evidence: captured output above; attestation saved at `<scratch>/at1/attestation-positive.json`; `loom-code/skills/build/SKILL.md:117-121`; `loom-code/scripts/loom_checker/probes.py` `TEST_COMMAND_MARKERS` first row.
- Verdict (first run, edc30a0b): partly — finalize-review half works; end-of-Build half not verified (no Build run, and the station text does not carry the rule).

### Re-run after fix c5038e3a..0ffd76e6
- Setup check: `git worktree add --detach <scratch>/at2/loom-clean 0ffd76e6` (`git status --short` empty); `loom-python --repair --list-rules` exit 0. Fresh sample clone `git clone /Users/kouko/GitHub/loom-dogfood-sandbox <scratch>/at2/sandbox`, branch `at2-main` from `origin/main` 66d763b, no `.venv`. `command -v python3` → `/Users/kouko/.conda/envs/dbt-redshift/bin/python3`; PATH unchanged.
- How I tried it (end-of-Build half, following `loom-code/skills/build/SKILL.md:117-121` at 0ffd76e6 literally):
  - `grep package-tests docs/loom/KICKOFF-DEFAULTS.md` → none.
  - Opened `TEST_COMMAND_MARKERS` in `<scratch>/at2/loom-clean/loom-code/scripts/loom_checker/probes.py:29-35`; first row `uv.lock` → `uv run --locked python -m pytest -q`. `git ls-files --error-unmatch uv.lock` → committed; `git check-ignore -q -- uv.lock` → not ignored. So step 3 resolves to `uv run --locked python -m pytest -q`.
  - Ran it, and for contrast `python3 -m pytest -q`; compared with what finalize-review detects (`detect.py` with the at2 checker, working tree and HEAD).
  - Ran the fix's own tests: `uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest -q loom-code/tests/test_build_mechanical_checks.py` in the clean worktree.
- What came back:
  - `python3 -m pytest -q` → `Interrupted: 4 errors during collection`, exit 2.
  - `uv run --locked python -m pytest -q` → `Built tasknote …`, `Installed 6 packages`, `31 passed in 0.09s`, exit 0. `uv.lock` sha256 `0518640a…b74da2` before and after; `git status --short` empty.
  - detect: `working-tree: ('uv run --locked python -m pytest -q', 'detected uv.lock')`, `revision HEAD: (same)` — identical to the command Build step 3 resolves to.
  - `test_build_mechanical_checks.py` → `24 passed in 0.07s` (includes `test_suite_command_points_to_checker_marker_table`, `test_verify_copies_no_marker_command`). The complete package suite is left to finalize-review, which runs it and refuses the attestation on failure.
  - Counts differ from the first run (25 passed / 3 collection errors were recorded then at the same 66d763b); the outcome (pass via locked env, fail via conda `python3`) is the same.
  - Not done: no full Build station session was run; the station's step 3 was executed by hand as written.
  - Gap noted (pre-existing, not uv): `probes.py:819-823` falls back to `python3 -m pytest -q` when no marker row matches but `test_*.py`/`*_test.py` files exist; Build step 3 does not mention this fallback.
- Verdict (re-run, 0ffd76e6): works.
- Rows 2-4: carried over. `git diff --stat c5038e3a..0ffd76e6` touches only `plan.md`, `loom-code/CHANGELOG.md`, `loom-code/skills/build/SKILL.md`, `loom-code/tests/test_build_mechanical_checks.py`; no checker code (`loom-code/scripts/`) changed, so detection (2), the locked-run stop (3) and suite collection (4) are unaffected.

## 2. A Python repository without a uv lockfile, and any repository that declares a package-tests command, gets the same suite command as before.
- How I tried it (detect.py, new vs base checker, each case committed on its own clone branch):
  - `no-lock`: `git rm uv.lock`, committed.
  - ignored lock: same branch, `uv.lock` added to `.gitignore` (committed), then a real `uv.lock` copied into the working tree (`git status --ignored` → `!! uv.lock`).
  - `declared`: from main (with `uv.lock`), added `- package-tests: python3 -m pytest -q tests — …` to `docs/loom/KICKOFF-DEFAULTS.md`, committed.
- What came back:
  - no uv.lock: new and base both `('python3 -m pytest -q', 'detected pyproject.toml')` for working tree and HEAD.
  - ignored uv.lock: new `working-tree` and `revision HEAD` both `('python3 -m pytest -q', 'detected pyproject.toml')` (same as a repo without the file).
  - declared: new and base both `('python3 -m pytest -q tests', 'docs/loom/KICKOFF-DEFAULTS.md')`.
  - Change's own tests: `uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest -q loom-code/tests/test_probe_ignored_uv_lock.py loom-code/tests/test_selection_finalize.py loom-code/tests/test_loom_attestation.py -k "uv or ignored or python3 or declared or pyproject or conda"` → `12 passed, 91 deselected`.
- Evidence: captured output above.
- Verdict: works.

## 3. In such a repository whose committed lockfile no longer matches its declared dependencies, the suite stops with a message naming how to update the lockfile, and the lockfile is left unchanged.
- How I tried it: branch `stale-lock-2` (intent a63b3c7 + commit changing `dev = ["pytest>=8"]` to `dev = ["pytest>=8", "iniconfig>=1"]` without relocking + plan). Ran the detected command directly, then `finalize-review 2026-10-29-at-probe --input <scratch>/at1/finalize-input-noprog.json` (no-program adversarial record so the run reaches the package step). Also ran finalize-review on `stale-lock` (same stale lock plus a graduated program).
- What came back:
  - direct: `error: The lockfile at `uv.lock` needs to be updated, but `--locked` was provided.` / `hint: To update the lockfile, run `uv lock`.`, exit 1.
  - finalize (package step): `BLOCK finalize.package-tests: `uv run --locked python -m pytest -q` exited 1` followed by the same error and `uv lock` hint, exit 1.
  - finalize (with graduated program): `BLOCK finalize.adversarial: package suite collection unavailable: error: The lockfile … hint: To update the lockfile, run `uv lock`.`, exit 1.
  - `uv.lock` sha256 `0518640a0ba29a609c3158411dcf384aafdd93be69a11d21c439ebbe20b74da2` before and after every run; `git status --short` empty after each.
- Evidence: captured output above.
- Verdict: works.

## 4. In such a repository, an adversarial program graduated into the package suite is recognized at finalize-review as collected by that suite.
- How I tried it:
  - Positive: the finalize-review run of row 1 included `{"command": "uv run --locked python -m pytest tests/test_adversarial_count_empty.py", "artifact": "tests/test_adversarial_count_empty.py"}` (a graduated program with a `# concern:` line under `tests/`).
  - Negative: branch `neg-outside` adds `scripts/test_outside_probe.py` (outside `testpaths`); finalize-review with `<scratch>/at1/finalize-input-neg.json` naming it.
  - Before/after: `detect.py --collect tests/test_adversarial_count_empty.py` with new and base checkers; `--collect src/tasknote/cli.py` with the new one.
- What came back:
  - Positive: finalize exit 0, attestation records the adversarial execution `result: pass`.
  - Negative: `BLOCK finalize.adversarial: adversarial artifact must be committed under docs/loom/2026-10-29-at-probe/evidence/probes/ or be a program the package suite already runs`, exit 1.
  - new: `suite_collection(tests/test_adversarial_count_empty.py): (True, '')`, `suite_collection(src/tasknote/cli.py): (False, '')`; base: `(None, 'pytest exited without collection')`.
- Evidence: captured output above; committed tests `loom-code/tests/test_selection_finalize.py` (uv cases) within the 12 passed above.
- Verdict: works.

## Data already in the user's repository
- `uv run --locked` creates `.venv` when absent (git-ignored in the sample). With an existing `.venv` holding `six` (extra) and `pytest 8.3.5` (lock says 9.1.1), one suite run printed `Installed 2 packages`; afterwards `pytest 9.1.1`, `six 1.17.0` — locked packages are brought to the lock's versions, extra packages stay. No committed file changed in any run (`git status --short` empty).

## Complete package suite of this repository
- Command (KICKOFF-DEFAULTS `package-tests:`), run once in the clean worktree at edc30a0b: `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q` → exit 0 in 2:19; pytest groups include `2453 passed, 2 skipped`, `260 passed`, `204 passed, 1 skipped`, `248 passed, 5 skipped`, all others passed. Full log: `<scratch>/at1/suite-full.log`.
