---
name: loom-interactive-diagram
description: |
  Create and check shared editable diagrams during Loom discussions. Use when the agent needs to create a diagram for the user to edit in an external editor or read back saved changes; draw.io is the default format.
version: 1.0.0
---

# Shared editable diagrams

Use this tool in any station when a diagram should persist in the change's
Git history and be editable by the user. The conversation carries the file
path and a text projection; the user opens the file in an editor.

Work from `docs/loom/<change-id>/`, or pass `--change-id <change-id>` when
running `new` or `project` from the repository root. The id must name an
existing `docs/loom/intent/<change-id>.md`; an explicit id inside a change
directory must match that directory. Generated files go to
`docs/loom/<change-id>/diagrams/`. Run
`python3 <plugin-root>/skills/loom-interactive-diagram/scripts/diagram.py`
with one of these commands:

- `list-backends`: show available formats.
- `new <name> [--change-id <id>]`: create an empty draw.io diagram and matching projection.
- `new <backend-id> <name> [--change-id <id>]`: create one with a selected format.
- `project [diagrams/<name>.<ext>] [--change-id <id>]`: regenerate a managed
  projection after an edit. The path must stay inside the selected change's
  `diagrams/` directory, including after resolving symlinks.
- `check [<diagram-path>]`: validate one diagram or every registered diagram
  under `diagrams/` and every diagram linked from `spec.md`; return nonzero
  and name each invalid file or difference. Spec links resolve from `spec.md`.
  Read-only checks of diagrams linked outside the managed directory remain supported.

The default backend is `drawio`. A backend is one file in `backends/`; the
selection is recorded in the projection header. See `references/backends.md`
for the callable contract and `references/projection.md` for the text format.

When the user is editing during the current conversation turn, tell them which
diagram you are waiting for and keep the turn active. After your last write,
run `python3 <plugin-root>/skills/loom-interactive-diagram/scripts/wait_for_save.py
diagrams/<name>.<ext> --timeout 120` in a live tool session that yields output
while the process keeps running; retain its session identifier. Wait for
`READY`, then tell the user they can edit and save that diagram. Continue
polling that same tool session during this turn for `CHANGED`, `TIMEOUT`, or
`ERROR`. `READY` means the content baseline was read. `CHANGED` means that
same file has held changed content across two reads; it does not identify who
or what wrote it. Read the file, run
`python3 <plugin-root>/skills/loom-interactive-diagram/scripts/diagram.py
project diagrams/<name>.<ext>` to regenerate its projection and `python3
<plugin-root>/skills/loom-interactive-diagram/scripts/diagram.py check` to
validate it, then restate the visible edit. On `TIMEOUT`, say that no
changed save was observed and the user can still send a message to continue.
On `ERROR`, name the file and ask the user to save it again. Unrelated file
changes and identical-content saves do not end the wait. The watcher cannot
resume a turn after it has ended.

For edits outside an active wait, read the saved file and follow the same
`project` then `check` procedure.
For VS Code and desktop setup and the acceptance procedure, follow
`references/editor-setup.md`. Do not claim live synchronization from a static
file check.
