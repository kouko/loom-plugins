# Fold workaround lessons into loom
originator: kouko
kind: engineering
needs-design: no — skill and agent guidance text, checker internals and one added hint line in an existing refusal message; no new command, argument, state or output format
evidence: [loom-code/scripts/loom_checker/probes.py, loom-code/scripts/loom_checker/command_handlers/publish.py, loom-code/skills/closing-review/references/adversarial.md, loom-code/agents/implementer.md, loom-design/skills/capture-intent/SKILL.md, AGENTS.md]
status: confirmed 2026-10-03
publication: automatic — authorized 2026-10-03 by kouko

## Problem
While building loom with loom, kouko kept private notes to get past traps that loom itself sets. Anyone installing loom without those notes hits the same traps: closing review refuses an ordinary test command because an option comes before the test file; the adversary guidance says to report an empty attack, which the checker then refuses on a wide change; publishing right after a push is refused with no hint that one retry is enough; adversary findings that only a deliberate bypass could trigger get fixed and widen the change; a removal task keeps tests of the removed behaviour because the guidance only says "never delete a test"; and capture-intent can open a second intent in the middle of an active change. This repository's own version-bump rule also invalidates the review evidence when the bump lands after it, which only a private note explains.

## Proposed outcome
Loom handles or explains each of these traps itself, with the smallest change for each and no new checker rule, so the private notes can be deleted.

## Acceptance
1. Closing review accepts an adversarial program command whose test-runner options come before the test file, and still refuses a command that does not run the declared program.
2. The adversary guidance tells an attack that found nothing on a change that needs an executed program to reuse an existing repository test instead of reporting a bare attempt.
3. When publishing is refused because the pull request does not yet show the pushed commit, the refusal tells the user to retry once right after a push and to stop if it is refused again; publishing still refuses and never retries on its own.
4. The adversary guidance rates a finding that only someone deliberately defeating a rule could trigger as a nit, so it is recorded as a known limitation rather than fixed, while findings that can happen without such intent keep their severity.
5. The implementer guidance says that removing a behaviour removes the tests that only check it, and that this is not deleting a test to reach green.
6. This repository's contributor guide says to bump versions in the last fix round before the review evidence is generated.
7. capture-intent's description no longer claims a request made inside an active change.
8. The existing package test suite passes, and each plugin whose files change carries a new version consistent across manifests, CHANGELOGs and READMEs.

## Constraints
- No new checker rule and no automatic retry in publishing (user-decided 2026-10-03).
- Build's rule that every fatal or important adversary finding is fixed stays unchanged.
- The stations' flow and the three decision points stay as they are.

## Out of scope
- Deleting kouko's private notes themselves; they are removed outside the repository after the merge.
- The private notes not listed in the Problem.
- Control characters in the repository defaults file breaking the session-start text (deferred until someone reports it, user-decided 2026-10-03).

## Open questions
- none
