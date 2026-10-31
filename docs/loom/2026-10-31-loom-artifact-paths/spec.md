# Per-change diagram artifacts — spec
intent: 2026-10-31-loom-artifact-paths@68c26f696ea4c01e853231debd77a31514be2cb4
pre-build-review: required — the diagram command's file path contract changes for every adopting repository

## Requirements
REQ-1 — Root invocation
  WHEN a change is identified and a diagram is created from the repository root, the tool shall write the diagram and projection under that change's `docs/loom/<change-id>/diagrams/` and create no root `diagrams/` → Acceptance #1
REQ-2 — Change-directory invocation
  WHEN a diagram is created from `docs/loom/<change-id>/`, the tool shall write it and its projection to that same change's `diagrams/` directory → Acceptance #2
REQ-3 — Bounded writes
  IF the change cannot be identified or a projection write targets a diagram outside that change's `docs/loom/<change-id>/diagrams/`, THEN the tool shall exit nonzero with a corrective error and write no diagram or projection outside the change directory → Acceptance #3
REQ-4 — Existing records
  The tool shall leave pre-existing diagrams and Loom records in place and preserve read-only validation of linked diagrams outside the managed directory → Acceptance #4

## Design decision
- `agent-decided` — `new [backend-id] <name> --change-id <id>` identifies the change when called from the repository root; inside a change directory, the directory identifies it. An explicit id must match an existing `docs/loom/intent/<id>.md`; requiring a named change avoids silently choosing among concurrent changes.
- `agent-decided` — Resolve the repository root by walking ancestors for `docs/loom/intent/`, and resolve the managed diagram directory before any write. The directory can be created for a confirmed intent that has no change folder yet. This makes the result independent of caller cwd and keeps new writes bounded.
- `agent-decided` — `project` may accept a diagram path or select managed diagrams from a change identified by cwd or `--change-id`. Resolve the diagram and projection before writing and reject paths escaping the managed directory, including symlinks. `check` retains its read-only ability to inspect spec-linked diagrams elsewhere.
- `agent-decided` — Keep the existing `diagrams/` subdirectory and projection filename pattern, because the skill and editor setup already name them; do not migrate old files.

## Alternatives considered
- Infer the change from the newest or sole intent: rejected because multiple concurrent changes make the destination unstable.
- Require every caller to change directory first: rejected because a root invocation would still be an easy source of misplaced files.
- Move existing root diagrams: rejected because the confirmed intent excludes modifying existing files.

## Current state evidence
- Forward: `loom-workflow/skills/loom-interactive-diagram/SKILL.md` documents `new`, `project`, `check`, and the change-directory workflow.
- Reverse: `loom-design/skills/write-spec/SKILL.md` and `loom-design/skills/architecture-design/SKILL.md` point to the shared diagram skill.
- Error: `loom-workflow/skills/loom-interactive-diagram/scripts/diagram.py` uses `DIAGRAMS = Path("diagrams")`, so root invocation writes at the root.
- Data: `loom-workflow/skills/loom-interactive-diagram/scripts/diagram.py` writes `<name>.<ext>` and `<name>.projection.md` together.
- Boundary: `loom-workflow/skills/loom-interactive-diagram/references/editor-setup.md` fixes the intended location at `docs/loom/<change-id>/diagrams/`; `check` also validates spec-linked files outside it.

## UI flows
- Empty: `new example` from a directory without an identifiable change → error naming `--change-id` or the change directory, exit 1; no files written. Retry with a valid change id or from its directory.
- In progress: creation and projection are local commands with no waiting phase.
- Success: `new example --change-id <id>` from the repository root → prints paths under `docs/loom/<id>/diagrams/`, exit 0; `new example` from that change directory → prints the same paths, exit 0.
- Error: an unknown change id → error naming the missing intent, exit 1; retry with an existing id.
- Error: `project <path>` for a diagram outside the selected change directory or through an escaping symlink → error naming the managed directory, exit 1; use a managed diagram path.
- Success: `project <managed-path>` → refreshes its adjacent projection and prints that path, exit 0.
- Success: `check <external-linked-path>` → validates without writing, as before.
