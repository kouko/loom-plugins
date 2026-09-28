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

## Re-run on 2026-09-28, at ab45f9b5

Fix range d8f2615f..ab45f9b5 (f16c5550, 61bcfcd0, ab45f9b5). Fresh worktrees:
`git worktree add --detach <scratchpad>/at2 HEAD` (ab45f9b5) and
`<scratchpad>/at2-base 7244374d`; both removed afterwards. pytest under
`env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID`; exit codes read directly.
Setup check: `uv run --isolated --with-requirements requirements-package-tests.lock`
resolved and ran in the clean copy; `run_ab.py build --base-ref 6ad80799` exit 0.

- 1: re-tested — `python3 docs/loom/2026-09-27-prose-pin-stock-cleanup/evidence/probes/classify-test-files.py` from the at2 root: exit 0, `counts: {'behavior': 108, 'gate-eval': 0, 'grammar-invariant': 2, 'not-prose': 54, 'other': 0, 'sentence-pin': 0, 'structure': 66}`. 19 rows `has_pins=yes`, 0 without `override=… reason=…`. The two reasons the first run found incomplete are now complete: `test_architecture_skill.py` says the direct sentence asserts were pruned in closing review round 1 (confirmed in the diff: `test_single_answer_proposal_not_allowed` deleted, five phrase asserts removed from `test_skill_states_redesign_updates_decisions_rules_guards`); `decision-map/test_skill_doc.py` names its direct asserts (181-183, 216-221, 281-287, 310-312) and leaves them for batch 3. census-report.md A1 now states the `has_pins` scope limit and lists 7 batch-3 files; spot-checked `loom-workflow/tests/loom-memory/test_skill_contract.py:358` (`"an unfinished item belongs in an intent." in flat`), `loom-code/tests/test_architecture_doc_consumers.py:34` — both still direct sentence pins at HEAD, as the list says. Verdict against the line as written: works. The Proposed outcome's repo-wide claim remains unmet (7 files).
- 2: re-tested — full package suite from the at2 root: `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q` → **exit 0**; 13 pytest sessions, 3283 passed (plus skips, e.g. `78 passed, 3 skipped`, `218 passed, 5 skipped`), 0 failed, 0 errors; 147 shell-test `PASS —` lines, no `FAIL`. Log kept in scratchpad during the run, not committed. Plus `pytest docs/loom/2026-09-14-loom-visualization-description-trigger/ab/test_run_ab.py docs/loom/2026-09-27-prose-pin-stock-cleanup/evidence/probes/` → 25 passed, exit 0. Fix-round test changes checked in the diff: only `test_single_answer_proposal_not_allowed` was deleted (text-only, runs nothing); the other edits drop assert lines inside kept functions (`test_dispatch_profile_contract.py` count-form, `test_expert_mode_skill.py` `== 1` → `<= 1`) or a comment (`test_skill_contract.py` header).
- 3: re-tested — the census report's `stitch_mappings.py`, extracted from its `<details>` block, does not parse: `SyntaxError: unterminated string literal (detected at line 99)`. The fix commit 61bcfcd0 expanded the `\n` escapes in the script's `out.write(...)` line into real newlines and spliced the stitched table in, so the script's tail (the row-writing loop, the four `print` lines), the closing code fence, `</details>` and the `### Stitched table` heading are gone; the python fence stays open until the next fence at A5, so A4 and A5 render as code. I restored the tail verbatim from `git show d8f2615f:<census-report.md>` (only change in the fix round: the pipe-split line, kept as at HEAD) and ran it from the at2 root: `rows: 187`, `by kind: {'review lens dimension': 73, 'kept structural test': 71, 'checker rule id': 16, 'review-only': 11, 'eval re-point': 10, 'cold-read record': 6}`, `deleted defs in changed files: 335`, `problems: 0`, exit 0. The 187 generated rows are byte-identical to the 187 `| mapping…` rows in the report. Population recount (own script, same rule as the report: a lens row is lens-only when its replacement cell matches none of `::name`, `test_*.py`, `same function`, `keep(s)`, `stay(s)`, `checker rule`, or a backticked id from `loom_checker.py --list-rules`): review-only 11 + lens-only 38 = **49 of 187** with no executable replacement — matches the report. The earlier row's "11 review-only" undercounted this population. The four new `mapping-residual` rows cover the fix-round removals (dispatch_profile presence half, expert_mode `== 1`, `test_single_answer_proposal_not_allowed`, the five redesign phrases). `test_skill_contract.py`'s new header points at `::test_record_section_matches_the_digest_the_cold_reader_eval_was_run_against` (:387) and `loom-workflow/skills/loom-memory/evals/record-timing.md`; both exist.
- 4: carried over — the fix range does not touch `docs/loom/evidence/mechanisms.yaml`. Three evals point into files the fix edited (`test_architecture_skill.py` and `loom-memory/test_skill_contract.py` as whole files, `test_expert_mode_skill.py::test_suggestion_then_plain_yes_skips_nothing` at :136); all still resolve, and none names the one deleted function. `python3 loom-code/scripts/check_mechanisms.py` at HEAD: exit 0, `all clear`.
- 5: re-tested — `restricted_count.py` (extracted verbatim from census-report.md A5) and `classify-test-files.py --count-exec <wt> --list` (HEAD classifier), on at2-base and at2. Restricted: base **1920**, HEAD **1921**; the list diff is one addition (`test_adversarial_description_ab_probes.py::test_set_output_case_variant_of_old_change_refused`), no removals. Broad: base 1922, HEAD 1925; removed `test_adversary_routing.py::test_recipe_test_module_and_pin_reader_synthetic` (runs nothing, see the first run), added the two `test_adversarial_batch2_loop_phrase_pin.py` functions (they now load the docs classifier by path), `test_census_loop_phrase_pin_is_pinned` and the ab-probe test above. The one fix-round deletion, `test_single_answer_proposal_not_allowed`, is on neither base list.
- 6: re-tested at script level, sessions not re-run (the fix changed only the all-errored exit path and the header/protocol text). Stub `<scratchpad>/stubbin/claude`: prints `{"type": "result", "is_error": true, "result": "unrecognized_model"}`, writes `unrecognized_model` to stderr, exits 1. In at2 with `AB_SCRATCH=<scratchpad>/abscratch2`: `build --base-ref 6ad80799` exit 0; `PATH=<stubbin>:$PATH python3 $AB run --prompts <scratchpad>/about/protocol.md --out <scratchpad>/about --runs 1` → 18 lines `… exit=1`, last line `every one of the 18 sessions errored; see the .stderr.txt files`, **exit 1** (before the fix `run` exited 0 in this case). `report` then printed `**INCOMPLETE**`. `git diff --quiet d8f2615f HEAD -- …/ab-rerun/results.md …/ab-A …/ab-B` exit 0: the earlier results are unchanged (A 1/18, B 9/18, errors 0, **SHIP**). Header of `run_ab.py` and `ab-rerun/protocol.md` now both say `export ANTHROPIC_MODEL=<model>` when `claude -p` rejects the default model, and that `run` exits non-zero when every session errored. `test_run_ab.py::test_run_exits_nonzero_when_every_session_errors` passes (in the 25 above).
