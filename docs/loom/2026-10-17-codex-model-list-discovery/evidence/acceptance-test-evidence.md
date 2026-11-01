# Codex review can list the account's models — acceptance test evidence

Tried on 2026-10-17, in a clean copy of the project at 01ac4bf7 (`git worktree add --detach <scratch>/at-head 01ac4bf7`); the before-contrast used a clean copy of main at dd4ec6d1. Setup: the script runs straight from the checkout with system `python3`; no install step needed, and it loaded fine.

Consent record (outside the repo): executor `codex`, review root = a fresh empty temp directory, `authorization_source.kind: direct-user-request` quoting the user's confirmed Acceptance 1, family `openai`, `allowed_efforts: ["high"]`, all five disclosures true. Only discovery was run; no preflight or review prompt.

## 1. With a working Codex login, loom's Codex candidate listing returns the account's current models (a non-empty list) instead of a "response missing" failure.
- How I tried it: `python3 <checkout>/loom-code/scripts/external_review.py --list-candidates --executor codex --scope <empty-root> --consent-record <record>` against the real `codex-cli 0.163.0` on PATH (`/Users/kouko/.local/bin/codex`), once at HEAD and once at main.
- What came back at HEAD (0.14 s):
  `{"status": "completed", "reason": null, "executor": "codex", "candidates": ["gpt-6.1-sol", "gpt-6-astra", "gpt-6-sol", "gpt-6-luna", "gpt-5.6-sol", "gpt-5.6-terra", "gpt-5.6-luna"], "source": "model/list"}`
- What came back at main (before):
  `{"status": "failed", "reason": "discovery-error: codex model/list response missing", "executor": "codex", "candidates": []}`
- Evidence: captured output above.

## 2. When Codex is reachable but never answers, the listing still ends within its time limit and reports a timeout or failure reason rather than hanging.
- How I tried it: a fake `codex` first on PATH (`#!/bin/sh` / `sleep 300 &` / `exec sleep 301`) — it never answers, and its background child also holds stdout open. Ran the same command at HEAD under `time`, then `pgrep -fl 'sleep 30[01]'`.
- What came back: `{"status": "failed", "reason": "discovery-timeout: 15s", "executor": "codex", "candidates": []}`, wall time 15.05 s; `pgrep` found no leftover process.
- Evidence: captured output above.

## 3. Candidate listing for Claude Code and Antigravity behaves as before, and the complete package suite passes.
- How I tried it: (a) `git diff dd4ec6d1 HEAD -- loom-code/scripts/external_review.py | grep '^[-+].*\(claude\|agy\)'` — no match; the change touches only the Codex path. (b) `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest -q loom-code/tests/test_external_review.py loom-code/tests/test_external_review_adversarial.py -k "claude or agy or antigravity"` → `38 passed, 82 deselected`. No network-backed agy discovery was run.
- Full suite: the package suite command is `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`. finalize-review executes it and refuses the attestation on failure. (I also launched it once in the clean copy; only the tail of its output was captured, without an overall summary or exit code, so that run is not cited as a result.)
- Evidence: test selection and counts above.
