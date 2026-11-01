# Auto-create store and station wiring for loom-memory — spec
intent: 2026-10-19-loom-memory-auto-create-and-station-wiring@7427832
pre-build-review: not-required — internal skill and script edits only; no security surface, no irreversible data action, no external contract, no cross-system ambiguity

## Requirements
REQ-1 — Record auto-creates the store
  WHEN Record runs against a store path that does not exist, the skill shall create the store from its bundled templates and complete the recording, with no separate user-initiated init step (carried detail: 「我不想讓使用者做 init 而是 record 要自動偵測並建立 store 資料夾」) → Acceptance #1
REQ-2 — Ship routes durable lessons
  WHEN Ship classifies the change for its pull-request body, it shall also route a qualifying durable repository lesson to loom-memory, symmetric with its existing git-memory invocation (carried detail: 「ship 站也要把 durable lesson 分流到 loom-memory」) → Acceptance #2
REQ-3 — Recall stays read-only
  WHEN Recall finds no store, it shall report a normal no-memory result and create nothing → Acceptance #3
REQ-4 — Retire approval unchanged
  WHEN Retire is requested, deletion shall still require explicit user approval → Acceptance #4
REQ-5 — Auto-created store validates
  WHEN the store is auto-created, `loom_memory.py validate <store>` shall exit 0 → Acceptance #5
REQ-6 — Existing stores unchanged
  WHEN a store already exists, every operation's current behaviour shall be preserved → Acceptance #6

## Design decision
- Store creation is a new `loom_memory.py` subcommand that instantiates the bundled `templates/` files, not agent hand-copying — agent-decided: the script stays the single writer of reserved store files; hand-copying drifts from the validated shape.
- The subcommand writes only when the target directory is absent or empty, refuses an existing populated store, and reports a detected legacy store as needing explicit migration — agent-decided: matches the skill's stated failure behaviour and keeps migration a separate explicit operation.
- Only Record creates; Recall never does — user-decided (2026-10-20): no user init; Record auto-detects and creates.
- Ship names loom-memory once, beside its git-memory classification sentence (`loom-code/skills/ship/SKILL.md:118`); the land checkpoint at `:230` stays git-memory-only — agent-decided: a lesson must ride the open change branch; land-time routing would arrive after the branch closes.
- The routing sentence repeats the scarcity bar (zero to one durable lesson per change is normal) and does not require loom-workflow to be installed — agent-decided: mirrors the git-memory sentence shape and the closing-review passage's plugin-optional stance.

## Alternatives considered
- Agent hand-copies the templates on first Record — rejected: no single writer; the validated store shape drifts.
- Recall creates the store when absent — rejected: breaks the normal no-memory contract (Acceptance #3).
- A separate user-facing init command — rejected: user chose no-init (2026-10-20).
- A durable-lesson outcome line in the closing-review finalize report (option B) — rejected: user chose A (2026-10-20); revisit only if lessons still leak after this change ships.

## Current state evidence
- Forward: `loom-workflow/skills/loom-memory/SKILL.md:102-119` — Record reads `index.md`, then regenerates and validates; no creation path exists anywhere in the skill.
- Reverse: `loom-code/skills/ship/SKILL.md:118-119` and `:230-231` — ship names only `loom-workflow:git-memory`; no durable-lesson routing to loom-memory.
- Error: `loom-workflow/skills/loom-memory/SKILL.md:69-76` — an absent store is a normal no-memory result; concept files without `index.md` are structural corruption.
- Data: `loom-workflow/skills/loom-memory/templates/memory-store-README.md:1-44` and `templates/memory-store-index.md` define the store's starting shape; `docs/loom/README.md:21` names `docs/loom/memory/**` as the store location convention.
- Boundary: `loom-workflow/skills/loom-memory/references/operations.md:102-113` — a legacy README-indexed store must stay an explicit-migration report; `SKILL.md:141-143` — Retire requires explicit user approval.

## UI flows
N/A
