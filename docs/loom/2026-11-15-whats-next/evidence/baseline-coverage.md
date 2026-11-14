# Ordinary baseline coverage

Fixtures were frozen before the eight native, fresh-context ordinary-answer
runs and before a candidate skill existed. Each case ran once, without tools,
file access, external services, edits or scoring criteria. The exact observed
answer text is retained in `ordinary-baseline.json`; no quality grades or retries
were introduced. Timing and token usage were unavailable and remain null.

Frozen SHA-256:
- `behavior_cases.json`: `4099a3674f46266836d8ae990b0ed8fc3e4960b1dadc028a89614f18359e7408`
- `trigger_queries.json`: `74b45b38e177e028ec2d441fe938668a20d5bc4ab63c8731600f83d494dfe03c`

Independent structural readback, reviewer `/root`, 2026-11-15: PASS.
The reviewer read all three complete JSON payloads and checked eight unique
B1–B8 outputs against the frozen visible state, permissions and prompt; twenty
queries with ten positive and ten negative labels across English, Traditional
Chinese and Japanese; blocker/viable-plan and existing/new-authority pairs;
criteria withheld from execution agents; candidate absence; and explicit
limitations and null measurements. This is completion and coverage verification,
not output-quality grading or independent acceptance testing.

JSON syntax checks passed for all three JSON files. This pilot does not establish
incremental benefit, statistical reliability, native-host skill selection or
installed-host effectiveness. Description-selection queries remain unexecuted.
