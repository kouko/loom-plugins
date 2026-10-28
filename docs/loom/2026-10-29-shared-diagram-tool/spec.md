# 跨站共用的圖表討論工具（draw.io 為首個後端） — spec
intent: 2026-10-29-shared-diagram-tool@3a626511bc1a134014e046f6d22f2d283c41372b
pre-build-review: required — this change adds a new shared tool to the loom-workflow plugin and registers it in the contract package consumed by three plugins; it modifies write-spec and architecture-design station text, adds a check script, a backend registry, tests, and a CHANGELOG budget-exception

## Requirements
REQ-1 — Agent writes diagram, VS Code shows it instantly
  WHEN the agent writes or updates a diagram file in the change's diagrams/ folder while the user has the same file open in VS Code's Draw.io Integration editor, the diagram shall reflect the new content without the user reopening the file, provided the VS Code text buffer is clean (saved or autosave enabled) → Acceptance #1

REQ-2 — User hand-edits diagram, agent reads it back
  WHEN the user makes a manual edit to the open diagram in VS Code's Draw.io Integration editor or the draw.io desktop app and saves the file, the agent reading the same diagram file shall restate the change correctly → Acceptance #2

REQ-3 — Diagram carries a text projection and the check enforces consistency
  The tool shall require each diagram referenced by a spec to carry a text projection (node and edge list) committed alongside it; the mechanical check script shall fail when the projection disagrees with the diagram, naming the difference → Acceptance #3

REQ-4 — Malformed or non-conforming diagrams are rejected
  IF a diagram file is malformed (cannot be parsed in its backend's declared format) or does not follow the backend's format convention, THEN the mechanical check script shall fail and name the offending file → Acceptance #4

REQ-5 — Clean-environment reproducibility
  Following the repository documentation, a clean environment with prerequisites installed shall reproduce the collaboration loop of Acceptance #1 and #2 → Acceptance #5

REQ-6 — Desktop app sync behaviour documented and working
  WHEN the same diagram file is open in the draw.io desktop app and autosave is enabled, the diagram shall synchronize without a click; when autosave is disabled, the app shall show the "file modified" prompt whose click displays the new content → Acceptance #6

REQ-7 — Backend registry with user selection
  The tool shall expose a registry of backends and a selection mechanism by which the user chooses the backend for the current diagram; the registry shall support multiple registered backends, and at least one minimal demonstration backend other than draw.io shall prove that registration and selection work → Acceptance #7

REQ-8 — Single shared home for diagram rules
  The generation, projection and validation rules for diagram files shall live in one shared location (the tool's skill), and station documents that use diagrams shall reference that location rather than restating its content → Acceptance #8

## Design decision
- New shared tool `loom-workflow:loom-diagram` in the loom-workflow plugin, next to loom-visualization — user-decided (scope B: cross-station shared tool, loom-workflow home)
- Backend registry: `backends/` folder in the skill, one file per backend exposing a minimal contract (extension, generate, project, check); `scripts/diagram.py` discovers backends by directory listing, so adding a backend is one file with no routing edit — agent-decided
- Backend contract as a plain callable protocol (function-per-capability), not classes or frameworks — data over abstractions; each backend self-contained so a new backend can't reach into another — agent-decided
- Selection mechanism: each diagram's projection file header carries `backend: <id>`; the tool reads the header to dispatch generation/validation; default `drawio` — the choice lives with the artifact (data over abstractions) — agent-decided
- Diagram file location: `docs/loom/<change-id>/diagrams/<slug>.<ext>` with `<slug>.projection.md` beside it — a convention, not a new artifact_type glob (artifact_types is reserved and not yet consumed by the checker) — agent-decided
- drawio backend writes uncompressed pretty-printed XML (mxfile or bare mxGraphModel) per draw.io AI generation rules (cells 0 and 1 mandatory, unique IDs, no XML comments); layout via the desktop CLI `--layout` when available, else fixed coordinates from the agent — agent-decided
- check_diagram.py is folded into `scripts/diagram.py` (subcommands new / project / check / list-backends); it validates structure (XSD when xmllint is available, else stdlib structural checks), regenerates the projection, diffs it against the committed projection, and reports a difference path; render-to-image verification stays optional via the draw.io CLI — agent-decided
- Station integration: write-spec SKILL.md gains a short "diagram collaboration" pointer to `loom-workflow:loom-diagram`; architecture-design SKILL.md gains the same pointer; neither restates format or validation rules — agent-decided
- Mechanism registration: new tool in manifest `tools:` with owner loom-workflow; skill count 23→24 declared via a `budget-exception` CHANGELOG line per PRINCIPLES non-negotiable 4; description catalog and sync manifests updated in the same change — agent-decided
- A minimal demonstration backend `demo-json` ships to prove registration and selection (writes a JSON description + a projection); Penpot and other real backends are out of scope — agent-decided

## Alternatives considered
- Keep the capability inside write-spec (the withdrawn 2026-10-27 change): rejected — a second consumer (architecture-design) and the user's cross-station discussion scenario make the tool shared, not station-owned
- Extend loom-visualization to also handle files: rejected — its boundary is chat output (tables/ASCII/Mermaid in chat); a file-editing canvas is a second role that complects the skill
- MCP server integration (lgazo/abossard): deferred — a running daemon and an external project braid the artifact contract; the file-on-disk loop satisfies the acceptance; re-trigger: when the loop proves valuable and agent-in-diagram annotation is demanded
- Backends as Python classes with inheritance: rejected — the module criteria favour one-file-per-backend with a plain protocol; classes add coupling without a second consumer benefit

## Current state evidence
- Forward: loom-design/skills/write-spec/SKILL.md §Step 2 "UI flows" — today UI flows are written in text only; loom-design/skills/architecture-design/SKILL.md — architecture documents use Mermaid in the document, none reference a shared diagram tool
- Reverse: capture-intent hands confirmed intent to write-spec; write-plan consumes the spec; stations read loom-workflow skills by name (cross-plugin delegation contract)
- Error: no diagram validation exists today; no diagram script in the repo; grep finds no diagram file convention or backend registry
- Data: a change folder today contains intent.md, spec.md, plan.md, evidence/ — no diagrams/ folder, no .drawio files, no projection files
- Boundary: this change adds the shared tool (skill + script + backends/ + tests) and two one-line station pointers; it does not add an artifact_type glob, a station, or a second real backend

## UI flows
### Surface: diagram file in VS Code Draw.io Integration editor
- Empty → no diagram in `diagrams/` yet; user opens a non-existent path → VS Code shows empty editor; way out: agent runs `diagram.py new` in the discussion
- In progress → agent writes the diagram file; the file on disk updates; the open webview merges the new XML and renders instantly; way out: wait for merge complete
- Error → malformed XML or non-conforming format; `diagram.py check` fails naming the file and the difference; way out: user or agent fixes the file and re-runs the check
- Success → diagram displays the intended flow; text projection matches; user can hand-edit

### Surface: diagram file in draw.io desktop app
- Empty → no diagram in `diagrams/` yet; user opens a non-existent path → app shows blank canvas; way out: agent runs `diagram.py new`
- In progress → agent writes the diagram file; within ~5 s the app detects the change; if autosave is enabled the diagram auto-merges silently; if disabled the status bar shows "The file has been modified. Click here to synchronize."; way out: user clicks status bar
- Error → stale file written (older copy of itself); modal "The file has been modified. Overwrite or Synchronize?"; Synchronize adopts the disk version; way out: user chooses Synchronize (or avoids stale writes by not editing the same file simultaneously in two editors)
- Success → diagram displays the intended flow; text projection matches; user can hand-edit

### Surface: `diagram.py` tool in a station conversation
- Empty → no backends registered or no diagrams yet; `diagram.py list-backends` prints the empty list and the way to add one; `diagram.py new` without a backend id defaults to drawio
- In progress → `diagram.py new` writes the file and its projection, printing the path; generation is instant for small diagrams
- Error → unknown backend id → prints the registered ids; unreadable input → names the file; projection mismatch → names the difference
- Success → `diagram.py check` exits 0 and prints "✓ projection matches"; `list-backends` shows drawio and demo-json

### Path walk (single graph)
Any station discussion → user or agent asks for a diagram → agent runs `diagram.py new` (or the user opens the editor and hand-draws) → user edits in the editor → saves → agent reads → discussion continues → the diagram's projection is checked at build. One forward edge (new → open), one back edge (edit → read). No orphan surface, no dead end.