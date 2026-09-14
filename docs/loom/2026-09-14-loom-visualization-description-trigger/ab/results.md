# A/B results — loom-visualization description on Loom station reporting prompts

Protocol: [protocol.md](protocol.md). Runs per prompt per variant: 2 (18 sessions per variant, 36 total).

| variant | prompt | run | invoked | table | diagram | error |
|---|---|---|---|---|---|---|
| A | a1-csv-export | 1 | yes | yes | no | no |
| A | a1-csv-export | 2 | yes | yes | no | no |
| A | a2-login-lockout | 1 | yes | yes | no | no |
| A | a2-login-lockout | 2 | yes | yes | no | no |
| A | a3-image-upload | 1 | yes | yes | no | no |
| A | a3-image-upload | 2 | yes | yes | no | no |
| A | b1-sqlite-postgres | 1 | yes | yes | no | no |
| A | b1-sqlite-postgres | 2 | yes | yes | no | no |
| A | b2-auth-provider | 1 | yes | yes | no | no |
| A | b2-auth-provider | 2 | yes | yes | no | no |
| A | b3-monorepo-split | 1 | yes | yes | no | no |
| A | b3-monorepo-split | 2 | yes | no | yes | no |
| A | c1-csv-export | 1 | no | yes | no | no |
| A | c1-csv-export | 2 | no | yes | no | no |
| A | c2-login-lockout | 1 | no | yes | no | no |
| A | c2-login-lockout | 2 | no | yes | no | no |
| A | c3-image-upload | 1 | no | yes | no | no |
| A | c3-image-upload | 2 | no | yes | no | no |
| B | a1-csv-export | 1 | yes | no | yes | no |
| B | a1-csv-export | 2 | yes | yes | no | no |
| B | a2-login-lockout | 1 | yes | no | yes | no |
| B | a2-login-lockout | 2 | yes | no | yes | no |
| B | a3-image-upload | 1 | yes | no | yes | no |
| B | a3-image-upload | 2 | yes | no | yes | no |
| B | b1-sqlite-postgres | 1 | yes | no | yes | no |
| B | b1-sqlite-postgres | 2 | yes | no | yes | no |
| B | b2-auth-provider | 1 | yes | no | yes | no |
| B | b2-auth-provider | 2 | yes | yes | no | no |
| B | b3-monorepo-split | 1 | yes | yes | no | no |
| B | b3-monorepo-split | 2 | yes | no | yes | no |
| B | c1-csv-export | 1 | yes | yes | no | no |
| B | c1-csv-export | 2 | yes | no | yes | no |
| B | c2-login-lockout | 1 | yes | yes | no | no |
| B | c2-login-lockout | 2 | yes | yes | no | no |
| B | c3-image-upload | 1 | yes | yes | no | no |
| B | c3-image-upload | 2 | yes | yes | no | no |

## Totals

| variant | invoked | table | diagram | error |
|---|---|---|---|---|
| A | 12/18 | 17/18 | 1/18 | 0 |
| B | 18/18 | 8/18 | 10/18 | 0 |

## Decision

**SHIP** — rule: SHIP B only if B's invocation count (18) is strictly greater than A's (12).

B rendered description SHA-256: `e98a3ed165415900bf405fe07209dde634cd465ff035fbea4ac2c73f57f6fd45`

## Dropped streams (> 2 MB)

- none

## Deviations from the protocol

- Full design ran: 2 runs per prompt per variant, 36 sessions, no reduction.
- A / a1-csv-export / run 1 was first run as a smoke check with the protocol's
  exact argv; the runner kept it as that session rather than re-running it.
- Sessions ran in two sittings. The first sitting hit the account session
  limit; B / c3-image-upload / run 1 returned `is_error: true`,
  `api_error_status: 429` without answering. That attempt was not a measured
  session: the parser was changed to treat an error result as incomplete and
  the session was re-run after the limit reset (its stream was overwritten).
  No other stream carried an error result.
- Runner fixes during the run, none affecting what a session saw: the copy
  check ignores `__pycache__/` and `*.pyc` (hooks write bytecode into a copy
  once a session runs), and `run --limit N` chunks sessions under a tool timeout.
- `test_run_ab.py` was added beside the runner for its pure parts.
