# Outside review steps end cleanly and report the right reason
originator: kouko
kind: engineering
needs-design: no — repairs how the external-review script stops outside CLIs and words its failure reasons, and raises its review time-limit default within the existing range; its arguments, output shape, and user-facing surfaces stay the same
status: confirmed 2026-10-18
publication: automatic — authorized 2026-10-18 by kouko

## Problem

PR #92 made Codex model discovery stop cleanly when Codex never answers, but every other outside step loom runs — Antigravity's model listing, the pre-review probe, and the review itself for Codex, Claude Code and Antigravity — still uses the older call. If the outside CLI leaves a child process holding its output open, that older call can hang after its time limit instead of ending, so the closing review stalls with no result. Separately, when Codex exits before answering the model-list request, loom reports "response missing", which hides that Codex itself failed. No hang has been observed yet; the exposure was shown by an adversarial probe during PR #92.

## Proposed outcome

Every outside step loom runs ends within its time limit and leaves no process behind, and a Codex that fails before answering is reported as a failure. Because the time limit will now actually hold, the review step's default limit rises from 10 to 30 minutes (the existing upper bound), so a long but working review is not cut off. The two code notes reviewers left on PR #92 are folded in: the Codex model-list launcher becomes an explicit replaceable parameter instead of being chosen by comparing the runner to `subprocess.run`, and the fallback path uses `CODEX_DISCOVERY_TIMEOUT` instead of a literal 15.

## Acceptance

1. When an outside CLI used for Antigravity model listing, the probe, or the review is still running at its time limit while a child process holds its output open, the step ends shortly after the limit, reports a timeout, and leaves no process running.
2. A review run with no explicit time limit is allowed 30 minutes before it is reported as timed out.
3. When Codex exits before answering the model-list request, the reported reason says Codex failed and carries its exit status, instead of "response missing".
4. Model listing, probe and review for Codex, Claude Code and Antigravity behave as before when the CLI answers normally, and the complete package suite passes.

## Constraints

- Consent checks, the explicit model and effort rules, and what is sent to each vendor stay unchanged.
- Every other time limit keeps its current value, and the allowed range for the review limit stays at most 30 minutes.

## Out of scope

- Choosing or changing any default model.
- Retrying a step after a timeout or failure.
- Showing whether a running review is still making progress (to be discussed separately afterwards).

## Open questions
- none
