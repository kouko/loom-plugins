# An outside review shows that it is still running — spec
intent: 2026-10-19-external-review-progress-lines@a9361215
pre-build-review: not-required — diagnostic stderr lines from an existing runner; no security, data, public-contract or cross-system change, and every line is removable

## Requirements
REQ-1 — periodic progress line
  WHEN an outside probe or review step has run for 60 seconds and every 60 seconds after, the runner shall write one plain line to its error stream naming the step, the elapsed time and the time since the CLI last produced output; the 60-second interval is the user's agreed revision of "每 30 秒左右印一行進度：已跑幾分鐘、距離上次輸出多久" → Acceptance #1
REQ-2 — closing line with longest silence
  WHEN a probe or review step ends by exit or by timeout, the runner shall write one plain line naming the step, how it ended, its total time and the longest silence observed ("記下『最長安靜了多久』") → Acceptance #2
REQ-3 — relay while waiting
  WHEN a station runs an outside review, the external-review skill shall tell the agent to keep the runner's error stream visible while it runs and relay its progress lines to the user → Acceptance #3
REQ-4 — nothing else changes
  WHEN progress reporting is active, the runner's JSON result, statuses, timeouts and discovery steps shall be unchanged, and the complete package suite shall pass → Acceptance #4

## Design decision
- agent-decided: progress lines go to the runner's stderr; stdout stays the single JSON result the stations parse.
- agent-decided: fixed 60 s interval, append-only plain lines, no ANSI or line rewriting (Terraform/Travis precedent; Bazel dropped back-off for non-TTY output).
- agent-decided: "last output" means the last complete line the CLI wrote on stdout or stderr; partial lines are not counted.
- agent-decided: only probe and review steps report; model discovery stays silent because it is bounded to 15 s.
- agent-decided: lines carry only step name, outcome and durations — never packet or CLI text (intent Constraint).

## Alternatives considered
- Print every 30 s — rejected by the user's revision: doubles relayed lines for no added decision value.
- Suppress the line while the CLI is producing output — rejected: Claude and Antigravity print only at exit, so it changes nothing for them and hides progress for Codex.
- Back-off intervals — rejected: Bazel removed them for non-TTY output.
- Put longest silence in the JSON result — rejected: changes the result shape the stations parse; the closing line is enough to collect data.

## Current state evidence
- Forward: `loom-code/scripts/external_review.py` `execute` loops over ("probe", "review") and calls `_run` → `_launch`.
- Reverse: `loom-code/skills/external-review/SKILL.md` "## Execute" consumes only the one JSON result on stdout.
- Error: `_launch` raises `subprocess.TimeoutExpired` after `proc.wait(timeout)`; `execute` maps it to `execution-timeout`.
- Data: `_launch` reader threads already append each stdout/stderr line as it arrives.
- Boundary: `_launch` with `until_response_id` serves Codex app-server discovery and must stay silent.

## UI flows
- review step running for 2m10s, CLI last wrote 40 s ago → `external-review: review still running · 2m00s elapsed · last output 40s ago` (one line per minute)
- review step ends → `external-review: review exited 0 after 2m35s · longest silence 1m12s`
- review step hits the cap → `external-review: review timed out after 30m00s · longest silence 30m00s`
