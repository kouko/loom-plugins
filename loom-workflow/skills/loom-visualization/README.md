# loom-visualization

[Loom](https://github.com/kouko/loom-plugins/blob/main/README.md) / [loom-workflow](../../README.md) / loom-visualization

Present comparisons and relationships in a form the reader’s coding client can actually display.

## When to use

Use this when a comparison, decision, flow, state change or relationship is clearer as a table or diagram. A single fact or a short explanation needs no visual.

## What you get

A chat table or diagram chosen for the information and client. Plain-language guidance covers decisions and reports; a separate page mode can turn already documented reasoning into a standalone HTML page.

## How to use

Install the plugin as described in its [README](../../README.md), then ask
your coding agent to use the skill. For example:

```text
Use loom-workflow:loom-visualization to compare these implementation options.
Use loom-workflow:loom-visualization to explain the review handoffs in this coding client.
```

## Boundaries

- Coding chat defaults to Markdown tables. Mermaid is used only where the client is known to render it; a shell-based client check does not authorize Mermaid in chat.
- Drawn text diagrams use width-aware generation and alignment checks, especially for CJK labels.
- Page mode presents reasoning already in the source; it is not a way to invent missing evidence or publish without authorization.
- Obsidian notes use their own visualization workflow. Editable diagram files belong to loom-interactive-diagram.

## Further reading

- [Plain-language guide](references/plain-language.md)
- [Reasoning-page workflow](references/page-mode.md)

## Related skills

- [loom-workflow:loom-interactive-diagram](../loom-interactive-diagram/README.md)
- [loom-workflow:recap-state](../recap-state/README.md)

Runtime instructions: [SKILL.md](SKILL.md).
