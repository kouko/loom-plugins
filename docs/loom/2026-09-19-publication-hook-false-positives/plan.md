# Plan: 2026-09-19-publication-hook-false-positives
intent: 2026-09-19-publication-hook-false-positives@HEAD
charter: 1.0

## Current State Evidence
- Forward: loom-code/scripts/loom_checker/command_handlers/push.py — contains _shell_c_argument and contains_pr_merge functions needing fixes
- Forward: loom-code/scripts/loom_checker/rule_checks/push.py — contains _heredoc_executes_body function needing improvement
- Forward: loom-code/scripts/test_adversarial_heredoc_carve_out.py — existing adversarial test covering the issues
- Reverse: No reverse dependencies identified
- Error: No error paths
- Data: No data files
- Boundary: No boundary cases

## Task DAG
### Wave 0 — implementation and testing (already partially done)
**W0-01 Fix shell detection for bundled flags**  after: none  acceptance: 1
- Files: loom-code/scripts/loom_checker/command_handlers/push.py
- Test: A1 positive: _shell_c_argument correctly identifies -lc, -euxc, -cl as shell commands; negative: misses bundled flags
- Risk: Low — isolated logic change; verified by adversarial tests

**W0-02 Improve heredoc body execution detection**  after: none  acceptance: 2
- Files: loom-code/scripts/loom_checker/rule_checks/push.py
- Test: A2 positive: _heredoc_executes_body considers full pipeline; negative: only checks command word
- Risk: Low — focused logic improvement; verified by adversarial tests

**W0-03 Run adversarial tests to verify fixes**  after: W0-01,W0-02  acceptance: 3
- Files: loom-code/scripts/test_adversarial_heredoc_carve_out.py
- Test: A3 positive: all adversarial tests pass; negative: any test fails
- Risk: Low — validation only; no code changes

## Questions asked
① — engineering — Fix publication hook false positives for heredoc carve-out cases; is the current approach of improving shell detection and heredoc analysis sufficient?

## Risks
- None — changes are localized to shell command recognition logic and verified by comprehensive adversarial test suite