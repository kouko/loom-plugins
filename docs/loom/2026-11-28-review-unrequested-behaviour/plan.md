# Reviewers flag behaviour the intent did not ask for — plan
intent: 2026-11-28-review-unrequested-behaviour@86d3e7d5d
charter: 1.1

## Current State Evidence
- Forward: `loom-code/agents/reviewer.md:13` reconciliation names omission, overclaim and contradiction against the intent, plan and text; no unrequested-addition case.
- Reverse: `loom-code/skills/closing-review/references/lenses.md:117` spec-conformance treats unrequired behaviour as a defect, but only under the spec lens, read only when a spec exists.
- Error: `loom-code/skills/closing-review/references/lenses.md:60` cross-task-coherence flags a task that did more than its title, not behaviour beyond the intent or inside its Out of scope.
- Data: `loom-code/tests/test_reviewer_mechanical_evidence.py` pins reviewer.md prose with `prose_pin.split_sentences`.
- Boundary: the acceptance tester (`loom-code/agents/acceptance-tester.md`) walks Acceptance lines only; out of scope per the intent.

## Task DAG

### Wave 1

**W1-01 Unrequested-behaviour clause in reviewer reconciliation**  after: none  acceptance: 1, 2
- Files: loom-code/agents/reviewer.md, loom-code/tests/test_reviewer_mechanical_evidence.py
- Test: A1 positive: clause-sentence-pinned; negative: clause-absent-fails-pin. A2 positive: clause-sentence-pinned; negative: clause-made-optional-fails-pin. All four are one whole-sentence pin entry; no new test function.
- Risk: one clause in the shared reconciliation paragraph so every lens applies it, not the code lens row alone; pin the sentence whole in the existing test module; agent-decided.

### Wave 2

**W2-01 Release metadata for loom-code 3.93.0**  after: W1-01  acceptance: 3
- Files: loom-code/.claude-plugin/plugin.json, loom-code/CHANGELOG.md, loom-code/README.md, loom-code/README.ja.md, loom-code/README.zh-TW.md, README.md, loom-code/tests/test_write_plan_station_text.py
- Test: A3 positive: release_sync; boundary: release_stale_pin. Existing pin `test_current_release_metadata_is_synchronized` covers it.
- Risk: minor bump (agent contract text) via SSOT then `sync_codex_manifests.py --all`, derived manifests committed; agent-decided.

## Simplicity check
- Add a new lens dimension — declined: findings already map to existing dimensions (deletion-first, omission, correctness); a dimension adds scoring surface for one clause.
- Put the clause in the code lens row only — declined: skill and docs lens changes, most of this repo's changes, would stay unchecked.
- One whole-sentence pin covers A1 and A2 instead of four separate tests (plan reviewer nit) — taken
- Merge W2-01 into W1-01 — declined: keeps release pin churn apart from the rule pin, as the prior change did.

## Questions asked
① — what — 回「好」確認 intent（含規則放在 reviewer 共用指引而非 code 清單、自動開 PR）(user: 「好 讓 codex 審一次」)

## Risks
1. No recorded incident grounds this rule; it is preventive. A reviewer may now raise findings on harmless incidental changes; the clause scopes it to behaviour, not wording.
2. user-decided — automatic publication after closing-review; merge stays a separate decision.
3. user-decided — Codex second reviewer at closing review, from the user's request 「好 讓 codex 審一次」.
user-decided — second-vendor selection-confirmed: codex
