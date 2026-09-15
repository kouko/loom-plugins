# Keep loom agents' replies in plain words, literal, and shaped as tables or diagrams — spec
intent: 2026-09-16-plain-language-replies@63bd57c5
pre-build-review: not-required — guidance text plus moving one existing hook to another event; no security, privacy, existing-data, public-contract or cross-system change, and a revert restores the old behaviour

## Requirements
REQ-1 — Per-turn reminder on Claude Code
  WHEN a user submits a message in a Claude Code session with loom-workflow installed, the loom-workflow hook shall add one English reminder to the agent's context that tells it to reply in the user's language, lead with the conclusion and its impact, replace internal terms with plain words, speak literally without metaphors ("用白話說明，但不要用比喻"), and show structured content as tables or diagrams through loom-visualization, choosing Mermaid only where the client can display it ("基於當前 client 是否能 preview mermaid 來決定呈現用的技術") → Acceptance #1

REQ-2 — Table-and-diagram trigger moves into the reminder
  WHEN a Claude Code or Codex session starts, the loom-workflow hooks shall not deliver the visualization trigger card separately, and WHEN ascii-graph-toolkit is active the per-turn reminder shall carry the coexist diagram wording so exactly one diagram trigger instruction is present → Acceptance #2

REQ-3 — Per-turn reminder on Codex CLI
  WHEN a user submits a message in a Codex CLI session with loom-workflow installed and its hooks trusted, the hook shall add the same reminder using only the canonical hookSpecificOutput shape → Acceptance #3

REQ-4 — Antigravity CLI rule
  WHILE loom-workflow is installed in Antigravity CLI, the generated plugin rule shall carry the same reminder text, produced from the same source file as REQ-1 → Acceptance #4

REQ-5 — Fail open
  IF the hook input is malformed or the card cannot be read, THEN the hook shall exit 0 without blocking the user's message → Acceptance #5

REQ-6 — Plain-language writing guide
  WHEN the user asks for a plainer explanation, the agent following the reminder shall load loom-visualization's plain-language reference and rewrite by its seven rules and five rewrite steps, whose before-and-after examples come from real complaints ("這些內容沒問題") → Acceptance #6

REQ-7 — Decision questions
  WHEN the agent asks the user how to do something, the guide shall require at least two workable alternatives with the recommended one marked, a check for do-nothing-or-later, smaller and combined alternatives with a one-sentence reason when none is workable, and one consequence sentence per option; a yes-or-no confirmation is asked directly ("可以") → Acceptance #7

REQ-8 — Table collections
  The loom-visualization skill shall carry, inside its existing skill folder with no new skill ("放進 loom-visualization 吧，我想要盡量減少 skill 的數量"), a general conversation set of eight situation tables plus table-writing rules and common mistakes ("併進這次"), and three domain collections for software development, design and business analysis holding every usage from the research, including the earlier table research's patterns and rules ("1. OK"; "三類專業表格集 在本次就收錄") → Acceptance #8

REQ-9 — Progressive loading
  WHEN the agent uses loom-visualization, SKILL.md shall route a conversation-situation reply to the general reference only and a named document type to the one domain collection that holds it → Acceptance #9

REQ-10 — Install limits documented
  The loom-workflow READMEs shall state that the reminder does not reach the Codex IDE extension or app, the Antigravity desktop app or IDE, or an install of loom-code without loom-workflow ("只放 loom-workflow 吧") → Acceptance #10

REQ-11 — Checks stay green without mechanism growth
  WHEN the change is complete, the package tests and mechanism checks shall pass and the registered mechanism count shall not exceed the base count → Acceptance #11

## Design decision
- user-decided (kouko, 2026-09-16): reduced shape — one English card, no conversation-language detection, delivered by moving the existing visualization-card hook from SessionStart to UserPromptSubmit; the agy rule is generated from the same card ("接受縮小方案，但是 三類專業表格集 在本次就收錄").
- user-decided (kouko, 2026-09-16): only loom-workflow ships it ("loom 所有工具都要生效" / "只放 loom-workflow 吧").
- user-decided (kouko, 2026-09-16): the guide, option rule, conversation tables and table rules share one reference; the three domain collections are separate references.
- agreed card content (full version, English; coexist variant keeps the ascii-graph-toolkit hand-off wording for diagrams):
  Reply to the user in their language. 1) First sentence: the conclusion and what it means for the user; details after. 2) Say in plain words what a thing does; name an internal term, file path or rule id only when needed, in brackets after the plain words. 3) Say it literally: who does what, what the user will see, what changes (no metaphors, analogies, "like", "imagine"). 4) Show option comparisons, flows of 3+ steps, branches and state changes as tables or diagrams, following loom-visualization. When the user asks for a plainer explanation, read loom-visualization's plain-language reference first.
- agreed guide content: scope = chat text for the user, including relayed subagent results, never written files. Rules: (1) conclusion and impact first; (2) plain words, name in brackets after; (3) literal wording; (4) abstract noun → "you do X, you see Y"; (5) decision questions per REQ-7; (6) comparisons, 3+ step flows, branches and state changes as tables or diagrams via loom-visualization; (7) only what the user needs, process detail on request. Internal terms = loom station names, gate or rule ids, REQ/finding ids, lane, attestation, probe, blind run, agent-coined temporary names, file and function names. Rewrite steps (reordered after W2-03 cold reads): first sentence states the conclusion or lead news with no announcement, heading or background before it; replace internal terms and abstractions with what they do and who-does-what-and-sees-what; keep every fact, number, name and outcome of the original; cut process detail the decision does not need but never the lead news; check for metaphor words before sending. The script (Traditional or Simplified) follows the user's.
- agreed conversation situations: decision consequences (Option / What you gain / What you give up / Best if); before-after or wording (Item / Before / After / Impact on you); progress (Item / Status / Blocked on / Next step); acceptance checklist (Criterion / Met? / Note); confirmed-unconfirmed-to-decide (Item / Status / Basis or next step); findings (Problem / Severity / Recommendation); risks (Risk / Likelihood / Impact / Mitigation); support matrix (Feature / Environment A / B / C). Table rules 1-10 as agreed, with the options-as-columns-only-for-three-or-fewer judgment marked as such.
- agent-decided: the card stays a single source file under loom-visualization/assets so the hook, the coexist variant and the agy generator read one text; rewording the card never changes the hook command, avoiding a Codex re-trust.
- agent-decided: domain collections keep source URLs and the research's unverified or synthesized markers; runtime references cite no repository development record.

## Alternatives considered
- Localized zh/ja/en cards with a copy of loom-code's language detector — rejected by the complexity critique (≈400 extra lines, no evidence localization changes behaviour).
- A new UserPromptSubmit hook beside the SessionStart card — rejected: grows the mechanism count and leaves the diagram trigger fading once per session.
- A new plain-language skill — rejected by the user to keep the skill count down; a skill loads only when the agent notices it needs it.
- Deferring the domain collections — the critique's recommendation, overridden by the user.
- Copies in loom-code and loom-workflow — rejected: duplicate reminders and a second sync surface, the reason the earlier plain-relay contract was removed.

## Current state evidence
- Forward: `loom-workflow/hooks/hooks.json:3-14` registers `visualization-card` on SessionStart only, and `loom-workflow/hooks/visualization-card:123` hardcodes `hookEventName: SessionStart`.
- Reverse: `scripts/sync_codex_manifests.py:77-80` generates `loom-workflow/rules/AGENTS.md` from `assets/trigger-card.md`; `scripts/test_sync_codex_manifests.py:643-664` reads the SessionStart registration.
- Error: `loom-workflow/hooks/visualization-card:118-122` falls back to the full card on any error and exits 0; Codex receives only the canonical key (`:124-126`).
- Data: `docs/loom/evidence/mechanisms.yaml:211-216` registers both SessionStart card hooks; `loom-code/scripts/check_mechanisms.py:227` derives hook ids from event and matcher, so a move renames without adding.
- Boundary: `loom-workflow/scripts/test_visualization_card_hook.py:245-246` caps each card at 150 words (full 80, coexist 113); `loom-workflow/scripts/test_loom_visualization_compaction.py:8` caps SKILL.md at 4,500 words.

## UI flows
N/A — no user-facing command or screen; the carried details are recorded on the Requirement and Design decision lines above.
