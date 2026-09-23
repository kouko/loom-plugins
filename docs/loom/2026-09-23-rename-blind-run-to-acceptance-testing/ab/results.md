# A/B results — renamed loom-visualization description on Loom station reporting prompts

Protocol: [protocol.md](protocol.md). Runs per prompt per variant: 2 (18 sessions per variant, 36 total).

| variant | prompt | run | loaded | invoked | table | diagram | error |
|---|---|---|---|---|---|---|---|
| A | a1-csv-export | 1 | yes | yes | yes | no | no |
| A | a1-csv-export | 2 | yes | yes | yes | no | no |
| A | a2-login-lockout | 1 | yes | yes | yes | no | no |
| A | a2-login-lockout | 2 | yes | yes | yes | no | no |
| A | a3-image-upload | 1 | yes | yes | yes | no | no |
| A | a3-image-upload | 2 | yes | yes | yes | no | no |
| A | b1-sqlite-postgres | 1 | yes | yes | yes | no | no |
| A | b1-sqlite-postgres | 2 | yes | yes | yes | no | no |
| A | b2-auth-provider | 1 | yes | yes | yes | no | no |
| A | b2-auth-provider | 2 | yes | yes | yes | no | no |
| A | b3-monorepo-split | 1 | yes | yes | yes | no | no |
| A | b3-monorepo-split | 2 | yes | yes | yes | no | no |
| A | c1-csv-export | 1 | yes | yes | yes | no | no |
| A | c1-csv-export | 2 | yes | yes | yes | no | no |
| A | c2-login-lockout | 1 | yes | yes | yes | no | no |
| A | c2-login-lockout | 2 | yes | yes | yes | no | no |
| A | c3-image-upload | 1 | yes | yes | yes | no | no |
| A | c3-image-upload | 2 | yes | yes | yes | no | no |
| B | a1-csv-export | 1 | yes | yes | yes | no | no |
| B | a1-csv-export | 2 | yes | yes | yes | no | no |
| B | a2-login-lockout | 1 | yes | yes | yes | no | no |
| B | a2-login-lockout | 2 | yes | yes | yes | no | no |
| B | a3-image-upload | 1 | yes | yes | yes | no | no |
| B | a3-image-upload | 2 | yes | yes | yes | no | no |
| B | b1-sqlite-postgres | 1 | yes | yes | yes | no | no |
| B | b1-sqlite-postgres | 2 | yes | yes | yes | no | no |
| B | b2-auth-provider | 1 | yes | yes | yes | no | no |
| B | b2-auth-provider | 2 | yes | yes | no | no | no |
| B | b3-monorepo-split | 1 | yes | yes | yes | no | no |
| B | b3-monorepo-split | 2 | yes | yes | yes | no | no |
| B | c1-csv-export | 1 | yes | yes | yes | no | no |
| B | c1-csv-export | 2 | yes | yes | yes | no | no |
| B | c2-login-lockout | 1 | yes | yes | yes | no | no |
| B | c2-login-lockout | 2 | yes | yes | yes | no | no |
| B | c3-image-upload | 1 | yes | yes | yes | no | no |
| B | c3-image-upload | 2 | yes | yes | yes | no | no |

## Totals (valid runs only; invalid = the skill did not load)

| variant | valid | invoked | rate | invalid | errored |
|---|---|---|---|---|---|
| A | 18 | 18 | 100% | 0 | 0 |
| B | 18 | 18 | 100% | 0 | 0 |

By prompt group (a = intent restatement, b = one-way-door choices, c = result report):

| variant | group | valid | invoked | rate |
|---|---|---|---|---|
| A | a | 6 | 6 | 100% |
| A | b | 6 | 6 | 100% |
| A | c | 6 | 6 | 100% |
| B | a | 6 | 6 | 100% |
| B | b | 6 | 6 | 100% |
| B | c | 6 | 6 | 100% |

## Decision

**KEEP B** — rule: KEEP B only if no session errored, both variants have a valid run, and B's trigger rate over valid runs (18/18) is at least A's (18/18); otherwise STOP.

B rendered description SHA-256: `b901f3528a8b1adbaaa412c1eb75034c973a0dac9e88def516f9ea147650c556`

## Dropped streams (> 2 MB)

- none

## Deviations and limits

- Full design ran: 2 runs per prompt per variant, 36 sessions, no reduction;
  no session errored and none was invalid, so nothing was re-run or excluded.
- A / a1-csv-export / run 1 was first run as a smoke check with the protocol's
  exact argv; the runner kept it as that session.
- Every session was checked for the loaded skill from its `system`/`init`
  event (`loom-workflow:loom-visualization` offered by `loom-workflow@inline`);
  all 36 passed.
- Both variants hit the ceiling (18/18). The comparison shows the rename lost
  nothing measurable on these prompts; it cannot show a difference smaller
  than one session in 18, and it does not re-establish the original's A/B
  gap, which was against the older description without the station clause.
- The (c) prompts still say 盲跑 (the original prompt text, kept identical so
  the prompt set is the same); the renamed phrase in B is not echoed by them.
- 36 sessions, 5.39 USD total (`total_cost_usd` summed over result events),
  about 2.3 M tokens (mostly cache reads), 688 s of summed session time,
  about 3.5 minutes wall clock at 4 workers.
- The prompts simulate station reporting moments from a situation
  description; no station skill ran, and live station sessions may behave
  differently.
