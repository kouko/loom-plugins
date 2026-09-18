# Blocked publication names the legal routes — spec

intent: 2026-09-18-blocked-publish-names-the-legal-routes@3bdaa258
pre-build-review: not-required — nothing in the gate is loosened, no data is touched and no public contract changes shape; the whole change is one refusal string plus the tests that lock it, and the three existing adversarial assertions stay green untouched

This spec exists under a `needs-design: no` intent because intake carried three
details the user stated about how the refusal must behave, and the repository's
two-document convention gives them no other home. It adds no requirement the
intent's Acceptance lines do not already carry.

## Requirements

REQ-1 — The refusal names both legal routes
  WHEN the publication gate refuses because the branch carries no attestation,
  the refusal shall name running the closing review and proposing a step
  selection the user confirms by typing → Acceptance #1

REQ-2 — The merge refusal carries the same information
  WHEN the merge command refuses for the same missing attestation, its output
  shall carry the same two routes → Acceptance #2

REQ-3 — The station prose forbids handing the command over
  WHEN an agent reads the ship station's prose, it shall find a rule stating
  that a blocked publication command is never handed to the user to run
  → Acceptance #3

REQ-4 — A confirmed skip publishes end to end
  WHEN the user has typed a skip confirmation, the closing review shall emit an
  attestation recording the skipped steps, and the publication command shall
  push and open a Ready pull request whose body carries the skip disclosure
  → Acceptance #4

REQ-5 — This change publishes and merges without user-typed git commands
  WHEN this change itself is published and merged, every git and gh action
  shall be executed by the agent → Acceptance #5

REQ-6 — No rule is loosened
  WHEN a branch carries neither an attestation nor a confirmed skip, the gate
  shall still refuse, and every existing refusal assertion shall still hold
  → Acceptance #6

REQ-7 — The blind run attributes each action
  WHEN the blind run walks the Acceptance lines, its report shall name the
  executing actor for each git and gh action observed → Acceptance #7

REQ-8 — The suite stays green
  WHEN the package suite runs, every existing test shall pass → Acceptance #8

## Design decision

- Naming the routes rather than downgrading the refusal is the user's choice,
  taken after the adversarial review of the downgrade exposed the four surfaces
  it would sever; the gate keeps every rule it has today. user-decided.
- Extend the existing missing-attestation reason (`command_handlers/push.py:260-264`)
  rather than adding a second emission path. The hook, `publish` (`publish.py:415`)
  and `land` (`land.py:939`) all route that verdict through `_cmd_push`, so one
  string reaches three callers. agent-decided.
- The reason stays a **single line**. `report()` (`helpers.py:40-43`) writes one
  `BLOCK <rule>: <reason>` line per failure, and
  `test_adversarial_push_reason.py:113-116` asserts every stderr line on a
  hostile unattested push begins with `BLOCK `. A wrapped reason would emit
  continuation lines without that prefix. agent-decided.
- `report()` itself is not touched: it is shared by every command handler, and
  the intent forbids changing its semantics. agent-decided.
- The two test constants asserting the current reason
  (`test_loom_publish.py:1210`, and the equivalent in
  `test_adversarial_push_reason.py:147-155`) are updated to the new text. They
  keep asserting a refusal; neither assertion is removed or weakened.
  agent-decided.
- The ship station's rule (REQ-3) is advisory prose, not a gate, and is not the
  primary carrier. `PRINCIPLES.md:18` forbids prose-only gates, and the observed
  failures happened mid-build where that file is not loaded. The refusal string
  is the carrier guaranteed to be read at the moment of failure; the prose only
  covers an agent that declines before attempting. agent-decided, from the
  complexity gate.
- `land` refuses earlier than the shared check when no attestation exists
  (`land.py:920-924` derives the change id and acceptor set from the
  attestation path). REQ-2 is therefore satisfied by the earlier refusal
  carrying the routes too, not by reaching `_cmd_push`. agent-decided.

## Alternatives considered

- Downgrade the refusal to a warning — rejected by adversarial spec review: the
  attestation is also the change-id source, the delivery witness, the
  skip-audit key and the disclosure input, so downgrading its verdict severs
  four unrelated surfaces and breaks two ratified non-negotiables. Recorded in
  the intent's Out of scope.
- Put the rule only in the ship station's prose — rejected: prose-only gates are
  forbidden, and the file is not loaded where the failure occurs.
- Give `report()` a severity dimension — rejected: it is shared by every command
  handler and the intent forbids changing its semantics.
- Fix it in the user's own global instructions — rejected: it would hold on one
  machine only, and the intent asks for behaviour the mechanism carries.

## Current state evidence

- Forward: `command_handlers/push.py:260-264` returns the missing-attestation
  refusal through `report()`.
- Reverse: `publish.py:415` and `land.py:939` both call `_cmd_push`;
  `land.py:920-924` refuses earlier when the attestation is absent.
- Error: `helpers.py:40-43` writes exactly one `BLOCK <rule>: <reason>` line per
  failure and returns 1.
- Data: `command_handlers/finalize.py:86-98` drops the reviewer floor to zero for
  a bound skip and records the selection in the attestation it emits.
- Boundary: `test_adversarial_push_reason.py:113-116` asserts every stderr line
  on fourteen hostile unattested pushes begins with `BLOCK `.

## UI flows

| case | what the caller does | what they see |
|---|---|---|
| unattested publication | runs the publication command on a branch with no attestation | the existing refusal, extended on the same line with the two routes and the instruction not to hand the command to the user |
| unattested merge | runs the merge command | the same two routes |
| confirmed skip | the user types the skip confirmation, then the agent runs closing review and publication | an attestation recording the skipped steps, a push, and a Ready pull request whose body discloses the skip |
| no attestation, no confirmation | anything else | refused exactly as today |
