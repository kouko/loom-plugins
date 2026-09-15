---
name: loom-visualization
description: |
  Show comparisons, flows, decisions, states or reasoning chains as tables, ASCII or Mermaid in coding chat, including when a Loom station reports to the user (intent restatement, choices, blind-run results); not Obsidian notes.
---

# Loom Visualization

Pick the right shape and form for information in a coding-harness
conversation, so the reader gets a table or a diagram that actually displays
in their client instead of prose or broken Mermaid source.

`<skill-dir>` is this skill's folder: `${CLAUDE_SKILL_DIR}` on Claude Code;
on any other host, the directory that holds this SKILL.md. Run every script
as `python3 <skill-dir>/scripts/<name>.py`; all other paths below are
relative to `<skill-dir>`. The scripts need only the Python standard library.

A one-line fact needs no table. Reach for this skill when the answer has a
shape: options side by side, three or more steps, a branch, a lifecycle, a
message exchange, a structure, dates, or numbers to compare.

## Boundary

<!-- gate: loom-visualization.obsidian-boundary -->
When the output is written to a file, first run
`python3 <skill-dir>/scripts/detect_client.py --target <path>`. Decline only when that
`--target` check reports `obsidian_vault: true`, or when the user asks for a
note in their Obsidian vault: say this skill serves coding-harness chat, and
name `obsidian:obsidian-mermaid-visualizer` as the skill for vault notes.
A chat answer proceeds normally even when the working directory is inside an
Obsidian vault. Never
put Obsidian-only syntax (wikilinks, callouts, `%%` comment lines) into
anything this skill produces.
<!-- /gate -->

Also out of scope: diagram rules for commit messages, pull requests and
repository documents. Those follow the rules of the skill that owns the
artifact (`loom-workflow:git-memory`, `loom-code:ship`,
`loom-design:write-spec`).

Documented reasoning turned into a standalone page is page mode, below.

## Plain language and conversation tables

These references sit beside the data-shape templates; the templates in
Step 1 stay as they are.

| Need | Read |
|---|---|
| A plainer explanation, a decision question, or a table for a conversation situation (decision, before and after, progress, checklist, confirmed and unconfirmed, findings, risks, support matrix) | `references/plain-language.md` |

## Step 1 — Classify the information shape

Name the one shape the information has. If it has two, draw the one the
reader must act on, and state the other in a sentence.

| Shape | Signals | Template | Generator |
|---|---|---|---|
| Option comparison | 2+ options, shared criteria | `templates/01-option-comparison.md` | `table` |
| Linear steps | 3+ steps, fixed order, no branch | `templates/02-linear-steps.md` | `flow` |
| Branching decision | a question sends work down different paths | `templates/03-branching-decision.md` | none |
| Reasoning chain | causes or inferences leading to a conclusion | `templates/04-reasoning-chain.md` | none |
| State lifecycle | named states changed by named events | `templates/05-state-lifecycle.md` | none |
| Actor sequence | actors exchanging messages in time order | `templates/06-actor-sequence.md` | `seq` |
| Hierarchy | parent-child, no cross-links | `templates/07-hierarchy.md` | `tree` |
| System architecture | components in layers with dependencies | `templates/08-system-architecture.md` | `arch` |
| Data model | entities, fields, cardinality | `templates/09-data-model.md` | none (table substitute) |
| Timeline | events on dates or periods | `templates/10-timeline.md` | none |
| Quantity | a few labelled numbers to compare | `templates/11-quantity.md` | `bar` |

## Step 2 — Read only that template

Read the one template file from Step 1, and no other. Each template gives the
shape's table form, ASCII form, Mermaid form and common mistakes, with a
worked example to adapt.

## Step 3 — Choose the form

Run `python3 <skill-dir>/scripts/detect_client.py`. It prints
`{client, mermaid, remote_viewer, obsidian_vault, reason}`. What each client
displays, with sources and a verified date, is in
`references/client-matrix.md`.

<!-- gate: loom-visualization.mermaid-only-when-confirmed -->
Use Mermaid only when you have no shell and your own host is claude.ai or the
Claude Desktop chat, where Mermaid is reported to render. If you can run the
client check at all, you have a shell, so do not use Mermaid. Everywhere else
use a markdown table plus ASCII in a fenced code block. When
`remote_viewer` is `true`, send the ASCII form in a code block and add the
table only when exact values matter. A wrong Mermaid choice shows the user
raw source; a table plus ASCII reads everywhere.
<!-- /gate -->

Within the table plus ASCII form:

- Option comparison always uses a GFM markdown table, in every client. Use the
  ASCII table generator only when the answer goes into a code block or a
  plain-text destination.
- Data model and quantity usually need only the markdown table; add the ASCII
  form when the channel may not render markdown.
- Flows, decisions, chains, states, sequences, hierarchies, architecture and
  timelines get the ASCII diagram, with the table when exact values matter.

## Step 4 — Generate and verify the ASCII

Where the template names a generator, generate; do not hand-pad:

```
printf '%s' '<json input from the template>' | python3 <skill-dir>/scripts/generate.py <shape>
```

Shapes: `table`, `flow`, `seq`, `tree`, `arch`, `bar`. Pass the JSON as the
`printf '%s'` argument so a `\n` inside a label reaches the script as a line
break request rather than a raw newline. `seq` and `bar` labels must be
single-line.

Where there is no generator (branching decision, reasoning chain, state
lifecycle, timeline), adapt the template's ASCII by hand. The data model has
no ASCII form; use its table substitute.

Always verify before sending:

```
printf '%s' '<your diagram>' | python3 <skill-dir>/scripts/align.py -
```

It prints a per-line width report, then either `line N: col C: message` for
each drift or `✓ no drift`, exiting 0 when clean and 1 on drift. Fix only the
flagged lines and rerun until it is clean. The checks it runs are the vertical
seam (`scripts/checks_seam.py`), table equal width
(`scripts/checks_table.py`) and kink plus arrowhead landing
(`scripts/checks_kink.py`). The one exception is `seq` output: it is correct
by construction, its blank off-span lifelines sit outside the seam model, and
it is sent unedited.

Width rules the checks depend on:

- Chinese and Japanese characters take two cells; the scripts measure this,
  so never count characters by eye.
- Keep emoji and pictographic symbols out of box labels and table cells.
  Their width differs between terminals, so no check can make them align.
- Keep ambiguous-width symbols (`→`, `★`, `·`, `°`, Greek letters) out of
  the column that sets a box's width. Use the generators' arrows (`▼ ▲ ► ◄`).

## Page mode

Page mode turns reasoning that already exists (in a document, a folder, or
this conversation) into one self-contained HTML page whose core is a
chain-of-thought Mermaid diagram. It is for how a conclusion was reached, not
for what a function does, and not for doing the thinking itself. The page is
a file the user opens, so the chat client check does not apply to it.

Read `references/page-mode.md` in full before starting. It holds the whole
procedure: resolve the source, extract the chain before drawing, build the
diagram to `references/mermaid-cot-spec.md`, write the markdown from
`assets/cot-report-template.md`, convert and verify, then run the fidelity
check in `references/fidelity-check.md` before the page is shared.

Ask once whether the user wants an Artifact; do not publish unprompted, and
never publish before the fidelity check passes.

## Failure modes to refuse

- **Prose for a shaped answer.** Three options described in paragraphs make
  the reader build the table themselves.
- **Mermaid "because it looks better".** Outside a confirmed client the user
  sees raw source. The client check decides, not taste.
- **Hand-padded CJK boxes sent without `scripts/align.py`.** Eyeballed widths
  break on the first full-width character.
- **Editing generator output by hand.** Change the JSON input and regenerate.
- **A diagram for a trivial answer.** Two steps or one fact is a sentence.
- **Reading every template "to be safe".** Read the one the shape names.
- **Writing a vault note.** Decline and name
  `obsidian:obsidian-mermaid-visualizer`.
- **A page drawn without reading the source, or padded to reach five nodes.**
  Page mode's extraction is the work; three reasoning states get prose.
