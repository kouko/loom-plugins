# Skill folder check and AGENTS.md cleanup — acceptance test evidence

Tried on 2026-11-18, in clean copies of the project at 9552e1de1
(9552e1de163016299fa863abad0017419fba089c). Every copy was a fresh
`git clone --no-hardlinks` at that commit with an empty `git status`. Each Acceptance 1
scenario had its own clone. No trial touched the session worktree, and nothing was
repaired. Section 2 is carried over from f3770eaec; see the last re-run section.

Setup: the README's Development section has no contributor test setup, so I used the
command the station gave. Every test command ran through
`env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python ...`;
the environment resolved in each clone and the baseline passed. The change edits no
plugin path (`git diff --name-only main...HEAD` outside `AGENTS.md`, `tests/` and
`docs/loom/`: 0 files), so no plugin install was needed to use it.

The full package suite was not run here; `finalize-review` executes it:
`env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`

## 1. 在任一 skill 的子資料夾內加入含檔案的巢狀資料夾後，不論是否已 commit，完整 package suite 都會失敗並指出該路徑；移除後恢復通過。

- How I tried it: built each case in its clone with ordinary `git` commands, then ran
  the suite runner on the covering file with the suite's flags:
  `python scripts/run_package_tests.py tests/test_skill_folder_flatness.py -q -n auto`.
- Suite membership: `loom_family_commands(Path.cwd())` starts with
  `pytest tests loom-code/tests --ignore=<clone>/loom-code/tests/local ...`, and
  `pytest tests loom-code/tests --collect-only -q -k test_repository_skill_folders_are_flat --ignore=loom-code/tests/local`
  reports `tests/test_skill_folder_flatness.py::test_repository_skill_folders_are_flat`,
  `1/2894 tests collected`.
- Failure message: ``AssertionError: skill subfolders must not contain subfolders, and no gitlink may sit at a plugin, its skills folder or beneath; move these files up one level, or remove a gitlink with `git rm --cached <path>` and commit:`` followed by the paths.
- In the tables, `F` is exit 1 with `1 failed, 15 passed`, the failure always being
  `test_repository_skill_folders_are_flat`; `P` is exit 0 with `16 passed`. Baseline: `P`.
  The one exception is the `loom-code` gitlink, described under its own table.
  `X` stands for `loom-code/skills/x`, `CR` for
  `loom-code/skills/closing-review/references`.

Ordinary nested folder (`git add`, `git commit`, then `git rm` + commit):

| Case | Uncommitted | Staged | Committed | Removed by commit | Path named |
|---|---|---|---|---|---|
| `CR/nested-trial/note.md` | F | F | F | P | that path |
| `loom-workflow/skills/critique/nested-new-sub/deeper/note.md` | F | F | F | P | that path |
| `loom-design/skills/write-spec/references/深層/說明 檔.md` | F | F | F | P | that path |

An uncommitted `CR/nested-trial/note.md` moved out of the clone, separate clone: F, then P,
with `git status --short` empty.

Nested git repository (inner repository has one commit; `git add <folder>` records mode
160000):

| Repository at | Holding | Untracked | Untracked, moved away | Gitlink staged | Gitlink committed | Committed, folder moved away | Removed by commit |
|---|---|---|---|---|---|---|---|
| `X/references/` | `deep/f.md` | F | P | F | F | F | P |
| `X/` | `references/deep/f.md` | F | P | F | F | F | P |
| `X/references/vendored/` | `inner.md` | F | P | F | F | F | P |

Paths named: untracked names the inner nested file (for `vendored/`, also the folder);
staged or committed names the gitlink folder and the inner file; with the folder moved
away, the gitlink folder only.

Committed gitlink in a new `git clone` of that commit (mode 160000, folder has 0 entries):

| Gitlink at | Result | Path named | After `git rm --cached` + commit, in that clone |
|---|---|---|---|
| `X/references/` | F | `X/references/` | P |
| `X/` | F | `X/` | P |
| `X/references/vendored/` | F | `X/references/vendored/` | P |

"Removed by commit" in the first table is `git rm --cached <path>`, the folder moved out,
commit.

Gitlink at every level. Each repository holds a file that would be nested once it sits in
the plugin (`.../references/deep/f.md`). For a folder git already tracked, its files were
first dropped from the index and moved out:

| Gitlink at | Committed, inner repository present | New clone, unfetched (0 entries) | There: `git rm --cached` + commit | There: `git rm -r -f` + commit | Inner repository present: `git rm --cached` + commit | Then folder moved away |
|---|---|---|---|---|---|---|
| `loom-design` | F | F | P | P | **F** | P |
| `loom-design/skills` | F | F | P | P | **F** | P |
| `loom-code/skills` | F | F | P | P | **F** | P |
| `X` | F | F | P | P | **F** | P |
| `X/references` | F | F | P | P | **F** | P |

Paths named: committed with the repository present, the gitlink folder and the inner nested
file; unfetched, the gitlink folder only; after `git rm --cached` with the repository still on
disk, the inner nested file only, because it is now an untracked repository. A flat repository
at `X/references` in that same state: P.

Gitlink at `loom-code` (mode 160000, 0 entries in a new clone). The suite runner imports
`repo_files` from that folder (`scripts/run_package_tests.py:47-49`), so it stops before any
test runs:

| State | Suite runner | `pytest tests/test_skill_folder_flatness.py -q` |
|---|---|---|
| committed, inner repository present | exit 1, `ModuleNotFoundError: No module named 'repo_files'`, **no path named** | F, names `loom-code/` and the inner file |
| new clone, unfetched | same | F, names `loom-code/` |
| `git rm --cached` + commit | same | P |
| plugin files restored from the earlier commit and committed | P | P |

`git rm -r -f <gitlink>`, run without `-n` at all six levels:

| Folder state | Result |
|---|---|
| holds the inner repository | exit 128, `fatal: could not lookup name for submodule '<path>'`; the entry stays in the index and the check still fails |
| empty, in a new clone | exit 0, `rm '<path>'`; the folder is gone; after a commit the check passes (at `loom-code` this last step was not run through the check) |
| absent, in a new clone | exit 0 |
| holds plain files and no `.git`, in a new clone | exit 0 |

A committed gitlink elsewhere in a plugin, `loom-code/vendor` holding `deep/er/f.md`: **P**,
also in a new clone.

Flat repositories (nothing nested inside):

| Repository at | Holding | Untracked | Committed gitlink | Gitlink in new clone | Path named |
|---|---|---|---|---|---|
| `X/references/` | `flat.md` | **P** | **F** | **F** | `X/references/` |
| `X/` | `SKILL.md`, `references/flat.md` | **P** | **F** | **F** | `X/` |

Ignored names, links, and folders outside the plugin list:

| Case | Result | Path named |
|---|---|---|
| uncommitted `CR/node_modules/f.txt` (`.gitignore:5`) | **P** | none |
| uncommitted `CR/__pycache__/f.txt` (`.gitignore:1`) | **P** | none |
| uncommitted `CR/.venv/f.txt` (`.gitignore:4`) | **P** | none |
| uncommitted `CR/.pytest_cache/f.txt` (`.gitignore:2`) | **P** | none |
| uncommitted `CR/sub/x.pyc` (`.gitignore:3`, `*.py[cod]`) | **P** | none |
| uncommitted repository at `CR/node_modules/` holding `inner.md` | **P** | none |
| uncommitted repository at `CR/node_modules/` holding `deep/f.md` | **P** | none |
| same, plus `__pycache__/x.pyc` ignored by its own rules (inner `git status` empty) | **P** | none |
| same repository added with `git add -f` (mode 160000) | F | the folder, `.gitignore`, `__pycache__/x.pyc`, `deep/f.md` |
| `CR/node_modules/f.txt` staged with `git add -f` | F | that path |
| same, committed | F | that path |
| symlink `CR/link-to-folder` to `trial-target/` holding `deep/f.md`, uncommitted; `deep/f.md` read through the link | **P** | none |
| same link and target committed (link mode 120000) | **P** | none |
| same, new clone; `deep/f.md` read through the link | **P** | none |
| `new-plugin/skills/x/references/deep/f.md`, a top-level folder not in `marketplace.json`, uncommitted | **P** | none |
| same, committed | **P** | none |

Ignored files inside a nested repository (inner `.gitignore` covers them; inner
`git status --short` empty; the root `.gitignore` also names `__pycache__/`):

| Case | Before | With the ignored file | After removing it | Path named |
|---|---|---|---|---|
| flat repository at `X/references/`, `__pycache__/x.pyc` | P | **F** | P | `X/references/__pycache__/x.pyc` |
| flat repository at `X/`, `scripts/__pycache__/a.pyc` | P | **F** | not tried | `X/scripts/__pycache__/a.pyc` |
| flat repository at `X/references/`, `cache/c.bin`, ignored only by the inner rule | not tried | **F** | not tried | `X/references/cache/c.bin` |
| repository at `X/references/vendored/`, `__pycache__/x.pyc` | not tried | F | not tried | the folder, `.gitignore`, `__pycache__/x.pyc`, `inner.md` |

Committed file deleted from disk (`CR/nested-trial/note.md`):

| State | Result | Path named |
|---|---|---|
| committed, on disk | F | that path |
| deleted from disk, deletion not committed (`git status`: ` D`) | **P** | none |
| new clone of that same commit | **F** | that path |
| deletion staged with `git rm` | P | none |
| deletion committed | P | none |
| new clone after the deletion commit | P | none |

Why each limit exists, from `tests/test_skill_folder_flatness.py`:

- Ignored paths pass: `:82-83` uses `git ls-files --cached --others --exclude-standard`;
  reason at `:16-17`.
- Folder symlinks pass: `:91` does not treat a link as a folder; reason at `:18`.
- Deleted but uncommitted files pass: `:90` keeps only listed paths still on disk; reason
  at `:19-20`.
- Every gitlink at a plugin, its `skills` folder or beneath fails, flat or not: `:50` and
  `:98-109`; reason at `:10-13`. A gitlink elsewhere in a plugin does not match `:50`.
- Ignored files inside a listed nested repository fail: `:58-72` walks the disk and applies
  no ignore rule; reason at `:22-25`.
- Folders outside `marketplace.json` are not checked: `:42-50`; reason at `:27-29`.

Verdict basis: `partly`. "Any nested folder, committed or not" does not hold for the bold
`P` rows of ignored names and symlinks, and a gitlink at `loom-code` fails the suite without
naming the path. The removal half holds in every case tried, once the nested content is
really gone.

## 2. `AGENTS.md` 不再提及不在這個 repo 的 plugin，也不再指向不存在的檔案或測試。

- How I tried it: in a clean clone, read `.claude-plugin/marketplace.json`; searched
  `AGENTS.md` for
  `domain-teams|investing|monkey|research-toolkit|obsidian|tsundoku|dbt|skill-dev|think-orbit|ascii-graph|redshift|briefing|toolkit|concept-model`
  (case-insensitive); checked every backticked path-like token on disk, expanding
  `<placeholder>` as a glob; checked the named pytest node id is defined.
- What came back: marketplace is `loom-workflow`, `loom-code`, `loom-design`; the name search
  has no match; 46 tokens resolve, including `tests/test_skill_folder_flatness.py`,
  `.claude/hooks/validate-skill-folder-structure.sh`,
  `loom-code/tests/test_module_criteria_text.py`, `scripts/run_package_tests.py`,
  `loom-code/scripts/check_contract_citations.py`,
  `loom-code/skills/closing-review/references/lenses.md`, the three pin test files, both
  `docs/loom/memory/` entries and `docs/loom/README.md`.
  `test_current_release_metadata_is_synchronized` is defined at
  `loom-code/tests/test_write_plan_station_text.py:392`.
- Tokens not resolved from the repository root, all non-pointers:
  - `AGENTS.md:7` `references/lenses.md`: the skill-relative example; its full form at
    `AGENTS.md:8` resolves.
  - `AGENTS.md:63` `probes/`, `AGENTS.md:64` `tests/local/`: generic folder names.
  - `AGENTS.md:65` `test_*.py`, `*_test.py`, `test-*.sh`; `AGENTS.md:81` `.py`, `.sh`: patterns.
  - `AGENTS.md:13` `REQ-<n> — <name>`, `AGENTS.md:14` `needs-design: yes`,
    `AGENTS.md:100` the gate marker, `AGENTS.md:108` the changelog heading: text formats.
  - `AGENTS.md:111` `claude plugin update`: a command.

## 3. `AGENTS.md` 對 skill 資料夾檢查、審查鏡頭與人數、版號及 changelog 的描述，都與 repo 現行的檢查和檔案一致。

- `AGENTS.md:42`, first half (violations fail the named test; exceptions and reasons are in
  that file's opening): section 1 shows the failure, and the opening is compared below.
- `AGENTS.md:42`, second half (no report at write time): `.claude/settings*.json` is absent,
  `.claude/hooks/validate-skill-folder-structure.sh` is executable, and
  `loom-workflow/scripts/validate-skill-folder-structure.sh:32-33` exits 0 when it is. Feeding
  that hook a real nested file
  (`<clone>/loom-code/skills/closing-review/references/hook-trial/f.md`) gave exit 0 and no
  message.
- Opening docstring of `tests/test_skill_folder_flatness.py` against section 1:

| Lines | Claim | Observed |
|---|---|---|
| 5-7 | tracked paths, even under an ignored folder, plus untracked non-ignored files, while on disk | matches: force-added `node_modules` F; deleted file P |
| 7-8 | a nested repository is searched on disk | matches: untracked repositories name inner files |
| 10-13 | a committed gitlink at a plugin, its `skills` folder, a skill or beneath always fails, with or without its folder | matches at every level, flat or not, in new clones; a staged gitlink fails too |
| 16-17 | an uncommitted ignored path passes | matches |
| 18 | a folder symlink passes | matches: uncommitted, committed, new clone |
| 19-20 | a committed file deleted from disk passes | matches |
| 22-25 | an ignored file inside a listed nested repository fails; a repository under an ignored name is not listed and passes | matches both halves |
| 27-29 | only top-level folders in `marketplace.json` are plugins | matches: `new-plugin/` P |

- Review lenses and count (`AGENTS.md:95-97`): `lenses.md` exists with Code, Docs, Conformance
  and question, Skill and Plan sections.
  `python3 loom-code/scripts/loom_checker.py reviewer-count 2026-11-18-skill-folder-check-and-agents-cleanup`
  printed `2`. `--list-rules` printed 31 lines (`AGENTS.md:98`). 14 files under `loom-*/skills/`
  carry `<!-- gate: ` markers (`AGENTS.md:100`).
- Versions and changelog (`AGENTS.md:105-112`):

| Plugin | SSOT | Codex | Root manifest | package.json | Newest changelog | Plugin READMEs (en/ja/zh-TW) | Root README hits |
|---|---|---|---|---|---|---|---|
| loom-code | 3.84.0 | 3.84.0 | 3.84.0 | 3.84.0 | `## [3.84.0] — 2026-11-17 — ...` | 1/1/1 | 2 |
| loom-design | 2.26.0 | 2.26.0 | 2.26.0 | 2.26.0 | `## [2.26.0] — 2026-11-16 — ...` | 1/1/1 | 2 |
| loom-workflow | 5.26.0 | 5.26.0 | 5.26.0 | 5.26.0 | `## [5.26.0] — 2026-11-16 — ...` | 1/1/1 | 2 |

- Behaviour trial in a separate clone: `python3 scripts/sync_codex_manifests.py --all` left
  `git status` empty. After changing only `loom-design/.claude-plugin/plugin.json` to 2.26.1,
  the same command changed `.codex-plugin/plugin.json`, `plugin.json` and `package.json`.
  With changelog and READMEs left alone,
  `pytest loom-design/tests/spec/test_capture_intent_contract.py -q` gave `1 failed, 27 passed`
  (`test_loom_design_version_2_17_0_consistent`).
- The older claims searched for (`11 維`, `≥2`, `三份`, `hook 擋`, `會被 ... 擋下`) have no match.
- Verdict basis: `works`: every `AGENTS.md` statement and every claim in the opening it
  points to matches what I observed.

## 4. `AGENTS.md` 仍保留 skill 資料夾扁平與版號 bump 的 MUST 規則，完整 package suite 通過。

- MUST rules: `AGENTS.md:18` (flat skill folders) and `AGENTS.md:105` (version bump for a PR
  touching a plugin), plus `:46`, `:59`, `:73`. Sections Module Criteria, Test Location,
  Contract Citations and loom 1.0 flow are all present.
- Tests covering this line, in a clean clone:
  - `python scripts/run_package_tests.py` with `-q -n auto` on
    `tests/test_skill_folder_flatness.py`, the four `tests/test_adversarial_flatness_*.py`,
    `tests/test_tests_folder_convention.py`, `tests/test_sync_codex_manifests.py`,
    `tests/test_adversarial_agy_rule_sync.py`, and `loom-code/tests/` files
    `test_module_criteria_text.py`, `test_check_contract_citations.py`,
    `test_check_skill_crossrefs.py`, `test_legacy_contract_removed.py`,
    `test_adversary_protocol.py`, `test_write_plan_station_text.py`: `235 passed`.
  - `pytest loom-design/tests/spec/test_capture_intent_contract.py -q`: `28 passed`.
  - `pytest loom-workflow/tests/scripts/test_release_metadata.py -q`: `15 passed`.
  - Total 278 passed; `git status --short` stayed empty.
- Repository checks: `loom-code/scripts/check_contract_citations.py` printed
  `OK: 1 known-violating files unchanged, no new contract citations of this repo's records.`;
  `loom-code/scripts/check-skill-crossrefs.py` printed `OK: all relative skill cross-references resolve.`
- Full suite: not run here. It is cited as the check `finalize-review` executes, with the
  command at the top of this file.

## Re-run on 2026-11-18, at f3770eaec

This run replaces the earlier one at 23682b64c; the functional content changed since then.

- 1: re-tested — every case in section 1: ordinary folders, repositories at all three
  depths, gitlinks in new clones, ignored names, folder symlinks, ignored files inside
  repositories, and files deleted before the deletion is committed.
- 2: re-tested — marketplace, name search, path tokens and node id in a clean clone.
- 3: re-tested — `AGENTS.md:42` and the test file's opening against section 1, hook trial,
  lenses, reviewer count, versions, sync and bump trial.
- 4: re-tested — MUST rules, covering tests and repository checks in a clean clone.

## Re-run on 2026-11-18, at 9552e1de1

Fix range `31126fefe..9552e1de1` changes only `tests/test_skill_folder_flatness.py`.

- 1: re-tested — every case in section 1 again, plus gitlinks at a plugin, its `skills`
  folder, a skill and a skill subfolder, unfetched, and each removal route.
- 2: carried over — the fix leaves `AGENTS.md` unchanged and the test file it names still
  exists.
- 3: re-tested — `AGENTS.md:42` and the changed opening against section 1, hook trial, lenses,
  reviewer count, versions, sync and bump trial.
- 4: re-tested — MUST rules, covering tests including the changed file, and repository checks.
