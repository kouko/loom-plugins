# 跨站共用的圖表討論工具（draw.io 為首個後端） — spec
intent: 2026-10-29-shared-diagram-tool@93d7b523f79445d925380c9dcbeda8c289537fd6
pre-build-review: required — this change adds a new shared tool to the loom-workflow plugin and registers it in the contract package consumed by three plugins; it modifies write-spec and architecture-design station text, adds a check script, a backend registry, tests, and a CHANGELOG budget-exception

## Requirements
REQ-1 — Agent writes diagram, VS Code shows it instantly
  WHEN the agent writes or updates a diagram file in the change's diagrams/ folder while the user has the same file open in VS Code's Draw.io Integration editor, the diagram shall reflect the new content without the user reopening the file, provided the VS Code text buffer is clean (saved or autosave enabled) → Acceptance #1

REQ-2 — User hand-edits diagram, agent reads it back
  WHEN the user makes a manual edit to the open diagram in VS Code's Draw.io Integration editor or the draw.io desktop app and saves the file, the agent reading the same diagram file shall restate the change correctly → Acceptance #2

REQ-3 — Diagram carries a text projection and the check enforces consistency
  The tool shall require each diagram referenced by a spec to carry a text projection (node and edge list) committed alongside it; the mechanical check script shall fail when the projection disagrees with the diagram, naming the difference. A spec references a diagram with a Markdown link whose target ends in a registered backend extension. `check` enumerates those links relative to the spec path, including links outside the conventional diagrams folder, and validates every target and its adjacent projection; it also checks every registered diagram in the change's diagrams folder so an unlinked file cannot hide there → Acceptance #3

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

REQ-9 — Read a saved user edit during the active turn
  WHEN the agent is waiting for a diagram edit during the active conversation turn and the user saves a changed diagram in VS Code Draw.io Integration or draw.io desktop, the agent shall detect the changed file, read it, and restate the edit without requiring a follow-up user message → Acceptance #9

REQ-10 — Ignore unchanged and unrelated saves
  WHILE the agent is waiting for a diagram edit, changes to other files and saves that leave the diagram content unchanged shall not be reported as a diagram edit → Acceptance #10

## Design decision
- New shared tool `loom-workflow:loom-interactive-diagram` in the loom-workflow plugin, next to loom-visualization — user-decided (scope B: cross-station shared tool, loom-workflow home)
- Backend registry: `backends/` folder in the skill, one file per backend exposing a minimal contract (extension, generate, project, check); `scripts/diagram.py` discovers backends by directory listing, so adding a backend is one file with no routing edit — agent-decided
- Backend contract as a plain callable protocol (function-per-capability), not classes or frameworks — data over abstractions; each backend self-contained so a new backend can't reach into another — agent-decided
- Selection mechanism: each diagram's projection file header carries `backend: <id>`; the tool reads the header to dispatch generation/validation; default `drawio` — the choice lives with the artifact (data over abstractions) — agent-decided
- Diagram file location: `docs/loom/<change-id>/diagrams/<slug>.<ext>` with `<slug>.projection.md` beside it; a spec references one through a Markdown link, and `check` resolves linked diagram paths from the spec directory even when outside the conventional folder — a convention, not a new artifact_type glob (artifact_types is reserved and not yet consumed by the checker) — agent-decided
- drawio backend writes uncompressed pretty-printed XML (mxfile or bare mxGraphModel) per draw.io AI generation rules (cells 0 and 1 mandatory, unique IDs, no XML comments); layout via the desktop CLI `--layout` when available, else fixed coordinates from the agent — agent-decided
- check_diagram.py is folded into `scripts/diagram.py` (subcommands new / project / check / list-backends); it validates structure (XSD when xmllint is available, else stdlib structural checks), regenerates the projection, diffs it against the committed projection, and reports a difference path; render-to-image verification stays optional via the draw.io CLI — agent-decided
- Station integration: write-spec SKILL.md gains a short "diagram collaboration" pointer to `loom-workflow:loom-interactive-diagram`; architecture-design SKILL.md gains the same pointer; neither restates format or validation rules — agent-decided
- Mechanism registration: new tool in manifest `tools:` with owner loom-workflow; skill count 23→24 declared via a `budget-exception` CHANGELOG line per PRINCIPLES non-negotiable 4; description catalog and sync manifests updated in the same change — agent-decided
- A minimal demonstration backend `demo-json` ships to prove registration and selection (writes a JSON description + a projection); Penpot and other real backends are out of scope — agent-decided
- Active-turn waiting uses a small Python file-content poller for one diagram with a finite timeout; it snapshots after the agent's last write and reports a new digest only after a stable read — agent-decided, because the host-side Node event watcher worked in the local probe but failed with EMFILE in the sandbox, and a poller needs no new runtime dependency
- The skill tells the agent to keep the turn active while waiting, then read the changed diagram, regenerate its projection, check it, and restate the change; after timeout it states that no changed save was observed and allows the existing manual prompt — agent-decided, because a skill cannot restart an ended host turn
- A content change is evidence of a changed file, not the editor or actor that wrote it; the agent shall not claim actor attribution from the watcher alone — agent-decided

## Alternatives considered
- Keep the capability inside write-spec (the withdrawn 2026-10-27 change): rejected — a second consumer (architecture-design) and the user's cross-station discussion scenario make the tool shared, not station-owned
- Extend loom-visualization to also handle files: rejected — its boundary is chat output (tables/ASCII/Mermaid in chat); a file-editing canvas is a second role that complects the skill
- MCP server integration (lgazo/abossard): deferred — a running daemon and an external project braid the artifact contract; the file-on-disk loop satisfies the acceptance; re-trigger: when the loop proves valuable and agent-in-diagram annotation is demanded
- Backends as Python classes with inheritance: rejected — the module criteria favour one-file-per-backend with a plain protocol; classes add coupling without a second consumer benefit
- A persistent background watcher or host-trigger bridge: rejected for this change — the user chose waiting only within the active turn; a skill alone cannot resume an ended turn
- A Node filesystem-event watcher: rejected for the runtime path — the probe succeeded on the host, but fs.watch returned EMFILE in the sandbox; polling the one target file is portable and simpler here

## Current state evidence
- Forward: loom-design/skills/write-spec/SKILL.md §Step 2 "UI flows" — today UI flows are written in text only; loom-design/skills/architecture-design/SKILL.md — architecture documents use Mermaid in the document, none reference a shared diagram tool
- Reverse: capture-intent hands confirmed intent to write-spec; write-plan consumes the spec; stations read loom-workflow skills by name (cross-plugin delegation contract)
- Error: no diagram validation exists today; no diagram script in the repo; grep finds no diagram file convention or backend registry
- Data: a change folder today contains intent.md, spec.md, plan.md, evidence/ — no diagrams/ folder, no .drawio files, no projection files
- Boundary: this change adds the shared tool (skill + script + backends/ + tests) and two one-line station pointers; it does not add an artifact_type glob, a station, or a second real backend
- New wait path: `loom-workflow/skills/loom-interactive-diagram/SKILL.md` currently waits for the user's follow-up message before reading disk; the 2026-10-31 temporary probe observed one changed-content event for an in-place write, an atomic replacement, and a VS Code editor save, but did not exercise agent turn resumption

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
Any station discussion → user or agent asks for a diagram → agent runs `diagram.py new` (or the user opens the editor and hand-draws) → user edits in the editor → saves → agent reads and restates the change → agent runs `diagram.py project` to regenerate the projection → agent runs `diagram.py check` before committing and again at build → discussion continues. One forward edge (new → open), one back edge (edit → read). No orphan surface, no dead end.

### Surface: active-turn wait for a saved diagram edit
- Empty → the agent has no diagram path to monitor; it asks the user to open the shared diagram before beginning the wait
- In progress → the agent says it is waiting for a save of that diagram and keeps the turn active; a content change in that file ends the wait, while unrelated files and identical-content saves do not
- Error → the diagram disappears or becomes unreadable; the agent names the problem and asks the user to save the diagram again
- Success → the agent reads the saved diagram, regenerates and checks its projection, and restates the visible edit without a follow-up message; if the finite wait expires first, it says no changed save was observed and the user can still send a message to continue
