# Every test lives in a tests folder — acceptance test evidence

Tried on 2026-09-25, in clean clones of the project: the branch head at
b560fb23 (`head`), the branch base at 23dad634 (`base`, = origin/main), and a
third throwaway clone of b560fb23 (`plant`) for planted tests. All three were
fresh `git clone --no-hardlinks` copies in the session scratch directory,
removed afterwards. The implementers' own count files were read only after my
counts were taken, to compare against.

Environment for every pytest run: `uv run --isolated --with-requirements
requirements-package-tests.lock` (the lock and runner named by the
`package-tests:` line in `docs/loom/KICKOFF-DEFAULTS.md`).

Setup check: the README has no developer-setup section beyond "each plugin keeps
its own tests"; the documented suite command
(`uv run --isolated --with-requirements requirements-package-tests.lock python
scripts/run_package_tests.py --loom-family -q`) ran in the clean head clone with
no extra steps and exited 0 (section 2).

## 1. Outside `docs/loom/`, every test file in the repository is under a plugin's `tests/` folder (that plugin's tests) or the root `tests/` folder (repository-level tests); none remains beside production code or inside a skill folder.
- How I tried it: in `head`,
  `git ls-files | grep -E '(^|/)(test_[^/]*\.py|[^/]*_test\.py|test-[^/]*\.sh)$' | grep -v '^docs/loom/'`,
  then filtered for paths with no `tests/` segment. Broader sweep for any name
  containing `test`/`_spec`/`conftest.py` outside a `tests/` folder. Same listing
  at `base`, and every base file mapped through
  `git diff -M --name-status 23dad634...b560fb23`.
- What came back:
  - 242 test files at head; 0 outside a `tests/` folder. By top folder: loom-code 112,
    loom-design 15, loom-workflow 99, root `tests/` 16.
  - Base had 238, of which 216 were outside a tests folder (the other 22 were
    already in loom-code/tests and loom-workflow/tests) (loom-code/scripts 104,
    loom-code/skills 3 probe files, loom-design/scripts 14, loom-workflow/scripts 21,
    loom-workflow/skills 58, loom-workflow/.claude-plugin 1, root scripts 12,
    .claude/hooks 3).
  - Every one of the 238 base files maps to a head file; the 4 head files with no
    base origin are the new guards `loom-code/tests/test_loom_code_tests_folder.py`,
    `loom-design/tests/test_loom_design_tests_folder.py`,
    `loom-workflow/tests/test_loom_workflow_tests_folder.py`,
    `tests/test_tests_folder_convention.py`.
  - Broader sweep hits outside tests folders are not tests:
    `*/test-prompts.json` (skill trigger-eval prompts, 6 files), the
    acceptance-tester agent and report template (`.md`), an example-run doc,
    `loom-design/scripts/interface/design_md_spec_keys.py`,
    `requirements-package-tests.lock`, `scripts/run_package_tests.py` (the runner).
  - `loom-workflow/tests/scripts/` is a subfolder of a tests folder (the old
    loom-workflow/scripts tests), not production code.
- Evidence: file list captured in the scratch run (242 lines); counts above.

## 2. The package suite collects and passes the same tests it collected before the move, plus the skill probe tests it did not collect before, with none lost; the before and after counts per plugin are recorded.
- How I tried it:
  - Collected node ids with each commit's OWN inventory: a script imported
    `scripts/run_package_tests.py::loom_family_commands` from the clone it ran in,
    ran every pytest command with `--collect-only -p no:cacheprovider` (xdist `-n`
    stripped), and keyed each id by (file basename, test name incl. params) — a
    move changes the folder, not that key; compared as multisets.
  - Ran the full suite once at head with the documented command.
- What came back (collection):
  - base 3574 ids (13 sessions: 2273, 246, 52, 196, 261, 121, 64, 43, 13, 1, 83, 209, 12).
  - head 3627 ids (13 sessions: 2321, 248, 55, 261, 121, 64, 43, 13, 1, 83, 209, 12, 196).
  - lost: 0. extra: 53, by file:
    | File (head) | + | Why |
    |---|---|---|
    | loom-code/tests/test_build_recovery_rules.py | 8 | ex skills/build/probes, never collected |
    | loom-code/tests/test_closing_review_recovery_rules.py | 13 | ex skills/closing-review/probes, never collected |
    | loom-code/tests/test_ship_guidance_presence.py | 2 | ex skills/ship/probes, never collected |
    | loom-workflow/tests/test_plugin_manifest.py | 1 | ex loom-workflow/.claude-plugin, never collected |
    | tests/test_run_package_tests.py | 5 | new inventory guards |
    | tests/test_tests_folder_convention.py | 17 | new convention + repo-wide guards |
    | loom-code/tests/test_loom_code_tests_folder.py | 2 | new guard |
    | loom-design/tests/test_loom_design_tests_folder.py | 2 | new guard |
    | loom-workflow/tests/test_loom_workflow_tests_folder.py | 2 | new guard |
    | loom-code/tests/test_probes_coldread_abuse_coldread_branch_end.py | 1 | new `test_byte_identity_tolerates_only_the_graduated_dir_line` |
    24 previously-uncollected (23 probes + 1 manifest) + 29 new guard tests = 53. Matches `after-counts.md` exactly.
- What came back (full run at head, clean clone, exit 0):
  - code `tests loom-code/tests`: 2319 passed, 2 skipped
  - design `loom-design/tests`: 247 passed, 1 skipped
  - workflow-python: 55, 261, 121, 64, 43, 13, 1, 80+3s, **204+5s**, 12, 196 → 1050 passed, 8 skipped
  - workflow-shell: 17 scripts, 145 PASS / 0 FAIL
  - workflow-mermaid: npm ci + 11/11 mermaid blocks parsed + negative check PASS
  - pytest total: 3616 passed, 11 skipped (= 3627 ids).
- Difference from `after-counts.md` (3621 passed, 6 skipped): 5 tests in
  `loom-workflow/tests/loom-visualization/test_adversarial_probes.py` skip with
  "node or tests/mermaid/node_modules absent" in a fresh clone, because the
  mermaid group's `npm ci` runs after the workflow-python group. Re-running that
  folder after the suite (node_modules now present) gave 209 passed. The base
  clone, also fresh, gives the same 204 passed + 5 skipped for its
  `loom-workflow/skills/loom-visualization/scripts`. So this is pre-existing
  order dependence, not something the move lost; the ids are all collected.
- Diff scan of the 128 non-identical renames for non-path changes: only path /
  import lines, release version pins (3.14.1, 2.3.2), and one loosening in
  `loom-code/tests/test_probes_coldread_abuse_coldread_branch_end.py::test_graduated_probe_copies_byte_identical_to_evidence_originals`
  (it now skips comparing its own file, and tolerates a differing
  `graduated_dir =` line; marked "decided 2026-09-25").
- Evidence: suite log and the two id tables in the scratch run; command above.

## 3. A test added later anywhere under a `tests/` folder is run by the package suite without editing the suite command, and CI runs the same tests; the one exception is a `tests/local/` folder, which holds tests that need a locally installed CLI and is named as local-only.
- How I tried it: in `plant`, wrote throwaway tests without touching the runner,
  then printed `loom_family_commands()` and ran each pytest command with
  `--collect-only`, filtering for `planted`:
  - pytest files: `tests/planted_sub/`, `loom-code/tests/planted_sub/`,
    `loom-design/tests/planted_sub/`, `loom-workflow/tests/planted_skill/`, a
    `*_test.py`-only folder `loom-code/tests/suffix_only/`, and one each in
    `tests/local/`, `loom-code/tests/local/`, `loom-design/tests/local/`,
    `loom-workflow/tests/local/`.
  - shell tests: `loom-workflow/tests/test-planted-top.sh`,
    `loom-workflow/tests/sub_sh/test-planted.sh`, `loom-code/tests/test-planted.sh`.
- What came back:
  - Run: all four `planted_sub`/`planted_skill` pytest files (the workflow one
    got its own new session `[11] pytest loom-workflow/tests/planted_skill`), the
    `*_test.py` file, and `loom-workflow/tests/test-planted-top.sh`.
  - Skipped: all four `tests/local/` files — each session carries
    `--ignore=<folder>/tests/local`.
  - **Not run:** `loom-code/tests/test-planted.sh` and
    `loom-workflow/tests/sub_sh/test-planted.sh`. The runner's shell group is only
    `sorted((repo / "loom-workflow/tests").glob("test-*.sh"))`
    (`scripts/run_package_tests.py`, `workflow-shell` branch), so a shell test in
    any other tests folder, or a subfolder of loom-workflow/tests, is silently not
    run. The repo's own guard
    `tests/test_tests_folder_convention.py::test_planted_test_in_a_tests_folder_or_docs_loom_is_allowed[loom-workflow/tests/loom-memory/test-zz-planted.sh]`
    declares that exact placement allowed; AGENTS.md "Test Location" says new
    tests need no suite-command edit.
  - Also by construction: the code group targets only `tests` and
    `loom-code/tests`, design only `loom-design/tests`, workflow only
    `loom-workflow/tests` — a tests folder of a new, fourth plugin would not be
    run (the guard also allows `loom-new/tests/`). Not a planted case.
- CI: `.github/workflows/loom-code-ci.yml` runs `--only code` and triggers on
  `tests/**`, `loom-code/**`, `loom-design/**`, `loom-workflow/**`, `scripts/**`;
  `loom-design-ci.yml` runs `--only design`, triggers on `loom-design/**` and
  the runner; `loom-workflow-ci.yml` runs `--only workflow-shell`,
  `--only workflow-python`, `--only workflow-mermaid`, triggers on
  `loom-workflow/**` and the runner. The five `--only` groups are all five
  groups in `GROUPS`, so CI covers the whole inventory; every tests folder is
  under a trigger path.
- Evidence: planted-run output captured in the scratch run (35 commands; 9
  planted ids run, the rest are pre-existing tests whose names contain "planted").

## 4. The repository's contributor guidance states where tests go, and every document an agent reads at run time names the new locations.
- How I tried it: read AGENTS.md at head; grepped runtime documents for every
  moved-away test path. Needles (434): each renamed test file's old repo path,
  its old plugin-relative form (e.g. `scripts/test_x.py`,
  `skills/<s>/scripts/test_x.py`), and the old folder prefixes
  (`loom-code/scripts/test_`, `loom-design/scripts/test_`,
  `loom-workflow/scripts/test_`, `.claude/hooks/test_`,
  `loom-code/skills/*/probes`, `loom-code/tests/integration`,
  `loom-workflow/.claude-plugin/test_`). Haystack (223 files at head): every
  tracked file under `loom-*/{skills,agents,contract,hooks,commands}/`, every
  top-level `loom-*/scripts/*.py|sh`, root `scripts/*.py`, AGENTS.md, CLAUDE.md,
  `loom-code/scripts/rehearse_probes.py`, `docs/loom/evidence/mechanisms.yaml`,
  `docs/loom/KICKOFF-DEFAULTS.md`, `docs/loom/README.md`; files under `/tests/`
  excluded.
- What came back:
  - AGENTS.md has a new "Test Location" section (plugin tests in `<plugin>/tests/`,
    skill tests in `loom-workflow/tests/<skill>/`, repo-level in root `tests/`,
    never beside production code or in a skill folder, `tests/local/` skipped,
    suite discovers tests, `docs/loom/` evidence exempt, remove a skill's tests
    folder with the skill); its Module Criteria line now points at
    `loom-code/tests/test_module_criteria_text.py`.
  - Head: 0 hits. Control run of the same script at base: 467 hits (e.g.
    AGENTS.md:54, mechanisms.yaml:50/77), so the needles do match old paths.
  - New locations present: `rehearse_probes.py:66` `DEFAULT_GLOB =
    "loom-code/tests/test_probes_*.py"`; mechanisms.yaml evals point at
    `loom-code/tests/…` and `loom-workflow/tests/…`;
    `loom-code/skills/closing-review/references/adversarial.md:146` names
    `loom-code/tests/test_adversarial_empty_input.py`.
- Evidence: grep script output (head 0 hits / base 467 hits).

## 5. The checker's rule list does not grow and no new step, reviewer or dispatch is added.
- How I tried it: `python3 loom-code/scripts/loom_checker.py --list-rules` in both
  clones and `diff`; `python3 loom-code/scripts/check_mechanisms.py --baseline
  origin/main` in `head` (origin/main = 23dad634), and `--baseline main` in the
  working repo; `git diff 23dad634...b560fb23 -U0` over skills, agents, contract
  and hooks prose.
- What came back:
  - 26 rules at both; `diff` empty (IDENTICAL).
  - check_mechanisms: skill 22/22, checker-rule 26/26, hook 10/9 (the exempt
    host-hygiene hook), contract 63/63, prose-gate 20/20; net 140 = baseline 140;
    "all clear", exit 0 (both invocations).
  - Runtime prose diff: only path substitutions (adversarial.md, distill-sessions
    SKILL.md and runtime-protocol.md, handoff, loom-memory docs) and fixtures
    that moved out of skill folders; no added step, reviewer, gate or dispatch
    wording.
- Evidence: rule lists diffed; check_mechanisms output quoted above.
