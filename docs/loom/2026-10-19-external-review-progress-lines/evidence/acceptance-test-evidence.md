# An outside review shows that it is still running — acceptance test evidence

Tried on 2026-10-20, in a clean copy of the project at 949aca74 (a fresh
detached `git worktree add` of HEAD), with the branch base f055b428 checked out
the same way beside it for comparison.

## Setup

- The runner is a plain Python script; setup is `python3 loom-code/scripts/external_review.py --help`, which printed its usage in the clean copy.
- No real vendor was called. A fake `claude` executable (Python, no network) was put first on a `PATH` of `<fake-bin>:/usr/bin:/bin` (neither `/usr/bin` nor `/bin` holds a real `claude`), with `env -i` so no other environment leaked in. The probe step answers at once; the review step behaves per `FAKE_MODE`:
  - `quick` — answers at once.
  - `long` — waits 30 s, writes one stderr line, waits 110 s, prints the result, exits 0.
  - `fail` — waits 65 s, writes one stderr line, exits 3.
  - `hang` — never answers (run with `--probe-timeout-seconds 5 --review-timeout-seconds 70`).
  - `probe-hang` — the probe never answers (`--probe-timeout-seconds 5`).
- Every run: `external_review.py --executor claude --model sonnet --effort high --family anthropic --scope <root> --consent-record <consent.json> < packet.txt`, where the packet contains the marker `ACCEPTANCE-PACKET-SECRET` and the fake CLI's own output contains `FAKE-CLI-…` markers.
- The progress interval was **not** shortened: it is the shipped 60 s. Only the review time limit was shortened (70 s instead of 1800 s) for the time-out case, which the command line allows.
- All ten runs (5 scenarios × HEAD and base) ran in parallel; stdout and stderr were captured to separate files.

## 1. While an outside review step runs longer than a minute, a progress line appears about once a minute stating the step, the elapsed time, and the time since the CLI last produced output.
- How I tried it: scenario `long` (review runs 2m20s, CLI's only output at 30 s), plus `fail` and `hang` (no output before the first minute), plus `quick` (under a minute).
- What came back (HEAD stderr, `long`):
  ```
  external-review: probe exited 0 after 0s · longest silence 0s
  external-review: review still running · 1m00s elapsed · last output 29s ago
  external-review: review still running · 2m00s elapsed · last output 1m29s ago
  external-review: review exited 0 after 2m20s · longest silence 1m50s
  ```
  `fail` and `hang` each showed `review still running · 1m00s elapsed · no output yet`. `quick` and `probe-hang` (5 s) showed no progress line — correct, they ended before a minute.
- Evidence: captured stderr above; the runner's own tests `loom-code/tests/test_external_review.py` (129 passed together with the adversarial file, see row 4).

## 2. When a step ends — completed, failed or timed out — one closing line reports its total time and the longest silence observed.
- How I tried it: all five scenarios at HEAD.
- What came back:
  - completed: `review exited 0 after 2m20s · longest silence 1m50s` (silence 30 s → 140 s = 110 s, correct)
  - failed: `review exited 3 after 1m05s · longest silence 1m05s`
  - timed out (review): `review timed out after 1m10s · longest silence 1m10s`
  - timed out (probe): `probe timed out after 5s · longest silence 5s`
  - every completed probe: `probe exited 0 after 0s · longest silence 0s`
  Exactly one closing line per step in every run.
- Evidence: captured stderr of each run.

## 3. While the station waits for an outside review, the agent relays the progress lines to the maintainer instead of waiting silently.
- How I tried it: read the instruction text; checked which stations reach the runner; watched the `long` run's stderr file from outside while the runner was still going.
- What came back:
  - `loom-code/skills/external-review/SKILL.md:139-145` (section "Execute") tells the agent that progress lines arrive about once a minute on the error stream, to keep that stream visible (e.g. run in the background and watch its output), and to relay each line to the user instead of waiting silently.
  - Callers reach the runner only through that skill: `loom-code/skills/closing-review/SKILL.md:182-183` and `loom-workflow/skills/independent-advisor/SKILL.md:23,185`; `grep` finds the script path in no other skill.
  - Background readability: the runner was started in the background with stderr to a file; the file was read at about 20 s, 65 s and 125 s while the runner was still running (it ended at 141 s). The three reads showed 1, 2 and 3 lines respectively — the probe closing line, then the 1m00s line, then the 2m00s line — so each line is readable as soon as it is written. (The snapshot header lines meant to label each read were dropped by zsh `print` treating `---` as an option; the read order and line counts are what is shown.)
  - Not done: no live agent session was run through a station to watch an agent actually relay the lines.
- Evidence: SKILL.md lines above; `live-snapshots.txt` contents reproduced in the transcript of this run.

## 4. The review result, its pass/fail status, the timeout behaviour and every existing outcome are unchanged, and the complete package suite passes.
- How I tried it: ran each of the five scenarios against HEAD and against the branch base f055b428 with the identical fake CLI, then compared the parsed stdout JSON and the exit codes; ran the runner's tests.
- What came back:
  | scenario | status / reason | exit HEAD / base | stdout JSON HEAD == base |
  |---|---|---|---|
  | quick | completed | 0 / 0 | identical |
  | long | completed | 0 / 0 | identical |
  | fail | failed, `review-exit-3: unknown error` | 1 / 1 | identical |
  | timeout | failed, `execution-timeout: 70s` | 1 / 1 | identical |
  | probetimeout | failed, `execution-timeout: 5s` | 1 / 1 | identical |
  Wall time per scenario was the same at HEAD and base (1, 141, 66, 71, 5 s): no step ended early. The base's stderr was empty in every scenario; HEAD's only addition is the `external-review:` lines.
  - Constraint check: `grep -e FAKE-CLI -e ACCEPTANCE-PACKET` over every HEAD stderr file found nothing — no packet or CLI text in the progress lines.
  - Tests: `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID python3 -m pytest -q -p no:cacheprovider loom-code/tests/test_external_review.py loom-code/tests/test_adversarial_external_review_progress.py` → `129 passed in 17.11s`.
  - Complete package suite: not run here by design. Command `python3 scripts/run_package_tests.py --loom-family`; it runs at finalize-review, which refuses the attestation if it fails. Build reported 2318 passed / 1 failed, the failure attributed to a sibling worktree named `loom-memory` beside the build worktree and passing 17/17 in a scratch worktree.
- Evidence: captured stdout/stderr/exit files per run; pytest output above.
