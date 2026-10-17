# Recap Alignment Schema — Reference Bundle

> **SSOT for `loom-workflow:recap-state` v0.1**
> This file owns the L3 orientation contract and retains the historical
> seven-block lineage for the possible L2 HANDOFF sister skill.
> Source research: `AI Agent Recap 框架研究` (2026-05-25),
> `對話接續綜論` (2026-05-25), and `2026-05-26-recap-v0.1-brief.md`.

The renderer keeps planning private. Never output `<thinking>` or `<recap>`
tags, their closing forms, or numbered `Block N` labels.

## L3 user-visible template

Use an orientation-first, variable-length recap in the conversation language.
For a long conversation, lead with the conversation-grounded original purpose,
current position, and proposed next step. Explain how key decisions and
completed work led here, then name the remaining gap. Mark assumptions and
unknown facts as such; never infer a purpose or completed work from silence.
If the purpose is unknown, say so and ask for it in the final question. In a
short session, omit sections with no useful content; never pad a history or
invent a pending question to fill a template.

Use clear section headings for content that warrants sections. Frame each
heading in an ASCII box with `■ ` before the heading text. Use
`loom-visualization` to generate or verify CJK alignment rather than eyeballing
cell widths. Put one fullwidth-space-only line between sections, and inspect
the rendered chat spacing; do not use visible HTML break tags. Keep the first
section focused on purpose and position, and the final section focused on a
directed question about the next step. Stop until the user responds.

Use bullets for a short path through decisions and work. Put a short
situation sentence before each table. A table earns its place by comparing
information or compressing meaningful metadata. Draw a relationship diagram
only for real dependency, branch, or merge topology; a flat status list needs
no diagram. Route the form and any ASCII alignment through
`loom-visualization`; follow its client-specific renderer guidance. Preserve
the user's exact wording when a phrase changes subsequent behavior, including
paths, errors, constraints, tools, and commands. Keep confirmed facts,
assumptions, and unknowns distinct. Answer in the current chat only; do not
write a recap file or replace HANDOFF or the built-in `/recap`.

## 1 — The Seven Blocks (historical lineage)

The V1 model used seven blocks. The map records why each mattered and how a
future L2 HANDOFF might use it. It is not the L3 display format.

| # | Block | Original purpose | L3 treatment | Future L2 |
|---|---|---|---|---|
| 1 | Situation | Open at the present moment | Lead with purpose and position | Render |
| 2 | Background | Preserve the reasoning trail | Include key decisions when relevant | Render |
| 3 | Assessment | Expose assumption, confidence, and unknowns | Distinguish facts from assumptions | Render |
| 4 | User messages | Preserve all user intent for a cold reader | Skip the full message dump | Render verbatim |
| 5 | Why-this-question | Explain a pending agent question | Include its stakes only when one exists | Skip |
| 6 | Pending | Show remaining work | Name the gap and useful next work | Render |
| 7 | Synthesis-check | Catch a direction mismatch | Ask a directed final question and wait | Render with L2-specific strength |

The original Block 2 guidance used 3–5 bullets and the original L3 renderer
used six natural sections. Those limits are history, not current requirements.
The full message dump was dropped at L3 because an in-session reader already
has their turns; consequential phrases still require exact quotation. L2 has
a different reader and may need every turn. HANDOFF-specific additions belong
to HANDOFF, not this recap.

## 2 — Visual aids

Use a table to compare alternatives or compress meaningful metadata, and put
a short situation sentence before it. A single row or unrelated items rarely
earn a table. Use a relationship diagram only for dependency, branch, or merge
topology that is easier to understand spatially. Follow `loom-visualization`
for client rendering choice, ASCII frames, and alignment verification. An
ordinary status snapshot works as prose or bullets. An explicit user format
request wins where the client can render it.

## 3 — The Five Shared Core Principles

### structured-schema

Lead with grounded purpose and current position, adapt the middle to the
conversation, and end with a directed question. Predictable endpoints help
orientation; mandatory empty sections hide useful work behind filler.

### quote-not-paraphrase

Reproduce behavior-changing user wording exactly, including paths, error
messages, named constraints, and tool or command names. For example,
"kill `config/base.py` and split into `config/db.py` + `config/app.py`"
cannot be reduced to "restructure the config file" without losing the action.

### all-user-messages

This is an L2-only principle for a cold reader. At L3, do not dump all user
turns. If a user asks for message history, provide that listing separately.

### synthesis-check

Finish with one directed next-step question and wait for the user's answer.
Any clear confirmation opens this soft pause; a correction replaces the
proposed direction. Do not resume a tool call, edit, or analysis on your own.

### plain-language

Explain the situation to the user in the conversation language, as a person
speaking to them. Define an unfamiliar term when first used. Prefer "We chose
Y because X would have delayed the migration" to shorthand such as
"Decision: Y; rationale: migration constraint." Keep sentences short and
separate facts, assumptions, and unknowns.

## 4 — Good Example

The following short-session example uses only the sections it needs. The
heading frames shown here are ASCII; generate or verify CJK frames with
`loom-visualization` when the actual heading uses CJK characters.

```text
+--------------------------+
| ■ Purpose and position   |
+--------------------------+
```

You asked us to make the recap easier to scan. We agreed on the behavior,
and the next step is to update its instructions. We have not edited them yet.

　

```text
+--------------------------+
| ■ Next step              |
+--------------------------+
```

Should I update the instructions now, or change the scope first?

## 5 — Bad Example

"Current state: implementation pending. Confidence: high. Next: proceed."
This hides the user's purpose, treats a guess as a fact, and continues without
a directed question. Six padded headings or a decorative graph would make the
same short exchange harder to scan.

The historical implementation example mentioned
`loom-workflow/skills/recap-state/scripts/`; it is retained here only as a
lineage pointer, not as a current test-location instruction.
