# An outside review shows that it is still running — plan
intent: 2026-10-19-external-review-progress-lines@a9361215
spec: docs/loom/2026-10-19-external-review-progress-lines/spec.md@3b203bf0
charter: 1.1

## Task DAG
Wave 1 — the runner's progress reporting, then the skill instruction with release metadata.

**W1-01 Progress and closing lines from the outside-review runner**  after: none  acceptance: 1, 2, 4
- Files: loom-code/scripts/external_review.py (entry: `_launch`), loom-code/tests/test_external_review.py
- Test: A1 positive: review_step_prints_progress_each_interval; negative: step_shorter_than_interval_prints_no_progress. A2 positive: closing_line_reports_longest_silence; boundary: timeout_prints_timed_out_closing_line. A4 positive: json_result_unchanged_with_progress; negative: discovery_prints_no_progress.
- Risk: agent-decided: no new thread; the wait loop wakes each interval, readers record line times, closing line follows the loop. `execute` passes the stage label; existing test_external_review.py cases preserved.

**W1-02 external-review skill relays progress; release 3.43.0**  after: W1-01  acceptance: 3, 4
- Files: loom-code/skills/external-review/SKILL.md, loom-code/tests/test_external_review.py, loom-code/plugin.json (+ .claude-plugin, .codex-plugin copies) + loom-code/package.json, loom-code/CHANGELOG.md, README.md + loom-code/README(.ja,.zh-TW).md + loom-code/tests/test_write_plan_station_text.py
- Test: A3 positive: execute_section_names_progress_relay; boundary: execute_section_still_names_one_json_result. A4 positive: test_current_release_metadata_is_synchronized at 3.43.0; negative: fails if any manifest stays 3.42.1.
- Risk: agent-decided minor bump because skill station guidance changes; host-neutral wording (keep the error stream visible, relay each line); no verbatim sentence pin.

**W1-03 Graduate the progress adversarial programs into the suite**  after: W1-01  acceptance: 4
- Files: loom-code/tests/test_adversarial_external_review_progress.py, docs/loom/2026-10-19-external-review-progress-lines/evidence/probes/
- Test: A4 positive: test_abuse_progress_closed_stderr keeps stdout pure JSON; negative: test_abuse_progress_broken_stderr keeps a completed review completed.
- Risk: agent-decided: move both red-then-green probes unchanged in behaviour so every later change runs them; the probe store keeps no copy.

## Simplicity check
- agent reports elapsed time itself with no code change — declined: cannot see time since last output or record longest silence, which the user asked for
- progress inside `_launch`'s wait loop instead of a separate ticker thread from `execute` — taken
- drop the list-candidates negative skill test — taken
- merge the release task into the skill task — taken

## Questions asked
① — what — 「這樣對嗎？」 (first restatement; the user asked for industry research before answering)
① — what — 「這樣對嗎？如果想維持 30 秒，直接說一聲就好。」 (revised to a 60-second interval after research; answered 「對」)

## Risks
1. Pipe buffering in a CLI can make "last output" look older than real work; the line reports what the runner received, never claims stuck.
2. second-vendor: suggest — availability notice given for codex; no grounded high-risk reason; not opted in.
