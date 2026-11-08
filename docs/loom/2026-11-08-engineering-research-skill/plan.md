# Engineering research — plan
intent: 2026-11-08-engineering-research-skill@da402f1b
spec: docs/loom/2026-11-08-engineering-research-skill/spec.md@fa5fcaf7
charter: 1.1

## Task DAG

### Wave 0 — Research capability

**W0-01 Promote question-scoped research instructions** after: none acceptance: 3,4,5,6,7
- Files: loom-workflow/skills/engineering-research/, loom-workflow/tests/engineering-research/
- Test: A3 positive: verified-evidence; negative: false-artifact. A4 positive: mixed-evaluation; boundary: direct-fact. A5 positive: continuation; boundary: changed-conditions. A6 positive: saved-record; negative: no-write. A7 positive: source-path; negative: graph-causality.
- Risk: agent-decided — Follow spec REQ-3 through REQ-7; preserve frozen revision-5 inputs and verify real research outputs rather than prose-only presence.

### Wave 1 — Discovery and finishing ownership

**W1-01 Integrate optional routing and preservation** after: W0-01 acceptance: 1,2,8,9
- Files: loom-workflow/skills/, loom-workflow/tests/, loom-design/skills/capture-intent/SKILL.md, loom-design/skills/write-spec/SKILL.md, loom-code/skills/write-plan/SKILL.md, loom-code/skills/build/SKILL.md, loom-code/skills/ship/SKILL.md, tests/
- Test: A1 positive: isolated-loader; negative: absent-plugin. A2 positive: consequential-small-check; negative: routine-lookup. A8 positive: merged-consented; negative: unpublished-unconsented. A9 positive: actual-record-readback; boundary: untested-host-disclosure.
- Risk: agent-decided — Follow spec REQ-1, REQ-2, REQ-8, REQ-9; use skill-name delegation and isolated fixture Vaults, preserving existing user installations and tests.

### Wave 2 — Registry and release integration

**W2-01 Register and release the bounded capability** after: W1-01 acceptance: 9
- Files: loom-code/contract/manifest.yaml, docs/loom/evidence/mechanisms.yaml, loom-code/scripts/check_mechanisms.py, loom-code/tests/, loom-workflow/tests/scripts/test_skill_count.py, README.md, CHANGELOG.md, **/plugin.json
- Test: A9 positive: synchronized-release; negative: registry-drift. Run manifest synchronization and complete declared package inventory; verify executable budget population and declared exceptions.
- Risk: agent-decided — Follow spec REQ-9; bump affected plugins minor for guidance/contracts, synchronize derived manifests, changelogs and README pins, and admit the counted tool explicitly without a standalone exemption.

## Simplicity check
- none found

## Questions asked
1 — what — 這份範圍與發布安排，可以確認嗎？

## Risks
1. Research guidance is probabilistic; routing and workflow benchmarks must distinguish actual loads from self-reports and explicit invocation from automatic discovery. No universal improvement claim follows from the prototype results.
2. Optional Vault preservation crosses a filesystem/privacy boundary; use temporary fixtures and explicit per-instance consent. No live Vault writes, automatic merge or installed-plugin changes are authorized by this implementation.
3. Existing frozen trial/dogfood directories are pre-existing untracked evidence. Preserve them unchanged; publish only evidence required to support this change, with explicit raw-evidence provenance and limits rather than silently bulk-staging historical sessions.
4. The new counted skill and contract tool increase the mechanism population; record budget-exception lines and executable admission updates, retaining every earlier population and budget regression case.
5. The spec received independent spec+adversarial PASS against da402f1b; engineering exemption applies to decision point ②, and the plan is agent-decided. The next user decision is acceptance after publication checks.
