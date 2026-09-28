# Prose-pin stock cleanup, batch 3, and deferred release bump — acceptance test evidence

Re-run on 2026-09-29 after the closing-review round-1 fixes, in a clean copy of the project at 767d97e6 (`git worktree add --detach <scratchpad>/at-head 767d97e6`), with clean copies of the base 5704cc23 (`<scratchpad>/at-base`) and of the first-run commit 6368d950 (`<scratchpad>/at-prev`) for before/after numbers. All three worktrees were removed afterwards.

Earlier run: this file and the report at commit 6368d950 (tested at c81ad8fc). Fix range checked: `6368d950..767d97e6` — 0dc2bbf7 (census-report exec-row count), 84e0a1a5 (plan W4), 2fdd740f (W4-02: 16 test renames), a933120c (W4-01: mapping re-verification, `VERSION_STEP` pin pruned from `tests/test_loom_plugin_install_layout.py`, census headline, loom-design CHANGELOG), 767d97e6 (evidence cites new names; one more rename, `test_sibling_lookup_allows_version_subdirectory` → `test_lookup_table_lives_in_one_place_and_every_skill_links_it`). 26 files changed: 17 test files (renames, docstrings, one pruned assert), 8 evidence/plan files, `loom-design/CHANGELOG.md`. Every row could be affected, so all six were re-tested in full; none is carried over.

Pytest form used throughout: `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest <paths> -q -p no:cacheprovider`. Exit codes were taken from the command itself (zsh `${pipestatus[1]}`), never from a trailing pipe.

## Setup — the README's own instructions

- How I tried it: README "Development" section, from the HEAD worktree root:
  - `python3 scripts/sync_codex_manifests.py --check --all` → exit 0
  - `python3 scripts/check_plugin_boundaries.py loom-code` → `OK: loom-code is filesystem-boundary clean.` exit 0
  - `python3 scripts/check_plugin_boundaries.py loom-design` → `OK: loom-design is filesystem-boundary clean.` exit 0
  - `python3 loom-code/scripts/check-skill-crossrefs.py` → `OK: all relative skill cross-references resolve.` exit 0
- The README's complete suite command is `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`. I did not run it (finalize-review runs it and refuses the attestation on failure); see row 2.
- Scope: outside test roots and `docs/loom/`, `5704cc23..HEAD` still changes only the 3×3 manifests, 3 CHANGELOGs, root `README.md` and the 9 plugin READMEs. No skill, agent or reference prose file changed.

## 1. 擴大後的普查腳本在乾淨副本中重算，回報逐字比對 skill／reference 句子的測試檔為零（已知 7 個檔與新找到的檔都算），除非報告中逐檔寫明理由；比對 checker／CLI 輸出的斷言不被算成散文比對。

- How I tried it:
  - HEAD census: `python3 docs/loom/2026-09-27-prose-pin-stock-cleanup/evidence/probes/classify-test-files.py` from the HEAD worktree root; same from the 6368d950 worktree; `diff` of the two `has_pins=yes` file lists.
  - Widening check: the classifier resolves its repo from `Path(__file__).resolve().parents[5]`, so I copied HEAD's classifier into the base worktree (scratch only, original restored from a copy) and ran it there.
  - `grep -rn "VERSION_STEP\|if its parent directory is named"` over the four test roots.
  - Classifier's own tests and the graduated adversary program.
- What came back:
  - HEAD census, exit 0: `counts: {'behavior': 109, 'gate-eval': 0, 'grammar-invariant': 2, 'not-prose': 54, 'other': 0, 'sentence-pin': 0, 'structure': 66}`, 23 `has_pins=yes`, 0 of them without `reason=` — identical to `census-report.md` §A1 headline and to the 6368d950 run (the flagged-file lists `diff` empty).
  - Base tree with the widened detector, exit 0: `counts: {'behavior': 108, 'gate-eval': 1, 'grammar-invariant': 2, 'not-prose': 54, 'other': 0, 'sentence-pin': 9, 'structure': 56}`, 40 `has_pins=yes`. All 7 known files are `has_pins=yes` there (`loom-memory/test_skill_contract.py`, `decision-map/test_skill_doc.py`, `loom-visualization/test_references.py`, `test_handoff_schema.py`, `test_goal_shape.py`, `test_architecture_doc_consumers.py`, `test_loom_skill_description_catalog.py`); `loom-code/tests/test_github_rules.py` (output-comparing) is `not-prose`, no pin flag.
  - Base-vs-HEAD flagged lists: 18 files flagged at base only; the only HEAD-only file is `loom-code/tests/test_adversarial_batch3_census_misses.py` (its hit is a synthetic source string fed to the classifier, explained in `census-report.md` §A1).
  - `VERSION_STEP` grep: no hit. The W4-01 residual pin is gone.
  - `test_classify_test_files.py`: `15 passed`, exit 0. `loom-code/tests/test_adversarial_batch3_census_misses.py`: `2 passed`, exit 0.
- Evidence: census output above; `census-report.md` §A1 and "Known limits" (the detector does not see two-word phrases, `.index()` lookups, sentence regexes, or literals inside local `*errors*`/`validate`/`check` helpers).

## 2. 被清理的檔裡的行為、結構與文法檢查仍在，清理後完整 package suite 全綠。

- How I tried it:
  - Changed test files: `git diff --name-only --diff-filter=AMR 5704cc23..HEAD -- loom-code/tests loom-workflow/tests loom-design/tests tests` → 26 files, the same list as the first run; `--diff-filter=D` → none.
  - Ran them in two invocations: 13 non-workflow files (8 loom-code, 3 loom-design, 2 root), then 13 loom-workflow files. (The first run's evidence said 12 and 14 for the same 26 files; the split was miscounted, the totals were not.)
  - Renames: `git diff 6368d950..767d97e6 -- '*.py'` → 17 `-def test_` / 17 `+def test_` lines. Grepped every old name across the tree (outside `.git`), and grepped old names against the 6368d950 exec list and new names against the HEAD exec list.
- What came back:
  - non-workflow 13 files: `189 passed`, exit 0.
  - loom-workflow 13 files: `188 passed, 1 warning`, exit 0.
  - Total 377, same as the first run: renames and the `VERSION_STEP` assert removal changed no test count.
  - Old names still appear only as history: `deletion-list.md` "(was `<old>`)" annotations and batch-2 evidence. None appears in `docs/loom/evidence/mechanisms.yaml`, `AGENTS.md` or `loom-code/tests/test_module_criteria_text.py`.
  - Exec lists: 0 old names on the 6368d950 list, 0 new names on the HEAD list — no renamed function runs a program.
- Suite command (not run here): `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`. finalize-review executes it and refuses the attestation when it fails.
- Evidence: the pytest results above.

## 3. 每個被移除的比對，其防守的缺陷類別對應到一個具名替代，對應表存於變更 evidence；acceptance testing 抽查可驗證該替代存在。

- How I tried it:
  - Extracted `stitch_mappings.py` verbatim from the `<details>` block in `census-report.md` §A3 (lines 125–250) into the scratchpad and ran it from the HEAD worktree root: `python3 stitch_mappings.py <scratch>/stitched.md <scratch>/exec-base.txt`.
  - Listed every `kept structural test` and `checker rule id` row of the stitched table (16 + 2) and compared them with the W4-01 verdict table in `mapping-residual.md`.
  - Ran 11 named replacements by node id; checked both rule ids in `loom_checker.py --list-rules`.
  - Negative probe: in the scratch worktree, replaced every "code block" (10, case-insensitive) in `loom-workflow/skills/distill-sessions/agents/prompt-advisory-analyst.md` with "fenced snippet", ran `test_prompts_parseable.py::test_advisory_prompt_structure`, then restored the file from a copy (`git status --short` empty).
- What came back:
  - Script, exit 0: `rows: 68` / `by kind: {'review lens dimension': 50, 'kept structural test': 16, 'checker rule id': 2}` / `deleted defs in changed test files: 44 (test functions: 42 )` / `deleted test functions on the base exec list: 0 []` / `deletion-list rows tagged exec: 2 ; of them deleted at HEAD: 0` / `problems: 0`.
  - W4-01 verdict table: 11 rows `overclaim; relabelled`, 6 `partial`, the rest `guards` — matches the plan summary and the 50/16/2 split.
  - Spot-check pytest, `11 passed, 1 warning`, exit 0:
    - `loom-workflow/tests/loom-visualization/test_references.py::test_rule_one_without_exception_fails`
    - `loom-workflow/tests/loom-visualization/test_references.py::test_conversation_reply_routes_to_general_only`
    - `loom-workflow/tests/loom-visualization/test_references.py::test_rule_five_example_is_a_table`
    - `loom-workflow/tests/distill-sessions/test_prompts_parseable.py::test_advisory_prompt_structure`
    - `loom-workflow/tests/decision-map/test_start_delivery.py::test_refuses_a_second_criterion_reusing_one_intent`
    - `loom-workflow/tests/decision-map/test_start_delivery.py::test_reuse_is_idempotent`
    - `loom-workflow/tests/decision-map/test_start_delivery.py::test_writes_no_brief_and_no_ticket_binding`
    - `loom-workflow/tests/scripts/test_visualization_card_hook.py::test_enabled_toolkit_prints_coexist_card`
    - `loom-workflow/tests/loom-memory/test_skill_contract.py::test_record_section_matches_the_digest_the_cold_reader_eval_was_run_against`
    - `tests/test_loom_plugin_install_layout.py::test_sibling_lookup_resolves_flat_and_versioned_installs`
    - `tests/test_loom_plugin_install_layout.py::test_lookup_table_lives_in_one_place_and_every_skill_links_it`
  - `--list-rules` contains `standing.warn` and `intake.test-case-pair`.
  - Negative probe: `AssertionError: prompt-advisory-analyst.md: body must document code-block wrapping rule` (`test_prompts_parseable.py:267`), `1 failed`, exit 1 — the kept test does guard the row it is credited with (`mapping-residual.md:52`).
  - 50 of 68 rows (74%) name a review lens dimension, not an executable check. Three replacements I ran in the first run (`test_dispatch_profile_resolver.py::test_host_rejection_is_not_capability_quality_escalation`, `::test_cli_is_deterministic_json_and_rejects_malformed_input`, `test_privacy_scan.py::test_planted_aws_key_exits_3_with_finding`) and `test_sibling_lookup_resolves_flat_and_versioned_installs` are among the relabelled rows: they exist and pass, but W4-01 found they do not guard the defect the row names.
- First-run nit (`census-report.md` §A5 said one `exec` row): fixed in 0dc2bbf7; §A5 now names both rows.
- Nit found: `census-report.md` §A3 prints the script output as `deleted defs in changed test files: 43 (test functions: 41 )` and says it ran "again unchanged after that follow-up", and that "W4-02 renamed 16 pruned test functions". At 767d97e6 the same script prints `44 (test functions: 42 )`, because 767d97e6 itself renamed a 17th function. The conclusion lines (`problems: 0`, 0 on the exec list) are unaffected; only the printed count and the rename count are one short.
- Evidence: script output above; `mapping-*.md`; `mapping-residual.md` "W4-01"; `census-report.md` §A3.

## 4. 若有 gate 以被移除的比對作為執行證據，`docs/loom/evidence/mechanisms.yaml` 改指向存在的替代，機制普查檢查通過。

- How I tried it:
  - `python3 loom-code/scripts/check_mechanisms.py` in the HEAD worktree.
  - `git diff --stat 5704cc23..HEAD` and `git diff 6368d950..HEAD` on `docs/loom/evidence/mechanisms.yaml`.
  - Grepped `mechanisms.yaml` for the 17 old and 17 new test names, and listed the evals pointing into changed files.
  - Read the `6368d950..HEAD` diff of `mapping-evals.md`.
- What came back:
  - HEAD: exit 0, `net mechanism count (excl. host-hygiene): 142`, `all clear`. Base (first run): 142, all clear. Count unchanged.
  - `mechanisms.yaml`: one line changed since base (the `decision-map` eval at L89, now `loom-workflow/tests/decision-map/test_start_delivery.py::test_creates_intent_and_lists_it_under_the_criterion`); 0 lines changed in the fix range.
  - 0 old names and 0 new names in `mechanisms.yaml`. Evals into changed files: L50/53/56/110 (`test_loom_skill_description_catalog.py`, whole file), L113 (`test_skill_contract.py`, whole file), L219 (`test_visualization_card_hook.py`, whole file), L354, L357 (`test_templates.py` single functions, not renamed), L89 above.
  - `mapping-evals.md` fix-range diff: only the two renamed function names in the L50/53/56 and L219 notes were updated.
- Evidence: check output above; `mapping-evals.md`.

## 5. 清理前後，「會執行程式（subprocess／checker 呼叫）」的測試函式數量不減少，重算可證。

- How I tried it: from the HEAD worktree, `python3 docs/loom/2026-09-27-prose-pin-stock-cleanup/evidence/probes/classify-test-files.py --count-exec <wt> --list` for `<at-base>`, `<at-prev>` and `<at-head>`, then `diff` of the sorted `::` lines.
- What came back:
  - base `1925`, 6368d950 `1927`, HEAD `1927`.
  - base vs HEAD `diff`: only two added lines, `loom-code/tests/test_adversarial_batch3_census_misses.py::test_census_yaml_frontmatter_helper_flags_pin` and `::test_residual_pins_named_files_absent_or_overridden`; zero removed.
  - 6368d950 vs HEAD `diff`: exit 0, identical. The 17 renames touched no executing function (none of the old or new names is on either list, row 2), so the renames cannot hide a removal behind a rename.
- Evidence: counts and diffs above.

## 6. 三個 plugin 的版號各升一個 patch，三份 manifest、CHANGELOG、README 與版號 pin 測試一致，版號一致性測試通過。

- How I tried it:
  - Read `version` from each of the 9 manifests at HEAD; first `## [` heading of each CHANGELOG; grep of root and plugin READMEs for old and new version strings.
  - Checked the reworded loom-design 2.6.1 entry: found the commit that introduced 2.6.0 (`git log -S'"version": "2.6.0"' -- loom-design/plugin.json`, oldest hit 42291a2e) and listed `loom-design` files changed since, excluding manifests, READMEs and CHANGELOG.
  - `pytest loom-code/tests/test_write_plan_station_text.py loom-design/tests/spec/test_capture_intent_contract.py loom-workflow/tests/scripts/test_release_metadata.py -k "release or version or metadata"`.
  - Negative probe: set `loom-workflow/.codex-plugin/plugin.json` version to `5.5.1` in the scratch worktree, ran `test_release_metadata.py`, restored from a copy (`git status --short` empty).
- What came back:
  - loom-code 3.22.2, loom-design 2.6.1, loom-workflow 5.5.2, identical across `plugin.json`, `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json` (base: 3.22.1, 2.6.0, 5.5.1).
  - CHANGELOG heads: `## [3.22.2] — 2026-09-29 — Prose-pin stock cleanup batches 2-3 and deferred release bump.`, `## [2.6.1] — 2026-09-29 — deferred release bump, version sync only`, `## [5.5.2] — 2026-09-29 — Prose-pin stock cleanup batches 2-3 and deferred release bump.`
  - loom-design 2.6.1 body now reads "batches 2-3 pruned sentence pins from loom-design tests only; no skill or reference content changed." True: since 42291a2e only five files under `loom-design/tests/` changed.
  - READMEs: 0 occurrences of the old versions; new versions in root `README.md` (lines 16–18, 117, 132, 150) and once in each of the 9 plugin READMEs.
  - Version tests: `17 passed, 42 deselected`, exit 0.
  - Negative probe: `FAILED loom-workflow/tests/scripts/test_release_metadata.py::test_manifest_version_is_current[.codex-plugin/plugin.json]`, `1 failed, 8 passed`, exit 1.
- Not verified here: that an installed copy actually receives the update through `claude plugin update`; that needs the change merged and published, which happens after this report.
- Evidence: outputs above.
