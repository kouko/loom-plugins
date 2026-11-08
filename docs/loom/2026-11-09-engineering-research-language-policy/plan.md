# Evidence-led search languages — plan
intent: 2026-11-09-engineering-research-language-policy@c0a17318
spec: docs/loom/2026-11-09-engineering-research-language-policy/spec.md@6c9789a9
charter: 1.1

## Task DAG

### Wave 1 — Supplemental evidence before adoption

**W1-01 Observe two genuine evidence gaps and preserve evidence** after: none acceptance: 4,5
- Files: docs/loom/2026-11-09-engineering-research-language-policy/evidence/
- Test: A4 positive: Chinese-and-Korean-real-gaps; boundary: adequate-alternative-stopping. A5 positive: frozen-evidence-integrity; boundary: retained-disagreement-and-unobserved-paths.
- Risk: agent-decided — REQ-4–5: neutral public tasks and two blind judges avoid language prompting; immutable archives preserve original results without shipping experimental runners. Existing first-trial data remains unchanged.

### Wave 2 — Adopt the bounded guidance

**W2-01 Integrate supported source-language guidance** after: W1-01 acceptance: 1,2,3,6
- Files: loom-code/skills/engineering-research/references/source-policy.md, loom-code/tests/engineering-research/test_package.py
- Test: A1 positive: separate-English-Japanese; boundary: exact-identifiers. A2 positive: reuse-sufficient-evidence; boundary: no-language-quota. A3 positive: independent-Chinese-Korean; boundary: early-other-original-language. A6 positive: bundled-policy-load; boundary: existing-contracts-preserved.
- Risk: agent-decided — REQ-1–3,6: use frozen candidate prose only if evidence supports adoption; preserve existing test_package.py coverage and add only meaningful integration checks. No behavior outside source-language selection changes.

**W2-02 Synchronize the required release packet** after: W2-01 acceptance: 6
- Files: loom-code/.claude-plugin/plugin.json, loom-code/.codex-plugin/plugin.json, loom-code/plugin.json, loom-code/package.json, loom-code/CHANGELOG.md, loom-code/README.md, README.md, loom-code/tests/test_write_plan_station_text.py
- Test: A6 positive: synchronized-release-metadata; boundary: unchanged-other-plugin-versions.
- Risk: agent-decided — REQ-6: minor bump for station guidance, derived manifests via existing synchronizer; locate version pins before editing and preserve all unrelated release behavior. Include changelog entry and pin-test rewrite.

### Wave 3 — Correct the validation invocation

**W3-01 Correct the adversarial command declaration** after: W2-02 acceptance: 6
- Files: docs/loom/2026-11-09-engineering-research-language-policy/evidence/finalize-command-repair.md
- Test: A6 positive: supported-direct-pytest-wrapper; boundary: preserve-rejected-env-declaration.
- Risk: agent-decided — REQ-6: preserve the rejected declaration and use the existing uv-wrapped Python command directly; pass cache environment through the launcher. No product, program or approved requirement changes; retain the same review episode.

## Simplicity check

- none found

## Questions asked

1 — what — 請確認：補中文、韓文各一個真實證據缺口案例，再依結果把已討論的語言指引納入 engineering-research，保留充分即停止等例外及既有證據。是否同意在審查與測試通過後，非強制推送並建立 Ready PR？合併仍另由你驗收決定。

## Risks

1. agent-decided — Two supplemental observations cannot establish reliable triggering, causality or host compatibility. Report actual expansion separately from sufficient alternative evidence; retain unobserved paths.
2. agent-decided — All archived fixtures and queries are public technical material. Native agents only; no outside-host CLI invocation, private-data export, global installation or real Vault writes.
3. user-decided — Confirmed scope and automatic nonforce push/Ready PR on 2026-11-09. Merge requires separate acceptance. Engineering change skips product decision point ②.
4. agent-decided — The installed Python probe recognizer rejects an env-prefixed wrapper. Declare uv directly and inherit cache environment; preserve the failed finalization and rerun Build checks before same-reviewer Round 2. No counters or requirements reset.
