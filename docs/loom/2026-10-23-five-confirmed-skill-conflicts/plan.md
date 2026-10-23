# Five confirmed skill conflicts — plan
intent: 2026-10-23-five-confirmed-skill-conflicts@3c775f5f
spec: docs/loom/2026-10-23-five-confirmed-skill-conflicts/spec.md@9f331d9f
charter: 1.1

## Task DAG
### Wave 1 — repair existing instruction contracts
**W1-01 Preserve confirmed requirement order** after: none acceptance: 1
- Files: loom-design/skills/write-spec/SKILL.md, loom-design/tests/spec/test_write_spec_contract.py
- Test: A1 positive: acceptance-order-preserved; boundary: principles-still-constrain-content.
- Risk: REQ-1; agent-decided — widen existing spec contract tests without changing their existing cases; principles constrain decisions without reordering confirmed Acceptance.

**W1-02 Report actual confirmation status** after: W1-01 acceptance: 2
- Files: loom-design/skills/write-spec/SKILL.md, loom-design/tests/spec/test_write_spec_contract.py
- Test: A2 positive: product-confirmed-handoff; boundary: engineering-exempt-handoff.
- Risk: REQ-2; agent-decided — preserve existing product-only stop and contract tests; no new confirmation field.

**W1-03 Use working language for dbt titles** after: W1-02 acceptance: 3
- Files: loom-workflow/skills/dbt-model-style/SKILL.md, loom-workflow/tests/scripts/test_dbt_model_style_compaction.py
- Test: A3 positive: working-language-title; boundary: illustrative-chinese-example.
- Risk: REQ-3; agent-decided — preserve compaction and syntax cases, extend language guidance coverage without introducing language detection.

**W1-04 Initialize before first Record** after: W1-03 acceptance: 4
- Files: loom-workflow/skills/loom-memory/SKILL.md, loom-workflow/skills/loom-memory/references/operations.md, loom-workflow/skills/loom-memory/evals/record-timing.md, loom-workflow/tests/loom-memory/test_loom_memory.py, loom-workflow/tests/loom-memory/test_skill_contract.py
- Test: A4 positive: first-record-roundtrip; boundary: existing-corrupt-legacy-preserved.
- Risk: REQ-4; agent-decided — preserve initializer refusal tests; use existing CLI. Refresh the existing Record digest only after its independent cold-reader evaluation; preserve test_skill_contract.py coverage while updating retired wording.

### Wave 2 — source-grounded retrospective
**W2-01 Preserve and inspect retrospective sources** after: W1-04 acceptance: 5
- Files: loom-workflow/skills/skill-retro/, loom-workflow/skills/using-loom-workflow/SKILL.md, loom-workflow/README*, loom-workflow/tests/skill-retro/, loom-workflow/tests/project-retro/test_routing.py, tests/test_loom_skill_description_catalog.py
- Test: A5 positive: cross-host-source-roundtrip; boundary: unavailable-historical-source-and-cutoff.
- Risk: REQ-5; agent-decided — widen ingest/main/report/propose/cluster and prompt contract tests while preserving observable-only inputs, target isolation, promotion thresholds and proposal-only behavior; replace only assertions requiring the retired no-read rule.

### Wave 3 — release synchronization
**W3-01 Synchronize affected plugin releases** after: W2-01 acceptance: 1, 2, 3, 4, 5
- Files: loom-design/, loom-workflow/, README.md
- Test: A1 positive: release-metadata-synchronized; boundary: stale-pin-rejected. A2 positive: release-metadata-synchronized; boundary: stale-pin-rejected. A3 positive: release-metadata-synchronized; boundary: stale-pin-rejected. A4 positive: release-metadata-synchronized; boundary: stale-pin-rejected. A5 positive: release-metadata-synchronized; boundary: stale-pin-rejected.
- Risk: agent-decided — release metadata and existing version-pin tests only; minor versions from current baseline, .claude-plugin manifests own derived manifests; no unrelated runtime changes.

## Simplicity check
- Combine W1-01/W1-02 — declined: they share files but assert different obligations; separate task commits retain one defect-class assertion per implementer, as required by its contract.

## Questions asked
① — what — 確認以上就是你要的五筆修正，我就開始；這不包含發布或合併。

## Risks
1. Source access changes consumed contracts. Preserve optional legacy defaults and evidence attribution; a readable current file never proves historical loading. Synthetic fixtures establish transport and instructed behavior, not every live host's execution.
2. Current-session scope is the captured event snapshot. The runtime must not silently ingest appended events or internal reasoning; missing locators remain disclosed limitations.
3. Agent-decided — no new vendor or live user-session dispatch; source categories remain subject to existing approval. Publication and merge are excluded by the confirmed intent.
4. Complete package suite: uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q. Build adversarial checks and independent acceptance testing precede closing review.
