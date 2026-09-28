# Prose-pin stock cleanup, batch 2 — acceptance test evidence

Tried on 2026-09-28, in a clean copy of the project at b2a1601b
(`git worktree add --detach <scratchpad>/at HEAD`), with the branch base
7244374d in a second fresh worktree (`<scratchpad>/at-base`). Both worktrees
were removed afterwards. pytest ran under `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID`.
Exit codes were read directly, not through a pipe.

Setup check: the repo has no install step for its own test tooling beyond
`uv run --isolated --with-requirements requirements-package-tests.lock`; that
command resolved and ran pytest in the clean copy (see 2). The A/B script's
`build` step ran in the clean copy and exited 0 (see 6).

## 1. 用第一批的普查腳本在乾淨副本重跑：句子釘住類為零，而且沒有任何檔案仍帶句子比對斷言（`has_pins=yes`），除非報告中逐檔寫明理由；分類結果可用腳本重算。

- How I tried it: from the clean HEAD worktree root,
  `python3 docs/loom/2026-09-27-prose-pin-stock-cleanup/evidence/probes/classify-test-files.py`.
  Then counted `has_pins=yes` rows and rows without `override=`. Then tested the
  known limitation: `grep -rnE '^\s*assert\s+"[A-Za-z][^"]*( [^" ]+){3,}[^"]*"\s+in\s'`
  over the four test roots (minus `not in`), and read the hits that assert against
  text read from a SKILL.md / reference / doc.
- What came back:
  - Exit 0. `counts: {'behavior': 108, 'gate-eval': 0, 'grammar-invariant': 2, 'not-prose': 54, 'other': 0, 'sentence-pin': 0, 'structure': 66}` (230 files) — identical to census-report.md A1.
  - 19 rows carry `has_pins=yes`; 0 of them lack an `override=… reason=…`. The 19 match the census report's table.
  - Classifier's own tests: `test_classify_test_files.py` + `test_run_ab.py` → 21 passed, exit 0.
  - Blind spot confirmed. The grep found 188 direct multi-word literal asserts in 59 files; most are asserts on program output (fine). The ones that read production prose and that the classifier does not flag include:
    - `loom-workflow/tests/loom-memory/test_skill_contract.py:393` `assert "an unfinished item belongs in an intent." in flat` (also :122, :166, :233, :234, :415, :418) — classified `behavior has_pins=no`.
    - `loom-design/tests/architecture-design/test_architecture_skill.py:81,87,90,92` e.g. `"keep the ratified root document and its active guards unchanged"` — this file is one of the 19 overrides; its reason names only the loop-form hit (four bold field labels) and does not mention these direct sentence asserts.
    - `loom-workflow/tests/decision-map/test_skill_doc.py:181-183,216-218,284,310-312` e.g. `"Exactly three ticket closure types exist" in skill_text` — also one of the 19 overrides; reason names only DOCUMENTED_COMMANDS.
    - `loom-code/tests/test_architecture_doc_consumers.py:34,40,50,61` e.g. `"Treat an unratified draft as advisory" in para` — `structure`, not flagged.
    - `loom-workflow/tests/handoff/test_handoff_schema.py:175,178,207` — `structure`, not flagged.
    - `tests/test_loom_skill_description_catalog.py:167-168` (goal-create description sentence).
    - Comprehension form `[p for p in DECISION_PHRASES if p not in rule5]` at `loom-workflow/tests/loom-visualization/test_references.py:174`, plus `:319` `"For each of the three" in sentence` — `structure`, not flagged. The `polarity_errors(...)` / `guide_errors(...)` asserts in that file check a validator's returned error message, which is program output, not a prose pin.
- Evidence: census output captured at run time; file:line list above.
- Verdict basis: the script's own result meets the line as written (zero, reproducible, every flagged file has a reason). Two of the 19 reasons are incomplete (they cover only the loop-form hit), and the Proposed outcome's repo-wide claim ("only grammar-level invariants remain") does not hold: at least 7 files still assert prose sentences, invisible to the classifier. → partly.

## 2. 這 26 個檔案裡的行為、結構與文法檢查仍在，清理後完整 package suite 全綠。

- How I tried it: `git diff --name-status 7244374d..HEAD` over the four test roots: 33 modified, 1 added (graduated probe), 1 deleted (`loom-code/tests/test_fix_handoff_text.py`, one of the 26, deleted whole per mapping-fix-budget.md). Ran only those changed/added files, one pytest session per plugin root:
  `uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest -q -p no:cacheprovider <files>`.
  Checked that the deleted test functions ran no programs (see 5).
- What came back: loom-code 23 files → 221 passed, exit 0; loom-design 3 files → 48 passed, exit 0; loom-workflow 7 files → 77 passed, exit 0. Total 346 passed.
- Full package suite (not run here, by contract): `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q` — executed by finalize-review, which refuses the attestation when it fails.
- Evidence: captured pytest tails above.

## 3. 每個被移除的釘住，其防守的缺陷類別對應到一個具名替代，對應表存於變更 evidence；acceptance testing 抽查可驗證該替代存在。

- How I tried it: re-ran the census report's `stitch_mappings.py` (extracted verbatim) from the clean HEAD root, then spot-checked by hand:
  - `loom-code/tests/test_selection_store.py::test_failure_survives_rebase` → :228 exists.
  - `loom-code/tests/test_expert_mode_skill.py::test_suggestion_then_plain_yes_skips_nothing` → :136.
  - `loom-code/tests/test_claude_reviewer.py::test_main_rejects_partial_override_before_spawn` → :173.
  - `loom-workflow/tests/distill-sessions/test_apply.py::test_refuses_without_approved_flag` → :137.
  - `loom-code/tests/test_selection_finalize.py::test_five_probe_programs_pass_and_a_sixth_is_refused` → :309.
  - checker rules `adversarial.proportionate`, `review.sync`, `land.merge` → present in `loom_checker.py --list-rules`.
  - lens dimensions `omission`, `inconsistency`, `deletion-first` → `loom-code/skills/closing-review/references/lenses.md:61,67,69,72`.
  - cold-read record `docs/loom/2026-09-19-loom-flow-recovery-loop/blind-run-report.md` exists.
- What came back: `rows: 183`, `by kind: {'kept structural test': 72, 'review lens dimension': 69, 'checker rule id': 15, 'review-only': 11, 'eval re-point': 10, 'cold-read record': 6}`, `problems: 0`, exit 0. Every spot-check resolved.
- Note: 11 rows are `review-only` (no automated replacement; review is the only guard), which the constraints allow.

## 4. 原本以被移除的釘住作為執行證據的每個 gate，在 `docs/loom/evidence/mechanisms.yaml` 中改指向一個存在的替代證據，機制普查檢查通過。

- How I tried it: `git diff 7244374d..HEAD -- docs/loom/evidence/mechanisms.yaml` (9 eval lines changed); a small AST script resolving every `eval:` that names a `.py` file (and `::function`) at HEAD; `python3 loom-code/scripts/check_mechanisms.py`.
- What came back: 9 re-points (distill-sessions, critique, expert-mode, codex hook trust, probe-graduation, atomic claude dispatch, class-relative route, build.absence-recovery → RL-12, review.absence-recovery → RL-04). `py evals 129 bad 0`. check_mechanisms exit 0, `net mechanism count (excl. host-hygiene): 142`, `all clear`.

## 5. 清理不刪除任何行為測試：清理前後，「會執行程式（subprocess／checker 呼叫）」的測試函式數量不減少，重算可證。

- How I tried it:
  - Broad counter: `classify-test-files.py --count-exec <wt> --list` (HEAD classifier) on the base and HEAD worktrees, diffed the lists.
  - Restricted counter: the census report's `restricted_count.py` (extracted verbatim) on both.
  - My own check (`deleted_exec.py`, scratch): every `test*` function defined at base and missing at HEAD in the changed test files, searched for `subprocess|os.system|os.popen|loom_checker|check_output|Popen|_run(`; each hit inspected for real calls.
- What came back:
  - Broad: base 1922, HEAD 1923. Removed: `test_adversary_routing.py::test_recipe_test_module_and_pin_reader_synthetic`. Added: `test_adversarial_census_gaming.py::test_census_loop_phrase_pin_is_pinned`, `test_adversarial_description_ab_probes.py::test_set_output_case_variant_of_old_change_refused`.
  - The removed function (base `loom-code/tests/test_adversary_routing.py:340-363`) only calls `importlib.import_module` on recipe *test* modules and compares dicts; no subprocess, no checker, no production script. It does not meet the intent's definition.
  - Restricted: base 1920, HEAD 1921; only difference is the added ab-probe test. Matches the census report.
  - Own check: 271 test functions deleted (census: 269 + 2 in the loop-form round = 271). 10 contain exec-looking tokens; all 10 only mention `loom_checker.py …` inside prose strings they searched for (calls are `.index`, `.count`, `_flat`, `affirms`, `read_text`), none runs a program.
  - Base classifier on base (`--count-exec .`) gives 728 — the older, narrower counter; not comparable to 1922.

## 6. loom-visualization 描述的 A/B 重跑腳本在乾淨副本照其說明能從頭跑完，對目前的描述產出新的一份結果，結果存於變更 evidence。

- How I tried it: in the clean worktree, `AB_SCRATCH=<scratchpad>/abscratch`, the three commands from the header of `docs/loom/2026-09-14-loom-visualization-description-trigger/ab/run_ab.py` / `ab-rerun/protocol.md`: `build --base-ref 6ad80799`, `run --prompts $OUT/protocol.md --out $OUT --runs 2`, `report … --runs 2`. No `--disable-slash-commands`.
- What came back:
  - `build`: exit 0; `diff -r A B` shows only the description line of `loom-visualization/SKILL.md` differs.
  - Attempt 1 (user's default settings): all 36 sessions `exit=1`; stderr `[claude-code:unrecognized_model] {"model":"hyper-coding-group[1m]","query_source":"sdk"}`; result text "There's an issue with the selected model (hyper-coding-group[1m])…". `~/.claude/settings.json:50` sets that model; `claude -p` rejects it on this machine. `run` itself exited 0. `report` printed `INCOMPLETE` with 18 errors per variant (kept as `ab-rerun/attempt1-model-error-results.md`; the error streams were not committed).
  - Attempt 2: same commands with `ANTHROPIC_MODEL=opus` exported (the script passes the environment through, so both variants get the same model). All 36 `exit=0`. `report` exit 0: A invoked 1/18, B invoked 9/18, table 18/18 both, diagram 0/18 both, errors 0. **Decision: SHIP** (B 9 > A 1, no errors).
  - Stream cross-check (own script over `ab-A/`, `ab-B/`): every init event has model `claude-opus-5-5`; the loaded loom plugins are the variant copies under `abscratch/A|B/`, not the installed ones. `loom-workflow:loom-visualization` Skill calls: B in a1-run2, a2-run1, b1-run2, b2-run1, b3-run1, b3-run2, c2-run1, c2-run2, c3-run1 (9); A in b3-run1 (1). Tool result in `ab-B/c2-login-lockout-run1.jsonl`: `Launching skill: loom-workflow:loom-visualization`, no error.
  - Outputs committed: `ab-rerun/results.md`, `ab-rerun/ab-A/` and `ab-rerun/ab-B/` (36 streams + stderr, 784K + 1.2M, none over 2 MB), scanned for secrets (none).
