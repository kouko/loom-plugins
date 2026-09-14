# Close the small follow-ups left by the expert-mode change — plan
intent: 2026-09-15-expert-mode-follow-up-cleanup@7f416055
charter: 1.0

## Current State Evidence
- Forward: `PRINCIPLES.md:3` carries `pending-ratification:` for the non-negotiable 2 user-skipped-steps amendment.
- Reverse: `loom-code/skills/expert-mode/SKILL.md:86-88` binds confirmation and finalization to one session; publication and re-propose are unstated.
- Error: `loom-code/CHANGELOG.md:28` says only "confirmation and finalization must share the same Claude Code session".
- Data: `loom-code/contract/manifest.yaml:246-256` gives every `step_selection` step `requires: []`; `loom-code/scripts/loom_checker/selection.py:145-147` loops over them.
- Boundary: `loom-code/README.md:11`, `README.ja.md:11`, `README.zh-TW.md:9` show version 3.1.4; the manifests show 3.4.0.

## Task DAG
<!-- When a spec requirement changes after this commit, the un-landed
     tasks it touches are replaced and the reason is named in the commit
     message. Landed tasks stay as they are. -->

### Wave 1 — independent edits

**W1-01 Sign the non-negotiable 2 amendment**  after: none  acceptance: 1
- Files: `PRINCIPLES.md`, `scripts/test_principles_ratification.py`
- Test: A1 positive: ratified-by-names-2026-09-15-non-negotiable-2-amendment; negative: pending-ratification-line-absent.
- Risk: signing for kouko is legitimate only because his confirmation of this intent signs it; the commit cites that confirmation. user-decided.

**W1-02 Complete the session-limit wording in expert-mode**  after: none  acceptance: 2
- Files: `loom-code/skills/expert-mode/SKILL.md`, `loom-code/scripts/test_expert_mode_skill.py`
- Test: A2 positive: skill-names-publication-and-re-propose-in-new-session; negative: finalization-only-session-sentence-absent.
- Risk: pinned sentences must avoid negation words under the prose-pin rule; wording only, no behaviour change. agent-decided.

**W1-03 Remove the unused step dependency mechanism**  after: none  acceptance: 4
- Files: `loom-code/contract/manifest.yaml`, `loom-code/scripts/loom_checker/selection.py`, `loom-code/scripts/test_selection_store.py`
- Test: A4 positive: steps-carry-no-requires-and-propose-refuses-unknown-and-intent; boundary: skipping-any-single-step-validates.
- Risk: removing a contract field is a contract patch release; readers ignore undeclared keys, so older manifests stay readable. agent-decided.

### Wave 2 — release

**W2-01 Release notes, README versions and checks**  after: W1-01, W1-02, W1-03  acceptance: 2, 3, 5
- Files: `loom-code/CHANGELOG.md`, `loom-code/README.md`, `loom-code/README.ja.md`, `loom-code/README.zh-TW.md`, `loom-code/.claude-plugin/plugin.json`, `loom-code/.codex-plugin/plugin.json`, `loom-code/plugin.json`, `loom-code/scripts/test_write_plan_station_text.py`
- Test: A2 positive: changelog-names-publication-session-limit; negative: changelog-finalization-only-limit-superseded. A3 positive: three-readmes-match-manifest-version; boundary: readme-version-drift-fails. A5 positive: package-groups-and-check-mechanisms-green; negative: stale-release-pin-fails.
- Risk: patch release 3.4.1 keeps the released 3.4.0 entry intact and adds a new entry; sync tool keeps all three manifests equal. agent-decided.

## Questions asked
① — what — which follow-up items this change includes; kouko: "好"
① — what — restated intent, principles signature and automatic publication; kouko: "對"

## Risks
1. user-decided — kouko's confirmation at ① (2026-09-15) signs the non-negotiable 2 amendment exactly as merged in PR #13.
2. Main may advance before shipping; a local guard blocks agents from merging main, so kouko runs any needed merge himself.
3. No expert-mode behaviour changes; the adversarial probe file from the previous change must still pass unchanged.
