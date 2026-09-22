---
originator: kouko
kind: engineering
needs-design: no — SKILL.md and station prose are skill/gate artifacts, not interface surfaces under the manifest globs
status: confirmed 2026-09-19
publication: automatic — authorized 2026-09-19 by kouko
---

## Problem
When a change reaches a station that needs something an earlier station was
supposed to produce, and that thing is absent, the flow stops making progress
and nobody says so. Ship refuses because the attestation is absent. Closing
Review refuses because the evidence it would attest to is absent. Build
reports nothing left to do because every planned task is already committed.
The agent cycles between the three stations. The user watches the same station
names scroll past for tens of minutes, asks what is happening, and has to
break out by hand and drive each missing step individually. On 2026-09-19 this
cost roughly thirty minutes and a manual rescue before PR #31 could be
published.

## Proposed outcome
A run that finds something missing goes back to the station that produces it,
produces it, and carries on to the end by itself. It stops in exactly two
situations: the missing thing needs a decision the user has not yet given, or
the attempt to produce it failed. In both it says what is missing and what it
tried. It never cycles between stations in silence.

## Acceptance
1. Starting from a change whose planned tasks are all committed but whose
   adversarial probes, blind-run report or attestation are absent, a run
   produces the missing items and a valid attestation without the user
   intervening.
2. The station sequence of that run is recorded, and no station appears in it
   more than twice.
3. For a missing item that some station is declared to produce, the run goes
   to that station and produces it there, choosing the station from the
   declared station-to-artifact mapping rather than from a list written into
   the recovery rule itself.
4. When producing the missing item needs a decision the user has not yet
   given, the run stops and asks. When the user has already given that
   decision, including a general "you decide", the run proceeds and records
   the choice as user-decided.
5. When the attempt to produce a missing item fails, the run stops and reports
   which item is missing, what was attempted, and where it failed. It does not
   attempt the same item a second time and does not hand on to another
   station.

## Constraints
- Preserve every existing quality gate and mechanical check. Recovery adds a
  path; it never skips a gate.
- Leave the expert-mode skip confirmation exactly as it is. Reducing that
  friction is a separate change.
- No new external dependencies.

## Out of scope
- Changing the order of the Loom stations.
- Changing the rule logic in `loom_checker.py`.
- Changing how a user-requested skip is confirmed. See intent
  2026-09-19-expert-mode-skip-friction.

## Later changes
- PR #43 made two lines historical. The Problem's "Ship refuses because the attestation is absent": Ship now publishes an unattested change with the verification status disclosed. The Constraint "Leave the expert-mode skip confirmation exactly as it is": plain-words skips now exist beside the typed route. Ship's current behaviour is in `loom-code/skills/ship/SKILL.md` §3.
- No Acceptance line was replaced: the absence-recovery rules still hold in `loom-code/skills/build/SKILL.md` §3 and `loom-code/skills/closing-review/SKILL.md`.
- Decision recorded in #43's PR body Decisions table and intent 2026-09-22-publication-floor-moves-to-github.

## Open questions
- none
