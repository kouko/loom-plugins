---
name: loom-interactive-diagram
description: |
  Create and check editable diagrams during standalone or Loom work. Use when the agent needs to create a diagram for the user to edit in an external editor or read back saved changes; draw.io is the default format.
version: 1.0.0
---

# Shared editable diagrams

Use this tool when a diagram should be editable by the user during a
discussion, with or without an active Loom change. The conversation carries
the file path and a text projection; the user opens the file in an editor.

Outside Loom, ask where to save a new diagram and use an explicit directory:
`new example --output-dir <project-dir>`. This creates `example.drawio` and
`example.projection.md` there. Do not infer a destination from the current
directory. A direct command without a destination reports an error.

For Loom work, start from `docs/loom/<change-id>/`. If starting at the
repository root, create the diagram with `new <name> --change-id <change-id>`
(or `new <backend-id> <name> --change-id <change-id>`), then run
`cd docs/loom/<change-id>/` before using any relative diagram path. The id must
name an existing `docs/loom/intent/<change-id>.md`; an explicit id inside a
change directory must match that directory. Generated files go to
`docs/loom/<change-id>/diagrams/`. Run
`python3 <plugin-root>/skills/loom-interactive-diagram/scripts/diagram.py`
with one of these commands:

- `list-backends`: show available formats.
- `new <name>`: create an empty draw.io diagram and matching projection.
- `new <backend-id> <name>`: create one with a selected format.
- `new <name> --output-dir <project-dir>`: create a standalone diagram and
  projection at the explicitly selected directory.
- `copy <source> --change-id <change-id>`: copy an existing diagram into the
  selected Loom change, with a new projection beside the copy. From its change
  directory, omit `--change-id`. Outside Loom, use
  `copy <source> --output-dir <project-dir>` after the user names that project
  directory. Never overwrite an existing diagram or projection.
- `project [diagrams/<name>.<ext>]`: regenerate a managed
  projection after an edit. The path must stay inside the selected change's
  `diagrams/` directory, including after resolving symlinks.
- `project <diagram-path> --in-place`: for a standalone diagram or after the
  user chooses direct editing, regenerate the adjacent projection. A missing
  projection is created for a registered diagram format. Symlinked diagram
  and projection paths are rejected; ask for the resolved original path.
- `check [<diagram-path>]`: validate one diagram or every registered diagram
  under `diagrams/` and every diagram linked from `spec.md`; return nonzero
  and name each invalid file or difference. Spec links resolve from `spec.md`.
  Read-only checks of named external diagrams remain supported. Outside Loom,
  pass the selected diagram path explicitly.

Before each external edit, ask the user whether to copy the diagram into the
project; show the resolved source path and the proposed destination. Wait for
the answer before copying or editing. Ask on every new edit request, even if
the user has previously selected direct editing, and do not act on silence.
If the user chooses a copy during Loom work, put it in
`docs/loom/<change-id>/diagrams/` and tell them that actual path. Outside
Loom, ask for the project directory if it is unknown, then use `--output-dir`.
If the user chooses the original, use its resolved path and `--in-place` after
the edit; the original and its adjacent projection may change, and no backup
is made. A read-only check does not trigger the copy question.

The default backend is `drawio`. A backend is one file in `backends/`; the
selection is recorded in the projection header. See `references/backends.md`
for the callable contract and `references/projection.md` for the text format.

For a Loom copy or new diagram, run the watcher and follow-up commands from
`docs/loom/<change-id>/`. For standalone or direct external editing, use the
selected diagram's path instead. When the user is editing during the current
conversation turn, tell them which diagram you are waiting for and keep the
turn active. After your last write,
run `python3 <plugin-root>/skills/loom-interactive-diagram/scripts/wait_for_save.py
<diagram-path> --timeout 120` in a live tool session that yields output
while the process keeps running; retain its session identifier. Wait for
`READY`, then tell the user they can edit and save that diagram. Continue
polling that same tool session during this turn for `CHANGED`, `TIMEOUT`, or
`ERROR`. `READY` means the content baseline was read. `CHANGED` means that
same file has held changed content across two reads; it does not identify who
or what wrote it. Read the file, run
`python3 <plugin-root>/skills/loom-interactive-diagram/scripts/diagram.py
project <diagram-path>` for a managed diagram or `project <diagram-path>
--in-place` for a standalone diagram or explicitly selected original. Run
`python3 <plugin-root>/skills/loom-interactive-diagram/scripts/diagram.py
check` to validate all managed diagrams, or `check <diagram-path>` for a
standalone or external original. Restate the visible edit. On `TIMEOUT`, say that no
changed save was observed and the user can still send a message to continue.
On `ERROR`, name the file and ask the user to save it again. Unrelated file
changes and identical-content saves do not end the wait. The watcher cannot
resume a turn after it has ended.

For edits outside an active wait, read the saved file and follow the same
`project` then `check` procedure.
For VS Code and desktop setup and the acceptance procedure, follow
`references/editor-setup.md`. Do not claim live synchronization from a static
file check.
