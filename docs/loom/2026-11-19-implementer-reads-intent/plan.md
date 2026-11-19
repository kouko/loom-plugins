# Implementer reads the confirmed intent — plan
intent: 2026-11-19-implementer-reads-intent@8974e66
charter: 1.1

## Current State Evidence
- Forward: `loom-code/agents/implementer.md` "### Resource paths" lists plan, spec, baseline, repo root and test command; no intent path.
- Reverse: Build hands the adversary the intent path (`loom-code/skills/build/SKILL.md` step 2 of the end-of-Build checks); reviewer and acceptance tester read intent too.
- Error: no failure recorded; risk is an implementer working from a narrow task while judges use the goal (intent Problem).
- Data: plan header already carries `intent: <change-id>@<sha>` (`contract/templates/plan.md` line 2); implementer is never told to read it.
- Boundary: skipped-plan path already passes intent (`implementer.md` "When the station says plan or spec is skipped"; build "When plan is skipped").

## Task DAG
One wave: the contract text and its pin tests change together; release metadata follows once the contract is final.

**W1-01 Point the implementer at the intent without widening its task**  after: none  acceptance: 1, 2, 3, 4
- Files: `loom-code/agents/implementer.md`, `loom-code/tests/test_build_mechanical_checks.py`
- Test: A1 positive: resource-paths-name-intent; negative: intent-line-removed-fails. A2 positive: intent-does-not-widen-task; negative: scope-sentence-removed-fails. A3 positive: skipped-plan-handoff-retained; boundary: skipped-plan-sentence-unchanged. A4 positive: complete-package-suite-passes; boundary: existing-implementer-pins-pass.
- Risk: agent-decided — one `intent:` path line plus one sentence tying it to Role contract 1 (no widening; extra work reported under DONE_WITH_CONCERNS). Existing implementer pins in this test file are preserved, not narrowed.

**W1-02 Minor release metadata**  after: W1-01  acceptance: 4
- Files: `loom-code/.claude-plugin/plugin.json`, derived release manifests, `loom-code/CHANGELOG.md`, `README.md`, `loom-code/README*.md`, `loom-code/tests/test_write_plan_station_text.py`
- Test: A4 positive: release-metadata-synchronized-3.85.0; boundary: readme-versions-match-manifest.
- Risk: agent-decided — minor 3.85.0 because an agent dispatch input gains a field; CHANGELOG entry, README versions, CURRENT_VERSION pin, manifests derived via scripts/sync_codex_manifests.py --all.

## Simplicity check
- none found

## Questions asked
① — what — 這樣是你要的嗎？

## Risks
1. Telling the implementer about the goal could invite out-of-task edits; the new sentence binds the intent to Role contract 1, so extra work is reported, never done.
2. No with/without trial measures output quality; intent Out of scope records this, so the change claims delivery of the goal only.
