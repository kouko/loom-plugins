# Codex model-list discovery — plan
intent: 2026-10-17-codex-model-list-discovery@aab1eda5
charter: 1.1

## Current State Evidence

- Forward: `loom-code/scripts/external_review.py:118` `_codex_candidates` sends initialize, initialized and `model/list` to `codex app-server` through `_run`.
- Reverse: `loom-code/scripts/external_review.py:178` `discover` calls `_codex_candidates`; `loom-code/skills/external-review/SKILL.md:107` documents app-server `model/list` as the candidate source.
- Error: `_run` passes the requests as `input=`, closing stdin; app-server exits on EOF before answering, so discovery reports `codex model/list response missing`.
- Data: tests in `loom-code/tests/test_external_review.py` inject a `subprocess.run`-shaped runner returning the app-server stdout as one string.
- Boundary: discovery timeout is 15 seconds (`external_review.py:124`); `subprocess.TimeoutExpired` becomes `discovery-timeout: <n>s` at `external_review.py:192`.

## Task DAG

**W1-01 Keep app-server stdin open until model/list answers**  after: none  acceptance: 1, 2, 3
- Files: `loom-code/scripts/external_review.py`, `loom-code/tests/test_external_review.py`
- Test: A1 positive: fake-codex-answers-only-while-stdin-open (RED today: response missing); boundary: reader-skips-notification-lines-before-id-2. A2 positive: silent-fake-reader-raises-TimeoutExpired; boundary: existing-timeout-mapping-reports-discovery-timeout. A3 positive: existing-injected-codex-claude-agy-tests-stay-green; boundary: package-suite-passes.
- Risk: agent-decided — real launches use a Popen reader that stops at the id-2 response or timeout; injected runners stay `run`-shaped, preserving existing test coverage in test_external_review.py.

**W1-02 Release metadata patch bump**  after: W1-01  acceptance: 3
- Files: `loom-code/plugin.json`, `loom-code/.claude-plugin/plugin.json`, `loom-code/.codex-plugin/plugin.json`, `loom-code/CHANGELOG.md`, `README.md`, `loom-code/README.md`, `loom-code/tests/test_write_plan_station_text.py`
- Test: A3 positive: release-metadata-synchronized at 3.40.1; boundary: package-suite-passes.
- Risk: agent-decided — patch bump (bug fix, no field, rule id or contract change); rewrite the version pin only where the synchronization test pins it.

## Simplicity check

- drop the stdin-closed negative case; the positive case's RED run already shows the EOF failure — taken
- reuse existing injected-runner, Claude, Agy and timeout-mapping tests for A3 instead of a new test — taken

## Questions asked

- ① — what — 你要的是：你同意讓 Codex 做審查之後，loom 能順利拿到你帳號目前可以用的模型清單，審查才能接著跑。……回答「對」也代表授權自動發布……這樣對嗎？

## Risks

1. The real-launch path cannot be exercised against live Codex in the package suite; a fake `codex` executable on PATH reproduces the EOF behaviour, and acceptance testing runs live discovery.
2. A fixed post-send delay was rejected: reading until the response arrives finishes as soon as Codex answers and still bounds a silent server by the timeout.
