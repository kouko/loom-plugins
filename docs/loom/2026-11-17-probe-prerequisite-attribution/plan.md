# Prerequisite probe attribution — plan
intent: 2026-11-17-probe-prerequisite-attribution@335042b4
spec: docs/loom/2026-11-17-probe-prerequisite-attribution/spec.md@c2c8be31
charter: 1.1

## Task DAG
### Wave 1 — Attribution and regression boundary
**W1-01 Implement historical prerequisite attribution** after: none acceptance: 1,2,3,4,5,6
- Files: loom-code/scripts/loom_checker/probe_attribution.py (entry: prerequisite_probe_programs), loom-code/scripts/loom_checker/probes.py, loom-code/tests/test_probe_attribution.py, loom-code/tests/test_selection_finalize.py
- Test: A1 positive: inherited-five; negative: invalid-evidence; A2 positive: supplied-reuse; boundary: deduplication; A3 positive: unchanged; negative: changed-copy-revert; A4 positive: ordinary-tests; negative: six-current; A5 positive: full-scope; negative: false-auto-skip; A6 positive: immutable-evidence; negative: late-evidence. Extend existing finalization fixtures; RED first.
- Risk: agent-decided — REQ-1/3 evidence is untrusted until historical validation; REQ-5 keeps shared delta unchanged. Preserve and extend test_selection_finalize.py and test_adversarial_probe_cap_coverage.py coverage; no current attestation reuse.

### Wave 2 — Document and release
**W2-01 Align policy and release metadata** after: W1-01 acceptance: 4,6
- Files: loom-code/skills/closing-review/references/adversarial.md, loom-code/scripts/loom_checker/rules.py, loom-code/.claude-plugin/plugin.json, loom-code/CHANGELOG.md, loom-code/README*.md, README.md, loom-code/tests/test_write_plan_station_text.py, derived manifests via scripts/sync_codex_manifests.py
- Test: A4 positive: current-release-synchronized; negative: stale-version; A6 positive: evidence-unchanged; boundary: no-finance-execution. Reuse test_write_plan_station_text.py release synchronization and adversary protocol tests.
- Risk: agent-decided — REQ-4/6 documents existing five-program policy with verified attribution; minor release for changed contract prose. Name CHANGELOG entry and CURRENT_VERSION pin; regenerate manifests rather than editing derived files.

## Simplicity check
- none found

## Questions asked
① — what — 以上就是這次要做的範圍，對嗎？

## Risks
1. Historical validation may recursively inspect no-program evidence; ignore records without adversarial program executions, and preserve conservative fallback without exclusions.
2. Historical metadata can outlive the matching tree; validate at the recorded attestation revision, never compare an old digest with current HEAD and call it valid.
3. Reverted or copied files cannot inherit exclusions. The implementation must verify ancestry and uninterrupted path identity, preserving existing rename behavior separately.
4. Local-only delivery; no external model content transmission, installation or finance episode retry is authorized. Use native fresh-context reviewers and retain original records.
