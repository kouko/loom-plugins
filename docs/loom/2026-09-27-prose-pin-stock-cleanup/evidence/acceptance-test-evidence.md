# Prose-pin stock cleanup (batch 1) — acceptance test evidence

Tried on 2026-09-28, in a clean copy of the project at ce126a4c
(`git worktree add <scratch>/at-wt HEAD`; branch base 946e06d1). Every
command below ran from that worktree. `C` stands for
`docs/loom/2026-09-27-prose-pin-stock-cleanup/evidence/probes/classify-test-files.py`.

## Setup

- How I tried it: followed README "Development": the package-test
  environment is `uv run --isolated --with-requirements requirements-package-tests.lock`.
  Used it (with `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID`) to run the
  tests named below. The full package suite was not run here (left to
  finalize-review).
- What came back: the environment resolved and every targeted run below passed.
- Scope note: the change touches no file under any `skills/` or `agents/`
  tree (`git diff --stat 946e06d1..HEAD -- '*/skills/*' '*/agents/*'` is empty);
  AGENTS.md changes one line (the module-criteria check pointer, since
  `test_module_criteria_text.py` was deleted); README/CHANGELOG/manifests carry
  the version bump.

## 1. 一份普查報告存在於變更 evidence：每個讀散文的測試檔被分類為行為／結構／句子釘住／文法不變量四類之一，分類方法可用腳本重算。

- How I tried it: `python3 $C` in the clean worktree; compared its table and
  counts with `evidence/census-report.md`. Also ran `$C` in the user's own
  working tree and at commit dce0c611 (the commit that regenerated the report).
  Listed every file the script puts in `other`.
- What came back:
  - Clean HEAD: `counts: {'behavior': 112, 'gate-eval': 5, 'grammar-invariant': 5, 'not-prose': 54, 'other': 12, 'sentence-pin': 0, 'structure': 42}` (230 files).
  - Report: behavior 111, gate-eval 5, grammar-invariant 5, not-prose 58, other 13, sentence-pin 0, structure 42 (234 files).
  - Clean dce0c611: behavior 111, other 13, not-prose 54 — so the report's
    prose classes reproduce at the commit it was made from, but its
    not-prose 58 came from a working tree with extra untracked files (the
    user's tree gives not-prose 59 today).
  - HEAD drift: `loom-code/tests/test_adversary_recipe_code.py` is
    `behavior` today, `other` in the report — commit 7d7600a9 (W4-01 fix)
    moved a subprocess case into it after the report was regenerated.
  - The script has a fifth outcome `other` (`_classify` falls through at
    `classify-test-files.py:278`) for a file that names a `.md` path but
    matches no class. It is printed only as a count; the per-file table
    omits it. The 12 `other` files at HEAD, all real test files:
    `loom-code/tests/test_adversary_recipe_skill_gate.py`,
    `loom-code/tests/test_adversary_recipe_spec.py`,
    `loom-code/tests/test_check_skill_crossrefs.py`,
    `loom-code/tests/test_codex_hook_trust_contract.py`,
    `loom-code/tests/test_principles_amendment.py`,
    `loom-code/tests/test_ship_guidance_presence.py`,
    `loom-workflow/tests/scripts/test_distill_sessions_compaction.py`,
    `loom-workflow/tests/scripts/test_loom_visualization_description_ab.py`,
    `loom-workflow/tests/scripts/test_no_retired_loom_code_skill_names.py`,
    `loom-workflow/tests/scripts/test_skill_count.py`,
    `tests/test_kickoff_defaults.py`, `tests/test_principles_ratification.py`.
- Evidence: captured outputs above; classifier probe
  `docs/loom/.../probes/test_classify_test_files.py` 3 passed.
- Verdict: partly — the report exists and the script recomputes it, but 12
  prose-reading test files land outside the four classes and are not listed,
  and the report is one file behind HEAD.

## 2. 純句子釘住檔案（零可執行行為）全數刪除；普查歸為句子釘住類的混合檔案只保留行為與結構部分；清理後完整 package suite 全綠。

- How I tried it: `git diff --name-status 946e06d1..HEAD` for deletions and
  prunes; read the `other` files from row 1 for execution and literal asserts
  (`grep -c subprocess`, `grep -n assert`); ran the tests of every file the
  change touched:
  `pytest -q -p no:cacheprovider loom-code/tests/test_adversarial_census_gaming.py loom-code/tests/test_adversary_recipe_code.py loom-code/tests/test_adversary_recipe_skill_gate.py loom-code/tests/test_adversary_recipe_spec.py loom-code/tests/test_adversary_recipe_shape.py loom-code/tests/test_dispatch_profile_contract.py loom-code/tests/test_write_plan_station_text.py loom-workflow/tests/goal-create/test_goal_shape.py loom-workflow/tests/goal-create/test_skill_md.py loom-workflow/tests/scripts/test_critique_compaction.py loom-workflow/tests/scripts/test_release_metadata.py`
  and `pytest -q loom-code/tests/test_adversary_routing.py` separately.
- What came back:
  - Deleted: `test_agy_tool_mapping.py`, `test_module_criteria_text.py`,
    `test_input_floor.py`, `test_goal_create_compaction.py`. Pruned: the
    three recipe modules, `test_adversary_routing.py`,
    `test_dispatch_profile_contract.py`, `test_skill_md.py`,
    `test_critique_compaction.py` (`test_write_plan_station_text.py` only
    bumps its version constant).
  - Touched tests: `129 passed in 1.70s`; routing file: `41 passed in 59.28s`.
  - Pure sentence-pin files with zero execution still present (all in `other`):
    - `loom-code/tests/test_codex_hook_trust_contract.py` — docstring
      "Contract pins…"; 0 subprocess; e.g. line 15
      `assert "As observed on Codex 0.153.4, creating another worktree does not create another installed Loom hook identity" in text`.
    - `loom-code/tests/test_principles_amendment.py` — 0 subprocess;
      lines 58-60 assert full PRINCIPLES.md sentences (`TWO_CASES_SENTENCE`, `DISCLOSURE_SENTENCE`).
    - `loom-code/tests/test_ship_guidance_presence.py` — 0 subprocess;
      checks `"Use a Markdown table for any list‑type or comparison‑type information" in content`.
    - `tests/test_kickoff_defaults.py` lines 54-59 also assert literal phrases
      of a note, alongside non-prose checks.
  - Package suite command (not run here; finalize-review runs it and
    refuses the attestation on failure):
    `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`
- Verdict: partly — the files the census found were handled and their tests
  pass; at least three pure pin files the census never surfaced remain.

## 3. 每個被刪除的釘住測試，其防守的缺陷類別對應到一個具名替代（checker 重算規則、結構測試或 review lens 面向），對應表存於 evidence，acceptance testing 抽查可驗。

- How I tried it: read the "Removed sentence-pin tests → replacement
  evidence" table in `census-report.md`; checked it covers every deleted or
  pruned file from row 2; grepped the named lens facets; checked the
  deleted-file replacements.
- What came back:
  - 12 rows, covering all 4 deleted and 7 pruned files, plus
    `test_adversary_recipe_shape.py`, marked "pruned" although its net diff
    946e06d1..HEAD is empty (changed in 45bd949d, restored in e4ec2437; it is
    now kept by a manual structure override).
    (`test_write_plan_station_text.py` changes only its version constant, so
    it needs no row.)
  - Lens facets `omission`, `incorrect-fact`, `ambiguity`, `inconsistency`
    all exist in `loom-code/skills/closing-review/references/lenses.md` and
    `loom-code/agents/reviewer.md`.
  - `test_input_floor.py` → "Structural tests": `test_goal_shape.py` keeps the
    input-floor checks (`test_input_floor_names_two_slots` etc. live there),
    and its docstring was updated to say it is now the only copy.
  - `test_module_criteria_text.py` → "Checker rules + review lens: ambiguity":
    AGENTS.md now points to `test_adversary_routing.py` / `test_adversary_layout.py`.
  - Ten rows lean on a generic "Structural tests" or "Checker rules" without
    naming which test or which checker rule id; for two of them
    (`test_input_floor.py`, `test_goal_create_compaction.py`) that is the
    whole replacement.
- Verdict: partly — every row has a replacement and the spot checks hold,
  but several replacements are a category, not a named test or rule.

## 4. 清理後普查報告證明句子釘住類為零：字面感應檔案只剩文法級不變量類，以及被 `docs/loom/evidence/mechanisms.yaml` 登記為 gate eval 的檔案（該 gate 的執行證據，本批保留並在報告中單獨列類）。

(Read with the 2026-09-28 amendment: the 15 behavior files with `has_pins=yes`
are also allowed, deferred to batch 2.)

- How I tried it: same classifier run as row 1; compared the literal-sensitive
  files at HEAD with the allowed set (grammar-invariant 5 + gate-eval 5 +
  batch-2 list 15).
- What came back: `sentence-pin: 0` reproduces, and gate-eval is listed as its
  own class. But the three pure pin files in row 2 (and the literal asserts in
  `tests/test_kickoff_defaults.py`) are literal-sensitive, are in none of the
  allowed sets, and appear in neither the report table nor the batch-2 list.
  The zero is produced by the `other` bucket, not by the files being gone.
- Evidence: row 1 and row 2 outputs.
- Verdict: fails.

## 5. 清理不刪除任何行為測試：清理前後，「會執行程式（subprocess／checker 呼叫）」的測試函式數量不減少，重算可證。

- How I tried it: `git archive 6f3acd78` and `git archive 946e06d1` into
  scratch dirs; `python3 $C --count-exec <dir>` on each and on HEAD. Then an
  independent count I wrote (AST: `test*` functions whose body contains
  `subprocess.`, `returncode` or `loom_checker`), with a per-name diff
  946e06d1 → HEAD.
- What came back:
  - Script: 6f3acd78 727, 946e06d1 727, HEAD 730 (report says 728; the two
    W4-01 graduations added since account for the difference).
  - Independent: 705 → 708. Gone: `test_adversary_routing.py::test_a_reworded_recipe_is_not_blamed_on_the_addition`;
    new in the same file: `test_a_reworded_recipe_plants_no_failure_for_the_addition_to_be_judged_on`
    (a rename listed in `NESTED_TESTS`; its assertion now expects a reword to
    plant no failure, which is the point of pruning the pins), plus
    `test_reword_plants_when_prose_pin_exists_synthetic`,
    `test_adversary_recipe_code.py::test_case_class_check_recipe_row_dropped_goes_red`,
    `test_adversarial_census_gaming.py::test_census_roots_flag_given_is_accepted`.
  - The deleted helper test `test_first_planting_fails_when_nothing_was_planted_synthetic`
    ran no program (pure function), so it is outside this count.
- Verdict: works.

## Evidence probes (each run as its own command)

- `probes/test_classify_test_files.py`: 3 passed
- `probes/test_adversarial_census_gaming.py`: 2 passed
- `probes/test_adversarial_pruned_guards.py`: 1 passed
