# Loom flow recovery loop — spec
intent: 2026-09-19-loom-flow-recovery-loop@e4a57bc8
pre-build-review: not-required — prose-only change to station instructions; no security, privacy, irreversible-data, public-contract or cross-system-architecture surface, and each requirement maps one-to-one onto an unambiguous Acceptance line

## Requirements
REQ-1 — A run carries on when something an earlier station owed is absent
  WHEN a run finds the adversarial programs, the blind-run report or the
  attestation absent while every planned task is already committed, the
  station instructions shall direct it to produce the missing item and
  continue to a valid attestation without asking the user. Carried detail —
  the user's words for the wanted default are 「整個 loom 邏輯要能夠自動走到
  底」: carrying on is the default and stopping is the exception.
  → Acceptance #1

REQ-2 — A recovery run enters no station more than twice
  WHEN a recovery happens, the run shall record the sequence of stations it
  entered, and no station shall appear in that sequence more than twice.
  → Acceptance #2

REQ-3 — The producing station is read from the declared mapping
  WHEN the run must decide which station produces a missing item, it shall
  read `stations[].produces` and `actions[].owner` in
  `loom-code/contract/manifest.yaml`, and the recovery instructions shall
  carry no second copy of that mapping. Carried details — 「如果缺了哪個東西
  就直接回去補 這樣邏輯更簡單」 sets the general rule in place of a
  verification-evidence special case, and 「回去補做之前跳過的步驟」 means the
  trigger is not limited to what the current station itself omitted.
  → Acceptance #3

REQ-4 — An unanswered user decision stops the run; an answered one does not
  WHEN producing a missing item requires a decision point the user has not
  answered for this change, the run shall stop and ask. WHEN the user has
  already answered it, including a general delegation such as "you decide",
  the run shall proceed and record the choice as user-decided. Carried
  detail — 「只要使用者說跳過或直接做哪件事 loom 機制就應該配合直接依照使用
  者的意願執行」; this requirement covers only whether the run asks again, and
  does not change how a skip is confirmed.
  → Acceptance #4

REQ-5 — A failed recovery stops and says what happened
  WHEN an attempt to produce a missing item fails, the run shall stop and
  report which item is missing, what it attempted and where it failed, and
  shall neither retry that item nor hand on to another station. Carried
  detail — the user's instruction for this case was 「停下來告訴我」.
  → Acceptance #5

## Design decision
- The recovery rule reads the producing station from `manifest.yaml` rather
  than listing artifacts and stations in its own prose. A second copy of that
  mapping drifts silently when a station or an artifact changes, and the
  evidence sweep confirmed `manifest.yaml` is currently the only copy.
  agent-decided.
- Two declarations are used, not one: `stations[].produces` covers intent,
  spec, plan, diff and attestation; `actions[].owner` covers the adversarial
  programs (build), the blind run (closing-review) and the package tests
  (closing-review). Neither the adversarial programs nor the blind-run report
  appears under `stations[].produces`, so `stations:` alone would not resolve
  the very items that were missing on 2026-09-19. agent-decided.
- The change adds "the item is absent" as an antecedent to the return edges
  that already exist, instead of introducing a new recovery mechanism. Every
  current return edge is conditioned on a failing check, a fix, or a
  `sync-trunk` result; none is conditioned on absence. agent-decided.
- Reducing the friction of confirming a user-requested skip is excluded and
  carried by intent 2026-09-19-expert-mode-skip-friction. The safety question
  it raises — what proves a human rather than the agent or a document asked —
  is unanswered, and leaving it here would block this change. user-decided:
  the user chose to do this change first and that one after.
- `artifacts.blind-run-report.charter.signoff: ship` is not in conflict with
  `actions.blind-run.owner: closing-review`. `signoff` names who closes the
  item out with the user at decision point ③; `owner` names who produces it.
  The recovery lookup uses `owner`, never `signoff`. agent-decided.

## Alternatives considered
- Special-case the three verification items in the recovery prose. Rejected:
  it leaves every other missing artifact with no route, and it is the second
  copy of the mapping that REQ-3 exists to prevent.
- Add a checker rule that detects the missing item mechanically. Rejected:
  the intent puts `loom_checker.py` rule logic out of scope, and the cycle was
  caused by prose that gives the agent no route, not by a check that failed to
  fire.
- Let the run retry a failed recovery until it succeeds. Rejected: the user
  asked for a stop, and unbounded retry reproduces the original complaint that
  the run burns time without saying anything.

## Current state evidence
- Forward: `loom-code/skills/build/SKILL.md:54-76` — the end-of-Build sequence
  is entered from the phrase "After all tasks land", a point in a forward
  pass, not a condition re-evaluated on re-entry.
- Reverse: `loom-code/skills/closing-review/SKILL.md:42`, `:46`, `:55`, `:262`
  — four return-to-Build edges already exist and already name the target
  section; each is conditioned on a failing check, a fix, or a `sync-trunk`
  result.
- Error: `loom-code/skills/ship/SKILL.md:128-132` — the attestation-missing
  remedy already names closing-review as route one; ship's prose was correct
  and is not changed by this work.
- Data: `loom-code/contract/manifest.yaml:12-19` (`stations[].produces`) and
  its `actions:` list (`adversarial` owner build, `blind-run` and
  `package-tests` owner closing-review) are the only declaration of which
  station produces what; a repo-wide sweep found no second copy.
- Boundary: `loom-code/skills/build/SKILL.md:91-100` — every existing re-run
  path requires a fix or a widening as its antecedent, and
  `build/SKILL.md` contains no clause for entry with no tasks left, which is
  the exact 2026-09-19 state.

## UI flows
N/A — the change alters station instructions read by agents. It touches no
command, screen, or file artifact a user or external system reads.
