# Keep loom agents' replies in plain words, literal, and shaped as tables or diagrams
originator: kouko
kind: engineering
needs-design: no — guidance text the agent reads plus its delivery on each host; no surface a user reads or types into changes
evidence: ["/Users/kouko/kouko-obsidian-vault/research/2026-09-16 表格在軟體／設計／商業產業中的使用慣例與寫作規則.md", "/Users/kouko/kouko-obsidian-vault/research/2026-09-04 Markdown 表格的業界變形用法與 Obsidian 能力邊界.md", "/Users/kouko/kouko-obsidian-vault/research/2026-08-15 loom skill 回應白話化研究——ADHD-friendly 溝通契約設計.md"]
status: confirmed 2026-09-16
publication: automatic — authorized 2026-09-16 by kouko

## Problem
When kouko works through loom tools, the agent's replies are often hard to
read, and kouko has to ask again — typically "請用白話說明，但不要用比喻".
A scan of 1,759 past Claude Code and Codex sessions found 14 such
readability complaints, all inside loom work, clustered at the moments the
agent asks kouko to decide something or reports progress and results. Every
one of the hard replies used loom-internal terms without explanation; others
were too long or offered too many options, cited file paths or rule ids, or
stated abstractions instead of what kouko would see. When asked to be plainer,
the agent fell back to metaphors in 5 of the 14 rewrites ("就像插座",
"家裡三個門禁"), which kouko does not want.

A plain-language contract for the loom family existed from 2026-08-15 until
the loom 1.0 cutover on 2026-09-03, delivered once at session start; it was
removed together with the cross-plugin reception mechanism it hung from, not
because it was judged ineffective. Seven complaints fell inside its lifetime
and seven in the thirteen days after its removal, and it never addressed
metaphors. A plain-language rule in kouko's global instructions did not
prevent them either, and loom-workflow's own table-and-diagram reminder is
likewise delivered only once at session start: guidance read once fades over
a long session. The consequence is extra round-trips at exactly the points
where kouko must understand before deciding.

## Proposed outcome
Whenever loom-workflow is installed, every loom tool's replies to the user
lead with the conclusion and what it means for the user, use plain words
instead of internal terms, say things literally rather than through metaphors
or analogies, ask for decisions with real alternatives and a recommendation,
and show structured content as tables or diagrams in a form the current client
can display. One short reminder carrying both the plain-language rules and the
existing table-and-diagram trigger reaches the agent on every turn instead of
once at session start. A fuller writing guide, and every table usage found in
the research, are available to the agent without being loaded when they are
not relevant.

## Acceptance
1. In a Claude Code session with loom-workflow installed, each user message reaches the agent together with one short reminder, written once in English, to reply in the user's language, lead with the conclusion and its impact, replace internal terms with plain words, speak literally without metaphors, and show structured content as tables or diagrams through loom-visualization.
2. The table-and-diagram trigger reaches the agent through that per-turn reminder; a session start no longer delivers it separately, and with ascii-graph-toolkit also installed the reminder still carries one diagram trigger instruction, not two conflicting ones.
3. In a Codex CLI session with loom-workflow installed and its hooks trusted, each user message reaches the agent with the same reminder.
4. In an Antigravity CLI session with loom-workflow installed, the same reminder is active in every session.
5. When the reminder cannot be produced, the user's message still goes through unchanged.
6. Given three past hard-to-read loom replies, a fresh agent following the reminder and loom-visualization's writing guide rewrites each so that its first sentence states the conclusion, it contains no metaphor or analogy, and it names no internal term, file path or rule id without saying in plain words what it does; the guide's before-and-after examples come from real complaints.
7. Given a decision question about how to do something, a fresh agent following the guide offers at least two workable alternatives, marks the one it recommends, and either includes a do-nothing-or-later, smaller, or combined alternative or says in one sentence why none is workable; a yes-or-no confirmation is asked directly without invented alternatives.
8. The loom-visualization skill carries every table usage found in the research — software development, design, and business analysis, plus the table patterns and table-writing rules from the earlier table research — together with a general set for common conversation situations (at least before versus after, per-item status, decision consequences, and hard-to-read versus plain wording) and the common mistakes to avoid; loom-workflow gains no new skill.
9. Given a reply that reports progress, a fresh agent using the skill reads the general conversation set and none of the domain-specific table collections; given a request to write an incident report, it reads only the collection that holds that document type.
10. loom-workflow's install documentation states that the reminder does not reach the Codex IDE extension or app, or the Antigravity desktop app and IDE, and that an install of loom-code without loom-workflow does not get it.
11. The repository's package tests and mechanism checks pass, and the number of registered mechanisms does not grow.

## Constraints
- user-decided (kouko, 2026-09-16): only loom-workflow ships this; loom-code and loom-design do not carry a copy.
- user-decided (kouko, 2026-09-16): the full writing guide and the table collections live inside loom-visualization, to keep the number of skills down.
- user-decided (kouko, 2026-09-16): the table collections are split so the general conversation set and each domain collection load separately, and all three domain collections ship in this change even though the complexity critique judged them deferrable.
- user-decided (kouko, 2026-09-16): no fixed minimum or maximum number of options; decisions offer at least two workable alternatives with a recommendation and a check for commonly missed alternatives.
- user-decided (kouko, 2026-09-16): the reduced shape from the complexity critique — one English reminder for every host with no conversation-language detection, delivered by moving the existing table-and-diagram reminder from session start to every turn, with the writing guide, option rule, conversation tables and table rules in one reference.
- Committed artifacts stay in English.
- Repository skill conventions hold: flat skill folder, SKILL.md size cap, no runtime citation of this repository's development records.
- On Codex the hook output uses only the canonical output shape, as the existing visualization trigger card does.

## Out of scope
- loom-code and loom-design: their hooks (including the existing conversation-language reminder) and their stations' report and decision-point formats are unchanged.
- An automatic scan of the agent's replies for metaphor words.
- Hosts where plugin hooks or plugin rules do not run: Codex IDE extension and app, Antigravity desktop app and IDE.
- Files the agent writes (intents, specs, plans, commits, code comments); they keep their own conventions.
- Updating the vault research notes or the vault's wiki layer.

## Open questions
- none
