# Help-first CLI result consistency — spec
intent: 2026-11-13-cli-result-contract@2f29db8ab63a49c5b69decf2973d201112e63f59
pre-build-review: required — extends the public CLI discovery contract

## Requirements

REQ-1 — Traceable command inventory and shared meanings
  The Loom CLI shall document all sixteen principal commands' accepted inputs, result families, process exits, observed outcomes, effects and exceptions against their actual handlers, including the distinction between process success and domain completion → Acceptance #1

REQ-2 — Source-accurate operational guidance
  The Loom CLI shall describe each principal command's actual arguments, modes, prerequisites, outcomes, error paths and operational consequences in help, with an independent source-by-source comparison for all sixteen commands → Acceptance #2

REQ-3 — Compatible and explicit adoption
  WHEN an existing invocation is used, the Loom CLI shall preserve its text streams, exits, checks, authorization and published preparation-v1/delivery JSON contracts, and disclose each command's supported modes without introducing any new JSON interface → Acceptance #3

REQ-4 — Accurate safe discovery first
  WHEN an operator invokes any principal command with exactly --help or -h as its only following argument, the Loom CLI shall return clear text guidance and exit 0 before executing its handler, reading stdin or performing repository/network work, describing actual inputs, prerequisites, outcomes, effects and recovery; independent help conformance verification shall precede delivery → Acceptance #4

## Design decision

- **Help-only delivery (user-decided):** on 2026-11-13 the user accepted “先把 help 整理獨立交付，JSON 留下一輪”. This supersedes the earlier two-wave JSON obligation in this change. Existing commits preserve that proposal's history; this active spec requires only inventory, accurate safe help and compatibility. JSON expansion is deferred to a separate future change whose intent and design are not confirmed here. Preserve the original failed checkpoint and subsequent correction/recheck evidence unchanged.
- **Discovery surface (agent-decided):** extend the existing dispatcher-level `COMMAND_HELP` exact-match path rather than teaching every handler a new parser. `COMMANDS` remains the command inventory; no parallel capability registry or rules framework is added. Update overall discovery text so it no longer advertises only six detailed pages. Non-exact combinations remain ordinary invocations with their existing behavior; help does not make `publish --help --json` safe or supported.
- **Safe boundary (agent-decided):** safe help means direct checker invocation or `loom-python --ready <command> --help/-h` with a ready runtime. It is synchronous, finite text on stdout, empty stderr, no handler dispatch, stdin read, subprocess, artifact parsing or network request. Tests must install tripwires for these operations and run outside a Git repository with unavailable network. Launcher startup/imports remain startup; the requirement does not redesign them. A missing ready runtime retains launcher exit 86 without provisioning. `--repair` may download/install Python and dependencies and write cache/locks before checker help; help must not promise offline or side-effect-free repair. Launcher own help remains separate.
- **Help content (agent-decided):** use a shared editorial checklist, not identical filler. Each page states purpose, complete supported syntax/modes/defaults, operand kind/path resolution, prerequisites, stdout/stderr and exits, completion limits, effects and recovery appropriate to the command. The evidence table is the change's conformance reference. Preserve the six existing pages' valuable examples, authenticity cautions, JSON semantics and workflow pointers; correct discrepancies instead of flattening them. Runtime help may cite portable bundled guidance, never this repository's development records.
- **Shared result semantics (agent-decided):** document result families instead of forcing all commands into one envelope. Distinguish process exit, check status, notice/diagnostic, command data, completion scope and authorization. Progress is never terminal success. Writer partial success remains documented text; no structured lifecycle/progress schema is added. The inventory explicitly retains CI annotations, hook host responses, delivery observations and preparation validation as separate families.
- **Deferred JSON (user-decided):** no new selector, serializer, result family, schema, data payload or consumer migration is part of this delivery. The retained research and previous spec history are consulted evidence, not an implemented contract or a confirmed next-change design.
- **Compatibility (agent-decided):** default text and all other commands retain current parsing/streams/exits; preparation v1 and delivery objects retain their existing selector/error boundaries. No broad parser cleanup, new global yes/force, network retry, dry-run promise, authorization relaxation, hook migration or launcher rename. Help documents only currently implemented JSON support.
- **Verification (agent-decided):** independent verification must inspect content, not merely count headings or snapshot prose. All sixteen exact-help pairs must be tested with handler/subprocess/stdin tripwires, outside-repository discovery, and ready-runtime/no-repair behavior. Exercise representative existing six-page and non-help text/JSON/hook cases for compatibility. Compatibility verification exercises existing preparation and delivery JSON consumers; it does not test or claim a new schema. No live publish, land, hook-install or cleanup is needed to verify help; use isolated fakes for dangerous paths. Preserve all existing worktrees and their evidence.

## Alternatives considered

- JSON-first implementation: rejected because the user's latest confirmed ordering makes accurate discovery the first deliverable.
- Add the same generic help paragraph to every handler: rejected because modes, effects, exits and completion differ materially, and per-handler dispatch risks executing work during discovery.
- Rewrite parsers into a new CLI framework or generate a second capability registry: rejected as unnecessary scope and a second drift surface.
- Reuse preparation v1 by appending undocumented data or wrapping existing prose: rejected because that changes a published family and loses typed command meaning.
- Retrofit all sixteen with JSON: rejected because hooks, CI adapters and writers carry distinct observation/partial-write contracts outside this batch.

## Current state evidence

- Forward: `loom-code/scripts/loom_checker.py::main`, `COMMANDS`, `COMMAND_HELP` — sixteen handlers and now sixteen exact-help pages; original six-page baseline and correction history remain in the evidence store.
- Reverse: `loom-code/skills/write-plan/SKILL.md` contract startup; `loom-code/skills/closing-review/SKILL.md` reviewer-count/finalization; `.github/workflows/loom-pr-floor-reusable.yml` pr-floor; `loom-code/hooks/hooks*.json` delivery host adapters — real consumers constrain compatibility.
- Error: `loom-code/scripts/loom_checker.py::main` UsageError/internal branches; `command_handlers/sync.py::cmd_sync_trunk` fetch warning returns 0; `command_handlers/publish.py::_observe_required_ci` publication may precede failed observation.
- Data: `loom-code/scripts/loom_checker/preparation_output.py::new_result`; `loom-code/scripts/loom_checker/command_handlers/publish.py::cmd_delivery`; `loom-code/scripts/loom_checker/command_handlers/reviewer_count.py::cmd_reviewer_count` — preparation-v1 object, delivery object and integer floor are distinct existing shapes.
- Boundary: `loom-code/scripts/loom-python::ready` and repair branch; `command_handlers/land.py::execute_cleanup`; `command_handlers/push.py::_native_hooks` — provisioning and mutation implementations are not redesigned by this change.

Full per-command help obligations and traceable source anchors: [help-conformance evidence](evidence/help-conformance.md). Retained trade study: [CLI guidance research](../research/2026-11-13-cli-agent-design-guidelines.md). These are development evidence, not runtime dependencies.

## UI flows

| Case | What the operator does | What they see |
|---|---|---|
| Help success | Runs any of the sixteen commands followed only by --help or -h with a ready runtime | Text describing its real purpose, complete syntax, prerequisites, outputs/exits, effects and recovery; exit 0, no actual work |
| Help empty state | Runs help outside a repository or without that command's required files | The same complete guidance and exit 0; no repository or input is required |
| Help in progress | Reads exact help | Finite synchronous text, no progress or background task |
| Runtime unavailable | Uses --ready with no valid cached runtime | Existing `loom-python: checker runtime is missing or invalid; run loom-python --repair with the same arguments in an agent station.` and exit 86; consciously provision through --repair if desired, then retry |
| Other invocation | Combines help with another argument or misspells a command | Existing ordinary parsing/errors and exits; use the exact help form to recover; no new permissive help parsing |

Normal command operations remain as inventoried; help explains but grants no authority to execute them. Reading help, returning to the terminal, correcting an invocation and retrying require no persistent state and preserve repository content. Writer recovery uses observation before retry because a nonzero terminal result may follow a successful write. No new irreversible operation is introduced. Narrow/piped terminals receive plain text with no TTY-dependent mode selection.
