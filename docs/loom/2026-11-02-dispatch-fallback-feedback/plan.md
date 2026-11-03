# Dispatch fallback feedback — plan
intent: 2026-11-02-dispatch-fallback-feedback@80861e57
spec: docs/loom/2026-11-02-dispatch-fallback-feedback/spec.md@a4136c8a
charter: 1.1

## Task DAG
### Wave 1 — Complete the resolver boundary
**W1-01 Truthful fallback feedback** acceptance: 1,2,3
- Files: `loom-code/scripts/dispatch_profile.py` (entry: resolve), `loom-code/references/dispatch-profile.md`, `loom-code/tests/test_dispatch_profile_resolver.py`
- Test: A1 positive: fallback-success; boundary: all-fallback-origins. A2 positive: verified-native-pair; negative: malformed-explicit-pair. A3 positive: fallback-malformed-retry; boundary: exhausted-or-no-escalation. Run resolver tests.
- Risk: agent-decided — REQ-1–3 preserve all existing resolver cases and widen symbolic feedback only; existing tests: test_dispatch_profile_resolver.py. Retain unknown labels and budget; no native-value arithmetic.

### Wave 2 — Clarify continuation responsibility
**W2-01 Separate review work and changed requirements** after: W1-01 acceptance: 4,6
- Files: `loom-code/skills/closing-review/SKILL.md`, `loom-code/skills/build/SKILL.md`, `loom-design/skills/capture-intent/SKILL.md`, `loom-code/skills/write-plan/references/confirm-intent.md`, `loom-code/tests/test_simplified_station_text.py`
- Test: A4 positive: conforming-defect-verdict; negative: excluded-execution. A6 positive: substantive-reconfirmation; boundary: wording-or-same-failed-task. Run simplified-station tests; independently exercise agent decisions during acceptance testing.
- Risk: agent-decided — REQ-4/6 preserve intent byte checks and existing bounded-episode gate; clarification replaces overbroad reset wording. Existing tests: test_simplified_station_text.py; preserve tested limits. Semantic behavior requires fresh-agent evidence.

### Wave 3 — Release the verified contract
**W3-01 Synchronize release metadata** after: W2-01 acceptance: 5
- Files: `loom-code/{.claude-plugin/plugin.json,CHANGELOG.md,README*.md}`, `loom-design/{.claude-plugin/plugin.json,CHANGELOG.md,README*.md}`, `README.md`, `loom-code/tests/test_write_plan_station_text.py`, `loom-design/tests/spec/test_capture_intent_contract.py`, derived manifests via `scripts/sync_codex_manifests.py`
- Test: A5 positive: synchronized-release; boundary: stale-version-pin. Run release metadata and manifest sync checks; end-of-Build package suite; independent isolated acceptance testing validates actual feedback/count continuity before finalization.
- Risk: agent-decided — REQ-5 bumps loom-code to 3.57.0 and loom-design to 2.20.0 before review. Update existing version assertions if pinned. No installed plugin update or external execution.

### Wave 4 — Repair an earned adversarial finding
**W4-01 Recheck inheritance for a new retry** after: W3-01 acceptance: 1,3
- Files: `loom-code/scripts/dispatch_profile.py`, `loom-code/references/dispatch-profile.md`, `loom-code/tests/test_dispatch_profile_resolver.py`
- Test: A1 positive: past-success-retains-label; boundary: changed-host-guarantee. A3 positive: stable-guarantee-retry; boundary: retry-uses-current-guarantee. Run resolver tests and the adversary's unchanged RED program.
- Risk: agent-decided — REQ-1/3 distinguish past observation from future invocation; adversary exposed a stale-guarantee overclaim. Preserve existing resolver coverage; update only the retry test's stable-host premise, not assertion strength.

**W4-02 Graduate earned inheritance regression** after: W4-01 acceptance: 5
- Files: `docs/loom/2026-11-02-dispatch-fallback-feedback/evidence/probes/test_retry_inheritance_truth.py`, `loom-code/tests/test_dispatch_fallback_inheritance.py`
- Test: A5 positive: byte-identical-suite-program; boundary: original-store-path-absent. Run graduated program and full suite; retain actual RED and move evidence.
- Risk: agent-decided — REQ-5 moves the adversary's exact program without editing it, before review finalization. No new probe or harness; do not recreate a removed store copy.

## Simplicity check
- none found

## Questions asked
① — what — 以上是否就是你要的完整範圍？

## Risks
1. Shared resolver data is an agent-consumed contract. Boundary tests preserve explicit profiles and all fallback origins; structural tests alone do not prove host behavior.
2. Independent acceptance testing must exercise completed success, permitted malformed retry, legal stop, normal fix-review and substantive versus wording-only intent changes using fresh agents and isolated repositories. Retain raw inputs/outputs and actual counters.
3. Preserve existing external-review receipts and authorization. Prior Claude consultation reviewed the draft problem only; it is not authorization for another execution or a closing verdict.
4. No new mechanism, semantic classifier, counter ledger or attestation schema. Extend existing resolution and bounded-episode obligations. Before implementation, search all touched content and affected Acceptance surfaces for the same defect classes.
5. Earlier untracked experiment evidence is retained as historical material, not current acceptance evidence. Commit only relevant sanitized records; archive redundant controller copies outside the worktree without deleting user session data.
