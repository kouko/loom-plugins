# Editor setup and collaboration check

Use a local Git checkout. Diagram files live in
`docs/loom/<change-id>/diagrams/` and are committed with their
`<name>.projection.md` files. The command below is run from
`docs/loom/<change-id>/`; replace `<plugin-root>` with the installed
`loom-workflow` directory.

## VS Code

1. Install VS Code and the Draw.io Integration extension, then record their
   versions for the acceptance report.
2. Enable autosave or save any pending edit before an agent updates the file.
3. Run `python3 <plugin-root>/skills/loom-interactive-diagram/scripts/diagram.py new example`.
4. Open `diagrams/example.drawio` in the Draw.io Integration editor. Have the
   agent add a node to that same file and save it. Observe whether the open
   editor shows the node without reopening the file.
5. Add or change a node in the editor and save. Have the agent read the XML
   from disk and identify that exact change. Run `diagram.py project
   diagrams/example.drawio`, then `diagram.py check`.

## draw.io desktop

1. Install the draw.io desktop app and record its version. Open the same
   `diagrams/example.drawio` file. The two applications must use the same
   checkout, not separate copies.
2. With autosave enabled, have the agent change and save the file. Observe
   whether the open diagram updates without a click.
3. Disable autosave and repeat. Observe the file modified prompt and click
   **synchronize**; verify the open diagram then shows the new content.
4. Edit a node manually, save, and have the agent read back the exact change.
   Regenerate and check the projection before committing.

Do not write to the same diagram concurrently in two editors: the final save
can replace the other editor's work. The desktop and VS Code interactions
must be observed on installed versions before marking those acceptance lines
passed. As of 2026-10-30 this worktree has neither the draw.io desktop app
nor the VS Code extension installed, so these interactions remain unverified.
