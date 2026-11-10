# Planning command recovery — spec
intent: 2026-11-11-planning-command-recovery@c4f03ba9
pre-build-review: required — the launcher and checker command-line help are a shared tooling contract.

## Requirements
REQ-1 — Recover from observed command mistakes
  WHEN an agent supplies the observed redundant checker path or omits the launcher mode, the tool shall provide enough guidance for an independent agent to correct the call and complete plan validation → Acceptance #1
REQ-2 — Discover valid usage
  WHEN an agent requests usage information, the tool shall expose a valid launcher invocation for planning and accurately describe the supported checker commands → Acceptance #2
REQ-3 — Preserve validation
  The tool shall preserve successful existing invocations and reject invalid invocations without reporting a successful validation → Acceptance #3

## Design decision
- agent-decided — REQ-1: clarify that the launcher selects the checker implicitly; report complete mode-plus-command usage on invalid launcher calls and a targeted redundant-checker-path diagnostic. Preserve exit 2; never silently normalize invalid arguments.
- agent-decided — REQ-2: support explicit top-level help and mode-prefixed checker help, with exit 0 for help alone. Launcher help must work before runtime/cache provisioning. Keep the checker command list in its existing usage text and guard its coverage against COMMANDS; no new command registry or framework.
- agent-decided — REQ-2: include plan and charter in checker usage and explain plan's file path versus intake's station/change-id. Keep custom --script forwarding intact, including its own help arguments.
- agent-decided — REQ-1/3: the user requested a same-pattern audit. Correct emitted recovery hints in host hook manifests and checker handlers that omit the mode, leave out the original command's arguments or assume the launcher is on PATH; preserve execution and failure policy. This is the same invalid-recovery-command class, not a new workflow.
- agent-decided — retain current runtime repair and read-only mode semantics. No new setting, persistent state, external service or one-way door is needed.

## Alternatives considered
- Documentation alone: rejected because the observed error/help path remains incomplete even with correct station examples.
- Accept redundant script arguments automatically: rejected because it expands accepted syntax and hides caller mistakes.
- Replace parsing with a CLI framework: rejected as unnecessary complexity for help and diagnostics.

## Current state evidence
- Forward: loom-code/scripts/loom-python:10 — mode parsing precedes default checker dispatch.
- Reverse: loom-code/skills/write-plan/SKILL.md:324 — valid mode-plus-plan call already documented.
- Error: loom-code/scripts/loom_checker.py:94 — unknown commands print incomplete usage; hooks/hooks-codex.json Stop emits a modeless recovery command.
- Data: loom-code/scripts/loom_checker/command_handlers/plan.py:19 — plan accepts one file path; command_handlers/intake.py:29 accepts station and change id.
- Boundary: loom-code/tests/test_loom_python_runtime.py — preserve runtime provisioning, offline ready and explicit script execution.

## UI flows
| Case | What the agent does | What it sees |
|---|---|---|
| Empty | Runs the launcher with no arguments | Exit 2 with mode/command usage and a complete planning example; retry using that example. |
| Help | Requests launcher help without a configured runtime | Exit 0 and local usage text; no installation or cache creation. |
| Checker help | Requests help after a valid mode | Exit 0 and supported checker commands including plan and charter. |
| Missing mode | Supplies the checker path before the mode | Exit 2, explanation that the checker is implicit, and a valid launcher form. |
| Redundant path | Supplies the checker path after the mode | Exit 2 with the instruction to omit that path and use the command directly. |
| Correct call | Supplies the mode, plan command and existing plan path | Existing validation result: 0 for a valid plan, 1 for a rule violation, 2 for invalid arguments. |
| Custom script | Uses explicit script selection with its arguments | Existing script output and exit code, including script-owned help. |
| Hook recovery | Reads a failed hook's recovery hint | A mode-bearing recovery instruction retaining the operation or explicitly retaining its original arguments. |

Help is immediate plain text; existing runtime repair progress is unchanged.
Error recovery retries the same plan without changing its content. No user data
is rewritten, and abandoning a failed command leaves the repository intact.
