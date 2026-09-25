# The probe-program cap counts only probes a change adds, not tests it moves — plan
intent: 2026-09-25-probe-cap-ignores-moved-tests@4af3ce72
charter: 1.0

## Current State Evidence
- Forward: `loom-code/scripts/loom_checker/probes.py:135-162` counts graduated programs as delta additions that the suite collects and that carry a `concern:` line.
- Reverse: `loom-code/scripts/loom_checker/reviewers.py:121-146` builds that delta with `git diff --no-renames`, so a moved file is a removal plus an addition.
- Error: PR #52 (2026-09-25) was refused with "9 probe programs … at most 5"; eight were renamed graduated probes, one was new.
- Data: `probes.py:79-100` `suite_collects` accepts any file under a declared suite directory, including skipped `tests/local/` folders.
- Boundary: `reviewers.py` delta also feeds the reviewer floor and narrow-change rules, which must keep reading renames as add plus remove.

## Task DAG

### Wave 0 — the count

**W0-01 Exclude moved tests and local-only folders from the probe count**  after: —  acceptance: 1, 2, 3, 5
- Files: `loom-code/scripts/loom_checker/probes.py`, `loom-code/tests/test_adversarial_probe_cap_coverage.py`
- Test: A1 positive: renamed-concern-tests-not-counted; negative: rename-plus-edit-into-new-probe-counted. A2 positive: new-probe-counted; boundary: copied-probe-under-new-name-counted. A3 positive: tests-local-program-not-graduated; negative: tests-program-still-graduated. A5 positive: rules-26; negative: delta-callers-unchanged.
- Risk: rename detection stays local to the probe count (git's rename pairing over the same base), so reviewer floor and narrow delta keep `--no-renames`; agent-decided.

### Wave 1 — record and release

**W1-01 Memory entry and minor release 3.15.0**  after: W0-01  acceptance: 4, 5
- Files: `docs/loom/memory/moving-graduated-probes-used-to-trip-the-probe-cap.md`, `docs/loom/memory/index.md`, `loom-code/plugin.json`, `loom-code/.claude-plugin/plugin.json`, `loom-code/.codex-plugin/plugin.json`, `loom-code/CHANGELOG.md`, `loom-code/tests/test_write_plan_station_text.py`, `README.md`
- Test: A4 positive: memory-entry-indexed-and-valid; negative: index-hand-merged-detected. A5 positive: versions-synchronized-3.15.0; negative: check-mechanisms-not-raised.
- Risk: minor because a checker rule's recomputation changes; loom-code READMEs bumped in the same commit though not listed for the eight-entry cap; agent-decided.

## Questions asked
① — what — 好
① — done — 對

## Risks
1. A copy of an existing probe under a new name looks like a rename to git; the count must treat a pair as a move only when the old path left the branch.
2. The behaviour is checker logic, so the acceptance test runs finalize-review in throwaway repositories with moved and new probes rather than reading prose.
