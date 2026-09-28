# Prose-pin stock cleanup, batch 3, and deferred release bump — acceptance test evidence

Tried on 2026-09-29, in a clean copy of the project at c81ad8fc (`git worktree add --detach <scratchpad>/at-head c81ad8fc`), with a second clean copy of the base 5704cc23 (`<scratchpad>/at-base`) for before/after numbers. Both worktrees were removed afterwards. First run; no earlier report.

Pytest form used throughout: `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest <paths> -q -p no:cacheprovider`. Exit codes were taken from the command itself (`$?` or zsh `${pipestatus[1]}`), never from a trailing pipe.

## Setup — the README's own instructions

- How I tried it: README "Development" section, from the HEAD worktree root:
  - `python3 scripts/sync_codex_manifests.py --check --all` → exit 0
  - `python3 scripts/check_plugin_boundaries.py loom-code` → `OK: loom-code is filesystem-boundary clean.` exit 0
  - `python3 scripts/check_plugin_boundaries.py loom-design` → `OK: loom-design is filesystem-boundary clean.` exit 0
  - `python3 loom-code/scripts/check-skill-crossrefs.py` → `OK: all relative skill cross-references resolve.` exit 0
- The README's complete suite command is `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`. I did not run it (finalize-review runs it and refuses the attestation on failure); see row 2.
- Scope of the change (`git diff --name-only 5704cc23..HEAD`, 61 files): outside test roots and `docs/loom/` only the 3×3 manifests, 3 CHANGELOGs, root `README.md` and the 9 plugin READMEs changed. No skill, agent or reference prose file changed (Constraint "不修改任何 production 散文" holds).

## 1. 擴大後的普查腳本在乾淨副本中重算，回報逐字比對 skill／reference 句子的測試檔為零（已知 7 個檔與新找到的檔都算），除非報告中逐檔寫明理由；比對 checker／CLI 輸出的斷言不被算成散文比對。

- How I tried it:
  - HEAD census: `python3 docs/loom/2026-09-27-prose-pin-stock-cleanup/evidence/probes/classify-test-files.py` from the HEAD worktree root.
  - Widening check: the classifier resolves its repo from `Path(__file__).resolve().parents[5]` (`classify-test-files.py:34`), so to scan the base tree with the widened detector I copied HEAD's classifier file into the base worktree (scratch only) and ran it there.
  - Independent residual scan: a crude `grep -E` over all four test roots for `assert "<4+ word literal>" in <name>` excluding obvious output names, then read every hit in prose-facing files; separately listed every 3+-word string literal left in the six known files not deleted wholesale.
  - Classifier's own tests: `pytest docs/loom/2026-09-27-prose-pin-stock-cleanup/evidence/probes/test_classify_test_files.py`.
- What came back:
  - HEAD census, exit 0: `counts: {'behavior': 109, 'gate-eval': 0, 'grammar-invariant': 2, 'not-prose': 54, 'other': 0, 'sentence-pin': 0, 'structure': 66}` — identical to `census-report.md` (W3-01 rerun line).
  - 23 files still print `has_pins=yes`; `grep 'has_pins=yes' | grep -v 'reason='` returns nothing, so every one carries an override reason. 22 are the override table in `census-report.md` §A1; the 23rd, `loom-code/tests/test_adversarial_batch3_census_misses.py`, is explained in the W3-01 paragraph of the same section (its hit is a synthetic source string fed to the classifier).
  - Base tree scanned with the widened detector, exit 0: `counts: {'behavior': 108, 'gate-eval': 1, 'grammar-invariant': 2, 'not-prose': 54, 'other': 0, 'sentence-pin': 9, 'structure': 56}`, 40 `has_pins=yes`. All 7 known files are flagged there (`test_skill_contract.py`, `decision-map/test_skill_doc.py`, `test_references.py`, `test_handoff_schema.py`, `test_goal_shape.py`, `test_architecture_doc_consumers.py`, `test_loom_skill_description_catalog.py` — each `has_pins=yes`). `loom-code/tests/test_github_rules.py`, the plan's example of an output-comparing file, is `not-prose` with no pin flag.
  - 18 files are flagged at base but not at HEAD; each one is named in `deletion-list.md` and in a mapping file (`mapping-known`, `mapping-new-code`, `mapping-new-design`, `mapping-new-workflow` or `mapping-residual`). The only file flagged at HEAD but not at base is the graduated adversary test above.
  - Crude residual scan: positive hits left are validator error strings (`test_references.py` 105–521, e.g. `"missing subsection: In-cell visuals" in in_cell_errors(broken)`), hook output (`test_session_start_words.py:94` `"this is what I want" in context`, where `context = _context(_run(empty_repo))`), CLI stderr (`test_legacy_contract_removed.py:156`), and the overridden table header (`test_templates.py:303`). All other hits are `not in` absence scans. Remaining literals in the known files are headings (`handoff` `REQUIRED_HEADINGS`), operation names and two-word terms (`decision-map/test_skill_doc.py:214-226`, e.g. `"zero-write preview"`), retired-wording absence lists, and assertion messages — below the 3-word threshold or not assertions on prose.
  - Classifier tests: `15 passed`, exit 0.
- Evidence: census output above; `census-report.md` §A1 and "Known limits" (the detector does not see two-word phrases, `.index()` lookups, sentence regexes, or literals inside local `*errors*`/`validate`/`check` helpers — found by reading instead).

## 2. 被清理的檔裡的行為、結構與文法檢查仍在，清理後完整 package suite 全綠。

- How I tried it:
  - Changed test files: `git diff --name-only --diff-filter=AMR 5704cc23..HEAD -- loom-code/tests loom-workflow/tests loom-design/tests tests` → 26 files (no test file deleted wholesale).
  - Ran those 26 files in two pytest invocations (non-workflow, then workflow).
  - Ran the named behavior replacements individually (see row 3).
- What came back:
  - non-workflow 12 files: `189 passed in 4.71s`, exit 0.
  - loom-workflow 14 files: `188 passed, 1 warning in 0.80s`, exit 0 (no `__pycache__` collision in the fresh worktree, so `--import-mode=importlib` was not needed).
  - Deleted defs: `stitch_mappings.py` reports 27 defs deleted across changed test files, 25 of them test functions; none is on the base executing-function list (row 5), so no program-running check was removed.
- Suite command (not run here): `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`. finalize-review executes it and refuses the attestation when it fails.
- Evidence: the two pytest results above.

## 3. 每個被移除的比對，其防守的缺陷類別對應到一個具名替代，對應表存於變更 evidence；acceptance testing 抽查可驗證該替代存在。

- How I tried it:
  - Extracted `stitch_mappings.py` verbatim from the `<details>` block in `census-report.md` §A3 into the scratchpad and ran it from the HEAD worktree root: `python3 stitch_mappings.py <scratch>/stitched.md <scratch>/exec-base.txt` (the base list from row 5).
  - Hand spot-check: ran 8 named replacements by node id, checked each existed at base (`git show 5704cc23:<file> | grep -c "def <name>"`), and checked the three rule ids in `loom_checker.py --list-rules`.
- What came back:
  - `rows: 67` / `by kind: {'review lens dimension': 38, 'kept structural test': 27, 'checker rule id': 2}` / `deleted defs in changed test files: 27 (test functions: 25 )` / `deleted test functions on the base exec list: 0 []` / `deletion-list rows tagged exec: 2 ; of them deleted at HEAD: 0` / `problems: 0`, exit 0 — identical to the report.
  - Spot-check pytest, `8 passed, 1 warning`, exit 0:
    - `loom-code/tests/test_dispatch_profile_resolver.py::test_host_rejection_is_not_capability_quality_escalation`
    - `loom-code/tests/test_dispatch_profile_resolver.py::test_cli_is_deterministic_json_and_rejects_malformed_input`
    - `tests/test_loom_plugin_install_layout.py::test_sibling_lookup_resolves_flat_and_versioned_installs` (builds flat and versioned install trees under `tmp_path`, lines 660–672)
    - `loom-workflow/tests/decision-map/test_start_delivery.py::test_refuses_a_second_criterion_reusing_one_intent`
    - `loom-workflow/tests/decision-map/test_start_delivery.py::test_creates_intent_and_lists_it_under_the_criterion`
    - `loom-workflow/tests/git-memory/test_privacy_scan.py::test_planted_aws_key_exits_3_with_finding`
    - `loom-workflow/tests/loom-visualization/test_references.py::test_rule_five_example_is_a_table`
    - `loom-workflow/tests/loom-memory/test_skill_contract.py::test_record_section_matches_the_digest_the_cold_reader_eval_was_run_against`
  - The four I checked at base all existed at base (count 1 each): the replacements are pre-existing tests, not tests written to fill the table.
  - `--list-rules` contains `standing.warn`, `intake.test-case-pair` and `push.contextual-body`.
  - 38 of 67 rows (57%) name a review lens dimension, not an executable check: those defect classes are now caught only by a reviewer reading the change.
- Nit found: `census-report.md` §A5 says "`deletion-list.md` tags one row `exec`", but the file has two (`deletion-list.md:37` and `:116`, the second added in W3-01), and the script output printed in the same report says 2. Neither function was deleted, so the conclusion holds; only the sentence is stale.
- Evidence: script output above; `mapping-*.md`; `census-report.md` §A3 stitched table.

## 4. 若有 gate 以被移除的比對作為執行證據，`docs/loom/evidence/mechanisms.yaml` 改指向存在的替代，機制普查檢查通過。

- How I tried it:
  - `python3 loom-code/scripts/check_mechanisms.py` in the HEAD worktree and in the base worktree.
  - `git diff 5704cc23..HEAD -- docs/loom/evidence/mechanisms.yaml`.
  - Grepped `mechanisms.yaml` for the basename of each of the 26 changed test files and compared with `mapping-evals.md`.
  - Ran the single-function evals that point into changed files.
- What came back:
  - HEAD: exit 0, `net mechanism count (excl. host-hygiene): 142`, `all clear`. Base: exit 0, 142, `all clear`. Count unchanged.
  - Diff: exactly one eval changed — `decision-map` from the whole `test_decision_map_intent_binding.py` to `loom-workflow/tests/decision-map/test_start_delivery.py::test_creates_intent_and_lists_it_under_the_criterion` (which passed in row 3).
  - Evals pointing at changed files: L50/53/56/110 (`test_loom_skill_description_catalog.py`, whole file), L113 (`test_skill_contract.py`, whole file), L219 (`test_visualization_card_hook.py`, whole file), L222, L351, L354, L357 (single functions). This matches `mapping-evals.md` exactly.
  - L222, L351, L354, L357 nodes: `6 passed`, exit 0.
- Evidence: check output above; `mapping-evals.md`.

## 5. 清理前後，「會執行程式（subprocess／checker 呼叫）」的測試函式數量不減少，重算可證。

- How I tried it: from the HEAD worktree, `python3 docs/loom/2026-09-27-prose-pin-stock-cleanup/evidence/probes/classify-test-files.py --count-exec <at-base> --list` and the same with `<at-head>`, then `diff` of the sorted `::` lines. Cross-checked with the base's own (batch-2) classifier from the base worktree, before the scratch copy of row 1.
- What came back:
  - HEAD classifier: base `1925`, HEAD `1927`. Base classifier: base `1925`, HEAD `1927` (same counting).
  - `diff` of the lists: only two added lines, `loom-code/tests/test_adversarial_batch3_census_misses.py::test_census_yaml_frontmatter_helper_flags_pin` and `::test_residual_pins_named_files_absent_or_overridden`; zero removed lines. So any stricter subset of this count cannot have dropped either.
- Evidence: counts and diff above.

## 6. 三個 plugin 的版號各升一個 patch，三份 manifest、CHANGELOG、README 與版號 pin 測試一致，版號一致性測試通過。

- How I tried it:
  - Read `version` from each of the 9 manifests at base (`git show 5704cc23:...`) and at HEAD.
  - First `## [` heading of each CHANGELOG; grep of root and plugin READMEs for old and new version strings.
  - `pytest loom-code/tests/test_write_plan_station_text.py loom-design/tests/spec/test_capture_intent_contract.py loom-workflow/tests/scripts/test_release_metadata.py -k "release or version or metadata"`.
  - Negative probe: set `loom-workflow/.codex-plugin/plugin.json` version back to `5.5.1` in the scratch worktree, ran `test_release_metadata.py`, then restored the file from a copy (`git status --short` empty afterwards).
- What came back:
  - loom-code 3.22.1 → 3.22.2, loom-design 2.6.0 → 2.6.1, loom-workflow 5.5.1 → 5.5.2, identical across `plugin.json`, `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`.
  - CHANGELOG heads: `## [3.22.2] — 2026-09-29 — Prose-pin stock cleanup batches 2-3 and deferred release bump.`, `## [2.6.1] — 2026-09-29 — deferred release bump, version sync only`, `## [5.5.2] — 2026-09-29 — Prose-pin stock cleanup batches 2-3 and deferred release bump.`
  - READMEs: 0 occurrences of the old versions; new versions in root `README.md` (table rows 16–18, sections 117/132/150) and all 9 plugin READMEs.
  - Version tests: `17 passed, 42 deselected`, exit 0.
  - Negative probe: `FAILED loom-workflow/tests/scripts/test_release_metadata.py::test_manifest_version_is_current[.codex-plugin/plugin.json]`, `1 failed, 9 passed`, exit 1.
- Not verified here: that an installed copy actually receives the update through `claude plugin update`; that needs the change merged and published, which happens after this report.
- Evidence: outputs above.
