# A/B results — loom-visualization description on Loom station reporting prompts

Protocol: [protocol.md](protocol.md). Runs per prompt per variant: 2 (18 sessions per variant, 36 total).

B (current SKILL.md description): `Show comparisons, flows, decisions, states or reasoning chains as tables, ASCII or Mermaid in coding chat, including when a Loom station reports to the user (intent restatement, choices, acceptance test results); not Obsidian notes.`

| variant | prompt | run | invoked | table | diagram | error |
|---|---|---|---|---|---|---|
| A | a1-csv-export | 1 | no | yes | no | no |
| A | a1-csv-export | 2 | no | yes | no | no |
| A | a2-login-lockout | 1 | no | yes | no | no |
| A | a2-login-lockout | 2 | no | yes | no | no |
| A | a3-image-upload | 1 | no | yes | no | no |
| A | a3-image-upload | 2 | no | yes | no | no |
| A | b1-sqlite-postgres | 1 | no | yes | no | no |
| A | b1-sqlite-postgres | 2 | no | yes | no | no |
| A | b2-auth-provider | 1 | no | yes | no | no |
| A | b2-auth-provider | 2 | no | yes | no | no |
| A | b3-monorepo-split | 1 | yes | yes | no | no |
| A | b3-monorepo-split | 2 | no | yes | no | no |
| A | c1-csv-export | 1 | no | yes | no | no |
| A | c1-csv-export | 2 | no | yes | no | no |
| A | c2-login-lockout | 1 | no | yes | no | no |
| A | c2-login-lockout | 2 | no | yes | no | no |
| A | c3-image-upload | 1 | no | yes | no | no |
| A | c3-image-upload | 2 | no | yes | no | no |
| B | a1-csv-export | 1 | no | yes | no | no |
| B | a1-csv-export | 2 | yes | yes | no | no |
| B | a2-login-lockout | 1 | yes | yes | no | no |
| B | a2-login-lockout | 2 | no | yes | no | no |
| B | a3-image-upload | 1 | no | yes | no | no |
| B | a3-image-upload | 2 | no | yes | no | no |
| B | b1-sqlite-postgres | 1 | no | yes | no | no |
| B | b1-sqlite-postgres | 2 | yes | yes | no | no |
| B | b2-auth-provider | 1 | yes | yes | no | no |
| B | b2-auth-provider | 2 | no | yes | no | no |
| B | b3-monorepo-split | 1 | yes | yes | no | no |
| B | b3-monorepo-split | 2 | yes | yes | no | no |
| B | c1-csv-export | 1 | no | yes | no | no |
| B | c1-csv-export | 2 | no | yes | no | no |
| B | c2-login-lockout | 1 | yes | yes | no | no |
| B | c2-login-lockout | 2 | yes | yes | no | no |
| B | c3-image-upload | 1 | yes | yes | no | no |
| B | c3-image-upload | 2 | no | yes | no | no |

## Totals

| variant | invoked | table | diagram | error |
|---|---|---|---|---|
| A | 1/18 | 18/18 | 0/18 | 0 |
| B | 9/18 | 18/18 | 0/18 | 0 |

## Decision

**SHIP** — rule: SHIP B only if no session errored and B's invocation count (9) is strictly greater than A's (1). B is already the shipped text, so this is a re-measurement: SHIP means the current description still out-invokes A; HOLD or INCOMPLETE is a finding for review, not a revert.

## Dropped streams (> 2 MB)

- none
