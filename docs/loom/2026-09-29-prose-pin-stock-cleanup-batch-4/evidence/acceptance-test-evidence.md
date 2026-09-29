# Prose-pin stock cleanup, batch 4: short phrases and hidden pins — acceptance test evidence

Tried on 2026-09-29, in a clean copy of the project at 9610d714 (`git worktree add --detach <scratchpad>/at-head 9610d714`), with a clean copy of the branch base 1ef82fe8 (`<scratchpad>/at-base`) for before/after numbers. Both worktrees were removed afterwards; `git status --short` was empty in both before removal. All scratch edits (probe file, mutations) were made in the HEAD or base worktree only and reverted from copies.

Sections 1-6 below are the first run. The re-run after the closing-review round-1 fix (a2812336..5eadcf74) is the dated section at the end; where the two disagree, the re-run's numbers are current.

Pytest form used throughout: `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest -q -p no:cacheprovider [--import-mode=importlib] <paths>`. Exit codes were taken from the command itself, never through a trailing pipe.

## Setup — the README's own instructions

- How I tried it: README "Development" section, from the HEAD worktree root:
  - `python3 scripts/sync_codex_manifests.py --check --all` → exit 0
  - `python3 scripts/check_plugin_boundaries.py loom-code` → `OK: loom-code is filesystem-boundary clean.` exit 0
  - `python3 scripts/check_plugin_boundaries.py loom-design` → `OK: loom-design is filesystem-boundary clean.` exit 0
  - `python3 loom-code/scripts/check-skill-crossrefs.py` → `OK: all relative skill cross-references resolve.` exit 0
- The README's complete suite command is `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`. I did not run it (finalize-review runs it and refuses the attestation on failure); see row 2.
- Scope (intent Constraint "only tests, evidence, mechanisms eval pointers, census script and version files"): `git diff --stat 1ef82fe8..HEAD -- . ':!docs/loom' ':!*/tests/*' ':!tests/*'` lists only the 3×3 manifests, 3 CHANGELOGs, root `README.md` and the 9 plugin READMEs (22 files, 44+/24-). No skill, agent or reference prose file changed.
- No new checker rule: `diff` of `loom_checker.py --list-rules` at base and HEAD is empty (26 rules).

## 1. 普查在乾淨副本中重算，涵蓋第三批看不到的寫法（兩個字的短語、檢查小工具內的字串、位置查找與正規表示式比對），回報比對 skill／reference 散文的測試檔為零，除非報告中逐檔寫明理由；比對 checker／CLI 輸出的斷言不被算成散文比對。

- How I tried it:
  - HEAD census: `python3 docs/loom/2026-09-27-prose-pin-stock-cleanup/evidence/probes/classify-test-files.py` and the same with `--candidates`, from the HEAD worktree root.
  - Decision coverage: extracted `decide.py` verbatim from `census-report.md` `<details>` into the scratchpad and ran `python3 decide.py <cand-head.txt> <out>` from the HEAD worktree root.
  - Widening check: copied HEAD's classifier over the base worktree's copy (the script resolves its repo from its own path), ran census and `--candidates` there, restored the base file from a copy, and ran the base's own (batch-3) classifier for comparison.
  - Blind probe of my own: in the HEAD worktree I planted `loom-workflow/tests/recap-state/test_zz_probe.py` reading `skills/recap-state/SKILL.md`, with one of each batch-3-invisible form — a two-word literal (`"short recap" in text`), a `.index("where we are")` lookup, a `re.search(r"recap the session", text)`, a local helper `_check_errors` holding `"plain words"` — plus a test asserting `"all clear"` in `subprocess.run(...).stdout`. Ran census and `--candidates`, then a second variant without the subprocess test. The probe file was moved out afterwards.
  - Classifier tests and the graduated adversary programs: `pytest docs/loom/2026-09-27-prose-pin-stock-cleanup/evidence/probes/test_classify_test_files.py loom-code/tests/test_adversarial_batch3_census_misses.py loom-code/tests/test_adversarial_batch4_census_lookup_forms.py`.
- What came back:
  - HEAD census, exit 0: `counts: {'behavior': 110, 'gate-eval': 0, 'grammar-invariant': 2, 'not-prose': 54, 'other': 0, 'sentence-pin': 0, 'structure': 66}`; 34 files `has_pins=yes`, 0 of them without `reason=`. Identical to `census-report.md` §A1 headline.
  - HEAD `--candidates`, exit 0: prose 106 / structural 622 / kept-batch3 3, 22 files with a prose row — identical to §A1 candidates table. `decide.py`: `prose rows: 106; undecided: 0`, exit 0. None of the 106 is a prune; each points to a Decisions row that keeps it (headings, labels, field keys, table cells, proper names, absence or one-home scans, kept gates). I read a sample: `test_goal_shape.py:76/111` (vendor names and field names in paragraphs picked by heading/bold label), `test_knowledge_triage.py:103-114` (tier names, lens name), `test_references.py:536` (concept terms like `width budget`, `bullet lines` required in node-structure.md), `test_visualization_card_hook.py:296` (the kept batch-3 `rule_polarity_errors` gate). Reasons match the code.
  - Base tree with the widened classifier, exit 0: `counts: {'behavior': 109, 'gate-eval': 3, 'grammar-invariant': 2, 'not-prose': 54, 'other': 0, 'sentence-pin': 8, 'structure': 55}`, 49 `has_pins=yes`; `--candidates`: prose 611 / structural 644 / kept-batch3 3, 39 files with a prose row. Base tree with its own batch-3 classifier: `sentence-pin: 0` — the widening is what makes the 8 files and 611 rows visible.
  - Blind probe, variant with subprocess test: `--candidates` listed all four planted forms as `prose` (`'plain words' (if requires)` in `_check_errors`, `'short recap' (assert in)`, `'where we are' (.index())`, `'recap the session' (re.search)`); the `"all clear"` output assert was not listed. Census exit 0, file classed `behavior` with `has_pins=yes` and no override row; headline `sentence-pin` stayed 0.
  - Blind probe, prose-only variant: census exit 0, file classed `sentence-pin`, headline `sentence-pin: 1`.
  - Classifier tests + adversary programs: `30 passed`, exit 0. Test names include `test_two_word_literal_against_skill_text_flagged`, `test_short_literal_in_checker_output_not_flagged`, `test_helper_fed_prose_and_index_and_regex_flagged`, `test_find_in_output_not_flagged`, `test_needles_against_script_output_not_flagged`.
- Nit found: a file that also runs a program (auto class `behavior`) and has a new unexplained prose pin shows `has_pins=yes` without `reason=` but does not move the headline `sentence-pin` count and does not fail the census (exit 0; only `other` exits 1). The "zero unless a reason is written" claim for such files rests on reading the `has_pins=yes` column, which I did (34/34 with a reason), not on the exit code.
- Evidence: outputs above; `census-report.md` §A1 and "Known limits" (two-level helper passing, subscripts, non-literal regexes, synthetic-only forms such as `.count`, `.partition`, `frozenset`, concatenation, `argvalues=` are still not seen).

## 2. 被清理的檔裡的行為、結構與文法檢查仍在，清理後完整 package suite 全綠。

- How I tried it:
  - Changed test files: `git diff --name-only --diff-filter=AMR 1ef82fe8..HEAD -- loom-code/tests loom-workflow/tests loom-design/tests tests` → 34 files; `--diff-filter=D` → none (no test file deleted).
  - Ran them in two invocations: 11 non-workflow files (5 loom-code, 5 loom-design, 1 root), then 23 loom-workflow files.
  - AST scan of every test function in the 34 files at HEAD for an assertion signal.
- What came back:
  - Non-workflow 11 files: `150 passed`, exit 0.
  - loom-workflow 23 files, default import mode: exit 2, `import file mismatch` collecting `loom-workflow/tests/distill-sessions` (basename collision `test_readmes.py`/`test_skill_md.py` across directories when many dirs are passed at once — the known environment trap). Rerun with `--import-mode=importlib`: `183 passed, 1 warning`, exit 0.
  - Total 333 passed, 0 failed.
  - Test functions in the 34 files: base 308, HEAD 269 (64 removed or renamed, see row 3). Two HEAD functions have no direct `assert` (`test_design_md_schema_keys.py::test_elevation_disambiguation_tolerates_meaning_preserving_reword`, `::test_shapes_documents_rounded_bullet`); both assert through helpers (`_bullet_line` asserts the bullet exists; the other calls the production check and must not raise). No empty test left.
- Suite command (not run here): `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`. finalize-review executes it and refuses the attestation when it fails. `census-report.md` "Package suite" records the author's run at W3-01: EXIT=0, 3213 passed — the author's word, not my result.
- Evidence: pytest results above.

## 3. 每個被移除的比對，其防守的缺陷類別對應到一個具名替代，對應表存於變更 evidence；acceptance testing 抽查可驗證該替代存在。

- How I tried it:
  - Extracted `stitch4.py` verbatim from `census-report.md` into the scratchpad; ran `python3 stitch4.py <exec-base.txt> <exec-head.txt>` from the HEAD worktree root (exec lists from row 5).
  - Coverage check of my own: for every test function present at base and absent at HEAD in the 34 changed files, grep its name across the six `mapping-*.md` files.
  - Listed every `kept structural test`, `checker rule id` and `review-only` row and ran 10 named replacements by node id; checked `standing.warn` in `loom_checker.py --list-rules`.
  - Negative probe: in the HEAD worktree, replaced both `design-conformance` in `loom-design/skills/design-system/references/knowledge-triage.md` with `design review`, ran `test_knowledge_triage.py::test_shaping_route_names_the_design_conformance_lens`, restored from a copy.
  - Reword-tolerance probe: replaced `advisory` (1 hit, case-insensitive) with `non-binding` in `loom-workflow/skills/goal-create/references/goal-shape.md`; ran HEAD's `test_goal_shape.py`, and the base version of the same test file (copied in as a temp file); restored both.
- What came back:
  - `stitch4.py`, exit 0: `rows: 72` / `by kind: {'kept structural test': 28, 'review lens dimension': 41, 'checker rule id': 1, 'review-only': 2}` / `replacement defs cited and resolved: 43` / `deleted defs in changed test files: 81 (test functions: 64 )` / `deleted test functions on the base exec list: []` / `problems: 0` — matches `census-report.md`.
  - Coverage: `deleted/renamed test functions: 64 not named in any mapping file: 0`.
  - Spot-check pytest, `10 passed`, exit 0:
    - `tests/test_loom_skill_description_catalog.py::test_router_tables_preserve_direct_leaf_targets`
    - `loom-code/tests/test_write_plan_station_text.py::test_suggest_station_names_every_policy_input_key`
    - `loom-design/tests/interface/test_design_md_schema_keys.py::test_shapes_documents_rounded_bullet`
    - `loom-design/tests/interface/test_design_system_skill.py::test_gate_marker_registered`
    - `loom-design/tests/interface/test_knowledge_triage.py::test_shaping_route_names_the_design_conformance_lens`
    - `loom-workflow/tests/goal-create/test_goal_shape.py::test_defines_four_fields_and_budget`
    - `loom-workflow/tests/loom-memory/test_skill_contract.py::test_no_fixed_station_mandatory_invocation`
    - `loom-workflow/tests/distill-sessions/test_prompts_parseable.py::test_advisory_prompt_declares_skill_dir_input`
    - `loom-workflow/tests/scripts/test_handoff_compaction.py::test_entrypoint_structure_and_schema_before_artifact_steps`
    - `loom-workflow/tests/recap-state/test_skill_md.py::TestFrontmatterAndRouting::test_b_multilingual_triggers`
  - `--list-rules` contains `standing.warn`.
  - Negative probe: `AssertionError: must name the design-conformance lens that renders the verdict`, `1 failed`, exit 1 — the kept test guards the row credited to it (`mapping-design.md`, knowledge-triage SHAPING row).
  - Reword probe: HEAD `test_goal_shape.py` `3 passed`, exit 0; base version `1 failed, 2 passed`, exit 1 — the pruned `advisory` pin no longer reddens on a reword.
  - 43 of 72 rows (41 review lens dimension + 2 review-only, 60%) name review, not an executable check.
- Evidence: outputs above; `mapping-*.md`; `census-report.md` "Mapping files, stitched".

## 4. 若有 gate 以被移除的比對作為執行證據，`docs/loom/evidence/mechanisms.yaml` 改指向存在的替代，機制普查檢查通過。

- How I tried it:
  - `python3 loom-code/scripts/check_mechanisms.py` in the HEAD and base worktrees.
  - `git diff --stat 1ef82fe8..HEAD -- docs/loom/evidence/mechanisms.yaml`.
  - Listed every `mechanisms.yaml` eval pointing into one of the 34 changed test files; counted `def test` in each at base and HEAD; ran the two single-function evals.
- What came back:
  - HEAD: exit 0, `net mechanism count (excl. host-hygiene): 142`, `all clear`. Base: exit 0, 142, `all clear`.
  - `mechanisms.yaml` diff: empty (no eval moved).
  - Evals into changed files: L50/53/56/110 `tests/test_loom_skill_description_catalog.py` (whole file, 7→7 tests), L86 `test_architecture_skill.py` (11→8), L92 `test_handoff_compaction.py` (2→2), L95 `test_recap_state_compaction.py` (2→1), L98 `test_loom_visualization_compaction.py` (3→3), L104 `test_git_memory_compaction.py` (2→2), L107 `test_independent_advisor_compaction.py` (8→3), L113 `loom-memory/test_skill_contract.py` (12→11), L219 `test_visualization_card_hook.py` (43→29), L354/L357 `test_templates.py::test_skill_declines_vault_target` and `::test_mermaid_gate_paragraph_present_requires_confirmed_host` (both still defined, `2 passed`).
  - Every whole-file eval still resolves to a file with tests. None names a deleted function. The skill-class evals (handoff, recap-state, git-memory, independent-advisor) now rest on structural-token, pointer and word-cap checks only; `mapping-compaction.md` Decisions rows 7-20 record which functions went and where their structural tokens moved.
- Evidence: check output above; `mapping-compaction.md`.

## 5. 清理前後，「會執行程式（subprocess／checker 呼叫）」的測試函式數量不減少，重算可證。

- How I tried it: from the scratchpad, `python3 at-head/docs/loom/2026-09-27-prose-pin-stock-cleanup/evidence/probes/classify-test-files.py --count-exec <wt> --list` for the base and HEAD worktrees, `diff` of the sorted `::` lines; cross-checked with the base's own classifier (`--count-exec` on both trees).
- What came back:
  - HEAD classifier: base `1927`, HEAD `1929`. Base classifier: base `1927`, HEAD `1929` (the counting code gives the same result either way).
  - `diff`: two added lines, `loom-code/tests/test_adversarial_batch4_census_lookup_forms.py::test_census_find_presence_lookup_flags_pin` and `::test_census_self_attribute_markdown_flags_pin`; zero removed.
  - `stitch4.py` (row 3): `deleted test functions on the base exec list: []` — none of the 64 removed/renamed test functions executed a program, so no rename hides a removal.
- Evidence: counts and diff above.

## 6. 三個 plugin 的版號各升一個 patch，三份 manifest、CHANGELOG、README 與版號 pin 測試一致，版號一致性測試通過。

- How I tried it:
  - Read `version` from each of the 9 manifests at HEAD and base; first `## [` heading and body of each CHANGELOG; grep of root and plugin READMEs for old and new version strings.
  - `pytest loom-code/tests/test_write_plan_station_text.py loom-design/tests/spec/test_capture_intent_contract.py loom-workflow/tests/scripts/test_release_metadata.py -k "release or version or metadata"`.
  - Negative probe: set `loom-design/.codex-plugin/plugin.json` version to `2.6.1` in the scratch worktree, reran, restored from a copy.
- What came back:
  - loom-code 3.22.2→3.22.3, loom-design 2.6.1→2.6.2, loom-workflow 5.5.2→5.5.3, identical across `plugin.json`, `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`.
  - CHANGELOG heads: `## [3.22.3] — 2026-09-29 — Prose-pin stock cleanup batch 4 and patch release bump.`, `## [2.6.2] — 2026-09-29 — batch 4 release bump, version sync only`, `## [5.5.3] — 2026-09-29 — Prose-pin stock cleanup batch 4 and patch release bump.`
  - READMEs: 0 occurrences of the old versions; 15 occurrences of the new ones (root `README.md` lines 16-18, 117, 132, 150, and each of the 9 plugin READMEs).
  - `sync_codex_manifests.py --check --all`: exit 0 (setup).
  - Version tests: `17 passed, 42 deselected`, exit 0.
  - Negative probe: `FAILED loom-design/tests/spec/test_capture_intent_contract.py::test_loom_design_version_2_2_0_consistent`, `1 failed, 16 passed`, exit 1.
- Nit found: the loom-design 2.6.2 CHANGELOG body says the batch 4 cleanup "touched `loom-code` and `loom-workflow` only". Not true: `git diff --name-only 1ef82fe8..HEAD -- loom-design` lists four pruned loom-design test files (`test_architecture_skill.py`, `test_design_md_schema_keys.py`, `test_design_system_skill.py`, `test_knowledge_triage.py`; W1-02, 16 mapping rows) plus the version pin test. Its first line ("tests only; no skill or reference content changed") is true.
- Not verified here: that an installed copy actually receives the update through `claude plugin update`; that needs the change merged and published, which happens after this report.
- Evidence: outputs above.

## Re-run on 2026-09-29, at 5eadcf74

Fix range `a2812336..5eadcf74`: `ec7a671e` (CHANGELOG and census-report nits), `aad576b4` (restores the `result:` value-set check in `loom-code/tests/test_acceptance_test_report_shape.py` and the Derivation-contract roster check (e) in `loom-design/tests/interface/test_design_md_schema_keys.py`), `c31c9ee3` (23 mapping rows re-marked `kept structural test` → `review lens dimension`), `8a1556dd` (review nits, incl. a docstring in `test_visualization_card_hook.py`), `5eadcf74` (regenerated `candidate-list.md`). The fix changed three test files, six mapping files, `census-report.md`, `candidate-list.md` and two CHANGELOGs; it did not touch the census script (`git diff --stat a2812336..5eadcf74 -- docs/loom/2026-09-27-prose-pin-stock-cleanup loom-code/scripts docs/loom/evidence/mechanisms.yaml` is empty). Every row was re-tested in full; none is carried over.

Clean worktrees: `git worktree add --detach <scratchpad>/at-head 5eadcf74` and `<scratchpad>/at-base 1ef82fe8`; `git status --short` empty in both before `git worktree remove`. Scratch edits (probe file, mutations) were made in the HEAD worktree and restored from copies. `decide.py` and `stitch4.py` were extracted verbatim from `census-report.md` at 5eadcf74 (lines 189-289 and 297-401).

- Setup: re-tested — README "Development" checks from the HEAD worktree root: `sync_codex_manifests.py --check --all` exit 0; `check_plugin_boundaries.py loom-code` and `loom-design` both `OK ... filesystem-boundary clean.` exit 0; `check-skill-crossrefs.py` `OK: all relative skill cross-references resolve.` exit 0. Scope: `git diff --name-only 1ef82fe8..HEAD -- . ':!docs/loom' ':!*/tests/*' ':!tests/*'` lists only the 9 manifests, 3 CHANGELOGs, root and 9 plugin READMEs (22 files, 45+/24-); no skill, agent or reference prose file. `loom_checker.py --list-rules` identical at base and HEAD (no new rule).
- 1: re-tested — `classify-test-files.py` exit 0, `counts: {'behavior': 110, 'gate-eval': 0, 'grammar-invariant': 2, 'not-prose': 54, 'other': 0, 'sentence-pin': 0, 'structure': 66}`, 34 `has_pins=yes`, 0 without `reason=`. `--candidates` exit 0: prose 106 / structural 625 / kept-batch3 3, 22 files with a prose row (matches `census-report.md` §A1 table: 625 = 622 + the 3 structural rows of the restored checks). `decide.py` → `prose rows: 106; undecided: 0`, exit 0; its output's table rows are identical to the committed `candidate-list.md` rows, pointers included (only the committed file's extra exec-count header table differs). Blind probe re-run with the same planted file in `loom-workflow/tests/recap-state/`: `--candidates` listed `'plain words' (if requires)` in `_check_errors`, `'short recap' (assert in)`, `'where we are' (.index())`, `'recap the session' (re.search)` all as `prose`; the `"all clear"` subprocess-output assert not listed; with the subprocess test the file is `behavior has_pins=yes` and the headline stays `sentence-pin: 0` (exit 0), without it the file is `sentence-pin` and the headline is `sentence-pin: 1`. This first-run nit is now recorded in `census-report.md` "Known limits" ("A behavior file can gain a pin without an override and still exit 0"). Classifier tests + batch-3/batch-4 adversary programs: `30 passed`, exit 0.
- 2: re-tested — 34 changed test files (`--diff-filter=AMR 1ef82fe8..HEAD`; `--diff-filter=D` none). 11 non-workflow files: `150 passed`, exit 0. 23 loom-workflow files with `--import-mode=importlib`: `183 passed, 1 warning`, exit 0. Total 333 passed. Test functions in the 34 files: base 308, HEAD 269 (the fix added assertions to existing functions, no new function). Mutation probes on the two restored checks (HEAD worktree, restored from copies):
  - `loom-code/agents/acceptance-tester.md` `result: works | partly | not verified | fails` → dropped `partly`: `test_acceptance_test_report_shape.py::test_template_has_one_row_per_criterion_and_evidence_file_path` `1 failed`, exit 1, `AssertionError` at line 76 (set mismatch).
  - `loom-design/skills/design-system/references/design-md-schema.md:94` Derivation-contract roster, `Elevation` inserted: `test_design_md_schema_keys.py::test_schema_keys_documented_and_token_groups_named` `1 failed`, exit 1, `AssertionError` at line 296. `/ Shapes` removed: same test `1 failed`, exit 1, line 296.
  - Suite command (not run here): `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`. finalize-review executes it and refuses the attestation when it fails. The orchestrator reported EXIT=0 at 5eadcf74 — its word, not my result.
- 3: re-tested — `stitch4.py <exec-base> <exec-head>` from the HEAD worktree root, exit 0: `rows: 73` / `by kind: {'kept structural test': 7, 'review lens dimension': 64, 'checker rule id': 1, 'review-only': 1}` / `by file: {'mapping-code': 7, 'mapping-design': 16, 'mapping-workflow': 21, 'mapping-workflow-2': 13, 'mapping-compaction': 7, 'mapping-containers': 9}` / `replacement defs cited and resolved: 43` / `deleted defs in changed test files: 81 (test functions: 64 )` / `deleted test functions on the base exec list: []` / `problems: 0` — matches `census-report.md` "Mapping files, stitched". Own coverage check (AST diff of the 34 files, base vs HEAD): 64 removed/renamed test functions, 0 not named in any `mapping-*.md`. All 7 `kept structural test` replacements run by node id, `7 passed`, exit 0:
  - `tests/test_loom_skill_description_catalog.py::test_router_tables_preserve_direct_leaf_targets`
  - `loom-code/tests/test_acceptance_test_report_shape.py::test_template_has_one_row_per_criterion_and_evidence_file_path`
  - `loom-design/tests/interface/test_design_md_schema_keys.py::test_schema_keys_documented_and_token_groups_named`
  - `loom-workflow/tests/recap-state/test_skill_md.py::TestFrontmatterAndRouting::test_b_multilingual_triggers`
  - `loom-workflow/tests/scripts/test_recap_state_compaction.py::test_entrypoint_tokens_and_schema_before_the_ordered_six_section_template`
  - `loom-workflow/tests/scripts/test_handoff_compaction.py::test_entrypoint_structure_and_schema_before_artifact_steps`
  - `loom-workflow/tests/decision-map/test_skill_doc.py::test_v3_public_surface_commands_templates_and_version_are_synchronized`
  - The two restored ones redden on their defect (row 2 probes). `checker rule id` row: `standing.warn` present in `--list-rules`. All 64 `review lens dimension` rows name a lens and dimension (skill/omission 40, docs/omission 8, skill/inconsistency 7, skill/ambiguity 4, docs/inconsistency 3, skill/incorrect-fact 2, docs/incorrect-fact 1, skill/deletion-first 1); each dimension appears in `loom-code/agents/reviewer.md` and `loom-code/skills/closing-review/references/lenses.md`.
  - Share: 65 of 73 rows (64 review lens dimension + 1 review-only, 89%) name review, not an executable check — up from 43 of 72 (60%) at the first run. The first run's figure "72 列裡 43 列" is superseded.
- 4: re-tested — `check_mechanisms.py` HEAD exit 0, `net mechanism count (excl. host-hygiene): 142`, `all clear`; base exit 0, 142. `mechanisms.yaml` diff `1ef82fe8..HEAD`: empty. Of the fix-range test files only `test_visualization_card_hook.py` is an eval (L219, whole file; 29 tests, docstring-only change); the first-run eval list otherwise stands, no eval names a deleted function.
- 5: re-tested — `classify-test-files.py --count-exec <wt> --list` (HEAD classifier): base 1927, HEAD 1929; the base's own classifier gives the same 1927/1929. Sorted `::` diff: two added (`test_adversarial_batch4_census_lookup_forms.py::test_census_find_presence_lookup_flags_pin`, `::test_census_self_attribute_markdown_flags_pin`), zero removed. `stitch4.py`: `deleted test functions on the base exec list: []`.
- 6: re-tested — versions at HEAD: loom-code 3.22.3, loom-design 2.6.2, loom-workflow 5.5.3 in all of `plugin.json`, `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`. CHANGELOG heads: all three `## [X.Y.Z] — 2026-09-29 — Prose-pin stock cleanup batch 4 and patch release bump.` READMEs: 0 old-version strings, 15 new. Version tests (`-k "release or version or metadata"` over the three pin files): `17 passed, 42 deselected`, exit 0; negative probe (`loom-design/.codex-plugin/plugin.json` → `2.6.1`): `FAILED loom-design/tests/spec/test_capture_intent_contract.py::test_loom_design_version_2_2_0_consistent`, `1 failed, 16 passed`, exit 1; restored. First-run nit closed: the loom-design 2.6.2 body now says pins were removed from "four `loom-design` test files", and `git diff --name-only 1ef82fe8..HEAD -- loom-design/tests` lists exactly those four (`test_architecture_skill.py`, `test_design_md_schema_keys.py`, `test_design_system_skill.py`, `test_knowledge_triage.py`) plus the version pin test. loom-code 3.22.3 body's new claim (batch-4 adversary program graduated to `tests/test_adversarial_batch4_census_lookup_forms.py`) checked: the file exists and passed in row 1. Not verified here: `claude plugin update` on an installed copy (needs merge and publish).
