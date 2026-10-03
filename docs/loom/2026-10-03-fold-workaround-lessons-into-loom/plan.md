# Fold workaround lessons into loom — plan
intent: 2026-10-03-fold-workaround-lessons-into-loom@852a72ae
charter: 1.1

## Current State Evidence
- Forward: `loom-code/scripts/loom_checker/probes.py` `command_executes_artifact` accepts `python -m pytest <artifact>` only when the artifact is the fourth token; options before it are refused.
- Reverse: the same function repeats the direct and `-m pytest` checks inside a second `uv run` branch; `test_loom_attestation.py` and `test_adversarial_probe_cap_coverage.py` call it.
- Error: `command_handlers/publish.py` `_publish_block("existing pull request identity does not match origin, HEAD, and base")` gives no next step when GitHub lags a push.
- Data: `closing-review/references/adversarial.md` says an empty attack "is reported as an attempt", while `adversarial` severity guidance has no rule for deliberate-only bypasses.
- Boundary: `agents/implementer.md` says never delete a test to reach green; capture-intent's description has no active-change exclusion; description budget 3,676 of 4,047 chars.

## Task DAG
Wave 1 changes three independent surfaces; wave 2 bumps versions.

**W1-01 Adversarial command check accepts runner options before the program**  after: none  acceptance: 1
- Files: loom-code/scripts/loom_checker/probes.py, loom-code/tests/test_loom_attestation.py
- Test: A1 positive: pytest-option-before-artifact-accepted; negative: pytest-without-declared-artifact-refused.
- Risk: agent-decided — one shared python-argv check skips leading `-` options and replaces the duplicated uv branch; widens test_loom_attestation.py coverage, preserves test_adversarial_probe_cap_coverage.py cases.

**W1-02 Publish identity refusal names the retry-once step**  after: none  acceptance: 3
- Files: loom-code/scripts/loom_checker/command_handlers/publish.py, loom-code/tests/test_loom_publish.py
- Test: A3 positive: identity-mismatch-message-says-retry-once-then-stop; negative: identity-mismatch-still-blocks-without-retry.
- Risk: agent-decided — append one hint sentence to the existing refusal text; no retry loop, exit code unchanged; existing publish tests matching the message stay valid.

**W1-03 Guidance text absorbs the lessons**  after: none  acceptance: 2, 4, 5, 6, 7
- Files: loom-code/skills/closing-review/references/adversarial.md, loom-code/agents/implementer.md, loom-code/agents/adversary.md, loom-design/skills/capture-intent/SKILL.md, AGENTS.md
- Test: A2 positive: empty-attack-reuses-test; negative: no-bare-attempt. A4 positive: bypass-rated-nit; boundary: ordinary-keeps-severity. A5 positive: removed-tests-deleted; negative: green-deletion-forbidden. A6 positive: bump-last-round; negative: rule-unchanged. A7 positive: excludes-active-change; boundary: budget-met.
- Risk: agent-decided — prose only, no gate marker, no docs/ citation; deliberate-only findings rated nit at the source keeps Build's fix-every-important rule; description stays within the 4,047-char budget.

**W2-01 Version bump**  after: W1-01, W1-02, W1-03  acceptance: 8
- Files: loom-*/**/plugin.json, loom-*/package.json, loom-*/CHANGELOG.md, README.md, loom-*/README*.md, loom-*/tests/**/test_*.py
- Test: A8 positive: release-metadata sync tests pass at the new versions; negative: `sync_codex_manifests.py --check --all` exits 0.
- Risk: agent-decided — minor for loom-code (station guidance, checker) and loom-design (entry description); loom-workflow untouched.

**W3-01 Graduate the pytest option-order probe into the suite**  after: W2-01  acceptance: 1
- Files: docs/loom/2026-10-03-fold-workaround-lessons-into-loom/evidence/probes/test_abuse_pytest_option_order.py, loom-code/tests/test_adversarial_pytest_option_order.py
- Test: A1 positive: value-option-before-artifact-accepted; negative: deselected-artifact-refused.
- Risk: agent-decided — move the adversary's red probe into loom-code/tests once the value-option fix makes it green; the probe leaves the change store.

## Simplicity check
- Drop adversary.md — reverted: its 'run ends here' sentence contradicted the reuse rule
- Drop the A7 description phrase test; the existing budget test covers the boundary — taken
- Merge the entry-description and AGENTS.md task into the guidance task — taken

## Questions asked
① — what — 建議先做 B+C 嗎／要照這樣開始嗎 → 「好」
① — what — 第 1 項改程式碼還是只寫文件；第 3 項只加提示還是自動重試 → 「1. 改程式碼 3.只加提示」
① — what — 第 4 項改成評為 nit；第 8 項延後 → 「好，兩項都同意」
① — consequence — 覆述 intent，含自動發布授權 → 「對」

## Risks
1. user-decided — publish never retries on its own; the hint relies on the agent or user following it once.
2. The collect-only gap is now closed: the check refuses any pytest option that runs no tests and any option not on its allowlist, in any position after `-m pytest`.
3. user-decided — second-vendor selection-confirmed: codex
