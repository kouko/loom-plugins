# An outside review shows that it is still running
originator: kouko
kind: engineering
needs-design: no — adds diagnostic progress lines to the existing outside-review runner's error stream; the JSON result the stations parse keeps its shape, and no user-typed surface changes
status: confirmed 2026-10-20
publication: automatic — authorized 2026-10-20 by kouko

## Problem
An outside review (Codex, Claude Code or Antigravity run as a second reviewer) can legitimately take 10 to 30 minutes. While it runs, the runner shows nothing until the CLI exits, so the maintainer cannot tell whether the review is working, silent, or stuck, and only learns at the 30-minute cap. Nobody has measured how long a normal review stays silent, so any future "no output for N minutes means stuck" rule would have to guess its threshold.

## Proposed outcome
While an outside review's preflight or review step runs, the maintainer periodically sees that it is still running, how long it has run, and how long since the CLI last produced output; when the step ends, the longest silence it showed is reported, so real silence data accumulates from ordinary reviews.

## Acceptance
1. While an outside review step runs longer than a minute, a progress line appears about once a minute stating the step, the elapsed time, and the time since the CLI last produced output.
2. When a step ends — completed, failed or timed out — one closing line reports its total time and the longest silence observed.
3. While the station waits for an outside review, the agent relays the progress lines to the maintainer instead of waiting silently.
4. The review result, its pass/fail status, the timeout behaviour and every existing outcome are unchanged, and the complete package suite passes.

## Constraints
- No step is ended early because of silence; only the existing time limits end a step.
- Progress lines never carry the review packet or the CLI's output text.

## Out of scope
- Killing a review after a period of no output (revisit once real silence data exists).
- Switching any CLI to a streaming event output format.
- The separate Claude reviewer retry runner.

## Open questions
- none
