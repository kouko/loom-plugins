---
name: recap-state
version: 0.1.0
description: |
  Give an in-session recap of current progress for 'where were we', '我們剛剛在幹嘛', '剛剛講到哪', '我跟丟了', 'ちょっと振り返って', '今どこだっけ', or '振り返り'. The built-in /recap is an away-summary.
user-invocable: true
---

# Recap

Re-orient the user inside the current conversation, then pause for alignment.
This is **in-session re-orientation**. The built-in `/recap` is an
`away-summary`; `HANDOFF` handles cross-session continuation.

## What to do

1. Read `references/seven-block-schema.md` fully before rendering every recap.
   Its L3 user-visible template is the authoritative orientation-first
   contract. The numbered seven blocks record historical lineage, not required
   headings.
2. Keep planning internal. In a long conversation, find the original purpose
   when available, current position, decisions that brought the work here,
   completed work, remaining gap, and, only when the purpose is grounded, a
   proposed next step. Ground each in the conversation; label unavailable facts
   unknown. Before calling something a historical decision, identify the user
   turn or prior action that establishes it; omit an unsupported claim. A
   formatting choice made for this recap is not a historical decision. In a
   short session, include only what helps the user regain their
   place. Use the user's conversation language and explain unfamiliar terms
   plainly.
3. Render the reference's variable-length sections and visual rules. Preserve
   behavior-changing user wording exactly. Use `loom-visualization` to choose
   and verify any meaningful table or relationship diagram and to frame section
   headings. Apply the same visual rules to natural-language requests and
   explicit skill calls. When the recap needs a table or multiple sections,
   frame at least the purpose/current-position and final-question headings.
   A long recap with several decisions, completed items, and an open gap needs
   those sections; do not compress it into one dense paragraph.
   If it contains a table, put one short situation sentence immediately before
   the table, in the same section. Nothing except a blank line may separate
   that sentence from the table; the heading alone does not serve as the sentence.
   Never expose planning tags or numbered block labels.
4. If the original purpose is unknown, ask only for the purpose. Do not invent
   a proposed work step when the purpose is unknown. When the original purpose
   is grounded, ask about the proposed next step. If asking for purpose, wait
   for the user to state or clarify it. Otherwise, wait for the user's answer
   before continuing work; a clear confirmation is enough, and a correction
   becomes the current direction.

## Five principles

- **structured-schema**: follow the orientation-first L3 contract; include
  only sections the conversation needs.
- **quote-not-paraphrase**: preserve exact user wording when it changes what
  happens next, including paths, errors, constraints, tools, and commands.
- **all-user-messages**: dormant at L3. Do not dump every user turn.
- **synthesis-check**: direct the final question to the purpose when unknown,
  or to the grounded next step, then wait for the answer.
- **plain-language**: explain the situation to the user in familiar words.

## Hard boundaries

- Chat only: do not write the recap to a file.
- Current session only: cross-session work belongs to HANDOFF.
- Do not replace the built-in `/recap` away-summary.
- Wait after the final alignment question; do not continue with a tool call,
  edit, or analysis until the user responds.

## See also

- `references/seven-block-schema.md` — authoritative L3 contract, visual
  guidance, examples, and historical seven-block lineage.
