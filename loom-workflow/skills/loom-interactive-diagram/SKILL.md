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

When the user is editing during the current conversation turn, tell them which
diagram you are waiting for and keep the turn active. After your last write,
run `python3 <plugin-root>/skills/loom-interactive-diagram/scripts/wait_for_save.py
diagrams/<name>.<ext> --timeout 120`. `READY` means the content baseline was
read and the user can save. `CHANGED` means that same file has held changed
content across two reads; it does not identify who or what wrote it. Read the
file, run `diagram.py project` to regenerate its projection and `diagram.py
check` to validate it, then restate the visible edit. On `TIMEOUT`, say that no
changed save was observed and the user can still send a message to continue.
On `ERROR`, name the file and ask the user to save it again. Unrelated file
changes and identical-content saves do not end the wait. The watcher cannot
resume a turn after it has ended.

For edits outside an active wait, read the saved file and follow the same
`project` then `check` procedure.
For VS Code and desktop setup and the acceptance procedure, follow
`references/editor-setup.md`. Do not claim live synchronization from a static
file check.
