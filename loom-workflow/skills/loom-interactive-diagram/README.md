# loom-interactive-diagram

[Loom](../../../README.md) / [loom-workflow](../../README.md) / loom-interactive-diagram

Create diagram files that you can edit in an external editor and that the agent can read back and validate.

## When to use

Use this when you need an editable diagram during a Loom change or a standalone discussion. The default format is draw.io.

## What you get

A diagram file and a neighboring Markdown projection describing its content. Loom files go in `docs/loom/<change-id>/diagrams/`; standalone files go to the directory you explicitly select.

## How to use

Install the plugin as described in its [README](../../README.md), then ask
your coding agent to use the skill. For example:

```text
Use loom-workflow:loom-interactive-diagram to create a draw.io architecture diagram in the project directory I specify.
Use loom-workflow:loom-interactive-diagram to read back and check this saved diagram.
```

## Boundaries

- Before each request to edit an existing external diagram, the agent asks whether to copy it into the project or edit the original, showing the paths and waiting for your choice.
- Copying never overwrites an existing diagram or projection. Editing the chosen original creates no backup automatically.
- During an active turn, the agent can wait for a changed save, then regenerate the projection and check it. A static file check is not evidence of live synchronization.
- The save watcher cannot resume a turn after it has ended; if it times out, send a message after saving.

## Further reading

- [Editor setup](references/editor-setup.md)
- [Supported-format contract](references/backends.md)
- [Text projection format](references/projection.md)

## Related skills

- [loom-workflow:loom-visualization](../loom-visualization/README.md)
- [loom-design:architecture-design](../../../loom-design/skills/architecture-design/README.md)
- [loom-design:write-spec](../../../loom-design/skills/write-spec/README.md)

Runtime instructions: [SKILL.md](SKILL.md).
