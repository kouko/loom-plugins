# Context-preserving intent confirmation — plan
intent: 2026-11-02-context-preserving-explanations@2cfaae5e
charter: 1.1

## Current State Evidence
- Forward: `loom-design/skills/capture-intent/SKILL.md` Step 4 requires a plain-language Problem and Acceptance restatement before confirmation.
- Reverse: `loom-code/skills/write-plan/references/confirm-intent.md` duplicates decision point 1 for code-only installations.
- Error: `loom-design/skills/capture-intent/SKILL.md` Step 4's short fill-in example does not explicitly connect unfamiliar terms, present pain and consequences.
- Data: `loom-design/skills/capture-intent/test-prompts.json` contains behavioral prompts; `loom-workflow/skills/loom-visualization/references/plain-language.md` already requires preserving facts when simplifying wording.
- Boundary: `loom-design/skills/write-spec/SKILL.md` Step 3 and `loom-code/skills/closing-review/references/acceptance-test-report.md` own other decision points, excluded here.

## Task DAG

**W0-01 Preserve context without prescribing sentences** after: none acceptance: 1,2,3,4
- Files: `loom-design/skills/capture-intent/`, `loom-code/skills/write-plan/references/confirm-intent.md`, `loom-design/tests/spec/`, `loom-code/tests/`
- Test: A1 positive: connected-background; negative: label-only. A2 positive: varied-expression; negative: mandatory-script. A3 positive: brief-familiar; boundary: unfamiliar-concepts. A4 positive: outcome-confirmation; negative: technical-approval.
- Risk: agent-decided — update both owners of decision point 1; use content checks and optional examples, preserving intent altitude, publication disclosure and the existing single confirmation stop.

**W0-02 Synchronize release metadata** after: W0-01 acceptance: 1,2,3,4
- Files: `loom-design/.claude-plugin/plugin.json`, `loom-code/.claude-plugin/plugin.json`, `loom-design/CHANGELOG.md`, `loom-code/CHANGELOG.md`, `loom-design/README.md`, `loom-code/README.md`, `loom-code/tests/test_write_plan_station_text.py`
- Test: A1 positive: synchronized-release; negative: stale-version. A2 positive: synchronized-release; negative: stale-version. A3 positive: synchronized-release; negative: stale-version. A4 positive: synchronized-release; negative: stale-version.
- Risk: agent-decided — minor bumps for changed station guidance: loom-design 2.20.0 and loom-code 3.57.0; preserve existing release checks and rewrite current-version pins where required.

**W1-01 Repair unsupported additions and excessive workflow language** after: W0-02 acceptance: 1,2,3,4
- Files: `loom-design/skills/capture-intent/`, `loom-code/skills/write-plan/references/confirm-intent.md`, `loom-design/tests/spec/test_capture_intent_contract.py`, `loom-code/tests/test_write_plan_station_text.py`, `loom-design/CHANGELOG.md`, `loom-code/CHANGELOG.md`
- Test: A1 positive: supplied-scope; negative: deterministic-addition. A2 positive: flexible-expression; negative: fixed-script. A3 positive: proportionate-context; negative: invented-date. A4 positive: concrete-authorization; negative: technical-approval.
- Risk: agent-decided — repair unsupported additions across both owners, preserving existing coverage and word caps. Replace redundant affected prose instead of adding structure. The existing unpublished minor bumps remain; independent review and host evidence need renewal.

## Simplicity check
- none found

## Questions asked
1 — what — 確認這次要做到：各確認點的說明都保留理解所需的背景、名詞與結果，簡單事情仍簡短，且不增加確認次數嗎？

## Risks
1. user-decided — after industry research, scope is narrowed to decision point 1; fixed sentences are examples only. Product behavior confirmation and final acceptance remain unchanged.
2. agent-decided — no new skill, checker rule, schema field or mandatory conversation section; reuse existing references and tests, adding focused examples only if necessary.
3. agent-decided — prose assertions cannot establish actual conversational behavior; fresh-context exercises must cover unfamiliar concepts, simple requests, and a user's detailed follow-up.
4. agent-decided — sources motivate the design, not a claim of proven effectiveness: GOV.UK check-answers, Google conversation design, NHS SBAR, Google Cloud ADR and Atlassian DACI guidance were consulted.
5. user-decided — repair dogfood findings D1–D3, fix the harness and rerun six original scenarios plus two counterexamples; publication remains held. This corrects observed failures under existing Acceptance, without changing requested outcomes or restarting review budgets.
6. agent-decided — defect class: unsupported additions during explanation, observed as deterministic-selection guarantees and an invented date fallback. Both first-confirmation owners and all cumulative changed files were searched; internal publication jargon is repaired in the same affected paragraphs.
