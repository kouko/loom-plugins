# Standalone diagrams and explicit external-file editing — spec
intent: 2026-11-01-standalone-diagram-files@699f87dbd4bbe8582820e6aa281093930c565224
confirmed-behavior: 2026-11-01 @cf509c5
pre-build-review: required — the change adds a public command surface and allows explicit in-place updates outside the managed Loom store

## Requirements
REQ-1 — Standalone creation
  WHEN a user requests a new draw.io diagram without a Loom change, the tool shall create the diagram and projection at the explicitly selected destination and report both paths → Acceptance #1

REQ-2 — Ask before editing an external diagram
  WHEN an existing diagram outside the current Loom-managed diagram directory is about to be edited, the agent shall ask whether to create a project copy and shall wait for the user's answer before either copying or editing → Acceptance #2

REQ-3 — Honor the selected source
  WHEN the user chooses in-place editing, the tool shall update and check a projection for the selected original without copying it; WHEN the user chooses a copy, the tool shall leave the original unchanged → Acceptance #3

REQ-4 — Managed copy location
  WHEN a user chooses a project copy during a Loom change, the tool shall put the copied diagram and its projection in that change's managed diagram directory → Acceptance #4

REQ-5 — Preserve managed creation and prevent implicit external writes
  WHEN a new diagram is created during a Loom change, the tool shall use that change's managed diagram directory; WHEN an external path is supplied for a write without an explicit in-place selection, the tool shall reject it without changing the original → Acceptance #5

REQ-6 — Explain both uses
  WHERE diagram guidance is shown, the skill shall distinguish standalone work from Loom work, require the copy question on every external edit, and name the actual destination → Acceptance #6

## Design decision
- agent-decided — Extend the existing skill and command rather than adding a second diagram skill; both uses share the same backend, projection, validation, and save watcher.
- agent-decided — Standalone creation requires an explicit destination; no current-directory `diagrams/` fallback is introduced because PR #125 removed that accidental destination.
- agent-decided — Standalone copying also requires an explicitly selected project directory; the agent asks for one when absent and the command never guesses from the current directory.
- agent-decided — A copy operation refuses an existing destination and never overwrites the source; this keeps the user's existing data intact when a name collides.
- agent-decided — Direct editing of an external original requires `project <path> --in-place` after the agent's question; the ordinary managed `project` command keeps its current boundary. Show the resolved original path before asking; reject a symlinked diagram path and ask for its resolved path instead.
- agent-decided — Before an in-place projection write, reject an existing or dangling symlink at the adjacent projection path. An absent regular projection is created using the registered backend selected by the diagram extension; an unsupported extension fails without a write.
- user-decided — Ask on every intended edit of an external diagram whether to make a project copy, even when a project copy is the recommended path. The answer selects the source to edit.
- user-decided — An explicit choice to edit the external original permits in-place editing; during Loom work this is an exception to the managed path policy. The original and its adjacent projection may then change outside the change store.
- user-decided — A project copy made during Loom work and its projection remain under `docs/loom/<change-id>/diagrams/`; use the plain phrase “copy into the project” in conversation and show the concrete path.

## Alternatives considered
- Add a separate standalone skill — rejected because it would duplicate the backend, projection, watcher, and editor instructions.
- Allow every `project <path>` to write anywhere — rejected because a path argument alone does not prove the user chose to edit the original.
- Always copy external diagrams into the Loom change — rejected because the user requires a question on each edit and may choose the original.
- Infer a standalone project destination from the current directory — rejected because it could copy into the wrong project without the user's choice.
- Require a Loom change for every diagram — rejected because it leaves the confirmed standalone use unavailable.

## Current state evidence
- Forward: `loom-workflow/skills/loom-interactive-diagram/SKILL.md:14-38` documents `new`, `project`, and `check` from a Loom change, with managed creation and projection.
- Reverse: `loom-design/skills/architecture-design/SKILL.md:19-20` recommends this skill during an architecture discussion that need not begin from a Loom change.
- Error: `loom-workflow/skills/loom-interactive-diagram/scripts/diagram.py:29-52,183-205` requires an intent for creation and projection and rejects external projection writes.
- Data: `loom-workflow/skills/loom-interactive-diagram/references/projection.md:1-28` defines an adjacent `.projection.md` with a backend header, nodes, and edges.
- Boundary: `loom-workflow/skills/loom-interactive-diagram/scripts/diagram.py:206-225` already supports read-only checks of explicitly named external files when their adjacent projection exists; PR #125 keeps managed writes inside the selected change.

## UI flows
| Case | What the user does | What they see |
|---|---|---|
| Standalone create | Requests a new diagram outside Loom and names a directory; agent runs `new <name> --output-dir <directory>` | Exit 0; prints the new diagram and projection paths, both in the named directory. |
| Standalone create without destination | Requests a new diagram outside Loom without naming where to save it | The agent asks for a directory before creating files; direct `new <name>` outside Loom exits 1 with `destination required outside Loom; use --output-dir DIR`. |
| Managed creation | Requests a new diagram for an existing Loom change; agent runs `new <name> --change-id <id>` or from that change's directory | Exit 0; prints diagram and projection paths in that change's diagram folder. |
| External edit prompt | Asks to edit an existing external diagram | Before any edit or copy, the agent shows the resolved source path and asks “Do you want to copy it into the project first?”; if a copy destination is not known, the agent asks for that directory too. |
| Standalone copy | Answers yes and names a project directory outside Loom; agent runs `copy <source> --output-dir <directory>` | Exit 0; prints the copy and its projection paths in the selected directory; the original remains unchanged. |
| Loom copy | Answers yes during a Loom change; agent runs `copy <source> --change-id <id>` or from that change's directory | Exit 0; prints the copy and its projection paths in that change's diagram folder; the original remains unchanged. |
| Direct edit selected | Answers no to the copy question; after editing the original, agent runs `project <path> --in-place` | Exit 0; prints the adjacent projection path. No copy is created; the original and any existing adjacent regular projection may change. |
| No answer | Does not answer the copy question | No file is copied or edited; the agent waits for the answer. |
| Source missing or invalid | Chooses an unavailable or invalid diagram | The command exits 1 with `<path>: missing or invalid diagram`; the agent asks for a valid diagram. |
| Source symlink | Chooses a symlinked diagram | The command exits 1 with `<path>: symlinked diagram; select resolved path`; no write occurs. |
| Projection symlink | Chooses direct edit while the adjacent projection is a symlink, including a dangling one | `project <path> --in-place` exits 1 with `<path>: symlinked projection; select a safe destination`; no write occurs. |
| No adjacent projection | Chooses direct edit of a registered diagram with no projection | `project <path> --in-place` creates an adjacent projection using the registered format and prints its path. |
| Unsupported extension | Chooses direct edit of a diagram with an unregistered extension | `project <path> --in-place` exits 1 with `<path>: unsupported diagram extension`; no projection is written. |
| Destination occupied | Chooses a project copy whose diagram or projection destination exists | `copy` exits 1 with `<path>: already exists`; leaves source and destination unchanged; the agent asks for a different name. |
| Copy without project directory | Answers yes outside Loom but has not named a project directory | The agent asks for it before copying; direct `copy <source>` outside Loom exits 1 with `destination required outside Loom; use --output-dir DIR`. |
| Save wait | Edits either selected diagram in an external editor during an active wait and saves changed content | The existing watcher reports `READY` then `CHANGED`; the agent updates and checks the selected projection. |
| Check mismatch | Checks a diagram whose projection differs | The command exits nonzero and names the projection difference; the user can regenerate it for the selected diagram. |

The copy question applies on each new edit request, including after an earlier edit or a resumed conversation. A clear direct-edit request still receives the question before this edit. A read-only check does not edit and does not trigger it. The user may abandon the question without changing files, then start another request. An error returns to destination or source selection without modifying the original. No automated transfer or background save watcher is introduced.
