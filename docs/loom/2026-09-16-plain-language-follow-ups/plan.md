# Close the follow-ups left by the plain-language reminder change — plan
intent: 2026-09-16-plain-language-follow-ups@c4fe0e68
charter: 1.0

## Current State Evidence
<!-- each bullet ≤30 words (checker rule plan.field-caps) -->
- Forward: `loom-workflow/scripts/test_visualization_card_hook.py:433` and `:442` assert coexist-card meaning with a bare `any(...)`, so a negated sentence keeps every required token.
- Reverse: the same file defines `NEGATION` at `:277` and applies it at `:293` and `:372`, so the guard to copy already exists beside the two gaps.
- Error: `docs/loom/2026-09-16-plain-language-replies/evidence/probes/test_probe_prose_gate_mutants.py:54-61` holds three mutants; none targets the coexist-only markdown-table or `align.py` sentences.
- Data: the old card name survives in `loom-workflow/README.md:144`, `README.ja.md:138`, `README.zh-TW.md:133`, `.codex-plugin/plugin.json:31`, `hooks/visualization-card:2`; changelog hits are history.
- Boundary: `loom-code` pins 3.7.0 at three `plugin.json:3` files, root `README.md:17` and `:131`, three plugin READMEs; `test_write_plan_station_text.py:467` asserts they agree.

## Task DAG
<!-- When a spec requirement changes after this commit, the un-landed
     tasks it touches are replaced and the reason is named in the commit
     message. Landed tasks stay as they are. -->

### Wave 1 — card guards and the inline check

**W1-01 Negation guard on the two loosened coexist assertions**  after: none  acceptance: 1
- Files: `loom-workflow/scripts/test_visualization_card_hook.py`, `docs/loom/2026-09-16-plain-language-replies/evidence/probes/test_probe_prose_gate_mutants.py`
- Test: A1 positive: negated-coexist-sentence-fails-card-tests; negative: affirmative-coexist-sentence-still-passes.
- Risk: the probe file is the previous change's committed adversarial program; the new mutant extends `CARD_MUTANTS` and every existing probe must still pass. agent-decided.

**W1-02 Cards state the missed-alternatives check inline**  after: W1-01  acceptance: 6
- Files: `loom-workflow/skills/loom-visualization/assets/trigger-card.md`, `loom-workflow/skills/loom-visualization/assets/trigger-card-coexist.md`, `loom-workflow/rules/AGENTS.md`, `loom-workflow/scripts/test_visualization_card_hook.py`
- Test: A6 positive: both-cards-name-the-three-missed-alternatives; boundary: both-cards-stay-within-150-words.
- Risk: the cards sit at 148 and 150 words, so every added word is trimmed from non-rule wording; rules 1-3 stay identical and the agy rule is regenerated, never hand-edited. user-decided.

**W1-03 Raise the card cap so the rule keeps its obligations**  after: W1-02  acceptance: 6
- Files: `loom-workflow/skills/loom-visualization/assets/trigger-card.md`, `loom-workflow/skills/loom-visualization/assets/trigger-card-coexist.md`, `loom-workflow/rules/AGENTS.md`, `loom-workflow/scripts/test_visualization_card_hook.py`, `docs/loom/2026-09-16-plain-language-replies/evidence/probes/test_probe_prose_gate_mutants.py`
- Test: A6 positive: cards-list-or-rule-out-each-missed-alternative; boundary: both-cards-stay-within-165-words.
- Risk: W1-02 hit the 150-word cap and paid with three coexist obligations and a weaker verb; raising the cap to 165 restores them and costs about 15 words each turn. agent-decided.

### Wave 2 — shipped text and the memory store

**W2-01 One name for the card in shipped text**  after: W1-02  acceptance: 2
- Files: `loom-workflow/README.md`, `loom-workflow/README.ja.md`, `loom-workflow/README.zh-TW.md`, `loom-workflow/.codex-plugin/plugin.json`, `loom-workflow/hooks/visualization-card`, `loom-workflow/scripts/test_readme_card_timing.py`
- Test: A2 positive: current-descriptions-use-one-card-name; negative: reintroduced-old-name-fails-in-any-language.
- Risk: changelog entries keep the name they shipped with, so only current descriptions change; the hook docstring is prose, not behaviour. agent-decided.

**W2-02 Two lessons enter the repository memory store**  after: W2-01  acceptance: 3
- Files: `docs/loom/memory/a-phrase-presence-guard-passes-a-negated-rule.md`, `docs/loom/memory/an-inline-rule-reaches-replies-that-a-routed-guide-never-does.md`, `docs/loom/memory/index.md`
- Test: A3 positive: both-entries-validate-against-the-memory-profile; negative: entry-missing-sources-is-rejected.
- Risk: both entries are recorded by invoking `loom-workflow:loom-memory`, which owns the profile and regenerates `index.md`; hand-written files and a hand-merged index are what its validator rejects. agent-decided.

### Wave 2b — what the card triggers on, and which form it asks for

**W2-03 The card names the conversation situations that carry a table**  after: W2-02  acceptance: 7
- Files: `loom-workflow/skills/loom-visualization/assets/trigger-card.md`, `loom-workflow/skills/loom-visualization/assets/trigger-card-coexist.md`, `loom-workflow/rules/AGENTS.md`, `loom-workflow/scripts/test_visualization_card_hook.py`, `docs/loom/2026-09-16-plain-language-replies/evidence/probes/test_probe_prose_gate_mutants.py`
- Test: A7 positive: both-cards-name-the-conversation-situations; boundary: both-cards-stay-within-their-cap.
- Risk: the eight situations reach replies only through the card, as the guide is not read; the coexist card has one word of headroom, so the cap moves again if the wording does not fit. user-decided.

**W2-04 Markdown table is the default form; ASCII is for plain-text destinations**  after: W2-03  acceptance: 8
- Files: `loom-workflow/skills/loom-visualization/SKILL.md`, `loom-workflow/skills/loom-visualization/references/client-matrix.md`, `loom-workflow/skills/loom-visualization/scripts/test_templates.py`, `loom-workflow/skills/loom-visualization/scripts/detect_client.py`, `loom-workflow/skills/loom-visualization/scripts/test_detect_client.py`, `loom-workflow/scripts/test_recap_state_compaction.py`, `loom-workflow/skills/recap-state/SKILL.md`
- Test: A8 positive: shaped-content-defaults-to-a-markdown-table; negative: remote-viewer-no-longer-forces-ascii.
- Risk: the registered prose gate pins the words "markdown table plus ASCII", and a sibling skill pins the terminal-means-ASCII story, so both move with the rule. user-decided.

### Wave 3 — release

**W3-01 loom-code 3.7.1 reaches installed copies**  after: W2-04  acceptance: 4, 5
- Files: `loom-code/plugin.json`, `loom-code/.claude-plugin/plugin.json`, `loom-code/.codex-plugin/plugin.json`, `loom-code/CHANGELOG.md`, `loom-code/README.md`, `loom-code/README.ja.md`, `loom-code/README.zh-TW.md`, `README.md`
- Test: A4 positive: every-loom-code-version-pin-reads-3-7-1; negative: one-stale-3-7-0-pin-fails. A5 positive: package-suite-and-check-mechanisms-green; negative: mechanism-count-growth-blocked.
- Risk: the changelog has no entry for PR #19, #20 and #21, so 3.7.1 records them as well as the bump; without it the version moves with nothing stating why. agent-decided.

## Questions asked
① — what — 上面那 6 條就是這次要做的，對嗎？
① — what — 指南的「先不做／更小版本／合併」檢查，要寫進提醒卡（A），還是記錄成只存在於指南（B）？
① — consequence — 回「是」代表同意：做完並通過審查後自動 push 並開 Ready PR，合併仍由你決定；不想自動發布現在說就可以。

## Risks
<!-- each numbered item ≤40 words (checker rule plan.field-caps) -->
1. user-decided — kouko chose option A: the missed-alternatives check is stated in the reminder itself, because the guide was opened in none of six recorded trials while the inline rule reached every one.
2. Both cards are at the 150-word cap, so W1-02 trims non-rule wording a second time; the previous change already trimmed once, and further trimming may cost diagram guidance.
3. Whether an installed copy refreshes can only be seen after this change merges and the plugin is updated on kouko's machine; the blind run proves the declared version and the checks only.
4. The installed loom-code checker predates the trunk, so this branch's own runs still use the older station contracts until the bump lands and is installed.
