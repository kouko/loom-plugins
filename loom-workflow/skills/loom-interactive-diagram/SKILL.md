---
name: loom-interactive-diagram
description: |
  Create and check shared editable diagram files during Loom discussions. Use when the user or agent needs a diagram both can edit in an external editor, including draw.io files.
version: 1.0.0
---

# Shared editable diagrams

Use this tool in any station when a diagram should persist in the change's
Git history and be editable by the user. The conversation carries the file
path and a text projection; the user opens the file in an editor.

Work from `docs/loom/<change-id>/`. Run
`python3 <plugin-root>/skills/loom-interactive-diagram/scripts/diagram.py`
with one of these commands:

- `list-backends`: show available formats.
- `new <name>`: create an empty draw.io diagram and matching projection.
- `new <backend-id> <name>`: create one with a selected format.
- `project [diagrams/<name>.<ext>]`: regenerate the projection after an edit.
- `check [<diagram-path>]`: validate one diagram or every registered diagram
  under `diagrams/` and every diagram linked from `spec.md`; return nonzero
  and name each invalid file or difference. Spec links resolve from `spec.md`.

The default backend is `drawio`. A backend is one file in `backends/`; the
selection is recorded in the projection header. See `references/backends.md`
for the callable contract and `references/projection.md` for the text format.

After the user edits and saves a diagram, read the file from disk and restate
what changed. Run `project` to regenerate its projection, then `check` before
committing.
For VS Code and desktop setup and the acceptance procedure, follow
`references/editor-setup.md`. Do not claim live synchronization from a static
file check.
