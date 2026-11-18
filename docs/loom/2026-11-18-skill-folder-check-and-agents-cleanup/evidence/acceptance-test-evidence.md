# Skill folder check and AGENTS.md cleanup — acceptance test evidence

Tried on 2026-11-18, in clean copies of the project at 23682b64c
(23682b64c3ef14afed97c9abbed286ed5ac49e80). Every copy was a fresh
`git clone --no-hardlinks` checked out at that commit with an empty `git status`.
Each Acceptance 1 trial sequence had its own clone. No trial touched the session
worktree, and nothing was repaired.

Setup: the README's Development section has no contributor test setup, so I used the
command in `AGENTS.md` and the closing-review station. Every test command ran through
`env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python ...`;
the environment resolved in each clone and the baseline passed. The change edits no
plugin path (`git diff --stat main...HEAD`: `AGENTS.md`, `tests/`, `docs/loom/`), so no
plugin install was needed to use it.

The full package suite was not run here; `finalize-review` executes it:
`env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`

## 1. 在任一 skill 的子資料夾內加入含檔案的巢狀資料夾後，不論是否已 commit，完整 package suite 都會失敗並指出該路徑；移除後恢復通過。

- How I tried it: in a fresh clone, built each case, then ran the suite runner on the
  covering file with the suite's own flags:
  `python scripts/run_package_tests.py tests/test_skill_folder_flatness.py -q -n auto`.
  Commits used `git add` / `git commit`; a plain `git add <nested repository>` records a
  gitlink (mode 160000, confirmed with `git ls-files -s`).
- Suite membership: `loom_family_commands(Path.cwd())[0]` runs
  `pytest tests loom-code/tests --ignore=<clone>/loom-code/tests/local -q -n auto`, and
  `pytest tests loom-code/tests --collect-only -q -k test_repository_skill_folders_are_flat --ignore=loom-code/tests/local`
  reports `tests/test_skill_folder_flatness.py::test_repository_skill_folders_are_flat`,
  `1/2889 tests collected`.
- Failure message: `AssertionError: skill subfolders must not contain subfolders; move these files up one level:` followed by the paths.
- In the tables, `F` is exit 1 with `1 failed, 10 passed`; `P` is exit 0 with `11 passed`.
  Baseline: `P`. `X` stands for `loom-code/skills/x`, `CR` for
  `loom-code/skills/closing-review/references`.

Ordinary nested folder:

| Case | Uncommitted | Staged | Committed | Removed | Path named |
|---|---|---|---|---|---|
| `CR/nested-trial/note.md` | F | F | F | P (`git rm` + commit); P (uncommitted copy moved away, separate clone) | that path |
| `loom-workflow/skills/critique/nested-new-sub/deeper/note.md` | F | F | F | P (moved away, deletion not committed); P (deletion committed) | that path |
| `loom-design/skills/write-spec/references/深層/說明 檔.md` | F | not tried | F | P (`git rm` + commit) | that path |

Nested git repository (inner repository has one commit):

| Repository at | Holding | Untracked | Untracked, moved away | Committed gitlink | Gitlink: folder moved away, still committed | Gitlink removed by commit | Path named on failure |
|---|---|---|---|---|---|---|---|
| `X/references/` | `deep/f.md` | F | P | F | P | P | `X/references/deep/f.md` |
| `X/` | `references/deep/f.md` | F | P | F | P | P | `X/references/deep/f.md` |
| `X/references/vendored/` | `inner.md` | F | P | F | P | P | `X/references/vendored/` and `X/references/vendored/inner.md` |

- Plain `git rm -r -f <gitlink>` refused in all three cases with
  `fatal: could not lookup name for submodule '<path>'`. "Removed by commit" is therefore
  `git rm --cached <path>`, the folder moved out of the clone, then a commit. The gitlink
  columns come from a second run after the first run's `git rm` failed; the first run's
  three "removed by commit" rows only showed the folder moved away and are not used.
- A repository at `X/references/` with no commit yet, holding `deep/f.md`: F, names
  `X/references/deep/f.md`.

Committed gitlink, seen from a new `git clone` of that commit (no content fetched, folder
has 0 entries, mode 160000):

| Gitlink at | Result | Path named |
|---|---|---|
| `X/references/` | **P** | none |
| `X/` | **P** | none |
| `X/references/vendored/` | F | `X/references/vendored/` only |

Ignored names and links:

| Case | Result | Path named |
|---|---|---|
| uncommitted `CR/node_modules/f.txt` | **P** | none |
| uncommitted `CR/__pycache__/f.txt` | **P** | none |
| uncommitted `CR/.venv/f.txt` | **P** | none |
| uncommitted `CR/.pytest_cache/f.txt` | **P** | none |
| uncommitted `CR/sub/x.pyc` (`.gitignore:3:*.py[cod]`) | **P** | none |
| uncommitted repository at `CR/node_modules/` holding `inner.md` | **P** | none |
| `CR/node_modules/f.txt` force-staged with `git add -f` | F | that path |
| same, committed | F | that path |
| symlink `CR/link-to-folder` to a folder holding `f.md`, uncommitted (`f.md` readable through the link) | **P** | none |
| same symlink, committed (mode 120000) | **P** | none |

Ignored file inside a nested repository:

| Case | Result | Path named |
|---|---|---|
| repository at `X/references/` with `deep/f.md` and `__pycache__/x.pyc` | F | `X/references/__pycache__/x.pyc`, `X/references/deep/f.md` |
| flat repository at `X/references/` (`flat.md`), `__pycache__/x.pyc` ignored by both inner and outer rules, inner `git status` empty | **F** | `X/references/__pycache__/x.pyc` |
| same, cache moved away | P | none |
| flat repository at `X/` (`SKILL.md`, `references/flat.md`, `scripts/a.py`) with ignored `scripts/__pycache__/a.pyc` | **F** | `X/scripts/__pycache__/a.pyc` |
| repository at `X/references/vendored/` with `inner.md` and `__pycache__/x.pyc` | F | the folder, `inner.md` and `__pycache__/x.pyc` |
| flat repository at `X/references/` with `cache/c.bin` ignored only by the inner `.gitignore` | **F** | `X/references/cache/c.bin` |

- Why the limits exist:
  - Ignored paths: `tests/test_skill_folder_flatness.py:69-70` uses
    `git ls-files --cached --others --exclude-standard`; the accepted limit is stated at
    `tests/test_skill_folder_flatness.py:10-12`.
  - Folder symlinks: `tests/test_skill_folder_flatness.py:78` does not treat a link as a
    folder; the accepted limit is stated at lines 10-12.
  - Unfetched gitlinks and content moved off disk: `tests/test_skill_folder_flatness.py:77`
    keeps only listed paths still on disk and `:45-59` walks the disk. A gitlink at
    `X/references/` or `X/` lists a path too short to match, and its empty folder has no
    files. This limit is not named in the file's docstring.
  - Ignored files inside a nested repository: `files_beneath` (`:45-59`) walks the disk and
    applies no ignore rule.
- Verdict basis: `partly`. "Any nested folder, committed or not" does not hold for the
  bold `P` rows, and the bold `F` rows show the ignored-path limit does not extend into
  nested repositories.

## 2. `AGENTS.md` 不再提及不在這個 repo 的 plugin，也不再指向不存在的檔案或測試。

- How I tried it: read `.claude-plugin/marketplace.json`; searched `AGENTS.md` for
  `domain-teams|investing|monkey|research-toolkit|obsidian|tsundoku|dbt|skill-dev|think-orbit|ascii-graph|redshift|briefing|toolkit|concept-model`;
  checked every backticked path-like token on disk, expanding `<placeholder>` as a glob;
  checked the named pytest node id is defined.
- What came back: marketplace is `loom-workflow`, `loom-code`, `loom-design`; the name
  search has no match (grep exit 1). All concrete paths resolve, including
  `tests/test_skill_folder_flatness.py`, `.claude/hooks/validate-skill-folder-structure.sh`,
  `loom-code/tests/test_module_criteria_text.py`, `scripts/run_package_tests.py`,
  `loom-code/scripts/check_contract_citations.py`,
  `loom-code/skills/closing-review/references/lenses.md`, the three pin test files, both
  `docs/loom/memory/` entries and `docs/loom/README.md`.
  `test_current_release_metadata_is_synchronized` is defined at
  `loom-code/tests/test_write_plan_station_text.py:392`.
- Tokens not resolved from the repository root, all non-pointers:
  - `AGENTS.md:7` `references/lenses.md`: the skill-relative example; it resolves inside
    `loom-code/skills/closing-review/` (`AGENTS.md:8`).
  - `AGENTS.md:63` `probes/`, `AGENTS.md:64` `tests/local/`: generic folder names
    (`loom-code/tests/local/` exists).
  - `AGENTS.md:65` `test_*.py`, `*_test.py`, `test-*.sh`; `AGENTS.md:81` `.py`, `.sh`: patterns.
  - `AGENTS.md:65` `scripts/run_package_tests.py --loom-family`: a command; the file exists.
  - `AGENTS.md:22-34` `skills/init/...`: labelled OK / NOT OK layout examples in a code block.

## 3. `AGENTS.md` 對 skill 資料夾檢查、審查鏡頭與人數、版號及 changelog 的描述，都與 repo 現行的檢查和檔案一致。

- Skill folder check (`AGENTS.md:42`): the named test fails as in row 1, and
  `.claude/settings*.json` is absent while `.claude/hooks/validate-skill-folder-structure.sh`
  is executable. Feeding the plugin hook a real nested file:
  `printf '{"tool_input":{"file_path":"<clone>/loom-code/skills/closing-review/references/hook-trial/f.md"}}' | bash loom-workflow/scripts/validate-skill-folder-structure.sh`
  gave exit 0 with no message, matching "no report at write time".
- Mismatch at `AGENTS.md:42`: it names one exception, uncommitted git-ignored paths. Row 1
  also observed passes for folder symlinks and for unfetched gitlinks, and failures for
  ignored files inside nested repositories.
- Review lenses and count (`AGENTS.md:95-100`): `loom-code/skills/closing-review/references/lenses.md`
  exists with Code, Docs, Conformance and question, Skill and Plan sections.
  `python3 loom-code/scripts/loom_checker.py reviewer-count 2026-11-18-skill-folder-check-and-agents-cleanup`
  printed `2`; `loom-code/skills/closing-review/SKILL.md:136` uses the same subcommand.
  `--list-rules` printed 31 lines. 14 files under `loom-*/skills/` carry `<!-- gate: ` markers.
- Versions and changelog (`AGENTS.md:105-112`), all three plugins:

| Plugin | SSOT | Codex | Root manifest | package.json | Newest changelog | Plugin READMEs (en/ja/zh-TW) | Root README hits |
|---|---|---|---|---|---|---|---|
| loom-code | 3.84.0 | 3.84.0 | 3.84.0 | 3.84.0 | `## [3.84.0] — 2026-11-17 — ...` | 1/1/1 | 2 |
| loom-design | 2.26.0 | 2.26.0 | 2.26.0 | 2.26.0 | `## [2.26.0] — 2026-11-16 — ...` | 1/1/1 | 2 |
| loom-workflow | 5.26.0 | 5.26.0 | 5.26.0 | 5.26.0 | `## [5.26.0] — 2026-11-16 — ...` | 1/1/1 | 2 |

- Behaviour trial in a separate clone: `python3 scripts/sync_codex_manifests.py --all` on
  the untouched clone left `git status` empty. After changing only
  `loom-design/.claude-plugin/plugin.json` to 2.26.1, the same command changed
  `.codex-plugin/plugin.json`, `plugin.json` and `package.json` to 2.26.1. With changelog
  and READMEs left alone, `pytest loom-design/tests/spec/test_capture_intent_contract.py -q`
  gave `1 failed, 27 passed` (`test_loom_design_version_2_17_0_consistent`).
- The older claims searched for (`11 維`, `≥2`, `三份`, `hook 擋`, `會被 ... 擋下`) are gone
  (grep exit 1).
- Verdict basis: `partly`, for the `AGENTS.md:42` mismatch only; lenses, count, versions and
  changelog match.

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
    `test_adversary_protocol.py`, `test_write_plan_station_text.py`: `230 passed`.
  - `pytest loom-design/tests/spec/test_capture_intent_contract.py -q`: `28 passed`.
  - `pytest loom-workflow/tests/scripts/test_release_metadata.py -q`: `15 passed`.
  - Total 273 passed.
- Repository checks: `loom-code/scripts/check_contract_citations.py` printed
  `OK: 1 known-violating files unchanged, no new contract citations of this repo's records.`;
  `loom-code/scripts/check-skill-crossrefs.py` printed `OK: all relative skill cross-references resolve.`
- Full suite: not run here. It is cited as the check `finalize-review` executes, with the
  command at the top of this file.

## Re-run on 2026-11-18, at 23682b64c

This run replaces the earlier one at a342d82d9; the functional content changed since then.

- 1: re-tested — every case in section 1, including nested repositories, ignored names,
  folder symlinks and unfetched gitlinks.
- 2: re-tested — marketplace, name search, path tokens and node id in a clean clone.
- 3: re-tested — hook trial, lenses, reviewer count, versions, sync and bump trial, plus
  the `AGENTS.md:42` wording against section 1.
- 4: re-tested — MUST rules, covering tests and repository checks in a clean clone.
