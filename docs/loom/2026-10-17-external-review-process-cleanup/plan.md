# External review process cleanup — plan
intent: 2026-10-17-external-review-process-cleanup@526ed8cf
charter: 1.1

## Current State Evidence

- Forward: `loom-code/scripts/external_review.py:112` `_run` calls the injected `runner` (default `subprocess.run`) with `timeout=` for Antigravity listing (`:206`) and the probe and review stages (`:399`).
- Reverse: `discover` and `execute` take `runner: Runner = subprocess.run`; `_run` and `_codex_candidates` (`:175`) branch on `runner is subprocess.run` to pick the real launch path.
- Error: timed-out `subprocess.run` kills only the child and waits for pipe EOF, which a descendant holding stdout blocks; `_codex_app_server` always returns returncode 0, hiding an early Codex exit.
- Data: `discover` maps only reason strings in its `known` set (`:257`), anything else becomes `unknown error`; every injected test runner is `run`-shaped and accepts `**kwargs`.
- Boundary: review timeout defaults to 600 s in `execute` (`:353`) and `--review-timeout-seconds` (`:461`), validated as `probe_timeout < review_timeout <= 1800`; discovery uses 15 s, the fallback as a literal (`:180`).

## Task DAG

**W1-01 One bounded launcher for every outside CLI, 30-minute review default**  after: none  acceptance: 1, 2, 3, 4
- Files: `loom-code/scripts/external_review.py`, `loom-code/tests/test_external_review.py`
- Test: A1 positive: agy-models-descendant-holds-stdout-times-out-no-process-left (RED today: hangs); boundary: review-stage-descendant-holds-stdout-reports-execution-timeout. A3 positive: fake-codex-exits-before-answer-reports-failed-with-exit-status; negative: answering-fake-codex-still-lists-models. A2 positive: execute-and-cli-default-review-timeout-is-1800; boundary: review-timeout-1801-still-rejected. A4 positive: existing-injected-runner-tests-stay-green; boundary: package-suite-passes.
- Risk: agent-decided — default `runner` becomes a module `run`-shaped launcher (own session, group kill on timeout); Codex passes `until_response_id=2`, removing both identity checks; review default 1800 is the validated upper bound; preserves test_external_review.py coverage.

**W1-02 Release metadata patch bump**  after: W1-01  acceptance: 4
- Files: `loom-code/plugin.json` (+ `.claude-plugin`, `.codex-plugin` copies), `loom-code/package.json`, `loom-code/CHANGELOG.md`, `README.md` (+ ja, zh-TW), `loom-code/README.md`, `loom-code/tests/test_write_plan_station_text.py`
- Test: A4 positive: release-metadata-synchronized at 3.41.1; boundary: package-suite-passes.
- Risk: agent-decided — patch bump (bug fix, no field, rule id or contract change); rewrite the version pin only where the synchronization test pins it.

**W1-03 Graduate the stdin-backpressure probe**  after: W1-01  acceptance: 1
- Files: `docs/loom/2026-10-17-external-review-process-cleanup/evidence/probes/test_launch_stdin_backpressure.py`, `loom-code/tests/test_external_review_adversarial.py`
- Test: A1 positive: large-prompt-to-non-reading-child-times-out runs in the package suite; boundary: probe file removed from the change store.
- Risk: agent-decided — move the red-then-green probe into the existing graduated external-review regression file with its concern line in the header block.

## Simplicity check

- merge the 30-minute default into W1-01; same files, two literals, no separate risk — taken
- reuse the PR #92 fake-`codex` PATH fixture for the new launcher cases instead of a new harness — taken

## Questions asked

- ① — what — 四項後續修正要一起做（A）、只做卡住風險（B）、只做小修正（C）、還是先不做（D）？
- ① — what — 正式審查時限：這次調到 30 分鐘（A）、維持 10 分鐘（B）、還是先實測再決定（C）？
- ① — what — 審查中看得到進度：只調時限另開改動（A）、Codex 無輸出判定卡住（B）、定時回報已跑時間（C）、三家改串流輸出（D）？
- ① — what — 更新後的需求覆述，對嗎？（含自動發布授權）

## Risks

1. A descendant that starts its own session escapes the group kill; the launcher still returns at the limit, but that process can outlive the step.
2. When the main process exits normally while a descendant keeps stdout open, the launcher must stop reading once the main process has exited plus a short grace, or a finished review would be reported as a timeout.
3. `loom-code/scripts/claude_reviewer.py` calls `subprocess.run` with a timeout and has the same descendant exposure; it is a separate script outside this intent's named steps and is left as a follow-up.
4. user-decided — second-vendor selection-confirmed: codex
