# Complete runnerless probe graduation — plan
intent: 2026-10-13-complete-runnerless-probe-graduation@3d242fbe4327f35bb8e6eabd71dfc62e71113176
charter: 1.1

## Current State Evidence
- Forward: `probes.py:_runner_launcher` recognizes the declared `uv run` options before locating the runner's Python executable.
- Reverse: `probes.py:suite_collection` uses that launcher for inventory and pytest collection; `finalize.py:_finalize` accepts graduated artifacts it collects.
- Error: `probes.py:_declared_suite_commands` refuses an unsupported declared runner launcher instead of silently accepting its inventory.
- Data: `docs/loom/KICKOFF-DEFAULTS.md:package-tests` declares `uv run --isolated --with-requirements` for this repository.
- Boundary: `test_selection_finalize.py` exercises collection, ignored tests, and declared Conda environments; the prior closing reviewer found missing `uv` CLI grounding.

## Task DAG

**W1-01 Ground the existing runner launcher**  after: none  acceptance: 1,2,3,4,5
- Files: `loom-code/scripts/loom_checker/probes.py`
- Test: A1 positive: runnerless-finalizes; negative: broken-collection-refused. A2 positive: selected-accepted; negative: unselected-refused. A3 positive: runner-root-accepted; negative: ignored-refused. A4 positive: conda-executes; negative: conda-noop-refused. A5 positive: official-uv-syntax-matches; negative: unsupported-launcher-refused.
- Risk: agent-decided — cite the official `uv run` option reference beside the existing parser; preserve its behavior and all existing test coverage in `test_selection_finalize.py`.

**W2-01 Honor configured pytest file names**  after: W1-01  acceptance: 3
- Files: `loom-code/scripts/loom_checker/probes.py`, `loom-code/tests/test_selection_finalize.py`
- Test: A3 positive: configured-name-finalizes; negative: configured-name-ignored-refused.
- Risk: agent-decided — remove the fixed filename prefilter because pytest collection is authoritative; preserve the existing root, ignored-path, and direct-command coverage in `test_selection_finalize.py` and `test_adversarial_probe_cap_coverage.py`.

## Simplicity check
- none found

## Questions asked
① — what — 我已把新意圖草稿限於完成原本的測試轉正修正：保留先前四條驗收，只補齊環境命令的官方依據並重新審查；Claude 呼叫方式與 Codex 探索問題不納入。審查通過後沿用你先前授權，非強制推送並開 Ready PR，合併另行決定。這個範圍符合你的意思嗎？

## Risks
1. The original functional behavior already passed the full package suite and clean-copy acceptance, but content-bound review must run again on the new confirmed intent.
2. Claude Code's session limit blocked the previous outside review; this plan does not alter that executor or assume its current availability.
3. An additional Codex review of PR #89 reproduced a runner-backed false refusal when `python_files` changes pytest's file naming; W2-01 closes that Acceptance #3 defect in the same branch.
