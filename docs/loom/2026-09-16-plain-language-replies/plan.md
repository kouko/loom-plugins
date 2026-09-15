# Keep loom agents' replies in plain words, literal, and shaped as tables or diagrams — plan
intent: 2026-09-16-plain-language-replies@63bd57c5
spec: docs/loom/2026-09-16-plain-language-replies/spec.md
charter: 1.0

Current state evidence lives in the spec (`## Current state evidence`); each task's Risk line points at the spec by REQ id.

## Task DAG
<!-- When a spec requirement changes after this commit, the un-landed
     tasks it touches are replaced and the reason is named in the commit
     message. Landed tasks stay as they are. -->

### Wave 1 — per-turn reminder

**W1-01 Card carries plain-language rules and fires every turn on Claude Code**  after: none  acceptance: 1, 2, 4, 5
- Files: `loom-workflow/skills/loom-visualization/assets/trigger-card.md`, `loom-workflow/skills/loom-visualization/assets/trigger-card-coexist.md`, `loom-workflow/hooks/visualization-card`, `loom-workflow/hooks/hooks.json`, `loom-workflow/scripts/test_visualization_card_hook.py`, `loom-workflow/scripts/test_adversarial_visualization_card_hosts.py`, `loom-workflow/rules/AGENTS.md`, `scripts/test_sync_codex_manifests.py`
- Test: A1 positive: prompt-submit-emits-card-with-four-rules; negative: sessionstart-no-longer-registered. A2 positive: coexist-card-one-diagram-trigger; negative: full-card-not-emitted-when-toolkit-active. A4 positive: agy-rule-equals-new-card; negative: stale-rule-fails-sync-check. A5 positive: malformed-stdin-exits-zero-with-card; boundary: unreadable-card-exits-zero-empty.
- Risk: both cards must stay within the existing 150-word cap; wording is compressed rather than the cap raised. REQ-1, REQ-2, REQ-4, REQ-5. agent-decided.

**W1-02 Codex manifest moves to every turn and mechanism ids are renamed**  after: W1-01  acceptance: 3, 11
- Files: `loom-workflow/hooks/hooks-codex.json`, `scripts/test_loom_plugin_install_layout.py`, `docs/loom/evidence/mechanisms.yaml`, `loom-workflow/scripts/test_adversarial_hook_probes.py`
- Test: A3 positive: codex-prompt-submit-canonical-key-only; negative: codex-extra-keys-rejected. A11 positive: mechanism-count-unchanged-after-rename; negative: stale-sessionstart-id-flagged-stale.
- Risk: Codex users must re-trust the moved hook; the command string stays unchanged apart from the event. REQ-3, REQ-11. agent-decided.

### Wave 2 — references

**W2-01 Plain-language reference with option rule, conversation tables and table rules**  after: W1-02  acceptance: 6, 7, 8
- Files: `loom-workflow/skills/loom-visualization/references/plain-language.md`, `loom-workflow/skills/loom-visualization/SKILL.md`, `loom-workflow/scripts/test_loom_visualization_compaction.py`, `loom-workflow/skills/loom-visualization/scripts/test_references.py`
- Test: A6 positive: guide-has-seven-rules-and-rewrite-steps; negative: guide-without-metaphor-check-fails. A7 positive: option-rule-two-alternatives-and-recommendation; boundary: yes-no-confirmation-asked-directly. A8 positive: eight-conversation-situations-present; negative: missing-table-rules-section-fails.
- Risk: the card names this file, so it follows the card; no gate marker is added, which would count a mechanism. REQ-6, REQ-7, REQ-8. agent-decided.

**W2-02 Domain table collections and routing**  after: W2-01  acceptance: 8, 9
- Files: `loom-workflow/skills/loom-visualization/references/tables-software.md`, `loom-workflow/skills/loom-visualization/references/tables-design.md`, `loom-workflow/skills/loom-visualization/references/tables-business.md`, `loom-workflow/skills/loom-visualization/SKILL.md`, `loom-workflow/skills/loom-visualization/scripts/test_references.py`
- Test: A8 positive: all-research-usages-present-per-domain; negative: duplicated-usage-points-to-general-set. A9 positive: routing-names-document-types-per-collection; negative: conversation-reply-routes-to-general-only.
- Risk: research lives in the intent's evidence vault notes; references keep source URLs and uncertainty markers, never repository development records. REQ-8, REQ-9. user-decided.

**W2-03 Cold-read evidence for rewrites, decisions and routing**  after: W2-02  acceptance: 6, 7, 9
- Files: `docs/loom/2026-09-16-plain-language-replies/evidence/coldread/rewrite.txt`, `docs/loom/2026-09-16-plain-language-replies/evidence/coldread/decision.txt`, `docs/loom/2026-09-16-plain-language-replies/evidence/coldread/routing.txt`
- Test: A6 positive: three-zh-complaints-rewritten-plain-and-literal; negative: metaphor-in-rewrite-flagged. A7 positive: how-question-gets-alternatives-and-recommendation; boundary: publish-confirmation-stays-yes-no. A9 positive: progress-reply-reads-general-only; negative: incident-report-reads-software-only.
- Risk: fresh agents vary run to run; Chinese inputs also show whether the English card pulls replies into English. REQ-6, REQ-7, REQ-9. agent-decided.

**W2-04 Guide fixes from cold-read failures and re-recorded runs**  after: W2-03  acceptance: 6, 7
- Files: `loom-workflow/skills/loom-visualization/references/plain-language.md`, `loom-workflow/skills/loom-visualization/scripts/test_references.py`, `docs/loom/2026-09-16-plain-language-replies/evidence/coldread/rewrite.txt`, `docs/loom/2026-09-16-plain-language-replies/evidence/coldread/decision.txt`
- Test: A6 positive: rewrite-opens-with-conclusion-and-keeps-facts; negative: announcing-or-heading-opener-flagged. A7 positive: each-missed-alternative-included-or-ruled-out; boundary: reply-keeps-user-script.
- Risk: W2-03 runs opened with a rewrite announcement or heading, dropped the lead news and skipped the do-nothing check; the guide, not the card, is changed. REQ-6, REQ-7. agent-decided.

### Wave 3 — release

**W3-01 Install limits, card timing in READMEs, changelog and versions**  after: W2-04  acceptance: 10, 11
- Files: `loom-workflow/README.md`, `loom-workflow/README.ja.md`, `loom-workflow/README.zh-TW.md`, `loom-workflow/CHANGELOG.md`, `loom-workflow/plugin.json`, `loom-workflow/.claude-plugin/plugin.json`, `loom-workflow/.codex-plugin/plugin.json`
- Test: A10 positive: readmes-state-unreached-hosts-and-loom-code-only; negative: sessionstart-wording-removed. A11 positive: package-suite-and-check-mechanisms-green; negative: version-mismatch-fails.
- Risk: minor release 5.3.0 because the card's delivery timing changes; no budget-exception line is needed while the count is unchanged. REQ-10, REQ-11. agent-decided.

### Wave 4 — adversary findings (probes at 4f1980ef)

**W4-01 Polarity-checked rule tests and fail-safe hook dependencies**  after: W3-01  acceptance: 1, 5, 6, 7, 10
- Files: `loom-workflow/scripts/test_visualization_card_hook.py`, `loom-workflow/skills/loom-visualization/scripts/test_references.py`, `loom-workflow/scripts/test_readme_card_timing.py`, `loom-workflow/hooks/visualization-card`, `loom-workflow/hooks/hooks.json`, `loom-workflow/hooks/hooks-codex.json`, `scripts/test_loom_plugin_install_layout.py`
- Test: A1 positive: affirmative-card-rule-accepted; negative: negated-card-rule-rejected. A5 positive: hung-settings-file-finishes-within-timeout; boundary: undecodable-plugin-root-card-falls-back. A6 positive: affirmative-metaphor-ban-accepted; negative: metaphor-ban-removed-rejected. A7 positive: affirmative-option-and-yes-no-rules-accepted; negative: negated-option-rule-rejected. A10 positive: per-turn-readme-wording-accepted; negative: localized-session-start-wording-rejected.
- Risk: phrase-presence tests let a rule flipped to its opposite pass; every committed probe must pass before hand-off. agent-decided.

**W4-02 In-cell visuals and time-as-column guidance from the earlier table research**  after: W4-01  acceptance: 8
- Files: `loom-workflow/skills/loom-visualization/references/plain-language.md`, `loom-workflow/skills/loom-visualization/scripts/test_references.py`
- Test: A8 positive: in-cell-visuals-and-time-axis-guidance-present; negative: removed-in-cell-section-fails.
- Risk: the blind run found the earlier research's in-cell micro-visualisation rules and time-as-column forms missing; only the table-rules section grows, so rewrite trials stay valid. agent-decided.

**W4-03 Card routes decision questions to the guide; three missing table criteria**  after: W4-02  acceptance: 1, 7, 8
- Files: `loom-workflow/skills/loom-visualization/assets/trigger-card.md`, `loom-workflow/skills/loom-visualization/assets/trigger-card-coexist.md`, `loom-workflow/rules/AGENTS.md`, `loom-workflow/scripts/test_visualization_card_hook.py`, `loom-workflow/skills/loom-visualization/references/plain-language.md`, `loom-workflow/skills/loom-visualization/scripts/test_references.py`
- Test: A1 positive: both-cards-name-decision-questions-for-guide; negative: card-over-150-words-fails. A7 positive: how-question-trial-reads-guide; boundary: yes-no-trial-stays-direct. A8 positive: three-earlier-criteria-present; negative: removed-criterion-fails.
- Risk: the blind run saw a how-question skip the guide because the card only routed plainer explanations; the wording is compressed within the existing cap. agent-decided.

### Wave 5 — closing review round 1 findings (reviewed 141fa27c)

**W4-04 Inline decision rule in the card; guide, routing and citation fixes**  after: W4-03  acceptance: 1, 7, 8, 9
- Files: `loom-workflow/skills/loom-visualization/assets/trigger-card.md`, `loom-workflow/skills/loom-visualization/assets/trigger-card-coexist.md`, `loom-workflow/rules/AGENTS.md`, `loom-workflow/scripts/test_visualization_card_hook.py`, `loom-workflow/skills/loom-visualization/references/plain-language.md`, `loom-workflow/skills/loom-visualization/SKILL.md`, `loom-workflow/skills/loom-visualization/references/tables-business.md`, `loom-workflow/skills/loom-visualization/scripts/test_references.py`
- Test: A1 positive: both-cards-state-inline-decision-rule; negative: card-over-150-words-fails. A7 positive: rule-five-example-is-a-table; negative: prose-option-example-rejected. A8 positive: rule-one-key-value-exception-stated; negative: unsupported-nutt-figures-absent. A9 positive: routing-rows-name-all-held-document-types; negative: raci-routed-to-software-only.
- Risk: routing decisions to the guide was fixed once and still fired for 1 of 3 how-questions; the rule moves inline instead of another routing sentence. REQ-1, REQ-7, REQ-9. agent-decided.

## Questions asked
① — what — 提醒要在什麼時機送：叫用 skill 後、每次你送出訊息時、或寫進各階段格式說明？
① — what — 「怎麼跟使用者說話」只在 loom 流程裡生效，還是 loom 所有工具都要生效？
① — what — 只放 loom-workflow 可以嗎，還是 loom-code 與 loom-workflow 兩邊都放？
① — what — 完整版要新增一個 skill，還是放進 loom-visualization 當參考檔？
① — what — 對話情境表格範例要併進這次，還是另開一個改動？
① — what — 表格集照「一般情境＋軟體／設計／商業三檔」分層並補上 09-04 的研究，可以嗎？
① — what — 決策選項規則（是非題直接問、至少兩個可行做法並標推荐、檢查常被漏掉的選項）這樣可以嗎？
① — consequence — 接受複雜度檢驗的縮小方案嗎？三類專業表格集要延後，還是這次收錄？
① — consequence — 確認 intent：每輪多用 token、Codex 要重新信任 hook、只裝 loom-code 收不到、通過審查後自動 push 並開 Ready PR？

## Risks
1. The reminder now costs roughly 150–200 tokens on every turn wherever loom-workflow is installed; user-decided when accepting the reduced shape.
2. The installed loom-code 3.7.0 policy script still requires a lane field; Build passes `full`, the default after lanes were removed. agent-decided.
3. Acceptance 6, 7 and 9 rest on fresh-agent behaviour, which is not deterministic; recorded runs are evidence, not a guarantee.
4. An English-only card may pull replies in Chinese conversations toward English; W2-03 uses Chinese inputs to observe it. user-decided shape.
5. user-decided — the domain collections ship now although the complexity critique judged them deferrable.
6. Cold-read rewrites still change or drop facts after two guide rounds; the fresh reader lacks the original context, so no third prose round. Reported, not hidden. agent-decided.
