# Evidence-grounded next action — spec
intent: 2026-11-15-whats-next@2a4c4321
pre-build-review: required — a new published skill contract selects advice and must preserve authority across workflow boundaries

## Requirements
REQ-1 — Grounded recommendation
  WHEN explicitly invoked or asked for next-action advice in natural language, the skill shall recommend a concrete goal-relevant action with its evidence, rationale and expected result, separating facts from unknowns → Acceptance #1
REQ-2 — Necessary alternatives
  The skill shall lead with one recommendation, expose alternatives whose consequences or unresolved preferences materially change the choice with conditions for choosing them, avoid filler, and allow stopping when no grounded follow-up remains → Acceptance #2
REQ-3 — Bounded proactive use
  WHEN a blocker or new evidence invalidates the current direction, the skill shall permit the agent to reconsider its next action and avoid repeated advice interruptions while an authorized plan remains viable → Acceptance #3
REQ-4 — Authority continuity
  The skill shall preserve existing task ownership and authorization, continue already authorized unfinished work without a generic extra confirmation, and route genuinely new scope or required consent to the original owner without granting authority through advice → Acceptance #4
REQ-5 — Honest validation
  The delivery shall include reproducible routing and output cases plus matched ordinary-answer comparisons, reporting their limits without claiming unmeasured native-host effectiveness → Acceptance #5

## Design decision
- user-decided — independent skill named whats-next; one recommendation plus necessary alternatives. Carried quotes: “我想要 獨立 whats-next”; “好 採用 首選＋必要替代方案”; “那就先用  whats-next 吧”.
- user-decided — proactive scope and natural-language use were included in the confirmed intent restatement; retain the original worktree and keep history private.
- agent-decided (REQ-1–REQ-4) — one flat SKILL.md owns advice; no script, per-turn hook, queue or execution dispatcher. This adds instruction/discovery surface without a new runtime mechanism or gate.
- agent-decided (REQ-1) — inspect only evidence whose uncertainty can change the recommendation; no mandatory history, Git or remote scan. Latest user corrections outrank unsupported backlog inference.
- agent-decided (REQ-2) — always consider plausible alternatives internally, including stop, smaller steps and compatible combinations; display only consequential differences, and address user-supplied alternatives even if deferred. No fixed option count, table or final question.
- agent-decided (REQ-3) — discovery description permits contextual selection; this is eligibility, not a host guarantee. A failed command with a known recovery does not justify repeated replanning. Reconsider again only after material new evidence, constraint or outcome change; no persistent cooldown machinery.
- agent-decided (REQ-4) — selection does not authorize a new implementation, spend, egress, deletion or merge. An already permitted step continues through its original owner; genuine scope intake remains intact.
- agent-decided (REQ-5) — synthetic fixtures use invented projects and visible state, not private session packets. Compare ordinary versus loaded skill with matched instructions and blind grading; keep routing selection separate from loaded-output quality. Baseline results may reveal insufficient improvement; preserve failures rather than weaken cases.
- agent-decided — no cross-vendor dispatch is authorized by suggest mode; native independent reviewers remain available. Source publication is authorized, installed-host updates are excluded.

## Alternatives considered
- Ordinary answering only: required baseline, but does not supply the user-selected independent invocation contract.
- Extending recap-state: changes the orientation owner's unconditional pause and conflates advice with reorientation.
- Always one action or always a menu: respectively hides material preferences or shifts ranking back to the user.
- Community per-turn predictive UI: adds host, latency and call costs outside this outcome; prediction of likely prompts is a different objective.
- A separate automatic dispatcher: unnecessary to permit contextual skill selection and would introduce unrequested runtime machinery.

## Current state evidence
- Forward: greenfield skill; `loom-workflow/skills/using-loom-workflow/SKILL.md` Request table currently routes orientation but has no next-action advice owner.
- Reverse: `loom-workflow/README.md` Skills table is the public discovery surface; adjacent recap-state has its own README triplet.
- Error: `docs/loom/research/2026-11-14-whats-next-skill-discovery.md` Finding 2 records wrong-premise and goal-displacement observations, not a reproduced current-version defect.
- Data: `loom-workflow/tests/recap-state/behavior_cases.json` demonstrates visible-message fixtures; private retained histories are not runtime inputs.
- Boundary: `loom-workflow/skills/recap-state/SKILL.md` owns orientation; `loom-code/skills/capture-intent` is not assumed to exist; available lifecycle stations retain action authority.

## UI flows
N/A — this change adds an agent instruction contract, not a CLI, screen or external API; natural advice, missing context, evidence failure and completed-goal responses are covered by REQ-1–REQ-4 rather than a new interface.
