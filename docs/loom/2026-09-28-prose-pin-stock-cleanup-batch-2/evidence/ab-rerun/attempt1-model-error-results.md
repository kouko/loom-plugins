# A/B results — loom-visualization description on Loom station reporting prompts

Protocol: [protocol.md](protocol.md). Runs per prompt per variant: 2 (18 sessions per variant, 36 total).

B (current SKILL.md description): `Show comparisons, flows, decisions, states or reasoning chains as tables, ASCII or Mermaid in coding chat, including when a Loom station reports to the user (intent restatement, choices, acceptance test results); not Obsidian notes.`

| variant | prompt | run | invoked | table | diagram | error |
|---|---|---|---|---|---|---|
| A | a1-csv-export | 1 | no | no | no | yes |
| A | a1-csv-export | 2 | no | no | no | yes |
| A | a2-login-lockout | 1 | no | no | no | yes |
| A | a2-login-lockout | 2 | no | no | no | yes |
| A | a3-image-upload | 1 | no | no | no | yes |
| A | a3-image-upload | 2 | no | no | no | yes |
| A | b1-sqlite-postgres | 1 | no | no | no | yes |
| A | b1-sqlite-postgres | 2 | no | no | no | yes |
| A | b2-auth-provider | 1 | no | no | no | yes |
| A | b2-auth-provider | 2 | no | no | no | yes |
| A | b3-monorepo-split | 1 | no | no | no | yes |
| A | b3-monorepo-split | 2 | no | no | no | yes |
| A | c1-csv-export | 1 | no | no | no | yes |
| A | c1-csv-export | 2 | no | no | no | yes |
| A | c2-login-lockout | 1 | no | no | no | yes |
| A | c2-login-lockout | 2 | no | no | no | yes |
| A | c3-image-upload | 1 | no | no | no | yes |
| A | c3-image-upload | 2 | no | no | no | yes |
| B | a1-csv-export | 1 | no | no | no | yes |
| B | a1-csv-export | 2 | no | no | no | yes |
| B | a2-login-lockout | 1 | no | no | no | yes |
| B | a2-login-lockout | 2 | no | no | no | yes |
| B | a3-image-upload | 1 | no | no | no | yes |
| B | a3-image-upload | 2 | no | no | no | yes |
| B | b1-sqlite-postgres | 1 | no | no | no | yes |
| B | b1-sqlite-postgres | 2 | no | no | no | yes |
| B | b2-auth-provider | 1 | no | no | no | yes |
| B | b2-auth-provider | 2 | no | no | no | yes |
| B | b3-monorepo-split | 1 | no | no | no | yes |
| B | b3-monorepo-split | 2 | no | no | no | yes |
| B | c1-csv-export | 1 | no | no | no | yes |
| B | c1-csv-export | 2 | no | no | no | yes |
| B | c2-login-lockout | 1 | no | no | no | yes |
| B | c2-login-lockout | 2 | no | no | no | yes |
| B | c3-image-upload | 1 | no | no | no | yes |
| B | c3-image-upload | 2 | no | no | no | yes |

## Totals

| variant | invoked | table | diagram | error |
|---|---|---|---|---|
| A | 0/18 | 0/18 | 0/18 | 18 |
| B | 0/18 | 0/18 | 0/18 | 18 |

## Decision

**INCOMPLETE** — rule: SHIP B only if no session errored and B's invocation count (0) is strictly greater than A's (0). B is already the shipped text, so this is a re-measurement: SHIP means the current description still out-invokes A; HOLD or INCOMPLETE is a finding for review, not a revert.

## Dropped streams (> 2 MB)

- none
