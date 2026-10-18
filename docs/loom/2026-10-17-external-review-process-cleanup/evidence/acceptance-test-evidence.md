# Outside review steps end cleanly and report the right reason — acceptance test evidence

Tried on 2026-10-18, in a clean copy of the project at 4f9faa9e (fresh `git worktree add --detach` in the session scratchpad).

Setup: no install step is needed for the script; `python3 loom-code/scripts/external_review.py --help` ran and printed its usage in the clean copy. Fake `codex`, `claude` and `agy` executables (one Python file, `fakecli.py`, symlinked three times) were put first on PATH. `FAKE_MODE` selects behaviour: `normal`, `hang_list`, `hang_probe`, `hang_review` (the CLI starts a `sleep 300` child that inherits stdout/stderr, records both pids, then sleeps 300 s itself), `exit_early` (`codex app-server` writes to stderr and exits 3 without answering). Consent records were valid per executor (approved, all disclosures true, direct-user-request authorization, `selection_authorized`, `allowed_efforts: [high]`). Every run went through the command-line entry point, with the prompt on stdin. Driver: `drive.sh MODE executor model family [flags]`, which prints the JSON result, exit code, elapsed time, and `kill -0` for each recorded pid.

## 1. When an outside CLI used for Antigravity model listing, the probe, or the review is still running at its time limit while a child process holds its output open, the step ends shortly after the limit, reports a timeout, and leaves no process running.
- How I tried it: `--probe-timeout-seconds 2 --review-timeout-seconds 4`, modes `hang_probe` and `hang_review` for codex/gpt-5.4, claude/sonnet, agy/gemini-3-pro; `hang_list` for agy through a review run and through `--list-candidates`.
- What came back:

| Case | reason | elapsed | CLI + child pids |
|---|---|---|---|
| hang_probe codex | execution-timeout: 2s | 2.1s | both gone |
| hang_probe claude | execution-timeout: 2s | 2.1s | both gone |
| hang_probe agy | execution-timeout: 2s | 2.1s | both gone |
| hang_review codex | execution-timeout: 4s | 4.1s | both gone |
| hang_review claude | execution-timeout: 4s | 4.1s | both gone |
| hang_review agy | execution-timeout: 4s | 4.1s | both gone |
| hang_list agy (in review run) | execution-timeout: 15s | 15.1s | both gone |
| hang_list agy (`--list-candidates`) | discovery-timeout: 15s | 15.03s | both gone |

- Evidence: captured output above; exit code 1 in every case.

## 2. A review run with no explicit time limit is allowed 30 minutes before it is reported as timed out.
- How I tried it: started a real run with no time-limit flag against a hanging review (`hang_review` claude). The coordinator asked to stop it before the 30 minutes ran out, so it was stopped with no result. Instead: (a) ran the CLI with no time-limit flag while recording the timeout the real launcher received for each stage; (b) `--review-timeout-seconds 1801` and `1800`; (c) compared the defaults on base 70b1be8f; (d) `pytest loom-code/tests/test_external_review.py -k timeout`.
- What came back: (a) `timeouts passed (probe, review): [45, 1800]`; (b) 1801 gives `invalid-explicit-profile`, 1800 gives `completed`; (c) base had `review_timeout: int = 600` and `--review-timeout-seconds ... default=600`; (d) `3 passed, 115 deselected`.
- Evidence: captured output above. The 30-minute timeout itself was not observed going off, but row 1 shows that the timeout ends the step on time.

## 3. When Codex exits before answering the model-list request, the reported reason says Codex failed and carries its exit status, instead of "response missing".
- How I tried it: `FAKE_MODE=exit_early` (app-server exits 3 without answering), through `--list-candidates --executor codex` and through a full review run (`--executor codex --model gpt-5.4 ...`). Repeated on base 70b1be8f for comparison.
- What came back:
  - model listing at HEAD: `"reason": "discovery-error: codex model/list failed: exit 3"`.
  - review run at HEAD: `"reason": "execution-error: unknown error"`.
  - base, same two runs: `discovery-error: unknown error` and `execution-error: unknown error`.
- Evidence: `loom-code/scripts/external_review.py` `execute()`'s `known` set (around line 471) does not contain `codex model/list failed: exit N`, so the `ValueError` that `_codex_candidates` raises gets turned into `unknown error`. `discover()` matches it with a regex. Tests pin only the discovery path (`test_external_review.py:951`).

## 4. Model listing, probe and review for Codex, Claude Code and Antigravity behave as before when the CLI answers normally, and the complete package suite passes.
- How I tried it: `FAKE_MODE=normal` full review runs for all three; a live Codex model-list discovery (`external_review.discover("codex", <abs root>, consent)`, codex-cli 0.163.0, model/list request only, no review content sent); the external-review tests.
- What came back: all three runs gave `status: completed` with review output `REVIEW: looks fine`, probe returncode 0, and codex observed model and effort `gpt-5.4`/`high`. Live Codex: `status: completed`, candidates `gpt-6.1-sol, gpt-6-astra, gpt-6-sol, gpt-6-luna, gpt-5.6-sol, gpt-5.6-terra, gpt-5.6-luna`, source `model/list`. `pytest loom-code/tests/test_external_review.py loom-code/tests/test_external_review_adversarial.py`: 127 passed.
- Not run here: live probe or review against any vendor (forbidden, since it would send content and use quota); the full package suite, which finalize-review runs: `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`.

## Re-run on 2026-10-18, at 0c5bb1eb
Fix range b99dd759..0c5bb1eb: only `external_review.py` (a new `_DISCOVERY_REASONS` set and `_is_discovery_reason()`, used by both `discover()` and `execute()`'s error branch) plus 3 test lines. Fresh `git worktree add --detach` at 0c5bb1eb; `--help` ran. The fake CLI gained `FAKE_EXIT` (the exit code for `exit_early`, default 3).
- 1: carried over — the diff does not touch `_launch`, the timeouts, or the process-group kill; it only changes how a `ValueError` message becomes a reason string.
- 2: carried over — the diff changes no timeout default, no range check, and no parser default.
- 3: re-tested — both surfaces, with exit 3 and exit 0:
  - `--list-candidates`, exit 3: `discovery-error: codex model/list failed: exit 3`
  - review run, exit 3: `execution-error: codex model/list failed: exit 3`
  - `--list-candidates`, exit 0: `discovery-error: codex model/list failed: exit 0`
  - review run, exit 0: `execution-error: codex model/list failed: exit 0`
- 4: re-tested — `FAKE_MODE=normal` full review runs: codex, claude and agy each `status: completed`, exit 0. Live `discover("codex", ...)` (model/list only): `completed`, the same 7 candidates. `pytest test_external_review.py test_external_review_adversarial.py`: 127 passed. The full suite is left to finalize-review (command above). The coordinator reported a full-suite rerun after the fix with exit 0, but I did not see that run myself, so it is not counted as my evidence.
