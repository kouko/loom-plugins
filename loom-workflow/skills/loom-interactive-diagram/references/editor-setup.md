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
can replace the other editor's work.

Observed in a temporary local fixture on 2026-10-30: VS Code Draw.io
Integration 1.17.0 displayed an externally added `Agent Added` node without
reopening the file. After the node was changed in the editor to `User Changed`
and saved through **File > Save**, the disk XML contained that value and
`diagram.py project` followed by `check` passed. Official draw.io Desktop
32.6.1 showed **The file has been modified. Click here to synchronize.**
with Autosave off; clicking displayed `Desktop External`. With Autosave on,
an external change displayed `Desktop Auto` without a click. Autosave was
restored to off after the check.

Separately on 2026-10-30, a fresh source checkout from `git archive HEAD`
was unpacked under `/private/tmp/loom-diagram-clean-check`. From
`docs/loom/2026-10-29-shared-diagram-tool/`, the documented command created
`clean-check.drawio`. With the already installed VS Code Draw.io Integration
1.17.0, an external `Clean Agent` node appeared in the open editor without
reopening it. The node was changed there to `Clean User` and saved; the disk
XML contained that exact value, and `diagram.py project` followed by `check`
passed. This verifies the procedure from a fresh source checkout with
installed prerequisites, not a fresh OS or extension installation.
